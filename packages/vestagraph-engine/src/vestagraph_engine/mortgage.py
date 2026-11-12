"""Repayment-mortgage arithmetic (decision 0021), ported from the C# ``Mortgage``."""

from dataclasses import dataclass
from typing import Final

from vestagraph_engine._checks import is_a
from vestagraph_engine.pence import Pence, round_ratio
from vestagraph_engine.result import Error, ErrorCategory, Result
from vestagraph_engine.whole_power import whole_power

# The longest term the engine will work out. A technical computation limit (the exact arithmetic
# gets very slow for huge terms), not a lending rule (register line BE-17).
MAX_TERM_YEARS: Final = 100

_MONTHS_PER_YEAR: Final = 12
# The denominator of the monthly rate: a rate in basis points is 1/10,000 of a year, and a month
# is 1/12 of that.
_BASIS_POINTS_PER_MONTH_DENOMINATOR: Final = 10_000 * _MONTHS_PER_YEAR


@dataclass(frozen=True, slots=True)
class MortgageRepayment:
    """A worked-out repayment mortgage: the inputs used and the monthly repayment.

    ``rate_basis_points`` is the yearly rate in whole basis points (550 is 5.5%); ``payments`` is
    the number of monthly payments, 12 a year; ``monthly_repayment`` is rounded once.
    """

    loan: Pence
    rate_basis_points: int
    term_years: int
    payments: int
    monthly_repayment: Pence


def monthly_repayment(
    loan: Pence, rate_basis_points: int, term_years: int
) -> Result[MortgageRepayment]:
    """The monthly repayment on a standard repayment mortgage, monthly compounding, in arrears.

    Formula: OpenStax, Contemporary Mathematics, section 6.8,
    https://openstax.org/books/contemporary-mathematics/pages/6-8-the-basics-of-loans
    (pmt = P i (1+i)^N / ((1+i)^N - 1), monthly rate i = rate / 12, N = 12 x years payments).
    The rate is a whole number of basis points b, so i = b / 120,000 exactly. Over the common
    denominator 120,000 the repayment is
    ``P b (120,000 + b)^N / (120,000 ((120,000 + b)^N - 120,000^N))``: an exact fraction of whole
    numbers, rounded once (nearest penny, halves away from zero; decision 0021). The source says
    nothing about rounding. No fraction division is needed (register line BE-32).

    Expected failures (``mortgage.loan-not-positive``, ``mortgage.rate-not-positive``,
    ``mortgage.term-not-positive``, ``mortgage.term-too-long``) come back as a failed ``Result``.
    Raises ``TypeError`` for arguments of the wrong type and ``OverflowError`` when the rounded
    repayment does not fit in 64 bits.
    """
    if not is_a(loan, Pence) or type(rate_basis_points) is not int or type(term_years) is not int:
        message = "monthly_repayment needs a Pence loan and whole-number (int) rate and term."
        raise TypeError(message)

    if loan.value <= 0:
        return _fail("mortgage.loan-not-positive", "The loan must be more than zero.")
    if rate_basis_points <= 0:
        return _fail("mortgage.rate-not-positive", "The interest rate must be more than zero.")
    if term_years <= 0:
        return _fail(
            "mortgage.term-not-positive", "The mortgage term must be more than zero years."
        )
    if term_years > MAX_TERM_YEARS:
        return _fail(
            "mortgage.term-too-long",
            f"The mortgage term can be at most {MAX_TERM_YEARS} years.",
        )

    payments = term_years * _MONTHS_PER_YEAR
    common = _BASIS_POINTS_PER_MONTH_DENOMINATOR
    growth = whole_power(common + rate_basis_points, payments)

    # Python integers do not wrap around, so nothing is lost before the one rounding step.
    numerator = loan.value * rate_basis_points * growth
    denominator = common * (growth - whole_power(common, payments))

    repayment = round_ratio(numerator, denominator)
    return Result.success(
        MortgageRepayment(loan, rate_basis_points, term_years, payments, repayment)
    )


def _fail(code: str, message: str) -> Result[MortgageRepayment]:
    return Result.failure(Error(code, message, ErrorCategory.VALIDATION))
