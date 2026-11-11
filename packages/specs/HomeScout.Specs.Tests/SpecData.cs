using System.Text.Json;

namespace HomeScout.Specs.Tests;

/// <summary>
/// The data the specifications check against: every figure ID in <c>packages/fixtures/generated/costs.json</c> and every
/// evidence ID in <c>packages/fixtures/data/evidence.json</c>. Read once, never changed (AGENTS.md rule 2: figures are cited
/// by ID, not typed into the specifications).
/// </summary>
internal static class SpecData
{
    private static readonly Lazy<Loaded> _loaded = new(Load);

    public static IReadOnlySet<string> EvidenceIds => _loaded.Value.Evidence;

    public static IReadOnlySet<string> HomeIds => _loaded.Value.Homes;

    public static IReadOnlyCollection<string> FigureIds => _loaded.Value.Figures.Keys;

    /// <summary>Looks a figure up by its ID (an object with an <c>id</c> property anywhere in costs.json).</summary>
    public static bool TryGetFigure(string id, out JsonElement figure) => _loaded.Value.Figures.TryGetValue(id, out figure);

    /// <summary>True if the home has a calculated scenario for the story step (<c>fromStep</c> up to <c>toStep</c>).</summary>
    public static bool HasScenarioFromStep(string homeId, int step) => TryFindScenario(homeId, step, out _);

    /// <summary>Finds the calculated scenario that covers a story step, for example B1 step 2 is "from-step-1".</summary>
    public static bool TryFindScenario(string homeId, int step, out string scenarioId)
    {
        foreach (var range in _loaded.Value.Scenarios)
        {
            if (range.HomeId == homeId && range.FromStep <= step && step <= range.ToStep)
            {
                scenarioId = range.ScenarioId;
                return true;
            }
        }

        scenarioId = string.Empty;
        return false;
    }

    private static Loaded Load()
    {
        var root = FindRepositoryRoot();

        using var costs = JsonDocument.Parse(File.ReadAllText(Path.Combine(root, "packages", "fixtures", "generated", "costs.json")));
        var figures = new Dictionary<string, JsonElement>(StringComparer.Ordinal);
        var scenarios = new List<ScenarioRange>();
        CollectFigures(costs.RootElement.Clone(), figures);
        foreach (var home in costs.RootElement.GetProperty("homes").EnumerateArray())
        {
            var homeId = home.GetProperty("homeId").GetString()!;
            foreach (var scenario in home.GetProperty("scenarios").EnumerateArray())
            {
                scenarios.Add(new ScenarioRange(
                    homeId,
                    scenario.GetProperty("scenarioId").GetString()!,
                    scenario.GetProperty("fromStep").GetInt32(),
                    scenario.GetProperty("toStep").GetInt32()));
            }
        }

        using var evidence = JsonDocument.Parse(File.ReadAllText(Path.Combine(root, "packages", "fixtures", "data", "evidence.json")));
        var evidenceIds = evidence.RootElement.GetProperty("evidence").EnumerateArray()
            .Select(item => item.GetProperty("id").GetString()!)
            .ToHashSet(StringComparer.Ordinal);

        using var homes = JsonDocument.Parse(File.ReadAllText(Path.Combine(root, "packages", "fixtures", "data", "homes.json")));
        var homeIds = homes.RootElement.GetProperty("homes").EnumerateArray()
            .Select(item => item.GetProperty("id").GetString()!)
            .ToHashSet(StringComparer.Ordinal);

        return new Loaded(figures, scenarios, evidenceIds, homeIds);
    }

    private static void CollectFigures(JsonElement element, Dictionary<string, JsonElement> figures)
    {
        if (element.ValueKind == JsonValueKind.Object)
        {
            if (element.TryGetProperty("id", out var id) && id.ValueKind == JsonValueKind.String)
            {
                figures[id.GetString()!] = element;
            }

            foreach (var property in element.EnumerateObject())
            {
                CollectFigures(property.Value, figures);
            }
        }
        else if (element.ValueKind == JsonValueKind.Array)
        {
            foreach (var item in element.EnumerateArray())
            {
                CollectFigures(item, figures);
            }
        }
    }

    private static string FindRepositoryRoot()
    {
        for (var directory = new DirectoryInfo(AppContext.BaseDirectory); directory is not null; directory = directory.Parent)
        {
            if (File.Exists(Path.Combine(directory.FullName, "HomeScout.slnx")))
            {
                return directory.FullName;
            }
        }

        throw new InvalidOperationException("HomeScout.slnx was not found above " + AppContext.BaseDirectory + ".");
    }

    private sealed record ScenarioRange(string HomeId, string ScenarioId, int FromStep, int ToStep);

    private sealed record Loaded(
        Dictionary<string, JsonElement> Figures,
        List<ScenarioRange> Scenarios,
        HashSet<string> Evidence,
        HashSet<string> Homes);
}
