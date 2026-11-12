# P4: Python generator with the port proof (issue #191)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) port step P4; rules in [0039](../../decisions/0039-python-engineering-foundation.md) sections 1–5, register lines BE-10 to BE-13 and BE-31. **Ledger:** the `P4` rows of [`python-port-ledger.md`](../../planning/python-port-ledger.md) (37 C# tests in `OutputShapeTests`, `RunTests`, `WorkedCaseTests`). **Builder:** Sonnet, test first; **review:** Opus before push. Builds on the finished Python engine (P2–P3b).

## Goal
Port the C# generator (`packages/cost-engine/src/Vestagraph.CostEngine.Generator/`: `Program.cs`, `FixtureReader.cs`, `CostsGenerator.cs`, `CostsDocument.cs`) to `packages/vestagraph-generator`, and switch `make generate` to it. **Port proof:** regenerating `packages/fixtures/generated/costs.json` with Python changes **no byte** (BE-31 made the header language-neutral in PC). If any byte moves, the engine or generator is fixed, never the expectations or the committed file; stop after 3 attempts.

The P3b review's throwaway comparison script (reads the fixtures as `FixtureReader` does, runs `build_home_costs`, serialises with `json.dumps(indent=2, ensure_ascii=False)` plus a final newline) already reproduced the file byte for byte; use it as a reference, not as code to paste unreviewed.

## Design
- `vestagraph_generator/`: `fixture_reader.py` (reads `packages/fixtures/data/` with `json.loads(text, parse_float=Fraction)`; never a `float`), `costs_document.py` (the output shape, keys in the contract's order), `costs_generator.py` (calls the engine, maps results; same error handling as C#: a covered home in no story, or in two, fails with its code; invalid data raises instead of writing guesses), `__main__.py` (`python -m vestagraph_generator [repo-root]`, same exit codes and messages as `Program.cs`; deletes any other `*.json` in `generated/`, as BE-10 says the generator owns the folder).
- Imports: the engine and the standard library only (`json`, `pathlib`, `sys`, `fractions`, `dataclasses`, `enum`, `typing`, `collections.abc`). A test checks the generator imports no third-party package (extend the existing metadata test).
- Output: LF line endings, two-space indent, one final newline, keys in the order of `generated-costs.schema.json`; no `float` anywhere (a test walks the output).
- **Makefile:** `generate` runs `uv run --locked python -m vestagraph_generator`. The C# generator stays (removed at P8) and its own test `CommittedCostsFile_matchesWhatTheGeneratorProduces` keeps proving the C# output equals the committed file, so until P8 **both** generators are proven against the same bytes on every `make check`.
- **Docs:** `AGENTS.md` "Commands" (`make generate` now runs the Python generator), the architecture page's generator row, and `docs/specs`/README only if they name the generator command.

## Tasks (each: failing test first, red run shown as an assertion failure)
1. Fixture reader, with tests for the bad-data cases (`RunTests`: missing file, list where an object is expected, text where a number is expected, unknown evidence status, a quantity in other units).
2. Costs document and generator mapping; port `OutputShapeTests` and `WorkedCaseTests` (worked cases read by ID from `story-calculations.json`).
3. Command line `__main__` and the run behaviour (twice gives identical text; deletes other JSON files; exit codes).
4. **Port proof test:** run the generator into a temporary folder and compare its bytes with the committed `costs.json` (the Python version of `CommittedCostsFile_matchesWhatTheGeneratorProduces`).
5. Switch `make generate`; run `make generate` and confirm `git status` shows no change to `packages/fixtures/generated/`.
6. Mutant self-check (at least 10, with `PYTHONDONTWRITEBYTECODE=1`): key order, a float slipping in, wrong scenario order, a dropped left-out-line rule, wrong exit code, CRLF, missing final newline.
7. Ledger: fill every `P4` row; update the docs listed above.

## Acceptance
- `make generate` uses Python and leaves `costs.json` byte-identical; `make check` passes (both generators proven).
- Every P4 ledger row names a Python test that exists.
- No change to the C#, `costs.json`, the fixtures, CI, `uv.lock` or `.claude/`.
