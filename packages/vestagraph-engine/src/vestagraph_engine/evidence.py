"""What the fixture data says about a home, as the engine reads it (ported from C# ``Evidence``)."""

from dataclasses import dataclass
from enum import Enum

from vestagraph_engine._checks import check_int32, is_a
from vestagraph_engine.cost_types import Mode, Period
from vestagraph_engine.pence import Pence


class Nation(Enum):
    """The UK nation a home is in (AGENTS.md rule 6)."""

    ENGLAND = "England"
    WALES = "Wales"
    SCOTLAND = "Scotland"
    NORTHERN_IRELAND = "Northern Ireland"


class EvidenceStatus(Enum):
    """What the fixture data says about an evidence item, as at the snapshot."""

    AVAILABLE = "available"
    MISSING = "missing"
    CONFLICTING = "conflicting"
    STALE = "stale"
    NOT_APPLICABLE = "not-applicable"
    NOT_CALCULATED = "not-calculated"
    INCLUDED = "included"


@dataclass(frozen=True, slots=True)
class MoneyValue:
    """An amount of money in whole pence, with the period its source states."""

    amount: Pence
    period: Period

    def __post_init__(self) -> None:
        if not is_a(self.amount, Pence):
            message = "A money value's amount must be a Pence."
            raise TypeError(message)
        if not is_a(self.period, Period):
            message = "A money value's period must be a Period."
            raise TypeError(message)


@dataclass(frozen=True, slots=True)
class RateValue:
    """A yearly rate in whole basis points (550 is 5.5%)."""

    basis_points: int

    def __post_init__(self) -> None:
        check_int32(self.basis_points, "A rate value's basis points")


@dataclass(frozen=True, slots=True)
class YearsValue:
    """A length of time in whole years."""

    years: int

    def __post_init__(self) -> None:
        check_int32(self.years, "A years value's years")


@dataclass(frozen=True, slots=True)
class OtherValue:
    """A value of another kind (text, a band, a certificate, a lease term).

    The engine never reads it as a cost.
    """


type EvidenceValue = MoneyValue | RateValue | YearsValue | OtherValue

VALUE_KINDS: tuple[type, ...] = (MoneyValue, RateValue, YearsValue, OtherValue)


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """One item of evidence, as the fixture data records it.

    ``id`` is carried through to the result; ``category`` is the evidence category (for example
    ``service-charge`` or ``water-responsibility``); ``status`` is the status as at the snapshot;
    ``value`` is ``None`` when the status has none; ``context_only`` is true when the item is shown
    for context and never enters a total; ``used_from_step`` is the first story step from which
    the item is used (``None`` when it is used from the start); ``supersedes`` is the id of an
    item this one replaces once it is in use, or ``None``.
    """

    id: str
    category: str
    status: EvidenceStatus
    value: EvidenceValue | None
    context_only: bool
    used_from_step: int | None
    supersedes: str | None

    def __post_init__(self) -> None:
        if not is_a(self.id, str):
            message = "An evidence item's id must be a str."
            raise TypeError(message)
        if not is_a(self.category, str):
            message = "An evidence item's category must be a str."
            raise TypeError(message)
        if not is_a(self.status, EvidenceStatus):
            message = "An evidence item's status must be an EvidenceStatus."
            raise TypeError(message)
        if self.value is not None and type(self.value) not in VALUE_KINDS:
            message = "An evidence item's value must be a MoneyValue, RateValue, YearsValue, "
            message += "OtherValue or None."
            raise TypeError(message)
        if not is_a(self.context_only, bool):
            message = "An evidence item's context_only must be a bool."
            raise TypeError(message)
        if self.used_from_step is not None:
            check_int32(self.used_from_step, "An evidence item's used_from_step")
        if self.supersedes is not None and not is_a(self.supersedes, str):
            message = "An evidence item's supersedes must be a str or None."
            raise TypeError(message)


@dataclass(frozen=True, slots=True)
class HomeFacts:
    """Everything the engine needs to know about one home.

    ``mode`` is ``None`` when the data does not say; ``evidence`` is the home's own evidence plus
    the household's (deposit, rate, term, moving costs), a tuple; ``monthly_budget`` is the
    household's monthly budget.
    """

    home_id: str
    mode: Mode | None
    nation: Nation
    evidence: tuple[EvidenceItem, ...]
    monthly_budget: Pence

    def __post_init__(self) -> None:
        if not is_a(self.home_id, str):
            message = "A home's home_id must be a str."
            raise TypeError(message)
        if self.mode is not None and not is_a(self.mode, Mode):
            message = "A home's mode must be a Mode or None."
            raise TypeError(message)
        if not is_a(self.nation, Nation):
            message = "A home's nation must be a Nation."
            raise TypeError(message)
        if type(self.evidence) is not tuple or any(
            type(item) is not EvidenceItem for item in self.evidence
        ):
            message = "A home's evidence must be a tuple of EvidenceItem."
            raise TypeError(message)
        if not is_a(self.monthly_budget, Pence):
            message = "A home's monthly_budget must be a Pence."
            raise TypeError(message)
