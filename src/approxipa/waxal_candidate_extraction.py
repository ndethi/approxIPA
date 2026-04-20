"""Candidate extraction utilities for local WAXAL Kikuyu parquet data."""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pyarrow.parquet as pq


WORD_PATTERN = re.compile(r"[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF']+")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
MAX_LISTED_UTTERANCE_IDS = 30
MAX_LISTED_SPEAKER_IDS = 10
MAX_SAMPLE_TEXT_CHARS = 180


@dataclass(frozen=True)
class WaxalWordCandidate:
    """A repeated lexical item observed across multiple WAXAL utterances."""

    word: str
    occurrence_count: int
    utterance_count: int
    speaker_count: int
    utterance_ids: tuple[str, ...]
    speaker_ids: tuple[str, ...]
    split_counts: tuple[str, ...]
    sample_texts: tuple[str, ...]
    utterance_ids_truncated: bool
    speaker_ids_truncated: bool


def _normalize_word(token: str) -> str:
    value = unicodedata.normalize("NFKC", token).strip().lower()
    return value.strip("'")


def load_stopwords(path: Path | None) -> set[str]:
    """Load newline-delimited stopwords if a file exists."""
    if path is None or not path.exists():
        return set()

    values: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        token = _normalize_word(line)
        if token and not token.startswith("#"):
            values.add(token)
    return values


def tokenize_words(text: str) -> list[str]:
    """Tokenize text into normalized lexical tokens."""
    clean_text = URL_PATTERN.sub(" ", text or "")
    tokens: list[str] = []
    for match in WORD_PATTERN.findall(clean_text):
        token = _normalize_word(match)
        if len(token) >= 3 and not token.startswith(("http", "www")):
            tokens.append(token)
    return tokens


def _compact_text(text: str) -> str:
    """Normalize whitespace and cap snippet length for CSV readability."""
    compact = " ".join((text or "").split())
    if len(compact) <= MAX_SAMPLE_TEXT_CHARS:
        return compact
    return compact[: MAX_SAMPLE_TEXT_CHARS - 1] + "…"


def load_rows_from_parquet(parquet_path: Path, split: str) -> list[dict[str, str]]:
    """Load minimal row fields required for lexical candidate mining."""
    table = pq.read_table(parquet_path, columns=["id", "speaker_id", "text", "locale"])
    rows: list[dict[str, str]] = []
    for row in table.to_pylist():
        rows.append(
            {
                "id": str(row.get("id", "")).strip(),
                "speaker_id": str(row.get("speaker_id", "")).strip(),
                "text": str(row.get("text", "")).strip(),
                "locale": str(row.get("locale", "")).strip().lower(),
                "split": split,
            }
        )
    return rows


def load_waxal_rows(data_dir: Path, splits: list[str]) -> list[dict[str, str]]:
    """Load rows from local split parquet files under data/waxal."""
    rows: list[dict[str, str]] = []
    for split in splits:
        parquet_path = data_dir / split / "0.parquet"
        if not parquet_path.exists():
            continue
        rows.extend(load_rows_from_parquet(parquet_path, split=split))
    return rows


def mine_word_candidates(
    rows: list[dict[str, str]],
    min_occurrences: int = 3,
    stopwords: set[str] | None = None,
    max_utterance_ratio: float = 0.2,
) -> list[WaxalWordCandidate]:
    """Mine repeated words from WAXAL rows for analyst review."""
    if not 0.0 < max_utterance_ratio <= 1.0:
        raise ValueError("max_utterance_ratio must be in (0, 1]")

    stopword_set = stopwords or set()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    kik_utterance_ids: set[str] = set()
    for row in rows:
        if row.get("locale") != "kik":
            continue
        utterance_id = row.get("id", "")
        if utterance_id:
            kik_utterance_ids.add(utterance_id)
        utterance_tokens = tokenize_words(row.get("text", ""))
        for token in utterance_tokens:
            if token in stopword_set:
                continue
            grouped[token].append(row)

    total_kik_utterances = max(1, len(kik_utterance_ids))

    candidates: list[WaxalWordCandidate] = []
    for word, items in grouped.items():
        if len(items) < min_occurrences:
            continue

        utterance_ids = tuple(sorted({item.get("id", "") for item in items if item.get("id", "")}))
        utterance_ratio = len(utterance_ids) / total_kik_utterances
        if utterance_ratio > max_utterance_ratio:
            continue

        speaker_ids = tuple(sorted({item.get("speaker_id", "") for item in items if item.get("speaker_id", "")}))

        split_counter: dict[str, int] = defaultdict(int)
        sample_texts: list[str] = []
        seen_texts: set[str] = set()
        for item in items:
            split = item.get("split", "")
            if split:
                split_counter[split] += 1
            text = item.get("text", "")
            if text and text not in seen_texts and len(sample_texts) < 3:
                seen_texts.add(text)
                sample_texts.append(_compact_text(text))

        candidates.append(
            WaxalWordCandidate(
                word=word,
                occurrence_count=len(items),
                utterance_count=len(utterance_ids),
                speaker_count=len(speaker_ids),
                utterance_ids=utterance_ids[:MAX_LISTED_UTTERANCE_IDS],
                speaker_ids=speaker_ids[:MAX_LISTED_SPEAKER_IDS],
                split_counts=tuple(f"{split}:{count}" for split, count in sorted(split_counter.items())),
                sample_texts=tuple(sample_texts),
                utterance_ids_truncated=len(utterance_ids) > MAX_LISTED_UTTERANCE_IDS,
                speaker_ids_truncated=len(speaker_ids) > MAX_LISTED_SPEAKER_IDS,
            )
        )

    return sorted(candidates, key=lambda item: (-item.occurrence_count, item.word))


def write_candidates_csv(path: Path, candidates: list[WaxalWordCandidate]) -> None:
    """Write mined lexical candidates to CSV for analyst filtering."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "word",
        "occurrence_count",
        "utterance_count",
        "speaker_count",
        "split_counts",
        "utterance_ids",
        "utterance_ids_truncated",
        "speaker_ids",
        "speaker_ids_truncated",
        "sample_texts",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "word": candidate.word,
                    "occurrence_count": str(candidate.occurrence_count),
                    "utterance_count": str(candidate.utterance_count),
                    "speaker_count": str(candidate.speaker_count),
                    "split_counts": " | ".join(candidate.split_counts),
                    "utterance_ids": " | ".join(candidate.utterance_ids),
                    "utterance_ids_truncated": str(candidate.utterance_ids_truncated).lower(),
                    "speaker_ids": " | ".join(candidate.speaker_ids),
                    "speaker_ids_truncated": str(candidate.speaker_ids_truncated).lower(),
                    "sample_texts": " || ".join(candidate.sample_texts),
                }
            )
