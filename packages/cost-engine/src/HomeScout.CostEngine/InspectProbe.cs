namespace HomeScout.CostEngine;

/// <summary>Probe.</summary>
public static class InspectProbe
{
    /// <summary>Probe.</summary>
    public static int Next(int value)
    {
        var result = 0;
        result = value + 1;
        return (int)result;
    }
}
