"""One cost line given to the engine: an amount, or the reason there is no amount.

Missing data is never an amount of zero (AGENTS.md rule 7), so the lines without an amount have
their own types. ``evidence_ids`` are the ids of the evidence items behind a line, carried
through to the result untouched.
"""

from dataclasses import dataclass

from vestagraph_engine.cost_types import CostCategory, Period
from vestagraph_engine.pence import Pence


@dataclass(frozen=True, slots=True)
class AmountLine:
    """A line with an amount, in the period its source states."""

    category: CostCategory
    amount: Pence
    period: Period
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IncludedLine:
    """A line covered by another charge. It adds nothing and does not make a total partial."""

    category: CostCategory
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class NotCalculatedLine:
    """A line this version does not work out. It adds nothing and makes the total partial."""

    category: CostCategory
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ConflictingLine:
    """A line whose sources disagree and is not settled. Adds nothing; makes the total partial."""

    category: CostCategory
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MissingLine:
    """A line with no evidence at all. It adds nothing and makes the total partial."""

    category: CostCategory

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
