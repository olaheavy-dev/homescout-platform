namespace HomeScout.CostEngine.Tests;

// FsCheck.NUnit supplies the test arguments, which the NUnit analyser cannot see (NUnit1027).
#pragma warning disable NUnit1027

/// <summary>Property tests for UpfrontCash (decision 0027). Pence amounts are bounded to 1..10^10.</summary>
[TestFixture]
internal sealed class UpfrontCashProperties
{
    [EngineProperty]
    public bool UpfrontCash_anyLines_totalEqualsTheSumOfTheCalculatedLines(UpfrontScenario scenario)
    {
        UpfrontBreakdown result = UpfrontCash.Calculate(scenario.Mode, scenario.Lines).Value;
        Pence sum = scenario.Lines.OfType<AmountLine>().Aggregate(Pence.Zero, (total, line) => total + line.Amount);

        return result.Total == sum;
    }

    [EngineProperty]
    public bool UpfrontCash_anyLines_isPartialExactlyWhenALineIsNotCalculatedConflictingOrMissing(UpfrontScenario scenario)
    {
        UpfrontBreakdown result = UpfrontCash.Calculate(scenario.Mode, scenario.Lines).Value;
        int linesWithNoAmount = scenario.Lines.Count(l => l is NotCalculatedLine or ConflictingLine or MissingLine);

        return result.IsPartial == (linesWithNoAmount > 0) && result.PartialReasons.Count == linesWithNoAmount;
    }

    [EngineProperty]
    public bool UpfrontCash_anyLines_noLineOrTotalIsNegative(UpfrontScenario scenario)
    {
        UpfrontBreakdown result = UpfrontCash.Calculate(scenario.Mode, scenario.Lines).Value;

        return result.Total >= Pence.Zero && result.Lines.All(l => l.Amount is null || l.Amount.Value > Pence.Zero);
    }

    [EngineProperty]
    public bool UpfrontCash_anyLines_aNonCalculatedLineNeverCarriesPence(UpfrontScenario scenario)
    {
        UpfrontBreakdown result = UpfrontCash.Calculate(scenario.Mode, scenario.Lines).Value;

        return result.Lines.All(l => (l.Status == LineStatus.Calculated) == (l.Amount is not null));
    }
}
