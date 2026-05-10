# Analyst Tone Decision Guide — Kikuyu H/L Annotation

**Audience:** the native-speaker analyst filling in `tone_a`, `tone_b`,
`gold_ipa_a`, `gold_ipa_b` for the 100 candidate rows in
`data/tonal_minimal_pairs.csv`.

**Read this before** `waxal-candidate-annotation-workflow.md`. The workflow
doc tells you to read tone off the orthographic diacritics. For the
WAXAL-mined candidates that instruction is misleading and will produce
incorrect annotations. This document gives you the correct decision rule.

---

## 1. The orthography trap

Standard Kikuyu writing uses five different diacritics on vowels. Only two
of them mark **tone**. The others mark vowel quality or vowel length and
must not be treated as tone.

| Diacritic     | Examples  | What it actually marks                        | Tonal?                    |
|---------------|-----------|-----------------------------------------------|---------------------------|
| Acute  (´)    | á í ú     | High tone                                     | **Yes — H**               |
| Grave  (`)    | à ì ù     | Low tone                                      | **Yes — L**               |
| Tilde  (~)    | ĩ ũ       | Central/lax vowel quality (ĩ = /ɪ/, ũ = /ʊ/) | No — segmental            |
| Macron (¯)    | ā ī ū     | Vowel length                                  | No — segmental            |
| Circumflex (^)| â î û     | Inconsistent in WAXAL; sometimes falling tone | Out of Phase 1 scope      |

The candidate-mining script did not encode this distinction. It grouped
words by stripping every diacritic, so it produced "tonal variant" pairs
that are in fact orthographic variants, segmental contrasts, or length
contrasts. **Most of those rows must be rejected.** That is expected, not a
problem with your work.

---

## 2. Reframe the question

The workflow doc asks: *what tone is marked on the vowels of `word_a` and
`word_b`?*

For these candidates the right question is:

> **Are `word_a` and `word_b` two distinct Kikuyu lexemes that I, as a
> Kikuyu speaker, recognise as having different meanings AND identical
> segmental content (same consonants, same vowel qualities, same vowel
> lengths)?**

If yes → it is a real minimal pair → assign H/L from your **lexical
knowledge of each word**, not from the spelling.

If no → it is not a tonal minimal pair → reject the row and move on.

This is consistent with `tonal-minimal-pairs-design.md` §4, criteria 1–4:
segmental identity, tonal contrast, semantic distinctness, speaker
verification. You are the speaker verifier (proposal §4 / design doc §4
Criterion 4); your judgement overrides the WAXAL spelling.

---

## 3. Decision tree (run this for every candidate row)

### Step A — Are these two real, distinct Kikuyu lexemes?

Read both forms aloud as you would say them. Then:

- **Same word, two spellings** (typical: WAXAL annotators differing on
  whether to write the central vowel as `ũ` or as `ú`) → **REJECT**.
  Set `notes = orthographic-variant; same-lexeme`. Leave tone and IPA
  fields blank. Keep `status = candidate`.
- **One side is not a real Kikuyu word** → **REJECT**.
  Set `notes = non-lexeme`. Leave tone and IPA blank. Keep
  `status = candidate`.
- **Two different real lexemes with different meanings** → continue.

### Step B — Are the segments identical once you ignore tone marks?

Mentally strip acute and grave from both forms and compare what remains.

- `i` vs `ĩ`, `u` vs `ũ` → **different vowels** (front vs central,
  back vs central). Pairs like `aingì` / `aingĩ` differ in vowel quality
  in addition to (or instead of) tone → **REJECT**. Set
  `notes = segmental-difference; tilde-is-vowel-quality`.
- `u` vs `ū`, `i` vs `ī` → length contrast, not tone → **REJECT**.
  Set `notes = segmental-difference; macron-is-length`.
- One side has a circumflex (`â î û`) → **REJECT** for Phase 1.
  Set `notes = circumflex-out-of-phase1-scope`.
- Otherwise (segments match) → continue.

A useful shortcut: **only acute-vs-grave pairs with otherwise-identical
spelling are eligible for Phase 1 annotation.** Tilde-anything,
macron-anything, and circumflex-anything are all rejections.

### Step C — Assign H or L from your speaker knowledge

For each accepted row:

- For `word_a`, recall how you say this word. Is the relevant
  tone-bearing syllable HIGH or LOW in your speech? Set `tone_a = H`
  or `tone_a = L`.
- Same for `word_b`. The two values must differ (the validator
  enforces `tone_a != tone_b`).
- If your speaker judgement disagrees with the orthographic mark
  (e.g. WAXAL writes `aingí` but you produce it L), **trust your
  speech** and add `notes = orthography-disagrees-with-speaker`.
  These cases are paper-quality evidence about WAXAL transcription
  noise; please flag them.

If a word has more than one tone-bearing syllable, assign H or L based
on the **contrastive syllable** — the one whose tone differs between
`word_a` and `word_b`. The IPA gold strings will encode the contrast
on that syllable; the row-level `tone_a` / `tone_b` summarises which
side is high and which is low at that position.

### Step D — Write the gold IPA

For each accepted row:

1. Strip both words back to their bare segmental form (no diacritics).
2. Convert to IPA segment by segment using the table in
   `waxal-candidate-annotation-workflow.md` Part 3 Step 2.
3. Place **only** acute (´, U+0301) for H and grave (`, U+0300) for L
   on the tone-bearing vowel. Use precomposed Unicode (e.g. `á` =
   U+00E1) per the design doc §3 encoding hygiene rule.
4. **Do not** put circumflex (`^`) or macron (`¯`) anywhere in
   `gold_ipa_a` / `gold_ipa_b` for Phase 1. The validator strips both
   characters as if they were tone marks
   (`evaluation/validate_tonal_minimal_pairs.py:19`), which will produce
   confusing failures if they appear in your IPA.
5. The two gold IPAs must be **identical except for the H/L diacritic
   on the contrastive vowel**. The validator enforces this.

### Step E — Fill `meaning_a` and `meaning_b`

Optional under the schema, but **strongly recommended for accepted rows**.
A short English (or Swahili) gloss for each word is the only auditable
evidence that the pair is a *semantic* minimal pair, not a spelling
artefact. One or two words is enough.

---

## 4. Worked examples (from real candidate rows)

### REJECT — segmental difference (tilde marks vowel quality, not tone)

```
aingì | aingĩ      → notes = segmental-difference; tilde-is-vowel-quality
arì   | arĩ        → same reason
andù  | andũ       → same reason
```

### REJECT — vowel length (macron marks length, not tone)

```
gatatù | gatatū    → notes = segmental-difference; macron-is-length
arûme  | arūme     → same reason (also: circumflex on the other side)
```

### REJECT — circumflex (out of Phase 1 scope)

```
aingì | aingî      → notes = circumflex-out-of-phase1-scope
gatatù | gatatû    → same reason
```

### REJECT — likely orthographic variant of the same lexeme

```
búrúri | bũrũri    → if both are "country" /βʊrʊrɪ/ written two ways:
                     notes = orthographic-variant; same-lexeme
```

Adjudicate by your speaker judgement: does `búrúri` denote a different
lexeme to you than `bũrũri`, or are they the same word with a different
diacritic convention? Most acute-only-vs-tilde-only pairs in WAXAL are
the same lexeme.

### ACCEPT — clean acute vs grave on identical segments

```
aingì | aingí      → tone_a=L, tone_b=H
                     gold_ipa_a, gold_ipa_b: identical except grave on
                     the contrastive vowel of a, acute on b
                     meaning_a, meaning_b: fill if you can identify the
                     two lexemes; otherwise leave blank and add
                     notes = meanings-pending
arì   | arí        → same shape
gìa   | gía        → same shape
```

If you cannot identify two distinct meanings for an acute-vs-grave pair,
treat it as a likely same-lexeme reject rather than forcing an annotation.
Honest rejection is better than a guessed minimal pair.

---

## 5. Expected reject rate and why that is fine

A first pass over the 100 candidates will likely reject **60–75 rows**
(tilde, macron, circumflex, and same-lexeme cases). The remaining
~25–40 acute-vs-grave pairs are the candidates worth your annotation
time.

This is the right outcome. The TCPR metric needs a clean small set far
more than it needs a noisy large one. A Phase 1 result that reports
*TCPR = X on N=30 verified pairs* is a stronger paper claim than
*TCPR = Y on N=100 noisy candidates*. The proposal's H1 (TCPR ≥ 0.80) is
testable on N≈30 with a reasonable bootstrap CI; design doc §7 already
anticipates this.

---

## 6. Recommended workflow (90–120 minutes total)

1. **Pass 1 — Triage (30–40 min).** Walk through every candidate row.
   For obvious rejects (tilde, macron, circumflex, same-lexeme),
   write a short `notes` value. Leave `tone_a`, `tone_b`, `gold_ipa_a`,
   `gold_ipa_b` blank. Keep `status = candidate`. The promote script
   will simply skip these.
2. **Pass 2 — Annotate accepts (40–60 min).** For each row you
   accepted, fill `tone_a`, `tone_b`, `gold_ipa_a`, `gold_ipa_b`,
   plus brief `meaning_a` and `meaning_b`.
3. **Pass 3 — Validate (10 min).** Run

   ```bash
   python -m evaluation.validate_tonal_minimal_pairs data/tonal_minimal_pairs.csv
   ```

   The validator only enforces non-empty tone/IPA on rows whose
   `status` is not `candidate`, so your rejected rows will pass
   silently as long as you left their status as `candidate`. Fix any
   errors flagged on your accepted rows.
4. **Pass 4 — Promote (5 min).** Run

   ```bash
   python scripts/promote_tonal_candidates.py --pairs-csv data/tonal_minimal_pairs.csv
   ```

   This graduates fully annotated rows to `status = evaluable` and
   leaves your rejects untouched at `status = candidate`. They will
   not enter the TCPR calculation.

---

## 7. When in doubt

- **You are the ground truth.** The proposal designates Watson Ndethi
  as the Phase 1 verifier (Kikuyu, Gĩkũyũ, Kiambu region; design doc
  §4 Criterion 4). Your speaker judgement overrides the WAXAL
  spelling whenever they conflict.
- **Reject liberally.** Phase 1 is a quality-first sample. If you
  doubt a pair, reject it with a one-line `notes` entry. Phase 2 will
  revisit.
- **Document disagreements.** Every time your speaker judgement
  conflicts with the orthography, leave a brief `notes` entry. These
  notes become evidence in the paper that WAXAL transcription is
  inconsistent on tone — a substantive finding in its own right.

---

*thiLLMo IPA Project | Kikuyu H/L annotation decision guide*
