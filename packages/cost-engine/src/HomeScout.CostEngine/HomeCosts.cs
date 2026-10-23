namespace HomeScout.CostEngine;

/// <summary>How a line changed from one scenario to the next.</summary>
public enum ChangeKind
{
    /// <summary>The line has a different amount, status or evidence.</summary>
    ValueChanged,

    /// <summary>The line had no amount before and has one now.</summary>
    NowCalculated,

    /// <summary>The line had an amount before and has none now.</summary>
    NoLongerCalculated,
}

/// <summary>One line that differs between a scenario and the one before it.</summary>
/// <param name="Category">What the line is for.</param>
/// <param name="Kind">How it changed.</param>
/// <param name="PreviousEvidenceIds">The evidence behind the line before.</param>
/// <param name="CurrentEvidenceIds">The evidence behind the line now.</param>
/// <param name="MonthlyDifference">Now minus before, both rounded monthly lines. Only for a monthly line that has an amount in both scenarios.</param>
/// <param name="AnnualDifference">Now minus before, both yearly amounts as the sources state them. Only when both are yearly.</param>
public sealed record CostChange(
    CostCategory Category,
    ChangeKind Kind,
    IReadOnlyList<string> PreviousEvidenceIds,
    IReadOnlyList<string> CurrentEvidenceIds,
    Pence? MonthlyDifference,
    Pence? AnnualDifference);

/// <summary>A worked-out mortgage with the evidence behind its inputs.</summary>
/// <param name="Repayment">The loan, rate, term and monthly repayment.</param>
/// <param name="EvidenceIds">The ids of the price, deposit, rate and term evidence.</param>
public sealed record MortgageSummary(MortgageRepayment Repayment, IReadOnlyList<string> EvidenceIds);

/// <summary>The costs of a home for the story steps from <paramref name="FromStep"/> to <paramref name="ToStep"/>, which all use the same evidence.</summary>
/// <param name="ScenarioId">Always <c>from-step-N</c>, where N is the first step.</param>
/// <param name="FromStep">The first story step.</param>
/// <param name="ToStep">The last story step that uses this evidence.</param>
/// <param name="Mortgage">The mortgage (buying only).</param>
/// <param name="Monthly">The monthly cost and budget check.</param>
/// <param name="Upfront">The upfront cash.</param>
/// <param name="Changes">What changed since the previous scenario. Empty for the first scenario.</param>
/// <param name="MonthlyTotalChange">This scenario's monthly total minus the previous one's. Null for the first scenario.</param>
public sealed record ScenarioCosts(
    string ScenarioId,
    int FromStep,
    int ToStep,
    MortgageSummary? Mortgage,
    MonthlyBreakdown Monthly,
    UpfrontBreakdown Upfront,
    IReadOnlyList<CostChange> Changes,
    Pence? MonthlyTotalChange);

/// <summary>The costs of one home, in the order of its scenarios.</summary>
/// <param name="HomeId">The home's id.</param>
/// <param name="Mode">Buy or rent.</param>
/// <param name="Nation">The nation the home is in.</param>
/// <param name="Scenarios">The scenarios, in step order.</param>
public sealed record HomeCosts(string HomeId, Mode Mode, Nation Nation, IReadOnlyList<ScenarioCosts> Scenarios);
