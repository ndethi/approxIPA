# approxIPA Paper Plan (WAXAL Validation)

## Objective
Test and report whether cross-lingual IPA approximation from nearby higher-resource languages can produce usable Kikuyu IPA and improve downstream TTS usability under low-resource constraints.

## Core Hypothesis
Approximating Kikuyu IPA from related source languages (especially tonal Yoruba vs non-tonal Swahili) preserves enough lexical tonal contrast and segmental quality to be usable for synthesis and evaluation tasks.

## Decision Criteria (Validate / Invalidate)

### Validate if most are true
- Yoruba-weighted condition clearly outperforms Swahili-weighted on tonal contrast preservation.
- TCPR is materially above a pre-registered minimum target for practical use.
- Segmental distance (PanPhon/CLTS) is competitive with or better than baseline alternatives.
- IPA-scaffolded synthesis is not worse than MMS-VITS baseline by a practically important margin on intelligibility and naturalness proxies.

### Invalidate if most are true
- Tonal contrast is frequently collapsed (especially in minimal pairs), with no meaningful gain over controls.
- Improvements are inconsistent or statistically weak after uncertainty estimation.
- Usability claims do not hold under WAXAL evaluation conditions.

## Pre-Registered Targets (to finalize before full run)
- TCPR target threshold for practical usability.
- Minimum effect size versus Swahili control.
- Minimum acceptable intelligibility gap versus direct baseline.
- Confidence interval policy and bootstrap settings.

## Experimental Matrix
- Source conditions:
  - Yoruba-weighted approximation (primary tonal source)
  - Swahili-weighted approximation (negative/control condition)
  - Optional neural G2P ablation (ByT5 fine-tuned on curated lexicon)
- Evaluation corpora:
  - WAXAL Kikuyu TTS (primary)
  - BibleTTS Kikuyu (independent alignment/reference stream)
  - WAXAL ASR split for intelligibility testing of synthesized output
  - WAXAL Luganda (generalization check, optional for paper v1)

## Work Packages

### WP1 — Data and Reference Integrity
- Lock dataset versions and hashes for WAXAL and BibleTTS assets.
- Build and validate alignment outputs for reference extraction.
- Produce a data card with inclusion/exclusion criteria and known limitations.

### WP2 — IPA Approximation Outputs
- Generate Kikuyu approximation outputs for Yoruba and Swahili conditions.
- Normalize and store deterministic JSONL outputs.
- Build merged lexicon artifact with manual gold entries when available.

### WP3 — Metric Implementation
- Implement TCPR with explicit contrast-preservation logic.
- Add bootstrap confidence intervals and reproducible random seed control.
- Add segmental distance metrics (PanPhon and CLTS-based comparisons).

### WP4 — TTS Usability Evaluation
- Run baseline synthesis and IPA-scaffolded synthesis on matched text sets.
- Compute intelligibility proxies and aggregate condition-level summaries.
- Prepare protocol for native-speaker tonal naturalness ratings (if included in v1).

### WP5 — Statistical Analysis and Robustness
- Report per-condition means, uncertainty intervals, and effect sizes.
- Run ablations (source language, lexicon size, optional neural G2P).
- Perform failure-mode analysis focused on tonal pattern classes.

### WP6 — Paper Writing and Packaging
- Draft complete paper with methods reproducibility appendix.
- Export artifacts: lexicon, approximation outputs, metric code, config files.
- Prepare replication checklist and release notes.

## Proposed Paper Structure
1. Introduction and problem framing
2. Related work and gap (tonally aware evaluation)
3. Hypothesis and evaluation design
4. Data and preprocessing (WAXAL + BibleTTS)
5. Approximation methods and conditions
6. Metrics (TCPR, segmental, intelligibility)
7. Results and uncertainty
8. Error analysis and failure taxonomy
9. Limitations, ethics, and community implications
10. Conclusion and future work

## Near-Term Execution Plan (Next 2 Weeks)

## Execution Status
- [x] Plan documented in repository.
- [x] Pre-registration thresholds finalized.
- [x] TCPR module + tests implemented.
- [x] Tonal minimal-pair seed dataset added.
- [x] Tonal minimal-pair validator added.
- [x] Tonal pair collection template added.
- [x] Lexicon candidate extraction workflow added.
- [x] Tonal source-access determination documented.
- [x] Gold-standard source strategy decided (literature core + BibleTTS extension).
- [x] Gold-standard operational plan documented.
- [x] BibleTTS fallback workflow documented.
- [x] First metric run completed on frozen outputs.
- [x] TCPR reporting utility added.
- [ ] Results notebook scaffolded.

### Week 1
- Finalize pre-registration thresholds and statistical protocol.
- Build tonal minimal-pair dataset v1 for Kikuyu.
- Implement TCPR and unit tests.
- Generate Yoruba/Swahili approximation outputs on frozen input lists.

### Week 2
- Run full metric suite on WAXAL evaluation partitions.
- Produce first results tables and plots.
- Write Results skeleton and Methods sections.
- Decide validate/invalidate status per hypothesis with evidence table.

## Immediate Next Tasks in This Repo
- Create evaluation/tcpr.py and tests for contrast-preservation rules.
- Create data/tonal_minimal_pairs.csv with initial curated seed set.
- Add notebooks for results tables/plots and confidence intervals.
- Add experiment config file to make all runs reproducible.

## Risks and Mitigations
- Risk: tonal annotation sparsity in references.
  - Mitigation: conservative labeling policy + manual spot checks.
- Risk: API/toolchain drift in speech libraries.
  - Mitigation: pinned versions and run logs for each experiment.
- Risk: overclaiming usability from proxy metrics.
  - Mitigation: explicitly separate proxy-based claims from human evaluation claims.

## Evidence Table Template (for final claim)
- Hypothesis: H1 tonal preservation
  - Status: pending
  - Key metric: TCPR
  - Result summary: pending
  - Confidence statement: pending
- Hypothesis: H2 practical usability for TTS
  - Status: pending
  - Key metrics: intelligibility + quality proxies
  - Result summary: pending
  - Confidence statement: pending
- Hypothesis: H3 generalization
  - Status: optional in paper v1
  - Key metrics: cross-language variance explained by phonological distance
  - Result summary: pending
  - Confidence statement: pending
