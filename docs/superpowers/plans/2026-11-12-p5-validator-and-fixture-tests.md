# P5: Python fixture validator and fixture tests (issue #192)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) port step P5; rules in [0039](../../decisions/0039-python-engineering-foundation.md) sections 1 and 4, [0018](../../decisions/0018-fixture-data-format.md) (fixture format) and register line BE-07 (JSON Schema 2020-12 validator). **Ledger:** the `P5` rows of [`python-port-ledger.md`](../../planning/python-port-ledger.md): 191 C# tests (`AreaDataTests` 43, `AreaSchemaRejectionTests` 45, `GeneratedCostsSchemaTests` 33, `RealDataTests` 23, `SchemaRejectionTests` 28, `StoryTests` 10, `TestCaseFileTests` 9). **Builder:** Sonnet, test first; **review:** Opus before push.

## Goal
Port the C# validator (`packages/fixtures/tools/Vestagraph.Fixtures.Validator/`: `FixtureValidator.cs`, `Program.cs`) to `packages/vestagraph-fixture-validator` using `jsonschema` and `referencing` (already locked, 0039 §6), switch `make validate` to it, and port the fixture tests (`packages/fixtures/tests/Vestagraph.Fixtures.Tests/`) to Python. The C# validator and tests stay until P8.

## Parity is the whole job
`make validate` must accept and reject **exactly the same files** as the C# validator (JsonSchema.Net, 2020-12). Settle and test each of these before writing the rest:
- **Dialect and references:** every schema is validated as 2020-12; `$ref` across files in `packages/fixtures/schema/` resolves through a `referencing.Registry` built from the schema files' `$id`s (no network access, ever; an unknown `$ref` is an error).
- **`format`:** find out whether the C# validator asserts formats (for example `date`) or treats them as annotations, and do the same. If C# asserts them, use jsonschema's `FormatChecker` for exactly those formats and test a bad date being rejected; if it doesn't, test that the Python doesn't either. Record the answer in the plan's "Findings" and the PR.
- **Numbers:** read data with `json.loads(text, parse_float=Fraction)` so decimals stay exact for `minimum`, `maximum` and `multipleOf`. Check that jsonschema treats a `Fraction` as a JSON number and a whole-valued decimal (`5.0`) the same way JsonSchema.Net does for `"type": "integer"`; test both. If jsonschema needs a custom type checker for `Fraction`, add the smallest one with a comment.
- **Which file gets which schema:** the same mapping as `FixtureValidator.cs` (data, test-cases, generated), and the same treatment of a file with no schema.
- **Output and exit codes:** the same problem lines (file, JSON pointer, message) and exit codes as `Program.cs`, so `make validate` reads the same. Message wording may differ where the libraries differ; tests match on file, pointer and keyword, not on library wording.

## Design
- `vestagraph_fixture_validator/`: `validator.py` (load schemas, build the registry, validate one file, validate the tree), `__main__.py` (`python -m vestagraph_fixture_validator [repo-root]`). Imports: `jsonschema`, `referencing` and the standard library; **never** the engine (a metadata test already checks the dependency; add an import check like the generator's).
- Fixture tests go in `packages/vestagraph-fixture-validator/tests/` with unique `test_fixtures_*.py` names; shared helpers in a uniquely named module added to `[tool.pytest] pythonpath`.
- Data tests (`RealDataTests`, `AreaDataTests`, `StoryTests`) check the fixture data itself; port each assertion with its own expected literal from the C# test. Never edit a fixture or schema to make a test pass; a disagreement is a finding to report.
- **Makefile:** `validate` runs `uv run --locked python -m vestagraph_fixture_validator`. `AGENTS.md` "Commands" (`make validate` row), the architecture page and register line BE-07 (its "JsonSchema.Net" now has a Python counterpart until P8) are updated.

## Tasks (each: failing test first, red run shown as an assertion failure)
1. Parity probes: dialect, cross-file `$ref`, `format`, decimals and integers (above). Write the findings down.
2. Validator and command line; port `SchemaRejectionTests`, `AreaSchemaRejectionTests`, `GeneratedCostsSchemaTests`, `TestCaseFileTests`.
3. Data tests: `RealDataTests`, `AreaDataTests`, `StoryTests`.
4. **Parity proof:** run both validators on the real tree (both pass) and on every bad sample the rejection tests use (both reject); a test asserts the Python result per sample.
5. Switch `make validate`; docs above.
6. Mutant self-check (at least 10, `PYTHONDONTWRITEBYTECODE=1`): wrong schema for a folder, `$ref` not resolved, format not checked (or checked when C# doesn't), decimal read as float, a skipped file, wrong exit code.
7. Ledger: fill every `P5` row.

## Acceptance
- Both validators accept the real tree and reject the same bad samples; `make validate` uses Python; `make check` passes.
- Every P5 ledger row names a Python test that exists.
- No change to fixtures, schemas, `costs.json`, the C#, CI, `uv.lock` or `.claude/`.

## Findings
Found by running JsonSchema.Net 9.6.0 (the C# validator's library) and jsonschema 4.26.0 / referencing 0.37.0 on the same cases, 12 Nov 2026. Each is pinned by a test in `test_fixtures_parity_probes.py`; the C# answers were measured, not assumed.

- **`format`:** none of the schemas uses `format`, and JsonSchema.Net does not assert it (`"format": "date"` accepts `"not-a-date"`, and the same for `email`, `uri` and `date-time`). jsonschema also skips it unless given a format checker, and none is given. The two agree; four probes prove it, and a mutant that adds the format checker is caught.
- **Integers and decimals:** JsonSchema.Net treats `5.0` and `1e2` as integers and compares decimals exactly (`maximum 0.3` rejects `0.30000000000000004`; `multipleOf 0.01` accepts `19.99`). jsonschema's default `integer` type would reject `Fraction(5)`, so the validator reads JSON with `parse_float=Fraction` and redefines the `integer` type to accept a number with no fractional part. Eighteen probes cover it, including `true` (not an integer) and a 30-digit integer.
- **`$ref`:** every `*.schema.json` is registered in a `referencing.Registry` under its `$id`; nothing is fetched. A reference to a missing schema raises `Unresolvable` in jsonschema (a crash with `RefResolutionException` in C#); the validator reports it as a problem instead. A schema file that cannot be read is also a problem, not a crash.
- **`pattern`:** .NET (ECMAScript mode) makes `\d` ASCII only, so `^\d+$` rejects Arabic-Indic and full-width digits; Python's `re` accepts them. The validator searches with `re.ASCII`. `$` also matches before a final newline in both. Not covered: other ECMAScript-versus-Python regex syntax differences (the schemas use only `^ $ \d \S [..] ( ) | ? * + {n,m}`).
- **Pointer of a `false` subschema (a real jsonschema 4.26 bug):** an error from `"value": false` under `properties` loses the property name, so the problem was reported at the parent (`/evidence/0`) instead of `/evidence/0/value`. The validator replaces `properties` with a copy that adds the name. A test fails if a schema ever puts `false` under another keyword that adds a path part.
- **Problem lines:** C# lists a problem at every ancestor of the failing value (`/`, `/homes`, `/homes/0`, ...); jsonschema reports the failing value only. The tests and `make validate` read the same (file, pointer, keyword), the Python list is shorter, and every C# deepest pointer equals or sits under a Python pointer (checked on all 140 samples). Messages use jsonschema's wording; fractions are shown as written (`240000.5`).
- **Reading the file:** same as C#: a byte-order mark is ignored, bytes that are not UTF-8 are replaced (not rejected), trailing commas, comments, `NaN` and `Infinity` are "Not valid JSON", and `"$schema": null` counts as absent.
- **Command line:** `[repo-root]` as in the generator (the C# tool took the `packages/fixtures` folder itself); the repository is found by `packages/fixtures/schema`, not by `Vestagraph.slnx`, which P8 removes. Exit codes are the same: 0 valid, 1 problems, 2 repository not found.
- **Left as in C#, not ported:** a nesting deeper than 64 levels is "Not valid JSON" in C# and parses in Python; a lone surrogate escape crashes C# and parses in Python; a schema with an unknown type or an invalid pattern crashes C# and raises in Python. None occurs in the fixtures.
- **Dead branch not ported:** C# `ValidateFile` had a `Missing.` case that cannot be reached (a file with no schema name returns earlier); a mutant proved it could not change any result.

**Parity proof (task 4).** 140 samples (every bad or good sample the rejection and costs tests build): the C# validator CLI and the Python one agree on all 140 (116 rejected by both, 24 accepted by both), and both accept the real tree. Per-sample assertions are the Python tests themselves.

**Mutant self-check (task 6).** 28 mutants (22 validator, 6 data), all killed; see the pull request.
