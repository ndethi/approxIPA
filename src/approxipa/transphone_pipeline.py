"""Transphone-based IPA approximation pipeline."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Iterable


def project_root() -> Path:
    """Return the repository root for the approxIPA project."""
    return Path(__file__).resolve().parents[2]


def load_words(input_path: Path) -> list[str]:
    """Load non-empty words from a newline-delimited word list."""
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    words: list[str] = []
    for raw_line in input_path.read_text(encoding="utf-8").splitlines():
        word = raw_line.strip()
        if word:
            words.append(word)
    return words


def normalize_transphone_output(value: Any) -> str:
    """Convert a Transphone result into a stable string representation."""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return " ".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def approximate_word(word: str, source_language: str, target_language: str = "kik") -> str:
    """Approximate one word with Transphone using the requested source language."""
    try:
        from transphone import read_tokenizer
    except ImportError as exc:  # pragma: no cover - dependency error path
        raise RuntimeError("transphone is not installed") from exc

    del target_language
    model = read_tokenizer(source_language)
    result = model.tokenize(word)
    return normalize_transphone_output(result)


def write_jsonl(records: Iterable[dict[str, Any]], output_path: Path) -> None:
    """Write dictionaries to JSONL, one record per line."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")


def run_pipeline(input_path: Path, output_path: Path) -> tuple[int, int, float]:
    """Run the full approximation pipeline and return summary statistics."""
    started_at = time.perf_counter()
    words = load_words(input_path)
    records: list[dict[str, Any]] = []
    differing_words = 0

    for word in words:
        ipa_yoruba = approximate_word(word, "yor")
        ipa_swahili = approximate_word(word, "swh")
        if ipa_yoruba != ipa_swahili:
            differing_words += 1
        records.append(
            {
                "word": word,
                "ipa_yoruba": ipa_yoruba,
                "ipa_swahili": ipa_swahili,
            }
        )

    write_jsonl(records, output_path)
    elapsed_seconds = time.perf_counter() - started_at
    return len(words), differing_words, elapsed_seconds


def main() -> int:
    """Execute the pipeline using the repository data paths."""
    input_path = project_root() / "data" / "kikuyu_wordlist.txt"
    output_path = project_root() / "data" / "ipa_approximations.jsonl"

    try:
        total_words, differing_words, elapsed_seconds = run_pipeline(input_path, output_path)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 1
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        return 1
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"[ERROR] Unexpected failure: {exc}")
        return 1

    print(
        f"[INFO] Processed {total_words} words; {differing_words} differed; "
        f"elapsed {elapsed_seconds:.2f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())