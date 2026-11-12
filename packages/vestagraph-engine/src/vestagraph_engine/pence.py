"""Money in whole pence (decisions 0021, 0034, 0039).

Every result is checked: a value outside the signed 64-bit range raises ``OverflowError``
rather than growing silently. This keeps the limits of the C# engine (``long``), so both give
the same answers. Overflow is a programming error (no real amount is near 9 x 10^18 pence),
so it raises and is not a ``Result`` failure (decisions 0021, 0032).
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import ClassVar

from vestagraph_engine._checks import is_a

_MIN_VALUE = -(2**63)
_MAX_VALUE = 2**63 - 1
_MONTHS_PER_YEAR = 12


def round_ratio(numerator: int, denominator: int) -> Pence:
    """Round the exact fraction ``numerator / denominator`` of pence once.

    Nearest penny, exact halves away from zero (decisions 0021, 0034). This is the only place
    money is divided, so no precision is lost before the one rounding step. A negative
    denominator is allowed; the sign of the result is the sign of the fraction.

    Raises ``ZeroDivisionError`` for a zero denominator and ``OverflowError`` when the rounded
    amount does not fit in 64 bits. Both arguments must be plain ``int`` (not ``bool``,
    ``float`` or ``Fraction``).
    """
    if type(numerator) is not int or type(denominator) is not int:
        message = "round_ratio needs two whole numbers (int)."
        raise TypeError(message)
    if denominator == 0:
        message = "A fraction of pence needs a denominator that is not zero."
        raise ZeroDivisionError(message)

    # Work on the size of the fraction, then put the sign back,
    # so halves round away from zero on both sides.
    is_negative = (numerator < 0) != (denominator < 0)
    size, remainder = divmod(abs(numerator), abs(denominator))

    # A remainder of half the denominator or more is half a penny or more.
    if 2 * remainder >= abs(denominator):
        size += 1

    return Pence(-size if is_negative else size)


@dataclass(frozen=True, slots=True, order=True)
class Pence:
    """An amount of money in whole pence. Negative values are allowed (for example a difference)."""

    value: int

    ZERO: ClassVar[Pence]

    def __post_init__(self) -> None:
        # type(...) is int rejects bool, float and Fraction, which isinstance would let through.
        if type(self.value) is not int:
            message = "Pence needs a whole number (int), not a bool, float or Fraction."
            raise TypeError(message)
        if not _MIN_VALUE <= self.value <= _MAX_VALUE:
            message = "A pence amount must fit in a signed 64-bit integer."
            raise OverflowError(message)

    @staticmethod
    def from_exact(amount: Fraction | int) -> Pence:
        """Convert an exact amount of pence to whole pence: nearest penny, halves away from zero."""
        if type(amount) is not int and not is_a(amount, Fraction):
            message = "from_exact needs a Fraction or an int."
            raise TypeError(message)
        return round_ratio(amount.numerator, amount.denominator)

    def add(self, other: Pence) -> Pence:
        """Add ``other``. Raises ``OverflowError`` if the sum does not fit in 64 bits."""
        return Pence(self.value + other.value)

    def subtract(self, other: Pence) -> Pence:
        """Subtract ``other``. Raises ``OverflowError`` if the result does not fit in 64 bits."""
        return Pence(self.value - other.value)

    def negate(self) -> Pence:
        """Flip the sign. The minimum value has no positive twin and raises ``OverflowError``."""
        return Pence(-self.value)

    def multiply(self, factor: int) -> Pence:
        """Multiply by a whole number (``int``, not ``bool``)."""
        if type(factor) is not int:
            message = "Pence can only be multiplied by a whole number (int)."
            raise TypeError(message)
        return Pence(self.value * factor)

    def annual_to_monthly(self) -> Pence:
        """Convert an annual amount to a monthly one, rounding once (decision 0021)."""
        return round_ratio(self.value, _MONTHS_PER_YEAR)

    def __add__(self, other: Pence) -> Pence:
        if not is_a(other, Pence):
            return NotImplemented
        return self.add(other)

    def __sub__(self, other: Pence) -> Pence:
        if not is_a(other, Pence):
            return NotImplemented
        return self.subtract(other)

    def __neg__(self) -> Pence:
        return self.negate()

    def __mul__(self, factor: int) -> Pence:
        if type(factor) is not int:
            return NotImplemented
        return self.multiply(factor)

    def __rmul__(self, factor: int) -> Pence:
        return self.__mul__(factor)


Pence.ZERO = Pence(0)
