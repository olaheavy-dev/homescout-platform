using System.Text.Json.Nodes;

namespace HomeScout.Fixtures.Tests;

/// <summary>
/// The schemas must refuse bad data, not only accept good data (stage 2 plan, task 2).
/// Each test starts from a real record, breaks one thing, and expects the schema to complain.
/// </summary>
[TestFixture]
internal sealed class SchemaRejectionTests
{
    [Test]
    public void Evidence_unchangedRealRecord_isAccepted()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-SC-LISTING");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item), Is.Empty);
    }

    [Test]
    public void Evidence_valueWithNoSource_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-SC-LISTING");
        item.Remove("source");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("source"));
    }

    [Test]
    public void Evidence_sourceWithNoOrigin_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-SC-LISTING");
        item["source"]!.AsObject().Remove("origin");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("origin"));
    }

    [Test]
    public void Evidence_moneyWithDecimals_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-SC-LISTING");
        item["value"]!["pence"] = JsonNode.Parse("240000.5");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value/pence"));
    }

    [Test]
    public void Evidence_moneyAsAPoundsString_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-SC-LISTING");
        item["value"]!["pence"] = "2400.00";

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value/pence"));
    }

    [Test]
    public void Evidence_rateAsADecimal_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("HH-MORTGAGE-RATE");
        item["value"]!["basisPoints"] = JsonNode.Parse("550.5");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value/basisPoints"));
    }

    [Test]
    public void Evidence_billRecordedAsZeroInsteadOfIncluded_isRejected()
    {
        // R2's water is covered by the rent. Recording it as 0 pence a month is the mistake rule 7 forbids.
        JsonObject item = FixtureFiles.EvidenceItem("R2-WATER");
        item["status"] = "available";
        item["value"] = new JsonObject { ["kind"] = "money", ["pence"] = 0, ["period"] = "month" };

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value/pence"));
    }

    [Test]
    public void Evidence_includedBillThatAlsoHasAValue_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("R2-WATER");
        item["value"] = new JsonObject { ["kind"] = "money", ["pence"] = 4500, ["period"] = "month" };

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value"));
    }

    [Test]
    public void Evidence_notCalculatedItemRecordedAsZero_isRejected()
    {
        // Stamp duty is not calculated in this version. Recording 0 pence would look like "no stamp duty".
        JsonObject item = FixtureFiles.EvidenceItem("B1-STAMP-DUTY");
        item["status"] = "available";
        item["value"] = new JsonObject { ["kind"] = "money", ["pence"] = 0, ["period"] = "once" };

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value/pence"));
    }

    [Test]
    public void Evidence_notCalculatedItemThatAlsoHasAValue_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-LEGAL-FEES");
        item["value"] = new JsonObject { ["kind"] = "money", ["pence"] = 150000, ["period"] = "once" };

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/value"));
    }

    [Test]
    public void Evidence_availableItemWithNoValue_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-PRICE");
        item.Remove("value");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("value"));
    }

    [Test]
    public void Evidence_certificateCostNotMarkedContextOnly_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-EPC-COST");
        item["contextOnly"] = false;

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/contextOnly"));
    }

    [Test]
    public void Evidence_unknownStatus_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-PRICE");
        item["status"] = "verified";

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("/status"));
    }

    [Test]
    public void Evidence_sourceWithNoSyntheticFlag_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("B1-CT-CHARGE");
        item["source"]!.AsObject().Remove("synthetic");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("synthetic"));
    }

    [Test]
    public void Evidence_citedTextWithoutCitationUrl_isRejected()
    {
        JsonObject item = FixtureFiles.EvidenceItem("R2-EPC");
        item["source"]!.AsObject().Remove("citationUrl");

        Assert.That(FixtureFiles.Validate("evidence", "evidence", item).Select(p => p.ToString()), Has.Some.Contain("citationUrl"));
    }

    [Test]
    public void Home_addressWithNoNation_isRejected()
    {
        JsonObject home = FixtureFiles.Home("B2");
        home["address"]!.AsObject().Remove("nation");

        Assert.That(FixtureFiles.Validate("homes", "homes", home).Select(p => p.ToString()), Has.Some.Contain("nation"));
    }

    [Test]
    public void Home_walesMarkedAsCovered_isRejected()
    {
        JsonObject home = FixtureFiles.Home("WALES-1");
        home["coverage"] = "covered";

        Assert.That(FixtureFiles.Validate("homes", "homes", home).Select(p => p.ToString()), Has.Some.Contain("/coverage"));
    }

    [Test]
    public void Home_englandMarkedAsNotCovered_isRejected()
    {
        JsonObject home = FixtureFiles.Home("B2");
        home["coverage"] = "not-yet-covered";

        Assert.That(FixtureFiles.Validate("homes", "homes", home).Select(p => p.ToString()), Has.Some.Contain("/coverage"));
    }

    [Test]
    public void Home_candidateUnitsWithNoSelectedUnit_isRejected()
    {
        JsonObject home = FixtureFiles.Home("B1");
        home["unit"]!.AsObject().Remove("selectedUnitId");

        Assert.That(FixtureFiles.Validate("homes", "homes", home).Select(p => p.ToString()), Has.Some.Contain("selectedUnitId"));
    }

    [TestCase("to-ask")]
    [TestCase("waiting-for-reply")]
    [TestCase("reply-needs-checking")]
    [TestCase("answer-recorded")]
    [TestCase("partially-answered")]
    [TestCase("needs-professional-review")]
    [TestCase("closed-by-user-without-answer")]
    [TestCase("reopened")]
    public void Question_eachStatusFromDoc02_isAccepted(string status)
    {
        JsonObject question = FixtureFiles.Question("B1-Q-MAJOR-WORKS");
        question["status"] = status;

        Assert.That(FixtureFiles.Validate("questions", "questions", question), Is.Empty);
    }

    [Test]
    public void Question_resolvedStatusThatIsNotInDoc02_isRejected()
    {
        JsonObject question = FixtureFiles.Question("B1-Q-MAJOR-WORKS");
        question["status"] = "resolved";

        Assert.That(FixtureFiles.Validate("questions", "questions", question).Select(p => p.ToString()), Has.Some.Contain("/status"));
    }

    [Test]
    public void Question_transitionWithNoReason_isRejected()
    {
        JsonObject question = FixtureFiles.Question("B1-Q-MAJOR-WORKS");
        question["statusHistory"]![0]!.AsObject().Remove("reason");

        Assert.That(FixtureFiles.Validate("questions", "questions", question).Select(p => p.ToString()), Has.Some.Contain("reason"));
    }
}
