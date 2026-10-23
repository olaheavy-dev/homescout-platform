# Independently worked test cases (stage 2, task 3)

These are the **expected values** the C# cost engine must reproduce. They were worked out by hand, from the inputs in [the stage 2 plan](../../../docs/planning/stage-2-plan.md) section 1 and the rules in decisions [0021](../../../docs/decisions/0021-dotnet-engineering-foundation.md) and [0034](../../../docs/decisions/0034-rounding-boundary-cases.md), without reading or running any engine code (AGENTS.md rule 2). Each figure was then re-checked with a separate throwaway Python calculation using `decimal.Decimal` and `ROUND_HALF_UP` applied to the absolute value (which is "half away from zero"). The Python is not committed.

Files:
- `rounding-boundaries.json`: rounding boundary cases (decision 0034).
- `story-calculations.json`: service-charge difference, mortgage repayments (including two boundary cases), monthly housing costs, upfront cash and the B1 budget beat.

## Case format

Each file is `{ "$schema": "../schema/test-case.schema.json", "formatVersion": 1, "planSnapshotDate": "2026-10-23", "money": "...", "cases": [ ... ] }`. Keys are camelCase; statuses and category names are hyphenated, matching `packages/fixtures/schema/` (statuses `included`, `not-calculated`, `conflicting`; categories such as `service-charge`, `council-tax`, `maintenance`, `first-month-rent`). Each case:

```json
{
  "id": "stable-kebab-case-id",
  "description": "what is being calculated",
  "rule": { "source": "the rule or source followed", "url": "link or repo path" },
  "inputs": { "...": "see below" },
  "steps": [ { "n": 1, "description": "...", "valuePence": 0, "rounding": "when and how rounded" } ],
  "expected": { "...": "pence, or a status" }
}
```

- **Money is integer pence**, in fields ending `Pence`. A data-driven test reads `inputs` and `expected`; `steps` are the working for reviewers.
- **Decimal strings**: values that are not whole pence or not money are strings, so no float is involved: `inputs.annualRate: "0.055"`, `inputs.unroundedPence: "0.4999"` (a fraction of a penny), and in steps `valueExact` / `valuePenceExact` / `valueDecimal` (recurring decimals shown to 8 or 15 places for reading only).
- **Step keys**: `n`, `description`, `rounding`, and one value key: `valuePence` (integer pence), `valueExact` / `valuePenceExact` / `valueDecimal` (decimal strings), `value` (a plain number or boolean, for example the number of payments `N`), or `status` (a line that is not added).
- **Text inputs** (`...Source`, `source`, `note`, `testOnlyNote`) say where a value came from. Sources use the plan's labels (listing claim, user-entered, synthetic, and so on). They are for people, not for the calculation.
- **Cost lines** in monthly and upfront cases are objects in `inputs.lines`: `{category, period: "year"|"month"|"once", amountPence, source}` (`once` for upfront lines), or `{category, status, note, source}` for lines with no amount, or `{category, mortgageCase}` for the mortgage line. **Cross-case links**: `mortgageCase` names another case's `id` whose rounded result is the line's amount; `listingTotalCase` and `budgetTotalCase` in the budget beat do the same.
- **`testOnly: true`** marks an input chosen to hit a boundary. It is not a plan home or a plan figure (the 5, 6, 7, 18 and 30 pence a year cases, the sub-penny rounding inputs, and the two mortgage boundary loans).
- **Statuses** in `expected.lines`: `included` (covered by another charge or by the rent), `not-calculated` (this version doesn't work it out), `conflicting` (sources disagree and it is not settled). Such a line adds nothing to the total and is never shown as zero.
- **Partial totals**: any `not-calculated` or unsettled line makes the total partial. Monthly and upfront cases carry `totalIsPartial` and `partialReasons`. A partial total is a floor, not the full cost.
- **Budget fields**, the same on every monthly case: `budgetPence` (160,000), `budgetDifferencePence` = budget minus total (positive = headroom, negative = over budget), and `withinBudget` (total at or below the budget).
- Rounding everywhere: nearest penny, half away from zero; each line rounded once; a total is the sum of the rounded lines.

## 1. Rounding boundaries (decision 0034)

| Case | Unrounded | Result |
|---|---|---|
| just below half | 0.4999p / -0.4999p | 0p / 0p |
| exactly half | 0.5p / -0.5p | 1p / -1p |
| just above half | 0.5001p / -0.5001p | 1p / -1p |

Annual-to-monthly (annual pence / 12), positive and negated: 5 gives 0.41667 so 0p; 6 gives exactly 0.5 so 1p; 7 gives 0.58333 so 1p; 18 gives exactly 1.5 so 2p; 30 gives exactly 2.5 so **3p** (banker's rounding would give 2p, which is why this case exists); 25000 (B1 ground rent) gives 2083.33 so 2083p; 185000 (B2 and R2 council tax) gives 15416.67 so 15417p.

Dividing a whole number of pence by 12 can only give fractions that are multiples of 1/12, so the 0.4999 and 0.5001 cases are applied directly to an unrounded value. The mortgage repayment uses the same rounding step, and its two boundary cases (below) put the unrounded value just either side of a half penny. The negative side of the repayment is covered by the direct rounding cases.

## 2. Story calculations

All inputs are quoted from the plan; "listing" figures are listing claims, "estimate" figures are user-entered.

### Service-charge difference (B1)
- Listing £2,400 = 240,000p a year. 2026 budget £3,720 = 372,000p a year.
- Yearly difference: 372,000 - 240,000 = **132,000p (£1,320)**.
- Monthly: 240,000 / 12 = 20,000p exactly; 372,000 / 12 = 31,000p exactly; difference **11,000p (£110)**. Nothing needs rounding. Cross-check: 132,000 / 12 = 11,000.

### Mortgage repayment
Formula (standard repayment, monthly compounding), from Kirk, D., *Contemporary Mathematics*, section 6.8 "The Basics of Loans", OpenStax (Rice University), 2023, <https://openstax.org/books/contemporary-mathematics/pages/6-8-the-basics-of-loans>: pmt = P(r/n)(1+r/n)^(nt) / ((1+r/n)^(nt) - 1). With n = 12 payments a year, monthly rate i = r/12 and N = 12 t payments, this is the same as **M = P i / (1 - (1+i)^-N)** (dividing top and bottom by (1+i)^N; that algebra is ours). A secondary source gives the same formula: Chase, [Understanding amortized loans and how to calculate mortgage payments](https://www.chase.com/personal/mortgage/education/financing-a-home/loan-amortization).

**The formula comes from the source; the rounding does not.** HomeScout rounds M once to the nearest penny, half away from zero (decision 0021), not the lender convention of always rounding up. i, (1+i)^N and M are kept at full precision (60 digits in the check), with no intermediate rounding.

Common values: i = 0.055 / 12 = 0.00458333...; N = 25 x 12 = 300; (1+i)^300 = 3.942671556436...; (1+i)^-300 = 0.253635126763...

| | P | Unrounded M | Rounded |
|---|---|---|---|
| B1 | £190,000 - £30,000 = £160,000 (16,000,000p) | 98,253.99877p | **98,254p (£982.54)** |
| B2 | £255,000 - £30,000 = £225,000 (22,500,000p) | 138,169.68576p | **138,170p (£1,381.70)** |
| Test-only boundary | £100,252 (10,025,200p) | 61,563.49928p | **61,563p** (rounding up would give 61,564p) |
| Test-only boundary | £100,607 (10,060,700p) | 61,781.50034p | **61,782p** (truncation would give 61,781p) |

Sense check by hand with the other form of the formula, using the unrounded i = 0.055/12: B1 = 160,000 x 0.00458333 x 3.942672 / 2.942672 = about £982.54. The 300th powers cannot be done by hand; they came from the Python check.

### Monthly housing cost
Each yearly item is divided by 12 and rounded once; monthly estimates are used as given; the total is the sum of the rounded lines. Yearly lines: B1 ground rent £250 = 25,000 / 12 = 2,083.33 so 2,083p; B1 council tax £2,100 = 17,500p exactly; B2 and R2 council tax £1,850 = 15,416.67 so 15,417p; R1 council tax £1,600 = 13,333.33 so 13,333p.

| Case | Working (pence) | Total | Partial? | Budget difference |
|---|---|---|---|---|
| B1, listing service charge (£2,400 = 20,000) | 98,254 + 20,000 + 2,083 + 17,500 + 8,500 + 4,500 + 3,000 | **153,837p (£1,538.37)** | yes: maintenance not calculated | +6,163p (£61.63 under) |
| B1, 2026 budget (£3,720 = 31,000) | same with 31,000 | **164,837p (£1,648.37)** | yes: maintenance not calculated | -4,837p (£48.37 over) |
| B2 | 138,170 + 15,417 + 12,000 + 5,000 + 3,000 + 3,500 (insurance) + 6,000 (maintenance) | **183,087p (£1,830.87)** | no | -23,087p (£230.87 over) |
| R1, before water settled | 120,000 + 13,333 + 8,000 + 3,000; water `conflicting`, left out | **144,333p (£1,443.33)** | yes: water not settled yet | +15,667p |
| R1, after water confirmed | 144,333 + 4,500 | **148,833p (£1,488.33)** | no | +11,167p |
| R2 | 127,500 + 15,417; energy, water, broadband `included` | **142,917p (£1,429.17)** | no | +17,083p |

B1 buildings insurance is `included` (in the service charge); B1 maintenance is `not-calculated`, and uses the same `maintenance` category as B2.

### Upfront cash
| Home | Working | Total |
|---|---|---|
| B1 | deposit 3,000,000 + moving 120,000; stamp duty and legal fees `not-calculated` | **3,120,000p (£31,200)**, partial |
| B2 | same | **3,120,000p (£31,200)**, partial |
| R1 | deposit 138,000 + first month's rent 120,000 + moving 120,000 | **378,000p (£3,780)** |
| R2 | deposit 147,000 + first month's rent 127,500 + moving 120,000 | **394,500p (£3,945)** |

### The B1 budget beat
Budget £1,600 = 160,000p. B1 on the listing figure: 153,837p, within budget with 6,163p (£61.63) to spare. B1 on the 2026 budget: 164,837p, **over by 4,837p (£48.37)**. **The beat lands as the plan intends.** Both totals are partial (maintenance is not calculated), so the real figures are higher; the beat still holds on the calculated lines. No inputs were changed.

## Independence check
Every figure above was worked by hand first, then recomputed in a separate Python script (Decimal, 60-digit precision, half away from zero) that checks the hand totals. No mismatches. The hand mortgage figures rely on the Python for the high-precision powers, as said above.

## Assumptions
Founder decisions (founder, 23 Oct 2026):
- **(a)** Purchase price equals the asking price, so loan = asking price - deposit.
- **(b)** "Within budget" means total at or below £1,600; exactly £1,600 is within.
- **(c)** Until R1's water responsibility is settled, water is left out of R1's monthly total (status `conflicting`) and the total is flagged partial ("water: not settled yet"). It is added once the user confirms.

Ours, for the founder to confirm:
1. Moving costs of £1,200 are a flat upfront line once per home.
2. Rate is exactly 5.5% a year (i = 0.055 / 12), compounded monthly with payments in arrears; no fees or other mortgage costs.
3. A line a home doesn't have (for example B2's service charge) is left out, not shown as zero.
4. The two mortgage boundary loans (£100,252 and £100,607) are test-only inputs, not plan homes.
5. `conflicting` (already in the fixture schema) is used for R1's unsettled water.
