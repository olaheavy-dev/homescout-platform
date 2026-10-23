namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Tests added after the first Stryker.NET run (docs/reviews/2026-10-23-stage-2-mutation-report.md). Each one kills a
/// mutant that survived because no test pinned the behaviour: a boundary of a comparison, a guard on a hostile argument,
/// the wording a person reads in an error, or an upfront-only code path. They use arbitrary inputs; none checks a calculated figure.
/// </summary>
[TestFixture]
internal sealed class MutationSurvivorTests
{
    private static readonly Pence _budget = new(200_000);

    private static Error SelectError(HomeFacts facts)
    {
        Result<SelectedInputs> result = AssumptionSelector.Select(facts, 1);
        Assert.That(result.IsFailure, Is.True);
        return result.Error;
    }

    // Pence comparison operators: equal amounts are on the boundary.

    [Test]
    public void Pence_equalAmounts_areNotStrictlyLessOrGreater()
    {
        var a = new Pence(500);
        var b = new Pence(500);

        Assert.That(a < b, Is.False);
        Assert.That(a > b, Is.False);
        Assert.That(a <= b, Is.True);
        Assert.That(a >= b, Is.True);
    }

    [Test]
    public void RoundRatio_zeroDenominator_saysTheDenominatorIsTheProblem() =>
        Assert.That(() => Pence.RoundRatio(1, 0), Throws.TypeOf<DivideByZeroException>().With.Message.Contains("denominator"));

    // Result: misuse messages tell the programmer what went wrong.

    [Test]
    public void Result_readingTheWrongSide_explainsWhichSideIsMissing()
    {
        Result ok = Result.Success();
        Result<Pence> okValue = Result.Success(new Pence(1));
        Result<Pence> failed = Result.Failure<Pence>(new Error("a.b", "Something is wrong.", ErrorCategory.Validation));

        Assert.That(() => ok.Error, Throws.InvalidOperationException.With.Message.Contains("no error"));
        Assert.That(() => okValue.Error, Throws.InvalidOperationException.With.Message.Contains("no error"));
        Assert.That(() => failed.Value, Throws.InvalidOperationException.With.Message.Contains("no value"));
    }

    [Test]
    public void ToResult_successWithAValue_isASuccess() =>
        Assert.That(Result.Success(new Pence(1)).ToResult().IsSuccess, Is.True);

    [Test]
    public void ToResult_failure_keepsTheError()
    {
        var error = new Error("a.b", "Something is wrong.", ErrorCategory.Conflict);

        Result result = Result.Failure<Pence>(error).ToResult();

        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error, Is.EqualTo(error));
    }

    [Test]
    public void Error_undefinedCategory_throwsAndNamesTheCategory() =>
        Assert.That(() => new Error("a.b", "Something is wrong.", (ErrorCategory)999),
            Throws.TypeOf<ArgumentOutOfRangeException>().With.Message.Contains("Unknown error category"));

    // Enum guards: a value that is not defined is a programming error and says so.

    [Test]
    public void ToId_undefinedCategory_throws() =>
        Assert.That(() => CostCategories.ToId((CostCategory)999), Throws.TypeOf<ArgumentOutOfRangeException>().With.Message.Contains("Unknown cost category"));

    [Test]
    public void StatusId_undefinedStatus_throws() =>
        Assert.That(() => CostCategories.StatusId((LineStatus)999), Throws.TypeOf<ArgumentOutOfRangeException>().With.Message.Contains("Unknown line status"));

    [Test]
    public void StatusId_missing_isNamedMissing() =>
        Assert.That(CostCategories.StatusId(LineStatus.Missing), Is.EqualTo("missing"));

    [Test]
    public void Calculate_undefinedMode_throwsForMonthlyAndUpfront()
    {
        Assert.That(() => MonthlyCost.Calculate((Mode)99, [], _budget), Throws.TypeOf<ArgumentOutOfRangeException>().With.Message.Contains("Unknown mode"));
        Assert.That(() => UpfrontCash.Calculate((Mode)99, []), Throws.TypeOf<ArgumentOutOfRangeException>().With.Message.Contains("Unknown mode"));
    }

    [Test]
    public void Calculate_nullLine_saysALineIsNull() =>
        Assert.That(() => MonthlyCost.Calculate(Mode.Rent, [null!], _budget), Throws.ArgumentException.With.Message.Contains("null"));

    [Test]
    public void Calculate_unknownKindOfLine_throwsAndNamesTheType() =>
        Assert.That(() => MonthlyCost.Calculate(Mode.Rent, [new UnknownLine()], _budget),
            Throws.ArgumentException.With.Message.Contains(nameof(UnknownLine)));

    // Selector.

    [Test]
    public void Select_nullEvidenceList_throws()
    {
        var facts = new HomeFacts("T1", Mode.Buy, Nation.England, null!, _budget);

        Assert.That(() => AssumptionSelector.Select(facts, 1), Throws.ArgumentNullException.With.Property("ParamName").EqualTo("facts.Evidence"));
    }

    [Test]
    public void Select_upfrontCostGivenAsRate_failsAsWrongKind()
    {
        HomeFacts facts = TestFacts.Buying([new EvidenceItem("MC", "moving-costs", EvidenceStatus.Available, new RateValue(500), false, null, null)]);

        Assert.That(SelectError(facts).Code, Is.EqualTo("input.wrong-kind.moving-costs"));
    }

    [Test]
    public void Select_wrongPeriodMessages_sayWhichPeriodIsNeeded()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "asking-price").ToList();
        evidence.Add(TestFacts.Money("PRICE", "asking-price", 20_000_000, Period.Month));
        Error price = SelectError(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, _budget));
        Error rent = SelectError(TestFacts.Renting([TestFacts.Money("RENT", "rent", 1_200_000, Period.Year)]));

        Assert.That(price.Message, Does.Contain("one-off"));
        Assert.That(rent.Message, Does.Contain("monthly"));
    }

    // Builder.

    [Test]
    public void Build_homeOutsideEnglandAndNoSteps_reportsTheHomeFirst()
    {
        Result<HomeCosts> result = HomeCostBuilder.Build(TestFacts.Buying([], Nation.Wales), []);

        Assert.That(result.Error.Code, Is.EqualTo("home.not-covered"));
    }

    [Test]
    public void Build_upfrontAmountChanges_isAValueChangeWithNoMonthlyOrAnnualDifference()
    {
        // The moving costs are paid once, so they have no monthly or annual difference to report.
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("MC-OLD", "moving-costs", 100_000, Period.Once, usedFromStep: 1),
            TestFacts.Money("MC-NEW", "moving-costs", 150_000, Period.Once, usedFromStep: 4, supersedes: "MC-OLD"),
        ]);

        Result<HomeCosts> result = HomeCostBuilder.Build(facts, [1, 2, 3, 4]);

        CostChange change = result.Value.Scenarios[1].Changes.Single();
        Assert.That(change.Category, Is.EqualTo(CostCategory.MovingCosts));
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.ValueChanged));
        Assert.That(change.MonthlyDifference, Is.Null);
        Assert.That(change.AnnualDifference, Is.Null);
    }

    [Test]
    public void Build_upfrontAmountThenSameAmountFromNewEvidence_isAnEvidenceChange()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("MC-OLD", "moving-costs", 100_000, Period.Once, usedFromStep: 1),
            TestFacts.Money("MC-NEW", "moving-costs", 100_000, Period.Once, usedFromStep: 4, supersedes: "MC-OLD"),
        ]);

        CostChange change = HomeCostBuilder.Build(facts, [1, 2, 3, 4]).Value.Scenarios[1].Changes.Single();

        Assert.That(change.Kind, Is.EqualTo(ChangeKind.EvidenceChanged));
    }

    [Test]
    public void Build_stepsThatStartAboveOne_areAccepted()
    {
        Result<HomeCosts> result = HomeCostBuilder.Build(TestFacts.Buying([]), [2, 3]);

        Assert.That(result.IsSuccess, Is.True);
        Assert.That(result.Value.Scenarios.Single().FromStep, Is.EqualTo(2));
    }

    [Test]
    public void Build_lineNotApplicableThenEstimated_isReportedAsNowCalculated()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            new EvidenceItem("W-OLD", "water", EvidenceStatus.NotApplicable, null, false, 1, null),
            TestFacts.Money("W-NEW", "water", 12_000, Period.Month, usedFromStep: 4, supersedes: "W-OLD"),
        ]);

        CostChange change = HomeCostBuilder.Build(facts, [1, 2, 3, 4]).Value.Scenarios[1].Changes.Single();

        Assert.That(change.Category, Is.EqualTo(CostCategory.Water));
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.NowCalculated));
    }

    [Test]
    public void Build_onlyTheMortgageRateChanges_givesTwoScenarios()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            new EvidenceItem("RATE-NEW", "mortgage-rate", EvidenceStatus.Available, new RateValue(600), false, 4, "RATE"),
        ]);

        Result<HomeCosts> result = HomeCostBuilder.Build(facts, [1, 2, 3, 4]);

        Assert.That(result.Value.Scenarios, Has.Count.EqualTo(2));
    }

    private sealed record UnknownLine() : LineInput(CostCategory.Rent, []);
}
