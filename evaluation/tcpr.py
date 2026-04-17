"""Tonal Contrast Preservation Rate (TCPR) utilities."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Sequence


# Core combining marks commonly used for IPA tone annotation.
TONE_MARKS = {
    "\u0300",  # grave
    "\u0301",  # acute
    "\u0302",  # circumflex
    "\u0304",  # macron
}


@dataclass(frozen=True)
class TCPRResult:
    """Container for TCPR aggregate outputs."""

    score: float
    preserved_pairs: int
    total_pairs: int
    ci_lower: float
    ci_upper: float
    n_bootstrap: int
    seed: int


def extract_tone_marks(ipa: str) -> tuple[str, ...]:
    """Extract tone diacritics from an IPA string in left-to-right order."""
    return tuple(character for character in ipa if character in TONE_MARKS)


def tonal_contrast(ipa_a: str, ipa_b: str) -> bool:
    """Return True when the two IPA forms differ in extracted tone signature."""
    return extract_tone_marks(ipa_a) != extract_tone_marks(ipa_b)


def pair_contrast_preserved(gold_a: str, gold_b: str, approx_a: str, approx_b: str) -> bool:
    """Check whether the pairwise contrast relation in gold is preserved in approximation."""
    return tonal_contrast(gold_a, gold_b) == tonal_contrast(approx_a, approx_b)


def _bootstrap_confidence_interval(
    outcomes: Sequence[int],
    n_bootstrap: int,
    confidence_level: float,
    seed: int,
) -> tuple[float, float]:
    """Compute a percentile bootstrap confidence interval for Bernoulli outcomes."""
    if not outcomes:
        raise ValueError("outcomes must not be empty")
    if n_bootstrap <= 0:
        raise ValueError("n_bootstrap must be > 0")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be in (0, 1)")

    rng = random.Random(seed)
    n = len(outcomes)
    bootstrap_scores: list[float] = []

    for _ in range(n_bootstrap):
        sample = [outcomes[rng.randrange(n)] for _ in range(n)]
        bootstrap_scores.append(sum(sample) / n)

    bootstrap_scores.sort()
    tail_probability = (1.0 - confidence_level) / 2.0
    lower_index = max(0, int(tail_probability * n_bootstrap))
    upper_index = min(n_bootstrap - 1, int((1.0 - tail_probability) * n_bootstrap) - 1)
    return bootstrap_scores[lower_index], bootstrap_scores[upper_index]


def compute_tcpr(
    pair_rows: Iterable[dict[str, str]],
    approx_lookup: dict[str, str],
    *,
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 7,
) -> TCPRResult:
    """
    Compute TCPR over a collection of minimal-pair rows.

    Required fields in each pair row: ``word_a``, ``word_b``, ``gold_ipa_a``, ``gold_ipa_b``.
    The lookup must contain approximated IPA strings keyed by word.
    """
    outcomes: list[int] = []

    for row in pair_rows:
        word_a = row["word_a"]
        word_b = row["word_b"]
        gold_a = row["gold_ipa_a"]
        gold_b = row["gold_ipa_b"]

        if word_a not in approx_lookup or word_b not in approx_lookup:
            continue

        preserved = pair_contrast_preserved(gold_a, gold_b, approx_lookup[word_a], approx_lookup[word_b])
        outcomes.append(1 if preserved else 0)

    if not outcomes:
        raise ValueError("No evaluable minimal pairs found. Check lookup coverage.")

    score = sum(outcomes) / len(outcomes)
    ci_lower, ci_upper = _bootstrap_confidence_interval(outcomes, n_bootstrap, confidence_level, seed)

    return TCPRResult(
        score=score,
        preserved_pairs=sum(outcomes),
        total_pairs=len(outcomes),
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        n_bootstrap=n_bootstrap,
        seed=seed,
    )
