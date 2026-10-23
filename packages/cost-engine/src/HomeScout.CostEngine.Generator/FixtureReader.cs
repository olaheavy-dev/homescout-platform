using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Generator;

/// <summary>A story: its steps in order, and the homes it covers.</summary>
internal sealed record StoryData(string Id, IReadOnlyList<int> Steps, IReadOnlyList<string> HomeIds);

/// <summary>A home as the data file describes it. The mode is null when the data does not say (a home that is not yet covered).</summary>
internal sealed record HomeData(string Id, Mode? Mode, Nation Nation);

/// <summary>One evidence item and whom it is about.</summary>
internal sealed record EvidenceRow(string SubjectType, string SubjectId, EvidenceItem Item);

/// <summary>Everything the generator reads from <c>packages/fixtures/data</c>.</summary>
internal sealed record FixtureData(
    string SnapshotDate,
    string HouseholdId,
    IReadOnlyList<string> HomeIds,
    IReadOnlyList<StoryData> Stories,
    IReadOnlyList<HomeData> Homes,
    Pence MonthlyBudget,
    IReadOnlyList<EvidenceRow> Evidence);

/// <summary>
/// Reads the fixture data files into the engine's own types. The files are checked against their schemas by
/// <c>make validate</c>; anything this reader does not understand is an <see cref="InvalidDataException"/> rather than a guess.
/// A missing file is an <see cref="IOException"/>.
/// </summary>
internal static class FixtureReader
{
    public static FixtureData Read(string fixturesDirectory)
    {
        try
        {
            return ReadFiles(fixturesDirectory);
        }
        catch (Exception exception) when (exception is InvalidOperationException or FormatException)
        {
            // JsonNode throws these when a value has the wrong JSON type (text where a number belongs, a list where an object belongs).
            throw new InvalidDataException($"A data file has a value of the wrong type: {exception.Message}", exception);
        }
    }

    private static FixtureData ReadFiles(string fixturesDirectory)
    {
        JsonNode snapshot = Load(fixturesDirectory, "snapshot")["snapshot"] ?? throw Invalid("snapshot.json has no snapshot.");
        JsonNode household = Load(fixturesDirectory, "household")["household"] ?? throw Invalid("household.json has no household.");
        JsonNode homes = Load(fixturesDirectory, "homes")["homes"] ?? throw Invalid("homes.json has no homes.");
        JsonNode evidence = Load(fixturesDirectory, "evidence")["evidence"] ?? throw Invalid("evidence.json has no evidence.");

        return new FixtureData(
            Text(snapshot, "snapshotDate"),
            Text(snapshot, "householdId"),
            Array(snapshot, "homeIds").Select(n => n!.GetValue<string>()).ToList(),
            Array(snapshot, "stories").Select(s => ReadStory(s!)).ToList(),
            homes.AsArray().Select(h => ReadHome(h!)).ToList(),
            ReadBudget(household),
            evidence.AsArray().Select(e => ReadEvidence(e!)).ToList());
    }

    private static JsonNode Load(string fixturesDirectory, string name)
    {
        string path = Path.Combine(fixturesDirectory, "data", name + ".json");
        return JsonNode.Parse(File.ReadAllText(path)) ?? throw Invalid($"{path} is empty.");
    }

    private static StoryData ReadStory(JsonNode story) =>
        new(
            Text(story, "id"),
            Array(story, "steps").Select(s => Number(s!, "step")).ToList(),
            Array(story, "homeIds").Select(n => n!.GetValue<string>()).ToList());

    private static HomeData ReadHome(JsonNode home)
    {
        Mode? mode = home["mode"]?.GetValue<string>() switch
        {
            null => null,
            "buy" => Mode.Buy,
            "rent" => Mode.Rent,
            var other => throw Invalid($"Unknown mode '{other}'."),
        };

        string nation = Text(home["address"] ?? throw Invalid("A home has no address."), "nation");
        return new HomeData(Text(home, "id"), mode, ParseNation(nation));
    }

    private static Nation ParseNation(string nation) => nation switch
    {
        "England" => Nation.England,
        "Wales" => Nation.Wales,
        "Scotland" => Nation.Scotland,
        "Northern Ireland" => Nation.NorthernIreland,
        _ => throw Invalid($"Unknown nation '{nation}'."),
    };

    private static Pence ReadBudget(JsonNode household)
    {
        JsonNode budget = household["monthlyBudget"] ?? throw Invalid("The household has no monthlyBudget.");
        if (Text(budget, "period") != "month")
        {
            throw Invalid("The household budget must be a monthly amount.");
        }

        return new Pence(budget["pence"]?.GetValue<long>() ?? throw Invalid("The household budget has no pence."));
    }

    private static EvidenceRow ReadEvidence(JsonNode item)
    {
        EvidenceStatus status = Text(item, "status") switch
        {
            "available" => EvidenceStatus.Available,
            "missing" => EvidenceStatus.Missing,
            "conflicting" => EvidenceStatus.Conflicting,
            "stale" => EvidenceStatus.Stale,
            "not-applicable" => EvidenceStatus.NotApplicable,
            "not-calculated" => EvidenceStatus.NotCalculated,
            "included" => EvidenceStatus.Included,
            var other => throw Invalid($"Unknown evidence status '{other}'."),
        };

        var evidence = new EvidenceItem(
            Text(item, "id"),
            Text(item, "category"),
            status,
            item["value"] is { } value ? ReadValue(value) : null,
            item["contextOnly"]?.GetValue<bool>() ?? throw Invalid($"{Text(item, "id")} has no contextOnly."),
            item["usedFromStep"] is { } from ? from.GetValue<int>() : null,
            item["supersedes"]?.GetValue<string>());

        return new EvidenceRow(Text(item, "subjectType"), Text(item, "subjectId"), evidence);
    }

    private static EvidenceValue ReadValue(JsonNode value) => Text(value, "kind") switch
    {
        "money" => new MoneyValue(new Pence(value["pence"]?.GetValue<long>() ?? throw Invalid("A money value has no pence.")), ReadPeriod(Text(value, "period"))),
        "rate" => new RateValue(Number(value, "basisPoints")),
        "quantity" when Text(value, "unit") == "years" => new YearsValue(Number(value, "amount")),
        _ => new OtherValue(),
    };

    private static Period ReadPeriod(string period) => period switch
    {
        "once" => Period.Once,
        "month" => Period.Month,
        "year" => Period.Year,
        _ => throw Invalid($"Unknown period '{period}'."),
    };

    private static string Text(JsonNode node, string key) =>
        node[key]?.GetValue<string>() ?? throw Invalid($"A required text field '{key}' is missing.");

    private static int Number(JsonNode node, string key) =>
        node[key]?.GetValue<int>() ?? throw Invalid($"A required number field '{key}' is missing.");

    private static JsonArray Array(JsonNode node, string key) =>
        node[key]?.AsArray() ?? throw Invalid($"A required list '{key}' is missing.");

    private static InvalidDataException Invalid(string message) => new(message);
}
