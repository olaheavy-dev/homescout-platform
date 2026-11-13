# Vestagraph: project goals and delivery approach

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
6. **Evaluations for every AI task.** Each model-backed task has a fixed evaluation set (synthetic documents, expected citations, known traps such as the listing's £2,400 service charge against the management pack's £3,720 for the same period) that runs in CI. A prompt or model change that lowers the score doesn't merge.
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
| Two complete stories (buyer and renter) in the private prototype (decision 0045) | Product thinking and finished UX | Next.js, accessibility, responsive design |
| Infrastructure as code, tracing, cost controls | Production habits on a small budget | Cost-first hosting (decision 0022), infrastructure as code, OpenTelemetry, cost management |
| Case study and decision records | Communication and judgement | Writing about trade-offs |

The prototype uses the synthetic fixtures and is labelled **Illustrative example** throughout, as doc 03 requires.

## 5. Proposed build sequence

Each step is a vertical slice that leaves a working, demonstrable product. It sequences engineering and learning. It does not remove features from the product or decide what launches. **The stage order in §9 governs timing:** step 1's parts happen in different §9 stages, as noted.

1. **Foundation:** repository conventions and agent instructions (§9 stage 1, done); the fixture catalogue and the **first slice of the C# cost engine**, covering only the calculations the two stories need (§9 stage 2, decision 0019); a minimal CI workflow, security scanning and Dependabot (§9 stage 2, decision 0027); IaC skeleton, deployment pipeline and budget alerts (§9 stage 4, after the infrastructure decisions, before the first deployment). The fixture catalogue covers four English homes, one Welsh home (WALES-1, 7 Harbour Mews, postcode ZZ1 0AA, shown as "not yet covered"), one household and a fixed 23 October 2026 snapshot.
2. **Clickable prototype of both stories** (§9 stage 5) on fixtures and the cost engine's generated results, with a design system from doc 03 §6. It is the **private vision and reference build** for the founder and the coding agents, not a public demo (decision 0045, which replaced the earlier "first public showcase" decision). Decision 0046 makes a free public area check the first public thing (stage 5b).
3. **Cost engine expansion** (§9 stage 6): grows the stage 2 engine to full buy and rent costs, England SDLT, move-in cash and stress scenarios, fully tested, behind the API.
4. **Real England evidence** for one category at a time, with provenance and "not covered" states. Area data (transport, schools, crime counts, flood, sold prices, planning, everyday places) goes live first, at stage 5b (decision 0046); this step then adds per-home evidence such as energy certificates and exact-address matching.
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
- **Brand.** Vestagraph is the working public brand (decision 0044; formerly the code name HomeScout); clearance stays open (0009). Make names and plan labels configurable so a rename is cheap.
- **Cost per home record.** Measure it from the first AI feature; it is the number that decides whether the Move pass can work.

## 8. Founder decisions

| Question | Decision |
|---|---|
| Repository visibility and licence | **Public, all rights reserved.** No open-source licence; a copyright notice in `LICENSE` and the README. Viewing the code doesn't grant permission to use it. Because it is public, never commit secrets, real personal data or licensed datasets, and accept that competitors can read the strategy documents. |
| First public showcase | Superseded by decision 0045: the clickable prototype stays private. Decision 0046: a free public area check first (stage 5b) |
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

The prototype's credibility depends on this, and the images show what happens without it. The approved sample data, the data contract and the task list are in [the stage 2 plan](../planning/stage-2-plan.md); this section summarises them.

- One household (Sam and Alex Rivers, Northbridge, a fictional English town), four English homes (a leasehold buyer flat, a freehold buyer comparison house, and two rentals, one with bills included) and one address in Wales that shows the "not yet covered" state. Every home has a fixed ID and a nation; each English home has a photo brief.
- Inputs live in `packages/fixtures/data/` (household, homes, evidence, documents, questions, replies, snapshot, area), each value with its source, scope and date. Money is in whole pence. JSON Schema 2020-12 files in `packages/fixtures/schema/` check them.
- Story documents: the listings, the leasehold lease, the managing agent's management pack, the written statements of terms for the two rentals (including a revised one), and the partial and specific replies. Fixed snapshot date of 23 October 2026. Any older source dates are stale deliberately.
- **Inputs and calculated outputs kept apart.** Every **calculated output** (monthly housing cost, upfront cash, differences, mortgage repayments) is computed by the cost engine from those inputs and written by the generator to `packages/fixtures/generated/costs.json`, each with a stable figure ID. It is never typed by hand. Test expectations are worked out independently in `packages/fixtures/test-cases/`, as reviewed examples showing their working, never generated by the engine. Items outside this version, such as stamp duty, legal fees and internal maintenance for the leasehold flat, are shown as "not calculated", never as zero.

**Gate:** the catalogue is stored as data files in the repository; every input has a recorded source; the cost engine, not the documents, is the source of every calculated output; doc 03 §4 and this section are corrected to the approved inputs and the engine's generated figures; no fixture contradicts another; CI, dependency review and CodeQL (default setup, `actions` and `csharp`) are required checks on `main` (decision 0027; CodeQL made required by the founder on 11 Nov 2026); a mutation-testing run (Stryker.NET) on the cost engine shows the tests catch planted bugs, with surviving mutants explained in the [mutation report](../reviews/2026-10-23-stage-2-mutation-report.md) (baseline 92.70 %, `break` 92; register line BE-26); C4 context and container diagrams are in [`docs/architecture/`](../architecture/README.md); there are no open `review-followup` issues or security alerts; the whole-repository audit is done; and the founder signs off (full list: stage 2 plan §4).

### Stage 3: Write the prototype specification

**Decisions:**
- **Specification format (SP-01):** where specs live, their template, and how acceptance criteria are written (for example given/when/then or numbered checks) so agents and tests can use them directly.
- **Work breakdown (SP-02):** how a spec turns into issues and slices that are small enough to review.

- A screen-by-screen spec for the 14 screens in doc 03 §5 (13, plus Check an area from decision 0046): the content, actions, states and which fixture each uses.
- Step-by-step scripts for the buyer and renter stories, with acceptance criteria for each step.
- The required states from doc 03 §5 (ambiguous match, not covered, stale, partial answer, and so on) assigned to specific screens.
- MCP tool surface for AI assistants (#117, decision 0037).
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
- **Hosting for the prototype (IN-02):** cost first (decision 0022), and private: local or an access-restricted preview (decision 0045); a fixture-only frontend needs nothing more.
- **Infrastructure as code (IN-03):** match the chosen hosting (decision 0022); Bicep only for any Azure parts.
- **CI/CD and environments (IN-04):** pipeline, pull-request previews, the public site's production environment, secrets handling and domain (needed before stage 5b, decision 0046).
- **Budget cap and cost alerts (IN-05):** the monthly cap and alert thresholds, plus a daily model-spend cap for later AI features.

Design work:
- Low-fidelity wireframes for both stories, reviewed against the spec.
- Design tokens and a small component set from doc 03 §6.
- High-fidelity versions of the key screens only: landing, home overview, costs, compare, question detail, reply checking and decision impact.
- One image pass: the shared hero and the matched buyer/renter pair, from the doc 03 §7 prompts.

**Gate:** wireframes and key screens approved; DS, FE and IN decision records accepted; the budget cap and alerts are in place on every paid service before the first deployment, and the existing server's security issues listed in decision 0022 are fixed before anything of Vestagraph's runs there.

### Stage 5: Start implementation, which is the clickable prototype

**Decisions:**
- **Privacy, part 1 (SE-02), and demo analytics and feedback (FE-05)** move to before the first public release, because the prototype stays private (decision 0045).

Build in vertical slices, each one deployed to the private preview:

1. App shell, navigation and design system, loading the fixture catalogue, and the component gallery.
2. Area screens: summary-first Nearby, the map and Check an area (decision 0046).
3. Home-to-home cost differences in the engine and its generated files (BE-27, #96), before the compare and decision-impact screens.
4. Buyer story end to end.
5. Renter story end to end, to the same standard.
6. Edge states, mobile layouts and an accessibility pass (WCAG 2.2 AA target).
7. "Illustrative example" labelling and a simulated-action audit. There is no public launch (decision 0045).

**Gate:** both stories run end to end on the private prototype, every input comes from the fixture files and every calculated number from the cost engine's generated files, and the accessibility checks pass.

### Stage 5b: Public area check (decision 0046)

The first public release: a free postcode check of what is around a home, with no accounts.

**Decisions first:** the API framework, architecture and contract (BE-01 framework and BE-02, #92) with the observability foundation (decision 0025); database and geospatial (DA-03), ingestion and caching (DA-04), source licences (DA-05), postcode lookup (DA-06, postcode only); hosting, infrastructure, environments, secrets, the domain and a budget cap (IN-01 to IN-05); rate limiting; privacy parts 1 and 2 (SE-02, decision 0014); analytics and feedback (FE-05); for the AI pieces (decision 0051): the AI-09 framework trial, then the model provider (AI-01) and orchestration (AI-04), and the evaluation set (AI-03).

**Build:** a minimal FastAPI API, started from a one-time copy of the founder's FastAPI template (decisions 0040, 0049), with the Aspire app host in TypeScript for local tracing; one adapter per free source with Live, Cached, Fallback or Unavailable labels (0029) and our own cached copies; the area check screens from stage 5 on live data; the small public site (landing as the area check, How it works, About the data, privacy notice, accessibility statement); and, from day one (decision 0051), an on-page area chat and a public read-only MCP server for ChatGPT and Claude, both on the same area tools (design `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`).

**Gate:** every fact shows its source, date and limits; the privacy notice and budget cap are live; searched postcodes are absent from every server, application and hosting log; accessibility checks pass; no feature that needs an account is presented as available; the AI spend caps, rate limits and bot check are live, and the chat and tools pass the evaluation set (decision 0051).

### Stage 6: Validate, then build the real product

Run the six-buyer, six-renter study from doc 02 §10 using the prototype, then revise the specification and fixtures. The [best-practice audit](../reviews/2026-10-23-best-practice-audit.md) lists the stage 6 practices to apply (API contract and generated types, testable time, resilience, log redaction, rate limiting, migrations, health checks and SLOs, build provenance, AI red-teaming). Then continue with section 5, steps 3–9. Each step has its own decision step before it starts:

| Before building | Decisions |
|---|---|
| Cost engine expansion (step 3) | BE-02 and the observability foundation are settled at stage 5b (decision 0046), with the first API; what follows records the starting position. **Backend language and framework (BE-01)** are decided: Python with FastAPI, final (decision 0049, which superseded 0042's .NET 11), with the cost engine started in stage 2 (decision 0019) and ported to Python before the app shell. The order of stage 6 work is in the [backlog](../planning/backlog.md). **Observability foundation (decision 0025):** OpenTelemetry and the Aspire app host and dashboard are set up with the first API code, so every later step is traceable locally. **Backend architecture (BE-02):** e.g. modular monolith, API style and contract (OpenAPI), shared types with the frontend. **Rules versioning (BE-03):** how tax and cost rule tables are stored, cited and reviewed. |
| Real England data (step 4) | DA-03 to DA-05 and privacy part 2 are settled at stage 5b for area data (decision 0046); here they extend to per-home data, and DA-06 decides paid address lookup and routing. Apply **no scraping** (DA-07, decision 0028) and the **outside-services rule** (OP-03, decision 0029) to every source. **Database and geospatial (DA-03):** PostgreSQL/PostGIS confirmation, migrations, hosting tier. **Ingestion and scheduling (DA-04):** batch jobs, storage of raw versus processed data, refresh cadence. **Source licence register (DA-05):** format and review process. **Address and routing providers (DA-06):** when, if ever, to pay for one. **Privacy, part 2 (SE-02):** lawful basis and privacy notice covering personal data in public records, and log handling, before any real data is loaded. |
| Questions workflow (step 5) | **Authentication and accounts (SE-01),** needed before saved homes (decision 0046): identity provider, account model, household sharing. **Privacy and data protection, part 3, the full decision (SE-02):** basis for user-stored data, retention and deletion, document isolation, ICO and DPIA steps. |
| Document extraction (step 6) | Apply the **extraction principles** (AI-06, decision 0030). **Model provider and runtime (AI-01):** the cheapest provider that passes the evaluation suite (decision 0022), Microsoft Foundry included as a candidate, and the model for each task. **Retrieval (AI-02):** pgvector versus Azure AI Search. **Evaluation tooling (AI-03):** evaluation-first is decided (decision 0025); eval sets, scoring and CI gating. **Orchestration (AI-04):** chosen at stage 6 after a short trial of Microsoft Agent Framework for Python against LangChain with LangGraph (decision 0049, AI-09), with the React chat connected over AG-UI, single agents for tasks and chat and a workflow with human approval for document investigation (decision 0023). **AI safety (AI-05):** requirements decided in decision 0025; prompt-injection defences and output validation. Build the AI capabilities in the order set in decision 0025, starting with the evaluation harness. |
| Entitlements (step 7) | **Entitlements and payments (CO-01):** how entitlements are enforced as business rules tied to the account and plan (feature flags only for gradual rollout), and the payment provider in test mode. |
| Monitoring (step 8) | **Observability (OP-01):** OpenTelemetry and the local Aspire dashboard already exist from step 3 (decision 0025); decide where production telemetry goes (cost first), error alerts and cost dashboards. **Scheduling and notifications (OP-02):** change-detection jobs and how users are told. |

## 10. Ways of working

The current rules live in **`AGENTS.md`**, the single rulebook (decisions 0035, 0050). Agents follow the founder's agent-workflows kit: Superpowers skills for each step, plus Vestagraph's own rules. In short:

- **Roles:** you make every decision, approve every gate, and merge founder-only pull requests; you learn through walkthroughs and a weekly explain-back. Agents plan, build, check and review. **Opus 5.5 plans and reviews; Sonnet 5.5 builds and verifies;** Haiku may do clearly mechanical subtasks. Codex reviews every pull request (except small dependency updates) as an independent second opinion.
- **How a decision gets made:** an agent drafts options with a recommendation and asks you in a prompt window (`AGENTS.md`, register WW-16), you choose and give your reason. Hard-to-reverse decisions get a full record; easily reversible ones get a line in the register. Changing a decision means a new record that supersedes the old one.
- **How a change gets made:** agree the change (brainstorming) → plan (data contract first, then backend and frontend tasks; saved in `docs/superpowers/`, summarised in the chat) → build test-first → `make check`, with each acceptance criterion matched to a test → pre-push Opus review with the security reviewer (and the visual reviewer for UI) → pull request → Codex review → fix → merge → summary.
- **Definition of ready:** a plan with acceptance criteria, its fixtures exist, and the decisions it depends on are accepted.
- **Definition of done:** acceptance criteria met; `make check` and CI pass; the change introduces no GitHub security alert (for alerts already open on `main`, see `AGENTS.md`, "When merging", condition 4); works on mobile and with keyboard; no hand-typed calculated figures (inputs come from data files with their source); docs and decision records updated; deployed to the private preview or the public site where relevant.
- **Cadence:** a short weekly plan (which gate is next, which issues serve it) and a weekly review (what shipped, your explain-back, cloud spend against the cap, and coding-agent spend and review rounds). The review ends with a **10-minute process slot**: open `process` issues in agent-workflows and three numbers (review rounds per pull request, P0/P1 findings Codex caught after the pre-push review, decisions reopened); change at most one or two things (decision 0050).
- **Handover:** `docs/planning/status.md` is overwritten at the end of every session with open pull requests, what's next, blockers and your to-dos.
