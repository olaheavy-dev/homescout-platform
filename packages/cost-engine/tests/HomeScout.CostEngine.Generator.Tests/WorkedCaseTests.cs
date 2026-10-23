using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Generator.Tests;

/// <summary>
/// The generator, run on the real fixture data, against every independently worked case in
/// test-cases/story-calculations.json. Inputs and expected values come from that file. The only thing written here is
/// which home and scenario each case describes, because the cases name the home and the story step only in words.
/// </summary>
[TestFixture]
internal sealed class WorkedCaseTests
{
    private static readonly Dictionary<string, (string Home, string Scenario)> _monthlyCases = new(StringComparer.Ordinal)
    {
        ["b1-monthly-housing-cost-listing-service-charge"] = ("B1", "from-step-1"),
        ["b1-monthly-housing-cost-2026-budget"] = ("B1", "from-step-4"),
        ["b2-monthly-housing-cost"] = ("B2", "from-step-1"),
        ["r1-monthly-housing-cost-before-water"] = ("R1", "from-step-1"),
        ["r1-monthly-housing-cost-after-water"] = ("R1", "from-step-4"),
        ["r2-monthly-housing-cost"] = ("R2", "from-step-1"),
    };

    private static readonly string[] _upfrontCases = ["b1-upfront-cash", "b2-upfront-cash", "r1-upfront-cash", "r2-upfront-cash"];

    private static IEnumerable<TestCaseData> MonthlyCases() =>
        _monthlyCases.Keys.Select(id => new TestCaseData(id).SetArgDisplayNames(id));

    private static IEnumerable<TestCaseData> UpfrontCases() =>
        _upfrontCases.Select(id => new TestCaseData(id).SetArgDisplayNames(id));

    [TestCaseSource(nameof(MonthlyCases))]
    public void Generate_monthlyStoryCase_matchesWorkedResult(string caseId)
    {
        JsonNode expected = GeneratedFixture.Case(caseId)["expected"]!;
        (string home, string scenarioId) = _monthlyCases[caseId];
        JsonNode monthly = GeneratedFixture.Scenario(home, scenarioId)["monthly"]!;

        AssertLines(monthly["lines"]!.AsArray(), expected["lines"]!.AsArray(), "monthlyPence");
        Assert.That(monthly["total"]!["pence"]!.GetValue<long>(), Is.EqualTo(expected["totalMonthlyPence"]!.GetValue<long>()));
        Assert.That(monthly["total"]!["isPartial"]!.GetValue<bool>(), Is.EqualTo(expected["totalIsPartial"]!.GetValue<bool>()));
        AssertReasonCategories(monthly["total"]!["partialReasons"]!.AsArray(), expected["partialReasons"]!.AsArray());
        Assert.That(monthly["budget"]!["budgetPence"]!.GetValue<long>(), Is.EqualTo(expected["budgetPence"]!.GetValue<long>()));
        Assert.That(monthly["budget"]!["differencePence"]!.GetValue<long>(), Is.EqualTo(expected["budgetDifferencePence"]!.GetValue<long>()));
        Assert.That(monthly["budget"]!["withinBudget"]!.GetValue<bool>(), Is.EqualTo(expected["withinBudget"]!.GetValue<bool>()));
        Assert.That(monthly["budget"]!["basedOnPartialTotal"]!.GetValue<bool>(), Is.EqualTo(expected["totalIsPartial"]!.GetValue<bool>()));
    }

    [TestCaseSource(nameof(UpfrontCases))]
    public void Generate_upfrontStoryCase_matchesWorkedResultInEveryScenario(string caseId)
    {
        JsonNode storyCase = GeneratedFixture.Case(caseId);
        JsonNode expected = storyCase["expected"]!;
        string home = storyCase["inputs"]!["home"]!.GetValue<string>();

        JsonArray scenarios = HomeNode(home)["scenarios"]!.AsArray();

        Assert.That(scenarios, Is.Not.Empty);
        foreach (JsonNode? scenario in scenarios)
        {
            JsonNode upfront = scenario!["upfront"]!;
            AssertLines(upfront["lines"]!.AsArray(), expected["lines"]!.AsArray(), "amountPence");
            Assert.That(upfront["total"]!["pence"]!.GetValue<long>(), Is.EqualTo(expected["totalUpfrontPence"]!.GetValue<long>()));
            Assert.That(upfront["total"]!["isPartial"]!.GetValue<bool>(), Is.EqualTo(expected["totalIsPartial"]!.GetValue<bool>()));
            AssertReasonCategories(upfront["total"]!["partialReasons"]!.AsArray(), expected["partialReasons"]!.AsArray());
        }
    }

    [Test]
    public void Generate_mortgageStoryCases_matchTheWorkedRepayments()
    {
        foreach ((string home, string caseId) in new[] { ("B1", "b1-mortgage-repayment"), ("B2", "b2-mortgage-repayment") })
        {
            JsonNode expected = GeneratedFixture.Case(caseId)["expected"]!;
            JsonNode inputs = GeneratedFixture.Case(caseId)["inputs"]!;

            JsonNode mortgage = GeneratedFixture.Scenario(home, "from-step-1")["mortgage"]!;

            Assert.That(mortgage["monthlyRepayment"]!["pence"]!.GetValue<long>(), Is.EqualTo(expected["monthlyRepaymentPence"]!.GetValue<long>()));
            Assert.That(mortgage["loan"]!["pence"]!.GetValue<long>(), Is.EqualTo(inputs["askingPricePence"]!.GetValue<long>() - inputs["depositPence"]!.GetValue<long>()));
            Assert.That(mortgage["termYears"]!.GetValue<int>(), Is.EqualTo(inputs["termYears"]!.GetValue<int>()));
        }
    }

    [Test]
    public void Generate_budgetBeatCase_landsAsWorked()
    {
        JsonNode expected = GeneratedFixture.Case("b1-budget-beat")["expected"]!;
        JsonNode listing = GeneratedFixture.Scenario("B1", "from-step-1")["monthly"]!;
        JsonNode budget = GeneratedFixture.Scenario("B1", "from-step-4")["monthly"]!;

        Assert.That(listing["total"]!["pence"]!.GetValue<long>(), Is.EqualTo(expected["listingTotalPence"]!.GetValue<long>()));
        Assert.That(budget["total"]!["pence"]!.GetValue<long>(), Is.EqualTo(expected["budgetTotalPence"]!.GetValue<long>()));
        Assert.That(listing["budget"]!["withinBudget"]!.GetValue<bool>(), Is.EqualTo(expected["withinBudgetOnListing"]!.GetValue<bool>()));
        Assert.That(budget["budget"]!["withinBudget"]!.GetValue<bool>(), Is.EqualTo(!expected["overBudgetOn2026Budget"]!.GetValue<bool>()));
        Assert.That(listing["budget"]!["differencePence"]!.GetValue<long>(), Is.EqualTo(expected["listingBudgetDifferencePence"]!.GetValue<long>()));
        Assert.That(budget["budget"]!["differencePence"]!.GetValue<long>(), Is.EqualTo(expected["budgetBudgetDifferencePence"]!.GetValue<long>()));
    }

    [Test]
    public void Generate_serviceChargeDifferenceCase_matchesWorkedResult()
    {
        JsonNode expected = GeneratedFixture.Case("b1-service-charge-difference")["expected"]!;

        JsonNode change = GeneratedFixture.Scenario("B1", "from-step-4")["changesFromPrevious"]!.AsArray()
            .Single(c => c!["category"]!.GetValue<string>() == "service-charge")!;

        Assert.That(change["id"]!.GetValue<string>(), Is.EqualTo("B1.from-step-4.change.service-charge"));
        Assert.That(change["kind"]!.GetValue<string>(), Is.EqualTo("value-changed"));
        Assert.That(change["annualDifferencePence"]!.GetValue<long>(), Is.EqualTo(expected["annualDifferencePence"]!.GetValue<long>()));
        Assert.That(change["monthlyDifferencePence"]!.GetValue<long>(), Is.EqualTo(expected["monthlyDifferencePence"]!.GetValue<long>()));
        Assert.That(change["previousEvidenceIds"]!.AsArray().Select(i => i!.GetValue<string>()), Is.EqualTo(new List<string> { "B1-SC-LISTING" }));
        Assert.That(change["currentEvidenceIds"]!.AsArray().Select(i => i!.GetValue<string>()), Is.EqualTo(new List<string> { "B1-SC-BUDGET" }));
    }

    [Test]
    public void Generate_waterAtStepOne_isConflictingWithBothStatementsAsEvidence()
    {
        JsonNode water = GeneratedFixture.Scenario("R1", "from-step-1")["monthly"]!["lines"]!.AsArray()
            .Single(l => l!["category"]!.GetValue<string>() == "water")!;

        Assert.That(water["status"]!.GetValue<string>(), Is.EqualTo("conflicting"));
        Assert.That(water["pence"], Is.Null);
        Assert.That(water["evidenceIds"]!.AsArray().Select(i => i!.GetValue<string>()), Is.EqualTo(new List<string> { "R1-WATER-LISTING", "R1-WATER-WSOT" }));
    }

    [Test]
    public void Generate_waterAtStepFour_isNowCalculated()
    {
        JsonNode change = GeneratedFixture.Scenario("R1", "from-step-4")["changesFromPrevious"]!.AsArray()
            .Single(c => c!["category"]!.GetValue<string>() == "water")!;

        Assert.That(change["kind"]!.GetValue<string>(), Is.EqualTo("now-calculated"));
        Assert.That(change["id"]!.GetValue<string>(), Is.EqualTo("R1.from-step-4.change.water"));
    }

    [Test]
    public void Generate_rentedHomeWhoseBillsAreIncluded_showsThemAsIncludedNotZero()
    {
        JsonArray lines = GeneratedFixture.Scenario("R2", "from-step-1")["monthly"]!["lines"]!.AsArray();

        foreach (string category in new[] { "energy", "water", "broadband" })
        {
            JsonNode line = lines.Single(l => l!["category"]!.GetValue<string>() == category)!;
            Assert.That(line["status"]!.GetValue<string>(), Is.EqualTo("included"), category);
            Assert.That(line["pence"], Is.Null, category);
        }
    }

    [Test]
    public void Generate_energyCertificateCosts_neverEnterAnyLineOrTotal()
    {
        string json = GeneratedFixture.Json;

        Assert.That(json, Does.Not.Contain("EPC-COST"));
    }

    private static JsonNode HomeNode(string homeId) =>
        GeneratedFixture.Output["homes"]!.AsArray().Single(h => h!["homeId"]!.GetValue<string>() == homeId)!;

    /// <summary>Lines are compared by category: the case file's order is not the engine's fixed order. No extra or missing line is allowed.</summary>
    private static void AssertLines(JsonArray actual, JsonArray expected, string penceKey)
    {
        Assert.That(actual.Select(l => l!["category"]!.GetValue<string>()), Is.EquivalentTo(expected.Select(l => l!["category"]!.GetValue<string>())));

        foreach (JsonNode? wanted in expected)
        {
            string category = wanted!["category"]!.GetValue<string>();
            JsonNode line = actual.Single(l => l!["category"]!.GetValue<string>() == category)!;
            if (wanted[penceKey] is { } pence)
            {
                Assert.That(line["status"]!.GetValue<string>(), Is.EqualTo("calculated"), category);
                Assert.That(line["pence"]!.GetValue<long>(), Is.EqualTo(pence.GetValue<long>()), category);
            }
            else
            {
                Assert.That(line["status"]!.GetValue<string>(), Is.EqualTo(wanted["status"]!.GetValue<string>()), category);
                Assert.That(line["pence"], Is.Null, category);
            }
        }
    }

    /// <summary>The worked cases give reasons as prose that starts with the category ("maintenance: not calculated..."), so reasons are compared by category.</summary>
    private static void AssertReasonCategories(JsonArray actual, JsonArray expected)
    {
        IEnumerable<string> wanted = expected.Select(r => r!.GetValue<string>().Split(':')[0]);

        Assert.That(actual.Select(r => r!["category"]!.GetValue<string>()), Is.EquivalentTo(wanted));
    }
}
