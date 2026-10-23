namespace HomeScout.CostEngine;

/// <summary>The hyphenated names used in the fixture data, the worked cases, error codes and the generated files.</summary>
public static class CostCategories
{
    /// <summary>The name of a category, for example <c>service-charge</c>.</summary>
    /// <exception cref="ArgumentOutOfRangeException">The value is not a defined category.</exception>
    public static string ToId(CostCategory category) => category switch
    {
        CostCategory.MortgageRepayment => "mortgage-repayment",
        CostCategory.ServiceCharge => "service-charge",
        CostCategory.GroundRent => "ground-rent",
        CostCategory.CouncilTax => "council-tax",
        CostCategory.Energy => "energy",
        CostCategory.Water => "water",
        CostCategory.Broadband => "broadband",
        CostCategory.BuildingsInsurance => "buildings-insurance",
        CostCategory.Maintenance => "maintenance",
        CostCategory.Rent => "rent",
        CostCategory.MortgageDeposit => "mortgage-deposit",
        CostCategory.Deposit => "deposit",
        CostCategory.FirstMonthRent => "first-month-rent",
        CostCategory.MovingCosts => "moving-costs",
        CostCategory.StampDuty => "stamp-duty",
        CostCategory.LegalFees => "legal-fees",
        _ => throw new ArgumentOutOfRangeException(nameof(category), category, "Unknown cost category."),
    };

    /// <summary>The name of a line status, for example <c>not-calculated</c>.</summary>
    /// <exception cref="ArgumentOutOfRangeException">The value is not a defined status.</exception>
    public static string StatusId(LineStatus status) => status switch
    {
        LineStatus.Calculated => "calculated",
        LineStatus.Included => "included",
        LineStatus.NotCalculated => "not-calculated",
        LineStatus.Conflicting => "conflicting",
        LineStatus.Missing => "missing",
        _ => throw new ArgumentOutOfRangeException(nameof(status), status, "Unknown line status."),
    };
}
