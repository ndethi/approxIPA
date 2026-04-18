# WAXAL Fallback and Non-Circularity Protocol

## Question
Can WAXAL be used to build tonal minimal pairs if BibleTTS Kikuyu data is unavailable, without invalidating downstream evaluation?

## Short Answer
Yes, but only with strict separation between:
- WAXAL data used for **candidate discovery**
- WAXAL data used for **final evaluation**

Without this separation, the workflow becomes circular and results are not defensible.

## Why Circularity Risk Exists
If the same corpus instances contribute to both:
1. constructing/validating the gold pair set, and
2. measuring final model performance,
then evaluation can overestimate quality due to information leakage.

## Allowed Use of WAXAL (Fallback)
WAXAL may be used for:
- candidate mining of repeated lexical forms
- exploratory acoustic checks (e.g., F0 contrasts)
- identifying potential H/L contrasts to send for analyst verification

WAXAL may **not** be used as the sole source of both pair construction and final scoring on the same instances.

## Non-Circular Protocol

### 1) Freeze a split policy before mining
Define immutable partitions first, e.g.:
- `construction_split`: WAXAL subset used only for candidate mining
- `evaluation_split`: WAXAL subset used only for final TCPR/TTS evaluation

No utterance overlap between splits.

### 2) Build pairs only from construction_split
- Mine candidate pairs from `construction_split` only.
- Route all candidates through analyst/native-speaker verification.
- Store provenance in `source` and `notes` fields.

### 3) Keep gold labels independent
- Final `gold_ipa_*` labels should come from speaker/analyst verification, not automatic approximations.
- Mark uncertain rows as `status=disputed`.

### 4) Evaluate only on evaluation_split
- Run TCPR and downstream TTS/ASR metrics only on held-out `evaluation_split`.
- Do not tune pair definitions using evaluation results.

### 5) Report split provenance in paper
Include:
- split definitions and sizes
- no-overlap statement
- candidate-mining split versus evaluation split
- any exclusions/disputed rows

## Practical Recommendation
Priority order remains:
1. BibleTTS Kikuyu aligned subset (if obtained)
2. WAXAL fallback with strict non-circular split protocol
3. Armstrong/Clements augmentation if lawful access later becomes available

## Minimum Reporting Checklist
- [ ] Split policy committed before mining
- [ ] Candidate mining restricted to construction_split
- [ ] Gold labels speaker-verified
- [ ] Evaluation uses held-out evaluation_split only
- [ ] Source-stratified metrics reported
