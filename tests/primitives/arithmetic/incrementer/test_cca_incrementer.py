"""Tests for the conditionally-clean-ancilla incrementer."""

from collections import Counter
from typing import no_type_check

import pytest
from guppylang import guppy
from guppylang.std.builtins import output
from guppylang.std.quantum import (
    collect_measurements,
    measure,
    measure_array,
    x,
    discard_array,
)
from guppyalgos.utils import qarray

from guppyalgos.primitives.arithmetic.incrementer.incrementer_cca import (
    cca_incrementer,
    cca_decrementer,
    cntrl_cca_incrementer,
    cntrl_cca_decrementer,
    required_clean_ancillas,
)


def _little_endian_bits(value: int, num_bits: int) -> list[bool]:
    return [bool((value >> i) & 1) for i in range(num_bits)]


def _output_string(value: int, num_bits: int) -> str:
    bits = _little_endian_bits(value, num_bits)
    return "".join("1" if bit else "0" for bit in bits)


@pytest.mark.parametrize("num_bits", [4, 5, 7, 12, 19])
def test_cca_incrementer_compiles(num_bits: int) -> None:
    """Test CCA incremeter compiles without ownership or borrowing errors."""

    @guppy
    @no_type_check
    def main() -> None:
        q = qarray(num_bits)

        cca_incrementer(q)

        discard_array(q)

    main.compile()


@pytest.mark.parametrize("num_bits", [5, 7, 10, 20, 50, 100, 200, 500])
def test_incrementer_does_not_panic(num_bits: int) -> None:
    """Test CCA incrementer runs without runtime panics."""
    num_ancillas = required_clean_ancillas(num_bits)

    @guppy
    @no_type_check
    def main() -> None:
        q = qarray(num_bits)

        cca_incrementer(q)

        discard_array(q)

    (main.emulator(n_qubits=num_bits + num_ancillas).coinflip_sim().run())


@pytest.mark.parametrize(
    ("num_bits", "value"),
    [
        (5, 0),
        (5, 1),
        (5, 13),
        (5, 30),
        (5, 31),
        (7, 0),
        (7, 1),
        (7, 63),
        (7, 126),
        (7, 127),
        # (12, 23),
    ],
)
def test_cca_incrementer(num_bits: int, value: int) -> None:
    """Increment an m-bit register using conditionally clean ancillas."""
    num_ancillas = required_clean_ancillas(num_bits)

    input_bits = _little_endian_bits(value, num_bits)
    expected_value = (value + 1) % (1 << num_bits)
    expected = _output_string(expected_value, num_bits)

    @guppy
    @no_type_check
    def main() -> None:
        q = qarray(num_bits)
        bits = input_bits

        for i in range(num_bits):
            if bits[i]:
                x(q[i])

        cca_incrementer(q)

        output(
            "out",
            collect_measurements(measure_array(q)),
        )

    emulator_result = (
        main.emulator(n_qubits=num_bits + num_ancillas)
        .with_seed(43)
        .with_shots(10)
        .run()
    )

    assert emulator_result.collated_counts() == Counter({(("out", expected),): 10})


@pytest.mark.parametrize(
    ("num_bits", "value"),
    [
        (5, 0),
        (5, 1),
        (5, 13),
        (5, 30),
        (5, 31),
        (7, 0),
        (7, 1),
        (7, 63),
        (7, 126),
        (7, 127),
    ],
)
def test_cca_decrementer(num_bits: int, value: int) -> None:
    """Decrement an m-bit register using conditionally clean ancillas."""
    num_ancillas = required_clean_ancillas(num_bits)

    input_bits = _little_endian_bits(value, num_bits)
    expected_value = (value - 1) % (1 << num_bits)
    expected = _output_string(expected_value, num_bits)

    @guppy
    @no_type_check
    def main() -> None:
        q = qarray(num_bits)
        bits = input_bits

        for i in range(num_bits):
            if bits[i]:
                x(q[i])

        cca_decrementer(q)

        output(
            "out",
            collect_measurements(measure_array(q)),
        )

    emulator_result = (
        main.emulator(n_qubits=num_bits + num_ancillas)
        .with_seed(43)
        .with_shots(10)
        .run()
    )

    assert emulator_result.collated_counts() == Counter({(("out", expected),): 10})


@pytest.mark.parametrize(
    ("num_bits", "value"),
    [
        (5, 0),
        (5, 1),
        (5, 13),
        (5, 30),
        (5, 31),
        (7, 0),
        (6, 1),
        (6, 63),
        (6, 126),
        (6, 127),
    ],
)
@pytest.mark.parametrize("control_on", [False, True])
@pytest.mark.parametrize("dagger", [False, True])
def test_cntrl_cca_incrementer(
    num_bits: int,
    value: int,
    control_on: bool,
    dagger: bool,
) -> None:
    """Increment/decrement iff all control qubits are set."""
    value %= 1 << num_bits

    num_controls = 1

    num_ancillas_big = required_clean_ancillas(num_bits + num_controls)
    num_ancillas_small = required_clean_ancillas(num_controls)
    num_ancillas = num_ancillas_big + num_ancillas_small + 1

    input_bits = _little_endian_bits(value, num_bits)

    # Test every possible control configuration.
    if not dagger:
        expected_value = (value + 1) % (1 << num_bits) if control_on else value
    else:
        expected_value = (value - 1) % (1 << num_bits) if control_on else value

    @guppy
    @no_type_check
    def main() -> None:
        control = qubit()
        q = qarray(num_bits)

        if control_on:
            x(control)

        bits = input_bits
        for i in range(num_bits):
            if bits[i]:
                x(q[i])

        if not dagger:
            cntrl_cca_incrementer(control, q)
        else:
            cntrl_cca_decrementer(control, q)

        output("ctrl", measure(control).read())
        output("out", collect_measurements(measure_array(q)))

    expected = _output_string(expected_value, num_bits)
    expected_ctrl = _output_string(control_on, num_controls)

    emulator_result = (
        main.emulator(n_qubits=(num_bits + num_controls + num_ancillas))
        .with_seed(41)
        .with_shots(10)
        .run()
    )

    assert emulator_result.collated_counts() == Counter(
        {(("ctrl", expected_ctrl), ("out", expected)): 10}
    )
