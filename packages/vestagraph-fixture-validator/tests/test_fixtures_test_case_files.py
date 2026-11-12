"""The independently worked test cases against their schema and each other.

Ported from TestCaseFileTests.
"""

import pytest
from fixtures_support import Json, lines, load_test_case_file, mentions, number, schema_directory
from vestagraph_fixture_validator.validator import FixtureProblem, validate_instance

_FILES = ["rounding-boundaries", "story-calculations"]


def _validate(file: Json) -> list[FixtureProblem]:
    return validate_instance(file, "test-case.schema.json", schema_directory())


def _all_cases() -> list[Json]:
    cases: list[Json] = []
    for name in _FILES:
        cases.extend(load_test_case_file(name)["cases"])
    return cases


def _case(file: Json, case_id: str) -> Json:
    return next(c for c in file["cases"] if c["id"] == case_id)


@pytest.mark.parametrize("name", _FILES)
def test_validate_instance_test_case_real_file_names_its_schema_and_is_accepted(name: str) -> None:
    file = load_test_case_file(name)

    assert file["$schema"] == "../schema/test-case.schema.json"
    assert _validate(file) == []


def test_validate_instance_test_case_money_field_with_decimals_is_rejected() -> None:
    file = load_test_case_file("story-calculations")
    file["cases"][0]["expected"]["annualDifferencePence"] = number("1320.5")

    assert mentions(_validate(file), "annualDifferencePence")


def test_validate_instance_test_case_case_with_no_rule_is_rejected() -> None:
    file = load_test_case_file("rounding-boundaries")
    del file["cases"][0]["rule"]

    assert mentions(_validate(file), "rule")


def test_validate_instance_test_case_cost_line_as_zero_amount_is_rejected() -> None:
    file = load_test_case_file("story-calculations")
    _case(file, "b1-upfront-cash")["inputs"]["lines"][0]["amountPence"] = 0

    assert mentions(_validate(file), "amountPence")


def test_validate_instance_test_case_partial_total_with_no_reason_is_rejected() -> None:
    file = load_test_case_file("story-calculations")
    _case(file, "b1-upfront-cash")["expected"]["partialReasons"] = []

    assert mentions(_validate(file), "partialReasons")


def _insurance_line(file: Json) -> Json:
    case = _case(file, "b1-monthly-housing-cost-management-pack-arrived")
    return next(
        line for line in case["expected"]["lines"] if line["category"] == "buildings-insurance"
    )


def test_validate_instance_test_case_line_status_missing_is_accepted() -> None:
    # The step 3 case has insurance as "included"; changing it to "missing" must still validate.
    # "missing" matches the generated-costs schema: a line with no evidence yet (BE-16), never
    # shown as zero.
    file = load_test_case_file("story-calculations")
    _insurance_line(file)["status"] = "missing"

    assert _validate(file) == []


def test_validate_instance_test_case_unknown_line_status_is_rejected() -> None:
    file = load_test_case_file("story-calculations")
    _insurance_line(file)["status"] = "unknown"

    assert lines(_validate(file)) != []


def test_test_cases_ids_are_unique() -> None:
    ids = [c["id"] for c in _all_cases()]

    assert len(ids) == len(set(ids))


def test_test_cases_cross_case_links_point_at_cases_that_exist() -> None:
    ids = {c["id"] for c in _all_cases()}
    broken: list[str] = []

    for case in _all_cases():
        inputs = case["inputs"]
        broken.extend(
            f"{case['id']} {key}"
            for key in ("listingTotalCase", "budgetTotalCase")
            if key in inputs and inputs[key] not in ids
        )
        broken.extend(
            f"{case['id']} mortgageCase {line['mortgageCase']}"
            for line in inputs.get("lines", [])
            if "mortgageCase" in line and line["mortgageCase"] not in ids
        )

    assert broken == [], "; ".join(broken)
