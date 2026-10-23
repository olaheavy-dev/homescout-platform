namespace HomeScout.CostEngine;

/// <summary>What monthly and upfront calculations share: checking the lines, placing them in the fixed order, and finding partial reasons.</summary>
internal static class CostLines
{
    /// <summary>Which categories belong in a monthly breakdown, in the fixed order (plan 4b, section 1).</summary>
    internal static IReadOnlyList<CostCategory> MonthlyOrder(Mode mode) => mode switch
    {
        Mode.Buy =>
        [
            CostCategory.MortgageRepayment, CostCategory.ServiceCharge, CostCategory.GroundRent, CostCategory.CouncilTax,
            CostCategory.Energy, CostCategory.Water, CostCategory.Broadband, CostCategory.BuildingsInsurance, CostCategory.Maintenance,
        ],
        Mode.Rent =>
        [
            CostCategory.Rent, CostCategory.CouncilTax, CostCategory.Energy, CostCategory.Water, CostCategory.Broadband,
        ],
        _ => throw new ArgumentOutOfRangeException(nameof(mode), mode, "Unknown mode."),
    };

    /// <summary>Which categories belong in an upfront breakdown, in the fixed order.</summary>
    internal static IReadOnlyList<CostCategory> UpfrontOrder(Mode mode) => mode switch
    {
        Mode.Buy => [CostCategory.MortgageDeposit, CostCategory.MovingCosts, CostCategory.StampDuty, CostCategory.LegalFees],
        Mode.Rent => [CostCategory.Deposit, CostCategory.FirstMonthRent, CostCategory.MovingCosts],
        _ => throw new ArgumentOutOfRangeException(nameof(mode), mode, "Unknown mode."),
    };

    /// <summary>
    /// Checks each line and turns it into a result line, returned in <paramref name="order"/>. A yearly amount becomes monthly
    /// with <see cref="Pence.AnnualToMonthly"/>, rounded once. The first problem found, in input order, is the failure.
    /// </summary>
    /// <param name="lines">The lines to check.</param>
    /// <param name="order">The categories that belong here, in output order.</param>
    /// <param name="upfront">True for upfront lines, which are amounts paid once; false for monthly lines.</param>
    internal static Result<List<LineResult>> Resolve(IReadOnlyList<LineInput> lines, IReadOnlyList<CostCategory> order, bool upfront)
    {
        var resolved = new Dictionary<CostCategory, LineResult>();
        foreach (LineInput line in lines)
        {
            if (line is null)
            {
                throw new ArgumentException("A line in the list is null.", nameof(lines));
            }

            string name = CostCategories.ToId(line.Category);
            if (!order.Contains(line.Category))
            {
                return Fail($"input.not-for-mode.{name}", $"The {name} line does not belong in this list for this kind of home.", ErrorCategory.Validation);
            }

            if (resolved.ContainsKey(line.Category))
            {
                return Fail($"input.ambiguous.{name}", $"There is more than one {name} line.", ErrorCategory.Conflict);
            }

            Result<LineResult> result = Resolve(line, name, upfront);
            if (result.IsFailure)
            {
                return Result.Failure<List<LineResult>>(result.Error);
            }

            resolved[line.Category] = result.Value;
        }

        return Result.Success(order.Where(resolved.ContainsKey).Select(category => resolved[category]).ToList());
    }

    /// <summary>The reasons a total is partial: every line without an amount that is not simply included in another charge.</summary>
    internal static List<PartialReason> PartialReasons(IEnumerable<LineResult> lines) =>
        lines
            .Where(l => l.Status is LineStatus.NotCalculated or LineStatus.Conflicting or LineStatus.Missing)
            .Select(l => new PartialReason(l.Category, l.Status))
            .ToList();

    /// <summary>The sum of the calculated lines.</summary>
    /// <exception cref="OverflowException">The sum does not fit in a <see cref="long"/>.</exception>
    internal static Pence Total(IEnumerable<LineResult> lines) =>
        lines.Where(l => l.Amount is not null).Aggregate(Pence.Zero, (total, line) => total + line.Amount!.Value);

    private static Result<LineResult> Resolve(LineInput line, string name, bool upfront) => line switch
    {
        AmountLine amount => ResolveAmount(amount, name, upfront),
        IncludedLine => Result.Success(new LineResult(line.Category, LineStatus.Included, null, null, line.EvidenceIds)),
        NotCalculatedLine => Result.Success(new LineResult(line.Category, LineStatus.NotCalculated, null, null, line.EvidenceIds)),
        ConflictingLine => Result.Success(new LineResult(line.Category, LineStatus.Conflicting, null, null, line.EvidenceIds)),
        MissingLine => Result.Success(new LineResult(line.Category, LineStatus.Missing, null, null, line.EvidenceIds)),
        _ => throw new ArgumentException($"Unknown kind of line: {line.GetType().Name}.", nameof(line)),
    };

    private static Result<LineResult> ResolveAmount(AmountLine line, string name, bool upfront)
    {
        if (line.Amount.Value <= 0)
        {
            return FailLine($"input.not-positive.{name}", $"The {name} amount must be more than zero.", ErrorCategory.Validation);
        }

        // Rent and the mortgage payment are monthly figures; upfront amounts are paid once; other bills may be monthly or yearly.
        bool monthOnly = line.Category is CostCategory.Rent or CostCategory.MortgageRepayment;
        bool allowed = upfront
            ? line.Period == Period.Once
            : line.Period == Period.Month || (line.Period == Period.Year && !monthOnly);
        if (!allowed)
        {
            return FailLine($"input.wrong-period.{name}", $"The {name} amount is given for a period that cannot be used here.", ErrorCategory.Validation);
        }

        Pence amount = line.Period == Period.Year ? line.Amount.AnnualToMonthly() : line.Amount;
        return Result.Success(new LineResult(line.Category, LineStatus.Calculated, amount, line.Period, line.EvidenceIds));
    }

    private static Result<List<LineResult>> Fail(string code, string message, ErrorCategory category) =>
        Result.Failure<List<LineResult>>(new Error(code, message, category));

    private static Result<LineResult> FailLine(string code, string message, ErrorCategory category) =>
        Result.Failure<LineResult>(new Error(code, message, category));
}
