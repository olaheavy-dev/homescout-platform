using System.Globalization;
using System.Text.Json;
using System.Text.Json.Nodes;
using Json.Schema;

namespace HomeScout.Fixtures.Validator;

/// <summary>One thing wrong with one fixture file.</summary>
internal sealed record FixtureProblem(string File, string Location, string Message)
{
    public override string ToString() => $"{File}: {Location}: {Message}";
}

/// <summary>
/// Checks fixture files against their JSON Schema 2020-12 schemas (decision 0018, register line BE-07).
/// Convention: <c>data/NAME.json</c> is checked against <c>schema/NAME.schema.json</c>.
/// Any file in <c>test-cases/</c> or <c>generated/</c> names its schema in a top-level <c>$schema</c> field
/// (a path relative to the file, such as <c>../schema/test-case.schema.json</c>).
/// </summary>
internal static class FixtureValidator
{
    private const string _schemaSuffix = ".schema.json";

    /// <summary>Walks up from <paramref name="startDirectory"/> until it finds the solution file.</summary>
    internal static string FindRepositoryRoot(string startDirectory)
    {
        DirectoryInfo? directory = new(startDirectory);
        while (directory is not null)
        {
            if (File.Exists(Path.Combine(directory.FullName, "HomeScout.slnx")))
            {
                return directory.FullName;
            }

            directory = directory.Parent;
        }

        throw new DirectoryNotFoundException($"HomeScout.slnx not found above {startDirectory}.");
    }

    /// <summary>Validates every data file and test case under a <c>packages/fixtures</c> directory.</summary>
    internal static IReadOnlyList<FixtureProblem> ValidateFixtures(string fixturesDirectory)
    {
        var problems = new List<FixtureProblem>();
        string schemaDirectory = Path.Combine(fixturesDirectory, "schema");
        int checkedFiles = 0;

        foreach (string path in JsonFiles(Path.Combine(fixturesDirectory, "data")))
        {
            checkedFiles++;
            string expected = Path.GetFileNameWithoutExtension(path) + _schemaSuffix;
            problems.AddRange(ValidateFile(path, expected, schemaDirectory, requireDeclaredSchema: false));
        }

        foreach (string path in JsonFiles(Path.Combine(fixturesDirectory, "test-cases")))
        {
            checkedFiles++;
            problems.AddRange(ValidateFile(path, null, schemaDirectory, requireDeclaredSchema: true));
        }

        // The generator's output (task 4b). The folder may be empty or absent until the generator exists.
        foreach (string path in JsonFiles(Path.Combine(fixturesDirectory, "generated")))
        {
            checkedFiles++;
            problems.AddRange(ValidateFile(path, null, schemaDirectory, requireDeclaredSchema: true));
        }

        if (checkedFiles == 0)
        {
            problems.Add(new FixtureProblem(fixturesDirectory, "/", "No fixture files found in data/, test-cases/ or generated/."));
        }

        return problems;
    }

    /// <summary>Validates one parsed JSON value against a schema file in <paramref name="schemaDirectory"/>.</summary>
    internal static IReadOnlyList<FixtureProblem> ValidateInstance(JsonNode? instance, string schemaFileName, string schemaDirectory)
    {
        if (!Directory.Exists(schemaDirectory))
        {
            return [new FixtureProblem(schemaFileName, "/", $"Schema folder not found: {schemaDirectory}.")];
        }

        // Each call uses its own registry. Every schema is loaded first so that
        // "$ref": "common.schema.json#/..." resolves against the $id of the shared definitions.
        BuildOptions build = new() { SchemaRegistry = new SchemaRegistry() };
        JsonSchema? target = null;
        foreach (string schemaPath in Directory.EnumerateFiles(schemaDirectory, "*" + _schemaSuffix))
        {
            JsonSchema schema = JsonSchema.FromText(File.ReadAllText(schemaPath), build);
            if (string.Equals(Path.GetFileName(schemaPath), schemaFileName, StringComparison.Ordinal))
            {
                target = schema;
            }
        }

        if (target is null)
        {
            return [new FixtureProblem(schemaFileName, "/", $"Schema file not found in {schemaDirectory}.")];
        }

        EvaluationOptions options = new() { OutputFormat = OutputFormat.List };
        EvaluationResults results = target.Evaluate(JsonSerializer.SerializeToElement(instance), options);
        var problems = new List<FixtureProblem>();
        if (!results.IsValid)
        {
            // Errors inside an "if" are the test of a condition, not a real failure, so they are left out.
            foreach (EvaluationResults detail in (results.Details ?? []).Where(d => !IsInsideIfCondition(d.EvaluationPath.ToString())))
            {
                foreach (KeyValuePair<string, string> error in detail.Errors ?? new Dictionary<string, string>())
                {
                    var problem = new FixtureProblem(schemaFileName, detail.InstanceLocation.ToString(), $"{error.Key}: {error.Value}");
                    if (!problems.Contains(problem))
                    {
                        problems.Add(problem);
                    }
                }
            }

            if (problems.Count == 0)
            {
                problems.Add(new FixtureProblem(schemaFileName, "/", "The value does not match the schema."));
            }
        }

        return problems;
    }

    private static bool IsInsideIfCondition(string evaluationPath) =>
        evaluationPath.Split('/').Any(segment => segment == "if");

    private static IEnumerable<string> JsonFiles(string directory) =>
        Directory.Exists(directory)
            ? Directory.EnumerateFiles(directory, "*.json").Order(StringComparer.Ordinal)
            : [];

    private static List<FixtureProblem> ValidateFile(string path, string? expectedSchema, string schemaDirectory, bool requireDeclaredSchema)
    {
        string name = Path.GetFileName(path);
        JsonNode? instance;
        try
        {
            instance = JsonNode.Parse(File.ReadAllText(path));
        }
        catch (JsonException exception)
        {
            return [new FixtureProblem(name, "/", "Not valid JSON: " + exception.Message)];
        }

        JsonNode? declaredNode = (instance as JsonObject)?["$schema"];
        string? declared = null;
        if (declaredNode is not null && !(declaredNode is JsonValue value && value.TryGetValue(out declared)))
        {
            return [new FixtureProblem(name, "/$schema", "Must be a string naming the schema, for example \"../schema/NAME.schema.json\".")];
        }

        string? declaredName = declared is null ? null : Path.GetFileName(declared);
        string? schemaName = expectedSchema ?? declaredName;

        if (schemaName is null)
        {
            return [new FixtureProblem(name, "/$schema", "Missing: name the schema this file follows, for example \"../schema/NAME.schema.json\".")];
        }

        if (declaredName is null && requireDeclaredSchema)
        {
            return [new FixtureProblem(name, "/$schema", "Missing.")];
        }

        if (declaredName is not null && expectedSchema is not null && !string.Equals(declaredName, expectedSchema, StringComparison.Ordinal))
        {
            return [new FixtureProblem(name, "/$schema", string.Create(CultureInfo.InvariantCulture, $"Names {declaredName} but the file name requires {expectedSchema}."))];
        }

        return ValidateInstance(instance, schemaName, schemaDirectory)
            .Select(p => p with { File = name })
            .ToList();
    }
}
