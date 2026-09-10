"""Helpers for basis-changed single-qubit rotation axes."""

from __future__ import annotations

from guppylang import guppy
from guppylang.std.quantum import h, qubit, s, sdg


@guppy.protocol
class RotationAxis:
    """Guppy object providing basis changes for a single-qubit rotation axis."""

    @guppy.require
    def prepare_basis(self, target_q: qubit) -> None:
        """Change basis before applying the underlying ``Rz`` rotation."""
        ...

    @guppy.require
    def restore_basis(self, target_q: qubit) -> None:
        """Undo the basis change after applying the underlying ``Rz`` rotation."""
        ...


@guppy.struct
class RotationAxisX:
    """Guppy axis object realizing ``Rx`` through an ``Rz`` basis change."""

    @guppy
    def prepare_basis(self, target_q: qubit) -> None:
        """Rotate the target from the Z basis into the X basis."""
        h(target_q)

    @guppy
    def restore_basis(self, target_q: qubit) -> None:
        """Return the target from the X basis to the Z basis."""
        h(target_q)


@guppy.struct
class RotationAxisY:
    """Guppy axis object realizing ``Ry`` through an ``Rz`` basis change."""

    @guppy
    def prepare_basis(self, target_q: qubit) -> None:
        """Rotate the target from the Z basis into the Y basis."""
        sdg(target_q)
        h(target_q)

    @guppy
    def restore_basis(self, target_q: qubit) -> None:
        """Return the target from the Y basis to the Z basis."""
        h(target_q)
        s(target_q)


@guppy.struct
class RotationAxisZ:
    """Guppy axis object leaving the underlying ``Rz`` rotation unchanged."""

    @guppy
    def prepare_basis(self, target_q: qubit) -> None:
        """Leave the target in the Z basis."""
        pass

    @guppy
    def restore_basis(self, target_q: qubit) -> None:
        """Leave the target in the Z basis."""
        pass
