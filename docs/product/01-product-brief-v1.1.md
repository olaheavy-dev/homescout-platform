# HomeScout Copilot
## Product Brief and Experience Direction
**Version:** 1.1 — Revised positioning and competitor landscape  
**Date:** 23 October 2026  
**Scope:** Entire proposed product; **no MVP / post-MVP feature classifications**  
**Status:** Historical concept record, with subsequent scope and review annotations; not the current implementation specification or a statement of integrated data or launched capability.  
**Precedence:** `02-research-and-direction.md` owns current product recommendations, decision status and geographic scope. `03-prototype-and-image-direction.md` owns proposed prototype behaviour and design within that scope. Current recommendations favour Home overview over Passport, contextual AI over named-agent presentation, and a Move pass experiment over a settled Copilot Plus offer. Payment model and entitlements remain open. The later documents also revise visual tokens and reject `HomeCompass` as a proposed brand alternative. Historical descriptions below do not establish current entitlements or approvals. `04-project-goals-and-delivery.md` owns how the product is built: mostly by AI coding agents, with multi-agent runtime orchestration (sections 6 and 13) deferred until a measured task needs it.  
**Launch geography:** England first (confirmed by the founder; see section 9). This is geographic scope, not an MVP feature classification.

> **Know the home before you commit.** Independent, evidence-led property intelligence for renting and buying across the United Kingdom.

The UK-wide line above describes the original ambition. Proposed launch-facing copy must state **England**, with other UK nations shown as not yet covered.

## 1. Executive summary
HomeScout Copilot (**working project name; public brand not selected**) is a UK-only evidence-led property decision workspace for people evaluating a home to rent or buy. It consolidates publicly available information, correctly licensed data, user-supplied property materials, transparent financial modelling and AI-assisted investigation into one coherent experience.

The platform is **not** another listing marketplace, a substitute for conveyancing or surveying, a mortgage adviser, or a general-purpose chat application. Its principal object is a **living property decision record** (consumer term: **home record**; see the glossary in `03-prototype-and-image-direction.md` §3): a persistent, versioned account of what is known, estimated, missing or conflicting; how it affects a particular household; which questions remain open; who can answer them; and what changed between decision checkpoints.

The entry point must be simple: search a postcode or address, choose renting/buying, and see a useful free investigation. The deeper product revolves around the **Property Intelligence Passport**, **Neighbourhood Explorer**, **True Cost & Household Fit Simulators**, and **Compare Homes**. The premium experience adds a **Living Evidence Record**, **Copilot Investigation**, **Document Reconciliation**, **Question-to-Resolution Workflow**, **Change Monitoring**, and a **Decision Workspace**.

The strongest opportunity is not a proprietary 0–100 "good home" score or a one-time AI-generated report. It is a consumer-first, accountable process that helps answer: **Does this home meet my priorities? What do the sources disagree on? Can I afford the realistic downside? Which questions need answers, who will provide them, and what changed since I last checked?**

## 2. Problem and opportunity
A UK house or flat is often evaluated using a sales or rental listing, a few viewings and fragmented web research. Users must navigate sold-price records, energy certificates, flood maps, local authority planning portals, school directories, broadband and transport data, council tax/rates, tenancy rules, mortgage calculators, lease packs and surveys. The existence of data does not mean it is complete or attached to the correct property.

Typical failures include:
- Confusing **postcode or area data** with **property-specific evidence**.
- Not seeing the true recurring and upfront costs of ownership or renting.
- Overlooking material leasehold, service-charge or tenancy conditions.
- Believing proximity to a school guarantees admission, or an available public-transport stop guarantees a suitable timetable.
- Taking old, missing or conflicting datasets as current verified facts.
- Losing track of findings, documents, viewing questions and property comparisons between sessions.

HomeScout combines evidence, accessible interpretation and next steps. Its product experience should reinforce that missing information is a meaningful finding, not something to fill in with AI invention.

## 3. Users and their jobs to be done
**First-time buyer:** 'Before I spend money or make an offer, show me the total cost, red flags, comparable evidence and questions for my solicitor/surveyor.'

**Move-up buyer:** 'Help me compare alternative homes against commute, schools, renovation potential, affordability and running costs.'

**Private renter:** 'Show the realistic cost of living here, the local amenities, tenancy considerations, deposit and rent requirements, and the questions to ask before signing.'

**Relocating household:** 'Help me understand an unfamiliar UK location through transport connections, nearby essentials, childcare, education, health services and lifestyle needs.'

**Leasehold flat buyer:** 'Help me assess missing documentation, service-charge history, major works, ground rent and lease terms without implying the product replaces legal review.'

Do not infer household attributes or values from demographics. Let users state their own priorities; the system should not label residents or communities as inherently desirable or undesirable.

## 4. Positioning and promise
**Category:** Independent UK property decision intelligence.  
**Primary promise:** Understand a home before you make a financial or legal commitment.  
**Supporting promises:** Evidence you can inspect; costs you can test; options you can compare; questions you can act on.

**Brand decision:** Public name **unselected**. `HomeScout Copilot` is a working title only, and brand assets must remain easy to rename. `HomeCompass` and `HomeLedger` have notable existing uses (section 5.5).
**Brand voice:** Assured, plain-spoken, specific, respectful and curious; never alarmist or falsely certain.  
**Recommended tagline:** *Know the home before you commit.*  
**Alternative:** *A clearer picture of every home.*

Avoid 'AI estate agent', 'guaranteed safe', 'legally approved', 'always accurate', or universal quality ratings. Never pretend that a service has assessed an entire building when it has only checked a surrounding geographic polygon.

## 5. Competitor landscape and design lessons
**Original register date:** 23 October 2026. Entries describe publicly advertised offerings, not tested subscriptions or independent claims of accuracy. The dated, inspected subset is the 12-product table in document 02, section 3; other entries below were not revalidated in that research pass. Retain them as research leads rather than treating this entire register as checked. Category placement is practical rather than exclusive. Some sources show inconsistent or changing pricing/coverage, so product design must not rely on competitor marketing claims as authoritative facts.

### 5.1 Direct UK consumer property intelligence and due diligence
| Product | Publicly presented positioning | Design implication for HomeScout |
|---|---|---|
| [bythenumbers](https://www.bythenumbers.uk/) | Area measure, transparent UK open-data categories and 22 free calculators | Basic data, maps, comparisons and calculators are a free baseline, not a paywall differentiator. |
| [HomeAtlas](https://gethomeatlas.co.uk/) | UK postcode and property-link analysis; schools, crime, commute, affordability and personalised scores | Location scoring and listing-link comparison are already market offerings. |
| [HomeBuyerCheck](https://www.homebuyercheck.co.uk/) | Low-price UK pre-offer checks; AI buyer verdicts, negotiation material and specialist briefs | AI-generated professional question packs and cheap reports are not unique. |
| [HouseCheckup](https://housecheckup.co.uk/) | Paid property/environmental report with covered sources, scores, professional review and gaps | Missing-data disclosure and human review already exist; HomeScout needs continuing, interactive workflows. |
| [CheckNext](https://checknext.co.uk/) | Listing analysis, viewing checklist, survey review and maintenance estimates | AI viewing and survey summaries already exist; improve traceability and issue closure. |
| [HomeVerdict](https://www.homeverdict.co.uk/) | Property-link AI verdict, personalised buyer-fit scoring, offer guidance, confidence | Personalised ranking and pricing heuristics cannot be the only promise. |
| [BackStory](https://backstory.homes/) | Human-reviewed investigation reports, especially UK flats, lease and building risks | Investigations need explainability and user-led updates beyond a one-time report. |
| [Property Due Diligence](https://propertyduediligence.co.uk/) | Baseline and paid risk briefs; public sources, workspace and conveyancing-oriented analysis | Workspace labels alone do not establish sustained decision workflows. |
| [PropertyChecker](https://beta.propertychecker.co.uk/house-check/) | Free England/Wales house checks with sold prices, EPC, running costs and other available fields | Simple facts and property identity must be credible, transparent and low friction. |
| [Chimnie Consumer](https://www.chimnie.co.uk/) | Property-level public research and data-backed reports | Property-level data aggregation already exists; differentiate on consumer decisions and follow-through. |
| [PlaceProof](https://placeproof.co.uk/) | Open-data-based place research, recorded crime, schools and amenities | Explain source limits and avoid simplistic area judgements. |
| [MyPropertyScan](https://www.mypropertyscan.com/) | Free property-risk preview and one-off buyer reports with costs and questions | Risk scans plus PDF outputs are already low-priced and widely available. |
| [Check Before You Buy](https://checkbeforeyoubuy.co.uk/) | Rightmove-link research, free snapshot, paid action-plan report and human-reviewed investigation (*not revalidated in the 02 research: site timed out*) | Even prioritised actions and human-reviewed one-off investigations exist; differentiation must include sustained evidence/answer tracking. |
| [LandSale Reports](https://www.landsale.co.uk/reports) | Property intelligence reports with official datasets, planning, flood and amenities | Extensive category-level checks are already sold cheaply; source quality and workflow matter more than the count of checks. |
| [UK Property Check](https://ukpropertycheck.co.uk/) | England/Wales property evidence checks with transparent freshness and geographic gaps | Freshness and source limitation are also competitive hygiene. |

### 5.2 Neighbourhood, schools, money and property guidance
| Product | Focus | Design implication |
|---|---|---|
| [Crystal Roof](https://crystalroof.co.uk/) | Neighbourhood intelligence covering transport, noise, environment, schools, amenities and demographics | Strong map/data inspiration; avoid demographic desirability rankings. |
| [Locrating](https://www.locrating.com/) | Schools and catchment-related research | Schools need careful nation-specific nuance; proximity does not guarantee admission. |
| [Dwellmark](https://dwellmark.co.uk/) | UK property guidance, calculators and dated primary-source references | Dated citations and accurate deterministic calculations are a minimum trust standard. |
| [NestVerdict](https://nestverdict.com/) | User-weighted home comparisons and decision rankings | User-controlled criteria are useful, but reduce misleading composite scores. |
| [Move iQ](https://www.moveiq.co.uk/) | Homebuying advice and property reports (historically Sprift-powered) | Use professional report structure without making a static PDF the centre of the experience. |
| [Before](https://www.before.ng/) | Nigerian address-first checks, including location security and flooding | Keep the very simple search-first UI as a design reference; not a UK direct competitor. |

### 5.3 Discovery, search and ongoing renter/buyer workflows
| Product | Focus | Design implication |
|---|---|---|
| [Rightmove](https://www.rightmove.co.uk/) | UK listings and house-search journey | HomeScout complements discovery rather than replicating listing inventory. |
| [Zoopla](https://www.zoopla.co.uk/) | UK listings, prices and consumer property information | Avoid attempting a generic portal. |
| [OnTheMarket](https://www.onthemarket.com/) | Listings and agency-led property search | Obtain content rights before relying on listing aggregation. |
| [OpenRent](https://www.openrent.co.uk/) | Direct rental listings and landlord/tenant workflows | A useful renter discovery reference; do not substitute for due diligence. |
| [HomeSift](https://homesift.app/) | Personalised daily UK property digests, price tracking and shared search | Shortlisting, alerts and collaborative preferences are already available. |
| [MyHomeScout](https://myhomescout.co.uk/) | Early-access tailored UK property matching and buyer preference interpretation (*not revalidated in the 02 research: no readable page body*) | Treat as a research lead until the advertised feature set can be inspected. |
| [HomeScout UK](https://www.homescout.org.uk/) | London rental alerts through messaging | Meaningful **naming conflict** with the existing HomeScout project name. |
| [HomeScout Ireland](https://homescout.io/) | AI renter search, viewing, messages and lease review | Strong adjacent renter workflow; also a meaningful **naming conflict**. |

### 5.4 Property data and professional transaction systems
| Product | Focus | Design implication |
|---|---|---|
| [Sprift](https://sprift.com/) | UK property data, reports, AI and monitoring for professionals | Data richness and AI search are not independent defensibility. |
| [PropertyData](https://propertydata.co.uk/) | Investor/developer analytics, mapped plots, comparable sales and AI assistant | Prefer household outcomes over investor yield-focused dashboards. |
| [Chimnie Data API](https://www.chimnie.com/) | Property entity resolution, data reconciliation and licensed API access | **Important:** even property record reconciliation exists at data infrastructure level. HomeScout must add consumer workflows, transparent resolution and decision change history. |
| [Reveal Title](https://revealtitle.ai/) | Solicitor/conveyancer AI document review, evidence-linked enquiries and reporting (*not revalidated in the 02 research: no readable page body*) | **Important:** enquiry-to-resolution exists professionally; consumer-first, cross-profession and cross-journey implementation is the potential gap. |
| [Groundsure](https://www.groundsure.com/) | Professional environmental and property risk reports | Avoid presenting public map screening as equivalent to regulated/formal environmental due diligence. |

### 5.5 Adjacent product names and brand-clearance warnings
The following are **not** included in the core product-competition matrix solely because of name similarity, but are material to public brand selection:
- [Home Compass](https://gethomecompass.com/): actively markets property decision support and due diligence; **very high conceptual and naming overlap** with proposed `HomeCompass`.
- [HomeLedger](https://www.homeledger.app/): existing home-management, records and service-workflow app; **related-sector naming overlap** with proposed `HomeLedger`.
- [HomeAtlas](https://gethomeatlas.co.uk/): directly competing UK area-intelligence product, so avoid `HomeAtlas`.
- Existing `HomeScout` services noted in 5.3 also suggest **HomeScout Copilot must remain a working title only** until a brand is chosen.

**Brand status:** Neither `HomeCompass` nor `HomeLedger` has passed UK trade mark/domain clearance. Check UK IPO marks, similar marks in relevant classes, Companies House, domains and app stores before final selection. Search is not legal clearance.

### 5.6 Competitive white space (hypothesis, not an exclusivity claim)
These pieces each have precedents in the market. The proposed differentiation is **their integrated consumer experience**, demonstrated by user outcomes rather than slogans:
1. A **living, versioned evidence record** integrating public data, licensed facts, seller/listing claims, user uploads, professional replies and contradiction status.
2. A **question-to-resolution loop**: detect a gap → specify needed evidence → identify who should answer → prepare a question → track response → verify and update the decision.
3. **Household-specific reality checks** connecting routines, transport, facilities, affordability and stress scenarios.
4. **Decision impact and history**: show what changed since the last investigation, whether costs or risk assumptions changed, and which previously held conclusions need review.
5. A **trust-first UX** separating source fact, modelled estimate, unverified claim, missing evidence and professional judgement at every stage.

**Strategic test:** If HomeScout merely provides a better-looking report with a chatbot, the product is insufficiently differentiated. The experience must measurably help customers *resolve* a material question more accurately or efficiently than using competitor products separately.

## 6. Product pillars
1. **Discover and investigate:** One UK address becomes an evidence-backed Property Intelligence Passport with explicit scope and gaps.
2. **Understand practical daily life:** Schools, amenities, transport and accessibility evaluated against user-stated routines, not demographic stereotypes.
3. **Model the real decision:** Reproducible rent/buy costs, lifecycle estimates and stress-tested household scenarios, distinguishing known values from assumptions.
4. **Reconcile evidence:** Preserve contradictory figures and clauses across listings, public sources, leases, survey reports and professional replies; do not overwrite inconvenient data.
5. **Resolve important questions:** Maintain issues, responsible parties, supporting evidence, requested documents and answer status. External communications require user review and explicit action.
6. **Track how the decision evolves:** Versioned snapshots, source changes, user updates and explicit decision impacts.
7. **Use AI where it adds value:** Foundry-backed specialised agents assist cross-document interpretation and investigation, while all numerical tools remain deterministic and all consequential claims evidence-linked.
8. **Compare without false precision:** Present personalised, auditable trade-offs instead of treating one composite score as a recommendation to buy.

## 7. Free and paid design philosophy
**Free is a complete, respectable product.** Users should be able to search, understand available public evidence, review nearby facilities, use financial calculators, inspect environmental information and compare a small set of homes. Public-interest safety findings should not be buried behind a subscription.

**Copilot Plus pays for computational and organisational depth**, not exclusive ownership of open facts. Paid capabilities include evidence-grounded conversations, multi-step investigations, document reconciliation, question-to-resolution tracking, change impact analysis, complex scenario modelling, expanded decision workspaces and versioned exports.

**Proposed commercial structure** (prices undecided): Free; monthly/short-term Copilot Plus; optionally one-off investigation report. Plan names, entitlements, quotas, document size limits and retention rules are product decisions to test, not facts established by this brief.

## 8. Complete experience map
### Public/anonymous
Home → buy/rent intent → postcode or address lookup → resolve candidate property → Property Passport (free) → neighbourhood map, sources, costs, hazards → calculator / comparison → save or sign in → optional upgrade.

### Rent
Rent intent → set household budget and commute needs → investigate an address → compare rent and bills → school/amenity access → record viewing notes → check available landlord/tenancy information and upload document on Plus → questions before paying/signing → decision report.

### Buy
Buy intent → address / listing details → property evidence and sale history → true cost of owning → examine risk/planning/tenure → compare alternative homes → paid document review (lease, survey, service charge) → solicitor/surveyor questions → export/revisit.

### Returning user
Sign in → investigations and alerts → see which evidence/assumptions have changed → examine unresolved questions and replies → add updated evidence → Copilot verifies, reconciles and re-calculates → compare previous and current decision state → export or share with consent.

### Investigation-to-resolution (critical end-to-end journey)
Search / import property → create issue from conflicting evidence or missing documentation → link precise source and relevance → identify who can clarify (agent, landlord, solicitor, surveyor, management company) → prepare a user-reviewed request → track unanswered/partially answered/resolved status → attach reply → verify answer and its authority → show material decision impact → preserve the previous state and audit record.

### Incomplete or conflicting evidence
Uncertain address match or missing official data → show coverage and implications → ask for user confirmation or additional document → provide primary-source link → do not silently invent facts → retain an explicit unresolved status.

## 9. Geographic and jurisdiction model
**Launch sequence: England first.** The first release covers addresses in England only, using English tenancy rules, English planning and flood sources, and SDLT. Addresses elsewhere in the UK must be shown as "not yet covered", never as a partial or clean result. The longer-term ambition stays UK-wide. The data model, jurisdiction routing and terminology must keep a nation field from the start, so the other nations can be added later without restructuring the product.

The product is **UK-only** and must eventually acknowledge four legal/data environments:
- **England:** English rental legislation, planning, environment, EPC, HMLR sales and SDLT where applicable.
- **Wales:** Renting Homes framework, Welsh flood/planning information, EPC, HMLR sales and LTT.
- **Scotland:** Scottish tenancy and property/title systems, SEPA flood data, Scottish EPC, LBTT.
- **Northern Ireland:** distinct tenancy system, Land & Property Services, DfI flood information, domestic rates and relevant SDLT rules.

Never describe a national feature as uniformly available when a source only covers Great Britain, England and Wales or England. Property address licensing—especially Northern Ireland—requires deliberate review.

## 10. Functional boundaries
HomeScout can display evidence, explain general regulations, calculate mathematical scenarios and organise questions. It must **not** claim to:
- Replace a solicitor, surveyor, mortgage adviser, insurer, flood professional or school admission authority.
- Guarantee a school place, commute time, broadband connection, insurance or mortgage offer.
- Determine actual property flood history from general flood-risk mapping alone.
- Provide an automated legal conclusion without a transparent jurisdictional basis and human review pathway.
- Display user-uploaded private documents publicly or mix them into another user's retrieval context.
- Scrape and re-publish estate-agent listings or proprietary mapping layers without rights.

## 11. Experience and visual principles
**Search first:** A memorable, calm homepage centred on one postcode/address entry and rent/buy selection.

**Evidence first:** Property Passport uses distinct states—verified for this property, applicable to surrounding area, modelled/estimated, user-entered, missing, or conflicting. Show original source, effective/observed dates, scope and match confidence.

**Readable density:** Give a concise 'what matters' layer, expandable rich cards, detailed map and source view, rather than an intimidating wall of data.

**Map-led discovery:** Amenity filters include schools, childcare, supermarkets, parks, health, places of worship (including churches), transport, recreation and accessibility. Use travel-time isochrones when legitimately calculated, not distance circles labelled as walking times.

**Property-first AI:** Paid Copilot runs alongside the current Passport and documents. Responses link to evidence and clearly identify unresolved matters and professional next steps.

**Inclusive and non-stigmatizing:** Avoid unexplained neighbourhood 'good/bad' scores, protected-group proxies or claims that crime summaries are precise street predictions. Label statistical boundaries and data limitations.

**Responsive and accessible:** WCAG 2.2 AA design target; keyboard access, screen-reader map alternatives, legible source text, colour-independent statuses, mobile financial controls and document access.

**Aesthetic direction:** Editorial UK-home photography, restrained forest-green/cream palette (navy dropped; tokens in `03-prototype-and-image-direction.md` §6), premium typography, generous whitespace, quiet motion, precise data visualisation. Original identity—not a visual clone of the referenced competitors.

## 12. Screen families and conceptual artefacts
The accompanying conceptual screenshots illustrate these seven screen families. The list numbers below are family numbers, **not** image numbers. The file-to-screen mapping is in `03-prototype-and-image-direction.md` §2, and an eighth image shows an alternative workspace. **All depicted addresses, prices, figures, maps, data matches and claims are synthetic placeholders and must never be mistaken for verified reports.**

1. **Public homepage:** promise, buy/rent switcher, universal search, brand trust and featured journeys.
2. **Property Passport (Free):** address header, structured evidence cards, sources, risk overview and upgrade route.
3. **Neighbourhood Explorer (Free):** full map, nearby schools, supermarkets, places of worship, transport, parks, health and accessibility filters.
4. **Compare & True Costs (Free core, Paid advanced):** side-by-side property cards, assumptions and understandable cost comparisons.
5. **Copilot Investigation (Plus):** guided conversation, cited findings, specialised analysis state, property context and an issue-resolution side panel.
6. **AI Document Review (Plus):** dual-pane original document and issue list with exact page/section citations.
7. **Decision Workspace:** saved homes, continuing investigations, open questions, assigned follow-ups, responses, evidence history and change alerts.

New required cross-screen artefacts: **Evidence Conflict Detail**, **Investigation Issue / Question Detail**, **Response & Verification**, **What Changed Since Last Visit**, and **Impact on My Decision**. Design must include both buyer and renter variants.

Required design states for each family: anonymous/authenticated; loading; no match; multiple property matches; partial data; sources stale; contradiction; unavailable data; empty list; offline/error; basic plan/Plus entitlement; small/mobile layout.

## 13. Technology decisions and design-facing constraints
| Layer | Decision |
|---|---|
| Frontend | Next.js, React, TypeScript |
| Backend and domain services | C# / ASP.NET Core |
| Cloud | Microsoft Azure |
| AI platform and models | Microsoft Foundry SDK |
| Multi-agent workflow | Microsoft Agent Framework for .NET, subject to architecture review |
| Knowledge retrieval | Versioned evidence corpus with Azure AI Search candidate implementation |
| Documents/object storage | Azure Blob Storage |
| Geospatial persistence | Azure Database for PostgreSQL with PostGIS candidate |
| Telemetry | OpenTelemetry, Azure Monitor / Application Insights, Foundry tracing/evaluations |
| IaC | Bicep candidate |

The architecture must separate property lookup, reproducible financial functions, geographic data processing, legal/document retrieval, multi-agent orchestration, source provenance and user data. The LLM must **not** invent authoritative facts or perform numeric calculations that can be produced deterministically.

## 14. AI reliability and evaluation constraints
- Ground consequential conclusions in retrieval or deterministic tool output; distinguish source facts from model interpretations.
- Maintain document/dataset source ID, version, checksum, licence, publisher, jurisdiction, applicability/effective date, ingestion timestamp and exact citation location.
- Separate user-private document indexes and enforce per-tenant access at every stage.
- Store investigation snapshots so a prior report can be understood and audited after sources or models change.
- Trace API request → workflow → agent → tool → retrieved evidence → validator → response; log costs and errors with privacy-aware redaction.
- Evaluate property matching, legal jurisdiction routing, citation support, date validity, numeric consistency, extraction precision/recall, missing-evidence handling and malicious document instructions.
- Never allow an answer to become 'verified' merely because multiple agents repeat it.

## 15. Success measures (definitions, not arbitrary targets)
- Search-to-Passport completion and address match resolution.
- Percentage of Passport claims with machine-inspectable, current provenance.
- Coverage by data category and UK nation; stale/missing/conflicting evidence rates.
- User comprehension of costs, geographic caveats and sources in usability tests.
- Property saves, comparisons, questions opened/resolved with verified supporting evidence, time to resolve and report exports.
- Paid conversion for useful investigative depth, excluding basic public-interest safety facts.
- Correctly supported AI assertions and document findings; user corrections and appeal rates.
- Mean and tail investigation latency, cost per investigation and provider outages.

## 16. Unresolved decisions for design and technical review
- Which address dataset or commercial provider supports production-grade autocomplete and property-to-UPRN matching across each UK nation?
- Which data categories can be displayed with sufficient certainty and permitted reuse in a commercial service?
- Should initial saved lists require accounts, and how should consent and retention work?
- Is the core paid value better expressed as a short-duration pass, subscription, report or combination?
- Which third-party transport/mapping service supplies reliable road-network travel times at acceptable cost?
- What wording, ordering and visual indicators communicate source coverage without false precision?
- How should users correct property identity, estimates and erroneous source joins?
- Which legal review boundaries and regulated-advice referrals apply to premium financial/tenancy features?
- What counts as a valid resolution of an issue, who can verify it, and when must the status remain “unresolved”?
- How will source-change detection distinguish a data-refresh event from a real-world property change?
- Which household routines can be calculated reliably with obtainable routing/timetable data?
- Which customer decision tasks demonstrate measurable improvement versus existing due-diligence reports and listing tools?
- What is the final cleared public brand? `HomeScout Copilot` remains an internal title.

**This document does not classify features as MVP/post-MVP or assign feature delivery phases.** The England-first geographic scope is recorded separately in section 9. A delivery roadmap remains to be validated.

## 17. Primary reference URLs and research register
**Direct and adjacent UK consumer research:** [Before](https://www.before.ng/), [bythenumbers](https://www.bythenumbers.uk/), [HomeAtlas](https://gethomeatlas.co.uk/), [HomeBuyerCheck](https://www.homebuyercheck.co.uk/), [HouseCheckup](https://housecheckup.co.uk/), [CheckNext](https://checknext.co.uk/), [HomeVerdict](https://www.homeverdict.co.uk/), [BackStory](https://backstory.homes/), [Property Due Diligence](https://propertyduediligence.co.uk/), [PropertyChecker](https://beta.propertychecker.co.uk/house-check/), [Chimnie](https://www.chimnie.co.uk/), [PlaceProof](https://placeproof.co.uk/), [MyPropertyScan](https://www.mypropertyscan.com/), [Check Before You Buy](https://checkbeforeyoubuy.co.uk/), [LandSale Reports](https://www.landsale.co.uk/reports), [UK Property Check](https://ukpropertycheck.co.uk/), [Crystal Roof](https://crystalroof.co.uk/), [Locrating](https://www.locrating.com/), [Dwellmark](https://dwellmark.co.uk/), [NestVerdict](https://nestverdict.com/), [Move iQ](https://www.moveiq.co.uk/).

**Search and discovery:** [Rightmove](https://www.rightmove.co.uk/), [Zoopla](https://www.zoopla.co.uk/), [OnTheMarket](https://www.onthemarket.com/), [OpenRent](https://www.openrent.co.uk/), [HomeSift](https://homesift.app/), [MyHomeScout](https://myhomescout.co.uk/), [HomeScout UK](https://www.homescout.org.uk/), [HomeScout Ireland](https://homescout.io/).

**Professional and infrastructure:** [Sprift](https://sprift.com/), [PropertyData](https://propertydata.co.uk/), [Chimnie Data API](https://www.chimnie.com/), [Reveal Title](https://revealtitle.ai/), [Groundsure](https://www.groundsure.com/).

**Brand-conflict references:** [Home Compass](https://gethomecompass.com/), [HomeLedger](https://www.homeledger.app/), [UK IPO mark search](https://www.gov.uk/search-for-trademark).

**Official source/data anchors:** [GIAS](https://www.gov.uk/guidance/get-information-about-schools), [OS Open UPRN](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-uprn), [HM Land Registry data](https://www.gov.uk/government/publications/hm-land-registry-data/public-data), [EPC developer data](https://get-energy-performance-data.communities.gov.uk/), [Planning Data API](https://www.planning.data.gov.uk/docs), [Flood Monitoring API](https://environment.data.gov.uk/flood-monitoring/doc/reference), [NaPTAN](https://naptan.dft.gov.uk/), [OpenStreetMap attribution](https://www.openstreetmap.org/copyright).

**Research discipline:** Competitor features, prices and coverage can change. Recheck official pages before pricing or product claims; classify “not publicly advertised” separately from “does not exist.” Market-positioning hypotheses are not validated customer demand.
