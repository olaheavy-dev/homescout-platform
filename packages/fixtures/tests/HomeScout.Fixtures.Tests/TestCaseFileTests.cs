using System.Text.Json.Nodes;
using HomeScout.Fixtures.Validator;

namespace HomeScout.Fixtures.Tests;

/// <summary>Checks the independently worked test cases (task 3) against their schema and each other.</summary>
[TestFixture]
internal sealed class TestCaseFileTests
{
    private static readonly string[] _files = ["rounding-boundaries", "story-calculations"];

    private static JsonNode Load(string name) =>
        JsonNode.Parse(File.ReadAllText(Path.Combine(FixtureFiles.FixturesDirectory, "test-cases", name + ".json")))!;

    private static IEnumerable<JsonNode> AllCases() =>
        _files.SelectMany(f => Load(f)["cases"]!.AsArray()).Select(c => c!);

    private static IReadOnlyList<FixtureProblem> Validate(JsonNode file) =>
        FixtureValidator.ValidateInstance(file, "test-case.schema.json", FixtureFiles.SchemaDirectory);

    [TestCaseSource(nameof(_files))]
    public void TestCaseFile_realFile_namesItsSchemaAndIsAccepted(string name)
    {
        JsonNode file = Load(name);

        Assert.That(file["$schema"]!.GetValue<string>(), Is.EqualTo("../schema/test-case.schema.json"));
        Assert.That(Validate(file), Is.Empty);
    }

    [Test]
    public void TestCaseFile_moneyFieldWithDecimals_isRejected()
    {
        JsonNode file = Load("story-calculations");
        file["cases"]![0]!["expected"]!["annualDifferencePence"] = JsonNode.Parse("1320.5");

        Assert.That(Validate(file).Select(p => p.ToString()), Has.Some.Contain("annualDifferencePence"));
    }

    [Test]
    public void TestCaseFile_caseWithNoRule_isRejected()
    {
        JsonNode file = Load("rounding-boundaries");
        file["cases"]![0]!.AsObject().Remove("rule");

        Assert.That(Validate(file).Select(p => p.ToString()), Has.Some.Contain("rule"));
    }

    [Test]
    public void TestCaseFile_costLineAsZeroAmount_isRejected()
    {
        JsonNode file = Load("story-calculations");
        JsonNode line = file["cases"]!.AsArray().First(c => c!["id"]!.GetValue<string>() == "b1-upfront-cash")!["inputs"]!["lines"]![0]!;
        line["amountPence"] = 0;

        Assert.That(Validate(file).Select(p => p.ToString()), Has.Some.Contain("amountPence"));
    }

    [Test]
    public void TestCaseFile_partialTotalWithNoReason_isRejected()
    {
        JsonNode file = Load("story-calculations");
        JsonNode expected = file["cases"]!.AsArray().First(c => c!["id"]!.GetValue<string>() == "b1-upfront-cash")!["expected"]!;
        expected["partialReasons"] = new JsonArray();

        Assert.That(Validate(file).Select(p => p.ToString()), Has.Some.Contain("partialReasons"));
    }

    [Test]
    public void TestCases_idsAreUnique()
    {
        string[] ids = AllCases().Select(c => c["id"]!.GetValue<string>()).ToArray();

        Assert.That(ids, Is.Unique);
    }

    [Test]
    public void TestCases_crossCaseLinks_pointAtCasesThatExist()
    {
        HashSet<string> ids = AllCases().Select(c => c["id"]!.GetValue<string>()).ToHashSet(StringComparer.Ordinal);
        var broken = new List<string>();

        foreach (JsonNode testCase in AllCases())
        {
            JsonNode inputs = testCase["inputs"]!;
            foreach (string key in new[] { "listingTotalCase", "budgetTotalCase" })
            {
                if (inputs[key] is { } link && !ids.Contains(link.GetValue<string>()))
                {
                    broken.Add(testCase["id"] + " " + key);
                }
            }

            foreach (JsonNode? line in inputs["lines"]?.AsArray() ?? [])
            {
                if (line!["mortgageCase"] is { } link && !ids.Contains(link.GetValue<string>()))
                {
                    broken.Add(testCase["id"] + " mortgageCase " + link);
                }
            }
        }

        Assert.That(broken, Is.Empty, string.Join("; ", broken));
    }
}
