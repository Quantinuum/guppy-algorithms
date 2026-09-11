# guppyalgos documentation

[guppy-algorithms](https://github.com/Quantinuum/guppy-algorithms) is a
library of reusable quantum-algorithm components built on
[guppy](https://docs.quantinuum.com/guppy/language_guide/language_guide_index.html). It combines
type-safe guppy primitives with Python builders for algorithms that start from
classical data.

The API is experimental before version 1.0 and may change between releases.
Pin the package version for reproducible work and review the
[changelog](https://github.com/Quantinuum/guppy-algorithms/blob/main/CHANGELOG.md) before upgrading.

Start with **Getting started** to compile a first program. The user guide
introduces the library and its composition patterns; the notebooks provide
runnable workflows, while the API reference documents individual components.

**See the library in action:** {doc}`examples/block_encoding/block_encoding_demo`
builds a Hamiltonian block encoding, adds a control, and transforms it with
qubitisation and QSVT. Small numerical examples and LaTeX equations connect each
operation to its encoded matrix, with an introduction to the THC workflow.


```{toctree}
:maxdepth: 2
:titlesonly:

getting-started.md
user-guide.md
```

```{toctree}
:maxdepth: 1
:titlesonly:

api/api.md
examples_index.md
```
