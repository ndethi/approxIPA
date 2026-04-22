"""Promote fully annotated tonal candidate rows to evaluable status."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.waxal_pairs import build_output_fieldnames, load_pairs, promote_candidate_rows, write_pairs  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for promoting candidate rows after analyst annotation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pairs-csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "tonal_minimal_pairs.csv",
        help="Path to the tonal minimal-pairs CSV.",
    )
    parser.add_argument(
        "--source-filter",
        default="waxal",
        help="Only promote candidate rows from this source (empty string disables filtering).",
    )
    parser.add_argument(
        "--target-status",
        default="evaluable",
        help="Status value to assign promoted rows.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report promotion counts without writing changes.",
    )
    args = parser.parse_args(argv)

    rows, existing_fieldnames = load_pairs(args.pairs_csv)

    source_filter = args.source_filter.strip()
    if not source_filter:
        source_filter = None

    updated_rows, promoted, skipped_incomplete = promote_candidate_rows(
        rows,
        source_filter=source_filter,
        target_status=args.target_status,
    )

    if not args.dry_run:
        output_fieldnames = build_output_fieldnames(existing_fieldnames)
        write_pairs(args.pairs_csv, updated_rows, output_fieldnames)

    print(f"[INFO] Candidate rows scanned: {len(rows)}")
    print(f"[INFO] Promoted rows: {promoted}")
    print(f"[INFO] Skipped rows (incomplete/invalid): {skipped_incomplete}")
    if args.dry_run:
        print("[INFO] Dry run mode enabled; no file changes written")
    else:
        print(f"[INFO] Updated pair CSV: {args.pairs_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
