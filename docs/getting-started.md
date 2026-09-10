---
file_format: mystnb
kernelspec:
  name: python3
---

# Getting started

`guppyalgos` provides reusable building blocks for quantum programs written in
[Guppy](https://github.com/Quantinuum/guppylang). A typical workflow is:

1. Use Python to choose or construct a library component.
2. Call that component from a Guppy function.
3. Type-check and compile the Guppy program.

The library requires Python 3.12 or newer. If you have not used Guppy before,
the [Guppy language guide](https://docs.quantinuum.com/guppy/language_guide/language_guide_index.html)
introduces its syntax and type system.

## Installation

We recommend [uv](https://docs.astral.sh/uv/) for managing Python and project
dependencies. After installing uv, create a project and add `guppyalgos`:

```console
uv init my-quantum-project
cd my-quantum-project
uv add guppyalgos
```

This creates an isolated environment and records `guppyalgos` as a project
dependency. To contribute to the library or work from a source checkout, use
the repository's locked environment instead:

```console
git clone https://github.com/Quantinuum/guppy-algorithms.git
cd guppy-algorithms
uv sync --all-extras --dev
```

## Compile your first program

This program prepares a uniform superposition on two qubits:

$$
|00\rangle
\longmapsto
\frac{1}{2}\left(|00\rangle+|01\rangle+|10\rangle+|11\rangle\right).
$$

```python
from guppylang import guppy
from guppylang.std.quantum import discard_array

from guppyalgos.primitives.state_preparation import uniform_state
from guppyalgos.utils import qarray


uniform = uniform_state(4)


@guppy
def main() -> None:
    register = qarray(2)
    uniform(register)
    discard_array(register)


main.check()
package = main.compile()
```

- `uniform_state(4)` runs in Python and builds a Guppy function for a uniform
  state over four basis states.
- `@guppy` marks `main` as code that Guppy will type-check and compile.
- `qarray(2)` allocates two qubits in $|00\rangle$.
- `uniform(register)` applies the function built above. Guppy infers the
  two-qubit register type from `register`.
- `discard_array(register)` consumes the qubits when they are no longer needed.
  Guppy requires every qubit to be returned, measured, or discarded.
- `main.check()` checks types and qubit ownership without compiling.
- `main.compile()` produces a HUGR package for a compatible runtime or
  simulator.

## Where to go next

- Read the {doc}`user guide <user-guide>` for registers, higher-order
  functions, structs, protocols, and larger algorithm examples.
- Browse the {doc}`example notebooks <examples_index>` for complete programs
  covering state preparation, arithmetic, Hamiltonian simulation, and phase
  estimation.
- Use the {doc}`API reference <api/api>` when you know which component you
  need and want its exact signature and options.
