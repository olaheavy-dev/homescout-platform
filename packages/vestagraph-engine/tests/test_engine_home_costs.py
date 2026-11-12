"""The result types of the home cost builder check what they hold when they are built: a wrong
type is a programming error, so it raises ``TypeError`` (``ValueError`` for a 32-bit ``int`` out
of range), never a failed ``Result``."""

from typing import Any

import pytest
from vestagraph_engine import MortgageRepayment, Pence
from vestagraph_engine.breakdowns import MonthlyBreakdown, UpfrontBreakdown
from vestagraph_engine.cost_types import CostCategory, Mode
from vestagraph_engine.evidence import Nation
from vestagraph_engine.home_costs import (
    ChangeKind,
    CostChange,
    HomeCosts,
    MortgageSummary,
    ScenarioCosts,
)

MONTHLY = MonthlyBreakdown((), Pence.ZERO, False, (), Pence(1), Pence(1), True, False)
UPFRONT = UpfrontBreakdown((), Pence.ZERO, False, ())
REPAYMENT = MortgageRepayment(Pence(100), 500, 20, 240, Pence(1))


def _change(**overrides: Any) -> CostChange:
    fields: dict[str, Any] = {
        "category": CostCategory.ENERGY,
        "kind": ChangeKind.VALUE_CHANGED,
        "previous_evidence_ids": ("A",),
        "current_evidence_ids": ("B",),
        "monthly_difference": Pence(5),
        "annual_difference": None,
    }
    fields.update(overrides)
    return CostChange(**fields)


def _scenario(**overrides: Any) -> ScenarioCosts:
    fields: dict[str, Any] = {
        "scenario_id": "from-step-1",
        "from_step": 1,
        "to_step": 3,
        "mortgage": None,
        "monthly": MONTHLY,
        "upfront": UPFRONT,
        "changes": (),
        "monthly_total_change": None,
    }
    fields.update(overrides)
    return ScenarioCosts(**fields)


def _home(**overrides: Any) -> HomeCosts:
    fields: dict[str, Any] = {
        "home_id": "B1",
        "mode": Mode.BUY,
        "nation": Nation.ENGLAND,
        "scenarios": (_scenario(),),
    }
    fields.update(overrides)
    return HomeCosts(**fields)


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        (ChangeKind.VALUE_CHANGED, "value-changed"),
        (ChangeKind.EVIDENCE_CHANGED, "evidence-changed"),
        (ChangeKind.NO_LONGER_APPLIES, "no-longer-applies"),
        (ChangeKind.NOW_CALCULATED, "now-calculated"),
        (ChangeKind.NO_LONGER_CALCULATED, "no-longer-calculated"),
    ],
)
def test_change_kind_each_kind_has_its_generated_file_name(kind: ChangeKind, expected: str) -> None:
    # The names used in packages/fixtures/generated/costs.json.
    assert kind.value == expected


def test_change_kind_has_no_other_members() -> None:
    assert len(ChangeKind) == 5


def test_cost_change_keeps_every_field() -> None:
    change = _change(annual_difference=Pence(60))

    assert change.category == CostCategory.ENERGY
    assert change.kind == ChangeKind.VALUE_CHANGED
    assert change.previous_evidence_ids == ("A",)
    assert change.current_evidence_ids == ("B",)
    assert change.monthly_difference == Pence(5)
    assert change.annual_difference == Pence(60)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("category", "energy"),
        ("kind", "value-changed"),
        ("previous_evidence_ids", ["A"]),
        ("previous_evidence_ids", ("A", 1)),
        ("current_evidence_ids", None),
        ("monthly_difference", 5),
        ("annual_difference", 60),
    ],
)
def test_cost_change_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    with pytest.raises(TypeError, match=field):
        _change(**{field: bad})


def test_mortgage_summary_keeps_its_repayment_and_evidence() -> None:
    summary = MortgageSummary(REPAYMENT, ("P", "D", "R", "T"))

    assert summary.repayment == REPAYMENT
    assert summary.evidence_ids == ("P", "D", "R", "T")


@pytest.mark.parametrize(
    ("field", "bad"),
    [("repayment", Pence(1)), ("evidence_ids", ["P"]), ("evidence_ids", (1,))],
)
def test_mortgage_summary_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    fields: dict[str, Any] = {"repayment": REPAYMENT, "evidence_ids": ("P",)}
    fields[field] = bad

    with pytest.raises(TypeError, match=field):
        MortgageSummary(**fields)


def test_scenario_costs_keeps_every_field() -> None:
    summary = MortgageSummary(REPAYMENT, ("P", "D", "R", "T"))
    change = _change()
    scenario = _scenario(
        mortgage=summary, changes=(change,), monthly_total_change=Pence(-7), from_step=2, to_step=2
    )

    assert scenario.scenario_id == "from-step-1"
    assert (scenario.from_step, scenario.to_step) == (2, 2)
    assert scenario.mortgage == summary
    assert scenario.monthly == MONTHLY
    assert scenario.upfront == UPFRONT
    assert scenario.changes == (change,)
    assert scenario.monthly_total_change == Pence(-7)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("scenario_id", 1),
        ("from_step", "1"),
        ("from_step", True),
        ("to_step", 3.0),
        ("mortgage", REPAYMENT),
        ("monthly", UPFRONT),
        ("upfront", MONTHLY),
        ("changes", [_change()]),
        ("changes", (_change(), "change")),
        ("monthly_total_change", 7),
    ],
)
def test_scenario_costs_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    with pytest.raises(TypeError, match=field):
        _scenario(**{field: bad})


@pytest.mark.parametrize("field", ["from_step", "to_step"])
@pytest.mark.parametrize("bad", [2**31, -(2**31) - 1])
def test_scenario_costs_step_outside_32_bits_raises_value_error(field: str, bad: int) -> None:
    with pytest.raises(ValueError, match="32-bit"):
        _scenario(**{field: bad})


def test_home_costs_keeps_every_field() -> None:
    scenario = _scenario()
    home = _home(scenarios=(scenario,), mode=Mode.RENT, nation=Nation.WALES, home_id="R1")

    assert home.home_id == "R1"
    assert home.mode == Mode.RENT
    assert home.nation == Nation.WALES
    assert home.scenarios == (scenario,)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("home_id", 1),
        ("mode", "buy"),
        ("mode", None),
        ("nation", "England"),
        ("scenarios", [_scenario()]),
        ("scenarios", (_scenario(), 1)),
    ],
)
def test_home_costs_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    with pytest.raises(TypeError, match=field):
        _home(**{field: bad})
