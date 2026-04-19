"""Tests for WAXAL Hugging Face ingestion utilities."""

from __future__ import annotations

from pathlib import Path

from approxipa.waxal_ingestion import build_access_report, config_urls, write_json


def test_config_urls_extracts_selected_splits() -> None:
    """The helper should select URLs for requested splits only."""
    manifest = {
        "kik_tts": {
            "train": ["https://example/train-0.parquet"],
            "validation": ["https://example/validation-0.parquet"],
            "test": ["https://example/test-0.parquet"],
        }
    }

    urls = config_urls(manifest, "kik_tts", splits=["train", "test"])

    assert set(urls.keys()) == {"train", "test"}
    assert urls["train"] == ["https://example/train-0.parquet"]
    assert urls["test"] == ["https://example/test-0.parquet"]


def test_build_access_report_counts_downloads(tmp_path: Path) -> None:
    """The access report should include split counts and downloaded path count."""
    split_urls = {"train": ["u1", "u2"], "test": ["u3"]}
    downloaded = [tmp_path / "train" / "0.parquet"]

    report = build_access_report("google/WaxalNLP", "kik_tts", split_urls, downloaded)

    assert report["dataset_id"] == "google/WaxalNLP"
    assert report["config"] == "kik_tts"
    assert report["splits"] == {"train": 2, "test": 1}
    assert report["downloaded_file_count"] == 1


def test_write_json_is_deterministic(tmp_path: Path) -> None:
    """JSON helper should write a readable payload with trailing newline."""
    path = tmp_path / "payload.json"
    payload = {"b": 2, "a": 1}

    write_json(path, payload)

    content = path.read_text(encoding="utf-8")
    assert '"a": 1' in content
    assert content.endswith("\n")
