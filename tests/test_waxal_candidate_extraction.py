"""Tests for WAXAL lexical candidate extraction."""

from __future__ import annotations

from approxipa.waxal_candidate_extraction import mine_word_candidates, tokenize_words


def test_tokenize_words_normalizes_case_and_apostrophes() -> None:
    """Tokenizer should normalize case and keep apostrophized forms."""
    tokens = tokenize_words("Njūkì nĩ mwega, NJŪKÌ na mũndũ's")
    assert "njūkì" in tokens
    assert "mũndũ's" in tokens


def test_tokenize_words_drops_url_tokens() -> None:
    """Tokenizer should drop URL fragments from lexical candidates."""
    tokens = tokenize_words("see https://example.com/path and www.test.org now")
    assert "https" not in tokens
    assert "www" not in tokens


def test_mine_word_candidates_filters_by_occurrence_and_locale() -> None:
    """Mining should emit repeated Kikuyu tokens only."""
    rows = [
        {"id": "u1", "speaker_id": "s1", "text": "njūkì nĩ mwega", "locale": "kik", "split": "train"},
        {"id": "u2", "speaker_id": "s2", "text": "njūkì nĩ nduru", "locale": "kik", "split": "test"},
        {"id": "u3", "speaker_id": "s1", "text": "njūkì cia andū", "locale": "kik", "split": "validation"},
        {"id": "u4", "speaker_id": "s9", "text": "different token", "locale": "yor", "split": "train"},
    ]

    candidates = mine_word_candidates(rows, min_occurrences=3, max_utterance_ratio=1.0)

    assert len(candidates) == 1
    assert candidates[0].word == "njūkì"
    assert candidates[0].occurrence_count == 3
    assert set(candidates[0].split_counts) == {"test:1", "train:1", "validation:1"}


def test_mine_word_candidates_applies_stopwords_and_ratio_filter() -> None:
    """Stopwords and max utterance ratio should reduce high-function tokens."""
    rows = [
        {"id": "u1", "speaker_id": "s1", "text": "na ndũrĩ", "locale": "kik", "split": "train"},
        {"id": "u2", "speaker_id": "s1", "text": "na andũ", "locale": "kik", "split": "train"},
        {"id": "u3", "speaker_id": "s1", "text": "na njūkì", "locale": "kik", "split": "train"},
        {"id": "u4", "speaker_id": "s2", "text": "na ndũrĩ", "locale": "kik", "split": "test"},
    ]

    candidates = mine_word_candidates(
        rows,
        min_occurrences=2,
        stopwords={"na"},
        max_utterance_ratio=0.75,
    )

    words = [candidate.word for candidate in candidates]
    assert "na" not in words
    assert "ndũrĩ" in words
