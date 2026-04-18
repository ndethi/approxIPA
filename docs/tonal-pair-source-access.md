# Tonal Pair Source Access Determination

This document records which sources are currently usable to build `data/tonal_minimal_pairs.csv` with real Kikuyu tonal minimal pairs.

## Imported Design Reference
- Primary design reference is now in repo: `docs/tonal-minimal-pairs-design.md`.

## Source Access Matrix

| Source | Access now | Usable for immediate pair construction | Notes |
| --- | --- | --- | --- |
| Armstrong (1967) (cited in design doc) | Not present in workspace and not legally assumed accessible without purchase/library copy | No | High-quality target source; treat as future augmentation rather than blocking dependency. |
| Clements & Ford (1981) (cited in design doc) | Not present in workspace and not legally assumed accessible without purchase/library copy | No | Same constraint as Armstrong for now. |
| BibleTTS mined candidates (design doc Source C) | Not present as aligned outputs in repo; official OpenSLR SLR129 currently does not expose Kikuyu aligned package in public list | Feasible only after Kikuyu aligned data is obtained | Remains fallback strategy, but now explicitly data-availability-gated. |
| WAXAL Kikuyu (fallback) | Mentioned in project plan; operational subset availability depends on local ingestion | Feasible with strict split isolation | Must use non-circular protocol: separate construction and evaluation splits with no overlap. |
| Current approximation outputs (`data/ipa_approximations.jsonl`) | Present | Partial (bootstrap only) | Useful for candidate generation/review workflow, not gold tonal pair truth. |
| Native-speaker / analyst verification | Awaiting analyst input | Not yet | Required to turn candidates into `status=primary` pairs. |

## Practical Determination
Right now we can keep a **BibleTTS-backed workflow scaffold** from existing approximation outputs and mining scripts, but full Kikuyu BibleTTS mining is blocked until a Kikuyu aligned subset is obtained.

If BibleTTS Kikuyu remains unavailable, WAXAL can be used as fallback only under a non-circular split protocol (see `docs/waxal-non-circular-fallback.md`).

For Hugging Face access, the rule is: **public dataset = no API key required; gated/private dataset = token required**. The exact Kikuyu BibleTTS repository ID is still unconfirmed, and OpenSLR is currently the authoritative source.

## Immediate Build Path (Doable Now)
1. Keep `data/tonal_minimal_pairs.csv` as seed/smoke-test data.
2. Use `scripts/extract_lexicon_candidates.py` to generate analyst review candidates in `data/lexicon/kikuyu_ipa_review_sheet.csv`.
3. Confirm the BibleTTS Hugging Face repo ID and whether it is public or gated/private.
4. Build BibleTTS alignment artifacts and mine tonal pair candidates.
5. Replace seed rows with verified BibleTTS rows and run:
   - `python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv`
   - `python -m evaluation.run_tcpr`
   - `python -m evaluation.tcpr_report`

Fallback branch when BibleTTS Kikuyu is unavailable:
6. Define immutable WAXAL construction/evaluation splits.
7. Mine and verify pairs from construction split only.
8. Evaluate only on held-out evaluation split.

## What To Request From Analyst
- CSV/TSV with at least columns:
  - `word_a`, `word_b`, `tone_a`, `tone_b`, `meaning_a`, `meaning_b`, `gold_ipa_a`, `gold_ipa_b`
- Optional but recommended metadata:
  - `source`, `status`, `notes`
- Encoding requirement:
  - Use precomposed acute/grave IPA tone characters consistently.
- If Armstrong/Clements pages are later made available lawfully, include page numbers and citations so they can be added as a secondary source stream.
- If the BibleTTS Kikuyu dataset is gated/private, request the Hugging Face repo ID and access token from the data steward.
