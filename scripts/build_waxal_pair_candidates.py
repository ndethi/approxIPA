"""Build WAXAL tonal-variant pair candidates for analyst review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.waxal_candidate_extraction import load_stopwords, load_waxal_rows  # noqa: E402
from approxipa.waxal_pair_candidates import mine_pair_candidates, write_pair_candidates_csv  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for pair candidate generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=PROJECT_ROOT / "data" / "waxal")
    parser.add_argument("--splits", default="train,validation,test")
    parser.add_argument("--stopwords-file", type=Path, default=PROJECT_ROOT / "data" / "waxal" / "kikuyu_stopwords.txt")
    parser.add_argument("--min-variant-occurrences", type=int, default=3)
    parser.add_argument("--construction-ratio", type=float, default=0.8)
    parser.add_argument("--salt", default="waxal-v1")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "waxal" / "kikuyu_pair_candidates.csv",
    )
    args = parser.parse_args(argv)

    splits = [split.strip() for split in args.splits.split(",") if split.strip()]
    rows = load_waxal_rows(args.data_dir, splits=splits)
    stopwords = load_stopwords(args.stopwords_file)
    candidates = mine_pair_candidates(
        rows,
        stopwords=stopwords,
        min_variant_occurrences=args.min_variant_occurrences,
        construction_ratio=args.construction_ratio,
        salt=args.salt,
    )
    write_pair_candidates_csv(args.output, candidates)

    print(f"[INFO] Loaded {len(rows)} WAXAL rows from {args.data_dir}")
    print(f"[INFO] Loaded {len(stopwords)} stopwords from {args.stopwords_file}")
    print(f"[INFO] Mined {len(candidates)} pair candidates")
    print(f"[INFO] Pair candidate CSV written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
