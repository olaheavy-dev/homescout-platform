namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Every worked case in test-cases/story-calculations.json must be run by a data-driven test, so a new case cannot be
/// added to the file and quietly never checked. No case is deferred any more: the service-charge difference runs through
/// HomeCostBuilder (and, end to end, in the generator tests).
/// </summary>
[TestFixture]
internal sealed class StoryCalculationCoverageTests
{
    [Test]
    public void StoryCalculations_everyCase_isRunByADataDrivenTest()
    {
        IEnumerable<string> run = StoryCases.IdsWithInput("annualRate")
            .Concat(MonthlyCostTests.CaseIds)
            .Concat(UpfrontCashTests.CaseIds)
            .Concat(BudgetBeatTests.CaseIds)
            .Concat(HomeCostBuilderTests.CaseIds);

        Assert.That(run, Is.EquivalentTo(StoryCases.AllIds));
    }
}
