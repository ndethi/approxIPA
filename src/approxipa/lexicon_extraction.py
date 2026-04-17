"""Utilities for extracting candidate Kikuyu IPA lexicons from approximation outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def load_approximations(path: Path) -> list[dict[str, str]]:
    """Load approximation JSONL rows from disk."""
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append(
            {
                "word": str(row.get("word", "")).strip(),
                "ipa_yoruba": str(row.get("ipa_yoruba", "")).strip(),
                "ipa_swahili": str(row.get("ipa_swahili", "")).strip(),
            }
        )
    return [row for row in rows if row["word"]]


def build_candidate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build candidate rows for analyst review from approximation outputs."""
    candidates: list[dict[str, str]] = []
    for row in rows:
        ipa_yoruba = row["ipa_yoruba"]
        ipa_swahili = row["ipa_swahili"]
        agreement = ipa_yoruba == ipa_swahili and bool(ipa_yoruba)

        primary_candidate = ipa_yoruba or ipa_swahili
        alternate_candidate = "" if agreement else ipa_swahili
        status = "auto-accepted" if agreement else "needs-analyst-review"

        candidates.append(
            {
                "word": row["word"],
                "ipa_yoruba": ipa_yoruba,
                "ipa_swahili": ipa_swahili,
                "agreement": "yes" if agreement else "no",
                "primary_candidate_ipa": primary_candidate,
                "alternate_candidate_ipa": alternate_candidate,
                "approved_ipa": primary_candidate if agreement else "",
                "review_status": status,
                "reviewer_notes": "",
                "source": "transphone_yoruba_swahili",
            }
        )
    return candidates


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    """Write a CSV file with explicit field order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def extract_lexicon_candidates(input_jsonl: Path, output_csv: Path) -> int:
    """Extract candidate lexicon rows from approximation JSONL and write review CSV."""
    rows = load_approximations(input_jsonl)
    candidates = build_candidate_rows(rows)

    fieldnames = [
        "word",
        "ipa_yoruba",
        "ipa_swahili",
        "agreement",
        "primary_candidate_ipa",
        "alternate_candidate_ipa",
        "approved_ipa",
        "review_status",
        "reviewer_notes",
        "source",
    ]
    write_csv(output_csv, candidates, fieldnames)
    return len(candidates)
