# HomeScout: project goals and delivery approach

**Date:** 23 October 2026  
**Confirmed by the founder:** The project is a portfolio and learning project first, built mostly by AI coding agents, on a small monthly running budget, and kept commercially viable for later.  
**Authority:** This document owns how the product is built, run and presented. `02-research-and-direction.md` still owns product and commercial decisions; `03-prototype-and-image-direction.md` still owns prototype behaviour and design.  
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

- **In the build:** agents write most of the code, tests, infrastructure and documentation, working from the specs in this folder. Opus 5.5 plans and reviews (including a fresh-context review before every push); Sonnet 5.5 builds and verifies; OpenAI Codex reviews every pull request (except small dependency updates) as an independent second opinion (decision 0035, rules in `AGENTS.md`). You set direction and own decisions, merge founder-only pull requests, and review routine changes by exception.
- **In the product:** behaviour stays mostly deterministic. AI is used inside specific tasks (document extraction, drafting a question, checking a reply, explaining a change) as single, task-specific model calls with tools, **plus an optional, closable chat panel about the current home** (decision 0004). The chat cites evidence or says it doesn't know, uses the cost engine for any number, and needs its own scripted sample replies in the prototype and its own evaluation set later. All numbers come from deterministic code. Microsoft Agent Framework is the AI framework (decision 0023): single agents for tasks and chat, and a workflow with a human approval step for document investigation. Calculations stay in plain code.

This is also the stronger portfolio story: "AI-assisted engineering with rigorous verification" is more credible to a reviewer than "a dashboard of agents."

## 3. Working rules for agent-built code

These keep agent output reviewable and keep you learning rather than rubber-stamping.

1. **Spec before code.** Each slice starts from a short written spec that links to the relevant sections in 02/03. Agents implement against the spec; changes to the spec are your decision.
2. **Small vertical slices.** One user-visible capability per pull request, kept small enough to review properly.
3. **Tests first for anything numeric or legal.** Cost, tax and lease-date logic gets table-driven tests with worked examples before implementation. The image 5 mortgage error in doc 03 is exactly what this prevents.
4. **Rules come from cited sources, not model memory.** SDLT bands, tenancy rules and inspection frameworks live in versioned rule tables with a source URL and effective date. You review every rule table change.
5. **Decision records.** Every hard-to-reverse choice gets a short decision record in `docs/decisions/`, written in your words; easily reversible ones get a line in the register (decision 0035). If you can't write the record, you don't understand the choice yet.
6. **Evaluations for every AI task.** Each model-backed task has a fixed evaluation set (synthetic documents, expected citations, known traps such as the £2,400 vs £3,720 period mismatch) that runs in CI. A prompt or model change that lowers the score doesn't merge.
7. **Agent guardrails in the repo.** A `CLAUDE.md` (or equivalent) records conventions, commands, the "no invented facts" rule and the commercial constraints below, so every agent session starts with them.
8. **No real personal data.** Development and demos use the synthetic fixture catalogue from doc 03. Real documents are only for consented research sessions, kept outside the repository.
9. **Licence check before ingestion.** No dataset, map tile or image enters the repository or pipeline until its licence and attribution terms are recorded.
10. **Explain-back.** Once a week, for each significant slice merged that week, you write a few lines on how it works (decision 0035). This is the learning record and the raw material for the case study.

## 4. What makes it portfolio-worthy

Reviewers have seen many AI-wrapper apps. These are the parts that make this one stand out, and what each teaches:

| Showcase | What it demonstrates | What you learn |
|---|---|---|
| Evidence model with provenance (origin, scope, time, status, interpretation) | Data modelling for trust, not just storage | Domain modelling, temporal data, PostgreSQL/PostGIS |
| Deterministic cost engine (buy and rent, England SDLT, stress scenarios) | Correctness, tested financial logic, versioned rules | Test design, money/rounding, rule versioning |
| England open-data ingestion (EPC, Price Paid, planning, flood) with coverage states | Real-world messy data, honest gaps, attribution | ETL, matching property identity, geospatial joins |
| Document extraction with page-level citations and conflict detection | Grounded AI with a measured evaluation suite | Retrieval, structured extraction, evals, prompt-injection defence |
| AI platform: tracing, token and cost monitoring, safety, workflows with human approval, routing, caching, streaming (decision 0025) | Production-grade AI engineering, debuggable locally with Aspire | Microsoft Agent Framework, OpenTelemetry, Aspire, evaluation-first development |
| Question → reply → decision history | Workflow and state-machine design with audit trail | Event history, versioning, UX for uncertainty |
| Two complete stories (buyer and renter) in a public demo | Product thinking and finished UX | Next.js, accessibility, responsive design |
| Infrastructure as code, tracing, cost controls | Production habits on a small budget | Cost-first hosting (decision 0022), infrastructure as code, OpenTelemetry, cost management |
| Case study and decision records | Communication and judgement | Writing about trade-offs |

The public demo uses the synthetic fixtures and is labelled **Illustrative example** throughout, as doc 03 requires.

## 5. Proposed build sequence

Each step is a vertical slice that leaves a working, demonstrable product. It sequences engineering and learning. It does not remove features from the product or decide what launches. **The stage order in §9 governs timing:** step 1's parts happen in different §9 stages, as noted.

1. **Foundation:** repository conventions and agent instructions (§9 stage 1, done); the fixture catalogue and the **first slice of the C# cost engine**, covering only the calculations the two stories need (§9 stage 2, decision 0019); a minimal CI workflow, security scanning and Dependabot (§9 stage 2, decision 0027); IaC skeleton, deployment pipeline and budget alerts (§9 stage 4, after the infrastructure decisions, before the first deployment). The fixture catalogue covers (four homes, one household, fixed 23 October 2026 snapshot).
2. **Clickable prototype of both stories** (§9 stage 5) on fixtures and the cost engine's generated results, with a design system from doc 03 §6. This alone is a presentable portfolio piece, and it is **the first public showcase** (founder decision).
3. **Cost engine expansion** (§9 stage 6): grows the stage 2 engine to full buy and rent costs, England SDLT, move-in cash and stress scenarios, fully tested, behind the API.
4. **Real England evidence** for one category at a time (EPC, then Price Paid, then planning and flood), with provenance and "not covered" states.
5. **Questions, replies and decision history** as real persisted workflow.
6. **Document extraction and conflict detection** with its evaluation suite.
7. **Entitlements** for the free/paid boundary in doc 02 §8, enforced as business rules tied to the account and plan (not a feature-flag toggle; flags are only for gradual rollout), with a payment provider in test mode. CO-01 settles the design.
8. **Change monitoring** and "what changed" explanations.
9. **Case study** write-up and a recorded walkthrough.

## 6. Running on a small monthly budget

Hosting is **cost first** (decision 0022): free options first, then the founder's existing server, and Azure or another paid service only where neither meets the need. Cost discipline is part of the portfolio story:

- Set **budget alerts** on every paid service before deploying anything, and a hard cap on model spend per day.
- Host the fixture-only demo on a **free** option, and the API and workers on the **existing server** where possible; if a paid cloud service is needed, prefer one that scales to zero.
- Run **PostgreSQL with PostGIS** on the existing server before paying for a managed database, and use **pgvector in PostgreSQL** before any paid search service, until needs justify more.
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

Each stage ends with a gate. Don't start the next stage until its gate is met, except that stages 3 and 4 may overlap (decision 0035). Agents can draft most of the artefacts; you approve each gate. Every gate also requires a whole-repository audit for contradictions and debt, and no open `review-followup` issues (decision 0035).

Every stage begins with its **decision step**: the individual decisions that must be made before the stage's work starts. Hard-to-reverse decisions each get a separate decision record in `docs/decisions/` with options, a recommendation and your choice. The full register, with IDs and status, is in `docs/decisions/README.md`. A decision is made at the latest stage that still lets the work go ahead. Choices that only matter later stay open until then. Easily reversible ones get one line in the register with their default (decision 0035).

### Stage 1: Close the design decisions and set how we work

**Decisions** (checklist: `docs/planning/stage-1-confirmation.md`):
- **Product (PD-01 to PD-07):** confirm or change each "Recommended" row in doc 02 §9.
- **Ways of working (WW-01):** roles, flow of a change, definition of done, how decisions get made and recorded (section 10).
- **AI coding tools and setup (WW-02):** which coding agent(s) and models, agent instructions file, permissions, hooks and integrations, how agent sessions are reviewed, and the tool subscription cost.
- **Repository and tracking conventions (WW-03):** repo layout, branch and commit conventions, branch protection, where issues and the plan are tracked.

Agents start producing artefacts in stage 2, so how they work has to be settled first.

**Gate:** every product row is confirmed or explicitly open with a reason; WW-01 to WW-03 accepted; `CLAUDE.md` and the decision-record template are in the repository.

### Stage 2: Build the fixture catalogue

**Decisions:**
- **Fixture data format (DA-01):** decided: JSON files with a JSON Schema (decision 0018).
- **Calculation script and test vectors (DA-02):** decided: the calculations start as the real C# cost engine, whose generator writes results into the sample-data files; tests check the engine against independently worked examples (decision 0019). Application languages are confirmed as C# for the backend and TypeScript with Next.js for the frontend (decision 0020).
- **Result type (BE-05):** decided: our own small type (decision 0032). **Rounding boundary cases (BE-06):** decision 0034. **Data sourcing (DA-07):** no scraping (decision 0028), which also shapes the fixtures.
- **.NET engineering foundation (BE-04):** decided: strict build settings, pinned packages, Makefile, NUnit and architecture tests (decision 0021).

The prototype's credibility depends on this, and the images show what happens without it.

- One household, four homes (leasehold buyer flat, buyer comparison home, renter flat, renter comparison home), all in England, each with a fixed ID.
- For each home: address, unit, tenure, type, photo brief, evidence records with source, scope and date, and cost inputs.
- Story documents: the listing, the managing-agent budget, the bills schedule, the partial and full replies.
- Fixed snapshot date of 23 October 2026. Any older source dates are stale deliberately.
- **Inputs and calculated outputs kept apart.** Inputs (the listing's £2,400 claim, the managing-agent budget's £3,720, rent, the user-entered £28 water estimate, and so on) are stored in the fixture files with their source. **Every calculated output** (totals, differences, monthly equivalents, comparisons) is computed by the C# cost engine from those inputs, never typed by hand, and written to the generated files. Test expectations are worked out independently as reviewed examples showing their working, never generated by the engine.

**Gate:** the catalogue is stored as data files in the repository; every input has a recorded source; the cost engine, not the documents, is the source of every calculated output; each value in doc 03 §4 has been checked against its output and corrected where it differed; no fixture contradicts another; the minimal CI, CodeQL and dependency review are running with required checks on `main` (decision 0027); and a mutation-testing run (Stryker.NET) on the cost engine shows the tests catch planted bugs, with any surviving mutants fixed or explained.

### Stage 3: Write the prototype specification

**Decisions:**
- **Specification format (SP-01):** where specs live, their template, and how acceptance criteria are written (for example given/when/then or numbered checks) so agents and tests can use them directly.
- **Work breakdown (SP-02):** how a spec turns into issues and slices that are small enough to review.

- A screen-by-screen spec for the 13 screens in doc 03 §5: the content, actions, states and which fixture each uses.
- Step-by-step scripts for the buyer and renter stories, with acceptance criteria for each step.
- The required states from doc 03 §5 (ambiguous match, not covered, stale, partial answer, and so on) assigned to specific screens.
- The free/paid draft from doc 02 §8 shown as labelled, simulated boundaries.

**Gate:** someone who hasn't read docs 01–03 could build the prototype from the spec and the fixtures alone.

### Stage 4: Design, frontend, infrastructure and deployment decisions

Inputs from the founder's earlier projects are summarised in the [foundations review](../reviews/2026-10-23-foundation-review.md). Stage 4 and stage 6 items from the [best-practice audit](../reviews/2026-10-23-best-practice-audit.md) are inputs too.

**Design decisions:**
- **Design tooling (DS-01):** decision 0031 indicates code-first with the designer-skills plugin; confirm here. Options were design-tool-first (for example Figma) versus code-first (wireframes and components built directly in code with a component workbench).
- **Design system foundation (DS-02):** tokens, typography and fonts, icon set, component inventory, and accessibility checks.

**Frontend decisions:**
- **Framework and rendering (FE-01):** TypeScript with Next.js is confirmed (decision 0020); decide the routing model, and static versus server rendering for a fixture-only demo.
- **Styling and components (FE-02):** styling approach and whether to build on an accessible headless component library.
- **Maps and charts (FE-03):** map library, tile provider and its terms, and the charting approach.
- **Frontend practices (FE-04):** unit, component and end-to-end testing, automated accessibility checks, linting and formatting, en-GB copy and number/currency formatting, performance budgets, and the folder structure.

**Infrastructure and deployment decisions:**
- **Prototype architecture (IN-01):** recommended: the prototype is the real frontend reading fixture files, with no backend yet.
- **Hosting for the public demo (IN-02):** cost first (decision 0022): a free static option or the existing server; a fixture-only frontend needs nothing more.
- **Infrastructure as code (IN-03):** match the chosen hosting (decision 0022); Bicep only for any Azure parts.
- **CI/CD and environments (IN-04):** pipeline, pull-request previews, production demo, secrets handling and domain.
- **Budget cap and cost alerts (IN-05):** the monthly cap and alert thresholds, plus a daily model-spend cap for later AI features.

Design work:
- Low-fidelity wireframes for both stories, reviewed against the spec.
- Design tokens and a small component set from doc 03 §6.
- High-fidelity versions of the key screens only: landing, home overview, costs, compare, question detail, reply checking and decision impact.
- One image pass: the shared hero and the matched buyer/renter pair, from the doc 03 §7 prompts.

**Gate:** wireframes and key screens approved; DS, FE and IN decision records accepted; the budget cap and alerts are in place on every paid service before the first deployment, and the existing server's security issues listed in decision 0022 are fixed before anything of HomeScout's runs there.

### Stage 5: Start implementation, which is the clickable prototype

**Decisions:**
- **Privacy, part 1, visitor data (SE-02):** lawful basis and a short privacy notice for visitor data handled by the site and hosting (IP addresses, browser details, host logs), whether the ICO data protection fee is due (and paying it if so), and a check of anything stored on visitors' devices, all before the demo goes public.
- **Demo analytics and feedback (FE-05):** whether to measure demo use at all, and if so a privacy-friendly option needing no cookie banner, plus how viewers can leave feedback.

Build in vertical slices, each one deployed to the demo:

1. App shell, navigation and design system, loading the fixture catalogue.
2. Buyer story end to end.
3. Renter story end to end, to the same standard.
4. Edge states, mobile layouts and an accessibility pass (WCAG 2.2 AA target).
5. "Illustrative example" labelling, a simulated-action audit, and the public launch of the demo.

**Gate:** both stories run end to end on the public demo, every input comes from the fixture files and every calculated number from the cost engine's generated files, and the accessibility checks pass.

### Stage 6: Validate, then build the real product

Run the six-buyer, six-renter study from doc 02 §10 using the prototype, then revise the specification and fixtures. The [best-practice audit](../reviews/2026-10-23-best-practice-audit.md) lists the stage 6 practices to apply (API contract and generated types, testable time, resilience, log redaction, rate limiting, migrations, health checks and SLOs, build provenance, AI red-teaming). Then continue with section 5, steps 3–9. Each step has its own decision step before it starts:

| Before building | Decisions |
|---|---|
| Cost engine expansion (step 3) | **Backend language (BE-01)** is decided: C# on .NET (decision 0020), and BE-01 stays open only for the framework, with the cost engine started in stage 2 (decision 0019); confirm ASP.NET Core for the API. **Observability foundation (decision 0025):** OpenTelemetry and the Aspire app host and dashboard are set up with the first API code, so every later step is traceable locally. **Backend architecture (BE-02):** e.g. modular monolith, API style and contract (OpenAPI), shared types with the frontend. **Rules versioning (BE-03):** how tax and cost rule tables are stored, cited and reviewed. |
| Real England data (step 4) | Apply **no scraping** (DA-07, decision 0028) and the **outside-services rule** (OP-03, decision 0029) to every source. **Database and geospatial (DA-03):** PostgreSQL/PostGIS confirmation, migrations, hosting tier. **Ingestion and scheduling (DA-04):** batch jobs, storage of raw versus processed data, refresh cadence. **Source licence register (DA-05):** format and review process. **Address and routing providers (DA-06):** when, if ever, to pay for one. **Privacy, part 2 (SE-02):** lawful basis and privacy notice covering personal data in public records, and log handling, before any real data is loaded. |
| Questions workflow (step 5) | **Authentication and accounts (SE-01):** identity provider, account model, household sharing. **Privacy and data protection, part 3, the full decision (SE-02):** basis for user-stored data, retention and deletion, document isolation, ICO and DPIA steps. |
| Document extraction (step 6) | Apply the **extraction principles** (AI-06, decision 0030). **Model provider and runtime (AI-01):** the cheapest provider that passes the evaluation suite (decision 0022), Microsoft Foundry included as a candidate, and the model for each task. **Retrieval (AI-02):** pgvector versus Azure AI Search. **Evaluation tooling (AI-03):** evaluation-first is decided (decision 0025); eval sets, scoring and CI gating. **Orchestration (AI-04):** decided: Microsoft Agent Framework, with single agents for tasks and chat and a workflow with human approval for document investigation (decision 0023). **AI safety (AI-05):** requirements decided in decision 0025; prompt-injection defences and output validation. Build the AI capabilities in the order set in decision 0025, starting with the evaluation harness. |
| Entitlements (step 7) | **Entitlements and payments (CO-01):** how entitlements are enforced as business rules tied to the account and plan (feature flags only for gradual rollout), and the payment provider in test mode. |
| Monitoring (step 8) | **Observability (OP-01):** OpenTelemetry and the local Aspire dashboard already exist from step 3 (decision 0025); decide where production telemetry goes (cost first), error alerts and cost dashboards. **Scheduling and notifications (OP-02):** change-detection jobs and how users are told. |

## 10. Ways of working

The current rules live in **`AGENTS.md`**, the single rulebook (decision 0035). In short:

- **Roles:** you make every decision, approve every gate, and merge founder-only pull requests; you learn through walkthroughs and a weekly explain-back. Agents plan, build, check and review. **Opus 5.5 plans and reviews; Sonnet 5.5 builds and verifies.** Codex reviews every pull request (except small dependency updates) as an independent second opinion.
- **How a decision gets made:** an agent drafts options with a recommendation, you choose and give your reason. Hard-to-reverse decisions get a full record; easily reversible ones get a line in the register. Changing a decision means a new record that supersedes the old one.
- **How a change gets made:** plan (data contract first, then backend and frontend tasks) → build → `make check` → pre-push Opus review → pull request → Codex review → fix → merge → summary.
- **Definition of ready:** a plan with acceptance criteria, its fixtures exist, and the decisions it depends on are accepted.
- **Definition of done:** acceptance criteria met; `make check` and CI pass; the change introduces no GitHub security alert (for alerts already open on `main`, see `AGENTS.md`, "When merging", condition 4); works on mobile and with keyboard; no hand-typed calculated figures (inputs come from data files with their source); docs and decision records updated; deployed to the demo where relevant.
- **Cadence:** a short weekly plan (which gate is next, which issues serve it) and a weekly review (what shipped, your explain-back, cloud spend against the cap, and coding-agent spend and review rounds).
