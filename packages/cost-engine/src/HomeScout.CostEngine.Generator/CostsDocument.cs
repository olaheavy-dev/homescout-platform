using System.Text.Json.Serialization;

namespace HomeScout.CostEngine.Generator;

// The records below are the shape of packages/fixtures/generated/costs.json. The order of the parameters of each record is
// the order of its keys in the file (the contract in schema/generated-costs.schema.json); a test checks the two agree.

/// <summary>The whole file.</summary>
internal sealed record CostsDocument(
    [property: JsonPropertyName("$schema")] string Schema,
    int FormatVersion,
    string GeneratedBy,
    string SnapshotDate,
    string Money,
    string Rounding,
    IReadOnlyList<HomeDocument> Homes);

internal sealed record HomeDocument(
    string HomeId,
    string? Mode,
    string Nation,
    string Coverage,
    string? StoryId,
    IReadOnlyList<ScenarioDocument> Scenarios);

internal sealed record ScenarioDocument(
    string ScenarioId,
    int FromStep,
    int ToStep,
    MortgageDocument? Mortgage,
    MonthlyDocument Monthly,
    UpfrontDocument Upfront,
    IReadOnlyList<ChangeDocument> ChangesFromPrevious,
    FigureDocument? MonthlyTotalChange);

internal sealed record FigureDocument(string Id, long Pence);

internal sealed record MortgageDocument(
    string Id,
    FigureDocument Loan,
    int RateBasisPoints,
    int TermYears,
    int Payments,
    FigureDocument MonthlyRepayment,
    IReadOnlyList<string> EvidenceIds);

internal sealed record MonthlyDocument(IReadOnlyList<LineDocument> Lines, TotalDocument Total, BudgetDocument Budget);

internal sealed record UpfrontDocument(IReadOnlyList<LineDocument> Lines, TotalDocument Total);

internal sealed record LineDocument(
    string Id,
    string Category,
    string Status,
    long? Pence,
    string? SourcePeriod,
    IReadOnlyList<string> EvidenceIds);

internal sealed record TotalDocument(string Id, long Pence, bool IsPartial, IReadOnlyList<PartialReasonDocument> PartialReasons);

internal sealed record PartialReasonDocument(string LineId, string Category, string Status);

internal sealed record BudgetDocument(
    string Id,
    long BudgetPence,
    string BudgetSource,
    long DifferencePence,
    bool WithinBudget,
    bool BasedOnPartialTotal);

internal sealed record ChangeDocument(
    string Id,
    string Category,
    string Kind,
    IReadOnlyList<string> PreviousEvidenceIds,
    IReadOnlyList<string> CurrentEvidenceIds,
    long? MonthlyDifferencePence,
    long? AnnualDifferencePence);
