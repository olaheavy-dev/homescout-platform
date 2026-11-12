"""The selector's output types check what they hold; the signature says when two steps use the
same evidence in the same way (ported from the C# ``SelectedInputs.Signature``)."""

from typing import Any

import pytest
from vestagraph_engine import Pence
from vestagraph_engine.cost_types import CostCategory, Mode, Period
from vestagraph_engine.line_input import (
    AmountLine,
    IncludedLine,
    LineInput,
    MissingLine,
    NotCalculatedLine,
)
from vestagraph_engine.selected_inputs import MortgageInputs, SelectedInputs

IDS = ("PRICE", "DEPOSIT", "RATE", "TERM")


def _mortgage(ids: tuple[str, ...] = IDS) -> MortgageInputs:
    return MortgageInputs(Pence(20_000_000), Pence(4_000_000), 500, 20, ids)


def _energy(pence: int, item_id: str = "EN") -> AmountLine:
    return AmountLine(CostCategory.ENERGY, Pence(pence), Period.MONTH, (item_id,))


def _inputs(
    *,
    mode: Mode = Mode.BUY,
    mortgage: MortgageInputs | None = None,
    monthly: tuple[LineInput, ...] = (),
    upfront: tuple[LineInput, ...] = (),
) -> SelectedInputs:
    return SelectedInputs(mode, mortgage, monthly, upfront)


def test_mortgage_inputs_keep_every_field() -> None:
    mortgage = _mortgage()

    assert mortgage.asking_price == Pence(20_000_000)
    assert mortgage.deposit == Pence(4_000_000)
    assert mortgage.rate_basis_points == 500
    assert mortgage.term_years == 20
    assert mortgage.evidence_ids == IDS


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("asking_price", 20_000_000),
        ("deposit", None),
        ("rate_basis_points", "500"),
        ("rate_basis_points", True),
        ("term_years", 20.0),
        ("evidence_ids", list(IDS)),
        ("evidence_ids", ("PRICE", 2)),
    ],
)
def test_mortgage_inputs_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    fields: dict[str, Any] = {
        "asking_price": Pence(20_000_000),
        "deposit": Pence(4_000_000),
        "rate_basis_points": 500,
        "term_years": 20,
        "evidence_ids": IDS,
    }
    fields[field] = bad

    with pytest.raises(TypeError, match=field):
        MortgageInputs(**fields)


@pytest.mark.parametrize("field", ["rate_basis_points", "term_years"])
@pytest.mark.parametrize("bad", [2**31, -(2**31) - 1])
def test_mortgage_inputs_number_outside_32_bits_raises_value_error(field: str, bad: int) -> None:
    fields: dict[str, Any] = {"rate_basis_points": 500, "term_years": 20}
    fields[field] = bad

    with pytest.raises(ValueError, match="32-bit"):
        MortgageInputs(Pence(2), Pence(1), evidence_ids=IDS, **fields)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("mode", "buy"),
        ("mortgage", "mortgage"),
        ("monthly_lines", [_energy(9_000)]),
        ("monthly_lines", (None,)),
        ("upfront_lines", [MissingLine(CostCategory.MOVING_COSTS)]),
        ("upfront_lines", ("moving-costs",)),
    ],
)
def test_selected_inputs_field_of_the_wrong_type_raises_type_error(field: str, bad: Any) -> None:
    fields: dict[str, Any] = {
        "mode": Mode.BUY,
        "mortgage": None,
        "monthly_lines": (),
        "upfront_lines": (),
    }
    fields[field] = bad

    with pytest.raises(TypeError, match=field):
        SelectedInputs(**fields)


def test_signature_same_evidence_in_the_same_way_gives_the_same_text() -> None:
    first = _inputs(mortgage=_mortgage(), monthly=(_energy(9_000),))
    second = _inputs(mortgage=_mortgage(), monthly=(_energy(9_000),))

    assert first.signature() == second.signature()


def test_signature_same_evidence_with_another_amount_gives_the_same_text() -> None:
    # The evidence ids decide the figures, so the amounts are not part of the signature.
    assert (
        _inputs(monthly=(_energy(9_000),)).signature()
        == _inputs(monthly=(_energy(9_500),)).signature()
    )


def test_signature_another_evidence_id_gives_another_text() -> None:
    assert (
        _inputs(monthly=(_energy(9_000, "EN-1"),)).signature()
        != _inputs(monthly=(_energy(9_000, "EN-2"),)).signature()
    )


def test_signature_another_kind_of_line_for_the_same_evidence_gives_another_text() -> None:
    included = _inputs(monthly=(IncludedLine(CostCategory.ENERGY, ("EN",)),))
    not_calculated = _inputs(monthly=(NotCalculatedLine(CostCategory.ENERGY, ("EN",)),))

    assert included.signature() != not_calculated.signature()


def test_signature_another_category_gives_another_text() -> None:
    water = AmountLine(CostCategory.WATER, Pence(9_000), Period.MONTH, ("EN",))

    assert _inputs(monthly=(_energy(9_000),)).signature() != _inputs(monthly=(water,)).signature()


def test_signature_another_mortgage_evidence_gives_another_text() -> None:
    other_ids = ("PRICE", "DEPOSIT", "RATE-2", "TERM")

    assert (
        _inputs(mortgage=_mortgage()).signature()
        != _inputs(mortgage=_mortgage(other_ids)).signature()
    )


def test_signature_with_and_without_a_mortgage_gives_another_text() -> None:
    assert _inputs(mortgage=_mortgage()).signature() != _inputs().signature()


def test_signature_another_mode_gives_another_text() -> None:
    assert _inputs(mode=Mode.BUY).signature() != _inputs(mode=Mode.RENT).signature()


def test_signature_a_line_with_no_evidence_is_told_apart_from_a_line_that_is_left_out() -> None:
    missing = _inputs(monthly=(MissingLine(CostCategory.BROADBAND),))

    assert missing.signature() != _inputs().signature()


def test_signature_the_order_of_a_lines_evidence_ids_matters() -> None:
    first = _inputs(
        monthly=(IncludedLine(CostCategory.WATER, ("A", "B")),),
    )
    second = _inputs(
        monthly=(IncludedLine(CostCategory.WATER, ("B", "A")),),
    )

    assert first.signature() != second.signature()
