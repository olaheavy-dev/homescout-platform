"""The shape of ``packages/fixtures/generated/costs.json`` (ported from the C# ``CostsDocument``).

The order of the fields of each class is the order of its keys in the file (the contract in
``schema/generated-costs.schema.json``); a test checks the two agree. A field that is ``None`` is
left out of the file. There is no ``float`` here: money is whole pence (``int``).
"""

from dataclasses import dataclass, fields, is_dataclass

type JsonValue = str | int | bool | list[JsonValue] | dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class FigureDocument:
    id: str
    pence: int


@dataclass(frozen=True, slots=True)
class MortgageDocument:
    id: str
    loan: FigureDocument
    rate_basis_points: int
    term_years: int
    payments: int
    monthly_repayment: FigureDocument
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LineDocument:
    id: str
    category: str
    status: str
    pence: int | None
    source_period: str | None
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PartialReasonDocument:
    line_id: str
    category: str
    status: str


@dataclass(frozen=True, slots=True)
class TotalDocument:
    id: str
    pence: int
    is_partial: bool
    partial_reasons: tuple[PartialReasonDocument, ...]


@dataclass(frozen=True, slots=True)
class BudgetDocument:
    id: str
    budget_pence: int
    budget_source: str
    difference_pence: int
    within_budget: bool
    based_on_partial_total: bool


@dataclass(frozen=True, slots=True)
class MonthlyDocument:
    lines: tuple[LineDocument, ...]
    total: TotalDocument
    budget: BudgetDocument


@dataclass(frozen=True, slots=True)
class UpfrontDocument:
    lines: tuple[LineDocument, ...]
    total: TotalDocument


@dataclass(frozen=True, slots=True)
class ChangeDocument:
    id: str
    category: str
    kind: str
    previous_evidence_ids: tuple[str, ...]
    current_evidence_ids: tuple[str, ...]
    monthly_difference_pence: int | None
    annual_difference_pence: int | None


@dataclass(frozen=True, slots=True)
class ScenarioDocument:
    scenario_id: str
    from_step: int
    to_step: int
    mortgage: MortgageDocument | None
    monthly: MonthlyDocument
    upfront: UpfrontDocument
    changes_from_previous: tuple[ChangeDocument, ...]
    monthly_total_change: FigureDocument | None


@dataclass(frozen=True, slots=True)
class HomeDocument:
    home_id: str
    mode: str | None
    nation: str
    coverage: str
    story_id: str | None
    scenarios: tuple[ScenarioDocument, ...]


@dataclass(frozen=True, slots=True)
class CostsDocument:
    """The whole file."""

    schema: str
    format_version: int
    generated_by: str
    snapshot_date: str
    money: str
    rounding: str
    homes: tuple[HomeDocument, ...]


def _key(field_name: str) -> str:
    """``snake_case`` field name to the file's ``camelCase`` key; ``schema`` is ``$schema``."""
    if field_name == "schema":
        return "$schema"
    first, *rest = field_name.split("_")
    return first + "".join(word.capitalize() for word in rest)


def to_json_value(value: object) -> JsonValue:
    """The document as plain dicts, lists, text, whole numbers and booleans, keys in field order."""
    if is_dataclass(value) and not isinstance(value, type):
        return {
            _key(f.name): to_json_value(getattr(value, f.name))
            for f in fields(value)
            if getattr(value, f.name) is not None
        }
    if isinstance(value, tuple):
        return [to_json_value(item) for item in value]
    if isinstance(value, bool | int | str):
        return value
    message = f"A value of type {type(value).__name__} cannot go into the costs file."
    raise TypeError(message)
