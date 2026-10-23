using System.Text.Json.Nodes;
using System.Text.RegularExpressions;

namespace HomeScout.CostEngine.Generator.Tests;

/// <summary>What the generated file looks like: its homes and scenarios, its key order, its figure ids, and that it is the same every time.</summary>
[TestFixture]
internal sealed partial class OutputShapeTests
{
    [GeneratedRegex(@"^[A-Z0-9]+(-[A-Z0-9]+)*(\.[a-z0-9]+(-[a-z0-9]+)*)+$")]
    private static partial Regex FigureIdPattern();

    private static JsonNode Snapshot() =>
        JsonNode.Parse(File.ReadAllText(Path.Combine(GeneratedFixture.FixturesDirectory, "data", "snapshot.json")))!["snapshot"]!;

    [Test]
    public void Generate_realData_listsTheHomesInTheOrderOfTheSnapshot()
    {
        IEnumerable<string> expected = Snapshot()["homeIds"]!.AsArray().Select(i => i!.GetValue<string>());

        IEnumerable<string> actual = GeneratedFixture.Output["homes"]!.AsArray().Select(h => h!["homeId"]!.GetValue<string>());

        Assert.That(actual, Is.EqualTo(expected));
    }

    [TestCase("B1", new[] { "from-step-1", "from-step-4" })]
    [TestCase("B2", new[] { "from-step-1" })]
    [TestCase("R1", new[] { "from-step-1", "from-step-4" })]
    [TestCase("R2", new[] { "from-step-1" })]
    [TestCase("WALES-1", new string[0])]
    public void Generate_realData_derivesTheExpectedScenarios(string homeId, string[] scenarioIds)
    {
        JsonNode home = GeneratedFixture.Output["homes"]!.AsArray().Single(h => h!["homeId"]!.GetValue<string>() == homeId)!;

        Assert.That(home["scenarios"]!.AsArray().Select(s => s!["scenarioId"]!.GetValue<string>()), Is.EqualTo(scenarioIds));
    }

    [Test]
    public void Generate_buyerStory_mergesStepsOneToThreeAndStartsAgainAtStepFour()
    {
        JsonNode first = GeneratedFixture.Scenario("B1", "from-step-1");
        JsonNode second = GeneratedFixture.Scenario("B1", "from-step-4");

        Assert.That((first["fromStep"]!.GetValue<int>(), first["toStep"]!.GetValue<int>()), Is.EqualTo((1, 3)));
        Assert.That((second["fromStep"]!.GetValue<int>(), second["toStep"]!.GetValue<int>()), Is.EqualTo((4, 4)));
    }

    [Test]
    public void Generate_walesHome_isNotYetCoveredWithNoScenariosAndNoMode()
    {
        JsonNode wales = GeneratedFixture.Output["homes"]!.AsArray().Single(h => h!["homeId"]!.GetValue<string>() == "WALES-1")!;

        Assert.That(wales["coverage"]!.GetValue<string>(), Is.EqualTo("not-yet-covered"));
        Assert.That(wales["nation"]!.GetValue<string>(), Is.EqualTo("Wales"));
        Assert.That(wales["scenarios"]!.AsArray(), Is.Empty);
        Assert.That(wales["mode"], Is.Null);
        Assert.That(wales["storyId"], Is.Null);
    }

    [Test]
    public void Generate_englishHomes_carryModeNationCoverageAndStory()
    {
        JsonNode r1 = GeneratedFixture.Output["homes"]!.AsArray().Single(h => h!["homeId"]!.GetValue<string>() == "R1")!;

        Assert.That((r1["mode"]!.GetValue<string>(), r1["nation"]!.GetValue<string>(), r1["coverage"]!.GetValue<string>(), r1["storyId"]!.GetValue<string>()),
            Is.EqualTo(("rent", "England", "covered", "RENTER")));
    }

    [Test]
    public void Generate_header_copiesTheSnapshotDateAndNamesTheContract()
    {
        JsonNode output = GeneratedFixture.Output;

        Assert.That(output["snapshotDate"]!.GetValue<string>(), Is.EqualTo(Snapshot()["snapshotDate"]!.GetValue<string>()));
        Assert.That(output["$schema"]!.GetValue<string>(), Is.EqualTo("../schema/generated-costs.schema.json"));
        Assert.That(output["formatVersion"]!.GetValue<int>(), Is.EqualTo(1));
        Assert.That(output["money"]!.GetValue<string>(), Is.EqualTo("integer pence"));
        Assert.That(output["rounding"]!.GetValue<string>(), Does.Contain("0021"));
        Assert.That(output["generatedBy"]!.GetValue<string>(), Is.Not.Empty);
    }

    [Test]
    public void Generate_everyFigureId_isUniqueAndMatchesThePattern()
    {
        var ids = new List<string>();
        CollectIds(GeneratedFixture.Output, ids);

        Assert.That(ids, Is.Not.Empty);
        Assert.That(ids, Is.Unique);
        Assert.That(ids.Where(i => !FigureIdPattern().IsMatch(i)), Is.Empty);
    }

    [Test]
    public void Generate_everyPartialReason_pointsAtALineInTheSameScenario()
    {
        foreach (JsonNode? home in GeneratedFixture.Output["homes"]!.AsArray())
        {
            foreach (JsonNode? scenario in home!["scenarios"]!.AsArray())
            {
                foreach (string section in new[] { "monthly", "upfront" })
                {
                    JsonNode block = scenario![section]!;
                    var lineIds = block["lines"]!.AsArray().Select(l => l!["id"]!.GetValue<string>()).ToList();

                    Assert.That(block["total"]!["partialReasons"]!.AsArray().Select(r => r!["lineId"]!.GetValue<string>()), Is.SubsetOf(lineIds));
                }
            }
        }
    }

    [Test]
    public void Generate_everyKey_followsTheOrderOfTheContractSchema()
    {
        JsonNode schema = JsonNode.Parse(File.ReadAllText(Path.Combine(GeneratedFixture.FixturesDirectory, "schema", "generated-costs.schema.json")))!;
        var problems = new List<string>();

        CheckKeyOrder(GeneratedFixture.Output, schema["properties"]!.AsObject(), schema["$defs"]!.AsObject(), "root", problems);

        Assert.That(problems, Is.Empty);
    }

    [Test]
    public void Generate_runTwice_givesIdenticalText()
    {
        Result<string> again = CostsGenerator.Generate(GeneratedFixture.FixturesDirectory);

        Assert.That(again.Value, Is.EqualTo(GeneratedFixture.Json));
    }

    [Test]
    public void Generate_text_usesLfLineEndingsTwoSpaceIndentAndOneFinalNewline()
    {
        string json = GeneratedFixture.Json;

        Assert.That(json, Does.Not.Contain('\r'));
        Assert.That(json, Does.Not.Contain('\t'));
        Assert.That(json, Does.EndWith("}\n"));
        Assert.That(json.Split('\n').Where(l => l.Length > 0).Select(l => l.Length - l.TrimStart(' ').Length), Is.All.Matches<int>(n => n % 2 == 0));
        Assert.That(json, Does.StartWith("{\n  \"$schema\""));
    }

    [Test]
    public void Generate_noMoneyAnywhere_isAFloatingPointNumber()
    {
        Assert.That(Regex.IsMatch(GeneratedFixture.Json, @"\d\.\d"), Is.False);
    }

    private static void CollectIds(JsonNode? node, List<string> ids)
    {
        switch (node)
        {
            case JsonObject obj:
                foreach ((string key, JsonNode? value) in obj)
                {
                    if (key == "id" && value is JsonValue id)
                    {
                        ids.Add(id.GetValue<string>());
                    }
                    else
                    {
                        CollectIds(value, ids);
                    }
                }

                break;
            case JsonArray array:
                foreach (JsonNode? item in array)
                {
                    CollectIds(item, ids);
                }

                break;
        }
    }

    /// <summary>Checks that the keys of every object appear in the order the schema lists its properties, following each $ref down.</summary>
    private static void CheckKeyOrder(JsonNode? node, JsonObject schemaProperties, JsonObject definitions, string path, List<string> problems)
    {
        if (node is JsonArray array)
        {
            foreach (JsonNode? item in array)
            {
                CheckKeyOrder(item, schemaProperties, definitions, path + "[]", problems);
            }

            return;
        }

        if (node is not JsonObject obj)
        {
            return;
        }

        List<string> schemaOrder = schemaProperties.Select(p => p.Key).ToList();
        List<int> positions = obj.Select(p => schemaOrder.IndexOf(p.Key)).ToList();
        if (positions.Contains(-1) || !positions.SequenceEqual(positions.Order()))
        {
            problems.Add($"{path}: keys {string.Join(",", obj.Select(p => p.Key))} do not follow {string.Join(",", schemaOrder)}");
        }

        foreach ((string key, JsonNode? value) in obj)
        {
            JsonNode? property = schemaProperties[key];
            string? reference = (property?["$ref"] ?? property?["items"]?["$ref"])?.GetValue<string>();
            if (reference is not null && reference.StartsWith("#/$defs/", StringComparison.Ordinal))
            {
                JsonNode? child = definitions[reference["#/$defs/".Length..]];
                if (child?["properties"] is JsonObject childProperties)
                {
                    CheckKeyOrder(value, childProperties, definitions, $"{path}.{key}", problems);
                }
            }
        }
    }
}
