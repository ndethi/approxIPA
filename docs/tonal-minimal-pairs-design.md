# Tonal Minimal Pairs Dataset — Design Decisions

**Project:** thiLLMo IPA / TCPR Evaluation Framework  
**Author:** Watson Ndethi  
**Date:** April 2026  
**Status:** v1.0 — First pass, H/L only  
**Location in repo:** `docs/tonal_minimal_pairs_design.md`  
**Companion file:** `data/tonal_minimal_pairs.csv`

---

## Purpose of this document

This document records every design decision made in constructing
`tonal_minimal_pairs.csv` — the evaluation dataset for the Tonal Contrast
Preservation Rate (TCPR) metric. The decisions here are not arbitrary; each
one is motivated by a specific requirement of the TCPR metric, a property of
Kikuyu phonology, or a constraint of the downstream TTS evaluation task.

Anyone extending the dataset, replicating the evaluation, or reviewing the
methodology should read this document before touching the CSV.

---

## 1. What this dataset is for

TCPR measures what proportion of lexically-contrastive tonal minimal pairs are
correctly distinguished by a cross-lingual IPA approximation system. A minimal
pair is correctly distinguished if the approximated IPA strings for word_a and
word_b differ in their tone marking in a way that mirrors the actual tonal
contrast between the two words.

The dataset is the ground truth against which IPA approximations are scored.
Its quality directly determines whether TCPR is a credible metric. A dataset
with ambiguous pairs, inconsistent IPA encoding, or pairs that are not genuine
minimal pairs produces a metric that cannot be trusted.

This is an evaluation dataset, not a full lexicon. It does not need to be
exhaustive. It needs to be correct, consistent, and representative of the
tonal contrasts that matter for TTS intelligibility in Kikuyu.

---

## 2. Scope decision: H/L contrasts only for Phase 1

**Decision:** The first-pass dataset covers lexical High (H) vs Low (L) tonal
contrasts only. Rising (LH) tone pairs and downstep are excluded from Phase 1.

**Rationale:**

Kikuyu has three lexically specified tonal categories relevant to this work:
High (H), Low (L), and a Low-High rising tone (LH) that operates on some
vowels and stems. It also has downstep — a post-lexical register-lowering
process triggered by floating L tones — which is phrase-governed rather than
lexically specified.

H vs L is the most productive and best-documented contrast in the Kikuyu
tonal literature. Armstrong (1967) documents it across monosyllabic and
disyllabic nouns, verbs, and adjectives. Clements and Ford (1981) build their
downstep analysis on H/L as the primitive distinction. It is the contrast that
Transphone is most likely to either preserve or fail on, making it the highest
diagnostic value for H1.

Rising tone pairs are excluded not because they are unimportant but because:
(a) they are less consistently documented in the literature, (b) their IPA
encoding varies across sources (LH diacritic vs. circumflex vs. sequence), and
(c) the TCPR regex for rising tone requires more complex pattern matching than
H/L, introducing implementation risk in Phase 1. Rising tone pairs are reserved
for Phase 2 once the H/L evaluation is validated.

Downstep is excluded from the dataset entirely, consistent with the proposal's
explicit scope statement: "TCPR is explicitly scoped to lexically-specified
tonal minimal pairs. Phrase-level tonal modelling represents a natural Phase 2
extension, motivated by Phase 1 empirical findings." Downstep is post-lexical
and cannot be evaluated at the word level without phrase context.

**Implication for the CSV:** The `tone_a` and `tone_b` columns will contain
only the values `H` and `L` in Phase 1. Any pair where either word carries a
rising tone is excluded from this version.

---

## 3. IPA encoding convention

**Decision:** Tone is marked using IPA diacritics on vowels: acute accent (´)
for High tone, grave accent (`) for Low tone. No tone letters. No superscripts.

**Convention in practice:**

| Tone | Diacritic | Example vowel | Unicode codepoint |
|------|-----------|---------------|-------------------|
| High (H) | acute accent | á | U+00E1 (precomposed) or a + U+0301 |
| Low (L) | grave accent | à | U+00E0 (precomposed) or a + U+0300 |
| Unmarked | none | a | reserved for future use only |

**Rationale:**

Acute/grave on vowel is the dominant convention in descriptive Kikuyu
phonology, used by Armstrong (1967), Clements and Ford (1981), and the IPA
Handbook examples for Bantu languages. It is also the convention used by
Epitran for languages it supports natively, making it consistent with the
broader toolchain.

Tone letters (˥ ˩) are used in some computational phonology work but are
less readable for manual annotation and require additional Unicode handling.
Superscript H/L is used in autosegmental notation in theoretical linguistics
but is not standard IPA and would require custom regex patterns.

The acute/grave convention produces TCPR-evaluable strings with a simple
regex: tone is present if the IPA string contains any character in the set
{á, é, í, ó, ú, à, è, ì, ò, ù} or their decomposed equivalents. The
contrast check is: do word_a and word_b differ in which tone diacritic
appears on the corresponding vowel?

**Encoding hygiene rule:** All IPA strings in the CSV must use precomposed
Unicode characters (e.g. á U+00E1, not a + U+0301). This prevents invisible
encoding mismatches that would cause the validator to report spurious
mismatches. The validator script will check for this and reject decomposed
forms.

**Kikuyu orthography note:** Standard Kikuyu orthography (as used in WAXAL
and BibleTTS) uses circumflex and tilde diacritics on vowels to mark
phonemic length and the central vowels (ũ, ĩ). These are orthographic, not
tonal. The IPA `ipa_gold` column encodes tone separately from vowel quality.
A word like *ngũgũ* has two high-toned central rounded vowels; its IPA entry
encodes both the vowel quality (ʊ) and the tone (high, marked with acute).

---

## 4. Minimal pair criteria

**Decision:** A pair qualifies as a tonal minimal pair for this dataset if and
only if all four of the following criteria are met.

**Criterion 1 — Segmental identity.** The two words are identical in all
consonants and vowels, in the same order. Vowel length differences are
permitted only if they are not the distinguishing feature (i.e. the pair is
distinguished by tone, not length). Pairs distinguished by a consonant, vowel
quality, or vowel length difference are not minimal pairs for this purpose and
are excluded.

**Criterion 2 — Tonal contrast.** The two words differ in at least one
lexically-specified tone. In Phase 1, this means one word has H where the
other has L on the same syllable, and this difference is the only phonological
difference between the words.

**Criterion 3 — Semantic distinctness.** Both words have distinct, recoverable
meanings. Words where the tonal distinction marks only grammatical categories
(e.g. tense distinctions in verb paradigms that are otherwise identical) are
included, but the grammatical distinction must be noted in the `meaning` fields.
Words where one member of the pair is archaic or no longer in active use are
flagged with `status: archaic` and excluded from the primary TCPR calculation,
though retained in the file for reference.

**Criterion 4 — Speaker verification.** Each pair must be verified by a native
Kikuyu speaker before inclusion in the primary evaluation set. In Phase 1,
the verifying speaker is Watson Ndethi (native Kikuyu, Gĩkũyũ dialect,
Kiambu region). Pairs sourced from literature are verified against the
speaker's own judgment; pairs where speaker judgment conflicts with the
literature source are flagged with `status: disputed` and excluded from the
primary TCPR calculation pending a second speaker review.

---

## 5. Sources

Pairs in Phase 1 are drawn from three sources, ranked by reliability:

**Source A — Armstrong (1967).** *The Phonetic and Tonal Structure of Kikuyu.*
Dawsons of Pall Mall. The primary descriptive reference for Kikuyu tone.
Armstrong's pairs are based on systematic elicitation with native speakers and
are the most cited source in the Kikuyu tonology literature. IPA encoding
requires transliteration from Armstrong's notation to current IPA conventions
(her system predates the 1989 IPA revision). All Armstrong pairs are
speaker-verified before inclusion.

**Source B — Clements and Ford (1981).** "On the phonological status of
downstep in Kikuyu." In *Phonology in the 1980s*, eds. D. Goyvaerts.
Story-Scientia, Ghent. Pairs used to argue the downstep analysis — smaller
set but high quality. These pairs are specifically selected for their clarity
as H/L contrasts, since downstep pairs are excluded.

**Source C — BibleTTS Kikuyu (Meyer et al., 2022).** Corpus-mined candidates:
words appearing in the MFA-aligned BibleTTS output with identical orthographic
form but measurably different F0 contours across occurrences. These candidates
are generated programmatically and require speaker verification before
inclusion. They provide ecological validity — pairs that actually occur in
naturalistic Kikuyu text — which is a stronger argument for TTS relevance than
purely elicited pairs.

Each row in the CSV carries a `source` field with values `armstrong_1967`,
`clements_ford_1981`, or `bibletss_mined`. This allows TCPR to be computed
separately per source as a data quality check.

---

## 6. CSV schema

```
word_a, word_b, tone_a, tone_b, ipa_gold_a, ipa_gold_b,
meaning_a, meaning_b, source, status, notes
```

| Field | Type | Values | Notes |
|-------|------|--------|-------|
| word_a | string | Kikuyu orthography | Standard Kikuyu spelling with diacritics for vowel quality (ũ, ĩ) |
| word_b | string | Kikuyu orthography | Same |
| tone_a | string | H, L | Lexical tone of word_a. Phase 1: H or L only |
| tone_b | string | H, L | Lexical tone of word_b. Phase 1: H or L only |
| ipa_gold_a | string | IPA with diacritics | Precomposed Unicode. Acute = H, grave = L |
| ipa_gold_b | string | IPA with diacritics | Same |
| meaning_a | string | English gloss | Keep brief. Note grammatical category if relevant |
| meaning_b | string | English gloss | Same |
| source | string | armstrong_1967, clements_ford_1981, bibletss_mined | Origin of the pair |
| status | string | primary, archaic, disputed | primary = included in TCPR; others excluded |
| notes | string | free text | Encoding decisions, conflicts with source, verification notes |

---

## 7. What TCPR does with this dataset

The TCPR metric takes each row where `status = primary`, retrieves the
approximated IPA strings for `word_a` and `word_b` from the approximation
pipeline output, and checks whether the approximated strings differ in tone
marking in a direction consistent with the `tone_a` / `tone_b` contrast.

Specifically: a pair is **preserved** if the approximated IPA for word_a
contains a tone mark corresponding to `tone_a` (acute for H, grave for L) and
the approximated IPA for word_b contains a tone mark corresponding to `tone_b`,
on the vowel that carries lexical tone. A pair is **not preserved** if the
approximated strings are tonally identical (both H, both L, or both unmarked),
or if the contrast is reversed.

TCPR = (number of preserved pairs) / (total primary pairs evaluated)

Bootstrap resampling (1000 iterations) produces a 95% confidence interval.
H1 predicts TCPR ≥ 0.80 for the Yoruba-weighted approximation condition.

The `source` field enables a secondary analysis: does TCPR differ between
Armstrong-sourced pairs (elicited, classical) and BibleTTS-mined pairs
(naturalistic, contemporary)? A gap here would be substantively interesting —
it would suggest that classical elicited pairs and naturalistic occurring pairs
test different aspects of tonal fidelity.

---

## 8. What this dataset is NOT

- It is not a full Kikuyu pronunciation lexicon. That is `data/kikuyu_ipa_lexicon.tsv`.
- It is not a comprehensive survey of Kikuyu tonal contrasts. It is a
  targeted evaluation set for one metric.
- It does not cover downstep, rising tone, or phrase-level tonal phenomena.
  Those are Phase 2.
- It does not constitute participatory co-design with the Kikuyu community.
  Speaker verification by the researcher-as-native-speaker is appropriate for
  Phase 1. Community participatory validation is planned future work, as
  stated in the proposal.

---

## 9. Versioning

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | April 2026 | First pass. H/L only. Sources: Armstrong (1967), Clements & Ford (1981), BibleTTS mined candidates. Verifier: Watson Ndethi. |
| v2.0 | TBD | Add rising tone (LH) pairs. Second speaker verification. |
| v3.0 | TBD | Community participatory validation. Phase 2. |

---

*thiLLMo IPA Project | Watson Ndethi | April 2026*
