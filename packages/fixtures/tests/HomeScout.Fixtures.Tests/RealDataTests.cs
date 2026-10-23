using System.Text.Json;
using System.Text.Json.Nodes;
using HomeScout.Fixtures.Validator;

namespace HomeScout.Fixtures.Tests;

/// <summary>
/// The real data files must pass their schemas and match the approved sample data in
/// docs/planning/stage-2-plan.md section 1. Expected figures below are copied from that plan
/// (pounds converted to pence by hand), not read back from the data files.
/// </summary>
[TestFixture]
internal sealed class RealDataTests
{
    private static readonly string[] _expectedContextOnly = ["B1-EPC-COST", "B2-EPC-COST", "R1-EPC-COST"];

    [Test]
    public void AllFixtureFiles_validateAgainstTheirSchemas_withNoProblems()
    {
        IReadOnlyList<FixtureProblem> problems = FixtureValidator.ValidateFixtures(FixtureFiles.FixturesDirectory);

        Assert.That(problems, Is.Empty, string.Join(Environment.NewLine, problems));
    }

    [Test]
    public void ValidateFixtures_dataFileWithNoSchemaAvailable_isReported()
    {
        string folder = Path.Combine(Path.GetTempPath(), "homescout-fixtures-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(Path.Combine(folder, "data"));
        File.WriteAllText(Path.Combine(folder, "data", "mystery.json"), "{}");
        try
        {
            IReadOnlyList<FixtureProblem> problems = FixtureValidator.ValidateFixtures(folder);

            Assert.That(problems, Is.Not.Empty);
        }
        finally
        {
            Directory.Delete(folder, true);
        }
    }

    [Test]
    public void ValidateFixtures_nonStringSchemaField_isReportedReadably()
    {
        string folder = Path.Combine(Path.GetTempPath(), "homescout-fixtures-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(Path.Combine(folder, "test-cases"));
        File.WriteAllText(Path.Combine(folder, "test-cases", "bad.json"), "{ \"$schema\": 5 }");
        try
        {
            IReadOnlyList<FixtureProblem> problems = FixtureValidator.ValidateFixtures(folder);

            Assert.That(problems.Select(p => p.ToString()), Has.Some.Contain("Must be a string"));
        }
        finally
        {
            Directory.Delete(folder, true);
        }
    }

    [Test]
    public void SnapshotDate_inSnapshotFile_isTheApprovedDate()
    {
        string date = FixtureFiles.Load("snapshot")["snapshot"]!["snapshotDate"]!.GetValue<string>();

        Assert.That(date, Is.EqualTo("2026-10-23"));
    }

    [Test]
    public void Wales1_address_isWalesAndNotYetCovered()
    {
        JsonObject home = FixtureFiles.Home("WALES-1");

        Assert.Multiple(() =>
        {
            Assert.That(home["address"]!["nation"]!.GetValue<string>(), Is.EqualTo("Wales"));
            Assert.That(home["coverage"]!.GetValue<string>(), Is.EqualTo("not-yet-covered"));
        });
    }

    [Test]
    public void Home_inEveryRecord_hasANation()
    {
        JsonArray homes = FixtureFiles.Load("homes")["homes"]!.AsArray();

        Assert.That(homes, Has.Count.EqualTo(5));
        Assert.That(homes.Select(h => h!["address"]!["nation"]?.GetValue<string>()), Has.None.Null);
    }

    [Test]
    public void NorthbridgeHomes_postcodes_startWithNb()
    {
        JsonArray homes = FixtureFiles.Load("homes")["homes"]!.AsArray();
        string[] postcodes = homes
            .Where(h => h!["address"]!["town"]!.GetValue<string>() == "Northbridge")
            .Select(h => h!["address"]!["postcode"]!.GetValue<string>())
            .ToArray();

        Assert.That(postcodes, Has.Length.EqualTo(4));
        Assert.That(postcodes, Has.All.StartsWith("NB"));
    }

    [Test]
    public void B1_postcode_matchesSixCandidateUnits_andTheSelectedOneIsAmongThem()
    {
        JsonObject unit = FixtureFiles.Home("B1")["unit"]!.AsObject();
        JsonArray candidates = unit["candidateUnits"]!.AsArray();
        string selected = unit["selectedUnitId"]!.GetValue<string>();

        Assert.That(candidates, Has.Count.EqualTo(6));
        Assert.That(candidates.Select(c => c!["id"]!.GetValue<string>()), Does.Contain(selected));
        Assert.That(candidates.Select(c => c!["id"]!.GetValue<string>()), Is.Unique);
    }

    [TestCase("R2-ENERGY")]
    [TestCase("R2-WATER")]
    [TestCase("R2-BROADBAND")]
    public void R2_bills_areIncluded_notZero(string id)
    {
        JsonObject item = FixtureFiles.EvidenceItem(id);

        Assert.That(item["status"]!.GetValue<string>(), Is.EqualTo("included"));
        Assert.That(item.ContainsKey("value"), Is.False);
    }

    [TestCase("B1-INSURANCE")]
    public void B1_buildingsInsurance_isIncludedInTheServiceCharge_notZero(string id)
    {
        JsonObject item = FixtureFiles.EvidenceItem(id);

        Assert.That(item["status"]!.GetValue<string>(), Is.EqualTo("included"));
        Assert.That(item.ContainsKey("value"), Is.False);
    }

    [TestCase("B1-MAINTENANCE")]
    [TestCase("B1-STAMP-DUTY")]
    [TestCase("B1-LEGAL-FEES")]
    [TestCase("B2-STAMP-DUTY")]
    [TestCase("B2-LEGAL-FEES")]
    public void NotCalculatedItems_areNotCalculated_notZero(string id)
    {
        JsonObject item = FixtureFiles.EvidenceItem(id);

        Assert.That(item["status"]!.GetValue<string>(), Is.EqualTo("not-calculated"));
        Assert.That(item.ContainsKey("value"), Is.False);
    }

    [TestCase("B1-EPC-COST", 78000, "2019 prices")]
    [TestCase("B2-EPC-COST", 115000, "2021 prices")]
    [TestCase("R1-EPC-COST", 72000, "2022 prices")]
    public void EnergyCertificateCosts_areFlaggedContextOnly_atTheirOldPrices(string id, long pence, string priceBasis)
    {
        JsonObject item = FixtureFiles.EvidenceItem(id);

        Assert.Multiple(() =>
        {
            Assert.That(item["contextOnly"]!.GetValue<bool>(), Is.True);
            Assert.That(item["value"]!["pence"]!.GetValue<long>(), Is.EqualTo(pence));
            Assert.That(item["value"]!["period"]!.GetValue<string>(), Is.EqualTo("year"));
            Assert.That(item["priceBasis"]!.GetValue<string>(), Is.EqualTo(priceBasis));
        });
    }

    [Test]
    public void EvidenceItem_markedContextOnly_isAnEnergyCertificateCost()
    {
        JsonArray items = FixtureFiles.Load("evidence")["evidence"]!.AsArray();
        string[] contextOnly = items.Where(i => i!["contextOnly"]!.GetValue<bool>()).Select(i => i!["id"]!.GetValue<string>()).ToArray();

        Assert.That(contextOnly, Is.EquivalentTo(_expectedContextOnly));
    }

    [Test]
    public void R2_certificate_isExpired2025_issued2015_withCitedGovUkText()
    {
        JsonObject item = FixtureFiles.EvidenceItem("R2-EPC");
        JsonObject source = item["source"]!.AsObject();

        Assert.Multiple(() =>
        {
            Assert.That(item["status"]!.GetValue<string>(), Is.EqualTo("stale"));
            Assert.That(item["value"]!["issuedYear"]!.GetValue<int>(), Is.EqualTo(2015));
            Assert.That(item["value"]!["expiredYear"]!.GetValue<int>(), Is.EqualTo(2025));
            Assert.That(source["citationUrl"]!.GetValue<string>(), Is.EqualTo("https://www.gov.uk/buy-sell-your-home/energy-performance-certificates"));
            Assert.That(source["citedText"]!.GetValue<string>(), Does.Contain("renting out a property"));
        });
    }

    // Expected values from the plan, section 1. Pounds converted to pence by hand: pounds x 100.
    [TestCase("B1-PRICE", 19000000, "once")]
    [TestCase("B1-SC-LISTING", 240000, "year")]
    [TestCase("B1-SC-BUDGET", 372000, "year")]
    [TestCase("B1-GROUND-RENT", 25000, "year")]
    [TestCase("B1-CT-CHARGE", 210000, "year")]
    [TestCase("B1-ENERGY-ESTIMATE", 8500, "month")]
    [TestCase("B1-WATER-ESTIMATE", 4500, "month")]
    [TestCase("B1-BROADBAND-ESTIMATE", 3000, "month")]
    [TestCase("B2-PRICE", 25500000, "once")]
    [TestCase("B2-CT-CHARGE", 185000, "year")]
    [TestCase("B2-INSURANCE", 3500, "month")]
    [TestCase("B2-MAINTENANCE", 6000, "month")]
    [TestCase("B2-ENERGY-ESTIMATE", 12000, "month")]
    [TestCase("B2-WATER-ESTIMATE", 5000, "month")]
    [TestCase("B2-BROADBAND-ESTIMATE", 3000, "month")]
    [TestCase("R1-RENT", 120000, "month")]
    [TestCase("R1-CT-CHARGE", 160000, "year")]
    [TestCase("R1-DEPOSIT", 138000, "once")]
    [TestCase("R1-FIRST-MONTH-RENT", 120000, "once")]
    [TestCase("R1-ENERGY-ESTIMATE", 8000, "month")]
    [TestCase("R1-WATER-ESTIMATE", 4500, "month")]
    [TestCase("R1-BROADBAND-ESTIMATE", 3000, "month")]
    [TestCase("R2-RENT", 127500, "month")]
    [TestCase("R2-CT-CHARGE", 185000, "year")]
    [TestCase("R2-DEPOSIT", 147000, "once")]
    [TestCase("R2-FIRST-MONTH-RENT", 127500, "once")]
    [TestCase("HH-MORTGAGE-DEPOSIT", 3000000, "once")]
    [TestCase("HH-MOVING-COSTS", 120000, "once")]
    public void MoneyInput_approvedInPlan_matchesTheFile(string id, long pence, string period)
    {
        JsonObject value = FixtureFiles.EvidenceItem(id)["value"]!.AsObject();

        Assert.Multiple(() =>
        {
            Assert.That(value["pence"]!.GetValue<long>(), Is.EqualTo(pence));
            Assert.That(value["period"]!.GetValue<string>(), Is.EqualTo(period));
        });
    }

    [Test]
    public void MortgageAndBudgetInputs_approvedInPlan_matchTheFile()
    {
        JsonObject rate = FixtureFiles.EvidenceItem("HH-MORTGAGE-RATE")["value"]!.AsObject();
        JsonObject term = FixtureFiles.EvidenceItem("HH-MORTGAGE-TERM")["value"]!.AsObject();
        JsonObject budget = FixtureFiles.Load("household")["household"]!["monthlyBudget"]!.AsObject();

        Assert.Multiple(() =>
        {
            Assert.That(rate["basisPoints"]!.GetValue<int>(), Is.EqualTo(550), "5.5% is 550 basis points");
            Assert.That(term["amount"]!.GetValue<int>(), Is.EqualTo(25));
            Assert.That(budget["pence"]!.GetValue<long>(), Is.EqualTo(160000));
            Assert.That(budget["period"]!.GetValue<string>(), Is.EqualTo("month"));
        });
    }

    [Test]
    public void LeaseAndCouncilTaxBands_approvedInPlan_matchTheFile()
    {
        JsonObject lease = FixtureFiles.EvidenceItem("B1-LEASE-TERM")["value"]!.AsObject();

        Assert.Multiple(() =>
        {
            Assert.That(lease["years"]!.GetValue<int>(), Is.EqualTo(125));
            Assert.That(lease["startDate"]!.GetValue<string>(), Is.EqualTo("2015-01-01"));
            Assert.That(FixtureFiles.EvidenceItem("B1-CT-BAND")["value"]!["band"]!.GetValue<string>(), Is.EqualTo("C"));
            Assert.That(FixtureFiles.EvidenceItem("B2-CT-BAND")["value"]!["band"]!.GetValue<string>(), Is.EqualTo("B"));
            Assert.That(FixtureFiles.EvidenceItem("R1-CT-BAND")["value"]!["band"]!.GetValue<string>(), Is.EqualTo("A"));
            Assert.That(FixtureFiles.EvidenceItem("R2-CT-BAND")["value"]!["band"]!.GetValue<string>(), Is.EqualTo("B"));
        });
    }

    [Test]
    public void B1_serviceCharge_keepsTheListingFigureAndTheLaterBudget()
    {
        JsonObject listing = FixtureFiles.EvidenceItem("B1-SC-LISTING");
        JsonObject budget = FixtureFiles.EvidenceItem("B1-SC-BUDGET");

        Assert.Multiple(() =>
        {
            Assert.That(listing["source"]!["origin"]!.GetValue<string>(), Is.EqualTo("listing-claim"));
            Assert.That(budget["source"]!["origin"]!.GetValue<string>(), Is.EqualTo("document"));
            Assert.That(budget["supersedes"]!.GetValue<string>(), Is.EqualTo("B1-SC-LISTING"));
        });
    }

    [Test]
    public void Numbers_inEveryFixtureFile_areWholeNumbers()
    {
        string[] files = { "household", "homes", "evidence", "documents", "questions", "replies", "snapshot" };

        foreach (string file in files)
        {
            Assert.That(FractionalNumbers(FixtureFiles.Load(file)), Is.Empty, file + " must contain no fractional numbers");
        }

        foreach (string file in Directory.EnumerateFiles(Path.Combine(FixtureFiles.FixturesDirectory, "test-cases"), "*.json"))
        {
            Assert.That(FractionalNumbers(JsonNode.Parse(File.ReadAllText(file))), Is.Empty, file + " must contain no fractional numbers");
        }
    }

    [Test]
    public void Question_finalStatus_equalsItsLastTransition()
    {
        JsonArray questions = FixtureFiles.Load("questions")["questions"]!.AsArray();

        foreach (JsonNode? question in questions)
        {
            string last = question!["statusHistory"]!.AsArray().Last()!["status"]!.GetValue<string>();
            Assert.That(question["status"]!.GetValue<string>(), Is.EqualTo(last), question["id"]!.GetValue<string>());
        }
    }

    [Test]
    public void Question_statuses_matchTheStoriesInThePlan()
    {
        Assert.Multiple(() =>
        {
            Assert.That(FixtureFiles.Question("B1-Q-MAJOR-WORKS")["status"]!.GetValue<string>(), Is.EqualTo("waiting-for-reply"));
            Assert.That(FixtureFiles.Question("B1-Q-SERVICE-CHARGE")["statusHistory"]!.AsArray().Select(h => h!["status"]!.GetValue<string>()),
                Does.Contain("partially-answered"));
            Assert.That(FixtureFiles.Question("R1-Q-WATER")["statusHistory"]!.AsArray().Select(h => h!["status"]!.GetValue<string>()),
                Does.Contain("partially-answered"));
        });
    }

    [Test]
    public void Reference_inAnyRecord_pointsAtARecordThatExists()
    {
        HashSet<string> homeIds = Ids(FixtureFiles.Load("homes")["homes"]!);
        HashSet<string> evidenceIds = Ids(FixtureFiles.Load("evidence")["evidence"]!);
        HashSet<string> documentIds = Ids(FixtureFiles.Load("documents")["documents"]!);
        HashSet<string> questionIds = Ids(FixtureFiles.Load("questions")["questions"]!);
        HashSet<string> replyIds = Ids(FixtureFiles.Load("replies")["replies"]!);
        var missing = new List<string>();

        foreach (JsonNode? item in FixtureFiles.Load("evidence")["evidence"]!.AsArray())
        {
            string subjectId = item!["subjectId"]!.GetValue<string>();
            bool known = item["subjectType"]!.GetValue<string>() == "home" ? homeIds.Contains(subjectId) : subjectId == "RIVERS";
            Check(known, item["id"] + " subject " + subjectId);
            CheckOptional(item["supersedes"], evidenceIds, item["id"] + " supersedes");
            CheckOptional(item["source"]!["documentId"], documentIds, item["id"] + " source document");
        }

        foreach (JsonNode? doc in FixtureFiles.Load("documents")["documents"]!.AsArray())
        {
            Check(homeIds.Contains(doc!["homeId"]!.GetValue<string>()), doc["id"] + " home");
            foreach (JsonNode? id in doc["evidenceIds"]!.AsArray())
            {
                Check(evidenceIds.Contains(id!.GetValue<string>()), doc["id"] + " evidence " + id);
            }
        }

        foreach (JsonNode? question in FixtureFiles.Load("questions")["questions"]!.AsArray())
        {
            Check(homeIds.Contains(question!["homeId"]!.GetValue<string>()), question["id"] + " home");
            foreach (JsonNode? step in question["statusHistory"]!.AsArray())
            {
                CheckOptional(step!["replyId"], replyIds, question["id"] + " reply");
                CheckOptional(step["documentId"], documentIds, question["id"] + " document");
            }

            if (question["relatedEvidenceIds"] is JsonArray related)
            {
                foreach (JsonNode? id in related)
                {
                    Check(evidenceIds.Contains(id!.GetValue<string>()), question["id"] + " evidence " + id);
                }
            }
        }

        foreach (JsonNode? reply in FixtureFiles.Load("replies")["replies"]!.AsArray())
        {
            Check(questionIds.Contains(reply!["questionId"]!.GetValue<string>()), reply["id"] + " question");
            CheckOptional(reply["documentId"], documentIds, reply["id"] + " document");
        }

        Assert.That(missing, Is.Empty, string.Join("; ", missing));
        return;

        void Check(bool ok, string what)
        {
            if (!ok)
            {
                missing.Add(what);
            }
        }

        void CheckOptional(JsonNode? reference, HashSet<string> known, string what)
        {
            if (reference is not null)
            {
                Check(known.Contains(reference.GetValue<string>()), what + " " + reference);
            }
        }
    }

    private static HashSet<string> Ids(JsonNode array) =>
        array.AsArray().Select(n => n!["id"]!.GetValue<string>()).ToHashSet(StringComparer.Ordinal);

    private static List<string> FractionalNumbers(JsonNode? node)
    {
        var found = new List<string>();
        switch (node)
        {
            case JsonObject obj:
                foreach (KeyValuePair<string, JsonNode?> pair in obj)
                {
                    found.AddRange(FractionalNumbers(pair.Value));
                }

                break;
            case JsonArray array:
                foreach (JsonNode? child in array)
                {
                    found.AddRange(FractionalNumbers(child));
                }

                break;
            case JsonValue value when value.TryGetValue(out double number) && value.GetValueKind() == JsonValueKind.Number:
                if (value.ToJsonString().Contains('.', StringComparison.Ordinal) || value.ToJsonString().Contains('e', StringComparison.OrdinalIgnoreCase))
                {
                    found.Add(number.ToString(System.Globalization.CultureInfo.InvariantCulture));
                }

                break;
        }

        return found;
    }
}
