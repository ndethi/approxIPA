"""Bridge WAXAL pair candidates into tonal_minimal_pairs.csv as review rows."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.waxal_pairs import build_output_fieldnames, load_pairs, write_pairs  # noqa: E402


def load_candidate_rows(path: Path) -> list[dict[str, str]]:
    """Load pair candidate rows from CSV."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for bridging candidate rows into tonal pair CSV."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate-csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "waxal" / "kikuyu_pair_candidates.csv",
    )
    parser.add_argument(
        "--pairs-csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "tonal_minimal_pairs.csv",
    )
    parser.add_argument("--max-new", type=int, default=100)
    parser.add_argument(
        "--require-construction",
        action="store_true",
        help="Only import candidates with source_split=construction",
    )
    args = parser.parse_args(argv)

    candidate_rows = load_candidate_rows(args.candidate_csv)
    pair_rows, existing_fieldnames = load_pairs(args.pairs_csv)

    existing_source_ids = {row.get("source_id", "").strip() for row in pair_rows if row.get("source_id", "").strip()}
    added = 0
    skipped_split = 0
    skipped_duplicate = 0

    for row in candidate_rows:
        if added >= args.max_new:
            break

        source_id = row.get("source_id", "").strip()
        source_split = row.get("source_split", "").strip().lower()
        if not source_id:
            continue

        if args.require_construction and source_split != "construction":
            skipped_split += 1
            continue

        if source_id in existing_source_ids:
            skipped_duplicate += 1
            continue

        pair_rows.append(
            {
                "word_a": row.get("word_a", "").strip(),
                "word_b": row.get("word_b", "").strip(),
                "tone_a": "",
                "tone_b": "",
                "meaning_a": "",
                "meaning_b": "",
                "gold_ipa_a": "",
                "gold_ipa_b": "",
                "source": "waxal",
                "source_id": source_id,
                "source_split": source_split,
                "status": "candidate",
                "notes": "imported from waxal pair candidates; analyst tone+IPA annotation required",
            }
        )
        existing_source_ids.add(source_id)
        added += 1

    output_fieldnames = build_output_fieldnames(existing_fieldnames)
    write_pairs(args.pairs_csv, pair_rows, output_fieldnames)

    print(f"[INFO] Candidate rows loaded: {len(candidate_rows)}")
    print(f"[INFO] Added rows: {added}")
    print(f"[INFO] Skipped (split policy): {skipped_split}")
    print(f"[INFO] Skipped (duplicate source_id): {skipped_duplicate}")
    print(f"[INFO] Updated pair CSV: {args.pairs_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
