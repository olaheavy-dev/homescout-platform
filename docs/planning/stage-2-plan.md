# Stage 2 plan: sample data and the first cost-engine slice

**Status:** approved by the founder on 23 October 2026 (sample data); plan drafted by the planner (Opus) under decision 0035.  
**Roadmap:** doc 04 §9, stage 2. **Gate:** see the end of this file.

## 1. Approved sample data (specification)

All data is **synthetic** and in England, except one Welsh "not yet covered" address. Every figure is an **input** with its stated source; every total or difference is a **calculated output** from the cost engine (AGENTS.md rule 2). Realism was checked against official and industry sources on 23 October 2026.

### Household
**Sam and Alex Rivers**, a couple relocating to England for work, deciding between buying a flat and renting. Budget up to **£1,600 a month** housing costs. Priorities: commute of 40 minutes or less by public transport, a second bedroom for a home office, no surprise costs.

### Place
**Northbridge**, a fictional English town; postcodes start **NB** (not a UK postcode area). A sixth address in Wales shows the "not yet covered" state.

### Homes and inputs

| Home | Inputs (source) |
|---|---|
| **B1** Flat 2, 14 Mill Court (leasehold 2-bed, purpose-built) | Asking price £205,000 (listing) · service charge £2,400/yr (listing) · 2026 budget £3,720/yr (managing agent's management pack, received via the conveyancer after the offer is accepted) · ground rent £250/yr (lease; the proposed £250 cap is **not law**) · lease 125 years from 1 Jan 2015 (lease) · council tax band C (listing) + Northbridge Council's published 2026/27 band C charge (council website) · energy certificate C, issued 2019, with its estimated yearly energy cost labelled "at 2019 prices – not today's bill" · a major-works question, open, awaiting management-pack answers · its postcode matches 6 flats (unit selection) |
| **B2** 9 Orchard Row (freehold 2-bed terraced house) | Asking price £255,000 (listing) · no service charge · council tax band B (listing) + published band B charge · energy certificate D with estimated cost (labelled as above) · buildings insurance £35/month and maintenance £60/month (user estimates) |
| **R1** Flat 5, 3 Station Road (2-bed, to rent) | Rent £1,200/month (listing) · listing says "water included" · written statement of terms, bills section, says the tenant pays water · council tax band (listing) + published charge · energy certificate estimate (labelled) · broadband £30/month (user estimate) · water £45/month (user estimate, guided by the water company's published 2026/27 charges) · deposit £1,380 (stated by the agent) · assured periodic tenancy |
| **R2** 21 Canal Street (2-bed, to rent) | Rent £1,275/month, bills included: energy, water, broadband; council tax not included (listing and written statement) · deposit £1,470 (stated by the agent) · energy certificate **expired in 2025**: a compliance flag ("the landlord must have a valid certificate before letting; ask for it") |
| **W1** (Wales) | Address only; shows "not yet covered" |

**User-entered:** mortgage deposit £30,000, interest rate 5.5%, term 25 years; moving costs £1,200.

Source labels describe listing practice as standard practice (leaving out material information is an unfair practice under the 2024 consumer law), not the withdrawn trading-standards guidance.

### Stories
- **Buyer (B1):** before the offer, the buyer asks the seller's estate agent about the service charge and gets a vague reply ("usually around the listing figure"). After the offer is accepted, the conveyancer receives the management pack with the 2026 budget (£3,720); the cost assumption updates and the comparison with B2 changes. The major-works question stays open. **Deliberate beat:** B1 should be within the £1,600 budget on the listing figure and over it on the real budget; if the engine's results don't land that way, the inputs are adjusted and shown to the founder before building on them.
- **Renter (R1):** the listing and the written statement disagree on water. A question goes to the agent; a partial reply ("most bills are included") keeps it partly answered; a specific reply with a revised written statement confirms the tenant pays water. The user adds the £45/month estimate. R1 is compared with R2 on the same basis; move-in cash (deposit, at most one month's rent after signing, and moving costs) is shown separately.

### Not in stage 2
Deposit-cap checks, stamp duty and any other legal or tax rule tables (they need cited rule tables and founder approval). Doc 03's provisional story figures are corrected to the engine's results.

## 2. Data contract (fixed first)

- **Inputs:** `packages/fixtures/data/*.json` — household, homes, evidence items, documents, questions and replies. Every value carries `source` (origin, document, date) and `applicability`. Money in whole pence.
- **Schemas:** `packages/fixtures/schema/*.schema.json` (JSON Schema; draft chosen in task 3).
- **Test cases:** `packages/fixtures/test-cases/*.json` — independently worked examples with their working shown (decisions 0019, 0034).
- **Outputs:** `packages/fixtures/generated/*.json` — written only by the cost engine's generator; stable key order; every figure has a stable ID.

## 3. Tasks (each one pull request)

There are no frontend tasks in stage 2; the prototype frontend starts in stage 5.

| # | Task | Side | Merge |
|---|---|---|---|
| 1 | **Build and CI foundation:** `global.json`, `HomeScout.slnx`, `Directory.Build.props`, `Directory.Packages.props` with lock files, `nuget.config`, `.editorconfig`, `Makefile` (`make check`, `make test`, `make generate`), .NET tool manifest with InspectCode, CI workflow running `make check`, CodeQL default setup, dependency-review (with the licence allow-list and the InspectCode exception), actionlint and zizmor, `dependabot.yml` (7-day cooldown; patch and minor grouped apart from majors), required checks on `main` | Backend | Founder (CI permissions, settings) |
| 2 | **Agents and permissions:** `.claude/settings.json` allow-list (push to `main` denied), agents (planner, implementer, verifier, reviewer, review handler) with their models, the test-first skill | Tooling | Founder (agent permissions) |
| 3 | **Fixture schemas and data:** the contract above; the approved sample data; schema validation in `make check` | Backend (data) | Claude |
| 4 | **Independently worked test cases:** story calculations and rounding boundaries (0034), worked by hand with sources, reviewed before any engine code | Backend (tests) | Claude |
| 5 | **Cost engine slice:** `Pence`, our `Result` type (0032), the story calculations, the generator, property-based tests (FsCheck), architecture tests | Backend | Claude |
| 6 | **Close-out:** mutation testing (Stryker.NET) on the cost engine, doc 03 figures corrected to the engine's output, C4 context and container diagrams, stage 2 audit | Backend and docs | Claude |

## 4. Stage 2 gate (from doc 04 §9)
Every input has a recorded source; the cost engine is the source of every calculated output; doc 03 §4 corrected to it; no fixture contradicts another; CI, CodeQL and dependency review run with required checks on `main`; a Stryker.NET run shows the tests catch planted bugs; no open `review-followup` issues or security alerts; whole-repository audit done; the founder signs off.
