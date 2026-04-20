"""Tests for WAXAL pair candidate mining."""

from __future__ import annotations

from approxipa.waxal_pair_candidates import mine_pair_candidates, strip_diacritics


def test_strip_diacritics_normalizes_variant_bases() -> None:
    """Diacritic stripping should align variant forms to one base."""
    assert strip_diacritics("mũndũ") == "mundu"


def test_mine_pair_candidates_builds_construction_or_evaluation_rows() -> None:
    """Variant forms sharing a base should produce pair candidates with split assignment."""
    # Use more repetitions to ensure variants meet thresholds and aren't filtered
    rows = [
        {"id": "u1", "speaker_id": "s1", "text": "mũndũ arĩa", "locale": "kik", "split": "train"},
        {"id": "u2", "speaker_id": "s2", "text": "mundu nĩwe", "locale": "kik", "split": "test"},
        {"id": "u3", "speaker_id": "s2", "text": "mũndũ nĩwe", "locale": "kik", "split": "validation"},
        {"id": "u4", "speaker_id": "s3", "text": "mundu agĩkũra", "locale": "kik", "split": "train"},
        {"id": "u5", "speaker_id": "s1", "text": "mũndũ gitwa", "locale": "kik", "split": "train"},
        {"id": "u6", "speaker_id": "s3", "text": "mundu rĩa", "locale": "kik", "split": "test"},
    ]

    candidates = mine_pair_candidates(rows, min_variant_occurrences=2)

    assert len(candidates) >= 1, f"Expected at least 1 candidate, got {len(candidates)}"
    # Find the mundu/mũndũ pair if it exists
    pair = None
    for candidate in candidates:
        if candidate.base_form == "mundu" and {candidate.word_a, candidate.word_b} == {"mundu", "mũndũ"}:
            pair = candidate
            break
    
    assert pair is not None, f"Expected mundu/mũndũ pair,got {[(c.base_form, c.word_a, c.word_b) for c in candidates]}"
    assert pair.source_id.startswith("waxal:mundu:")
    assert pair.source_split in {"construction", "evaluation"}
