"""Tests for round_ratio, ported from the C# RoundRatioTests (decisions 0021, 0034)."""

import pytest
from vestagraph_engine import Pence, round_ratio


@pytest.mark.parametrize(
    ("numerator", "denominator", "expected_pence"),
    [
        (1, 2, 1),
        (-1, 2, -1),
        (1, -2, -1),
        (-1, -2, 1),
        (3, 2, 2),
        (5, 2, 3),
        (-5, 2, -3),
        (7, 3, 2),
        (-7, 3, -2),
        (0, 7, 0),
    ],
)
def test_round_ratio_signs_and_halves_round_away_from_zero(
    numerator: int, denominator: int, expected_pence: int
) -> None:
    assert round_ratio(numerator, denominator) == Pence(expected_pence)


def test_round_ratio_large_exact_half_rounds_away_from_zero_without_losing_precision() -> None:
    # (2n + 1) / 2 is exactly n + 0.5, so the answer is n + 1 (and -(n + 1)).
    # 2n + 1 is already too big for a signed 64-bit integer.
    n = 4_000_000_000_000_000_000
    assert round_ratio(2 * n + 1, 2) == Pence(4_000_000_000_000_000_001)
    assert round_ratio(-(2 * n + 1), 2) == Pence(-4_000_000_000_000_000_001)


def test_round_ratio_result_too_big_for_64_bit_raises_overflow() -> None:
    with pytest.raises(OverflowError):
        round_ratio(10**30, 1)


def test_round_ratio_result_too_small_for_64_bit_raises_overflow() -> None:
    with pytest.raises(OverflowError):
        round_ratio(-(10**30), 1)


def test_round_ratio_zero_denominator_raises_zero_division() -> None:
    with pytest.raises(ZeroDivisionError):
        round_ratio(1, 0)


@pytest.mark.parametrize(("numerator", "denominator"), [(True, 2), (1, True), (1.0, 2), (1, 2.0)])
def test_round_ratio_non_int_argument_raises_type_error(
    numerator: object, denominator: object
) -> None:
    with pytest.raises(TypeError):
        round_ratio(numerator, denominator)  # type: ignore[arg-type]  # deliberately wrong types
