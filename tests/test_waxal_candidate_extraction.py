"""Tests for WAXAL lexical candidate extraction."""

from __future__ import annotations

from approxipa.waxal_candidate_extraction import mine_word_candidates, tokenize_words


def test_tokenize_words_normalizes_case_and_apostrophes() -> None:
    """Tokenizer should normalize case and keep apostrophized forms."""
    tokens = tokenize_words("Njūkì nĩ mwega, NJŪKÌ na mũndũ's")
    assert "njūkì" in tokens
    assert "mũndũ's" in tokens


def test_mine_word_candidates_filters_by_occurrence_and_locale() -> None:
    """Mining should emit repeated Kikuyu tokens only."""
    rows = [
        {"id": "u1", "speaker_id": "s1", "text": "njūkì nĩ mwega", "locale": "kik", "split": "train"},
        {"id": "u2", "speaker_id": "s2", "text": "njūkì nĩ nduru", "locale": "kik", "split": "test"},
        {"id": "u3", "speaker_id": "s1", "text": "njūkì cia andū", "locale": "kik", "split": "validation"},
        {"id": "u4", "speaker_id": "s9", "text": "different token", "locale": "yor", "split": "train"},
    ]

    candidates = mine_word_candidates(rows, min_occurrences=3)

    assert len(candidates) == 1
    assert candidates[0].word == "njūkì"
    assert candidates[0].occurrence_count == 3
    assert set(candidates[0].split_counts) == {"test:1", "train:1", "validation:1"}
