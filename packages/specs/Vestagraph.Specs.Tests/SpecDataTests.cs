namespace Vestagraph.Specs.Tests;

[TestFixture]
internal sealed class SpecDataTests
{
    [Test]
    public void TryGetFigure_knownFigureId_findsIt()
    {
        var found = SpecData.TryGetFigure("B1.from-step-1.monthly.total", out var figure);

        Assert.That(found, Is.True);
        Assert.That(figure.GetProperty("id").GetString(), Is.EqualTo("B1.from-step-1.monthly.total"));
    }

    [Test]
    public void TryGetFigure_unknownFigureId_doesNotFindIt()
    {
        Assert.That(SpecData.TryGetFigure("B1.from-step-1.monthly.no-such-line", out _), Is.False);
    }

    [Test]
    public void TryGetFigure_wrongCase_doesNotFindIt()
    {
        Assert.That(SpecData.TryGetFigure("b1.from-step-1.monthly.total", out _), Is.False);
    }

    [Test]
    public void EvidenceIds_knownEvidence_containsIt()
    {
        Assert.That(SpecData.EvidenceIds, Does.Contain("B1-STAMP-DUTY"));
    }

    [Test]
    public void HasScenarioFromStep_stepWithNoScenario_isFalse()
    {
        Assert.That(SpecData.HasScenarioFromStep("B1", 99), Is.False);
    }

    [Test]
    public void FigureIds_generatedFile_isNotEmpty()
    {
        Assert.That(SpecData.FigureIds, Is.Not.Empty);
    }

    [Test]
    public void HasScenarioFromStep_stepInsideAScenarioRange_isTrue()
    {
        Assert.That(SpecData.HasScenarioFromStep("B1", 1), Is.True);
        Assert.That(SpecData.HasScenarioFromStep("B1", 2), Is.True);
    }

    [Test]
    public void HomeIds_knownHome_containsItAndNotAnUnknownOne()
    {
        Assert.That(SpecData.HomeIds, Does.Contain("B1"));
        Assert.That(SpecData.HomeIds, Does.Not.Contain("NOPE"));
    }
}
