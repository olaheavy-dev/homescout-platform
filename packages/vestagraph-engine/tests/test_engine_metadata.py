"""Metadata test: the engine has no runtime dependencies (decision 0039 section 1)."""

from importlib import import_module
from importlib.metadata import requires
from pathlib import Path


def test_requires_engine_package_has_no_runtime_dependencies() -> None:
    assert requires("vestagraph-engine") is None


def test_import_engine_ships_py_typed_marker() -> None:
    package = import_module("vestagraph_engine")
    assert package.__file__ is not None
    assert (Path(package.__file__).parent / "py.typed").is_file()
