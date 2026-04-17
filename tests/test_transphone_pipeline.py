"""Tests for the Transphone approximation pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from approxipa import transphone_pipeline as pipeline


def test_load_words_skips_blank_lines(tmp_path: Path) -> None:
    """Blank lines should be ignored when loading the word list."""
    wordlist = tmp_path / "kikuyu_wordlist.txt"
    wordlist.write_text("word1\n\n word2 \n\t\nword3\n", encoding="utf-8")

    assert pipeline.load_words(wordlist) == ["word1", "word2", "word3"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("  IPA  ", "IPA"),
        (["a", "b", "c"], "a b c"),
        (("a", "", "c"), "a c"),
    ],
)
def test_normalize_transphone_output(value, expected) -> None:
    """Transphone outputs should normalize to a stable string."""
    assert pipeline.normalize_transphone_output(value) == expected


def test_run_pipeline_writes_jsonl_and_returns_summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The pipeline should write JSONL records and compute summary counts."""
    input_path = tmp_path / "kikuyu_wordlist.txt"
    output_path = tmp_path / "ipa_approximations.jsonl"
    input_path.write_text("alpha\nbeta\n", encoding="utf-8")

    def fake_approximate_word(word: str, source_language: str, target_language: str = "kik") -> str:
        del target_language
        if source_language == "yor":
            return f"{word}-yor"
        return f"{word}-swh" if word == "beta" else f"{word}-yor"

    monkeypatch.setattr(pipeline, "approximate_word", fake_approximate_word)

    total_words, differing_words, elapsed_seconds = pipeline.run_pipeline(input_path, output_path)

    assert total_words == 2
    assert differing_words == 1
    assert elapsed_seconds >= 0

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in lines] == [
        {"word": "alpha", "ipa_yoruba": "alpha-yor", "ipa_swahili": "alpha-yor"},
        {"word": "beta", "ipa_yoruba": "beta-yor", "ipa_swahili": "beta-swh"},
    ]


def test_load_words_missing_file_raises(tmp_path: Path) -> None:
    """A missing input file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        pipeline.load_words(tmp_path / "missing.txt")