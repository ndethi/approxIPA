# BibleTTS Fallback Workflow for Gold Standard Tonal Pairs

## Why this exists
Armstrong (1967) and Clements & Ford (1981) remain the preferred literature sources, but they are not the operational dependency when lawful access is not currently available. BibleTTS becomes the feasible fallback path for building the gold-standard tonal pair set now.

## Hugging Face Access Status
- Public Hugging Face datasets do not require an API key for download.
- Gated or private datasets do require a token.
- In this workspace, a Kikuyu BibleTTS dataset was not confirmed in Hugging Face search results, so the dataset should be treated as **unconfirmed until the exact repo ID is known**.
- If the BibleTTS Kikuyu dataset is published openly, the workflow can proceed without an API key.
- If it is gated/private, a Hugging Face token will be required.

## Workflow
1. Obtain or generate BibleTTS Kikuyu alignment artifacts.
2. Mine candidate lexical items that recur with stable segmental form.
3. Inspect repeated occurrences for tonal contrasts that are consistent with the Phase 1 H/L scope.
4. Mark only speaker-verified rows as `status=primary`.
5. Keep uncertain items as `status=disputed` or exclude them from TCPR.

## What counts as acceptable fallback data
- Same segmental form across the pair.
- Clear H vs L tonal distinction in the gold IPA.
- Analyst/native-speaker confirmation that the pair is genuinely contrastive.
- Stable provenance fields in the CSV.

## What does not count
- Approximation output alone.
- Unverified repeated words with no tonal evidence.
- Rising tone and downstep in Phase 1.

## Output artifacts
- `data/tonal_minimal_pairs.csv` for the primary pair set.
- `data/lexicon/kikuyu_ipa_review_sheet.csv` for candidate lexicon review.
- `evaluation/results/tcpr_summary.json` for scoring.

## Relationship to Armstrong/Clements
If Armstrong/Clements pages later become available lawfully, they can be added as a secondary augmentation stream and compared against the BibleTTS fallback set. They do not block starting the workflow.
