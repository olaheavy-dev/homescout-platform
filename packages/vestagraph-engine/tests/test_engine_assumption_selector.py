"""The five selection rules of the assumption selector, one test group each, then one test per
error code (ported from the C# AssumptionSelectorTests).

The amounts are arbitrary inputs; the expectations are which item is chosen and what kind of line
comes out. No calculated figure is checked here.
"""

from typing import Any

import pytest
from engine_support import (
    anchors_except,
    buy_anchors,
    buying,
    buying_from,
    money,
    monthly_line,
    no_value,
    other,
    renting,
    upfront_line,
    years,
)
from vestagraph_engine import ErrorCategory, Pence
from vestagraph_engine.assumption_selector import select_assumptions
from vestagraph_engine.cost_types import CostCategory, Mode, Period
from vestagraph_engine.evidence import (
    EvidenceItem,
    EvidenceStatus,
    HomeFacts,
    Nation,
    RateValue,
    YearsValue,
)
from vestagraph_engine.line_input import (
    AmountLine,
    ConflictingLine,
    IncludedLine,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.selected_inputs import SelectedInputs

BUY_MONTHLY_ORDER = [
    CostCategory.SERVICE_CHARGE,
    CostCategory.GROUND_RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
    CostCategory.BUILDINGS_INSURANCE,
    CostCategory.MAINTENANCE,
]
RENT_MONTHLY_ORDER = [
    CostCategory.RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
]
BUY_UPFRONT_ORDER = [
    CostCategory.MORTGAGE_DEPOSIT,
    CostCategory.MOVING_COSTS,
    CostCategory.STAMP_DUTY,
    CostCategory.LEGAL_FEES,
]
RENT_UPFRONT_ORDER = [
    CostCategory.DEPOSIT,
    CostCategory.FIRST_MONTH_RENT,
    CostCategory.MOVING_COSTS,
]


def _select(facts: HomeFacts, step: int = 1) -> SelectedInputs:
    result = select_assumptions(facts, step)
    assert result.is_success, result.error.code if result.is_failure else ""
    return result.value


def _failure_code(facts: HomeFacts, step: int = 1) -> str:
    result = select_assumptions(facts, step)
    assert result.is_failure
    return result.error.code


def _item(item_id: str, category: str, value: Any) -> EvidenceItem:
    """An available item with a value of any kind (for the wrong-kind tests)."""
    return EvidenceItem(item_id, category, EvidenceStatus.AVAILABLE, value, False, None, None)


# Rule 1: context-only items are ignored.


def test_select_assumptions_context_only_item_is_ignored() -> None:
    facts = buying([money("EPC-COST", "water", 78_000, Period.YEAR, context_only=True)])

    water = monthly_line(_select(facts), CostCategory.WATER)

    assert water == MissingLine(CostCategory.WATER)


def test_select_assumptions_context_only_item_that_supersedes_replaces_nothing() -> None:
    facts = buying(
        [
            money("SC-OLD", "service-charge", 100_000, Period.YEAR),
            money(
                "SC-CTX",
                "service-charge",
                200_000,
                Period.YEAR,
                supersedes="SC-OLD",
                context_only=True,
            ),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.SERVICE_CHARGE)

    assert line == AmountLine(CostCategory.SERVICE_CHARGE, Pence(100_000), Period.YEAR, ("SC-OLD",))


# Rule 2: an item is in use from its step, until an item that supersedes it starts.


def test_select_assumptions_item_not_yet_used_is_ignored_before_its_step() -> None:
    facts = buying([money("EN-LATER", "energy", 9_000, Period.MONTH, used_from_step=4)])

    assert monthly_line(_select(facts, 3), CostCategory.ENERGY) == MissingLine(CostCategory.ENERGY)
    assert isinstance(monthly_line(_select(facts, 4), CostCategory.ENERGY), AmountLine)


def test_select_assumptions_item_with_no_start_step_is_in_use_from_the_first_step() -> None:
    facts = buying([money("EN", "energy", 9_000, Period.MONTH)])

    assert isinstance(monthly_line(_select(facts), CostCategory.ENERGY), AmountLine)


def test_select_assumptions_superseded_item_is_used_until_the_new_one_starts() -> None:
    facts = buying(
        [
            money("SC-OLD", "service-charge", 100_000, Period.YEAR, used_from_step=1),
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

    before = monthly_line(_select(facts, 3), CostCategory.SERVICE_CHARGE)
    after = monthly_line(_select(facts, 4), CostCategory.SERVICE_CHARGE)

    assert before == AmountLine(
        CostCategory.SERVICE_CHARGE, Pence(100_000), Period.YEAR, ("SC-OLD",)
    )
    assert after == AmountLine(
        CostCategory.SERVICE_CHARGE, Pence(200_000), Period.YEAR, ("SC-NEW",)
    )


# Rule 2 with a chain: A is replaced by B from step 2, and B by C from step 3.


def _chain() -> HomeFacts:
    return buying(
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


@pytest.mark.parametrize(
    ("step", "expected_id"), [(1, "SC-A"), (2, "SC-B"), (3, "SC-C"), (4, "SC-C")]
)
def test_select_assumptions_supersede_chain_uses_only_the_latest_item_that_has_started(
    step: int, expected_id: str
) -> None:
    line = monthly_line(_select(_chain(), step), CostCategory.SERVICE_CHARGE)

    assert isinstance(line, AmountLine)
    assert line.evidence_ids == (expected_id,)


# Rule 3: for each category, an amount first, then conflicting, not-calculated, included,
# not-applicable, missing.


@pytest.mark.parametrize(
    "status", [EvidenceStatus.AVAILABLE, EvidenceStatus.CONFLICTING, EvidenceStatus.STALE]
)
def test_select_assumptions_money_item_with_a_value_gives_an_amount_whatever_its_status(
    status: EvidenceStatus,
) -> None:
    facts = buying([money("EN", "energy", 9_000, Period.MONTH, status)])

    line = monthly_line(_select(facts), CostCategory.ENERGY)

    assert line == AmountLine(CostCategory.ENERGY, Pence(9_000), Period.MONTH, ("EN",))


def test_select_assumptions_yearly_money_item_keeps_its_yearly_period() -> None:
    facts = buying([money("SC", "service-charge", 240_000, Period.YEAR)])

    line = monthly_line(_select(facts), CostCategory.SERVICE_CHARGE)

    assert line == AmountLine(CostCategory.SERVICE_CHARGE, Pence(240_000), Period.YEAR, ("SC",))


def test_select_assumptions_included_item_gives_an_included_line() -> None:
    facts = buying([no_value("INS", "buildings-insurance", EvidenceStatus.INCLUDED)])

    line = monthly_line(_select(facts), CostCategory.BUILDINGS_INSURANCE)

    assert line == IncludedLine(CostCategory.BUILDINGS_INSURANCE, ("INS",))


def test_select_assumptions_not_calculated_item_gives_a_not_calculated_line() -> None:
    facts = buying([no_value("STAMP", "stamp-duty", EvidenceStatus.NOT_CALCULATED)])

    line = upfront_line(_select(facts), CostCategory.STAMP_DUTY)

    assert line == NotCalculatedLine(CostCategory.STAMP_DUTY, ("STAMP",))


def test_select_assumptions_several_not_calculated_items_are_all_named_in_order() -> None:
    facts = buying(
        [
            no_value("M-1", "maintenance", EvidenceStatus.NOT_CALCULATED),
            no_value("M-2", "maintenance", EvidenceStatus.INCLUDED),
            no_value("M-3", "maintenance", EvidenceStatus.NOT_CALCULATED),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.MAINTENANCE)

    assert line == NotCalculatedLine(CostCategory.MAINTENANCE, ("M-1", "M-3"))


def test_select_assumptions_several_included_items_are_all_named_in_order() -> None:
    facts = buying(
        [
            no_value("M-1", "maintenance", EvidenceStatus.INCLUDED),
            no_value("M-2", "maintenance", EvidenceStatus.NOT_APPLICABLE),
            no_value("M-3", "maintenance", EvidenceStatus.INCLUDED),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.MAINTENANCE)

    assert line == IncludedLine(CostCategory.MAINTENANCE, ("M-1", "M-3"))


def test_select_assumptions_not_applicable_item_leaves_the_line_out() -> None:
    facts = buying([no_value("SC", "service-charge", EvidenceStatus.NOT_APPLICABLE)])

    inputs = _select(facts)

    assert monthly_line(inputs, CostCategory.SERVICE_CHARGE) is None
    assert CostCategory.SERVICE_CHARGE not in [line.category for line in inputs.monthly_lines]


def test_select_assumptions_not_applicable_alongside_a_missing_item_leaves_the_line_out() -> None:
    facts = buying(
        [
            no_value("GR-1", "ground-rent", EvidenceStatus.MISSING),
            no_value("GR-2", "ground-rent", EvidenceStatus.NOT_APPLICABLE),
        ]
    )

    assert monthly_line(_select(facts), CostCategory.GROUND_RENT) is None


def test_select_assumptions_conflicting_item_without_an_amount_gives_a_conflicting_line() -> None:
    # A conflicting item that has a value which is not money is a wrong-kind failure; with no
    # value at all it is a conflict.
    facts = buying([other("GR", "ground-rent", EvidenceStatus.CONFLICTING)])
    assert _failure_code(facts) == "input.wrong-kind.ground-rent"

    no_amount = buying([no_value("GR", "ground-rent", EvidenceStatus.CONFLICTING)])
    line = monthly_line(_select(no_amount), CostCategory.GROUND_RENT)

    assert line == ConflictingLine(CostCategory.GROUND_RENT, ("GR",))


def test_select_assumptions_conflicting_line_names_every_item_of_its_own_category() -> None:
    facts = buying(
        [
            no_value("GR-1", "ground-rent", EvidenceStatus.CONFLICTING),
            no_value("GR-2", "ground-rent", EvidenceStatus.INCLUDED),
            no_value("EN-1", "energy", EvidenceStatus.NOT_APPLICABLE),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.GROUND_RENT)

    assert line == ConflictingLine(CostCategory.GROUND_RENT, ("GR-1", "GR-2"))


def test_select_assumptions_no_evidence_for_a_category_gives_a_missing_line_without_evidence() -> (
    None
):
    line = monthly_line(_select(buying([])), CostCategory.BROADBAND)

    assert line == MissingLine(CostCategory.BROADBAND)
    assert line is not None
    assert line.evidence_ids == ()


def test_select_assumptions_item_with_status_missing_gives_a_missing_line_without_evidence() -> (
    None
):
    facts = buying([no_value("BB", "broadband", EvidenceStatus.MISSING)])

    line = monthly_line(_select(facts), CostCategory.BROADBAND)

    assert line == MissingLine(CostCategory.BROADBAND)
    assert line is not None
    assert line.evidence_ids == ()


def test_select_assumptions_line_that_does_not_belong_to_the_mode_is_not_returned() -> None:
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            money("SC", "service-charge", 100_000, Period.YEAR),
        ]
    )

    inputs = _select(facts)

    assert CostCategory.SERVICE_CHARGE not in [line.category for line in inputs.monthly_lines]
    assert CostCategory.SERVICE_CHARGE not in [line.category for line in inputs.upfront_lines]


# The lines come back in the engine's fixed order for the mode.


def test_select_assumptions_buying_gives_the_buy_lines_in_the_fixed_order() -> None:
    inputs = _select(buying([]))

    assert [line.category for line in inputs.monthly_lines] == BUY_MONTHLY_ORDER
    assert [line.category for line in inputs.upfront_lines] == BUY_UPFRONT_ORDER
    # With only the anchors given, every other line is a missing line with no evidence.
    assert all(
        line == MissingLine(line.category)
        for line in (*inputs.monthly_lines, *inputs.upfront_lines)
        if line.category != CostCategory.MORTGAGE_DEPOSIT
    )


def test_select_assumptions_renting_gives_the_rent_lines_in_the_fixed_order() -> None:
    inputs = _select(renting([money("RENT", "rent", 100_000, Period.MONTH)]))

    assert inputs.mode == Mode.RENT
    assert [line.category for line in inputs.monthly_lines] == RENT_MONTHLY_ORDER
    assert [line.category for line in inputs.upfront_lines] == RENT_UPFRONT_ORDER
    assert all(isinstance(line, MissingLine) for line in inputs.upfront_lines)
    assert all(isinstance(line, MissingLine) for line in inputs.monthly_lines[1:])


# Precedence between statuses (rule 3).


def test_select_assumptions_included_alongside_conflicting_gives_conflicting() -> None:
    facts = buying(
        [
            no_value("INS-1", "buildings-insurance", EvidenceStatus.INCLUDED),
            no_value("INS-2", "buildings-insurance", EvidenceStatus.CONFLICTING),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.BUILDINGS_INSURANCE)

    assert line == ConflictingLine(CostCategory.BUILDINGS_INSURANCE, ("INS-1", "INS-2"))


def test_select_assumptions_included_water_alongside_conflicting_responsibility_conflicts() -> None:
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            no_value("W-INC", "water", EvidenceStatus.INCLUDED),
            other("W-RESP", "water-responsibility", EvidenceStatus.CONFLICTING),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.WATER)

    assert line == ConflictingLine(CostCategory.WATER, ("W-INC", "W-RESP"))


def test_select_assumptions_not_applicable_alongside_conflicting_gives_conflicting() -> None:
    facts = buying(
        [
            no_value("GR-1", "ground-rent", EvidenceStatus.NOT_APPLICABLE),
            no_value("GR-2", "ground-rent", EvidenceStatus.CONFLICTING),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.GROUND_RENT)

    assert line == ConflictingLine(CostCategory.GROUND_RENT, ("GR-1", "GR-2"))


def test_select_assumptions_not_calculated_alongside_included_gives_not_calculated() -> None:
    # Not calculated wins, as the more cautious.
    facts = buying(
        [
            no_value("M-1", "maintenance", EvidenceStatus.INCLUDED),
            no_value("M-2", "maintenance", EvidenceStatus.NOT_CALCULATED),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.MAINTENANCE)

    assert line == NotCalculatedLine(CostCategory.MAINTENANCE, ("M-2",))


def test_select_assumptions_included_alongside_not_applicable_gives_included() -> None:
    facts = buying(
        [
            no_value("M-1", "maintenance", EvidenceStatus.NOT_APPLICABLE),
            no_value("M-2", "maintenance", EvidenceStatus.INCLUDED),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.MAINTENANCE)

    assert line == IncludedLine(CostCategory.MAINTENANCE, ("M-2",))


def test_select_assumptions_conflicting_alongside_not_calculated_gives_conflicting() -> None:
    facts = buying(
        [
            no_value("M-1", "maintenance", EvidenceStatus.NOT_CALCULATED),
            no_value("M-2", "maintenance", EvidenceStatus.CONFLICTING),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.MAINTENANCE)

    assert line == ConflictingLine(CostCategory.MAINTENANCE, ("M-1", "M-2"))


def test_select_assumptions_money_alongside_conflicting_still_gives_the_amount() -> None:
    facts = buying(
        [
            money("EN-1", "energy", 9_000, Period.MONTH),
            no_value("EN-2", "energy", EvidenceStatus.CONFLICTING),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.ENERGY)

    assert line == AmountLine(CostCategory.ENERGY, Pence(9_000), Period.MONTH, ("EN-1",))


# Wrong kind is reported before ambiguous, for ordinary lines and for anchors.


def test_select_assumptions_wrong_kind_and_two_values_fails_as_wrong_kind_for_a_line() -> None:
    facts = buying(
        [
            money("EN-1", "energy", 9_000, Period.MONTH),
            _item("EN-2", "energy", RateValue(500)),
        ]
    )

    assert _failure_code(facts) == "input.wrong-kind.energy"


def test_select_assumptions_wrong_kind_and_two_values_fails_as_wrong_kind_for_an_anchor() -> None:
    facts = buying([_item("PRICE-2", "asking-price", RateValue(500))])

    assert _failure_code(facts) == "input.wrong-kind.asking-price"


def test_select_assumptions_rent_with_wrong_kind_and_two_values_fails_as_wrong_kind() -> None:
    facts = renting(
        [
            money("RENT-1", "rent", 100_000, Period.MONTH),
            _item("RENT-2", "rent", YearsValue(3)),
        ]
    )

    assert _failure_code(facts) == "input.wrong-kind.rent"


# Rule 4: water-responsibility items count towards the water line, for the conflicting check only.


def test_select_assumptions_conflicting_water_responsibility_names_both_items() -> None:
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            other("W-LISTING", "water-responsibility", EvidenceStatus.CONFLICTING),
            other("W-STATEMENT", "water-responsibility", EvidenceStatus.AVAILABLE),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.WATER)

    assert line == ConflictingLine(CostCategory.WATER, ("W-LISTING", "W-STATEMENT"))


def test_select_assumptions_water_estimate_wins_over_conflicting_responsibility() -> None:
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            other("W-LISTING", "water-responsibility", EvidenceStatus.CONFLICTING),
            money("W-EST", "water", 4_500, Period.MONTH, used_from_step=4),
        ]
    )

    assert isinstance(monthly_line(_select(facts, 3), CostCategory.WATER), ConflictingLine)

    after = monthly_line(_select(facts, 4), CostCategory.WATER)
    assert after == AmountLine(CostCategory.WATER, Pence(4_500), Period.MONTH, ("W-EST",))


def test_select_assumptions_water_responsibility_does_not_affect_another_category() -> None:
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            other("W-LISTING", "water-responsibility", EvidenceStatus.CONFLICTING),
        ]
    )

    assert monthly_line(_select(facts), CostCategory.ENERGY) == MissingLine(CostCategory.ENERGY)


def test_select_assumptions_water_responsibility_that_is_not_conflicting_adds_nothing() -> None:
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            other("W-STATEMENT", "water-responsibility", EvidenceStatus.AVAILABLE),
        ]
    )

    assert monthly_line(_select(facts), CostCategory.WATER) == MissingLine(CostCategory.WATER)


# Rule 5: two in-use money items for one category are a failure.


def test_select_assumptions_two_money_items_for_one_category_fails_as_ambiguous() -> None:
    facts = buying(
        [
            money("EN-1", "energy", 9_000, Period.MONTH),
            money("EN-2", "energy", 9_500, Period.MONTH),
        ]
    )

    result = select_assumptions(facts, 1)

    assert result.is_failure
    assert result.error.code == "input.ambiguous.energy"
    assert result.error.category == ErrorCategory.CONFLICT


def test_select_assumptions_two_money_items_for_an_upfront_cost_fails_as_ambiguous() -> None:
    facts = buying(
        [
            money("MC-1", "moving-costs", 100_000, Period.ONCE),
            money("MC-2", "moving-costs", 110_000, Period.ONCE),
        ]
    )

    assert _failure_code(facts) == "input.ambiguous.moving-costs"


def test_select_assumptions_two_items_where_the_older_is_superseded_is_not_ambiguous() -> None:
    facts = buying(
        [
            money("EN-1", "energy", 9_000, Period.MONTH),
            money("EN-2", "energy", 9_500, Period.MONTH, supersedes="EN-1"),
        ]
    )

    line = monthly_line(_select(facts), CostCategory.ENERGY)

    assert line == AmountLine(CostCategory.ENERGY, Pence(9_500), Period.MONTH, ("EN-2",))


# The inputs a purchase needs.


def test_select_assumptions_buying_home_returns_the_mortgage_inputs_with_their_evidence() -> None:
    mortgage = _select(buying([])).mortgage

    assert mortgage is not None
    assert mortgage.asking_price == Pence(20_000_000)
    assert mortgage.deposit == Pence(4_000_000)
    assert mortgage.rate_basis_points == 500
    assert mortgage.term_years == 20
    assert mortgage.evidence_ids == ("PRICE", "DEPOSIT", "RATE", "TERM")


def test_select_assumptions_buying_home_has_no_repayment_line_and_the_deposit_upfront() -> None:
    inputs = _select(buying([]))

    assert inputs.mode == Mode.BUY
    assert monthly_line(inputs, CostCategory.MORTGAGE_REPAYMENT) is None
    assert upfront_line(inputs, CostCategory.MORTGAGE_DEPOSIT) == AmountLine(
        CostCategory.MORTGAGE_DEPOSIT, Pence(4_000_000), Period.ONCE, ("DEPOSIT",)
    )


def test_select_assumptions_anchor_with_a_stale_or_conflicting_status_is_still_used() -> None:
    stale_price = money("PRICE", "asking-price", 21_000_000, Period.ONCE, EvidenceStatus.STALE)
    deposit = money("DEPOSIT", "mortgage-deposit", 4_000_000, Period.ONCE)
    conflicting_rate = EvidenceItem(
        "RATE", "mortgage-rate", EvidenceStatus.CONFLICTING, RateValue(650), False, None, None
    )
    facts = buying_from([stale_price, deposit, conflicting_rate, years("TERM", 20)])

    mortgage = _select(facts).mortgage

    assert mortgage is not None
    assert mortgage.asking_price == Pence(21_000_000)
    assert mortgage.rate_basis_points == 650


def test_select_assumptions_anchor_with_a_missing_item_and_a_real_one_uses_the_real_one() -> None:
    facts = buying([no_value("PRICE-GAP", "asking-price", EvidenceStatus.MISSING)])

    mortgage = _select(facts).mortgage

    assert mortgage is not None
    assert mortgage.evidence_ids == ("PRICE", "DEPOSIT", "RATE", "TERM")


def test_select_assumptions_renting_home_has_no_mortgage() -> None:
    facts = renting([money("RENT", "rent", 100_000, Period.MONTH)])

    inputs = _select(facts)

    assert inputs.mortgage is None
    assert monthly_line(inputs, CostCategory.RENT) == AmountLine(
        CostCategory.RENT, Pence(100_000), Period.MONTH, ("RENT",)
    )


def test_select_assumptions_renting_home_takes_the_deposit_and_first_month_rent_from_evidence() -> (
    None
):
    facts = renting(
        [
            money("RENT", "rent", 100_000, Period.MONTH),
            money("DEP", "deposit", 115_000, Period.ONCE),
            money("FMR", "first-month-rent", 100_000, Period.ONCE),
        ]
    )

    inputs = _select(facts)

    assert upfront_line(inputs, CostCategory.DEPOSIT) == AmountLine(
        CostCategory.DEPOSIT, Pence(115_000), Period.ONCE, ("DEP",)
    )
    assert upfront_line(inputs, CostCategory.FIRST_MONTH_RENT) == AmountLine(
        CostCategory.FIRST_MONTH_RENT, Pence(100_000), Period.ONCE, ("FMR",)
    )


# One test per error code.


@pytest.mark.parametrize(
    "category", ["asking-price", "mortgage-deposit", "mortgage-rate", "mortgage-term"]
)
def test_select_assumptions_buying_without_an_anchor_input_fails_as_missing(category: str) -> None:
    facts = buying_from(anchors_except(category))

    result = select_assumptions(facts, 1)

    assert result.is_failure
    assert result.error.code == f"input.missing.{category}"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_two_missing_anchors_report_the_first_one_checked() -> None:
    evidence = [
        item for item in buy_anchors() if item.category not in ("asking-price", "mortgage-deposit")
    ]

    assert _failure_code(buying_from(evidence)) == "input.missing.asking-price"


def test_select_assumptions_anchor_item_with_status_missing_fails_as_missing() -> None:
    gap = no_value("PRICE", "asking-price", EvidenceStatus.MISSING)

    facts = buying_from(anchors_except("asking-price", gap))

    assert _failure_code(facts) == "input.missing.asking-price"


def test_select_assumptions_renting_without_rent_fails_as_missing() -> None:
    assert _failure_code(renting([])) == "input.missing.rent"


def test_select_assumptions_anchor_from_two_items_fails_as_ambiguous() -> None:
    facts = buying([money("PRICE-2", "asking-price", 21_000_000, Period.ONCE)])

    result = select_assumptions(facts, 1)

    assert result.is_failure
    assert result.error.code == "input.ambiguous.asking-price"
    assert result.error.category == ErrorCategory.CONFLICT


def test_select_assumptions_rent_from_two_items_fails_as_ambiguous() -> None:
    facts = renting(
        [
            money("RENT-1", "rent", 100_000, Period.MONTH),
            money("RENT-2", "rent", 110_000, Period.MONTH),
        ]
    )

    assert _failure_code(facts) == "input.ambiguous.rent"


def test_select_assumptions_price_given_monthly_fails_as_wrong_period() -> None:
    price = money("PRICE", "asking-price", 20_000_000, Period.MONTH)

    result = select_assumptions(buying_from(anchors_except("asking-price", price)), 1)

    assert result.is_failure
    assert result.error.code == "input.wrong-period.asking-price"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_deposit_given_yearly_fails_as_wrong_period() -> None:
    deposit = money("DEPOSIT", "mortgage-deposit", 4_000_000, Period.YEAR)

    facts = buying_from(anchors_except("mortgage-deposit", deposit))

    assert _failure_code(facts) == "input.wrong-period.mortgage-deposit"


def test_select_assumptions_rent_given_yearly_fails_as_wrong_period() -> None:
    facts = renting([money("RENT", "rent", 1_200_000, Period.YEAR)])

    assert _failure_code(facts) == "input.wrong-period.rent"


def test_select_assumptions_rent_given_once_fails_as_wrong_period() -> None:
    facts = renting([money("RENT", "rent", 100_000, Period.ONCE)])

    assert _failure_code(facts) == "input.wrong-period.rent"


@pytest.mark.parametrize("pence", [0, -1])
def test_select_assumptions_rent_not_more_than_zero_fails_as_not_positive(pence: int) -> None:
    facts = renting([money("RENT", "rent", pence, Period.MONTH)])

    result = select_assumptions(facts, 1)

    assert result.is_failure
    assert result.error.code == "input.not-positive.rent"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_price_zero_fails_as_not_positive() -> None:
    price = money("PRICE", "asking-price", 0, Period.ONCE)

    facts = buying_from(anchors_except("asking-price", price))

    assert _failure_code(facts) == "input.not-positive.asking-price"


def test_select_assumptions_deposit_zero_fails_as_not_positive() -> None:
    deposit = money("DEPOSIT", "mortgage-deposit", 0, Period.ONCE)

    facts = buying_from(anchors_except("mortgage-deposit", deposit))

    assert _failure_code(facts) == "input.not-positive.mortgage-deposit"


def test_select_assumptions_price_in_the_wrong_period_and_zero_reports_the_period_first() -> None:
    price = money("PRICE", "asking-price", 0, Period.MONTH)

    facts = buying_from(anchors_except("asking-price", price))

    assert _failure_code(facts) == "input.wrong-period.asking-price"


def test_select_assumptions_rate_given_as_money_fails_as_wrong_kind() -> None:
    rate = money("RATE", "mortgage-rate", 500, Period.ONCE)

    result = select_assumptions(buying_from(anchors_except("mortgage-rate", rate)), 1)

    assert result.is_failure
    assert result.error.code == "input.wrong-kind.mortgage-rate"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_term_given_as_rate_fails_as_wrong_kind() -> None:
    term = _item("TERM", "mortgage-term", RateValue(500))

    facts = buying_from(anchors_except("mortgage-term", term))

    assert _failure_code(facts) == "input.wrong-kind.mortgage-term"


def test_select_assumptions_price_given_as_years_fails_as_wrong_kind() -> None:
    price = _item("PRICE", "asking-price", YearsValue(20))

    facts = buying_from(anchors_except("asking-price", price))

    assert _failure_code(facts) == "input.wrong-kind.asking-price"


def test_select_assumptions_deposit_given_as_a_rate_fails_as_wrong_kind() -> None:
    deposit = _item("DEPOSIT", "mortgage-deposit", RateValue(5))

    facts = buying_from(anchors_except("mortgage-deposit", deposit))

    assert _failure_code(facts) == "input.wrong-kind.mortgage-deposit"


def test_select_assumptions_service_charge_given_as_a_rate_fails_as_wrong_kind() -> None:
    facts = buying([_item("SC", "service-charge", RateValue(500))])

    assert _failure_code(facts) == "input.wrong-kind.service-charge"


def test_select_assumptions_upfront_cost_given_as_a_rate_fails_as_wrong_kind() -> None:
    facts = buying([_item("MC", "moving-costs", RateValue(500))])

    assert _failure_code(facts) == "input.wrong-kind.moving-costs"


def test_select_assumptions_line_with_an_other_value_fails_as_wrong_kind() -> None:
    facts = buying([other("EN", "energy", EvidenceStatus.AVAILABLE)])

    assert _failure_code(facts) == "input.wrong-kind.energy"


@pytest.mark.parametrize("nation", [Nation.WALES, Nation.SCOTLAND, Nation.NORTHERN_IRELAND])
def test_select_assumptions_home_outside_england_fails_as_not_covered(nation: Nation) -> None:
    result = select_assumptions(buying([], nation), 1)

    assert result.is_failure
    assert result.error.code == "home.not-covered"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_home_with_no_mode_fails_as_mode_missing() -> None:
    facts = HomeFacts("T1", None, Nation.ENGLAND, tuple(buy_anchors()), Pence(200_000))

    result = select_assumptions(facts, 1)

    assert result.is_failure
    assert result.error.code == "home.mode-missing"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_home_outside_england_with_no_mode_reports_the_nation_first() -> None:
    facts = HomeFacts("T1", None, Nation.WALES, tuple(buy_anchors()), Pence(200_000))

    assert _failure_code(facts) == "home.not-covered"


@pytest.mark.parametrize("step", [0, -3])
def test_select_assumptions_step_below_one_fails_as_out_of_range(step: int) -> None:
    result = select_assumptions(buying([]), step)

    assert result.is_failure
    assert result.error.code == "story.step-out-of-range"
    assert result.error.category == ErrorCategory.VALIDATION


def test_select_assumptions_step_below_one_is_reported_before_a_missing_anchor() -> None:
    facts = buying_from(anchors_except("asking-price"))

    assert _failure_code(facts, 0) == "story.step-out-of-range"


def test_select_assumptions_home_problem_is_reported_before_the_step() -> None:
    assert _failure_code(buying([], Nation.WALES), 0) == "home.not-covered"


def test_select_assumptions_step_one_is_accepted() -> None:
    assert _select(buying([]), 1).mode == Mode.BUY


def test_select_assumptions_non_facts_raises_type_error() -> None:
    with pytest.raises(TypeError, match="HomeFacts"):
        select_assumptions(None, 1)  # type: ignore[arg-type]  # deliberately wrong


def test_select_assumptions_evidence_that_is_not_a_tuple_raises_type_error() -> None:
    # The C# null evidence list throws; here the facts cannot even be built with a wrong list.
    with pytest.raises(TypeError, match="evidence"):
        HomeFacts("T1", Mode.BUY, Nation.ENGLAND, None, Pence(200_000))  # type: ignore[arg-type]  # deliberately wrong


@pytest.mark.parametrize("bad", ["1", 1.0, None, True])
def test_select_assumptions_step_that_is_not_an_int_raises_type_error(bad: Any) -> None:
    with pytest.raises(TypeError, match="step"):
        select_assumptions(buying([]), bad)


def test_select_assumptions_step_above_32_bits_raises_value_error() -> None:
    with pytest.raises(ValueError, match="32-bit"):
        select_assumptions(buying([]), 2**31)


def test_select_assumptions_step_at_the_32_bit_maximum_is_accepted() -> None:
    assert _select(buying([]), 2**31 - 1).mode == Mode.BUY


def test_select_assumptions_two_money_and_a_wrong_kind_item_fails_as_wrong_kind_for_a_line() -> (
    None
):
    facts = buying(
        [
            money("EN-1", "energy", 9_000, Period.MONTH),
            money("EN-2", "energy", 9_500, Period.MONTH),
            _item("EN-3", "energy", RateValue(500)),
        ]
    )

    assert _failure_code(facts) == "input.wrong-kind.energy"


def test_select_assumptions_two_money_and_a_wrong_kind_item_fails_as_wrong_kind_for_an_anchor() -> (
    None
):
    facts = buying(
        [
            money("PRICE-2", "asking-price", 21_000_000, Period.ONCE),
            _item("PRICE-3", "asking-price", RateValue(500)),
        ]
    )

    assert _failure_code(facts) == "input.wrong-kind.asking-price"
