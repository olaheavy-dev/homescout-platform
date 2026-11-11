using System.Text.Json.Nodes;
using Vestagraph.Fixtures.Validator;

namespace Vestagraph.Fixtures.Tests;

/// <summary>
/// The area schema must refuse bad data (issue 120, test-first). Each test starts from a real area record,
/// breaks one thing, and expects the schema to complain about that thing.
/// </summary>
[TestFixture]
internal sealed class AreaSchemaRejectionTests
{
    private const string _school = "B1-AREA-SCHOOL-1";
    private const string _crime = "B1-AREA-CRIME-1";
    private const string _inspection = "B1-AREA-SCHOOL-INSPECTION-1";

    private static List<string> Problems(JsonObject item) =>
        FixtureFiles.Validate("area", "area", item).Select(p => p.ToString()).ToList();

    [TestCase(_school)]
    [TestCase(_crime)]
    [TestCase(_inspection)]
    [TestCase("UK-AREA-BANK-RATE-1")]
    [TestCase("B1-AREA-ENERGY-CERTIFICATE-1")]
    [TestCase("B1-AREA-COMMUTE-1")]
    public void Area_unchangedRealRecord_isAccepted(string id)
    {
        Assert.That(FixtureFiles.Validate("area", "area", FixtureFiles.AreaItem(id)), Is.Empty);
    }

    [Test]
    public void Area_itemWithNoSource_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item.Remove("source");

        Assert.That(Problems(item), Has.Some.Contain("source"));
    }

    [Test]
    public void Area_sourceWithNoSyntheticFlag_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["source"]!.AsObject().Remove("synthetic");

        Assert.That(Problems(item), Has.Some.Contain("synthetic"));
    }

    [Test]
    public void Area_sourceWithNoDate_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["source"]!.AsObject().Remove("date");

        Assert.That(Problems(item), Has.Some.Contain("date"));
    }

    [Test]
    public void Area_itemWithNoDoesNotEstablishText_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item.Remove("doesNotEstablish");

        Assert.That(Problems(item), Has.Some.Contain("doesNotEstablish"));
    }

    [Test]
    public void Area_itemWithNoCoverage_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item.Remove("coverage");

        Assert.That(Problems(item), Has.Some.Contain("coverage"));
    }

    [TestCase("rating")]
    [TestCase("score")]
    [TestCase("safetyLevel")]
    public void Area_crimeItemWithARatingField_isRejected(string field)
    {
        JsonObject item = FixtureFiles.AreaItem(_crime);
        item["value"]![field] = "low";

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_crimeCountOfZero_isRejected()
    {
        // A category with no recorded crimes is simply absent; a zero would read as "none happened" (rule 7).
        JsonObject item = FixtureFiles.AreaItem(_crime);
        item["value"]!["counts"]![0]!["count"] = 0;

        Assert.That(Problems(item), Has.Some.Contain("/value/counts/0/count"));
    }

    [Test]
    public void Area_crimeCategoryOutsideTheList_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_crime);
        item["value"]!["counts"]![0]!["category"] = "dangerous-area";

        Assert.That(Problems(item), Has.Some.Contain("/value/counts/0/category"));
    }

    [Test]
    public void Area_schoolInspectionWithNoFramework_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_inspection);
        item["value"]!.AsObject().Remove("framework");

        Assert.That(Problems(item), Has.Some.Contain("framework"));
    }

    [Test]
    public void Area_schoolInspectionWithNoInspectionDate_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_inspection);
        item["value"]!.AsObject().Remove("inspectionDate");

        Assert.That(Problems(item), Has.Some.Contain("inspectionDate"));
    }

    [Test]
    public void Area_schoolInspectionWithASingleOverallGrade_isRejected()
    {
        // Doc 02 section 7: no single overall grade; outcomes are listed per area under their framework.
        JsonObject item = FixtureFiles.AreaItem(_inspection);
        item["value"]!["overallGrade"] = "Good";

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_topicOutsideTheEnum_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["topic"] = "council-tax";

        Assert.That(Problems(item), Has.Some.Contain("/topic"));
    }

    [TestCase("none")]
    [TestCase("available")]
    [TestCase("zero")]
    public void Area_statusOutsideTheEnum_isRejected(string status)
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["status"] = status;

        Assert.That(Problems(item), Has.Some.Contain("/status"));
    }

    [Test]
    public void Area_notCoveredItemThatCarriesAValue_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["status"] = "not-covered";

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_recordedItemWithNoValue_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item.Remove("value");

        Assert.That(Problems(item), Has.Some.Contain("value"));
    }

    [Test]
    public void Area_distanceWithNoMethod_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["value"]!.AsObject().Remove("distanceMethod");

        Assert.That(Problems(item), Has.Some.Contain("distanceMethod"));
    }

    [Test]
    public void Area_distanceAsADecimal_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["value"]!["distanceMetres"] = JsonNode.Parse("450.5");

        Assert.That(Problems(item), Has.Some.Contain("/value/distanceMetres"));
    }

    [Test]
    public void Area_amenityWithNoSubtype_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-AMENITY-1");
        item.Remove("subtype");

        Assert.That(Problems(item), Has.Some.Contain("subtype"));
    }

    [Test]
    public void Area_amenitySubtypeOutsideTheList_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-AMENITY-1");
        item["subtype"] = "casino";

        Assert.That(Problems(item), Has.Some.Contain("/subtype"));
    }

    [Test]
    public void Area_subtypeOnATopicThatHasNone_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["subtype"] = "supermarket";

        Assert.That(Problems(item), Has.Some.Contain("/subtype"));
    }

    [Test]
    public void Area_idThatDoesNotFollowThePattern_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["id"] = "b1-school-1";

        Assert.That(Problems(item), Has.Some.Contain("/id"));
    }

    [Test]
    public void Area_homeItemWithNoHomeId_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item.Remove("homeId");

        Assert.That(Problems(item), Has.Some.Contain("homeId"));
    }

    [Test]
    public void Area_bankRateTiedToAHome_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("UK-AREA-BANK-RATE-1");
        item["homeId"] = "B1";

        Assert.That(Problems(item), Has.Some.Contain("homeId"));
    }

    [Test]
    public void Area_bankRateAsADecimal_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("UK-AREA-BANK-RATE-1");
        item["value"]!["basisPoints"] = JsonNode.Parse("400.5");

        Assert.That(Problems(item), Has.Some.Contain("/value/basisPoints"));
    }

    [Test]
    public void Area_floodItemThatHasNoFloodType_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B2-AREA-FLOOD-1");
        item.Remove("subtype");

        Assert.That(Problems(item), Has.Some.Contain("subtype"));
    }

    [Test]
    public void Area_linkThatIsNotHttps_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-FLOOD-1");
        item["link"]!["url"] = "http://example.invalid/flood";

        Assert.That(Problems(item), Has.Some.Contain("/link/url"));
    }

    [Test]
    public void Area_unknownExtraField_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["areaScore"] = 7;

        Assert.That(Problems(item), Has.Some.Contain("areaScore"));
    }

    [Test]
    public void ValidateFixtures_invalidAreaFile_isReportedAgainstTheAreaSchema()
    {
        string folder = Path.Combine(Path.GetTempPath(), "vestagraph-fixtures-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(Path.Combine(folder, "data"));
        Directory.CreateDirectory(Path.Combine(folder, "schema"));
        foreach (string schema in Directory.EnumerateFiles(FixtureFiles.SchemaDirectory))
        {
            File.Copy(schema, Path.Combine(folder, "schema", Path.GetFileName(schema)));
        }

        File.WriteAllText(Path.Combine(folder, "data", "area.json"), "{ \"area\": [ { \"id\": \"x\" } ] }");
        try
        {
            IReadOnlyList<FixtureProblem> problems = FixtureValidator.ValidateFixtures(folder);

            Assert.That(problems.Select(p => p.ToString()), Has.Some.Contain("area.json").And.Some.Contain("\"topic\""));
        }
        finally
        {
            Directory.Delete(folder, true);
        }
    }

    [TestCase("no-record-in-source")]
    [TestCase("source-failed")]
    [TestCase("not-covered")]
    public void Area_gapItemThatCarriesAValue_isRejected(string status)
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["status"] = status;

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_staleItemWithNoValue_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem(_school);
        item["status"] = "stale";
        item.Remove("value");

        Assert.That(Problems(item), Has.Some.Contain("value"));
    }

    [Test]
    public void Area_floodSubtypeOnAnAmenity_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-AMENITY-1");
        item["subtype"] = "rivers-and-sea";

        Assert.That(Problems(item), Has.Some.Contain("/subtype"));
    }

    [Test]
    public void Area_amenitySubtypeOnAFloodItem_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B2-AREA-FLOOD-1");
        item["subtype"] = "supermarket";

        Assert.That(Problems(item), Has.Some.Contain("/subtype"));
    }

    [Test]
    public void Area_liveFloodWarningOnSurfaceWater_isRejected()
    {
        // The Environment Agency issues no surface-water warnings; long-term surface-water risk is a link only.
        JsonObject item = FixtureFiles.AreaItem("B2-AREA-FLOOD-1");
        item["subtype"] = "surface-water";

        Assert.That(Problems(item), Has.Some.Contain("/subtype"));
    }

    [Test]
    public void Area_childcareAmenity_isAccepted()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-AMENITY-1");
        item["subtype"] = "childcare";

        Assert.That(Problems(item), Is.Empty);
    }

    [Test]
    public void Area_energyItemWithNoEvidenceLink_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-ENERGY-CERTIFICATE-1");
        item["value"]!.AsObject().Remove("evidenceItemIds");

        Assert.That(Problems(item), Has.Some.Contain("evidenceItemIds"));
    }

    [Test]
    public void Area_energyItemThatCopiesTheRating_isRejected()
    {
        // Inputs are recorded once (rule 2): the certificate lives in the evidence file, the area item points at it.
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-ENERGY-CERTIFICATE-1");
        item["value"]!["rating"] = "C";

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_energyItemThatCopiesTheIssuedYear_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-ENERGY-CERTIFICATE-1");
        item["value"]!["issuedYear"] = 2019;

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_energyItemWithAHandMadeCostRange_isRejected()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-ENERGY-CERTIFICATE-1");
        item["value"]!["estimatedAnnualCostRange"] = new JsonObject { ["lowPence"] = 1, ["highPence"] = 2 };

        Assert.That(Problems(item), Has.Some.Contain("/value"));
    }

    [Test]
    public void Area_crimeCountsThatAreExactDuplicates_areRejected()
    {
        // uniqueItems catches exact duplicates only; a repeated category with a different count is caught by
        // AreaDataTests.Area_crimeCategories_areUniqueWithinEachItem.
        JsonObject item = FixtureFiles.AreaItem(_crime);
        JsonNode first = item["value"]!["counts"]![0]!.DeepClone();
        item["value"]!["counts"]!.AsArray().Add(first);

        Assert.That(Problems(item), Has.Some.Contain("counts"));
    }

    [Test]
    public void Area_soldPriceOfAnOtherPropertyType_isAccepted()
    {
        JsonObject item = FixtureFiles.AreaItem("B1-AREA-SOLD-PRICE-1");
        item["value"]!["propertyType"] = "other";

        Assert.That(Problems(item), Is.Empty);
    }
}
