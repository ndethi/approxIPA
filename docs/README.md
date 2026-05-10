# Docs

This directory holds the reference materials for approxIPA.

## Design & Planning Documents

- [approxIPA-research-proposal.docx](approxIPA-research-proposal.docx)
- [approxIPA-implementation-guide.docx](approxIPA-implementation-guide.docx)
- [paper-plan-waxal.md](paper-plan-waxal.md)
- [tonal-minimal-pairs-design.md](tonal-minimal-pairs-design.md) — Tonal pair dataset design conventions and rationale

## Operational & Workflow Guides

- [**analyst-tone-decision-guide.md**](analyst-tone-decision-guide.md) — **READ FIRST** before annotating WAXAL candidates: the H/L decision rule, the orthography trap (tilde/macron are segmental, not tonal), rejection protocol, and worked examples
- [waxal-primary-analyst-csv-guide.md](waxal-primary-analyst-csv-guide.md) — Short guide for the primary analyst filling in `data/tonal_minimal_pairs.csv`
- [waxal-candidate-annotation-workflow.md](waxal-candidate-annotation-workflow.md) — Full annotation workflow for WAXAL candidate pairs (read after the decision guide)
- [waxal-second-reviewer-guide-elif.md](waxal-second-reviewer-guide-elif.md) — Simple non-technical second-pass review checklist for Elif
- [tonal-pair-source-access.md](tonal-pair-source-access.md)
- [gold-standard-source-decision.md](gold-standard-source-decision.md)
- [gold-standard-operational-plan.md](gold-standard-operational-plan.md)
- [gold-standard-bibletts-fallback.md](gold-standard-bibletts-fallback.md)
- [bibletts-operational-plan.md](bibletts-operational-plan.md)
- [bibletts-hf-access-status.md](bibletts-hf-access-status.md)
- [bibletts-source-verification.md](bibletts-source-verification.md)
- [waxal-non-circular-fallback.md](waxal-non-circular-fallback.md)
- [agentic-bootstrap-guide.md](agentic-bootstrap-guide.md) — Framework-agnostic bootstrap guide for Hermes or Nemo on this Mac, with SOUL-driven startup and Track A execution flow

## Operational Scripts Related to These Docs

- `scripts/check_waxal_access_and_split.py`
- `scripts/ingest_waxal_hf.py`

---

**Note:** The OPIT proposal is intentionally not included here because it belongs to a different project.