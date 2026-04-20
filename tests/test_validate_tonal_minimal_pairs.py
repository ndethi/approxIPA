"""Tests for tonal minimal-pair dataset validation."""

from __future__ import annotations

from pathlib import Path

from evaluation.validate_tonal_minimal_pairs import validate_file, validate_row


def test_validate_row_accepts_well_formed_pair() -> None:
    """A structurally correct minimal pair should pass validation."""
    row = {
        "word_a": "word1",
        "word_b": "word2",
        "tone_a": "H",
        "tone_b": "L",
        "meaning_a": "meaning a",
        "meaning_b": "meaning b",
        "gold_ipa_a": "wo\u0301rd",
        "gold_ipa_b": "wo\u0300rd",
        "source": "bibletts",
        "source_split": "",
    }

    assert validate_row(row, 2) == []


def test_validate_row_flags_same_tone_and_segmental_mismatch() -> None:
    """Validation should flag rows that do not form a true tonal minimal pair."""
    row = {
        "word_a": "word1",
        "word_b": "word1",
        "tone_a": "H",
        "tone_b": "H",
        "meaning_a": "meaning a",
        "meaning_b": "meaning b",
        "gold_ipa_a": "wo\u0301rd",
        "gold_ipa_b": "ward",
        "source": "waxal",
        "source_split": "",
    }

    issues = validate_row(row, 3)

    assert any("word_a and word_b must differ" in issue.message for issue in issues)
    assert any("tone_a and tone_b must differ" in issue.message for issue in issues)
    assert any("segmental base differs" in issue.message for issue in issues)
    assert any("WAXAL rows must set source_split" in issue.message for issue in issues)


def test_validate_file_accepts_seed_dataset(tmp_path: Path) -> None:
    """The current seed dataset should remain structurally valid."""
    csv_path = tmp_path / "tonal_minimal_pairs.csv"
    csv_path.write_text(
        "word_a,word_b,tone_a,tone_b,meaning_a,meaning_b,gold_ipa_a,gold_ipa_b,source,source_split\n"
        "word1,word2,H,L,meaning a,meaning b,wórd,wòrd,bibletts,\n"
        "word2,word3,H,L,meaning c,meaning d,wórd,wòrd,waxal,construction\n",
        encoding="utf-8",
    )

    assert validate_file(csv_path) == []


def test_validate_row_accepts_candidate_with_provenance_only() -> None:
    """Candidate rows may omit tone/IPA while awaiting analyst annotation."""
    row = {
        "word_a": "mũndũ",
        "word_b": "mundu",
        "tone_a": "",
        "tone_b": "",
        "meaning_a": "",
        "meaning_b": "",
        "gold_ipa_a": "",
        "gold_ipa_b": "",
        "source": "waxal",
        "source_id": "waxal:mundu:mundu:mũndũ",
        "source_split": "construction",
        "status": "candidate",
    }

    assert validate_row(row, 4) == []
