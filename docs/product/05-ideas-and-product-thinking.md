# 05: How we think about new features, and ideas to explore

**Status:** Current (founder, 11 Nov 2026: "document all these as things we can explore and this should be the way we think")  
**Owns:** the way new features are found and shaped (part 1) and the list of ideas worth exploring (part 2). Doc 02 owns scope and product decisions; where this document differs from doc 02 or from an accepted decision record, they win.

Nothing in part 2's idea tables is in scope or scheduled. An idea becomes work only through the normal route: a research issue where sources or rules are unknown, a decision record when it opens a new product area, then a plan (`AGENTS.md`, "Planning"). Ideas that turned out to be planned already are listed under "Already planned elsewhere" so they aren't researched twice.

## Part 1: How we think about new features

Use these questions on every new idea, in this order. They come from the work on the public area check (0046) and the move-in checklist proposal (0047). They are current product thinking, not new rules: anything that would change a rule goes through a decision record.

1. **Whose moment is it?** Name the person (buyer, renter, household) and the moment in their move: choosing where to look, checking a home or area, deciding, moving in. The person brings the address or listing details themselves (doc 02 §1); we never fetch listings (0028).
2. **Free official sources first.** What open or official source answers it, under what licence, at what detail (postcode or address), and at what cost and limits? Check `docs/references/data-sources.md` first; unknowns go into a research issue, never into the product (rules 1 and 3).
3. **Answer, link or say unknown.** Split the idea into pieces and give each one of three honest outcomes:
   - **answer** it, when a source supports it;
   - **link** to the official place that does, when we can't hold the data (for example bin days, 0028);
   - **say it's unknown** and how to find out, when nothing can tell us (for example who supplies a home's energy). Never a guess (rule 7).
4. **Gaps can be features.** What we can't tell is useful when it becomes an action: "go and check this in person", "ask the agent this".
5. **No scores or verdicts from us.** Facts with their source, date and limits; nothing is called safe, verified or approved (rule 4). Doc 02 §5 D allows comparing by priorities the user selects; any total or ranking would need its own decision record.
6. **Browser first, no account.** Keep inputs in the browser where possible; anything the server needs (such as a postcode) travels in the request body or URL fragment and is neither stored nor logged (0046, 0014). Accounts come only when saving something is the value (SE-01).
7. **Reuse before building.** Name what the idea reuses: the postcode lookup, the source adapters (0029), the cost engine (0019), the browser export, the checklist pattern, the 3D map. Prefer ideas that are mostly reuse.
8. **AI explains, drafts and fills in; it never decides.** Following 0004 (and 0030 for extraction):
   - good uses: plain-language explanations of a cited source, drafts the user sends themselves, turning typed sentences into form inputs the user confirms;
   - never: calculating money or deadlines (the cost engine and cited rule tables do that), marking a step done, judging a home or area, filling a gap with a guess;
   - build each feature on rules and sources first; AI is an optional layer, and each use is checked for running cost and privacy (the provider sees what the user typed).
9. **Smallest useful slice.** Find the version that is achievable now and still useful; say plainly what is left out and why.
10. **Weigh it.** Usefulness, uniqueness (checked against competitors, doc 02 §3, never assumed), effort, and risk (privacy, licence, running cost). Anything on the founder-only list in `AGENTS.md` ("When merging") is the founder's decision.

## Part 2: Ideas to explore

Grouped by theme. "Reuses" names existing or planned parts; "To check or needs" names what must be confirmed first.

### Small free tools (browser first, no account)

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Move-in checklist** | A checklist timed to the move date, tailored by postcode, tenure and a tick-list | Postcode lookup (#126), Ofcom source (#136), export | Proposed in [0047](../decisions/0047-move-in-checklist.md); research #177 |
| **Questions to ask the agent** | From what the user enters about a listing, a ready-to-send list of questions for what it leaves out (council tax band, service charge, lease length, energy rating) | Gap logic, Questions (#169) | Which gaps apply to which tenure (cited); a free, no-account version of doc 02 §5 E |
| **Compare two postcodes** | Two area checks side by side (near work, near family) | The area check (B6a) | None beyond the area check |
| **Renter's deposit check** | Links to the government-approved deposit protection schemes, plus deposit rules from a cited table | Rule tables (rule 3) | England only; other nations "not yet covered" (rule 6). Legal source and effective dates; the founder merges the rule table |
| **Flood alerts for your new home** | A link to the Environment Agency's free flood warning sign-up near a warning area | Flood source (#131) | The current sign-up page and its terms |

### After the first Nearby features: seeing the place more truly

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Sunlight on the 3D map** | A time-of-day and season slider showing roughly where shadows fall on the building and garden, and when | 3D map (B7), approximate building heights | Labelled approximate; no data on rooms or windows |
| **"Go and check in person" list** | Built from what we can't tell: rush-hour traffic, phone signal indoors, the walk after dark | Gap and `doesNotEstablish` text | Wording that never implies a judgement |
| **Environment pack** | Air quality, mobile signal, road and rail noise as facts with limits; radon as a link | Source adapters | Air quality: Defra UK-AIR, assessed in `data-sources.md` (OGL). Mobile: Ofcom, terms unread and its v1 API ends 30 Nov 2026 (`data-sources.md`). Radon: link to the official map, don't ingest (`data-sources.md`). Noise: not yet assessed (to check) |
| **Walk mode during a viewing** | On a phone, what's near as you walk the area | Nearby data, map | Location stays on the device with the area's nearby data downloaded, or is treated like a postcode under 0046; battery and accuracy |

### After the first Nearby features: joining the area to the decision

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **The cost of getting around** | The user's season ticket or fuel estimate goes into the monthly real cost | Cost engine (as a user input) | Engine support for the new line |
| **What matters to you** | The user picks priorities (a park for the dog, a step-free station, a place of worship nearby, a nursery); matches and gaps are highlighted | Nearby data, household criteria (#147) | No total or ranking without a decision record (part 1, question 5). A worship priority is faith-neutral, stays in the browser and is never stored (PD-13, 0014); storing it would need an Article 9 condition first |
| **A day in your life** | A weekday timeline from the user's own estimates: school run, commute, shop | Household estimates | Times are the user's own; we never invent journey times |

### Watching an area over time (needs accounts)

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Watch this area** | Alerts for new planning applications, flood warnings and recent sales near a saved home | Sources #139, #131, #132; builds on change monitoring (doc 04 roadmap step 8, epic #105), which watches a home's evidence | Accounts (SE-01), notification consent, running cost |
| **How this area has changed** | Several years of sold prices and crime counts with their dates, never a rating | Sources #132, #130 | History depth and licence of each source |
| **Share with your household** | A shared area report the household can comment on | Export; builds on doc 02 §5 F's sharing with explicit permissions; commenting is the new part | Accounts, privacy of shared notes |

### Reaching people elsewhere

| Idea | What it is | Reuses | To check or needs |
|---|---|---|---|
| **Ask the area in AI assistants** | The area check and checklist as tools with our widget inside ChatGPT or Claude | MCP server (0037, #117) | Already in the MCP spec work |
| **Area panel for property sites** | Sourced area facts embedded on estate agent and letting listings | The area check | Business use (#151): its own decision on licences, pricing and brand control |

### AI layers on these tools (decision 0004)

| Idea | Where it helps | Guardrail |
|---|---|---|
| **Plain-language explainers** | "What does this mean?" beside any sourced item (for example "no current flood warning") | Rewrites the cited source and links it; adds no facts |
| **Change-of-address drafts** | Emails or letters to a bank, employer or other organisation from the move-in checklist's tick-list | The user reviews and sends; we never send (an extension of 0047, not planned) |
| **Type instead of a form** | "Moving from Leeds to a flat in Bristol on 3 March, I have a car" fills the inputs | The user confirms before anything runs |

### Already planned elsewhere (not ideas; linked so they aren't researched again)

| Feature | Where it is planned |
|---|---|
| Upfront cash estimate | Core scope (doc 02 §5 B); the cost engine's `upfront` figures, with stamp duty not yet calculated |
| Energy rating lookup | #134 (stage 6); the energy certificate register is assessed in `data-sources.md` and needs exact-home matching |
| Viewing checklist | The viewing companion, doc 02 §5 A |
| Drafted messages to agents | Doc 02 §5 E; the Questions screen (#169) |
| Reading an uploaded document | Document extraction, doc 04 and decision 0030; privacy points in 0014 |

### Current leaning (to revisit at each stage gate)

1. **"Go and check in person" list:** cheap, and a clear expression of the honesty principle (uniqueness not yet checked).
2. **The cost of getting around:** the bridge between area and cost.
3. **Sunlight on the 3D map:** the strongest visual moment, building on the immersive map.
4. **Watch this area,** once accounts exist, because it brings people back.
