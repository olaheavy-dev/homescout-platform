# P7: mutation testing with mutmut (issue #194)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) item 11b and port step P7; [0039](../../decisions/0039-python-engineering-foundation.md) section 4 (mutation testing); register line BE-26 (survivors kept and explained), which this step supersedes with a mutmut line. **Builder:** Sonnet; **review:** Opus before push. No ledger rows (P7 ports a tool, not tests).

## Goal
`make mutate` runs **mutmut** (3.8.1, already in the `dev` group) on the Python cost engine (`packages/vestagraph-engine/src/vestagraph_engine/`), the same scope Stryker.NET covers today (the C# engine). It stays **out of `make check` and CI** (slow, run by hand when the engine or its tests change), and fails below a **break score** set just below the first measured run. Stryker.NET moves to `make mutate-dotnet` until P8 removes it.

## Rules (0049 item 11b, 0039 §4)
- **Repeatable score:** Hypothesis is derandomised during the run. The simplest documented route is to run mutmut with `CI=true`, which makes Hypothesis load its built-in `ci` profile (`derandomize=True`, no deadline, no database); confirm in the locked Hypothesis source (`_settings.py`, `is_in_ci`) that this holds inside mutmut's test runs, and that no profile named `ci` is registered by us.
- **Break score:** mutmut has no built-in pass mark, so a small script (`packages/vestagraph-engine/tests/` is not the place: put it in a tools location the plan's review agrees, e.g. `tools/mutation_score.py`, with its own tests) reads mutmut's results (`mutmut export-cicd-stats` or the results files; check what **3.8.1** actually provides in `.venv`, not the latest docs) and fails when `killed / (killed + survived)` is below the break score. Timeouts and "suspicious" mutants count as stated in the report.
- **Survivors explained:** every surviving mutant is either killed by a new test (preferred, test first) or explained in a new report `docs/reviews/2026-11-12-python-mutation-report.md` as equivalent (no behaviour change), unreachable defensive code, or deliberately unpinned wording, following BE-26's principle. Never change engine behaviour to kill a mutant.
- **Same platform note:** mutmut needs `fork` (macOS and Linux; Windows through WSL), as 0039 says.

## Design
- `[tool.mutmut]` in the root `pyproject.toml`, with the option names **as 3.8.1 reads them** (check `.venv/.../mutmut` source: `paths_to_mutate` vs `source_paths`, `tests_dir` vs `pytest_add_cli_args_test_selection`, `also_copy`, `do_not_mutate`). Test selection: the engine's tests only (`packages/vestagraph-engine/tests`), so the score measures the engine's own suite.
- mutmut writes a `mutants/` folder (already git-ignored, P1); `make clean` already removes it.
- **Makefile:** `mutate: restore` runs `CI=true uv run --locked mutmut run` (or the 3.8.1 equivalent) then the score script; `mutate-dotnet` keeps today's Stryker command and `MUTATION_REPLAY`. `help` text updated.
- **Docs:** `AGENTS.md` "Commands" (`make mutate` row, plus `make mutate-dotnet` until P8), `third-party.md` mutmut row ("from P7"), register: **BE-33** (new line: mutmut on the Python engine, break score N, first run's score, survivors in the new report; supersedes BE-26) and BE-26's status to "Superseded by BE-33 (P7, #194)"; 0039 §4 is unchanged (it already says mutmut).
- **Gate proof (lesson from P6, agent-workflows#10):** the report states, with the commands' output, that mypy, ruff and pytest cover any new Python file (mypy "N source files" before and after).

## Tasks
1. Read mutmut 3.8.1's configuration and result-reading code in `.venv`; write findings into this plan's "Findings".
2. Score script with tests (test first: fails below the break, passes at or above, handles zero mutants as a failure, reports the numbers).
3. `[tool.mutmut]`, Makefile targets; first full run; record killed, survived, timeout, suspicious, the score and run time.
4. For each survivor: add a test (red against the mutant, then green) or explain it in the report.
5. Set the break score just below the final measured score; run `make mutate` twice to show the score is the same both times.
6. Docs and register lines above; `make check` passes (mutate is not in it).

## Acceptance
- `make mutate` runs mutmut on the Python engine, prints the score and fails below the break; two runs give the same score.
- Every survivor is killed by a test or explained in the report; BE-33 recorded; BE-26 superseded.
- `make check` passes; no change to engine behaviour, the C#, fixtures, `costs.json`, CI, `uv.lock` or `.claude/`.

## Findings
Checked in the installed mutmut 3.8.1 (`.venv/lib/python3.14/site-packages/mutmut`), not the online docs.

- **Configuration** (`configuration.py`, read from `[tool.mutmut]` in the `pyproject.toml` of the **current folder only**, else `setup.cfg`): `source_paths` (`paths_to_mutate` is deprecated), `pytest_add_cli_args_test_selection` (`tests_dir` is deprecated), `pytest_add_cli_args`, `also_copy` (always adds `tests/`, `test/`, `pyproject.toml`, `uv.lock` and the like), `only_mutate`, `do_not_mutate`, `timeout_multiplier` (15.0), `timeout_constant` (1.0), `type_check_command`, `process_isolation` (`fork` default), `use_git_change_detection`, and others. Defaults are guessed from `lib/`, `src/` or a folder named like the current one.
- **Layout constraint:** a mutant is named from the source path relative to the current folder with a leading `src.` stripped, and the trampoline records the module name the tests import. The two must match or every mutant is "no tests" ("Stopping early, because we could not find any test case for any mutant"; attempt 1 from the repository root hit this). So mutmut runs in `packages/vestagraph-engine` with `source_paths = ["src/vestagraph_engine"]`, and the settings live in that package's `pyproject.toml`, not the workspace root (a deviation from the plan's root `[tool.mutmut]`). `mutants/` is created inside that folder (already ignored by `mutants/` in `.gitignore`).
- **Source-reading test:** the architecture purity test reads the source text, which mutmut has rewritten, so it fails on every mutant ("Failed to run clean test" / stats collection fails, attempt 2). It is deselected through `pytest_add_cli_args`.
- **Running:** `mutmut run [names]` (exit 0 even with survivors; `--max-children`), results are cached per mutant in `mutants/**.meta`, so `make mutate` deletes `mutants/` first. A named rerun (`mutmut run <mutant>`) prints each result.
- **Reading results:** `mutmut results` (lists everything except killed, **timeouts included**), `mutmut show <mutant>` (diff), and `mutmut export-cicd-stats`, which exists in 3.8.1 and writes `mutants/mutmut-cicd-stats.json` with `killed`, `survived`, `total`, `no_tests`, `skipped`, `suspicious`, `timeout`, `check_was_interrupted_by_user`, `segfault` (no `caught_by_type_check`). There is no pass mark. Exit codes map in `stats.py`: 1 and 3 killed, 0 survived, 33 and 5 no tests, 36/24/-24/152/255 timeout, 35 and any unknown code suspicious, -9/-11 segfault.
- **Hypothesis:** `hypothesis/_settings.py` registers a `ci` profile (`derandomize=True`, `deadline=None`, `database=None`, `print_blob=True`, `suppress_health_check=[too_slow]`) and loads it at import when `is_in_ci()` is true: any of the `_CI_VARS` environment variables is set (`CI` with any value, `GITHUB_ACTIONS=true`, and so on). The environment is inherited by mutmut's forked workers, so `CI=true uv run mutmut run` derandomises every test run. Checked: `CI=true` gives profile `ci`, no `CI` gives `default`. No profile named `ci` is registered anywhere under `packages/`.
- **Result:** first run 1698 killed, 2 timeout, 302 survived of 2002 (84.92%, 33 s); final 85.36% after 9 survivors were killed; two runs identical. Details in `docs/reviews/2026-11-12-python-mutation-report.md`.
