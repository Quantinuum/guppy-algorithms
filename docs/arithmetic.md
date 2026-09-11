# Arithmetic

- Use reversible arithmetic to manipulate values stored in quantum registers,
  including superpositions of values.
- Choose an implementation to suit the required register sizes, carry behavior,
  and available workspace.
- The repository default is little endian.

## Non-modular ripple-carry addition

`adder_ripple_cuccaro_carry_out` implements an optimized Cuccaro ripple-carry
adder. It preserves the addend, overwrites the target with the low bits of the
sum, and records overflow in a separate carry qubit:

$$
\lvert a\rangle\lvert b\rangle\lvert 0\rangle
\longmapsto
\lvert a\rangle\lvert (a+b) \bmod 2^n\rangle
\left\lvert\left\lfloor\frac{a+b}{2^n}\right\rfloor\right\rangle.
$$

```python
from guppylang import guppy
from guppylang.std.builtins import array, nat
from guppylang.std.quantum import qubit

from guppyalgos.primitives.arithmetic.adder.adder_ripple_cuccaro import (
    adder_ripple_cuccaro_carry_out,
)


@guppy
def non_modular_add[n: nat](
    a_qreg: array[qubit, n],
    b_qreg: array[qubit, n],
    carry_out: qubit,
) -> None:
    adder_ripple_cuccaro_carry_out(a_qreg, b_qreg, carry_out)
```

- Initialize `carry_out` in `|0\rangle`.
- `a_qreg` is restored unchanged.
- `b_qreg` contains the low $n$ bits of the result.
- Together, `b_qreg` and `carry_out` represent the full $(n+1)$-bit,
  non-modular sum.
- The implementation allocates and cleans up its internal work qubit.

See the {doc}`ripple-carry addition notebook
<examples/arithmetic/ripple_carry_addition_example>` for state preparation,
measurement,
and the corresponding subtraction example.

## Multiplication and exponentiation

- The {doc}`multiplication example <examples/arithmetic/multiplier>` shows how
  to compose a product circuit from arithmetic components.
- The {doc}`exponentiation example <examples/arithmetic/exponentiator>` builds
  on these routines for a larger arithmetic workflow.
- Check each routine's register and workspace requirements before composing it;
  output widths determine whether a result fits without truncation.

See all {doc}`arithmetic notebooks <example_indexes/arithmetic_index>` for
runnable examples.
