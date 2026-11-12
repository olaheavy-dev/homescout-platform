"""Mortgage repayment against the independently worked cases, ported from the C# MortgageTests.

Standard repayment, monthly compounding, rounded once (OpenStax Contemporary Mathematics 6.8).
Inputs and expected values come from story-calculations.json, never from the engine.
"""

from typing import Any

import pytest
from engine_support import basis_points, case, case_ids_where
from vestagraph_engine import ErrorCategory, Pence
from vestagraph_engine.mortgage import MAX_TERM_YEARS, MortgageRepayment, monthly_repayment

MORTGAGE_CASE_IDS = case_ids_where("annualRate")


def _mortgage_inputs(case_id: str) -> tuple[Pence, int, int]:
    """Loan (direct, or asking price minus deposit: founder, 23 Oct 2026), rate and term."""
    inputs: dict[str, Any] = case(case_id)["inputs"]
    if "loanPence" in inputs:
        loan = inputs["loanPence"]
    else:
        loan = inputs["askingPricePence"] - inputs["depositPence"]
    return Pence(loan), basis_points(inputs["annualRate"]), inputs["termYears"]


def test_mortgage_cases_file_has_the_four_worked_mortgage_cases() -> None:
    assert len(MORTGAGE_CASE_IDS) == 4


@pytest.mark.parametrize("case_id", MORTGAGE_CASE_IDS)
def test_monthly_repayment_story_case_matches_worked_result(case_id: str) -> None:
    loan, rate, term = _mortgage_inputs(case_id)
    expected = case(case_id)["expected"]["monthlyRepaymentPence"]

    result = monthly_repayment(loan, rate, term)

    assert result.is_success
    repayment = result.value
    assert isinstance(repayment, MortgageRepayment)
    assert repayment.monthly_repayment == Pence(expected)
    assert repayment.loan == loan
    assert repayment.rate_basis_points == rate
    assert repayment.term_years == term
    assert repayment.payments == term * 12


def test_basis_points_rate_that_is_not_whole_basis_points_fails_the_test() -> None:
    with pytest.raises(AssertionError):
        basis_points("0.05505")


def test_basis_points_whole_rate_reads_as_basis_points() -> None:
    assert basis_points("0.055") == 550


@pytest.mark.parametrize(
    ("loan", "rate", "term", "code"),
    [
        (0, 550, 25, "mortgage.loan-not-positive"),
        (-1, 550, 25, "mortgage.loan-not-positive"),
        (1_000_000, 0, 25, "mortgage.rate-not-positive"),
        (1_000_000, -5, 25, "mortgage.rate-not-positive"),
        (1_000_000, 550, 0, "mortgage.term-not-positive"),
        (1_000_000, 550, -1, "mortgage.term-not-positive"),
    ],
)
def test_monthly_repayment_invalid_input_fails_with_the_code(
    loan: int, rate: int, term: int, code: str
) -> None:
    result = monthly_repayment(Pence(loan), rate, term)

    assert result.is_failure
    assert result.error.code == code
    assert result.error.category == ErrorCategory.VALIDATION


@pytest.mark.parametrize("term", [101, 50_000, 2**31 - 1])
def test_monthly_repayment_term_over_100_years_fails_as_too_long(term: int) -> None:
    # 100 years is a computation limit (register line BE-17), not a lending rule.
    result = monthly_repayment(Pence(1_000_000), 550, term)

    assert result.error.code == "mortgage.term-too-long"
    assert result.error.category == ErrorCategory.VALIDATION


def test_monthly_repayment_term_of_100_years_is_calculated() -> None:
    assert MAX_TERM_YEARS == 100
    assert monthly_repayment(Pence(1_000_000), 550, 100).is_success


@pytest.mark.parametrize("loan", [5_000_000_000_000_000, (2**63 - 1) // 1000, (2**63 - 1) // 100])
def test_monthly_repayment_very_large_loan_never_gives_a_wrong_success(loan: int) -> None:
    # Independent bounds, not an engine figure. At 2,000 basis points the monthly rate is
    # i = 2000 / 120,000 = 1/60. Interest alone each month is loan / 60, and the repayment is more
    # than that and less than the whole loan (the first payment of a 25-year loan is a fraction of
    # the loan). Only whole-number comparisons: 60 x repayment > loan, repayment < loan.
    try:
        result = monthly_repayment(Pence(loan), 2000, 25)
    except OverflowError:
        return  # throwing is allowed; a wrong success is not
    assert result.is_success
    repayment = result.value.monthly_repayment.value
    assert 60 * repayment > loan
    assert repayment < loan


@pytest.mark.parametrize(
    ("loan", "rate", "term"),
    [(True, 550, 25), (1_000_000, True, 25), (1_000_000, 550, True), (1_000_000, 550.0, 25)],
)
def test_monthly_repayment_non_int_argument_raises_type_error(
    loan: object, rate: object, term: object
) -> None:
    with pytest.raises(TypeError):
        monthly_repayment(
            Pence(loan) if type(loan) is int else loan,  # type: ignore[arg-type]  # deliberately wrong
            rate,  # type: ignore[arg-type]  # deliberately wrong types
            term,  # type: ignore[arg-type]  # deliberately wrong types
        )
