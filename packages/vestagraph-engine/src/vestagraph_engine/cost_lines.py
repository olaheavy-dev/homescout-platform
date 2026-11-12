"""What monthly and upfront calculations share: checking the lines and placing them in a
fixed order, finding partial reasons, and totalling (ported from the C# ``CostLines``)."""

from collections.abc import Iterable, Sequence
from typing import assert_never

from vestagraph_engine._checks import is_a
from vestagraph_engine.breakdowns import LineResult, PartialReason
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import CostCategory, LineStatus, Mode, Period
from vestagraph_engine.line_input import (
    LINE_KINDS,
    AmountLine,
    ConflictingLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.pence import Pence
from vestagraph_engine.result import Error, ErrorCategory, Result

_MONTHLY_BUY_ORDER = (
    CostCategory.MORTGAGE_REPAYMENT,
    CostCategory.SERVICE_CHARGE,
    CostCategory.GROUND_RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
    CostCategory.BUILDINGS_INSURANCE,
    CostCategory.MAINTENANCE,
)
_MONTHLY_RENT_ORDER = (
    CostCategory.RENT,
    CostCategory.COUNCIL_TAX,
    CostCategory.ENERGY,
    CostCategory.WATER,
    CostCategory.BROADBAND,
)
_UPFRONT_BUY_ORDER = (
    CostCategory.MORTGAGE_DEPOSIT,
    CostCategory.MOVING_COSTS,
    CostCategory.STAMP_DUTY,
    CostCategory.LEGAL_FEES,
)
_UPFRONT_RENT_ORDER = (
    CostCategory.DEPOSIT,
    CostCategory.FIRST_MONTH_RENT,
    CostCategory.MOVING_COSTS,
)
_MONTH_ONLY = (CostCategory.RENT, CostCategory.MORTGAGE_REPAYMENT)


def monthly_order(mode: Mode) -> tuple[CostCategory, ...]:
    """Which categories belong in a monthly breakdown, in the fixed order (plan 4b, section 1)."""
    if not is_a(mode, Mode):
        message = "monthly_order needs a Mode."
        raise TypeError(message)
    match mode:
        case Mode.BUY:
            return _MONTHLY_BUY_ORDER
        case Mode.RENT:
            return _MONTHLY_RENT_ORDER
        case _:
            assert_never(mode)


def upfront_order(mode: Mode) -> tuple[CostCategory, ...]:
    """Which categories belong in an upfront breakdown, in the fixed order."""
    if not is_a(mode, Mode):
        message = "upfront_order needs a Mode."
        raise TypeError(message)
    match mode:
        case Mode.BUY:
            return _UPFRONT_BUY_ORDER
        case Mode.RENT:
            return _UPFRONT_RENT_ORDER
        case _:
            assert_never(mode)


def resolve(
    lines: Sequence[LineInput], order: Sequence[CostCategory], *, upfront: bool = False
) -> Result[tuple[LineResult, ...]]:
    """Check each line and turn it into a result line, returned in ``order``.

    ``upfront`` is true for upfront lines, which are amounts paid once; false for monthly lines.
    A yearly monthly-list amount becomes monthly with ``Pence.annual_to_monthly``, rounded once.
    The first problem found, in input order, is the failure. A line that is not one of the known
    kinds (including ``None``) raises ``TypeError``.
    """
    resolved: dict[CostCategory, LineResult] = {}
    for line in lines:
        if type(line) not in LINE_KINDS:
            message = "Every line must be an AmountLine, IncludedLine, NotCalculatedLine, "
            message += "ConflictingLine or MissingLine."
            raise TypeError(message)

        name = category_id(line.category)
        if line.category not in order:
            return _fail(
                f"input.not-for-mode.{name}",
                f"The {name} line does not belong in this list for this kind of home.",
                ErrorCategory.VALIDATION,
            )
        if line.category in resolved:
            return _fail(
                f"input.ambiguous.{name}",
                f"There is more than one {name} line.",
                ErrorCategory.CONFLICT,
            )

        result = _resolve_line(line, name, upfront=upfront)
        if result.is_failure:
            return Result.failure(result.error)
        resolved[line.category] = result.value

    return Result.success(tuple(resolved[category] for category in order if category in resolved))


def partial_reasons(lines: Iterable[LineResult]) -> tuple[PartialReason, ...]:
    """The reasons a total is partial: every line without an amount that is not simply included."""
    no_amount = (LineStatus.NOT_CALCULATED, LineStatus.CONFLICTING, LineStatus.MISSING)
    return tuple(
        PartialReason(line.category, line.status) for line in lines if line.status in no_amount
    )


def total(lines: Iterable[LineResult]) -> Pence:
    """The sum of the calculated lines. Raises ``OverflowError`` if it does not fit in 64 bits."""
    running = Pence.ZERO
    for line in lines:
        if line.amount is not None:
            running += line.amount
    return running


def _resolve_line(line: LineInput, name: str, *, upfront: bool) -> Result[LineResult]:
    match line:
        case AmountLine():
            return _resolve_amount(line, name, upfront=upfront)
        case IncludedLine():
            return _without_amount(line.category, LineStatus.INCLUDED, line.evidence_ids)
        case NotCalculatedLine():
            return _without_amount(line.category, LineStatus.NOT_CALCULATED, line.evidence_ids)
        case ConflictingLine():
            return _without_amount(line.category, LineStatus.CONFLICTING, line.evidence_ids)
        case MissingLine():
            return _without_amount(line.category, LineStatus.MISSING, line.evidence_ids)
        case _:
            assert_never(line)


def _without_amount(
    category: CostCategory, status: LineStatus, evidence_ids: tuple[str, ...]
) -> Result[LineResult]:
    return Result.success(LineResult(category, status, None, None, evidence_ids))


def _resolve_amount(line: AmountLine, name: str, *, upfront: bool) -> Result[LineResult]:
    if line.amount.value <= 0:
        return _fail_line(
            f"input.not-positive.{name}",
            f"The {name} amount must be more than zero.",
            ErrorCategory.VALIDATION,
        )

    # Upfront amounts are paid once; rent and the mortgage payment are monthly figures; other
    # bills may be monthly or yearly.
    month_only = line.category in _MONTH_ONLY
    if upfront:
        allowed = line.period == Period.ONCE
    else:
        allowed = line.period == Period.MONTH or (line.period == Period.YEAR and not month_only)
    if not allowed:
        return _fail_line(
            f"input.wrong-period.{name}",
            f"The {name} amount is given for a period that cannot be used here.",
            ErrorCategory.VALIDATION,
        )

    amount = line.amount.annual_to_monthly() if line.period == Period.YEAR else line.amount
    return Result.success(
        LineResult(line.category, LineStatus.CALCULATED, amount, line.period, line.evidence_ids)
    )


def _fail(code: str, message: str, category: ErrorCategory) -> Result[tuple[LineResult, ...]]:
    return Result.failure(Error(code, message, category))


def _fail_line(code: str, message: str, category: ErrorCategory) -> Result[LineResult]:
    return Result.failure(Error(code, message, category))
