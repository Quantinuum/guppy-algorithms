"""Regression tests for complete, read-only CI test discovery."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "discover_test_matrix.py"
spec = importlib.util.spec_from_file_location("discover_test_matrix", SCRIPT)
assert spec is not None
assert spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_every_test_has_one_shard(tmp_path: Path) -> None:
    """Cover loose, nested, newly added, and alternative-pattern test files."""
    root = tmp_path / "tests"
    files = [
        "test_root.py",
        "algorithms/test_loose.py",
        "algorithms/new/test_nested.py",
        "primitives/new/deep/example_test.py",
        "new_category/test_new.py",
        "new_category/deep/test_deep.py",
        "notebooks/test_notebook.py",
        "empty/helper.py",
        "test_benchmark.json",
    ]
    for name in files:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    shards = [Path(p) for p in module.discover_test_paths(root)]
    for test in [root / name for name in files[:6]]:
        owners = [s for s in shards if s == test or s in test.parents]
        assert len(owners) == 1, str(test)
    assert not any("notebooks" in p.parts for p in shards)
    assert shards == [Path(p) for p in module.discover_test_paths(root)]
    after = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    assert before == after


def test_empty_suite_fails(tmp_path: Path) -> None:
    """Fail visibly rather than producing an empty passing matrix."""
    with pytest.raises(ValueError, match="No non-notebook tests found"):
        module.discover_test_paths(tmp_path)


def test_repository_coverage() -> None:
    """Require all current library tests to have exactly one matrix owner."""
    root = SCRIPT.parents[2] / "tests"
    shards = [Path(p) for p in module.discover_test_paths(root)]
    tests = [p for p in root.rglob("*.py") if module._is_test(p)]
    assert tests
    for test in tests:
        owners = [s for s in shards if s == test or s in test.parents]
        assert len(owners) == (0 if "notebooks" in test.relative_to(root).parts else 1)
