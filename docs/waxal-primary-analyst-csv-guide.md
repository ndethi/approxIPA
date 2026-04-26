# Primary Analyst Guide: WAXAL CSV Annotation

**Audience:** Primary analyst  
**Purpose:** Fill in the WAXAL candidate rows in `data/tonal_minimal_pairs.csv`  
**Related docs:** [waxal-candidate-annotation-workflow.md](waxal-candidate-annotation-workflow.md)  
**Reviewer guide:** [waxal-second-reviewer-guide-elif.md](waxal-second-reviewer-guide-elif.md)

---

## What this guide is for

This guide tells you exactly what to enter in the CSV and what to leave alone.

The file already contains:

- 3 seed rows at the top
- 100 WAXAL candidate rows below them

Your job is to complete the candidate rows, one row at a time.

---

## What you are inputting

For each candidate row, you are filling in only these fields:

- `tone_a`
- `tone_b`
- `gold_ipa_a`
- `gold_ipa_b`

You may also use:

- `meaning_a`
- `meaning_b`
- `notes`

Only use the optional fields if they help clarify the row.

---

## What you should not change

Do not edit these fields unless you are fixing an obvious formatting problem:

- `word_a`
- `word_b`
- `source`
- `source_id`
- `source_split`
- `status`

Do not change the 3 seed rows.
Do not delete rows.
Do not add new rows.

---

## Which rows to work on

- Row 1: header
- Rows 2-4: seed examples, leave unchanged
- Rows 5-104: candidate rows to annotate

If you are unsure whether a row is a seed or a candidate, leave it and ask for a check.

---

## How to fill each candidate row

For every row you annotate:

1. Look at `word_a` and `word_b`.
2. Decide whether each word is `H` or `L`.
3. Enter those values in `tone_a` and `tone_b`.
4. Write the IPA forms in `gold_ipa_a` and `gold_ipa_b`.
5. Keep the segmental shape the same unless the pair is clearly not valid.
6. If something is uncertain, write a short note in `notes`.

---

## What the tone fields should contain

Use only these values:

- `H`
- `L`

Do not use:

- `High`
- `Low`
- `h`
- `l`
- `H/L`

---

## What the IPA fields should contain

`gold_ipa_a` and `gold_ipa_b` should be the best IPA transcription you can provide for each word.

Keep the transcription consistent with the seed rows:

- use tone marking on vowels
- keep the segmental structure aligned between the two words
- do not leave the IPA fields blank

If you are unsure about a transcription, add a short note rather than guessing silently.

---

## When to use notes

Use `notes` for short comments only when needed.

Examples:

- `check tone assignment`
- `ipa uncertain`
- `pair may not be minimal`
- `needs second review`

Keep notes brief and factual.

---

## Quick self-check before handing off

Before you send the file for review, check that:

- all candidate rows have `tone_a`, `tone_b`, `gold_ipa_a`, and `gold_ipa_b`
- the seed rows are unchanged
- tone values are only `H` or `L`
- `source_id` and `source_split` are still intact
- rows with uncertainty have notes

Then hand the file to Elif using the second-review guide.

---

## Next step after you finish

1. Run validation on the CSV.
2. Give the file to Elif for second review.
3. Fix any rows she flags.
4. Run validation again.
5. Promote approved candidate rows when the file is clean.
