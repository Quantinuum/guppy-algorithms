"""Comparators for comparing integers in registers."""

from .comparator_ripple_cuccaro import (
    comparator_ripple_cuccaro,
    partial_comparator_ripple_cuccaro,
)
from .comparator_vandaele import comparator_vandaele

__all__ = [
    "comparator_ripple_cuccaro",
    "comparator_vandaele",
    "partial_comparator_ripple_cuccaro",
]
