"""The evidence types check what they hold when they are built: a wrong type is a programming
error, so it raises ``TypeError`` (or ``ValueError`` for a 32-bit ``int`` out of range), never a
failed ``Result``."""

from typing import Any

import pytest
from engine_support import evidence_item, home_facts
from vestagraph_engine import Pence
from vestagraph_engine.cost_types import Mode, Period
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

INT32_MAX = 2**31 - 1
INT32_MIN = -(2**31)


@pytest.mark.parametrize(
    ("nation", "expected"),
    [
        (Nation.ENGLAND, "England"),
        (Nation.WALES, "Wales"),
        (Nation.SCOTLAND, "Scotland"),
        (Nation.NORTHERN_IRELAND, "Northern Ireland"),
    ],
)
def test_nation_each_nation_has_its_fixture_name(nation: Nation, expected: str) -> None:
    # The names in packages/fixtures/schema/common.schema.json (#/$defs/nation).
    assert nation.value == expected


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (EvidenceStatus.AVAILABLE, "available"),
        (EvidenceStatus.MISSING, "missing"),
        (EvidenceStatus.CONFLICTING, "conflicting"),
        (EvidenceStatus.STALE, "stale"),
        (EvidenceStatus.NOT_APPLICABLE, "not-applicable"),
        (EvidenceStatus.NOT_CALCULATED, "not-calculated"),
        (EvidenceStatus.INCLUDED, "included"),
    ],
)
def test_evidence_status_each_status_has_its_fixture_name(
    status: EvidenceStatus, expected: str
) -> None:
    # The names in packages/fixtures/schema/evidence.schema.json (status).
    assert status.value == expected


def test_nation_and_evidence_status_have_no_other_members() -> None:
    assert len(Nation) == 4
    assert len(EvidenceStatus) == 7


def test_money_value_keeps_its_amount_and_period() -> None:
    value = MoneyValue(Pence(100), Period.YEAR)

    assert value.amount == Pence(100)
    assert value.period == Period.YEAR


def test_money_value_amount_that_is_an_int_raises_type_error() -> None:
    with pytest.raises(TypeError, match="amount"):
        MoneyValue(100, Period.MONTH)  # type: ignore[arg-type]  # deliberately wrong


def test_money_value_period_that_is_a_string_raises_type_error() -> None:
    with pytest.raises(TypeError, match="period"):
        MoneyValue(Pence(100), "month")  # type: ignore[arg-type]  # deliberately wrong


def test_rate_value_keeps_its_basis_points() -> None:
    assert RateValue(550).basis_points == 550


@pytest.mark.parametrize("bad", [True, "550", Pence(550)])
def test_rate_value_basis_points_that_is_not_an_int_raises_type_error(bad: Any) -> None:
    with pytest.raises(TypeError, match="basis points"):
        RateValue(bad)


@pytest.mark.parametrize("bad", [INT32_MAX + 1, INT32_MIN - 1])
def test_rate_value_basis_points_outside_32_bits_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match="32-bit"):
        RateValue(bad)


@pytest.mark.parametrize("edge", [INT32_MAX, INT32_MIN, 0])
def test_rate_value_basis_points_at_the_32_bit_edges_is_accepted(edge: int) -> None:
    assert RateValue(edge).basis_points == edge


def test_years_value_keeps_its_years() -> None:
    assert YearsValue(25).years == 25


@pytest.mark.parametrize("bad", [False, "25", 25.0])
def test_years_value_years_that_is_not_an_int_raises_type_error(bad: Any) -> None:
    with pytest.raises(TypeError, match="years"):
        YearsValue(bad)


@pytest.mark.parametrize("bad", [INT32_MAX + 1, INT32_MIN - 1])
def test_years_value_years_outside_32_bits_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match="32-bit"):
        YearsValue(bad)


def test_other_value_carries_nothing_and_equals_another() -> None:
    assert OtherValue() == OtherValue()


def test_evidence_item_keeps_every_field() -> None:
    item = EvidenceItem(
        "E-1",
        "energy",
        EvidenceStatus.STALE,
        MoneyValue(Pence(9_000), Period.MONTH),
        True,
        4,
        "E-0",
    )

    assert item.id == "E-1"
    assert item.category == "energy"
    assert item.status == EvidenceStatus.STALE
    assert item.value == MoneyValue(Pence(9_000), Period.MONTH)
    assert item.context_only is True
    assert item.used_from_step == 4
    assert item.supersedes == "E-0"


def test_evidence_item_optional_fields_may_be_none() -> None:
    item = EvidenceItem("E-1", "energy", EvidenceStatus.MISSING, None, False, None, None)

    assert item.value is None
    assert item.used_from_step is None
    assert item.supersedes is None


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("id", 1),
        ("category", None),
        ("status", "available"),
        ("value", 9_000),
        ("context_only", 1),
        ("used_from_step", "4"),
        ("used_from_step", True),
        ("supersedes", 5),
    ],
)
def test_evidence_item_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    with pytest.raises(TypeError, match=field):
        evidence_item(**{field: bad})


@pytest.mark.parametrize("bad", [INT32_MAX + 1, INT32_MIN - 1])
def test_evidence_item_used_from_step_outside_32_bits_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match="32-bit"):
        evidence_item(used_from_step=bad)


def test_home_facts_keeps_every_field() -> None:
    item = evidence_item()
    facts = HomeFacts("T1", Mode.RENT, Nation.WALES, (item,), Pence(200_000))

    assert facts.home_id == "T1"
    assert facts.mode == Mode.RENT
    assert facts.nation == Nation.WALES
    assert facts.evidence == (item,)
    assert facts.monthly_budget == Pence(200_000)


def test_home_facts_mode_may_be_none() -> None:
    assert home_facts(mode=None).mode is None


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("home_id", 1),
        ("mode", "buy"),
        ("nation", "England"),
        ("evidence", None),
        ("evidence", [evidence_item()]),
        ("evidence", (evidence_item(), "not evidence")),
        ("monthly_budget", 200_000),
    ],
)
def test_home_facts_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    with pytest.raises(TypeError, match=field):
        home_facts(**{field: bad})
