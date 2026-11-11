# .NET 11 and C# 15 adoption plan

**Decision:** [0042](../decisions/0042-back-to-dotnet-11.md) (back to .NET; React stays). **Written:** 10 Nov 2026, the day .NET 11 shipped, by the Opus planner. **Ordered tickets:** [backlog](backlog.md).

Every feature below was checked against Microsoft's official pages on 10 Nov 2026 (sources at the end). Package versions are the latest on nuget.org or npm that day, for orientation only: each pull request that adds a package checks its documentation and pins the version then. Anything not confirmed is marked **unverified**.

## 1. In one paragraph
Vestagraph keeps its C# cost engine and moves to .NET 11 in two steps (register line BE-25, founder, 10 Nov 2026). The SDK and runtime move now, in issue #58, with the language pinned at C# 14 (`LangVersion` 14), so CodeQL, which lists C# 14 but not yet C# 15, still reads every file. C# 15 syntax follows in issue #59 once CodeQL lists C# 15 and Stryker.NET handles it. The first C# 15 change makes the engine's two families of record types **closed**, so the compiler proves every kind of cost line is handled, which protects the rule that missing data is never shown as zero. The rest of .NET 11 is used where the roadmap already needs it: ASP.NET Core 11 for the API (stage 6), Microsoft Agent Framework with AG-UI for the agent chat, and the official MCP C# SDK for the MCP server. Preview features are not used.

## 2. Feature by feature

Status as shipped in .NET 11 GA. "Use" says whether Vestagraph uses it and where.

### C# 15
| Feature | Status | Use | Where |
|---|---|---|---|
| **Closed hierarchies** (`closed` on a base type: only types in the same assembly may derive from it, so a `switch` over its subtypes can be exhaustive) | Stable | **Yes, first.** `LineInput` (amount, included, not calculated, conflicting, missing) and `EvidenceValue` (money, rate, years, other) become closed (`closed` replaces `abstract`: the two modifiers can't be combined); the `_ => throw` arm in `CostLines.Resolve` is removed, so adding a new kind of line without handling it is a compile error rather than a runtime exception. The test that derives an unknown line kind in the test assembly (`MonthlyCost_unknownKindOfLine_throwsForThatLine`) no longer compiles and is deleted, because the compiler now does its job. No engine switch covers every `EvidenceValue` kind, so closing it is a safeguard only | Engine, after the upgrade |
| **Union types** (`union Name(CaseA, CaseB)`: a value that is exactly one of a fixed list of types, with exhaustive pattern matching; lowered to a struct holding `object? Value`, so value-type cases are boxed; a `default` union holds `null`, so switches keep a `null` arm) | Stable (the runtime's `UnionAttribute` is labelled "preview" on one Learn page and stable on another: **unverified** which is right) | **Trial.** A spike compares the current `Result`/`Result<T>` classes (0032) with a union-based version and keeps the current classes unless the union version is clearly simpler and has no boxing cost on the hot path. Later, API request and response bodies that are "one of" several shapes (for example a cost line that is known, missing or included) may be unions, which ASP.NET Core 11 describes as `anyOf` in OpenAPI | Engine spike; API at stage 6 |
| Collection expression arguments (`[with(comparer), ..items]`) | Stable | Where a collection needs a comparer or capacity; style only | As code is touched |
| Extension indexers | Stable | Not needed now | — |
| Labelled `break` and `continue` | Stable | Only if a nested loop needs it; the new style rule IDE0410 may raise suggestions under `AnalysisMode` `All`, handled in the upgrade | As code is touched |
| Updated memory-safety rules | **Preview** | **No** (0042: no preview features) | — |

### Runtime and libraries
| Feature | Status | Use | Where |
|---|---|---|---|
| JIT and Native AOT improvements | Stable | Free with the upgrade; nothing to change | Upgrade |
| **Runtime Async** (`<Features>runtime-async=on</Features>`) | **Preview** | **No** | — |
| **LINQ `FullJoin`** (new in .NET 11; `LeftJoin` and `RightJoin` already exist in .NET 10) | Stable | **Yes.** The compare view aligns two homes' cost lines by category; a line that exists for one home and not the other must appear as "missing" for that home, never as zero (rule 7). `FullJoin` expresses that directly | Engine comparison, built in **stage 5** (#96, moved there by the founder on 11 Nov 2026) |
| **System.Text.Json union and closed-type support** (unions written without a wrapper; `[JsonPolymorphic(InferClosedTypePolymorphism = true)]` for closed types) | Stable | **Careful.** The generated `costs.json` must stay byte-identical; the generator keeps its explicit writer. Used in the API's request and response bodies | API, stage 6 |
| JSON Lines from async sequences | Stable | Possibly for streaming large exports later | Not planned |
| `Decimal32`, `Decimal64`, `Decimal128` | Stable | **No.** Money stays `long` pence; `decimal` only for exact inputs (0021, 0034) | — |
| Zstandard, new `Process` APIs, in-memory stream adapters | Stable | Not needed | — |
| **Breaking: `Math.Round(double, digits)` and `decimal`/`BigInteger` to and from `double`/`float` conversions are now correctly rounded** | Stable (no switch back) | **Check.** The engine uses only `Math.Round(decimal, 0, AwayFromZero)` in `Pence.cs` and no `double` (an architecture test forbids it in public members); `BigInteger` (mortgage and ratio rounding) is never converted to a floating-point type; so no figure should move. The upgrade proves it: `costs.json` byte-identical, every worked test unchanged | Upgrade |
| Breaking: `DateOnly`/`TimeOnly` `TryParse` throws on an invalid style; floating-point to small integer conversions saturate; CPU baseline x86-64-v2 | Stable | Search the code in the upgrade; GitHub's runners meet the CPU baseline | Upgrade |

### ASP.NET Core 11 (stage 6 API)
| Feature | Status | Use |
|---|---|---|
| **OpenAPI 3.2** as the default document version (Microsoft.OpenApi 3.x underneath) | Stable | **Yes.** The API's OpenAPI document is generated at build time, committed, and checked in `make check` like `costs.json`; TypeScript types for the frontend are generated from it. Whether the chosen TypeScript generator reads OpenAPI 3.2 is **unverified**: if not, the document is pinned to 3.1 until it does |
| **Union types in JSON bodies** (shown as `anyOf`) | Stable (bodies only, not route, query or header values) | Yes, for "one of" shapes |
| **Async validation** (`AsyncValidationAttribute`, `IAsyncValidatableObject`) | Stable | Yes, for checks that need a lookup (for example "this home ID exists"); simple checks stay synchronous |
| **Built-in OpenTelemetry tags** on hosting activities | Stable | Yes, with Aspire's dashboard locally (0025); the separate ASP.NET Core instrumentation package becomes optional |
| SignalR authentication refresh | Stable | Not needed (AG-UI streams over server-sent events) |
| Blazor AI components (`Microsoft.AspNetCore.Components.AI`) | **Experimental** | **No** (React stays, 0042) |

### EF Core 11 (only if DA-03 picks EF Core with PostgreSQL)
Removes unneeded joins, better `GroupBy`, translates `FullJoin`, JSON columns with table-per-type inheritance. SQL Server vector search is experimental and SQL Server only, so it is not relevant (AI-02 chooses between pgvector and Azure AI Search).

### SDK and tooling
| Feature | Use |
|---|---|
| `dotnet test` on Microsoft.Testing.Platform: run-level `--timeout` and `--maximum-failed-tests` | **Yes**, in `make test` with the upgrade: a hung test run fails instead of waiting for the CI job limit |
| NuGet **minimum package publish age** (`minPublishAgeHours` on a package source in `nuget.config`) | **Yes**, 168 hours to match Dependabot's 7-day cooldown (0027). It only applies when a version is picked by `dotnet package add` or `update`; normal restore does not enforce it for exact versions, so Dependabot's cooldown stays the main guard. A floating version (`*`) now fails restore with NU1020; Vestagraph pins exact versions, so this does not affect it |
| MSBuild server and Native AOT CLI host on by default | Nothing to do; if CI shows stale-build problems, turn the server off with `DOTNET_CLI_USE_MSBUILD_SERVER=false` |
| `dotnet new mcpserver` (in the SDK, per the announcement; **unverified** locally) | Starting point for the MCP server project, then trimmed |
| `dotnetup` (toolchain manager) | **Preview**; not used |
| `.NET Skills` (dotnet/skills: guidance for coding agents) | Evaluate once: licence, overlap with Vestagraph's own agents and skills; adopt only what passes review |

### AI stack (stage 6)
| Package (nuget.org, 10 Nov 2026) | Status | Use |
|---|---|---|
| `Microsoft.Agents.AI` and `.OpenAI`, `.Anthropic`, `.Workflows` (1.28.0) | Stable | Agents, tools with approval, and the document-investigation workflow with human approval (0023) |
| `Microsoft.Agents.AI.Hosting`, `.Hosting.AspNetCore` and `.Hosting.AGUI.AspNetCore` (all 1.28.0-preview.261106.1; the AG-UI package depends on the other two) | **Prerelease** | AG-UI endpoint (`AddAGUIServer`, `MapAGUIServer`); behind Vestagraph's adapter, pinned exactly (0042) |
| `Microsoft.Agents.AI.Mcp` | **Alpha** | **No**; use `ModelContextProtocol` directly |
| `Microsoft.Agents.AI.AGUI` | **Deprecated** | **No** |
| `Microsoft.Extensions.AI` (10.11.0; MAF 1.28 needs at least this) | Stable | Model-access abstractions and evaluation libraries (0025) |
| `ModelContextProtocol`, `ModelContextProtocol.AspNetCore` (2.4.0) | Stable | MCP server (0037) |
| `Anthropic` (13.8.0), `OpenAI` (2.15.0) | Stable | Model providers, chosen per task by AI-01 against the evaluation suite |

Microsoft Agent Framework for .NET supports Claude through `Microsoft.Agents.AI.Anthropic`, including function tools, tool approval and MCP; code interpreter and web search are not supported in .NET.

## 3. How the pieces connect (stage 6)

```
Next.js page (React, CopilotKit chat)
  → Next.js route /api/copilotkit (CopilotKit runtime, HttpAgent)   ← open-source path; no Enterprise licence
  → ASP.NET Core 11 API: MapAGUIServer (server-sent events)
  → Microsoft Agent Framework agent ── tools ──→ read-only cost queries → C# cost engine
                                     └─ approval requests → shown in the chat for the user to accept or decline
  ASP.NET Core 11 API: REST endpoints (OpenAPI 3.2) → generated TypeScript types → Next.js screens
  ASP.NET Core 11 host: MCP endpoint (ModelContextProtocol.AspNetCore) → the same read-only tools
  Aspire app host: runs the API and the Next.js app locally with the OpenTelemetry dashboard
```

The agent never calculates a figure: every number in a reply comes from a tool that calls the cost engine (rule 4, decision 0004). The prototype (stage 5) needs none of this: it reads the generated fixture files.

## 4. Order and conditions
1. **Done:** decision 0042 and this plan; the Python tooling removed (#57). **Open:** close out stage 2 (#24).
2. **Done:** SDK and runtime on .NET 11 (#58, pull request #108, BE-25), with `LangVersion` 14. That pull request's own CodeQL run showed CodeQL still analyses every file.
3. **C# 15 in the engine (#59, then #60)** when CodeQL lists C# 15 and Stryker.NET handles it: closed hierarchies first, then the `Result` union spike. Check CodeQL's supported-languages page at each weekly review.
4. **Stages 3 and 4** do not depend on .NET 11; stage 5's #96 uses `FullJoin` (available since #58).
5. **Stage 6:** API skeleton and Aspire, generated TypeScript types, MCP server, evaluation harness, agent gateway, AG-UI chat, document workflow.

## 5. Not verified
- When CodeQL will support C# 15 and .NET 11 (a .NET 11 RC1 extractor change was merged in `github/codeql` pull request 22565; no release announcement found).
- Whether Stryker.NET 5.1 parses C# 15 (its release notes do not mention it).
- Whether InspectCode 2026.3 raises new warnings on the existing code (a question for #59; the pinned 2026.2.4.1, #113 analyses the net11.0, C# 14 code cleanly (checked in #58 with 2026.2.3.1 and again in #113)).
- Whether the runtime's `UnionAttribute` is stable or preview (two Learn pages disagree).
- Whether the TypeScript generator chosen in stage 6 reads OpenAPI 3.2.

## Sources
- [Announcing .NET 11](https://devblogs.microsoft.com/dotnet/announcing-dotnet-11/)
- [What's new in C# 15](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-15) and [union types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/union)
- What's new in .NET 11: [runtime](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-11/runtime), [libraries](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-11/libraries), [SDK](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-11/sdk)
- [Breaking changes in .NET 11](https://learn.microsoft.com/en-us/dotnet/core/compatibility/11), including [Math.Round with digits](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/11/math-round-digits) and [decimal and floating-point conversions](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/11/decimal-biginteger-floating-point-conversions)
- [What's new in ASP.NET Core 11](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-11) and [ASP.NET Core 11 breaking changes](https://learn.microsoft.com/en-us/aspnet/core/breaking-changes/11/overview)
- [Minimum package publication age (.NET 11 SDK)](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-11/sdk#configure-minimum-package-publication-age-from-the-cli)
- [CodeQL supported languages and frameworks](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/)
- [What's New in ReSharper 2026.3](https://www.jetbrains.com/resharper/whatsnew/), [ReSharper command line tools on NuGet](https://www.nuget.org/packages/JetBrains.ReSharper.GlobalTools), [Stryker.NET releases](https://github.com/stryker-mutator/stryker-net/releases)
- [Agent Framework: AG-UI getting started](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/getting-started), [Anthropic provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/anthropic)
- [CopilotKit with a Microsoft Agent Framework .NET backend](https://docs.copilotkit.ai/ms-agent-dotnet)
