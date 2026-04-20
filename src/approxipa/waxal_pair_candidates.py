"""Build tonal-variant pair candidates from WAXAL lexical observations."""

from __future__ import annotations

import csv
import itertools
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .waxal_candidate_extraction import tokenize_words
from .waxal_pairs import assign_split


@dataclass(frozen=True)
class WaxalPairCandidate:
    """A candidate pair based on orthographic tonal variation."""

    word_a: str
    word_b: str
    base_form: str
    count_a: int
    count_b: int
    split_counts_a: tuple[str, ...]
    split_counts_b: tuple[str, ...]
    sample_ids_a: tuple[str, ...]
    sample_ids_b: tuple[str, ...]
    sample_text_a: str
    sample_text_b: str
    source_id: str
    source_split: str


def strip_diacritics(token: str) -> str:
    """Remove combining marks while preserving base letters."""
    normalized = unicodedata.normalize("NFD", token)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def _split_counts(items: list[dict[str, str]]) -> tuple[str, ...]:
    counter: dict[str, int] = defaultdict(int)
    for item in items:
        split = item.get("split", "")
        if split:
            counter[split] += 1
    return tuple(f"{split}:{count}" for split, count in sorted(counter.items()))


def _sample_ids(items: list[dict[str, str]], limit: int = 10) -> tuple[str, ...]:
    ids = sorted({item.get("id", "") for item in items if item.get("id", "")})
    return tuple(ids[:limit])


def _sample_text(items: list[dict[str, str]]) -> str:
    for item in items:
        text = " ".join(item.get("text", "").split())
        if text:
            return text[:180]
    return ""


def mine_pair_candidates(
    rows: list[dict[str, str]],
    stopwords: set[str] | None = None,
    min_variant_occurrences: int = 3,
    construction_ratio: float = 0.8,
    salt: str = "waxal-v1",
) -> list[WaxalPairCandidate]:
    """Mine pair candidates from variant forms sharing the same de-accented base."""
    stopword_set = stopwords or set()

    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        if row.get("locale") != "kik":
            continue
        for token in tokenize_words(row.get("text", "")):
            if token in stopword_set:
                continue
            base = strip_diacritics(token)
            if not base or base == token:
                continue
            grouped[base][token].append(row)

    results: list[WaxalPairCandidate] = []
    for base, variants in grouped.items():
        surviving = {variant: items for variant, items in variants.items() if len(items) >= min_variant_occurrences}
        if len(surviving) < 2:
            continue

        for word_a, word_b in itertools.combinations(sorted(surviving.keys()), 2):
            items_a = surviving[word_a]
            items_b = surviving[word_b]
            source_id = f"waxal:{base}:{word_a}:{word_b}"
            source_split = assign_split(source_id, construction_ratio=construction_ratio, salt=salt)

            results.append(
                WaxalPairCandidate(
                    word_a=word_a,
                    word_b=word_b,
                    base_form=base,
                    count_a=len(items_a),
                    count_b=len(items_b),
                    split_counts_a=_split_counts(items_a),
                    split_counts_b=_split_counts(items_b),
                    sample_ids_a=_sample_ids(items_a),
                    sample_ids_b=_sample_ids(items_b),
                    sample_text_a=_sample_text(items_a),
                    sample_text_b=_sample_text(items_b),
                    source_id=source_id,
                    source_split=source_split,
                )
            )

    return sorted(results, key=lambda item: (-min(item.count_a, item.count_b), item.base_form, item.word_a, item.word_b))


def write_pair_candidates_csv(path: Path, candidates: list[WaxalPairCandidate]) -> None:
    """Write pair candidates as a review-ready CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "word_a",
        "word_b",
        "base_form",
        "count_a",
        "count_b",
        "split_counts_a",
        "split_counts_b",
        "sample_ids_a",
        "sample_ids_b",
        "sample_text_a",
        "sample_text_b",
        "source",
        "source_id",
        "source_split",
        "status",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "word_a": candidate.word_a,
                    "word_b": candidate.word_b,
                    "base_form": candidate.base_form,
                    "count_a": str(candidate.count_a),
                    "count_b": str(candidate.count_b),
                    "split_counts_a": " | ".join(candidate.split_counts_a),
                    "split_counts_b": " | ".join(candidate.split_counts_b),
                    "sample_ids_a": " | ".join(candidate.sample_ids_a),
                    "sample_ids_b": " | ".join(candidate.sample_ids_b),
                    "sample_text_a": candidate.sample_text_a,
                    "sample_text_b": candidate.sample_text_b,
                    "source": "waxal",
                    "source_id": candidate.source_id,
                    "source_split": candidate.source_split,
                    "status": "candidate",
                    "notes": "auto-mined orthographic tonal-variant candidate; analyst verification required",
                }
            )
