namespace HomeScout.CostEngine;

/// <summary>One line of a result. Only a calculated line has an amount.</summary>
/// <param name="Category">What the line is for.</param>
/// <param name="Status">Whether it has an amount, and if not, why.</param>
/// <param name="Amount">The whole-pence amount (per month for a monthly breakdown, once for an upfront one). Null unless calculated.</param>
/// <param name="SourcePeriod">The period the source stated. Null unless calculated.</param>
/// <param name="EvidenceIds">The evidence behind the line.</param>
public sealed record LineResult(CostCategory Category, LineStatus Status, Pence? Amount, Period? SourcePeriod, IReadOnlyList<string> EvidenceIds);

/// <summary>Why a total is partial: which line has no amount, and why. Codes, not prose.</summary>
public sealed record PartialReason(CostCategory Category, LineStatus Status);

/// <summary>The monthly cost of a home with its budget check.</summary>
/// <param name="Lines">The lines, in the engine's fixed order for the mode.</param>
/// <param name="Total">The sum of the calculated lines (each rounded once).</param>
/// <param name="IsPartial">True exactly when some line is not calculated, conflicting or missing.</param>
/// <param name="PartialReasons">One reason for each such line.</param>
/// <param name="Budget">The monthly budget.</param>
/// <param name="BudgetDifference">The budget minus the total: positive is headroom, negative is over budget.</param>
/// <param name="WithinBudget">True when the total is at or below the budget (exactly equal is within).</param>
/// <param name="BasedOnPartialTotal">True when the total is partial, so the real figure is higher ("at least").</param>
public sealed record MonthlyBreakdown(
    IReadOnlyList<LineResult> Lines,
    Pence Total,
    bool IsPartial,
    IReadOnlyList<PartialReason> PartialReasons,
    Pence Budget,
    Pence BudgetDifference,
    bool WithinBudget,
    bool BasedOnPartialTotal);

/// <summary>The cash needed up front for a home.</summary>
/// <param name="Lines">The lines, in the engine's fixed order for the mode.</param>
/// <param name="Total">The sum of the calculated lines.</param>
/// <param name="IsPartial">True exactly when some line is not calculated, conflicting or missing.</param>
/// <param name="PartialReasons">One reason for each such line.</param>
public sealed record UpfrontBreakdown(
    IReadOnlyList<LineResult> Lines,
    Pence Total,
    bool IsPartial,
    IReadOnlyList<PartialReason> PartialReasons);
