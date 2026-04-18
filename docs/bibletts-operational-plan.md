# BibleTTS Operational Plan

## Goal
Use BibleTTS as the near-term operational source for building the Kikuyu tonal minimal-pair gold set when Armstrong/Clements are not legally accessible.

## Hugging Face Access Status
- Hugging Face public datasets do **not** require an API key or token to download.
- Gated or private datasets do require authentication.
- Current search in the repository workflow did **not** confirm a publicly listed Kikuyu BibleTTS dataset on Hugging Face.
- If a BibleTTS Kikuyu dataset is published openly, the workflow can proceed without an API key.
- If the dataset is gated or private, access will require a Hugging Face token or the maintainer to grant access.

## Required Inputs
- BibleTTS Kikuyu aligned transcript export
- Sentence/audio identifiers
- Orthographic word tokens
- Optional forced-alignment metadata
- Optional acoustic summaries such as F0 statistics or tonal annotations

## Minimum Input Schema
Each aligned row should provide at least:
- `utterance_id`
- `word`
- `orthography`
- `start_time`
- `end_time`
- `source_sentence`

Recommended additional fields:
- `speaker_id`
- `audio_path`
- `f0_mean`
- `f0_min`
- `f0_max`
- `alignment_confidence`

## Build Steps
1. Ingest aligned BibleTTS exports into a normalized CSV or JSONL file.
2. Group repeated orthographic forms within the same lexical item.
3. Surface candidate tonal contrasts for manual review.
4. Mark candidate rows as `needs-analyst-review` until verified.
5. Promote only verified rows into `data/tonal_minimal_pairs.csv`.

## What Counts as a Candidate
- Same orthographic/segmental form across occurrences.
- Distinct tonal behavior across aligned realizations.
- Speaker or analyst confirmation that the pair is contrastive.

## What Does Not Count
- One-off transcription noise.
- Unaligned transcript text without timing or acoustic evidence.
- Approximated IPA only.

## Output Artifacts
- `data/bibletts/aligned/` for raw aligned exports, once available.
- `data/bibletts/candidate_pairs.csv` for review candidates.
- `data/tonal_minimal_pairs.csv` for the verified gold set.

## Access Note
Do not block the workflow on an API key unless the dataset page is explicitly gated or private. For a public dataset, `huggingface_hub` download helpers can fetch data without a token.

## Relationship to Armstrong/Clements
BibleTTS is the operational fallback. Armstrong/Clements remain the preferred literature augmentation path if lawful access is later obtained.
