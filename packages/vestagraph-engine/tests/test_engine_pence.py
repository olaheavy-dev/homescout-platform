"""Tests for Pence, ported from the C# PenceTests. Expected values are hand-worked literals."""

from fractions import Fraction

import pytest
from vestagraph_engine import Pence

MAX = 2**63 - 1
MIN = -(2**63)


def test_zero_default_equals_pence_of_zero() -> None:
    assert Pence(0) == Pence.ZERO
    assert Pence.ZERO.value == 0


def test_add_two_amounts_returns_sum() -> None:
    assert Pence(250) + Pence(75) == Pence(325)


def test_add_negative_amount_reduces_total() -> None:
    assert Pence(250).add(Pence(-300)) == Pence(-50)


def test_subtract_two_amounts_returns_difference() -> None:
    assert Pence(250) - Pence(300) == Pence(-50)


def test_subtract_method_form_matches_operator() -> None:
    assert Pence(250).subtract(Pence(300)) == Pence(250) - Pence(300)


def test_negate_positive_returns_negative() -> None:
    assert -Pence(125) == Pence(-125)


def test_negate_negative_returns_positive() -> None:
    assert Pence(-125).negate() == Pence(125)


def test_negate_zero_returns_zero() -> None:
    assert -Pence.ZERO == Pence.ZERO


def test_multiply_by_whole_number_returns_product() -> None:
    assert Pence(1500) * 12 == Pence(18000)
    assert 12 * Pence(1500) == Pence(18000)
    assert Pence(1500).multiply(-2) == Pence(-3000)


def test_compare_smaller_and_larger_orders_by_value() -> None:
    assert Pence(-5) < Pence(3)
    assert Pence(3) > Pence(-5)
    assert not Pence(3) < Pence(3)
    assert not Pence(3) > Pence(3)


def test_comparison_operators_various_pairs_follow_value_order() -> None:
    assert Pence(1) < Pence(2)
    assert Pence(2) > Pence(1)
    assert Pence(2) <= Pence(1 + 1)
    assert not Pence(2) >= Pence(3)


def test_equals_same_value_is_equal() -> None:
    first = Pence(7)
    second = Pence(3) + Pence(4)
    assert first == second
    assert hash(first) == hash(second)


def test_comparison_equal_amounts_are_not_strictly_less_or_greater() -> None:
    a = Pence(500)
    b = Pence(500)
    assert not a < b
    assert not a > b
    assert a <= b
    assert a >= b


def test_add_overflow_raises_overflow_error() -> None:
    with pytest.raises(OverflowError):
        Pence(MAX) + Pence(1)


def test_subtract_overflow_raises_overflow_error() -> None:
    with pytest.raises(OverflowError):
        Pence(MIN) - Pence(1)


def test_negate_min_value_raises_overflow_error() -> None:
    with pytest.raises(OverflowError):
        -Pence(MIN)


def test_multiply_overflow_raises_overflow_error() -> None:
    with pytest.raises(OverflowError):
        Pence(MAX) * 2
    with pytest.raises(OverflowError):
        2 * Pence(MAX)


@pytest.mark.parametrize("value", [MAX + 1, MIN - 1])
def test_constructor_outside_64_bit_range_raises_overflow_error(value: int) -> None:
    with pytest.raises(OverflowError):
        Pence(value)


def test_constructor_range_ends_are_accepted() -> None:
    assert Pence(MAX).value == MAX
    assert Pence(MIN).value == MIN


@pytest.mark.parametrize("value", [True, 1.0, Fraction(1), "1", None])
def test_constructor_non_int_value_raises_type_error(value: object) -> None:
    with pytest.raises(TypeError):
        Pence(value)  # type: ignore[arg-type]  # deliberately wrong types


def test_add_plain_int_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Pence(1) + 3  # type: ignore[operator]  # deliberately mixing types
    with pytest.raises(TypeError):
        3 + Pence(1)  # type: ignore[operator]  # deliberately mixing types


@pytest.mark.parametrize("factor", [True, 1.5, Fraction(1, 2)])
def test_multiply_non_int_factor_raises_type_error(factor: object) -> None:
    with pytest.raises(TypeError):
        Pence(10) * factor  # type: ignore[operator]  # deliberately wrong types


def test_multiply_pence_by_pence_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Pence(2) * Pence(3)  # type: ignore[operator]  # money times money has no meaning


def test_from_exact_whole_number_is_unchanged() -> None:
    assert Pence.from_exact(Fraction(1234)) == Pence(1234)
    assert Pence.from_exact(1234) == Pence(1234)


def test_from_exact_half_penny_is_not_bankers_rounding() -> None:
    # Banker's rounding would give 2 and -2 for these.
    assert Pence.from_exact(Fraction(5, 2)) == Pence(3)
    assert Pence.from_exact(Fraction(-5, 2)) == Pence(-3)


def test_from_exact_amount_too_large_raises_overflow_error() -> None:
    with pytest.raises(OverflowError):
        Pence.from_exact(Fraction(10**30))


@pytest.mark.parametrize("amount", [1.5, True, "1"])
def test_from_exact_non_fraction_raises_type_error(amount: object) -> None:
    with pytest.raises(TypeError):
        Pence.from_exact(amount)  # type: ignore[arg-type]  # deliberately wrong types


def test_annual_to_monthly_min_value_does_not_overflow() -> None:
    assert Pence(MIN).annual_to_monthly().value == -768614336404564651


def test_annual_to_monthly_max_value_does_not_overflow() -> None:
    # 12 x 768614336404564650 + 7, and 7/12 is more than half, so it rounds up.
    assert Pence(MAX).annual_to_monthly().value == 768614336404564651


def test_annual_to_monthly_exact_multiple_of_twelve_is_exact() -> None:
    assert Pence(240000).annual_to_monthly() == Pence(20000)


def test_multiply_method_bool_factor_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Pence(10).multiply(True)


def test_subtract_plain_int_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Pence(1) - 3  # type: ignore[operator]  # deliberately mixing types
