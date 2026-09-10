# guppy-algorithms

A library of reusable primitives for composing abstract quantum algorithms,
written in [Guppy](https://github.com/Quantinuum/guppylang).

The `guppyalgos` package includes quantum arithmetic, state preparation, QROM,
block encoding, Hamiltonian simulation, and phase estimation. Its reusable
components let you choose circuit implementations when assembling an algorithm.

## Getting started

Requires Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).
Install from a source checkout:

```sh
git clone https://github.com/quantinuum-dev/guppy-algorithms.git
cd guppy-algorithms
uv sync
```

Explore the [example notebooks](examples/) and the
[getting-started guide](docs/getting-started.md) for usage and compilation examples.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, checks, and our
`gh stack` workflow for stacked pull requests.

## License

The `guppyalgos` package is licensed under the [Apache License 2.0](LICENSE).
Bundled material with a separate license retains its own license terms.
