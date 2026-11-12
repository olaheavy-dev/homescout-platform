"""Monthly cost against the independently worked cases, ported from the C# MonthlyCostTests.

Every input and expected value is read from story-calculations.json or is a hand-worked literal
that says how it was worked. Lines are compared by category (the file's line order is not the
engine's fixed order).
"""

from typing import Any

import pytest
from engine_support import budget_of, case, case_ids_where, category_from_id, lines_of, mode_of
from vestagraph_engine import ErrorCategory, Pence
from vestagraph_engine.breakdowns import LineResult, PartialReason
from vestagraph_engine.cost_categories import category_id, status_id
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode, Period
from vestagraph_engine.line_input import (
    AmountLine,
    ConflictingLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.monthly_cost import monthly_cost

ANY_EVIDENCE = ("EVIDENCE-1",)
COUNCIL_TAX_EVIDENCE = ("CT-1", "CT-2")
BUDGET_160000 = Pence(160_000)

RENT_ORDER = [
    CostCategory.RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
]
BUY_ORDER = [
    CostCategory.MORTGAGE_REPAYMENT,
    CostCategory.SERVICE_CHARGE,
    CostCategory.GROUND_RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
    CostCategory.BUILDINGS_INSURANCE,
    CostCategory.MAINTENANCE,
]

# The monthly cases are those with a budget and a list of lines.
MONTHLY_CASE_IDS = [
    c_id for c_id in case_ids_where("lines") if c_id in case_ids_where("budgetPence")
]


def _rent(pence: int) -> AmountLine:
    return AmountLine(CostCategory.RENT, Pence(pence), Period.MONTH, ANY_EVIDENCE)


def _amount(category: CostCategory, pence: int, period: Period) -> AmountLine:
    return AmountLine(category, Pence(pence), period, ANY_EVIDENCE)


def test_monthly_cases_file_has_the_seven_worked_monthly_cases() -> None:
    assert len(MONTHLY_CASE_IDS) == 7


@pytest.mark.parametrize("case_id", MONTHLY_CASE_IDS)
def test_monthly_cost_story_case_matches_worked_result(case_id: str) -> None:
    story_case = case(case_id)
    expected = story_case["expected"]

    result = monthly_cost(mode_of(story_case), lines_of(story_case), budget_of(story_case))

    assert result.is_success
    actual = result.value
    assert actual.total == Pence(expected["totalMonthlyPence"])
    assert actual.is_partial == expected["totalIsPartial"]
    assert actual.budget == Pence(expected["budgetPence"])
    assert actual.budget_difference == Pence(expected["budgetDifferencePence"])
    assert actual.within_budget == expected["withinBudget"]
    assert actual.based_on_partial_total == actual.is_partial

    _assert_lines_match(actual.lines, expected["lines"])
    _assert_partial_reasons_match(actual.partial_reasons, expected["partialReasons"])


def _assert_lines_match(actual: tuple[LineResult, ...], expected: list[dict[str, Any]]) -> None:
    assert len(actual) == len(expected)
    for expected_line in expected:
        category = category_from_id(expected_line["category"])
        (line,) = [candidate for candidate in actual if candidate.category == category]

        if "monthlyPence" in expected_line:
            assert line.status == LineStatus.CALCULATED, category
            assert line.amount == Pence(expected_line["monthlyPence"]), category
        else:
            assert line.amount is None, category
            assert status_id(line.status) == expected_line["status"], category


def _assert_partial_reasons_match(actual: tuple[PartialReason, ...], expected: list[str]) -> None:
    # The worked cases give each reason as prose that starts with the category ("water: not
    # settled yet"). The engine gives codes instead, so only the category before the colon is
    # compared (plan 4b, known risk 4).
    expected_categories = sorted(reason.split(":")[0] for reason in expected)
    assert sorted(category_id(reason.category) for reason in actual) == expected_categories


def test_monthly_cost_total_exactly_equal_to_budget_is_within_budget() -> None:
    # 1,600 pounds is within budget (founder, 23 Oct 2026): 160,000p a month against 160,000p.
    result = monthly_cost(Mode.RENT, [_rent(160_000)], BUDGET_160000).value

    assert result.total == Pence(160_000)
    assert result.budget_difference == Pence.ZERO
    assert result.within_budget


def test_monthly_cost_total_one_penny_over_budget_is_not_within_budget() -> None:
    result = monthly_cost(Mode.RENT, [_rent(160_001)], BUDGET_160000).value

    assert result.budget_difference == Pence(-1)
    assert not result.within_budget


def test_monthly_cost_lines_given_out_of_order_come_back_in_the_fixed_rent_order() -> None:
    lines: list[LineInput] = [
        _amount(CostCategory.BROADBAND, 3_000, Period.MONTH),
        IncludedLine(CostCategory.WATER, ANY_EVIDENCE),
        _amount(CostCategory.ENERGY, 8_000, Period.MONTH),
        _amount(CostCategory.COUNCIL_TAX, 160_000, Period.YEAR),
        _rent(120_000),
    ]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    assert [line.category for line in result.lines] == RENT_ORDER


def test_monthly_cost_lines_given_out_of_order_come_back_in_the_fixed_buy_order() -> None:
    lines: list[LineInput] = [
        NotCalculatedLine(CostCategory.MAINTENANCE, ANY_EVIDENCE),
        _amount(CostCategory.WATER, 4_500, Period.MONTH),
        IncludedLine(CostCategory.BUILDINGS_INSURANCE, ANY_EVIDENCE),
        _amount(CostCategory.GROUND_RENT, 25_000, Period.YEAR),
        _amount(CostCategory.MORTGAGE_REPAYMENT, 98_254, Period.MONTH),
        _amount(CostCategory.SERVICE_CHARGE, 240_000, Period.YEAR),
        _amount(CostCategory.ENERGY, 8_500, Period.MONTH),
        _amount(CostCategory.BROADBAND, 3_000, Period.MONTH),
        _amount(CostCategory.COUNCIL_TAX, 210_000, Period.YEAR),
    ]

    result = monthly_cost(Mode.BUY, lines, BUDGET_160000).value

    assert [line.category for line in result.lines] == BUY_ORDER


def test_monthly_cost_a_line_the_home_does_not_have_is_left_out_never_zero() -> None:
    # Register line BE-13: only the rent was given, so only the rent comes back.
    result = monthly_cost(Mode.RENT, [_rent(120_000)], BUDGET_160000).value

    assert [line.category for line in result.lines] == [CostCategory.RENT]


def test_monthly_cost_yearly_line_keeps_its_source_period_and_evidence() -> None:
    lines: list[LineInput] = [
        _rent(120_000),
        AmountLine(CostCategory.COUNCIL_TAX, Pence(160_000), Period.YEAR, COUNCIL_TAX_EVIDENCE),
    ]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    (council_tax,) = [line for line in result.lines if line.category == CostCategory.COUNCIL_TAX]
    # 160,000 a year / 12 = 13,333.33, which rounds to 13,333.
    assert council_tax.amount == Pence(13_333)
    assert council_tax.source_period == Period.YEAR
    assert council_tax.evidence_ids == COUNCIL_TAX_EVIDENCE


def test_monthly_cost_non_calculated_lines_have_no_amount_and_no_source_period() -> None:
    lines: list[LineInput] = [
        _rent(120_000),
        IncludedLine(CostCategory.WATER, ANY_EVIDENCE),
        NotCalculatedLine(CostCategory.ENERGY, ANY_EVIDENCE),
        ConflictingLine(CostCategory.BROADBAND, ANY_EVIDENCE),
        MissingLine(CostCategory.COUNCIL_TAX),
    ]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    others = [line for line in result.lines if line.category != CostCategory.RENT]
    assert len(others) == 4
    assert all(line.amount is None for line in others)
    assert all(line.source_period is None for line in others)
    assert result.total == Pence(120_000)
    # The evidence behind a line with no amount is carried through untouched.
    evidence = {line.category: line.evidence_ids for line in others}
    assert evidence == {
        CostCategory.WATER: ANY_EVIDENCE,
        CostCategory.ENERGY: ANY_EVIDENCE,
        CostCategory.BROADBAND: ANY_EVIDENCE,
        CostCategory.COUNCIL_TAX: (),
    }


def test_monthly_cost_monthly_line_keeps_month_as_its_source_period_and_its_evidence() -> None:
    result = monthly_cost(Mode.RENT, [_rent(120_000)], BUDGET_160000).value

    (rent,) = result.lines
    assert rent.status == LineStatus.CALCULATED
    assert rent.source_period == Period.MONTH
    assert rent.evidence_ids == ANY_EVIDENCE


def test_monthly_cost_partial_reasons_name_each_line_without_an_amount_and_its_status() -> None:
    lines: list[LineInput] = [
        _rent(120_000),
        IncludedLine(CostCategory.WATER, ANY_EVIDENCE),
        NotCalculatedLine(CostCategory.ENERGY, ANY_EVIDENCE),
        ConflictingLine(CostCategory.BROADBAND, ANY_EVIDENCE),
        MissingLine(CostCategory.COUNCIL_TAX),
    ]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    # Fixed rent order: council tax, energy, water (included: no reason), broadband.
    assert result.partial_reasons == (
        PartialReason(CostCategory.COUNCIL_TAX, LineStatus.MISSING),
        PartialReason(CostCategory.ENERGY, LineStatus.NOT_CALCULATED),
        PartialReason(CostCategory.BROADBAND, LineStatus.CONFLICTING),
    )


def test_monthly_cost_missing_line_makes_the_total_partial_with_a_coded_reason() -> None:
    lines: list[LineInput] = [_rent(120_000), MissingLine(CostCategory.WATER)]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    assert result.is_partial
    assert result.partial_reasons == (PartialReason(CostCategory.WATER, LineStatus.MISSING),)


def test_monthly_cost_included_line_does_not_make_the_total_partial() -> None:
    lines: list[LineInput] = [_rent(120_000), IncludedLine(CostCategory.WATER, ANY_EVIDENCE)]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    assert not result.is_partial
    assert result.partial_reasons == ()


def test_monthly_cost_tiny_yearly_amount_rounds_to_zero_but_stays_calculated() -> None:
    # 5p a year is 0.41667p a month, which rounds to 0p (rounding-boundaries.json).
    # A calculated 0p is not the same as missing.
    lines: list[LineInput] = [_rent(120_000), _amount(CostCategory.COUNCIL_TAX, 5, Period.YEAR)]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000).value

    (council_tax,) = [line for line in result.lines if line.category == CostCategory.COUNCIL_TAX]
    assert council_tax.amount == Pence.ZERO
    assert council_tax.status == LineStatus.CALCULATED


def test_monthly_cost_monthly_difference_is_the_difference_of_the_rounded_monthly_lines() -> None:
    # Register line BE-14. 5p a year is 0.4167p a month (rounds to 0p); 7p a year is 0.5833p a
    # month (rounds to 1p). The difference of the rounded lines is 1p. Rounding the yearly
    # difference (2p / 12 = 0.1667p) would give 0p, which is not what the screen shows.
    low = monthly_cost(
        Mode.RENT,
        [_rent(120_000), _amount(CostCategory.COUNCIL_TAX, 5, Period.YEAR)],
        BUDGET_160000,
    ).value
    high = monthly_cost(
        Mode.RENT,
        [_rent(120_000), _amount(CostCategory.COUNCIL_TAX, 7, Period.YEAR)],
        BUDGET_160000,
    ).value

    assert high.total - low.total == Pence(1)


def test_service_charge_difference_case_matches_the_difference_of_the_two_monthly_lines() -> None:
    # Worked case b1-service-charge-difference: the 2026 budget minus the listing claim. Both
    # monthly lines come from the monthly engine, and the difference is the difference of the
    # two rounded lines (register line BE-14).
    worked = case("b1-service-charge-difference")
    listing_case = case("b1-monthly-housing-cost-listing-service-charge")
    budget_case = case("b1-monthly-housing-cost-2026-budget")

    def service_charge_line(story_case: dict[str, Any]) -> LineResult:
        result = monthly_cost(
            mode_of(story_case), lines_of(story_case), budget_of(story_case)
        ).value
        (line,) = [x for x in result.lines if x.category == CostCategory.SERVICE_CHARGE]
        return line

    on_listing = service_charge_line(listing_case)
    on_budget = service_charge_line(budget_case)

    assert on_listing.amount is not None
    assert on_budget.amount is not None

    # The two monthly cases use the same yearly service charges as the difference case.
    def service_charge_input(story_case: dict[str, Any]) -> int:
        (line,) = [x for x in story_case["inputs"]["lines"] if x["category"] == "service-charge"]
        assert line["period"] == "year"
        amount: int = line["amountPence"]
        return amount

    assert service_charge_input(listing_case) == worked["inputs"]["listingServiceChargeAnnualPence"]
    assert service_charge_input(budget_case) == worked["inputs"]["budgetServiceChargeAnnualPence"]
    assert on_budget.amount - on_listing.amount == Pence(
        worked["expected"]["monthlyDifferencePence"]
    )


@pytest.mark.parametrize(
    ("mode", "code"),
    [(Mode.RENT, "input.missing.rent"), (Mode.BUY, "input.missing.mortgage-repayment")],
)
def test_monthly_cost_no_anchor_line_fails_as_missing(mode: Mode, code: str) -> None:
    lines: list[LineInput] = [_amount(CostCategory.ENERGY, 8_000, Period.MONTH)]

    result = monthly_cost(mode, lines, BUDGET_160000)

    assert result.is_failure
    assert result.error.code == code
    assert result.error.category == ErrorCategory.VALIDATION


def test_monthly_cost_anchor_line_that_is_not_an_amount_fails_as_missing() -> None:
    result = monthly_cost(
        Mode.RENT, [ConflictingLine(CostCategory.RENT, ANY_EVIDENCE)], BUDGET_160000
    )

    assert result.error.code == "input.missing.rent"


def test_monthly_cost_rent_given_yearly_fails_as_wrong_period() -> None:
    result = monthly_cost(
        Mode.RENT, [_amount(CostCategory.RENT, 1_440_000, Period.YEAR)], BUDGET_160000
    )

    assert result.error.code == "input.wrong-period.rent"
    assert result.error.category == ErrorCategory.VALIDATION


def test_monthly_cost_mortgage_repayment_given_yearly_fails_as_wrong_period() -> None:
    lines: list[LineInput] = [_amount(CostCategory.MORTGAGE_REPAYMENT, 1_179_048, Period.YEAR)]

    result = monthly_cost(Mode.BUY, lines, BUDGET_160000)

    assert result.error.code == "input.wrong-period.mortgage-repayment"


def test_monthly_cost_bill_given_once_fails_as_wrong_period() -> None:
    lines: list[LineInput] = [_rent(120_000), _amount(CostCategory.ENERGY, 8_000, Period.ONCE)]

    assert monthly_cost(Mode.RENT, lines, BUDGET_160000).error.code == "input.wrong-period.energy"


@pytest.mark.parametrize("pence", [0, -1])
def test_monthly_cost_amount_not_positive_fails_as_not_positive(pence: int) -> None:
    lines: list[LineInput] = [_rent(120_000), _amount(CostCategory.ENERGY, pence, Period.MONTH)]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000)

    assert result.error.code == "input.not-positive.energy"
    assert result.error.category == ErrorCategory.VALIDATION


def test_monthly_cost_budget_not_positive_fails_as_not_positive() -> None:
    result = monthly_cost(Mode.RENT, [_rent(120_000)], Pence.ZERO)

    assert result.error.code == "input.not-positive.budget"
    assert result.error.category == ErrorCategory.VALIDATION


def test_monthly_cost_same_category_twice_fails_as_ambiguous() -> None:
    result = monthly_cost(Mode.RENT, [_rent(120_000), _rent(130_000)], BUDGET_160000)

    assert result.error.code == "input.ambiguous.rent"
    assert result.error.category == ErrorCategory.CONFLICT


def test_monthly_cost_line_that_does_not_belong_to_the_mode_fails_as_not_for_mode() -> None:
    lines: list[LineInput] = [
        _rent(120_000),
        _amount(CostCategory.SERVICE_CHARGE, 240_000, Period.YEAR),
    ]

    result = monthly_cost(Mode.RENT, lines, BUDGET_160000)

    assert result.error.code == "input.not-for-mode.service-charge"
    assert result.error.category == ErrorCategory.VALIDATION


def test_monthly_cost_upfront_category_in_a_monthly_list_fails_as_not_for_mode() -> None:
    lines: list[LineInput] = [_rent(120_000), _amount(CostCategory.DEPOSIT, 138_000, Period.ONCE)]

    assert monthly_cost(Mode.RENT, lines, BUDGET_160000).error.code == "input.not-for-mode.deposit"


def test_monthly_cost_first_problem_in_input_order_is_the_failure() -> None:
    # Resolution stops at the first problem found, in input order (C# CostLines.Resolve).
    lines: list[LineInput] = [
        _amount(CostCategory.ENERGY, 0, Period.MONTH),
        _amount(CostCategory.WATER, 8_000, Period.ONCE),
    ]

    assert monthly_cost(Mode.RENT, lines, BUDGET_160000).error.code == "input.not-positive.energy"


def test_monthly_cost_non_sequence_lines_raises_type_error() -> None:
    with pytest.raises(TypeError):
        monthly_cost(Mode.RENT, None, BUDGET_160000)  # type: ignore[arg-type]  # deliberately wrong


def test_monthly_cost_none_in_the_list_of_lines_raises_type_error() -> None:
    with pytest.raises(TypeError):
        monthly_cost(Mode.RENT, [_rent(120_000), None], BUDGET_160000)  # type: ignore[list-item]  # deliberately wrong


def test_monthly_cost_undefined_mode_raises_type_error() -> None:
    with pytest.raises(TypeError):
        monthly_cost(99, [_rent(120_000)], BUDGET_160000)  # type: ignore[arg-type]  # deliberately wrong


def test_monthly_cost_non_pence_budget_raises_type_error() -> None:
    with pytest.raises(TypeError):
        monthly_cost(Mode.RENT, [_rent(120_000)], 160_000)  # type: ignore[arg-type]  # deliberately wrong


def test_monthly_cost_total_too_big_for_64_bits_raises_overflow() -> None:
    lines: list[LineInput] = [
        _rent(2**63 - 1),
        _amount(CostCategory.ENERGY, 1, Period.MONTH),
    ]

    with pytest.raises(OverflowError):
        monthly_cost(Mode.RENT, lines, BUDGET_160000)


def test_monthly_cost_unknown_kind_of_line_raises_type_error() -> None:
    class UnknownLine:
        category = CostCategory.RENT

    with pytest.raises(TypeError):
        monthly_cost(Mode.RENT, [UnknownLine()], BUDGET_160000)  # type: ignore[list-item]  # deliberately wrong


def test_cost_categories_undefined_values_raise_type_error() -> None:
    with pytest.raises(TypeError):
        category_id(999)  # type: ignore[arg-type]  # deliberately wrong
    with pytest.raises(TypeError):
        status_id(999)  # type: ignore[arg-type]  # deliberately wrong


def test_cost_categories_missing_status_is_named_missing() -> None:
    assert status_id(LineStatus.MISSING) == "missing"


@pytest.mark.parametrize(
    ("category", "expected"),
    [
        (CostCategory.MORTGAGE_REPAYMENT, "mortgage-repayment"),
        (CostCategory.SERVICE_CHARGE, "service-charge"),
        (CostCategory.GROUND_RENT, "ground-rent"),
        (CostCategory.COUNCIL_TAX, "council-tax"),
        (CostCategory.ENERGY, "energy"),
        (CostCategory.WATER, "water"),
        (CostCategory.BROADBAND, "broadband"),
        (CostCategory.BUILDINGS_INSURANCE, "buildings-insurance"),
        (CostCategory.MAINTENANCE, "maintenance"),
        (CostCategory.RENT, "rent"),
        (CostCategory.MORTGAGE_DEPOSIT, "mortgage-deposit"),
        (CostCategory.DEPOSIT, "deposit"),
        (CostCategory.FIRST_MONTH_RENT, "first-month-rent"),
        (CostCategory.MOVING_COSTS, "moving-costs"),
        (CostCategory.STAMP_DUTY, "stamp-duty"),
        (CostCategory.LEGAL_FEES, "legal-fees"),
    ],
)
def test_cost_categories_each_category_has_its_fixture_name(
    category: CostCategory, expected: str
) -> None:
    # The names are the hyphenated ones used in the fixture data and error codes.
    assert category_id(category) == expected


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (LineStatus.CALCULATED, "calculated"),
        (LineStatus.INCLUDED, "included"),
        (LineStatus.NOT_CALCULATED, "not-calculated"),
        (LineStatus.CONFLICTING, "conflicting"),
        (LineStatus.MISSING, "missing"),
    ],
)
def test_cost_categories_each_status_has_its_fixture_name(
    status: LineStatus, expected: str
) -> None:
    assert status_id(status) == expected
