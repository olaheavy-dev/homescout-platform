namespace HomeScout.CostEngine;

/// <summary>The UK nation a home is in. The engine covers England only; the field is kept so other nations can be added (AGENTS.md rule 6).</summary>
public enum Nation
{
    /// <summary>England.</summary>
    England,

    /// <summary>Wales.</summary>
    Wales,

    /// <summary>Scotland.</summary>
    Scotland,

    /// <summary>Northern Ireland.</summary>
    NorthernIreland,
}

/// <summary>What the fixture data says about an evidence item, as at the snapshot (after the stories have finished).</summary>
public enum EvidenceStatus
{
    /// <summary>A usable value.</summary>
    Available,

    /// <summary>No value is known.</summary>
    Missing,

    /// <summary>Sources disagree.</summary>
    Conflicting,

    /// <summary>The value is out of date.</summary>
    Stale,

    /// <summary>The cost does not exist for this home (for example a service charge on a freehold house).</summary>
    NotApplicable,

    /// <summary>This version of the product does not work it out.</summary>
    NotCalculated,

    /// <summary>Covered by another charge.</summary>
    Included,
}

/// <summary>A value recorded in evidence. Only money, rates and years matter to the engine; everything else is <see cref="OtherValue"/>.</summary>
public abstract record EvidenceValue;

/// <summary>An amount of money in whole pence, with the period its source states.</summary>
public sealed record MoneyValue(Pence Amount, Period Period) : EvidenceValue;

/// <summary>A yearly rate in whole basis points (550 is 5.5%).</summary>
public sealed record RateValue(int BasisPoints) : EvidenceValue;

/// <summary>A length of time in whole years.</summary>
public sealed record YearsValue(int Years) : EvidenceValue;

/// <summary>A value of another kind (text, a band, a certificate, a lease term). The engine never reads it as a cost.</summary>
public sealed record OtherValue : EvidenceValue;

/// <summary>One item of evidence, as the fixture data records it.</summary>
/// <param name="Id">The evidence id, carried through to the result.</param>
/// <param name="Category">The evidence category, for example <c>service-charge</c> or <c>water-responsibility</c>.</param>
/// <param name="Status">The status as at the snapshot.</param>
/// <param name="Value">The value, or null when the status has none.</param>
/// <param name="ContextOnly">True when the item is shown for context and never enters a total.</param>
/// <param name="UsedFromStep">The first story step from which the item is used, or null when it is used from the start.</param>
/// <param name="Supersedes">The id of an item this one replaces once it is in use, or null.</param>
public sealed record EvidenceItem(
    string Id,
    string Category,
    EvidenceStatus Status,
    EvidenceValue? Value,
    bool ContextOnly,
    int? UsedFromStep,
    string? Supersedes);

/// <summary>Everything the engine needs to know about one home.</summary>
/// <param name="HomeId">The home's id.</param>
/// <param name="Mode">Buy or rent, or null when the data does not say.</param>
/// <param name="Nation">The nation the home is in.</param>
/// <param name="Evidence">The home's own evidence plus the household's (deposit, rate, term, moving costs).</param>
/// <param name="MonthlyBudget">The household's monthly budget.</param>
public sealed record HomeFacts(string HomeId, Mode? Mode, Nation Nation, IReadOnlyList<EvidenceItem> Evidence, Pence MonthlyBudget);
