"""Extract first-pass Kikuyu lexical candidates from local WAXAL parquet files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.waxal_candidate_extraction import (  # noqa: E402
    load_waxal_rows,
    mine_word_candidates,
    write_candidates_csv,
)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for WAXAL word-level candidate extraction."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "waxal",
        help="Directory containing split parquet files under train/validation/test",
    )
    parser.add_argument(
        "--splits",
        default="train,validation,test",
        help="Comma-separated local split directories to include",
    )
    parser.add_argument(
        "--min-occurrences",
        type=int,
        default=3,
        help="Minimum token occurrence count required to emit a candidate",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "waxal" / "kikuyu_candidate_words.csv",
        help="Output CSV for candidate words",
    )
    args = parser.parse_args(argv)

    splits = [split.strip() for split in args.splits.split(",") if split.strip()]
    rows = load_waxal_rows(args.data_dir, splits=splits)
    candidates = mine_word_candidates(rows, min_occurrences=args.min_occurrences)
    write_candidates_csv(args.output, candidates)

    print(f"[INFO] Loaded {len(rows)} WAXAL rows from {args.data_dir}")
    print(f"[INFO] Mined {len(candidates)} lexical candidates with min_occurrences={args.min_occurrences}")
    print(f"[INFO] Candidate CSV written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
