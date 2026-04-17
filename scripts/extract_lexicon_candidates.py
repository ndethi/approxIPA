"""Generate a review-ready Kikuyu IPA candidate lexicon from approximation outputs."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.lexicon_extraction import extract_lexicon_candidates  # noqa: E402


def main() -> int:
    """Create a candidate lexicon CSV for analyst verification."""
    input_jsonl = PROJECT_ROOT / "data" / "ipa_approximations.jsonl"
    output_csv = PROJECT_ROOT / "data" / "lexicon" / "kikuyu_ipa_review_sheet.csv"

    count = extract_lexicon_candidates(input_jsonl, output_csv)
    print(f"[INFO] Wrote {count} candidate rows to {output_csv}")
    print("[INFO] Next step: analyst reviews rows with review_status=needs-analyst-review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
