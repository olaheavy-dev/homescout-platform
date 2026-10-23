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
| WW-09 | Stage 2 engineering and security hardening | 2 | Accepted (partly superseded by 0035) | [0027](0027-stage-2-engineering-hardening.md) |
| WW-10 | Agent roster, design skills and working rules | 2 | Accepted (partly superseded by 0035) | [0031](0031-agent-roster.md) |
| WW-11 | Review fallback when Codex is unavailable | 2 | Superseded by 0035 | [0033](0033-review-fallback.md) |
| WW-12 | Ways of working v2 (consolidated rulebook) | 2 | Accepted | [0035](0035-ways-of-working-v2.md) |
| DA-01 | Fixture data format | 2 | Accepted (partly superseded by 0027) | [0018](0018-fixture-data-format.md) |
| DA-02 | Calculation script and test vectors | 2 | Accepted (partly superseded by 0021: solution location) | [0019](0019-cost-engine-in-csharp.md) |
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
| BE-01 | Backend language and framework | 2 (language), 6 (framework) | Proposed (C# on .NET accepted in 0020; ASP.NET Core to confirm at stage 6) | [0020](0020-application-languages.md) |
| BE-02 | Backend architecture and API contract | 6 (before cost engine) | Not started | |
| BE-03 | Rules versioning | 6 (before cost engine) | Not started | |
| BE-04 | .NET engineering foundation | 2 | Accepted (partly superseded by 0034) | [0021](0021-dotnet-engineering-foundation.md) |
| BE-05 | Our own Result type | 2 | Accepted | [0032](0032-own-result-type.md) |
| BE-06 | Rounding boundary test cases | 2 | Accepted | [0034](0034-rounding-boundary-cases.md) |
| WW-13 | Licence allow-list addition | 2 | Accepted (register line: `zlib-acknowledgement`, a permissive Zlib-family licence used by NUnit 5, added to the 0027 allow-list; founder, 23 Oct 2026) | — |
| BE-07 | Fixture schema validator | 2 | Accepted (register line: JsonSchema.Net with JSON Schema 2020-12; added to the pre-approved packages; founder, 23 Oct 2026) | — |
| BE-08 | Validator licence | 2 | Accepted (register line, which is the founder's recorded licence-exception decision required by 0027: JsonSchema.Net 9.x and its two dependencies accepted under their Open Source Maintenance Fee EULA; source remains MIT; fee applies only to binary-release use in revenue-generating activities with ≥ US$10,000 annual revenue, otherwise build from source; founder, 23 Oct 2026) | — |
| BE-09 | Architecture-test package licence | 2 | Accepted (register line, the founder's recorded licence-exception decision required by 0027: NetArchTest.Rules 1.3.2 and its dependency Mono.Cecil are MIT per their GitHub repositories, but their NuGet metadata declares no SPDX licence; founder approved their use, 23 Oct 2026; no dependency-review workflow change is needed) | — |
| BE-10 | Cost-engine output file | 2 | Accepted (register line: the generator writes one file, `packages/fixtures/generated/costs.json`, checked by `schema/generated-costs.schema.json`; the generator owns the folder; founder, 23 Oct 2026) | — |
| BE-11 | Figure ID format | 2 | Accepted (register line: `{homeId}.{scenarioId}.{section}.{name}`, for example `B1.from-step-4.monthly.service-charge`; unique across the file; founder, 23 Oct 2026) | — |
| BE-12 | Scenario IDs | 2 | Accepted (register line: scenarios are worked out from the data; consecutive story steps that use the same evidence merge, and the ID is `from-step-N` for the first step; founder, 23 Oct 2026) | — |
| BE-13 | Lines that do not apply | 2 | Accepted (register line: a line a home does not have is left out of the output, never shown as zero; the line order is fixed by the engine per mode; founder, 23 Oct 2026) | — |
| BE-14 | Monthly differences | 2 | Accepted (register line: a monthly difference is the difference of the two rounded monthly lines, not a rounded difference of yearly figures; founder, 23 Oct 2026) | — |
| BE-15 | Rates in whole basis points | 2 | Accepted (register line: the engine takes rates as whole basis points (550 is 5.5%); a rate that is not a whole number of basis points is not accepted until a decision says otherwise; founder, 23 Oct 2026) | — |
| BE-16 | Missing inputs in a calculation | 2 | Accepted (register line: an anchor input (asking price, mortgage deposit, rate and term when buying; rent when renting) that is missing stops the calculation with a `Result` failure; any other missing bill becomes a `missing` line and makes the total partial; founder, 23 Oct 2026) | — |
| BE-17 | Mortgage term limit | 2 | Accepted (register line: the engine fails a mortgage term over 100 years with `mortgage.term-too-long`, and the evidence and output schemas allow at most 100; this is a technical computation limit because the exact arithmetic gets very slow for huge terms, not a lending rule; founder, 23 Oct 2026) | — |
| BE-18 | Differences between homes | 2 (deferred) | Accepted (register line: calculated differences between homes, B1 against B2 and R1 against R2, are deferred by the founder on 23 Oct 2026 until independently worked test cases exist; they are needed before the stage 5 compare and decision-impact screens; stage 2 shows each home's own figures; founder, 23 Oct 2026) | — |
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
| AI-04 | Orchestration | 6 (decided early) | Accepted (Microsoft Agent Framework) | [0023](0023-microsoft-agent-framework.md) |
| AI-05 | AI safety | 6 (requirements decided early) | Accepted (capability requirements; partly superseded by 0035) | [0025](0025-ai-platform-capabilities.md) |
| AI-06 | Document extraction principles | 6 (rules set early) | Accepted | [0030](0030-extraction-principles.md) |
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
