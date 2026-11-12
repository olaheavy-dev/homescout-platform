"""Shared test helpers: read the worked cases in story-calculations.json.

Expectations come only from that hand-worked file (decision 0034, AGENTS rule 2), never from the
engine. Decimals are read as exact ``Fraction`` values, so no float is ever involved.
"""

import json
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_engine import Pence
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import CostCategory, Mode, Period
from vestagraph_engine.evidence import (
    EvidenceItem,
    EvidenceStatus,
    HomeFacts,
    MoneyValue,
    Nation,
    OtherValue,
    RateValue,
    YearsValue,
)
from vestagraph_engine.line_input import (
    AmountLine,
    ConflictingLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.selected_inputs import SelectedInputs


def repository_root() -> Path:
    for folder in Path(__file__).resolve().parents:
        if (folder / "packages" / "fixtures" / "test-cases").is_dir():
            return folder
    message = "Repository root not found above the test helper."
    raise FileNotFoundError(message)


def _load() -> list[dict[str, Any]]:
    path = repository_root() / "packages" / "fixtures" / "test-cases" / "story-calculations.json"
    document = json.loads(path.read_text(encoding="utf-8"), parse_float=Fraction)
    cases: list[dict[str, Any]] = document["cases"]
    return cases


CASES: list[dict[str, Any]] = _load()


def case(case_id: str) -> dict[str, Any]:
    matches = [c for c in CASES if c["id"] == case_id]
    assert len(matches) == 1, f"expected exactly one case {case_id}"
    return matches[0]


def case_ids_where(key: str, *, inside: str = "inputs") -> list[str]:
    """The ids of the cases whose ``inside`` section has ``key``."""
    return [c["id"] for c in CASES if key in c[inside]]


def basis_points(annual_rate: str) -> int:
    """Read a rate such as "0.055" as whole basis points (550); a fractional basis point fails."""
    exact = Fraction(annual_rate) * 10_000
    assert exact.denominator == 1, "The rate is not a whole number of basis points."
    return exact.numerator


def mode_of(story_case: dict[str, Any]) -> Mode:
    """The mode of the home a monthly case is about (B1 and B2 are bought, R1 and R2 rented)."""
    modes = {"B1": Mode.BUY, "B2": Mode.BUY, "R1": Mode.RENT, "R2": Mode.RENT}
    return modes[story_case["inputs"]["home"]]


def budget_of(story_case: dict[str, Any]) -> Pence:
    return Pence(story_case["inputs"]["budgetPence"])


def category_from_id(category_id_text: str) -> CostCategory:
    matches = [c for c in CostCategory if category_id(c) == category_id_text]
    assert len(matches) == 1, f"unknown category {category_id_text}"
    return matches[0]


def _line(line: dict[str, Any]) -> LineInput:
    category = category_from_id(line["category"])

    if "mortgageCase" in line:
        # The amount is the referenced case's independently worked result, not the engine's output.
        repayment = case(line["mortgageCase"])["expected"]["monthlyRepaymentPence"]
        return AmountLine(category, Pence(repayment), Period.MONTH, ())

    if "status" in line:
        status = line["status"]
        if status == "included":
            return IncludedLine(category, ())
        if status == "not-calculated":
            return NotCalculatedLine(category, ())
        if status == "conflicting":
            return ConflictingLine(category, ())
        assert status == "missing", f"unknown line status {status}"
        return MissingLine(category)

    periods = {"once": Period.ONCE, "month": Period.MONTH, "year": Period.YEAR}
    return AmountLine(category, Pence(line["amountPence"]), periods[line["period"]], ())


def lines_of(story_case: dict[str, Any]) -> list[LineInput]:
    return [_line(line) for line in story_case["inputs"]["lines"]]


# Small builders for the evidence the assumption selector reads (ported from the C# TestFacts).
# The amounts here are arbitrary inputs: the selector tests check which item is chosen and which
# kind of line results, never a calculated figure.


def money(
    item_id: str,
    category: str,
    pence: int,
    period: Period,
    status: EvidenceStatus = EvidenceStatus.AVAILABLE,
    *,
    used_from_step: int | None = None,
    supersedes: str | None = None,
    context_only: bool = False,
) -> EvidenceItem:
    return EvidenceItem(
        item_id,
        category,
        status,
        MoneyValue(Pence(pence), period),
        context_only,
        used_from_step,
        supersedes,
    )


def no_value(
    item_id: str,
    category: str,
    status: EvidenceStatus,
    *,
    used_from_step: int | None = None,
    supersedes: str | None = None,
) -> EvidenceItem:
    return EvidenceItem(item_id, category, status, None, False, used_from_step, supersedes)


def other(item_id: str, category: str, status: EvidenceStatus) -> EvidenceItem:
    return EvidenceItem(item_id, category, status, OtherValue(), False, None, None)


def rate(item_id: str, basis_points_value: int) -> EvidenceItem:
    return EvidenceItem(
        item_id,
        "mortgage-rate",
        EvidenceStatus.AVAILABLE,
        RateValue(basis_points_value),
        False,
        None,
        None,
    )


def years(item_id: str, term_years: int) -> EvidenceItem:
    return EvidenceItem(
        item_id,
        "mortgage-term",
        EvidenceStatus.AVAILABLE,
        YearsValue(term_years),
        False,
        None,
        None,
    )


def buy_anchors() -> list[EvidenceItem]:
    """The four inputs a purchase needs before anything can be worked out."""
    return [
        money("PRICE", "asking-price", 20_000_000, Period.ONCE),
        money("DEPOSIT", "mortgage-deposit", 4_000_000, Period.ONCE),
        rate("RATE", 500),
        years("TERM", 20),
    ]


def anchors_except(category: str, *replacement: EvidenceItem) -> list[EvidenceItem]:
    """The purchase anchors with one category taken out and (optionally) another item put in."""
    return [item for item in buy_anchors() if item.category != category] + list(replacement)


def buying(extra: Iterable[EvidenceItem], nation: Nation = Nation.ENGLAND) -> HomeFacts:
    return HomeFacts("T1", Mode.BUY, nation, (*buy_anchors(), *extra), Pence(200_000))


def renting(evidence: Iterable[EvidenceItem], nation: Nation = Nation.ENGLAND) -> HomeFacts:
    return HomeFacts("T2", Mode.RENT, nation, tuple(evidence), Pence(200_000))


def buying_from(evidence: Iterable[EvidenceItem], budget: Pence | None = None) -> HomeFacts:
    """A purchase with exactly this evidence (no anchors added); the budget is 200,000p."""
    return HomeFacts(
        "T1",
        Mode.BUY,
        Nation.ENGLAND,
        tuple(evidence),
        Pence(200_000) if budget is None else budget,
    )


def evidence_item(**overrides: Any) -> EvidenceItem:
    """A valid item with any field replaced (the value may be deliberately the wrong type)."""
    fields: dict[str, Any] = {
        "id": "E-1",
        "category": "energy",
        "status": EvidenceStatus.AVAILABLE,
        "value": MoneyValue(Pence(9_000), Period.MONTH),
        "context_only": False,
        "used_from_step": None,
        "supersedes": None,
    }
    fields.update(overrides)
    return EvidenceItem(**fields)


def home_facts(**overrides: Any) -> HomeFacts:
    """A valid home with any field replaced (the value may be deliberately the wrong type)."""
    fields: dict[str, Any] = {
        "home_id": "T1",
        "mode": Mode.BUY,
        "nation": Nation.ENGLAND,
        "evidence": (evidence_item(),),
        "monthly_budget": Pence(200_000),
    }
    fields.update(overrides)
    return HomeFacts(**fields)


def monthly_line(inputs: SelectedInputs, category: CostCategory) -> LineInput | None:
    matches = [line for line in inputs.monthly_lines if line.category == category]
    assert len(matches) <= 1, f"more than one {category} line"
    return matches[0] if matches else None


def upfront_line(inputs: SelectedInputs, category: CostCategory) -> LineInput | None:
    matches = [line for line in inputs.upfront_lines if line.category == category]
    assert len(matches) <= 1, f"more than one {category} line"
    return matches[0] if matches else None
