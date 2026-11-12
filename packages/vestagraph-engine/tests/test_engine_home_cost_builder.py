"""The home cost builder: scenarios derived from the evidence, and what changes between them
(ported from the C# HomeCostBuilderTests).

The service-charge change and the end-to-end homes are checked against the independently worked
cases in test-cases/story-calculations.json; the other tests use arbitrary inputs with the working
shown in a comment.
"""

from typing import Any

import pytest
from engine_support import (
    anchors_except,
    basis_points,
    budget_of,
    buy_anchors,
    buying,
    buying_from,
    case,
    case_ids_where,
    category_from_id,
    mode_of,
    money,
    no_value,
    other,
    rate,
    renting,
    years,
)
from vestagraph_engine import ErrorCategory, Pence
from vestagraph_engine.breakdowns import LineResult
from vestagraph_engine.cost_categories import category_id, status_id
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode, Period
from vestagraph_engine.evidence import (
    EvidenceItem,
    EvidenceStatus,
    HomeFacts,
    Nation,
    RateValue,
)
from vestagraph_engine.home_cost_builder import build_home_costs
from vestagraph_engine.home_costs import ChangeKind, CostChange, HomeCosts

DIFFERENCE_CASE_ID = "b1-service-charge-difference"
FOUR_STEPS = (1, 2, 3, 4)

# The cases this file runs against the file: the service-charge difference, and every monthly and
# upfront case again, end to end through the builder.
CASE_IDS = [DIFFERENCE_CASE_ID]
MONTHLY_CASE_IDS = [
    c_id for c_id in case_ids_where("lines") if c_id in case_ids_where("budgetPence")
]


BUY_BILLS = (
    "service-charge",
    "ground-rent",
    "council-tax",
    "energy",
    "water",
    "broadband",
    "buildings-insurance",
    "maintenance",
)
RENT_BILLS = ("council-tax", "energy", "water", "broadband")
# Bills a worked monthly case leaves out because the home does not have them.
NOT_APPLICABLE_BILLS: dict[str, tuple[str, ...]] = {
    "b2-monthly-housing-cost": ("service-charge", "ground-rent"),
}


def _build(facts: HomeFacts, steps: tuple[int, ...] | list[int]) -> HomeCosts:
    result = build_home_costs(facts, steps)
    assert result.is_success, result.error.code if result.is_failure else ""
    return result.value


def _failure_code(facts: HomeFacts, steps: tuple[int, ...] | list[int]) -> str:
    result = build_home_costs(facts, steps)
    assert result.is_failure
    return result.error.code


def _buyer_with_service_charge_change(old_yearly: int, new_yearly: int) -> HomeFacts:
    return buying(
        [
            money(
                "SC-OLD",
                "service-charge",
                old_yearly,
                Period.YEAR,
                EvidenceStatus.CONFLICTING,
                used_from_step=1,
            ),
            money(
                "SC-NEW",
                "service-charge",
                new_yearly,
                Period.YEAR,
                used_from_step=4,
                supersedes="SC-OLD",
            ),
        ]
    )


def _only_change(home: HomeCosts, scenario: int = 1) -> CostChange:
    (change,) = home.scenarios[scenario].changes
    return change


def _change_for(home: HomeCosts, category: CostCategory, scenario: int = 1) -> CostChange:
    (change,) = [c for c in home.scenarios[scenario].changes if c.category == category]
    return change


def _line(lines: tuple[LineResult, ...], category: CostCategory) -> LineResult:
    (line,) = [candidate for candidate in lines if candidate.category == category]
    return line


def test_service_charge_change_story_case_matches_worked_result() -> None:
    inputs = case(DIFFERENCE_CASE_ID)["inputs"]
    expected = case(DIFFERENCE_CASE_ID)["expected"]
    listing = inputs["listingServiceChargeAnnualPence"]
    budget = inputs["budgetServiceChargeAnnualPence"]

    home = _build(_buyer_with_service_charge_change(listing, budget), FOUR_STEPS)

    change = _change_for(home, CostCategory.SERVICE_CHARGE)
    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.annual_difference == Pence(expected["annualDifferencePence"])
    assert change.monthly_difference == Pence(expected["monthlyDifferencePence"])
    # The monthly total moves by the same amount, as nothing else changed.
    assert home.scenarios[1].monthly_total_change == Pence(expected["monthlyDifferencePence"])


def test_service_charge_change_that_falls_gives_the_negative_of_the_worked_result() -> None:
    # The worked case reversed: the 2026 budget first, then the listing claim.
    inputs = case(DIFFERENCE_CASE_ID)["inputs"]
    expected = case(DIFFERENCE_CASE_ID)["expected"]
    listing = inputs["listingServiceChargeAnnualPence"]
    budget = inputs["budgetServiceChargeAnnualPence"]

    home = _build(_buyer_with_service_charge_change(budget, listing), FOUR_STEPS)

    change = _change_for(home, CostCategory.SERVICE_CHARGE)
    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.annual_difference == Pence(-expected["annualDifferencePence"])
    assert change.monthly_difference == Pence(-expected["monthlyDifferencePence"])


def test_build_home_costs_evidence_changes_at_step_four_gives_two_scenarios_named_from_step() -> (
    None
):
    home = _build(_buyer_with_service_charge_change(240_000, 372_000), FOUR_STEPS)

    assert [s.scenario_id for s in home.scenarios] == ["from-step-1", "from-step-4"]
    assert [(s.from_step, s.to_step) for s in home.scenarios] == [(1, 3), (4, 4)]


def test_build_home_costs_same_evidence_at_every_step_gives_one_scenario_covering_all_steps() -> (
    None
):
    facts = buying([money("EN", "energy", 9_000, Period.MONTH)])

    home = _build(facts, FOUR_STEPS)

    (only,) = home.scenarios
    assert only.scenario_id == "from-step-1"
    assert (only.from_step, only.to_step) == (1, 4)
    assert only.changes == ()
    assert only.monthly_total_change is None


def test_build_home_costs_first_scenario_has_no_changes() -> None:
    home = _build(_buyer_with_service_charge_change(240_000, 372_000), FOUR_STEPS)

    assert home.scenarios[0].changes == ()
    assert home.scenarios[0].monthly_total_change is None


def test_build_home_costs_monthly_difference_is_the_difference_of_the_rounded_monthly_lines() -> (
    None
):
    # 100,000p a year is 8,333.33p a month, which rounds to 8,333p. 200,000p a year is
    # 16,666.67p, which rounds to 16,667p. The monthly difference is 16,667 - 8,333 = 8,334p (not
    # 100,000 / 12 = 8,333p). The annual difference is 100,000p.
    home = _build(_buyer_with_service_charge_change(100_000, 200_000), FOUR_STEPS)

    change = _change_for(home, CostCategory.SERVICE_CHARGE)
    assert change.monthly_difference == Pence(8_334)
    assert change.annual_difference == Pence(100_000)
    assert home.scenarios[1].monthly_total_change == Pence(8_334)


def test_build_home_costs_change_evidence_names_the_previous_and_current_items() -> None:
    home = _build(_buyer_with_service_charge_change(240_000, 372_000), FOUR_STEPS)

    change = _only_change(home)
    assert change.category == CostCategory.SERVICE_CHARGE
    assert change.previous_evidence_ids == ("SC-OLD",)
    assert change.current_evidence_ids == ("SC-NEW",)


def test_build_home_costs_three_scenarios_compare_each_with_the_one_before() -> None:
    # A is replaced by B from step 2 and B by C from step 3. A = 100,000p a year (8,333p a month),
    # B = 200,000p (16,667p), C = 300,000p (25,000p exactly).
    facts = buying(
        [
            money("SC-A", "service-charge", 100_000, Period.YEAR),
            money(
                "SC-B", "service-charge", 200_000, Period.YEAR, used_from_step=2, supersedes="SC-A"
            ),
            money(
                "SC-C", "service-charge", 300_000, Period.YEAR, used_from_step=3, supersedes="SC-B"
            ),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    assert [s.scenario_id for s in home.scenarios] == ["from-step-1", "from-step-2", "from-step-3"]
    assert [(s.from_step, s.to_step) for s in home.scenarios] == [(1, 1), (2, 2), (3, 4)]
    second = _only_change(home, 1)
    assert (second.previous_evidence_ids, second.current_evidence_ids) == (("SC-A",), ("SC-B",))
    assert second.monthly_difference == Pence(8_334)
    assert second.annual_difference == Pence(100_000)
    third = _only_change(home, 2)
    assert (third.previous_evidence_ids, third.current_evidence_ids) == (("SC-B",), ("SC-C",))
    assert third.monthly_difference == Pence(8_333)
    assert third.annual_difference == Pence(100_000)
    assert home.scenarios[2].monthly_total_change == Pence(8_333)


def test_build_home_costs_changes_come_in_the_monthly_order_then_the_upfront_order() -> None:
    facts = buying(
        [
            money("MT-1", "maintenance", 1_000, Period.MONTH),
            money("MT-2", "maintenance", 2_000, Period.MONTH, used_from_step=4, supersedes="MT-1"),
            money("MC-1", "moving-costs", 100_000, Period.ONCE),
            money(
                "MC-2", "moving-costs", 150_000, Period.ONCE, used_from_step=4, supersedes="MC-1"
            ),
            money("SC-1", "service-charge", 100_000, Period.YEAR),
            money(
                "SC-2", "service-charge", 200_000, Period.YEAR, used_from_step=4, supersedes="SC-1"
            ),
            money("EN-1", "energy", 9_000, Period.MONTH),
            money("EN-2", "energy", 9_500, Period.MONTH, used_from_step=4, supersedes="EN-1"),
            EvidenceItem(
                "RATE-NEW",
                "mortgage-rate",
                EvidenceStatus.AVAILABLE,
                RateValue(600),
                False,
                4,
                "RATE",
            ),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    assert [c.category for c in home.scenarios[1].changes] == [
        CostCategory.MORTGAGE_REPAYMENT,
        CostCategory.SERVICE_CHARGE,
        CostCategory.ENERGY,
        CostCategory.MAINTENANCE,
        CostCategory.MOVING_COSTS,
    ]


def test_build_home_costs_conflicting_water_then_an_estimate_is_reported_as_now_calculated() -> (
    None
):
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            other("W-LISTING", "water-responsibility", EvidenceStatus.CONFLICTING),
            money("W-EST", "water", 4_500, Period.MONTH, used_from_step=4),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    change = _change_for(home, CostCategory.WATER)
    assert change.kind == ChangeKind.NOW_CALCULATED
    assert change.monthly_difference is None
    assert change.annual_difference is None
    assert change.previous_evidence_ids == ("W-LISTING",)
    assert change.current_evidence_ids == ("W-EST",)
    assert home.scenarios[0].monthly.is_partial
    assert (
        _line(home.scenarios[1].monthly.lines, CostCategory.WATER).status == LineStatus.CALCULATED
    )


def test_build_home_costs_amount_then_included_is_reported_as_no_longer_calculated() -> None:
    facts = buying(
        [
            money("INS-OLD", "buildings-insurance", 3_000, Period.MONTH, used_from_step=1),
            no_value(
                "INS-NEW",
                "buildings-insurance",
                EvidenceStatus.INCLUDED,
                used_from_step=4,
                supersedes="INS-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.category == CostCategory.BUILDINGS_INSURANCE
    assert change.kind == ChangeKind.NO_LONGER_CALCULATED
    assert change.monthly_difference is None
    assert change.previous_evidence_ids == ("INS-OLD",)
    assert change.current_evidence_ids == ("INS-NEW",)


def test_build_home_costs_status_change_between_two_lines_with_no_amount_is_evidence_changed() -> (
    None
):
    facts = buying(
        [
            no_value("M-OLD", "maintenance", EvidenceStatus.NOT_CALCULATED),
            no_value(
                "M-NEW",
                "maintenance",
                EvidenceStatus.INCLUDED,
                used_from_step=4,
                supersedes="M-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.kind == ChangeKind.EVIDENCE_CHANGED
    assert change.monthly_difference is None
    assert change.annual_difference is None


def test_build_home_costs_new_evidence_with_the_same_amount_is_evidence_changed_not_value() -> None:
    # 240,000p a year both times: no figure moves, only the source does.
    home = _build(_buyer_with_service_charge_change(240_000, 240_000), FOUR_STEPS)

    change = _only_change(home)
    assert change.kind == ChangeKind.EVIDENCE_CHANGED
    assert change.monthly_difference is None
    assert change.annual_difference is None
    # No figure moved, so the monthly total moved by nothing (not "unknown").
    assert home.scenarios[1].monthly_total_change == Pence.ZERO


def test_build_home_costs_yearly_rise_hidden_by_monthly_rounding_still_reports_annual() -> None:
    # 240,000p a year is exactly 20,000p a month; 240,001p a year is 20,000.08p, which also rounds
    # to 20,000p. The source amount rose by 1p, so this is a value change: monthly difference 0p,
    # annual difference 1p.
    home = _build(_buyer_with_service_charge_change(240_000, 240_001), FOUR_STEPS)

    change = _only_change(home)
    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.monthly_difference == Pence.ZERO
    assert change.annual_difference == Pence(1)


def test_build_home_costs_same_amount_changing_period_is_reported_as_value_changed() -> None:
    # 12,000p a month and 144,000p a year are both 12,000p a month, but the source changed from
    # monthly to yearly.
    facts = buying(
        [
            money("E-OLD", "energy", 12_000, Period.MONTH, used_from_step=1),
            money("E-NEW", "energy", 144_000, Period.YEAR, used_from_step=4, supersedes="E-OLD"),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.monthly_difference == Pence.ZERO
    assert change.annual_difference is None


def test_build_home_costs_yearly_to_monthly_with_the_same_monthly_amount_is_a_value_change() -> (
    None
):
    facts = buying(
        [
            money("E-OLD", "energy", 144_000, Period.YEAR, used_from_step=1),
            money("E-NEW", "energy", 12_000, Period.MONTH, used_from_step=4, supersedes="E-OLD"),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.monthly_difference == Pence.ZERO
    assert change.annual_difference is None


def test_build_home_costs_same_source_amount_changing_period_is_reported_as_value_changed() -> None:
    # 12,000p a month, then 12,000p a year: the source amount is the same, only its period
    # changed. That is a value change. The monthly lines are 12,000p and 12,000 / 12 = 1,000p, so
    # the monthly difference is 1,000 - 12,000 = -11,000p; the sides are not both yearly, so there
    # is no annual difference.
    facts = buying(
        [
            money("E-OLD", "energy", 12_000, Period.MONTH, used_from_step=1),
            money("E-NEW", "energy", 12_000, Period.YEAR, used_from_step=4, supersedes="E-OLD"),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.monthly_difference == Pence(-11_000)
    assert change.annual_difference is None


def test_build_home_costs_amount_then_not_applicable_is_reported_as_no_longer_applies() -> None:
    facts = buying(
        [
            money("SC-OLD", "service-charge", 240_000, Period.YEAR, used_from_step=1),
            no_value(
                "SC-NEW",
                "service-charge",
                EvidenceStatus.NOT_APPLICABLE,
                used_from_step=4,
                supersedes="SC-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.category == CostCategory.SERVICE_CHARGE
    assert change.kind == ChangeKind.NO_LONGER_APPLIES
    assert change.previous_evidence_ids == ("SC-OLD",)
    assert change.current_evidence_ids == ()
    assert change.monthly_difference is None


def test_build_home_costs_conflicting_then_not_applicable_is_reported_as_no_longer_applies() -> (
    None
):
    facts = buying(
        [
            no_value("GR-OLD", "ground-rent", EvidenceStatus.CONFLICTING),
            no_value(
                "GR-NEW",
                "ground-rent",
                EvidenceStatus.NOT_APPLICABLE,
                used_from_step=4,
                supersedes="GR-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.kind == ChangeKind.NO_LONGER_APPLIES
    assert change.previous_evidence_ids == ("GR-OLD",)
    assert change.current_evidence_ids == ()


# A line that is left out (not applicable) has no result at all, and a line with no information has
# a result with status Missing, no amount and no evidence. Neither has an amount, and neither has
# evidence ids, so only the status says they differ. A line that was left out and is now unknown
# has had its status change with no figure moving (evidence changed); a line that was unknown and
# is now left out "became not applicable". Both must be reported, or the change from "does not
# apply" to "unknown" would be hidden (AGENTS.md rule 7).


def test_build_home_costs_not_applicable_then_missing_is_reported_as_evidence_changed() -> None:
    facts = buying(
        [
            no_value("M-OLD", "maintenance", EvidenceStatus.NOT_APPLICABLE),
            no_value(
                "M-NEW",
                "maintenance",
                EvidenceStatus.MISSING,
                used_from_step=4,
                supersedes="M-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.category == CostCategory.MAINTENANCE
    assert change.kind == ChangeKind.EVIDENCE_CHANGED
    assert change.monthly_difference is None
    assert change.previous_evidence_ids == ()
    assert change.current_evidence_ids == ()


def test_build_home_costs_missing_then_not_applicable_is_reported_as_no_longer_applies() -> None:
    facts = buying(
        [
            no_value("M-OLD", "maintenance", EvidenceStatus.MISSING),
            no_value(
                "M-NEW",
                "maintenance",
                EvidenceStatus.NOT_APPLICABLE,
                used_from_step=4,
                supersedes="M-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.category == CostCategory.MAINTENANCE
    assert change.kind == ChangeKind.NO_LONGER_APPLIES


def test_build_home_costs_amount_that_changes_is_reported_as_value_changed() -> None:
    home = _build(_buyer_with_service_charge_change(240_000, 372_000), FOUR_STEPS)

    assert _only_change(home).kind == ChangeKind.VALUE_CHANGED


# monthly_total_change is only given when both totals leave out the same lines (rule 7: a line
# that becomes unknown must not look like a saving).


def test_build_home_costs_line_that_becomes_conflicting_gives_no_monthly_total_change() -> None:
    facts = buying(
        [
            money("SC-OLD", "service-charge", 240_000, Period.YEAR, used_from_step=1),
            no_value(
                "SC-NEW",
                "service-charge",
                EvidenceStatus.CONFLICTING,
                used_from_step=2,
                supersedes="SC-OLD",
            ),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    assert home.scenarios[1].monthly_total_change is None
    assert _only_change(home).kind == ChangeKind.NO_LONGER_CALCULATED


def test_build_home_costs_conflicting_water_then_an_estimate_gives_no_monthly_total_change() -> (
    None
):
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            other("W-LISTING", "water-responsibility", EvidenceStatus.CONFLICTING),
            money("W-EST", "water", 4_500, Period.MONTH, used_from_step=4),
        ]
    )

    assert _build(facts, FOUR_STEPS).scenarios[1].monthly_total_change is None


def test_build_home_costs_same_lines_left_out_of_both_totals_keeps_the_monthly_total_change() -> (
    None
):
    # The same lines are missing in both scenarios; only the service charge moves:
    # 16,667 - 8,333 = 8,334p.
    home = _build(_buyer_with_service_charge_change(100_000, 200_000), FOUR_STEPS)

    assert home.scenarios[1].monthly_total_change == Pence(8_334)


def test_build_home_costs_a_different_reason_for_the_same_line_gives_no_monthly_total_change() -> (
    None
):
    # Maintenance is left out of both totals, but for a different reason (not calculated, then
    # conflicting), so the totals are not comparable.
    facts = buying(
        [
            no_value("M-OLD", "maintenance", EvidenceStatus.NOT_CALCULATED),
            no_value(
                "M-NEW",
                "maintenance",
                EvidenceStatus.CONFLICTING,
                used_from_step=4,
                supersedes="M-OLD",
            ),
        ]
    )

    assert _build(facts, FOUR_STEPS).scenarios[1].monthly_total_change is None


def test_build_home_costs_monthly_line_with_only_one_side_yearly_has_no_annual_difference() -> None:
    # 9,000p a month, then 120,000p a year, which is 10,000p a month: monthly difference 1,000p.
    facts = buying(
        [
            money("E-OLD", "energy", 9_000, Period.MONTH, used_from_step=1),
            money("E-NEW", "energy", 120_000, Period.YEAR, used_from_step=4, supersedes="E-OLD"),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.monthly_difference == Pence(1_000)
    assert change.annual_difference is None


def test_build_home_costs_buying_home_has_a_mortgage_with_the_evidence_behind_it() -> None:
    home = _build(buying([]), [1])

    (scenario,) = home.scenarios
    assert scenario.mortgage is not None
    assert scenario.mortgage.evidence_ids == ("PRICE", "DEPOSIT", "RATE", "TERM")
    repayment = scenario.mortgage.repayment
    # The loan is the price minus the deposit: 20,000,000 - 4,000,000 = 16,000,000p.
    assert repayment.loan == Pence(16_000_000)
    assert repayment.rate_basis_points == 500
    assert repayment.term_years == 20
    first = scenario.monthly.lines[0]
    assert first.category == CostCategory.MORTGAGE_REPAYMENT
    assert first.status == LineStatus.CALCULATED
    assert first.source_period == Period.MONTH
    assert first.evidence_ids == scenario.mortgage.evidence_ids
    assert first.amount == repayment.monthly_repayment


def test_build_home_costs_renting_home_has_no_mortgage() -> None:
    facts = renting([money("RENT", "rent", 100_000, Period.MONTH)])

    (scenario,) = _build(facts, [1]).scenarios

    assert scenario.mortgage is None
    assert scenario.monthly.lines[0].category == CostCategory.RENT


def test_build_home_costs_home_details_come_from_the_facts() -> None:
    home = _build(buying([]), [1])

    assert (home.home_id, home.mode, home.nation) == ("T1", Mode.BUY, Nation.ENGLAND)


def test_build_home_costs_any_monthly_budget_is_carried_into_each_scenario() -> None:
    home = _build(_buyer_with_service_charge_change(240_000, 372_000), FOUR_STEPS)

    assert [s.monthly.budget for s in home.scenarios] == [Pence(200_000), Pence(200_000)]


def test_build_home_costs_scenario_keeps_the_upfront_cash_of_its_steps() -> None:
    facts = buying(
        [
            money("MC-1", "moving-costs", 100_000, Period.ONCE),
            money(
                "MC-2", "moving-costs", 150_000, Period.ONCE, used_from_step=4, supersedes="MC-1"
            ),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    # The deposit of 4,000,000p plus the moving costs; stamp duty and legal fees have no evidence,
    # so they are missing and the total is partial.
    assert home.scenarios[0].upfront.total == Pence(4_100_000)
    assert home.scenarios[1].upfront.total == Pence(4_150_000)
    assert home.scenarios[0].upfront.is_partial


# One test per error code the builder owns, and the failures it passes on.


@pytest.mark.parametrize("nation", [Nation.WALES, Nation.SCOTLAND, Nation.NORTHERN_IRELAND])
def test_build_home_costs_home_outside_england_fails_as_not_covered(nation: Nation) -> None:
    result = build_home_costs(buying([], nation), [1])

    assert result.is_failure
    assert result.error.code == "home.not-covered"
    assert result.error.category == ErrorCategory.VALIDATION


def test_build_home_costs_home_with_no_mode_fails_as_mode_missing() -> None:
    facts = HomeFacts("T1", None, Nation.ENGLAND, tuple(buy_anchors()), Pence(200_000))

    result = build_home_costs(facts, [1])

    assert result.is_failure
    assert result.error.code == "home.mode-missing"
    assert result.error.category == ErrorCategory.VALIDATION


@pytest.mark.parametrize("steps", [[], [0, 1], [2, 1], [1, 1], [1, 3, 2], [-1], [1, 2, 2]])
def test_build_home_costs_steps_that_are_empty_below_one_or_not_increasing_fail_as_out_of_range(
    steps: list[int],
) -> None:
    result = build_home_costs(buying([]), steps)

    assert result.is_failure
    assert result.error.code == "story.step-out-of-range"
    assert result.error.category == ErrorCategory.VALIDATION


def test_build_home_costs_anchor_input_missing_passes_on_the_selectors_failure() -> None:
    facts = buying_from(anchors_except("mortgage-rate"))

    assert _failure_code(facts, [1]) == "input.missing.mortgage-rate"


def test_build_home_costs_a_later_step_that_fails_to_select_fails_the_whole_build() -> None:
    # Two rate items in use from step 2: the selector fails at step 2, so the build fails.
    facts = buying([rate("RATE-2", 600)])
    facts = HomeFacts(
        facts.home_id,
        facts.mode,
        facts.nation,
        tuple(
            EvidenceItem(item.id, item.category, item.status, item.value, False, 2, item.supersedes)
            if item.id == "RATE-2"
            else item
            for item in facts.evidence
        ),
        facts.monthly_budget,
    )

    assert _failure_code(facts, FOUR_STEPS) == "input.ambiguous.mortgage-rate"


def test_build_home_costs_deposit_larger_than_the_price_fails_as_loan_not_positive() -> None:
    deposit = money("DEPOSIT", "mortgage-deposit", 25_000_000, Period.ONCE)

    facts = buying_from(anchors_except("mortgage-deposit", deposit))

    assert _failure_code(facts, [1]) == "mortgage.loan-not-positive"


def test_build_home_costs_no_budget_fails_as_not_positive() -> None:
    facts = buying_from(buy_anchors(), Pence.ZERO)

    assert _failure_code(facts, [1]) == "input.not-positive.budget"


@pytest.mark.parametrize("bad", [None, "facts", 1])
def test_build_home_costs_facts_that_are_not_home_facts_raise_type_error(bad: Any) -> None:
    with pytest.raises(TypeError, match="HomeFacts"):
        build_home_costs(bad, [1])


@pytest.mark.parametrize("bad", [None, 1, "text"])
def test_build_home_costs_steps_that_are_not_a_sequence_raise_type_error(bad: Any) -> None:
    with pytest.raises(TypeError, match="steps"):
        build_home_costs(buying([]), bad)


@pytest.mark.parametrize("bad_step", ["2", 2.0, None, True])
def test_build_home_costs_a_step_that_is_not_an_int_raises_type_error(bad_step: Any) -> None:
    with pytest.raises(TypeError, match="step"):
        build_home_costs(buying([]), [1, bad_step])


def test_build_home_costs_a_step_above_32_bits_raises_value_error() -> None:
    with pytest.raises(ValueError, match="32-bit"):
        build_home_costs(buying([]), [1, 2**31])


def test_build_home_costs_a_step_of_exactly_the_largest_32_bit_number_is_accepted() -> None:
    home = _build(buying([]), [2**31 - 1])

    (scenario,) = home.scenarios
    assert (scenario.from_step, scenario.to_step) == (2**31 - 1, 2**31 - 1)


def test_build_home_costs_a_line_not_applicable_in_every_scenario_is_left_out_of_the_changes() -> (
    None
):
    # Ground rent is not applicable in both scenarios, so it is in neither list of lines and is
    # not a change; only the energy bill moves.
    facts = buying(
        [
            no_value("GR", "ground-rent", EvidenceStatus.NOT_APPLICABLE),
            money("EN-OLD", "energy", 9_000, Period.MONTH),
            money("EN-NEW", "energy", 12_000, Period.MONTH, used_from_step=4, supersedes="EN-OLD"),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    assert [c.category for c in home.scenarios[1].changes] == [CostCategory.ENERGY]


def test_build_home_costs_home_outside_england_and_no_steps_reports_the_home_first() -> None:
    assert _failure_code(buying([], Nation.WALES), []) == "home.not-covered"


def test_build_home_costs_steps_that_start_above_one_are_accepted() -> None:
    home = _build(buying([]), [2, 3])

    (scenario,) = home.scenarios
    assert scenario.scenario_id == "from-step-2"
    assert (scenario.from_step, scenario.to_step) == (2, 3)


def test_build_home_costs_steps_as_a_tuple_or_a_list_are_accepted() -> None:
    assert len(_build(buying([]), (1, 2)).scenarios) == 1
    assert len(_build(buying([]), [1, 2]).scenarios) == 1


@pytest.mark.parametrize("bad", [range(1, 5), b"\x01\x02", bytearray(b"\x01"), {1: 2}.keys()])
def test_build_home_costs_steps_that_are_not_a_list_or_tuple_raise_type_error(bad: Any) -> None:
    with pytest.raises(TypeError, match="list or tuple"):
        build_home_costs(buying([]), bad)


def test_build_home_costs_upfront_line_given_monthly_fails_as_wrong_period() -> None:
    # The selector checks only the anchors; the upfront calculation rejects a one-off cost given
    # per month.
    facts = buying([money("MC", "moving-costs", 100_000, Period.MONTH)])

    assert _failure_code(facts, [1]) == "input.wrong-period.moving-costs"


def test_build_home_costs_upfront_line_of_zero_fails_as_not_positive() -> None:
    facts = buying([money("MC", "moving-costs", 0, Period.ONCE)])

    assert _failure_code(facts, [1]) == "input.not-positive.moving-costs"


def test_build_home_costs_monthly_line_of_zero_fails_as_not_positive() -> None:
    facts = buying([money("EN", "energy", 0, Period.MONTH)])

    assert _failure_code(facts, [1]) == "input.not-positive.energy"


def test_build_home_costs_upfront_amount_changes_is_a_value_change_with_no_differences() -> None:
    # The moving costs are paid once, so they have no monthly or annual difference to report.
    facts = buying(
        [
            money("MC-OLD", "moving-costs", 100_000, Period.ONCE, used_from_step=1),
            money(
                "MC-NEW",
                "moving-costs",
                150_000,
                Period.ONCE,
                used_from_step=4,
                supersedes="MC-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.category == CostCategory.MOVING_COSTS
    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.monthly_difference is None
    assert change.annual_difference is None
    assert change.previous_evidence_ids == ("MC-OLD",)
    assert change.current_evidence_ids == ("MC-NEW",)


def test_build_home_costs_upfront_same_amount_from_new_evidence_is_evidence_changed() -> None:
    facts = buying(
        [
            money("MC-OLD", "moving-costs", 100_000, Period.ONCE, used_from_step=1),
            money(
                "MC-NEW",
                "moving-costs",
                100_000,
                Period.ONCE,
                used_from_step=4,
                supersedes="MC-OLD",
            ),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.kind == ChangeKind.EVIDENCE_CHANGED


def test_build_home_costs_line_not_applicable_then_estimated_is_reported_as_now_calculated() -> (
    None
):
    facts = buying(
        [
            EvidenceItem("W-OLD", "water", EvidenceStatus.NOT_APPLICABLE, None, False, 1, None),
            money("W-NEW", "water", 12_000, Period.MONTH, used_from_step=4, supersedes="W-OLD"),
        ]
    )

    change = _only_change(_build(facts, FOUR_STEPS))

    assert change.category == CostCategory.WATER
    assert change.kind == ChangeKind.NOW_CALCULATED
    assert change.previous_evidence_ids == ()
    assert change.current_evidence_ids == ("W-NEW",)


def test_build_home_costs_only_the_mortgage_rate_changes_gives_a_repayment_change() -> None:
    facts = buying(
        [
            EvidenceItem(
                "RATE-NEW",
                "mortgage-rate",
                EvidenceStatus.AVAILABLE,
                RateValue(600),
                False,
                4,
                "RATE",
            ),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    assert len(home.scenarios) == 2
    change = _only_change(home)
    assert change.category == CostCategory.MORTGAGE_REPAYMENT
    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.previous_evidence_ids == ("PRICE", "DEPOSIT", "RATE", "TERM")
    assert change.current_evidence_ids == ("PRICE", "DEPOSIT", "RATE-NEW", "TERM")
    # The repayment is a monthly source amount, so there is a monthly difference and no annual one.
    # A higher rate on the same loan costs more each month.
    assert change.monthly_difference is not None
    assert change.monthly_difference > Pence.ZERO
    assert change.annual_difference is None
    first, second = (s.mortgage for s in home.scenarios)
    assert first is not None
    assert second is not None
    assert second.evidence_ids == ("PRICE", "DEPOSIT", "RATE-NEW", "TERM")
    assert second.repayment.rate_basis_points == 600
    assert second.repayment.monthly_repayment - first.repayment.monthly_repayment == (
        change.monthly_difference
    )
    assert home.scenarios[1].monthly_total_change == change.monthly_difference


def test_build_home_costs_changes_are_given_as_tuples_of_ids() -> None:
    change = _only_change(_build(_buyer_with_service_charge_change(240_000, 372_000), FOUR_STEPS))

    assert isinstance(change.previous_evidence_ids, tuple)
    assert isinstance(change.current_evidence_ids, tuple)


def test_build_home_costs_does_not_report_a_line_that_did_not_change() -> None:
    facts = buying(
        [
            money("EN", "energy", 9_000, Period.MONTH),
            money("SC-OLD", "service-charge", 100_000, Period.YEAR),
            money(
                "SC-NEW",
                "service-charge",
                200_000,
                Period.YEAR,
                used_from_step=4,
                supersedes="SC-OLD",
            ),
        ]
    )

    home = _build(facts, FOUR_STEPS)

    assert [c.category for c in home.scenarios[1].changes] == [CostCategory.SERVICE_CHARGE]


# End to end: a home built from the evidence matches the independently worked monthly and
# upfront cases in the file, line by line.


def _mapped_evidence(
    case_id: str, story_case: dict[str, Any]
) -> tuple[list[EvidenceItem], dict[str, tuple[str, ...]]]:
    """Evidence for the lines of a worked case, and the evidence ids each line should carry."""
    items: list[EvidenceItem] = []
    ids: dict[str, tuple[str, ...]] = {}
    for line in story_case["inputs"]["lines"]:
        name = line["category"]
        item_id = f"{case_id}:{name}"
        if "mortgageCase" in line:
            inputs = case(line["mortgageCase"])["inputs"]
            items += [
                money("PRICE", "asking-price", inputs["askingPricePence"], Period.ONCE),
                money("DEPOSIT", "mortgage-deposit", inputs["depositPence"], Period.ONCE),
                rate("RATE", basis_points(inputs["annualRate"])),
                years("TERM", inputs["termYears"]),
            ]
            ids[name] = ("PRICE", "DEPOSIT", "RATE", "TERM")
        elif "amountPence" in line:
            period = {"once": Period.ONCE, "month": Period.MONTH, "year": Period.YEAR}[
                line["period"]
            ]
            if name != "mortgage-deposit":  # a buyer's deposit is the mortgage anchor
                items.append(money(item_id, name, line["amountPence"], period))
                ids[name] = (item_id,)
        elif line["status"] == "missing":
            items.append(no_value(item_id, name, EvidenceStatus.MISSING))
            ids[name] = ()
        else:
            status = EvidenceStatus(line["status"])
            items.append(no_value(item_id, name, status))
            ids[name] = (item_id,)
    return items, ids


@pytest.mark.parametrize("case_id", MONTHLY_CASE_IDS)
def test_build_home_costs_worked_home_matches_the_worked_monthly_and_upfront_cases(
    case_id: str,
) -> None:
    monthly_case = case(case_id)
    home_id = monthly_case["inputs"]["home"]
    upfront_case = case(f"{home_id.lower()}-upfront-cash")
    monthly_items, monthly_ids = _mapped_evidence(case_id, monthly_case)
    # A bill the case does not list must be named here as "not applicable" (rule 7: an unlisted
    # bill is never quietly assumed away). B2 is a freehold house: the fixture records B2-SC and
    # B2-GROUND-RENT as not-applicable evidence (packages/fixtures/data/evidence.json).
    listed = {line["category"] for line in monthly_case["inputs"]["lines"]}
    bills = BUY_BILLS if mode_of(monthly_case) == Mode.BUY else RENT_BILLS
    not_applicable = NOT_APPLICABLE_BILLS.get(case_id, ())
    unexplained = [name for name in bills if name not in listed and name not in not_applicable]
    assert unexplained == [], f"{case_id} leaves out {unexplained} without saying why"
    assert not [name for name in not_applicable if name in listed], "listed and not applicable"
    monthly_items += [
        no_value(f"{case_id}:{name}", name, EvidenceStatus.NOT_APPLICABLE)
        for name in not_applicable
    ]
    upfront_items, upfront_ids = _mapped_evidence(upfront_case["id"], upfront_case)
    # A buyer's deposit is one input: both worked cases must agree on it.
    for line in upfront_case["inputs"]["lines"]:
        if line["category"] == "mortgage-deposit":
            (deposit,) = [i for i in monthly_items if i.category == "mortgage-deposit"]
            assert deposit.value is not None
            assert deposit.value.amount == Pence(line["amountPence"])  # type: ignore[union-attr]  # a money value
            upfront_ids[line["category"]] = ("DEPOSIT",)
    facts = HomeFacts(
        home_id,
        mode_of(monthly_case),
        Nation.ENGLAND,
        tuple(monthly_items + upfront_items),
        budget_of(monthly_case),
    )

    (scenario,) = _build(facts, [1]).scenarios

    expected = monthly_case["expected"]
    monthly = scenario.monthly
    assert monthly.total == Pence(expected["totalMonthlyPence"])
    assert monthly.is_partial == expected["totalIsPartial"]
    assert monthly.budget == Pence(expected["budgetPence"])
    assert monthly.budget_difference == Pence(expected["budgetDifferencePence"])
    assert monthly.within_budget == expected["withinBudget"]
    assert len(monthly.lines) == len(expected["lines"])
    for expected_line in expected["lines"]:
        category = category_from_id(expected_line["category"])
        line = _line(monthly.lines, category)
        if "monthlyPence" in expected_line:
            assert line.status == LineStatus.CALCULATED, category
            assert line.amount == Pence(expected_line["monthlyPence"]), category
        else:
            assert line.amount is None, category
            assert status_id(line.status) == expected_line["status"], category
        assert line.evidence_ids == monthly_ids[category_id(category)], category

    expected_upfront = upfront_case["expected"]
    upfront = scenario.upfront
    assert upfront.total == Pence(expected_upfront["totalUpfrontPence"])
    assert upfront.is_partial == expected_upfront["totalIsPartial"]
    assert len(upfront.lines) == len(expected_upfront["lines"])
    for expected_line in expected_upfront["lines"]:
        category = category_from_id(expected_line["category"])
        line = _line(upfront.lines, category)
        if "amountPence" in expected_line:
            assert line.status == LineStatus.CALCULATED, category
            assert line.amount == Pence(expected_line["amountPence"]), category
        else:
            assert line.amount is None, category
            assert status_id(line.status) == expected_line["status"], category
        assert line.evidence_ids == upfront_ids[category_id(category)], category


def _b1_story() -> HomeFacts:
    """B1 over four steps: the insurance arrives at step 3, the 2026 budget at step 4."""
    listing_case = case("b1-monthly-housing-cost-listing-service-charge")
    items, _ = _mapped_evidence("listing", listing_case)
    items = [item for item in items if item.category not in ("service-charge",)]
    items = [item for item in items if item.category != "buildings-insurance"]
    inputs = case(DIFFERENCE_CASE_ID)["inputs"]
    items += [
        money(
            "SC-LISTING",
            "service-charge",
            inputs["listingServiceChargeAnnualPence"],
            Period.YEAR,
            used_from_step=1,
        ),
        no_value("INS-GAP", "buildings-insurance", EvidenceStatus.MISSING, used_from_step=1),
        no_value(
            "INS-PACK",
            "buildings-insurance",
            EvidenceStatus.INCLUDED,
            used_from_step=3,
            supersedes="INS-GAP",
        ),
        money(
            "SC-BUDGET",
            "service-charge",
            inputs["budgetServiceChargeAnnualPence"],
            Period.YEAR,
            used_from_step=4,
            supersedes="SC-LISTING",
        ),
    ]
    return HomeFacts("B1", Mode.BUY, Nation.ENGLAND, tuple(items), budget_of(listing_case))


def test_build_home_costs_b1_story_matches_the_three_worked_monthly_cases() -> None:
    listing = case("b1-monthly-housing-cost-listing-service-charge")["expected"]
    pack = case("b1-monthly-housing-cost-management-pack-arrived")["expected"]
    budget = case("b1-monthly-housing-cost-2026-budget")["expected"]

    home = _build(_b1_story(), FOUR_STEPS)

    assert [s.scenario_id for s in home.scenarios] == ["from-step-1", "from-step-3", "from-step-4"]
    assert [(s.from_step, s.to_step) for s in home.scenarios] == [(1, 2), (3, 3), (4, 4)]
    totals = [s.monthly.total for s in home.scenarios]
    assert totals == [
        Pence(listing["totalMonthlyPence"]),
        Pence(pack["totalMonthlyPence"]),
        Pence(budget["totalMonthlyPence"]),
    ]
    assert [s.monthly.budget_difference for s in home.scenarios] == [
        Pence(listing["budgetDifferencePence"]),
        Pence(pack["budgetDifferencePence"]),
        Pence(budget["budgetDifferencePence"]),
    ]
    assert [s.monthly.within_budget for s in home.scenarios] == [
        listing["withinBudget"],
        pack["withinBudget"],
        budget["withinBudget"],
    ]
    # Step 3: the insurance went from missing to included, so no figure moved; the totals leave
    # out different lines, so no monthly total change is given.
    insurance = _change_for(home, CostCategory.BUILDINGS_INSURANCE)
    assert insurance.kind == ChangeKind.EVIDENCE_CHANGED
    assert (insurance.previous_evidence_ids, insurance.current_evidence_ids) == ((), ("INS-PACK",))
    assert home.scenarios[1].monthly_total_change is None
    # Step 4: only the service charge moves, by the worked monthly difference.
    expected = case(DIFFERENCE_CASE_ID)["expected"]
    assert home.scenarios[2].monthly_total_change == Pence(expected["monthlyDifferencePence"])
    assert [c.category for c in home.scenarios[2].changes] == [CostCategory.SERVICE_CHARGE]


def test_build_home_costs_r1_story_matches_the_worked_before_and_after_water_cases() -> None:
    before = case("r1-monthly-housing-cost-before-water")
    after = case("r1-monthly-housing-cost-after-water")
    items, _ = _mapped_evidence("r1", before)
    items = [item for item in items if item.category != "water"]
    items += [
        no_value("W-LISTING", "water", EvidenceStatus.CONFLICTING),
        money("W-EST", "water", 4_500, Period.MONTH, used_from_step=4),
    ]
    (after_water,) = [line for line in after["inputs"]["lines"] if line["category"] == "water"]
    assert after_water["amountPence"] == 4_500  # the estimate the worked "after" case uses
    facts = HomeFacts("R1", Mode.RENT, Nation.ENGLAND, tuple(items), budget_of(before))

    home = _build(facts, FOUR_STEPS)

    assert [s.monthly.total for s in home.scenarios] == [
        Pence(before["expected"]["totalMonthlyPence"]),
        Pence(after["expected"]["totalMonthlyPence"]),
    ]
    assert [s.monthly.is_partial for s in home.scenarios] == [True, False]
    assert home.scenarios[1].monthly_total_change is None
    assert _only_change(home).kind == ChangeKind.NOW_CALCULATED
