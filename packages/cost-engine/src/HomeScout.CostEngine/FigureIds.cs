namespace HomeScout.CostEngine;

/// <summary>
/// The id of every figure in the generated file: <c>{homeId}.{scenarioId}.{section}.{name}</c>, for example
/// <c>B1.from-step-4.monthly.service-charge</c>. Screens and documents quote a figure by this id.
/// </summary>
public static class FigureIds
{
    /// <summary>The id of a line in a section (<c>monthly</c> or <c>upfront</c>).</summary>
    public static string Line(string homeId, string scenarioId, string section, CostCategory category) =>
        Make(homeId, scenarioId, section, CostCategories.ToId(category));

    /// <summary>The id of a section's total.</summary>
    public static string Total(string homeId, string scenarioId, string section) =>
        Make(homeId, scenarioId, section, "total");

    /// <summary>The id of the monthly budget check.</summary>
    public static string Budget(string homeId, string scenarioId) =>
        Make(homeId, scenarioId, "monthly", "budget");

    /// <summary>The id of the mortgage as a whole.</summary>
    public static string Mortgage(string homeId, string scenarioId) =>
        $"{homeId}.{scenarioId}.mortgage";

    /// <summary>The id of the amount borrowed.</summary>
    public static string MortgageLoan(string homeId, string scenarioId) =>
        Make(homeId, scenarioId, "mortgage", "loan");

    /// <summary>The id of the monthly repayment.</summary>
    public static string MonthlyRepayment(string homeId, string scenarioId) =>
        Make(homeId, scenarioId, "mortgage", "monthly-repayment");

    /// <summary>The id of a change to one line since the previous scenario.</summary>
    public static string Change(string homeId, string scenarioId, CostCategory category) =>
        Make(homeId, scenarioId, "change", CostCategories.ToId(category));

    /// <summary>The id of the change to the monthly total since the previous scenario.</summary>
    public static string MonthlyTotalChange(string homeId, string scenarioId) =>
        Make(homeId, scenarioId, "change", "monthly-total");

    private static string Make(string homeId, string scenarioId, string section, string name) =>
        $"{homeId}.{scenarioId}.{section}.{name}";
}
