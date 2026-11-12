"""What the monthly and upfront calculations give back (ported from the C# ``Breakdowns``)."""

from dataclasses import dataclass

from vestagraph_engine.cost_types import CostCategory, LineStatus, Period
from vestagraph_engine.pence import Pence


@dataclass(frozen=True, slots=True)
class LineResult:
    """One line of a result. Only a calculated line has an amount.

    ``amount`` is whole pence per month for a monthly breakdown, and ``source_period`` the period
    the source stated; both are ``None`` unless the line is calculated.
    """

    category: CostCategory
    status: LineStatus
    amount: Pence | None
    source_period: Period | None
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PartialReason:
    """Why a total is partial: which line has no amount, and why. Codes, not prose."""

    category: CostCategory
    status: LineStatus


@dataclass(frozen=True, slots=True)
class MonthlyBreakdown:
    """The monthly cost of a home with its budget check.

    ``lines`` are in the engine's fixed order for the mode; ``total`` is the sum of the calculated
    lines (each rounded once); ``is_partial`` is true exactly when some line is not calculated,
    conflicting or missing, with one reason for each; ``budget_difference`` is the budget minus
    the total (positive is headroom, negative is over budget); ``within_budget`` is true when the
    total is at or below the budget (exactly equal is within); ``based_on_partial_total`` is true
    when the total is partial, so the real figure is higher ("at least").
    """

    lines: tuple[LineResult, ...]
    total: Pence
    is_partial: bool
    partial_reasons: tuple[PartialReason, ...]
    budget: Pence
    budget_difference: Pence
    within_budget: bool
    based_on_partial_total: bool


@dataclass(frozen=True, slots=True)
class UpfrontBreakdown:
    """The cash needed up front for a home.

    ``lines`` are in the engine's fixed order for the mode, each amount paid once; ``total`` is
    the sum of the calculated lines; ``is_partial`` is true exactly when some line is not
    calculated, conflicting or missing, with one reason for each.
    """

    lines: tuple[LineResult, ...]
    total: Pence
    is_partial: bool
    partial_reasons: tuple[PartialReason, ...]
