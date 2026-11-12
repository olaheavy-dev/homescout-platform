"""Metadata tests: the generator depends only on the engine (decision 0039 section 1)."""

import ast
import sys
from importlib import import_module
from importlib.metadata import requires
from pathlib import Path


def test_requires_generator_depends_only_on_engine() -> None:
    assert requires("vestagraph-generator") == ["vestagraph-engine"]


def test_import_generator_ships_py_typed_marker() -> None:
    package = import_module("vestagraph_generator")
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


def test_import_generator_modules_use_only_the_engine_and_the_standard_library() -> None:
    package = import_module("vestagraph_generator")
    assert package.__file__ is not None

    names = _imported_top_level_names(Path(package.__file__).parent)

    allowed = set(sys.stdlib_module_names) | {"vestagraph_engine", "vestagraph_generator"}
    assert names, "no imports found: the check would prove nothing"
    assert names - allowed == set()
    assert "vestagraph_engine" in names


def test_import_generator_does_not_use_the_float_type_for_money() -> None:
    package = import_module("vestagraph_generator")
    assert package.__file__ is not None

    for file in Path(package.__file__).parent.glob("*.py"):
        used = {
            n.id
            for n in ast.walk(ast.parse(file.read_text(encoding="utf-8")))
            if isinstance(n, ast.Name)
        }
        assert "float" not in used, f"{file.name} uses float"
