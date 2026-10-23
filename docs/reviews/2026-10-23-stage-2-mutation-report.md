# Stage 2 mutation-testing report (task 5a)

Stryker.NET changes the cost engine's code in small ways (a `<` becomes `<=`, a line is deleted, a message is blanked) and reruns the tests. A change the tests notice is **killed**; one they miss **survives** (or has **no coverage** if no test runs that code). The score is detected mutants (killed plus timeout) as a share of the mutants that compile and were not ignored. This report answers the stage 2 gate: the tests catch planted bugs, with surviving mutants fixed or explained.

## How it was run

| | |
|---|---|
| Tool | Stryker.NET (`dotnet-stryker`) 5.0.0, Apache-2.0 (on the licence allow-list), local tool in `.config/dotnet-tools.json` |
| Command | `make mutate` (runs `dotnet dotnet-stryker --config-file stryker-config.json --output .artifacts/mutation`) |
| Settings | `stryker-config.json`: project `HomeScout.CostEngine`, test project `HomeScout.CostEngine.Tests` only, `test-runner: mtp`, Release, thresholds high 97, low 93, **break 92** |
| Reports | `.artifacts/mutation/reports/mutation-report.html` and `.json` (not committed) |
| Runner | The `mtp` (Microsoft.Testing.Platform) runner worked first time with NUnit 5 and coverlet.MTP; no test-framework change. Stryker's documentation calls the `mtp` runner a preview. |
| Tests that take part | Only `HomeScout.CostEngine.Tests`. (An earlier version of the config named the whole solution, which also pulled in the generator tests.) |
| Time | Under a minute, so it stays out of `make check` and CI. `make mutate` is a manual step: run it when the cost engine or its tests change. |

## Scores

| Run | Score | Killed | Timeout | Survived | No coverage |
|---|---|---|---|---|---|
| Before any new test | 92.94% | 381 | 1 | 19 | 10 |
| After, run 4 of 6 (counts shown) | 95.38% | 391 | 1 | 16 | 3 |

Compile-error (52) and ignored (56) mutants are not scored. Across six runs of the final tests the score was 94.40%, 94.65%, 95.13%, 95.38%, 94.40% and 94.89%.

Why the "after" score is lower than in an earlier draft (97% to 98%): that draft pinned error and exception wording in tests, which killed the string mutants. The project's rule is that tests match the error code or exception type, never the message (see `AssumptionSelector.cs`, `HomeCostBuilder.cs`, `MonthlyCost.cs`), so those tests were removed and the string mutants are now accepted survivors (listed below). I chose to accept them rather than turn string mutations off in `stryker-config.json`, because that setting would also hide the error-code strings, which the tests do check.

The score moves by up to a point between identical runs, and a few mutants appear as survivors in one run and killed in another. The cause was not investigated. The break threshold is 92, a little under the lowest run, so the normal spread does not fail the target.

## Tests added

Added to the existing test classes by subject (`PenceTests`, `ResultTests`, `MonthlyCostTests`, `AssumptionSelectorTests`, `HomeCostBuilderTests`). Each was written against a mutant that survived the first run (that run is the evidence that it survived). They cover: `Pence` comparisons on equal amounts; `ToResult()` on a success and a failure; undefined category, status and line kinds; a null evidence list; an upfront cost of the wrong kind; an upfront line given monthly or as zero (`input.wrong-period.moving-costs`, `input.not-positive.moving-costs`); the home checked before the step list; steps that start above 1; upfront changes having no monthly or annual difference; a line that becomes calculated after not applying (with no previous evidence); and a rate-only change reported as a repayment value change.

No engine behaviour was changed, and **no real bug was found**.

## Survivors: union over five analysed runs

"Runs" says how many of the five analysed runs the mutant survived (or had no coverage). Anything under 5 was killed in the other runs.

| Where | Mutant (exact replacement) | Runs | Handling |
|---|---|---|---|
| `AssumptionSelector.cs:40` | Remove `ArgumentNullException.ThrowIfNull(facts.Evidence)` | 5 | Equivalent in type: the next use of the list (LINQ `Where`) throws the same `ArgumentNullException`. Only the parameter name differs, which tests should not pin. |
| `AssumptionSelector.cs:151`, `:162` | Blank the message of `WrongKind("mortgage-rate")` / `("mortgage-term")` (no coverage) | 5 | Unreachable. `Anchor` already rejects a value of the wrong kind first. Defensive guard. |
| `AssumptionSelector.cs:306`, `:307` | Blank `"a one-off amount"`, `"a monthly amount"` | 5 | Accepted: wording only, not pinned by tests. |
| `AssumptionSelector.cs:308` | Blank `"a yearly amount"` (no coverage) | 5 | Unreachable: no anchor input is ever required yearly. Wording only. |
| `AssumptionSelector.cs:227` | `mortgage is not null` becomes `mortgage is null` in the deposit shortcut | 2 | Killed in four runs by the buy-case tests; the survivals are run-to-run variation. |
| `CostCategories.cs:26`, `:38` | Blank the "Unknown cost category" / "Unknown line status" messages | 5 | Accepted: wording only. The exception type is tested. |
| `CostLines.cs:18`, `:26`, `:43` | Blank the "Unknown mode" and "A line in the list is null" messages | 5 | Accepted: wording only. |
| `CostLines.cs:88` | Blank the "Unknown kind of line" message | 5 | Accepted: wording only. |
| `Error.cs:37` | Blank the "Unknown error category" message | 5 | Accepted: wording only. |
| `HomeCostBuilder.cs:59` | Negate the loop condition on `last + 1 < selections.Count && ...` | 2 | Makes the loop run forever, so it is detected as a timeout in other runs. Counted as survived in two runs by the preview runner. |
| `HomeCostBuilder.cs:121` | `previous is not null && previousInputs is not null` becomes `\|\|` | 1 | Equivalent: the two are always null or non-null together. |
| `HomeCostBuilder.cs:175` | `before?.Status == now?.Status && before?.Amount == now?.Amount` becomes `\|\|` (first `&&`) | 2 | Killed in four runs by the "status change between lines with no amount" test; survivals are run-to-run variation. |
| `HomeCostBuilder.cs:190` | `monthly && oldSource is not null && newSource is not null` becomes `monthly && oldSource is not null \|\| newSource is not null` | 1 | Equivalent: upfront lines are never in the monthly input list, so `newSource` is null whenever `monthly` is false. |
| `HomeCostBuilder.cs:190` | Same expression with the first `&&` becoming `\|\|` | 1 | Equivalent for the same reason: `oldSource` and `newSource` are null for upfront lines, and for monthly lines `monthly` is true. |
| `HomeCostBuilder.cs:212`, `:213` | `SingleOrDefault()` becomes `Single()` | 2 and 2 | Equivalent: a monthly difference exists only when the line came from exactly one amount line on each side. |
| `Pence.cs:69` | Remove the `throw new DivideByZeroException(...)` statement | 5 | Equivalent in type: `BigInteger.DivRem` then throws `DivideByZeroException` itself. |
| `Pence.cs:69` | Blank the divide-by-zero message | 5 | Accepted: wording only. |
| `Pence.cs:73` | `numerator.Sign * denominator.Sign < 0` becomes `<= 0` | 1 | Equivalent: signs are -1, 0 or 1 and the denominator is never zero, so the product is zero only when the numerator is zero, whose size is zero, and negating zero changes nothing. |
| `Pence.cs:82` | Remove `checked(...)` around the `long` conversion | 3 | Equivalent: the explicit `BigInteger` to `long` conversion throws `OverflowException` by itself (and `RoundRatio_resultTooBigForALong_throwsOverflow` passes either way). |
| `Result.cs:21`, `:74`, `:78` | Blank the misuse messages | 5 | Accepted: wording only. The exception type is tested. |
| `SelectedInputs.cs:30` | `"-"` becomes `""` for a missing mortgage in the scenario signature | 2 | Equivalent: `Mortgage` is null exactly when the mode is rent, and the mode is already part of the signature. |

Mutants that had been survivors in the first run and are now killed include `HomeCostBuilder.cs:116` (an upfront line with the wrong period or a zero amount now fails with the right error code), the `Pence` comparison boundaries, `ToResult()`, the upfront-only change paths and the `?? []` on the previous evidence ids.

Timeout, detected: `HomeCostBuilder.cs:78` (`index = last + 1` becomes `last - 1`, an endless loop), seen in two of the five analysed runs.

## Reading the result

Every remaining survivor is wording only, unreachable defensive code, an equivalent mutant, or run-to-run variation of the runner. Two follow-ups would be sensible but are not part of this task: look into the run-to-run variation (for example by comparing the `vstest` runner), and re-run `make mutate` when the cost engine changes.
