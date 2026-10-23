using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// HomeCostBuilder: scenarios derived from the evidence, and what changes between them. The service-charge change is
/// checked against the independently worked case in test-cases/story-calculations.json; the other tests use arbitrary
/// inputs with the working shown in a comment.
/// </summary>
[TestFixture]
internal sealed class HomeCostBuilderTests
{
    private const string _differenceCaseId = "b1-service-charge-difference";

    private static readonly int[] _fourSteps = [1, 2, 3, 4];

    /// <summary>The ids of the cases this fixture runs against the file.</summary>
    public static IEnumerable<string> CaseIds { get; } = [_differenceCaseId];

    private static HomeCosts Build(HomeFacts facts, IReadOnlyList<int> steps)
    {
        Result<HomeCosts> result = HomeCostBuilder.Build(facts, steps);
        Assert.That(result.IsSuccess, Is.True, result.IsFailure ? result.Error.Code : string.Empty);
        return result.Value;
    }

    private static string FailureCode(HomeFacts facts, IReadOnlyList<int> steps)
    {
        Result<HomeCosts> result = HomeCostBuilder.Build(facts, steps);
        Assert.That(result.IsFailure, Is.True);
        return result.Error.Code;
    }

    private static HomeFacts BuyerWithServiceChargeChange(long oldYearly, long newYearly) =>
        TestFacts.Buying(
        [
            TestFacts.Money("SC-OLD", "service-charge", oldYearly, Period.Year, EvidenceStatus.Conflicting, usedFromStep: 1),
            TestFacts.Money("SC-NEW", "service-charge", newYearly, Period.Year, usedFromStep: 4, supersedes: "SC-OLD"),
        ]);

    [Test]
    public void ServiceChargeChange_storyCase_matchesWorkedResult()
    {
        JsonNode inputs = StoryCases.Case(_differenceCaseId)["inputs"]!;
        JsonNode expected = StoryCases.Case(_differenceCaseId)["expected"]!;
        long listing = inputs["listingServiceChargeAnnualPence"]!.GetValue<long>();
        long budget = inputs["budgetServiceChargeAnnualPence"]!.GetValue<long>();

        HomeCosts home = Build(BuyerWithServiceChargeChange(listing, budget), _fourSteps);

        CostChange change = home.Scenarios[1].Changes.Single(c => c.Category == CostCategory.ServiceCharge);
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.ValueChanged));
        Assert.That(change.AnnualDifference, Is.EqualTo(new Pence(expected["annualDifferencePence"]!.GetValue<long>())));
        Assert.That(change.MonthlyDifference, Is.EqualTo(new Pence(expected["monthlyDifferencePence"]!.GetValue<long>())));
    }

    [Test]
    public void Build_evidenceChangesAtStepFour_givesTwoScenariosNamedFromTheirFirstStep()
    {
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 372_000), _fourSteps);

        Assert.That(home.Scenarios.Select(s => s.ScenarioId), Is.EqualTo(new List<string> { "from-step-1", "from-step-4" }));
        Assert.That(home.Scenarios.Select(s => (s.FromStep, s.ToStep)), Is.EqualTo(new List<(int, int)> { (1, 3), (4, 4) }));
    }

    [Test]
    public void Build_sameEvidenceAtEveryStep_givesOneScenarioCoveringAllSteps()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("EN", "energy", 9_000, Period.Month)]);

        HomeCosts home = Build(facts, _fourSteps);

        ScenarioCosts only = home.Scenarios.Single();
        Assert.That(only.ScenarioId, Is.EqualTo("from-step-1"));
        Assert.That((only.FromStep, only.ToStep), Is.EqualTo((1, 4)));
        Assert.That(only.Changes, Is.Empty);
        Assert.That(only.MonthlyTotalChange, Is.Null);
    }

    [Test]
    public void Build_firstScenario_hasNoChanges()
    {
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 372_000), _fourSteps);

        Assert.That(home.Scenarios[0].Changes, Is.Empty);
        Assert.That(home.Scenarios[0].MonthlyTotalChange, Is.Null);
    }

    [Test]
    public void Build_monthlyDifference_isTheDifferenceOfTheRoundedMonthlyLines()
    {
        // 100,000p a year is 8,333.33p a month, which rounds to 8,333p. 200,000p a year is 16,666.67p, which rounds to 16,667p.
        // The monthly difference is 16,667 - 8,333 = 8,334p (not 100,000 / 12 = 8,333p). The annual difference is 100,000p.
        HomeCosts home = Build(BuyerWithServiceChargeChange(100_000, 200_000), _fourSteps);

        CostChange change = home.Scenarios[1].Changes.Single(c => c.Category == CostCategory.ServiceCharge);
        Assert.That(change.MonthlyDifference, Is.EqualTo(new Pence(8_334)));
        Assert.That(change.AnnualDifference, Is.EqualTo(new Pence(100_000)));
        Assert.That(home.Scenarios[1].MonthlyTotalChange, Is.EqualTo(new Pence(8_334)));
    }

    [Test]
    public void Build_changeEvidence_namesThePreviousAndCurrentItems()
    {
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 372_000), _fourSteps);

        CostChange change = home.Scenarios[1].Changes.Single();
        Assert.That(change.PreviousEvidenceIds, Is.EqualTo(new List<string> { "SC-OLD" }));
        Assert.That(change.CurrentEvidenceIds, Is.EqualTo(new List<string> { "SC-NEW" }));
    }

    [Test]
    public void Build_conflictingWaterThenAnEstimate_isReportedAsNowCalculated()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.Other("W-LISTING", "water-responsibility", EvidenceStatus.Conflicting),
            TestFacts.Money("W-EST", "water", 4_500, Period.Month, usedFromStep: 4),
        ]);

        HomeCosts home = Build(facts, _fourSteps);

        CostChange change = home.Scenarios[1].Changes.Single(c => c.Category == CostCategory.Water);
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.NowCalculated));
        Assert.That(change.MonthlyDifference, Is.Null);
        Assert.That(change.AnnualDifference, Is.Null);
        Assert.That(change.PreviousEvidenceIds, Is.EqualTo(new List<string> { "W-LISTING" }));
        Assert.That(change.CurrentEvidenceIds, Is.EqualTo(new List<string> { "W-EST" }));
        Assert.That(home.Scenarios[0].Monthly.IsPartial, Is.True);
        Assert.That(home.Scenarios[1].Monthly.Lines.Single(l => l.Category == CostCategory.Water).Status, Is.EqualTo(LineStatus.Calculated));
    }

    [Test]
    public void Build_amountThenIncluded_isReportedAsNoLongerCalculated()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("INS-OLD", "buildings-insurance", 3_000, Period.Month, usedFromStep: 1),
            TestFacts.NoValue("INS-NEW", "buildings-insurance", EvidenceStatus.Included) with { UsedFromStep = 4, Supersedes = "INS-OLD" },
        ]);

        HomeCosts home = Build(facts, _fourSteps);

        Assert.That(home.Scenarios[1].Changes.Single(c => c.Category == CostCategory.BuildingsInsurance).Kind, Is.EqualTo(ChangeKind.NoLongerCalculated));
    }

    [Test]
    public void Build_statusChangeBetweenTwoLinesWithNoAmount_isReportedAsEvidenceChanged()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.NoValue("M-OLD", "maintenance", EvidenceStatus.NotCalculated),
            TestFacts.NoValue("M-NEW", "maintenance", EvidenceStatus.Included) with { UsedFromStep = 4, Supersedes = "M-OLD" },
        ]);

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

        Assert.That(change.Kind, Is.EqualTo(ChangeKind.EvidenceChanged));
        Assert.That(change.MonthlyDifference, Is.Null);
    }

    [Test]
    public void Build_newEvidenceWithTheSameAmount_isReportedAsEvidenceChangedNotValueChanged()
    {
        // 240,000p a year both times: no figure moves, only the source does.
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 240_000), _fourSteps);

        CostChange change = home.Scenarios[1].Changes.Single();
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.EvidenceChanged));
        Assert.That(change.MonthlyDifference, Is.Null);
        Assert.That(change.AnnualDifference, Is.Null);
    }

    [Test]
    public void Build_yearlyAmountRisesByOnePenceButMonthlyRoundingHidesIt_stillReportsTheAnnualDifference()
    {
        // 240,000p a year is exactly 20,000p a month; 240,001p a year is 20,000.08p, which also rounds to 20,000p.
        // The source amount rose by 1p, so this is a value change: monthly difference 0p, annual difference 1p.
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 240_001), _fourSteps);

        CostChange change = home.Scenarios[1].Changes.Single();
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.ValueChanged));
        Assert.That(change.MonthlyDifference, Is.EqualTo(Pence.Zero));
        Assert.That(change.AnnualDifference, Is.EqualTo(new Pence(1)));
    }

    [Test]
    public void Build_sameAmountChangingPeriod_isReportedAsValueChanged()
    {
        // 12,000p a month and 144,000p a year are both 12,000p a month, but the source changed from monthly to yearly.
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("E-OLD", "energy", 12_000, Period.Month, usedFromStep: 1),
            TestFacts.Money("E-NEW", "energy", 144_000, Period.Year, usedFromStep: 4, supersedes: "E-OLD"),
        ]);

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

        Assert.That(change.Kind, Is.EqualTo(ChangeKind.ValueChanged));
        Assert.That(change.MonthlyDifference, Is.EqualTo(Pence.Zero));
        Assert.That(change.AnnualDifference, Is.Null);
    }

    [Test]
    public void Build_amountThenNotApplicable_isReportedAsNoLongerApplies()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("SC-OLD", "service-charge", 240_000, Period.Year, usedFromStep: 1),
            TestFacts.NoValue("SC-NEW", "service-charge", EvidenceStatus.NotApplicable) with { UsedFromStep = 4, Supersedes = "SC-OLD" },
        ]);

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

        Assert.That(change.Kind, Is.EqualTo(ChangeKind.NoLongerApplies));
        Assert.That(change.CurrentEvidenceIds, Is.Empty);
    }

    [Test]
    public void Build_conflictingThenNotApplicable_isReportedAsNoLongerApplies()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.NoValue("GR-OLD", "ground-rent", EvidenceStatus.Conflicting),
            TestFacts.NoValue("GR-NEW", "ground-rent", EvidenceStatus.NotApplicable) with { UsedFromStep = 4, Supersedes = "GR-OLD" },
        ]);

        Assert.That(Build(facts, _fourSteps).Scenarios[1].Changes.Single().Kind, Is.EqualTo(ChangeKind.NoLongerApplies));
    }

    [Test]
    public void Build_amountThatChanges_isReportedAsValueChanged()
    {
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 372_000), _fourSteps);

        Assert.That(home.Scenarios[1].Changes.Single().Kind, Is.EqualTo(ChangeKind.ValueChanged));
    }

    // monthlyTotalChange is only given when both totals leave out the same lines (rule 7: a line that becomes unknown must
    // not look like a saving).

    [Test]
    public void Build_lineThatBecomesConflicting_givesNoMonthlyTotalChange()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("SC-OLD", "service-charge", 240_000, Period.Year, usedFromStep: 1),
            TestFacts.NoValue("SC-NEW", "service-charge", EvidenceStatus.Conflicting) with { UsedFromStep = 2, Supersedes = "SC-OLD" },
        ]);

        HomeCosts home = Build(facts, _fourSteps);

        Assert.That(home.Scenarios[1].MonthlyTotalChange, Is.Null);
        Assert.That(home.Scenarios[1].Changes.Single().Kind, Is.EqualTo(ChangeKind.NoLongerCalculated));
    }

    [Test]
    public void Build_conflictingWaterThenAnEstimate_givesNoMonthlyTotalChange()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.Other("W-LISTING", "water-responsibility", EvidenceStatus.Conflicting),
            TestFacts.Money("W-EST", "water", 4_500, Period.Month, usedFromStep: 4),
        ]);

        Assert.That(Build(facts, _fourSteps).Scenarios[1].MonthlyTotalChange, Is.Null);
    }

    [Test]
    public void Build_sameLinesLeftOutOfBothTotals_keepsTheMonthlyTotalChange()
    {
        // The same lines are missing in both scenarios; only the service charge moves: 16,667 - 8,333 = 8,334p.
        HomeCosts home = Build(BuyerWithServiceChargeChange(100_000, 200_000), _fourSteps);

        Assert.That(home.Scenarios[1].MonthlyTotalChange, Is.EqualTo(new Pence(8_334)));
    }

    [Test]
    public void Build_monthlyLineOnTheSourceEvidenceButNewAmount_hasNoAnnualDifferenceWhenOnlyOneSideIsYearly()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("E-OLD", "energy", 9_000, Period.Month, usedFromStep: 1),
            TestFacts.Money("E-NEW", "energy", 120_000, Period.Year, usedFromStep: 4, supersedes: "E-OLD"),
        ]);

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

        Assert.That(change.MonthlyDifference, Is.EqualTo(new Pence(1_000)));
        Assert.That(change.AnnualDifference, Is.Null);
    }

    [Test]
    public void Build_buyingHome_hasAMortgageWithTheEvidenceBehindIt()
    {
        HomeCosts home = Build(TestFacts.Buying([]), [1]);

        MortgageSummary mortgage = home.Scenarios.Single().Mortgage!;
        Assert.That(mortgage.EvidenceIds, Is.EqualTo(new List<string> { "PRICE", "DEPOSIT", "RATE", "TERM" }));
        Assert.That(mortgage.Repayment.Loan, Is.EqualTo(new Pence(16_000_000)));
        Assert.That(home.Scenarios.Single().Monthly.Lines[0].Category, Is.EqualTo(CostCategory.MortgageRepayment));
        Assert.That(home.Scenarios.Single().Monthly.Lines[0].EvidenceIds, Is.EqualTo(mortgage.EvidenceIds));
    }

    [Test]
    public void Build_rentingHome_hasNoMortgage()
    {
        HomeFacts facts = TestFacts.Renting([TestFacts.Money("RENT", "rent", 100_000, Period.Month)]);

        Assert.That(Build(facts, [1]).Scenarios.Single().Mortgage, Is.Null);
    }

    [Test]
    public void Build_homeDetails_comeFromTheFacts()
    {
        HomeCosts home = Build(TestFacts.Buying([]), [1]);

        Assert.That((home.HomeId, home.Mode, home.Nation), Is.EqualTo(("T1", Mode.Buy, Nation.England)));
    }

    [Test]
    public void Build_anyMonthlyBudget_isCarriedIntoEachScenario()
    {
        HomeCosts home = Build(BuyerWithServiceChargeChange(240_000, 372_000), _fourSteps);

        Assert.That(home.Scenarios.Select(s => s.Monthly.Budget), Is.All.EqualTo(new Pence(200_000)));
    }

    // One test per error code the builder owns, and the failures it passes on.

    [Test]
    public void Build_homeOutsideEngland_failsAsNotCovered() =>
        Assert.That(FailureCode(TestFacts.Buying([], Nation.Wales), [1]), Is.EqualTo("home.not-covered"));

    [Test]
    public void Build_homeWithNoMode_failsAsModeMissing()
    {
        var facts = new HomeFacts("T1", null, Nation.England, TestFacts.BuyAnchors(), new Pence(200_000));

        Assert.That(FailureCode(facts, [1]), Is.EqualTo("home.mode-missing"));
    }

    [TestCase(new int[0])]
    [TestCase(new[] { 0, 1 })]
    [TestCase(new[] { 2, 1 })]
    [TestCase(new[] { 1, 1 })]
    public void Build_stepsThatAreEmptyBelowOneOrNotIncreasing_failAsOutOfRange(int[] steps) =>
        Assert.That(FailureCode(TestFacts.Buying([]), steps), Is.EqualTo("story.step-out-of-range"));

    [Test]
    public void Build_anchorInputMissing_passesOnTheSelectorsFailure()
    {
        var facts = new HomeFacts("T1", Mode.Buy, Nation.England, TestFacts.BuyAnchors().Where(e => e.Category != "mortgage-rate").ToList(), new Pence(200_000));

        Assert.That(FailureCode(facts, [1]), Is.EqualTo("input.missing.mortgage-rate"));
    }

    [Test]
    public void Build_depositLargerThanThePrice_failsBecauseTheLoanIsNotPositive()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "mortgage-deposit").ToList();
        evidence.Add(TestFacts.Money("DEPOSIT", "mortgage-deposit", 25_000_000, Period.Once));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000)), [1]), Is.EqualTo("mortgage.loan-not-positive"));
    }

    [Test]
    public void Build_noBudget_failsAsNotPositive()
    {
        var facts = new HomeFacts("T1", Mode.Buy, Nation.England, TestFacts.BuyAnchors(), Pence.Zero);

        Assert.That(FailureCode(facts, [1]), Is.EqualTo("input.not-positive.budget"));
    }

    [Test]
    public void Build_nullArguments_throw()
    {
        Assert.That(() => HomeCostBuilder.Build(null!, [1]), Throws.ArgumentNullException);
        Assert.That(() => HomeCostBuilder.Build(TestFacts.Buying([]), null!), Throws.ArgumentNullException);
    }

    // Figure ids (plan 4b, section 1).

    [Test]
    public void FigureIds_lineTotalBudgetAndChange_followTheContractFormat()
    {
        Assert.That(FigureIds.Line("B1", "from-step-1", "monthly", CostCategory.ServiceCharge), Is.EqualTo("B1.from-step-1.monthly.service-charge"));
        Assert.That(FigureIds.Total("B1", "from-step-4", "monthly"), Is.EqualTo("B1.from-step-4.monthly.total"));
        Assert.That(FigureIds.Budget("R1", "from-step-1"), Is.EqualTo("R1.from-step-1.monthly.budget"));
        Assert.That(FigureIds.MortgageLoan("B1", "from-step-1"), Is.EqualTo("B1.from-step-1.mortgage.loan"));
        Assert.That(FigureIds.Change("B1", "from-step-4", CostCategory.ServiceCharge), Is.EqualTo("B1.from-step-4.change.service-charge"));
        Assert.That(FigureIds.MonthlyTotalChange("B1", "from-step-4"), Is.EqualTo("B1.from-step-4.change.monthly-total"));
        Assert.That(FigureIds.Mortgage("B1", "from-step-1"), Is.EqualTo("B1.from-step-1.mortgage"));
        Assert.That(FigureIds.MonthlyRepayment("B1", "from-step-1"), Is.EqualTo("B1.from-step-1.mortgage.monthly-repayment"));
    }

    [Test]
    public void Build_homeOutsideEnglandAndNoSteps_reportsTheHomeFirst() =>
        Assert.That(FailureCode(TestFacts.Buying([], Nation.Wales), []), Is.EqualTo("home.not-covered"));

    [Test]
    public void Build_stepsThatStartAboveOne_areAccepted()
    {
        HomeCosts home = Build(TestFacts.Buying([]), [2, 3]);

        Assert.That(home.Scenarios.Single().FromStep, Is.EqualTo(2));
    }

    [Test]
    public void Build_upfrontLineGivenMonthly_failsAsWrongPeriod()
    {
        // The selector checks only the anchors; the upfront calculation rejects a one-off cost given per month.
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("MC", "moving-costs", 100_000, Period.Month)]);

        Assert.That(FailureCode(facts, [1]), Is.EqualTo("input.wrong-period.moving-costs"));
    }

    [Test]
    public void Build_upfrontLineOfZero_failsAsNotPositive()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("MC", "moving-costs", 0, Period.Once)]);

        Assert.That(FailureCode(facts, [1]), Is.EqualTo("input.not-positive.moving-costs"));
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

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

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

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

        Assert.That(change.Kind, Is.EqualTo(ChangeKind.EvidenceChanged));
    }

    [Test]
    public void Build_lineNotApplicableThenEstimated_isReportedAsNowCalculated()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            new EvidenceItem("W-OLD", "water", EvidenceStatus.NotApplicable, null, false, 1, null),
            TestFacts.Money("W-NEW", "water", 12_000, Period.Month, usedFromStep: 4, supersedes: "W-OLD"),
        ]);

        CostChange change = Build(facts, _fourSteps).Scenarios[1].Changes.Single();

        Assert.That(change.Category, Is.EqualTo(CostCategory.Water));
        Assert.That(change.Kind, Is.EqualTo(ChangeKind.NowCalculated));
        Assert.That(change.PreviousEvidenceIds, Is.Empty);
    }

    [Test]
    public void Build_onlyTheMortgageRateChanges_givesTwoScenariosWithARepaymentChange()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            new EvidenceItem("RATE-NEW", "mortgage-rate", EvidenceStatus.Available, new RateValue(600), false, 4, "RATE"),
        ]);

        HomeCosts home = Build(facts, _fourSteps);

        Assert.That(home.Scenarios, Has.Count.EqualTo(2));
        Assert.That(home.Scenarios[1].Changes.Single(c => c.Category == CostCategory.MortgageRepayment).Kind, Is.EqualTo(ChangeKind.ValueChanged));
    }
}
