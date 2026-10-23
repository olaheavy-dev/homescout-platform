namespace HomeScout.CostEngine;

/// <summary>
/// One cost line given to the engine: an amount, or the reason there is no amount. Missing data is never an amount of
/// zero (AGENTS.md rule 7), so the lines without an amount have their own types.
/// </summary>
/// <param name="Category">What the line is for.</param>
/// <param name="EvidenceIds">The ids of the evidence items behind it, carried through to the result untouched.</param>
public abstract record LineInput(CostCategory Category, IReadOnlyList<string> EvidenceIds);

/// <summary>A line with an amount, in the period its source states.</summary>
public sealed record AmountLine(CostCategory Category, Pence Amount, Period Period, IReadOnlyList<string> EvidenceIds)
    : LineInput(Category, EvidenceIds);

/// <summary>A line covered by another charge. It adds nothing and does not make a total partial.</summary>
public sealed record IncludedLine(CostCategory Category, IReadOnlyList<string> EvidenceIds)
    : LineInput(Category, EvidenceIds);

/// <summary>A line this version does not work out. It adds nothing and makes the total partial.</summary>
public sealed record NotCalculatedLine(CostCategory Category, IReadOnlyList<string> EvidenceIds)
    : LineInput(Category, EvidenceIds);

/// <summary>A line whose sources disagree and is not settled. It adds nothing and makes the total partial.</summary>
public sealed record ConflictingLine(CostCategory Category, IReadOnlyList<string> EvidenceIds)
    : LineInput(Category, EvidenceIds);

/// <summary>A line with no evidence at all. It adds nothing and makes the total partial.</summary>
public sealed record MissingLine(CostCategory Category)
    : LineInput(Category, []);
