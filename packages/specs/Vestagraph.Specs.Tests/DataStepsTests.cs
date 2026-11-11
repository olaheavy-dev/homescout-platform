namespace Vestagraph.Specs.Tests;

[TestFixture]
internal sealed class DataStepsTests
{
    private const string _total = "B1.from-step-1.monthly.total";
    private const string _insurance = "B1.from-step-1.monthly.buildings-insurance";
    private const string _serviceCharge = "B1.from-step-1.monthly.service-charge";

    private readonly StoryPosition _position = new();
    private DataSteps _steps = null!;

    [SetUp]
    public void SetUp()
    {
        _position.Set("B1", "from-step-1");
        _steps = new DataSteps(_position);
    }

    [Test]
    public void ThenFigureExists_unknownFigure_failsNamingTheId()
    {
        var failure = Assert.Throws<AssertionException>(() => _steps.ThenFigureExists("B1.from-step-1.monthly.nope"));

        Assert.That(failure.Message, Does.Contain("B1.from-step-1.monthly.nope"));
    }

    [Test]
    public void ThenFigureExists_figureFromAnotherStep_fails()
    {
        var failure = Assert.Throws<AssertionException>(() => _steps.ThenFigureExists("B1.from-step-3.monthly.total"));

        Assert.That(failure.Message, Does.Contain("B1.from-step-1."));
    }

    [Test]
    public void ThenFigureHasStatus_wrongStatus_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.ThenFigureHasStatus(_insurance, "calculated"));
    }

    [Test]
    public void ThenFigureHasStatus_correctStatus_passes()
    {
        Assert.DoesNotThrow(() => _steps.ThenFigureHasStatus(_insurance, "missing"));
    }

    [Test]
    public void ThenFigureHasStatus_total_failsSayingItIsATotal()
    {
        var failure = Assert.Throws<AssertionException>(() => _steps.ThenFigureHasStatus(_total, "calculated"));

        Assert.That(failure.Message, Does.Contain("has no status (it is a total, not a line)"));
    }

    [Test]
    public void ThenFigureShowsNoAmount_lineWithPence_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.ThenFigureShowsNoAmount(_serviceCharge));
    }

    [Test]
    public void ThenFigureShowsNoAmount_lineWithoutAmount_passes()
    {
        Assert.DoesNotThrow(() => _steps.ThenFigureShowsNoAmount(_insurance));
    }

    [Test]
    public void ThenFigureShowsNoAmount_total_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.ThenFigureShowsNoAmount(_total));
    }

    [Test]
    public void ThenFigureShowsNoAmount_budgetWithBudgetPence_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.ThenFigureShowsNoAmount("B1.from-step-1.monthly.budget"));
    }

    [Test]
    public void ThenFigureCitesEvidence_evidenceNotCitedByFigure_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.ThenFigureCitesEvidence(_serviceCharge, "B1-STAMP-DUTY"));
    }

    [Test]
    public void ThenFigureCitesEvidence_unknownEvidence_fails()
    {
        var failure = Assert.Throws<AssertionException>(() => _steps.ThenFigureCitesEvidence(_serviceCharge, "NO-SUCH-EVIDENCE"));

        Assert.That(failure.Message, Does.Contain("NO-SUCH-EVIDENCE"));
    }

    [Test]
    public void ThenFigureCitesEvidence_citedEvidence_passes()
    {
        Assert.DoesNotThrow(() => _steps.ThenFigureCitesEvidence(_serviceCharge, "B1-SC-LISTING"));
    }

    [Test]
    public void ThenTotalIsPartialWithReason_reasonNotListed_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.ThenTotalIsPartialWithReason(_total, "council-tax"));
    }

    [Test]
    public void ThenTotalIsPartialWithReason_listedReason_passes()
    {
        Assert.DoesNotThrow(() => _steps.ThenTotalIsPartialWithReason(_total, "buildings-insurance"));
    }

    [Test]
    public void ThenTotalIsPartialWithReason_totalNotPartial_fails()
    {
        var notPartial = SpecData.FigureIds.First(id => id.EndsWith(".total", StringComparison.Ordinal)
                                                        && SpecData.TryGetFigure(id, out var f)
                                                        && f.TryGetProperty("isPartial", out var p)
                                                        && p.ValueKind == System.Text.Json.JsonValueKind.False);
        _position.Set(notPartial.Split('.')[0], notPartial.Split('.')[1]);

        Assert.Throws<AssertionException>(() => _steps.ThenTotalIsPartialWithReason(notPartial, "buildings-insurance"));
    }

    [Test]
    public void GivenHomeIsAtStoryStep_stepInsideRange_setsTheScenario()
    {
        _steps.GivenHomeIsAtStoryStep("B1", 2);

        Assert.That(_position.ScenarioId, Is.EqualTo("from-step-1"));
    }

    [TestCase(0)]
    [TestCase(5)]
    public void GivenHomeIsAtStoryStep_stepOutOfRange_fails(int step)
    {
        Assert.Throws<AssertionException>(() => _steps.GivenHomeIsAtStoryStep("B1", step));
    }

    [Test]
    public void GivenHomeIsAtStoryStep_unknownHome_fails()
    {
        Assert.Throws<AssertionException>(() => _steps.GivenHomeIsAtStoryStep("NOPE", 1));
    }
}
