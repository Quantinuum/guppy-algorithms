"""Ancilla-free quantum-quantum comparator."""

from typing import no_type_check

from guppylang import guppy
from guppylang.defs import GuppyFunctionDefinition
from guppylang.std.builtins import array, comptime
from guppylang.std.quantum import cx, qubit, x

from guppyalgos.primitives.subroutines.ladders.ccx_v_chain import ccx_v_chain_logdepth
from guppyalgos.primitives.subroutines.ladders.cx_ladder import (
    ladder_inds_from_ascending,
    log_cx_ladder_indices,
)
from guppyalgos.primitives.subroutines.ladders.ladder import LadderIndexing


def comparator_vandaele(n: int) -> GuppyFunctionDefinition:
    """Ancilla-free comparator with linear gate count and logarithmic depth.

    Transforms ``|a>|b>|z> -> |a>|b>|z XOR (a < b)>``.

    Based on Section 4.1 of https://arxiv.org/abs/2603.12917

    Args:
        n: Number of bits of each register.

    Returns:
        A Guppy function implementing the ancilla-free comparator.

    """
    if n < 1:
        raise ValueError("The comparator needs at least one bit")
    ladder_gates = (
        ladder_inds_from_ascending(
            log_cx_ladder_indices(n), LadderIndexing.ASCENDING_DAGGER
        )
        if n >= 2
        else []
    )
    undo_gates = log_cx_ladder_indices(n - 1) if n >= 3 else []
    v_chain = ccx_v_chain_logdepth(n)

    @guppy.comptime
    @no_type_check
    def comparator_vandaele_impl(
        a_reg: array[qubit, comptime(n)],
        b_reg: array[qubit, comptime(n)],
        target: qubit,
    ) -> None:
        """Apply the Clifford slice, the CCX V chain, and the slice reversed."""
        a = list(a_reg)
        b = list(b_reg)
        chain = [*b[1:], target]

        def clifford_slice(undo: bool = False) -> None:
            """X layer, CX layer and CX ladder."""
            if not undo:
                for wire in a:
                    x(wire)
                for i in range(1, n):
                    cx(b[i], a[i])
                for control_wire, target_wire in ladder_gates:
                    cx(chain[control_wire], chain[target_wire])
            else:
                for control_wire, target_wire in undo_gates:
                    cx(chain[control_wire], chain[target_wire])
                for i in range(1, n):
                    cx(b[i], a[i])
                for wire in a:
                    x(wire)

        clifford_slice()
        v_chain(b, a, target)
        clifford_slice(undo=True)

    return comparator_vandaele_impl
