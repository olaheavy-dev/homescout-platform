using System.Globalization;
using System.Numerics;
using System.Text.Json.Nodes;

namespace HomeScout.CostEngine.Tests;

/// <summary>
/// Pence.RoundRatio rounds an exact fraction of pence once: nearest penny, exact halves away from zero (decisions 0021, 0034).
/// The six boundary cases come from test-cases/rounding-boundaries.json, written there as decimal text and read here as ratios.
/// </summary>
[TestFixture]
internal sealed class RoundRatioTests
{
    private static IEnumerable<TestCaseData> BoundaryCases() =>
        JsonNode.Parse(File.ReadAllText(RepositoryFiles.TestCases("rounding-boundaries.json")))!["cases"]!.AsArray()
            .Where(c => c!["inputs"]!["unroundedPence"] is not null)
            .Select(c =>
            {
                string text = c!["inputs"]!["unroundedPence"]!.GetValue<string>();
                (BigInteger numerator, BigInteger denominator) = AsRatio(text);
                return new TestCaseData(numerator, denominator, c["expected"]!["pence"]!.GetValue<long>())
                    .SetArgDisplayNames(c["id"]!.GetValue<string>());
            });

    /// <summary>"-0.4999" becomes -4999 / 10000: the digits without the point over a power of ten.</summary>
    private static (BigInteger Numerator, BigInteger Denominator) AsRatio(string decimalText)
    {
        int point = decimalText.IndexOf('.', StringComparison.Ordinal);
        int fractionDigits = point < 0 ? 0 : decimalText.Length - point - 1;

        return (BigInteger.Parse(decimalText.Replace(".", string.Empty, StringComparison.Ordinal), CultureInfo.InvariantCulture), BigInteger.Pow(10, fractionDigits));
    }

    [Test]
    public void BoundaryFile_loaded_hasAllSixRatioCases() =>
        Assert.That(BoundaryCases().Count(), Is.EqualTo(6));

    [TestCaseSource(nameof(BoundaryCases))]
    public void RoundRatio_boundaryCaseFromFile_matchesWorkedResult(BigInteger numerator, BigInteger denominator, long expectedPence) =>
        Assert.That(Pence.RoundRatio(numerator, denominator), Is.EqualTo(new Pence(expectedPence)));

    [TestCase(1, 2, 1)]
    [TestCase(-1, 2, -1)]
    [TestCase(1, -2, -1)]
    [TestCase(-1, -2, 1)]
    [TestCase(3, 2, 2)]
    [TestCase(5, 2, 3)]
    [TestCase(-5, 2, -3)]
    [TestCase(7, 3, 2)]
    [TestCase(-7, 3, -2)]
    [TestCase(0, 7, 0)]
    public void RoundRatio_signsAndHalves_roundAwayFromZero(long numerator, long denominator, long expectedPence) =>
        Assert.That(Pence.RoundRatio(numerator, denominator), Is.EqualTo(new Pence(expectedPence)));

    [Test]
    public void RoundRatio_largeExactHalf_roundsAwayFromZeroWithoutLosingPrecision()
    {
        // (2n + 1) / 2 is exactly n + 0.5, so the answer is n + 1 (and -(n + 1)). 2n + 1 is already too big for a long.
        BigInteger n = 4_000_000_000_000_000_000;

        Assert.That(Pence.RoundRatio((2 * n) + 1, 2), Is.EqualTo(new Pence(4_000_000_000_000_000_001)));
        Assert.That(Pence.RoundRatio(-((2 * n) + 1), 2), Is.EqualTo(new Pence(-4_000_000_000_000_000_001)));
    }

    [Test]
    public void RoundRatio_resultTooBigForALong_throwsOverflow() =>
        Assert.Throws<OverflowException>(() => Pence.RoundRatio(BigInteger.Pow(10, 30), 1));

    [Test]
    public void RoundRatio_resultTooSmallForALong_throwsOverflow() =>
        Assert.Throws<OverflowException>(() => Pence.RoundRatio(-BigInteger.Pow(10, 30), 1));

    [Test]
    public void RoundRatio_zeroDenominator_throwsDivideByZero() =>
        Assert.Throws<DivideByZeroException>(() => Pence.RoundRatio(1, 0));
}
