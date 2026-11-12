"""What the generated file looks like: homes, scenarios, key order, figure ids, same every time."""

import json
import re
from pathlib import Path
from typing import Any

import pytest
from generator_support import (
    copy_data_to,
    fixtures_directory,
    generated_json,
    home,
    output,
    read_json,
    scenario,
    write_json,
)
from vestagraph_generator.costs_generator import generate

FIGURE_ID = re.compile(r"^[A-Z0-9]+(-[A-Z0-9]+)*(\.[a-z0-9]+(-[a-z0-9]+)*)+$")


def _snapshot() -> dict[str, Any]:
    snapshot: dict[str, Any] = read_json(fixtures_directory() / "data" / "snapshot.json")[
        "snapshot"
    ]
    return snapshot


def test_generate_real_data_lists_the_homes_in_the_order_of_the_snapshot() -> None:
    assert [h["homeId"] for h in output()["homes"]] == _snapshot()["homeIds"]


@pytest.mark.parametrize(
    ("home_id", "scenario_ids"),
    [
        ("B1", ["from-step-1", "from-step-3", "from-step-4"]),
        ("B2", ["from-step-1"]),
        ("R1", ["from-step-1", "from-step-4"]),
        ("R2", ["from-step-1"]),
        ("WALES-1", []),
    ],
)
def test_generate_real_data_derives_the_expected_scenarios(
    home_id: str, scenario_ids: list[str]
) -> None:
    assert [s["scenarioId"] for s in home(home_id)["scenarios"]] == scenario_ids


def test_generate_buyer_story_merges_steps_one_to_two_then_splits_at_steps_three_and_four() -> None:
    # B1-INSURANCE is used from step 3 (issue #37): steps 1 and 2 merge, 3 and 4 stand alone.
    expected = {"from-step-1": (1, 2), "from-step-3": (3, 3), "from-step-4": (4, 4)}

    for scenario_id, steps in expected.items():
        found = scenario("B1", scenario_id)
        assert (found["fromStep"], found["toStep"]) == steps, scenario_id


def test_generate_wales_home_is_not_yet_covered_with_no_scenarios_and_no_mode() -> None:
    wales = home("WALES-1")

    assert wales["coverage"] == "not-yet-covered"
    assert wales["nation"] == "Wales"
    assert wales["scenarios"] == []
    assert "mode" not in wales
    assert "storyId" not in wales


def test_generate_english_homes_carry_mode_nation_coverage_and_story() -> None:
    r1 = home("R1")

    assert (r1["mode"], r1["nation"], r1["coverage"], r1["storyId"]) == (
        "rent",
        "England",
        "covered",
        "RENTER",
    )


def test_generate_header_copies_the_snapshot_date_and_names_the_contract() -> None:
    document = output()

    assert document["snapshotDate"] == _snapshot()["snapshotDate"]
    assert document["$schema"] == "../schema/generated-costs.schema.json"
    assert document["formatVersion"] == 1
    assert document["money"] == "integer pence"
    assert document["rounding"].endswith("(decisions 0034 and 0036).")
    assert document["generatedBy"] == "Vestagraph cost engine"


def _collect_ids(node: object, ids: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "id" and isinstance(value, str):
                ids.append(value)
            else:
                _collect_ids(value, ids)
    elif isinstance(node, list):
        for item in node:
            _collect_ids(item, ids)


def test_generate_every_figure_id_is_unique_and_matches_the_pattern() -> None:
    ids: list[str] = []
    _collect_ids(output(), ids)

    assert ids
    assert len(ids) == len(set(ids))
    assert [i for i in ids if not FIGURE_ID.match(i)] == []


def test_generate_every_partial_reason_points_at_a_line_in_the_same_scenario() -> None:
    checked = 0
    for found_home in output()["homes"]:
        for found_scenario in found_home["scenarios"]:
            for section in ("monthly", "upfront"):
                block = found_scenario[section]
                line_ids = {line["id"] for line in block["lines"]}
                reason_ids = {r["lineId"] for r in block["total"]["partialReasons"]}
                assert reason_ids <= line_ids
                checked += len(reason_ids)
    assert checked > 0


def _check_key_order(
    node: object,
    schema_properties: dict[str, Any],
    definitions: dict[str, Any],
    path: str,
    problems: list[str],
) -> None:
    if isinstance(node, list):
        for item in node:
            _check_key_order(item, schema_properties, definitions, path + "[]", problems)
        return
    if not isinstance(node, dict):
        return
    schema_order = list(schema_properties)
    positions = [schema_order.index(key) if key in schema_order else -1 for key in node]
    if -1 in positions or positions != sorted(positions):
        problems.append(f"{path}: keys {list(node)} do not follow {schema_order}")
    for key, value in node.items():
        prop = schema_properties.get(key) or {}
        reference = prop.get("$ref") or (prop.get("items") or {}).get("$ref")
        if isinstance(reference, str) and reference.startswith("#/$defs/"):
            child = definitions.get(reference.removeprefix("#/$defs/")) or {}
            if "properties" in child:
                _check_key_order(value, child["properties"], definitions, f"{path}.{key}", problems)


def test_generate_every_key_follows_the_order_of_the_contract_schema() -> None:
    schema = read_json(fixtures_directory() / "schema" / "generated-costs.schema.json")
    problems: list[str] = []

    _check_key_order(output(), schema["properties"], schema["$defs"], "root", problems)

    assert problems == []


def test_generate_key_order_check_notices_keys_out_of_order() -> None:
    problems: list[str] = []

    _check_key_order({"b": 1, "a": 2}, {"a": {}, "b": {}}, {}, "root", problems)
    _check_key_order({"a": 1, "z": 2}, {"a": {}, "b": {}}, {}, "root", problems)

    assert len(problems) == 2


def test_generate_run_twice_gives_identical_text() -> None:
    again = generate(fixtures_directory())

    assert again.value == generated_json()


def test_generate_text_uses_lf_line_endings_two_space_indent_and_one_final_newline() -> None:
    text = generated_json()

    assert "\r" not in text
    assert "\t" not in text
    assert text.endswith("}\n")
    assert not text.endswith("\n\n")
    indents = [len(line) - len(line.lstrip(" ")) for line in text.split("\n") if line]
    assert all(n % 2 == 0 for n in indents)
    assert max(indents) >= 2
    assert text.startswith('{\n  "$schema"')


def _refuse_float(text: str) -> float:
    message = f"A decimal number {text} is in the generated file."
    raise AssertionError(message)


def test_generate_no_money_anywhere_is_a_floating_point_number() -> None:
    text = generated_json()

    json.loads(text, parse_float=_refuse_float)
    assert re.search(r"\d\.\d", text) is None


def test_generate_text_with_accents_is_written_as_utf8_not_escaped(tmp_path: Path) -> None:
    fixtures = copy_data_to(tmp_path)
    path = fixtures / "data" / "snapshot.json"
    document = read_json(path)
    document["snapshot"]["snapshotDate"] = "2026-10-23 café"
    write_json(path, document)

    result = generate(fixtures)

    assert result.is_success
    assert '"snapshotDate": "2026-10-23 café"' in result.value
