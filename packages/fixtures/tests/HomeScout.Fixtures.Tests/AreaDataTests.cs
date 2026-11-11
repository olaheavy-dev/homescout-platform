using System.Text.RegularExpressions;
using System.Text.Json.Nodes;

namespace HomeScout.Fixtures.Tests;

/// <summary>
/// Story and consistency checks on data/area.json (issue 120): every England home has each topic or an explicit gap,
/// Wales is not covered, every link points at a real record, and the wording rules hold.
/// </summary>
[TestFixture]
internal sealed class AreaDataTests
{
    private static readonly string[] _englandHomes = ["B1", "B2", "R1", "R2"];

    // Doc 02 section 7 / issue 120 topic order.
    private static readonly string[] _topics =
    [
        "transport-stop", "school", "crime", "flood", "sold-price", "amenity", "energy-certificate",
        "school-inspection", "broadband", "bank-rate", "commute", "planning", "leasehold-company",
    ];

    private static readonly string[] _crimeFields = ["month", "counts", "neighbourhoodTeam"];

    private static readonly string[] _healthcareSubtypes = ["pharmacy", "hospital", "gp-surgery", "clinic", "dentist"];

    private static readonly string[] _amenitySubtypes =
        ["supermarket", "shop", "park", "pharmacy", "police-station", "hospital", "gp-surgery", "clinic", "dentist"];

    private static readonly string[] _liveFloodHomes = ["B2"];

    private static readonly string[] _gapStatuses = ["no-record-in-source", "stale", "source-failed", "not-covered"];

    private static IEnumerable<JsonObject> ForHome(string homeId) =>
        FixtureFiles.AreaItems().Where(i => i["homeId"]?.GetValue<string>() == homeId);

    private static string Text(JsonNode? node, string field) => node![field]!.GetValue<string>();

    [Test]
    public void Area_everyHomeId_isAHomeInTheHomesFile()
    {
        var homeIds = FixtureFiles.Load("homes")["homes"]!.AsArray().Select(h => Text(h, "id")).ToList();

        IEnumerable<string> used = FixtureFiles.AreaItems().Where(i => i["homeId"] is not null).Select(i => Text(i, "homeId"));

        Assert.That(used, Is.All.AnyOf(homeIds));
    }

    [Test]
    public void Area_ids_areUnique()
    {
        Assert.That(FixtureFiles.AreaItems().Select(i => Text(i, "id")), Is.Unique);
    }

    [Test]
    public void Area_everyId_followsHomeAreaTopicNumber()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems())
        {
            string owner = item["homeId"]?.GetValue<string>() ?? "UK";
            string topic = Text(item, "topic").ToUpperInvariant();
            Assert.That(Text(item, "id"), Does.Match("^" + Regex.Escape($"{owner}-AREA-{topic}-") + "[0-9]+$"));
        }
    }

    [Test]
    public void Area_everyTopic_isInTheAgreedEnumOrder()
    {
        JsonNode schema = JsonNode.Parse(File.ReadAllText(Path.Combine(FixtureFiles.SchemaDirectory, "area.schema.json")))!;
        string[] enumValues = schema["$defs"]!["areaItem"]!["properties"]!["topic"]!["enum"]!.AsArray().Select(n => n!.GetValue<string>()).ToArray();

        Assert.That(enumValues, Is.EqualTo(_topics));
    }

    [TestCase("B1")]
    [TestCase("B2")]
    [TestCase("R1")]
    [TestCase("R2")]
    public void Area_eachEnglandHome_hasEveryRequiredTopicOrAnExplicitGap(string homeId)
    {
        string tenure = Text(FixtureFiles.Home(homeId), "tenure");
        IEnumerable<string> required = _topics.Where(t => t != "bank-rate" && (t != "leasehold-company" || tenure == "leasehold"));
        var present = ForHome(homeId).Select(i => Text(i, "topic")).ToHashSet();

        Assert.That(required.Where(t => !present.Contains(t)), Is.Empty);
    }

    [Test]
    public void Area_everyHomeItem_ofAnEnglandHome_isCoveredOrAGapThatSaysWhy()
    {
        foreach (string homeId in _englandHomes)
        {
            Assert.That(ForHome(homeId).Select(i => Text(i, "status")), Is.All.Not.EqualTo("not-covered"), homeId);
        }
    }

    [Test]
    public void Area_wales1_hasOnlyNotCoveredItems()
    {
        List<JsonObject> items = ForHome("WALES-1").ToList();

        Assert.Multiple(() =>
        {
            Assert.That(items, Is.Not.Empty);
            Assert.That(items.Select(i => Text(i, "status")), Is.All.EqualTo("not-covered"));
        });
    }

    [Test]
    public void Area_wales1_hasAnItemForEachPerHomeTopicExceptLeaseholdAndBankRate()
    {
        var topics = ForHome("WALES-1").Select(i => Text(i, "topic")).ToHashSet();

        Assert.That(_topics.Where(t => t != "bank-rate" && t != "leasehold-company" && !topics.Contains(t)), Is.Empty);
    }

    [Test]
    public void Area_gapExamples_includeEveryStatusTheIssueRequires()
    {
        var statuses = FixtureFiles.AreaItems().Select(i => Text(i, "status")).ToHashSet();

        Assert.That(_gapStatuses.Where(s => !statuses.Contains(s)), Is.Empty);
    }

    [Test]
    public void Area_everySource_isSyntheticAndLabelled()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems())
        {
            Assert.Multiple(() =>
            {
                Assert.That(item["source"]!["synthetic"]!.GetValue<bool>(), Is.True, Text(item, "id"));
                Assert.That(Text(item["source"], "origin"), Is.EqualTo("synthetic"), Text(item, "id"));
            });
        }
    }

    [Test]
    public void Area_dates_areNotAfterTheSnapshotDate()
    {
        string snapshot = Text(FixtureFiles.Load("snapshot")["snapshot"], "snapshotDate");
        foreach (JsonObject item in FixtureFiles.AreaItems())
        {
            string date = Text(item["source"], "date");
            Assert.That(string.CompareOrdinal(date, snapshot[..date.Length]), Is.LessThanOrEqualTo(0), Text(item, "id"));
        }
    }

    [Test]
    public void Area_file_neverUsesSafeUnsafeVerifiedOrApprovedWording()
    {
        // Rule 4: the product never says a home is verified, safe or approved, and crime is never presented as safe or unsafe.
        string text = File.ReadAllText(Path.Combine(FixtureFiles.FixturesDirectory, "data", "area.json"));

        Assert.That(Regex.Matches(text, @"\b(safe|unsafe|verified|approved)\b", RegexOptions.IgnoreCase).Select(m => m.Value), Is.Empty);
    }

    [Test]
    public void Area_schemaFile_hasNoRatingOrScoreFieldOnCrime()
    {
        string schema = File.ReadAllText(Path.Combine(FixtureFiles.SchemaDirectory, "area.schema.json"));
        JsonNode crime = JsonNode.Parse(schema)!["$defs"]!["crimeValue"]!;

        Assert.Multiple(() =>
        {
            Assert.That(crime["additionalProperties"]!.GetValue<bool>(), Is.False);
            Assert.That(crime["properties"]!.AsObject().Select(p => p.Key), Is.EquivalentTo(_crimeFields));
        });
    }

    [Test]
    public void Area_everyDistance_namesItsSyntheticMethod()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => i["value"]?["distanceMetres"] is not null))
        {
            Assert.That(Text(item["value"], "distanceMethod"), Does.Contain("synthetic"), Text(item, "id"));
        }
    }

    [TestCase("B1", "transport-stop")]
    [TestCase("B2", "transport-stop")]
    [TestCase("R1", "transport-stop")]
    [TestCase("R2", "transport-stop")]
    [TestCase("B1", "school")]
    [TestCase("B2", "school")]
    [TestCase("R1", "school")]
    [TestCase("R2", "school")]
    [TestCase("B1", "crime")]
    [TestCase("B2", "crime")]
    [TestCase("R1", "crime")]
    [TestCase("R2", "crime")]
    [TestCase("B1", "sold-price")]
    [TestCase("B2", "sold-price")]
    [TestCase("B1", "amenity")]
    [TestCase("B2", "amenity")]
    [TestCase("R1", "amenity")]
    [TestCase("R2", "amenity")]
    public void Area_priorityTopic_hasTwoToFourItemsForEachHome(string homeId, string topic)
    {
        int count = ForHome(homeId).Count(i => Text(i, "topic") == topic);

        Assert.That(count, Is.InRange(2, 4));
    }

    [Test]
    public void Area_crimeForB1AndB2_coversTwoDifferentMonths()
    {
        foreach (string homeId in new[] { "B1", "B2" })
        {
            var months = ForHome(homeId).Where(i => Text(i, "topic") == "crime" && Text(i, "status") == "recorded")
                .Select(i => Text(i["value"], "month")).Distinct().ToList();
            Assert.That(months, Has.Count.GreaterThanOrEqualTo(2), homeId);
        }
    }

    [Test]
    public void Area_everyHome_hasAHealthcareLocation()
    {
        foreach (string homeId in _englandHomes)
        {
            Assert.That(ForHome(homeId).Any(i => Text(i, "topic") == "amenity" && i["subtype"] is not null && _healthcareSubtypes.Contains(Text(i, "subtype"))), Is.True, homeId);
        }
    }

    [Test]
    public void Area_amenities_coverEverySubtypeSomewhereInEngland()
    {
        var present = _englandHomes.SelectMany(ForHome).Where(i => Text(i, "topic") == "amenity" && i["subtype"] is not null).Select(i => Text(i, "subtype")).ToHashSet();

        Assert.That(_amenitySubtypes.Where(s => !present.Contains(s)), Is.Empty);
    }

    [Test]
    public void Area_floodWarnings_exactlyOneHomeHasALiveWarning()
    {
        IEnumerable<JsonObject> live = FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "flood" && Text(i, "status") == "recorded");

        Assert.That(live.Select(i => Text(i, "homeId")), Is.EqualTo(_liveFloodHomes));
    }

    [Test]
    public void Area_floodItemsWithNoRecord_pointTheUserToTheLongTermChecker()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "flood" && Text(i, "status") == "no-record-in-source"))
        {
            Assert.That(Text(item["link"], "url"), Is.EqualTo("https://www.gov.uk/check-long-term-flood-risk"), Text(item, "id"));
        }
    }

    [Test]
    public void Area_everyEnglandHome_hasAFloodItem()
    {
        foreach (string homeId in _englandHomes)
        {
            Assert.That(ForHome(homeId).Any(i => Text(i, "topic") == "flood"), Is.True, homeId);
        }
    }

    [TestCase("B1", "C", 2019)]
    [TestCase("B2", "D", 2021)]
    [TestCase("R1", "C", 2022)]
    public void Area_energyRating_matchesTheCertificateInTheEvidenceFile(string homeId, string rating, int year)
    {
        JsonNode value = ForHome(homeId).Single(i => Text(i, "topic") == "energy-certificate")["value"]!;

        Assert.Multiple(() =>
        {
            Assert.That(Text(value, "rating"), Is.EqualTo(rating));
            Assert.That(value["issuedYear"]!.GetValue<int>(), Is.EqualTo(year));
        });
    }

    [Test]
    public void Area_r2Energy_isStaleLikeItsExpiredCertificateAndHasNoRatingOrCost()
    {
        JsonObject item = ForHome("R2").Single(i => Text(i, "topic") == "energy-certificate");

        Assert.Multiple(() =>
        {
            Assert.That(Text(item, "status"), Is.EqualTo("stale"));
            Assert.That(item["value"]!["issuedYear"]!.GetValue<int>(), Is.EqualTo(2015));
            Assert.That(item["value"]!["expiredYear"]!.GetValue<int>(), Is.EqualTo(2025));
            Assert.That(item["value"]!["rating"], Is.Null);
            Assert.That(item["value"]!["estimatedAnnualCostRange"], Is.Null);
        });
    }

    [Test]
    public void Area_energyCostRange_lowIsNotAboveHigh()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => i["value"]?["estimatedAnnualCostRange"] is not null))
        {
            JsonNode range = item["value"]!["estimatedAnnualCostRange"]!;
            Assert.That(range["lowPence"]!.GetValue<int>(), Is.LessThanOrEqualTo(range["highPence"]!.GetValue<int>()), Text(item, "id"));
        }
    }

    [Test]
    public void Area_bankRate_isOneSharedItemWithASourceDate()
    {
        List<JsonObject> items = FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "bank-rate").ToList();

        Assert.Multiple(() =>
        {
            Assert.That(items, Has.Count.EqualTo(1));
            Assert.That(items[0]["homeId"], Is.Null);
            Assert.That(Text(items[0]["source"], "date"), Is.Not.Empty);
        });
    }

    [Test]
    public void Area_commute_usesTheHouseholdCommuteCriterion()
    {
        JsonNode household = FixtureFiles.Load("household")["household"]!;
        var criterionIds = household["priorities"]!.AsArray().Select(p => Text(p, "id")).ToList();

        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "commute" && Text(i, "status") == "recorded"))
        {
            Assert.That(criterionIds, Does.Contain(Text(item["value"], "criterionId")), Text(item, "id"));
        }
    }

    [Test]
    public void Area_everyEnglandHome_hasACommuteItem()
    {
        foreach (string homeId in _englandHomes)
        {
            Assert.That(ForHome(homeId).Any(i => Text(i, "topic") == "commute"), Is.True, homeId);
        }
    }

    [Test]
    public void Area_schoolInspections_pointAtASchoolOfTheSameHome()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "school-inspection" && i["value"] is not null))
        {
            string schoolId = Text(item["value"], "schoolItemId");
            JsonObject school = FixtureFiles.AreaItems().Single(i => Text(i, "id") == schoolId);
            Assert.Multiple(() =>
            {
                Assert.That(Text(school, "topic"), Is.EqualTo("school"), schoolId);
                Assert.That(Text(school, "homeId"), Is.EqualTo(Text(item, "homeId")), schoolId);
            });
        }
    }

    [Test]
    public void Area_councilTax_isNotAreaData()
    {
        // Council tax is a user-entered cost input already (evidence file); it has no area topic.
        Assert.That(FixtureFiles.AreaItems().Select(i => Text(i, "topic")), Has.None.Contain("council"));
    }
}
