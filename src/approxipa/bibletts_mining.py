"""BibleTTS candidate mining utilities for tonal pair construction."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BibleTTSCandidate:
    """A repeatable BibleTTS lexical candidate for tonal pair review."""

    word: str
    utterance_ids: tuple[str, ...]
    orthographies: tuple[str, ...]
    f0_means: tuple[str, ...]
    source_sentence_count: int


def load_aligned_rows(path: Path) -> list[dict[str, str]]:
    """Load aligned BibleTTS rows from CSV or TSV."""
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        return [dict(row) for row in reader]


def mine_repeated_words(rows: list[dict[str, str]]) -> list[BibleTTSCandidate]:
    """Group repeated orthographic words across BibleTTS aligned rows."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        word = row.get("word", "").strip().lower()
        if word:
            grouped[word].append(row)

    candidates: list[BibleTTSCandidate] = []
    for word, items in grouped.items():
        if len(items) < 2:
            continue

        candidates.append(
            BibleTTSCandidate(
                word=word,
                utterance_ids=tuple(item.get("utterance_id", "").strip() for item in items if item.get("utterance_id", "").strip()),
                orthographies=tuple(item.get("orthography", word).strip() for item in items),
                f0_means=tuple(item.get("f0_mean", "").strip() for item in items if item.get("f0_mean", "").strip()),
                source_sentence_count=len({item.get("source_sentence", "").strip() for item in items if item.get("source_sentence", "").strip()}),
            )
        )

    return candidates


def write_candidates_csv(path: Path, candidates: list[BibleTTSCandidate]) -> None:
    """Write mined BibleTTS candidate groups to CSV for review."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["word", "utterance_ids", "orthographies", "f0_means", "source_sentence_count"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "word": candidate.word,
                    "utterance_ids": " | ".join(candidate.utterance_ids),
                    "orthographies": " | ".join(candidate.orthographies),
                    "f0_means": " | ".join(candidate.f0_means),
                    "source_sentence_count": str(candidate.source_sentence_count),
                }
            )
