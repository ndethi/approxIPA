# Agentic Bootstrap Guide for Hermes and Nemo

This guide describes how to bootstrap an external agentic framework on this Mac for approxIPA, using `SOUL.md` as the control-plane manifest.

## Purpose

The goal is to let either Hermes or Nemo:

1. Read project state from `SOUL.md`.
2. Respect the role and invariant boundaries already defined there.
3. Start with Track A implementation work.
4. Leave a clear handoff note when the session ends.

## Assumptions About This Mac

- The repo lives at `/Users/ndethi/dev/ir/approxIPA`.
- `dev` is the working branch for implementation.
- The project uses script-first execution and tests from the repo root.
- Analyst annotation is deferred to the next-iteration gate, not the first task.

## Bootstrap Sequence

### 1. Open the repo and read the control plane

The framework should read these files first:

- `SOUL.md`
- `docs/paper-plan-waxal.md`
- `docs/analyst-tone-decision-guide.md`
- `docs/waxal-candidate-annotation-workflow.md`
- `docs/README.md`

### 2. Identify the role

Use `SOUL.md` §2 to decide which role is active.

Recommended default for this phase:

- **PM Agent** for task ordering and branch-level coordination.
- **Senior Dev Agent** for Track A implementation.
- **Tester Agent** for validation after each Track A milestone.

### 3. Enforce invariants

Before any action, hard-fail if the proposed step violates one of the following:

- Do not mutate `data/tonal_minimal_pairs.csv` tone or gold IPA fields unless acting as NLP Researcher.
- Do not bypass the script-first execution rule.
- Do not treat analyst annotation as optional for final H1 scoring.
- Do not bypass WAXAL/BibleTTS circularity constraints.

### 4. Select the first task

For this pivot, the first actionable work is Track A.

Recommended order:

1. Expand `data/kikuyu_wordlist.txt`.
2. Regenerate `data/ipa_approximations.jsonl`.
3. Import or validate gold lexicon entries.
4. Harden BibleTTS/WAXAL ingestion and split checks.
5. Run the non-analyst validation suite.

### 5. Execute with repository commands

Use repo-local commands only. The framework should prefer commands like:

```bash
uv sync
python scripts/run_transphone.py
python scripts/extract_lexicon_candidates.py
python scripts/check_waxal_access_and_split.py
python -m pytest tests/ -q
```

When a command is not yet wired, the framework should record the missing step in the session handoff note instead of improvising around it.

## Hermes Setup Pattern

If Hermes is the active framework, treat it as the orchestrator that reads `SOUL.md`, selects the role, and delegates work to subagents.

Minimum Hermes bootstrap steps:

1. Load `SOUL.md`.
2. Load this guide.
3. Create a run plan with Track A tasks only.
4. Check current git branch and working tree state.
5. Execute the first non-blocked Track A task.

Recommended Hermes prompt shape:

```text
Read SOUL.md and docs/agentic-bootstrap-guide.md. Assume the Senior Dev role. Execute Track A only, starting with wordlist expansion and approximation regeneration. Respect all invariants in SOUL.md. Stop and write a handoff note if you hit a blocker.
```

## Nemo Setup Pattern

If Nemo is the active framework, use the same control plane but keep the execution loop explicit and stepwise.

Minimum Nemo bootstrap steps:

1. Parse `SOUL.md` and extract the current state snapshot.
2. Parse the pivot checklist in `SOUL.md`.
3. Select Track A1 as the first task unless it is already complete.
4. Run one task at a time and validate after each task.
5. Record status in a session handoff note.

Recommended Nemo prompt shape:

```text
Use SOUL.md as the control plane. Execute the implementation-first pivot. Do Track A tasks in order, validate after each task, and leave a concise handoff note when complete.
```

## Suggested Session Loop

1. Read the control plane.
2. Choose the current role.
3. Pick the highest-priority non-blocked task.
4. Run the smallest useful command.
5. Validate the result.
6. Update the handoff note.
7. Stop when the task is done or blocked.

## Output Contract

At the end of a run, the framework should report:

- Current branch
- Role selected
- Task completed
- Validation result
- Remaining blockers
- Next recommended task

## Track A Starting Point

The recommended first implementation task is:

- Expand `data/kikuyu_wordlist.txt`.
- Regenerate `data/ipa_approximations.jsonl`.
- Verify that the new outputs are deterministic and reproducible.

That work can begin without analyst input.

## Handoff Note Template

Use this template when the framework stops:

```text
## Session Handoff Note

What I did:
- ...

What I validated:
- ...

What is next:
- ...

Blockers:
- ...

Questions for Watson or PM:
- ...
```
