"""Parity probes (P5 task 1): the Python validator must judge files as the C# one does.

The expected answers below are what the C# validator (JsonSchema.Net 9.6.0, JSON Schema 2020-12)
does, found by running that library on each case on 12 Nov 2026; they are not read from the Python
validator. Each probe builds a tiny fixtures folder with one schema (``probe.schema.json``) and one
data file (``data/probe.json``, checked against the schema of the same name).
"""

import json
from pathlib import Path

import pytest
from fixtures_support import Json, lines, read_file, schema_directory
from vestagraph_fixture_validator.validator import validate_fixtures

_DIALECT = "https://json-schema.org/draft/2020-12/schema"
_BASE = "https://probe.invalid/schema/"


def _write_schema(fixtures: Path, name: str, body: Json) -> None:
    schema = {"$schema": _DIALECT, "$id": f"{_BASE}{name}.schema.json", **body}
    (fixtures / "schema" / f"{name}.schema.json").write_text(json.dumps(schema), encoding="utf-8")


def _probe(
    tmp_path: Path,
    schema: Json,
    data: str | bytes,
    *,
    extra_schemas: dict[str, Json] | None = None,
) -> list[str]:
    fixtures = tmp_path / "fixtures"
    (fixtures / "schema").mkdir(parents=True)
    (fixtures / "data").mkdir()
    _write_schema(fixtures, "probe", schema)
    for name, body in (extra_schemas or {}).items():
        _write_schema(fixtures, name, body)
    target = fixtures / "data" / "probe.json"
    if isinstance(data, bytes):
        target.write_bytes(data)
    else:
        target.write_text(data, encoding="utf-8")
    return lines(validate_fixtures(fixtures))


# --- Dialect and references -------------------------------------------------------------------


def test_validate_fixtures_prefix_items_a_2020_12_keyword_is_enforced(tmp_path: Path) -> None:
    schema = {"prefixItems": [{"type": "integer"}]}

    assert _probe(tmp_path / "bad", schema, '["a"]') != []
    assert _probe(tmp_path / "good", schema, "[1]") == []


def test_validate_fixtures_dependent_required_is_enforced(tmp_path: Path) -> None:
    schema = {"dependentRequired": {"a": ["b"]}}

    assert any("b" in line for line in _probe(tmp_path / "bad", schema, '{"a": 1}'))
    assert _probe(tmp_path / "good", schema, '{"a": 1, "b": 2}') == []


def test_validate_fixtures_ref_next_to_other_keywords_applies_both(tmp_path: Path) -> None:
    schema = {"$ref": "#/$defs/short", "minLength": 2, "$defs": {"short": {"maxLength": 3}}}

    assert _probe(tmp_path / "long", schema, '"abcd"') != []
    assert _probe(tmp_path / "tiny", schema, '"a"') != []
    assert _probe(tmp_path / "ok", schema, '"abc"') == []


def test_validate_fixtures_ref_to_another_schema_file_resolves_by_id(tmp_path: Path) -> None:
    schema = {"properties": {"n": {"$ref": "shared.schema.json#/$defs/small"}}}
    shared = {"$defs": {"small": {"type": "integer", "maximum": 9}}}

    bad = _probe(tmp_path / "bad", schema, '{"n": 10}', extra_schemas={"shared": shared})
    good = _probe(tmp_path / "good", schema, '{"n": 9}', extra_schemas={"shared": shared})

    assert any("/n" in line for line in bad)
    assert good == []


def test_validate_fixtures_ref_to_a_schema_that_does_not_exist_is_reported_not_fetched(
    tmp_path: Path,
) -> None:
    schema = {"properties": {"n": {"$ref": "https://probe.invalid/schema/missing.schema.json"}}}

    problems = _probe(tmp_path, schema, '{"n": 1}')

    assert len(problems) == 1
    assert problems[0].startswith("probe.json: /")
    assert "missing.schema.json" in problems[0]


def test_validate_fixtures_a_property_the_schema_forbids_with_false_is_reported_at_that_property(
    tmp_path: Path,
) -> None:
    # jsonschema 4.26 leaves the property name out of the path of an error from a `false` subschema;
    # the schemas use `"value": false` to say "no value here", so the pointer must still name it.
    schema = {"properties": {"outer": {"properties": {"value": False}}}}

    problems = _probe(tmp_path, schema, '{"outer": {"value": 1}}')

    assert len(problems) == 1
    assert problems[0].startswith("probe.json: /outer/value: ")


def test_the_schema_files_never_use_a_false_subschema_where_the_path_fix_does_not_reach() -> None:
    # The path fix in the validator covers `properties` only (see its comment). A `false` under
    # `then`, `else`, `not` and the like adds no path part, so nothing is lost there. If a schema
    # starts using `false` under a keyword that does add one, this fails so the validator is fixed
    # first, not after a pointer goes missing.
    path_keywords_taking_a_schema = {"items", "unevaluatedItems", "unevaluatedProperties"}
    found: list[str] = []

    def walk(node: Json, keyword: str, where: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                if child is False and (
                    key in path_keywords_taking_a_schema or keyword == "patternProperties"
                ):
                    found.append(f"{where}/{key}")
                walk(child, key, f"{where}/{key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                if child is False and keyword == "prefixItems":
                    found.append(f"{where}/{index}")
                walk(child, keyword, f"{where}/{index}")

    for path in sorted(schema_directory().glob("*.schema.json")):
        walk(read_file(path), "", path.name)

    assert found == []


def test_validate_fixtures_a_pointer_escapes_slash_and_tilde_in_a_property_name(
    tmp_path: Path,
) -> None:
    schema = {"properties": {"a/b": {"type": "integer"}, "c~d": {"type": "integer"}}}

    problems = _probe(tmp_path, schema, '{"a/b": "x", "c~d": "y"}')

    assert [p.split(": ")[1] for p in problems] == ["/a~1b", "/c~0d"]


# --- format is an annotation, never an assertion (JsonSchema.Net 2020-12 default) -------------


@pytest.mark.parametrize(
    ("format_name", "bad_value"),
    [
        ("date", "not-a-date"),
        ("email", "nope"),
        ("uri", "not a uri"),
        ("date-time", "nope"),
    ],
)
def test_validate_fixtures_format_is_not_asserted(
    tmp_path: Path, format_name: str, bad_value: str
) -> None:
    schema = {"format": format_name}

    assert _probe(tmp_path, schema, json.dumps(bad_value)) == []


# --- Numbers: exact decimals, whole-valued decimals are integers -------------------------------


@pytest.mark.parametrize(
    ("schema", "data", "accepted"),
    [
        ({"type": "integer"}, "5.0", True),
        ({"type": "integer"}, "5.5", False),
        ({"type": "integer"}, "1e2", True),
        ({"type": "integer"}, "true", False),
        ({"type": "integer"}, '"5"', False),
        ({"type": "integer", "minimum": 1}, "5.0", True),
        ({"type": "integer", "minimum": 1}, "0.5", False),
        ({"minimum": 0.1}, "0.1", True),
        ({"maximum": 0.3}, "0.30000000000000004", False),
        ({"multipleOf": 0.1}, "0.3", True),
        ({"multipleOf": 0.01}, "19.99", True),
        ({"type": "integer"}, "123456789012345678901234567890", True),
        ({"maximum": 10}, "123456789012345678901234567890", False),
        ({"const": 1}, "1.0", True),
        ({"const": 1}, "true", False),
        ({"enum": [1]}, "1.0", True),
        ({"uniqueItems": True}, "[1, 1.0]", False),
        ({"uniqueItems": True}, "[1, 2]", True),
    ],
)
def test_validate_fixtures_numbers_are_judged_the_way_json_schema_net_judges_them(
    tmp_path: Path, schema: Json, data: str, accepted: bool
) -> None:
    problems = _probe(tmp_path, schema, data)

    assert (problems == []) is accepted, problems


# --- pattern: ASCII only, as in .NET's ECMAScript mode ----------------------------------------


@pytest.mark.parametrize(
    ("pattern", "value", "accepted"),
    [
        (r"^\d+$", "١٢", False),  # Arabic-Indic digits
        (r"^\d+$", "\uff11", False),  # full-width digit
        (r"^\d+$", "12", True),
        (r"^\S+$", "a\u00a0b", True),  # no-break space is not ASCII white space
        (r"^\S+$", "a b", False),
        (r"^a$", "a\n", True),  # $ also matches before a final newline, as in .NET
        (r"^[A-Z]+$", "İ", False),
        (r"b", "abc", True),  # not anchored: matches anywhere
    ],
)
def test_validate_fixtures_pattern_matches_the_way_json_schema_net_matches(
    tmp_path: Path, pattern: str, value: str, accepted: bool
) -> None:
    problems = _probe(tmp_path, {"pattern": pattern}, json.dumps(value))

    assert (problems == []) is accepted, problems


# --- if / then / else: errors inside the condition are not reported -----------------------------


def test_validate_fixtures_a_failed_if_condition_is_not_a_problem(tmp_path: Path) -> None:
    schema = {
        "if": {"properties": {"kind": {"const": "a"}}, "required": ["kind"]},
        "then": {"required": ["a"]},
        "else": {"required": ["b"]},
    }

    assert _probe(tmp_path / "else", schema, '{"b": 1}') == []
    assert _probe(tmp_path / "then", schema, '{"kind": "a", "a": 1}') == []
    assert any("'a'" in line for line in _probe(tmp_path / "bad", schema, '{"kind": "a"}'))
    assert not any("kind" in line for line in _probe(tmp_path / "bad2", schema, '{"c": 1}'))


# --- Reading the file --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    ["", "   ", "{nope", '{"a": 1,}', '{/* c */ "a": 1}', "NaN", '{"a": Infinity}', '{"a": 1} x'],
)
def test_validate_fixtures_text_that_is_not_json_is_reported(tmp_path: Path, text: str) -> None:
    problems = _probe(tmp_path, {}, text)

    assert len(problems) == 1
    assert problems[0].startswith("probe.json: /: Not valid JSON: ")


def test_validate_fixtures_a_byte_order_mark_is_ignored(tmp_path: Path) -> None:
    assert _probe(tmp_path, {"type": "object"}, b"\xef\xbb\xbf{}") == []


def test_validate_fixtures_bytes_that_are_not_utf8_become_replacement_characters(
    tmp_path: Path,
) -> None:
    # .NET's File.ReadAllText replaces them instead of failing, so the file is still valid JSON.
    assert _probe(tmp_path, {"type": "string"}, b'"\xff"') == []
