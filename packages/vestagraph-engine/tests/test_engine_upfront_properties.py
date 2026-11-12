"""Property tests for upfront cash, ported from the C# UpfrontCashProperties.

FsCheck becomes Hypothesis. Pence amounts are bounded to 1..10^10 so that sums cannot overflow
(overflow has its own unit test). Oracles are written here in plain arithmetic and never call the
function under test.
"""

from dataclasses import dataclass

from hypothesis import given
from hypothesis import strategies as st
from vestagraph_engine import Pence
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode, Period
from vestagraph_engine.line_input import (
    AmountLine,
    ConflictingLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.upfront_cash import upfront_cash

_MAX_PENCE = 10_000_000_000
EVIDENCE = ("EVIDENCE-1",)

PENNIES = st.one_of(
    st.integers(1, 1_000),
    st.integers(1, 2**31 - 1),
    st.sampled_from([1, _MAX_PENCE]),
)

_BUY_UPFRONT = [
    CostCategory.MORTGAGE_DEPOSIT,
    CostCategory.MOVING_COSTS,
    CostCategory.STAMP_DUTY,
    CostCategory.LEGAL_FEES,
]
_RENT_UPFRONT = [CostCategory.DEPOSIT, CostCategory.FIRST_MONTH_RENT, CostCategory.MOVING_COSTS]


@dataclass(frozen=True)
class UpfrontScenario:
    """Upfront lines for one mode; a buyer's mortgage deposit always has an amount."""

    mode: Mode
    lines: list[LineInput]


@st.composite
def _line(draw: st.DrawFn, category: CostCategory, *, force_amount: bool) -> LineInput:
    amount = AmountLine(category, Pence(draw(PENNIES)), Period.ONCE, EVIDENCE)
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
def upfront_scenarios(draw: st.DrawFn) -> UpfrontScenario:
    mode = draw(st.sampled_from([Mode.BUY, Mode.RENT]))
    categories = _BUY_UPFRONT if mode == Mode.BUY else _RENT_UPFRONT
    lines = [
        draw(_line(category, force_amount=mode == Mode.BUY and index == 0))
        for index, category in enumerate(categories)
    ]
    return UpfrontScenario(mode, lines)


@given(upfront_scenarios())
def test_upfront_cash_any_lines_total_equals_the_sum_of_the_calculated_lines(
    scenario: UpfrontScenario,
) -> None:
    expected = sum(line.amount.value for line in scenario.lines if isinstance(line, AmountLine))

    assert upfront_cash(scenario.mode, scenario.lines).value.total == Pence(expected)


@given(upfront_scenarios())
def test_upfront_cash_any_lines_is_partial_exactly_when_a_line_has_no_amount(
    scenario: UpfrontScenario,
) -> None:
    result = upfront_cash(scenario.mode, scenario.lines).value
    without_amount = [
        line
        for line in scenario.lines
        if isinstance(line, NotCalculatedLine | ConflictingLine | MissingLine)
    ]

    assert result.is_partial == (len(without_amount) > 0)
    assert len(result.partial_reasons) == len(without_amount)


@given(upfront_scenarios())
def test_upfront_cash_any_lines_no_line_or_total_is_negative(scenario: UpfrontScenario) -> None:
    result = upfront_cash(scenario.mode, scenario.lines).value

    assert result.total >= Pence.ZERO
    assert all(line.amount is None or line.amount > Pence.ZERO for line in result.lines)


@given(upfront_scenarios())
def test_upfront_cash_any_lines_a_non_calculated_line_never_carries_pence(
    scenario: UpfrontScenario,
) -> None:
    result = upfront_cash(scenario.mode, scenario.lines).value

    assert all(
        (line.status == LineStatus.CALCULATED) == (line.amount is not None) for line in result.lines
    )
