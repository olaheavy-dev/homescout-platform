namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Small builders for the evidence the assumption selector reads. The amounts here are arbitrary inputs: the selector
/// tests check which item is chosen and which kind of line results, never a calculated figure.
/// </summary>
internal static class TestFacts
{
    public static EvidenceItem Money(
        string id,
        string category,
        long pence,
        Period period,
        EvidenceStatus status = EvidenceStatus.Available,
        int? usedFromStep = null,
        string? supersedes = null,
        bool contextOnly = false) =>
        new(id, category, status, new MoneyValue(new Pence(pence), period), contextOnly, usedFromStep, supersedes);

    public static EvidenceItem NoValue(string id, string category, EvidenceStatus status) =>
        new(id, category, status, null, false, null, null);

    public static EvidenceItem Other(string id, string category, EvidenceStatus status) =>
        new(id, category, status, new OtherValue(), false, null, null);

    public static EvidenceItem Rate(string id, int basisPoints) =>
        new(id, "mortgage-rate", EvidenceStatus.Available, new RateValue(basisPoints), false, null, null);

    public static EvidenceItem Years(string id, int years) =>
        new(id, "mortgage-term", EvidenceStatus.Available, new YearsValue(years), false, null, null);

    /// <summary>The four inputs a purchase needs before anything can be worked out.</summary>
    public static List<EvidenceItem> BuyAnchors() =>
    [
        Money("PRICE", "asking-price", 20_000_000, Period.Once),
        Money("DEPOSIT", "mortgage-deposit", 4_000_000, Period.Once),
        Rate("RATE", 500),
        Years("TERM", 20),
    ];

    public static HomeFacts Buying(IEnumerable<EvidenceItem> extra, Nation nation = Nation.England) =>
        new("T1", Mode.Buy, nation, [.. BuyAnchors(), .. extra], new Pence(200_000));

    public static HomeFacts Renting(IEnumerable<EvidenceItem> evidence, Nation nation = Nation.England) =>
        new("T2", Mode.Rent, nation, [.. evidence], new Pence(200_000));

    public static LineInput? MonthlyLine(SelectedInputs inputs, CostCategory category) =>
        inputs.MonthlyLines.SingleOrDefault(l => l.Category == category);

    public static LineInput? UpfrontLine(SelectedInputs inputs, CostCategory category) =>
        inputs.UpfrontLines.SingleOrDefault(l => l.Category == category);
}
