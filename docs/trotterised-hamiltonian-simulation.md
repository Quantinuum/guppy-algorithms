---
file_format: mystnb
kernelspec:
  name: python3
mystnb:
  execution_mode: force
  execution_timeout: 120
---

# Trotterised Hamiltonian simulation

Trotterization approximates Hamiltonian time evolution by applying
exponentials of simpler terms:

$
H=\sum_{j=1}^{m}h_j,
\qquad
U(t)=e^{-iHt}.
$

## Zixy Hamiltonians

[Zixy](https://github.com/CQCL/zixy) stores a Hamiltonian as a sum of
coefficient-weighted Pauli strings:

$
H=\sum_{j=1}^{m}a_jP_j,
\qquad
P_j\in\{I,X,Y,Z\}^{\otimes n}.
$

```{code-cell} ipython3
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

## Pauli exponentials

`pauli_exp` constructs a Guppy function implementing
a Pauli-string exponential:

$
U_P(\theta)=e^{-i\theta P/2}.
$

```{code-cell} ipython3
from guppyalgos.primitives.pauli.pauli_exp import cntrl_pauli_exp, pauli_exp

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

$
C(U_P)=|0\rangle\!\langle 0|\otimes I
+|1\rangle\!\langle 1|\otimes U_P(\theta).
$

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

## Constructing the Trotter simulation

A first-order Trotter simulation applies the Zixy term exponentials
sequentially, then repeats the resulting step:

$
e^{-iHt}
\approx
\left(\prod_{j=1}^{m}e^{-ih_jt/r}\right)^r,
\qquad
\text{error}=O\!\left(\frac{t^2}{r}\right).
$

```{code-cell} ipython3
from guppyalgos.algorithms.time_evolution.trotter import ham_sim_trotter, trotter_first_order

n_state_qubits = len(hamiltonian.qubits)
trotter_step = trotter_first_order(hamiltonian, n_state_qubits)
simulation = ham_sim_trotter(
    trotter_step, n_steps=10, time_step=0.01,
    n_state_qubits=n_state_qubits,
)
```

See the {doc}`Trotter Hamiltonian-simulation notebook
<examples/hamiltonian_simulation/ham_sim_trotter_demo>` for the complete
construction, execution, and
accuracy comparison.

Continue with {doc}`phase-estimation` to use controlled Trotter steps in QPE.
