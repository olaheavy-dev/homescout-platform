"""The deliberate story beat, ported from the C# BudgetBeatTests.

B1 is within the 1,600 pound budget on the listing service charge and over it on the 2026 budget.
Both totals come from the monthly cost and are compared with the worked case.
"""

from typing import Any

from engine_support import budget_of, case, case_ids_where, lines_of, mode_of
from vestagraph_engine import Pence
from vestagraph_engine.breakdowns import MonthlyBreakdown
from vestagraph_engine.monthly_cost import monthly_cost

# The budget-beat cases are those that name the two monthly cases they combine.
BUDGET_BEAT_CASE_IDS = case_ids_where("listingTotalCase")


def _run(case_id: str) -> MonthlyBreakdown:
    monthly_case: dict[str, Any] = case(case_id)
    return monthly_cost(
        mode_of(monthly_case), lines_of(monthly_case), budget_of(monthly_case)
    ).value


def test_budget_beat_file_has_one_budget_beat_case() -> None:
    assert len(BUDGET_BEAT_CASE_IDS) == 1


def test_budget_beat_story_case_lands_as_worked() -> None:
    beat = case(BUDGET_BEAT_CASE_IDS[0])
    on_listing = _run(beat["inputs"]["listingTotalCase"])
    on_budget = _run(beat["inputs"]["budgetTotalCase"])
    expected = beat["expected"]

    assert on_listing.total == Pence(expected["listingTotalPence"])
    assert on_budget.total == Pence(expected["budgetTotalPence"])
    assert on_listing.budget_difference == Pence(expected["listingBudgetDifferencePence"])
    assert on_budget.budget_difference == Pence(expected["budgetBudgetDifferencePence"])
    assert on_listing.within_budget == expected["withinBudgetOnListing"]
    assert (not on_budget.within_budget) == expected["overBudgetOn2026Budget"]
    assert (on_listing.is_partial and on_budget.is_partial) == expected["totalsArePartial"]
    assert (on_listing.within_budget and not on_budget.within_budget) == expected["landed"]
