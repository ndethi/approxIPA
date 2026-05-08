<!-- Supplementary to AGENTS.md at repo root.
     Both files are read by Copilot. AGENTS.md takes primary precedence.
     This file adds Copilot-specific behaviour, agent profiles, and
     the setup workflow entry point. -->

## Entry point for Copilot coding agent

When you are assigned to this repo for the first time, do this before
anything else:

1. Read AGENTS.md at the repo root. It contains domain knowledge,
   IPA encoding rules, and project conventions that are not negotiable.

2. Read docs/tonal_minimal_pairs_design.md. It defines the evaluation
   dataset schema and the four criteria for a valid minimal pair.

3. Check whether docs/skills/ contains SKILL.md files. If it does,
   load the relevant one before starting any task.

4. If you have been asked to "set up the infrastructure" or "run the
   setup", read docs/hermes_git_and_skills_guide.md and look for
   a GitHub Issue titled "Hermes Self-Setup: thiLLMo IPA Infrastructure"
   in the repo issues. If it exists, execute it as a task manifest
   (checkboxes in order, human gates respected).

---

## Custom agent profiles

Copilot cloud agent can activate role-specific profiles from
.github/agents/. These are available when you assign issues
or tasks to specific roles in this repo.

Assign the appropriate profile based on the task type:
- Writing or updating Python scripts → senior-dev
- Writing tests → tester
- Interpreting evaluation results → evaluator
- Extracting data from literature → research-analyst
- Writing documentation → writer
- Decomposing a task into a spec → pm

---

## Path-specific instructions

These apply automatically when Copilot is working on files in
the corresponding paths. See .github/instructions/ for the files.

| Path pattern | Instructions file |
|---|---|
| scripts/**/*.py | .github/instructions/scripts.instructions.md |
| evaluation/**/*.py | .github/instructions/evaluation.instructions.md |
| tests/**/*.py | .github/instructions/tests.instructions.md |
| data/*.csv | .github/instructions/data.instructions.md |

---

## Copilot code review behaviour

When reviewing PRs in this repo, flag as BLOCKING:
- Any IPA string using combining diacritics instead of precomposed
  Unicode (U+0301 or U+0300 instead of á à etc.)
- Any script missing a main() function or if __name__ guard
- Any script using a logging framework instead of print()
- Any PR that sets status: primary in tonal_minimal_pairs.csv
  (this is Watson's manual step — never automated)
- Any script without docstrings on every function

Flag as MINOR:
- Missing IMPLEMENTATION NOTES comment block at end of script
- Conventional commit message not followed
- Missing edge case handler listed in the spec

---

## MCP servers available to Copilot agents in this repo


mcp_servers:
  github:
    url: https://api.githubcopilot.com/mcp/


Use the GitHub MCP server for all repo operations — branch creation,
file commits, PR management. Do not use raw git shell commands
unless the MCP server is unavailable.

---

*thiLLMo IPA | Watson Ndethi | April 2026*
