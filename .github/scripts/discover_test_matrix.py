#!/usr/bin/env python3
"""Discover deterministic test shards without running tests or modifying the repo."""

from __future__ import annotations

import json
import os
from pathlib import Path

NESTED_MATRIX_DIRS = {"algorithms", "primitives"}


def _is_test(path: Path) -> bool:
    return path.is_file() and (path.match("test_*.py") or path.match("*_test.py"))


def discover_test_paths(tests_dir: Path = Path("tests")) -> list[str]:
    """Include every test once, with notebooks handled by their dedicated job."""
    paths: list[Path] = []
    for path in sorted(tests_dir.iterdir()):
        if path.name == "notebooks":
            continue
        if _is_test(path):
            paths.append(path)
        elif path.is_dir() and path.name in NESTED_MATRIX_DIRS:
            for child in sorted(path.iterdir()):
                if _is_test(child) or (
                    child.is_dir() and any(_is_test(p) for p in child.rglob("*.py"))
                ):
                    paths.append(child)
        elif path.is_dir() and any(_is_test(p) for p in path.rglob("*.py")):
            paths.append(path)
    if not paths:
        raise ValueError("No non-notebook tests found")
    return [path.as_posix() for path in paths]


def main() -> None:
    """Write the matrix to GitHub Actions output, or print it for local inspection."""
    value = json.dumps(discover_test_paths())
    line = f"test-paths={value}\n"
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a", encoding="utf-8") as output_file:
            output_file.write(line)
    print(line, end="")


if __name__ == "__main__":
    main()
