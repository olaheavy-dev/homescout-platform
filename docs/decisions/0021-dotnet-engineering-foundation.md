# 0021: .NET engineering foundation

**ID:** BE-04  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2

## Context
The founder supplied earlier projects as foundations to build on and improve, not copy. A review of them (summarised in [the foundations review](../reviews/2026-10-23-foundation-review.md)) found that the newest .NET project already fixes many problems in its predecessor. The first C# code in HomeScout is the stage 2 cost engine (decision 0019), so its build and test setup is needed now.

## Options
- **Adopt the newer foundation's .NET setup, rewritten under HomeScout names (chosen):** strict and reproducible from the first commit; agent mistakes fail early.
- **Same setup with xUnit:** more common in .NET, but differs from the founder's other projects.
- **Lighter setup:** faster to start; mistakes caught later.

## Recommendation
Adopt the newer foundation's setup.

## Decision
The founder chose to adopt it. All files are written fresh for HomeScout; nothing is copied from the private repositories.

Build and packages:
- `global.json` pins the .NET 10 SDK; `HomeScout.slnx` solution at the repository root.
- `Directory.Build.props`: target net10.0, nullable reference types, `AnalysisMode=All`, warnings as errors, code style enforced in build, deterministic builds, invariant globalisation, NuGet audit.
- `Directory.Packages.props`: central package management with transitive pinning and exact versions; lock files committed and restored in locked mode in CI.
- `nuget.config` clears inherited sources and maps packages to nuget.org only.
- A `Makefile` is the single entry point (`make check`, `make test`, `make generate`); CI runs the same commands.
- No MediatR and no SonarAnalyzer (both have licence restrictions).

Cost engine design:
- Pure library: no input/output, HTTP, AI, Azure, clock or random dependencies. Dates are passed in as `DateOnly`.
- Money is a `Pence` value type over whole pence (integer). Each cost line is rounded once; a total is the sum of its rounded lines.
- Every calculated output carries a stable ID (for example `CostLineId`), so later AI features can only quote figures that exist (decisions 0004, AI-01 to AI-05).
- A `Result` type only where inputs can legitimately fail; programmer errors throw.
- The generator writes JSON with stable key order; running it twice produces identical files, and CI fails if regenerating changes `packages/fixtures/generated/`.

Tests:
- NUnit with its analysers. Test names follow `Method_condition_result`.
- Data-driven tests read the independently worked examples in `packages/fixtures/test-cases/` (decision 0019).
- Architecture tests (NetArchTest) enforce the cost engine's no-dependency rule.

## Consequences
- The first implementation pull request adds these files and NuGet test packages; adding dependencies is a founder merge.
- `AGENTS.md` gains the commands and the test naming rule when that pull request lands.
- The API (stage 6) follows the same foundation: ASP.NET Core minimal APIs, one OpenAPI stack, Problem Details errors, referencing the cost engine directly.
