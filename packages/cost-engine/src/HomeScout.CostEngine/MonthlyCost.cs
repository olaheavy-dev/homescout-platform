namespace HomeScout.CostEngine;

/// <summary>Adds up the monthly cost of a home and checks it against the monthly budget (decision 0021).</summary>
public static class MonthlyCost
{
    /// <summary>
    /// Works out the monthly cost. Each yearly amount is divided by 12 and rounded once; a monthly amount is used as given;
    /// the total is the sum of the rounded lines. A line with no amount (included, not calculated, conflicting or missing)
    /// adds nothing and is never treated as zero. The total is partial when any line is not calculated, conflicting or missing.
    /// </summary>
    /// <remarks>
    /// The budget check: the difference is the budget minus the total, and a total exactly equal to the budget is within
    /// it (founder, 23 Oct 2026). On a partial total only the calculated lines are counted, so
    /// <see cref="MonthlyBreakdown.BasedOnPartialTotal"/> tells the screen to say "at least".
    /// The anchor line (the mortgage repayment when buying, the rent when renting) must have an amount.
    /// </remarks>
    /// <param name="mode">Whether the home is bought or rented.</param>
    /// <param name="lines">The lines. Lines that do not apply to the home are simply not given.</param>
    /// <param name="budget">The monthly budget, more than zero.</param>
    /// <exception cref="ArgumentNullException"><paramref name="lines"/> is null.</exception>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="mode"/> is not a defined mode.</exception>
    /// <exception cref="OverflowException">A total does not fit in a <see cref="long"/>.</exception>
    public static Result<MonthlyBreakdown> Calculate(Mode mode, IReadOnlyList<LineInput> lines, Pence budget)
    {
        ArgumentNullException.ThrowIfNull(lines);
        IReadOnlyList<CostCategory> order = CostLines.MonthlyOrder(mode);

        if (budget.Value <= 0)
        {
            return Fail("input.not-positive.budget", "The monthly budget must be more than zero.", ErrorCategory.Validation);
        }

        Result<List<LineResult>> resolved = CostLines.Resolve(lines, order, upfront: false);
        if (resolved.IsFailure)
        {
            return Result.Failure<MonthlyBreakdown>(resolved.Error);
        }

        CostCategory anchor = order[0];
        LineResult? anchorLine = resolved.Value.SingleOrDefault(l => l.Category == anchor);
        if (anchorLine is not { Status: LineStatus.Calculated })
        {
            string name = CostCategories.ToId(anchor);
            return Fail($"input.missing.{name}", $"The {name} amount is needed before a monthly cost can be worked out.", ErrorCategory.Validation);
        }

        List<PartialReason> reasons = CostLines.PartialReasons(resolved.Value);
        Pence total = CostLines.Total(resolved.Value);
        bool isPartial = reasons.Count > 0;

        return Result.Success(new MonthlyBreakdown(
            resolved.Value,
            total,
            isPartial,
            reasons,
            budget,
            budget - total,
            total <= budget,
            isPartial));
    }

    private static Result<MonthlyBreakdown> Fail(string code, string message, ErrorCategory category) =>
        Result.Failure<MonthlyBreakdown>(new Error(code, message, category));
}
