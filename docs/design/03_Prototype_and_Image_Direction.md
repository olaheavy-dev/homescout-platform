# HomeScout: prototype and image direction

**Date:** 23 October 2026  
**Purpose:** A reviewable experience and art-direction brief informed by `02_Product_Research_and_Direction.md`.  
**Audience decision:** Buyers and renters have equal weight.  
**Geography decision:** England first. Both stories use English fixtures.  
**Authority:** This document proposes prototype behaviour and design within the product scope and decision status recorded in `02_Product_Research_and_Direction.md`. Prototype wording does not approve payment terms, data integrations or a public brand.  
**Status:** Recommended direction, not approved screens or an implementation roadmap. All example homes, documents, costs and outcomes below are synthetic.

## 1. The design decision

Choose **warm editorial clarity**: the approachability of the existing homepage, the usefulness of the neighbourhood map, and the precision of the document viewer, brought together in one consistent product.

The user should feel: **“I understand this home better, and I know what to do next.”**

The prototype must demonstrate a change in understanding, not simply display a large collection of cards. Its strongest moment is an answer that changes the cost comparison while preserving the original evidence.

| Possible direction | Strength | Trade-off | Recommendation |
|---|---|---|---|
| Warm editorial clarity | Welcoming photography, readable explanation, precise evidence | Requires discipline to keep decorative content out of working screens | **Use this** |
| Technical property dashboard | Dense datasets and maps feel powerful | Harder to understand; risks favouring experienced buyers and implying comprehensive coverage | Use its detail only when requested |
| AI concierge | Conversational and approachable | Can hide missing evidence and make the product resemble other AI wrappers | Use conversation within the current task |

**Founder decision (0004):** AI appears inside tasks **and** as an optional, closable chat panel about the current home, not a permanent column. In the prototype, chat replies are scripted from the sample data, cite their evidence, and are labelled as simulated.

## 2. What to keep and change in the eight existing images

**These images are AI-generated with ChatGPT (OpenAI) by Sunkanmi Olawuwo** (provenance in `ASSETS.md`). Image numbers refer to the filename suffixes in this folder. They are visual concepts, not verified property reports. Several filenames do not describe their screen, and two other numbering schemes exist (the brief's screen families and the contact sheet), so use this mapping:

| Image | File | Screen | Brief §12 family | Contact sheet |
|---|---|---|---|---|
| 1 | `HomeScout Copilot Property Intelligence-1.png` | Public homepage | 1 | 01 |
| 2 | `HomeScout Property Intelligence Dashboard-2.png` | Property passport | 2 | 02 |
| 3 | `HomeScout Property Intelligence Dashboard-3.png` | Copilot investigation | 5 | 05 |
| 4 | `HomeScout Neighborhood Dashboard-4.png` | Neighbourhood explorer | 3 | 03 |
| 5 | `HomeScout Property Comparison Dashboard-5.png` | Comparison and costs | 4 | 04 |
| 6 | `HomeScout Lease Review Dashboard-6.png` | Document review | 6 | 06 |
| 7 | `HomeScout Property Dashboard-7.png` | Workspace | 7 | not shown |
| 8 | `HomeScout Property Insights Dashboard-8.png` | Alternative workspace | 7 (variant) | 07 |

`abode_copilot.jpeg` is a contact sheet of images **1, 2, 4, 5, 3, 6 and 8**, in that order. Its final tile is image 8; image 7 is absent. It is an overview only. Use the filename image numbers above in reviews.

| Image | Keep | Change before prototyping |
|---|---|---|
| **1 — Public homepage** | Strong main promise; clear address entry; buy/rent choice; UK residential character; serif headline with restrained green | Remove the invented testimonial, unsupported “40+ sources” and “1,000+ insights” counts, and any implied endorsement from official-source branding. A pictured street must not appear to be the searched home. Add an equally credible renting example and a small demonstration of an answered question. Reduce competing navigation. Fix the "postcoe" typo in the search placeholder. Replace the "Property intelligence for a brighter tomorrow" eyebrow, which does not match the brief's plain-spoken voice. With England first, replace the "All UK nations" and "UK-specific… Northern Ireland" claims, and the Edinburgh/Cardiff example postcodes, with honest coverage wording. |
| **2 — Property passport** | Address context; understandable fact cards; source access; an explicit missing-evidence section | Promote “what matters and what to ask” above a row of equally weighted facts. Show field-level scope/date, not only a footer of logos. Resolve the confusing case where “couldn't verify” is followed by “no applications found.” The small circular “10 min walk” map should use real routing or be labelled as distance. Do not imply flood mapping verifies a particular home. "Several good and outstanding schools nearby" uses single overall grades that new Ofsted report cards no longer give; show framework and date instead. |
| **3 — Copilot investigation** | Property context beside evidence-linked findings; question entry; connected documents | Replace named-agent completion with user-meaningful work states. The screenshot calls the property freehold while prominently warning about missing lease documents; handle relevance before generating questions. The same example street name appears in Sheffield in image 2 and Leeds here—use one controlled fixture (see the fixture table below). The school finding and the "Good – Outstanding" key-findings card use single overall grades; apply the same framework/date treatment as image 5. Reduce duplicated navigation and the permanent full chat column. |
| **4 — Neighbourhood explorer** | Map-plus-list layout; visible everyday essentials; category filters; including worship and healthcare | The irregular "5 min walk" and "15 min walk" areas look like network isochrones but name no routing provider, mode assumptions or calculation date; record them or relabel as distance. (The concentric "10 min walk" circle is in image 2.) The "Last updated: 15 Jan 2025" data note is stale against the 23 October 2026 snapshot. The home shown, 23 Mayfield Road S11 8TY, is a third Sheffield fixture alongside image 2's address. Avoid implying a nearby GP accepts registrations or school proximity guarantees admission. Start from household priorities instead of showing every pin. Retain visible map attribution. |
| **5 — Comparison and costs** | Aligned homes; shared assumptions; understandable stacked monthly costs | Remove automatic winner numbering and unexplained confidence dots. Add renter-native comparisons, upfront cash, uncertainty ranges and source links. Historical school grades need framework/date context. Distinguish monthly cash outgoings from longer-term economic cost. “Within entered budget” must state exclusions and is not lending approval. **The mortgage bars do not match the screen's own inputs.** A £50,000 deposit at 4.5% over 25 years gives repayments of about £1,251, £1,529 and £1,390 a month, not £994, £1,173 and £1,083. The corrected totals are about £1,684, £2,005 and £1,851, so 47 Westbourne Road **exceeds** the £2,000 budget and the "all three within budget" message is wrong. Generate every figure from the deterministic cost engine, never by hand or image generation. |
| **6 — Document review** | Original document alongside findings; page-specific references; multiple document types | Show both sides of a conflict and align reporting periods. A historic estimate of £2,400 and later actual charges of £3,720 do not alone prove contradictory current charges. The visible ground-rent clauses describe a 25-year cadence and the greater of an RPI increase or 1% per annum compounded, so the mechanism is not wholly absent. The excerpt does not establish every definition or the first review date: 2040 is only a conditional calculation if the full lease anchors reviews to 1 January 2015. Do not present that assumption as a confirmed date; seek the relevant definitions, review schedule and any variations. Recompute time-dependent lease wording from the snapshot date: a term ending 31 December 2139 has about 113 years remaining on 23 October 2026, not 114. Missing evidence should not automatically mean low severity. Clarify plan state: the screenshot simultaneously presents Plus and a free-plan account. |
| **7 — Workspace** | Saved homes; viewing questions; recent activity | Replace arbitrary investigation percentages with specific open matters. Bring the next relevant action above generic totals and city photography. “Report updated” should explain the actual change and its effect. Give renter homes equal visual space: all four saved homes show purchase prices and none shows rent. Replace the "10 Downing Street" search placeholder with a synthetic address. |
| **8 — Alternative workspace** | Calmer light navigation; clearer property-card action; readable hierarchy | Use this as the starting shell, with fewer dashboard tiles. Remove gold crowns, oversized decorative icons and repeated Copilot promotions. “100% complete” must not imply complete due diligence. Separate investigation status from the household's decision status. The paid tier is called "HomeScout Plus" here and "Copilot Plus" elsewhere; neither is settled (see glossary). "28 Victoria Park Road" is labelled a flat but pictured as a terrace. "17 Willow Lane" appears in activity but not among saved homes. An area-wide asking-price change is presented as a property alert. |

### Cross-image consistency fixes

- One wordmark, navigation model, account identity and set of component styles.
- One canonical record per sample home: identifier, unit, address, location, photograph, property type, tenure, dates and document links.
- "42 Ashfield Road" currently contradicts itself across images 2, 3 and 6:

  | Field | Image 2 | Image 3 | Image 6 |
  |---|---|---|---|
  | City / postcode | Sheffield S11 8AE | Leeds LS6 3AA | — |
  | Tenure | Freehold ("lease information not applicable") | Freehold | Leasehold agreement under review |
  | EPC | C (69) | D | — |
  | Floor area / built | ~96 m², 1900–1929 | 112 m², 1910–1930 | — |

  The buyer story (section 4) needs a **leasehold flat in England**, so make that the canonical buyer fixture and use it for images 3 and 6. If the freehold terrace is kept, give it a different address and use it as the comparison home.
- Beyond Ashfield Road, the images use near-duplicate addresses that look like one home but aren't: 12 Maple Avenue (5), 12 Maple Grove (8) and 28 Maple Street (7); 28 Oakfield Road, Sheffield (5) and 4 Oakfield Road, Leeds (8); 9 Willow Lane, Harrogate (7) and 17 Willow Lane, Manchester (8). Image 2's £285,000 last sale reappears as image 7's price for a different home. Replace them with a small fixture catalogue: one leasehold buyer flat, one buyer comparison home, one renter flat and one renter comparison home, each with a fixed ID.
- The account holder changes from image to image ("JD"/James, Sarah Mitchell, Sarah Thompson). Use one synthetic household.
- Source dates in the images (January 2024, October 2023, January 2025) are older than the 23 October 2026 snapshot without being marked as stale. Either date the fixtures consistently or show the stale state deliberately.
- No swapping a terrace photograph onto a flat record or showing unrelated building imagery as evidence.
- Use **Neighbourhood** consistently in the interface; keep existing filenames unchanged.
- No fabricated testimonials, official seals, success metrics or professional endorsements.
- Make “not found,” “not covered,” “not applicable” and “not supplied” visibly different.
- Label a complete demo as **Illustrative example**. Keep that label in shared views and exports.

## 3. Product structure and navigation

**Public navigation:** How it works · Example home · Costs and comparison · Sign in. One primary **Check a home** action. Buying and renting are equally visible; neither is hidden under “More.”

**Signed-in navigation:** My move · Homes · Compare. Settings and plan management sit in the account menu. A persistent **Check a home** action starts another record.

**Inside a home:** Overview · Nearby · Costs · Viewings · Questions · Documents · Activity. Evidence detail opens from the relevant fact or finding. Questions, viewing notes and documents remain attached to the current home. The viewing companion lives under **Viewings**, and its notes and photos also appear as evidence sources in Questions.

**Glossary**

| Consumer term | Internal / earlier terms | Meaning |
|---|---|---|
| Home record | Living property decision record, home decision record, living evidence record | Everything known, estimated, missing, asked and decided about one home |
| Home overview | Property (Intelligence) Passport | The summary tab of a home record |
| My move | Decision workspace | The signed-in space holding all home records and comparisons |
| Neighbourhood / Nearby | Neighbourhood Explorer, Area insights | Daily-life context around a home |
| Move pass | Candidate replacement for the earlier Copilot Plus label | Payment-model hypothesis, not a confirmed tier or an entitlement-equivalent rename (see `02_Product_Research_and_Direction.md` §8) |

“Property Passport” and “living evidence record” may remain internal concepts; a first-time user should not need to learn them.

On mobile, keep a compact home header and a short bottom navigation for Overview, Nearby, Costs and Questions; make Viewings, Documents and Activity accessible from a labelled menu, with Viewings one tap away during a visit. Use a full-screen evidence sheet and a switch between original document and findings rather than shrinking two columns.

## 4. The prototype needs two complete stories

**Figures in these stories are provisional.** They were worked out by hand. The stage 2 calculation script becomes their source of truth: it computes each value from the sample inputs, and this document is then checked against the script's output and corrected where they differ. These stories define what the prototype proves. They do not remove other features from the product brief or assign implementation phases.

### Shared path before the evidence question

Each story must demonstrate this path using its own home, cost model and household priorities:

1. Choose Buying or Renting, confirm an English address and exact unit, then open the home overview with its evidence gaps visible.
2. Open Nearby, add an optional routine/destination and inspect the route assumptions or the unavailable-data state.
3. Open Costs, edit a relevant assumption, distinguish upfront cash from recurring outgoings, and inspect a downside scenario.
4. Compare with a second home under aligned assumptions; unknown values remain explicit.
5. Open Viewings on mobile, record a note or photo and turn an observation into a question. Return to the overview and continue with the story below.

The remaining document conflict, reply and decision steps are also part of each story. Use stable fixture IDs and a fixed **23 October 2026** snapshot date throughout. Exact demo addresses, inputs, documents and screen transitions still need to be collected in the product/prototype specification; the existing image contents are not that fixture catalogue.

### Buyer story: a service-charge question changes the decision

1. Complete the shared path in **Buying** using the canonical leasehold flat and an English comparison home.
2. The listing claims **£2,400 annual service charge for the 2026 budget period**. A supplied managing-agent budget states **£3,720 for the same period and charging scope**. Both remain visible with their source and date.
3. Open the finding: “Two sources give different service-charge figures for the same period.” Do not assume either is authoritative merely because it was uploaded.
4. Review the request: “Please confirm the annual charge for this flat for this budget period and provide the current budget, explaining the difference from the listing.” Identify the relevant agent/managing agent and any conveyancer follow-up. Copy/export the draft, then separately record that it was sent; the prototype labels this as a simulated action.
5. Attach a partial sample reply saying “the charge is usually around the listing figure” without the requested current budget. Keep the question **Partially answered** and the cost uncertainty visible.
6. Attach a subsequent specific reply and matching schedule supporting the higher budget; show who made the statement and what was checked. A user/reviewer explicitly records the supported answer. A separate major-works question remains unanswered.
7. Propose changing the cost assumption from £2,400 to £3,720 a year. After explicit user confirmation, show **£1,320/year more**, a **£110/month budget equivalent**. Preserve the original value, source and scenario version. This is arithmetic applied to synthetic inputs; annual/12 is not a claim that the charge is billed monthly or a prediction of future charges.
8. Reopen comparison and see the changed cost, the unresolved major-works question and the user's own revised preference. Record a decision or a next step without declaring the home approved.

### Renter story: “bills included” needs a precise answer

1. Complete the shared path in **Renting** using an English rental and comparison home. Enter an optional move date and monthly budget after the overview is available.
2. The listing says **water included**. The supplied draft bills schedule says **tenant pays water** for the same intended arrangement.
3. Open the two excerpts and prepare a request to the letting agent/landlord: “Please confirm who pays the water bill and update the written bills schedule to match.” Copy/export it, then separately record that it was sent as a labelled simulated action.
4. Attach a partial reply saying “most bills are included.” Keep the question **Partially answered**; it does not resolve water responsibility.
5. Attach a subsequent specific reply and revised schedule supporting that water is excluded. A user/reviewer explicitly records the answer and supporting materials; this is not a general legal approval of the tenancy.
6. Propose an explicitly **user-entered £28/month water estimate**. After user confirmation, the previous illustrative monthly total of £1,450 becomes **£1,478**, retaining the previous scenario. Define the baseline as £1,200 rent plus £250 other monthly outgoings excluding water in the controlled fixture. Responsibility is supported by documents; the amount remains an estimate.
7. Compare with another rental under the same assumptions. Show move-in cash separately, including that a refundable deposit is cash required rather than a monthly bill. Keep any unanswered repair or paperwork question visible before recording a decision.

Use ordinary current English private-renting terminology for the English fixture; do not build the story around an assumed 12-month fixed term. Other nations are not covered at launch. Show a clear "not yet covered" state for their addresses, and keep jurisdiction and tenancy-type routing in the data model so they can be added later. [Current English tenant guidance](https://www.gov.uk/guidance/renters-rights-act-overview-for-tenants)

### What makes the stories equally developed

Both must include: entry, identity confirmation, useful overview, daily-life context, editable costs, viewing notes, document evidence, a question, an inadequate reply, a supported answer, updated comparison and a recorded decision. A renter tab that merely replaces a mortgage slider with rent fails this requirement.

Prototype controls must distinguish simulated source checks, document attachments, replies, sending and paid access from live services. Use bundled synthetic examples for this demonstration. It must be possible to explore each complete journey without an actual payment; production entitlements remain open. Research sessions using consented, redacted real materials are a separate activity from the public demonstration.

## 5. Screen and state specification

| Screen / interaction | Main question it answers | Required content and behaviour |
|---|---|---|
| Search-led landing | “What can this help me do?” | Shared promise, equal buy/rent choice, address input, optional example journey |
| Identity confirmation | “Is this the exact home?” | Unit/building candidates, clear correction route; no quiet postcode-to-flat inference |
| Home overview | “What matters here?” | Three concise findings as appropriate, current cost assumption, open questions, source/scope labels and next action |
| Nearby and routines | “Would daily life work?” | Map/list, optional destinations, selected categories, route assumptions and missing information |
| Real costs | “What cash would I need?” | Monthly estimate, upfront timeline, editable inputs, exclusions and downside scenario; buyer/renter variants |
| Compare | “Which trade-offs matter to us?” | Aligned criteria, identical assumptions where applicable, visible unknowns; no universal winner |
| Viewing companion | “What should I check and ask?” | Relevant questions, notes/photos, time and source of observation; mobile layout |
| Document review | “What supports this finding?” | Exact excerpt, document/page/version, comparison source and create-question action |
| Question detail | “What answer do I need, and from whom?” | Evidence, specific request, recipient role, status and requested supporting documents |
| Reply checking | “Does this actually answer it?” | Reply, respondent, supporting material, partial-answer state and remaining uncertainty |
| Decision impact | “What changed for us?” | Previous/current assumption, deterministic delta, affected comparison and continuing questions |
| My move / activity | “What deserves attention now?” | Outstanding actions, material changes, saved homes and access to the dated decision snapshot |
| Share / snapshot | “What am I sharing?” | Content preview, permissions, evidence dates, assumptions and remaining unknowns; private-document access separately controlled |

Include realistic empty, loading, failure and ambiguity states. In particular:

- A postcode matching several flats.
- An expired or superseded certificate.
- A source that does not cover the location.
- A source request that failed, which must not look like a clean result.
- Different cost periods that require comparison rather than a contradiction claim.
- A photo or reply that belongs to another property.
- A document with poor extraction quality.
- A partially answered question and a reopened question.
- A copied/exported request that has not been recorded as sent.
- A proposed cost correction that the user declines, keeping their override and the evidence conflict visible.
- A refreshed dataset whose substantive value has not changed.
- An address in Wales, Scotland or Northern Ireland, shown as "not yet covered" rather than as a partial or empty result.
- Basic/paid boundaries and record access after a pass expires.
- Narrow/mobile layouts with a list alternative to the map.

## 6. Visual system recommendation

The following are proposed design tokens for exploration, not a claim of completed accessibility validation.

| Element | Direction |
|---|---|
| Main green | Deep forest `#153F35` for primary actions and restrained brand moments |
| Main text | Ink `#182923`; keep body text high contrast |
| Background | Warm paper `#F7F5EF`, with clean white working surfaces |
| Supporting tone | Muted sage `#DCE7DD`; avoid making large green areas mean “safe” |
| Attention | Amber `#8F560E`; pair with words and icons |
| Confirmed material concern | Restrained red `#A33636`; use on specific supported findings rather than the whole home |
| Typography | Editorial serif for a few public-page headings; clear sans serif for navigation, facts, costs and documents; tabular numbers where values align |
| Component treatment | Modest corners, thin dividers, subtle shadows only where useful; generous spacing without large decorative gaps |
| Data visuals | Direct labels, clear units, comparable scales, uncertainty ranges and visible assumptions |
| Motion | Quiet transitions that explain state changes; no theatrical agent activity |

Amber and red were darkened from `#A86712` / `#B23C3C`: the original amber fell below 4.5:1 on paper (4.17) and sage (3.58). As text, the revised values reach at least 4.5:1 on white, paper and sage (amber 5.99 / 5.50 / 4.71; red 6.69 / 6.14 / 5.26). Forest and ink exceed 9:1 on all three. Validate text, icon and focus contrast in context. Evidence status must never rely on colour alone. Keep source and caveat text readable rather than shrinking it to fit a fixed card. Respect reduced-motion preferences and keyboard interaction throughout.

Use larger photography on the public introduction. In the workspace, smaller property images should aid recognition while questions and costs receive the stronger hierarchy. The suggested outcome is emotionally welcoming at entry and practically useful during the decision.

## 7. Image strategy

### The three image roles

1. **Editorial atmosphere:** representative UK homes and everyday surroundings on public pages. Explicitly representative, with no claim that the image shows a searched address.
2. **Property recognition:** a correctly matched, permitted photo supplied by the user or a licensed source. If absent, use a neutral “No property photo supplied” placeholder rather than inventing a facade.
3. **Decision evidence:** the user's viewing photos and document pages, kept with their date, provenance and home record. An image can support an observation; it does not establish a structural diagnosis or identify the exact cause of damage.

Maps, charts, source labels and document text are interface/data content. They should be built from controlled content and appropriate mapping tools, not painted into an AI-generated screenshot. Official marks and endorsement cues should not be generated as decoration.

### Proposed asset set

| Asset | Subject | Placement / crop | Guardrail |
|---|---|---|---|
| Shared hero | An ordinary, appealing mixed UK residential street, including houses and flats | 16:9 master, with room for a 4:5 mobile crop | Avoid presenting only expensive detached or London period houses as the normal home |
| Buyer story | Building exterior for the canonical leasehold flat, with recognisable shared entrance and architectural detail | 3:2 master and consistent card crop | Caption the building-level view; do not use a semi-detached-house image for this flat or portray it as a verified address |
| Renter story | A believable modern or converted flat exterior and a naturally lit interior | 3:2 master, matched image family | Give it the same photographic care as the buyer image |
| Everyday-life image | Local shops, public transport or a park seen at normal eye level | Small editorial support image | Do not imply actual travel times, service quality or accessibility from a photograph |
| Viewing companion | A hand making notes in an ordinary home, with no legible private information | 4:5 for mobile-oriented explanation | No visible identity documents, bank details or addresses |
| No-photo state | Quiet neutral house/building placeholder | Consistent card ratio | Clearly a placeholder, never a convincing replacement photo |

Do not purchase or generate a large image library before choosing the visual direction and canonical demo fixtures. The next image pass should validate one shared hero and a matched buyer/renter pair, then apply the chosen treatment consistently.

### Generation-ready editorial prompts

These are proposals for a future image pass; no new raster assets were generated during this research.

**Shared hero:** “Natural editorial architectural photograph of a believable British residential street, ordinary brick terraces and a modest apartment building, soft bright overcast daylight, green planting, eye-level perspective, accurate UK architectural details, calm everyday atmosphere, restrained forest-green and warm stone colour accents, no luxury staging, no legible address numbers, no logos, no text, horizontal 16:9 composition with a quiet left area for separate interface copy. Representative invented location, not a real property listing.”

**Buyer flat building:** “Editorial architectural photograph of a modest low-rise brick apartment building in England, a believable shared entrance and separate flat windows, realistic proportions and materials, small communal planting area, natural overcast daylight, lived-in but cared-for appearance, perspective close to eye level, neutral colour grading, no signage or legible building number, no dramatic sky, no exaggerated wide-angle lens, horizontal 3:2. Invented representative building for the synthetic leasehold-flat story; the exterior is a building view and does not establish an individual flat's boundaries or condition.”

**Renter exterior:** “Editorial architectural photograph of a modest contemporary British apartment building, brick facade, believable shared entrance and windows, small planting area, everyday residential setting, soft daylight, the same neutral colour grading and camera height as the buyer-flat-building reference, no logos, no readable address, no luxury tower aesthetic, horizontal 3:2. Invented representative building.”

**Renter interior:** “Natural editorial interior photograph of an ordinary UK rented flat living room, realistic compact dimensions, simple furniture, natural window light, warm neutral materials, comfortable everyday atmosphere, no excessive staging, no wide-angle distortion, no personal documents, no text, horizontal 3:2. Invented representative interior.”

**Everyday life:** “Natural editorial street photograph of an ordinary UK neighbourhood with a small grocery shop, a bus stop and visible public pavement, soft daylight, realistic street scale, restrained colour grading, people only as incidental unidentifiable background figures, no readable private details, no brand focus, horizontal 3:2. Representative invented location.”

**Viewing moment:** “Editorial close-up photograph of an adult's hands making viewing notes on a plain notebook in a modest naturally lit UK flat, home details softly visible in the background, no readable notebook text, no personal documents, ordinary realistic setting, calm neutral palette, vertical 4:5. Illustrative scene.”

### Image acceptance criteria

- Clear permission/provenance, including whether the image is illustrative or property-specific.
- Plausible architecture, windows, doors, stairs and reflections; no generated signage used as evidence.
- Matched lighting, crop and colour treatment for buyer and renter stories.
- Useful mobile crop and text contrast where copy sits nearby.
- No dramatic hazard imagery that implies a finding not established by evidence.
- Informative alternative text for meaningful images; decorative imagery does not repeat surrounding content to screen readers.
- No personal information exposed through viewing photos or document thumbnails.

## 8. Review checklist and open decisions

The direction is ready to discuss when we can answer these questions together:

1. Does **understand, cost, compare, resolve** describe the product clearly enough?
2. Does the preferred warm editorial treatment feel right for both a renter and a buyer?
3. Is the home record the centre of the experience, with AI available inside the task?
4. Do both demonstration journeys earn their value by changing a decision rather than only producing a report?
5. Is the extra effort of tracking replies worthwhile to real users?
6. Which public brand and commercial model should be explored after the product direction is accepted?

**Confirmed by the founder:** equal buyer/renter weight, England first, and decisions 0001–0007 in `docs/decisions/`. Those cover the product category, one record per home, answers changing the decision, AI inside tasks plus an optional chat panel, the warm and calm visual direction, both stories in full, and free basics with paid extras. Implement within them; changing one needs a new decision record. **Still proposals:** the screen-level details in this document (layouts, navigation labels, state lists, image briefs), to be settled in the stage 3 specification. The public name, commercial model and prices remain open. No application, publishing flow or public brand has been created.
