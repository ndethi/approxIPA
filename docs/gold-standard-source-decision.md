# Gold Standard Source Decision (Tonal Minimal Pairs)

## Question
For building the Phase 1 gold-standard tonal minimal-pair dataset, which source is more reasonable right now:
- Armstrong (1967) and Clements & Ford (1981)
- BibleTTS-mined candidates

## Short Answer
Use a **BibleTTS-first fallback strategy** for the operational workflow, while keeping Armstrong/Clements as the preferred literature source if lawful access becomes available later.

Operationally:
1. **BibleTTS-mined candidates become the immediate working source** because they are accessible in principle through the dataset and can be mined from the aligned corpus once the pipeline is ready.
2. **Armstrong/Clements remain the gold-standard reference target** for later augmentation, but they are not the blocking dependency for starting the project.

## Comparison

| Criterion | Armstrong/Clements | BibleTTS-mined candidates |
| --- | --- | --- |
| Linguistic clarity of tonal contrast | High | Medium (requires mining + filtering) |
| Risk of false minimal pairs | Lower (curated literature examples) | Higher (automatic candidate generation noise) |
| Relevance to contemporary TTS text domain | Medium | High |
| Effort to operationalize now in this repo | High (requires lawful access to purchased/held text) | Medium (requires alignment/mining pipeline artifacts) |
| Suitability for first defensible TCPR baseline | High, if access exists | High, as fallback when access is not available |

## Why This Is Reasonable
- Phase 1 needs a **credible, low-noise gold set** for validating metric behavior.
- Armstrong/Clements provides high-quality tonal contrasts with explicit linguistic grounding, but only if we can lawfully access the source material.
- BibleTTS candidates are the practical fallback because they can be derived from the corpus workflow already tied to the project.

## Recommended Construction Plan

### Phase 1A: Operational Gold Set (primary fallback)
- Source: BibleTTS-mined candidates, speaker-verified.
- Target size: small but high confidence (e.g., 30-50 primary pairs).
- Status in CSV: `source=bibletss_mined`, `status=primary`.

### Phase 1B: Literature Augmentation (secondary, when access exists)
- Source: Armstrong/Clements pairs.
- Include only lawfully accessed, speaker-verified true minimal pairs.
- Status in CSV: `source=armstrong_1967` or `source=clements_ford_1981`, `status=primary` or `status=disputed`.

## Analysis Policy
- Report TCPR overall and stratified by `source`.
- Treat large source-wise variance as a finding, not as noise.

## Immediate Next Step
Populate `data/tonal_minimal_pairs.csv` with a first verified BibleTTS-mined subset, validate with:

```bash
python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv
python -m evaluation.run_tcpr
python -m evaluation.tcpr_report
```
