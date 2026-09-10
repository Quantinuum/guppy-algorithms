"""Single bit adder and half adders."""

from guppylang.std.quantum import toffoli, cx

from guppylang import guppy, qubit


@guppy
def full_adder(c_in: qubit, a: qubit, b: qubit, c_out: qubit) -> None:
    """Bitwise adder, sum bit computed onto b."""
    half_adder(c_in, a, c_out)
    half_adder(a, b, c_out)
    cx(c_in, a)


@guppy
def half_adder(a: qubit, b: qubit, c_out: qubit) -> None:
    """Bitwise half-adder, sum bit computed onto b."""
    toffoli(a, b, c_out)
    cx(a, b)


@guppy
def full_adder_inverse(c_in: qubit, a: qubit, b: qubit, c_out: qubit) -> None:
    """Inverse of bitwise adder, sum bit computed onto b."""
    cx(c_in, a)
    half_adder_inverse(a, b, c_out)
    half_adder_inverse(c_in, a, c_out)


@guppy
def half_adder_inverse(a: qubit, b: qubit, c_out: qubit) -> None:
    """Inverse of bitwise half-adder, sum bit computed onto b."""
    cx(a, b)
    toffoli(a, b, c_out)
