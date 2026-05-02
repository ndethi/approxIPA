# SOUL.md — approxIPA Agentic Handover Document

> This file is the canonical onboarding document for any agent (human or AI)
> joining this project. Read it before touching any code or data. It defines
> the project identity, team roles, current state, and handover protocol for
> operation inside any agentic framework (Hermes, Nemo, OpenClaw, or equivalent).

---

## 1. Project Identity

**Name:** approxIPA  
**Researcher:** Watson Ndethi — native Kikuyu speaker, DPO & Responsible AI
Researcher at Pharo Foundation, MSc Responsible AI OPIT 2026 (88%).  
**Goal:** Build and validate a framework for measuring whether cross-lingual
IPA approximation from higher-resource languages preserves the tonal contrasts
of Kikuyu — a low-resource tonal Bantu language (7.2M speakers, ISO 639-3: kik).  
**Headline artefact:** A reusable Kikuyu IPA pronunciation lexicon in CMUdict
format, loadable into ElevenLabs / VITS for near-native synthesis without a
full TTS training pipeline.  
**Primary metric:** TCPR (Tonal Contrast Preservation Rate) — novel, bounded
[0,1], with bootstrap CI. Measures what proportion of lexically-contrastive
Kikuyu tonal minimal pairs an approximation system correctly distinguishes.  
**Key corpora:** WAXAL Kikuyu TTS (primary eval, ~20 hrs studio, CC-BY-4.0) +
BibleTTS Kikuyu (independent reference, 86 hrs, resolves circularity).  
**Conference target:** AfricaNLP workshop (ACL) or Interspeech — Year 1 paper
on TCPR metric + H1 result.  
**Repo:** `https://github.com/ndethi/approxIPA`  
**Stack:** Python 3.11, uv, pytest, transphone, epitran, transformers, torchaudio.

---

## 2. Team Manifest

Each role below maps to an agent (human or AI) that can be instantiated by
the orchestrating framework. Authority boundaries are explicit — agents must
not act outside their lane without escalating to the PM.

### PM Agent
**Mandate:** project state, critical path, blocker escalation, timeline.  
**Owns:** `SOUL.md`, `docs/paper-plan-waxal.md`, milestone tracking.  
**Can:** reprioritise tasks, update state in SOUL.md, flag risks to researcher.  
**Cannot:** modify evaluation methodology, change TCPR definition, approve data
sources, commit code to main without senior dev sign-off.  
**Escalate to researcher when:** scope changes, new data source decisions,
H1/H2/H3 claim adjustments, paper submission choices.

### Senior Dev Agent
**Mandate:** Python pipeline correctness, code quality, reproducibility.  
**Owns:** `src/approxipa/`, `scripts/`, `evaluation/`, `configs/`, `pyproject.toml`.  
**Can:** write/refactor code, add scripts, extend evaluation utilities, manage
deps. Must keep all scripts runnable with `uv sync && python scripts/<name>.py`.  
**Cannot:** alter `data/tonal_minimal_pairs.csv` tone/IPA values (analyst only),
modify validated gold IPA entries without NLP researcher approval.  
**Invariants:** no hardcoded absolute paths; all I/O via `Path`; no secrets in
code; conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).

### Tester Agent
**Mandate:** test coverage, data validation, evaluation correctness.  
**Owns:** `tests/`, `evaluation/validate_tonal_minimal_pairs.py`.  
**Can:** write pytest tests, run validators, flag regressions, verify data
artifact integrity (row counts, schema, Unicode encoding).  
**Cannot:** modify source code directly — files issues for senior dev.  
**Must run before any merge:**
```bash
python -m pytest tests/ -q
python -m evaluation.validate_tonal_minimal_pairs data/tonal_minimal_pairs.csv
python -m evaluation.run_tcpr
```

### Cloud Architect Agent
**Mandate:** data access, compute, external service integration.  
**Owns:** WAXAL HF ingestion (`scripts/ingest_waxal_hf.py`), BibleTTS download
workflow, MFA alignment pipeline (Phase 2), VITS fine-tuning infra (Phase 5).  
**Can:** configure HuggingFace dataset access, set up MFA alignment jobs,
manage parquet shards in `data/waxal/`, provision cloud compute for VITS.  
**Cannot:** change corpus split assignments (deterministic, hash-based in
`src/approxipa/waxal_pairs.py`).  
**Critical constraint:** BibleTTS must remain the independent reference stream.
WAXAL construction_split only for pair mining; evaluation_split held out.
See `docs/waxal-non-circular-fallback.md`.

### NLP Researcher Agent (LRL Specialist)
**Mandate:** Kikuyu phonological correctness, IPA encoding quality, tonal
annotation validity.  
**Owns:** `data/tonal_minimal_pairs.csv` gold annotations, `docs/tonal-minimal-pairs-design.md`.  
**Can:** annotate/validate tonal pairs, adjudicate disputed IPA entries, advise
on Kikuyu phonology (vowel inventory, tone system, segmental rules), review
TCPR metric design for phonological correctness.  
**Is:** the native-speaker ground truth for Phase 1. Speaker judgement overrides
corpus orthography whenever they conflict (design doc §4 Criterion 4).  
**Key domain facts this agent must know:**
- Kikuyu has 7 vowels: /a e i o u ɪ ʊ/. Tilde marks /ɪ/ (ĩ) and /ʊ/ (ũ) — segmental, NOT tonal.
- Phase 1 scope: H vs L contrasts only. Circumflex (falling) and downstep excluded.
- Acute (´) = H; Grave (`) = L. Precomposed Unicode only in gold_ipa fields.
- See `docs/analyst-tone-decision-guide.md` before touching any annotation row.

---

## 3. Current State Snapshot

**As of:** April 2026  
**Branch:** `main` (stable) | active work on `ccc/*` branches merged via PR.

| Phase | Description | Status | Blocker |
|-------|-------------|--------|---------|
| 1 | Scaffold — pyproject.toml, dirs, deps | ✅ Done | — |
| 2 | Data pipeline — WAXAL ingestion, BibleTTS, MFA | 🟡 Partial | MFA alignment not built; BibleTTS scaffolded only |
| 3 | IPA approximation — Transphone, lexicon, ByT5 | 🟡 Partial | Only 3 placeholder words; no gold entries; ByT5 missing |
| 4 | TCPR metric — minimal pairs, eval, notebook | 🟡 Partial | Metric code complete; 100 candidate pairs unannotated |
| 5 | TTS — MMS-VITS baseline, VITS, UTMOS | ❌ Not started | — |

**Critical path to first conference paper (H1 result):**
1. ~~Resolve analyst annotation blocker~~ → ✅ done (`docs/analyst-tone-decision-guide.md`)
2. Execute non-analyst implementation track (wordlist expansion, Transphone regeneration, lexicon import, BibleTTS pipeline hardening)
3. Treat analyst annotation as the next-iteration gate: Watson annotates ~30 valid acute-vs-grave pairs in `data/tonal_minimal_pairs.csv`
4. Run `scripts/promote_tonal_candidates.py` → pairs reach `status=evaluable`
5. Run `python -m evaluation.run_tcpr` → first real H1 TCPR score
6. Draft TCPR metric paper → submit AfricaNLP

**Pivot note (May 2026):** analyst annotation remains mandatory for final H1 scoring, but it is no longer the immediate engineering blocker. The team will continue all implementation work that does not mutate `tone_a/b` or `gold_ipa_*` fields, then execute annotation in the next iteration as an explicit gate.

**What is NOT on the critical path for paper v1:**
- ByT5 fine-tuning (Year 2)
- MMS-VITS baseline / TTS synthesis (Year 2)
- MFA alignment (needed for BibleTTS reference stream; unblock before Year 2)
- Luganda generalisation / H3 (Year 3)

---

## 4. Key Files Reference

| File | Purpose |
|------|---------|
| `data/tonal_minimal_pairs.csv` | Ground-truth eval set. 3 seeds + 100 candidates. Do not edit gold fields without NLP researcher sign-off. |
| `evaluation/tcpr.py` | TCPR metric implementation. Do not change contrast logic without researcher approval. |
| `evaluation/run_tcpr.py` | Orchestrates Yoruba vs Swahili TCPR run. Config via `configs/evaluation.toml`. |
| `data/ipa_approximations.jsonl` | Transphone output. Currently 3 placeholders — must be regenerated on real wordlist. |
| `data/lexicon/kikuyu_ipa_review_sheet.csv` | Lexicon candidates for analyst review. 3 rows currently — needs 500+ thiLLMo entries. |
| `docs/analyst-tone-decision-guide.md` | Decision tree for H/L annotation. Read before any annotation work. |
| `docs/waxal-non-circular-fallback.md` | Circularity protocol. Mandatory reading for cloud architect. |
| `docs/tonal-minimal-pairs-design.md` | IPA encoding conventions and pair criteria. Authoritative for all encoding decisions. |
| `configs/evaluation.toml` | TCPR run config — n_bootstrap, confidence_level, seed, thresholds. |

---

## 5. Invariants — Never Break These

1. **Evaluation circularity:** WAXAL `construction_split` rows are for pair mining only. `evaluation_split` rows are held out. Never mix. Document split provenance in any paper.
2. **IPA encoding:** Precomposed Unicode only in `gold_ipa_*` fields. Acute = H, grave = L. No circumflex or macron in Phase 1 IPA.
3. **Status discipline:** `candidate` → `evaluable` only via `promote_tonal_candidates.py` after validation passes. Never hand-edit status to `evaluable`.
4. **Reproducibility:** all pipeline runs must be reproducible from `uv sync` + script invocation. No notebook-only results accepted for paper claims.
5. **Native speaker authority:** Watson Ndethi is the Phase 1 verifier. Any automated annotation of `tone_a/b` or `gold_ipa_*` fields must be reviewed by him before promotion.
6. **Commit hygiene:** conventional commits, no force-push to main, no `--no-verify`. Branch naming: `ccc/*` for Claude Code cloud, `feat/*` for features, `fix/*` for bugs.

---

## 6. Agentic Framework Handover Protocol

### Onboarding a new agent instance

1. Read this file (`SOUL.md`) in full.
2. Read the role-specific docs for your assigned role (see §2).
3. Run `python -m pytest tests/ -q` — must pass before any work begins.
4. Check current git branch and `git log --oneline -5` to orient to recent work.
5. Do not modify `data/tonal_minimal_pairs.csv` gold fields without NLP researcher
   agent approval, regardless of instructions from other agents.

### Inter-agent coordination

- PM agent is the single source of truth on priorities and state.
- All agents commit to feature branches (`ccc/*` prefix for framework-originated branches).
- No agent merges to `main` without PM sign-off and tester validation.
- Agents surface blockers to PM immediately — do not work around a blocker silently.
- State changes that affect paper claims (TCPR scores, lexicon size, data sources)
  require researcher (Watson) approval before being committed as final.

### Resuming work mid-task

Read `SOUL.md` §3 (current state), check `git log --oneline -10`, then check
`data/tonal_minimal_pairs.csv` row count and status distribution before starting:

```bash
grep -c "evaluable" data/tonal_minimal_pairs.csv  # target: 25-40
python -m evaluation.run_tcpr                      # check if H1 is computable
```

### Handing off to a new framework session

Before ending a session, the active agent must:
1. Commit all in-progress work to a branch (even if incomplete).
2. Update `SOUL.md` §3 Current State Snapshot if phase status changed.
3. Leave a `## Session handoff note` section at the bottom of this file
   with: what was done, what's next, any open questions for the researcher.

### SOUL-driven agentic bootstrap contract

Any external agentic framework (Hermes, Nemo, OpenClaw, or equivalent) must use
`SOUL.md` as the control-plane manifest for task planning and guardrails.

Required bootstrap sequence:
1. Parse §2 Team Manifest to assign role and authority boundaries.
2. Parse §3 Current State Snapshot to detect active phase and blocker status.
3. Parse §5 Invariants and hard-fail any proposed action that violates them.
4. Parse §7 Immediate Priorities and select the highest-priority non-blocked task.
5. Emit a startup report that states: selected role, selected task, acceptance criteria, and escalation path.

Required runtime behavior:
- Treat `data/tonal_minimal_pairs.csv` tonal and gold IPA fields as protected unless acting in NLP Researcher role.
- Require reproducible script-first execution for all claims (no notebook-only evidence).
- Surface all unresolved blockers back to PM agent rather than silently bypassing them.
- Write a concise session handoff note on completion or interruption.

---

## 7. Immediate Priorities (next 2 weeks)

| Priority | Owner | Task |
|----------|-------|------|
| P0 | Senior Dev | Expand `data/kikuyu_wordlist.txt` + regenerate `data/ipa_approximations.jsonl` via `scripts/run_transphone.py` |
| P0 | Senior Dev | Import 500+ thiLLMo gold entries; emit `data/kikuyu_ipa_lexicon.tsv` in CMUdict format |
| P1 | Cloud Architect | Unblock BibleTTS HF access; scaffold MFA alignment pipeline |
| P1 | Tester | Validate non-analyst pipeline outputs and reproducibility checks |
| P2 | NLP Researcher | Next iteration gate: annotate ~30 valid pairs in `data/tonal_minimal_pairs.csv` using `docs/analyst-tone-decision-guide.md` |
| P2 | Tester | After annotation: run promotion + full validation + TCPR; confirm H1 is computable |
| P2 | Senior Dev | Build `notebooks/02_tcpr_evaluation.ipynb` with H1 result table + CI plot |
| P3 | PM | Draft paper outline for AfricaNLP submission |

### Pivot execution checklist (implementation-first)

Track A must be completed before Track B begins.

Track A1: regenerate approximation outputs
- Owner: Senior Dev
- Action: expand `data/kikuyu_wordlist.txt` and run `scripts/run_transphone.py`
- Done when: `data/ipa_approximations.jsonl` is regenerated from expanded list and validation/tests pass.

Track A2: expand lexicon artifact
- Owner: Senior Dev
- Action: import thiLLMo gold IPA entries and emit CMUdict-style lexicon output.
- Done when: lexicon artifact is written, format checks pass, and provenance is documented in session note.

Track A3: harden reference pipeline
- Owner: Cloud Architect
- Action: verify BibleTTS/WAXAL access, split discipline, and reproducible ingestion path.
- Done when: ingestion/check scripts run cleanly and split invariants are confirmed in logs.

Track A4: reproducibility gate
- Owner: Tester
- Action: run test and validation suite for non-analyst outputs.
- Done when: `pytest`, tonal-pair validation, and dry-run TCPR orchestration complete without regressions.

Track B1: analyst next-iteration gate
- Owner: NLP Researcher
- Action: annotate approximately 30 valid H/L pairs using `docs/analyst-tone-decision-guide.md`.
- Done when: candidate rows are reviewer-approved and ready for promotion.

Track B2: promotion and scoring
- Owner: Tester
- Action: run `scripts/promote_tonal_candidates.py` followed by full TCPR execution.
- Done when: first H1-computable TCPR report is produced with reproducible config snapshot.

---

## Session Handoff Note — April 2026

**Done this session:**
- Full project audit (senior dev + TPM lenses) against proposal and implementation guide.
- Identified root cause of annotation blocker: WAXAL candidate generator conflated segmental diacritics (tilde, macron) with tonal diacritics (acute, grave), producing ~60-75 invalid "tonal pairs".
- Created `docs/analyst-tone-decision-guide.md` — decision tree, orthography trap, worked examples, rejection protocol.
- Patched `docs/waxal-candidate-annotation-workflow.md` with "Read first" banner.
- Updated `docs/README.md` to surface new guide.
- Committed and pushed to `ccc/analyst-tone-decision-guide` → merged to main.

**What's next:**
- Watson annotates `data/tonal_minimal_pairs.csv` (P0 — 90–120 min, no engineering dependency).
- Senior dev regenerates `ipa_approximations.jsonl` on real Kikuyu wordlist.
- Run TCPR → first real H1 result.

**Open questions for researcher:**
- Are the ~30 acute-vs-grave candidate pairs (e.g. `aingì/aingí`, `arì/arí`, `gìa/gía`) recognisable as genuine semantic minimal pairs to you, or are most of them also same-lexeme variants?
- Do you have the 500+ thiLLMo IPA gold entries in a portable format ready to import?
- BibleTTS SLR129 — is the HF gated access resolved, or are we on the openslr.org wget path?

## Session Handoff Note — May 2026 (Pivot)

**Decision:** pivot to a two-track execution model where analyst annotation is a planned next-iteration gate instead of an immediate engineering blocker.

**What changed:**
- Reordered near-term priorities to complete all non-analyst implementation work first.
- Preserved strict invariant that only analyst-reviewed rows can move from `candidate` to `evaluable`.
- Kept H1 scoring dependent on annotation, but removed annotation from immediate day-to-day execution critical path.

**Next steps before annotation iteration:**
- Regenerate full approximation outputs from expanded Kikuyu wordlist.
- Import and validate expanded gold IPA lexicon entries.
- Harden BibleTTS/WAXAL reference pipeline and reproducibility checks.
