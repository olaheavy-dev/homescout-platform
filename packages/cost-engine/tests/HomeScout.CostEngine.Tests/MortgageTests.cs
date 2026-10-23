namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Mortgage.MonthlyRepayment against the independently worked cases (standard repayment, monthly compounding,
/// rounded once; OpenStax Contemporary Mathematics 6.8). Inputs and expected values are read from the case file.
/// </summary>
[TestFixture]
internal sealed class MortgageTests
{
    private static IEnumerable<TestCaseData> MortgageCases() =>
        StoryCases.IdsWithInput("annualRate").Select(id => new TestCaseData(id).SetArgDisplayNames(id));

    [Test]
    public void MortgageCases_file_hasTheFourWorkedMortgageCases() =>
        Assert.That(MortgageCases().Count(), Is.EqualTo(4));

    [TestCaseSource(nameof(MortgageCases))]
    public void MonthlyRepayment_storyCase_matchesWorkedResult(string caseId)
    {
        (Pence loan, int rateBasisPoints, int termYears) = StoryCases.MortgageInputs(caseId);
        long expected = StoryCases.Case(caseId)["expected"]!["monthlyRepaymentPence"]!.GetValue<long>();

        Result<MortgageRepayment> result = Mortgage.MonthlyRepayment(loan, rateBasisPoints, termYears);

        Assert.That(result.IsSuccess, Is.True);
        Assert.That(result.Value.MonthlyRepayment, Is.EqualTo(new Pence(expected)));
        Assert.That(result.Value.Loan, Is.EqualTo(loan));
        Assert.That(result.Value.RateBasisPoints, Is.EqualTo(rateBasisPoints));
        Assert.That(result.Value.TermYears, Is.EqualTo(termYears));
        Assert.That(result.Value.Payments, Is.EqualTo(termYears * 12));
    }

    [Test]
    public void BasisPoints_rateThatIsNotWholeBasisPoints_failsTheTest() =>
        Assert.Throws<AssertionException>(() => StoryCases.BasisPoints("0.05505"));

    [TestCase(0L, 550, 25, "mortgage.loan-not-positive")]
    [TestCase(-1L, 550, 25, "mortgage.loan-not-positive")]
    [TestCase(1_000_000L, 0, 25, "mortgage.rate-not-positive")]
    [TestCase(1_000_000L, -5, 25, "mortgage.rate-not-positive")]
    [TestCase(1_000_000L, 550, 0, "mortgage.term-not-positive")]
    [TestCase(1_000_000L, 550, -1, "mortgage.term-not-positive")]
    public void MonthlyRepayment_invalidInput_failsWithTheCode(long loan, int rateBasisPoints, int termYears, string code)
    {
        Result<MortgageRepayment> result = Mortgage.MonthlyRepayment(new Pence(loan), rateBasisPoints, termYears);

        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error.Code, Is.EqualTo(code));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [TestCase(101)]
    [TestCase(50_000)]
    [TestCase(int.MaxValue)]
    public void MonthlyRepayment_termOver100Years_failsAsTooLong(int termYears)
    {
        // 100 years is a computation limit (a huge term makes the exact arithmetic very slow), not a lending rule.
        Result<MortgageRepayment> result = Mortgage.MonthlyRepayment(new Pence(1_000_000), 550, termYears);

        Assert.That(result.Error.Code, Is.EqualTo("mortgage.term-too-long"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [Test]
    public void MonthlyRepayment_termOf100Years_isCalculated() =>
        Assert.That(Mortgage.MonthlyRepayment(new Pence(1_000_000), 550, 100).IsSuccess, Is.True);

    [TestCase(5_000_000_000_000_000L)]
    [TestCase(long.MaxValue / 1000)]
    [TestCase(long.MaxValue / 100)]
    public void MonthlyRepayment_veryLargeLoan_neverGivesAWrongSuccess(long loan)
    {
        // Independent bounds, not an engine figure. At 2,000 basis points the monthly rate is i = 2000 / 120,000 = 1/60.
        // Interest alone each month is loan / 60, and the repayment is more than that and less than the whole loan
        // (the first payment of a 25-year loan is a fraction of the loan). A wrapped-around multiplication fails these bounds.
        Result<MortgageRepayment> result;
        try
        {
            result = Mortgage.MonthlyRepayment(new Pence(loan), 2000, 25);
        }
        catch (OverflowException)
        {
            Assert.Pass("Throwing is allowed; a wrong success is not.");
            return;
        }

        Assert.That(result.IsSuccess, Is.True);
        Assert.That(result.Value.MonthlyRepayment.Value, Is.GreaterThan(loan / 60));
        Assert.That(result.Value.MonthlyRepayment.Value, Is.LessThan(loan));
    }
}
