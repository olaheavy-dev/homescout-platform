# 0042: Back to .NET: C# 15 on .NET 11 for the backend, React stays for the frontend

**ID:** BE-24  
**Status:** Superseded by [0049](0049-back-to-python-final.md) (founder, 12 Nov 2026: "Switch to python"); its frontend stack, frontend packages, prerelease rule, `0.x` minor-bump rule and BE-22 gate are carried over. Had been accepted on 10 Nov 2026, with upgrade conditions amended by register line BE-25  
**Date:** 2026-11-10  
**Stage:** 2 (reopens the backend language choice before the port went past step P1)  
**Supersedes (no older text is rewritten):**
- fully: [0036](0036-python-backend.md) (Python backend), [0039](0039-python-engineering-foundation.md) (Python engineering foundation), [0040](0040-fastapi-template-as-api-starting-point.md) (the FastAPI template as the API starting point) and [0041](0041-maf-gateway-built-in-the-template.md) (the MAF gateway built in the template first), and the register lines that only served the port: BE-21, BE-22's Python exemptions, BE-23;
- in part: [0021](0021-dotnet-engineering-foundation.md) (the SDK and target framework move from .NET 10 to .NET 11 when the upgrade conditions below are met; everything else stands), [0023](0023-microsoft-agent-framework.md) (Microsoft Agent Framework is used through its .NET packages), [0035](0035-ways-of-working-v2.md) point 9 (the pre-approved package list gains the packages below), [0037](0037-mcp-server-and-agent-integrations.md) (Proposed; the MCP server uses the official MCP C# SDK, not FastMCP) and [0038](0038-accounts-and-api-keys-for-mcp.md) (Proposed; token checks use ASP.NET Core authentication, not FastMCP's verifier).

## Context
On 6 November 2026 decision 0036 moved the backend to Python "for my own learning experience". Only port step P1 (the Python tooling, PR #49) merged; the C# cost engine, generator, validator, tests and mutation testing are still in the repository and still pass `make check`. Decisions 0019, 0020, 0021 and 0032 were only to be superseded "when the port merges", which never happened.

On 10 November 2026 .NET 11 and C# 15 were released. The founder reviewed what they add (union types, closed hierarchies, ASP.NET Core 11, the .NET AI stack with Microsoft Agent Framework, the MCP C# SDK and AG-UI) and decided, in their words: "want to learn .NET more than Python AND ALSO the .NET 11 features." Asked whether the frontend should move to Blazor, the founder chose to keep React, because AG-UI events work with React too (the reasons are in the options below), and then: "Approved all the necessary packages that you need."

## Options
### Option A: C# on .NET 11 for the backend, React and Next.js for the frontend (chosen)
- **For:** the founder learns the language they want; the merged C# engine and its strict setup are kept, so nothing is ported; one backend language covers the cost engine, the API (ASP.NET Core), the MCP server (official C# SDK) and the agents (Microsoft Agent Framework for .NET, version 1.x stable). React keeps the larger ecosystem, the design skills' examples (0031) and the most mature AG-UI client (CopilotKit). Decision 0020's frontend half stands unchanged.
- **Against:** two languages (C# and TypeScript); TypeScript types must be generated from the API's OpenAPI document. The Python tooling from P1 is removed. The founder's FastAPI template is no longer HomeScout's starting point (it stays its own project).

### Option B: C# on .NET 11 everywhere, with Blazor for the frontend
- **For:** one language; the same C# types on both sides; the .NET 11 Blazor AI components.
- **Against:** those components are experimental throughout .NET 11; React has the larger component and design ecosystem and is the more marketable frontend skill; AG-UI works with React, so the agent chat does not need Blazor. Not chosen.

### Option C: stay with Python (0036)
- **For:** no change of direction.
- **Against:** the founder now prefers to learn .NET. Not chosen.

## Recommendation
Option A.

## Decision
Option A.

**Language and runtime.** The backend is C# on .NET. The target is **.NET 11 with C# 15**, adopted through one upgrade pull request when the conditions below hold; until then the code stays on .NET 10 (`global.json` `10.0.x`, `net10.0`), which is supported until November 2028, the same month as .NET 11. Plan the move to .NET 12 (the next long-term release, November 2027) during 2028.

**Upgrade conditions** (all must hold before the upgrade pull request merges):
1. **CodeQL** supports .NET 11 and C# 15. On 10 November 2026 its supported-languages page lists C# 14 and .NET 10 as the highest supported versions. CodeQL is a required stage 2 security check, so the upgrade waits for it rather than weakening the check.
2. **JetBrains InspectCode** (ReSharper command line tools 2026.3 or later; JetBrains' [What's New in ReSharper 2026.3](https://www.jetbrains.com/resharper/whatsnew/) claims full C# 15 support; the repository pins 2026.2, so the upgrade bumps it) and **Stryker.NET** both run cleanly on the upgraded code. Stryker.NET does not yet state C# 15 support; if it cannot parse C# 15, the cost engine does not use C# 15 syntax until it can.
3. `packages/fixtures/generated/costs.json` is **byte-identical** after regeneration, and every independently worked test passes **without editing an expectation**. .NET 11 changes `Math.Round(double, digits)` and `decimal`/`double` conversions; the engine uses only `Math.Round(decimal, …)`, no `double`, and never converts `BigInteger` to a floating-point type, so no figure should move. If one does, stop and report.

**Rules for new .NET 11 and C# 15 features** (detail in the [adoption plan](../planning/dotnet-11-and-csharp-15-plan.md)):
- Stable language and library features may be used where they make the code clearer or safer; each first use is explained in the pull request's "Concepts to learn".
- **Preview language or runtime features are not used** in merged code (for example Runtime Async, the updated memory-safety rules).
- **Prerelease or experimental packages** are used only in the AI layer, behind HomeScout's own adapter (0029), pinned to an exact version, and never on the path that produces a calculated figure. Alpha packages are not used.
- Money stays `long` pence with `decimal` only for exact inputs, as 0021 and 0034 set; the new `Decimal32`/`Decimal64`/`Decimal128` types are not used for money.

**Backend stack** (built at stage 6 unless a later decision brings a piece forward): ASP.NET Core minimal APIs with the OpenAPI 3.2 document checked into the repository; Aspire and OpenTelemetry for local tracing (0025); the official MCP C# SDK for the MCP server (0037); Microsoft Agent Framework for .NET for agents and workflows (0023), with OpenAI and Anthropic model providers behind HomeScout's adapter; AG-UI hosting so the React frontend can stream agent replies, tool calls and approval requests.

**Frontend stack:** TypeScript with Next.js and React (0020, unchanged). The agent chat uses CopilotKit through its open-source runtime route in Next.js, connected to the .NET AG-UI endpoint; CopilotKit's direct "self-managed agents" mode is an Enterprise-tier feature and is not used. TypeScript types for API data are generated from the OpenAPI document, never hand-written.

**Pre-approved packages** (founder, 10 Nov 2026; adds to 0035 point 9, which already lists Aspire, OpenTelemetry, Microsoft Agent Framework, Microsoft.Extensions.AI and its evaluation libraries, and Npgsql if DA-03 confirms PostgreSQL). Each still passes the 0027 licence allow-list (a package that fails it goes back to the founder) and gets a `docs/references/third-party.md` entry when first added; exact versions are pinned in lock files at that time, after checking the official documentation for that version:
- **.NET:** the Microsoft Agent Framework packages (`Microsoft.Agents.AI` and its `.Abstractions`, `.OpenAI`, `.Anthropic`, `.Workflows`, `.Hosting`, `.Hosting.AspNetCore` and `.Hosting.AGUI.AspNetCore` packages; the three hosting packages are prerelease on 10 Nov 2026, so the prerelease rule above applies to them), `ModelContextProtocol` and `ModelContextProtocol.AspNetCore`, the AG-UI .NET packages (`AGUI.Client`, `AGUI.Server`, `AGUI.Abstractions`) if the hosting package needs them directly, the official `Anthropic` and `OpenAI` SDKs, `Microsoft.AspNetCore.OpenApi`, `Scalar.AspNetCore` (API reference page, development only), `Microsoft.AspNetCore.Mvc.Testing` (API tests), and the .NET 11 SDK's `mcpserver` template.
- **Frontend:** `next`, `react`, `react-dom`, `typescript`, `@copilotkit/react-core`, `@copilotkit/runtime`, `@ag-ui/client` (at the exact version CopilotKit pins) and an OpenAPI-to-TypeScript generator.
- **Packages chosen by a later decision** (FE-02 styling and components, FE-03 maps and charts, FE-04 frontend testing, DA-03 database) are pre-approved once that decision record names them, under the same licence and documentation checks.

**Carried over unchanged:** everything 0036 said stays the same whatever the language (the rules in `AGENTS.md`, the fixtures, schemas, worked test cases, the shape of `costs.json`, the cost engine as the only source of calculated figures); the 8 Nov 2026 rule that a minor bump of a direct `0.x` dependency or action pin counts as a major bump (from 0039 Q3; the live rule is in `AGENTS.md`); and the dependency-review step that fails on packages with no detectable licence (BE-22, issue #30), which stays for NuGet and npm.

## Consequences
- **Python tooling removed** in one founder-merged chore pull request: `pyproject.toml`, `uv.lock`, `.python-version`, `packages/homescout-*`, the Python steps in the Makefile (`lint`, uv in `restore`, mypy in `build`, ruff in `format-check`, pytest in `test`, Python caches in `clean`, the `requirements` targets), `setup-uv` in CI, the `uv` Dependabot entry and its groups, the PyPI exemptions in `dependency-review.yml`, and the Python rules in `.claude/settings.json`. `AGENTS.md` "Commands", the README and `third-party.md` change in the same pull request, so the documented commands always match the Makefile. Until it merges, the Python steps keep running and the documents keep describing them.
- **Issue #42** (the port plan) is closed as not planned. **Issue #24** (stage 2 close-out) returns to its C# scope: doc 03/04 corrections, C4 context and container diagrams (C# engine, Next.js frontend, planned ASP.NET Core API), Stryker.NET report and the stage 2 audit.
- **Backlog:** the ordered tickets for this decision, the stage 2 close-out and stages 3 to 6 are listed in [`docs/planning/backlog.md`](../planning/backlog.md), with milestones per stage.
- **CodeQL:** default setup covers `actions`, `csharp` and `python` (checked 10 Nov 2026). When issue #57 removes the Python code, the founder removes `python` from the default setup in the repository settings (a founder-only change).
- **The founder's FastAPI template** stays a separate project; HomeScout no longer imports it, and `AGENTS.md`'s exception for it is withdrawn.
- **Revisit if:** CodeQL still lacks .NET 11 support at the stage 2 gate (then the gate passes on .NET 10 and the upgrade follows later), or Stryker.NET cannot handle C# 15 by the time the engine needs a C# 15 feature.
