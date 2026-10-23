# Stage 2 plan: sample data and the first cost-engine slice

**Status:** sample data and inputs approved by the founder on 23 October 2026; plan by the planner (Opus) under decision 0035.  
**Roadmap:** doc 04 §9, stage 2. **Snapshot date for all data:** 23 October 2026.  
**Supersedes for stage 2:** the inputs and story flow in doc 03 §4 and doc 04 §9 stage 2 (for example the £28 water estimate, the £250 "other costs" baseline and the "bills schedule"). Those sections are corrected in task 5.

## 1. Approved sample data (specification)

All data is **synthetic**. Every figure is an **input** with its source label; every total or difference is a **calculated output** from the cost engine (AGENTS.md rule 2). Figures not taken from a real-world document type are labelled honestly, for example "synthetic, modelled on typical 2026/27 English figures". Realism was checked against official and industry sources on 23 October 2026.

### Household
**Sam and Alex Rivers**, a couple moving to Northbridge for work from elsewhere in England, deciding between buying a flat and renting. Budget up to **£1,600 a month** in monthly housing cost (defined below). Priorities: a commute of 40 minutes or less by public transport (routes and destinations are deferred to stage 3), a second bedroom for a home office, no surprise costs.

### Place
**Northbridge**, a fictional English town; postcodes start **NB** (not a UK postcode area). Every address carries a nation field (rule 6). A fifth address, **WALES-1**, in Wales, shows the "not yet covered" state.

### Homes and inputs

| Home | Inputs (source) |
|---|---|
| **B1** Flat 2, 14 Mill Court (leasehold 2-bed, purpose-built) | Asking price £190,000 (listing claim, supplied by you) · service charge £2,400/yr for the 2026 budget period (listing claim) · 2026 budget £3,720/yr (managing agent's management pack, received by the conveyancer after the offer is accepted) · ground rent £250/yr (lease; the proposed £250 cap is **not law**) · lease 125 years from 1 Jan 2015 (lease) · council tax band C (listing) and £2,100/yr for 2026/27 (synthetic Northbridge Council charge) · energy certificate C, issued 2019, estimated £780/yr **at 2019 prices** (context only) · buildings insurance **included in the service charge** (management pack) · internal maintenance **not calculated in this version** (shown as such, never zero) · a major-works question, open, awaiting management-pack answers · its postcode matches 6 flats (unit selection) |
| **B2** 9 Orchard Row (freehold 2-bed terraced house) | Asking price £255,000 (listing claim) · no service charge · council tax band B and £1,850/yr (synthetic) · energy certificate D, issued 2021, estimated £1,150/yr at 2021 prices (context only) · buildings insurance £35/month and maintenance £60/month (user estimates) |
| **R1** Flat 5, 3 Station Road (2-bed, to rent) | Rent £1,200/month (listing claim) · listing says "water included" · written statement of terms, bills section, says the tenant pays water · council tax band A and £1,600/yr (synthetic) · energy certificate C, issued 2022, estimated £720/yr at 2022 prices (context only) · deposit £1,380 (stated by the agent) · first month's rent of £1,200 due after signing (stated by the agent) · assured periodic tenancy |
| **R2** 21 Canal Street (2-bed, to rent) | Rent £1,275/month, bills included: energy, water, broadband; council tax not included (listing and written statement) · council tax band B and £1,850/yr (synthetic) · deposit £1,470 (stated by the agent) · first month's rent of £1,275 due after signing (stated by the agent) · energy certificate **expired in 2025** (issued 2015), shown with cited guidance text: an EPC is needed when a property is let ([gov.uk](https://www.gov.uk/buy-sell-your-home/energy-performance-certificates)); HomeScout's own suggested action (not gov.uk wording): "ask the landlord for a valid certificate" |
| **WALES-1** | Address only; nation Wales; shows "not yet covered" |

**User estimates at today's prices (used in totals):**

| | B1 | B2 | R1 | R2 |
|---|---|---|---|---|
| Energy | £85/month | £120/month | £80/month | included |
| Water (guided by the synthetic Northbridge Water's published 2026/27 charges) | £45/month | £50/month | £45/month | included |
| Broadband | £30/month | £30/month | £30/month | included |

**User-entered:** mortgage deposit £30,000, interest rate 5.5%, term 25 years; moving costs £1,200.

**Energy certificate costs are context only** and never enter totals: their old prices would understate today's cost (rule 7).

**Photo briefs:** B1 a modest low-rise brick block with shared entrance; B2 an ordinary brick terrace; R1 a converted-house flat entrance; R2 a modern small block. Images follow doc 03 §7 and the asset register; none are generated in stage 2.

### Who pays the bills when renting (default)
Tenants pay **energy, water, broadband and council tax** themselves unless the tenancy is **bills included**, in which case the written statement of terms lists exactly which bills the rent covers. R1 is a normal tenancy, so its listing's "water included" is an error the story catches; R2 is a genuine bills-included tenancy (energy, water and broadband; council tax still paid by the tenant).

### Monthly housing cost (definition)
- **Buying:** mortgage repayment + service charge + ground rent + council tax + energy + water + broadband + buildings insurance + maintenance, where each applies; yearly figures converted to monthly by the engine.
- **Renting:** rent + council tax + energy + water + broadband; bills included in the rent are shown as "included", not zero.
- **Upfront cash** is separate. Buying: deposit and moving costs; **stamp duty and legal fees are shown as "not calculated in this version"**, never zero. Renting: deposit + first month's rent (after signing) + moving costs.

### Stories
- **Buyer (B1):** before the offer, the buyer asks the seller's estate agent about the service charge; the vague reply ("usually around the listing figure") leaves the question **Partially answered**. After the offer is accepted, the conveyancer receives the management pack with the 2026 budget (£3,720). **After the user confirms**, the cost assumption updates, keeping the previous value, and B1's own figures change (the comparison with B2 is shown as each home's own figures; the difference between homes is deferred). The major-works question stays open. **Deliberate beat:** B1 within the £1,600 budget on the listing figure and over it on the real budget. This is checked in task 3's hand-worked examples before any engine code; if it doesn't land, the inputs are adjusted and shown to the founder.
- **Renter (R1):** the listing wrongly says "water included"; the tenancy's written statement of terms (required for new private tenancies in England from 1 May 2026: [legislation.gov.uk](https://www.legislation.gov.uk/uksi/2026/324/made), [gov.uk](https://www.gov.uk/guidance/renters-rights-act-overview-for-tenants)) says the tenant pays water, as is normal unless bills are included. A question goes to the agent; a partial reply ("most bills are included") keeps it **Partially answered**; a specific reply with a revised written statement confirms the tenant pays water. **After the user confirms**, the £45/month water estimate is added. R1 and R2 are shown on the same basis, with upfront cash shown separately. Calculated differences between homes are deferred (founder decision), so stage 2 produces each home's own figures and the change within one home.

### Not in stage 2
Deposit-cap checks, stamp duty, legal fees and any other legal or tax rule tables (they need cited rule tables and founder approval). Legal statements appear only as cited text in the data, never as engine logic.

## 2. Data contract (fixed first)

- **Inputs:** `packages/fixtures/data/*.json` — household, homes, evidence items, documents, questions and replies, with the snapshot date. Every value has `source` (origin, document type, date, and "synthetic" where applicable) and `applicability` (unit, building, area). Money in whole pence. Every home and address has a `nation`.
- **Schemas:** `packages/fixtures/schema/*.schema.json`, **JSON Schema 2020-12**, validated by **JsonSchema.Net** (register lines BE-07, licence exception BE-08).
- **Test cases:** `packages/fixtures/test-cases/*.json` — independently worked examples with their working and sources (decisions 0019, 0034).
- **Outputs:** `packages/fixtures/generated/costs.json` — written only by the generator; stable key order; every figure has a stable ID.

## 3. Tasks (one pull request each)

There are no frontend tasks in stage 2; the prototype frontend starts in stage 5. **Dependencies:** tasks 2 and 3 can run alongside task 1 once this plan is merged; task 4a needs task 1 (solution, test runner, CI) and task 3 (reviewed examples); task 4b needs 2, 3 and 4a; task 5 comes last.

| # | Task | Acceptance criteria | Edge cases | Proving tests | Merge |
|---|---|---|---|---|---|
| 1 | **Foundation, agents and permissions:** `global.json`, `HomeScout.slnx`, `Directory.Build.props`, `Directory.Packages.props` with lock files, `nuget.config`, `.editorconfig`, `Makefile` (`check`, `test`, `generate`), .NET tool manifest with InspectCode, Microsoft.Testing.Platform and coverage; CI workflow running `make check` with least-privilege `permissions:` and SHA-pinned actions; CodeQL default setup; dependency review (licence allow-list, InspectCode exception); actionlint and zizmor; `dependabot.yml` (7-day cooldown, patch and minor grouped apart from majors); `.claude/settings.json` (push to `main` denied); agents and the test-first skill; required checks on `main` | `make check` passes locally and in CI on an empty solution; CI fails on a formatting error, an analyser warning and an InspectCode warning; Dependabot config validates | A workflow with an unpinned action is rejected; a package with a non-allowed licence fails dependency review | A deliberate failing commit for each check, reverted | **Founder** (CI, settings, agent permissions) |
| 2 | **Fixture schemas and data:** the contract above and the approved data | Every input in section 1 is present with a source; schemas validate all files in `make check` | WALES-1 is "not yet covered"; R2 bills marked "included", not zero; B1 postcode matches 6 flats; certificate costs flagged context-only; R2 expired certificate with cited text | Schema tests that reject a missing source, a money value with decimals, a missing nation, and a bill recorded as 0 instead of "included" | Founder (approved: licence BE-08) |
| 3 | **Independently worked test cases** | Story calculations worked by hand with working shown: service-charge difference (yearly and monthly), each home's monthly housing cost, upfront cash, renter totals before and after water, mortgage repayment; the B1 budget beat confirmed | Rounding boundaries from decision 0034 applied to each rounded step (annual to monthly, repayment); "not calculated" items stay not calculated | Reviewed by the Opus reviewer before task 4 starts | Claude |
| 4a | **Cost engine basics:** `Pence`, our `Result` type (0032), architecture tests | `Pence` arithmetic and explicit rounding; `Result` for expected failures | Negative amounts; half-penny cases from 0034 | Unit and FsCheck property tests; NetArchTest: no I/O, HTTP, AI, Azure, clock or random | Claude |
| 4b | **Cost engine calculations and generator** | Every task 3 case passes; generator writes `generated/` with stable IDs | Missing **required** inputs return a `Result` failure (any other missing bill becomes a "missing" line and the total is partial), never zero; included bills stay "included" | Data-driven tests from `test-cases/`; FsCheck properties (total equals sum of lines; no negative costs; higher rent never lowers the monthly cost); regenerate-and-diff check in `make check` (`make generated-check`); generator tests run every worked case end to end. Delivered in two pull requests: 4b-1 (output contract and calculations) and 4b-2 (selection, generator and the check) | Claude |
| 5 | **Close-out:** Stryker.NET on the cost engine; doc 03 §4 and doc 04 §9 corrected to this plan's inputs and flow and the engine's outputs; C4 context and container diagrams in `docs/architecture/`; stage 2 audit | Surviving mutants fixed or explained; docs match the generated outputs | — | Stryker report attached to the pull request | Claude |

## 4. Stage 2 gate (from doc 04 §9)
The catalogue is stored as data files; every input has a recorded source; the cost engine is the source of every calculated output; doc 03 §4 and doc 04 §9 corrected to it; no fixture contradicts another; CI, CodeQL and dependency review run with required checks on `main`; a Stryker.NET run shows the tests catch planted bugs, with surviving mutants fixed or explained; no open `review-followup` issues or security alerts; whole-repository audit done; the founder signs off.
