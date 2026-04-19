# approxIPA

Research scaffold for IPA approximation and tonal contrast evaluation.

## Layout

- `src/approxipa/`: Python package for reusable code
- `scripts/`: runnable pipeline scripts
- `evaluation/`: metric and analysis utilities
- `data/`: local datasets, annotations, and outputs
- `tests/`: pytest suite
- `notebooks/`: exploratory notebooks

## Getting Started

1. Create a Python 3.11 environment.
2. Install dependencies with `uv sync` or your preferred toolchain.
3. Run scripts from `scripts/` and keep research artifacts under `data/`.

## Transphone Pipeline

Run the Kikuyu approximation pipeline with:

```bash
python scripts/run_transphone.py
```

The script reads `data/kikuyu_wordlist.txt` and writes `data/ipa_approximations.jsonl`.

## Candidate Lexicon Extraction

Generate a review-ready Kikuyu IPA candidate lexicon from approximation outputs:

```bash
python scripts/extract_lexicon_candidates.py
```

The script reads `data/ipa_approximations.jsonl` and writes
`data/lexicon/kikuyu_ipa_review_sheet.csv`.
Rows where Yoruba/Swahili disagree are marked `needs-analyst-review`.

## WAXAL Ingestion

Populate WAXAL metadata for Kikuyu from Hugging Face:

```bash
python scripts/ingest_waxal_hf.py --dataset-id google/WaxalNLP --config kik_tts --splits train,validation,test
```

This creates:
- `data/waxal/parquet_manifest.json`
- `data/waxal/kik_tts_selected_urls.json`
- `data/waxal/access_report.json`

Add `--download` to fetch parquet shards into `data/waxal/{split}/`.
