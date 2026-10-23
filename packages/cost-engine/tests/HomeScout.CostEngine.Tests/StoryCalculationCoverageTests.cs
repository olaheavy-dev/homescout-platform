namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Every worked case in test-cases/story-calculations.json must be run by a data-driven test, so a new case cannot be
/// added to the file and quietly never checked. A case that needs the assumption selector or the generator (task 4b-2)
/// is listed here by name, with the reason, and that list is checked too.
/// </summary>
[TestFixture]
internal sealed class StoryCalculationCoverageTests
{
    /// <summary>Cases that wait for task 4b-2. Each id must exist in the file and must not also be run elsewhere.</summary>
    private static readonly Dictionary<string, string> _deferred = new(StringComparer.Ordinal)
    {
        ["b1-service-charge-difference"] =
            "The difference between two scenarios (annual and monthly) is worked out by the change step of HomeCostBuilder (4b-2).",
    };

    [Test]
    public void StoryCalculations_everyCase_isRunByADataDrivenTest()
    {
        IEnumerable<string> run = StoryCases.IdsWithInput("annualRate")
            .Concat(MonthlyCostTests.CaseIds)
            .Concat(UpfrontCashTests.CaseIds)
            .Concat(BudgetBeatTests.CaseIds)
            .Concat(_deferred.Keys);

        Assert.That(run, Is.EquivalentTo(StoryCases.AllIds));
    }

    [Test]
    public void StoryCalculations_caseWaitingForTask4b2_isNotAlsoRunInThisTask()
    {
        IEnumerable<string> run = StoryCases.IdsWithInput("annualRate")
            .Concat(MonthlyCostTests.CaseIds)
            .Concat(UpfrontCashTests.CaseIds)
            .Concat(BudgetBeatTests.CaseIds);

        Assert.That(run, Has.None.AnyOf(_deferred.Keys));
    }
}
