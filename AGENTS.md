<!-- Universal agent entry point. Read by Copilot, Codex, Cursor,
     Jules, Amp, Factory, Hermes, and any agent that follows the
     agentsmd.io open standard. -->

## Project: thiLLMo IPA

A Python research pipeline for IPA phoneme approximation and tonal
contrast evaluation for Kikuyu (`kik`), a low-resource tonal Bantu
language. The end goal is a pronunciation lexicon loadable into TTS
systems that reproduce Kikuyu speech with correct tonal fidelity.

Researcher and native speaker: Watson Ndethi  
Repo: github.com/ndethi/approxipa  
Language: Python 3.11, uv package manager  
Primary metric: TCPR (Tonal Contrast Preservation Rate)

---

## Read these docs first

Before doing any work, read these files in order. They contain design
decisions that are not in the code — violating them silently will
cause your PR to be rejected.


docs/tonal_minimal_pairs_design.md   ← IPA encoding rules, pair criteria
docs/thillmo_ipa_implementation_guide.md  ← full pipeline overview


For the automated setup workflow:

docs/hermes_git_and_skills_guide.md  ← git handoff and skill config


---

## Repo structure


data/
  tonal_minimal_pairs.csv     eval dataset — do not modify without instruction
  kikuyu_wordlist.txt         input wordlist for Transphone
  ipa_approximations.jsonl    Transphone output (word, ipa_yoruba, ipa_swahili)
  thillmo_ipa_gold.csv        500+ manually annotated IPA entries
  bibletss_pair_candidates.csv  mined candidates, Watson verifies
scripts/
  run_transphone.py           batch G2P approximation
  mine_bibletss_pairs.py      BibleTTS corpus candidate miner
  validate_pairs.py           pre-TCPR validation gate
  build_lexicon.py            merge gold + Transphone → CMUdict lexicon
evaluation/
  tcpr.py                     TCPR metric with bootstrap CI
  mos_eval.py                 UTMOS automated MOS evaluation
tests/                        pytest suites — one per script
docs/
  skills/                     Hermes skill snapshots (auto-synced)
  progress/                   daily progress notes (auto-generated)
.github/
  copilot-instructions.md     Copilot-specific supplementary instructions
  agents/                     custom agent profiles (one per role)
    pm.agent.md
    senior-dev.agent.md
    tester.agent.md
    evaluator.agent.md
    research-analyst.agent.md
    writer.agent.md


---

## Domain knowledge — read carefully

Language: Kikuyu (Gĩkũyũ), ISO 639-3 kik. Tonal Bantu,
East Africa. Two level tones: High (H) and Low (L). Also rising (LH)
and downstep, but these are out of Phase 1 scope.

IPA encoding — non-negotiable:
- Acute accent (´) = High tone: á é í ó ú (precomposed Unicode)
- Grave accent (`) = Low tone: à è ì ò ù (precomposed Unicode)
- Never use combining diacritics (U+0301, U+0300). They look identical
  but break the TCPR regex. The validator script enforces this.
- Kikuyu orthographic diacritics (ũ ĩ) mark vowel quality, not tone.
  Do not confuse them with IPA tone marks.

TCPR — the primary metric:
TCPR = preserved tonal minimal pairs / total primary pairs evaluated.
WER is a secondary metric and is tonally blind — never cite it as
the primary result.

Native speaker authority:
Watson Ndethi is a native Kikuyu speaker. On any tonal question
his judgment supersedes literature sources and agent outputs.
The status field in tonal_minimal_pairs.csv is set only by Watson:
- primary — verified, included in TCPR
- unverified — candidate, Watson has not reviewed yet
- disputed — conflict between literature and speaker judgment
- archaic — real but not in active use
Never set status: primary in a task. Watson sets that manually.

Participatory design:
The research involves a Kikuyu community. Speaker verification in
Phase 1 is done by Watson alone. Community participatory validation
is planned future work. Do not imply it is complete in any output.

---

## Branch and commit conventions
- Branch naming: task/<short-slug> for all work
- Never push directly to main
- Always open a PR for Watson's review
- Conventional commit format:
  - feat: new scripts or features
  - docs: documentation changes
  - fix: bug fixes
  - test: test additions or changes
  - chore: config, tooling

---

## Running the pipeline


# Setup
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -e .

# Validate pairs before running TCPR
python scripts/validate_pairs.py        # exit 1 on BLOCKING issues

# Run Transphone approximation
python scripts/run_transphone.py

# Run TCPR evaluation
python evaluation/tcpr.py

# Run tests
pytest tests/ -q


The validator is a gate — run_transphone.py and tcpr.py should
only run if validate_pairs.py exits 0.

---

## Key libraries and usage patterns


# Transphone — cross-lingual G2P
from transphone.run import read_tokenizer, tokenize
model = read_tokenizer('yor')   # Yoruba-weighted
ipa = tokenize(word, model, lang='kik', force_approximate=True)

# ByT5 — neural G2P fine-tuning
from transformers import T5ForConditionalGeneration, AutoTokenizer
model = T5ForConditionalGeneration.from_pretrained('google/byt5-small')

# MMS-VITS TTS baseline
from transformers import VitsModel, AutoTokenizer
model = VitsModel.from_pretrained('facebook/mms-tts-kik')

# WAXAL dataset
from datasets import load_dataset
ds = load_dataset('google/waxal', 'kik', split='train')


---

## Dev team agent roles

Custom agent profiles live in .github/agents/. Point any agent at
this repo and the appropriate profile activates based on the task.

| Role | Profile file | Activates for |
|------|-------------|---------------|
| PM | pm.agent.md | spec writing, task decomposition |
| Senior Dev | senior-dev.agent.md | Python script implementation |
| Tester | tester.agent.md | pytest suites, bug reports |
| Evaluator | evaluator.agent.md | TCPR interpretation, results |
| Research Analyst | research-analyst.agent.md | literature extraction |
| Writer | writer.agent.md | documentation, READMEs |

For Hermes-specific setup, see docs/hermes_dev_team_guide.md.
For the automated self-setup workflow, see docs/hermes_git_and_skills_guide.md
and open thillmo_setup_issue.md on GitHub to activate the task manifest.

---

## Scope discipline

This is a research codebase. Scope discipline is critical for
reproducibility. When implementing any task:

1. Do exactly what the spec says. No extra features.
2. If the spec is ambiguous, make the simplest assumption,
   note it in an IMPLEMENTATION NOTES comment block, and proceed.
3. Do not ask clarifying questions. Act on the simplest interpretation.
4. Single script per task unless the spec requires multiple files.
5. No logging frameworks — use print() with [INFO] [WARN] [ERROR].
6. Every function gets a docstring.

---

*thiLLMo IPA | Watson Ndethi | April 2026*
*github.com/ndethi/approxipa*
