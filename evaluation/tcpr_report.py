"""Generate a paper-friendly summary for TCPR evaluation results."""

from __future__ import annotations

import json
from pathlib import Path


def project_root() -> Path:
    """Return the repository root for this project."""
    return Path(__file__).resolve().parents[1]


def load_tcpr_summary(path: Path) -> dict[str, object]:
    """Load the JSON summary written by the TCPR runner."""
    return json.loads(path.read_text(encoding="utf-8"))


def format_row(label: str, result: dict[str, object], threshold: float) -> str:
    """Format one condition as a compact markdown table row."""
    score = float(result["score"])
    ci_lower = float(result["ci_lower"])
    ci_upper = float(result["ci_upper"])
    preserved_pairs = int(result["preserved_pairs"])
    total_pairs = int(result["total_pairs"])
    margin = score - threshold
    return (
        f"| {label} | {score:.3f} | {ci_lower:.3f} | {ci_upper:.3f} | "
        f"{preserved_pairs}/{total_pairs} | {margin:+.3f} |"
    )


def build_markdown_summary(summary: dict[str, object]) -> str:
    """Build a markdown report from a summary payload."""
    config = summary["config"]
    threshold = float(config["practical_use_threshold"])

    lines = [
        "# TCPR Summary",
        "",
        f"Practical-use threshold: {threshold:.3f}",
        "",
        "| Condition | Score | CI low | CI high | Preserved | Margin vs threshold |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        format_row("Yoruba", summary["yoruba"], threshold),
        format_row("Swahili", summary["swahili"], threshold),
        "",
        "Interpretation: positive margin would support the practical usability target; negative margin indicates the current result is still a baseline sanity check.",
    ]
    return "\n".join(lines)


def main() -> int:
    """Print a markdown summary of the latest TCPR run."""
    root = project_root()
    summary_path = root / "evaluation" / "results" / "tcpr_summary.json"
    summary = load_tcpr_summary(summary_path)
    print(build_markdown_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
