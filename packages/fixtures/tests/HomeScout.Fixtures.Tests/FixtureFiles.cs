using System.Text.Json.Nodes;
using HomeScout.Fixtures.Validator;

namespace HomeScout.Fixtures.Tests;

/// <summary>Finds and reads the fixture files in the repository, so each test starts from the real data.</summary>
internal static class FixtureFiles
{
    private static readonly string _repositoryRoot = FixtureValidator.FindRepositoryRoot(AppContext.BaseDirectory);

    public static string FixturesDirectory { get; } = Path.Combine(_repositoryRoot, "packages", "fixtures");

    public static string SchemaDirectory { get; } = Path.Combine(FixturesDirectory, "schema");

    public static JsonNode Load(string name)
    {
        string path = Path.Combine(FixturesDirectory, "data", name + ".json");
        return JsonNode.Parse(File.ReadAllText(path)) ?? throw new InvalidOperationException($"{path} is empty.");
    }

    public static JsonObject EvidenceItem(string id)
    {
        JsonArray items = Load("evidence")["evidence"]!.AsArray();
        JsonNode item = items.Single(i => i!["id"]!.GetValue<string>() == id)!;
        return item.DeepClone().AsObject();
    }

    public static JsonObject Home(string id)
    {
        JsonArray homes = Load("homes")["homes"]!.AsArray();
        JsonNode home = homes.Single(h => h!["id"]!.GetValue<string>() == id)!;
        return home.DeepClone().AsObject();
    }

    public static JsonObject Question(string id)
    {
        JsonArray questions = Load("questions")["questions"]!.AsArray();
        JsonNode question = questions.Single(q => q!["id"]!.GetValue<string>() == id)!;
        return question.DeepClone().AsObject();
    }

    /// <summary>Wraps one record in its file shape and validates it against that file's schema.</summary>
    public static IReadOnlyList<FixtureProblem> Validate(string schemaName, string collectionKey, JsonObject record)
    {
        var file = new JsonObject { [collectionKey] = new JsonArray(record.DeepClone()) };
        return FixtureValidator.ValidateInstance(file, schemaName + ".schema.json", SchemaDirectory);
    }
}
