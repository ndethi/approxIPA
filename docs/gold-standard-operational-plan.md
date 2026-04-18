# Gold Standard Operational Plan

## Goal
Build a defensible Phase 1 gold standard for Kikuyu tonal minimal pairs that can be used to train and evaluate TCPR.

The current decision is to start with an Armstrong/Clements literature core and then expand with BibleTTS-mined, speaker-verified pairs.

## Operating Principle
Do not treat approximation outputs as gold. Use them only for candidate generation and sanity checks. Gold rows must be backed by a verified source stream.

## Phase 1 Build Sequence

### Step 1 — Acquire the Armstrong/Clements subset
Primary access route:
1. Locate the source documents referenced in [gold-standard-source-decision.md](gold-standard-source-decision.md).
2. Request a scan or PDF of the relevant pages from the analyst or a library source.
3. Extract only H/L tonal minimal pairs into a staging sheet.
4. Record page number, citation, and any transcription assumptions in the `notes` column.

### Step 2 — Create a staging sheet
Use the following fields for all candidate rows before anything is accepted into the gold set:

`word_a, word_b, tone_a, tone_b, meaning_a, meaning_b, gold_ipa_a, gold_ipa_b, source, status, notes`

Recommended values:
- `source = armstrong_1967`
- `source = clements_ford_1981`
- `status = primary` only after speaker verification
- `status = disputed` if a pair is cited in literature but the speaker disagrees

### Step 3 — Speaker verification
- Compare each literature pair with native-speaker judgment.
- Accept into the primary set only when the speaker confirms the contrast and meaning.
- Exclude or quarantine ambiguous cases.

### Step 4 — Expand with BibleTTS candidates
- Mine lexical candidates from aligned BibleTTS text/audio once the alignment pipeline is ready.
- Keep them separate from the literature core.
- Use them as an extension layer, not as the first gold standard.

### Step 5 — Validate and score
Run:

```bash
python evaluation/validate_tonal_minimal_pairs.py data/tonal_minimal_pairs.csv
python -m evaluation.run_tcpr
python -m evaluation.tcpr_report
```

## How To Access the Armstrong/Clements Subset

### Current repository status
- The repo contains only the citations and design notes.
- The actual pair tables are not yet present in the workspace.

### Practical access plan
1. Pull Armstrong/Clements pages from the original publications or scanned notes.
2. If the analyst already has a PDF or OCR scan, use that as the source of truth.
3. If no scan exists, request a library copy or analyst-provided excerpt.
4. Transcribe only the pairs that meet the Phase 1 H/L criterion from the design doc.

### Extraction rules
- Keep only same-segmental-form pairs.
- Keep only H vs L contrasts in Phase 1.
- Exclude downstep and rising tone until Phase 2.
- Normalize tone marks to precomposed Unicode acute/grave forms.

## Source Priority
1. Armstrong/Clements literature pairs: build the gold core.
2. BibleTTS mined pairs: add only after speaker verification.
3. Approximation outputs: use for candidate generation, never as gold truth.

## Deliverables
- `data/tonal_minimal_pairs.csv` — primary gold set
- `data/tonal_minimal_pairs.template.csv` — staging template
- `data/lexicon/kikuyu_ipa_review_sheet.csv` — candidate lexicon review sheet
- `evaluation/results/tcpr_summary.json` — scoring artifact

## Failure Modes To Avoid
- Mixing candidate IPA with gold IPA.
- Marking unverified literature pairs as primary.
- Expanding to LH/downstep before Phase 1 is validated.
- Losing citation provenance while transcribing pairs.
