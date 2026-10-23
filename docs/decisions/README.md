# Decision register

Every significant product, technical and working decision gets its own record in this folder, named `NNNN-short-title.md` (for example `0001-ways-of-working.md`). The process is in `docs/design/04_Project_Goals_and_Delivery.md` §10. Each decision is made at the stage listed, the latest point that still lets the work go ahead.

**Statuses:** Not started · Proposed (options drafted) · Accepted · Superseded by NNNN · Open (deliberately undecided, with a reason)

## Already decided

| ID | Decision | Outcome | Where recorded |
|---|---|---|---|
| — | Audience | Buyers and renters with equal weight | Doc 02 §9 |
| — | Launch geography | England first | Doc 02 §7, §9 |
| — | Project purpose | Portfolio and learning first, built by AI coding agents, small monthly budget, kept commercially viable | Doc 04 |
| — | Repository | Public, all rights reserved | Doc 04 §8, `LICENSE` |
| — | First public showcase | Clickable prototype | Doc 04 §8 |

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
| PD-08 | Name shown on the public demo | 1 | Parked (decide before public demo) | [0008](0008-demo-name.md) |
| PD-09 | Public brand | 1 | Open (needs clearance) | [0009](0009-public-brand.md) |
| PD-10 | Commercial model and prices | 1 | Open (needs user study) | [0010](0010-commercial-model.md) |
| WW-01 | Ways of working | 1 | Accepted | [0011](0011-ways-of-working.md) |
| WW-02 | AI coding tools and setup | 1 | Accepted | [0012](0012-ai-coding-tools.md) |
| WW-03 | Repository and tracking conventions | 1 | Accepted | [0013](0013-repo-and-tracking.md) |
| DA-01 | Fixture data format | 2 | Not started | |
| DA-02 | Calculation script and test vectors | 2 | Not started | |
| SP-01 | Specification format | 3 | Not started | |
| SP-02 | Work breakdown | 3 | Not started | |
| DS-01 | Design tooling | 4 | Not started | |
| DS-02 | Design system foundation | 4 | Not started | |
| FE-01 | Frontend framework and rendering | 4 | Not started | |
| FE-02 | Styling and components | 4 | Not started | |
| FE-03 | Maps and charts | 4 | Not started | |
| FE-04 | Frontend practices | 4 | Not started | |
| IN-01 | Prototype architecture | 4 | Not started | |
| IN-02 | Demo hosting | 4 | Not started | |
| IN-03 | Infrastructure as code | 4 | Not started | |
| IN-04 | CI/CD and environments | 4 | Not started | |
| IN-05 | Budget cap and cost alerts | 4 | Not started | |
| FE-05 | Demo analytics and feedback | 5 | Not started | |
| BE-01 | Backend language and framework | 6 (before cost engine) | Not started | |
| BE-02 | Backend architecture and API contract | 6 (before cost engine) | Not started | |
| BE-03 | Rules versioning | 6 (before cost engine) | Not started | |
| DA-03 | Database and geospatial | 6 (before real data) | Not started | |
| DA-04 | Ingestion and scheduling | 6 (before real data) | Not started | |
| DA-05 | Source licence register | 6 (before real data) | Not started | |
| DA-06 | Address and routing providers | 6 (before real data) | Not started | |
| SE-01 | Authentication and accounts | 6 (before questions workflow) | Not started | |
| SE-02 | Privacy and data protection | 6 (before real data; completed before questions workflow) | Proposed (starting position agreed) | [0014](0014-privacy-and-data-protection.md) |
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
**Status:** Proposed | Accepted | Superseded by NNNN  
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
