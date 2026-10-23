using System.Text.Json.Nodes;
using HomeScout.Fixtures.Validator;

namespace HomeScout.Fixtures.Tests;

/// <summary>
/// The output schema (generated-costs.schema.json) must refuse a wrong cost file, not only accept a right one
/// (stage 2 plan, task 4b section 1). The sample below only shows the shape of the file. Its figures are placeholders
/// for the schema to check; they are not cost-engine results and no test quotes them as expected values.
/// </summary>
[TestFixture]
internal sealed class GeneratedCostsSchemaTests
{
    private const string _schema = "generated-costs.schema.json";

    private const string _sample = """
        {
          "$schema": "../schema/generated-costs.schema.json",
          "formatVersion": 1,
          "generatedBy": "HomeScout.CostEngine.Generator",
          "snapshotDate": "2026-10-23",
          "money": "integer pence",
          "rounding": "Nearest penny, exact halves away from zero (decision 0021).",
          "homes": [
            {
              "homeId": "B1",
              "mode": "buy",
              "nation": "England",
              "coverage": "covered",
              "storyId": "BUYER",
              "scenarios": [
                {
                  "scenarioId": "from-step-1",
                  "fromStep": 1,
                  "toStep": 3,
                  "mortgage": {
                    "id": "B1.from-step-1.mortgage",
                    "loan": { "id": "B1.from-step-1.mortgage.loan", "pence": 100 },
                    "rateBasisPoints": 550,
                    "termYears": 25,
                    "payments": 300,
                    "monthlyRepayment": { "id": "B1.from-step-1.mortgage.repayment", "pence": 10 },
                    "evidenceIds": ["B1-PRICE", "HH-MORTGAGE-DEPOSIT"]
                  },
                  "monthly": {
                    "lines": [
                      {
                        "id": "B1.from-step-1.monthly.service-charge",
                        "category": "service-charge",
                        "status": "calculated",
                        "pence": 20,
                        "sourcePeriod": "year",
                        "evidenceIds": ["B1-SC-LISTING"]
                      },
                      {
                        "id": "B1.from-step-1.monthly.buildings-insurance",
                        "category": "buildings-insurance",
                        "status": "included",
                        "evidenceIds": ["B1-INSURANCE"]
                      },
                      {
                        "id": "B1.from-step-1.monthly.maintenance",
                        "category": "maintenance",
                        "status": "not-calculated",
                        "evidenceIds": ["B1-MAINTENANCE"]
                      },
                      {
                        "id": "B1.from-step-1.monthly.water",
                        "category": "water",
                        "status": "conflicting",
                        "evidenceIds": ["R1-WATER-LISTING", "R1-WATER-WSOT"]
                      },
                      {
                        "id": "B1.from-step-1.monthly.energy",
                        "category": "energy",
                        "status": "missing",
                        "evidenceIds": []
                      }
                    ],
                    "total": {
                      "id": "B1.from-step-1.monthly.total",
                      "pence": 20,
                      "isPartial": true,
                      "partialReasons": [
                        { "lineId": "B1.from-step-1.monthly.maintenance", "category": "maintenance", "status": "not-calculated" }
                      ]
                    },
                    "budget": {
                      "id": "B1.from-step-1.monthly.budget",
                      "budgetPence": 160000,
                      "budgetSource": "household:RIVERS.monthlyBudget",
                      "differencePence": 159980,
                      "withinBudget": true,
                      "basedOnPartialTotal": true
                    }
                  },
                  "upfront": {
                    "lines": [
                      {
                        "id": "B1.from-step-1.upfront.moving-costs",
                        "category": "moving-costs",
                        "status": "calculated",
                        "pence": 30,
                        "sourcePeriod": "once",
                        "evidenceIds": ["HH-MOVING-COSTS"]
                      }
                    ],
                    "total": {
                      "id": "B1.from-step-1.upfront.total",
                      "pence": 30,
                      "isPartial": false,
                      "partialReasons": []
                    }
                  },
                  "changesFromPrevious": []
                },
                {
                  "scenarioId": "from-step-4",
                  "fromStep": 4,
                  "toStep": 4,
                  "monthly": {
                    "lines": [
                      {
                        "id": "B1.from-step-4.monthly.service-charge",
                        "category": "service-charge",
                        "status": "calculated",
                        "pence": 31,
                        "sourcePeriod": "year",
                        "evidenceIds": ["B1-SC-BUDGET"]
                      }
                    ],
                    "total": {
                      "id": "B1.from-step-4.monthly.total",
                      "pence": 31,
                      "isPartial": false,
                      "partialReasons": []
                    },
                    "budget": {
                      "id": "B1.from-step-4.monthly.budget",
                      "budgetPence": 160000,
                      "budgetSource": "household:RIVERS.monthlyBudget",
                      "differencePence": 159969,
                      "withinBudget": true,
                      "basedOnPartialTotal": false
                    }
                  },
                  "upfront": {
                    "lines": [],
                    "total": {
                      "id": "B1.from-step-4.upfront.total",
                      "pence": 0,
                      "isPartial": false,
                      "partialReasons": []
                    }
                  },
                  "changesFromPrevious": [
                    {
                      "id": "B1.from-step-4.change.service-charge",
                      "category": "service-charge",
                      "kind": "value-changed",
                      "previousEvidenceIds": ["B1-SC-LISTING"],
                      "currentEvidenceIds": ["B1-SC-BUDGET"],
                      "monthlyDifferencePence": 11,
                      "annualDifferencePence": 132
                    }
                  ],
                  "monthlyTotalChange": { "id": "B1.from-step-4.change.monthly-total", "pence": 11 }
                }
              ]
            },
            {
              "homeId": "WALES-1",
              "nation": "Wales",
              "coverage": "not-yet-covered",
              "scenarios": []
            }
          ]
        }
        """;

    private static JsonObject Sample() => JsonNode.Parse(_sample)!.AsObject();

    private static JsonObject FirstScenario(JsonObject file) => file["homes"]![0]!["scenarios"]![0]!.AsObject();

    private static JsonObject FirstMonthlyLine(JsonObject file) => FirstScenario(file)["monthly"]!["lines"]![0]!.AsObject();

    private static List<string> Problems(JsonObject file) =>
        FixtureValidator.ValidateInstance(file, _schema, FixtureFiles.SchemaDirectory).Select(p => p.ToString()).ToList();

    [Test]
    public void GeneratedCosts_sampleShape_isAccepted() =>
        Assert.That(Problems(Sample()), Is.Empty);

    [Test]
    public void GeneratedCosts_calculatedLineWithoutPence_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file).Remove("pence");

        Assert.That(Problems(file), Has.Some.Contain("pence"));
    }

    [Test]
    public void GeneratedCosts_calculatedLineWithoutSourcePeriod_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file).Remove("sourcePeriod");

        Assert.That(Problems(file), Has.Some.Contain("sourcePeriod"));
    }

    [TestCase(1)]
    [TestCase(2)]
    [TestCase(3)]
    public void GeneratedCosts_nonCalculatedLineWithPence_isRejected(int lineIndex)
    {
        // Lines 1, 2, 3 are included, not-calculated and conflicting. None may carry an amount (rule 7).
        JsonObject file = Sample();
        JsonObject line = FirstScenario(file)["monthly"]!["lines"]![lineIndex]!.AsObject();
        line["pence"] = 0;

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/" + lineIndex + "/pence"));
    }

    [Test]
    public void GeneratedCosts_missingLineWithPence_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["lines"]![4]!["pence"] = 0;

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/4/pence"));
    }

    [Test]
    public void GeneratedCosts_includedLineWithNoEvidence_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["lines"]![1]!["evidenceIds"] = new JsonArray();

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/1/evidenceIds"));
    }

    [Test]
    public void GeneratedCosts_missingLineThatNamesEvidence_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["lines"]![4]!["evidenceIds"] = new JsonArray("B1-PRICE");

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/4/evidenceIds"));
    }

    [Test]
    public void GeneratedCosts_negativePenceOnACalculatedLine_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file)["pence"] = -1;

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/0/pence"));
    }

    [Test]
    public void GeneratedCosts_decimalPence_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file)["pence"] = JsonNode.Parse("20.5");

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/0/pence"));
    }

    [TestCase("b1.from-step-1.monthly.total")]
    [TestCase("B1.From-Step-1.monthly.total")]
    [TestCase("B1")]
    [TestCase("B1..monthly.total")]
    [TestCase("B1.from-step-1.monthly.total.")]
    [TestCase("B1.from_step_1.monthly.total")]
    [TestCase("B1.from-step-1.monthly total")]
    public void GeneratedCosts_badFigureId_isRejected(string id)
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["total"]!["id"] = id;

        Assert.That(Problems(file), Has.Some.Contain("/monthly/total/id"));
    }

    [Test]
    public void GeneratedCosts_notYetCoveredHomeWithScenarios_isRejected()
    {
        JsonObject file = Sample();
        JsonObject wales = file["homes"]![1]!.AsObject();
        wales["scenarios"] = FirstScenarioArrayClone(file);

        Assert.That(Problems(file), Has.Some.Contain("/homes/1/scenarios"));
    }

    [Test]
    public void GeneratedCosts_coveredHomeWithNoScenarios_isRejected()
    {
        JsonObject file = Sample();
        file["homes"]![0]!["scenarios"] = new JsonArray();

        Assert.That(Problems(file), Has.Some.Contain("/homes/0/scenarios"));
    }

    [Test]
    public void GeneratedCosts_walesMarkedCovered_isRejected()
    {
        JsonObject file = Sample();
        file["homes"]![1]!["coverage"] = "covered";

        Assert.That(Problems(file), Has.Some.Contain("/homes/1/coverage"));
    }

    [Test]
    public void GeneratedCosts_partialTotalWithNoReasons_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["total"]!["partialReasons"] = new JsonArray();

        Assert.That(Problems(file), Has.Some.Contain("/monthly/total/partialReasons"));
    }

    [Test]
    public void GeneratedCosts_completeTotalWithReasons_isRejected()
    {
        JsonObject file = Sample();
        JsonObject total = FirstScenario(file)["monthly"]!["total"]!.AsObject();
        total["isPartial"] = false;

        Assert.That(Problems(file), Has.Some.Contain("/monthly/total/partialReasons"));
    }

    [Test]
    public void GeneratedCosts_partialReasonForACalculatedLine_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["total"]!["partialReasons"]![0]!["status"] = "calculated";

        Assert.That(Problems(file), Has.Some.Contain("/partialReasons/0/status"));
    }

    [Test]
    public void GeneratedCosts_unknownKeyInALine_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file)["verified"] = true;

        Assert.That(Problems(file), Has.Some.Contain("verified"));
    }

    [Test]
    public void GeneratedCosts_unknownLineStatus_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file)["status"] = "verified";

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/0/status"));
    }

    [Test]
    public void GeneratedCosts_unknownCategory_isRejected()
    {
        JsonObject file = Sample();
        FirstMonthlyLine(file)["category"] = "service-charges";

        Assert.That(Problems(file), Has.Some.Contain("/monthly/lines/0/category"));
    }

    [Test]
    public void GeneratedCosts_wrongScenarioId_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["scenarioId"] = "step-1";

        Assert.That(Problems(file), Has.Some.Contain("/scenarioId"));
    }

    [Test]
    public void GeneratedCosts_wrongFormatVersion_isRejected()
    {
        JsonObject file = Sample();
        file["formatVersion"] = 2;

        Assert.That(Problems(file), Has.Some.Contain("/formatVersion"));
    }

    [Test]
    public void GeneratedCosts_missingSnapshotDate_isRejected()
    {
        JsonObject file = Sample();
        file.Remove("snapshotDate");

        Assert.That(Problems(file), Has.Some.Contain("snapshotDate"));
    }

    [Test]
    public void GeneratedCosts_budgetWithoutPartialFlag_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["monthly"]!["budget"]!.AsObject().Remove("basedOnPartialTotal");

        Assert.That(Problems(file), Has.Some.Contain("basedOnPartialTotal"));
    }

    [Test]
    public void GeneratedCosts_changeWithUnknownKind_isRejected()
    {
        JsonObject file = Sample();
        file["homes"]![0]!["scenarios"]![1]!["changesFromPrevious"]![0]!["kind"] = "cheaper";

        Assert.That(Problems(file), Has.Some.Contain("/changesFromPrevious/0/kind"));
    }

    [Test]
    public void GeneratedCosts_mortgageWithZeroRate_isRejected()
    {
        JsonObject file = Sample();
        FirstScenario(file)["mortgage"]!["rateBasisPoints"] = 0;

        Assert.That(Problems(file), Has.Some.Contain("/mortgage/rateBasisPoints"));
    }

    [Test]
    public void ValidateFixtures_invalidGeneratedFile_isReported()
    {
        using TempFixtures fixtures = TempFixtures.CopyOfRealFiles();
        JsonObject file = Sample();
        FirstMonthlyLine(file).Remove("pence");
        fixtures.WriteGenerated("costs.json", file.ToJsonString());

        IEnumerable<string> problems = FixtureValidator.ValidateFixtures(fixtures.Path).Select(p => p.ToString());

        Assert.That(problems, Has.Some.StartsWith("costs.json: /homes/0/scenarios/0/monthly/lines/0"));
    }

    [Test]
    public void ValidateFixtures_generatedFileWithNoSchemaLine_isReported()
    {
        using TempFixtures fixtures = TempFixtures.CopyOfRealFiles();
        JsonObject file = Sample();
        file.Remove("$schema");
        fixtures.WriteGenerated("costs.json", file.ToJsonString());

        IEnumerable<string> problems = FixtureValidator.ValidateFixtures(fixtures.Path).Select(p => p.ToString());

        Assert.That(problems, Has.Some.Contain("costs.json: /$schema"));
    }

    [Test]
    public void ValidateFixtures_validGeneratedFile_isAccepted()
    {
        using TempFixtures fixtures = TempFixtures.CopyOfRealFiles();
        fixtures.WriteGenerated("costs.json", Sample().ToJsonString());

        Assert.That(FixtureValidator.ValidateFixtures(fixtures.Path), Is.Empty);
    }

    [Test]
    public void ValidateFixtures_noGeneratedFolder_isAccepted()
    {
        // Until the generator exists (task 4b-2) the folder is absent or empty, and that is not an error.
        using TempFixtures fixtures = TempFixtures.CopyOfRealFiles();

        Assert.That(FixtureValidator.ValidateFixtures(fixtures.Path), Is.Empty);
    }

    private static JsonArray FirstScenarioArrayClone(JsonObject file) =>
        new(FirstScenario(file).DeepClone());

    /// <summary>A throwaway copy of the real fixtures folder, so a test can add a generated file without touching the repository.</summary>
    private sealed class TempFixtures : IDisposable
    {
        private TempFixtures(string path) => Path = path;

        public string Path { get; }

        public static TempFixtures CopyOfRealFiles()
        {
            string target = System.IO.Path.Combine(System.IO.Path.GetTempPath(), "homescout-fixtures-" + Guid.NewGuid().ToString("N"));
            foreach (string folder in new[] { "schema", "data", "test-cases" })
            {
                string source = System.IO.Path.Combine(FixtureFiles.FixturesDirectory, folder);
                Directory.CreateDirectory(System.IO.Path.Combine(target, folder));
                foreach (string file in Directory.EnumerateFiles(source, "*.json"))
                {
                    File.Copy(file, System.IO.Path.Combine(target, folder, System.IO.Path.GetFileName(file)));
                }
            }

            return new TempFixtures(target);
        }

        public void WriteGenerated(string name, string json)
        {
            string folder = System.IO.Path.Combine(Path, "generated");
            Directory.CreateDirectory(folder);
            File.WriteAllText(System.IO.Path.Combine(folder, name), json);
        }

        public void Dispose() => Directory.Delete(Path, recursive: true);
    }
}
