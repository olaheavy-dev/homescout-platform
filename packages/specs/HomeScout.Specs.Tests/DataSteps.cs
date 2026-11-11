using System.Diagnostics.CodeAnalysis;
using System.Text.Json;
using Reqnroll;

namespace HomeScout.Specs.Tests;

/// <summary>
/// The data steps: they check a specification's quoted IDs against the fixtures and the cost engine's generated file, so a
/// wrong or stale ID fails <c>make check</c>. Steps are matched by their wording (the Cucumber expressions below).
/// </summary>
[Binding]
[SuppressMessage("Microsoft.Performance", "CA1812", Justification = "Reqnroll creates binding classes by reflection.")]
internal sealed class DataSteps
{
    [Given("home {string} is at story step {int}")]
    public static void GivenHomeIsAtStoryStep(string homeId, int step)
    {
        Assert.That(SpecData.HomeIds, Does.Contain(homeId),
            $"Home \"{homeId}\" is not in packages/fixtures/data/homes.json.");
        Assert.That(SpecData.HasScenarioFromStep(homeId, step), Is.True,
            $"packages/fixtures/generated/costs.json has no scenario for home \"{homeId}\" from story step {step}.");
    }

    [Then("figure {string} exists")]
    public static void ThenFigureExists(string figureId) => _ = RequireFigure(figureId);

    [Then("figure {string} has status {string}")]
    public static void ThenFigureHasStatus(string figureId, string status)
    {
        var figure = RequireFigure(figureId);
        Assert.That(figure.TryGetProperty("status", out var actual) ? actual.GetString() : null, Is.EqualTo(status),
            $"Figure \"{figureId}\" has a different status in packages/fixtures/generated/costs.json.");
    }

    [Then("figure {string} shows no amount")]
    public static void ThenFigureShowsNoAmount(string figureId)
    {
        var figure = RequireFigure(figureId);
        Assert.That(figure.TryGetProperty("pence", out _), Is.False,
            $"Figure \"{figureId}\" has an amount, but this specification expects none (missing is never shown as zero).");
    }

    [Then("the total {string} is partial with reason {string}")]
    public static void ThenTotalIsPartialWithReason(string totalId, string category)
    {
        var total = RequireFigure(totalId);
        Assert.That(total.TryGetProperty("isPartial", out var isPartial) && isPartial.ValueKind == JsonValueKind.True, Is.True,
            $"Total \"{totalId}\" is not partial in packages/fixtures/generated/costs.json.");
        var categories = total.GetProperty("partialReasons").EnumerateArray()
            .Select(reason => reason.GetProperty("category").GetString())
            .ToList();
        Assert.That(categories, Does.Contain(category),
            $"Total \"{totalId}\" is partial, but not because of \"{category}\".");
    }

    [Then("evidence {string} exists")]
    public static void ThenEvidenceExists(string evidenceId) =>
        Assert.That(SpecData.EvidenceIds, Does.Contain(evidenceId),
            $"Evidence \"{evidenceId}\" is not in packages/fixtures/data/evidence.json.");

    private static JsonElement RequireFigure(string figureId)
    {
        if (!SpecData.TryGetFigure(figureId, out var figure))
        {
            Assert.Fail($"Figure \"{figureId}\" is not in packages/fixtures/generated/costs.json. "
                        + "Check the ID against that file; figures are cited by ID and never typed.");
        }

        return figure;
    }
}
