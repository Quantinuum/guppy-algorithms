# Feature highlights

These examples show how the core ideas are used in larger algorithms.
Choose a topic or jump directly to one of its subsections.

```{toctree}
:maxdepth: 3

trotterised-hamiltonian-simulation.md
block-encoding.md
phase-estimation.md
```

## Measurement

The measurement module provides the basic circuit and statistics tools needed
to estimate real Pauli observables. For a Zixy Hamiltonian
$H=\sum_j c_jP_j$, it combines independently sampled Pauli terms as

$$
\widehat{\langle H\rangle}=\sum_j c_j\widehat{\langle P_j\rangle}.
$$

- `make_direct_measure_pauli_simple` rotates a state into the measurement basis
  for one Pauli string and returns the measured bitstring.
- `make_hadamard_test_pauli` provides the corresponding ancilla-based Hadamard
  test.
- The estimators convert binary samples or full-register bitstrings into an
  expectation value, variance, and standard error.

Coverage is intentionally limited to these common building blocks and simple
independent-term statistics. More advanced workflows—such as measurement
grouping, optimized shot allocation, covariance-aware estimators, or error
mitigation—can consume the same samples from a dedicated external package.

See the {doc}`direct operator-averaging notebook
<examples/measurement/operator_averaging_direct>` and the {doc}`Hadamard-test
operator-averaging notebook <examples/measurement/operator_averaging>` for
complete examples.

## Arithmetic

### Non-modular ripple-carry addition

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

from guppyalgos.arithmetic import adder_ripple_cuccaro_carry_out


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
