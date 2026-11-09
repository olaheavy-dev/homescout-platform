# Decision register

Every significant product, technical and working decision gets its own record in this folder, named `NNNN-short-title.md` (for example `0011-ways-of-working.md`). The process is in `docs/product/04-project-goals-and-delivery.md` §10. Each decision is made at the stage listed, the latest point that still lets the work go ahead.

Hard-to-reverse decisions get a full record; easily reversible choices get one line in this register with their default (decision 0035).

**Statuses** (use exactly these; a short note in brackets may follow):
- **Not started:** no record yet.
- **Proposed:** options drafted, or a starting position agreed, but not yet fully decided.
- **Accepted:** decided by the founder.
- **Accepted (partly superseded by NNNN):** some parts replaced by a later record.
- **Superseded by NNNN:** fully replaced.
- **Open:** deliberately undecided, with a reason and a revisit point.
- **Parked:** paused, with a point by which it must resume.

## Already decided

| ID | Decision | Outcome | Where recorded |
|---|---|---|---|
| — | Audience | Buyers and renters with equal weight | Doc 02 §9 |
| — | Launch geography | England first | Doc 02 §7, §9 |
| — | Project purpose | Portfolio and learning first, built by AI coding agents, small monthly budget, kept commercially viable | Doc 04 |
| — | Repository | Public, all rights reserved | Doc 04 §8, `LICENSE` |
| — | First public showcase | Clickable prototype | Doc 04 §8 |
| — | Stage 1 sign-off | Signed off by the founder on 23 October 2026 | `docs/planning/stage-1-confirmation.md` |

## Register

| ID | Decision | Stage | Status | Record |
|---|---|---|---|---|
| PD-01 | Product category | 1 | Accepted | [0001](0001-product-category.md) |
| PD-02 | Core object | 1 | Accepted | [0002](0002-core-object.md) |
| PD-03 | Main value | 1 | Accepted | [0003](0003-main-value.md) |
| PD-04 | AI presentation in the product | 1 | Accepted | [0004](0004-ai-in-the-product.md) |
| PD-05 | Visual direction | 1 | Accepted | [0005](0005-visual-direction.md) |
| PD-06 | Prototype centrepiece | 1 | Accepted | [0006](0006-prototype-centrepiece.md) |
| PD-07 | Free/paid principle | 1 | Accepted | [0007](0007-free-paid-principle.md) |
| PD-08 | Name shown on the public demo | 1 | Parked (resume before the public demo) | [0008](0008-demo-name.md) |
| PD-09 | Public brand | 1 | Open (needs clearance) | [0009](0009-public-brand.md) |
| PD-10 | Commercial model and prices | 1 | Open (needs user study) | [0010](0010-commercial-model.md) |
| WW-01 | Ways of working | 1 | Accepted (partly superseded by 0015, 0035) | [0011](0011-ways-of-working.md) |
| WW-02 | AI coding tools and setup | 1 | Accepted (partly superseded by 0015, 0035) | [0012](0012-ai-coding-tools.md) |
| WW-03 | Repository and tracking conventions | 1 | Accepted | [0013](0013-repo-and-tracking.md) |
| WW-04 | Merge policy and single agent instructions file | 1 | Superseded by 0035 | [0015](0015-agent-merges-after-review.md) |
| WW-05 | Holistic reviews and debt limits | 1 | Superseded by 0035 | [0016](0016-holistic-reviews-and-debt-limits.md) |
| WW-06 | Documentation folder structure and naming | 1 | Accepted | [0017](0017-docs-structure.md) |
| WW-07 | Dependency updates and documentation upkeep | 2 | Accepted (partly superseded by 0027, 0035) | [0024](0024-dependency-updates.md) |
| WW-08 | Learning-first engineering | 2 | Accepted (partly superseded by 0035) | [0026](0026-learning-first-engineering.md) |
| WW-09 | Stage 2 engineering and security hardening | 2 | Accepted (partly superseded by 0035; tool-only licence exception for `typing_extensions` by 0039; tool-only exception for `libcst` and the package-URL exemptions for HomeScout's own Python packages by register line BE-22) | [0027](0027-stage-2-engineering-hardening.md) |
| WW-10 | Agent roster, design skills and working rules | 2 | Accepted (partly superseded by 0035) | [0031](0031-agent-roster.md) |
| WW-11 | Review fallback when Codex is unavailable | 2 | Superseded by 0035 | [0033](0033-review-fallback.md) |
| WW-12 | Ways of working v2 (consolidated rulebook) | 2 | Accepted (partly superseded by 0039: Python packages added to the point 9 pre-approved list; the small-update rule changes: a minor bump of a direct `0.x` dependency or action pin counts as major) | [0035](0035-ways-of-working-v2.md) |
| DA-01 | Fixture data format | 2 | Accepted (partly superseded by 0027) | [0018](0018-fixture-data-format.md) |
| DA-02 | Calculation script and test vectors | 2 | Accepted (partly superseded by 0021: solution location; by 0036: language) | [0019](0019-cost-engine-in-csharp.md) |
| SP-01 | Specification format | 3 | Not started | |
| SP-02 | Work breakdown | 3 | Not started | |
| DS-01 | Design tooling | 4 | Not started (code-first indicated by 0031) | |
| DS-02 | Design system foundation | 4 | Not started | |
| FE-01 | Frontend framework and rendering | 4 | Proposed (TypeScript and Next.js accepted in 0020; routing and rendering at stage 4) | [0020](0020-application-languages.md) |
| FE-02 | Styling and components | 4 | Not started | |
| FE-03 | Maps and charts | 4 | Not started | |
| FE-04 | Frontend practices | 4 | Not started | |
| IN-00 | Hosting strategy | 2 (brought forward) | Accepted (cost first) | [0022](0022-cost-first-hosting.md) |
| IN-01 | Prototype architecture | 4 | Not started | |
| IN-02 | Demo hosting | 4 | Not started | |
| IN-03 | Infrastructure as code | 4 | Not started | |
| IN-04 | CI/CD and environments | 4 | Not started | |
| IN-05 | Budget cap and cost alerts | 4 | Not started | |
| FE-05 | Demo analytics and feedback | 5 | Not started | |
| BE-01 | Backend language and framework | 2 (language), 6 (framework) | Proposed (Python accepted in 0036, replacing C# on .NET from 0020; FastAPI to confirm at stage 6) | [0020](0020-application-languages.md) |
| BE-02 | Backend architecture and API contract | 6 (before cost engine) | Not started | |
| BE-03 | Rules versioning | 6 (before cost engine) | Not started | |
| BE-04 | .NET engineering foundation | 2 | Accepted (partly superseded by 0034; by 0036: .NET setup; Python successor for the toolchain is 0039) | [0021](0021-dotnet-engineering-foundation.md) |
| BE-05 | Our own Result type | 2 | Accepted (partly superseded by 0036: rewritten in Python, principle stands) | [0032](0032-own-result-type.md) |
| BE-06 | Rounding boundary test cases | 2 | Accepted | [0034](0034-rounding-boundary-cases.md) |
| WW-13 | Licence allow-list addition | 2 | Accepted (register line: `zlib-acknowledgement`, a permissive Zlib-family licence used by NUnit 5, added to the 0027 allow-list; founder, 23 Oct 2026) | — |
| BE-07 | Fixture schema validator | 2 | Accepted (register line: JsonSchema.Net with JSON Schema 2020-12; added to the pre-approved packages; founder, 23 Oct 2026) | — |
| BE-08 | Validator licence | 2 | Accepted (register line, which is the founder's recorded licence-exception decision required by 0027: JsonSchema.Net 9.x and its two dependencies accepted under their Open Source Maintenance Fee EULA; source remains MIT; fee applies only to binary-release use in revenue-generating activities with ≥ US$10,000 annual revenue, otherwise build from source; founder, 23 Oct 2026) | — |
| BE-09 | Architecture-test package licence | 2 | Accepted (register line, the founder's recorded licence-exception decision required by 0027: NetArchTest.Rules 1.3.2 and its dependency Mono.Cecil are MIT per their GitHub repositories, but their NuGet metadata declares no SPDX licence; founder approved their use, 23 Oct 2026; from P1 the unlicensed step is a safeguard in case GitHub cannot detect their licence (GitHub's dependency graph shows MIT for both on 9 Nov 2026), so P1 exempts them by package (BE-22) and the note that no dependency-review workflow change is needed is out of date) | — |
| BE-10 | Cost-engine output file | 2 | Accepted (register line: the generator writes one file, `packages/fixtures/generated/costs.json`, checked by `schema/generated-costs.schema.json`; the generator owns the folder; founder, 23 Oct 2026) | — |
| BE-11 | Figure ID format | 2 | Accepted (register line: `{homeId}.{scenarioId}.{section}.{name}`, for example `B1.from-step-4.monthly.service-charge`; unique across the file; founder, 23 Oct 2026) | — |
| BE-12 | Scenario IDs | 2 | Accepted (register line: scenarios are worked out from the data; consecutive story steps that use the same evidence merge, and the ID is `from-step-N` for the first step; founder, 23 Oct 2026) | — |
| BE-13 | Lines that do not apply | 2 | Accepted (register line: a line a home does not have is left out of the output, never shown as zero; the line order is fixed by the engine per mode; founder, 23 Oct 2026) | — |
| BE-14 | Monthly differences | 2 | Accepted (register line: a monthly difference is the difference of the two rounded monthly lines, not a rounded difference of yearly figures; founder, 23 Oct 2026) | — |
| BE-15 | Rates in whole basis points | 2 | Accepted (register line: the engine takes rates as whole basis points (550 is 5.5%); a rate that is not a whole number of basis points is not accepted until a decision says otherwise; founder, 23 Oct 2026) | — |
| BE-16 | Missing inputs in a calculation | 2 | Accepted (register line: an anchor input (asking price, mortgage deposit, rate and term when buying; rent when renting) that is missing stops the calculation with a `Result` failure; any other missing bill becomes a `missing` line and makes the total partial; founder, 23 Oct 2026) | — |
| BE-17 | Mortgage term limit | 2 | Accepted (register line: the engine fails a mortgage term over 100 years with `mortgage.term-too-long`, and the evidence and output schemas allow at most 100; this is a technical computation limit because the exact arithmetic gets very slow for huge terms, not a lending rule; founder, 23 Oct 2026) | — |
| BE-18 | Python for the backend, cost engine and AI layer | 2 (reopens stage 2) | Accepted (founder, 6 Nov 2026; supersedes the C# parts of 0019, 0020, 0021, 0032; the C# code and docs stay until the port pull request merges; partly superseded by 0039: `Fraction`, not `decimal`, for decimal inputs, and the tool choices) | [0036](0036-python-backend.md) |
| AI-07 | MCP server and coding-agent integrations | 6 (local fixture-backed server may come earlier) | Proposed | [0037](0037-mcp-server-and-agent-integrations.md) |
| SE-03 | Accounts and API keys for MCP and API access | 6 (before any public remote MCP server) | Proposed | [0038](0038-accounts-and-api-keys-for-mcp.md) |
| BE-19 | The founder's FastAPI template as the API starting point | 6 (template changes may run earlier) | Accepted (one-time import, trimmed; amends the private-reference rule for that template only; founder, 6 Nov 2026; partly superseded by 0041: the MAF gateway is built in the template first; imported with the API at P7 if ready, otherwise at stage 6) | [0040](0040-fastapi-template-as-api-starting-point.md) |
| BE-20 | Python engineering foundation | 2 (port step P0) | Accepted (founder's answers to the port plan's nine questions, 7 Nov 2026; successor to 0021 for the toolchain; Python pre-approved packages; `typing_extensions` tool-only licence exception; the rest of the port plan and the details beyond it confirmed by the founder's merge; 8 Nov 2026 answers: Q1, commit an exported requirements file for dependency review (its proof blocks P1); Q2, CodeQL default setup with no workflow (the founder adds Python in settings); Q3, a minor bump of a direct `0.x` dependency or action pin counts as a major bump; Q1's export file is amended by BE-23, and the licence exemptions made in P1 are in BE-22) | [0039](0039-python-engineering-foundation.md) |
| BE-21 | Python build backend | 2 (port step P1) | Accepted (register line: `uv_build` (MIT OR Apache-2.0, 0.13.x, Astral) is the build backend of the three Python packages, pinned `>=0.13.7,<0.14`; founder, 9 Nov 2026; plan on issue #42) | — |
| BE-22 | Licence gate fails on unlicensed packages | 2 (port step P1) | Accepted (register line: issue #30 is fixed in P1: dependency review gets a step that fails on packages with no detectable licence, as 0027 requires; actions are not exempted. Named exemptions, all by package URL in `allow-dependencies-licenses`: `pkg:nuget/NetArchTest.Rules` and `pkg:nuget/Mono.Cecil` (BE-09; a safeguard, GitHub shows MIT for both); `pkg:pypi/typing-extensions` (0039 section 7); **`pkg:pypi/libcst`**, a tool-only exception (Apache-2.0 AND MIT AND Python-2.0 per GitHub; its LICENSE is MIT plus files derived from the Python standard library and from dataclasses; dev-only through mutmut, never imported or shipped); and HomeScout's own `pkg:pypi/homescout-engine`, `homescout-generator` and `homescout-fixture-validator` (all rights reserved; GitHub's `uv.lock` parser lists repository-local uv projects as PyPI dependencies with no licence). P7's new packages need the same kind of entry; founder, 9 Nov 2026) | — |
| BE-23 | Committed export of `uv.lock` | 2 (port step P1) | Pending the P1 proof (register line, amends 0039 Q1: the committed export file is NOT added in P1; it amends 0039 Q1 only if the proof shows `uv.lock` alone is caught (to be confirmed by the proof pull requests); if not, adopt the export targets as the Makefile comment says; founder, 9 Nov 2026) | — |
| WW-14 | Dependabot groups for `0.x` tools | 2 (port step P1) | Accepted (register line, follows 0039 Q3: `ruff` and `referencing` (uv ecosystem) and the zizmor and dependency-submission actions each sit in a `*-zero-x` group listed before the minor-and-patch group, so their minor bumps go to full review; founder, 9 Nov 2026; the first Dependabot run checks the grouping) | — |
| DA-03 | Database and geospatial | 6 (before real data) | Not started | |
| DA-04 | Ingestion and scheduling | 6 (before real data) | Not started | |
| DA-05 | Source licence register | 6 (before real data) | Not started | |
| DA-06 | Address and routing providers | 6 (before real data) | Not started | |
| DA-07 | Data sourcing: no scraping | 2 | Accepted | [0028](0028-no-scraping.md) |
| SE-01 | Authentication and accounts | 6 (before questions workflow) | Not started | |
| SE-02 | Privacy and data protection | 5 (visitor data), 6 step 4 (public records, logs), 6 step 5 (full) | Proposed (starting position agreed) | [0014](0014-privacy-and-data-protection.md) |
| AI-01 | Model provider and runtime | 6 (before document extraction) | Not started | |
| AI-02 | Retrieval | 6 (before document extraction) | Not started | |
| AI-03 | Evaluation tooling | 6 (before document extraction) | Proposed (evaluation-first accepted in 0025; tooling at stage 6) | [0025](0025-ai-platform-capabilities.md) |
| AI-04 | Orchestration | 6 (decided early) | Accepted (Microsoft Agent Framework; reaffirmed 6 Nov 2026 as definite for HomeScout, used through its Python package, not LangChain; partly superseded by 0041: the template builds the neutral core and the MAF gateway first; at P7 if ready, otherwise stage 6, with that exception to "no framework packages before stage 6") | [0023](0023-microsoft-agent-framework.md) |
| AI-05 | AI safety | 6 (requirements decided early) | Accepted (capability requirements; partly superseded by 0035) | [0025](0025-ai-platform-capabilities.md) |
| AI-06 | Document extraction principles | 6 (rules set early) | Accepted | [0030](0030-extraction-principles.md) |
| AI-08 | MAF gateway built in the template first | 6 (template work runs earlier) | Accepted (founder, 7 Nov 2026; reverses the order in the "Template follow-up" of 0023 and the "Template track" sentence of 0040; gateway with the API at P7 if ready (template release, DA-03 chose PostgreSQL, packages approved), otherwise at stage 6; relaxes 0023's "no framework packages before stage 6" and 0040's gateway-off skeleton) | [0041](0041-maf-gateway-built-in-the-template.md) |
| CO-01 | Entitlements and payments | 6 (before entitlements) | Not started | |
| OP-01 | Observability | 6 (before monitoring) | Proposed (OpenTelemetry and local Aspire accepted in 0025; production telemetry at stage 6) | [0025](0025-ai-platform-capabilities.md) |
| OP-02 | Scheduling and notifications | 6 (before monitoring) | Not started | |
| OP-03 | Outside services: provenance and live tests | 6 (rule set early) | Accepted | [0029](0029-external-services.md) |

## Record template

```markdown
# NNNN: <decision title>

**ID:** <register ID>  
**Status:** Not started | Proposed | Accepted | Accepted (partly superseded by NNNN) | Superseded by NNNN | Open | Parked  
**Date:** <YYYY-MM-DD>  
**Stage:** <roadmap stage>

## Context
What needs deciding, why now, and the constraints (goals, budget, England first, public repo).

## Options
### Option A: <name>
What it is. Trade-offs, cost, learning value, effect on commercial options.

### Option B: <name>
…

## Recommendation
The drafter's recommendation and why.

## Decision
The founder's choice, and the reason in their own words.

## Consequences
What this commits us to, what it rules out, and what would make us revisit it.
```
