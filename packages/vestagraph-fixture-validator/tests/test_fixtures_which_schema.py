"""Which file gets which schema, and what is said when none fits (ported from FixtureValidator.cs).

``data/NAME.json`` is checked against ``schema/NAME.schema.json``. A file in ``test-cases/`` or
``generated/`` names its schema in a top-level ``$schema`` field (a path; only its file name
counts).
"""

import json
from pathlib import Path

from fixtures_support import lines
from vestagraph_fixture_validator.validator import validate_fixtures

_NOTHING_REQUIRED = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://probe.invalid/schema/thing.schema.json",
    "type": "object",
}


def _tree(tmp_path: Path, schema_names: tuple[str, ...] = ("thing",)) -> Path:
    for name in schema_names:
        schema = {**_NOTHING_REQUIRED, "$id": f"https://probe.invalid/schema/{name}.schema.json"}
        (tmp_path / "schema").mkdir(exist_ok=True)
        (tmp_path / "schema" / f"{name}.schema.json").write_text(
            json.dumps(schema), encoding="utf-8"
        )
    return tmp_path


def _put(root: Path, folder: str, name: str, text: str) -> None:
    (root / folder).mkdir(exist_ok=True)
    (root / folder / name).write_text(text, encoding="utf-8")


def test_validate_fixtures_data_file_is_checked_against_the_schema_with_its_name(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "data", "thing.json", "[]")

    problems = lines(validate_fixtures(root))

    assert len(problems) == 1
    assert problems[0].startswith("thing.json: /: ")


def test_validate_fixtures_data_file_with_no_schema_of_its_name_names_the_missing_schema(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "data", "mystery.json", "{}")

    problems = lines(validate_fixtures(root))

    assert problems == [f"mystery.json: /: Schema file not found in {root / 'schema'}."]


def test_validate_fixtures_missing_schema_folder_is_reported(tmp_path: Path) -> None:
    _put(tmp_path, "data", "thing.json", "{}")

    problems = lines(validate_fixtures(tmp_path))

    assert problems == [f"thing.json: /: Schema folder not found: {tmp_path / 'schema'}."]


def test_validate_fixtures_data_file_declaring_another_schema_is_reported(tmp_path: Path) -> None:
    root = _tree(tmp_path, ("thing", "other"))
    _put(root, "data", "thing.json", '{"$schema": "../schema/other.schema.json"}')

    problems = lines(validate_fixtures(root))

    assert problems == [
        "thing.json: /$schema: Names other.schema.json "
        "but the file name requires thing.schema.json."
    ]


def test_validate_fixtures_data_file_declaring_its_own_schema_is_accepted(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "data", "thing.json", '{"$schema": "../schema/thing.schema.json"}')

    assert validate_fixtures(root) == []


def test_validate_fixtures_data_file_declaring_null_counts_as_declaring_nothing(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "data", "thing.json", '{"$schema": null}')

    assert validate_fixtures(root) == []


def test_validate_fixtures_test_case_file_names_its_schema_by_file_name_only(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "test-cases", "case.json", '{"$schema": "any/folder/thing.schema.json"}')

    assert validate_fixtures(root) == []


def test_validate_fixtures_test_case_file_with_no_schema_line_is_reported(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    _put(root, "test-cases", "case.json", "{}")

    problems = lines(validate_fixtures(root))

    assert len(problems) == 1
    assert problems[0].startswith(
        "case.json: /$schema: Missing: name the schema this file follows, "
        'for example "../schema/NAME.schema.json".'
    )


def test_validate_fixtures_test_case_file_that_is_not_an_object_has_no_schema_line(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "test-cases", "case.json", "[1]")

    assert lines(validate_fixtures(root))[0].startswith("case.json: /$schema: Missing: ")


def test_validate_fixtures_test_case_file_naming_a_schema_that_is_not_there_is_reported(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "test-cases", "case.json", '{"$schema": "../schema/nope.schema.json"}')

    assert lines(validate_fixtures(root)) == [
        f"case.json: /: Schema file not found in {root / 'schema'}."
    ]


def test_validate_fixtures_schema_field_that_is_not_a_string_is_reported_readably(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "test-cases", "bad.json", '{ "$schema": 5 }')

    assert lines(validate_fixtures(root)) == [
        "bad.json: /$schema: Must be a string naming the schema, "
        'for example "../schema/NAME.schema.json".'
    ]


def test_validate_fixtures_a_file_that_is_not_json_is_reported_against_its_own_name(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "data", "thing.json", "{nope")

    problems = lines(validate_fixtures(root))

    assert len(problems) == 1
    assert problems[0].startswith("thing.json: /: Not valid JSON: ")


def test_validate_fixtures_no_files_at_all_is_a_problem_naming_the_folder(tmp_path: Path) -> None:
    problems = lines(validate_fixtures(tmp_path))

    assert problems == [
        f"{tmp_path}: /: No fixture files found in data/, test-cases/ or generated/."
    ]


def test_validate_fixtures_only_json_files_directly_inside_the_folders_are_read(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    _put(root, "data", "thing.json", "{}")
    _put(root, "data", "notes.md", "not json")
    _put(root, "data", "thing.json.bak", "not json")
    (root / "data" / "nested").mkdir()
    _put(root / "data", "nested", "inner.json", "not json")
    (root / "data" / "folder.json").mkdir()

    assert validate_fixtures(root) == []


def test_validate_fixtures_problems_come_in_folder_order_then_file_name_order(
    tmp_path: Path,
) -> None:
    root = _tree(tmp_path)
    for folder, name in [
        ("generated", "b.json"),
        ("test-cases", "z.json"),
        ("data", "thing.json"),
        ("test-cases", "a.json"),
        ("generated", "a.json"),
        ("data", "Thing2.json"),
    ]:
        _put(root, folder, name, "{nope")

    order = [line.split(":")[0] for line in lines(validate_fixtures(root))]

    assert order == ["Thing2.json", "thing.json", "a.json", "z.json", "a.json", "b.json"]


def test_validate_fixtures_the_same_problem_is_listed_once(tmp_path: Path) -> None:
    root = _tree(tmp_path)
    (root / "schema" / "thing.schema.json").write_text(
        json.dumps(
            {
                **_NOTHING_REQUIRED,
                "allOf": [{"required": ["a"]}, {"required": ["a"]}],
            }
        ),
        encoding="utf-8",
    )
    _put(root, "data", "thing.json", "{}")

    problems = lines(validate_fixtures(root))

    assert len(problems) == len(set(problems)) == 1
