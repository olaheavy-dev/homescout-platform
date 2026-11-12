# P3b: Python engine upfront cash, assumption selector and builder (issue #190)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) port step P3b; rules in [0039](../../decisions/0039-python-engineering-foundation.md) sections 2–4, register lines BE-11 to BE-17, BE-27 and BE-32. **Ledger:** the `P3b` rows of [`python-port-ledger.md`](../../planning/python-port-ledger.md): 109 C# tests (`AssumptionSelectorTests` 47, `HomeCostBuilderTests` 41, `UpfrontCashTests` 16, `UpfrontCashProperties` 4, `StoryCalculationCoverageTests` 1) and the four `*-upfront-cash` cases. **Builder:** Sonnet, test first; **review:** Opus before push. Builds on P2 and P3a.

## Goal
Port the rest of the C# engine: `UpfrontCash.cs`, `Evidence.cs` (`Nation`, `EvidenceStatus`, the evidence values, `EvidenceItem`, `HomeFacts`), `AssumptionSelector.cs`, `SelectedInputs.cs`, `HomeCosts.cs`, `FigureIds.cs` and `HomeCostBuilder.cs`, plus the upfront parts P3a left out of `cost_lines.py` and `breakdowns.py` (upfront order, the `upfront` flag in resolution, the upfront breakdown). After P3b the Python engine can do everything the C# engine does; P4 wires it to the generator. The C# keeps running.

## Lessons from P2 and P3a (apply from the start)
- **Red runs must be assertion failures**, not "module not found": create the module with a stub that returns a wrong value or raises `NotImplementedError` first, then show the test failing on the assertion.
- **Type-check every dataclass field in `__post_init__`** (`TypeError` for a wrong type; `tuple` of `str` for ids, never a list), and range-check any `int` that C# holds as a 32-bit `int` (`ValueError` above `2**31 - 1`), so programming errors never look like user-input failures.
- **Assert every field the C# carries**: evidence ids, statuses, partial reasons (exact tuples), periods, figure IDs, change kinds. A field no test checks can be silently wrong.
- **Self-check with mutants before reporting**: make at least 15 small deliberate breaks to the new code (wrong sign, wrong status, dropped evidence, wrong order, off-by-one, wrong figure ID, wrong scenario merge, wrong change kind, missing line shown as zero), run the tests against each, restore, and report which survived and the test you added for each survivor.

## Design notes
- Same shapes, names and **error codes** as C#, in Python style (frozen slotted dataclasses, `Enum`s whose values are the fixture ids, `match … case` with `assert_never`, `Result[...]` for expected failures).
- Figure IDs follow BE-11 exactly (`{homeId}.{scenarioId}.{section}.{name}`); scenario IDs and merging follow BE-12; differences between homes (BE-27) are **not** in scope (#96).
- Expected values only from `story-calculations.json` (by case ID, `parse_float=Fraction`) and the C# tests' literals. Port the C# test helpers that P3a didn't (`StoryCases` parts for upfront and the builder) into `tests/engine_support.py`.
- No `/`, no variable `**`, no new architecture exemption (BE-32); extend the import allow-list only with a reason.

## Tasks (each: failing test first, then code, then `make check`)
1. Upfront parts of the line types, then `upfront_cash(mode, lines) -> Result[UpfrontBreakdown]`; port `UpfrontCashTests`, `UpfrontCashProperties` and the four upfront cases.
2. `Evidence` types and `HomeFacts`.
3. `select_assumptions(...)` (the assumption selector) and `SelectedInputs`; port `AssumptionSelectorTests`.
4. `FigureIds`, `HomeCosts` types, and `build_home_costs(...)` (the builder); port `HomeCostBuilderTests`, including the end-to-end `b1-service-charge-difference` check (yearly and monthly differences).
5. `StoryCalculationCoverageTests`: every case in `story-calculations.json` is used by some test.
6. Mutant self-check (see Lessons).
7. Ledger: fill every `P3b` row.

## Acceptance
- Every P3b ledger row names a Python test that exists; every upfront case is checked by ID; error codes and figure IDs match C#.
- `make check` passes; no change to the C#, `costs.json`, CI, Makefile, `uv.lock` or `.claude/`.
