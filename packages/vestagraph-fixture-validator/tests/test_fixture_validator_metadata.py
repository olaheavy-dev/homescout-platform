"""Metadata test: the validator never depends on the engine (decision 0039 section 1)."""

import ast
import re
import sys
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


def _imported_top_level_names(source_folder: Path) -> set[str]:
    names: set[str] = set()
    for file in source_folder.glob("*.py"):
        for node in ast.walk(ast.parse(file.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert node.level == 0, f"{file.name}: use absolute imports"
                assert node.module is not None
                names.add(node.module.split(".")[0])
    return names


def test_import_validator_modules_use_only_jsonschema_referencing_and_the_standard_library() -> (
    None
):
    package = import_module("vestagraph_fixture_validator")
    assert package.__file__ is not None

    names = _imported_top_level_names(Path(package.__file__).parent)

    allowed = set(sys.stdlib_module_names) | {
        "jsonschema",
        "referencing",
        "vestagraph_fixture_validator",
    }
    assert names, "no imports found: the check would prove nothing"
    assert names - allowed == set()
    assert {"jsonschema", "referencing"} <= names
    assert "vestagraph_engine" not in names
