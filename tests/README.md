# Tests Benchmark Guide

The workflow in `.github/workflows/tests-matrix.yml` uses `tests/test_benchmark.json` to build grouped test buckets for parallel CI runs.

## How `test_benchmark.json` is used

- Each key is a path relative to `tests/` (for example,
  `algorithms/time_evolution` or `primitives/rotations`).
- Each value is a relative runtime weight used to balance matrix jobs.
   - Values greater than or equal to `1` are kept in their own jobs.
   - Lower-weight paths are grouped until their combined weight reaches approximately `1`.
- During matrix discovery, CI:
   - Finds top-level folders under `tests/`, expanding `algorithms` and
     `primitives` into separate entries for each immediate subdirectory.
   - Verifies that every discovered folder has an entry in `tests/test_benchmark.json`.
    - If benchmark entries exist for folders that no longer exist in `tests/`, removes
       those stale entries, commits, and pushes to the PR branch.
    - Exits the current workflow run after pushing so CI can rerun with the cleaned benchmark file.
   - If a folder is missing, benchmarks `pauli_exp` and the missing folder(s), updates
     `tests/test_benchmark.json`, commits the change, and pushes it to the PR branch.
   - Exits the current workflow run after pushing so CI can rerun with the updated matrix.
   - Groups folders into buckets by summing relative runtimes until the bucket reaches at least `1.0`, then starts a new bucket.

## When adding a new test folder

Normally no manual action is required. CI will auto-benchmark and update
`tests/test_benchmark.json` for you in PR runs.

Manual update is still available if needed:

1. Benchmark the new path against the current longest benchmarked path.
2. Compute the relative value:

    `relative_time = new_folder_runtime / pauli_exp_runtime`

3. Add the new path entry to `tests/test_benchmark.json` at the BOTTOM of the JSON file.
