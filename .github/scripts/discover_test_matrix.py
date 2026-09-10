#!/usr/bin/env python3
"""Discover and bucket test folders for the parallel test workflow.

It can update tests/test_benchmark.json when stale or missing entries are found,
commit/push those changes, and set GitHub Actions outputs for downstream jobs.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

BENCHMARK_FILE = Path("tests/test_benchmark.json")
TESTS_DIR = Path("tests")
EXCLUDED_TEST_DIRS = {"__pycache__", ".pytest_cache"}
NESTED_MATRIX_DIRS = {"algorithms", "primitives"}


def _run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True)


def _run_capture(
    cmd: list[str], *, check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def _set_output(name: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    line = f"{name}={value}\n"
    if github_output:
        with open(github_output, "a", encoding="utf-8") as output_file:
            output_file.write(line)
    else:
        # Fallback for local runs.
        print(f"{name}={value}")


def _read_benchmark() -> dict[str, float]:
    with BENCHMARK_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(
            f"Expected object in {BENCHMARK_FILE}, got {type(data).__name__}"
        )
    return data


def _write_benchmark(data: dict[str, float]) -> None:
    with BENCHMARK_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        file.write("\n")


def _discover_folders() -> list[str]:
    """Return test paths used as units of work by the CI matrix.

    Most top-level test directories remain a single matrix entry. The broad
    ``algorithms`` and ``primitives`` categories are split into their immediate
    children so they can execute in parallel instead of serializing most of the
    suite into two jobs.
    """
    discovered: list[str] = []
    for path in sorted(TESTS_DIR.iterdir()):
        if not path.is_dir():
            continue
        if path.name in EXCLUDED_TEST_DIRS:
            continue

        if path.name in NESTED_MATRIX_DIRS:
            for child in sorted(path.iterdir()):
                if not child.is_dir() or child.name in EXCLUDED_TEST_DIRS:
                    continue
                if not any(child.rglob("test_*.py")):
                    continue
                discovered.append(child.relative_to(TESTS_DIR).as_posix())
            continue

        if not any(path.rglob("test_*.py")):
            continue
        discovered.append(path.name)
    return discovered


def _commit_and_push_if_needed(commit_message: str) -> None:
    _run(["git", "config", "user.name", "hugrbot"])
    _run(["git", "config", "user.email", "hugrbot@users.noreply.github.com"])
    _run(["git", "add", str(BENCHMARK_FILE)])

    diff_check = _run_capture(["git", "diff", "--cached", "--quiet"], check=False)
    if diff_check.returncode == 0:
        return

    _run(["git", "commit", "-m", commit_message])

    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    head_ref = os.environ.get("GITHUB_HEAD_REF", "")
    ref_name = os.environ.get("GITHUB_REF_NAME", "")

    if event_name == "pull_request" and head_ref:
        _run(["git", "push", "origin", f"HEAD:{head_ref}"])
    elif ref_name:
        _run(["git", "push", "origin", f"HEAD:{ref_name}"])
    else:
        raise RuntimeError(
            "Could not determine branch to push to (missing GITHUB_REF_NAME)."
        )


def _benchmark_folder_seconds(folder: str) -> int:
    start = int(time.time())
    _run(["uv", "run", "pytest", "-q", f"tests/{folder}"])
    end = int(time.time())
    seconds = end - start
    return max(seconds, 1)


def _group_folders(folders: list[str], benchmark: dict[str, float]) -> list[str]:
    buckets: list[str] = []
    current_folders: list[str] = []
    current_weight = 0.0

    def flush_bucket() -> None:
        nonlocal current_folders, current_weight
        if current_folders:
            buckets.append(" ".join(current_folders))
            current_folders = []
            current_weight = 0.0

    for folder in folders:
        weight = float(benchmark.get(folder, 0))
        if weight >= 1:
            # Keep heavyweight folders (for example pauli_exp) isolated.
            flush_bucket()
            buckets.append(folder)
            continue

        current_folders.append(folder)
        current_weight += weight
        if current_weight >= 1:
            flush_bucket()

    flush_bucket()
    return buckets


def main(update_whole: bool = False) -> int:
    """Discover tests, keep benchmark metadata in sync, and write matrix outputs."""
    discovered_folders = _discover_folders()
    update_whole = ("--update-whole" in sys.argv) or update_whole
    current_benchmark = _read_benchmark()
    current_max_time = max(current_benchmark.values(), default=0)
    folder_of_max_time = next(
        folder for folder, time in current_benchmark.items() if time == current_max_time
    )
    if update_whole:
        test_times = [
            _benchmark_folder_seconds(folder) for folder in discovered_folders
        ]
        max_time = max(test_times)
        max_folder = discovered_folders[test_times.index(max_time)]
        print(f"Longest test folder: {max_folder} ({max_time}s)")
        # Update benchmark with relative runtimes.
        benchmark = {
            folder: test_times[ind] / max_time
            for ind, folder in enumerate(discovered_folders)
        }
        _write_benchmark(benchmark)
        return 0

    # Read tests/test_benchmark.json (folder -> relative runtime vs folder_of_max_time),
    # ensure every discovered folder has an entry, then build matrix buckets.
    # Buckets are created by summing relative runtimes in folder order and
    # flushing a bucket whenever the cumulative weight reaches at least 1.0.
    benchmark = _read_benchmark()
    benchmark_ordered_folders = list(benchmark.keys())

    extra = [
        folder
        for folder in benchmark_ordered_folders
        if folder not in discovered_folders
    ]

    if extra:
        print(
            "Stale benchmark entries detected. Removing folders "
            "that no longer exist in tests/."
        )
        for folder in extra:
            print(folder)

        benchmark = {k: v for k, v in benchmark.items() if k in set(discovered_folders)}
        _write_benchmark(benchmark)

        _commit_and_push_if_needed("chore(ci): remove stale test benchmark entries")

        _set_output("benchmark-updated", "true")
        _set_output("test-folders", "[]")
        print(
            "Benchmark file cleaned and pushed. Exiting this run "
            "so CI can rerun with fresh matrix."
        )
        return 0

    missing = [
        folder
        for folder in discovered_folders
        if folder not in benchmark_ordered_folders
    ]

    if missing:
        print(
            "Missing benchmark entries detected. Auto-benchmarking and updating "
            "tests/test_benchmark.json."
        )
        for folder in missing:
            print(folder)

        # Benchmark baseline.
        pauli_seconds = _benchmark_folder_seconds(folder_of_max_time)

        # Benchmark each missing folder and append relative runtime at the end
        # of tests/test_benchmark.json.
        for folder in missing:
            folder_seconds = _benchmark_folder_seconds(folder)
            if folder_seconds > pauli_seconds:
                print(
                    f"Warning: {folder} took longer than {folder_of_max_time}"
                    " to benchmark "
                    f"({folder_seconds}s vs {pauli_seconds}s). "
                    "Running full update to re-benchmark all folders."
                )
                return main(update_whole=True)
            relative = folder_seconds / pauli_seconds
            benchmark[folder] = relative
            _write_benchmark(benchmark)
            print(
                f"Added benchmark: {folder}={relative}"
                f"(relative to {folder_of_max_time})"
            )

        # Commit and push back to the PR branch, then end this run.
        _commit_and_push_if_needed("chore(ci): benchmark missing test folders")

        _set_output("benchmark-updated", "true")
        _set_output("test-folders", "[]")
        print(
            "Benchmark file updated and pushed. Exiting this run "
            "so CI can rerun with fresh matrix."
        )
        return 0

    _set_output("benchmark-updated", "false")

    # Iterate using the order in tests/test_benchmark.json while keeping only
    # folders that currently exist in tests/.
    discovered_set = set(discovered_folders)
    folders = [
        folder for folder in benchmark_ordered_folders if folder in discovered_set
    ]
    grouped_folders = _group_folders(folders, benchmark)

    _set_output("test-folders", json.dumps(grouped_folders))
    print("Discovered test buckets:")
    print(json.dumps(grouped_folders, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        raise
