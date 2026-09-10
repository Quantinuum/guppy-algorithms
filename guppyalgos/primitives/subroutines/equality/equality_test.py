"""Equality tests between same-sized registers."""

from collections.abc import Callable
from typing import no_type_check

from guppylang import guppy
from guppylang.std.builtins import array, nat
from guppylang.std.quantum import cx, qubit, x


@guppy
@no_type_check
def equality_test[n_register_qubits: nat](
    cnx_box: Callable[[array[qubit, n_register_qubits], qubit], None],
    lhs: array[qubit, n_register_qubits],
    rhs: array[qubit, n_register_qubits],
    flag: qubit,
) -> None:
    """Flip ``flag`` when two same-sized registers encode the same basis state.

    The routine computes the bitwise XOR of ``lhs`` and ``rhs`` into ``rhs``,
    so the temporary ``rhs`` register is all-zero exactly when the original
    registers were equal. It then uses ``cnx_box`` to flip ``flag`` on that
    all-zero condition by surrounding the multi-controlled X with bit flips on
    the temporary register. Finally, it uncomputes the XOR so both input
    registers are restored to their original values.

    Args:
        cnx_box: Exact multi-controlled X implementation acting on the temporary
            comparison register and the flag qubit.
        lhs: First input register.
        rhs: Second input register, used as temporary workspace during the
            comparison and restored before returning.
        flag: Target qubit flipped iff the original input registers were equal.

    """
    for i in range(n_register_qubits):
        cx(lhs[i], rhs[i])

    for i in range(n_register_qubits):
        x(rhs[i])

    cnx_box(rhs, flag)

    for i in range(n_register_qubits):
        x(rhs[i])

    for i in range(n_register_qubits):
        cx(lhs[i], rhs[i])
