# Launch Hermes for Track A Implementation

Use this prompt to invoke Hermes and start Track A implementation.

## Exact Prompt to Use

```text
Read HERMES_INSTRUCTIONS.md from the repo at /Users/ndethi/dev/ir/approxIPA.
Also read SOUL.md as your control plane.
Execute Track A (tasks A1 through A4) as the Senior Dev Agent.
Work on the `dev` branch.
Commit frequently with conventional messages.
When you hit a blocker or complete all tasks, write a handoff note.
```

## What Happens Next

Hermes will:

1. Clone or pull the repo.
2. Checkout the `dev` branch.
3. Read HERMES_INSTRUCTIONS.md and SOUL.md.
4. Understand that it is the Senior Dev Agent.
5. Execute Track A tasks in order (A1, A2, A3, A4).
6. Commit each task with a semantic message.
7. Validate outputs with tests and reproducibility checks.
8. Write a handoff note when complete.

## Repo State

- `dev` branch is clean and ready.
- All guidance documents are present and committed.
- No implementation work has started (ready for Hermes to begin).

## After Hermes Finishes

Track B (analyst annotation) can begin. See SOUL.md for the next-iteration gate definition.
