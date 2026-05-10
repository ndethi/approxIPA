# Second Reviewer Guide (Elif)

**Audience:** Non-technical reviewer  
**Project stage:** After analyst annotation of WAXAL candidate rows  
**Primary file to review:** `data/tonal_minimal_pairs.csv`

---

## Goal

Your job is to do a quick quality pass on the newly annotated candidate rows.

You are not expected to write code or run scripts.
You are checking for clarity, consistency, and obvious mistakes before final approval.

---

## What You Need To Check

Review the 100 candidate rows only:

- Candidate rows are rows **5 to 104** (row 1 is header; rows 2-4 are seed examples).
- Seed rows (2-4) are reference rows and should not be changed.

For each candidate row, confirm:

1. `tone_a` and `tone_b` are filled and contain only `H` or `L`.
2. `gold_ipa_a` and `gold_ipa_b` are not blank.
3. The pair still looks like the same base word with tonal variation (not clearly different words).
4. `source` is `waxal` and `source_split` is `construction`.
5. `status` remains `candidate` (do not change it yet).
6. Notes are present for any doubtful row.

---

## Simple Decision Rules

Mark a row as **OK** if:

- all required fields are present,
- the pair appears plausible,
- and nothing looks inconsistent with nearby rows.

Mark a row as **Needs Follow-up** if:

- tone values are missing or not `H`/`L`,
- IPA is missing,
- pair appears segmentally different (not really minimal-like),
- or the meaning/notes suggest uncertainty.

Use the `notes` column to record short comments like:

- `review: check tone assignment`
- `review: ipa missing`
- `review: pair may not be minimal`

---

## What Not To Change

- Do not edit rows 2-4 (seed rows).
- Do not delete rows.
- Do not change `source_id` values.
- Do not change `source_split` values.
- Do not promote `status` from `candidate` to `evaluable` yourself.

---

## Expected Output From You

At the end, provide a short handoff note with:

1. How many rows looked OK
2. How many rows need follow-up
3. Top 3 recurring issues (if any)

Template:

```
Second review complete (Elif)
- OK rows: __
- Needs follow-up rows: __
- Common issues:
  1) __
  2) __
  3) __
```

---

## If You Have Time (Optional)

Do a quick consistency scan:

- Are there repeated patterns where one side is always H and the other always L?
- Are there rows with obviously malformed IPA symbols?
- Are reviewer notes clear enough for the analyst to fix quickly?

---

## Escalation

If many rows are problematic (for example more than 15), stop and flag the dataset for analyst rework before final evaluation.

This keeps the evaluation set reliable and avoids spending time on low-quality entries.
