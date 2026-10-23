namespace HomeScout.CostEngine;

/// <summary>
/// Chooses, for one home at one story step, which evidence each cost line uses. The engine works on the chosen lines only,
/// so this is where "which figure counts" is decided and written down.
/// </summary>
public static class AssumptionSelector
{
    private const string _waterResponsibility = "water-responsibility";

    /// <summary>
    /// Chooses the inputs for a home at a story step (steps start at 1).
    /// </summary>
    /// <remarks>
    /// The selection rules:
    /// <list type="number">
    /// <item><description>Rule 1: context-only items are ignored, so a value shown for context (for example the cost on an energy certificate) never enters a total.</description></item>
    /// <item><description>Rule 2: an item is in use at step s when its <see cref="EvidenceItem.UsedFromStep"/> is null or at most s, and no item that has started by step s names it in <see cref="EvidenceItem.Supersedes"/>.</description></item>
    /// <item><description>Rule 3: for each category the first match in this order is used: a value of the wrong kind fails the selection (<c>input.wrong-kind</c>, checked before ambiguity, for ordinary lines and anchors alike); a money item with a value gives an amount, whatever its status in the snapshot (the snapshot is taken after the story ends); otherwise a conflicting item (including the rule 4 group) gives a conflicting line, so nothing can hide a disagreement; then a not-calculated item gives a not-calculated line, and an included item an included line (not-calculated wins, as the more cautious); then a not-applicable item leaves the line out; and no evidence at all gives a missing line.</description></item>
    /// <item><description>Rule 4: <c>water-responsibility</c> items count towards the water line, for the conflicting check only. This is the only link between categories, and a narrow stand-in until the data has a proper "who pays" field.</description></item>
    /// <item><description>Rule 5: two in-use money items for one category cannot both be used, so the selection fails.</description></item>
    /// </list>
    /// An anchor input that has no usable value stops the whole selection: the asking price, the mortgage deposit, rate and term when buying, and the rent when renting (founder, 23 Oct 2026).
    /// <para>
    /// Error codes (tests match the code, never the message):
    /// <c>home.not-covered</c> (the home is not in England), <c>home.mode-missing</c> (neither buy nor rent),
    /// <c>story.step-out-of-range</c> (the step is below 1),
    /// <c>input.missing.{category}</c> (an anchor input has no value), <c>input.ambiguous.{category}</c> (rule 5),
    /// <c>input.wrong-period.{category}</c> (the price or deposit is not once, or the rent is not monthly),
    /// <c>input.not-positive.{category}</c> (an anchor amount is zero or less),
    /// <c>input.wrong-kind.{category}</c> (a value of the wrong kind, for example a rate given as money).
    /// </para>
    /// </remarks>
    /// <param name="facts">The home and its evidence.</param>
    /// <param name="storyStep">The story step, 1 or more.</param>
    /// <exception cref="ArgumentNullException"><paramref name="facts"/> is null.</exception>
    public static Result<SelectedInputs> Select(HomeFacts facts, int storyStep)
    {
        ArgumentNullException.ThrowIfNull(facts);
        ArgumentNullException.ThrowIfNull(facts.Evidence);

        Error? homeError = CheckHome(facts);
        if (homeError is not null)
        {
            return Result.Failure<SelectedInputs>(homeError);
        }

        Mode mode = facts.Mode!.Value;

        if (storyStep < 1)
        {
            return Fail("story.step-out-of-range", "A story step starts at 1.", ErrorCategory.Validation);
        }

        List<EvidenceItem> inUse = InUse(facts.Evidence, storyStep);

        MortgageInputs? mortgage = null;
        if (mode == Mode.Buy)
        {
            Result<MortgageInputs> found = BuyerInputs(inUse);
            if (found.IsFailure)
            {
                return Result.Failure<SelectedInputs>(found.Error);
            }

            mortgage = found.Value;
        }

        var monthly = new List<LineInput>();
        foreach (CostCategory category in CostLines.MonthlyOrder(mode).Where(c => c != CostCategory.MortgageRepayment))
        {
            Error? error = ChooseLine(inUse, category, mortgage, out LineInput? line);
            if (error is not null)
            {
                return Result.Failure<SelectedInputs>(error);
            }

            if (line is not null)
            {
                monthly.Add(line);
            }
        }

        var upfront = new List<LineInput>();
        foreach (CostCategory category in CostLines.UpfrontOrder(mode))
        {
            Error? error = ChooseLine(inUse, category, mortgage, out LineInput? line);
            if (error is not null)
            {
                return Result.Failure<SelectedInputs>(error);
            }

            if (line is not null)
            {
                upfront.Add(line);
            }
        }

        return Result.Success(new SelectedInputs(mode, mortgage, monthly, upfront));
    }

    /// <summary>Checks that the home is one the engine covers: in England, and either for sale or to rent.</summary>
    internal static Error? CheckHome(HomeFacts facts)
    {
        if (facts.Nation != Nation.England)
        {
            return new Error("home.not-covered", $"Home {facts.HomeId} is not in England, which is the only nation covered so far.", ErrorCategory.Validation);
        }

        if (facts.Mode is null)
        {
            return new Error("home.mode-missing", $"Home {facts.HomeId} is neither for sale nor to rent in the data.", ErrorCategory.Validation);
        }

        return null;
    }

    /// <summary>Rules 1 and 2: the items that count at this step.</summary>
    private static List<EvidenceItem> InUse(IReadOnlyList<EvidenceItem> evidence, int step)
    {
        List<EvidenceItem> started = evidence
            .Where(e => !e.ContextOnly && (e.UsedFromStep is null || e.UsedFromStep <= step))
            .ToList();
        HashSet<string> replaced = started.Where(e => e.Supersedes is not null).Select(e => e.Supersedes!).ToHashSet(StringComparer.Ordinal);

        return started.Where(e => !replaced.Contains(e.Id)).ToList();
    }

    private static Result<MortgageInputs> BuyerInputs(List<EvidenceItem> inUse)
    {
        Result<EvidenceItem> price = MoneyAnchor(inUse, "asking-price", Period.Once);
        if (price.IsFailure)
        {
            return Result.Failure<MortgageInputs>(price.Error);
        }

        Result<EvidenceItem> deposit = MoneyAnchor(inUse, "mortgage-deposit", Period.Once);
        if (deposit.IsFailure)
        {
            return Result.Failure<MortgageInputs>(deposit.Error);
        }

        Result<EvidenceItem> rate = Anchor(inUse, "mortgage-rate", v => v is RateValue);
        if (rate.IsFailure)
        {
            return Result.Failure<MortgageInputs>(rate.Error);
        }

        if (rate.Value.Value is not RateValue rateValue)
        {
            return Result.Failure<MortgageInputs>(WrongKind("mortgage-rate"));
        }

        Result<EvidenceItem> term = Anchor(inUse, "mortgage-term", v => v is YearsValue);
        if (term.IsFailure)
        {
            return Result.Failure<MortgageInputs>(term.Error);
        }

        if (term.Value.Value is not YearsValue termValue)
        {
            return Result.Failure<MortgageInputs>(WrongKind("mortgage-term"));
        }

        return Result.Success(new MortgageInputs(
            ((MoneyValue)price.Value.Value!).Amount,
            ((MoneyValue)deposit.Value.Value!).Amount,
            rateValue.BasisPoints,
            termValue.Years,
            [price.Value.Id, deposit.Value.Id, rate.Value.Id, term.Value.Id]));
    }

    /// <summary>
    /// Finds the one item with a value for an anchor input. Items with no value (missing, for example) do not count, so an
    /// anchor with none of them is missing, and an anchor with two is ambiguous (rule 5).
    /// </summary>
    private static Result<EvidenceItem> Anchor(List<EvidenceItem> inUse, string category, Func<EvidenceValue, bool> isExpectedKind)
    {
        List<EvidenceItem> valued = inUse.Where(e => e.Category == category && e.Value is not null).ToList();

        // Wrong kind is reported before ambiguity, as it is for ordinary lines.
        if (valued.Any(e => !isExpectedKind(e.Value!)))
        {
            return Result.Failure<EvidenceItem>(WrongKind(category));
        }

        return valued.Count switch
        {
            0 => Result.Failure<EvidenceItem>(new Error($"input.missing.{category}", $"The {category} value is needed before a cost can be worked out.", ErrorCategory.Validation)),
            1 => Result.Success(valued[0]),
            _ => Result.Failure<EvidenceItem>(Ambiguous(category)),
        };
    }

    /// <summary>An anchor input that must be a positive amount of money paid in a given period.</summary>
    private static Result<EvidenceItem> MoneyAnchor(List<EvidenceItem> inUse, string category, Period period)
    {
        Result<EvidenceItem> found = Anchor(inUse, category, v => v is MoneyValue);
        if (found.IsFailure)
        {
            return found;
        }

        if (found.Value.Value is not MoneyValue money)
        {
            return Result.Failure<EvidenceItem>(WrongKind(category));
        }

        if (money.Period != period)
        {
            return Result.Failure<EvidenceItem>(new Error($"input.wrong-period.{category}", $"The {category} amount must be given as {PeriodWords(period)}.", ErrorCategory.Validation));
        }

        if (money.Amount.Value <= 0)
        {
            return Result.Failure<EvidenceItem>(new Error($"input.not-positive.{category}", $"The {category} amount must be more than zero.", ErrorCategory.Validation));
        }

        return found;
    }

    /// <summary>Rule 3 for one category, with the anchor lines (rent, and the mortgage deposit) checked first. A null line means the line is left out.</summary>
    private static Error? ChooseLine(List<EvidenceItem> inUse, CostCategory category, MortgageInputs? mortgage, out LineInput? line)
    {
        line = null;

        if (category == CostCategory.MortgageDeposit && mortgage is not null)
        {
            // The deposit was already checked as an anchor input; its id is the second one.
            line = new AmountLine(category, mortgage.Deposit, Period.Once, [mortgage.EvidenceIds[1]]);
            return null;
        }

        if (category == CostCategory.Rent)
        {
            Result<EvidenceItem> rent = MoneyAnchor(inUse, "rent", Period.Month);
            if (rent.IsFailure)
            {
                return rent.Error;
            }

            line = new AmountLine(category, ((MoneyValue)rent.Value.Value!).Amount, Period.Month, [rent.Value.Id]);
            return null;
        }

        string name = CostCategories.ToId(category);
        List<EvidenceItem> items = inUse.Where(e => e.Category == name).ToList();
        List<EvidenceItem> valued = items.Where(e => e.Value is not null).ToList();

        if (valued.Any(e => e.Value is not MoneyValue))
        {
            return WrongKind(name);
        }

        if (valued.Count > 1)
        {
            return Ambiguous(name);
        }

        if (valued.Count == 1)
        {
            var money = (MoneyValue)valued[0].Value!;
            line = new AmountLine(category, money.Amount, money.Period, [valued[0].Id]);
            return null;
        }

        // Rule 4: for water, the "who pays" items join the conflicting check. Conflicting comes before the statuses that have
        // no value, so an "included" or "not applicable" item cannot hide a disagreement.
        List<EvidenceItem> group = category == CostCategory.Water
            ? inUse.Where(e => e.Category == name || e.Category == _waterResponsibility).ToList()
            : items;
        if (group.Any(e => e.Status == EvidenceStatus.Conflicting))
        {
            line = new ConflictingLine(category, group.Select(e => e.Id).ToList());
            return null;
        }

        List<string> notCalculated = IdsWithStatus(items, EvidenceStatus.NotCalculated);
        if (notCalculated.Count > 0)
        {
            line = new NotCalculatedLine(category, notCalculated);
            return null;
        }

        List<string> included = IdsWithStatus(items, EvidenceStatus.Included);
        if (included.Count > 0)
        {
            line = new IncludedLine(category, included);
            return null;
        }

        if (items.Any(e => e.Status == EvidenceStatus.NotApplicable))
        {
            return null;
        }

        line = new MissingLine(category);
        return null;
    }

    private static List<string> IdsWithStatus(List<EvidenceItem> items, EvidenceStatus status) =>
        items.Where(e => e.Status == status).Select(e => e.Id).ToList();

    private static string PeriodWords(Period period) => period switch
    {
        Period.Once => "a one-off amount",
        Period.Month => "a monthly amount",
        _ => "a yearly amount",
    };

    private static Error WrongKind(string category) =>
        new($"input.wrong-kind.{category}", $"The {category} value is not the kind of value this cost needs.", ErrorCategory.Validation);

    private static Error Ambiguous(string category) =>
        new($"input.ambiguous.{category}", $"There is more than one {category} value in use, so none can be chosen.", ErrorCategory.Conflict);

    private static Result<SelectedInputs> Fail(string code, string message, ErrorCategory category) =>
        Result.Failure<SelectedInputs>(new Error(code, message, category));
}
