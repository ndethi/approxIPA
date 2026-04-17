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

## Collection Rules
- The two words should differ only in tone for the first version of the dataset.
- Keep segmental material identical unless a pair is intentionally annotated as a harder case.
- Prefer minimal pairs with clear lexical contrast.
- Record the source of each pair in a separate notes file or annotation log if available.
- Validate the file with `python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv` after each update.

## Current Status
- `data/tonal_minimal_pairs.csv` is still a seed/smoke-test file.
- `data/tonal_minimal_pairs.template.csv` is the blank template for curated replacement data.

## Next Action
Replace the placeholder rows in `data/tonal_minimal_pairs.csv` with curated Kikuyu examples and gold IPA from speaker-verified sources.
