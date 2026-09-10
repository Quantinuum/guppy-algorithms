"""Binary measurement statistics helpers.

This module provides the core dataclass and estimator for binary measurement
samples. Outcomes are interpreted as a +/- 1 random variable with the
convention ``False -> +1`` and ``True -> -1``.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class BinaryShotEstimate:
    """Frozen dataclass holding empirical statistics from finite shots.

    A single two-outcome observable is assumed.

    For N shots with ``n_plus`` false outcomes and ``n_minus`` true outcomes,
    the sample mean is

        mu_hat = (n_plus - n_minus) / N

    and the estimated variance of the sample mean is

        var_hat = (1 - mu_hat**2) / N.
    """

    expectation: float
    variance: float
    standard_error: float
    shots: int
    positive_shots: int
    negative_shots: int

    def _pretty(self, term: str = "I", term_width: int | None = None) -> str:
        """Return a compact table row for human-readable printing."""
        if term_width is None:
            term_width = max(6, len(term))
        return (
            f"{term:<{term_width}}  "
            f"{self.expectation:+10.6f}  "
            f"{self.variance:10.6f}  "
            f"{self.standard_error:10.6f}  "
            f"{self.shots:5d}  "
            f"{self.positive_shots:4d}  "
            f"{self.negative_shots:4d}"
        )


def _normalize_bool_samples(
    samples: Sequence[bool] | Mapping[bool, int],
) -> Counter[bool]:
    """Normalize boolean samples or histograms into a Counter of bool counts."""
    counts = Counter(samples)
    if any(value < 0 for value in counts.values()):
        raise ValueError("Binary sample histogram counts must be non-negative")
    return counts


def estimate_expectation_from_binary_samples(
    samples: Sequence[bool] | Mapping[bool, int],
) -> BinaryShotEstimate:
    """Estimate the mean of binary measurement samples.

    The measured outcomes are mapped to a ``+/- 1`` random variable with
    ``False -> +1`` and ``True -> -1``.

    The estimate also includes the variance of the sample mean.
    The returned variance is estimated from the observed samples, so the
    corresponding uncertainty is ``sqrt(variance)``.
    """
    counts = _normalize_bool_samples(samples)
    positive_shots = counts.get(False, 0)
    negative_shots = counts.get(True, 0)
    total_shots = positive_shots + negative_shots
    if total_shots <= 0:
        raise ValueError("At least one sample is required to estimate an expectation")

    expectation = (positive_shots - negative_shots) / total_shots
    variance = (1.0 - expectation**2) / total_shots
    return BinaryShotEstimate(
        expectation=expectation,
        variance=variance,
        standard_error=sqrt(variance),
        shots=total_shots,
        positive_shots=positive_shots,
        negative_shots=negative_shots,
    )


__all__ = [
    "BinaryShotEstimate",
    "estimate_expectation_from_binary_samples",
]
