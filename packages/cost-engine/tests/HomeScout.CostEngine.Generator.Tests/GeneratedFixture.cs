using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Generator.Tests;

/// <summary>
/// Finds the repository's real fixtures and the independently worked cases, and runs the generator on them once.
/// Tests take their inputs and expected values from the files and never from a copy (AGENTS.md rule 2).
/// </summary>
internal static class GeneratedFixture
{
    private static readonly Lazy<string> _root = new(() => FindRoot(AppContext.BaseDirectory));

    private static readonly Lazy<string> _json = new(() =>
    {
        Result<string> result = CostsGenerator.Generate(FixturesDirectory);
        Assert.That(result.IsSuccess, Is.True, result.IsFailure ? result.Error.Code : string.Empty);
        return result.Value;
    });

    private static readonly Lazy<JsonNode> _cases = new(() =>
        JsonNode.Parse(File.ReadAllText(Path.Combine(FixturesDirectory, "test-cases", "story-calculations.json")))!["cases"]!);

    public static string FixturesDirectory => Path.Combine(_root.Value, "packages", "fixtures");

    /// <summary>The text the generator produces from the real data.</summary>
    public static string Json => _json.Value;

    public static JsonNode Output => JsonNode.Parse(Json)!;

    public static JsonNode Case(string id) =>
        _cases.Value.AsArray().Single(c => c!["id"]!.GetValue<string>() == id)!;

    public static JsonNode Scenario(string homeId, string scenarioId) =>
        Output["homes"]!.AsArray().Single(h => h!["homeId"]!.GetValue<string>() == homeId)!["scenarios"]!.AsArray()
            .Single(s => s!["scenarioId"]!.GetValue<string>() == scenarioId)!;

    /// <summary>Copies the real data files to a new temporary fixtures folder, so a test can change them.</summary>
    public static string CopyDataToTemporaryFixtures()
    {
        string fixtures = Path.Combine(Path.GetTempPath(), "homescout-generator-tests-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(Path.Combine(fixtures, "data"));
        foreach (string file in Directory.GetFiles(Path.Combine(FixturesDirectory, "data"), "*.json"))
        {
            File.Copy(file, Path.Combine(fixtures, "data", Path.GetFileName(file)));
        }

        return fixtures;
    }

    private static string FindRoot(string start)
    {
        DirectoryInfo? directory = new(start);
        while (directory is not null)
        {
            if (File.Exists(Path.Combine(directory.FullName, "HomeScout.slnx")))
            {
                return directory.FullName;
            }

            directory = directory.Parent;
        }

        throw new InvalidOperationException($"HomeScout.slnx not found above {start}.");
    }
}
