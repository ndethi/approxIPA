"""Tests for the TCPR evaluation utilities."""

from __future__ import annotations

import pytest

from evaluation import tcpr


def test_extract_tone_marks_returns_ordered_marks() -> None:
    """Tone extraction should preserve the left-to-right diacritic order."""
    ipa = "a\u0301ma b\u0300"
    assert tcpr.extract_tone_marks(ipa) == ("\u0301", "\u0300")


def test_pair_contrast_preserved_when_relation_matches() -> None:
    """A contrasting gold pair should remain contrasting in approximation."""
    assert tcpr.pair_contrast_preserved(
        gold_a="a\u0301",
        gold_b="a\u0300",
        approx_a="o\u0301",
        approx_b="o\u0300",
    )


def test_pair_contrast_preserved_false_when_contrast_collapses() -> None:
    """If approximation collapses a gold contrast, the pair is not preserved."""
    assert not tcpr.pair_contrast_preserved(
        gold_a="a\u0301",
        gold_b="a\u0300",
        approx_a="o\u0301",
        approx_b="o\u0301",
    )


def test_compute_tcpr_returns_expected_counts_and_score() -> None:
    """TCPR should compute aggregate score and counts from evaluable pairs."""
    rows = [
        {
            "word_a": "w1",
            "word_b": "w2",
            "gold_ipa_a": "a\u0301",
            "gold_ipa_b": "a\u0300",
        },
        {
            "word_a": "w3",
            "word_b": "w4",
            "gold_ipa_a": "e\u0301",
            "gold_ipa_b": "e\u0300",
        },
    ]
    lookup = {
        "w1": "o\u0301",
        "w2": "o\u0300",  # preserved
        "w3": "u\u0301",
        "w4": "u\u0301",  # collapsed
    }

    result = tcpr.compute_tcpr(rows, lookup, n_bootstrap=200, seed=3)

    assert result.total_pairs == 2
    assert result.preserved_pairs == 1
    assert result.score == pytest.approx(0.5)
    assert 0.0 <= result.ci_lower <= result.ci_upper <= 1.0


def test_compute_tcpr_raises_for_no_evaluable_pairs() -> None:
    """TCPR should fail fast when no rows can be evaluated."""
    with pytest.raises(ValueError):
        tcpr.compute_tcpr(
            pair_rows=[
                {
                    "word_a": "missing_a",
                    "word_b": "missing_b",
                    "gold_ipa_a": "a\u0301",
                    "gold_ipa_b": "a\u0300",
                }
            ],
            approx_lookup={},
            n_bootstrap=20,
        )
