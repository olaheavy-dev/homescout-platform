# P3a: Python engine monthly costs and mortgage repayment (issue #189)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) port step P3a; rules in [0039](../../decisions/0039-python-engineering-foundation.md) sections 2–4, register lines BE-13 to BE-17 and BE-32. **Ledger:** the `P3a` rows of [`python-port-ledger.md`](../../planning/python-port-ledger.md) (45 C# tests in `MonthlyCostTests`, `MortgageTests`, `CalculationProperties`, `BudgetBeatTests`, and 13 worked cases in `story-calculations.json`). **Builder:** Sonnet, test first; **review:** Opus before push. Builds on P2 (`Pence`, `round_ratio`, `Result`).

## Goal
Port `MonthlyCost.cs` and `Mortgage.cs`, and the shared line types they need (`LineInput.cs`, `CostLines.cs`, `CostCategories.cs`, `CostTypes.cs`, `Evidence.cs`, `Breakdowns.cs`; only what monthly costs and the mortgage use; P3b adds the upfront parts), with their tests. Upfront cash, the builder, the assumption selector and figure IDs stay for P3b. The C# keeps running.

## BE-32 decision (division)
The C# mortgage formula needs no fraction division: with `common = 10_000 × 12` and `grown = common + rate`, the repayment is `round_ratio(loan × rate × grown^n, common × (grown^n − common^n))`, all whole numbers. So **the `/` ban stands unchanged** and no `Fraction` division is added. BE-32's revisit point is answered: "P3a needed no `Fraction` division (the mortgage formula is whole-number arithmetic plus one `round_ratio`)".

`grown^n` has a variable exponent, which the architecture test forbids for `**`. Add a small helper `whole_power(base: int, exponent: int) -> int` that multiplies in a loop (`exponent` is at most 1,200 under BE-17's 100-year limit), with `type(x) is int` checks and `ValueError` for a negative exponent. No new architecture exemption.

## Design notes
- Same shapes and names as C#, in Python style: frozen slotted dataclasses, `Enum`s for categories, statuses and modes, `match … case` ending in `assert_never`. Each public function returns `Result[...]` for expected failures with the **same error codes** as C# (`mortgage.loan-not-positive`, `mortgage.rate-not-positive`, `mortgage.term-not-positive`, `mortgage.term-too-long`, `input.not-positive.budget`, `input.missing.<category>`, …); programming errors raise.
- Rules to keep: a line a home doesn't have is left out, never zero (BE-13); line order fixed per mode (BE-13); a monthly difference is the difference of the two rounded monthly lines (BE-14); rates are whole basis points (BE-15); a missing anchor stops the calculation, other missing bills make the total partial (BE-16); term over 100 years fails (BE-17); missing data is never shown as zero (rule 7).
- Expected values only from `story-calculations.json` (read by case ID with `parse_float=Fraction`) and the C# tests' literals. Port the C# test helpers (`StoryCases`, `CaseLines`, `TestFacts`, `RepositoryFiles`, `EngineArbitraries`) as plain Python test helpers.

## Tasks (each: failing test first, then code, then `make check`)
1. `whole_power` with its tests.
2. Mortgage: `monthly_repayment(loan, rate_basis_points, term_years) -> Result[MortgageRepayment]`; port `MortgageTests` and the four mortgage cases.
3. Line types and `CostLines` resolution, totals and partial reasons needed by monthly costs.
4. `monthly_cost(mode, lines, budget) -> Result[MonthlyBreakdown]`; port `MonthlyCostTests`, `BudgetBeatTests` and the monthly, service-charge-difference and budget-beat cases.
5. Properties: port `CalculationProperties` with Hypothesis (oracles written in the test, not by calling the engine).
6. Architecture test still passes on the bigger engine; extend its import allow-list only with a reason.
7. Ledger: fill every `P3a` row; update BE-32 in `docs/decisions/README.md` with the answer above.

## Acceptance
- Every P3a ledger row has a Python test; every P3a worked case is checked by ID; error codes match C#.
- `make check` passes; no change to the C#, `costs.json`, CI, Makefile, `uv.lock` or `.claude/`.
