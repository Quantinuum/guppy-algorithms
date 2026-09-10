"""Utility functions for AND operations."""

from guppylang import guppy

from guppylang.std.quantum import (
    qubit,
    x,
)
from collections.abc import Callable


from typing import no_type_check


@guppy
@no_type_check
def index_and(
    target_q: qubit,
    control_q0: qubit,
    control_0_ind: bool,
    control_q1: qubit,
    control_1_ind: bool,
    and_operation: Callable[[qubit, qubit, qubit], None],
) -> None:
    """Perform an AND operation on indexed control qubits and store the result.

    Args:
        target_q (qubit): The target qubit to store the result.
        control_q0 (qubit): The first control qubit.
        control_0_ind (bool): Indicator for the first control qubit.
        control_q1 (qubit): The second control qubit.
        control_1_ind (bool): Indicator for the second control qubit.
        and_operation (Callable[[qubit, qubit, qubit], None]): The AND operation
            to apply.

    """
    if not control_0_ind:
        x(control_q0)
    if not control_1_ind:
        x(control_q1)
    and_operation(control_q0, control_q1, target_q)
    if not control_0_ind:
        x(control_q0)
    if not control_1_ind:
        x(control_q1)
