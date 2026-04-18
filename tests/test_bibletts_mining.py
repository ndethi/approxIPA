"""Tests for BibleTTS candidate mining utilities."""

from __future__ import annotations

from pathlib import Path

from approxipa.bibletts_mining import load_aligned_rows, mine_repeated_words, write_candidates_csv


def test_mine_repeated_words_groups_by_lexeme() -> None:
    """Repeated aligned words should be grouped into a candidate record."""
    rows = [
        {"utterance_id": "u1", "word": "ngug", "orthography": "ngug", "f0_mean": "120", "source_sentence": "s1"},
        {"utterance_id": "u2", "word": "ngug", "orthography": "ngug", "f0_mean": "150", "source_sentence": "s2"},
        {"utterance_id": "u3", "word": "other", "orthography": "other", "f0_mean": "100", "source_sentence": "s3"},
    ]

    candidates = mine_repeated_words(rows)

    assert len(candidates) == 1
    assert candidates[0].word == "ngug"
    assert candidates[0].source_sentence_count == 2
    assert candidates[0].utterance_ids == ("u1", "u2")


def test_load_aligned_rows_reads_csv(tmp_path: Path) -> None:
    """The loader should read aligned rows from a CSV export."""
    path = tmp_path / "aligned.csv"
    path.write_text(
        "utterance_id,word,orthography,f0_mean,source_sentence\n"
        "u1,ngug,ngug,120,s1\n"
        "u2,ngug,ngug,150,s2\n",
        encoding="utf-8",
    )

    rows = load_aligned_rows(path)

    assert len(rows) == 2
    assert rows[0]["word"] == "ngug"


def test_write_candidates_csv_round_trips(tmp_path: Path) -> None:
    """Candidate groups should be written to a review CSV."""
    candidates = mine_repeated_words(
        [
            {"utterance_id": "u1", "word": "ngug", "orthography": "ngug", "f0_mean": "120", "source_sentence": "s1"},
            {"utterance_id": "u2", "word": "ngug", "orthography": "ngug", "f0_mean": "150", "source_sentence": "s2"},
        ]
    )
    output = tmp_path / "candidate_pairs.csv"

    write_candidates_csv(output, candidates)

    content = output.read_text(encoding="utf-8")
    assert "word,utterance_ids,orthographies,f0_means,source_sentence_count" in content
    assert "ngug" in content
