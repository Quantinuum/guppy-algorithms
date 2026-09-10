"""Shared helpers for single- and multi-register fanout operations."""

from typing import no_type_check

from guppylang import guppy
from guppylang.defs import GuppyFunctionDefinition
from guppylang.std.builtins import array, comptime, frozenarray
from guppylang.std.option import nothing, some
from guppylang.std.quantum import qubit

from guppyalgos.utils.guppy.array import join_nested_arrays, split_nested_array


def fanout_from_data(
    data: list[bool] | list[list[bool]],
    fan_out_flat_fn: GuppyFunctionDefinition,
) -> GuppyFunctionDefinition:
    """Build a single- or multi-register fanout from a flat Guppy operation.

    The ``True`` entries in ``data`` identify selected data qubits. For nested
    data, selected qubits from every target register are gathered into one
    flat array before ``fan_out_flat_fn`` is called. The operation is invoked
    exactly once, rather than once per target register, and the qubits are then
    returned to their original locations.

    This is useful for measurement-based fanout, where the flat operation can be
    implemented with a single measurement and feed-forward correction, rather than
    one measurement per target register, leading to constant depth.

    Args:
        data: Boolean mask for one target register or equally sized masks for
            a rectangular register array.
        fan_out_flat_fn: In-place Guppy operation that borrows the control and
            flat data-qubit register.

    Returns:
        A Guppy function accepting a control and target register shape
        matching ``data``.

    Raises:
        TypeError: If ``data`` is not a non-empty boolean list or nested list.
        ValueError: If nested target masks have unequal lengths.

    """
    match data:
        case [bool(), *_] if all(isinstance(bit, bool) for bit in data):
            n_state_qubits = len(data)
            data_bits = [bit for bit, selected in enumerate(data) if selected]
            n_data_qubits = len(data_bits)

            @guppy
            @no_type_check
            def fan_out_single_target_fn(
                control: qubit,
                qreg: array[qubit, n_state_qubits],
            ) -> None:
                bits: frozenarray[int, n_data_qubits] = data_bits
                data_opts = array(
                    nothing[qubit]() for _ in range(comptime(n_data_qubits))
                )

                for i in range(n_data_qubits):
                    data_opts[i].swap(some(qreg.take(bits[i]))).unwrap_nothing()

                data_qs = array(q.unwrap() for q in data_opts)
                fan_out_flat_fn(control, data_qs)

                for i in range(n_data_qubits):
                    qreg.put(data_qs.take(i), bits[i])
                data_qs.discard_all_taken()

            return fan_out_single_target_fn

        case [[bool(), *_], *_] if all(
            isinstance(bits, list) and all(isinstance(bit, bool) for bit in bits)
            for bits in data
        ):
            nested_data = data
            if len({len(bits) for bits in nested_data}) != 1:
                raise ValueError(
                    "For fanout on multiple output registers, "
                    "the bitstrings must all be the same length"
                )

            n_target_registers = len(nested_data)
            n_state_qubits = len(nested_data[0])
            n_flat_qubits = n_target_registers * n_state_qubits
            flat_data = [bit for bits in nested_data for bit in bits]
            flat_fanout = fanout_from_data(flat_data, fan_out_flat_fn)

            @guppy
            @no_type_check
            def fan_out_multi_target_fn(
                control: qubit,
                target_qregs: array[
                    array[qubit, n_state_qubits],
                    n_target_registers,
                ],
            ) -> None:
                owned_qregs = array(
                    target_qregs.take(register)
                    for register in range(n_target_registers)
                )
                flattened = join_nested_arrays(
                    owned_qregs,
                    comptime(n_flat_qubits),
                )

                flat_fanout(control, flattened)

                owned_qregs = split_nested_array(
                    flattened,
                    comptime(n_state_qubits),
                    comptime(n_target_registers),
                )

                for register in range(n_target_registers):
                    target_qregs.put(owned_qregs.take(register), register)
                owned_qregs.discard_all_taken()

            return fan_out_multi_target_fn

        case _:
            raise TypeError(
                "Invalid data argument for fanout; expected list[bool] "
                "or list[list[bool]]"
            )
