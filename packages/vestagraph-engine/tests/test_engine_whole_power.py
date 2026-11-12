"""Tests for whole_power: a whole-number power with a variable exponent (register line BE-32).

The architecture test forbids ``**`` with a variable exponent, so the engine multiplies in a loop.
Expected values are small hand-worked powers.
"""

import pytest
from vestagraph_engine import whole_power


@pytest.mark.parametrize(
    ("base", "exponent", "expected"),
    [
        (2, 0, 1),
        (0, 0, 1),
        (7, 1, 7),
        (2, 10, 1024),
        (3, 5, 243),
        (-2, 3, -8),
        (-2, 4, 16),
        (0, 5, 0),
        (1, 1200, 1),
        (10, 20, 100_000_000_000_000_000_000),
    ],
)
def test_whole_power_small_cases_match_hand_worked_values(
    base: int, exponent: int, expected: int
) -> None:
    assert whole_power(base, exponent) == expected


def test_whole_power_result_beyond_64_bits_is_exact() -> None:
    # 2^100 = 1267650600228229401496703205376, worked by hand from 2^10 = 1024 (1024^10).
    assert whole_power(2, 100) == 1_267_650_600_228_229_401_496_703_205_376


def test_whole_power_negative_exponent_raises_value_error() -> None:
    with pytest.raises(ValueError, match="negative"):
        whole_power(2, -1)


@pytest.mark.parametrize(("base", "exponent"), [(True, 2), (2, True), (2.0, 2), (2, 2.0), ("2", 2)])
def test_whole_power_non_int_argument_raises_type_error(base: object, exponent: object) -> None:
    with pytest.raises(TypeError):
        whole_power(base, exponent)  # type: ignore[arg-type]  # deliberately wrong types
