using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// UpfrontCash.Calculate against the independently worked upfront cases (read from test-cases/story-calculations.json).
/// Stamp duty and legal fees are not calculated in this version: they stay flagged and never become zero.
/// </summary>
[TestFixture]
internal sealed class UpfrontCashTests
{
    private static readonly string[] _anyEvidence = ["EVIDENCE-1"];

    private static readonly CostCategory[] _rentOrder = [CostCategory.Deposit, CostCategory.FirstMonthRent, CostCategory.MovingCosts];

    private static readonly CostCategory[] _buyOrder =
        [CostCategory.MortgageDeposit, CostCategory.MovingCosts, CostCategory.StampDuty, CostCategory.LegalFees];

    /// <summary>The ids of the upfront cases: those with a list of lines and no budget.</summary>
    public static IEnumerable<string> CaseIds { get; } =
        StoryCases.IdsWhere(c => c["inputs"]!["lines"] is not null && c["inputs"]!["budgetPence"] is null).ToList();

    private static IEnumerable<TestCaseData> UpfrontCases() =>
        CaseIds.Select(id => new TestCaseData(id).SetArgDisplayNames(id));

    [Test]
    public void UpfrontCases_file_hasTheFourWorkedUpfrontCases() =>
        Assert.That(CaseIds.Count(), Is.EqualTo(4));

    [TestCaseSource(nameof(UpfrontCases))]
    public void UpfrontCash_storyCase_matchesWorkedResult(string caseId)
    {
        JsonNode storyCase = StoryCases.Case(caseId);
        JsonNode expected = storyCase["expected"]!;

        Result<UpfrontBreakdown> result = UpfrontCash.Calculate(CaseLines.ModeOf(storyCase), CaseLines.Lines(storyCase));

        Assert.That(result.IsSuccess, Is.True);
        UpfrontBreakdown actual = result.Value;
        Assert.That(actual.Total, Is.EqualTo(new Pence(expected["totalUpfrontPence"]!.GetValue<long>())));
        Assert.That(actual.IsPartial, Is.EqualTo(expected["totalIsPartial"]!.GetValue<bool>()));

        JsonArray expectedLines = expected["lines"]!.AsArray();
        Assert.That(actual.Lines, Has.Count.EqualTo(expectedLines.Count));
        foreach (JsonNode? expectedLine in expectedLines)
        {
            LineResult line = actual.Lines.Single(l => l.Category == CaseLines.Category(expectedLine!["category"]!.GetValue<string>()));
            if (expectedLine!["amountPence"] is { } amount)
            {
                Assert.That(line.Status, Is.EqualTo(LineStatus.Calculated), line.Category.ToString());
                Assert.That(line.Amount, Is.EqualTo(new Pence(amount.GetValue<long>())), line.Category.ToString());
            }
            else
            {
                Assert.That(line.Amount, Is.Null, line.Category.ToString());
                Assert.That(CostCategories.StatusId(line.Status), Is.EqualTo(expectedLine["status"]!.GetValue<string>()), line.Category.ToString());
            }
        }

        string[] expectedCategories = expected["partialReasons"]!.AsArray().Select(r => r!.GetValue<string>().Split(':')[0]).ToArray();
        Assert.That(actual.PartialReasons.Select(r => CostCategories.ToId(r.Category)), Is.EquivalentTo(expectedCategories));
    }

    [Test]
    public void UpfrontCash_linesGivenOutOfOrder_comeBackInTheFixedBuyOrder()
    {
        List<LineInput> lines =
        [
            new NotCalculatedLine(CostCategory.LegalFees, _anyEvidence),
            new NotCalculatedLine(CostCategory.StampDuty, _anyEvidence),
            Once(CostCategory.MovingCosts, 120_000),
            Once(CostCategory.MortgageDeposit, 3_000_000),
        ];

        UpfrontBreakdown result = UpfrontCash.Calculate(Mode.Buy, lines).Value;

        Assert.That(result.Lines.Select(l => l.Category), Is.EqualTo(_buyOrder));
    }

    [Test]
    public void UpfrontCash_linesGivenOutOfOrder_comeBackInTheFixedRentOrder()
    {
        List<LineInput> lines =
        [
            Once(CostCategory.MovingCosts, 120_000),
            Once(CostCategory.FirstMonthRent, 120_000),
            Once(CostCategory.Deposit, 138_000),
        ];

        UpfrontBreakdown result = UpfrontCash.Calculate(Mode.Rent, lines).Value;

        Assert.That(result.Lines.Select(l => l.Category), Is.EqualTo(_rentOrder));
    }

    [Test]
    public void UpfrontCash_stampDutyAndLegalFees_stayNotCalculatedWithNoAmount()
    {
        List<LineInput> lines =
        [
            Once(CostCategory.MortgageDeposit, 3_000_000),
            new NotCalculatedLine(CostCategory.StampDuty, _anyEvidence),
            new NotCalculatedLine(CostCategory.LegalFees, _anyEvidence),
        ];

        UpfrontBreakdown result = UpfrontCash.Calculate(Mode.Buy, lines).Value;

        Assert.That(result.Lines.Where(l => l.Category is CostCategory.StampDuty or CostCategory.LegalFees).Select(l => l.Amount), Has.All.Null);
        Assert.That(result.Total, Is.EqualTo(new Pence(3_000_000)));
        Assert.That(result.IsPartial, Is.True);
        Assert.That(result.PartialReasons.Select(r => r.Status), Has.All.EqualTo(LineStatus.NotCalculated));
    }

    [Test]
    public void UpfrontCash_missingMovingCosts_makesTheTotalPartial()
    {
        List<LineInput> lines = [Once(CostCategory.MortgageDeposit, 3_000_000), new MissingLine(CostCategory.MovingCosts)];

        UpfrontBreakdown result = UpfrontCash.Calculate(Mode.Buy, lines).Value;

        Assert.That(result.IsPartial, Is.True);
        Assert.That(result.PartialReasons, Is.EqualTo(new[] { new PartialReason(CostCategory.MovingCosts, LineStatus.Missing) }));
    }

    [Test]
    public void UpfrontCash_buyingWithNoLines_failsAsMissingMortgageDeposit()
    {
        Result<UpfrontBreakdown> result = UpfrontCash.Calculate(Mode.Buy, []);

        Assert.That(result.Error.Code, Is.EqualTo("input.missing.mortgage-deposit"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [Test]
    public void UpfrontCash_buyingWithMortgageDepositMissing_failsAsMissingMortgageDeposit()
    {
        List<LineInput> lines = [new MissingLine(CostCategory.MortgageDeposit), Once(CostCategory.MovingCosts, 120_000)];

        Assert.That(UpfrontCash.Calculate(Mode.Buy, lines).Error.Code, Is.EqualTo("input.missing.mortgage-deposit"));
    }

    [Test]
    public void UpfrontCash_rentingWithNoLines_hasNoLinesAndATotalOfZeroThatIsNotPartial()
    {
        // Renting has no required upfront input (register line BE-16 names only rent as a renter's anchor, and that is a monthly figure).
        UpfrontBreakdown result = UpfrontCash.Calculate(Mode.Rent, []).Value;

        Assert.That(result.Lines, Is.Empty);
        Assert.That(result.Total, Is.EqualTo(Pence.Zero));
        Assert.That(result.IsPartial, Is.False);
    }

    [Test]
    public void UpfrontCash_amountGivenMonthly_failsAsWrongPeriod()
    {
        Result<UpfrontBreakdown> result = UpfrontCash.Calculate(Mode.Rent, [new AmountLine(CostCategory.Deposit, new Pence(138_000), Period.Month, _anyEvidence)]);

        Assert.That(result.Error.Code, Is.EqualTo("input.wrong-period.deposit"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [TestCase(0L)]
    [TestCase(-1L)]
    public void UpfrontCash_amountNotPositive_failsAsNotPositive(long pence) =>
        Assert.That(UpfrontCash.Calculate(Mode.Rent, [Once(CostCategory.MovingCosts, pence)]).Error.Code, Is.EqualTo("input.not-positive.moving-costs"));

    [Test]
    public void UpfrontCash_sameCategoryTwice_failsAsAmbiguous()
    {
        Result<UpfrontBreakdown> result = UpfrontCash.Calculate(Mode.Rent, [Once(CostCategory.Deposit, 138_000), Once(CostCategory.Deposit, 140_000)]);

        Assert.That(result.Error.Code, Is.EqualTo("input.ambiguous.deposit"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Conflict));
    }

    [Test]
    public void UpfrontCash_lineThatDoesNotBelongToTheMode_failsAsNotForMode() =>
        Assert.That(UpfrontCash.Calculate(Mode.Rent, [Once(CostCategory.StampDuty, 1_000)]).Error.Code, Is.EqualTo("input.not-for-mode.stamp-duty"));

    [Test]
    public void UpfrontCash_nullLines_throws() =>
        Assert.Throws<ArgumentNullException>(() => UpfrontCash.Calculate(Mode.Rent, null!));

    [Test]
    public void UpfrontCash_undefinedMode_throws() =>
        Assert.Throws<ArgumentOutOfRangeException>(() => UpfrontCash.Calculate((Mode)99, []));

    [Test]
    public void UpfrontCash_totalTooBigForALong_throwsOverflow() =>
        Assert.Throws<OverflowException>(() => UpfrontCash.Calculate(Mode.Rent, [Once(CostCategory.Deposit, long.MaxValue), Once(CostCategory.MovingCosts, 1)]));

    private static AmountLine Once(CostCategory category, long pence) =>
        new(category, new Pence(pence), Period.Once, _anyEvidence);
}
