namespace HomeScout.CostEngine;

/// <summary>Adds up the cash needed up front for a home (decision 0021).</summary>
public static class UpfrontCash
{
    /// <summary>
    /// Works out the upfront cash. Every amount is paid once. A line with no amount (included, not calculated, conflicting or
    /// missing) adds nothing and is never treated as zero; stamp duty and legal fees are given as not calculated in this
    /// version, so a buyer's total is partial. The total is partial when any line is not calculated, conflicting or missing.
    /// </summary>
    /// <remarks>
    /// Buying requires a calculated mortgage deposit, otherwise this fails with <c>input.missing.mortgage-deposit</c>.
    /// Renting has no required upfront input, so an empty list gives a total of 0 that is not partial; callers that expect
    /// a deposit and first month's rent should pass them as lines (the selector passes missing ones as <see cref="MissingLine"/>).
    /// </remarks>
    /// <param name="mode">Whether the home is bought or rented.</param>
    /// <param name="lines">The lines. Lines that do not apply to the home are simply not given.</param>
    /// <exception cref="ArgumentNullException"><paramref name="lines"/> is null.</exception>
    /// <exception cref="ArgumentOutOfRangeException"><paramref name="mode"/> is not a defined mode.</exception>
    /// <exception cref="OverflowException">The total does not fit in a <see cref="long"/>.</exception>
    public static Result<UpfrontBreakdown> Calculate(Mode mode, IReadOnlyList<LineInput> lines)
    {
        ArgumentNullException.ThrowIfNull(lines);
        IReadOnlyList<CostCategory> order = CostLines.UpfrontOrder(mode);

        Result<List<LineResult>> resolved = CostLines.Resolve(lines, order, upfront: true);
        if (resolved.IsFailure)
        {
            return Result.Failure<UpfrontBreakdown>(resolved.Error);
        }

        // A buyer's deposit is a required input (register line BE-16), as the anchor line is for MonthlyCost.
        if (mode == Mode.Buy && resolved.Value.SingleOrDefault(l => l.Category == CostCategory.MortgageDeposit) is not { Status: LineStatus.Calculated })
        {
            return Result.Failure<UpfrontBreakdown>(new Error(
                "input.missing.mortgage-deposit",
                "The mortgage deposit amount is needed before upfront cash can be worked out.",
                ErrorCategory.Validation));
        }

        List<PartialReason> reasons = CostLines.PartialReasons(resolved.Value);
        return Result.Success(new UpfrontBreakdown(resolved.Value, CostLines.Total(resolved.Value), reasons.Count > 0, reasons));
    }
}
