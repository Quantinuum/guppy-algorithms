"""Diagonal operator module — unitary and non-unitary synthesis."""

from .walsh import diagonal_unitary_walsh, fast_walsh_hadamard_transform

__all__ = ["diagonal_unitary_walsh", "fast_walsh_hadamard_transform"]
