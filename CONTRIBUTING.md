# Contributing

Open an issue for a bug, feature, or proposed algorithm before starting substantial
work. Include a minimal reproducer for bugs and a paper reference for new algorithms.

## Development setup

Use Python 3.12 or newer and [uv](https://docs.astral.sh/uv/). From a source
checkout, install the development dependencies and Git hooks:

```sh
uv sync --extra dev-dependencies
uv run prek install
```

## Pull requests and gh stack

Keep each PR focused on one logical change. We use
[`gh stack`](https://github.com/github/gh-stack) for dependent changes: each branch
builds on the previous one, giving reviewers a small diff for each layer. A single
PR is fine for an independent change.

Install and authenticate the [GitHub CLI](https://cli.github.com/), then install
the extension:

```sh
gh auth login
gh extension install github/gh-stack
```

For a change with two dependent parts:

```sh
gh stack init --base main feature/core
# Make and commit the first part.
gh stack add feature/integration
# Make and commit the dependent part.
gh stack submit
```

Use `gh stack sync` to update the stack after changes or merges. See the
[gh stack guide](https://github.github.com/gh-stack/introduction/overview/)
for rebasing, navigation, and other commands.

Open draft PRs while work is in progress. Link each PR to exactly one issue with
`Closes #123`, and use a Conventional Commit title such as `feat: add an algorithm`
or `fix: correct a rotation`. Describe the behavior change and how you tested it.

## Before requesting review

- Add or update tests for behavior changes, and update docs for public API changes.
- Use American English in prose and identifiers; follow nearby code conventions.
- Cite the source paper when implementing an algorithm.
- Run the affected tests first, then the repository checks:

```sh
uv run pytest tests/path/to/test_module.py -q
uv run prek run --all-files
```

Replace the example test path with the relevant files. For changes that affect the
whole library, run `uv run pytest -n auto`. The hooks check formatting, lint,
types, spelling, and file hygiene.

## Releases

Release Please manages versions and the changelog from Conventional Commit titles.
Before `1.0.0`, `fix:` and `feat:` increment the patch version; a breaking change
marked with `!` or a `BREAKING CHANGE:` footer increments the minor version.

The unpublished baseline is `0.0.0`. The initial release commit uses the footer
`Release-As: 0.1.0` to request the first public release. Never publish or tag
`0.0.0`; review and merge the release PR when publication is ready. Reserve
`Release-As: 1.0.0` for the deliberate decision to declare the public API stable.
