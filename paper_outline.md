# approxIPA Paper Outline: Tonal Contrast Preservation in Cross-Lingual IPA Approximation for Kikuyu

## 1. Introduction
- Problem: Low-resource tonal languages lack TTS systems due to data scarcity
- Insight: Cross-lingual approximation from higher-resource relatives may preserve tonal contrasts
- Gap: No systematic evaluation framework for tonal preservation in approximation
- Contribution: TCPR metric + thiLLMo pipeline + Kikuyu case study

## 2. Related Work
- Low-resource TTS approaches (transfer learning, multilingual, zero-shot)
- Cross-lingual G2P and IPA approximation (Transphone, Epitran, ByT5)
- Tonal language TTS challenges (Mandarin, Vietnamese, Yoruba studies)
- Minimal pair-based evaluation in phonology and speech tech
- Existing metrics: WER, PER, BLEU (tonal-blind); need tonal-aware metrics

## 3. Methods
### 3.1 Language Focus: Kikuyu (Gĩkũyũ)
- Speaker population: 7.2M (Ethnologue)
- Tonal system: 2 level tones (H, L); rising/falling/downstep in Phase 2
- Orthographic note: Tilde (ĩ, ũ) marks vowel quality, NOT tone
- IPA encoding standard: Precomposed Unicode only (á=H, à=L)

### 3.2 Data Sources
- **WAXAL Kikuyu**: Primary evaluation corpus (~20h studio, CC-BY-4.0)
- **BibleTTS Kikuyu**: Independent reference stream (86h, resolves circularity)
- **thiLLMo Gold Lexicon**: 500+ manually validated IPA entries (to be integrated)

### 3.3 Approximation Methods
- **Transphone**: Cross-lingual G2P with weighted tokenizers
  - Yoruba-weighted: Primary tonal approximation (condition A)
  - Swahili-weighted: Non-tonal control (condition B)
- **ByT5** (optional ablation): Neural G2P fine-tuning on thiLLMo lexicon

### 3.4 TCPR Metric: Tonal Contrast Preservation Rate
- Definition: Proportion of lexically-contrastive tonal minimal pairs correctly distinguished
- Formula: TCPR = (# preserved pairs) / (# total primary pairs evaluated)
- Properties: Bounded [0,1], bootstrap CI for uncertainty estimation
- Validation: Requires speaker-verified gold standard minimal pairs

### 3.5 Experimental Setup
- Wordlist: 1,000 high-frequency Kikuyu words from WAXAL
- Approximation pipeline: Deterministic Transphone calls
- Lexicon artifact: CMUdict format (word<space>PHONEMES)
- Evaluation: TCPR computation with bootstrap resampling (n=1000)

## 4. Results (Placeholder - to be updated with gold data)
### 4.1 Lexicon Statistics
- Total entries: 1,000 (from Transphone approximations)
- Yoruba/Swahili agreement: 32.3% (323 entries)
- Disagreements: 67.7% (677 entries) - resolved via Yoruba preference

### 4.2 TCPR Results (with placeholder/pseudo-data)
[To be filled when gold minimal pairs are available]

### 4.3 Analysis
- Yoruba vs Swahili comparison
- Error analysis by tonal pattern
- Segmental quality assessment
- Failure mode taxonomy

## 5. Discussion
- Interpretation of TCPR scores
- Comparison to baselines and prior work
- Limitations: Annotation sparsity, approximation biases
- Ethical considerations: Community involvement, speaker authority
- Implications for low-resource tonal language TTS

## 6. Conclusion
- Summary of findings
- Answer to research questions
- Future work directions
- Broader impact

## References
[To be compiled]

## Appendix
A. IPA encoding conventions and validation rules
B. TCPR algorithm pseudocode
C. Lexicon artifact samples
D. Experimental configuration and seed values
E. Full tonal minimal pair set (when available)