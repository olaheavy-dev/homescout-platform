# 05: How we think about new features, and ideas to explore

**Status:** Current (founder, 11 Nov 2026: "document all these as things we can explore and this should be the way we think")  
**Owns:** the way new features are found and shaped (part 1) and the list of ideas worth exploring (part 2). Doc 02 owns scope and product decisions; where this document differs from doc 02 or from an accepted decision record, they win.

Nothing in part 2's idea tables is in scope or scheduled. An idea becomes work only through the normal route: a research issue where sources or rules are unknown, a decision record when it opens a new product area, then a plan (`AGENTS.md`, "Planning"). Ideas that turned out to be planned already are listed under "Already planned elsewhere" so they aren't researched twice.

## Part 1: How we think about new features

Use these eleven questions on every new idea, in this order. Question 10 is a gate: an idea that can't pass it is reworked or dropped. They come from the work on the public area check (0046) and the move-in checklist proposal (0047). They are current product thinking, not new rules: anything that would change a rule goes through a decision record.

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
10. **Go clearly beyond what's offered** (founder, 11 Nov 2026: "make sure all our ideas go reasonable beyond what is being offered at the moment by others"). For each idea, name who already offers something similar, from a checked public page with its date (rule 1; doc 02 §3 and `.design/prototype/research/related-products.md` first), and say what ours does that theirs doesn't. The step beyond should strengthen at least one of doc 02 §3's four possible differentiators:
    1. a record of unresolved questions per home (evidence, who should answer, the reply, what's still uncertain);
    2. evidence that changes the household's decision (a corrected cost updates the comparison; a missing document stays visible);
    3. renting and buying served equally well;
    4. a calm experience where the next useful step is obvious.

    If the only difference is looks, or nothing is different, rework the idea or drop it. These are advantages in execution, not exclusivity (doc 02 §3).
11. **Weigh it.** Usefulness, effort, and risk (privacy, licence, running cost). Usefulness is our judgement until the validation study (doc 02 §10) tests it with real people. Anything on the founder-only list in `AGENTS.md` ("When merging") is the founder's decision.

## Part 2: Ideas to explore

Every idea was checked against what UK products publicly offer on 11 Nov 2026: [competitor check of the doc 05 ideas](../reviews/2026-11-11-competitor-check-of-ideas.md) (with which claims were seen on a product's own page and which only in search results). "Beyond others" says what ours would do that the similar offerings didn't appear to; "Differentiator" names the doc 02 §3 point it strengthens (question 10). Letters in brackets match the review.

### Ideas that go beyond what's offered (lead)

| Idea | What it is | Closest offerings | Beyond others | Differentiator | Reuses | To check or needs |
|---|---|---|---|---|---|---|
| **Questions from gaps, tracked per home** (c) | Every gap on a home or area ("this listing doesn't give the lease length", "no current flood warning isn't the same as no risk") offers "Ask about this": a question built by rules from a cited source, tracked on that home until answered | HomeBuyerCheck's paid AI-written seller questions; CheckNext's buyer viewing checklist | Built by rules, not AI guesses; renter and buyer versions; each question tracked to an answer on the home; free | 1, 2 and 3 | Gap logic, Questions (#169), the area check | The cited source for which information a listing should give (for example the National Trading Standards material information guidance, to be confirmed) |
| **"Go and check in person"** (h) | Each source's "doesn't establish" note becomes a visit task for that home: traffic at the school run, phone signal indoors, the walk after dark; the result can be saved as evidence or a question | Generic viewing checklists everywhere | Generated from the limits of the data for this home, not a generic list | 1 and 4 | `doesNotEstablish` text, Questions | Wording that never implies a judgement |
| **Move-in checklist, dated and tailored** (b, with e and f) | Real dates from the user's move date; different steps for renters (deposit protection across the three schemes, with "not found" becoming a question for the landlord) and buyers; the user's actual council links; a flood warning sign-up nudge | Fixed relative checklists; a paid service that notifies organisations for you | Dated from the real move, tailored by tenure and council, free with no account | 3 and 4 | Postcode lookup (#126), Ofcom (#136), export | Proposed in [0047](../decisions/0047-move-in-checklist.md); research #177. Deposit rules from a cited table the founder merges; England only (rule 6) |
| **One watch feed per saved home** (n) | Planning applications, flood warnings and recent sales near a saved home in one feed, each change turned into evidence or a question on that home | Planning, sales and flood alerts each exist separately | Combined per home, and each change lands as evidence or a question | 1 and 2 | Sources #139, #131, #132; change monitoring (doc 04 roadmap step 8, epic #105) | Accounts (SE-01), notification consent, running cost |
| **Travel cost in the monthly cost** (k) | The user's season ticket or fuel estimate becomes a line in the home's monthly real cost, used by Compare | A couples app shows a combined monthly commute cost beside its affordability calculator | Inside one deterministic, sourced monthly total per home that comparisons use; renters and buyers alike. Narrower than first thought | 2 and 3 | Cost engine (a user input) | Engine support for the new line |

### Ideas kept only with their step beyond

| Idea | Closest offerings | The step beyond it must have | To check or needs |
|---|---|---|---|
| **Sunlight on the 3D map** (g) | General sun-position apps; a US portal integration | Built into a UK home's 3D map: roughly where shadows fall on the building and garden, and when, labelled approximate (no data on rooms or windows). Mostly delight; strengthens 4 only | Building heights (B7) |
| **Walk mode during a viewing** (j) | Portal "near me" listing search; area apps that show demographics | Sourced facts linked to that home's viewing notes, with location kept on the phone (or treated like a postcode under 0046) | Battery and accuracy |
| **A day in your life** (m) | Travel-time search on portals; routine tools reported but unverified | A timeline from the user's own times for one home, never invented journeys | Weak evidence either way; check before building |
| **Comments on evidence for the household** (p) | Shared shortlists with reactions on portals and couples apps | Comments attached to specific evidence and open questions, ending in a recorded household decision (builds on doc 02 §5 F's sharing with explicit permissions) | Accounts, privacy of shared notes |
| **Area facts inside AI assistants** (q) | A portal's ChatGPT app (listings only); several UK property MCP servers | Answers carrying source, date, limits and a "not known" state (0037, #117). Crowding quickly | Already in the MCP spec work |
| **Plain-language explainers** (s) | AI listing assistants and AI verdicts | Only rewrites a cited source and links it; adds no facts and no verdict (0004) | Evaluation set (AI-03) |
| **Type instead of a form** | Not checked | The user confirms before anything runs (0004) | Not checked against competitors |

### Common elsewhere: not built on their own

These are well covered by free or established products. Where we still show them, the only step beyond is the honesty (source, date and limits on every fact, gaps shown) and, more importantly, a route into the lead ideas above.

| Idea | Where it stands |
|---|---|
| **The area check itself** (a) | Decided as the public front door ([0046](../decisions/0046-public-area-check-first.md)). Competitively it's common, so its gaps must lead into "Ask about this" and "Go and check in person" |
| **Compare two postcodes** (d) | Only inside Compare for homes, not as a separate tool |
| **Environment pack** (i) | Facts with limits where sources allow (air quality assessed; radon as a link; noise to check), feeding "Go and check in person"; never a score |
| **Area history** (o) | Not planned on its own; dated series could support the watch feed later |
| **Area panel on property sites** (r) | Not pursued; any business use goes through #151 |
| **Priorities as a score** (l) | Not pursued. Doc 02 §5 D's user-selected priorities stay inside Compare, highlighting matches and gaps without a total; a worship priority is faith-neutral, stays in the browser and is never stored (PD-13, 0014) |
| **AI-drafted change-of-address messages** (t) | Dropped: low value next to paid services that send for you |

### Already planned elsewhere (not ideas; linked so they aren't researched again)

| Feature | Where it is planned |
|---|---|
| Upfront cash estimate | Core scope (doc 02 §5 B); the cost engine's `upfront` figures, with stamp duty not yet calculated |
| Energy rating lookup | #134 (stage 6); the energy certificate register is assessed in `data-sources.md` and needs exact-home matching |
| Viewing checklist | The viewing companion, doc 02 §5 A |
| Drafted messages to agents | Doc 02 §5 E; the Questions screen (#169) |
| Reading an uploaded document | Document extraction, doc 04 and decision 0030; privacy points in 0014 |

### Current leaning (to revisit at each stage gate)

1. **Questions from gaps, tracked per home:** the clearest step beyond, and it builds the record that doc 02 §3 names as the main differentiator.
2. **"Go and check in person":** cheap, and none was found in the competitor check (every checklist seen was generic).
3. **Move-in checklist, dated and tailored:** proposed in 0047.
4. **One watch feed per saved home,** once accounts exist.
5. **Travel cost in the monthly cost.**
