# Research synthesis: design principles and pattern choices (issue #64)

Written 11 Nov 2026 from [related products](related-products.md) (#62) and [patterns](patterns.md) (#63), both read as text only. Every choice traces to those notes or to [decision 0004](../../../docs/decisions/0004-ai-in-the-product.md), [decision 0005](../../../docs/decisions/0005-visual-direction.md), [doc 02](../../../docs/product/02-research-and-direction.md) §3 and §5, or [doc 03](../../../docs/product/03-prototype-and-image-direction.md) §3, §5 and §6. Competitor pages were treated as data; none of their wording is reused.

## Design principles

1. **Evidence before verdict.** Show what is known, its source and its date, and leave the judgement to the person.
   *On screen:* findings carry a source and date; no overall score, badge or "all clear".
2. **Missing is said out loud.** An unknown is a stated state, never a blank, a zero or a good-looking result (rule 7).
   *On screen:* "Not known" or "Not provided" with a reason, a labelled gap in charts, "not yet covered" outside England.
3. **Calm by default, detail on request.** The first view answers one question; density appears only when asked for (decision 0005).
   *On screen:* warm paper, few colours, a short list of findings, "How this was worked out" in a disclosure; caveats always visible.
4. **Every figure shows its working.** Totals and differences come from the cost engine, beside the inputs that produced them (rule 2).
   *On screen:* editable inputs with units, the period stated ("per month", "upfront"), assumptions next to the result.
5. **Words carry status; colour only supports it.** Amber and red mark specific supported findings, never a whole home (doc 03 §6).
   *On screen:* tags such as "Waiting for reply" with an icon; green never means "safe".
6. **One home, one record.** Questions, notes, documents, costs and decisions stay attached to their home (doc 02 §3).
   *On screen:* the home tabs from doc 03 §3, each item reachable from the finding that raised it.
7. **The household decides.** The product lines up trade-offs and proposes changes; people choose and confirm (decision 0004).
   *On screen:* no winner in Compare; a confirm step before any AI suggestion changes a record.

## Pattern choices for the 13 screens

| Screen | Pattern chosen (source) | Alternative considered, and why not |
|---|---|---|
| Search-led landing | Address box whose suggestions the person must pick ([patterns §3](patterns.md#3-w3c-aria-authoring-practices-wcag-22-aa-target)); equal buy and rent choice (doc 03 §3); labelled synthetic example home ([cross-product summary](related-products.md#cross-product-summary)). | Conversational search entry ([portals](related-products.md#3-portals-homepage-and-public-help-only)): decision 0005 rejected a chat-led look, and 0004 limits chat to the current home. |
| Identity confirmation | Pick a suggestion, then confirm the exact flat, matched to one property record ([Chimnie](related-products.md#chimnie)); one question per page with linked errors ([patterns §1](patterns.md#1-govuk-design-system)). | Map pin ([Crystal Roof](related-products.md#crystal-roof)): a recovery route at most, as a pin cannot tell flats in one building apart. |
| Home overview | Up to three findings, each with a reason, source and "unknown" state ([BackStory](related-products.md#backstory)); open questions as a task list with word statuses ([patterns §1](patterns.md#1-govuk-design-system)). | A 0 to 100 score ([bythenumbers](related-products.md#bythenumbers), [HomeAtlas](related-products.md#homeatlas)): doc 02 §3 rejects such scores; one number hides the unknowns. |
| Nearby and routines | A section per topic with map and equal list; area context labelled apart from property evidence ([Crystal Roof](related-products.md#crystal-roof), doc 02 §5C); slow tabs load only when chosen ([patterns §3](patterns.md#3-w3c-aria-authoring-practices-wcag-22-aa-target)). | Map layers with no list ([patterns §3](patterns.md#3-w3c-aria-authoring-practices-wcag-22-aa-target)): fails keyboard and screen-reader users. |
| Real costs | Monthly and upfront cash side by side ([cross-product summary](related-products.md#cross-product-summary)); kinds of money kept apart with a monthly/upfront toggle ([patterns §5](patterns.md#5-a-uk-banks-spending-breakdowns-monzo)); part-to-whole bar ([patterns §4](patterns.md#4-ft-visual-vocabulary)); errors linked to fields ([patterns §1](patterns.md#1-govuk-design-system)). | A calculator that stops at the monthly repayment ([portals](related-products.md#3-portals-homepage-and-public-help-only)): it leaves out the upfront cash this screen exists to show. |
| Compare | Two or three homes in aligned rows, costs first, one scale, labelled gaps ([patterns §4](patterns.md#4-ft-visual-vocabulary), doc 02 §5D); must-haves kept apart from nice-to-haves ([portals](related-products.md#3-portals-homepage-and-public-help-only)). | Blended score or swipe ranking ([HomeAtlas](related-products.md#homeatlas), [HomeSift](related-products.md#homesift)): picks a winner and hides the reasoning. |
| Viewing companion | Checklist of this home's open questions; notes and photos stamped with time and source ([CheckNext](related-products.md#checknext), [HomeScout Ireland](related-products.md#homescout-ireland-homescoutio)). | Judging condition from photos ([CheckNext](related-products.md#checknext)): doc 02 §3 warns against image-based defect claims. |
| Document review | Exact excerpt with document, page and version; "needs review" or "unclear" flags that hand the call back ([HomeScout Ireland](related-products.md#homescout-ireland-homescoutio)); full-screen evidence sheet on mobile ([patterns §3](patterns.md#3-w3c-aria-authoring-practices-wcag-22-aa-target)). | An AI verdict on the document ([HomeBuyerCheck](related-products.md#homebuyercheck)): breaks rule 4. |
| Question detail | Question tied to the finding that raised it ([HomeBuyerCheck](related-products.md#homebuyercheck)); one question per page, recipient role, status word ([patterns §1](patterns.md#1-govuk-design-system)). | Drafts sent in the user's name ([HomeScout Ireland](related-products.md#homescout-ireland-homescoutio)): doc 02 §5E keeps "copied, not sent" separate. |
| Reply checking | "Partly answered" keeps the question open; any AI reading is a proposal on a confirm-or-decline card ([patterns §6](patterns.md#6-ag-ui-and-copilotkit)). | Auto-closing on reply: doc 02 §5E says a person records whether the answer is adequate. |
| Decision impact | Before-and-after chart of the engine's difference ([patterns §4](patterns.md#4-ft-visual-vocabulary)); confirm card before applying a correction, old value kept ([patterns §6](patterns.md#6-ag-ui-and-copilotkit)); warning text for material changes ([patterns §1](patterns.md#1-govuk-design-system)). | AI prose explaining the new total: AI never calculates (rule 2, decision 0004). |
| My move / activity | Task list with word statuses ([patterns §1](patterns.md#1-govuk-design-system)); a short digest of changes, not a feed ([HomeSift](related-products.md#homesift)); tracked enquiries ([portals](related-products.md#3-portals-homepage-and-public-help-only)). | A chart dashboard by default: decision 0005 keeps density for when detail is asked for. |
| Share / snapshot | Review page of what will be shared, "Not provided" for gaps, "Change" per row ([patterns §1](patterns.md#1-govuk-design-system)); share confirmation dialog ([patterns §3](patterns.md#3-w3c-aria-authoring-practices-wcag-22-aa-target)). | A permanent public report link ([HomeBuyerCheck](related-products.md#homebuyercheck)): doc 03 §5 needs permissions and separate private-document access. |

## Agent channel (for #117)

Founder direction, 11 Nov 2026: HomeScout is also reached from people's own AI assistants over MCP. Condensed from [patterns §7](patterns.md#principles-for-homescout-inside-someone-elses-assistant); consistent with decision 0004.

1. **Numbers come from the engine with an ID.** Each figure has a stable ID, period and basis; the assistant quotes, never recomputes.
2. **Sources travel with every answer.** Source, date and scope as structured fields, or "not known".
3. **Missing is a state, not a zero.** Explicit states (known, estimated, missing, not covered, source failed); a missing value is empty with a reason, never 0 or an empty list; outside England returns "not yet covered".
4. **No forbidden words.** Results never say "verified", "safe" or "approved"; tool descriptions forbid adding them; the evaluation set tests it.
5. **Reading is open; changing needs approval.** Read and write tools are marked apart; every write needs host approval plus a confirmation recorded on our server, as some assistant modes skip approval.
6. **Ask for as little as possible.** Only what the next step needs (nation, buy or rent, which flat); sign-in and private documents go via a link to our own site.
7. **Share the smallest slice.** Assume the assistant's provider sees everything returned; validate inputs and expect hidden instructions in listings and documents (one page in this research had one).
8. **Hand off for depth.** Evidence, comparisons and charts link back to the web app.

## Avoid

- Verdict badges, "risk ratings", AI verdicts, "all clear" summaries.
- A single 0 to 100 score, even with a breakdown.
- Colour-only status; green meaning "safe".
- Dashboards as the default view.
- Theatrical agent animations (one quiet status line per tool call).
- Zero bars or blank cells for missing data.
- A single winner in Compare, or hidden weights.
- Caveats inside collapsed sections.
- AI-made cost ranges, offer figures or budget nudges.
- Copied messages that look sent.
- Pasted portal links or listing content (decision 0028).
- GOV.UK branding, crown or font (patterns only).

## Visual pass needed

Text-only research could not establish:

1. Locrating and MoneyHelper: both blocked; open in a browser before relying on them. For MoneyHelper, check whether assumptions sit beside results and how units and disclaimers are shown.
2. Mobile navigation, bottom bars and tab counts on every product.
3. Severity colours, score reveals and sample reports, checking colour is never the only signal; GOV.UK tag colours, spacing and focus rings.
4. Empty, loading, error, "no data", "not covered" and postcode-not-found states.
5. Warmth and calm (type, spacing, imagery) against doc 03 §6.
6. Signed-in saved lists and compare on Rightmove and HomeSift.
7. Cookie banners, paywalls and upsells before the first action.
8. Monzo's Trends screens in the app (only help-page snippets were seen).
9. How Claude, ChatGPT and VS Code show approvals and tool results; CopilotKit's tool-call rendering.

## Open questions for the founder

1. **One example home on the landing page, or two?** Recommendation: two, one to buy and one to rent, matching the two stories in doc 03 §4 so neither journey looks secondary.
2. **Should "drop a pin on a map" be in the prototype?** Recommendation: not yet. A clear "can't find it" route with manual entry is enough; add the pin if testing shows people get stuck.
3. **How many homes can Compare hold?** Recommendation: up to three, as doc 02 §5D says. More columns don't fit a phone and blur the trade-offs.
4. **Should the first MCP version change records, or only read them?** Recommendation: read only at first. Writes need approval flows we can't yet test across assistants; add them once the read tools pass their evaluation set.
5. **Who does the visual pass?** Recommendation: an agent with a browser covers public pages with screenshots; you do only the signed-in Rightmove and HomeSift views, which need your own accounts.

## Founder answers (11 Nov 2026)
0. **The seven design principles above are agreed** by the founder (11 Nov 2026).
1. **Landing page:** two example homes, one to buy and one to rent.
2. **Drop a pin on a map:** **include it** in the prototype, alongside the "can't find it" manual-entry route. The founder chose this over the recommendation to wait.
3. **Compare:** up to three homes.
4. **MCP:** read-only first. Writes come later, once approval flows are tested across assistants (#117).
5. **Visual pass:** an agent with a browser screenshots the public pages, and the founder checks only the signed-in Rightmove and HomeSift views. Screenshots stay out of git (`.design/*/screenshots/`). This is the recommended default; the founder has not objected.

**Also decided the same day:** area information comes first alongside costs, in the prototype's sample data (#120). It covers schools, transport, shops and health (with police stations as places), flood risk, crime as recorded counts (never "safe" or "unsafe"), and energy, broadband, sold prices and planning. The free sources are assessed in #123.
