namespace HomeScout.CostEngine;

/// <summary>
/// Works out the costs of one home across the story: the inputs at each step come from <see cref="AssumptionSelector"/>,
/// consecutive steps that use the same evidence are merged into one scenario, and each scenario after the first records
/// what changed since the one before (decision 0021).
/// </summary>
public static class HomeCostBuilder
{
    /// <summary>
    /// Builds the scenarios of a home. A scenario is named <c>from-step-N</c> after its first step. A change is reported for
    /// every line whose status, amount or evidence differs from the previous scenario; a monthly difference is the difference
    /// of the two rounded monthly lines, never a rounding of the yearly difference.
    /// </summary>
    /// <remarks>
    /// Error codes (tests match the code, never the message): <c>home.not-covered</c>, <c>home.mode-missing</c> and
    /// <c>story.step-out-of-range</c> (no steps, a step below 1, or steps that do not strictly increase), plus every failure
    /// of <see cref="AssumptionSelector"/>, <see cref="Mortgage"/>, <see cref="MonthlyCost"/> and <see cref="UpfrontCash"/>,
    /// passed on unchanged.
    /// </remarks>
    /// <param name="facts">The home and its evidence.</param>
    /// <param name="storySteps">The story's steps, for example 1, 2, 3, 4, strictly increasing.</param>
    /// <exception cref="ArgumentNullException">An argument is null.</exception>
    public static Result<HomeCosts> Build(HomeFacts facts, IReadOnlyList<int> storySteps)
    {
        ArgumentNullException.ThrowIfNull(facts);
        ArgumentNullException.ThrowIfNull(storySteps);

        Error? homeError = AssumptionSelector.CheckHome(facts);
        if (homeError is not null)
        {
            return Result.Failure<HomeCosts>(homeError);
        }

        if (storySteps.Count == 0 || storySteps[0] < 1 || storySteps.Zip(storySteps.Skip(1), (a, b) => b <= a).Any(notIncreasing => notIncreasing))
        {
            return Result.Failure<HomeCosts>(new Error("story.step-out-of-range", "The story steps must start at 1 or more and increase.", ErrorCategory.Validation));
        }

        var selections = new List<(int Step, SelectedInputs Inputs)>();
        foreach (int step in storySteps)
        {
            Result<SelectedInputs> selected = AssumptionSelector.Select(facts, step);
            if (selected.IsFailure)
            {
                return Result.Failure<HomeCosts>(selected.Error);
            }

            selections.Add((step, selected.Value));
        }

        var scenarios = new List<ScenarioCosts>();
        List<LineInput>? previousInputs = null;
        int index = 0;
        while (index < selections.Count)
        {
            int last = index;
            string signature = selections[index].Inputs.Signature();
            while (last + 1 < selections.Count && selections[last + 1].Inputs.Signature() == signature)
            {
                last++;
            }

            Result<(ScenarioCosts Scenario, List<LineInput> MonthlyInputs)> built = BuildScenario(
                facts,
                selections[index].Inputs,
                selections[index].Step,
                selections[last].Step,
                scenarios.Count > 0 ? scenarios[^1] : null,
                previousInputs);
            if (built.IsFailure)
            {
                return Result.Failure<HomeCosts>(built.Error);
            }

            scenarios.Add(built.Value.Scenario);
            previousInputs = built.Value.MonthlyInputs;
            index = last + 1;
        }

        return Result.Success(new HomeCosts(facts.HomeId, selections[0].Inputs.Mode, facts.Nation, scenarios));
    }

    private static Result<(ScenarioCosts Scenario, List<LineInput> MonthlyInputs)> BuildScenario(
        HomeFacts facts,
        SelectedInputs inputs,
        int fromStep,
        int toStep,
        ScenarioCosts? previous,
        List<LineInput>? previousInputs)
    {
        var monthlyInputs = new List<LineInput>();
        MortgageSummary? mortgage = null;
        if (inputs.Mortgage is { } m)
        {
            Result<MortgageRepayment> repayment = Mortgage.MonthlyRepayment(m.AskingPrice - m.Deposit, m.RateBasisPoints, m.TermYears);
            if (repayment.IsFailure)
            {
                return Result.Failure<(ScenarioCosts, List<LineInput>)>(repayment.Error);
            }

            mortgage = new MortgageSummary(repayment.Value, m.EvidenceIds);
            monthlyInputs.Add(new AmountLine(CostCategory.MortgageRepayment, repayment.Value.MonthlyRepayment, Period.Month, m.EvidenceIds));
        }

        monthlyInputs.AddRange(inputs.MonthlyLines);

        Result<MonthlyBreakdown> monthly = MonthlyCost.Calculate(inputs.Mode, monthlyInputs, facts.MonthlyBudget);
        if (monthly.IsFailure)
        {
            return Result.Failure<(ScenarioCosts, List<LineInput>)>(monthly.Error);
        }

        Result<UpfrontBreakdown> upfront = UpfrontCash.Calculate(inputs.Mode, inputs.UpfrontLines);
        if (upfront.IsFailure)
        {
            return Result.Failure<(ScenarioCosts, List<LineInput>)>(upfront.Error);
        }

        var scenario = new ScenarioCosts($"from-step-{fromStep}", fromStep, toStep, mortgage, monthly.Value, upfront.Value, [], null);
        if (previous is not null && previousInputs is not null)
        {
            scenario = scenario with
            {
                Changes = Changes(inputs.Mode, previous, previousInputs, scenario, monthlyInputs),
                MonthlyTotalChange = SameLinesLeftOut(previous.Monthly, scenario.Monthly) ? scenario.Monthly.Total - previous.Monthly.Total : null,
            };
        }

        return Result.Success((scenario, monthlyInputs));
    }

    /// <summary>
    /// True when both totals leave out exactly the same lines for the same reasons. Only then is the difference of the two
    /// totals meaningful: otherwise a line that became unknown would look like a saving (AGENTS.md rule 7).
    /// </summary>
    private static bool SameLinesLeftOut(MonthlyBreakdown previous, MonthlyBreakdown current) =>
        previous.PartialReasons.ToHashSet().SetEquals(current.PartialReasons);

    private static List<CostChange> Changes(
        Mode mode,
        ScenarioCosts previous,
        List<LineInput> previousInputs,
        ScenarioCosts current,
        List<LineInput> currentInputs)
    {
        var changes = new List<CostChange>();
        foreach (CostCategory category in CostLines.MonthlyOrder(mode))
        {
            AddChange(changes, category, previous.Monthly.Lines, current.Monthly.Lines, previousInputs, currentInputs, monthly: true);
        }

        foreach (CostCategory category in CostLines.UpfrontOrder(mode))
        {
            AddChange(changes, category, previous.Upfront.Lines, current.Upfront.Lines, previousInputs, currentInputs, monthly: false);
        }

        return changes;
    }

    private static void AddChange(
        List<CostChange> changes,
        CostCategory category,
        IReadOnlyList<LineResult> previousLines,
        IReadOnlyList<LineResult> currentLines,
        List<LineInput> previousInputs,
        List<LineInput> currentInputs,
        bool monthly)
    {
        LineResult? before = previousLines.SingleOrDefault(l => l.Category == category);
        LineResult? now = currentLines.SingleOrDefault(l => l.Category == category);
        IReadOnlyList<string> beforeIds = before?.EvidenceIds ?? [];
        IReadOnlyList<string> nowIds = now?.EvidenceIds ?? [];

        bool unchanged = before?.Status == now?.Status && before?.Amount == now?.Amount && beforeIds.SequenceEqual(nowIds);
        if (unchanged)
        {
            return;
        }

        bool hadAmount = before is { Status: LineStatus.Calculated };
        bool hasAmount = now is { Status: LineStatus.Calculated };
        ChangeKind kind;
        if (hadAmount && hasAmount)
        {
            // Both calculated: a value change only when the amount moves; a new source for the same amount is an evidence change.
            kind = before!.Amount == now!.Amount ? ChangeKind.EvidenceChanged : ChangeKind.ValueChanged;
        }
        else if (hasAmount)
        {
            kind = ChangeKind.NowCalculated;
        }
        else if (now is null)
        {
            // The line is not in this scenario at all: it became not applicable.
            kind = ChangeKind.NoLongerApplies;
        }
        else
        {
            kind = hadAmount ? ChangeKind.NoLongerCalculated : ChangeKind.EvidenceChanged;
        }

        Pence? monthlyDifference = monthly && kind == ChangeKind.ValueChanged ? now!.Amount!.Value - before!.Amount!.Value : null;
        Pence? annualDifference = null;
        if (monthlyDifference is not null
            && previousInputs.OfType<AmountLine>().SingleOrDefault(l => l.Category == category) is { Period: Period.Year } oldYearly
            && currentInputs.OfType<AmountLine>().SingleOrDefault(l => l.Category == category) is { Period: Period.Year } newYearly)
        {
            annualDifference = newYearly.Amount - oldYearly.Amount;
        }

        changes.Add(new CostChange(category, kind, beforeIds, nowIds, monthlyDifference, annualDifference));
    }
}
