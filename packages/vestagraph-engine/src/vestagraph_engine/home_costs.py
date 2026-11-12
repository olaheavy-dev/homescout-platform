"""The costs of one home across the story (ported from the C# ``HomeCosts``)."""

from dataclasses import dataclass
from enum import Enum

from vestagraph_engine._checks import check_int32, is_a
from vestagraph_engine.breakdowns import MonthlyBreakdown, UpfrontBreakdown
from vestagraph_engine.cost_types import CostCategory, Mode
from vestagraph_engine.evidence import Nation
from vestagraph_engine.mortgage import MortgageRepayment
from vestagraph_engine.pence import Pence


def _check_ids(ids: object, owner: str, name: str) -> None:
    if type(ids) is not tuple or any(type(item) is not str for item in ids):
        message = f"{owner}'s {name} must be a tuple of str."
        raise TypeError(message)


def _check_optional_pence(value: object, owner: str, name: str) -> None:
    if value is not None and not is_a(value, Pence):
        message = f"{owner}'s {name} must be a Pence or None."
        raise TypeError(message)


class ChangeKind(Enum):
    """How a line changed from one scenario to the next.

    The value is the name used in the generated file.
    """

    VALUE_CHANGED = "value-changed"
    """Calculated in both scenarios and its source amount or period differs (even if both round
    to the same monthly amount)."""

    EVIDENCE_CHANGED = "evidence-changed"
    """The line's evidence or status changed but no figure moved: the source amount and period
    are the same, or neither scenario has an amount."""

    NO_LONGER_APPLIES = "no-longer-applies"
    """The line was in the previous scenario and is not in this one, because it became not
    applicable."""

    NOW_CALCULATED = "now-calculated"
    """The line had no amount before and has one now."""

    NO_LONGER_CALCULATED = "no-longer-calculated"
    """The line had an amount before and has none now."""


@dataclass(frozen=True, slots=True)
class CostChange:
    """One line that differs between a scenario and the one before it.

    ``monthly_difference`` is now minus before, both rounded monthly lines; only for a
    value-changed monthly line, and it may be 0 when rounding hides a small change.
    ``annual_difference`` is now minus before, both yearly amounts as the sources state them;
    only when both are yearly.
    """

    category: CostCategory
    kind: ChangeKind
    previous_evidence_ids: tuple[str, ...]
    current_evidence_ids: tuple[str, ...]
    monthly_difference: Pence | None
    annual_difference: Pence | None

    def __post_init__(self) -> None:
        if not is_a(self.category, CostCategory):
            message = "A change's category must be a CostCategory."
            raise TypeError(message)
        if not is_a(self.kind, ChangeKind):
            message = "A change's kind must be a ChangeKind."
            raise TypeError(message)
        _check_ids(self.previous_evidence_ids, "A change", "previous_evidence_ids")
        _check_ids(self.current_evidence_ids, "A change", "current_evidence_ids")
        _check_optional_pence(self.monthly_difference, "A change", "monthly_difference")
        _check_optional_pence(self.annual_difference, "A change", "annual_difference")


@dataclass(frozen=True, slots=True)
class MortgageSummary:
    """A worked-out mortgage with the evidence behind its inputs (price, deposit, rate, term)."""

    repayment: MortgageRepayment
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not is_a(self.repayment, MortgageRepayment):
            message = "A mortgage summary's repayment must be a MortgageRepayment."
            raise TypeError(message)
        _check_ids(self.evidence_ids, "A mortgage summary", "evidence_ids")


@dataclass(frozen=True, slots=True)
class ScenarioCosts:
    """The costs of a home for the story steps ``from_step`` to ``to_step``, which all use the
    same evidence.

    ``scenario_id`` is always ``from-step-N``, where N is the first step; ``changes`` is what
    changed since the previous scenario (empty for the first); ``monthly_total_change`` is this
    scenario's monthly total minus the previous one's. It is ``None`` for the first scenario, and
    ``None`` when the two totals leave out different lines (a line that became unknown must not
    look like a saving); the changes list explains what moved.
    """

    scenario_id: str
    from_step: int
    to_step: int
    mortgage: MortgageSummary | None
    monthly: MonthlyBreakdown
    upfront: UpfrontBreakdown
    changes: tuple[CostChange, ...]
    monthly_total_change: Pence | None

    def __post_init__(self) -> None:
        if not is_a(self.scenario_id, str):
            message = "A scenario's scenario_id must be a str."
            raise TypeError(message)
        check_int32(self.from_step, "A scenario's from_step")
        check_int32(self.to_step, "A scenario's to_step")
        if self.mortgage is not None and not is_a(self.mortgage, MortgageSummary):
            message = "A scenario's mortgage must be a MortgageSummary or None."
            raise TypeError(message)
        if not is_a(self.monthly, MonthlyBreakdown):
            message = "A scenario's monthly must be a MonthlyBreakdown."
            raise TypeError(message)
        if not is_a(self.upfront, UpfrontBreakdown):
            message = "A scenario's upfront must be an UpfrontBreakdown."
            raise TypeError(message)
        if type(self.changes) is not tuple or any(
            type(change) is not CostChange for change in self.changes
        ):
            message = "A scenario's changes must be a tuple of CostChange."
            raise TypeError(message)
        _check_optional_pence(self.monthly_total_change, "A scenario", "monthly_total_change")


@dataclass(frozen=True, slots=True)
class HomeCosts:
    """The costs of one home, in the order of its scenarios."""

    home_id: str
    mode: Mode
    nation: Nation
    scenarios: tuple[ScenarioCosts, ...]

    def __post_init__(self) -> None:
        if not is_a(self.home_id, str):
            message = "A home's home_id must be a str."
            raise TypeError(message)
        if not is_a(self.mode, Mode):
            message = "A home's mode must be a Mode."
            raise TypeError(message)
        if not is_a(self.nation, Nation):
            message = "A home's nation must be a Nation."
            raise TypeError(message)
        if type(self.scenarios) is not tuple or any(
            type(scenario) is not ScenarioCosts for scenario in self.scenarios
        ):
            message = "A home's scenarios must be a tuple of ScenarioCosts."
            raise TypeError(message)
