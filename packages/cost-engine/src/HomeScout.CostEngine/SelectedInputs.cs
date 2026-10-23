namespace HomeScout.CostEngine;

/// <summary>The inputs of a purchase's mortgage, with the evidence they came from.</summary>
/// <param name="AskingPrice">The asking price.</param>
/// <param name="Deposit">The deposit; the loan is the price minus the deposit.</param>
/// <param name="RateBasisPoints">The yearly rate in whole basis points.</param>
/// <param name="TermYears">The term in years.</param>
/// <param name="EvidenceIds">The ids of the price, deposit, rate and term evidence, in that order.</param>
public sealed record MortgageInputs(Pence AskingPrice, Pence Deposit, int RateBasisPoints, int TermYears, IReadOnlyList<string> EvidenceIds);

/// <summary>What the assumption selector chose for one home at one story step.</summary>
/// <param name="Mode">Buy or rent.</param>
/// <param name="Mortgage">The mortgage inputs (buying only).</param>
/// <param name="MonthlyLines">The monthly lines, except the mortgage repayment, which only the mortgage calculation can supply.</param>
/// <param name="UpfrontLines">The upfront lines.</param>
public sealed record SelectedInputs(
    Mode Mode,
    MortgageInputs? Mortgage,
    IReadOnlyList<LineInput> MonthlyLines,
    IReadOnlyList<LineInput> UpfrontLines)
{
    /// <summary>
    /// A text that is the same for two steps exactly when they use the same evidence in the same way. Consecutive steps with the
    /// same signature are merged into one scenario.
    /// </summary>
    internal string Signature()
    {
        IEnumerable<string> lines = MonthlyLines.Concat(UpfrontLines)
            .Select(line => $"{CostCategories.ToId(line.Category)}:{line.GetType().Name}:{string.Join(',', line.EvidenceIds)}");
        string mortgage = Mortgage is null ? "-" : string.Join(',', Mortgage.EvidenceIds);

        return $"{Mode}|{mortgage}|{string.Join(';', lines)}";
    }
}
