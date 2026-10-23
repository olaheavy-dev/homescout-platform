# HomeScout: project goals and delivery approach

**Date:** 23 October 2026  
**Confirmed by the founder:** The project is a portfolio and learning project first, built mostly by AI coding agents, on a small monthly running budget, and kept commercially viable for later.  
**Authority:** This document owns how the product is built, run and presented. `02_Product_Research_and_Direction.md` still owns product and commercial decisions; `03_Prototype_and_Image_Direction.md` still owns prototype behaviour and design.  
**Status:** Proposed approach. The build sequence in section 5 orders engineering work for learning and demonstration. It is not an MVP classification or a validated launch roadmap.

## 1. Three goals, and how to trade them off

| Goal | What success looks like |
|---|---|
| **Portfolio** | A reviewer can open a live demo, follow both stories end to end in a few minutes, and read how the hard problems were solved |
| **Learning** | You can explain and defend every architectural decision, including the code the agents wrote |
| **Commercial option** | Nothing built now blocks a later launch: data rights, privacy, brand and code ownership stay clean |

When they conflict: **never trade away commercial cleanliness** (licences, privacy, ownership), because it is expensive to recover. Between portfolio polish and learning depth, prefer depth in the areas that set the product apart (section 4) and polish everywhere a reviewer looks first.

## 2. What "agent-driven" means here

The product is **built mostly by AI coding agents**, with you as product owner, architect and reviewer. It does not mean the product runs on a multi-agent system.

- **In the build:** agents write most of the code, tests, infrastructure and documentation, working from the specs in this folder. You set direction, review every change, and own decisions.
- **In the product:** behaviour stays mostly deterministic. AI is used inside specific tasks (document extraction, drafting a question, checking a reply, explaining a change) as single, task-specific model calls with tools. All numbers come from deterministic code. Multi-agent orchestration (Microsoft Agent Framework in the brief's stack) is deferred until a measured task needs it.

This is also the stronger portfolio story: "AI-assisted engineering with rigorous verification" is more credible to a reviewer than "a dashboard of agents."

## 3. Working rules for agent-built code

These keep agent output reviewable and keep you learning rather than rubber-stamping.

1. **Spec before code.** Each slice starts from a short written spec that links to the relevant sections in 02/03. Agents implement against the spec; changes to the spec are your decision.
2. **Small vertical slices.** One user-visible capability per pull request, kept small enough to review properly.
3. **Tests first for anything numeric or legal.** Cost, tax and lease-date logic gets table-driven tests with worked examples before implementation. The image 5 mortgage error in doc 03 is exactly what this prevents.
4. **Rules come from cited sources, not model memory.** SDLT bands, tenancy rules and inspection frameworks live in versioned rule tables with a source URL and effective date. You review every rule table change.
5. **Decision records.** Every significant choice gets a short architecture decision record in `docs/decisions/`, written in your words. If you can't write the record, you don't understand the choice yet.
6. **Evaluations for every AI task.** Each model-backed task has a fixed evaluation set (synthetic documents, expected citations, known traps such as the £2,400 vs £3,720 period mismatch) that runs in CI. A prompt or model change that lowers the score doesn't merge.
7. **Agent guardrails in the repo.** A `CLAUDE.md` (or equivalent) records conventions, commands, the "no invented facts" rule and the commercial constraints below, so every agent session starts with them.
8. **No real personal data.** Development and demos use the synthetic fixture catalogue from doc 03. Real documents are only for consented research sessions, kept outside the repository.
9. **Licence check before ingestion.** No dataset, map tile or image enters the repository or pipeline until its licence and attribution terms are recorded.
10. **Explain-back.** For each merged slice, you write a few lines on how it works. This is the learning record and the raw material for the case study.

## 4. What makes it portfolio-worthy

Reviewers have seen many AI-wrapper apps. These are the parts that make this one stand out, and what each teaches:

| Showcase | What it demonstrates | What you learn |
|---|---|---|
| Evidence model with provenance (origin, scope, time, status, interpretation) | Data modelling for trust, not just storage | Domain modelling, temporal data, PostgreSQL/PostGIS |
| Deterministic cost engine (buy and rent, England SDLT, stress scenarios) | Correctness, tested financial logic, versioned rules | Test design, money/rounding, rule versioning |
| England open-data ingestion (EPC, Price Paid, planning, flood) with coverage states | Real-world messy data, honest gaps, attribution | ETL, matching property identity, geospatial joins |
| Document extraction with page-level citations and conflict detection | Grounded AI with a measured evaluation suite | Retrieval, structured extraction, evals, prompt-injection defence |
| Question → reply → decision history | Workflow and state-machine design with audit trail | Event history, versioning, UX for uncertainty |
| Two complete stories (buyer and renter) in a public demo | Product thinking and finished UX | Next.js, accessibility, responsive design |
| Infrastructure as code, tracing, cost controls | Production habits on a small budget | Azure, Bicep, OpenTelemetry, cost management |
| Case study and decision records | Communication and judgement | Writing about trade-offs |

The public demo uses the synthetic fixtures and is labelled **Illustrative example** throughout, as doc 03 requires.

## 5. Proposed build sequence

Each step is a vertical slice that leaves a working, demonstrable product. It sequences engineering and learning. It does not remove features from the product or decide what launches.

1. **Foundation:** repository conventions, CLAUDE.md, CI, IaC skeleton, budget alerts (cap set in the infrastructure discussion, section 9 stage 4), the fixture catalogue (four homes, one household, fixed 23 October 2026 snapshot).
2. **Clickable prototype of both stories** on fixtures, with a design system from doc 03 §6. This alone is a presentable portfolio piece, and it is **the first public showcase** (founder decision).
3. **Cost engine** behind the prototype: buy and rent, England SDLT, move-in cash, stress scenarios, fully tested.
4. **Real England evidence** for one category at a time (EPC, then Price Paid, then planning and flood), with provenance and "not covered" states.
5. **Questions, replies and decision history** as real persisted workflow.
6. **Document extraction and conflict detection** with its evaluation suite.
7. **Entitlements** for the free/paid boundary in doc 02 §8, as feature flags, with a payment provider in test mode.
8. **Change monitoring** and "what changed" explanations.
9. **Case study** write-up and a recorded walkthrough.

## 6. Running on a small monthly budget

The brief's Azure stack stays. Cost discipline is part of the portfolio story:

- Set an **Azure budget with alerts** before deploying anything, and a hard cap on model spend per day.
- Prefer **scale-to-zero hosting** (for example Azure Container Apps) for the API and workers; the demo doesn't need to be warm.
- Use the **smallest burstable PostgreSQL** tier, and consider **pgvector in PostgreSQL** before Azure AI Search, avoiding a second paid service until retrieval needs justify it.
- Pick the **cheapest model that passes the evaluation suite** for each task; cache extraction results per document version.
- Use **open data and synthetic fixtures** first. Add a paid address or routing provider only when a slice needs it, and record its terms.
- Run ingestion as **scheduled batch jobs**, not always-on services.

Exact prices aren't recorded here because they change. Check current pricing when provisioning, and log the actual monthly cost in the case study.

## 7. Keeping the commercial option open

Do these now, because they are cheap now and expensive later:

- **Code ownership and licence.** Decided: public repository, all rights reserved (section 8). Don't add an open-source licence or accept outside contributions without a contributor agreement, since either would complicate ownership.
- **Data rights.** Record the licence, attribution and commercial-reuse position of every source as it is added (doc 02 §7 lists the open questions, including the EPC terms and OSM tile usage).
- **Privacy by design.** Per-user document isolation, deletion and retention from the first document feature. Before any real user data: UK GDPR basis, a privacy notice, ICO registration if required, and a data protection impact assessment for document processing.
- **Regulated-advice boundary.** Mortgage, legal and tenancy outputs stay information, not advice; wording follows doc 01 §10. Seek professional review before charging.
- **Brand.** Keep "HomeScout" internal, as docs 01 and 02 require. Make names and plan labels configurable so a rename is cheap.
- **Cost per home record.** Measure it from the first AI feature; it is the number that decides whether the Move pass can work.

## 8. Founder decisions

| Question | Decision |
|---|---|
| Repository visibility and licence | **Public, all rights reserved.** No open-source licence; a copyright notice in `LICENSE` and the README. Viewing the code doesn't grant permission to use it. Because it is public, never commit secrets, real personal data or licensed datasets, and accept that competitors can read the strategy documents. |
| First public showcase | **The clickable prototype** (section 5, step 2) |
| Monthly budget cap | **Decided in the infrastructure discussion** (stage 4 below), recorded as an architecture decision record before anything is deployed |

## 9. Roadmap from design decisions to implementation

Each stage ends with a gate. Don't start the next stage until its gate is met. Agents can draft most of the artefacts; you approve each gate.

### Stage 1: Close the design decisions

- Go through the decisions table in doc 02 §9. Confirm or change each "Recommended" row: product category, core object, main value, AI presentation, visual direction, prototype centrepiece and free/paid principle.
- Leave the open ones open (public brand, commercial model, prices). The prototype can work around them with configurable labels.

**Gate:** every row in doc 02 §9 is either confirmed or explicitly marked open with a reason.

### Stage 2: Build the fixture catalogue

The prototype's credibility depends on this, and the images show what happens without it.

- One household, four homes (leasehold buyer flat, buyer comparison home, renter flat, renter comparison home), all in England, each with a fixed ID.
- For each home: address, unit, tenure, type, photo brief, evidence records with source, scope and date, and cost inputs.
- Story documents: the listing, the managing-agent budget, the bills schedule, the partial and full replies.
- Fixed snapshot date of 23 October 2026. Any older source dates are stale deliberately.
- **Every figure computed by a small script**, not typed by hand. The script's worked examples become the first cost-engine tests.

**Gate:** the catalogue is stored as data files in the repository, the script reproduces every number in doc 03 §4, and no fixture contradicts another.

### Stage 3: Write the prototype specification

- A screen-by-screen spec for the 13 screens in doc 03 §5: the content, actions, states and which fixture each uses.
- Step-by-step scripts for the buyer and renter stories, with acceptance criteria for each step.
- The required states from doc 03 §5 (ambiguous match, not covered, stale, partial answer, and so on) assigned to specific screens.
- The free/paid draft from doc 02 §8 shown as labelled, simulated boundaries.

**Gate:** someone who hasn't read docs 01–03 could build the prototype from the spec and the fixtures alone.

### Stage 4: Design, then infrastructure decisions

Design:
- Low-fidelity wireframes for both stories, reviewed against the spec.
- Design tokens and a small component set from doc 03 §6.
- High-fidelity versions of the key screens only: landing, home overview, costs, compare, question detail, reply checking and decision impact.
- One image pass: the shared hero and the matched buyer/renter pair, from the doc 03 §7 prompts.

Infrastructure and architecture, each as a decision record in `docs/decisions/`:
- **Prototype architecture.** Recommended: build the prototype as the real Next.js frontend reading the fixture files, with no backend yet. The prototype code then becomes the product's frontend instead of being thrown away.
- **Hosting for the public demo**, within the Azure direction (a static or scale-to-zero option is enough for a fixture-only frontend).
- **Monthly budget cap** and alert thresholds, plus a daily model-spend cap for later AI features.
- **Repository foundation:** layout, tooling, CI, branch protection and the `CLAUDE.md` agent instructions.

**Gate:** wireframes and key screens approved; decision records merged; the budget cap is set in Azure before the first deployment.

### Stage 5: Start implementation, which is the clickable prototype

Build in vertical slices, each one deployed to the demo:

1. App shell, navigation and design system, loading the fixture catalogue.
2. Buyer story end to end.
3. Renter story end to end, to the same standard.
4. Edge states, mobile layouts and an accessibility pass (WCAG 2.2 AA target).
5. "Illustrative example" labelling, a simulated-action audit, and the public launch of the demo.

**Gate:** both stories run end to end on the public demo, every number comes from the fixture script, and the accessibility checks pass.

### Stage 6: Validate, then build the real product

- Run the six-buyer, six-renter study from doc 02 §10 using the prototype, then revise the specification and fixtures.
- Continue with section 5, steps 3–9: cost engine, real England data, questions workflow, document extraction, entitlements, monitoring, case study. Each starts with its own short spec and decision records, following the rules in section 3.
