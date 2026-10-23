using System.Text;
using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Generator.Tests;

/// <summary>The generator as a program: what it writes, what it deletes, and how it fails.</summary>
[TestFixture]
internal sealed class RunTests
{
    private readonly List<string> _temporaryFolders = [];

    [TearDown]
    public void DeleteTemporaryFolders()
    {
        foreach (string folder in _temporaryFolders)
        {
            Directory.Delete(folder, recursive: true);
        }

        _temporaryFolders.Clear();
    }

    private string NewFixtures()
    {
        string fixtures = GeneratedFixture.CopyDataToTemporaryFixtures();
        _temporaryFolders.Add(fixtures);
        return fixtures;
    }

    [Test]
    public void Run_realData_writesCostsJsonAsUtf8WithoutByteOrderMark()
    {
        string fixtures = NewFixtures();

        int exit = CostsGenerator.Run(fixtures, TextWriter.Null);

        byte[] bytes = File.ReadAllBytes(Path.Combine(fixtures, "generated", "costs.json"));
        Assert.That(exit, Is.EqualTo(0));
        Assert.That(bytes.Take(3), Is.Not.EqualTo(new byte[] { 0xEF, 0xBB, 0xBF }));
        Assert.That(bytes, Is.EqualTo(new UTF8Encoding(false).GetBytes(GeneratedFixture.Json)));
        Assert.That(bytes[^1], Is.EqualTo((byte)'\n'));
        Assert.That(bytes[^2], Is.Not.EqualTo((byte)'\n'));
    }

    [Test]
    public void Run_twice_givesByteIdenticalFiles()
    {
        string fixtures = NewFixtures();
        string path = Path.Combine(fixtures, "generated", "costs.json");

        CostsGenerator.Run(fixtures, TextWriter.Null);
        byte[] first = File.ReadAllBytes(path);
        CostsGenerator.Run(fixtures, TextWriter.Null);

        Assert.That(File.ReadAllBytes(path), Is.EqualTo(first));
    }

    [Test]
    public void Run_otherJsonFileInGenerated_isDeletedAndOtherFilesAreKept()
    {
        string fixtures = NewFixtures();
        string generated = Path.Combine(fixtures, "generated");
        Directory.CreateDirectory(generated);
        File.WriteAllText(Path.Combine(generated, "old.json"), "{}");
        File.WriteAllText(Path.Combine(generated, "notes.md"), "keep me");

        int exit = CostsGenerator.Run(fixtures, TextWriter.Null);

        Assert.That(exit, Is.EqualTo(0));
        Assert.That(File.Exists(Path.Combine(generated, "old.json")), Is.False);
        Assert.That(File.Exists(Path.Combine(generated, "notes.md")), Is.True);
        Assert.That(File.Exists(Path.Combine(generated, "costs.json")), Is.True);
    }

    [Test]
    public void Run_engineFailure_exitsNonZeroNamesTheErrorCodeAndWritesNothing()
    {
        string fixtures = NewFixtures();
        RemoveEvidence(fixtures, "B1-PRICE");
        using var error = new StringWriter();

        int exit = CostsGenerator.Run(fixtures, error);

        Assert.That(exit, Is.Not.EqualTo(0));
        Assert.That(error.ToString(), Does.Contain("input.missing.asking-price"));
        Assert.That(error.ToString(), Does.Contain("B1"));
        Assert.That(Directory.Exists(Path.Combine(fixtures, "generated")), Is.False);
    }

    [Test]
    public void Run_engineFailure_leavesAnExistingGeneratedFolderUntouched()
    {
        string fixtures = NewFixtures();
        string generated = Path.Combine(fixtures, "generated");
        Directory.CreateDirectory(generated);
        File.WriteAllText(Path.Combine(generated, "costs.json"), "previous");
        File.WriteAllText(Path.Combine(generated, "old.json"), "{}");
        RemoveEvidence(fixtures, "B1-PRICE");

        int exit = CostsGenerator.Run(fixtures, TextWriter.Null);

        Assert.That(exit, Is.Not.EqualTo(0));
        Assert.That(File.ReadAllText(Path.Combine(generated, "costs.json")), Is.EqualTo("previous"));
        Assert.That(File.Exists(Path.Combine(generated, "old.json")), Is.True);
    }

    [Test]
    public void Generate_coveredHomeInNoStory_failsWithItsCodeNotGuessing()
    {
        string fixtures = NewFixtures();
        string path = Path.Combine(fixtures, "data", "snapshot.json");
        JsonNode snapshot = JsonNode.Parse(File.ReadAllText(path))!;
        snapshot["snapshot"]!["stories"]!.AsArray()[0]!["homeIds"] = new JsonArray("B2");
        File.WriteAllText(path, snapshot.ToJsonString());

        Result<string> result = CostsGenerator.Generate(fixtures);

        Assert.That(result.IsFailure, Is.True);
        Assert.That(result.Error.Code, Is.EqualTo("home.not-in-a-story"));
    }

    [Test]
    public void Generate_dataFileMissing_throwsInsteadOfWritingGuesses()
    {
        string fixtures = NewFixtures();
        File.Delete(Path.Combine(fixtures, "data", "household.json"));

        Assert.That(() => CostsGenerator.Generate(fixtures), Throws.InstanceOf<IOException>());
    }

    [Test]
    public void Generate_unknownEvidenceStatus_throwsInsteadOfGuessing()
    {
        string fixtures = NewFixtures();
        string path = Path.Combine(fixtures, "data", "evidence.json");
        JsonNode evidence = JsonNode.Parse(File.ReadAllText(path))!;
        evidence["evidence"]!.AsArray()[0]!["status"] = "surprising";
        File.WriteAllText(path, evidence.ToJsonString());

        Assert.That(() => CostsGenerator.Generate(fixtures), Throws.InstanceOf<InvalidDataException>());
    }

    [Test]
    public void CommittedCostsFile_matchesWhatTheGeneratorProduces()
    {
        string committed = Path.Combine(GeneratedFixture.FixturesDirectory, "generated", "costs.json");

        Assert.That(File.ReadAllBytes(committed), Is.EqualTo(new UTF8Encoding(false).GetBytes(GeneratedFixture.Json)), "Run 'make generate' and commit the result.");
    }

    private static void RemoveEvidence(string fixtures, string id)
    {
        string path = Path.Combine(fixtures, "data", "evidence.json");
        JsonNode evidence = JsonNode.Parse(File.ReadAllText(path))!;
        JsonArray items = evidence["evidence"]!.AsArray();
        items.Remove(items.Single(i => i!["id"]!.GetValue<string>() == id));
        File.WriteAllText(path, evidence.ToJsonString());
    }
}
