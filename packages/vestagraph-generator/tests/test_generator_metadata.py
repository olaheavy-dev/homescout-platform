"""Metadata test: the generator depends only on the engine (decision 0039 section 1)."""

from importlib import import_module
from importlib.metadata import requires
from pathlib import Path


def test_requires_generator_depends_only_on_engine() -> None:
    assert requires("vestagraph-generator") == ["vestagraph-engine"]


def test_import_generator_ships_py_typed_marker() -> None:
    package = import_module("vestagraph_generator")
    assert package.__file__ is not None
    assert (Path(package.__file__).parent / "py.typed").is_file()
