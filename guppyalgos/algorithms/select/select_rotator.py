"""Generic selection composed from QROM rotations and a Pauli action."""

from __future__ import annotations

from typing import no_type_check

from guppylang import guppy
from guppylang.std.builtins import Function

from guppyalgos.primitives.rotations import QROMRotations, Rotator


@guppy.struct
class SelectRotator[
    IndexRegs,
    TargetRegs,
    RotationTargetRegs,
    ControlRegs,
    ComputeRotator: Rotator[  # ty: ignore[invalid-type-variable-bound]
        TargetRegs, RotationTargetRegs
    ],
]:
    """Generic ``U_mu^dagger P U_mu`` selection around a QROM rotation.

    The forward and inverse operations are supplied as two fully configured
    :class:`QROMRotations` instances. Any shared quantum resource belongs to
    ``RotationRegs`` rather than either rotator, so the same register can be borrowed
    sequentially by both operations. The central Pauli action receives only the
    target stored in :class:`GivensCascadeRegs`, making it independent of any
    resource used by the cascades.

    ``pauli_action`` supplies the central operation on the selection controls and
    rotation target.

    The index, QROM target, rotation, and control registers must own disjoint
    qubits. In particular, a controlled QROM flag belongs to ``IndexRegs``, while
    the controls for the central Pauli action are passed separately. These controls
    must therefore be distinct for each configured selection operation.

    Args:
        qrom_rotations_compute: Fully configured QROM rotation that loads the
            selected data and applies the forward rotator.
        pauli_action: Central controlled-Z or doubly-controlled-Z operation acting
            on the Pauli controls and the first rotation target.
        qrom_rotations_uncompute: Fully configured inverse QROM rotation.

    """

    qrom_rotations: QROMRotations[
        IndexRegs,
        TargetRegs,
        RotationTargetRegs,
        ComputeRotator,
    ]
    pauli_action: Function[[ControlRegs, RotationTargetRegs], None]

    @guppy
    @no_type_check
    def compose(
        self,
        index_regs: IndexRegs,
        data_qregs: TargetRegs,
        control_regs: ControlRegs,
        rotation_regs: RotationTargetRegs,
    ) -> None:
        """Apply the configured QROM cascade, Pauli action, and inverse cascade.

        Args:
            index_regs: Registers used to address and optionally control the QROM.
            data_qregs: QROM target registers holding the loaded rotation data.
            control_regs: One or two qubits controlling the central Pauli action.
            rotation_regs: Registers used by both rotators and the central Pauli
                action. These may include a shared phase-gradient resource.

        """
        self.qrom_rotations.compose(
            index_regs,
            data_qregs,
            rotation_regs,
        )

        self.pauli_action(control_regs, rotation_regs)

        self.qrom_rotations.daggered(
            index_regs,
            data_qregs,
            rotation_regs,
        )
