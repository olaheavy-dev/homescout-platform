using FsCheck;
using FsCheck.Fluent;

namespace HomeScout.CostEngine.Tests;

// FsCheck.NUnit supplies the test arguments, which the NUnit analyser cannot see (NUnit1027).
#pragma warning disable NUnit1027

/// <summary>An amount of pence from 1 to 10^10 (up to 100 million pounds), small enough that sums never overflow.</summary>
internal readonly record struct BoundedPence(long Value)
{
    public Pence Pence => new(Value);
}

/// <summary>A yearly rate in whole basis points, 1 to 3,000 (0.01% to 30%).</summary>
internal readonly record struct RateBasisPoints(int Value);

/// <summary>A mortgage term in whole years, 1 to 40.</summary>
internal readonly record struct TermYears(int Value);

/// <summary>
/// A set of monthly lines for one mode. The anchor line (rent, or the mortgage repayment) always has an amount;
/// every other applicable line is randomly calculated (monthly or yearly), included, not calculated, conflicting or missing.
/// </summary>
internal sealed record MonthlyScenario(Mode Mode, IReadOnlyList<LineInput> Lines, Pence Budget);

/// <summary>A set of upfront lines for one mode. Every line is randomly calculated, included, not calculated, conflicting or missing.</summary>
internal sealed record UpfrontScenario(Mode Mode, IReadOnlyList<LineInput> Lines);

/// <summary>Bounded generators for the engine properties (decision 0027).</summary>
internal static class EngineArbitraries
{
    private const long _maxPence = 10_000_000_000;

    private static readonly CostCategory[] _buyMonthly =
    [
        CostCategory.MortgageRepayment, CostCategory.ServiceCharge, CostCategory.GroundRent, CostCategory.CouncilTax, CostCategory.Energy,
        CostCategory.Water, CostCategory.Broadband, CostCategory.BuildingsInsurance, CostCategory.Maintenance,
    ];

    private static readonly CostCategory[] _rentMonthly =
    [
        CostCategory.Rent, CostCategory.CouncilTax, CostCategory.Energy, CostCategory.Water, CostCategory.Broadband,
    ];

    private static readonly CostCategory[] _buyUpfront =
    [
        CostCategory.MortgageDeposit, CostCategory.MovingCosts, CostCategory.StampDuty, CostCategory.LegalFees,
    ];

    private static readonly CostCategory[] _rentUpfront =
    [
        CostCategory.Deposit, CostCategory.FirstMonthRent, CostCategory.MovingCosts,
    ];

    private static readonly string[] _evidence = ["EVIDENCE-1"];

    private static Gen<long> PenceGen =>
        Gen.OneOf(Gen.Choose(1, 1_000).Select(n => (long)n), Gen.Choose(1, int.MaxValue).Select(n => (long)n), Gen.Elements(1L, _maxPence));

    public static Arbitrary<BoundedPence> Pennies() =>
        PenceGen.Select(n => new BoundedPence(n)).ToArbitrary();

    public static Arbitrary<RateBasisPoints> Rates() =>
        Gen.OneOf(Gen.Choose(1, 3_000), Gen.Elements(1, 550, 3_000)).Select(n => new RateBasisPoints(n)).ToArbitrary();

    public static Arbitrary<TermYears> Terms() =>
        Gen.Choose(1, 40).Select(n => new TermYears(n)).ToArbitrary();

    public static Arbitrary<MonthlyScenario> MonthlyScenarios() =>
        Gen.Elements(Mode.Buy, Mode.Rent)
            .SelectMany(mode => Lines(mode == Mode.Buy ? _buyMonthly : _rentMonthly, anchorFirst: true, upfront: false)
                .SelectMany(lines => Gen.Choose(1, int.MaxValue).Select(budget => new MonthlyScenario(mode, lines, new Pence(budget)))))
            .ToArbitrary();

    public static Arbitrary<UpfrontScenario> UpfrontScenarios() =>
        Gen.Elements(Mode.Buy, Mode.Rent)
            .SelectMany(mode => Lines(mode == Mode.Buy ? _buyUpfront : _rentUpfront, anchorFirst: false, upfront: true)
                .Select(lines => new UpfrontScenario(mode, lines)))
            .ToArbitrary();

    private static Gen<IReadOnlyList<LineInput>> Lines(CostCategory[] categories, bool anchorFirst, bool upfront)
    {
        IEnumerable<Gen<LineInput>> perCategory = categories.Select((category, index) =>
            Line(category, forceAmount: anchorFirst && index == 0, upfront));

        Gen<List<LineInput>> all = Gen.Constant(new List<LineInput>());
        foreach (Gen<LineInput> next in perCategory)
        {
            all = all.SelectMany(soFar => next.Select(line => new List<LineInput>(soFar) { line }));
        }

        return all.Select(lines => (IReadOnlyList<LineInput>)lines);
    }

    private static Gen<LineInput> Line(CostCategory category, bool forceAmount, bool upfront)
    {
        bool monthOnly = category is CostCategory.Rent or CostCategory.MortgageRepayment;
        Gen<Period> periods = upfront ? Gen.Constant(Period.Once)
            : monthOnly ? Gen.Constant(Period.Month)
            : Gen.Elements(Period.Month, Period.Year);
        Gen<LineInput> amount = Gen.Zip(PenceGen, periods).Select(pair => (LineInput)new AmountLine(category, new Pence(pair.Item1), pair.Item2, _evidence));

        if (forceAmount)
        {
            return amount;
        }

        return Gen.OneOf(
            amount,
            Gen.Constant<LineInput>(new IncludedLine(category, _evidence)),
            Gen.Constant<LineInput>(new NotCalculatedLine(category, _evidence)),
            Gen.Constant<LineInput>(new ConflictingLine(category, _evidence)),
            Gen.Constant<LineInput>(new MissingLine(category)));
    }
}

/// <summary>A property run with the generators above.</summary>
[AttributeUsage(AttributeTargets.Method)]
internal sealed class EngineProperty : FsCheck.NUnit.PropertyAttribute
{
    public EngineProperty() => Arbitrary = [typeof(EngineArbitraries)];
}
