"""Tests for prepare-and-measure amplitude estimation."""

from math import sqrt
from typing import no_type_check

import pytest
from guppylang import comptime, guppy
from guppylang.defs import GuppyFunctionDefinition
from guppylang.std.angles import angle
from guppylang.std.builtins import array, nat, result
from guppylang.std.quantum import cx, h, qubit, ry

from guppyalgos.algorithms.amplitude_amplification.qae import prepare_and_measure

ESTIMATE_TAG = "estimate"

#: Number of sampling standard deviations allowed when asserting on an estimate.
N_SIGMA = 3.0


def make_ry_target_prep(
    angle_half_turns: float, n_register: int
) -> GuppyFunctionDefinition[[array[qubit, nat], qubit], None]:
    r"""State prep that rotates the target qubit by ``ry(angle)``.

    ``angle_half_turns`` is in half-turns, i.e. the ``guppylang`` ``angle`` unit where
    ``1.0`` corresponds to :math:`\pi` radians. The register is placed in an
    independent superposition so the input is a genuine superposition, while the target
    marginal stays exactly
    :math:`P(\text{target}=1) = \sin^2(\pi \cdot \text{angle\_half\_turns} / 2)`.
    """

    @guppy
    @no_type_check
    def state_prep(register: array[qubit, comptime(n_register)], target: qubit) -> None:
        ry(target, angle(comptime(angle_half_turns)))
        for i in range(comptime(n_register)):
            h(register[i])

    return state_prep


def make_entangled_target_prep(
    angle_half_turns: float, n_register: int
) -> GuppyFunctionDefinition[[array[qubit, nat], qubit], None]:
    r"""State prep that entangles the target with the first register qubit.

    ``angle_half_turns`` is in half-turns (the ``guppylang`` ``angle`` unit where
    ``1.0`` is :math:`\pi` radians). ``ry`` rotates ``register[0]`` and a ``cx`` copies
    it onto the target, producing the entangled state
    :math:`\sqrt{1-a}\,\ket{00} + \sqrt{a}\,\ket{11}` on ``(register[0], target)``
    with :math:`a = \sin^2(\pi \cdot \text{angle\_half\_turns} / 2)`. Measuring the
    target therefore yields :math:`\ket{1}` with probability :math:`a`.
    """

    @guppy
    @no_type_check
    def state_prep(register: array[qubit, comptime(n_register)], target: qubit) -> None:
        ry(register[0], angle(comptime(angle_half_turns)))
        cx(register[0], target)

    return state_prep


def build_program(
    state_prep: GuppyFunctionDefinition[[array[qubit, nat], qubit], None],
    repeat: int,
) -> GuppyFunctionDefinition[[], None]:
    """Wrap the prepare-and-measure estimator into a runnable, zero-argument program.

    This is the workflow layer: it invokes the estimator with the given ``state_prep``
    and repetition count, and records the returned estimate under ``ESTIMATE_TAG``.
    """

    @guppy
    @no_type_check
    def main() -> None:
        result(
            comptime(ESTIMATE_TAG), prepare_and_measure(state_prep, comptime(repeat))
        )

    return main


def run_estimate(
    state_prep: GuppyFunctionDefinition[[array[qubit, nat], qubit], None],
    n_register: int,
    repeat: int = 4000,
    seed: int = 2,
) -> float:
    """Emulate the prepare-and-measure program and return the amplitude estimate.

    The estimator averages ``repeat`` internal repetitions in a single program run, so
    one shot yields one estimate. The emulator is always seeded so the sampling
    assertions are deterministic rather than flaky at the ``N_SIGMA`` boundary; the
    default seed was chosen so every estimate lands within 1 sigma of its expectation.
    """
    program = build_program(state_prep, repeat)
    shots = (
        program.emulator(n_qubits=n_register + 1).with_seed(seed).with_shots(1).run()
    )
    return shots.collated_shots()[0][ESTIMATE_TAG][0]


def sampling_tolerance(expected_amplitude: float, repeat: int) -> float:
    """Return the ``N_SIGMA`` binomial sampling tolerance for an estimate.

    Each repetition's target outcome is Bernoulli with success probability equal to the
    amplitude ``a``, so ``count(1) / repeat`` has standard deviation
    ``sqrt(a * (1 - a) / repeat)``. Deterministic endpoints (``a in {0, 1}``) give a
    zero-width tolerance, requiring an exact result.
    """
    std = sqrt(expected_amplitude * (1.0 - expected_amplitude) / repeat)
    return N_SIGMA * std


@pytest.mark.parametrize(
    ("angle_half_turns", "expected_amplitude"),
    [(0.0, 0.0), (1.0 / 3.0, 0.25), (0.5, 0.5), (2.0 / 3.0, 0.75), (1.0, 1.0)],
)
def test_prepare_and_measure_amplitude_estimate(
    angle_half_turns: float, expected_amplitude: float
) -> None:
    """The estimated amplitude matches sin^2(pi * angle / 2) within sampling error."""
    repeat = 4000
    estimate = run_estimate(
        make_ry_target_prep(angle_half_turns, n_register=2), n_register=2, repeat=repeat
    )
    assert estimate == pytest.approx(
        expected_amplitude, abs=sampling_tolerance(expected_amplitude, repeat)
    )


@pytest.mark.parametrize(
    ("angle_half_turns", "expected_amplitude"),
    [(1.0 / 3.0, 0.25), (0.5, 0.5), (2.0 / 3.0, 0.75)],
)
def test_prepare_and_measure_estimate_with_entangled_target(
    angle_half_turns: float, expected_amplitude: float
) -> None:
    """The estimate is correct when the target is entangled with the register."""
    repeat = 4000
    estimate = run_estimate(
        make_entangled_target_prep(angle_half_turns, n_register=1),
        n_register=1,
        repeat=repeat,
    )
    assert estimate == pytest.approx(
        expected_amplitude, abs=sampling_tolerance(expected_amplitude, repeat)
    )


def test_prepare_and_measure_target_only_no_register() -> None:
    """A target-only preparation (``n_register == 0``) works and estimates correctly."""
    repeat = 4000
    estimate = run_estimate(
        make_ry_target_prep(0.5, n_register=0), n_register=0, repeat=repeat
    )
    assert estimate == pytest.approx(0.5, abs=sampling_tolerance(0.5, repeat))


def test_prepare_and_measure_is_deterministic_under_fixed_seed() -> None:
    """Re-running the program with the same seed reproduces the same estimate."""
    state_prep = make_ry_target_prep(1.0 / 3.0, n_register=2)
    first = run_estimate(state_prep, n_register=2, repeat=2000, seed=1234)
    second = run_estimate(state_prep, n_register=2, repeat=2000, seed=1234)
    assert first == second
