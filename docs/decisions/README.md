# Decision register

Every significant product, technical and working decision gets its own record in this folder, named `NNNN-short-title.md` (for example `0011-ways-of-working.md`). The process is in `docs/product/04-project-goals-and-delivery.md` §10. Each decision is made at the stage listed, the latest point that still lets the work go ahead.

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
| WW-01 | Ways of working | 1 | Accepted (partly superseded by 0015) | [0011](0011-ways-of-working.md) |
| WW-02 | AI coding tools and setup | 1 | Accepted (partly superseded by 0015) | [0012](0012-ai-coding-tools.md) |
| WW-03 | Repository and tracking conventions | 1 | Accepted | [0013](0013-repo-and-tracking.md) |
| WW-04 | Merge policy and single agent instructions file | 1 | Accepted (partly superseded by 0016) | [0015](0015-agent-merges-after-review.md) |
| WW-05 | Holistic reviews and debt limits | 1 | Accepted | [0016](0016-holistic-reviews-and-debt-limits.md) |
| WW-06 | Documentation folder structure and naming | 1 | Accepted | [0017](0017-docs-structure.md) |
| DA-01 | Fixture data format | 2 | Accepted | [0018](0018-fixture-data-format.md) |
| DA-02 | Calculation script and test vectors | 2 | Accepted (C# cost engine) | [0019](0019-cost-engine-in-csharp.md) |
| SP-01 | Specification format | 3 | Not started | |
| SP-02 | Work breakdown | 3 | Not started | |
| DS-01 | Design tooling | 4 | Not started | |
| DS-02 | Design system foundation | 4 | Not started | |
| FE-01 | Frontend framework and rendering | 4 | Proposed (TypeScript and Next.js accepted in 0020; routing and rendering at stage 4) | [0020](0020-application-languages.md) |
| FE-02 | Styling and components | 4 | Not started | |
| FE-03 | Maps and charts | 4 | Not started | |
| FE-04 | Frontend practices | 4 | Not started | |
| IN-01 | Prototype architecture | 4 | Not started | |
| IN-02 | Demo hosting | 4 | Not started | |
| IN-03 | Infrastructure as code | 4 | Not started | |
| IN-04 | CI/CD and environments | 4 | Not started | |
| IN-05 | Budget cap and cost alerts | 4 | Not started | |
| FE-05 | Demo analytics and feedback | 5 | Not started | |
| BE-01 | Backend language and framework | 2 (language), 6 (framework) | Proposed (C# on .NET accepted in 0020; ASP.NET Core to confirm at stage 6) | [0020](0020-application-languages.md) |
| BE-02 | Backend architecture and API contract | 6 (before cost engine) | Not started | |
| BE-03 | Rules versioning | 6 (before cost engine) | Not started | |
| DA-03 | Database and geospatial | 6 (before real data) | Not started | |
| DA-04 | Ingestion and scheduling | 6 (before real data) | Not started | |
| DA-05 | Source licence register | 6 (before real data) | Not started | |
| DA-06 | Address and routing providers | 6 (before real data) | Not started | |
| SE-01 | Authentication and accounts | 6 (before questions workflow) | Not started | |
| SE-02 | Privacy and data protection | 5 (visitor data), 6 step 4 (public records, logs), 6 step 5 (full) | Proposed (starting position agreed) | [0014](0014-privacy-and-data-protection.md) |
| AI-01 | Model provider and runtime | 6 (before document extraction) | Not started | |
| AI-02 | Retrieval | 6 (before document extraction) | Not started | |
| AI-03 | Evaluation tooling | 6 (before document extraction) | Not started | |
| AI-04 | Orchestration | 6 (before document extraction) | Not started | |
| AI-05 | AI safety | 6 (before document extraction) | Not started | |
| CO-01 | Entitlements and payments | 6 (before entitlements) | Not started | |
| OP-01 | Observability | 6 (before monitoring) | Not started | |
| OP-02 | Scheduling and notifications | 6 (before monitoring) | Not started | |

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
