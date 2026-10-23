using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>Turns the cost lines of a worked case (test-cases/story-calculations.json) into engine inputs.</summary>
internal static class CaseLines
{
    private static readonly Dictionary<string, Mode> _modes = new(StringComparer.Ordinal)
    {
        ["B1"] = Mode.Buy,
        ["B2"] = Mode.Buy,
        ["R1"] = Mode.Rent,
        ["R2"] = Mode.Rent,
    };

    public static Mode ModeOf(JsonNode storyCase) => _modes[storyCase["inputs"]!["home"]!.GetValue<string>()];

    public static CostCategory Category(string id) =>
        Enum.GetValues<CostCategory>().Single(c => CostCategories.ToId(c) == id);

    public static Pence Budget(JsonNode storyCase) => new(storyCase["inputs"]!["budgetPence"]!.GetValue<long>());

    public static List<LineInput> Lines(JsonNode storyCase) =>
        storyCase["inputs"]!["lines"]!.AsArray().Select(line => Line(line!)).ToList();

    private static LineInput Line(JsonNode line)
    {
        CostCategory category = Category(line["category"]!.GetValue<string>());

        if (line["mortgageCase"] is { } mortgageCase)
        {
            (Pence loan, int rateBasisPoints, int termYears) = StoryCases.MortgageInputs(mortgageCase.GetValue<string>());
            Pence repayment = Mortgage.MonthlyRepayment(loan, rateBasisPoints, termYears).Value.MonthlyRepayment;
            return new AmountLine(category, repayment, Period.Month, []);
        }

        if (line["status"] is { } status)
        {
            return status.GetValue<string>() switch
            {
                "included" => new IncludedLine(category, []),
                "not-calculated" => new NotCalculatedLine(category, []),
                "conflicting" => new ConflictingLine(category, []),
                "missing" => new MissingLine(category),
                var other => throw new InvalidOperationException($"Unknown line status {other}."),
            };
        }

        Period period = line["period"]!.GetValue<string>() switch
        {
            "once" => Period.Once,
            "month" => Period.Month,
            "year" => Period.Year,
            var other => throw new InvalidOperationException($"Unknown period {other}."),
        };

        return new AmountLine(category, new Pence(line["amountPence"]!.GetValue<long>()), period, []);
    }
}
