# Independently worked test cases (stage 2, task 3)

These are the **expected values** the C# cost engine must reproduce. They were worked out by hand, from the inputs in [the stage 2 plan](../../../docs/planning/stage-2-plan.md) section 1 and the rules in decisions [0021](../../../docs/decisions/0021-dotnet-engineering-foundation.md) and [0034](../../../docs/decisions/0034-rounding-boundary-cases.md), without reading or running any engine code (AGENTS.md rule 2). Each figure was then re-checked with a separate throwaway Python calculation using `decimal.Decimal` and `ROUND_HALF_UP` applied to the absolute value (which is "half away from zero"). The Python is not committed.

Files:
- `rounding-boundaries.json`: rounding boundary cases (decision 0034).
- `story-calculations.json`: service-charge difference, mortgage repayments, monthly housing costs, upfront cash and the B1 budget beat.

## Case format

Each file is `{ "format_version": 1, "plan_snapshot_date": "2026-10-23", "money": "...", "cases": [ ... ] }`. Each case:

```json
{
  "id": "stable-kebab-case-id",
  "description": "what is being calculated",
  "rule": { "source": "the rule or source followed", "url": "link or repo path" },
  "inputs": { "...": "money in whole pence" },
  "steps": [ { "n": 1, "description": "...", "value_pence": 0, "rounding": "when and how rounded" } ],
  "expected": { "...": "pence, or a status string" }
}
```

- **Money is integer pence.** The two exceptions are rounding inputs that are fractions of a penny (`unrounded_pence`, a decimal string such as `"0.4999"`), and display-only fields in `steps` named `value_pence_exact` or `value_decimal` (decimal strings; recurring decimals are shown to 8 or 15 places for reading only). A data-driven test should read `inputs` and `expected`; `steps` are the working for reviewers.
- **Statuses** in `expected.lines`: `"included"` (paid by the landlord or in another charge, shown as included, never zero), `"not_calculated"` (excluded and flagged, never zero), `"unconfirmed"` (see assumption 1). Their lines add nothing to the total.
- Rounding everywhere: nearest penny, half away from zero; each line rounded once; a total is the sum of the rounded lines.

## 1. Rounding boundaries (decision 0034)

| Case | Unrounded | Result |
|---|---|---|
| just below half | 0.4999p / -0.4999p | 0p / 0p |
| exactly half | 0.5p / -0.5p | 1p / -1p |
| just above half | 0.5001p / -0.5001p | 1p / -1p |

Annual-to-monthly (annual pence / 12), positive and negated: 5 gives 0.41667 so 0p; 6 gives exactly 0.5 so 1p; 7 gives 0.58333 so 1p; 18 gives exactly 1.5 so 2p; 30 gives exactly 2.5 so **3p** (banker's rounding would give 2p, which is why this case exists); 25000 (B1 ground rent) gives 2083.33 so 2083p; 185000 (B2 and R2 council tax) gives 15416.67 so 15417p. Plain divisions by 8 give 0.125 (0p), 0.375 (0p), 0.625 (1p), and the negatives mirror them (-0.625 gives -1p).

Dividing a whole number of pence by 12 can only produce fractions that are multiples of 1/12, so the 0.4999 and 0.5001 style cases are applied directly to an unrounded value. The mortgage repayment uses the same rounding step; its unrounded value cannot be controlled to land on a boundary, so the boundary behaviour is proved by the direct rounding cases above (assumption 3).

## 2. Story calculations

All inputs below are quoted from the plan; "listing" figures are listing claims, "estimate" figures are user-entered.

### Service-charge difference (B1)
- Listing £2,400 = 240,000p a year. 2026 budget £3,720 = 372,000p a year.
- Yearly difference: 372,000 - 240,000 = **132,000p (£1,320)**.
- Monthly: 240,000 / 12 = 20,000p exactly; 372,000 / 12 = 31,000p exactly; difference **11,000p (£110)**. No rounding is needed (all exact). Cross-check: 132,000 / 12 = 11,000.

### Mortgage repayment
Formula (standard repayment, monthly compounding): **M = P r / (1 - (1+r)^-n)**, with r = annual rate / 12 and n = years x 12. Source: the monthly payment formula as printed by Chase, [Understanding amortized loans and how to calculate mortgage payments](https://www.chase.com/personal/mortgage/education/financing-a-home/loan-amortization): M = P r (1+r)^n / ((1+r)^n - 1), with r the annual rate divided by 12 and n the number of monthly payments. Multiplying top and bottom by (1+r)^-n gives the form above (that algebra is ours). Note: this is a US lender's educational page, not a central bank or university; see "assumptions".

Rounding: r, (1+r)^n and M are kept at full precision (60 digits in the check; no intermediate rounding), then **M is rounded once to the penny, half away from zero.**

Common values: r = 0.055 / 12 = 0.00458333...; n = 25 x 12 = 300; (1+r)^300 = 3.942671556436...; (1+r)^-300 = 0.253635126763...; 1 - (1+r)^-300 = 0.746364873237...

| | P | Unrounded M | Rounded |
|---|---|---|---|
| B1 | £190,000 - £30,000 = £160,000 (16,000,000p) | 98,253.99877p | **98,254p (£982.54)** |
| B2 | £255,000 - £30,000 = £225,000 (22,500,000p) | 138,169.68576p | **138,170p (£1,381.70)** |

Sense check using the other form of the formula: B1 = 160,000 x 0.0045833 x 3.942672 / 2.942672 = about £982.54. The 60-digit powers above cannot be done by hand; they were produced in the Python check, and the sense check by hand agrees to the penny.

### Monthly housing cost
Each yearly item is divided by 12 and rounded once; monthly estimates are used as given; total is the sum of the rounded lines.

Rounded yearly lines used: B1 ground rent £250 = 25,000 / 12 = 2,083.33 so 2,083p; B1 council tax £2,100 = 210,000 / 12 = 17,500p exactly; B2 council tax £1,850 = 185,000 / 12 = 15,416.67 so 15,417p; R1 council tax £1,600 = 160,000 / 12 = 13,333.33 so 13,333p; R2 council tax £1,850 = 15,417p.

**B1, listing service charge** (service charge £2,400 = 20,000p): 98,254 + 20,000 + 2,083 + 17,500 + 8,500 (energy) + 4,500 (water) + 3,000 (broadband) = **153,837p (£1,538.37)**. Buildings insurance: included in service charge. Internal maintenance: not calculated (excluded, flagged).

**B1, 2026 budget** (service charge £3,720 = 31,000p): same lines with 31,000 instead of 20,000 = **164,837p (£1,648.37)**.

**B2**: 138,170 + 15,417 + 12,000 + 5,000 + 3,000 + 3,500 (insurance) + 6,000 (maintenance) = **183,087p (£1,830.87)**.

**R1 before water**: 120,000 (rent) + 13,333 + 8,000 + 3,000 = **144,333p (£1,443.33)**; water shown as unconfirmed (assumption 1).
**R1 after water**: 144,333 + 4,500 = **148,833p (£1,488.33)**.

**R2**: 127,500 (rent) + 15,417 (council tax) = **142,917p (£1,429.17)**; energy, water, broadband "included".

### Upfront cash
| Home | Working | Total |
|---|---|---|
| B1 | deposit 3,000,000 + moving 120,000; stamp duty and legal fees not calculated | **3,120,000p (£31,200)**, flagged partial |
| B2 | same | **3,120,000p (£31,200)**, flagged partial |
| R1 | deposit 138,000 + first month's rent 120,000 + moving 120,000 | **378,000p (£3,780)** |
| R2 | deposit 147,000 + first month's rent 127,500 + moving 120,000 | **394,500p (£3,945)** |

### The B1 budget beat
Budget £1,600 = 160,000p. B1 on the listing figure: 153,837p, within budget with £62.63 to spare. B1 on the 2026 budget: 164,837p, **over by £48.37**. **The beat lands as the plan intends.** No inputs were changed.

## Independence check
Every figure above was worked by hand first, then recomputed in a separate Python script (Decimal, 60-digit precision, half away from zero) that took only the plan's inputs. **No mismatches** were found between the hand working and the check (the hand mortgage figures rely on the Python for the high-precision powers, as said above).

## Assumptions the plan did not specify
1. R1 "before water": water is not added and is marked `unconfirmed` (the listing claims it is included but the statement says the tenant pays it). The plan says only that the 45-pound estimate is added after the user confirms.
2. Moving costs of £1,200 are applied once to each home, as a flat upfront line.
3. Mortgage rounding boundary cases are tested through direct rounding cases, since the formula's output can't be set to a boundary value.
4. Mortgage formula is cited from a lender's educational page (fetched and read), plus algebra; no central-bank or university source could be retrieved as text. A reviewer may want a stronger citation.
5. Rate is exactly 5.5% a year (r = 0.055 / 12), compounded monthly with payments in arrears; no fees or other mortgage costs.
6. Where a home has no council tax or other line (B2 has no service charge or ground rent), the line is simply absent, not zero.
