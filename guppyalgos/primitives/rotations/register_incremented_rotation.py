"""Register-controlled ancilla rotations."""

from __future__ import annotations

from typing import no_type_check

from guppylang import guppy
from guppylang.std.angles import angle
from guppylang.std.builtins import array, nat
from guppylang.std.quantum import crz, qubit

from .rotation_helper import RotationAxis


@guppy.struct
class RotationRegisterIncremented[
    n_data_q: nat,
    Axis: RotationAxis,
]:
    """Build a positive register-controlled rotation from data-register bits.

    The little-endian data register encodes the integer
    ``x = sum_j 2**j * data_qreg[j]``. This rotator applies a controlled rotation
    for each bit, with half-turn angle ``2**(j + 1 - n_data_q)`` for bit ``j``.
    The resulting total half-turn parameter is therefore
    ``theta = 2 * x / 2**n_data_q``, matching the positive phase-gradient rotation
    convention without a scaling factor.

    Unlike :class:`RotationPhaseGradient`, this rotator has no private quantum
    resource. It applies the unscaled fixed-point angle schedule directly.

    Args:
        axis: Guppy basis-change object that realizes the positive rotation around
            the X, Y, or Z axis.

    """

    axis: Axis

    @guppy
    @no_type_check
    def compose(
        self,
        data_qreg: array[qubit, n_data_q],
        rotation_target: qubit,
    ) -> None:
        """Apply the register-incremented rotation encoded by ``data_qreg``.

        Args:
            data_qreg: Little-endian register whose bits control the fixed-point
                rotation increments.
            rotation_target: Qubit receiving the resulting positive axis rotation.

        """
        self.axis.prepare_basis(rotation_target)
        for bit_index in range(n_data_q):
            crz(
                data_qreg[bit_index],
                rotation_target,
                angle(2.0 ** (bit_index + 1 - n_data_q)),
            )
        self.axis.restore_basis(rotation_target)

    @guppy.comptime
    @no_type_check
    def daggered(
        self,
        data_qreg: array[qubit, n_data_q],
        rotation_target: qubit,
    ) -> None:
        """Report that the inverse register-incremented rotation is unavailable."""
        raise NotImplementedError
