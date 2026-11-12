"""Upfront cash against the independently worked cases, ported from the C# UpfrontCashTests.

Stamp duty and legal fees are not calculated in this version: they stay flagged and never become
zero. Every input and expected value is read from story-calculations.json or is a hand-worked
literal.
"""

from typing import Any

import pytest
from engine_support import case, case_ids_where, category_from_id, lines_of, mode_of
from vestagraph_engine import ErrorCategory, Pence
from vestagraph_engine.breakdowns import LineResult, PartialReason
from vestagraph_engine.cost_categories import category_id, status_id
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode, Period
from vestagraph_engine.line_input import (
    AmountLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.upfront_cash import upfront_cash

ANY_EVIDENCE = ("EVIDENCE-1",)

RENT_ORDER = [CostCategory.DEPOSIT, CostCategory.FIRST_MONTH_RENT, CostCategory.MOVING_COSTS]
BUY_ORDER = [
    CostCategory.MORTGAGE_DEPOSIT,
    CostCategory.MOVING_COSTS,
    CostCategory.STAMP_DUTY,
    CostCategory.LEGAL_FEES,
]

# The upfront cases are those with a list of lines and no budget.
UPFRONT_CASE_IDS = [
    c_id for c_id in case_ids_where("lines") if c_id not in case_ids_where("budgetPence")
]


def _once(category: CostCategory, pence: int) -> AmountLine:
    return AmountLine(category, Pence(pence), Period.ONCE, ANY_EVIDENCE)


def test_upfront_cases_file_has_the_four_worked_upfront_cases() -> None:
    assert len(UPFRONT_CASE_IDS) == 4


@pytest.mark.parametrize("case_id", UPFRONT_CASE_IDS)
def test_upfront_cash_story_case_matches_worked_result(case_id: str) -> None:
    story_case = case(case_id)
    expected = story_case["expected"]

    result = upfront_cash(mode_of(story_case), lines_of(story_case))

    assert result.is_success
    actual = result.value
    assert actual.total == Pence(expected["totalUpfrontPence"])
    assert actual.is_partial == expected["totalIsPartial"]

    _assert_lines_match(actual.lines, expected["lines"])
    _assert_partial_reasons_match(actual.partial_reasons, expected["partialReasons"])


def _assert_lines_match(actual: tuple[LineResult, ...], expected: list[dict[str, Any]]) -> None:
    assert len(actual) == len(expected)
    for expected_line in expected:
        category = category_from_id(expected_line["category"])
        (line,) = [candidate for candidate in actual if candidate.category == category]

        if "amountPence" in expected_line:
            assert line.status == LineStatus.CALCULATED, category
            assert line.amount == Pence(expected_line["amountPence"]), category
            assert line.source_period == Period.ONCE, category
        else:
            assert line.amount is None, category
            assert line.source_period is None, category
            assert status_id(line.status) == expected_line["status"], category
        # The case lines carry no evidence, so none comes back.
        assert line.evidence_ids == (), category


def _assert_partial_reasons_match(actual: tuple[PartialReason, ...], expected: list[str]) -> None:
    # The cases give each reason as prose that starts with the category ("stamp-duty: not
    # calculated in this version"); only the category before the colon is compared.
    expected_categories = sorted(reason.split(":")[0] for reason in expected)
    assert sorted(category_id(reason.category) for reason in actual) == expected_categories
    # Every reason in the upfront cases is "not calculated" (or there are none).
    assert all(reason.status == LineStatus.NOT_CALCULATED for reason in actual)


def test_upfront_cash_lines_given_out_of_order_come_back_in_the_fixed_buy_order() -> None:
    lines: list[LineInput] = [
        NotCalculatedLine(CostCategory.LEGAL_FEES, ANY_EVIDENCE),
        NotCalculatedLine(CostCategory.STAMP_DUTY, ANY_EVIDENCE),
        _once(CostCategory.MOVING_COSTS, 120_000),
        _once(CostCategory.MORTGAGE_DEPOSIT, 3_000_000),
    ]

    result = upfront_cash(Mode.BUY, lines).value

    assert [line.category for line in result.lines] == BUY_ORDER


def test_upfront_cash_lines_given_out_of_order_come_back_in_the_fixed_rent_order() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.MOVING_COSTS, 120_000),
        _once(CostCategory.FIRST_MONTH_RENT, 120_000),
        _once(CostCategory.DEPOSIT, 138_000),
    ]

    result = upfront_cash(Mode.RENT, lines).value

    assert [line.category for line in result.lines] == RENT_ORDER


def test_upfront_cash_stamp_duty_and_legal_fees_stay_not_calculated_with_no_amount() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.MORTGAGE_DEPOSIT, 3_000_000),
        NotCalculatedLine(CostCategory.STAMP_DUTY, ANY_EVIDENCE),
        NotCalculatedLine(CostCategory.LEGAL_FEES, ANY_EVIDENCE),
    ]

    result = upfront_cash(Mode.BUY, lines).value

    flagged = [
        line
        for line in result.lines
        if line.category in (CostCategory.STAMP_DUTY, CostCategory.LEGAL_FEES)
    ]
    assert len(flagged) == 2
    assert all(line.amount is None for line in flagged)
    assert result.total == Pence(3_000_000)
    assert result.is_partial
    assert all(reason.status == LineStatus.NOT_CALCULATED for reason in result.partial_reasons)
    assert [reason.category for reason in result.partial_reasons] == [
        CostCategory.STAMP_DUTY,
        CostCategory.LEGAL_FEES,
    ]


def test_upfront_cash_missing_moving_costs_makes_the_total_partial() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.MORTGAGE_DEPOSIT, 3_000_000),
        MissingLine(CostCategory.MOVING_COSTS),
    ]

    result = upfront_cash(Mode.BUY, lines).value

    assert result.is_partial
    assert result.partial_reasons == (PartialReason(CostCategory.MOVING_COSTS, LineStatus.MISSING),)


def test_upfront_cash_calculated_line_keeps_its_evidence_and_once_period() -> None:
    lines: list[LineInput] = [
        AmountLine(CostCategory.DEPOSIT, Pence(138_000), Period.ONCE, ("D-1", "D-2")),
    ]

    (line,) = upfront_cash(Mode.RENT, lines).value.lines

    assert line.status == LineStatus.CALCULATED
    assert line.amount == Pence(138_000)
    assert line.source_period == Period.ONCE
    assert line.evidence_ids == ("D-1", "D-2")


def test_upfront_cash_buying_with_no_lines_fails_as_missing_mortgage_deposit() -> None:
    result = upfront_cash(Mode.BUY, [])

    assert result.is_failure
    assert result.error.code == "input.missing.mortgage-deposit"
    assert result.error.category == ErrorCategory.VALIDATION


def test_upfront_cash_buying_with_mortgage_deposit_missing_fails_as_missing_mortgage_deposit() -> (
    None
):
    lines: list[LineInput] = [
        MissingLine(CostCategory.MORTGAGE_DEPOSIT),
        _once(CostCategory.MOVING_COSTS, 120_000),
    ]

    assert upfront_cash(Mode.BUY, lines).error.code == "input.missing.mortgage-deposit"


def test_upfront_cash_renting_with_no_lines_has_no_lines_and_a_total_of_zero_not_partial() -> None:
    # Renting has no required upfront input (register line BE-16 names only rent as a renter's
    # anchor, and that is a monthly figure).
    result = upfront_cash(Mode.RENT, []).value

    assert result.lines == ()
    assert result.total == Pence.ZERO
    assert not result.is_partial
    assert result.partial_reasons == ()


def test_upfront_cash_amount_given_monthly_fails_as_wrong_period() -> None:
    lines: list[LineInput] = [
        AmountLine(CostCategory.DEPOSIT, Pence(138_000), Period.MONTH, ANY_EVIDENCE)
    ]

    result = upfront_cash(Mode.RENT, lines)

    assert result.error.code == "input.wrong-period.deposit"
    assert result.error.category == ErrorCategory.VALIDATION


def test_upfront_cash_amount_given_yearly_fails_as_wrong_period() -> None:
    lines: list[LineInput] = [
        AmountLine(CostCategory.DEPOSIT, Pence(138_000), Period.YEAR, ANY_EVIDENCE)
    ]

    assert upfront_cash(Mode.RENT, lines).error.code == "input.wrong-period.deposit"


@pytest.mark.parametrize("pence", [0, -1])
def test_upfront_cash_amount_not_positive_fails_as_not_positive(pence: int) -> None:
    result = upfront_cash(Mode.RENT, [_once(CostCategory.MOVING_COSTS, pence)])

    assert result.error.code == "input.not-positive.moving-costs"
    assert result.error.category == ErrorCategory.VALIDATION


def test_upfront_cash_same_category_twice_fails_as_ambiguous() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.DEPOSIT, 138_000),
        _once(CostCategory.DEPOSIT, 140_000),
    ]

    result = upfront_cash(Mode.RENT, lines)

    assert result.error.code == "input.ambiguous.deposit"
    assert result.error.category == ErrorCategory.CONFLICT


def test_upfront_cash_line_that_does_not_belong_to_the_mode_fails_as_not_for_mode() -> None:
    result = upfront_cash(Mode.RENT, [_once(CostCategory.STAMP_DUTY, 1_000)])

    assert result.error.code == "input.not-for-mode.stamp-duty"
    assert result.error.category == ErrorCategory.VALIDATION


def test_upfront_cash_monthly_category_in_an_upfront_list_fails_as_not_for_mode() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.MORTGAGE_DEPOSIT, 3_000_000),
        _once(CostCategory.ENERGY, 8_000),
    ]

    assert upfront_cash(Mode.BUY, lines).error.code == "input.not-for-mode.energy"


def test_upfront_cash_first_problem_in_input_order_is_the_failure() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.MOVING_COSTS, 0),
        AmountLine(CostCategory.DEPOSIT, Pence(138_000), Period.MONTH, ANY_EVIDENCE),
    ]

    assert upfront_cash(Mode.RENT, lines).error.code == "input.not-positive.moving-costs"


def test_upfront_cash_non_sequence_lines_raises_type_error() -> None:
    with pytest.raises(TypeError):
        upfront_cash(Mode.RENT, None)  # type: ignore[arg-type]  # deliberately wrong


def test_upfront_cash_text_as_lines_raises_type_error() -> None:
    with pytest.raises(TypeError):
        upfront_cash(Mode.RENT, "deposit")  # type: ignore[arg-type]  # deliberately wrong


def test_upfront_cash_none_in_the_list_of_lines_raises_type_error() -> None:
    with pytest.raises(TypeError):
        upfront_cash(Mode.RENT, [_once(CostCategory.DEPOSIT, 1), None])  # type: ignore[list-item]  # deliberately wrong


def test_upfront_cash_undefined_mode_raises_type_error() -> None:
    with pytest.raises(TypeError):
        upfront_cash(99, [])  # type: ignore[arg-type]  # deliberately wrong


def test_upfront_cash_total_too_big_for_64_bits_raises_overflow() -> None:
    lines: list[LineInput] = [
        _once(CostCategory.DEPOSIT, 2**63 - 1),
        _once(CostCategory.MOVING_COSTS, 1),
    ]

    with pytest.raises(OverflowError):
        upfront_cash(Mode.RENT, lines)
