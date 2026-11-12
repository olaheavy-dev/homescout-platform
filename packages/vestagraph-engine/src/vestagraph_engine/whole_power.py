"""A whole-number power with a variable exponent (register line BE-32).

The architecture test only allows ``**`` with a constant exponent, so a power whose exponent is a
variable (the mortgage's number of payments) is built by multiplying in a loop.
"""


def whole_power(base: int, exponent: int) -> int:
    """Return ``base`` to the whole power ``exponent``, exactly (no rounding, no size limit).

    Both arguments must be plain ``int`` (not ``bool``, ``float`` or ``Fraction``). Raises
    ``ValueError`` for a negative exponent, since that would not be a whole number.
    """
    if type(base) is not int or type(exponent) is not int:
        message = "whole_power needs two whole numbers (int)."
        raise TypeError(message)
    if exponent < 0:
        message = "whole_power needs an exponent that is not negative."
        raise ValueError(message)

    result = 1
    for _ in range(exponent):
        result *= base
    return result
