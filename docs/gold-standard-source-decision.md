# Gold Standard Source Decision (Tonal Minimal Pairs)

## Question
For building the Phase 1 gold-standard tonal minimal-pair dataset, which source is more reasonable right now:
- Armstrong (1967) and Clements & Ford (1981)
- BibleTTS-mined candidates

## Short Answer
Use a **hybrid strategy**:
1. **Start with Armstrong/Clements** for the initial gold core (higher linguistic reliability per pair).
2. **Add BibleTTS-mined candidates** as a second layer after speaker verification (higher ecological relevance).

If one source must be chosen first for Phase 1, choose **Armstrong/Clements first**.

## Comparison

| Criterion | Armstrong/Clements | BibleTTS-mined candidates |
| --- | --- | --- |
| Linguistic clarity of tonal contrast | High | Medium (requires mining + filtering) |
| Risk of false minimal pairs | Lower (curated literature examples) | Higher (automatic candidate generation noise) |
| Relevance to contemporary TTS text domain | Medium | High |
| Effort to operationalize now in this repo | Medium (manual transcription) | High (needs alignment/mining pipeline artifacts) |
| Suitability for first defensible TCPR baseline | High | Medium |

## Why This Is Reasonable
- Phase 1 needs a **credible, low-noise gold set** for validating metric behavior.
- Armstrong/Clements provides high-quality tonal contrasts with explicit linguistic grounding.
- BibleTTS candidates are still valuable, but they are strongest as a **naturalistic extension set** once mined and speaker-verified.

## Recommended Construction Plan

### Phase 1A: Core Gold Set (primary)
- Source: Armstrong/Clements pairs, speaker-verified.
- Target size: small but high confidence (e.g., 30-50 primary pairs).
- Status in CSV: `source=armstrong_1967` or `source=clements_ford_1981`, `status=primary`.

### Phase 1B: Naturalistic Extension (secondary)
- Source: BibleTTS-mined candidates.
- Include only speaker-verified true minimal pairs.
- Status in CSV: `source=bibletss_mined`, `status=primary` or `status=disputed`.

## Analysis Policy
- Report TCPR overall and stratified by `source`.
- Treat large source-wise variance as a finding, not as noise.

## Immediate Next Step
Populate `data/tonal_minimal_pairs.csv` with a first verified Armstrong/Clements subset, validate with:

```bash
python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv
python -m evaluation.run_tcpr
python -m evaluation.tcpr_report
```
