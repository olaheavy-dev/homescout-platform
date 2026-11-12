# Python mutation-testing report (port step P7, issue #194)

mutmut changes the Python cost engine's code in small ways (a `<` becomes `<=`, a string is altered, a call is given `None`, a `case` is removed) and reruns the tests. A change the tests notice is **killed**; one they miss **survives**; one that makes the code hang is a **timeout**. This report is the Python replacement for the [Stage 2 Stryker.NET report](2026-10-23-stage-2-mutation-report.md) (decision 0049 item 11b, decision 0039 section 4, register line BE-33, which carries BE-26's principle forward). It answers: do the tests catch planted bugs, with every survivor killed by a new test or explained.

## How it was run

| | |
|---|---|
| Tool | mutmut 3.8.1 (BSD-3-Clause), in the `dev` group of `uv.lock`; no new package |
| Command | `make mutate`: deletes `packages/vestagraph-engine/mutants/`, runs `CI=true uv run --locked mutmut run` and `mutmut export-cicd-stats` in `packages/vestagraph-engine`, then `tools/mutation_score.py` |
| Scope | `packages/vestagraph-engine/src/vestagraph_engine` (19 files, 2002 mutants), the same code Stryker.NET covered in the C# engine |
| Tests that decide | the engine's own tests, `packages/vestagraph-engine/tests` (1435 tests after this step) |
| Settings | `[tool.mutmut]` in `packages/vestagraph-engine/pyproject.toml` (see "Setup notes") |
| Repeatable score | `CI=true`: Hypothesis loads its built-in `ci` profile at import (`derandomize=True`, no deadline, no database; `hypothesis/_settings.py`, `is_in_ci()`), so the property tests draw the same examples on every run. We register no profile of our own |
| Pass mark | mutmut has none. `tools/mutation_score.py` reads `mutants/mutmut-cicd-stats.json` and fails below `MUTATION_BREAK` (Makefile). Score = (killed + timeout) / (killed + timeout + survived + suspicious + no tests + segfault); a timeout counts as detected, the others as not detected; skipped mutants are left out; no scored mutants, or an interrupted run, fails |
| Time | about 33 to 41 seconds on the author's machine (10 cores), so it stays out of `make check` and CI; run `make mutate` when the engine or its tests change |
| Platform | needs `fork`: macOS and Linux (Windows through WSL) |

### Setup notes (mutmut 3.8.1 specifics)

- mutmut reads `[tool.mutmut]` only from the `pyproject.toml` (or `setup.cfg`) in the folder it runs in, so the settings live in the engine package's `pyproject.toml`, not the workspace root, and `make mutate` runs there.
- mutmut names a mutant from the source path relative to that folder (`src/vestagraph_engine/x.py` becomes `vestagraph_engine.x`) and matches it to the module name the tests import. Run from the repository root the names would start `packages.vestagraph-engine...` and every mutant would be "no tests"; the first attempt hit exactly that ("could not find any test case for any mutant").
- `pytest_add_cli_args_test_selection = ["tests"]` limits the run to the engine tests.
- One test cannot run on a mutant and is deselected through `pytest_add_cli_args`: `test_engine_source_obeys_every_purity_rule` reads the engine's source text, and mutmut has rewritten it (it adds its own `import` and trampoline code), so the rule check fails on every mutant. `make test` still runs it on the real source.
- Removed `mutants/` before each run, so a run never reuses an earlier verdict (mutmut caches them).

## Scores

| Run | Killed | Timeout | Survived | Suspicious | No tests | Score | Time |
|---|---|---|---|---|---|---|---|
| First run, before any new test | 1698 | 2 | 302 | 0 | 0 | 84.92% | 33 s |
| Final, run 1 of `make mutate` | 1707 | 2 | 293 | 0 | 0 | 85.36% | 33 s |
| Final, run 2 of `make mutate` | 1707 | 2 | 293 | 0 | 0 | 85.36% | 41 s |

The two final runs agree on every count. A third run (with the break score set) gave 1706 killed, 3 timeout, 293 survived: one infinite-loop mutant was cut off by the timeout instead of failing a test first, which moves one mutant between "killed" and "timeout" under machine load. Both count as detected, so the score is the same 85.36%. **Break score: 85**, just below the final 85.36%. The two timeouts (`build_home_costs`, `last += 1` becoming `last = 1` and `index = last + 1` becoming `last - 1`) are infinite loops the run correctly cut off; they count as detected.

The Stryker.NET score on the C# engine was 92 to 95%. The figures are not comparable: mutmut mutates every string literal (three or four variants each) and the engine's rule is that tests match error codes and exception types, never their wording, so most survivors are wording (see below).

## Tests added (9 survivors killed)

Each was written against a survivor from the first run; the targeted rerun (`mutmut run <mutant>`) after adding the tests shows all nine killed, and the tests pass on the real engine.

| Mutant | New test | What it pins |
|---|---|---|
| `_money_anchor`: `amount <= 0` became `<= 1` | `test_select_assumptions_one_penny_rent_is_accepted_as_positive`, `test_select_assumptions_one_penny_price_or_deposit_is_accepted_as_positive` | 1p is positive, not a failure |
| `build_home_costs`: `step > INT32_MAX` became `>=` | `test_build_home_costs_a_step_of_exactly_the_largest_32_bit_number_is_accepted` | the 32-bit boundary itself is allowed |
| `_add_change`: a missing line looked up as `before.amount` / `now.amount` (two mutants) | `test_build_home_costs_a_line_not_applicable_in_every_scenario_is_left_out_of_the_changes` | a line that is not applicable in both scenarios is in neither list and is not a change |
| `monthly_cost`: text-as-lines check `or` became `and`, and `is_a(lines, str)` became `is_a(None, str)` (two mutants) | `test_monthly_cost_empty_text_as_lines_raises_type_error` | an empty string is rejected, not read as "no lines" |
| `upfront_cash`: the same two | `test_upfront_cash_empty_text_as_lines_raises_type_error` | same, for upfront cash |
| `figure_ids.mortgage`: the check dropped `scenario_id` | `test_figure_ids_text_part_that_is_not_a_str_raises_type_error` (extra assertion) | a non-text scenario id is rejected for the mortgage id |

No engine behaviour was changed, and **no real bug was found**.

## Survivors: 293 left, all explained

By kind (the counts add up to 293):

| Kind | Count | Handling |
|---|---|---|
| Wording of an error or exception message, or of a field label passed to a check (`"A change"`, `"A scenario's from_step"`), changed to `XX...XX`, upper case, lower case, or `None` | 266 | **Deliberately unpinned.** Tests match the error code and the exception type, never the message (AGENTS.md "Rules for every agent", and the docstrings of `select_assumptions`, `monthly_cost` and `build_home_costs`). Pinning wording would make a copy edit fail a test. The error codes themselves (first argument of `Error`) are mutated too and are all killed. |
| Equivalent: no behaviour change | 13 | listed below |
| Unreachable defensive code | 10 | listed below |
| Separators in `SelectedInputs.signature` | 4 | listed below |

### Equivalent (13)

- `assumption_selector.py`: in `select_assumptions` the mortgage argument of `_choose_line` is passed as `None` (monthly loop and upfront loop, 2 mutants), and in `_choose_line` `mortgage is not None` becomes `is None` (1). The deposit shortcut builds `AmountLine(deposit, ONCE, (evidence_ids[1],))`; the general path builds `AmountLine(money.amount, money.period, (item.id,))` from the single in-use deposit item that `_money_anchor` already checked. Same line. The monthly loop has no deposit category at all.
- `pence.round_ratio`, the sign test `(numerator < 0) != (denominator < 0)` with `<= 0` or `< 1` on either side (4). A zero numerator gives a zero result whatever its sign; a zero denominator raises before this line; for whole numbers `< 1` equals `<= 0`.
- `build_home_costs`: `previous_inputs = None` becomes `""` (1). It is read only when `previous` is not `None`, and is overwritten after the first scenario.
- `_build_scenario`: `previous is not None and previous_inputs is not None` becomes `or` (1). The two are `None` together, never one without the other.
- `_changes`: `monthly=False` becomes `monthly=None` (1). Both are falsy.
- `_add_change` (3): `monthly and old is not None and new is not None` becomes `monthly and old is not None or new is not None` or `monthly or old is not None and new is not None`, and `before.amount is not None and now.amount is not None` becomes `or`. A line calculated on both sides comes from an `AmountLine` on both sides in the monthly inputs and has an amount; upfront categories never appear in the monthly inputs, so the changed branch cannot give a different answer.

### Unreachable defensive code (10)

- `assumption_selector._period_words`: removing `case Period.YEAR` or the `case _: assert_never(...)` branch, and `assert_never(period)` becoming `assert_never(None)` (3). No anchor input is ever required yearly.
- `cost_lines.monthly_order` and `upfront_order`: removing `case _: assert_never(mode)`, and `assert_never(None)` (4). A mode that is not a `Mode` raises `TypeError` earlier in the same function.
- `cost_lines._resolve_line`: removing `case _: assert_never(line)` and `assert_never(None)` (2). `resolve` rejects a value that is not one of the five line kinds with `TypeError` before this function is called.
- `figure_ids._make`: dropping `name` from the text check (1). `name` is a fixed literal in every public function that calls `_make`, or comes from `category_id`, which returns text.

### Separators in `SelectedInputs.signature` (4)

`";"`, `","` and `"-"` replaced by `"XX;XX"`, `"XX,XX"` and `"XX-XX"` (two on the evidence-id join, one on the line join, one on the "no mortgage" marker). The signature is only compared for equality between steps, and the replacements are as unambiguous as the originals unless an evidence id literally contains `XX,XX`. Its exact format is not part of the contract, so it is deliberately unpinned.

## Gate proof (lesson from P6)

The new Python files (`tools/mutation_score.py` and `tools/tests/test_tools_mutation_score.py`) sit inside every gate:

| Gate | Before | After |
|---|---|---|
| mypy strict (`[tool.mypy] files` gains `tools`; `mypy_path` gains `tools`) | `Success: no issues found in 78 source files` | `Success: no issues found in 80 source files` |
| ruff check and format (no file list: it covers the whole workspace, and the new files are linted under the same explicit rules; `print` is banned by T20, so the script writes through `sys.stdout`) | `All checks passed!` | `All checks passed!`, `80 files already formatted` |
| pytest (`testpaths` gains `tools/tests`; `pythonpath` gains `tools`) | `pytest --co` lists none of the script's tests | `pytest --co` lists 11 tests from `test_tools_mutation_score.py` |

## Not covered, and what to do next time

- mutmut mutates only the engine package. The generator, the fixture validator and the specs runner are not in scope, as Stryker's scope was the cost engine only.
- The break score is a floor for the next change, not a target. When a survivor appears that is not wording or one of the 27 explained above, add a test; when the engine grows, rerun `make mutate`, update this report and move `MUTATION_BREAK` in the same pull request with a stated reason.
