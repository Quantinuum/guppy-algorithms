"""Calculate alias table for use in loading probability distributions."""

import warnings

import numpy as np
import numpy.typing as npt

from guppyalgos.utils.python.warnings import QuantumEfficiencyWarning


class Aliaser:
    """Calculate alias table for use in loading probability distributions."""

    def __init__(self, probs: npt.NDArray[np.float64], n_precision_bits: int) -> None:
        """Generate an alias table from a probabiity distribution."""
        if np.any(probs == 0):
            warnings.warn(
                "Probability distribution loaded via alias sampling contains 0 entries"
                ",wasting quantum resources. "
                "Consider reorganizing indices to remove 0 entries.",
                QuantumEfficiencyWarning,
                stacklevel=2,
            )
        self.probs = discretize_distribution(probs, n_precision_bits)
        is_normalized = np.allclose(np.linalg.norm(self.probs, ord=1), 1)
        has_negatives = np.any(self.probs < 0)
        if not is_normalized:
            raise ValueError("Invalid probability distribution: cause non-normalized")
        if has_negatives:
            raise ValueError("Invalid probability distribution: cause negative values")
        self.aliases = np.zeros(len(probs), dtype=np.int64)
        self.mean = np.mean(self.probs)
        # the indices higher than mean
        higher: list[int] = []
        # the indices lower than mean
        lower: list[int] = []
        # set up stacks
        for i, c in enumerate(probs):
            (higher if np.abs(c) > self.mean else lower).append(i)

        while higher and lower:
            # get the next pair of indices: one higher and one lower than the mean
            hi, lo = higher.pop(), lower.pop()
            # set the alias for the lo (source) bin to the hi (target) bin
            self.aliases[lo] = hi
            # update the probability that we get the hi bin for the possibility
            # that we aliased there
            self.probs[hi] = self.probs[hi] - (self.mean - self.probs[lo])
            # make target bin available as a source
            if self.probs[hi] < self.mean:
                lower.append(hi)
            # otherwise, it's available as a target
            else:
                higher.append(hi)

        # modify so self.probs contains the keep probability
        self.probs = self.probs / self.mean
        # anywhere where keep is certain should have its alternative be itself
        prob_1_mask = np.isclose(self.probs, 1)
        self.aliases[prob_1_mask] = np.arange(len(self.aliases))[prob_1_mask]

    def draw(self, n: int) -> npt.NDArray[np.int64]:
        """Sample from the probability distribution using the alias table."""
        # draw n random numbers on [0, 1)
        r = np.random.random(n) * len(self.probs)
        # get the uniformly drawn bin indices
        bins = np.asarray(np.floor(r), dtype=np.int64)
        # the remainder are the probabilities that we do not go to the aliased bin
        remainder = r - bins
        # mask for those selected bins that we should alias
        aliased_inds = np.where(remainder >= self.probs[bins])
        # mask for those selected bins that we should not alias
        unaliased_inds = np.where(remainder < self.probs[bins])
        # combine these indices
        return np.hstack((bins[unaliased_inds], self.aliases[bins[aliased_inds]]))

    def get_indices_with_no_alternative(self) -> npt.NDArray[np.int64]:
        """Get indices where the alternative value is the same as the present index."""
        return np.arange(len(self.aliases))[
            self.aliases == np.arange(len(self.aliases))
        ]

    def probability_dist_from_table(self) -> npt.NDArray[np.float64]:
        """Recalculate the input (discretized) probability distribution."""
        uniform_prob = 1 / len(self.probs)
        prob_dist = np.zeros_like(self.probs)
        for i, keep_prob in enumerate(self.probs):
            prob_dist[i] += uniform_prob * keep_prob
            prob_dist[self.aliases[i]] += uniform_prob * (1 - keep_prob)
        return prob_dist

    def __len__(self) -> int:
        """Get number of terms in the alias table."""
        return len(self.probs)


def discretize_distribution(
    dist: npt.NDArray[np.float64], n_bits: int
) -> npt.NDArray[np.float64]:
    """Discretize distribution to be representable by n_bit fixed point numbers."""
    M = 2**n_bits
    scaled_dist = dist * M
    floors = np.asarray(np.floor(scaled_dist), dtype=np.int64)
    remainders = scaled_dist - floors
    bits_to_add = M - np.sum(floors)
    remainder_sort_indices = np.argsort(remainders)
    if bits_to_add > 0:
        floors[remainder_sort_indices[-bits_to_add:]] += 1
    return floors / M
