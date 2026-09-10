"""Tests for temporary AND operations using different implementations."""

import pytest

from guppylang.decorator import guppy
from guppylang.std.builtins import output
from guppylang.std.quantum import (
    measure_array,
    qubit,
    toffoli,
    x,
    measure,
    collect_measurements,
)

from guppyalgos.utils import int_to_bits
from guppyalgos.utils import qarray

from guppyalgos.primitives.gate_decompositions.and_op import (
    temp_and_compute,
    temp_and_uncompute,
)

from guppylang.defs import GuppyFunctionDefinition


from typing import no_type_check


@pytest.mark.parametrize("comp_and_op", [toffoli, temp_and_compute])
@pytest.mark.parametrize("i", [0, 1, 2, 3])
def test_compute_temp_and(
    i: int,
    comp_and_op: GuppyFunctionDefinition,
) -> None:
    """Test temp_and_compute with different implementations.

    Temporary AND which only acts on an incoming |0> target state loops
    over the incoming input bits possibilities and applies the AND operation.

    Args:
        i (int): Integer index to determine input bits.
        comp_and_op (GuppyFunctionDefinition): The AND computation operation
            to be tested. This can be either the toffoli or the temp_and_compute
            function.

    """
    binary_index = int_to_bits(i, 2)

    @guppy
    @no_type_check
    def main() -> None:
        idx = binary_index
        index_qreg = qarray(2)
        target = qubit()

        for bit in range(2):
            if idx[bit]:
                x(index_qreg[bit])

        comp_and_op(index_qreg[0], index_qreg[1], target)

        output("index", collect_measurements(measure_array(index_qreg)))
        output("state", measure(target).read())

    total_qubits = 3
    my_shots = main.emulator(n_qubits=total_qubits).with_seed(42).with_shots(1).run()
    bool_and = binary_index[0] and binary_index[1]
    assert my_shots.collated_shots()[0]["state"][0] == bool_and


@pytest.mark.parametrize("comp_and_op", [toffoli, temp_and_uncompute])
@pytest.mark.parametrize("i", [0, 1, 2, 3])
def test_uncompute_temp_and(
    i: int,
    comp_and_op: GuppyFunctionDefinition,
) -> None:
    """Test temp_and_uncompute with different implementations.

    Temporary AND which acts on an incoming |1> target state loops
    over the incoming input bits possibilities and applies the AND operation.

    Because it acts on |1>, the output is flipped and is expected to be False

    Args:
        i (int): Integer index to determine input bits.
        comp_and_op (GuppyFunctionDefinition): The AND computation operation
            to be tested. This can be either the toffoli or the temp_and_uncompute
            function.

    """
    binary_index = int_to_bits(i, 2)

    @guppy
    @no_type_check
    def main() -> None:
        idx = binary_index
        index_qreg = qarray(2)
        target = qubit()

        x(target)

        for bit in range(2):
            if idx[bit]:
                x(index_qreg[bit])

        comp_and_op(index_qreg[0], index_qreg[1], target)

        output("index", collect_measurements(measure_array(index_qreg)))
        output("state", measure(target).read())

    total_qubits = 3
    my_shots = main.emulator(n_qubits=total_qubits).with_seed(42).with_shots(1).run()
    bool_and = binary_index[0] and binary_index[1]
    assert my_shots.collated_shots()[0]["state"][0] is not bool_and
