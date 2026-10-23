using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// The deliberate story beat: B1 is within the 1,600 pound budget on the listing service charge and over it on the
/// 2026 budget. Both totals come from the engine and are compared with the worked case.
/// </summary>
[TestFixture]
internal sealed class BudgetBeatTests
{
    /// <summary>The ids of the budget-beat cases: those that name the two monthly cases they combine.</summary>
    public static IEnumerable<string> CaseIds { get; } =
        StoryCases.IdsWhere(c => c["inputs"]!["listingTotalCase"] is not null).ToList();

    [Test]
    public void BudgetBeat_file_hasOneBudgetBeatCase() =>
        Assert.That(CaseIds.Count(), Is.EqualTo(1));

    [Test]
    public void BudgetBeat_storyCase_landsAsWorked()
    {
        JsonNode beat = StoryCases.Case(CaseIds.Single());
        MonthlyBreakdown onListing = Run(beat["inputs"]!["listingTotalCase"]!.GetValue<string>());
        MonthlyBreakdown onBudget = Run(beat["inputs"]!["budgetTotalCase"]!.GetValue<string>());
        JsonNode expected = beat["expected"]!;

        Assert.That(onListing.Total, Is.EqualTo(new Pence(expected["listingTotalPence"]!.GetValue<long>())));
        Assert.That(onBudget.Total, Is.EqualTo(new Pence(expected["budgetTotalPence"]!.GetValue<long>())));
        Assert.That(onListing.BudgetDifference, Is.EqualTo(new Pence(expected["listingBudgetDifferencePence"]!.GetValue<long>())));
        Assert.That(onBudget.BudgetDifference, Is.EqualTo(new Pence(expected["budgetBudgetDifferencePence"]!.GetValue<long>())));
        Assert.That(onListing.WithinBudget, Is.EqualTo(expected["withinBudgetOnListing"]!.GetValue<bool>()));
        Assert.That(!onBudget.WithinBudget, Is.EqualTo(expected["overBudgetOn2026Budget"]!.GetValue<bool>()));
        Assert.That(onListing.IsPartial && onBudget.IsPartial, Is.EqualTo(expected["totalsArePartial"]!.GetValue<bool>()));
        Assert.That(onListing.WithinBudget && !onBudget.WithinBudget, Is.EqualTo(expected["landed"]!.GetValue<bool>()));
    }

    private static MonthlyBreakdown Run(string caseId)
    {
        JsonNode monthlyCase = StoryCases.Case(caseId);

        return MonthlyCost.Calculate(CaseLines.ModeOf(monthlyCase), CaseLines.Lines(monthlyCase), CaseLines.Budget(monthlyCase)).Value;
    }
}
