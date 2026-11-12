"""The schemas must refuse bad data, not only accept good data (ported from SchemaRejectionTests).

Each test starts from a real record, breaks one thing, and expects the schema to complain.
"""

import pytest
from fixtures_support import (
    Json,
    evidence_item,
    home,
    mentions,
    number,
    question,
    validate_record,
)
from vestagraph_fixture_validator.validator import FixtureProblem


def _evidence(item: Json) -> list[FixtureProblem]:
    return validate_record("evidence", "evidence", item)


def _home(item: Json) -> list[FixtureProblem]:
    return validate_record("homes", "homes", item)


def test_validate_instance_evidence_unchanged_real_record_is_accepted() -> None:
    assert _evidence(evidence_item("B1-SC-LISTING")) == []


def test_validate_instance_evidence_value_with_no_source_is_rejected() -> None:
    item = evidence_item("B1-SC-LISTING")
    del item["source"]

    assert mentions(_evidence(item), "source")


def test_validate_instance_evidence_source_with_no_origin_is_rejected() -> None:
    item = evidence_item("B1-SC-LISTING")
    del item["source"]["origin"]

    assert mentions(_evidence(item), "origin")


def test_validate_instance_evidence_money_with_decimals_is_rejected() -> None:
    item = evidence_item("B1-SC-LISTING")
    item["value"]["pence"] = number("240000.5")

    assert mentions(_evidence(item), "/value/pence")


def test_validate_instance_evidence_money_as_a_pounds_string_is_rejected() -> None:
    item = evidence_item("B1-SC-LISTING")
    item["value"]["pence"] = "2400.00"

    assert mentions(_evidence(item), "/value/pence")


def test_validate_instance_evidence_rate_as_a_decimal_is_rejected() -> None:
    item = evidence_item("HH-MORTGAGE-RATE")
    item["value"]["basisPoints"] = number("550.5")

    assert mentions(_evidence(item), "/value/basisPoints")


def test_validate_instance_evidence_bill_recorded_as_zero_instead_of_included_is_rejected() -> None:
    # R2's water is covered by the rent. Recording it as 0 pence a month is the mistake rule 7
    # forbids.
    item = evidence_item("R2-WATER")
    item["status"] = "available"
    item["value"] = {"kind": "money", "pence": 0, "period": "month"}

    assert mentions(_evidence(item), "/value/pence")


def test_validate_instance_evidence_included_bill_that_also_has_a_value_is_rejected() -> None:
    item = evidence_item("R2-WATER")
    item["value"] = {"kind": "money", "pence": 4500, "period": "month"}

    assert mentions(_evidence(item), "/value")


def test_validate_instance_evidence_not_calculated_item_recorded_as_zero_is_rejected() -> None:
    # Stamp duty is not calculated in this version. Recording 0 pence would look like
    # "no stamp duty".
    item = evidence_item("B1-STAMP-DUTY")
    item["status"] = "available"
    item["value"] = {"kind": "money", "pence": 0, "period": "once"}

    assert mentions(_evidence(item), "/value/pence")


def test_validate_instance_evidence_not_calculated_item_that_also_has_a_value_is_rejected() -> None:
    item = evidence_item("B1-LEGAL-FEES")
    item["value"] = {"kind": "money", "pence": 150000, "period": "once"}

    assert mentions(_evidence(item), "/value")


def test_validate_instance_evidence_available_item_with_no_value_is_rejected() -> None:
    item = evidence_item("B1-PRICE")
    del item["value"]

    assert mentions(_evidence(item), "value")


def test_validate_instance_evidence_certificate_cost_not_marked_context_only_is_rejected() -> None:
    item = evidence_item("B1-EPC-COST")
    item["contextOnly"] = False

    assert mentions(_evidence(item), "/contextOnly")


def test_validate_instance_evidence_unknown_status_is_rejected() -> None:
    item = evidence_item("B1-PRICE")
    item["status"] = "verified"

    assert mentions(_evidence(item), "/status")


def test_validate_instance_evidence_source_with_no_synthetic_flag_is_rejected() -> None:
    item = evidence_item("B1-CT-CHARGE")
    del item["source"]["synthetic"]

    assert mentions(_evidence(item), "synthetic")


def test_validate_instance_evidence_cited_text_without_citation_url_is_rejected() -> None:
    item = evidence_item("R2-EPC")
    del item["source"]["citationUrl"]

    assert mentions(_evidence(item), "citationUrl")


def test_validate_instance_home_address_with_no_nation_is_rejected() -> None:
    item = home("B2")
    del item["address"]["nation"]

    assert mentions(_home(item), "nation")


def test_validate_instance_home_wales_marked_as_covered_is_rejected() -> None:
    item = home("WALES-1")
    item["coverage"] = "covered"

    assert mentions(_home(item), "/coverage")


def test_validate_instance_home_england_marked_as_not_covered_is_rejected() -> None:
    item = home("B2")
    item["coverage"] = "not-yet-covered"

    assert mentions(_home(item), "/coverage")


def test_validate_instance_home_candidate_units_with_no_selected_unit_is_rejected() -> None:
    item = home("B1")
    del item["unit"]["selectedUnitId"]

    assert mentions(_home(item), "selectedUnitId")


@pytest.mark.parametrize(
    "status",
    [
        "to-ask",
        "waiting-for-reply",
        "reply-needs-checking",
        "answer-recorded",
        "partially-answered",
        "needs-professional-review",
        "closed-by-user-without-answer",
        "reopened",
    ],
)
def test_validate_instance_question_each_status_from_doc02_is_accepted(status: str) -> None:
    item = question("B1-Q-MAJOR-WORKS")
    item["status"] = status

    assert validate_record("questions", "questions", item) == []


def test_validate_instance_question_resolved_status_that_is_not_in_doc02_is_rejected() -> None:
    item = question("B1-Q-MAJOR-WORKS")
    item["status"] = "resolved"

    assert mentions(validate_record("questions", "questions", item), "/status")


def test_validate_instance_question_transition_with_no_reason_is_rejected() -> None:
    item = question("B1-Q-MAJOR-WORKS")
    del item["statusHistory"][0]["reason"]

    assert mentions(validate_record("questions", "questions", item), "reason")


def test_validate_instance_evidence_mortgage_term_over_100_years_is_rejected() -> None:
    # 100 years is the engine's computation limit (register line BE-17), not a lending rule.
    item = evidence_item("HH-MORTGAGE-TERM")
    item["value"]["amount"] = 101

    assert mentions(_evidence(item), "/value/amount")


def test_validate_instance_evidence_mortgage_term_of_100_years_is_accepted() -> None:
    item = evidence_item("HH-MORTGAGE-TERM")
    item["value"]["amount"] = 100

    assert _evidence(item) == []


def test_validate_instance_evidence_misspelt_category_is_rejected() -> None:
    item = evidence_item("B1-PRICE")
    item["category"] = "askin-price"

    assert mentions(_evidence(item), "/category")


def test_validate_instance_evidence_synthetic_origin_with_synthetic_flag_false_is_rejected() -> (
    None
):
    item = evidence_item("B1-CT-CHARGE")
    item["source"]["synthetic"] = False

    assert mentions(_evidence(item), "synthetic")


@pytest.mark.parametrize("field", ["tenure", "mode", "propertyType", "bedrooms", "unit"])
def test_validate_instance_home_english_home_missing_a_descriptive_field_is_rejected(
    field: str,
) -> None:
    item = home("B2")
    del item[field]

    assert mentions(_home(item), field)


def test_validate_instance_home_selected_unit_outside_the_candidates_is_not_caught_by_schema() -> (
    None
):
    # JSON Schema cannot say "selectedUnitId is one of candidateUnits", so the real-data test
    # test_b1_postcode_matches_six_candidate_units_and_the_selected_one_is_among_them covers it.
    # This test documents the gap.
    item = home("B1")
    item["unit"]["selectedUnitId"] = "B1-UNIT-9"

    assert _home(item) == []
