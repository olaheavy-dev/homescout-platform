namespace HomeScout.CostEngine.Tests;

// FsCheck.NUnit supplies the test arguments, which the NUnit analyser cannot see (NUnit1027).
#pragma warning disable NUnit1027

/// <summary>
/// Property tests for the mortgage and monthly-cost calculations (decision 0027). Pence amounts are bounded to
/// 1..10^10 so that sums cannot overflow; overflow has its own unit tests.
/// </summary>
[TestFixture]
internal sealed class CalculationProperties
{
    private static readonly string[] _evidence = ["EVIDENCE-1"];

    [EngineProperty]
    public bool MonthlyRepayment_largerLoan_neverLowersTheRepayment(BoundedPence loan, BoundedPence extra, RateBasisPoints rate, TermYears term)
    {
        Pence smaller = Mortgage.MonthlyRepayment(loan.Pence, rate.Value, term.Value).Value.MonthlyRepayment;
        Pence larger = Mortgage.MonthlyRepayment(loan.Pence + extra.Pence, rate.Value, term.Value).Value.MonthlyRepayment;

        return larger >= smaller;
    }

    [EngineProperty]
    public bool MonthlyRepayment_higherRate_neverLowersTheRepayment(BoundedPence loan, RateBasisPoints rate, RateBasisPoints extra, TermYears term)
    {
        Pence lower = Mortgage.MonthlyRepayment(loan.Pence, rate.Value, term.Value).Value.MonthlyRepayment;
        Pence higher = Mortgage.MonthlyRepayment(loan.Pence, rate.Value + extra.Value, term.Value).Value.MonthlyRepayment;

        return higher >= lower;
    }

    [EngineProperty]
    public bool MonthlyRepayment_anyValidInput_isNeverNegative(BoundedPence loan, RateBasisPoints rate, TermYears term) =>
        Mortgage.MonthlyRepayment(loan.Pence, rate.Value, term.Value).Value.MonthlyRepayment >= Pence.Zero;

    [EngineProperty]
    public bool MonthlyCost_anyLines_totalEqualsTheSumOfTheCalculatedLines(MonthlyScenario scenario)
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(scenario.Mode, scenario.Lines, scenario.Budget).Value;
        // The expected sum is worked out from the input lines: monthly amounts as given, yearly amounts divided by 12 and rounded once.
        Pence sum = scenario.Lines.OfType<AmountLine>()
            .Aggregate(Pence.Zero, (total, line) => total + (line.Period == Period.Year ? Pence.RoundRatio(line.Amount.Value, 12) : line.Amount));

        return result.Total == sum;
    }

    [EngineProperty]
    public bool MonthlyCost_anyLines_isPartialExactlyWhenALineIsNotCalculatedConflictingOrMissing(MonthlyScenario scenario)
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(scenario.Mode, scenario.Lines, scenario.Budget).Value;
        bool someLineHasNoAmount = scenario.Lines.Any(l => l is NotCalculatedLine or ConflictingLine or MissingLine);

        return result.IsPartial == someLineHasNoAmount
            && result.PartialReasons.Count == scenario.Lines.Count(l => l is NotCalculatedLine or ConflictingLine or MissingLine);
    }

    [EngineProperty]
    public bool MonthlyCost_anyLines_noLineOrTotalIsNegative(MonthlyScenario scenario)
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(scenario.Mode, scenario.Lines, scenario.Budget).Value;

        return result.Total >= Pence.Zero && result.Lines.All(l => l.Amount is null || l.Amount.Value >= Pence.Zero);
    }

    [EngineProperty]
    public bool MonthlyCost_anyLines_aNonCalculatedLineNeverCarriesPence(MonthlyScenario scenario)
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(scenario.Mode, scenario.Lines, scenario.Budget).Value;

        return result.Lines.All(l => (l.Status == LineStatus.Calculated) == (l.Amount is not null));
    }

    [EngineProperty]
    public bool MonthlyCost_anyLines_budgetDifferenceIsBudgetMinusTotalAndWithinMeansAtOrBelow(MonthlyScenario scenario)
    {
        MonthlyBreakdown result = MonthlyCost.Calculate(scenario.Mode, scenario.Lines, scenario.Budget).Value;

        return result.BudgetDifference == scenario.Budget - result.Total && result.WithinBudget == (result.Total <= scenario.Budget);
    }

    [EngineProperty]
    public bool MonthlyCost_higherRent_neverLowersTheTotal(BoundedPence rent, BoundedPence extra, BoundedPence councilTax)
    {
        Pence lower = RentTotal(rent.Pence, councilTax.Pence);
        Pence higher = RentTotal(rent.Pence + extra.Pence, councilTax.Pence);

        return higher >= lower;
    }

    private static Pence RentTotal(Pence rent, Pence yearlyCouncilTax)
    {
        List<LineInput> lines =
        [
            new AmountLine(CostCategory.Rent, rent, Period.Month, _evidence),
            new AmountLine(CostCategory.CouncilTax, yearlyCouncilTax, Period.Year, _evidence),
        ];

        return MonthlyCost.Calculate(Mode.Rent, lines, new Pence(1)).Value.Total;
    }
}
