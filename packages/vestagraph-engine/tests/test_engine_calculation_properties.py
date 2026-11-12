"""Property tests for the mortgage and monthly cost, ported from the C# CalculationProperties.

FsCheck becomes Hypothesis. Pence amounts are bounded to 1..10^10 so that sums cannot overflow
(overflow has its own unit tests). Oracles are written here in plain whole-number arithmetic and
never call the function under test.
"""

from dataclasses import dataclass

from hypothesis import given
from hypothesis import strategies as st
from vestagraph_engine import Pence
from vestagraph_engine.breakdowns import MonthlyBreakdown
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
from vestagraph_engine.mortgage import monthly_repayment

_MAX_PENCE = 10_000_000_000
EVIDENCE = ("EVIDENCE-1",)

PENNIES = st.one_of(
    st.integers(1, 1_000),
    st.integers(1, 2**31 - 1),
    st.sampled_from([1, _MAX_PENCE]),
)
RATES = st.one_of(st.integers(1, 3_000), st.sampled_from([1, 550, 3_000]))
TERMS = st.integers(1, 40)

_BUY_MONTHLY = [
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
_RENT_MONTHLY = [
    CostCategory.RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
]


@dataclass(frozen=True)
class MonthlyScenario:
    """Monthly lines for one mode; the anchor line always has an amount."""

    mode: Mode
    lines: list[LineInput]
    budget: Pence


@st.composite
def _line(draw: st.DrawFn, category: CostCategory, *, force_amount: bool) -> LineInput:
    month_only = category in (CostCategory.RENT, CostCategory.MORTGAGE_REPAYMENT)
    period = Period.MONTH if month_only else draw(st.sampled_from([Period.MONTH, Period.YEAR]))
    amount = AmountLine(category, Pence(draw(PENNIES)), period, EVIDENCE)
    if force_amount:
        return amount
    options: list[LineInput] = [
        amount,
        IncludedLine(category, EVIDENCE),
        NotCalculatedLine(category, EVIDENCE),
        ConflictingLine(category, EVIDENCE),
        MissingLine(category),
    ]
    return draw(st.sampled_from(options))


@st.composite
def monthly_scenarios(draw: st.DrawFn) -> MonthlyScenario:
    mode = draw(st.sampled_from([Mode.BUY, Mode.RENT]))
    categories = _BUY_MONTHLY if mode == Mode.BUY else _RENT_MONTHLY
    lines = [
        draw(_line(category, force_amount=index == 0)) for index, category in enumerate(categories)
    ]
    return MonthlyScenario(mode, lines, Pence(draw(st.integers(1, 2**31 - 1))))


def _round_half_up_twelfth(yearly: int) -> int:
    """A positive yearly amount over 12, nearest penny, exact halves up (worked in the test)."""
    return (2 * yearly + 12) // 24


def _run(scenario: MonthlyScenario) -> MonthlyBreakdown:
    return monthly_cost(scenario.mode, scenario.lines, scenario.budget).value


@given(PENNIES, PENNIES, RATES, TERMS)
def test_monthly_repayment_larger_loan_never_lowers_the_repayment(
    loan: int, extra: int, rate: int, term: int
) -> None:
    smaller = monthly_repayment(Pence(loan), rate, term).value.monthly_repayment
    larger = monthly_repayment(Pence(loan + extra), rate, term).value.monthly_repayment

    assert larger >= smaller


@given(PENNIES, RATES, RATES, TERMS)
def test_monthly_repayment_higher_rate_never_lowers_the_repayment(
    loan: int, rate: int, extra: int, term: int
) -> None:
    lower = monthly_repayment(Pence(loan), rate, term).value.monthly_repayment
    higher = monthly_repayment(Pence(loan), rate + extra, term).value.monthly_repayment

    assert higher >= lower


@given(PENNIES, RATES, TERMS)
def test_monthly_repayment_any_valid_input_is_never_negative(
    loan: int, rate: int, term: int
) -> None:
    assert monthly_repayment(Pence(loan), rate, term).value.monthly_repayment >= Pence.ZERO


@given(monthly_scenarios())
def test_monthly_cost_any_lines_total_equals_the_sum_of_the_calculated_lines(
    scenario: MonthlyScenario,
) -> None:
    # Worked from the input lines: monthly amounts as given, yearly amounts divided by 12 and
    # rounded once (positive amounts, so exact halves round up).
    expected = sum(
        _round_half_up_twelfth(line.amount.value)
        if line.period == Period.YEAR
        else line.amount.value
        for line in scenario.lines
        if isinstance(line, AmountLine)
    )

    assert _run(scenario).total == Pence(expected)


@given(monthly_scenarios())
def test_monthly_cost_any_lines_is_partial_exactly_when_a_line_has_no_amount(
    scenario: MonthlyScenario,
) -> None:
    result = _run(scenario)
    without_amount = [
        line
        for line in scenario.lines
        if isinstance(line, NotCalculatedLine | ConflictingLine | MissingLine)
    ]

    assert result.is_partial == (len(without_amount) > 0)
    assert len(result.partial_reasons) == len(without_amount)


@given(monthly_scenarios())
def test_monthly_cost_any_lines_no_line_or_total_is_negative(scenario: MonthlyScenario) -> None:
    result = _run(scenario)

    assert result.total >= Pence.ZERO
    assert all(line.amount is None or line.amount >= Pence.ZERO for line in result.lines)


@given(monthly_scenarios())
def test_monthly_cost_any_lines_a_non_calculated_line_never_carries_pence(
    scenario: MonthlyScenario,
) -> None:
    result = _run(scenario)

    assert all(
        (line.status == LineStatus.CALCULATED) == (line.amount is not None) for line in result.lines
    )


@given(monthly_scenarios())
def test_monthly_cost_any_lines_budget_difference_is_budget_minus_total(
    scenario: MonthlyScenario,
) -> None:
    result = _run(scenario)

    assert result.budget_difference.value == scenario.budget.value - result.total.value
    assert result.within_budget == (result.total.value <= scenario.budget.value)


@given(PENNIES, PENNIES, PENNIES)
def test_monthly_cost_higher_rent_never_lowers_the_total(rent: int, extra: int, tax: int) -> None:
    def total(rent_pence: int) -> Pence:
        lines: list[LineInput] = [
            AmountLine(CostCategory.RENT, Pence(rent_pence), Period.MONTH, EVIDENCE),
            AmountLine(CostCategory.COUNCIL_TAX, Pence(tax), Period.YEAR, EVIDENCE),
        ]
        return monthly_cost(Mode.RENT, lines, Pence(1)).value.total

    assert total(rent + extra) >= total(rent)
