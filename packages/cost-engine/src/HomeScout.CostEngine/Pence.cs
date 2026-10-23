using System.Numerics;

namespace HomeScout.CostEngine;

/// <summary>
/// An amount of money in whole pence (decision 0021). Negative values are allowed (for example a difference).
/// </summary>
/// <remarks>
/// Arithmetic is checked: a result that does not fit in a <see cref="long"/> throws <see cref="OverflowException"/>
/// rather than wrapping round to a wrong figure. Overflow is a programming error (no real amount is near 9 x 10^18 pence),
/// so it throws and is not a <c>Result</c> failure (decisions 0021, 0032).
/// </remarks>
public readonly record struct Pence(long Value) : IComparable<Pence>
{
    /// <summary>Months in a year, for annual to monthly conversion.</summary>
    private const int _monthsPerYear = 12;

    /// <summary>No money.</summary>
    public static Pence Zero => default;

    /// <summary>Adds two amounts.</summary>
    public static Pence operator +(Pence left, Pence right) => left.Add(right);

    /// <summary>Subtracts <paramref name="right"/> from <paramref name="left"/>.</summary>
    public static Pence operator -(Pence left, Pence right) => left.Subtract(right);

    /// <summary>Flips the sign.</summary>
    public static Pence operator -(Pence value) => value.Negate();

    /// <summary>Multiplies an amount by a whole number.</summary>
    public static Pence operator *(Pence amount, long factor) => amount.Multiply(factor);

    /// <summary>Multiplies an amount by a whole number.</summary>
    public static Pence operator *(long factor, Pence amount) => amount.Multiply(factor);

    /// <summary>Whether <paramref name="left"/> is less than <paramref name="right"/>.</summary>
    public static bool operator <(Pence left, Pence right) => left.Value < right.Value;

    /// <summary>Whether <paramref name="left"/> is greater than <paramref name="right"/>.</summary>
    public static bool operator >(Pence left, Pence right) => left.Value > right.Value;

    /// <summary>Whether <paramref name="left"/> is less than or equal to <paramref name="right"/>.</summary>
    public static bool operator <=(Pence left, Pence right) => left.Value <= right.Value;

    /// <summary>Whether <paramref name="left"/> is greater than or equal to <paramref name="right"/>.</summary>
    public static bool operator >=(Pence left, Pence right) => left.Value >= right.Value;

    /// <summary>
    /// Converts an exact amount of pence to whole pence: nearest penny, exact halves away from zero (decision 0021).
    /// This is the one place a <see cref="decimal"/> enters the public API. Rounding an exact fraction of a penny
    /// needs an exact decimal value, and <see cref="decimal"/> (unlike double or float) holds decimal fractions without error.
    /// </summary>
    /// <exception cref="OverflowException">The rounded amount does not fit in a <see cref="long"/>.</exception>
    public static Pence Round(decimal exactPence) =>
        new(decimal.ToInt64(Math.Round(exactPence, 0, MidpointRounding.AwayFromZero)));

    /// <summary>
    /// Rounds an exact fraction of pence, <paramref name="numerator"/> over <paramref name="denominator"/>, once:
    /// nearest penny, exact halves away from zero (decisions 0021, 0034). The fraction is exact whole-number arithmetic,
    /// so no precision is lost before the one rounding step. A negative denominator is allowed; the sign of the result
    /// is the sign of the fraction.
    /// </summary>
    /// <exception cref="DivideByZeroException"><paramref name="denominator"/> is zero.</exception>
    /// <exception cref="OverflowException">The rounded amount does not fit in a <see cref="long"/>.</exception>
    public static Pence RoundRatio(BigInteger numerator, BigInteger denominator)
    {
        if (denominator.IsZero)
        {
            throw new DivideByZeroException("A fraction of pence needs a denominator that is not zero.");
        }

        // Work on the size of the fraction, then put the sign back, so halves round away from zero on both sides.
        bool isNegative = numerator.Sign * denominator.Sign < 0;
        BigInteger size = BigInteger.DivRem(BigInteger.Abs(numerator), BigInteger.Abs(denominator), out BigInteger remainder);

        // A remainder of half the denominator or more is half a penny or more.
        if (remainder * 2 >= BigInteger.Abs(denominator))
        {
            size += BigInteger.One;
        }

        return new Pence(checked((long)(isNegative ? -size : size)));
    }

    /// <summary>Adds <paramref name="other"/>.</summary>
    /// <exception cref="OverflowException">The sum does not fit in a <see cref="long"/>.</exception>
    public Pence Add(Pence other) => new(checked(Value + other.Value));

    /// <summary>Subtracts <paramref name="other"/>.</summary>
    /// <exception cref="OverflowException">The difference does not fit in a <see cref="long"/>.</exception>
    public Pence Subtract(Pence other) => new(checked(Value - other.Value));

    /// <summary>Flips the sign.</summary>
    /// <exception cref="OverflowException">The value is <see cref="long.MinValue"/>, which has no positive twin.</exception>
    public Pence Negate() => new(checked(-Value));

    /// <summary>Multiplies by a whole number.</summary>
    /// <exception cref="OverflowException">The product does not fit in a <see cref="long"/>.</exception>
    public Pence Multiply(long factor) => new(checked(Value * factor));

    /// <inheritdoc />
    public int CompareTo(Pence other) => Value.CompareTo(other.Value);

    /// <summary>
    /// Converts an annual amount to a monthly one, rounding once: nearest penny, exact halves away from zero (decision 0021).
    /// Uses whole-number arithmetic, so there is no intermediate rounding.
    /// </summary>
    public Pence AnnualToMonthly()
    {
        long wholePart = Value / _monthsPerYear;
        long remainder = Value % _monthsPerYear;

        // A remainder of 6 or more twelfths is half a penny or more; round away from zero.
        if (Math.Abs(remainder) * 2 >= _monthsPerYear)
        {
            wholePart += Math.Sign(Value);
        }

        return new Pence(wholePart);
    }
}
