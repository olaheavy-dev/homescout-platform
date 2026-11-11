using System.Text.Json.Nodes;
using System.Text.RegularExpressions;

namespace Vestagraph.Fixtures.Tests;

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
        ["supermarket", "shop", "park", "pharmacy", "police-station", "hospital", "gp-surgery", "clinic", "dentist", "childcare", "place-of-worship"];

    private static readonly string[] _r2Certificate = ["R2-EPC"];

    private static readonly string[] _allowedOrigins = ["official-dataset", "user-entered", "plan"];

    private static readonly string[] _recordedCrimeMonths = ["2026-07", "2026-08"];

    private static readonly string[][] _amenityCategories =
    [
        ["supermarket", "shop"],
        ["park"],
        ["hospital", "gp-surgery", "clinic", "dentist", "pharmacy"],
        ["police-station"],
        ["childcare"],
        ["place-of-worship"],
    ];

    private static readonly string[] _liveFloodHomes = ["B2"];

    private static readonly string[] _worshipValueFields = ["name", "distanceMetres", "distanceMethod", "religion"];

    private const string _worshipLimit = "does not establish service times, which community it serves, or that the list of places is complete.";

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
                Assert.That(_allowedOrigins, Does.Contain(Text(item["source"], "origin")), Text(item, "id"));
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

    [TestCase("B1", "B1-EPC", "B1-EPC-COST")]
    [TestCase("B2", "B2-EPC", "B2-EPC-COST")]
    [TestCase("R1", "R1-EPC", "R1-EPC-COST")]
    public void Area_energyItem_pointsAtTheCertificateAndItsCostInTheEvidenceFile(string homeId, string certificateId, string costId)
    {
        JsonObject item = ForHome(homeId).Single(i => Text(i, "topic") == "energy-certificate");

        Assert.Multiple(() =>
        {
            Assert.That(Text(item, "status"), Is.EqualTo("recorded"));
            Assert.That(item["value"]!["evidenceItemIds"]!.AsArray().Select(n => n!.GetValue<string>()), Is.EqualTo([certificateId, costId]));
        });
    }

    [Test]
    public void Area_r2Energy_isStaleAndPointsAtItsExpiredCertificateOnly()
    {
        JsonObject item = ForHome("R2").Single(i => Text(i, "topic") == "energy-certificate");

        Assert.Multiple(() =>
        {
            Assert.That(Text(item, "status"), Is.EqualTo("stale"));
            Assert.That(item["value"]!["evidenceItemIds"]!.AsArray().Select(n => n!.GetValue<string>()), Is.EqualTo(_r2Certificate));
        });
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

    // Places of worship are listed as the nearest places only, every faith alike: never counts,
    // densities or an area's religious makeup (founder decision, 11 Nov 2026; register PD-13).
    [Test]
    public void Area_placesOfWorship_areSinglePlacesWithAReligionAndOneSharedLimit()
    {
        List<JsonObject> worship = _englandHomes.SelectMany(ForHome)
            .Where(i => Text(i, "topic") == "amenity" && i["subtype"] is not null && Text(i, "subtype") == "place-of-worship").ToList();

        Assert.That(worship, Is.Not.Empty);
        foreach (JsonObject item in worship.Where(i => Text(i, "status") is "recorded" or "stale"))
        {
            Assert.That(item["value"]!.AsObject().Select(p => p.Key), Is.EquivalentTo(_worshipValueFields), Text(item, "id"));
        }

        Assert.That(worship.Select(i => Text(i, "doesNotEstablish")), Has.All.Contain(_worshipLimit));
    }

    [TestCase("B1")]
    [TestCase("B2")]
    [TestCase("R1")]
    [TestCase("R2")]
    public void Area_eachEnglandHome_hasEveryAmenityCategoryOrAnExplicitNoRecordItem(string homeId)
    {
        List<JsonObject> amenities = ForHome(homeId).Where(i => Text(i, "topic") == "amenity" && i["subtype"] is not null).ToList();

        foreach (string[] category in _amenityCategories)
        {
            Assert.That(
                amenities.Any(i => category.Contains(Text(i, "subtype")) && Text(i, "status") is "recorded" or "no-record-in-source" or "stale"),
                Is.True,
                homeId + ": " + string.Join("/", category));
        }
    }

    [Test]
    public void Area_energyItems_pointAtEvidenceItemsThatExist()
    {
        var evidenceIds = FixtureFiles.Load("evidence")["evidence"]!.AsArray().Select(e => Text(e, "id")).ToHashSet();

        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "energy-certificate" && i["value"] is not null))
        {
            IEnumerable<string> ids = item["value"]!["evidenceItemIds"]!.AsArray().Select(n => n!.GetValue<string>());
            Assert.That(ids, Has.All.Matches<string?>(id => id is not null && evidenceIds.Contains(id)), Text(item, "id"));
        }
    }

    [Test]
    public void Area_energyItems_neverSayThisFlat()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "energy-certificate" && Text(i, "status") != "not-covered"))
        {
            Assert.That(Text(item, "doesNotEstablish"), Does.Not.Contain("this flat").And.Contain("this home").And.Contain("not actual bills"), Text(item, "id"));
        }
    }

    [Test]
    public void Area_floodItems_neverUseSurfaceWaterAsASubtypeAndSayWhyAndWhereToLook()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "flood" && Text(i, "status") != "not-covered"))
        {
            Assert.Multiple(() =>
            {
                Assert.That(Text(item, "subtype"), Is.AnyOf("rivers-and-sea", "groundwater"), Text(item, "id"));
                Assert.That(Text(item, "doesNotEstablish"), Does.Contain("Warnings are not issued for surface water flooding"), Text(item, "id"));
            });
        }
    }

    [Test]
    public void Area_commute_isTheHouseholdsOwnEstimateNotARoutedJourney()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "commute" && Text(i, "status") != "not-covered"))
        {
            Assert.Multiple(() =>
            {
                Assert.That(Text(item["source"], "origin"), Is.EqualTo("user-entered"), Text(item, "id"));
                Assert.That(Text(item["source"], "label"), Is.EqualTo("the household's own estimate"), Text(item, "id"));
                Assert.That(Text(item, "doesNotEstablish"), Does.Contain("not a routed or timetabled journey"), Text(item, "id"));
                Assert.That(Text(item["value"], "method"), Is.EqualTo("estimated by the household; not a routed journey time (routing is DA-06)"), Text(item, "id"));
            });
        }
    }

    [Test]
    public void Area_soldPriceAddresses_areUniqueSoNoAddressHasTwoPrices()
    {
        Assert.That(FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "sold-price" && i["value"] is not null).Select(i => Text(i["value"], "addressText")), Is.Unique);
    }

    [Test]
    public void Area_aSchoolInspected_isInspectedTheSameWayEverywhereItAppears()
    {
        var bySchool = FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "school-inspection" && i["value"] is not null)
            .GroupBy(i => Text(i["value"], "schoolName"));

        foreach (IGrouping<string, JsonObject> group in bySchool)
        {
            Assert.That(group.Select(i => Text(i["value"], "framework") + "|" + Text(i["value"], "inspectionDate")).Distinct().Count(), Is.EqualTo(1), group.Key);
        }
    }

    [Test]
    public void Area_crimeMonths_areTheTwoLaggedMonths()
    {
        var months = FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "crime" && i["value"] is not null).Select(i => Text(i["value"], "month"));

        Assert.That(months, Has.All.Matches<string>(m => _recordedCrimeMonths.Contains(m)));
    }

    [Test]
    public void Area_everyEnglandHomeWithCrime_coversBothLaggedMonthsRecordedOrNamedAsFailed()
    {
        foreach (string homeId in _englandHomes)
        {
            List<JsonObject> crime = ForHome(homeId).Where(i => Text(i, "topic") == "crime").ToList();
            foreach (string month in _recordedCrimeMonths)
            {
                bool recorded = crime.Any(i => i["value"] is not null && Text(i["value"], "month") == month);
                bool failed = crime.Any(i => Text(i, "status") == "source-failed" && Text(i, "label").Contains(month, StringComparison.Ordinal));
                Assert.That(recorded || failed, Is.True, homeId + " " + month);
            }
        }
    }

    [Test]
    public void Area_energyItemsThatAreStale_doNotCopyTheCertificateYear()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "energy-certificate" && Text(i, "status") == "stale"))
        {
            Assert.That(Text(item, "label"), Does.Not.Match(@"\d{4}"), Text(item, "id"));
        }
    }

    [Test]
    public void Area_valueDates_areNotAfterTheSnapshotDate()
    {
        string snapshot = Text(FixtureFiles.Load("snapshot")["snapshot"], "snapshotDate");
        string[] dateFields = ["month", "saleDate", "inspectionDate", "statusDate", "receivedDate", "effectiveDate"];
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => i["value"] is not null))
        {
            foreach (string field in dateFields.Where(f => item["value"]![f] is not null))
            {
                string date = Text(item["value"], field);
                Assert.That(string.CompareOrdinal(date, snapshot[..date.Length]), Is.LessThanOrEqualTo(0), Text(item, "id") + " " + field);
            }
        }
    }

    [Test]
    public void Area_bankRate_isLabelledAsASampleNotTheActualRate()
    {
        JsonObject item = FixtureFiles.AreaItems().Single(i => Text(i, "topic") == "bank-rate");

        Assert.Multiple(() =>
        {
            Assert.That(Text(item, "label"), Does.Contain("sample value, not the actual Bank Rate"));
            Assert.That(Text(item, "doesNotEstablish"), Does.Contain("sample value, not the actual Bank Rate"));
        });
    }

    [Test]
    public void Area_r1_isSetOnStationRoadAndR2OnCanalStreet()
    {
        Assert.Multiple(() =>
        {
            Assert.That(ForHome("R1").Where(i => i["value"] is not null).SelectMany(i => i["value"]!.AsObject().Select(p => p.Value?.ToString() ?? string.Empty)), Has.None.Contain("Canal"));
            Assert.That(ForHome("R2").Where(i => i["value"] is not null).SelectMany(i => i["value"]!.AsObject().Select(p => p.Value?.ToString() ?? string.Empty)), Has.None.Contain("Station Road"));
        });
    }

    [Test]
    public void Area_crimeCategories_areUniqueWithinEachItem()
    {
        foreach (JsonObject item in FixtureFiles.AreaItems().Where(i => Text(i, "topic") == "crime" && i["value"] is not null))
        {
            Assert.That(item["value"]!["counts"]!.AsArray().Select(c => Text(c, "category")), Is.Unique, Text(item, "id"));
        }
    }

    [Test]
    public void Area_councilTax_isNotAreaData()
    {
        // Council tax is a user-entered cost input already (evidence file); it has no area topic.
        Assert.That(FixtureFiles.AreaItems().Select(i => Text(i, "topic")), Has.None.Contain("council"));
    }
}
