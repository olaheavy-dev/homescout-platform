using System.Globalization;
using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Reads the independently worked cases in test-cases/story-calculations.json. Tests take their inputs and expected
/// values from here and never from a copy, so a wrong calculation cannot confirm itself (AGENTS.md rule 2).
/// </summary>
internal static class StoryCases
{
    private static readonly Lazy<JsonArray> _cases = new(() =>
        JsonNode.Parse(File.ReadAllText(RepositoryFiles.TestCases("story-calculations.json")))!["cases"]!.AsArray());

    public static IEnumerable<string> AllIds => _cases.Value.Select(c => c!["id"]!.GetValue<string>());

    public static JsonNode Case(string id) =>
        _cases.Value.Single(c => c!["id"]!.GetValue<string>() == id)!;

    public static IEnumerable<string> IdsWhere(Func<JsonNode, bool> predicate) =>
        _cases.Value.Where(c => predicate(c!)).Select(c => c!["id"]!.GetValue<string>());

    /// <summary>The ids of cases whose inputs have this key.</summary>
    public static IEnumerable<string> IdsWithInput(string key) =>
        IdsWhere(c => c["inputs"]![key] is not null);

    /// <summary>
    /// Reads a rate such as "0.055" as whole basis points (550). The text must convert exactly: a rate that is not a
    /// whole number of basis points fails the test instead of being rounded (register line: whole basis points only).
    /// </summary>
    public static int BasisPoints(string annualRate)
    {
        decimal basisPoints = decimal.Parse(annualRate, CultureInfo.InvariantCulture) * 10_000m;
        Assert.That(basisPoints, Is.EqualTo(decimal.Truncate(basisPoints)), "The rate is not a whole number of basis points.");

        return decimal.ToInt32(basisPoints);
    }

    /// <summary>
    /// The mortgage inputs of a case: the loan (given directly, or the asking price minus the deposit, as the founder decided
    /// on 23 Oct 2026), the rate in basis points, and the term.
    /// </summary>
    public static (Pence Loan, int RateBasisPoints, int TermYears) MortgageInputs(string id)
    {
        JsonNode inputs = Case(id)["inputs"]!;
        long loan = inputs["loanPence"] is { } direct
            ? direct.GetValue<long>()
            : inputs["askingPricePence"]!.GetValue<long>() - inputs["depositPence"]!.GetValue<long>();

        return (new Pence(loan), BasisPoints(inputs["annualRate"]!.GetValue<string>()), inputs["termYears"]!.GetValue<int>());
    }
}
