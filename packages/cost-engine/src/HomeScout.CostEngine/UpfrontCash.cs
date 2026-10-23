namespace HomeScout.CostEngine;

/// <summary>Adds up the cash needed up front for a home (decision 0021).</summary>
public static class UpfrontCash
{
    /// <summary>
    /// Works out the upfront cash. Every amount is paid once. A line with no amount (included, not calculated, conflicting or
    /// missing) adds nothing and is never treated as zero; stamp duty and legal fees are given as not calculated in this
    /// version, so a buyer's total is partial. The total is partial when any line is not calculated, conflicting or missing.
    /// </summary>
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

        List<PartialReason> reasons = CostLines.PartialReasons(resolved.Value);
        return Result.Success(new UpfrontBreakdown(resolved.Value, CostLines.Total(resolved.Value), reasons.Count > 0, reasons));
    }
}
