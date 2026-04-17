"""Run TCPR evaluation from repository data artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from evaluation.tcpr import compute_tcpr
else:
    from evaluation.tcpr import compute_tcpr


def project_root() -> Path:
    """Return the repository root for this project."""
    return Path(__file__).resolve().parents[1]


def load_minimal_pairs(path: Path) -> list[dict[str, str]]:
    """Load tonal minimal pair rows from CSV."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_approximations(path: Path, field: str) -> dict[str, str]:
    """Load word->IPA lookup from JSONL approximation output."""
    lookup: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        lookup[row["word"]] = row[field]
    return lookup


def main() -> int:
    """Run TCPR for Yoruba and Swahili conditions and write a JSON summary."""
    root = project_root()
    pairs_path = root / "data" / "tonal_minimal_pairs.csv"
    approximations_path = root / "data" / "ipa_approximations.jsonl"
    results_path = root / "evaluation" / "results" / "tcpr_summary.json"

    pair_rows = load_minimal_pairs(pairs_path)
    yor_lookup = load_approximations(approximations_path, "ipa_yoruba")
    swh_lookup = load_approximations(approximations_path, "ipa_swahili")

    yor_result = compute_tcpr(pair_rows, yor_lookup)
    swh_result = compute_tcpr(pair_rows, swh_lookup)

    payload = {
        "yoruba": yor_result.__dict__,
        "swahili": swh_result.__dict__,
    }

    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("[INFO] TCPR summary written to", results_path)
    print("[INFO] Yoruba TCPR:", f"{yor_result.score:.3f}")
    print("[INFO] Swahili TCPR:", f"{swh_result.score:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
