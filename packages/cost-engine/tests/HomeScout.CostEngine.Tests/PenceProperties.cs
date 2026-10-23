namespace HomeScout.CostEngine.Tests;

// FsCheck.NUnit supplies the test arguments, which the NUnit analyser cannot see (NUnit1027).
#pragma warning disable NUnit1027

/// <summary>
/// Property tests (decision 0027). Inputs are 32-bit integers widened to <see cref="long"/> so that sums and products
/// cannot overflow; overflow itself has its own unit tests. Fractions of a penny come from thousandths: n / 1000.
/// </summary>
[TestFixture]
internal sealed class PenceProperties
{
    private static decimal Thousandths(int n) => n / 1000m;

    [FsCheck.NUnit.Property]
    public bool Round_wholePence_isIdempotent(long n) =>
        Pence.Round(n).Value == n;

    [FsCheck.NUnit.Property]
    public bool Round_appliedTwice_equalsAppliedOnce(int thousandths)
    {
        Pence once = Pence.Round(Thousandths(thousandths));

        return Pence.Round(once.Value) == once;
    }

    [FsCheck.NUnit.Property]
    public bool Round_negatedInput_isNegatedResult(int thousandths)
    {
        decimal exact = Thousandths(thousandths);

        return Pence.Round(-exact) == -Pence.Round(exact);
    }

    [FsCheck.NUnit.Property]
    public bool Round_anyInput_isWithinHalfAPennyOfTheInput(int thousandths)
    {
        decimal exact = Thousandths(thousandths);

        return Math.Abs(Pence.Round(exact).Value - exact) <= 0.5m;
    }

    [FsCheck.NUnit.Property]
    public bool AnnualToMonthly_twelveTimesMonthly_returnsMonthly(int monthly) =>
        new Pence(12L * monthly).AnnualToMonthly() == new Pence(monthly);

    [FsCheck.NUnit.Property]
    public bool AnnualToMonthly_negatedInput_isNegatedResult(int annual)
    {
        var amount = new Pence(annual);

        return amount.Negate().AnnualToMonthly() == amount.AnnualToMonthly().Negate();
    }

    [FsCheck.NUnit.Property]
    public bool AnnualToMonthly_anyInput_matchesRoundingTheExactQuotient(int annual) =>
        new Pence(annual).AnnualToMonthly() == Pence.Round(annual / 12m);

    [FsCheck.NUnit.Property]
    public bool Add_threeAmounts_isAssociative(int a, int b, int c)
    {
        var x = new Pence(a);
        var y = new Pence(b);
        var z = new Pence(c);

        return (x + y) + z == x + (y + z);
    }

    [FsCheck.NUnit.Property]
    public bool Add_twoAmounts_isCommutative(int a, int b)
    {
        var x = new Pence(a);
        var y = new Pence(b);

        return x + y == y + x;
    }

    [FsCheck.NUnit.Property]
    public bool Add_negatedAmount_returnsZero(int a)
    {
        var x = new Pence(a);

        return x + (-x) == Pence.Zero;
    }

    [FsCheck.NUnit.Property]
    public bool Subtract_amount_equalsAddingTheNegation(int a, int b)
    {
        var x = new Pence(a);
        var y = new Pence(b);

        return x - y == x + (-y);
    }

    [FsCheck.NUnit.Property]
    public bool CompareTo_twoAmounts_agreesWithSign(int a, int b) =>
        Math.Sign(new Pence(a).CompareTo(new Pence(b))) == Math.Sign(((long)a).CompareTo(b));
}
