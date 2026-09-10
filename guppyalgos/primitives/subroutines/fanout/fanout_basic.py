"""Basic fanout operation for quantum computing."""

from typing import no_type_check

from guppylang import guppy
from guppylang.std.builtins import array, nat
from guppylang.std.quantum import cx, qubit


@guppy
@no_type_check
def fanout_basic[n_data_qubits: nat](
    control: qubit,
    data_qs: array[qubit, n_data_qubits],
) -> None:
    """Apply basic fanout to one flat data register."""
    for i in range(n_data_qubits):
        cx(control, data_qs[i])
