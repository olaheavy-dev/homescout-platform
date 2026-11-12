"""Adds up the monthly cost of a home and checks it against the monthly budget (decision 0021)."""

from collections.abc import Sequence

from vestagraph_engine import cost_lines
from vestagraph_engine._checks import is_a
from vestagraph_engine.breakdowns import MonthlyBreakdown
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import LineStatus, Mode
from vestagraph_engine.line_input import LineInput
from vestagraph_engine.pence import Pence
from vestagraph_engine.result import Error, ErrorCategory, Result


def monthly_cost(mode: Mode, lines: Sequence[LineInput], budget: Pence) -> Result[MonthlyBreakdown]:
    """Work out the monthly cost.

    Each yearly amount is divided by 12 and rounded once; a monthly amount is used as given; the
    total is the sum of the rounded lines. A line with no amount (included, not calculated,
    conflicting or missing) adds nothing and is never treated as zero. The total is partial when
    any line is not calculated, conflicting or missing. A line the home does not have is simply
    not given, and is left out of the result (register line BE-13).

    The budget check: the difference is the budget minus the total, and a total exactly equal to
    the budget is within it (founder, 23 Oct 2026). On a partial total only the calculated lines
    are counted, so ``based_on_partial_total`` tells the screen to say "at least". The anchor line
    (the mortgage repayment when buying, the rent when renting) must have an amount (BE-16).

    Expected failures come back as a failed ``Result``; tests match the code, never the message:
    ``input.not-positive.budget`` and ``input.not-positive.{category}`` (the budget or an amount
    is zero or less); ``input.wrong-period.{category}`` (for example rent given yearly);
    ``input.not-for-mode.{category}`` (a line that does not belong in this list for this mode);
    ``input.ambiguous.{category}`` (the same category given twice); ``input.missing.{category}``
    (the anchor line is absent or has no amount).

    Raises ``TypeError`` for a wrong type (a mode that is not a ``Mode``, lines that are not a
    sequence of the known line kinds, a budget that is not ``Pence``) and ``OverflowError`` when
    a total does not fit in 64 bits.
    """
    if not is_a(lines, Sequence) or is_a(lines, str):
        message = "monthly_cost needs its lines as a list or tuple."
        raise TypeError(message)
    if not is_a(budget, Pence):
        message = "monthly_cost needs a Pence budget."
        raise TypeError(message)
    order = cost_lines.monthly_order(mode)

    if budget.value <= 0:
        return _fail("input.not-positive.budget", "The monthly budget must be more than zero.")

    resolved = cost_lines.resolve(lines, order)
    if resolved.is_failure:
        return Result.failure(resolved.error)
    result_lines = resolved.value

    anchor = order[0]
    anchor_lines = [line for line in result_lines if line.category == anchor]
    if not anchor_lines or anchor_lines[0].status != LineStatus.CALCULATED:
        name = category_id(anchor)
        return _fail(
            f"input.missing.{name}",
            f"The {name} amount is needed before a monthly cost can be worked out.",
        )

    reasons = cost_lines.partial_reasons(result_lines)
    total = cost_lines.total(result_lines)
    is_partial = len(reasons) > 0

    return Result.success(
        MonthlyBreakdown(
            lines=result_lines,
            total=total,
            is_partial=is_partial,
            partial_reasons=reasons,
            budget=budget,
            budget_difference=budget - total,
            within_budget=total <= budget,
            based_on_partial_total=is_partial,
        )
    )


def _fail(code: str, message: str) -> Result[MonthlyBreakdown]:
    return Result.failure(Error(code, message, ErrorCategory.VALIDATION))
