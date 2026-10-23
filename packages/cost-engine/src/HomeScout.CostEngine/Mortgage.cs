using System.Numerics;

namespace HomeScout.CostEngine;

/// <summary>A worked-out repayment mortgage: the inputs used and the monthly repayment.</summary>
/// <param name="Loan">The amount borrowed.</param>
/// <param name="RateBasisPoints">The yearly rate in whole basis points (550 is 5.5%).</param>
/// <param name="TermYears">The length of the loan in years.</param>
/// <param name="Payments">The number of monthly payments, 12 a year.</param>
/// <param name="MonthlyRepayment">The monthly payment, rounded once to the nearest penny.</param>
public sealed record MortgageRepayment(Pence Loan, int RateBasisPoints, int TermYears, int Payments, Pence MonthlyRepayment);

/// <summary>Repayment-mortgage arithmetic (decision 0021).</summary>
public static class Mortgage
{
    /// <summary>
    /// The longest term the engine will work out. This is a technical computation limit (the exact arithmetic gets very slow
    /// for huge terms), not a lending rule (register line BE-17).
    /// </summary>
    public const int MaxTermYears = 100;

    private const int _monthsPerYear = 12;

    /// <summary>The denominator of the monthly rate: a rate in basis points is 1/10,000 of a year, and a month is 1/12 of that.</summary>
    private const int _basisPointsPerMonthDenominator = 10_000 * _monthsPerYear;

    /// <summary>
    /// The monthly repayment on a standard repayment mortgage with monthly compounding and payments in arrears.
    /// </summary>
    /// <remarks>
    /// Formula: OpenStax, Contemporary Mathematics, section 6.8, https://openstax.org/books/contemporary-mathematics/pages/6-8-the-basics-of-loans
    /// (pmt = P i (1+i)^N / ((1+i)^N - 1), with monthly rate i = rate / 12 and N = 12 x years payments).
    /// The rate is a whole number of basis points b, so i = b / 120,000 exactly. Putting everything over the common
    /// denominator 120,000 gives M = P b (120,000 + b)^N / (120,000 ((120,000 + b)^N - 120,000^N)), an exact fraction
    /// worked out with whole numbers. It is rounded once, nearest penny with halves away from zero (decision 0021),
    /// which is HomeScout's rule; the source's formula says nothing about rounding.
    /// </remarks>
    /// <exception cref="OverflowException">The rounded repayment does not fit in a <see cref="long"/>.</exception>
    public static Result<MortgageRepayment> MonthlyRepayment(Pence loan, int rateBasisPoints, int termYears)
    {
        if (loan.Value <= 0)
        {
            return Fail("mortgage.loan-not-positive", "The loan must be more than zero.");
        }

        if (rateBasisPoints <= 0)
        {
            return Fail("mortgage.rate-not-positive", "The interest rate must be more than zero.");
        }

        if (termYears <= 0)
        {
            return Fail("mortgage.term-not-positive", "The mortgage term must be more than zero years.");
        }

        if (termYears > MaxTermYears)
        {
            return Fail("mortgage.term-too-long", $"The mortgage term can be at most {MaxTermYears} years.");
        }

        int payments = checked(termYears * _monthsPerYear);
        BigInteger common = _basisPointsPerMonthDenominator;
        BigInteger grown = common + rateBasisPoints;
        BigInteger growth = BigInteger.Pow(grown, payments);

        // Widen to BigInteger first: a long times an int would wrap around silently (overflow checking is off).
        BigInteger numerator = new BigInteger(loan.Value) * rateBasisPoints * growth;
        BigInteger denominator = common * (growth - BigInteger.Pow(common, payments));

        Pence repayment = Pence.RoundRatio(numerator, denominator);
        return Result.Success(new MortgageRepayment(loan, rateBasisPoints, termYears, payments, repayment));
    }

    private static Result<MortgageRepayment> Fail(string code, string message) =>
        Result.Failure<MortgageRepayment>(new Error(code, message, ErrorCategory.Validation));
}
