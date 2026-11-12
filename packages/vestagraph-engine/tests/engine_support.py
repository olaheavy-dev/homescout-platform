"""Shared test helpers: read the worked cases in story-calculations.json.

Expectations come only from that hand-worked file (decision 0034, AGENTS rule 2), never from the
engine. Decimals are read as exact ``Fraction`` values, so no float is ever involved.
"""

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from vestagraph_engine import Pence
from vestagraph_engine.cost_categories import category_id
from vestagraph_engine.cost_types import CostCategory, Mode, Period
from vestagraph_engine.line_input import (
    AmountLine,
    ConflictingLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)


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
