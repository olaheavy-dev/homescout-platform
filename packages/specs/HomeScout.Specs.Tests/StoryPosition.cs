namespace HomeScout.Specs.Tests;

/// <summary>
/// Where a scenario is in the story: the home and the calculated scenario (for example "from-step-1") that covers its story
/// step. Reqnroll creates one per scenario and hands it to the step classes (context injection), so it starts empty each time.
/// </summary>
internal sealed class StoryPosition
{
    public string? HomeId { get; private set; }

    public string? ScenarioId { get; private set; }

    public void Set(string homeId, string scenarioId)
    {
        HomeId = homeId;
        ScenarioId = scenarioId;
    }

    /// <summary>The prefix every figure ID cited at this position must start with, or null before a Given step has set one.</summary>
    public string? FigurePrefix => HomeId is null ? null : HomeId + "." + ScenarioId + ".";
}
