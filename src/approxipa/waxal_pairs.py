"""Utilities for WAXAL source access checks and split assignment."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PAIR_FIELDNAMES = [
    "word_a",
    "word_b",
    "tone_a",
    "tone_b",
    "meaning_a",
    "meaning_b",
    "gold_ipa_a",
    "gold_ipa_b",
    "source",
    "source_id",
    "source_split",
    "status",
    "notes",
]


def normalize_source(source: str) -> str:
    """Normalize a source label for comparisons."""
    return source.strip().lower()


def find_accessible_paths(paths: list[Path]) -> list[Path]:
    """Return existing local WAXAL candidate paths."""
    return [path for path in paths if path.exists()]


def _pair_key(row: dict[str, str]) -> str:
    """Build a stable key used to assign deterministic splits."""
    source_id = row.get("source_id", "").strip()
    if source_id:
        return source_id
    return "|".join(
        [
            row.get("word_a", "").strip(),
            row.get("word_b", "").strip(),
            row.get("gold_ipa_a", "").strip(),
            row.get("gold_ipa_b", "").strip(),
        ]
    )


def assign_split(key: str, construction_ratio: float = 0.8, salt: str = "waxal-v1") -> str:
    """Assign a deterministic split label using a hash bucket."""
    if not 0.0 < construction_ratio < 1.0:
        raise ValueError("construction_ratio must be in the open interval (0, 1)")

    digest = hashlib.sha256(f"{salt}:{key}".encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) / float(16**8)
    if bucket < construction_ratio:
        return "construction"
    return "evaluation"


def load_pairs(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    """Load pair rows and preserve source CSV column order."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
        existing_fieldnames = list(reader.fieldnames or [])
    return rows, existing_fieldnames


def apply_waxal_split(
    rows: list[dict[str, str]],
    construction_ratio: float = 0.8,
    salt: str = "waxal-v1",
) -> tuple[list[dict[str, str]], int]:
    """Assign source_split for WAXAL rows and return changed row count."""
    updated: list[dict[str, str]] = []
    changed = 0

    for row in rows:
        new_row = dict(row)
        source = normalize_source(new_row.get("source", ""))
        if source == "waxal":
            key = _pair_key(new_row)
            split = assign_split(key, construction_ratio=construction_ratio, salt=salt)
            if new_row.get("source_split", "").strip() != split:
                changed += 1
            new_row["source_split"] = split
        updated.append(new_row)

    return updated, changed


def build_output_fieldnames(existing_fieldnames: list[str]) -> list[str]:
    """Keep existing columns first and append missing recommended metadata fields."""
    output_fieldnames = list(existing_fieldnames)
    for fieldname in PAIR_FIELDNAMES:
        if fieldname not in output_fieldnames:
            output_fieldnames.append(fieldname)
    return output_fieldnames


def write_pairs(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    """Write pair rows to CSV with stable field order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({fieldname: row.get(fieldname, "") for fieldname in fieldnames})
