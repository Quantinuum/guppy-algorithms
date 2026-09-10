# Running tests

Run the tests affected by your change with `uv run pytest tests/path -q`.
Run the full library suite with `uv run pytest tests --ignore=tests/notebooks -n auto`,
and execute notebooks separately with `uv run pytest tests/notebooks -v`.
Notebook execution must remain sequential.

## CI test discovery

`.github/workflows/ci.yml` runs library tests on Python 3.12, 3.13, and 3.14.
Notebooks run in a separate Python 3.13 job. Preview the test matrix with:

```sh
python3 .github/scripts/discover_test_matrix.py
```

Every top-level test directory becomes a shard, except `algorithms` and
`primitives`, which are split into their immediate subdirectories. Loose test
files at either level also get shards. Both `test_*.py` and `*_test.py` are
included. New test directories are discovered automatically; no timing metadata
is required. Discovery never runs tests or changes files in the repository.

The matrix runs at most six jobs at once. Each library test shard uses four
pytest-xdist workers (`-n 4`) on its own Ubuntu runner. Notebooks remain sequential.
