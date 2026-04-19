"""Tests for WAXAL pair source utilities."""

from __future__ import annotations

from pathlib import Path

from approxipa.waxal_pairs import (
    apply_waxal_split,
    assign_split,
    build_output_fieldnames,
    find_accessible_paths,
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
