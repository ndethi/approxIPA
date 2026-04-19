"""Ingestion helpers for WAXAL data hosted on Hugging Face."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path


def fetch_parquet_manifest(dataset_id: str) -> dict[str, dict[str, list[str]]]:
    """Fetch the parquet file manifest for a Hugging Face dataset."""
    url = f"https://huggingface.co/api/datasets/{dataset_id}/parquet"
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError(f"Unexpected parquet payload type: {type(payload).__name__}")
    return payload


def config_urls(
    manifest: dict[str, dict[str, list[str]]],
    config_name: str,
    splits: list[str] | None = None,
) -> dict[str, list[str]]:
    """Extract split->url mapping for a specific dataset config."""
    if config_name not in manifest:
        available = ", ".join(sorted(manifest.keys()))
        raise KeyError(f"Config {config_name!r} not found. Available: {available}")

    config_entry = manifest[config_name]
    wanted_splits = splits or sorted(config_entry.keys())
    result: dict[str, list[str]] = {}
    for split in wanted_splits:
        urls = config_entry.get(split, [])
        if not isinstance(urls, list):
            raise ValueError(f"Unexpected split entry type for {split}: {type(urls).__name__}")
        result[split] = [str(url) for url in urls]
    return result


def write_json(path: Path, payload: object) -> None:
    """Write JSON payload with deterministic formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def download_parquet_files(
    split_urls: dict[str, list[str]],
    output_dir: Path,
    overwrite: bool = False,
) -> list[Path]:
    """Download parquet shards into split subdirectories."""
    downloaded: list[Path] = []
    for split, urls in split_urls.items():
        split_dir = output_dir / split
        split_dir.mkdir(parents=True, exist_ok=True)
        for index, url in enumerate(urls):
            filename = f"{index}.parquet"
            destination = split_dir / filename
            if destination.exists() and not overwrite:
                downloaded.append(destination)
                continue
            urllib.request.urlretrieve(url, destination)
            downloaded.append(destination)
    return downloaded


def build_access_report(
    dataset_id: str,
    config_name: str,
    split_urls: dict[str, list[str]],
    downloaded_paths: list[Path],
) -> dict[str, object]:
    """Build a compact machine-readable ingestion report."""
    return {
        "dataset_id": dataset_id,
        "config": config_name,
        "splits": {split: len(urls) for split, urls in split_urls.items()},
        "downloaded_file_count": len(downloaded_paths),
        "downloaded_paths": [str(path) for path in downloaded_paths],
    }
