"""Tests for adapting flat fanout to selected data qubits."""

from typing import no_type_check

from guppylang import guppy
from guppylang.std.builtins import array, output
from guppylang.std.quantum import collect_measurements, measure, measure_array, qubit, x

from guppyalgos.primitives.subroutines.fanout import fanout_basic, fanout_from_data
from guppyalgos.utils import qarray


def test_fanout_from_data_single_register() -> None:
    """Apply data-selected fanout to one target register."""
    data = [True, False, True]
    n_state_qubits = len(data)
    fan_out = fanout_from_data(data, fanout_basic)

    @guppy
    @no_type_check
    def main() -> None:
        control = qubit()
        target_qreg = qarray(n_state_qubits)

        x(control)
        fan_out(control, target_qreg)

        output("control", measure(control).read())
        output("state", collect_measurements(measure_array(target_qreg)))

    result = (
        main.emulator(n_qubits=n_state_qubits + 1)
        .with_seed(42)
        .with_shots(1)
        .run()
        .collated_shots()[0]
    )
    assert result["state"][0] == data
    assert result["control"][0] == 1


def test_fanout_from_data_two_registers() -> None:
    """Apply data-selected fanout to two target registers."""
    data = [[True, False, True], [False, True, True]]
    n_target_registers = len(data)
    n_state_qubits = len(data[0])
    fan_out = fanout_from_data(data, fanout_basic)

    @guppy
    @no_type_check
    def main() -> None:
        control = qubit()
        target_qregs = array(qarray(n_state_qubits) for _ in range(n_target_registers))

        x(control)
        fan_out(control, target_qregs)

        output(
            "state_0",
            collect_measurements(measure_array(target_qregs.take(0))),
        )
        output(
            "state_1",
            collect_measurements(measure_array(target_qregs.take(1))),
        )
        target_qregs.discard_all_taken()
        output("control", measure(control).read())

    result = (
        main.emulator(n_qubits=n_target_registers * n_state_qubits + 1)
        .with_seed(42)
        .with_shots(1)
        .run()
        .collated_shots()[0]
    )
    assert result["state_0"][0] == data[0]
    assert result["state_1"][0] == data[1]
    assert result["control"][0] == 1
