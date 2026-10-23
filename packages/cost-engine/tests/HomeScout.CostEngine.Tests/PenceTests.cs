namespace HomeScout.CostEngine.Tests;

[TestFixture]
internal sealed class PenceTests
{
    [Test]
    public void Zero_default_equalsNewPenceOfZero()
    {
        Assert.That(Pence.Zero, Is.EqualTo(new Pence(0)));
        Assert.That(default(Pence), Is.EqualTo(Pence.Zero));
    }

    [Test]
    public void Add_twoAmounts_returnsSum() =>
        Assert.That(new Pence(250) + new Pence(75), Is.EqualTo(new Pence(325)));

    [Test]
    public void Add_negativeAmount_reducesTotal() =>
        Assert.That(new Pence(250).Add(new Pence(-300)), Is.EqualTo(new Pence(-50)));

    [Test]
    public void Subtract_twoAmounts_returnsDifference() =>
        Assert.That(new Pence(250) - new Pence(300), Is.EqualTo(new Pence(-50)));

    [Test]
    public void Subtract_methodForm_matchesOperator() =>
        Assert.That(new Pence(250).Subtract(new Pence(300)), Is.EqualTo(new Pence(250) - new Pence(300)));

    [Test]
    public void Negate_positive_returnsNegative() =>
        Assert.That(-new Pence(125), Is.EqualTo(new Pence(-125)));

    [Test]
    public void Negate_negative_returnsPositive() =>
        Assert.That(new Pence(-125).Negate(), Is.EqualTo(new Pence(125)));

    [Test]
    public void Negate_zero_returnsZero() =>
        Assert.That(-Pence.Zero, Is.EqualTo(Pence.Zero));

    [Test]
    public void Multiply_byWholeNumber_returnsProduct()
    {
        Assert.That(new Pence(1500) * 12, Is.EqualTo(new Pence(18000)));
        Assert.That(12 * new Pence(1500), Is.EqualTo(new Pence(18000)));
        Assert.That(new Pence(1500).Multiply(-2), Is.EqualTo(new Pence(-3000)));
    }

    [Test]
    public void CompareTo_smallerAndLarger_ordersByValue()
    {
        Assert.That(new Pence(-5), Is.LessThan(new Pence(3)));
        Assert.That(new Pence(3), Is.GreaterThan(new Pence(-5)));
        Assert.That(new Pence(3).CompareTo(new Pence(3)), Is.Zero);
    }

    [Test]
    public void ComparisonOperators_variousPairs_followValueOrder()
    {
        Assert.That(new Pence(1) < new Pence(2), Is.True);
        Assert.That(new Pence(2) > new Pence(1), Is.True);
        Assert.That(new Pence(2) <= new Pence(1 + 1), Is.True);
        Assert.That(new Pence(2) >= new Pence(3), Is.False);
    }

    [Test]
    public void Equals_sameValue_isEqual()
    {
        var first = new Pence(7);
        var second = new Pence(3) + new Pence(4);

        Assert.That(first, Is.EqualTo(second));
        Assert.That(first == second, Is.True);
    }

    [Test]
    public void Add_overflow_throwsOverflowException() =>
        Assert.That(() => new Pence(long.MaxValue) + new Pence(1), Throws.TypeOf<OverflowException>());

    [Test]
    public void Subtract_overflow_throwsOverflowException() =>
        Assert.That(() => new Pence(long.MinValue) - new Pence(1), Throws.TypeOf<OverflowException>());

    [Test]
    public void Negate_minValue_throwsOverflowException() =>
        Assert.That(() => -new Pence(long.MinValue), Throws.TypeOf<OverflowException>());

    [Test]
    public void Multiply_overflow_throwsOverflowException() =>
        Assert.That(() => new Pence(long.MaxValue) * 2, Throws.TypeOf<OverflowException>());

    [Test]
    public void Round_amountTooLargeForLong_throwsOverflowException() =>
        Assert.That(() => Pence.Round(decimal.MaxValue), Throws.TypeOf<OverflowException>());

    [Test]
    public void Round_wholeNumber_isUnchanged() =>
        Assert.That(Pence.Round(1234m), Is.EqualTo(new Pence(1234)));

    [Test]
    public void Round_halfPenny_isNotBankersRounding()
    {
        // Banker's rounding would give 2 and -2 for these.
        Assert.That(Pence.Round(2.5m), Is.EqualTo(new Pence(3)));
        Assert.That(Pence.Round(-2.5m), Is.EqualTo(new Pence(-3)));
    }

    [Test]
    public void AnnualToMonthly_minValue_doesNotOverflow() =>
        Assert.That(new Pence(long.MinValue).AnnualToMonthly().Value, Is.EqualTo(-768614336404564651L));

    [Test]
    public void AnnualToMonthly_exactMultipleOfTwelve_isExact() =>
        Assert.That(new Pence(240000).AnnualToMonthly(), Is.EqualTo(new Pence(20000)));
}
