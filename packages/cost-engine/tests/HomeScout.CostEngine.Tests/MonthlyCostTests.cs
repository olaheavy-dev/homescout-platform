using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// MonthlyCost.Calculate against the independently worked monthly cases. Every input and expected value is read
/// from test-cases/story-calculations.json; the lines are compared by category (the file's line order is not the
/// engine's fixed order).
/// </summary>
[TestFixture]
internal sealed class MonthlyCostTests
{
    private static readonly string[] _anyEvidence = ["EVIDENCE-1"];
    private static readonly string[] _councilTaxEvidence = ["CT-1", "CT-2"];

    private static readonly CostCategory[] _rentOrder =
        [CostCategory.Rent, CostCategory.CouncilTax, CostCategory.Energy, CostCategory.Water, CostCategory.Broadband];

    private static readonly CostCategory[] _buyOrder =
    [
        CostCategory.MortgageRepayment, CostCategory.ServiceCharge, CostCategory.GroundRent, CostCategory.CouncilTax,
        CostCategory.Energy, CostCategory.Water, CostCategory.Broadband, CostCategory.BuildingsInsurance, CostCategory.Maintenance,
    ];

    /// <summary>The ids of the monthly cases: those with a budget and a list of lines.</summary>
    public static IEnumerable<string> CaseIds { get; } =
        StoryCases.IdsWhere(c => c["inputs"]!["lines"] is not null && c["inputs"]!["budgetPence"] is not null).ToList();

    private static IEnumerable<TestCaseData> MonthlyCases() =>
        CaseIds.Select(id => new TestCaseData(id).SetArgDisplayNames(id));

    private static Pence Budget160000 => new(160_000);

    [Test]
    public void MonthlyCases_file_hasTheSixWorkedMonthlyCases() =>
        Assert.That(CaseIds.Count(), Is.EqualTo(6));

    [TestCaseSource(nameof(MonthlyCases))]
    public void MonthlyCost_storyCase_matchesWorkedResult(string caseId)
    {
        JsonNode storyCase = StoryCases.Case(caseId);
        JsonNode expected = storyCase["expected"]!;

        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(CaseLines.ModeOf(storyCase), CaseLines.Lines(storyCase), CaseLines.Budget(storyCase));

        Assert.That(result.IsSuccess, Is.True);
        MonthlyBreakdown actual = result.Value;
        Assert.That(actual.Total, Is.EqualTo(new Pence(expected["totalMonthlyPence"]!.GetValue<long>())));
        Assert.That(actual.IsPartial, Is.EqualTo(expected["totalIsPartial"]!.GetValue<bool>()));
        Assert.That(actual.Budget, Is.EqualTo(new Pence(expected["budgetPence"]!.GetValue<long>())));
        Assert.That(actual.BudgetDifference, Is.EqualTo(new Pence(expected["budgetDifferencePence"]!.GetValue<long>())));
        Assert.That(actual.WithinBudget, Is.EqualTo(expected["withinBudget"]!.GetValue<bool>()));
        Assert.That(actual.BasedOnPartialTotal, Is.EqualTo(actual.IsPartial));

        AssertLinesMatch(actual.Lines, expected["lines"]!.AsArray());
        AssertPartialReasonsMatch(actual.PartialReasons, expected["partialReasons"]!.AsArray());
    }

    [Test]
    public void MonthlyCost_totalExactlyEqualToBudget_isWithinBudget()
    {
        // 1,600 pounds is within budget (founder, 23 Oct 2026). One calculated line of 160,000p a month against a 160,000p budget.
        List<LineInput> lines = [Rent(160_000)];

        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Value;

        Assert.That(result.Total, Is.EqualTo(new Pence(160_000)));
        Assert.That(result.BudgetDifference, Is.EqualTo(Pence.Zero));
        Assert.That(result.WithinBudget, Is.True);
    }

    [Test]
    public void MonthlyCost_totalOnePennyOverBudget_isNotWithinBudget()
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, [Rent(160_001)], Budget160000).Value;

        Assert.That(result.BudgetDifference, Is.EqualTo(new Pence(-1)));
        Assert.That(result.WithinBudget, Is.False);
    }

    [Test]
    public void MonthlyCost_linesGivenOutOfOrder_comeBackInTheFixedRentOrder()
    {
        List<LineInput> lines =
        [
            new AmountLine(CostCategory.Broadband, new Pence(3_000), Period.Month, _anyEvidence),
            new IncludedLine(CostCategory.Water, _anyEvidence),
            new AmountLine(CostCategory.Energy, new Pence(8_000), Period.Month, _anyEvidence),
            new AmountLine(CostCategory.CouncilTax, new Pence(160_000), Period.Year, _anyEvidence),
            Rent(120_000),
        ];

        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Value;

        Assert.That(
            result.Lines.Select(l => l.Category),
            Is.EqualTo(_rentOrder));
    }

    [Test]
    public void MonthlyCost_linesGivenOutOfOrder_comeBackInTheFixedBuyOrder()
    {
        List<LineInput> lines =
        [
            new NotCalculatedLine(CostCategory.Maintenance, _anyEvidence),
            new AmountLine(CostCategory.Water, new Pence(4_500), Period.Month, _anyEvidence),
            new IncludedLine(CostCategory.BuildingsInsurance, _anyEvidence),
            new AmountLine(CostCategory.GroundRent, new Pence(25_000), Period.Year, _anyEvidence),
            new AmountLine(CostCategory.MortgageRepayment, new Pence(98_254), Period.Month, _anyEvidence),
            new AmountLine(CostCategory.ServiceCharge, new Pence(240_000), Period.Year, _anyEvidence),
            new AmountLine(CostCategory.Energy, new Pence(8_500), Period.Month, _anyEvidence),
            new AmountLine(CostCategory.Broadband, new Pence(3_000), Period.Month, _anyEvidence),
            new AmountLine(CostCategory.CouncilTax, new Pence(210_000), Period.Year, _anyEvidence),
        ];

        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Buy, lines, Budget160000).Value;

        Assert.That(
            result.Lines.Select(l => l.Category),
            Is.EqualTo(_buyOrder));
    }

    [Test]
    public void MonthlyCost_yearlyLine_keepsItsSourcePeriodAndEvidence()
    {
        List<LineInput> lines =
        [
            Rent(120_000),
            new AmountLine(CostCategory.CouncilTax, new Pence(160_000), Period.Year, _councilTaxEvidence),
        ];

        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Value;

        LineResult councilTax = result.Lines.Single(l => l.Category == CostCategory.CouncilTax);
        Assert.That(councilTax.Amount, Is.EqualTo(new Pence(13_333)));
        Assert.That(councilTax.SourcePeriod, Is.EqualTo(Period.Year));
        Assert.That(councilTax.EvidenceIds, Is.EqualTo(_councilTaxEvidence));
    }

    [Test]
    public void MonthlyCost_nonCalculatedLines_haveNoAmountAndNoSourcePeriod()
    {
        List<LineInput> lines =
        [
            Rent(120_000),
            new IncludedLine(CostCategory.Water, _anyEvidence),
            new NotCalculatedLine(CostCategory.Energy, _anyEvidence),
            new ConflictingLine(CostCategory.Broadband, _anyEvidence),
            new MissingLine(CostCategory.CouncilTax),
        ];

        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Value;

        List<LineResult> others = result.Lines.Where(l => l.Category != CostCategory.Rent).ToList();
        Assert.That(others.Select(l => l.Amount), Has.All.Null);
        Assert.That(others.Select(l => l.SourcePeriod), Has.All.Null);
        Assert.That(result.Total, Is.EqualTo(new Pence(120_000)));
    }

    [Test]
    public void MonthlyCost_missingLine_makesTheTotalPartialWithACodedReason()
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, [Rent(120_000), new MissingLine(CostCategory.Water)], Budget160000).Value;

        Assert.That(result.IsPartial, Is.True);
        Assert.That(result.PartialReasons, Is.EqualTo(new[] { new PartialReason(CostCategory.Water, LineStatus.Missing) }));
    }

    [Test]
    public void MonthlyCost_includedLine_doesNotMakeTheTotalPartial()
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, [Rent(120_000), new IncludedLine(CostCategory.Water, _anyEvidence)], Budget160000).Value;

        Assert.That(result.IsPartial, Is.False);
        Assert.That(result.PartialReasons, Is.Empty);
    }

    [Test]
    public void MonthlyCost_tinyYearlyAmount_roundsToZeroButStaysCalculated()
    {
        // 5p a year is 0.41667p a month, which rounds to 0p (rounding-boundaries.json). A calculated 0p is not the same as missing.
        List<LineInput> lines = [Rent(120_000), new AmountLine(CostCategory.CouncilTax, new Pence(5), Period.Year, _anyEvidence)];

        MonthlyBreakdown result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Value;

        Assert.That(result.Lines.Single(l => l.Category == CostCategory.CouncilTax).Amount, Is.EqualTo(Pence.Zero));
    }

    [TestCase(Mode.Rent)]
    [TestCase(Mode.Buy)]
    public void MonthlyCost_noAnchorLine_failsAsMissing(Mode mode)
    {
        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(mode, [new AmountLine(CostCategory.Energy, new Pence(8_000), Period.Month, _anyEvidence)], Budget160000);

        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error.Code, Is.EqualTo(mode == Mode.Rent ? "input.missing.rent" : "input.missing.mortgage-repayment"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [Test]
    public void MonthlyCost_anchorLineThatIsNotAnAmount_failsAsMissing()
    {
        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(Mode.Rent, [new ConflictingLine(CostCategory.Rent, _anyEvidence)], Budget160000);

        Assert.That(result.Error.Code, Is.EqualTo("input.missing.rent"));
    }

    [Test]
    public void MonthlyCost_rentGivenYearly_failsAsWrongPeriod()
    {
        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(Mode.Rent, [new AmountLine(CostCategory.Rent, new Pence(1_440_000), Period.Year, _anyEvidence)], Budget160000);

        Assert.That(result.Error.Code, Is.EqualTo("input.wrong-period.rent"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [Test]
    public void MonthlyCost_billGivenOnce_failsAsWrongPeriod()
    {
        List<LineInput> lines = [Rent(120_000), new AmountLine(CostCategory.Energy, new Pence(8_000), Period.Once, _anyEvidence)];

        Assert.That(MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Error.Code, Is.EqualTo("input.wrong-period.energy"));
    }

    [TestCase(0L)]
    [TestCase(-1L)]
    public void MonthlyCost_amountNotPositive_failsAsNotPositive(long pence)
    {
        List<LineInput> lines = [Rent(120_000), new AmountLine(CostCategory.Energy, new Pence(pence), Period.Month, _anyEvidence)];

        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000);

        Assert.That(result.Error.Code, Is.EqualTo("input.not-positive.energy"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [Test]
    public void MonthlyCost_budgetNotPositive_failsAsNotPositive() =>
        Assert.That(MonthlyCost.Calculate(Mode.Rent, [Rent(120_000)], Pence.Zero).Error.Code, Is.EqualTo("input.not-positive.budget"));

    [Test]
    public void MonthlyCost_sameCategoryTwice_failsAsAmbiguous()
    {
        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(Mode.Rent, [Rent(120_000), Rent(130_000)], Budget160000);

        Assert.That(result.Error.Code, Is.EqualTo("input.ambiguous.rent"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Conflict));
    }

    [Test]
    public void MonthlyCost_lineThatDoesNotBelongToTheMode_failsAsNotForMode()
    {
        List<LineInput> lines = [Rent(120_000), new AmountLine(CostCategory.ServiceCharge, new Pence(240_000), Period.Year, _anyEvidence)];

        Result<MonthlyBreakdown> result = MonthlyCost.Calculate(Mode.Rent, lines, Budget160000);

        Assert.That(result.Error.Code, Is.EqualTo("input.not-for-mode.service-charge"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Validation));
    }

    [Test]
    public void MonthlyCost_upfrontCategoryInAMonthlyList_failsAsNotForMode()
    {
        List<LineInput> lines = [Rent(120_000), new AmountLine(CostCategory.Deposit, new Pence(138_000), Period.Once, _anyEvidence)];

        Assert.That(MonthlyCost.Calculate(Mode.Rent, lines, Budget160000).Error.Code, Is.EqualTo("input.not-for-mode.deposit"));
    }

    [Test]
    public void MonthlyCost_nullLines_throws() =>
        Assert.Throws<ArgumentNullException>(() => MonthlyCost.Calculate(Mode.Rent, null!, Budget160000));

    [Test]
    public void MonthlyCost_nullLineInTheList_throws() =>
        Assert.Throws<ArgumentException>(() => MonthlyCost.Calculate(Mode.Rent, [Rent(120_000), null!], Budget160000));

    [Test]
    public void MonthlyCost_undefinedMode_throws() =>
        Assert.Throws<ArgumentOutOfRangeException>(() => MonthlyCost.Calculate((Mode)99, [Rent(120_000)], Budget160000));

    [Test]
    public void MonthlyCost_totalTooBigForALong_throwsOverflow()
    {
        List<LineInput> lines = [Rent(long.MaxValue), new AmountLine(CostCategory.Energy, new Pence(1), Period.Month, _anyEvidence)];

        Assert.Throws<OverflowException>(() => MonthlyCost.Calculate(Mode.Rent, lines, Budget160000));
    }

    private static AmountLine Rent(long pence) =>
        new(CostCategory.Rent, new Pence(pence), Period.Month, _anyEvidence);

    private static void AssertLinesMatch(IReadOnlyList<LineResult> actual, JsonArray expected)
    {
        Assert.That(actual, Has.Count.EqualTo(expected.Count));
        foreach (JsonNode? expectedLine in expected)
        {
            CostCategory category = CaseLines.Category(expectedLine!["category"]!.GetValue<string>());
            LineResult line = actual.Single(l => l.Category == category);

            if (expectedLine["monthlyPence"] is { } monthly)
            {
                Assert.That(line.Status, Is.EqualTo(LineStatus.Calculated), category.ToString());
                Assert.That(line.Amount, Is.EqualTo(new Pence(monthly.GetValue<long>())), category.ToString());
            }
            else
            {
                Assert.That(line.Amount, Is.Null, category.ToString());
                Assert.That(CostCategories.StatusId(line.Status), Is.EqualTo(expectedLine["status"]!.GetValue<string>()), category.ToString());
            }
        }
    }

    /// <summary>
    /// The worked cases give each reason as prose that starts with the category ("water: not settled yet"). The engine
    /// gives codes instead, so only the category before the colon is compared (plan 4b, known risk 4).
    /// </summary>
    private static void AssertPartialReasonsMatch(IReadOnlyList<PartialReason> actual, JsonArray expected)
    {
        string[] expectedCategories = expected.Select(r => r!.GetValue<string>().Split(':')[0]).ToArray();

        Assert.That(actual.Select(r => CostCategories.ToId(r.Category)), Is.EquivalentTo(expectedCategories));
    }

    [Test]
    public void CostCategories_undefinedValues_throw()
    {
        Assert.That(() => CostCategories.ToId((CostCategory)999), Throws.TypeOf<ArgumentOutOfRangeException>());
        Assert.That(() => CostCategories.StatusId((LineStatus)999), Throws.TypeOf<ArgumentOutOfRangeException>());
    }

    [Test]
    public void CostCategories_missingStatus_isNamedMissing() =>
        Assert.That(CostCategories.StatusId(LineStatus.Missing), Is.EqualTo("missing"));

    [Test]
    public void MonthlyCost_unknownKindOfLine_throwsForThatLine() =>
        Assert.That(() => MonthlyCost.Calculate(Mode.Rent, [new UnknownLine()], Budget160000), Throws.ArgumentException);

    private sealed record UnknownLine() : LineInput(CostCategory.Rent, []);
}
