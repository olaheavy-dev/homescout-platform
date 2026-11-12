"""Shared helpers for the fixture-validator tests.

Every test starts from the repository's real fixture files and breaks one thing; no copy of the
data is kept here (AGENTS rule 2). Decimals are read as exact fractions (``Fraction``), so a
test can tell ``240000.5`` and ``5.0`` from a whole number, the same way the validator does.
"""

import copy
import json
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_fixture_validator.validator import FixtureProblem, validate_instance

Json = Any


def repository_root() -> Path:
    for folder in Path(__file__).resolve().parents:
        if (folder / "packages" / "fixtures" / "data").is_dir():
            return folder
    message = "The repository root was not found above the tests."
    raise RuntimeError(message)


def fixtures_directory() -> Path:
    return repository_root() / "packages" / "fixtures"


def schema_directory() -> Path:
    return fixtures_directory() / "schema"


def parse(text: str) -> Json:
    """Read JSON text with decimals as exact fractions."""
    return json.loads(text, parse_float=Fraction)


def number(text: str) -> Fraction | int:
    """A JSON number written as ``text``, for example ``"240000.5"`` or ``"5.0"``."""
    parsed: Fraction | int = parse(text)
    return parsed


def read_file(path: Path) -> Json:
    return parse(path.read_text(encoding="utf-8"))


def load(name: str) -> Json:
    """The parsed ``data/NAME.json``."""
    return read_file(fixtures_directory() / "data" / f"{name}.json")


def load_test_case_file(name: str) -> Json:
    return read_file(fixtures_directory() / "test-cases" / f"{name}.json")


def _item(file: str, key: str, item_id: str) -> Json:
    matches = [i for i in load(file)[key] if i["id"] == item_id]
    assert len(matches) == 1, item_id
    return copy.deepcopy(matches[0])


def evidence_item(item_id: str) -> Json:
    return _item("evidence", "evidence", item_id)


def area_item(item_id: str) -> Json:
    return _item("area", "area", item_id)


def area_items() -> list[Json]:
    items: list[Json] = load("area")["area"]
    return items


def home(home_id: str) -> Json:
    return _item("homes", "homes", home_id)


def question(question_id: str) -> Json:
    return _item("questions", "questions", question_id)


def validate_record(schema_name: str, collection_key: str, record: Json) -> list[FixtureProblem]:
    """Wrap one record in its file shape and check it against that file's schema."""
    return validate_instance(
        {collection_key: [copy.deepcopy(record)]}, f"{schema_name}.schema.json", schema_directory()
    )


def lines(problems: list[FixtureProblem]) -> list[str]:
    return [str(p) for p in problems]


def mentions(problems: list[FixtureProblem], text: str) -> bool:
    """True when some problem line contains ``text`` (the C# tests' ``Has.Some.Contain``)."""
    return any(text in line for line in lines(problems))


def copy_fixture_folders(target: Path, folders: tuple[str, ...]) -> Path:
    """Copy the real ``*.json`` files of the named folders into a new fixtures folder."""
    for folder in folders:
        (target / folder).mkdir(parents=True)
        for file in sorted((fixtures_directory() / folder).glob("*.json")):
            shutil.copy(file, target / folder / file.name)
    return target
