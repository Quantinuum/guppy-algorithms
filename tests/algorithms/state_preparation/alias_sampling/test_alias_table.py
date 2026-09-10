"""Test classical alias table calculation."""

import numpy as np
import numpy.typing as npt
import pytest

from guppyalgos.algorithms.state_preparation.alias_sampling.alias_table import Aliaser

dist = np.array([4.0, 1.0, 3.5, 0, 9.0, 1.0])
dist2 = np.array([0.5, 0.25, 0.25, 0.0])


@pytest.mark.parametrize(
    ("prob_dist"),
    [dist / np.linalg.norm(dist, ord=1), dist2],
)
def test_alias_table_calc(prob_dist: npt.NDArray[np.float64]) -> None:
    """Test alias table produces correct sampling of probability distribution."""
    n_bits_precision = 14
    alias_table = Aliaser(prob_dist, n_bits_precision)
    recalculated_dist = alias_table.probability_dist_from_table()
    np.testing.assert_allclose(prob_dist, recalculated_dist, atol=1e-4)


@pytest.mark.parametrize(("prob_dist"), [dist, np.array([-0.5, 0.5])])
def test_failure_on_incorrect_prob_dist(prob_dist: npt.NDArray[np.float64]) -> None:
    """Test that non-normalized or dists with negative values raise errors."""
    with pytest.raises(ValueError, match="Invalid probability distribution"):
        _ = Aliaser(prob_dist, 10)
