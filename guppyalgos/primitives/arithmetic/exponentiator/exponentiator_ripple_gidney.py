"""Exponentiator using Gidney's ripple-carry adder."""

from typing import no_type_check

from guppylang import guppy
from guppylang.defs import GuppyFunctionDefinition
from guppylang.std.builtins import Function, array, comptime, nat
from guppylang.std.quantum import qubit

from guppyalgos.primitives.arithmetic.multiplier.multiplier_ripple_gidney import (
    cntrl_multiplier_ripple_gidney_mod_in_place,
)


def _base_pow_2_exp_mod(base: int, modulus: int, index: int) -> int:
    """Compute ``base^(2^index) mod modulus`` via repeated squaring.

    Args:
        base: Classical base.
        modulus: Classical modulus.
        index: Non-negative index of the power of two exponent.

    Returns:
        The value ``base^(2^index) mod modulus``.

    """
    result = base % modulus
    for _ in range(index):
        result = (result * result) % modulus
    return result


def _cntrl_multiplier(
    size: int,
    b: int,
) -> GuppyFunctionDefinition:
    """Build a controlled multiplier specialized to a classical constant."""
    if size == 0:

        @guppy
        @no_type_check
        def multiplier(ctrl: qubit, a_reg: array[qubit, size]) -> None:
            pass

        return multiplier

    @guppy
    @no_type_check
    def multiplier(ctrl: qubit, a_reg: array[qubit, size]) -> None:
        cntrl_multiplier_ripple_gidney_mod_in_place(ctrl, a_reg, b)

    return multiplier


@guppy.comptime
@no_type_check
def _build_multipliers[n_exponent: nat, n_output: nat](
    base: int @ comptime,
) -> array[Function[[qubit, array[qubit, n_output]], None], n_exponent]:
    if base < 0:
        msg = "In-place exponentiation requires a non-negative base"
        raise ValueError(msg)
    if base % 2 == 0:
        msg = "In-place exponentiation modulo 2**n requires an odd base"
        raise ValueError(msg)
    return [
        _cntrl_multiplier(n_output, _base_pow_2_exp_mod(base, 2**n_output, i))
        for i in range(n_exponent)
    ]


@guppy
@no_type_check
def exponentiator_ripple_gidney_mod[n_exponent: nat, n_output: nat](
    exponent_reg: array[qubit, n_exponent],
    output_reg: array[qubit, n_output],
    base: int @ comptime,
) -> None:
    """Multiply the output register by ``base^exponent`` modulo ``2**n_output``.

    Base must be odd since the multiplication is performed in-place, and multiplication
    modulo ``2**n_output`` requires an odd multiplicand for reversibility.

    Explicitly, performs the transformation
    ``|x⟩|a⟩ → |x⟩|a * base^x mod 2**n_output⟩``.

    Args:
        exponent_reg: Quantum register holding the exponent.
        output_reg: Quantum register to store the result. Typically initialized to
            ``|1⟩``.
        base: Classical base to be exponentiated.

    Raises:
        ValueError: If the base is negative or even.

    """
    multipliers: array[Function[[qubit, array[qubit, n_output]], None], n_exponent] = (
        _build_multipliers(base)
    )
    for i in range(n_exponent):
        multipliers[i](exponent_reg[i], output_reg)
