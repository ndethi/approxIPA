# Tonal Minimal Pair Collection Guide

Use this guide to replace the placeholder seed pairs with real Kikuyu tonal minimal pairs.

## Required Columns
- `word_a`: first Kikuyu orthographic form
- `word_b`: second Kikuyu orthographic form
- `tone_a`: tone label for `word_a` using a consistent scheme, e.g. `H`, `L`, `LH`
- `tone_b`: tone label for `word_b`
- `meaning_a`: gloss or short English meaning for `word_a`
- `meaning_b`: gloss or short English meaning for `word_b`
- `gold_ipa_a`: manually verified IPA for `word_a`
- `gold_ipa_b`: manually verified IPA for `word_b`
- `source`: provenance label such as `waxal`, `bibletts`, `armstrong1967`
- `source_id`: source-local stable ID (utterance id, page-line id, or record id)
- `source_split`: required for WAXAL rows; set to `construction` or `evaluation`

## Recommended Columns
- `status`: lifecycle value such as `seed`, `candidate`, `primary`, `disputed`
- `notes`: free-text provenance and reviewer notes

## Collection Rules
- The two words should differ only in tone for the first version of the dataset.
- Keep segmental material identical unless a pair is intentionally annotated as a harder case.
- Prefer minimal pairs with clear lexical contrast.
- For WAXAL rows, assign immutable split labels before mining and never mix splits during evaluation.
- Validate the file with `python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv` after each update.

## WAXAL Split Workflow
- Run `python scripts/ingest_waxal_hf.py --dataset-id google/WaxalNLP --config kik_tts --splits train,validation,test` to populate `data/waxal/` metadata from Hugging Face.
- Run `python scripts/extract_waxal_candidates.py --data-dir data/waxal --splits train,validation,test --min-occurrences 3 --stopwords-file data/waxal/kikuyu_stopwords.txt --max-utterance-ratio 0.2` for filtered lexical candidates.
- Run `python scripts/build_waxal_pair_candidates.py --data-dir data/waxal --splits train,validation,test --stopwords-file data/waxal/kikuyu_stopwords.txt --min-variant-occurrences 3` to build reviewable pair candidates.
- Run `python scripts/bridge_waxal_pairs_to_tonal_csv.py --candidate-csv data/waxal/kikuyu_pair_candidates.csv --pairs-csv data/tonal_minimal_pairs.csv --max-new 100 --require-construction` to import construction-only candidate rows into the tonal CSV.
- Run `python scripts/check_waxal_access_and_split.py --pairs data/tonal_minimal_pairs.csv` to check local WAXAL access and assign deterministic split labels.
- Keep `source_split=construction` rows for mining and analyst review only.
- Keep `source_split=evaluation` rows held out for final metrics only.

## Current Status
- `data/tonal_minimal_pairs.csv` now contains 3 seed pairs + 100 WAXAL-sourced candidate pairs (status=candidate, awaiting analyst annotation).
- Candidates have word forms and provenance populated; tones and IPA marked as empty.
- `data/tonal_minimal_pairs.template.csv` is the blank template for future replacement iterations.

## Analyst Annotation Workflow (CURRENT STEP)

**For annotators:** See [docs/waxal-candidate-annotation-workflow.md](../docs/waxal-candidate-annotation-workflow.md) for step-by-step instructions to annotate the 100 candidate rows.

The workflow guide includes:
- Understanding candidate vs. seed rows
- Using seed rows as reference examples
- Step-by-step tone and IPA annotation
- Validation and quality assurance
- Troubleshooting common issues

## Next Action
Analysts should annotate the 100 candidate rows (rows 5-104) with tone and IPA values per [docs/waxal-candidate-annotation-workflow.md](../docs/waxal-candidate-annotation-workflow.md).

Once annotated and validated, promote approved rows with:

`python scripts/promote_tonal_candidates.py --pairs-csv data/tonal_minimal_pairs.csv`

This command promotes only complete candidate rows from `status=candidate` to `status=evaluable` and leaves incomplete rows as candidates.
