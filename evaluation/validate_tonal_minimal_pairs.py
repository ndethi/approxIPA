"""Validate tonal minimal-pair datasets before TCPR evaluation."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from evaluation.tcpr import extract_tone_marks
else:
    from evaluation.tcpr import extract_tone_marks


TONE_MARK_PATTERN = re.compile(r"[\u0300\u0301\u0302\u0304]")


@dataclass(frozen=True)
class ValidationIssue:
    """A single row-level validation issue."""

    row_number: int
    message: str


def strip_tone_marks(value: str) -> str:
    """Remove tone diacritics from an IPA string."""
    return TONE_MARK_PATTERN.sub("", value)


def validate_row(row: dict[str, str], row_number: int) -> list[ValidationIssue]:
    """Validate one tonal minimal-pair row."""
    issues: list[ValidationIssue] = []

    status = row.get("status", "").strip().lower()
    is_candidate = status == "candidate"

    required_fields = [
        "word_a",
        "word_b",
        "source",
    ]

    if not is_candidate:
        required_fields.extend(["tone_a", "tone_b", "meaning_a", "meaning_b", "gold_ipa_a", "gold_ipa_b"])
    else:
        required_fields.extend(["source_id", "source_split"])

    for field in required_fields:
        if not row.get(field, "").strip():
            issues.append(ValidationIssue(row_number, f"missing value for {field}"))

    if row.get("word_a", "").strip() == row.get("word_b", "").strip():
        issues.append(ValidationIssue(row_number, "word_a and word_b must differ"))

    if not is_candidate:
        tone_a = row.get("tone_a", "").strip()
        tone_b = row.get("tone_b", "").strip()
        if tone_a == tone_b:
            issues.append(ValidationIssue(row_number, "tone_a and tone_b must differ"))

        ipa_a = row.get("gold_ipa_a", "").strip()
        ipa_b = row.get("gold_ipa_b", "").strip()
        if not ipa_a or not ipa_b:
            return issues

        if strip_tone_marks(ipa_a) != strip_tone_marks(ipa_b):
            issues.append(ValidationIssue(row_number, "segmental base differs after removing tone marks"))

        if extract_tone_marks(ipa_a) == extract_tone_marks(ipa_b):
            issues.append(ValidationIssue(row_number, "gold IPA tone marks do not differ"))

    source = row.get("source", "").strip().lower()
    source_split = row.get("source_split", "").strip().lower()
    if source == "waxal":
        if source_split not in {"construction", "evaluation"}:
            issues.append(
                ValidationIssue(
                    row_number,
                    "WAXAL rows must set source_split to construction or evaluation",
                )
            )

    return issues


def validate_file(path: Path) -> list[ValidationIssue]:
    """Validate every row in a tonal minimal-pair CSV file."""
    issues: list[ValidationIssue] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            issues.extend(validate_row(row, row_number))
    return issues


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for pair validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to tonal_minimal_pairs.csv")
    args = parser.parse_args(argv)

    issues = validate_file(args.path)
    if issues:
        for issue in issues:
            print(f"[ERROR] row {issue.row_number}: {issue.message}")
        print(f"[ERROR] validation failed with {len(issues)} issue(s)")
        return 1

    print(f"[INFO] validation passed for {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
