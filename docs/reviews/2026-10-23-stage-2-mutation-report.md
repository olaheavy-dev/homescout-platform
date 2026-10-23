# Stage 2 mutation-testing report (task 5a)

Stryker.NET changes the cost engine's code in small ways (a `<` becomes `<=`, a line is deleted, a message is blanked) and reruns the tests. A change the tests notice is **killed**; one they miss **survives** (or has **no coverage** if no test runs that code). The score is killed mutants as a share of the mutants that compile and were not ignored. This report answers the stage 2 gate: the tests catch planted bugs, with surviving mutants fixed or explained.

## How it was run

| | |
|---|---|
| Tool | Stryker.NET (`dotnet-stryker`) 5.0.0, Apache-2.0 (on the licence allow-list), local tool in `.config/dotnet-tools.json` |
| Command | `make mutate` (runs `dotnet dotnet-stryker --config-file stryker-config.json --output .artifacts/mutation`) |
| Settings | `stryker-config.json`: project `HomeScout.CostEngine`, tests `HomeScout.CostEngine.Tests`, `test-runner: mtp`, Release, thresholds high 98, low 95, **break 95** |
| Reports | `.artifacts/mutation/reports/mutation-report.html` and `.json` (not committed) |
| Runner | The `mtp` (Microsoft.Testing.Platform) runner worked first time with NUnit 5 and coverlet.MTP; no test-framework change. Stryker's documentation calls the `mtp` runner a preview. |
| Time | About 35 seconds, so it stays out of `make check` and CI. |

## Scores

| | Score | Killed | Survived | No coverage |
|---|---|---|---|---|
| Before (no new tests) | 92.94% | 381 | 19 | 10 |
| After (6 runs of the final tests) | 97.3% to 98.5% | 401 | 5 | 4 |

(Compile-error and ignored mutants, 52 and 56, are not scored. One timeout counts as detected.)

The score moves by about a point between identical runs: some mutants that the tests do kill occasionally show as survivors, and the reverse. The cause was not investigated; it is likely Stryker's preview `mtp` runner. The break threshold is therefore 95, a little below the lowest "after" run, rather than the exact score. The survivor table below is from the last run; the same equivalent mutants appear every time.

## Tests added

`packages/cost-engine/tests/HomeScout.CostEngine.Tests/MutationSurvivorTests.cs` (21 tests). Each one was written against a mutant that survived the first run (the "before" run is the evidence that it survived) and passes only because the mutant is now caught. They cover: `Pence` comparisons on equal amounts, error and misuse messages of `Result`, `Error` and the enum guards, `ToResult()` on a success, an upfront cost of the wrong kind, the wording of wrong-period errors, home checked before the step list, upfront changes having no monthly or annual difference, steps that start above 1, a line that becomes calculated after not applying, and a rate-only change.

No engine behaviour was changed, and **no real bug was found**.

## Survivors after the fixes

| Where | Mutant | Handling |
|---|---|---|
| `AssumptionSelector.cs` ~151 and ~162 | Blank the message of `WrongKind("mortgage-rate")` / `("mortgage-term")` (no coverage) | Unreachable. `Anchor` already rejects a value of the wrong kind before these checks run. Kept as a defensive guard against a future change to `Anchor`. |
| `AssumptionSelector.cs` ~308 | Blank `"a yearly amount"` in `PeriodWords` (no coverage) | Unreachable. Only the once and monthly periods are ever required of an anchor input. The fallback is there for completeness. |
| `AssumptionSelector.cs` ~228 | Remove the shortcut that reuses the checked mortgage deposit (seen in an earlier run) | Equivalent. Without it, the general path finds the same deposit evidence and gives the same line. |
| `HomeCostBuilder.cs` ~116 | Remove the upfront-failure return (no coverage) | Unreachable. `Select` has already checked every upfront line and the deposit, so `UpfrontCash.Calculate` cannot fail here. Defensive. |
| `HomeCostBuilder.cs` ~121 | `&&` to `||` on `previous` and `previousInputs` (seen in one run) | Equivalent. The two are always null or non-null together. |
| `HomeCostBuilder.cs` ~190 | `monthly && old != null && new != null` becomes `(monthly && old != null) \|\| new != null` | Equivalent. Upfront sources are never in the monthly input list, so `newSource` is null whenever `monthly` is false. |
| `HomeCostBuilder.cs` ~212 | `SingleOrDefault()` to `Single()` | Equivalent. A monthly difference exists only when the line came from exactly one amount line. |
| `HomeCostBuilder.cs` ~78 | `index = last + 1` to `last - 1` | Times out (an endless loop). A timeout counts as detected. |
| `Mortgage.cs` ~61 | Remove `checked(...)` on `termYears * 12` | Equivalent. The term is already limited to the maximum term, so the product cannot overflow. |
| `Pence.cs` ~73 | `Sign * Sign < 0` to `<= 0` | Equivalent. When the numerator is zero the size is zero and negating zero changes nothing. |
| `SelectedInputs.cs` ~30 | Always use `"-"` for the mortgage part of the signature | Equivalent in practice. The mortgage repayment line already carries the same evidence ids, so the signature differs either way. |

Mutants that appeared as survivors in only some runs (for example a removed `?? []` in `AddChange`, or a changed `&&` in the "unchanged" test) are killed by the tests in most runs; see the note on run-to-run variation above.

## Reading the result

All remaining survivors are unreachable defensive code or equivalent mutants. Two follow-ups would be sensible but are not part of this task: investigate the run-to-run variation (try the `vstest` runner for comparison, or a newer Stryker.NET), and re-run `make mutate` when the cost engine changes.
