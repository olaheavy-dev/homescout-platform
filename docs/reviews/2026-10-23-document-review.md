# Product document review

**Date:** 23 October 2026, Europe/London  
**Reviewed:** README; product brief 01; research/direction 02; prototype/image direction 03; the image inventory and contact sheet. The original eight images had previously been inspected; this pass re-opened the lease-review image and contact sheet to check disputed details.  
**Outcome:** The documents provide a coherent basis for wireframes and discussion. They do not yet form a complete implementation specification. Corrections below were applied to the documents; the original image files were not recreated or edited.

## 1. Direction retained

- Equal quality for buyer and renter journeys.
- England first, with other UK addresses clearly marked not yet covered; longer-term UK ambition retained.
- A home record connecting evidence, household costs, comparison, questions and decisions.
- Contextual AI with inspectable evidence and deterministic calculations.
- Warm editorial photography and a precise, accessible working interface.
- Public brand, commercial model, entitlements and detailed suppliers remain open.
- No MVP/post-MVP feature classification or new feature-delivery roadmap was introduced.

## 2. Corrections applied

| Finding | Why it mattered | Correction |
|---|---|---|
| Document authority was ambiguous | Two later documents both claimed precedence, while the historical brief still described old labels and paid capabilities | README and document headers now distinguish product decisions in 02, proposed design in 03 and the historical concept in 01. A prototype label cannot approve a payment model. |
| The original register could appear fully revalidated | Only a 12-product subset was inspected in the research pass; inaccessible pages were not the only unchecked entries | Both research documents now state the scope of verification and retain unchecked entries as research leads. |
| A proposed geographic expansion was described as cheapest without cost evidence | Source overlap does not establish delivery cost or country order | Replaced the cost ranking and “close to new builds” assertion with an explicitly uncosted inference and supplier/effort dependencies. |
| Core cost-source dependencies were incomplete | Council tax and purchase tax were in the product promise but missing from the feasibility table | Added official source anchors and the distinction between a tax band, the local charge and household assumptions; added effective-date and supported-case requirements for purchase-tax calculations. |
| The feasibility table could be mistaken for a complete source catalogue | Several historical features had no corresponding source/access assessment | Added an explicit list of categories still requiring diligence, including crime, noise, air quality, ground risk, safety records, amenities and cost estimates. |
| Question closure and cost application lacked an explicit actor | An AI-generated assessment could otherwise silently close a matter or overwrite a household scenario | Added user/reviewer responsibility, retained evidence and history, explicit cost application, affected-scenario visibility and preserved user overrides. |
| Copying a question could be mistaken for sending it | “Waiting for reply” would otherwise be an unsupported status | Require a recorded send action, or a future authorised integration's recorded delivery state. The prototype labels its action as simulated. |
| Buyer/renter parity was required but not demonstrated | The buyer story lacked the inadequate reply shown for the renter; common viewing/cost/routine steps were not written into both stories | Added a shared path and a partial buyer reply; both stories now contain the relevant evidence and decision steps. |
| The buyer image prompt contradicted the buyer fixture | A semi-detached house prompt was paired with a leasehold-flat investigation | Changed the primary buyer asset/prompt to an appropriate building exterior and required a building-level caption. |
| Contact-sheet numbering was wrong | A designer could reproduce the wrong workspace variant | Corrected the mapping: the sheet contains images 1, 2, 4, 5, 3, 6 and 8. Image 7 is absent. |
| The image review overstated the ground-rent review date | A 25-year cadence plus a lease commencement date does not establish the full review schedule without the relevant terms | Kept 2040 only as a conditional calculation and required the full definitions/schedule and any variations. Preserved the visible greater-of/compounding wording. |
| Payment labels and expiry suggestions could imply settled entitlements | Move pass was described too much like an approved rename of Copilot Plus | Marked it as a payment-model hypothesis; called out free/paid boundaries, expiry, retention and deletion as unresolved together. |

## 3. Verification performed

- Read all current Markdown documents and checked their roles, terminology, scope, journeys, evidence treatment, commercial claims and image references.
- Rechecked the contact sheet against its source screenshots and inspected the visible lease excerpt. This verifies what the concept image depicts, not the legal validity of its fictional document.
- Recalculated the service-charge difference: £3,720 − £2,400 = £1,320/year; annual/12 gives a £110 monthly budget equivalent, not a billing schedule.
- Recalculated the renter example: £1,450 + £28 = £1,478/month. Made the synthetic baseline composition explicit.
- Recalculated the stated revised amber/red contrast ratios on white, paper and sage. They match the rounded values in document 03. This is token-level verification, not a complete accessibility audit.
- Rechecked selected primary web sources: [English renting guidance](https://www.gov.uk/guidance/renters-rights-act-overview-for-tenants), [Ofsted report-card guidance](https://www.gov.uk/guidance/understanding-ofsted-report-cards-and-grades), [Planning Data coverage](https://www.planning.data.gov.uk/about/), [flood-check scope](https://www.gov.uk/check-long-term-flood-risk), [home-buying reform roadmap](https://www.gov.uk/government/consultations/home-buying-and-selling-reform/outcome/home-buying-and-selling-reform-roadmap), and the [renters' reform implementation briefing](https://commonslibrary.parliament.uk/research-briefings/cbp-10669/).
- Added source anchors for [council tax bands](https://www.gov.uk/council-tax-bands), [local council-tax charges and adjustments](https://www.gov.uk/council-tax), and [SDLT](https://www.gov.uk/stamp-duty-land-tax). No full tax rules engine or relief assessment was performed.
- Spot-checked the public [HomeBuyerCheck offering](https://www.homebuyercheck.co.uk/) and [HomeLedger positioning](https://www.homeledger.app/). This was not a new full competitor study or a paid product test.

No authenticated API, data licence, professional legal review, customer interview or production integration was validated by this document review.

## 4. What is still needed before implementation

### Product and prototype specification

Create a single actionable specification drawing from 02 and 03. It needs:

- A complete feature inventory carried forward explicitly from the historical brief, with each feature's proposed behaviour and dependencies. Do not silently lose a feature because it does not appear in one demonstration story.
- Screen/action/state contracts for anonymous, signed-in, shared and paid-access cases, including persistence and returning-user behaviour.
- Canonical synthetic fixture records: stable IDs, exact display addresses, property type, tenure, dates, costs, document versions/pages, excerpts, replies and matched photographs. Keep synthetic identifiers out of live data lookup.
- Reproducible cost inputs, periods, rounding, ranges, exclusions and expected outputs. Define monthly budget averages separately from actual payment dates and longer-term economic costs.
- Question transitions, reviewer identity, inadequate/reopened replies, explicit scenario updates and the user's decision with unresolved matters.
- A provisional entitlement matrix clearly labelled for testing, including the free manual workflow and paid assisted functions. It must not turn an untested recommendation into a founder decision.
- Account/household roles, sharing permissions, consent, revocation, document access, export, retention and deletion behaviour.
- Prototype acceptance criteria and a task-based buyer/renter research script. The two narrated journeys do not prove the whole feature system.

### Data and evidence specification

Create a field-level catalogue for the proposed England scope:

- Provider, source URL, geographic and record-level coverage, licence/reuse status, access method, cost and review date.
- Property/unit/building identity rules and the correction/relinking process; a mistaken match must not silently move private evidence to another home.
- Fact, claim, estimate and interpretation records; dates, applicability, exact citation location and source version.
- Category-specific definitions of missing, no match, not covered, failed, stale, conflicting and not applicable.
- Refresh schedules, outages, detection of substantive changes and affected-scenario recalculation.
- Input/output contracts for calculators and routing, with supported and unsupported cases.
- Private-document access boundaries, extraction-quality handling, instruction-in-document handling, retention and audit requirements.

The technical architecture can then map these contracts to the existing proposed Next.js/.NET/Azure direction. SDK versions, service choices, multi-agent necessity, operating costs and deployment design remain technical decisions to examine; this review did not approve them.

## 5. Readiness conclusion

Proceed with low-fidelity wireframes while writing the two specifications above. A new image pass should follow stable fixtures and screen structure. The current documents are suitable direction-setting material; production claims, complete entitlements and build-ready acceptance contracts remain unfinished.
