# Tonal Pair Source Access Determination

This document records which sources are currently usable to build `data/tonal_minimal_pairs.csv` with real Kikuyu tonal minimal pairs.

## Imported Design Reference
- Primary design reference is now in repo: `docs/tonal-minimal-pairs-design.md`.

## Source Access Matrix

| Source | Access now | Usable for immediate pair construction | Notes |
| --- | --- | --- | --- |
| Armstrong (1967) (cited in design doc) | Not present in workspace | No (until digitized excerpts/notes provided) | High-quality target source; currently a bibliographic reference only. |
| Clements & Ford (1981) (cited in design doc) | Not present in workspace | No (until excerpts/notes provided) | Same constraint as Armstrong for now. |
| BibleTTS mined candidates (design doc Source C) | Not present as aligned outputs in repo | Not yet | Can become usable once BibleTTS + MFA alignment pipeline artifacts are generated. |
| Current approximation outputs (`data/ipa_approximations.jsonl`) | Present | Partial (bootstrap only) | Useful for candidate generation/review workflow, not gold tonal pair truth. |
| Native-speaker / analyst verification | Awaiting analyst input | Not yet | Required to turn candidates into `status=primary` pairs. |

## Practical Determination
Right now we can only do a **bootstrap candidate workflow** from existing approximation outputs and templates. We cannot claim a true gold tonal minimal-pair set until at least one verified source stream is available (literature extraction notes, BibleTTS-mined verified candidates, or analyst-provided list).

## Immediate Build Path (Doable Now)
1. Keep `data/tonal_minimal_pairs.csv` as seed/smoke-test data.
2. Use `scripts/extract_lexicon_candidates.py` to generate analyst review candidates in `data/lexicon/kikuyu_ipa_review_sheet.csv`.
3. Wait for analyst-provided verified pairs or literature-transcribed pairs.
4. Replace seed rows with verified rows and run:
   - `python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv`
   - `python -m evaluation.run_tcpr`
   - `python -m evaluation.tcpr_report`

## What To Request From Analyst
- CSV/TSV with at least columns:
  - `word_a`, `word_b`, `tone_a`, `tone_b`, `meaning_a`, `meaning_b`, `gold_ipa_a`, `gold_ipa_b`
- Optional but recommended metadata:
  - `source`, `status`, `notes`
- Encoding requirement:
  - Use precomposed acute/grave IPA tone characters consistently.
