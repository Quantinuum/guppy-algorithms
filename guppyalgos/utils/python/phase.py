"""Phase conversion utilities for quantum algorithms."""

from math import cos, pi

from .binary import fixed_point_to_float


def binary_fraction(readout: list[bool]) -> float:
    r"""Convert bits into a QPE-style fraction number [0, 2)."""
    return fixed_point_to_float(readout, int_bits=1)


def phase_to_energy_qpe(phase: float, total_time: float, phase_wraps: int = 0) -> float:
    r"""Convert a QPE phase into an energy for ``U(t) = e^{-i \pi t H / 2}``.

    Uses ``E = -2 * (phase + 2 * phase_wraps) / total_time``. The default
    ``phase_wraps=0`` selects the principal branch.

    """
    return float(-2 * (phase + 2 * phase_wraps) / total_time)


def phase_to_energy_qubitized_qpe(phase: float, normalization: float) -> float:
    """Convert a qubitization walk phase to its encoded operator energy."""
    return float(-normalization * cos(pi * phase))


def phase_distance_mod_2(phase_a: float, phase_b: float) -> float:
    r"""Return the shortest distance between two phases on the circle ``[0, 2)``.

    This is useful when comparing QPE phases modulo ``2``, where values that
    differ by an integer multiple of ``2`` represent the same point on the
    phase circle.

    """
    return float(min((phase_a - phase_b) % 2, (phase_b - phase_a) % 2))
