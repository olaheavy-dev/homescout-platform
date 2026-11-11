using System.Diagnostics.CodeAnalysis;
using System.Text.Json;
using Reqnroll;

namespace Vestagraph.Specs.Tests;

/// <summary>
/// The data steps: they check a specification's quoted IDs against the fixtures and the cost engine's generated file, so a
/// wrong or stale ID fails <c>make check</c>. Steps are matched by their wording (the Cucumber expressions below).
/// </summary>
[Binding]
[SuppressMessage("Microsoft.Performance", "CA1812", Justification = "Reqnroll creates binding classes by reflection.")]
internal sealed class DataSteps(StoryPosition position)
{
    [Given("home {string} is at story step {int}")]
    public void GivenHomeIsAtStoryStep(string homeId, int step)
    {
        Assert.That(SpecData.HomeIds, Does.Contain(homeId),
            $"Home \"{homeId}\" is not in packages/fixtures/data/homes.json.");
        if (!SpecData.TryFindScenario(homeId, step, out var scenarioId))
        {
            Assert.Fail($"packages/fixtures/generated/costs.json has no scenario for home \"{homeId}\" at story step {step}.");
        }

        position.Set(homeId, scenarioId);
    }

    [Then("figure {string} exists")]
    public void ThenFigureExists(string figureId) => _ = RequireFigure(figureId);

    [Then("figure {string} has status {string}")]
    public void ThenFigureHasStatus(string figureId, string status)
    {
        var figure = RequireFigure(figureId);
        if (!figure.TryGetProperty("status", out var actual))
        {
            Assert.Fail($"Figure \"{figureId}\" has no status (it is a total, not a line).");
        }

        Assert.That(actual.GetString(), Is.EqualTo(status),
            $"Figure \"{figureId}\" has a different status in packages/fixtures/generated/costs.json.");
    }

    [Then("figure {string} shows no amount")]
    public void ThenFigureShowsNoAmount(string figureId)
    {
        var figure = RequireFigure(figureId);
        if (!figure.TryGetProperty("status", out _))
        {
            Assert.Fail($"Figure \"{figureId}\" is not a cost line (it has no status), so \"shows no amount\" does not apply to it.");
        }

        var amounts = figure.EnumerateObject()
            .Where(property => property.Name.EndsWith("pence", StringComparison.OrdinalIgnoreCase))
            .Select(property => property.Name)
            .ToList();
        Assert.That(amounts, Is.Empty,
            $"Figure \"{figureId}\" has an amount, but this specification expects none (missing is never shown as zero).");
    }

    [Then("figure {string} cites evidence {string}")]
    public void ThenFigureCitesEvidence(string figureId, string evidenceId)
    {
        var figure = RequireFigure(figureId);
        Assert.That(SpecData.EvidenceIds, Does.Contain(evidenceId),
            $"Evidence \"{evidenceId}\" is not in packages/fixtures/data/evidence.json.");
        var cited = figure.TryGetProperty("evidenceIds", out var ids)
            ? ids.EnumerateArray().Select(item => item.GetString()).ToList()
            : [];
        Assert.That(cited, Does.Contain(evidenceId),
            $"Figure \"{figureId}\" does not cite evidence \"{evidenceId}\" in packages/fixtures/generated/costs.json.");
    }

    [Then("the total {string} is partial with reason {string}")]
    public void ThenTotalIsPartialWithReason(string totalId, string category)
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

    private JsonElement RequireFigure(string figureId)
    {
        if (!SpecData.TryGetFigure(figureId, out var figure))
        {
            Assert.Fail($"Figure \"{figureId}\" is not in packages/fixtures/generated/costs.json. "
                        + "Check the ID against that file; figures are cited by ID and never typed.");
        }

        var prefix = position.FigurePrefix;
        if (prefix is not null && !figureId.StartsWith(prefix, StringComparison.Ordinal))
        {
            Assert.Fail($"Figure \"{figureId}\" does not belong to this scenario's story step: figures here start with \"{prefix}\".");
        }

        return figure;
    }
}
