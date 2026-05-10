# Hermes Track A Implementation Instructions

**Date:** May 2, 2026  
**Branch:** `dev`  
**Cwd:** `/Users/ndethi/dev/ir/approxIPA`  
**Control Plane:** `SOUL.md`  

---

## Your Mission

Execute **Track A** (non-analyst implementation) of the approxIPA pivot workflow. Track A must complete before analyst annotation begins (Track B).

## Before You Start

1. Read `SOUL.md` in full — it is your source of truth for roles, invariants, current state, and task definitions.
2. Read `docs/agentic-bootstrap-guide.md` — it documents the SOUL-driven execution contract.
3. Read `docs/paper-plan-waxal.md` — it explains the two-track model and why we're doing this pivot.

## Your Role

**Senior Dev Agent** (as defined in `SOUL.md` §2).

**Mandate:** Python pipeline correctness, code quality, reproducibility.

**You can:**
- Write/refactor code, add scripts, extend evaluation utilities, manage deps.
- Keep all scripts runnable with `uv sync && python scripts/<name>.py`.

**You cannot:**
- Alter `data/tonal_minimal_pairs.csv` tone/IPA values (analyst only).
- Modify validated gold IPA entries without NLP researcher approval.

**Invariants you must never break:**
- No hardcoded absolute paths; all I/O via `Path`.
- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Script-first execution — no notebook-only results.
- Do not touch analyst-reserved fields.

## Your Track A Tasks (In Order)

### A1: Regenerate approximation outputs

**Owner:** You (Senior Dev)

**Action:** Expand `data/kikuyu_wordlist.txt` and run `scripts/run_transphone.py`.

**Done when:** 
- `data/ipa_approximations.jsonl` is regenerated from expanded list.
- Validation/tests pass.

**Next:** Commit with message: `feat(data): expand wordlist and regenerate Transphone approximations`

---

### A2: Expand lexicon artifact

**Owner:** You (Senior Dev)

**Action:** Import thiLLMo gold IPA entries and emit CMUdict-style lexicon output.

**Done when:**
- Lexicon artifact is written.
- Format checks pass.
- Provenance is documented in the commit message.

**Next:** Commit with message: `feat(lexicon): import thiLLMo gold entries and build CMUdict artifact`

---

### A3: Harden reference pipeline

**Owner:** Cloud Architect (but you can scaffold it)

**Action:** Verify BibleTTS/WAXAL access, split discipline, and reproducible ingestion path.

**Done when:** 
- Ingestion/check scripts run cleanly.
- Split invariants are confirmed in logs.

**Next:** Commit with message: `feat(pipeline): validate BibleTTS and WAXAL split integrity`

---

### A4: Reproducibility gate

**Owner:** You (validate as part of your work)

**Action:** Run test and validation suite for non-analyst outputs.

**Done when:** 
- `pytest` passes.
- Tonal-pair validation passes.
- Dry-run TCPR orchestration completes without regressions.

**Next:** Commit with message: `test(validation): confirm Track A outputs pass reproducibility checks`

---

## How to Execute

1. Confirm you're on `dev` branch:
   ```bash
   git branch --show-current  # should show: dev
   ```

2. Ensure working tree is clean:
   ```bash
   git status --short  # should show nothing
   ```

3. For each Track A task:
   - Read the task description above.
   - Implement the work.
   - Run tests and validators.
   - Commit with conventional message.
   - Verify all tests still pass.

4. When a task is done, move to the next one.

5. If you hit a blocker, stop and write a handoff note (see below).

## Commands You'll Need

```bash
# Ensure environment is ready
uv sync

# Run Transphone for wordlist expansion
python scripts/run_transphone.py

# Extract lexicon candidates
python scripts/extract_lexicon_candidates.py

# Check WAXAL/BibleTTS access and splits
python scripts/check_waxal_access_and_split.py

# Run full test suite
python -m pytest tests/ -q

# Run tonal-pair validation
python -m evaluation.validate_tonal_minimal_pairs data/tonal_minimal_pairs.csv

# Dry-run TCPR (won't compute scores without annotations)
python -m evaluation.run_tcpr

# Check git status and logs
git status --short
git log --oneline -5
```

## When You Hit a Blocker

If a script is missing or a data file doesn't exist as expected:

1. Record what the blocker is.
2. Write a concise handoff note (see template below).
3. Stop and let Watson or the PM know.

## When You're Done

Write a session handoff note and commit it or append it to `SOUL.md` under a new section:

```text
## Session Handoff Note — Hermes Track A (May 2, 2026)

**What I did:**
- Expanded `data/kikuyu_wordlist.txt` from X to Y entries
- Regenerated `data/ipa_approximations.jsonl` deterministically
- Imported Z thiLLMo entries into lexicon artifact
- Validated BibleTTS/WAXAL splits and ingestion
- Confirmed all tests pass

**What I validated:**
- Wordlist expansion is idempotent and reproducible
- IPA approximations match expected format and count
- Lexicon artifact is in CMUdict format with correct provenance
- Split invariants are preserved
- pytest suite passes with no regressions

**What is next:**
- Analyst annotation phase (Track B) can now begin
- Watson should annotate ~30 minimal pairs using docs/analyst-tone-decision-guide.md
- After annotation, run scripts/promote_tonal_candidates.py and full TCPR

**Blockers:**
- None (all of Track A is complete)

**Questions for Watson or PM:**
- None at this time
```

## Emergency: What to Do If Stuck

1. Check `git status` and `git log --oneline -5` to understand current state.
2. Re-read `SOUL.md` §5 Invariants to ensure you haven't violated any constraints.
3. If a script doesn't exist, check `scripts/` directory for similar scripts.
4. If a data file is missing, check `data/` directory and the relevant operational guide in `docs/`.
5. If a test fails, look at the test file (`tests/`) to understand what went wrong.
6. If you get stuck, write a clear handoff note and stop.

---

## Summary

You are the Senior Dev Agent. Your mission is to complete Track A (A1 through A4) on the `dev` branch. Use `SOUL.md` as your control plane. Respect all invariants. Commit frequently with conventional messages. Stop when done and write a handoff note.

Good luck. 🚀
