namespace HomeScout.CostEngine.Tests;

/// <summary>
/// The five selection rules of AssumptionSelector (plan 4b, section 2), one test group each, then one test per error code.
/// The amounts are arbitrary inputs; the expectations are which item is chosen and what kind of line comes out.
/// </summary>
[TestFixture]
internal sealed class AssumptionSelectorTests
{
    private static List<string> Ids(params string[] ids) => [.. ids];

    private static SelectedInputs Select(HomeFacts facts, int step = 1)
    {
        Result<SelectedInputs> result = AssumptionSelector.Select(facts, step);
        Assert.That(result.IsSuccess, Is.True, result.IsFailure ? result.Error.Code : string.Empty);
        return result.Value;
    }

    private static string FailureCode(HomeFacts facts, int step = 1)
    {
        Result<SelectedInputs> result = AssumptionSelector.Select(facts, step);
        Assert.That(result.IsFailure, Is.True);
        return result.Error.Code;
    }

    // Rule 1: context-only items are ignored.

    [Test]
    public void Select_contextOnlyItem_isIgnored()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("EPC-COST", "water", 78_000, Period.Year, contextOnly: true)]);

        LineInput? water = TestFacts.MonthlyLine(Select(facts), CostCategory.Water);

        Assert.That(water, Is.InstanceOf<MissingLine>());
    }

    // Rule 2: an item is in use from its step, until an item that supersedes it starts.

    [Test]
    public void Select_itemNotYetUsed_isIgnoredBeforeItsStep()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("EN-LATER", "energy", 9_000, Period.Month, usedFromStep: 4)]);

        Assert.That(TestFacts.MonthlyLine(Select(facts, 3), CostCategory.Energy), Is.InstanceOf<MissingLine>());
        Assert.That(TestFacts.MonthlyLine(Select(facts, 4), CostCategory.Energy), Is.InstanceOf<AmountLine>());
    }

    [Test]
    public void Select_itemWithNoStartStep_isInUseFromTheFirstStep()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("EN", "energy", 9_000, Period.Month)]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.Energy), Is.InstanceOf<AmountLine>());
    }

    [Test]
    public void Select_supersededItem_isUsedUntilTheNewOneStarts()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("SC-OLD", "service-charge", 100_000, Period.Year, usedFromStep: 1),
            TestFacts.Money("SC-NEW", "service-charge", 200_000, Period.Year, usedFromStep: 4, supersedes: "SC-OLD"),
        ]);

        var before = (AmountLine)TestFacts.MonthlyLine(Select(facts, 3), CostCategory.ServiceCharge)!;
        var after = (AmountLine)TestFacts.MonthlyLine(Select(facts, 4), CostCategory.ServiceCharge)!;

        Assert.That(before.EvidenceIds, Is.EqualTo(Ids("SC-OLD")));
        Assert.That(after.EvidenceIds, Is.EqualTo(Ids("SC-NEW")));
    }

    // Rule 3: for each category, an amount first, then included, not-calculated, not-applicable, conflicting, missing.

    [TestCase(EvidenceStatus.Available)]
    [TestCase(EvidenceStatus.Conflicting)]
    [TestCase(EvidenceStatus.Stale)]
    public void Select_moneyItemWithAValue_givesAnAmountWhateverItsStatus(EvidenceStatus status)
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("EN", "energy", 9_000, Period.Month, status)]);

        var line = (AmountLine)TestFacts.MonthlyLine(Select(facts), CostCategory.Energy)!;

        Assert.That(line.Amount, Is.EqualTo(new Pence(9_000)));
        Assert.That(line.Period, Is.EqualTo(Period.Month));
        Assert.That(line.EvidenceIds, Is.EqualTo(Ids("EN")));
    }

    [Test]
    public void Select_includedItem_givesAnIncludedLine()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.NoValue("INS", "buildings-insurance", EvidenceStatus.Included)]);

        var line = TestFacts.MonthlyLine(Select(facts), CostCategory.BuildingsInsurance);

        Assert.That(line, Is.InstanceOf<IncludedLine>());
        Assert.That(line!.EvidenceIds, Is.EqualTo(Ids("INS")));
    }

    [Test]
    public void Select_notCalculatedItem_givesANotCalculatedLine()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.NoValue("STAMP", "stamp-duty", EvidenceStatus.NotCalculated)]);

        var line = TestFacts.UpfrontLine(Select(facts), CostCategory.StampDuty);

        Assert.That(line, Is.InstanceOf<NotCalculatedLine>());
        Assert.That(line!.EvidenceIds, Is.EqualTo(Ids("STAMP")));
    }

    [Test]
    public void Select_notApplicableItem_leavesTheLineOut()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.NoValue("SC", "service-charge", EvidenceStatus.NotApplicable)]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.ServiceCharge), Is.Null);
    }

    [Test]
    public void Select_conflictingItemWithoutAnAmount_givesAConflictingLine()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Other("GR", "ground-rent", EvidenceStatus.Conflicting)]);

        // A conflicting item that has a value which is not money is a wrong-kind failure; with no value at all it is a conflict.
        Assert.That(FailureCode(facts), Is.EqualTo("input.wrong-kind.ground-rent"));

        HomeFacts noValue = TestFacts.Buying([TestFacts.NoValue("GR", "ground-rent", EvidenceStatus.Conflicting)]);
        var line = TestFacts.MonthlyLine(Select(noValue), CostCategory.GroundRent);

        Assert.That(line, Is.InstanceOf<ConflictingLine>());
        Assert.That(line!.EvidenceIds, Is.EqualTo(Ids("GR")));
    }

    [Test]
    public void Select_noEvidenceForACategory_givesAMissingLineWithNoEvidence()
    {
        var line = TestFacts.MonthlyLine(Select(TestFacts.Buying([])), CostCategory.Broadband);

        Assert.That(line, Is.InstanceOf<MissingLine>());
        Assert.That(line!.EvidenceIds, Is.Empty);
    }

    [Test]
    public void Select_itemWithStatusMissing_givesAMissingLineWithNoEvidence()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.NoValue("BB", "broadband", EvidenceStatus.Missing)]);

        var line = TestFacts.MonthlyLine(Select(facts), CostCategory.Broadband);

        Assert.That(line, Is.InstanceOf<MissingLine>());
        Assert.That(line!.EvidenceIds, Is.Empty);
    }

    [Test]
    public void Select_lineThatDoesNotBelongToTheMode_isNotReturned()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.Money("SC", "service-charge", 100_000, Period.Year),
        ]);

        SelectedInputs inputs = Select(facts);

        Assert.That(inputs.MonthlyLines.Select(l => l.Category), Does.Not.Contain(CostCategory.ServiceCharge));
    }

    // Precedence between statuses (rule 3): money, then conflicting, then not-calculated, included, not-applicable, missing.

    [Test]
    public void Select_includedAlongsideConflicting_givesConflicting()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.NoValue("INS-1", "buildings-insurance", EvidenceStatus.Included),
            TestFacts.NoValue("INS-2", "buildings-insurance", EvidenceStatus.Conflicting),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.BuildingsInsurance), Is.InstanceOf<ConflictingLine>());
    }

    [Test]
    public void Select_includedWaterAlongsideConflictingResponsibility_givesConflicting()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.NoValue("W-INC", "water", EvidenceStatus.Included),
            TestFacts.Other("W-RESP", "water-responsibility", EvidenceStatus.Conflicting),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.Water), Is.InstanceOf<ConflictingLine>());
    }

    [Test]
    public void Select_notApplicableAlongsideConflicting_givesConflicting()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.NoValue("GR-1", "ground-rent", EvidenceStatus.NotApplicable),
            TestFacts.NoValue("GR-2", "ground-rent", EvidenceStatus.Conflicting),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.GroundRent), Is.InstanceOf<ConflictingLine>());
    }

    [Test]
    public void Select_notCalculatedAlongsideIncluded_givesNotCalculatedAsTheMoreCautious()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.NoValue("M-1", "maintenance", EvidenceStatus.Included),
            TestFacts.NoValue("M-2", "maintenance", EvidenceStatus.NotCalculated),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.Maintenance), Is.InstanceOf<NotCalculatedLine>());
    }

    [Test]
    public void Select_includedAlongsideNotApplicable_givesIncluded()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.NoValue("M-1", "maintenance", EvidenceStatus.NotApplicable),
            TestFacts.NoValue("M-2", "maintenance", EvidenceStatus.Included),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.Maintenance), Is.InstanceOf<IncludedLine>());
    }

    [Test]
    public void Select_moneyAlongsideConflicting_stillGivesTheAmount()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("EN-1", "energy", 9_000, Period.Month),
            TestFacts.NoValue("EN-2", "energy", EvidenceStatus.Conflicting),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.Energy), Is.InstanceOf<AmountLine>());
    }

    // Wrong kind is reported before ambiguous, for ordinary lines and for anchors.

    [Test]
    public void Select_wrongKindAndTwoValues_failsAsWrongKindForAnOrdinaryLine()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("EN-1", "energy", 9_000, Period.Month),
            new EvidenceItem("EN-2", "energy", EvidenceStatus.Available, new RateValue(500), false, null, null),
        ]);

        Assert.That(FailureCode(facts), Is.EqualTo("input.wrong-kind.energy"));
    }

    [Test]
    public void Select_wrongKindAndTwoValues_failsAsWrongKindForAnAnchor()
    {
        HomeFacts facts = TestFacts.Buying([new EvidenceItem("PRICE-2", "asking-price", EvidenceStatus.Available, new RateValue(500), false, null, null)]);

        Assert.That(FailureCode(facts), Is.EqualTo("input.wrong-kind.asking-price"));
    }

    [Test]
    public void Select_rentWithWrongKindAndTwoValues_failsAsWrongKind()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT-1", "rent", 100_000, Period.Month),
            new EvidenceItem("RENT-2", "rent", EvidenceStatus.Available, new YearsValue(3), false, null, null),
        ]);

        Assert.That(FailureCode(facts), Is.EqualTo("input.wrong-kind.rent"));
    }

    // Rule 2 with a chain: A is replaced by B from step 2, and B by C from step 3.

    private static HomeFacts Chain() =>
        TestFacts.Buying(
        [
            TestFacts.Money("SC-A", "service-charge", 100_000, Period.Year),
            TestFacts.Money("SC-B", "service-charge", 200_000, Period.Year, usedFromStep: 2, supersedes: "SC-A"),
            TestFacts.Money("SC-C", "service-charge", 300_000, Period.Year, usedFromStep: 3, supersedes: "SC-B"),
        ]);

    [TestCase(1, "SC-A")]
    [TestCase(2, "SC-B")]
    [TestCase(3, "SC-C")]
    [TestCase(4, "SC-C")]
    public void Select_supersedeChain_usesOnlyTheLatestItemThatHasStarted(int step, string expectedId)
    {
        var line = (AmountLine)TestFacts.MonthlyLine(Select(Chain(), step), CostCategory.ServiceCharge)!;

        Assert.That(line.EvidenceIds, Is.EqualTo(Ids(expectedId)));
    }

    // Rule 4: water-responsibility items count towards the water line, for the conflicting check only.

    [Test]
    public void Select_conflictingWaterResponsibility_givesConflictingWaterWithBothItems()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.Other("W-LISTING", "water-responsibility", EvidenceStatus.Conflicting),
            TestFacts.Other("W-STATEMENT", "water-responsibility", EvidenceStatus.Available),
        ]);

        var line = TestFacts.MonthlyLine(Select(facts), CostCategory.Water);

        Assert.That(line, Is.InstanceOf<ConflictingLine>());
        Assert.That(line!.EvidenceIds, Is.EqualTo(Ids("W-LISTING", "W-STATEMENT")));
    }

    [Test]
    public void Select_waterEstimate_winsOverConflictingResponsibility()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.Other("W-LISTING", "water-responsibility", EvidenceStatus.Conflicting),
            TestFacts.Money("W-EST", "water", 4_500, Period.Month, usedFromStep: 4),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts, 3), CostCategory.Water), Is.InstanceOf<ConflictingLine>());

        var after = (AmountLine)TestFacts.MonthlyLine(Select(facts, 4), CostCategory.Water)!;
        Assert.That(after.EvidenceIds, Is.EqualTo(Ids("W-EST")));
    }

    [Test]
    public void Select_waterResponsibility_doesNotAffectAnotherCategory()
    {
        HomeFacts facts = TestFacts.Renting(
        [
            TestFacts.Money("RENT", "rent", 100_000, Period.Month),
            TestFacts.Other("W-LISTING", "water-responsibility", EvidenceStatus.Conflicting),
        ]);

        Assert.That(TestFacts.MonthlyLine(Select(facts), CostCategory.Energy), Is.InstanceOf<MissingLine>());
    }

    // Rule 5: two in-use money items for one category are a failure.

    [Test]
    public void Select_twoMoneyItemsForOneCategory_failsAsAmbiguous()
    {
        HomeFacts facts = TestFacts.Buying(
        [
            TestFacts.Money("EN-1", "energy", 9_000, Period.Month),
            TestFacts.Money("EN-2", "energy", 9_500, Period.Month),
        ]);

        Result<SelectedInputs> result = AssumptionSelector.Select(facts, 1);

        Assert.That(result.Error.Code, Is.EqualTo("input.ambiguous.energy"));
        Assert.That(result.Error.Category, Is.EqualTo(ErrorCategory.Conflict));
    }

    // The inputs a purchase needs.

    [Test]
    public void Select_buyingHome_returnsTheMortgageInputsWithTheirEvidence()
    {
        MortgageInputs mortgage = Select(TestFacts.Buying([])).Mortgage!;

        Assert.That(mortgage.AskingPrice, Is.EqualTo(new Pence(20_000_000)));
        Assert.That(mortgage.Deposit, Is.EqualTo(new Pence(4_000_000)));
        Assert.That(mortgage.RateBasisPoints, Is.EqualTo(500));
        Assert.That(mortgage.TermYears, Is.EqualTo(20));
        Assert.That(mortgage.EvidenceIds, Is.EqualTo(Ids("PRICE", "DEPOSIT", "RATE", "TERM")));
    }

    [Test]
    public void Select_buyingHome_hasNoMortgageRepaymentLineAndTheDepositUpfront()
    {
        SelectedInputs inputs = Select(TestFacts.Buying([]));

        Assert.That(TestFacts.MonthlyLine(inputs, CostCategory.MortgageRepayment), Is.Null);
        var deposit = (AmountLine)TestFacts.UpfrontLine(inputs, CostCategory.MortgageDeposit)!;
        Assert.That(deposit.Amount, Is.EqualTo(new Pence(4_000_000)));
        Assert.That(deposit.Period, Is.EqualTo(Period.Once));
    }

    [Test]
    public void Select_rentingHome_hasNoMortgage()
    {
        HomeFacts facts = TestFacts.Renting([TestFacts.Money("RENT", "rent", 100_000, Period.Month)]);

        SelectedInputs inputs = Select(facts);

        Assert.That(inputs.Mortgage, Is.Null);
        Assert.That(TestFacts.MonthlyLine(inputs, CostCategory.Rent), Is.InstanceOf<AmountLine>());
    }

    // One test per error code.

    [TestCase("asking-price")]
    [TestCase("mortgage-deposit")]
    [TestCase("mortgage-rate")]
    [TestCase("mortgage-term")]
    public void Select_buyingWithoutAnAnchorInput_failsAsMissing(string category)
    {
        var facts = new HomeFacts("T1", Mode.Buy, Nation.England, TestFacts.BuyAnchors().Where(e => e.Category != category).ToList(), new Pence(200_000));

        Assert.That(FailureCode(facts), Is.EqualTo($"input.missing.{category}"));
    }

    [Test]
    public void Select_anchorItemWithStatusMissing_failsAsMissing()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "asking-price").ToList();
        evidence.Add(TestFacts.NoValue("PRICE", "asking-price", EvidenceStatus.Missing));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000))), Is.EqualTo("input.missing.asking-price"));
    }

    [Test]
    public void Select_rentingWithoutRent_failsAsMissing() =>
        Assert.That(FailureCode(TestFacts.Renting([])), Is.EqualTo("input.missing.rent"));

    [Test]
    public void Select_anchorFromTwoItems_failsAsAmbiguous()
    {
        HomeFacts facts = TestFacts.Buying([TestFacts.Money("PRICE-2", "asking-price", 21_000_000, Period.Once)]);

        Assert.That(FailureCode(facts), Is.EqualTo("input.ambiguous.asking-price"));
    }

    [Test]
    public void Select_priceGivenMonthly_failsAsWrongPeriod()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "asking-price").ToList();
        evidence.Add(TestFacts.Money("PRICE", "asking-price", 20_000_000, Period.Month));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000))), Is.EqualTo("input.wrong-period.asking-price"));
    }

    [Test]
    public void Select_depositGivenYearly_failsAsWrongPeriod()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "mortgage-deposit").ToList();
        evidence.Add(TestFacts.Money("DEPOSIT", "mortgage-deposit", 4_000_000, Period.Year));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000))), Is.EqualTo("input.wrong-period.mortgage-deposit"));
    }

    [Test]
    public void Select_rentGivenYearly_failsAsWrongPeriod() =>
        Assert.That(FailureCode(TestFacts.Renting([TestFacts.Money("RENT", "rent", 1_200_000, Period.Year)])), Is.EqualTo("input.wrong-period.rent"));

    [TestCase(0)]
    [TestCase(-1)]
    public void Select_rentNotMoreThanZero_failsAsNotPositive(long pence) =>
        Assert.That(FailureCode(TestFacts.Renting([TestFacts.Money("RENT", "rent", pence, Period.Month)])), Is.EqualTo("input.not-positive.rent"));

    [Test]
    public void Select_priceZero_failsAsNotPositive()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "asking-price").ToList();
        evidence.Add(TestFacts.Money("PRICE", "asking-price", 0, Period.Once));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000))), Is.EqualTo("input.not-positive.asking-price"));
    }

    [Test]
    public void Select_rateGivenAsMoney_failsAsWrongKind()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "mortgage-rate").ToList();
        evidence.Add(TestFacts.Money("RATE", "mortgage-rate", 500, Period.Once));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000))), Is.EqualTo("input.wrong-kind.mortgage-rate"));
    }

    [Test]
    public void Select_termGivenAsRate_failsAsWrongKind()
    {
        List<EvidenceItem> evidence = TestFacts.BuyAnchors().Where(e => e.Category != "mortgage-term").ToList();
        evidence.Add(new EvidenceItem("TERM", "mortgage-term", EvidenceStatus.Available, new RateValue(500), false, null, null));

        Assert.That(FailureCode(new HomeFacts("T1", Mode.Buy, Nation.England, evidence, new Pence(200_000))), Is.EqualTo("input.wrong-kind.mortgage-term"));
    }

    [Test]
    public void Select_serviceChargeGivenAsRate_failsAsWrongKind()
    {
        HomeFacts facts = TestFacts.Buying([new EvidenceItem("SC", "service-charge", EvidenceStatus.Available, new RateValue(500), false, null, null)]);

        Assert.That(FailureCode(facts), Is.EqualTo("input.wrong-kind.service-charge"));
    }

    [Test]
    public void Select_homeOutsideEngland_failsAsNotCovered()
    {
        HomeFacts facts = TestFacts.Buying([], Nation.Wales);

        Assert.That(FailureCode(facts), Is.EqualTo("home.not-covered"));
    }

    [Test]
    public void Select_homeWithNoMode_failsAsModeMissing()
    {
        var facts = new HomeFacts("T1", null, Nation.England, TestFacts.BuyAnchors(), new Pence(200_000));

        Assert.That(FailureCode(facts), Is.EqualTo("home.mode-missing"));
    }

    [TestCase(0)]
    [TestCase(-3)]
    public void Select_stepBelowOne_failsAsOutOfRange(int step) =>
        Assert.That(FailureCode(TestFacts.Buying([]), step), Is.EqualTo("story.step-out-of-range"));

    [Test]
    public void Select_nullFacts_throws() =>
        Assert.That(() => AssumptionSelector.Select(null!, 1), Throws.ArgumentNullException);
}
