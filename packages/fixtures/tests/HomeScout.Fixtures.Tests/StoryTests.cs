using System.Text.Json.Nodes;

namespace HomeScout.Fixtures.Tests;

/// <summary>The stories and cross-file links in the approved sample data (stage 2 plan, section 1).</summary>
[TestFixture]
internal sealed class StoryTests
{
    private static readonly string[] _recordFiles = ["evidence", "documents", "questions", "replies"];

    [TestCase("B1-EPC", "C", 2019)]
    [TestCase("B2-EPC", "D", 2021)]
    [TestCase("R1-EPC", "C", 2022)]
    public void EnergyCertificate_ofEachHomeWithOne_hasTheApprovedRatingAndYear(string id, string rating, int year)
    {
        JsonObject value = FixtureFiles.EvidenceItem(id)["value"]!.AsObject();

        Assert.Multiple(() =>
        {
            Assert.That(value["rating"]!.GetValue<string>(), Is.EqualTo(rating));
            Assert.That(value["issuedYear"]!.GetValue<int>(), Is.EqualTo(year));
        });
    }

    [Test]
    public void R1WaterListingClaim_whenCheckedAgainstTheStatement_isConflicting()
    {
        JsonObject listing = FixtureFiles.EvidenceItem("R1-WATER-LISTING");

        Assert.Multiple(() =>
        {
            Assert.That(listing["status"]!.GetValue<string>(), Is.EqualTo("conflicting"));
            Assert.That(listing["value"]!["text"]!.GetValue<string>(), Is.EqualTo("Water included"));
        });
    }

    [Test]
    public void R1WaterWrittenStatement_inBillsSection_saysTenantPaysWater()
    {
        JsonObject statement = FixtureFiles.EvidenceItem("R1-WATER-WSOT");

        Assert.Multiple(() =>
        {
            Assert.That(statement["value"]!["text"]!.GetValue<string>(), Is.EqualTo("Tenant pays water"));
            Assert.That(statement["source"]!["documentType"]!.GetValue<string>(), Is.EqualTo("written-statement-of-terms"));
        });
    }

    [Test]
    public void R1WaterEstimate_afterTheUserConfirms_isUsedFromStep4()
    {
        Assert.That(FixtureFiles.EvidenceItem("R1-WATER-ESTIMATE")["usedFromStep"]!.GetValue<int>(), Is.EqualTo(4));
    }

    [Test]
    public void B1ServiceChargeBudget_afterTheUserConfirms_isUsedFromStep4()
    {
        Assert.That(FixtureFiles.EvidenceItem("B1-SC-BUDGET")["usedFromStep"]!.GetValue<int>(), Is.EqualTo(4));
    }

    [Test]
    public void R2CouncilTax_whenRentIncludesBills_isPresentAndNotIncluded()
    {
        JsonObject charge = FixtureFiles.EvidenceItem("R2-CT-CHARGE");
        JsonObject band = FixtureFiles.EvidenceItem("R2-CT-BAND");

        Assert.Multiple(() =>
        {
            Assert.That(charge["status"]!.GetValue<string>(), Is.EqualTo("available"));
            Assert.That(charge["value"]!["pence"]!.GetValue<long>(), Is.EqualTo(185000));
            Assert.That(band["status"]!.GetValue<string>(), Is.EqualTo("available"));
        });
    }

    [Test]
    public void Ids_acrossEvidenceDocumentsQuestionsAndReplies_areUnique()
    {
        string[] ids = _recordFiles
            .SelectMany(file => FixtureFiles.Load(file)[file]!.AsArray())
            .Select(record => record!["id"]!.GetValue<string>())
            .ToArray();

        Assert.That(ids, Is.Unique);
    }

    [Test]
    public void Snapshot_householdAndHomeIds_resolveToRecords()
    {
        JsonObject snapshot = FixtureFiles.Load("snapshot")["snapshot"]!.AsObject();
        string householdId = FixtureFiles.Load("household")["household"]!["id"]!.GetValue<string>();
        string[] homeIds = FixtureFiles.Load("homes")["homes"]!.AsArray().Select(h => h!["id"]!.GetValue<string>()).ToArray();

        Assert.Multiple(() =>
        {
            Assert.That(snapshot["householdId"]!.GetValue<string>(), Is.EqualTo(householdId));
            Assert.That(snapshot["homeIds"]!.AsArray().Select(h => h!.GetValue<string>()), Is.EquivalentTo(homeIds));
        });
    }

    [Test]
    public void Story_homeIds_resolveToHomesInTheSnapshot()
    {
        JsonObject snapshot = FixtureFiles.Load("snapshot")["snapshot"]!.AsObject();
        HashSet<string> homeIds = snapshot["homeIds"]!.AsArray().Select(h => h!.GetValue<string>()).ToHashSet(StringComparer.Ordinal);
        string[] storyHomes = snapshot["stories"]!.AsArray()
            .SelectMany(story => story!["homeIds"]!.AsArray())
            .Select(h => h!.GetValue<string>())
            .ToArray();

        Assert.That(storyHomes, Is.Not.Empty);
        Assert.That(storyHomes.Where(h => !homeIds.Contains(h)), Is.Empty);
    }

    [Test]
    public void Source_syntheticFlag_isTrueInEveryDataFile()
    {
        string[] files = ["household", "homes", "evidence", "documents", "questions", "replies", "snapshot"];
        var notSynthetic = new List<string>();

        foreach (string file in files)
        {
            Collect(FixtureFiles.Load(file), file, notSynthetic);
        }

        Assert.That(notSynthetic, Is.Empty, string.Join("; ", notSynthetic));
    }

    private static void Collect(JsonNode? node, string path, List<string> notSynthetic)
    {
        switch (node)
        {
            case JsonObject obj:
                if (obj.ContainsKey("origin") && obj["synthetic"]?.GetValue<bool>() != true)
                {
                    notSynthetic.Add(path);
                }

                foreach (KeyValuePair<string, JsonNode?> pair in obj)
                {
                    Collect(pair.Value, path + "/" + pair.Key, notSynthetic);
                }

                break;
            case JsonArray array:
                for (int i = 0; i < array.Count; i++)
                {
                    Collect(array[i], path + "/" + i, notSynthetic);
                }

                break;
        }
    }
}
