"""Tests for phase conversion utilities."""

import pytest

from guppyalgos.utils.python.phase import (
    binary_fraction,
    fixed_point_to_float,
    phase_distance_mod_2,
    phase_to_energy_qpe,
    phase_to_energy_qubitized_qpe,
)


def test_binary_fraction() -> None:
    """Test QPE-style binary fraction decoding."""
    assert binary_fraction([True, False, False]) == 0.25
    assert binary_fraction([False, False, True]) == 1.0


def test_invalid_fixed_point_to_float() -> None:
    """Test invalid radix placement arguments raise exceptions."""
    with pytest.raises(ValueError, match="int_bits"):
        fixed_point_to_float([True, False], int_bits=-1)

    with pytest.raises(ValueError, match="int_bits"):
        fixed_point_to_float([True, False], int_bits=3)


def test_phase_to_energy_qpe_principal_branch() -> None:
    """Test conversion from QPE phase to energy on the principal branch."""
    assert phase_to_energy_qpe(0.125, 0.21990654270669038) == pytest.approx(
        -1.1368465754720543
    )


def test_phase_to_energy_qpe_shifted_branch() -> None:
    """Test conversion from QPE phase to energy on a shifted modulo-2 branch."""
    assert phase_to_energy_qpe(
        0.125, 0.21990654270669038, phase_wraps=1
    ) == pytest.approx(-19.32639178302492)


def test_phase_to_energy_qubitized_qpe() -> None:
    """Test conversion from conjugate qubitization phases to an energy."""
    normalization = 1.1
    expected_eigenvalue = 1 / 2**0.5

    assert phase_to_energy_qubitized_qpe(0.75, normalization) == pytest.approx(
        expected_eigenvalue * normalization
    )
    assert phase_to_energy_qubitized_qpe(1.25, normalization) == pytest.approx(
        expected_eigenvalue * normalization
    )


def test_phase_distance_mod_2() -> None:
    """Test shortest-distance comparisons on the QPE phase circle."""
    assert phase_distance_mod_2(0.75, 0.75) == pytest.approx(0.0)
    assert phase_distance_mod_2(0.25, 0.75) == pytest.approx(0.5)
    assert phase_distance_mod_2(0.25, 2.25) == pytest.approx(0.0)
    assert phase_distance_mod_2(0.05, 1.95) == pytest.approx(0.1)
    assert phase_distance_mod_2(1.9, 0.1) == pytest.approx(0.2)
