using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace HomeScout.CostEngine.Generator;

/// <summary>
/// Reads the fixture data, asks the cost engine for every figure, and writes <c>packages/fixtures/generated/costs.json</c>.
/// Nothing in the file is typed by hand (AGENTS.md rule 2). The output depends only on the data files, never on the clock.
/// </summary>
internal static class CostsGenerator
{
    internal const string FileName = "costs.json";

    private const string _notYetCovered = "not-yet-covered";

    private static readonly JsonSerializerOptions _options = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
        IndentSize = 2,
        IndentCharacter = ' ',
        NewLine = "\n",
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
    };

    /// <summary>
    /// Generates the file and writes it to <c>generated/</c> under <paramref name="fixturesDirectory"/>, deleting any other
    /// <c>*.json</c> file there. Writes nothing when the engine reports a failure. Returns the exit code: 0 for success, 1 when
    /// the engine or the data's story links report a problem (printed to <paramref name="error"/> with its code).
    /// </summary>
    /// <exception cref="IOException">A data file is missing or cannot be read.</exception>
    /// <exception cref="InvalidDataException">A data file holds something the reader does not understand.</exception>
    internal static int Run(string fixturesDirectory, TextWriter error)
    {
        Result<string> generated = Generate(fixturesDirectory);
        if (generated.IsFailure)
        {
            error.WriteLine($"Generator failed [{generated.Error.Code}]: {generated.Error.Message}");
            return 1;
        }

        string folder = Path.Combine(fixturesDirectory, "generated");
        Directory.CreateDirectory(folder);
        foreach (string other in Directory.GetFiles(folder, "*.json").Where(f => Path.GetFileName(f) != FileName))
        {
            File.Delete(other);
        }

        File.WriteAllBytes(Path.Combine(folder, FileName), new UTF8Encoding(encoderShouldEmitUTF8Identifier: false).GetBytes(generated.Value));
        return 0;
    }

    /// <summary>The text of <c>costs.json</c>: two-space indent, LF line endings and one final newline.</summary>
    internal static Result<string> Generate(string fixturesDirectory)
    {
        FixtureData data = FixtureReader.Read(fixturesDirectory);
        var homes = new List<HomeDocument>();

        foreach (string homeId in data.HomeIds)
        {
            HomeData home = data.Homes.SingleOrDefault(h => h.Id == homeId)
                ?? throw new InvalidDataException($"Home {homeId} is in the snapshot but not in homes.json.");
            StoryData? story = data.Stories.FirstOrDefault(s => s.HomeIds.Contains(homeId));

            if (home.Nation != Nation.England)
            {
                homes.Add(new HomeDocument(home.Id, ModeName(home.Mode), NationName(home.Nation), _notYetCovered, story?.Id, []));
                continue;
            }

            if (story is null)
            {
                return Failure(homeId, new Error("home.not-in-a-story", "The home is in England but in no story, so it has no steps to work out.", ErrorCategory.Validation));
            }

            var facts = new HomeFacts(
                home.Id,
                home.Mode,
                home.Nation,
                data.Evidence
                    .Where(e => (e.SubjectType == "household" && e.SubjectId == data.HouseholdId) || (e.SubjectType == "home" && e.SubjectId == homeId))
                    .Select(e => e.Item)
                    .ToList(),
                data.MonthlyBudget);

            Result<HomeCosts> costs = HomeCostBuilder.Build(facts, story.Steps);
            if (costs.IsFailure)
            {
                return Failure(homeId, costs.Error);
            }

            homes.Add(MapHome(costs.Value, story.Id, $"household:{data.HouseholdId}.monthlyBudget"));
        }

        var document = new CostsDocument(
            "../schema/generated-costs.schema.json",
            1,
            "HomeScout.CostEngine.Generator",
            data.SnapshotDate,
            "integer pence",
            "Each yearly amount is divided by 12 and rounded once to the nearest penny, halves away from zero; a total is the sum of its rounded lines; a mortgage repayment is rounded once from the exact fraction (decision 0021).",
            homes);

        return Result.Success(JsonSerializer.Serialize(document, _options) + "\n");
    }

    private static Result<string> Failure(string homeId, Error error) =>
        Result.Failure<string>(new Error(error.Code, $"{homeId}: {error.Message}", error.Category));

    private static HomeDocument MapHome(HomeCosts home, string storyId, string budgetSource) =>
        new(
            home.HomeId,
            ModeName(home.Mode),
            NationName(home.Nation),
            "covered",
            storyId,
            home.Scenarios.Select(s => MapScenario(home.HomeId, s, budgetSource)).ToList());

    private static ScenarioDocument MapScenario(string homeId, ScenarioCosts scenario, string budgetSource)
    {
        string id = scenario.ScenarioId;
        MonthlyBreakdown monthly = scenario.Monthly;

        return new ScenarioDocument(
            id,
            scenario.FromStep,
            scenario.ToStep,
            scenario.Mortgage is { } mortgage ? MapMortgage(homeId, id, mortgage) : null,
            new MonthlyDocument(
                MapLines(homeId, id, "monthly", monthly.Lines),
                MapTotal(homeId, id, "monthly", monthly.Total, monthly.IsPartial, monthly.PartialReasons),
                new BudgetDocument(
                    FigureIds.Budget(homeId, id),
                    monthly.Budget.Value,
                    budgetSource,
                    monthly.BudgetDifference.Value,
                    monthly.WithinBudget,
                    monthly.BasedOnPartialTotal)),
            new UpfrontDocument(
                MapLines(homeId, id, "upfront", scenario.Upfront.Lines),
                MapTotal(homeId, id, "upfront", scenario.Upfront.Total, scenario.Upfront.IsPartial, scenario.Upfront.PartialReasons)),
            scenario.Changes.Select(c => MapChange(homeId, id, c)).ToList(),
            scenario.MonthlyTotalChange is { } change ? new FigureDocument(FigureIds.MonthlyTotalChange(homeId, id), change.Value) : null);
    }

    private static MortgageDocument MapMortgage(string homeId, string scenarioId, MortgageSummary mortgage) =>
        new(
            FigureIds.Mortgage(homeId, scenarioId),
            new FigureDocument(FigureIds.MortgageLoan(homeId, scenarioId), mortgage.Repayment.Loan.Value),
            mortgage.Repayment.RateBasisPoints,
            mortgage.Repayment.TermYears,
            mortgage.Repayment.Payments,
            new FigureDocument(FigureIds.MonthlyRepayment(homeId, scenarioId), mortgage.Repayment.MonthlyRepayment.Value),
            mortgage.EvidenceIds);

    private static List<LineDocument> MapLines(string homeId, string scenarioId, string section, IReadOnlyList<LineResult> lines) =>
        lines.Select(l => new LineDocument(
            FigureIds.Line(homeId, scenarioId, section, l.Category),
            CostCategories.ToId(l.Category),
            CostCategories.StatusId(l.Status),
            l.Amount?.Value,
            l.SourcePeriod is { } period ? PeriodName(period) : null,
            l.EvidenceIds)).ToList();

    private static TotalDocument MapTotal(string homeId, string scenarioId, string section, Pence total, bool isPartial, IReadOnlyList<PartialReason> reasons) =>
        new(
            FigureIds.Total(homeId, scenarioId, section),
            total.Value,
            isPartial,
            reasons.Select(r => new PartialReasonDocument(
                FigureIds.Line(homeId, scenarioId, section, r.Category),
                CostCategories.ToId(r.Category),
                CostCategories.StatusId(r.Status))).ToList());

    private static ChangeDocument MapChange(string homeId, string scenarioId, CostChange change) =>
        new(
            FigureIds.Change(homeId, scenarioId, change.Category),
            CostCategories.ToId(change.Category),
            change.Kind switch
            {
                ChangeKind.ValueChanged => "value-changed",
                ChangeKind.NowCalculated => "now-calculated",
                ChangeKind.NoLongerCalculated => "no-longer-calculated",
                _ => throw new ArgumentOutOfRangeException(nameof(change), change.Kind, "Unknown kind of change."),
            },
            change.PreviousEvidenceIds,
            change.CurrentEvidenceIds,
            change.MonthlyDifference?.Value,
            change.AnnualDifference?.Value);

    private static string? ModeName(Mode? mode) => mode switch
    {
        null => null,
        Mode.Buy => "buy",
        Mode.Rent => "rent",
        _ => throw new ArgumentOutOfRangeException(nameof(mode), mode, "Unknown mode."),
    };

    private static string NationName(Nation nation) => nation switch
    {
        Nation.England => "England",
        Nation.Wales => "Wales",
        Nation.Scotland => "Scotland",
        Nation.NorthernIreland => "Northern Ireland",
        _ => throw new ArgumentOutOfRangeException(nameof(nation), nation, "Unknown nation."),
    };

    private static string PeriodName(Period period) => period switch
    {
        Period.Once => "once",
        Period.Month => "month",
        Period.Year => "year",
        _ => throw new ArgumentOutOfRangeException(nameof(period), period, "Unknown period."),
    };
}
