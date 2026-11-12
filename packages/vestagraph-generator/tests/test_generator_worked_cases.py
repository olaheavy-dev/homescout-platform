"""The generator, run on the real data, against every hand-worked case in story-calculations.json.

Inputs and expected values come from that file. The only thing written here is which home and
scenario each case describes, because the cases name them only in words.
"""

from typing import Any

import pytest
from generator_support import generated_json, home, scenario, worked_case

MONTHLY_CASES = {
    "b1-monthly-housing-cost-listing-service-charge": ("B1", "from-step-1"),
    "b1-monthly-housing-cost-management-pack-arrived": ("B1", "from-step-3"),
    "b1-monthly-housing-cost-2026-budget": ("B1", "from-step-4"),
    "b2-monthly-housing-cost": ("B2", "from-step-1"),
    "r1-monthly-housing-cost-before-water": ("R1", "from-step-1"),
    "r1-monthly-housing-cost-after-water": ("R1", "from-step-4"),
    "r2-monthly-housing-cost": ("R2", "from-step-1"),
}

UPFRONT_CASES = ["b1-upfront-cash", "b2-upfront-cash", "r1-upfront-cash", "r2-upfront-cash"]


def _assert_lines(
    actual: list[dict[str, Any]], expected: list[dict[str, Any]], pence_key: str
) -> None:
    """Lines are compared by category: the case file's order is not the engine's fixed order."""
    assert sorted(line["category"] for line in actual) == sorted(
        line["category"] for line in expected
    )
    for wanted in expected:
        category = wanted["category"]
        line = next(line for line in actual if line["category"] == category)
        if pence_key in wanted:
            assert line["status"] == "calculated", category
            assert line["pence"] == wanted[pence_key], category
        else:
            assert line["status"] == wanted["status"], category
            assert "pence" not in line, category


def _assert_reason_categories(actual: list[dict[str, Any]], expected: list[str]) -> None:
    """The cases give reasons as prose that starts with the category, so compare by category."""
    assert sorted(r["category"] for r in actual) == sorted(r.split(":")[0] for r in expected)


@pytest.mark.parametrize("case_id", list(MONTHLY_CASES))
def test_generate_monthly_story_case_matches_worked_result(case_id: str) -> None:
    expected = worked_case(case_id)["expected"]
    home_id, scenario_id = MONTHLY_CASES[case_id]
    monthly = scenario(home_id, scenario_id)["monthly"]

    _assert_lines(monthly["lines"], expected["lines"], "monthlyPence")
    assert monthly["total"]["pence"] == expected["totalMonthlyPence"]
    assert monthly["total"]["isPartial"] == expected["totalIsPartial"]
    _assert_reason_categories(monthly["total"]["partialReasons"], expected["partialReasons"])
    assert monthly["budget"]["budgetPence"] == expected["budgetPence"]
    assert monthly["budget"]["differencePence"] == expected["budgetDifferencePence"]
    assert monthly["budget"]["withinBudget"] == expected["withinBudget"]
    assert monthly["budget"]["basedOnPartialTotal"] == expected["totalIsPartial"]


@pytest.mark.parametrize("case_id", UPFRONT_CASES)
def test_generate_upfront_story_case_matches_worked_result_in_every_scenario(case_id: str) -> None:
    story_case = worked_case(case_id)
    expected = story_case["expected"]

    scenarios = home(story_case["inputs"]["home"])["scenarios"]

    assert scenarios
    for found in scenarios:
        upfront = found["upfront"]
        _assert_lines(upfront["lines"], expected["lines"], "amountPence")
        assert upfront["total"]["pence"] == expected["totalUpfrontPence"]
        assert upfront["total"]["isPartial"] == expected["totalIsPartial"]
        _assert_reason_categories(upfront["total"]["partialReasons"], expected["partialReasons"])


def test_generate_mortgage_story_cases_match_the_worked_repayments() -> None:
    for home_id, case_id in (("B1", "b1-mortgage-repayment"), ("B2", "b2-mortgage-repayment")):
        case = worked_case(case_id)
        expected, inputs = case["expected"], case["inputs"]

        mortgage = scenario(home_id, "from-step-1")["mortgage"]

        assert mortgage["monthlyRepayment"]["pence"] == expected["monthlyRepaymentPence"]
        assert mortgage["loan"]["pence"] == inputs["askingPricePence"] - inputs["depositPence"]
        assert mortgage["termYears"] == inputs["termYears"]


def test_generate_budget_beat_case_lands_as_worked() -> None:
    expected = worked_case("b1-budget-beat")["expected"]
    listing = scenario("B1", "from-step-1")["monthly"]
    budget = scenario("B1", "from-step-4")["monthly"]

    assert listing["total"]["pence"] == expected["listingTotalPence"]
    assert budget["total"]["pence"] == expected["budgetTotalPence"]
    assert listing["budget"]["withinBudget"] == expected["withinBudgetOnListing"]
    assert budget["budget"]["withinBudget"] == (not expected["overBudgetOn2026Budget"])
    assert listing["budget"]["differencePence"] == expected["listingBudgetDifferencePence"]
    assert budget["budget"]["differencePence"] == expected["budgetBudgetDifferencePence"]


def test_generate_service_charge_difference_case_matches_worked_result() -> None:
    expected = worked_case("b1-service-charge-difference")["expected"]

    changes = [
        c
        for c in scenario("B1", "from-step-4")["changesFromPrevious"]
        if c["category"] == "service-charge"
    ]

    assert len(changes) == 1
    change = changes[0]
    assert change["id"] == "B1.from-step-4.change.service-charge"
    assert change["kind"] == "value-changed"
    assert change["annualDifferencePence"] == expected["annualDifferencePence"]
    assert change["monthlyDifferencePence"] == expected["monthlyDifferencePence"]
    assert change["previousEvidenceIds"] == ["B1-SC-LISTING"]
    assert change["currentEvidenceIds"] == ["B1-SC-BUDGET"]


def _line(home_id: str, scenario_id: str, category: str) -> dict[str, Any]:
    matches = [
        line
        for line in scenario(home_id, scenario_id)["monthly"]["lines"]
        if line["category"] == category
    ]
    assert len(matches) == 1
    found: dict[str, Any] = matches[0]
    return found


def test_generate_water_at_step_one_is_conflicting_with_both_statements_as_evidence() -> None:
    water = _line("R1", "from-step-1", "water")

    assert water["status"] == "conflicting"
    assert "pence" not in water
    assert water["evidenceIds"] == ["R1-WATER-LISTING", "R1-WATER-WSOT"]


def test_generate_insurance_at_step_three_is_evidence_changed_with_no_total_change() -> None:
    # Worked reasoning: insurance has no amount before step 3 (missing) or from it (included in the
    # service charge), so no figure moves and there is no difference to report; the totals differ in
    # which lines are left out, so no monthly-total change is given (rule 7). At step 4 only the
    # service charge changes, by 31,000 - 20,000 = 11,000p a month (worked case
    # b1-service-charge-difference).
    step_three = scenario("B1", "from-step-3")
    assert len(step_three["changesFromPrevious"]) == 1
    change = step_three["changesFromPrevious"][0]

    assert change["id"] == "B1.from-step-3.change.buildings-insurance"
    assert change["kind"] == "evidence-changed"
    assert change["previousEvidenceIds"] == []
    assert change["currentEvidenceIds"] == ["B1-INSURANCE"]
    assert "annualDifferencePence" not in change
    assert "monthlyDifferencePence" not in change
    assert "monthlyTotalChange" not in step_three

    step_four = scenario("B1", "from-step-4")
    worked = worked_case("b1-service-charge-difference")["expected"]["monthlyDifferencePence"]
    assert len(step_four["changesFromPrevious"]) == 1
    assert step_four["changesFromPrevious"][0]["category"] == "service-charge"
    assert step_four["monthlyTotalChange"]["pence"] == worked


def test_generate_water_at_step_four_is_now_calculated() -> None:
    changes = [
        c for c in scenario("R1", "from-step-4")["changesFromPrevious"] if c["category"] == "water"
    ]

    assert len(changes) == 1
    assert changes[0]["kind"] == "now-calculated"
    assert changes[0]["id"] == "R1.from-step-4.change.water"


def test_generate_rented_home_whose_bills_are_included_shows_them_as_included_not_zero() -> None:
    for category in ("energy", "water", "broadband"):
        line = _line("R2", "from-step-1", category)

        assert line["status"] == "included", category
        assert "pence" not in line, category


def test_generate_energy_certificate_costs_never_enter_any_line_or_total() -> None:
    assert "EPC-COST" not in generated_json()
