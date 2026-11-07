# 0036: Python for the backend, cost engine and AI layer

**ID:** BE-18  
**Status:** Accepted (the C# code and the docs describing it stay until the port pull request merges; partly superseded by [0039](0039-python-engineering-foundation.md): decimal inputs use `Fraction`, not `decimal`, and the proposed tools are settled there)  
**Date:** 2026-11-06  
**Stage:** 2 (reopens the stage 2 cost engine)  
**Supersedes in part:** [0019](0019-cost-engine-in-csharp.md) (the C# language choice only), [0020](0020-application-languages.md) (the backend half; the TypeScript and Next.js frontend half stands), [0021](0021-dotnet-engineering-foundation.md) (the .NET setup; its design rules are carried over, see below) and [0032](0032-own-result-type.md) (the type is rewritten in Python; the principle stands).

## Context
The founder wants to build the backend in Python, for their own learning, and wants these pieces: a Python API (FastAPI), MCP servers (FastMCP, decision 0037) and the Microsoft Agent Framework (decision 0023). The repository already holds the stage 2 C# code: about 7,600 lines in 53 `.cs` files under `packages/cost-engine/` plus the fixture validator and fixture tests under `packages/fixtures/` (cost engine, generator, tests, architecture tests, Stryker mutation testing), with tasks 1 to 5a merged and PR #38 (docs and C4 diagrams) open at the time of writing.

Decisions 0019, 0020 and 0021 are accepted, so under `AGENTS.md` this change needs a new record rather than an edit. The founder's reason, in their words: "I would rather develop this in python for my own learning experience."

What stays the same whatever the language: the rules in `AGENTS.md`, the fixtures, the JSON Schemas, the independently worked test cases, the shape of `costs.json`, and the cost engine as the only source of calculated figures (decisions 0004, 0019).

## Options
### Option A: Everything in Python (recommended)
The cost engine, generator, API, MCP server and AI layer are all Python. The C# is removed.
- **For:** one backend language, which fits the learning goal. The API, MCP server (FastMCP) and agents (Microsoft Agent Framework) all use the same engine in-process, with no language boundary to cross for any figure. FastAPI produces the OpenAPI contract that the plan already wanted. Porting is cheapest now, while the engine is small and its worked-example tests are the specification.
- Decision 0019 rejected a Python script because it "adds a third language". That no longer applies: Python replaces C# rather than joining it.
- **Against:** the merged stage 2 C# work is replaced, so the stage 2 gate is re-done on Python. Python has fewer compile-time guarantees, so the strictness decision 0021 built into the compiler must be rebuilt with type-checking and linting.

### Option B: C# cost engine, Python for the API, MCP and AI
- **For:** keeps the merged work and the strict .NET setup.
- **Against:** every figure crosses a language boundary (a service call or a subprocess), two toolchains and two sets of CI checks, and the engine would be written in a language the founder doesn't want to practise. Not recommended.

### Option C: Keep C# for the backend; Python for the MCP server only
- **For:** least rework.
- **Against:** the MCP server would still have to call the C# engine over a network, and the founder's learning goal for the API is not met. Not recommended.

## Recommendation
Option A, and do the port now rather than later.

## Decision
The founder confirmed on 6 November 2026: "Yes, full Python." Option A. The backend is Python; the frontend stays TypeScript with Next.js (0020). Microsoft Agent Framework stays the AI framework (0023) and is used through its Python package.

Carried over unchanged from 0019 and 0021 (restated in Python terms):
- The engine is a pure library: no input/output, HTTP, AI, cloud, clock or random dependencies. Dates are passed in.
- Money is a Python `int` number of pence, never a float and never `Decimal` (the output schema fixes money as integer pence). Each line is rounded once, from the exact value; a total is the sum of its rounded lines.
- **Rounding:** nearest penny, exact half-pennies rounded away from zero. The engine keeps exact whole-number (or `fractions.Fraction`) arithmetic and rounds once through a single helper: take `divmod(abs(n), abs(d))`, round up when twice the remainder is at least `abs(d)`, then restore the sign. Python's `//` and `%` round towards minus infinity, whereas C#'s truncate towards zero, so they are never used on signed money. `decimal` with an explicit `ROUND_HALF_UP` (ties away from zero) is used only to quantise a decimal input, never for chained calculations: its default precision is 28 digits, which would round a long mortgage calculation more than once. The built-in `round()` rounds halves to even and is never used. Where an official rule sets its own rounding, the calculation follows it and cites it.
- Boundary examples are written before the code (0034). Test expectations stay the independently worked examples in `packages/fixtures/test-cases/`.
- Every calculated output keeps its stable figure ID (BE-11). The register lines BE-10 to BE-17 (output file, ID format, scenarios, lines that do not apply, monthly differences, whole basis points, missing inputs, term limit) apply unchanged to the Python engine, because they describe behaviour, not language.
- A small `Result` type for expected failures; programming errors raise (0032's principle). The `Error` shape is kept: a stable code (for example `mortgage.term-too-long`), a plain-language message and a category.
- The generator writes stable JSON; running it twice gives identical files, and CI fails if regenerating changes `packages/fixtures/generated/`.

## Consequences
- **Removed when the port merges:** `HomeScout.slnx`, `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `nuget.config`, `.config/dotnet-tools.json`, `stryker-config.json`, the C# parts of `.editorconfig`, every .NET project (under `packages/cost-engine/` and `packages/fixtures/tools/` and `packages/fixtures/tests/`), and the JetBrains InspectCode step.
- **Kept:** the fixture data, schemas, test cases and generated output in `packages/fixtures/`.
- **Ported, not dropped:** the fixture validator (what `make validate` runs) and the fixture tests (story, real-data, schema-rejection, generated-output and test-case tests, about 1,700 lines). They back the stage 2 gate conditions "every input has a recorded source" and "no fixture contradicts another", so they get Python equivalents before the C# is deleted. The property-based tests (FsCheck) are ported with Hypothesis, and the architecture tests (NetArchTest, "no outside packages" from 0032) with an import check such as import-linter or a pytest over imports.
- **Port proof:** the `homes` data in `costs.json` must be identical before and after the port. Only the metadata fields that name the C# generator and cite decision 0021 may change.
- **Test naming:** `Method_condition_result` becomes `test_<method>_<condition>_<result>` (pytest needs the `test_` prefix).
- **Tooling to propose** (each is a package or tool not on the pre-approved list, so the founder approves it in the port pull request, with the licence check from 0027 and an entry in `docs/references/third-party.md`): a project and dependency manager (for example `uv`), `pytest`, `ruff`, a strict type-checker (`mypy --strict` or `pyright`), `hypothesis`, an import checker, a mutation tester (for example `mutmut`) and a JSON Schema 2020-12 validator. `make check` keeps its name and order: restore (locked), build or type-check, format-check, generated-check, validate, lint, test. Mutation testing stays outside `make check`, as now.
- **Other accepted records that name .NET and must be updated in the port pull request,** each with its Python replacement: [0024](0024-dependency-updates.md) (Dependabot checks NuGet), [0025](0025-ai-platform-capabilities.md) (Microsoft.Extensions.AI evaluation libraries, OpenTelemetry for .NET, the Aspire app host: decide how evaluation and local tracing work in Python and whether Aspire can run without a C# app host), [0026](0026-learning-first-engineering.md) (learning map), [0027](0027-stage-2-engineering-hardening.md) (NUnit, `dotnet format`, CodeQL for C#), [0029](0029-external-services.md) (.NET HTTP resilience, NUnit categories) and [0035](0035-ways-of-working-v2.md) point 9, whose pre-approved package list is .NET only. Changing a merge rule or the pre-approved list is a founder merge.
- **Register lines made obsolete** by the port: BE-07 and BE-08 (JsonSchema.Net), BE-09 (NetArchTest) and WW-13 (the NUnit licence). They get "superseded by 0036" notes.
- **CI and security, in the port pull request:** the `nuget` and `dotnet-sdk` entries in `.github/dependabot.yml` become the Python ecosystem; `dependency-submission.yml` and the NuGet licence exceptions in `dependency-review.yml` are replaced (check that it reads the Python lock file; this ties to issue #30); CodeQL is a repository setting (default setup, currently `actions` and `csharp`), so adding Python is a founder action. Keep the CI job name `make check` so the required checks on `main` don't change. `.claude/settings.json` (`dotnet tool restore`, `make inspect`, the dotnet deny rules) changes with the port, which is a founder merge.
- **Docs to correct in the port pull request:** README, `AGENTS.md` (commands, Result rule, test naming and the "C# cost engine" wording), doc 04 (stage 2 and 6 tables), the stage 2 plan, the cross-references in 0019, 0020, 0021, 0032 and 0035, the register, `docs/references/third-party.md` and the C4 diagrams (PR #38). A repository-wide search for "C#", ".NET", "NuGet", "NUnit", "Stryker" and "ASP.NET" is the pre-flight check.
- **BE-01:** the language is Python; the web framework is FastAPI, confirmed when the API is built (stage 6), unless decision 0038 pulls a small API forward.
- **PR #38 and issue #24:** don't spend more effort on the C# audit. #24 is rescoped, not dropped: its doc 03/04 corrections, C4 diagrams and whole-repository audit are not about C#, and the audit and stage gate run on Python after the port. PR #38 is merged only if its docs survive the port; otherwise they are folded into it.
- **Port order:** the Python engine test-first against the existing worked examples, then the generator, validator and fixture tests, then delete the C#. The founder merges the port, because it adds packages and changes agent permission settings.
- **Revisit if:** the Python engine can't reproduce the committed `homes` data exactly, or strict type-checking proves too weak to protect money calculations.
