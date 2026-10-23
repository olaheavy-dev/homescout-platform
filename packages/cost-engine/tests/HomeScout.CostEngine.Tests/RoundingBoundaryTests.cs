using System.Globalization;
using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Runs every case in test-cases/rounding-boundaries.json (worked independently of the engine, decision 0034).
/// The cases are read from the file, never copied here.
/// </summary>
[TestFixture]
internal sealed class RoundingBoundaryTests
{
    private static JsonArray Cases() =>
        JsonNode.Parse(File.ReadAllText(RepositoryFiles.TestCases("rounding-boundaries.json")))!["cases"]!.AsArray();

    private static IEnumerable<TestCaseData> CasesWith(string inputKey, string expectedKey) =>
        Cases()
            .Where(c => c!["inputs"]![inputKey] is not null)
            .Select(c => new TestCaseData(
                c!["inputs"]![inputKey]!.ToString(),
                c["expected"]![expectedKey]!.GetValue<long>()).SetArgDisplayNames(c["id"]!.GetValue<string>()));

    private static IEnumerable<TestCaseData> DirectRoundingCases() => CasesWith("unroundedPence", "pence");

    private static IEnumerable<TestCaseData> AnnualToMonthlyCases() => CasesWith("annualPence", "monthlyPence");

    [Test]
    public void BoundaryFile_loaded_hasAllSixDirectRoundingCases() =>
        Assert.That(DirectRoundingCases().Count(), Is.EqualTo(6));

    [Test]
    public void BoundaryFile_loaded_hasTheAnnualToMonthlyCases() =>
        Assert.That(AnnualToMonthlyCases().Count(), Is.EqualTo(14));

    [TestCaseSource(nameof(DirectRoundingCases))]
    public void Round_boundaryCaseFromFile_matchesWorkedResult(string unroundedPence, long expectedPence)
    {
        decimal exact = decimal.Parse(unroundedPence, CultureInfo.InvariantCulture);

        Assert.That(Pence.Round(exact), Is.EqualTo(new Pence(expectedPence)));
    }

    [TestCaseSource(nameof(AnnualToMonthlyCases))]
    public void AnnualToMonthly_boundaryCaseFromFile_matchesWorkedResult(string annualPence, long expectedPence)
    {
        var annual = new Pence(long.Parse(annualPence, CultureInfo.InvariantCulture));

        Assert.That(annual.AnnualToMonthly(), Is.EqualTo(new Pence(expectedPence)));
    }
}
