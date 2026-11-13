# Pilot release: area check with AI on the page and in ChatGPT and Claude — design

**Date:** 13 Nov 2026 · **Stage:** 5b (the public area check, decision 0046) · **Status:** approved by the founder, 13 Nov 2026 ("Approve (Recommended)"); extended after approval by the founder's later answers (goal 7, the isometric card, the 0014 change, search distances, outbound links, and the Accuracy and Countries sections, each approved in a prompt window)

## Intent
The pilot (stage 5b) is Vestagraph's first public release: anyone types a postcode and sees what is around it, with sources and limits, no account and no personal details collected (0046). The founder wants the pilot to also offer AI in two places from day one:
- **on the page:** a chat about the area result in front of the visitor;
- **in the visitor's own ChatGPT or Claude:** Vestagraph's area tools, through the MCP server planned in 0037.

Founder, 13 Nov 2026: typed "both, on the page and in their own ChatGPT or Claude"; in prompt windows, "Both on day one" (over the recommended staged rollout) and extras "Questions to ask, Broadband and mobile, Sold prices nearby, Go-check-in-person list, what else can we add from the data we plan". The founder also typed "can we not have disclaimer?"; the agent answered yes, a short disclaimer on top of the safeguards below, never instead of them, and the founder then approved the design that includes it.

Why it matters: it shows what makes Vestagraph different (every fact with its source, date and limits, and honest gaps) in the places people already ask questions, and it tests the data adapters, hosting, privacy and AI rules on the lowest-risk data before any account or personal data exists.

## Goals
1. **One set of area tools** used by the page, the MCP server and the on-page chat, so all three give the same facts with the same labels.
2. **Public read-only MCP server** with the area tools, usable from ChatGPT and Claude, no key, rate-limited.
3. **On-page chat** on Check an area and the landing result, answering only from that postcode's sourced area data.
4. **Pilot extras, wave 1** (founder's picks): questions to ask, broadband and mobile coverage, nearby sold prices, a "go and check in person" list.
5. **Pilot extras, wave 2** (agent's proposal from the planned data, for the founder to trim): planning applications nearby, school inspection results, air quality, compare two postcodes.
6. Day-one safeguards for cost, abuse, privacy and accuracy, all in place before launch.
7. **More pilot features with no personal data** (founder, 13 Nov 2026, asked in a prompt window, chose all four: "Explain-this buttons, Share a link, Recent postcodes (browser), Report a problem"):
   - **Explain this:** one tap per topic for a plain-language explanation of that source (0004's task AI), using the same AI rules as the chat; counts towards the daily AI cap and sits behind the same bot check and rate limits as the chat. Each topic's explanation is cached once written (an exact-match cache per topic and source version, 0025), so repeat taps cost nothing; `explain_source` in the MCP server returns only cached or pre-written text and never calls a model; every pilot topic's text is written and reviewed before launch, and if one is missing it returns "Explanation not yet available" with no text, never an empty or invented one (rule 7).
   - **Share a link:** copies a link to the postcode's result with the postcode in the `#` part, so nothing is stored or logged.
   - **Recent postcodes:** off by default; the visitor turns on "Remember postcodes on this device", which is their consent under PECR (0014's rule for "Recently viewed"); a short list kept only in their browser, with a Clear button; never sent to us. Named in the privacy notice and the PECR check.
   - **Report a problem with this fact:** a one-tap flag stored only as a daily count per source, topic, fact record ID and local authority (never the postcode, no per-report row, no time finer than the day, no client key or IP address); sold-price facts are counted by source and local authority only, without the record ID, because a sale points to one address; no free text, so no personal details can be typed in; counts kept for 90 days; rate-limited and behind the bot check; part of FE-05 and named in the privacy notice.

## Non-goals
- Accounts, saved homes, stored searches or chat history (0046: accounts come after the pilot).
- Costs, compare-homes, documents, questions tracking or any home-level feature; the chat and tools are about an area only.
- Any write tool, in MCP or chat (0004, doc 05: writes need their own decision).
- Energy ratings (need the exact home, a paid address lookup, DA-06) and commute times (paid routing) in the pilot.
- Business-only features (#151).

## Anti-goals (failure even if it works)
- The AI or any tool calls an area "safe", "good", "verified" or "approved", recommends an area, or turns crime, flood or worship data into a score (rule 4, 0004, PD-13). ChatGPT's or Claude's own model is outside our control (0037): the tool descriptions say "quote the sourced facts; do not calculate, score or call an area safe or good", the MCP docs say plainly that the host's wording is not Vestagraph's, and the evaluation set covers our tool outputs and our own chat only.
- A missing or failed source shown as zero, none or a clean result (rule 7).
- AI states a fact with no source, invents one, or calculates a figure (rule 1, 0004).
- A searched postcode or chat text ends up in any of our logs, analytics or error reports (0014), or with the AI provider beyond what its terms allow: never used for training, and kept no longer than its stated abuse-check period, which the privacy notice states (founder's choice, answer 2 below). The stage 5b gate's "absent from every server, application and hosting log" means our logs and our hosting's, not that abuse-check copy.
- A public endpoint that lets anyone run up an unbounded AI bill.
- Listing content scraped or copied (0028).

## Constraints
- **Rules 1–9 in `AGENTS.md`**, decision 0004 (AI behaviour), 0014 (privacy), 0028 (no scraping), 0029 (adapters label each value Live, Cached, Fallback or Unavailable), 0037 (MCP: tools first, then MCP Apps widgets, open `ui://` standard only), 0049 (Python; the official `mcp` SDK; FastAPI from the founder's template), PD-13 (places of worship), England only (rule 6: other nations "not yet covered").
- **Sources:** only those in `docs/references/data-sources.md`, each with its licence recorded in DA-05 before use, and attribution in the page, the chat, the MCP results and the printout.
- **Privacy (0014, extended):** the postcode travels in the URL fragment or a request body, never a query string; message text and tool arguments are never written to server, application, hosting or tracing logs; IP addresses are dropped or anonymised before logging; chats are not stored; the AI provider never trains on inputs and keeps them only briefly for abuse checks, as its terms state (founder's choice, answer 2 below; confirmed for the chosen provider under AI-01).
- **Cost:** a hard monthly budget cap and alerts (IN-05) before launch; a daily AI spend cap after which the chat shows an honest "Chat is paused for today, the area check still works" state; if the AI provider fails, the chat shows "Chat unavailable right now" (0029 applies to the provider too); token use and cost are monitored (0025).
- **Abuse:** rate limits per anonymised client for the API, the chat and the MCP server; a bot check on the chat, Explain this and Report a problem (an invisible challenge such as Cloudflare Turnstile, since the domains use Cloudflare; it reads device signals, so it is named in the privacy notice and the PECR check, 0014 part 1); limits on message length, turns per chat and tokens per answer.
- **AI safety (0025):** output guards check every answer for the forbidden words and verdicts before it is shown; tool results and page content are treated as data, never as instructions (prompt-injection defence).
- **Accuracy (0004 applied to an area):** the chat answers only about the current postcode's area result, using the area tools; every claim links its source and date or says it isn't known; it never calculates (any figure comes from a tool); gaps become suggested questions.

## The disclaimer (copy to finalise in the build)
Shown above the chat box and in the MCP server's description, short and plain:
- "Answers come only from the sources shown, and can still be wrong. Check the source before relying on it."
- "Don't type personal details. Chats aren't saved."
- A link to the privacy notice, which says the same and names the AI provider.

## Approaches
1. **Staged pilot (agent's recommendation):** area check plus the MCP server on day one (almost no running cost, since the visitor's assistant pays for the AI), on-page chat a few weeks later with a daily cap once real traffic and abuse are known. Lowest risk.
2. **Both on day one (chosen by the founder, 13 Nov 2026):** the MCP server and the on-page chat launch with the area check. A bigger launch; the AI bill and abuse exposure start with everything else, so every safeguard above is a launch blocker, not a follow-up.
3. **Area check alone:** today's plan, AI at stage 6. Cheapest, but drops the founder's request.

All three share one area-tools layer, so approach 2 adds launch-day risk, not extra architecture.

## Shape of the build
```
area tools (Python, one package)
  find_postcode_area(postcode)         -> area codes, nation; "not yet covered" outside England
  nearby_places(postcode, categories)  -> places with straight-line distance, source, date, label
  area_topic(postcode, topic)          -> flood, crime counts, schools, transport, broadband, sold prices, ...
  explain_source(topic)                -> what the source says and doesn't establish
  questions_for_gaps(postcode)         -> ready questions from the gaps (wave 1 "questions to ask")
        |                    |                         |
  FastAPI API          MCP server (public,       on-page chat (agent; calls
  (Check an area page)  read-only, no key,        the same tools; never
                        rate-limited)             calculates; cites sources)
```
- Each tool returns values with their source, date and Live / Cached / Fallback / Unavailable label (0029); a failed source returns "Unavailable", never empty.
- The MCP server exposes the same tools; MCP Apps widgets (an area summary card) come after the tools work everywhere (0037).
- **Isometric area card in answers** (founder, 13 Nov 2026, typed "would we be able to use the 3d designs presentation in the chat as reponse?" [sic]; the agent answered yes, then asked): a card showing the postcode's nearest places as a small isometric scene in the approved style (FE-10, like the landing hero), generated from the same tool data, never hand-placed. It appears in the on-page chat and, as an MCP Apps widget (`ui://`, 0037), inside hosts that support widgets. Each place sits at its true straight-line distance and direction; every card carries its sources and dates; the text answer is always there too, as the accessible version and for hosts without widgets. It comes after the plain tools work in every host (0037's order). Like the 3D map (0046), it never suggests flood or crime risk. The founder confirmed it in a prompt window: "Yes, include it (Recommended)".
- The chat runs server-side, holds the conversation only for the open page (no storage), and is given the area result plus tool access; it cannot fetch the web.

## Decisions needed before building (each recorded; founder answers in prompt windows)
1. **New decision record (amends 0038 and 0046, extends 0004):** a public read-only MCP server without keys for public area data, and AI on the public pilot. 0038 currently allows no-auth only for fixture data; 0004's chat currently answers only about a home.
2. **AI-01 model provider and AI-04 framework,** brought forward from stage 6. AI-09's trial (Microsoft Agent Framework for Python against LangChain and LangGraph) would run first, or the pilot uses the simplest option and the trial follows.
3. **IN-05 budget:** the monthly cap and the daily AI cap, in pounds (founder-only, running cost).
4. **SE-02 parts 1 and 2:** the privacy notice covering chat, the provider and how long it keeps inputs, and the log rules.
5. **DA-05 licences** for each wave 1 and wave 2 source, including whether each allows keyless, bulk-capable access through the public MCP server (0014 rate-limits partly because some licences require it) (Ofcom's API terms are unread and its mobile v1 API ends 30 Nov 2026; Price Paid limits address use to price display; Ofsted's licence is unverified).
6. **AI-03 evaluation set** for the chat and tools before launch (0025: evaluation first): a fixed set of questions, including attempts to get "is it safe", a score, a calculation or personal advice, each with the expected refusal or sourced answer.
7. **Doc 04 §9:** stage 5b grows to include the AI pieces; the order inside 5b is planned in `writing-plans`.

## Privacy rule changed (13 Nov 2026)
0014 says the free public view makes "no AI calls per anonymous visitor". The founder, asked in a prompt window, chose "Allow with safeguards (Recommended)": for the pilot's chat and Explain this only, AI calls per anonymous visitor are allowed when the provider never trains on inputs and keeps them only briefly, nothing is stored by us, the disclaimer is shown and the privacy notice names the provider. Recorded in decision 0051; everything else in 0014 stands.

## How it differs from Google Maps
The founder asked, typed: "how is this different from Google maps? just validating". Google Maps is better at finding places, opening hours, reviews, directions and Street View, and the pilot does not compete there: it links out (below). The pilot leads with what Google Maps doesn't show: official public records (recorded crime counts, flood warnings, school inspections, sold prices, planning applications), every fact with its source, date and limits, gaps said out loud, questions to ask and a check-in-person list, AI that cites or says "not known", and no tracking, account or ads. Nearby places are context, not the headline.

## Search distances
Founder, 13 Nov 2026: typed "I like the show wider should we default 5km for all the topics, lets discuss?", then, in a prompt window, "Yes, this split (Recommended)":
| Topic | Default | Wider |
|---|---|---|
| Nearest places (shops, pharmacy, GP, parks, bus stops, stations, schools) | Look up to 5 km; show the nearest few, each with its distance | "Show more" lists more places, not a wider area |
| Sold prices, planning applications | 500 m | "Show wider" up to 5 km, the radius stated beside the results |
| Crime counts | 1 mile, matching police.uk's own street-level search ("within a 1 mile radius of a single point", [data.police.uk](https://data.police.uk/docs/method/crime-street/)) | Kept fixed in the pilot so counts compare with police.uk, and because crime locations are approximate; the page says so. The source also accepts a custom area, so widening is possible later |
| Flood, broadband, air quality | The postcode itself | — |

- Nothing is shown as "none": beyond the limit the page says "No pharmacy found within 5 km", never "none" or zero (rule 7).
- The landing hero's "+N more nearby" counts places within 5 km; the home workspace's Nearby follows the same distances.
- Every distance is labelled "straight-line from the postcode centre".
- The chosen widths live in the link's `#` part, like the postcode; the chat and the MCP tools take a radius up to the same 5 km cap and state it in every answer.
- The map fits itself to the places shown; the list holds everything. The 400 m ring on the landing hero is an illustration, not this rule.

## Outbound links
Founder, 13 Nov 2026: typed "yes add the Google Maps link"; then, in prompt windows, the link groups "Official checks, School and health pages, Local council, Travel" and, for the postcode, "Any site that accepts it" (the agent had recommended official sites only).
- **Google Maps:** directions and the place itself, beside each place.
- **Official checks:** the GOV.UK long-term flood risk checker, find an energy certificate, check a council tax band, the police.uk neighbourhood team, the Coal Authority map. These cover what the pilot cannot show itself (licences or exact-address limits).
- **School and health pages:** each school's Ofsted report and register page; each GP's or pharmacy's NHS page.
- **Local council:** the council's website and planning search for the postcode's area.
- **Travel:** National Rail journey planner from the nearest station.

Rules for every link:
- The link names where it goes and, when it carries the postcode, says so ("Opens Google Maps · Google will see this postcode").
- Nothing is sent until the visitor clicks; links use `rel="noreferrer"`, and the site sends a `Referrer-Policy` header too. (Browsers never send the `#` part of a link in the referrer anyway, so the page's own postcode doesn't leak that way; this is extra protection.)
- The postcode never reaches our own logs (0014); the privacy notice says which linked sites receive it when clicked (0014, "Still to decide"). Scenario AREA-18 covers the label and the referrer; AREA-15 covers requests the page makes by itself.
- A link is never a fact: the page never says what the linked site will show.

## Accuracy
The founder asked, typed: "how do we ensure that the 3d representation and our facts are very very accurate". The agent's proposal, approved by the founder in a prompt window ("Approve (Recommended)", 13 Nov 2026):

**Facts**
1. Nothing typed by hand: every value comes from a stored, cited source with its date (official records, or OpenStreetMap for places) (rule 2); the fixtures are the only test data.
2. Tested distance maths: straight-line distance (and its display in metres or kilometres) is a calculated output, so rule 2 applies to it: one deterministic geometry module in the area tools package, written test-first with independent worked examples, from the postcode centre; the result is stored with the area result, and screens and AI only quote it. Nearby's "never calculated figures" means the UI and AI never calculate.
3. Source-change alarms: each adapter has a contract test that fails when a source changes its format, run nightly and advisory, outside the merge gate, a failure opening an issue (0029); a stale source is labelled "Old", never shown as current (0029).
4. Spot checks: a fixed set of postcodes is compared with the official sites on a schedule, by hand first and by script where the site allows; "Report a problem" adds a signal.
5. AI cannot invent numbers: every number in a chat answer must appear in the tool results it was given, or the answer is rejected; the evaluation set tests attempts to make it guess.

**The 3D map and the area card**
1. Drawn only from data: positions from coordinates at one fixed scale, never placed by hand.
2. A map-matches-list test: every listed place is drawn at its listed distance within 2%, in list order, or named "off the map" (the check that caught the canvas maps' mismatch on 13 Nov 2026).
3. Honest labels: building heights "approximate"; no flood or crime shading (0046); the list is the source of truth and the accessible version.
4. Screenshot tests catch a map that changes silently between versions.

## Countries support different things
The founder, typed: "this should inform us on how to set up our model as different countries will support different things". England is the only country at launch ("keep it out of the pilot"), but the pilot's data contract (DA-03, BE-02) is built so that adding a country is a data job, not a rewrite (the agent's proposal, approved by the founder in a prompt window, "Approve (Recommended)", 13 Nov 2026):
- **A coverage registry:** for each country (and region where it varies), which topics exist, the source for each, its licence and its geographic level. Screens and tools read the topic list from it, never from a hard-coded list.
- **A location scheme per country:** the UK postcode now; others later (for example Nigeria's 11-character building-level NIPOST code), each with its own format check and privacy rule.
- **Every topic answer carries its geographic level** (street, council area, state), so a coarse figure is never shown as if it described the street.
- **A privacy profile per country:** which notice applies and what may be stored.
- Units, currency and language come from the country entry.
Research on Nigeria is in `docs/product/05-ideas-and-product-thinking.md`.

## Answers to the builder check (13 Nov 2026)
A fresh reviewer read this design as its builder. Its questions, settled:
1. **Scope and timing (agent's call).** This design covers the AI layer and the pilot extras on top of the stage 5b area check; it does not plan the data layer. The data layer (DA-03 database, DA-04 ingestion and caching, DA-05 licences, DA-06 postcode lookup, BE-02 API contract, IN-01 to IN-05) is 0046's own plan and comes first; the area tools read only from our cached copies, never live from the sources on a visitor's request. Timing: stage 5b, built before the home workspace (decision 0052, pilot-only gate). The home-level MCP tools specified in `mcp-tools.feature` (#117, stage 6) stay; the area tools sit alongside them.
2. **AI provider retention** (founder, 13 Nov 2026, asked in a prompt window: "No training, short checks OK (Recommended)"). The provider's standard business terms are accepted if inputs are never used for training and are kept only briefly for abuse checks; the privacy notice states the provider and how long, and the chat says "Don't type personal details". Zero retention is not required. The exact terms are confirmed for the chosen provider under AI-01 before launch.
3. **What blocks launch (agent's call).** Every safeguard in Constraints blocks launch. Each extra (wave 1 and wave 2) sits behind its own switch and is left out at launch if its source fails the DA-05 licence or terms check; launch never waits for an extra.
4. **Hosting (agent's call, final under IN-02).** Designed for Cloudflare in front of the API, the MCP server and the chat, since the domains are already there: its bot check, rate rules and log settings. The rate limits and the daily AI spend counter live in one shared store, not per instance, holding only anonymised keys with a short expiry (0014: raw IP addresses in memory only). If IN-02 picks otherwise, those three controls are re-checked before launch.
5. **MCP distribution and limits (agent's call).** At launch the server is a URL people add as a custom connector; no directory submission (ChatGPT apps, Claude connectors) until after the pilot, because those bring review and possibly sign-in requirements. Calls from ChatGPT and Claude arrive from those companies' servers, so limits are a global cap plus a per-host cap; the sources are protected anyway, because the tools read only our cached copies.
6. **Sold prices (agent's call).** Individual recorded sales only, each with its date, as Price Paid publishes them, the address shown only beside its price (the licence's limit); no medians, averages or other summaries in the pilot, since any calculated figure needs a tested engine module (rule 2).
7. **Compare two postcodes (agent's call).** A page feature only; the chat and the MCP tools stay one postcode at a time, and the comparison shows the two areas' sourced facts side by side with no calculated differences.
8. **Questions to ask (agent's call).** `questions_for_gaps` is rule-based templates built from each gap, with no AI model, so MCP calls cost no AI money.

## Left to the builder
An "Ask about this area" entry in the information architecture (`.design/prototype/INFORMATION_ARCHITECTURE.md`, which has only "Ask about this home"), added by the pilot specs; tool names and exact signatures, prompt wording within the rules above, the chat panel's layout (an optional, closable panel per 0004), widget design, rate-limit numbers within the caps, and which wave 2 extras fit before launch.
