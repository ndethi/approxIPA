"""Ingest WAXAL Kikuyu parquet metadata (and optional files) from Hugging Face."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from approxipa.waxal_ingestion import (  # noqa: E402
    build_access_report,
    config_urls,
    download_parquet_files,
    fetch_parquet_manifest,
    write_json,
)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for WAXAL ingestion from Hugging Face."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-id", default="google/WaxalNLP", help="Hugging Face dataset id")
    parser.add_argument("--config", default="kik_tts", help="Dataset config to ingest")
    parser.add_argument(
        "--splits",
        default="train,validation,test",
        help="Comma-separated split names to include",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "waxal",
        help="Output directory under repository",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download parquet shards locally in addition to writing manifests",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing local parquet files")
    args = parser.parse_args(argv)

    requested_splits = [split.strip() for split in args.splits.split(",") if split.strip()]

    manifest = fetch_parquet_manifest(args.dataset_id)
    split_urls = config_urls(manifest, args.config, splits=requested_splits)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_dir / "parquet_manifest.json"
    selected_path = args.output_dir / f"{args.config}_selected_urls.json"
    write_json(manifest_path, manifest)
    write_json(selected_path, split_urls)

    downloaded_paths: list[Path] = []
    if args.download:
        downloaded_paths = download_parquet_files(split_urls, args.output_dir, overwrite=args.overwrite)

    report = build_access_report(args.dataset_id, args.config, split_urls, downloaded_paths)
    report_path = args.output_dir / "access_report.json"
    write_json(report_path, report)

    print(f"[INFO] Wrote full parquet manifest: {manifest_path}")
    print(f"[INFO] Wrote selected split URLs: {selected_path}")
    if args.download:
        print(f"[INFO] Downloaded {len(downloaded_paths)} parquet file(s) into {args.output_dir}")
    else:
        print("[INFO] Download skipped (metadata-only mode). Use --download to fetch parquet files.")
    print(f"[INFO] Wrote access report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
