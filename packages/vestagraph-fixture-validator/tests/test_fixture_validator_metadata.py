"""Metadata test: the validator never depends on the engine (decision 0039 section 1)."""

import re
from importlib import import_module
from importlib.metadata import requires
from pathlib import Path


def test_requires_validator_never_depends_on_engine() -> None:
    requirements = requires("vestagraph-fixture-validator") or []
    names = {re.split(r"[\s<>=!~;\[]", requirement, maxsplit=1)[0] for requirement in requirements}
    assert names == {"jsonschema", "referencing"}


def test_import_fixture_validator_ships_py_typed_marker() -> None:
    package = import_module("vestagraph_fixture_validator")
    assert package.__file__ is not None
    assert (Path(package.__file__).parent / "py.typed").is_file()
