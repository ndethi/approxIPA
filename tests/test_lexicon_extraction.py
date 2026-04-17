"""Tests for candidate lexicon extraction utilities."""

from __future__ import annotations

from pathlib import Path

from approxipa.lexicon_extraction import build_candidate_rows, extract_lexicon_candidates


def test_build_candidate_rows_marks_agreement_as_auto_accepted() -> None:
    """When both sources agree, candidate rows should auto-accept."""
    rows = [{"word": "w1", "ipa_yoruba": "a b", "ipa_swahili": "a b"}]

    candidates = build_candidate_rows(rows)

    assert candidates[0]["agreement"] == "yes"
    assert candidates[0]["review_status"] == "auto-accepted"
    assert candidates[0]["approved_ipa"] == "a b"
    assert candidates[0]["alternate_candidate_ipa"] == ""


def test_build_candidate_rows_marks_disagreement_for_review() -> None:
    """When sources differ, rows should be flagged for analyst review."""
    rows = [{"word": "w2", "ipa_yoruba": "a b", "ipa_swahili": "a c"}]

    candidates = build_candidate_rows(rows)

    assert candidates[0]["agreement"] == "no"
    assert candidates[0]["review_status"] == "needs-analyst-review"
    assert candidates[0]["approved_ipa"] == ""
    assert candidates[0]["alternate_candidate_ipa"] == "a c"


def test_extract_lexicon_candidates_writes_review_csv(tmp_path: Path) -> None:
    """Extraction should generate a review CSV with all expected rows."""
    input_jsonl = tmp_path / "ipa_approximations.jsonl"
    output_csv = tmp_path / "lexicon" / "kikuyu_ipa_review_sheet.csv"
    input_jsonl.write_text(
        "\n".join(
            [
                '{"word":"word1","ipa_yoruba":"w o r d","ipa_swahili":"w o r d"}',
                '{"word":"word2","ipa_yoruba":"w o r d","ipa_swahili":"w ɔ r d"}',
            ]
        ),
        encoding="utf-8",
    )

    count = extract_lexicon_candidates(input_jsonl, output_csv)

    assert count == 2
    content = output_csv.read_text(encoding="utf-8")
    assert "word,ipa_yoruba,ipa_swahili" in content
    assert "word1,w o r d,w o r d,yes" in content
    assert "word2,w o r d,w ɔ r d,no" in content
