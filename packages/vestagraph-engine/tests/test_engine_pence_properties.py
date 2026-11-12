"""Property tests for Pence, ported from the C# PenceProperties (FsCheck becomes Hypothesis).

Hypothesis loads its built-in `ci` profile itself when it detects a CI run (checked in the locked
version, 6.170.15); no profile is registered here.
"""

from fractions import Fraction

from hypothesis import given
from hypothesis import strategies as st
from vestagraph_engine import Pence

INT32 = st.integers(min_value=-(2**31), max_value=2**31 - 1)
INT64 = st.integers(min_value=-(2**63), max_value=2**63 - 1)
_MAX_PENNIES = 10**15

PENNIES = st.one_of(
    st.integers(-1000, 1000),
    INT32,
    st.sampled_from([-_MAX_PENNIES, _MAX_PENNIES, 0]),
)
THOUSANDTHS = st.one_of(st.integers(0, 999), st.sampled_from([0, 499, 500, 501, 999]))
EXACT = st.builds(lambda p, t: Fraction(p) + Fraction(t, 1000), PENNIES, THOUSANDTHS)


def _abs(value: Fraction) -> Fraction:
    return value if value >= 0 else -value


@given(INT64)
def test_from_exact_whole_pence_is_idempotent(n: int) -> None:
    assert Pence.from_exact(Fraction(n)).value == n


@given(EXACT)
def test_from_exact_applied_twice_equals_applied_once(amount: Fraction) -> None:
    once = Pence.from_exact(amount)
    assert Pence.from_exact(Fraction(once.value)) == once


@given(EXACT)
def test_from_exact_negated_input_is_negated_result(amount: Fraction) -> None:
    assert Pence.from_exact(-amount) == -Pence.from_exact(amount)


@given(EXACT)
def test_from_exact_any_input_is_within_half_a_penny_of_the_input(amount: Fraction) -> None:
    assert _abs(Pence.from_exact(amount).value - amount) <= Fraction(1, 2)


@given(INT32)
def test_from_exact_exact_half_rounds_away_from_zero(whole: int) -> None:
    n = abs(whole)
    assert Pence.from_exact(n + Fraction(1, 2)).value == n + 1
    assert Pence.from_exact(-n - Fraction(1, 2)).value == -n - 1


@given(INT32)
def test_annual_to_monthly_twelve_times_monthly_returns_monthly(monthly: int) -> None:
    assert Pence(12 * monthly).annual_to_monthly() == Pence(monthly)


@given(INT32)
def test_annual_to_monthly_negated_input_is_negated_result(annual: int) -> None:
    amount = Pence(annual)
    assert (-amount).annual_to_monthly() == -amount.annual_to_monthly()


@given(INT32)
def test_annual_to_monthly_any_input_is_the_nearest_penny_to_the_exact_quotient(
    annual: int,
) -> None:
    # An oracle written here, not a second call to round_ratio: the result is within half a penny
    # of annual / 12, and when it is exactly half a penny away the choice is the one away from zero.
    exact = Fraction(annual, 12)
    monthly = Pence(annual).annual_to_monthly().value
    distance = abs(Fraction(monthly) - exact)
    assert distance <= Fraction(1, 2)
    if distance == Fraction(1, 2):
        assert abs(monthly) > abs(exact)


@given(INT32, INT32, INT32)
def test_add_three_amounts_is_associative(a: int, b: int, c: int) -> None:
    x, y, z = Pence(a), Pence(b), Pence(c)
    assert (x + y) + z == x + (y + z)


@given(INT32, INT32)
def test_add_two_amounts_is_commutative(a: int, b: int) -> None:
    x, y = Pence(a), Pence(b)
    assert x + y == y + x


@given(INT32)
def test_add_negated_amount_returns_zero(a: int) -> None:
    x = Pence(a)
    assert x + (-x) == Pence.ZERO


@given(INT32, INT32)
def test_subtract_amount_equals_adding_the_negation(a: int, b: int) -> None:
    x, y = Pence(a), Pence(b)
    assert x - y == x + (-y)


@given(INT32, INT32)
def test_compare_two_amounts_agrees_with_sign(a: int, b: int) -> None:
    assert (Pence(a) < Pence(b)) == (a < b)
    assert (Pence(a) > Pence(b)) == (a > b)
    assert (Pence(a) == Pence(b)) == (a == b)
