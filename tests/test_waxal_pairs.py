"""Tests for WAXAL pair source utilities."""

from __future__ import annotations

from pathlib import Path

from approxipa.waxal_pairs import (
    apply_waxal_split,
    assign_split,
    build_output_fieldnames,
    find_accessible_paths,
    promote_candidate_rows,
)


def test_assign_split_is_deterministic() -> None:
    """The same key and salt should always produce the same split."""
    split_one = assign_split("u123", construction_ratio=0.8, salt="fixed")
    split_two = assign_split("u123", construction_ratio=0.8, salt="fixed")
    assert split_one == split_two
    assert split_one in {"construction", "evaluation"}


def test_apply_waxal_split_updates_only_waxal_rows() -> None:
    """Only rows with source=WAXAL should receive split labels."""
    rows = [
        {
            "word_a": "w1",
            "word_b": "w2",
            "gold_ipa_a": "wo\u0301rd",
            "gold_ipa_b": "wo\u0300rd",
            "source": "waxal",
            "source_id": "utt-1",
            "source_split": "",
        },
        {
            "word_a": "w3",
            "word_b": "w4",
            "gold_ipa_a": "wo\u0301rd",
            "gold_ipa_b": "wo\u0300rd",
            "source": "bibletts",
            "source_id": "utt-2",
            "source_split": "",
        },
    ]

    split_rows, changed = apply_waxal_split(rows, construction_ratio=0.5, salt="fixed")

    assert changed == 1
    assert split_rows[0]["source_split"] in {"construction", "evaluation"}
    assert split_rows[1]["source_split"] == ""


def test_find_accessible_paths_filters_existing(tmp_path: Path) -> None:
    """Only existing paths should be returned by access checks."""
    existing = tmp_path / "waxal"
    existing.mkdir()
    missing = tmp_path / "missing"

    found = find_accessible_paths([existing, missing])
    assert found == [existing]


def test_build_output_fieldnames_appends_missing_metadata() -> None:
    """Metadata fields should be appended without dropping existing columns."""
    output = build_output_fieldnames(["word_a", "word_b", "gold_ipa_a", "gold_ipa_b"])
    assert output[:4] == ["word_a", "word_b", "gold_ipa_a", "gold_ipa_b"]
    assert "source" in output
    assert "source_split" in output


def test_promote_candidate_rows_promotes_only_complete_candidate_rows() -> None:
    """Only complete candidate rows should be promoted to evaluable."""
    rows = [
        {
            "word_a": "mũndũ",
            "word_b": "mundu",
            "tone_a": "H",
            "tone_b": "L",
            "meaning_a": "person",
            "meaning_b": "person",
            "gold_ipa_a": "mu\u0301ndu",
            "gold_ipa_b": "mu\u0300ndu",
            "source": "waxal",
            "status": "candidate",
        },
        {
            "word_a": "kura",
            "word_b": "kura",
            "tone_a": "H",
            "tone_b": "L",
            "meaning_a": "x",
            "meaning_b": "y",
            "gold_ipa_a": "ku\u0301ra",
            "gold_ipa_b": "ku\u0300ra",
            "source": "waxal",
            "status": "candidate",
        },
        {
            "word_a": "tha",
            "word_b": "tha",
            "tone_a": "",
            "tone_b": "",
            "meaning_a": "",
            "meaning_b": "",
            "gold_ipa_a": "",
            "gold_ipa_b": "",
            "source": "waxal",
            "status": "candidate",
        },
        {
            "word_a": "guku",
            "word_b": "guku",
            "tone_a": "H",
            "tone_b": "L",
            "meaning_a": "here",
            "meaning_b": "here",
            "gold_ipa_a": "gu\u0301ku",
            "gold_ipa_b": "gu\u0300ku",
            "source": "bibletts",
            "status": "candidate",
        },
    ]

    updated, promoted, skipped = promote_candidate_rows(rows)

    assert promoted == 1
    assert skipped == 2
    assert updated[0]["status"] == "evaluable"
    assert updated[1]["status"] == "candidate"
    assert updated[2]["status"] == "candidate"
    assert updated[3]["status"] == "candidate"


def test_promote_candidate_rows_allows_disabling_source_filter() -> None:
    """An empty source filter should promote complete candidates from any source."""
    rows = [
        {
            "word_a": "guku",
            "word_b": "gũkũ",
            "tone_a": "H",
            "tone_b": "L",
            "meaning_a": "here",
            "meaning_b": "here",
            "gold_ipa_a": "gu\u0301ku",
            "gold_ipa_b": "gu\u0300ku",
            "source": "bibletts",
            "status": "candidate",
        }
    ]

    updated, promoted, skipped = promote_candidate_rows(rows, source_filter=None)

    assert promoted == 1
    assert skipped == 0
    assert updated[0]["status"] == "evaluable"
