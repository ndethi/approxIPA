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

Build first-pass lexical candidates from local Kikuyu parquet files:

```bash
python scripts/extract_waxal_candidates.py --data-dir data/waxal --splits train,validation,test --min-occurrences 3 --stopwords-file data/waxal/kikuyu_stopwords.txt --max-utterance-ratio 0.2
```

This writes `data/waxal/kikuyu_candidate_words.csv`.
The CSV keeps full occurrence counts but stores compact utterance/speaker samples for review.

Build tonal-variant pair candidates for analyst review:

```bash
python scripts/build_waxal_pair_candidates.py --data-dir data/waxal --splits train,validation,test --stopwords-file data/waxal/kikuyu_stopwords.txt --min-variant-occurrences 3
```

This writes `data/waxal/kikuyu_pair_candidates.csv` with deterministic `source_split` assignments.

Bridge construction-safe pair candidates into `data/tonal_minimal_pairs.csv`:

```bash
python scripts/bridge_waxal_pairs_to_tonal_csv.py --candidate-csv data/waxal/kikuyu_pair_candidates.csv --pairs-csv data/tonal_minimal_pairs.csv --max-new 100 --require-construction
```

These imported rows are marked `status=candidate` and must be manually annotated for tones and gold IPA before TCPR evaluation.

## Analyst Annotation Workflow

Once candidate pairs are in `data/tonal_minimal_pairs.csv`, analysts must annotate tone and IPA values:

**See [docs/waxal-candidate-annotation-workflow.md](docs/waxal-candidate-annotation-workflow.md) for detailed instructions.**

**Quick summary:**
1. Open `data/tonal_minimal_pairs.csv` (rows 5-104 are the 100 candidate rows)
2. Use the 3 seed rows at the top as reference examples
3. For each candidate, determine `tone_a` and `tone_b` (H or L) from orthographic diacritics
4. Construct `gold_ipa_a` and `gold_ipa_b` using Kikuyu segmental phonology and tonal marking conventions
5. Validate with: `python -m evaluation.validate_tonal_minimal_pairs data/tonal_minimal_pairs.csv`
6. Submit completed CSV for TCPR metric evaluation

Estimated time: 1-2 hours for an analyst with Kikuyu phonological knowledge.
