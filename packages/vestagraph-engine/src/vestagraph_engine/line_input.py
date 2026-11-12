"""One cost line given to the engine: an amount, or the reason there is no amount.

Missing data is never an amount of zero (AGENTS.md rule 7), so the lines without an amount have
their own types. ``evidence_ids`` are the ids of the evidence items behind a line, carried
through to the result untouched.
"""

from dataclasses import dataclass

from vestagraph_engine._checks import is_a
from vestagraph_engine.cost_types import CostCategory, Period
from vestagraph_engine.pence import Pence


def _check_category(category: object) -> None:
    if not is_a(category, CostCategory):
        message = "A line's category must be a CostCategory."
        raise TypeError(message)


def _check_evidence_ids(evidence_ids: object) -> None:
    if type(evidence_ids) is not tuple or any(type(item) is not str for item in evidence_ids):
        message = "A line's evidence_ids must be a tuple of str."
        raise TypeError(message)


@dataclass(frozen=True, slots=True)
class AmountLine:
    """A line with an amount, in the period its source states."""

    category: CostCategory
    amount: Pence
    period: Period
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_category(self.category)
        if not is_a(self.amount, Pence):
            message = "A line's amount must be a Pence."
            raise TypeError(message)
        if not is_a(self.period, Period):
            message = "A line's period must be a Period."
            raise TypeError(message)
        _check_evidence_ids(self.evidence_ids)


@dataclass(frozen=True, slots=True)
class IncludedLine:
    """A line covered by another charge. It adds nothing and does not make a total partial."""

    category: CostCategory
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_category(self.category)
        _check_evidence_ids(self.evidence_ids)


@dataclass(frozen=True, slots=True)
class NotCalculatedLine:
    """A line this version does not work out. It adds nothing and makes the total partial."""

    category: CostCategory
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_category(self.category)
        _check_evidence_ids(self.evidence_ids)


@dataclass(frozen=True, slots=True)
class ConflictingLine:
    """A line whose sources disagree and is not settled. Adds nothing; makes the total partial."""

    category: CostCategory
    evidence_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_category(self.category)
        _check_evidence_ids(self.evidence_ids)


@dataclass(frozen=True, slots=True)
class MissingLine:
    """A line with no evidence at all. It adds nothing and makes the total partial."""

    category: CostCategory

    def __post_init__(self) -> None:
        _check_category(self.category)

    @property
    def evidence_ids(self) -> tuple[str, ...]:
        return ()


type LineInput = AmountLine | IncludedLine | NotCalculatedLine | ConflictingLine | MissingLine

LINE_KINDS: tuple[type, ...] = (
    AmountLine,
    IncludedLine,
    NotCalculatedLine,
    ConflictingLine,
    MissingLine,
)
