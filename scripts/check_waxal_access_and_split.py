"""Check WAXAL local access and apply deterministic pair split labels."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.waxal_pairs import (  # noqa: E402
    apply_waxal_split,
    build_output_fieldnames,
    find_accessible_paths,
    load_pairs,
    normalize_source,
    write_pairs,
)


def _default_waxal_paths() -> list[Path]:
    """Return default local paths where WAXAL assets are expected."""
    return [
        PROJECT_ROOT / "data" / "waxal",
        PROJECT_ROOT / "data" / "waxal" / "aligned.csv",
        PROJECT_ROOT / "data" / "waxal" / "aligned.tsv",
    ]


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for access checks and split assignment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pairs",
        type=Path,
        default=PROJECT_ROOT / "data" / "tonal_minimal_pairs.csv",
        help="Input tonal minimal pairs CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (defaults to input path)",
    )
    parser.add_argument(
        "--waxal-path",
        type=Path,
        action="append",
        default=[],
        help="Additional local path to check for WAXAL access (repeatable)",
    )
    parser.add_argument(
        "--construction-ratio",
        type=float,
        default=0.8,
        help="Share assigned to construction split (0<value<1)",
    )
    parser.add_argument(
        "--salt",
        type=str,
        default="waxal-v1",
        help="Salt string for deterministic split assignment",
    )
    args = parser.parse_args(argv)

    candidate_paths = _default_waxal_paths() + args.waxal_path
    accessible = find_accessible_paths(candidate_paths)
    if accessible:
        print("[INFO] WAXAL access: local path(s) found")
        for path in accessible:
            print(f"[INFO]   {path}")
    else:
        print("[WARN] WAXAL access: no local path found")
        print("[WARN] Checked paths:")
        for path in candidate_paths:
            print(f"[WARN]   {path}")

    rows, existing_fieldnames = load_pairs(args.pairs)
    waxal_rows = sum(1 for row in rows if normalize_source(row.get("source", "")) == "waxal")
    if waxal_rows == 0:
        print("[WARN] No WAXAL rows found in pair CSV (source=waxal)")

    split_rows, changed = apply_waxal_split(
        rows,
        construction_ratio=args.construction_ratio,
        salt=args.salt,
    )

    output_path = args.output or args.pairs
    output_fieldnames = build_output_fieldnames(existing_fieldnames)
    write_pairs(output_path, split_rows, output_fieldnames)

    print(f"[INFO] Pair file written: {output_path}")
    print(f"[INFO] WAXAL rows: {waxal_rows}; source_split values set/updated: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
