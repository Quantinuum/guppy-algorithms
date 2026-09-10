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
whole library, follow the full-suite commands in [tests/README.md](tests/README.md).
The hooks check formatting, lint, types, spelling, and file hygiene.

## Continuous integration

PRs targeting any branch run the same validation, including layers of a `gh stack`.
CI checks code, tests Python 3.12–3.14, executes notebooks sequentially, builds the
docs, and checks an installed wheel. Validation uses public dependencies and the
read-only built-in GitHub token; contributors do not need CI secrets or a PAT.
Vendored skill material is excluded from formatting and spelling hooks.

The standalone `test-docs-build.yml` workflow provides the `Test sphinx docs` check.
For branch protection, require `CI passed`, `Test sphinx docs`, and
`Conventional Commit title`. `CI passed` covers the jobs in `ci.yml` and fails if
any of them fails, is canceled, or is skipped. All three checks support the merge
queue. Dependency review runs separately on every
PR and rejects newly introduced high or critical severity vulnerabilities; keep
it as a PR review gate, since it does not run on merge-queue events.

## Releases

Release Please manages versions and the changelog from Conventional Commit titles.
Before `1.0.0`, `fix:` and `feat:` increment the patch version; a breaking change
marked with `!` or a `BREAKING CHANGE:` footer increments the minor version.

The unpublished baseline is `0.0.0`. The initial release commit uses the footer
`Release-As: 0.1.0` to request the first public release. Never publish or tag
`0.0.0`; review and merge the release PR when publication is ready. Reserve
`Release-As: 1.0.0` for the deliberate decision to declare the public API stable.

### Publishing setup (maintainers)

Before merging the first public release PR:

1. Keep the repository private during preparation. PyPI publication is disabled
   while it is private. Make it public only when the release is approved.
   In GitHub Actions settings, allow GitHub Actions to create pull requests. Protect
   `main` with the required CI checks described above.
2. Create a GitHub environment named `pypi`, add required reviewers, and allow
   deployment tags matching `v*`. Publishing runs on version tags, not branches.
   Environment protection is configured on GitHub; the workflow file alone does
   not require approval.
3. On PyPI, configure a GitHub Trusted Publisher for `guppyalgos` using:

   | Field | Value |
   | --- | --- |
   | Owner | `Quantinuum` (use the actual owner if the repo moves) |
   | Repository | `guppy-algorithms` |
   | Workflow filename | `build_wheels.yml` |
   | Environment | `pypi` |

   For an existing project, use its Publishing settings. For the first release of
   a new project, configure a pending publisher under your PyPI account's Publishing
   settings. See the [PyPI Trusted Publishing guide](https://docs.pypi.org/trusted-publishers/).

PyPI publishing uses Trusted Publishing and needs no PyPI API token. The separate
Release Please workflow currently uses the `HUGRBOT_PAT` GitHub secret so its
release events can trigger `build_wheels.yml`. Keep that token (or a GitHub App
installation token) when using this event-based setup. Replacing it with
`GITHUB_TOKEN` would require explicit dispatch of the build workflow, because a
release event created with `GITHUB_TOKEN` does not trigger another workflow. See
[GitHub's token behavior](https://docs.github.com/en/actions/concepts/security/github_token).

### Publishing a release

Review the version and changelog in the release PR, mark it ready, and merge it
once all required checks pass. Release Please creates the tag and GitHub release.
The separate `Build wheels` workflow then builds and checks distributions on
Ubuntu x64, Ubuntu ARM, macOS ARM, macOS Intel, and Windows using Python 3.12.
It also builds on pushes to `main` and `release-please--*` branches, and supports
manual runs. Branch runs only validate; publication requires a published release
or a manual run selecting a version tag. The unpublished `0.0.0` baseline is
rejected for publication, and the tag must match the package and manifest versions.

`guppyalgos` is pure Python, so `uv build` produces a universal `py3-none-any` wheel
and a source archive. Every runner validates both distributions with Twine; the
Ubuntu x64 job also installs its wheel and compiles a Guppy program. This matrix
checks packaging across platforms, not native runtime compatibility on every OS.
Cargo caching and `cibuildwheel` are unnecessary for this package.

Once all builds pass, review the artifacts and approve the `pypi` environment
job. It attaches the Ubuntu-built wheel and source archive to the GitHub release
and publishes those same files to PyPI with attestations. The other builds have
the same distribution filenames and are retained as CI artifacts, not merged
into the upload directory. Artifacts are retained for 30 days.

For a failed publication, rerun the failed jobs or manually run `Build wheels`
against the same version tag. `skip-existing: true` allows PyPI retries, and
existing GitHub release assets are preserved. Already-published files cannot be
replaced; if the source needs a correction, release a new version instead of
moving the old tag.

Documentation continues to build separately and is not deployed by this workflow.
