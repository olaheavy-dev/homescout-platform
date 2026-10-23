using FsCheck;
using FsCheck.Fluent;

namespace HomeScout.CostEngine.Tests;

// FsCheck.NUnit supplies the test arguments, which the NUnit analyser cannot see (NUnit1027).
#pragma warning disable NUnit1027

/// <summary>An exact amount of pence with a fraction: whole pennies plus 0 to 999 thousandths of a penny.</summary>
internal readonly record struct ExactPence(long Pennies, int Thousandths)
{
    public decimal Value => Pennies + (Thousandths / 1000m);
}

/// <summary>
/// Input generators for the properties. FsCheck's defaults keep numbers within about +/-100, which would hide most
/// rounding behaviour, so integers and longs here cover their full range and exact amounts are built from whole pennies
/// plus thousandths, with the interesting ones (0, 499, 500, 501, 999 thousandths) always likely.
/// </summary>
internal static class PenceArbitraries
{
    private const long _maxPennies = 1_000_000_000_000_000; // 10^15, far below the decimal and long limits

    public static Arbitrary<int> FullRangeInt() =>
        Gen.Choose(int.MinValue, int.MaxValue).ToArbitrary();

    public static Arbitrary<long> FullRangeLong() =>
        Gen.Zip(Gen.Choose(int.MinValue, int.MaxValue), Gen.Choose(int.MinValue, int.MaxValue))
            .Select(pair => ((long)pair.Item1 << 32) | (uint)pair.Item2)
            .ToArbitrary();

    public static Arbitrary<ExactPence> ExactAmounts()
    {
        Gen<int> thousandths = Gen.OneOf(Gen.Choose(0, 999), Gen.Elements(0, 499, 500, 501, 999));
        Gen<long> pennies = Gen.OneOf(
            Gen.Choose(-1000, 1000).Select(n => (long)n),
            Gen.Choose(int.MinValue, int.MaxValue).Select(n => (long)n),
            Gen.Elements(-_maxPennies, _maxPennies, 0L));

        return Gen.Zip(pennies, thousandths).Select(pair => new ExactPence(pair.Item1, pair.Item2)).ToArbitrary();
    }
}

/// <summary>A property run with the generators above.</summary>
[AttributeUsage(AttributeTargets.Method)]
internal sealed class PenceProperty : FsCheck.NUnit.PropertyAttribute
{
    public PenceProperty() => Arbitrary = [typeof(PenceArbitraries)];
}

/// <summary>
/// Property tests (decision 0027). Whole-pence inputs use the full 32-bit and 64-bit range. Sums and products use
/// 32-bit values widened to <see cref="long"/> so they cannot overflow; overflow has its own unit tests.
/// Fractions of a penny come from <see cref="ExactPence"/>.
/// </summary>
[TestFixture]
internal sealed class PenceProperties
{
    [PenceProperty]
    public bool Round_wholePence_isIdempotent(long n) =>
        Pence.Round(n).Value == n;

    [PenceProperty]
    public bool Round_appliedTwice_equalsAppliedOnce(ExactPence amount)
    {
        Pence once = Pence.Round(amount.Value);

        return Pence.Round(once.Value) == once;
    }

    [PenceProperty]
    public bool Round_negatedInput_isNegatedResult(ExactPence amount)
    {
        decimal exact = amount.Value;

        return Pence.Round(-exact) == -Pence.Round(exact);
    }

    [PenceProperty]
    public bool Round_anyInput_isWithinHalfAPennyOfTheInput(ExactPence amount)
    {
        decimal exact = amount.Value;

        return Math.Abs(Pence.Round(exact).Value - exact) <= 0.5m;
    }

    [PenceProperty]
    public bool Round_exactHalf_roundsAwayFromZero(int whole)
    {
        long n = Math.Abs((long)whole);

        return Pence.Round(n + 0.5m).Value == n + 1 && Pence.Round(-n - 0.5m).Value == -n - 1;
    }

    [PenceProperty]
    public bool AnnualToMonthly_twelveTimesMonthly_returnsMonthly(int monthly) =>
        new Pence(12L * monthly).AnnualToMonthly() == new Pence(monthly);

    [PenceProperty]
    public bool AnnualToMonthly_negatedInput_isNegatedResult(int annual)
    {
        var amount = new Pence(annual);

        return amount.Negate().AnnualToMonthly() == amount.AnnualToMonthly().Negate();
    }

    [PenceProperty]
    public bool AnnualToMonthly_anyInput_matchesRoundingTheExactQuotient(int annual) =>
        new Pence(annual).AnnualToMonthly() == Pence.Round(annual / 12m);

    [PenceProperty]
    public bool Add_threeAmounts_isAssociative(int a, int b, int c)
    {
        var x = new Pence(a);
        var y = new Pence(b);
        var z = new Pence(c);

        return (x + y) + z == x + (y + z);
    }

    [PenceProperty]
    public bool Add_twoAmounts_isCommutative(int a, int b)
    {
        var x = new Pence(a);
        var y = new Pence(b);

        return x + y == y + x;
    }

    [PenceProperty]
    public bool Add_negatedAmount_returnsZero(int a)
    {
        var x = new Pence(a);

        return x + (-x) == Pence.Zero;
    }

    [PenceProperty]
    public bool Subtract_amount_equalsAddingTheNegation(int a, int b)
    {
        var x = new Pence(a);
        var y = new Pence(b);

        return x - y == x + (-y);
    }

    [PenceProperty]
    public bool CompareTo_twoAmounts_agreesWithSign(int a, int b) =>
        Math.Sign(new Pence(a).CompareTo(new Pence(b))) == Math.Sign(((long)a).CompareTo(b));
}
