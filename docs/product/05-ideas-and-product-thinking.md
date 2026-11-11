# 05: How we think about new features, and ideas to explore

**Status:** Current (founder, 11 Nov 2026: "document all these as things we can explore and this should be the way we think")  
**Owns:** the way new features are found and shaped (part 1) and the list of ideas worth exploring (part 2).

Nothing in part 2 is in scope or scheduled. An idea becomes work only through the normal route: a research issue where sources or rules are unknown, a decision record when it opens a new product area, then a plan (`AGENTS.md`, "Planning"). Where this document and an accepted decision record differ, the record wins.

## Part 1: How we think about new features

Use these questions on every new idea, in this order. They come from the work on the public area check (0046) and the move-in checklist proposal (0047).

1. **Whose moment is it?** Name the person (buyer, renter, household) and the moment in their move: finding, checking, deciding, moving in. A feature that serves no moment isn't Vestagraph's.
2. **Free official sources first.** What open or official source answers it, under what licence, at what detail (postcode or address), and at what cost and limits? Unknowns go into a research issue, never into the product (rules 1 and 3; `docs/references/data-sources.md`).
3. **Answer, link or say unknown.** Split the idea into pieces and give each one of three honest outcomes:
   - **answer** it, when a source supports it;
   - **link** to the official place that does, when we can't hold the data (for example bin days, 0028);
   - **say it's unknown** and how to find out, when nothing can tell us (for example who supplies a home's energy). Never a guess (rule 7).
4. **Gaps can be features.** What we can't tell is useful when it becomes an action: "go and check this in person", "ask the agent this". Honesty is the product.
5. **No scores, no verdicts.** Facts with their source, date and limits. Matches can be shown; they are never added up into a rating, and nothing is called safe, verified or approved (rule 4).
6. **Browser first, no account.** Keep inputs in the browser and nothing stored or logged, as in the public area check (0046, 0014), until saving something is the value. Accounts come only when the feature needs them (SE-01).
7. **Reuse before building.** Name what the idea reuses: the postcode lookup, the source adapters (0029), the cost engine (0019), the browser export, the checklist pattern, the 3D map. Prefer ideas that are mostly reuse.
8. **AI explains, drafts and fills in; it never decides.** Following 0004:
   - good uses: plain-language explanations of a cited source, drafts the user sends themselves, turning typed sentences into form inputs the user confirms, pulling dates and figures out of a document for the user to confirm;
   - never: calculating money or deadlines (the cost engine and cited rule tables do that), marking a step done, judging a home or area, filling a gap with a guess;
   - build each feature on rules and sources first; AI is an optional layer, and each use is checked for running cost and privacy (the provider sees what the user typed).
9. **Smallest useful slice.** Find the version that is achievable now and still useful; say plainly what is left out and why.
10. **Weigh it.** Usefulness, uniqueness (does any other product do it honestly?), effort, and risk (privacy, licence, running cost). Running costs and new legal or tenancy rule tables are founder decisions (`AGENTS.md`).

## Part 2: Ideas to explore

Grouped by theme. "Reuses" names existing or planned parts; "To check" names what must be confirmed first. Source claims marked "to check" are unconfirmed.

### Small free tools (browser first, no account)

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Move-in checklist** | A checklist timed to the move date, tailored by postcode, tenure and a tick-list | Postcode lookup (#126), Ofcom source (#136), export | Proposed in [0047](../decisions/0047-move-in-checklist.md); research #177 |
| **Questions to ask the agent** | From what a listing leaves out (council tax band, service charge, lease length, energy rating), a ready-to-send list of questions | Gap logic, Questions (#169) | Which gaps apply to which tenure (cited) |
| **Viewing checklist** | What to look at and ask at a viewing, by buying or renting, flat or house, leasehold or freehold; print or phone | Checklist pattern | Sources for each item |
| **Compare two postcodes** | Two area checks side by side (near work, near family) | The area check (B6a) | None beyond the area check |
| **Energy rating lookup** | A home's energy certificate details | A new source adapter | Which official register and API, its licence and limits (to check) |
| **Renter's deposit check** | Links to the government-approved deposit protection schemes, plus deposit rules from a cited table | Rule tables (rule 3) | Legal source and effective dates; founder merges the rule table |
| **Flood alerts for your new home** | A link to the Environment Agency's free flood warning sign-up near a warning area | Flood source (#131) | The sign-up page and its terms |
| **Upfront cash estimate** | Deposit, moving costs and fees from the cost engine, with anything not calculated shown as unknown | Cost engine | Which items the engine covers |

### After the first Nearby features: seeing the place more truly

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Sunlight on the 3D map** | A time-of-day and season slider that moves shadows: which rooms and gardens get sun, and when | 3D map (B7), building heights | Labelled approximate; how heights are sourced |
| **"Go and check in person" list** | Built from what we can't tell: rush-hour traffic, phone signal indoors, the walk after dark | Gap and `doesNotEstablish` text | Wording that never implies a judgement |
| **Environment pack** | Road and rail noise, air quality, radon, mobile signal, as facts with limits | Source adapters | Whether official open maps exist for each, their licences and detail (to check) |
| **Walk mode during a viewing** | On a phone, the device's location (kept on the phone) shows what's near as you walk | Nearby data, map | Location never leaves the device; battery and accuracy |

### After the first Nearby features: joining the area to the decision

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **The cost of getting around** | The user's season ticket or fuel estimate goes into the monthly real cost | Cost engine (as a user input) | Engine support for the new line |
| **What matters to you** | The user picks priorities (a park for the dog, a step-free station, a place of worship nearby, a nursery); matches and gaps are highlighted, never scored | Nearby data, household criteria (#147) | No ranking or total; PD-13 for worship |
| **A day in your life** | A weekday timeline from the user's own estimates: school run, commute, shop | Household estimates | Times are the user's own; we never invent journey times |

### Watching an area over time (needs accounts)

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Watch this area** | Alerts for new planning applications, flood warnings and recent sales near a saved home | Sources #139, #131, #132 | Accounts (SE-01), notification consent, running cost |
| **How this area has changed** | Several years of sold prices and crime counts with their dates, never a rating | Sources #132, #130 | History depth and licence of each source |
| **Share with your household** | A shared area report the household can comment on | Export, accounts | Accounts, privacy of shared notes |

### Reaching people elsewhere

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Ask the area in AI assistants** | The area check and checklist as tools with our widget inside ChatGPT or Claude | MCP server (0037, #117) | Already in the MCP spec work |
| **Area panel for property sites** | Sourced area facts embedded on estate agent and letting listings | The area check | Business use (#151): its own decision on licences, pricing and brand control |

### AI layers on these tools (decision 0004)

| Idea | Where it helps | Guardrail |
|---|---|---|
| **Plain-language explainers** | "What does this mean?" beside any sourced item (for example "no current flood warning") | Rewrites the cited source and links it; adds no facts |
| **Drafted messages** | Questions to an agent from the gaps; change-of-address emails | The user reviews and sends; we never send |
| **Type instead of a form** | "Moving from Leeds to a flat in Bristol on 3 March, I have a car" fills the inputs | The user confirms before anything runs |
| **Read an uploaded document** | Dates and figures from a tenancy agreement or management pack for the user to confirm | Needs its own privacy decision first |

### Current leaning (to revisit at each stage gate)

1. **"Go and check in person" list:** cheap, unique, the clearest expression of the honesty principle.
2. **The cost of getting around:** the bridge between area and cost.
3. **Sunlight on the 3D map:** the strongest visual moment, building on the immersive map.
4. **Watch this area,** once accounts exist, because it brings people back.
