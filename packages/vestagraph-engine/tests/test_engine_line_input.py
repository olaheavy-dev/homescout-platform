"""The fields of each line kind are checked when the line is built (a wrong type is a programming
error, so it raises ``TypeError`` rather than becoming a failed ``Result``)."""

import pytest
from vestagraph_engine import (
    AmountLine,
    ConflictingLine,
    CostCategory,
    IncludedLine,
    MissingLine,
    NotCalculatedLine,
    Pence,
    Period,
)

RENT = CostCategory.RENT


def test_amount_line_period_that_is_a_string_raises_type_error() -> None:
    with pytest.raises(TypeError, match="period"):
        AmountLine(RENT, Pence(120_000), "month", ())  # type: ignore[arg-type]  # deliberately wrong


def test_amount_line_amount_that_is_an_int_raises_type_error() -> None:
    with pytest.raises(TypeError, match="amount"):
        AmountLine(RENT, 120_000, Period.MONTH, ())  # type: ignore[arg-type]  # deliberately wrong


def test_amount_line_category_that_is_a_string_raises_type_error() -> None:
    with pytest.raises(TypeError, match="category"):
        AmountLine("rent", Pence(120_000), Period.MONTH, ())  # type: ignore[arg-type]  # deliberately wrong


def test_amount_line_evidence_ids_that_are_a_list_raise_type_error() -> None:
    with pytest.raises(TypeError, match="evidence_ids"):
        AmountLine(RENT, Pence(120_000), Period.MONTH, ["E1"])  # type: ignore[arg-type]  # deliberately wrong


def test_amount_line_evidence_ids_holding_a_non_string_raise_type_error() -> None:
    with pytest.raises(TypeError, match="evidence_ids"):
        AmountLine(RENT, Pence(120_000), Period.MONTH, (1,))  # type: ignore[arg-type]  # deliberately wrong


@pytest.mark.parametrize("kind", [IncludedLine, NotCalculatedLine, ConflictingLine])
def test_lines_without_an_amount_check_category_and_evidence_ids(kind: type) -> None:
    assert kind(RENT, ("E1",)).evidence_ids == ("E1",)
    with pytest.raises(TypeError, match="category"):
        kind("rent", ())
    with pytest.raises(TypeError, match="evidence_ids"):
        kind(RENT, ["E1"])


def test_missing_line_category_that_is_a_string_raises_type_error() -> None:
    assert MissingLine(RENT).evidence_ids == ()
    with pytest.raises(TypeError, match="category"):
        MissingLine("rent")  # type: ignore[arg-type]  # deliberately wrong
