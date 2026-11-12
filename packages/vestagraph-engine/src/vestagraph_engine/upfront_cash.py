"""Adds up the cash needed up front for a home (decision 0021)."""

from collections.abc import Sequence

from vestagraph_engine import cost_lines
from vestagraph_engine._checks import is_a
from vestagraph_engine.breakdowns import UpfrontBreakdown
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode
from vestagraph_engine.line_input import LineInput
from vestagraph_engine.result import Error, ErrorCategory, Result


def upfront_cash(mode: Mode, lines: Sequence[LineInput]) -> Result[UpfrontBreakdown]:
    """Work out the upfront cash.

    Every amount is paid once. A line with no amount (included, not calculated, conflicting or
    missing) adds nothing and is never treated as zero; stamp duty and legal fees are given as
    not calculated in this version, so a buyer's total is partial. The total is partial when any
    line is not calculated, conflicting or missing. A line the home does not have is simply not
    given, and is left out of the result (register line BE-13).

    Buying requires a calculated mortgage deposit (register line BE-16), otherwise this fails with
    ``input.missing.mortgage-deposit``. Renting has no required upfront input, so an empty list
    gives a total of 0 that is not partial; callers that expect a deposit and the first month's
    rent should pass them as lines (the assumption selector passes missing ones as
    ``MissingLine``).

    Expected failures come back as a failed ``Result``; tests match the code, never the message:
    ``input.not-positive.{category}``, ``input.wrong-period.{category}`` (anything but a one-off
    amount), ``input.not-for-mode.{category}``, ``input.ambiguous.{category}`` and
    ``input.missing.mortgage-deposit``.

    Raises ``TypeError`` for a wrong type (a mode that is not a ``Mode``, lines that are not a
    sequence of the known line kinds) and ``OverflowError`` when a total does not fit in 64 bits.
    """
    if not is_a(lines, Sequence) or is_a(lines, str):
        message = "upfront_cash needs its lines as a list or tuple."
        raise TypeError(message)
    order = cost_lines.upfront_order(mode)

    resolved = cost_lines.resolve(lines, order, upfront=True)
    if resolved.is_failure:
        return Result.failure(resolved.error)
    result_lines = resolved.value

    # A buyer's deposit is a required input (register line BE-16), as the anchor line is for the
    # monthly cost.
    if mode == Mode.BUY:
        deposit = [line for line in result_lines if line.category == CostCategory.MORTGAGE_DEPOSIT]
        if not deposit or deposit[0].status != LineStatus.CALCULATED:
            return Result.failure(
                Error(
                    "input.missing.mortgage-deposit",
                    "The mortgage deposit amount is needed before upfront cash can be worked out.",
                    ErrorCategory.VALIDATION,
                )
            )

    reasons = cost_lines.partial_reasons(result_lines)
    return Result.success(
        UpfrontBreakdown(
            lines=result_lines,
            total=cost_lines.total(result_lines),
            is_partial=len(reasons) > 0,
            partial_reasons=reasons,
        )
    )
