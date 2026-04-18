"""Mine BibleTTS tonal pair candidates from aligned transcript exports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.bibletts_mining import load_aligned_rows, mine_repeated_words, write_candidates_csv  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    """Mine repeated BibleTTS lexical items for tonal pair review."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path, help="Aligned BibleTTS CSV/TSV export")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "bibletts" / "candidate_pairs.csv",
        help="Output CSV for candidate review rows",
    )
    args = parser.parse_args(argv)

    rows = load_aligned_rows(args.input_path)
    candidates = mine_repeated_words(rows)
    write_candidates_csv(args.output, candidates)

    print(f"[INFO] Mined {len(candidates)} repeated-word candidates from {args.input_path}")
    print(f"[INFO] Review sheet written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
