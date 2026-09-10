# Feature highlights

These examples show how the core ideas are used in larger algorithms.

## Phase estimation over different register shapes

Canonical phase estimation is a practical example of the same generic-register
pattern. Its essential interface is:

$$
U|\psi\rangle=e^{2\pi i\phi}|\psi\rangle,
\qquad
\mathrm{QPE}(U,|\psi\rangle)\longrightarrow|\widetilde{\phi}\rangle|\psi\rangle.
$$

```python
from guppylang import guppy
from guppylang.std.builtins import Function, array, nat
from guppylang.std.quantum import qubit


@guppy
def qpe[n_phase: nat, UnitaryRegs](
    phase_qreg: array[qubit, n_phase],
    unitary_qregs: UnitaryRegs,
    power_oracle: Function[[qubit, UnitaryRegs, int], None],
) -> None:
    ...
```

- `qpe` implements phase estimation without inspecting `unitary_registers`.
- `UnitaryRegs` describes the complete register shape needed by the selected
  unitary implementation.
- The same `UnitaryRegs` appears in the register argument and the oracle
  signature, so Guppy checks that they are compatible.
- Switching algorithms changes the registers and power oracle, not `qpe`.

For Trotterized time evolution, the unitary usually acts on one state register:

```python
@guppy
def trotter_power_oracle[n_state: nat](
    control: qubit,
    state_qreg: array[qubit, n_state],
    power: int,
) -> None:
    for _ in range(power):
        cntrl_trotter_step(control, state_qreg, time_step)
```

- Here, `UnitaryRegs` becomes `array[qubit, n_state]`.
- The oracle realizes each requested power by repeating a controlled Trotter
  step.

Qubitization needs both a PREPARE register and the target registers used by its
block encoding. They can be grouped into one generic register value:

```python
@guppy.struct
class QubitizationRegs[n_prepare: nat, TargetRegs]:
    prep_qreg: array[qubit, n_prepare]
    target_qregs: TargetRegs


@guppy
def qubitization_power_oracle[n_prepare: nat, TargetRegs](
    control: qubit,
    qregs: QubitizationRegs[n_prepare, TargetRegs],
    power: int,
) -> None:
    for _ in range(power):
        cntrl_walk(control, qregs.prep_qreg, qregs.target_qregs)
```

- Here, `UnitaryRegs` becomes
  `QubitizationRegs[n_prepare, TargetRegs]`.
- `cntrl_walk` applies one controlled qubitization step; the power oracle
  repeats it exactly as the Trotter oracle repeats its controlled step.
- `TargetRegs` can itself be a qubit array, tuple, or Guppy struct, provided the
  controlled walk and power oracle accept the same type.

This keeps phase estimation independent of how the simulated unitary arranges
its state and work registers. See the
{doc}`canonical phase-estimation notebook
<examples/phase_estimation/canonical_phase_estimation>`
for array and struct examples, and the
{doc}`Trotterized phase-estimation notebook
<examples/phase_estimation/zixy_phase_estimation>`
for complete powered-Trotter oracles.

## Trotterized Hamiltonian simulation

Trotterization approximates Hamiltonian time evolution by applying
exponentials of simpler terms:

$$
H=\sum_{j=1}^{m}h_j,
\qquad
U(t)=e^{-iHt}.
$$

### Zixy Hamiltonians

[Zixy](https://github.com/CQCL/zixy) stores a Hamiltonian as a sum of
coefficient-weighted Pauli strings:

$$
H=\sum_{j=1}^{m}a_jP_j,
\qquad
P_j\in\{I,X,Y,Z\}^{\otimes n}.
$$

```python
import zixy.qubit.pauli as zqp

pauli_string = zqp.String.from_str("Z0 X1", 2)
hamiltonian = zqp.RealTermSum.from_str(
    "(-0.5, Z0 X1), (-0.1, X0 Z1), (-0.2, Y0 Y1)"
)
```

- `zqp.String` represents one tensor product of Pauli operators.
- `zqp.RealTermSum` represents a Hermitian Pauli Hamiltonian by pairing those
  strings with real coefficients.
- `trotter_first_order` converts every non-identity term into a Pauli
  exponential.

### Pauli exponentials

`pauli_exp` constructs a Guppy function implementing
a Pauli-string exponential:

$$
U_P(\theta)=e^{-i\theta P/2}.
$$

```python
from guppyalgos.pauli_exp import cntrl_pauli_exp, pauli_exp

pauli_gadget = pauli_exp(pauli_string, n_qubits=2)
controlled_pauli_gadget = cntrl_pauli_exp(pauli_string, n_qubits=2)
```

For $P = Z_0X_1$, the ordinary gadget is:

```{tikz}
:alt: A Pauli gadget for Z on q_0 and X on q_1. A Hadamard changes q_1 to the Z basis, a pair of controlled-NOT gates surrounds an RZ rotation on q_1, and a final Hadamard restores the original basis.

\begin{tikzcd}[column sep=0.7cm]
\lstick{$q_0: Z$} & \qw      & \ctrl{1} & \qw                  & \ctrl{1} & \qw      & \qw \\
\lstick{$q_1: X$} & \gate{H} & \targ{}  & \gate{R_Z(\theta)} & \targ{}  & \gate{H} & \qw
\end{tikzcd}
```

The controlled form uses the same basis changes and parity ladder, but the
external qubit controls the central rotation:

$$
C(U_P)=|0\rangle\!\langle 0|\otimes I
+|1\rangle\!\langle 1|\otimes U_P(\theta).
$$

```{tikz}
:alt: A controlled Pauli gadget for Z on q_0 and X on q_1. The parity ladder surrounds an RZ rotation on q_1 controlled by an external control qubit.

\begin{tikzcd}[column sep=0.7cm]
\lstick{$c$}      & \qw      & \qw      & \ctrl{2}              & \qw      & \qw      & \qw \\
\lstick{$q_0: Z$} & \qw      & \ctrl{1} & \qw                   & \ctrl{1} & \qw      & \qw \\
\lstick{$q_1: X$} & \gate{H} & \targ{}  & \gate{R_Z(\theta)}  & \targ{}  & \gate{H} & \qw
\end{tikzcd}
```

- Basis changes map every non-identity Pauli to the Z basis.
- A CX ladder computes the joint parity onto its target qubit.
- `pauli_exp` applies `R_Z` to the parity target.
- `cntrl_pauli_exp` replaces it with `CR_Z`, leaving the target operation
  inactive when the external control is zero.
- The CX ladder and basis changes are then uncomputed.
- The uncontrolled factory rejects an identity string. The controlled factory
  preserves its observable relative phase by rotating the control qubit.

See the {doc}`Pauli-exponential notebook
<examples/pauli_exponential/pauli_exponential>` for a
complete executable example and alternative rotation implementations.

### Constructing the Trotter simulation

A first-order Trotter simulation applies the Zixy term exponentials
sequentially, then repeats the resulting step:

$$
e^{-iHt}
\approx
\left(\prod_{j=1}^{m}e^{-ih_jt/r}\right)^r,
\qquad
\text{error}=O\!\left(\frac{t^2}{r}\right).
$$

```python
from guppyalgos.trotter import ham_sim_trotter, trotter_first_order

n_state_qubits = len(hamiltonian.qubits)
trotter_step = trotter_first_order(hamiltonian, n_state_qubits)
simulation = ham_sim_trotter(
    trotter_step, n_steps=10, time_step=0.01,
    n_state_qubits=n_state_qubits,
)
```

See the {doc}`Trotter Hamiltonian-simulation notebook
<examples/hamiltonian_simulation/ham_sim_trotter>` for the complete
construction, execution, and
accuracy comparison.

## QSVT

Quantum singular value transformation (QSVT) applies a polynomial to the
singular values of a block-encoded matrix. If
$U_A$ is an $a$-ancilla block encoding of $A$ with normalization $\alpha$,
then

$$
(\langle 0^a|\otimes I)U_A(|0^a\rangle\otimes I)=\frac{A}{\alpha}.
$$

QSVT interleaves $U_A$, $U_A^\dagger$, and phase rotations to implement a
polynomial transformation:

$$
\frac{A}{\alpha}
\xrightarrow{\mathrm{QSVT}}
P^{(\mathrm{SV})}\!\left(\frac{A}{\alpha}\right).
$$

For a Hermitian matrix, this is the usual matrix polynomial
$P(A/\alpha)$. A standard degree-$d$ QSVT sequence uses a bounded polynomial
with parity matching its degree:

$$
P(-x)=(-1)^dP(x),
\qquad
|P(x)|\leq 1\quad\text{for }x\in[-1,1].
$$

The `QSVT` struct stores the block encoding, its adjoint, and the phase
sequence:

```python
from guppylang import guppy
from guppylang.std.builtins import array, comptime
from guppylang.std.quantum import qubit

from guppyalgos.lcu import LCU
from guppyalgos.qsvt import QSVT

# Assume PREPARE, SELECT, SELECT dagger, and UNPREPARE define a
# block encoding of A / alpha. Phase synthesis is omitted here.
# The block encoding fixes n_prep_qubits and n_matrix_qubits.
qsvt_phases = [...]


@guppy
def apply_matrix_polynomial(
    signal: qubit,
    prep_qreg: array[qubit, n_prep_qubits],
    matrix_qreg: array[qubit, n_matrix_qubits],
) -> None:
    QSVT(
        LCU(prepare, select, unprepare),
        LCU(prepare, select_dagger, unprepare),
        comptime(qsvt_phases),
    ).compose(signal, prep_qreg, matrix_qreg)
```

- `LCU(prepare, select, unprepare)` supplies $U_A$.
- Replacing `select` with `select_dagger` supplies $U_A^\dagger$.
- `qsvt_phases` determines the polynomial $P$ and must use the reflection
  convention expected by `QSVT`.
- The signal and PREPARE registers are projected onto zero to expose the
  transformed block on `matrix_register`.
- The register types describe the block encoding; QSVT itself is independent
  of the application represented by $A$.

See the {doc}`QSVT notebook <examples/block_encoding/qsvt>` for a complete
phase sequence and projected-block verification.

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
