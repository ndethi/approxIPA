# WAXAL Candidate Annotation Workflow

**Project:** thiLLMo IPA / TCPR Evaluation Framework  
**Author:** Watson Ndethi  
**Date:** April 2026  
**Related docs:** [tonal-minimal-pairs-design.md](tonal-minimal-pairs-design.md)  
**Data file:** `data/tonal_minimal_pairs.csv`  

---

## Overview

This document describes the workflow for a Kikuyu language analyst to annotate the 100 WAXAL-sourced tonal pair candidate rows that have been automatically generated and added to the tonal minimal pairs evaluation dataset.

### What These Candidates Are

The 100 new candidate rows were mined from the WAXAL (Wikimedia Audio Lexicon) Kikuyu dataset through an automated variant-pairing process:

1. **Variant detection:** Words in WAXAL text are grouped by their base form (same segmental structure, different tone diacritics)
2. **Pair generation:** All combinations of tonal variants from the same base form are proposed as minimal pair candidates
3. **Split assignment:** Candidates are deterministically assigned to construction or evaluation splits for reproducible partitioning
4. **Safety checks:** Only candidates from the construction split are included here (evaluation-split candidates are held separately)

### Expected Annotation Scope

- **100 candidate rows** in the CSV spanning approximately **50-70 distinct base forms**
- Each row requires annotation of **4 fields**: `tone_a`, `tone_b`, `gold_ipa_a`, `gold_ipa_b`
- Estimated time: **1-2 hours** for an analyst with Kikuyu phonological knowledge
- No other rows should be modified; seed rows are locked in place

---

## Part 1: Understanding the CSV Structure

### Row Types

**Seed rows (3 total):**
- Already complete with all annotations
- Examples of correctly annotated pairs which serve as reference
- Located at top of CSV for easy reference
- Status: `evaluable`

**Candidate rows (100 total):**
- Automatically generated from WAXAL variant pairing
- Require manual tone and IPA annotation
- Status: `candidate`
- Source: `waxal` (with source_id and source_split fields that are pre-filled)

### Required and Provided Fields

| Field | Pre-filled? | Requirement | Example |
|-------|-------------|-------------|---------|
| `word_a` | ✓ Yes | Orthographic form with tone diacritics | mũndũ |
| `word_b` | ✓ Yes | Orthographic form with tone diacritics | mundu |
| `tone_a` | ✗ **ANNOTATE** | Single character: `H` or `L` | H |
| `tone_b` | ✗ **ANNOTATE** | Single character: `H` or `L` | L |
| `meaning_a` | ✓ Optional | Meaning in English or Swahili | person |
| `meaning_b` | ✓ Optional | Meaning in English or Swahili | person (other sense) |
| `gold_ipa_a` | ✗ **ANNOTATE** | IPA form with tone marking | ˈmũ.ndṹ |
| `gold_ipa_b` | ✗ **ANNOTATE** | IPA form with tone marking | ˈmu.ndù |
| `source` | ✓ Yes | Always `waxal` | waxal |
| `source_id` | ✓ Yes | Deterministic pair identifier | waxal:mundu:mundu:mũndũ |
| `source_split` | ✓ Yes | Always `construction` (evaluation rows filtered out) | construction |
| `status` | ✓ Yes | Always `candidate` until evaluation | candidate |
| `notes` | ✓ Optional | Empty; for analyst comments | |

---

## Part 2: Reference — Using Seed Rows as Examples

Before annotating, open the CSV and locate the **3 seed rows at the top** (rows 2-4 of the CSV, after header).

### Seed Row Example Format

```
word_a:    njūkì
word_b:    njuki
tone_a:    H
tone_b:    L
gold_ipa_a: n.ˈdʒũ.kí (or detailed form)
gold_ipa_b: n.ˈdʒu.kì
meaning_a: (Kikuyu meaning)
meaning_b: (Kikuyu meaning)
```

**Note the key observations:**

1. **Base form alignment:** Both words share the same segmental structure (n-dʒ-u-k-i or n-j-u-k-i)
2. **Tone differences:** The words differ only in tonal diacritics on the vowels
3. **IPA representation:** 
   - High tone marked with acute accent: `í` (or combining acute on `i`)
   - Low tone marked with grave accent: `ì` (or combining grave on `i`)
4. **Meaning notes:** Both meanings are present to distinguish senses

### Identifying Tone from Orthography

Look at the orthographic forms (`word_a` and `word_b`) to determine the tones:

- **High tone (H):** Marked with acute accent or upper tone mark in Kikuyu orthography: `á`, `é`, `í`, `ó`, `ú`, etc. and their long vowel versions
- **Low tone (L):** Marked with grave accent or lower tone mark: `à`, `è`, `ì`, `ò`, `ù`, etc. and their long vowel versions
- **Unmarked vowels:** Treated as a third tone in standard Kikuyu but Phase 1 focuses on H vs. L contrasts

---

## Part 3: Step-by-Step Annotation Process

### Workflow Overview

For each of the 100 candidate rows:

1. **Examine** the orthographic forms in `word_a` and `word_b`
2. **Extract tone** from the diacritics (H for acute/high mark, L for grave/low mark)
3. **Record tone values** in `tone_a` and `tone_b` columns
4. **Construct IPA forms** using segmental and syllabic rules for Kikuyu
5. **Mark tones in IPA** using acute and grave accents on vowels
6. **Validate** against seed row examples for consistency
7. **Optional:** Add meaning notes if you know them; leave blank otherwise

### Detailed Instructions for Your Annotation Tool

#### Step 1: Identify the Tonal Diacritics

For the pair, look at each word:

**Example pair:**
- `mũndũ` (has acute marks on both vowels: ũ and ũ → both H)
- `mundu` (has grave mark on second vowel: u → L, first u is unmarked)

**Your determination:**
- `word_a` = mũndũ → tone_a = H (both vowels H, contour = H)
- `word_b` = mundu → tone_b = L (has L mark, or downstep from H to L contour)

**Note:** In Kikuyu, the tonal category is typically assigned at the word level (noun class) rather than per vowel. Focus on the overall tonal class of the word.

#### Step 2: Construct IPA Forms

Use standard Kikuyu segmental phonology:

| Orthography | IPA Segment |
|---------|---------|
| c | [tʃ] (mid/high back unrounded) or [tʃ] (palatal) |
| j | [dʒ] (palatal affricate) |
| ny | [ɲ] (palatal nasal) |
| th | [tʰ] or [t̚] (aspirated or plain t) |
| ch | [tʃ] (palatal affricate) |
| vowels | [a e i o u ɪ ʊ] (IPA vowel set) |
| long vowels | Use [aː eː iː oː uː] or [a: e: i: o: u:] |

**Steps for IPA construction:**

1. Convert each orthographic segment to IPA equivalent
2. Identify syllable boundaries (mora-based)
3. Add stress marker (typically primary stress on first or penultimate mora): `ˈ`
4. Add tone diacritics to the vowel nucleus of each tonal bearing unit:
   - H tone: acute accent on vowel (á, é, í, ó, ú) or combining acute (a + U+0301)
   - L tone: grave accent on vowel (à, è, ì, ò, ù) or combining grave (a + U+0300)

**Example:**

```
Orthography:  mũndũ (H tone word)
Segmental:    m + u + n + d + u
IPA without tone: [mu.ndu]
With stress:  [ˈmu.ndu]
With H tone on each mora: [ˈmú.ndú]
```

```
Orthography:  mundu (L tone word)
Segmental:    m + u + n + d + u
IPA without tone: [mu.ndu]
With stress:  [ˈmu.ndu]
With L tone on each mora: [ˈmù.ndù]
```

#### Step 3: Fill in the Fields

In your spreadsheet/CSV editor:

1. Find the candidate row (rows 5-104)
2. For row N:
   - Column `tone_a`: Type the single character determined above (H or L)
   - Column `tone_b`: Type the single character determined above (H or L)
   - Column `gold_ipa_a`: Type the IPA form with tone marks
   - Column `gold_ipa_b`: Type the IPA form with tone marks
3. Leave `meaning_a` and `meaning_b` blank unless you have reliable gloss data
4. Leave `notes` blank unless problematic (see validation below)

#### Step 4: Validate Each Pair

Before moving to the next row, check:

- **Tone values are single characters:** Either `H` or `L`, not `H/L` or `h` or `high`
- **IPA forms use correct vowel inventory:** Compare to seed row IPA
- **Tone diacritics present:** Both H and L forms should have diacritics on vowels
- **Consistent segmentalization:** Same number of phonemes/syllables in both IPA forms
- **Forms differ only in tone:** The IPA pair should be identical except for diacritics

**Validation failures** (mark in `notes` column):

- If the words don't form a true minimal pair (segmental content differs significantly)
- If you cannot reliably determine the tone (ambiguous orthographic marking)
- If the word is a loan word or non-Kikuyu cognate (and you're excluding those)
- If the IPA transcription is uncertain due to dialectal variation

---

## Part 4: Use of Reference Materials

You should have available:

1. **This CSV itself:** The seed rows (top 3) are your reference examples
2. **[tonal-minimal-pairs-design.md](tonal-minimal-pairs-design.md):** Explains the design rationale, tone conventions, and IPA encoding
3. **Kikuyu word lists and dictionaries:** For meanings and segmental validation
4. **IPA chart:** For segment-to-IPA mapping reference
5. **This workflow document:** (which you're reading now)

### Consulting References

- **For segment-to-IPA mappings:** See the table above or refer to your IPA training
- **For tone assignment:** Look at the orthographic diacritics in word_a and word_b relative to the seed rows
- **For meaning validation:** Consult Kikuyu lexical resources (this is optional; good to have but not required)
- **For phonotactic plausibility:** Check against Kikuyu syllable structure rules (CVVC, CV-V, etc.)

---

## Part 5: Quality Assurance

### Self-Check Before Submission

After completing all 100 rows, scan the CSV for:

1. **No empty cells in required fields:**
   - tone_a, tone_b, gold_ipa_a, gold_ipa_b should have values for all 100 candidate rows
   - Seed rows should be unchanged

2. **Consistent tone marking across all rows:**
   - All H tone vowels use acute accent (á, é, í, ó, ú)
   - All L tone vowels use grave accent (à, è, ì, ò, ù)
   - No mixed styles (e.g., some rows using macron for long vowels, others using colons)

3. **No stray characters in tone columns:**
   - tone_a and tone_b contain only `H` or `L` (case-sensitive uppercase)
   - No spaces, typos, or alternative representations

4. **Seed row integrity:**
   - Rows 2-4 (the 3 seed rows) are completely unmodified
   - This ensures the reference data is preserved

5. **Row count unchanged:**
   - CSV should have 104 rows (1 header + 3 seed + 100 candidates)
   - No rows deleted or added

### Automated Validation

Once you've completed annotation, run:

```bash
python -m evaluation.validate_tonal_minimal_pairs data/tonal_minimal_pairs.csv
```

This will check:

- ✓ All candidate rows have non-empty tone and IPA fields
- ✓ tone_a and tone_b values are in {H, L}
- ✓ IPA forms contain tone marking (diacritics present)
- ✓ No rows with invalid status
- ✓ Seed rows remain evaluable and unchanged

If validation fails, the error message will indicate which row(s) and field(s) need correction.

---

## Part 6: Submission and Next Steps

### What to Submit

1. **Completed CSV:** `data/tonal_minimal_pairs.csv` with all 100 candidate rows annotated
2. **Optional summary:** A brief note of any problematic pairs you marked in the `notes` column and your reasoning

### What Happens Next

1. **Validation run:** Your annotations are validated for consistency and completeness
2. **Spot checking:** A second analyst may review a random sample for agreement
3. **Promotion to evaluable:** Confirmed candidate rows graduate to `status=evaluable` for TCPR metric evaluation
4. **Phase 2 planning:** Results will inform decisions about rising-tone pairs and downstep annotation

---

## Part 7: Troubleshooting

### Common Issues and Solutions

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Unsure of tone from orthography | Diacritics unclear or ambiguous | Consult the CSV seed rows; look for words with similar patterns in your Kikuyu knowledge |
| Don't know the English meaning | Meaning not in your vocabulary | Leave `meaning_a` and `meaning_b` blank; they are optional |
| Word doesn't look like a real Kikuyu word | Plausibility concern | Add a note in the `notes` column (e.g., "appears to be Swahili loanword") |
| Segmental structure differs between word_a and word_b | Possible erroneous pairing | Mark in `notes` and annotate the IPA anyway; validator will flag if it's a concern |
| IPA convention unclear (which tone mark to use?) | Uncertainty about diacritic choice | Refer to [tonal-minimal-pairs-design.md](tonal-minimal-pairs-design.md), Section 3, which specifies acute (H) and grave (L) on vowels |
| Spreadsheet freezing or slow to edit | Large file or software limitation | Save frequently; consider annotating in chunks if needed |

### Getting Help

If you encounter:

- **Phonological uncertainty:** Consult Kikuyu linguistic literature (Armstrong 1967, Clements & Ford 1981)
- **Technical issues:** Check the `[tonal-minimal-pairs-design.md](tonal-minimal-pairs-design.md)` document
- **Validation errors:** The error message will tell you which row and field failed; review that cell

---

## Summary Checklist

Before you begin annotation:

- [ ] Read [tonal-minimal-pairs-design.md](tonal-minimal-pairs-design.md) for context and conventions
- [ ] Open `data/tonal_minimal_pairs.csv` in your spreadsheet editor
- [ ] Review the 3 seed rows (rows 2-4) as reference
- [ ] Confirm you have Kikuyu language resources available
- [ ] Understand the tone and IPA notation (acute = H, grave = L)

During annotation (for each row 5-104):

- [ ] Extract tone from orthographic diacritics (word_a, word_b)
- [ ] Determine tone_a and tone_b values (H or L)
- [ ] Construct segmental IPA form from orthography
- [ ] Add tone marking using acute/grave on vowils
- [ ] Fill gold_ipa_a and gold_ipa_b
- [ ] Spot-check against seed rows for consistency
- [ ] Flag problematic pairs in `notes` if needed

After annotation:

- [ ] Verify all 100 candidate rows are complete (no empty cells in required fields)
- [ ] Verify seed rows unchanged (rows 2-4)
- [ ] Run `python -m evaluation.validate_tonal_minimal_pairs data/tonal_minimal_pairs.csv`
- [ ] Resolve any validation errors
- [ ] Submit completed CSV

---

**Done?** Great! Your annotations will now be evaluated against Transphone IPA approximations to measure the Tonal Contrast Preservation Rate (TCPR) metric for Kikuyu TTS systems.
