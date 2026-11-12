# P6: pytest-bdd spec runner for the data scenarios (issue #193)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) item 4 and port step P6; [0043](../../decisions/0043-specification-format.md) (IDs, tags, wording unchanged); register line SP-03 (two runners split by tag). **Ledger:** the `P6` rows of [`python-port-ledger.md`](../../planning/python-port-ledger.md) (26 C# tests in `DataStepsTests` and `SpecDataTests`). **Builder:** Sonnet, test first; **review:** Opus before push.

## Goal
Run every scenario in `docs/specs/` that is **not** tagged `@ui`, `@mcp` or `@withdrawn` with **pytest-bdd** in `make test`, with the same seven data steps as `packages/specs/Vestagraph.Specs.Tests/DataSteps.cs` (wording exactly as `docs/specs/README.md` lists it). The Reqnroll project stays until P8.

## The package
`pytest-bdd` (9.0.1, MIT, pytest-dev; pre-approved by 0049 item 4) added to the root `dev` dependency group with `uv add --dev "pytest-bdd>=9.0.1,<10"`, which needs the founder-approved command prompt. Its dependencies (`parse`, `parse-type`, `gherkin-official`, `Mako`, `packaging`, `typing_extensions`) pass the licence gate in the PR's dependency review; add a `third-party.md` row with the official documentation link (https://pytest-bdd.readthedocs.io/en/stable/). A `0.x` direct dependency would join the `uv-zero-x` Dependabot group; pytest-bdd itself is 9.x.

## The three proofs (0049 item 4; if one fails, stop and report: it goes back to the founder)
1. **Scenario ID in the test name:** `pytest -k COSTS_02` (or the ID as written) selects exactly that scenario, and the test report names it.
2. **`Rule:` blocks:** a scenario inside a `Rule:` runs and keeps its tags (prove with a small feature file under the tests folder, since `docs/specs/` has no `Rule:` yet).
3. **Feature files outside the package:** the tests load `docs/specs/**/*.feature` from the repository root without copying them into the package.

## Design
- Package: a new small workspace member `packages/vestagraph-specs` (src layout like the others, depends on `vestagraph-engine`? **No**: like the C# specs, steps read the committed `costs.json` and `packages/fixtures/data/` only), or tests-only under `packages/vestagraph-specs/tests/` if no source is needed. Unique module names.
- Tags become **strict pytest markers** registered in `pyproject.toml` (`ui`, `mcp`, `withdrawn`, `screen`, `buying`, `renting`, …; unknown tags fail under `strict = true`); `make test` adds `-m "not ui and not mcp and not withdrawn"`.
- A scenario citing an ID missing from `costs.json` or the data fails with a message naming the ID; an undefined step fails the scenario.
- `docs/specs/README.md` "Running the specifications" gains the Python command (`uv run --locked pytest -m "..." packages/vestagraph-specs`) beside the Reqnroll one until P8; `AGENTS.md` "Commands" `make test` row mentions pytest-bdd.

## Tasks (test first, red runs as assertion failures)
1. Add pytest-bdd; prove the three items above first.
2. Port `SpecData` and its tests (`SpecDataTests`).
3. Port the seven data steps and `DataStepsTests` (each step's failure message for a missing ID, wrong status, an amount where none should be, a missing evidence ID).
4. Wire the real `docs/specs` scenarios; `make test` runs them with the marker filter.
5. Mutant self-check (≥ 8, `PYTHONDONTWRITEBYTECODE=1`): step text changed, status compared loosely, "shows no amount" accepting 0, evidence existence not checked, step range accepted outside `fromStep..toStep`, marker filter dropped.
6. Ledger: fill every `P6` row; docs above.
