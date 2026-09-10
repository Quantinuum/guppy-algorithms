"""Uncompute the logical AND operation."""

from guppylang import guppy
from guppylang.std.quantum import (
    qubit,
    project_z,
    cz,
    h,
)


from typing import no_type_check


@guppy
@no_type_check
def temp_and_uncompute(q_0: qubit, q_1: qubit, target_q: qubit) -> None:
    """Uncompute the logical AND operation.

    This function reverses the effects of the logical AND operation
    applied to the input qubits and the target qubit. It is equivalent to
    measurement based uncomputation as described in Fig 4.
    https://arxiv.org/pdf/1805.03662. The qubit must be discarded after use.

    Args:
        q_0 (qubit): The first input qubit.
        q_1 (qubit): The second input qubit.
        target_q (qubit): The auxiliary qubit used in computation.

    """
    h(target_q)
    if project_z(target_q).read():
        cz(q_0, q_1)
