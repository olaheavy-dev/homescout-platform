"""Works out the costs of one home across the story (ported from the C# ``HomeCostBuilder``).

The inputs at each step come from the assumption selector, consecutive steps that use the same
evidence are merged into one scenario, and each scenario after the first records what changed
since the one before (decision 0021).
"""

from collections.abc import Sequence

from vestagraph_engine import cost_lines
from vestagraph_engine._checks import INT32_MAX, is_a
from vestagraph_engine.assumption_selector import check_home, select_assumptions
from vestagraph_engine.breakdowns import LineResult, MonthlyBreakdown, UpfrontBreakdown
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode, Period
from vestagraph_engine.evidence import HomeFacts
from vestagraph_engine.home_costs import (
    ChangeKind,
    CostChange,
    HomeCosts,
    MortgageSummary,
    ScenarioCosts,
)
from vestagraph_engine.line_input import AmountLine, LineInput
from vestagraph_engine.monthly_cost import monthly_cost
from vestagraph_engine.mortgage import monthly_repayment
from vestagraph_engine.pence import Pence
from vestagraph_engine.result import Error, ErrorCategory, Result
from vestagraph_engine.selected_inputs import SelectedInputs
from vestagraph_engine.upfront_cash import upfront_cash


def build_home_costs(facts: HomeFacts, story_steps: Sequence[int]) -> Result[HomeCosts]:
    """Build the scenarios of a home.

    A scenario is named ``from-step-N`` after its first step. A change is reported for every line
    whose status, amount or evidence differs from the previous scenario; a monthly difference is
    the difference of the two rounded monthly lines, never a rounding of the yearly difference
    (register line BE-14). ``story_steps`` are the story's steps, for example 1, 2, 3, 4, strictly
    increasing.

    Error codes (tests match the code, never the message): ``home.not-covered``,
    ``home.mode-missing`` and ``story.step-out-of-range`` (no steps, a step below 1, or steps that
    do not strictly increase), plus every failure of the assumption selector, the mortgage
    calculation, the monthly cost and the upfront cash, passed on unchanged.

    Raises ``TypeError`` for facts that are not ``HomeFacts``, steps that are not a list or tuple
    of ``int``, and ``ValueError`` for a step above the largest 32-bit ``int`` (the C# step is an
    ``int``).
    """
    if not is_a(facts, HomeFacts):
        message = "build_home_costs needs HomeFacts."
        raise TypeError(message)
    if not is_a(story_steps, Sequence) or is_a(story_steps, str):
        message = "build_home_costs needs its steps as a list or tuple of whole numbers (int)."
        raise TypeError(message)
    steps = tuple(story_steps)
    for step in steps:
        if type(step) is not int:
            message = "Every story step must be a whole number (int)."
            raise TypeError(message)
        if step > INT32_MAX:
            message = "A story step is above the largest 32-bit whole number."
            raise ValueError(message)

    home = check_home(facts)
    if home.is_failure:
        return Result.failure(home.error)

    if not steps or steps[0] < 1 or any(steps[i + 1] <= steps[i] for i in range(len(steps) - 1)):
        return Result.failure(
            Error(
                "story.step-out-of-range",
                "The story steps must start at 1 or more and increase.",
                ErrorCategory.VALIDATION,
            )
        )

    selections: list[tuple[int, SelectedInputs]] = []
    for step in steps:
        selected = select_assumptions(facts, step)
        if selected.is_failure:
            return Result.failure(selected.error)
        selections.append((step, selected.value))

    scenarios: list[ScenarioCosts] = []
    previous_inputs: tuple[LineInput, ...] | None = None
    index = 0
    while index < len(selections):
        last = index
        signature = selections[index][1].signature()
        while last + 1 < len(selections) and selections[last + 1][1].signature() == signature:
            last += 1

        built = _build_scenario(
            facts,
            selections[index][1],
            selections[index][0],
            selections[last][0],
            scenarios[-1] if scenarios else None,
            previous_inputs,
        )
        if built.is_failure:
            return Result.failure(built.error)

        scenario, previous_inputs = built.value
        scenarios.append(scenario)
        index = last + 1

    return Result.success(HomeCosts(facts.home_id, home.value, facts.nation, tuple(scenarios)))


def _build_scenario(
    facts: HomeFacts,
    inputs: SelectedInputs,
    from_step: int,
    to_step: int,
    previous: ScenarioCosts | None,
    previous_inputs: tuple[LineInput, ...] | None,
) -> Result[tuple[ScenarioCosts, tuple[LineInput, ...]]]:
    monthly_inputs: list[LineInput] = []
    mortgage: MortgageSummary | None = None
    if inputs.mortgage is not None:
        m = inputs.mortgage
        repayment = monthly_repayment(m.asking_price - m.deposit, m.rate_basis_points, m.term_years)
        if repayment.is_failure:
            return Result.failure(repayment.error)

        mortgage = MortgageSummary(repayment.value, m.evidence_ids)
        monthly_inputs.append(
            AmountLine(
                CostCategory.MORTGAGE_REPAYMENT,
                repayment.value.monthly_repayment,
                Period.MONTH,
                m.evidence_ids,
            )
        )

    monthly_inputs.extend(inputs.monthly_lines)

    monthly = monthly_cost(inputs.mode, monthly_inputs, facts.monthly_budget)
    if monthly.is_failure:
        return Result.failure(monthly.error)

    upfront = upfront_cash(inputs.mode, inputs.upfront_lines)
    if upfront.is_failure:
        return Result.failure(upfront.error)

    changes: tuple[CostChange, ...] = ()
    monthly_total_change: Pence | None = None
    if previous is not None and previous_inputs is not None:
        changes = _changes(
            inputs.mode,
            previous,
            previous_inputs,
            monthly.value,
            upfront.value,
            tuple(monthly_inputs),
        )
        if _same_lines_left_out(previous.monthly, monthly.value):
            monthly_total_change = monthly.value.total - previous.monthly.total

    scenario = ScenarioCosts(
        f"from-step-{from_step}",
        from_step,
        to_step,
        mortgage,
        monthly.value,
        upfront.value,
        changes,
        monthly_total_change,
    )
    return Result.success((scenario, tuple(monthly_inputs)))


def _same_lines_left_out(previous: MonthlyBreakdown, current: MonthlyBreakdown) -> bool:
    """True when both totals leave out exactly the same lines for the same reasons.

    Only then is the difference of the two totals meaningful: otherwise a line that became
    unknown would look like a saving (AGENTS.md rule 7).
    """
    return set(previous.partial_reasons) == set(current.partial_reasons)


def _changes(
    mode: Mode,
    previous: ScenarioCosts,
    previous_inputs: tuple[LineInput, ...],
    current_monthly: MonthlyBreakdown,
    current_upfront: UpfrontBreakdown,
    current_inputs: tuple[LineInput, ...],
) -> tuple[CostChange, ...]:
    changes: list[CostChange] = []
    for category in cost_lines.monthly_order(mode):
        _add_change(
            changes,
            category,
            previous.monthly.lines,
            current_monthly.lines,
            previous_inputs,
            current_inputs,
            monthly=True,
        )
    for category in cost_lines.upfront_order(mode):
        _add_change(
            changes,
            category,
            previous.upfront.lines,
            current_upfront.lines,
            previous_inputs,
            current_inputs,
            monthly=False,
        )
    return tuple(changes)


def _line_of(lines: Sequence[LineResult], category: CostCategory) -> LineResult | None:
    return next((line for line in lines if line.category == category), None)


def _source_of(inputs: Sequence[LineInput], category: CostCategory) -> AmountLine | None:
    return next(
        (line for line in inputs if isinstance(line, AmountLine) and line.category == category),
        None,
    )


def _add_change(
    changes: list[CostChange],
    category: CostCategory,
    previous_lines: Sequence[LineResult],
    current_lines: Sequence[LineResult],
    previous_inputs: Sequence[LineInput],
    current_inputs: Sequence[LineInput],
    *,
    monthly: bool,
) -> None:
    before = _line_of(previous_lines, category)
    now = _line_of(current_lines, category)
    before_ids = () if before is None else before.evidence_ids
    now_ids = () if now is None else now.evidence_ids

    unchanged = (
        (None if before is None else before.status) == (None if now is None else now.status)
        and (None if before is None else before.amount) == (None if now is None else now.amount)
        and before_ids == now_ids
    )
    if unchanged:
        return

    kind: ChangeKind
    monthly_difference: Pence | None = None
    annual_difference: Pence | None = None
    if (
        before is not None
        and now is not None
        and before.status == LineStatus.CALCULATED
        and now.status == LineStatus.CALCULATED
    ):
        # Both calculated: a value change when the source amount or its period changed, even if
        # both round to the same monthly amount; a new source for the same amount and period is an
        # evidence change.
        old_source = _source_of(previous_inputs, category)
        new_source = _source_of(current_inputs, category)
        if monthly and old_source is not None and new_source is not None:
            source_changed = (
                old_source.amount != new_source.amount or old_source.period != new_source.period
            )
        else:
            source_changed = before.amount != now.amount
        kind = ChangeKind.VALUE_CHANGED if source_changed else ChangeKind.EVIDENCE_CHANGED

        if monthly and kind == ChangeKind.VALUE_CHANGED:
            if before.amount is not None and now.amount is not None:
                monthly_difference = now.amount - before.amount
            if (
                monthly_difference is not None
                and old_source is not None
                and new_source is not None
                and old_source.period == Period.YEAR
                and new_source.period == Period.YEAR
            ):
                annual_difference = new_source.amount - old_source.amount
    elif now is not None and now.status == LineStatus.CALCULATED:
        kind = ChangeKind.NOW_CALCULATED
    elif now is None:
        # The line is not in this scenario at all: it became not applicable.
        kind = ChangeKind.NO_LONGER_APPLIES
    elif before is not None and before.status == LineStatus.CALCULATED:
        kind = ChangeKind.NO_LONGER_CALCULATED
    else:
        kind = ChangeKind.EVIDENCE_CHANGED

    changes.append(
        CostChange(category, kind, before_ids, now_ids, monthly_difference, annual_difference)
    )
