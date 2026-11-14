# Information Architecture: Vestagraph clickable prototype

**Phase 3 of the design flow, 11 Nov 2026.** Built on `DESIGN_BRIEF.md`, doc 03 §3 (navigation and glossary), §4 (stories) and §5 (screens and required states), and the fixtures in `packages/fixtures/data/` (`snapshot.json`: two stories, four steps each, snapshot date 23 Oct 2026). There's no app code yet; the Next.js App Router routes below are the target structure (FE-01, #73).

**Founder decisions (11 Nov 2026):**
- **My move is the main view** (the 80% screen).
- Story steps are moved through with a **labelled demo timeline**.
- Addresses are **readable, with the step in the URL**.
- The assistant is a **contextual "Ask about this home"** inside each home, not a top-level tab.

**Maximum depth:** three levels (My move → home → tab), with detail opening as a sheet or a sub-page.

## Site Map

- **Public site at launch** (stage 5b, decision 0046)
  - Landing `/`: search first, with the area check as the main action (see Landing below).
  - Check an area `/area#postcode=…`: postcode in, the Nearby topic summary out (without the commute row, which needs the household's own destination), with Summary and Map views and a download with sources. Saving a home appears only in a "Coming next · not available yet" panel until accounts exist (no active button). No account to use it. The map pin is labelled **Postcode centre**; address pins are only for homes the user has chosen. **The postcode goes in the URL fragment, never the query string**, so it never reaches server, application or hosting logs (0014); on live data the API call sends it in the request body (POST), never in a query string or URL path. The first public page (decision 0046, accepted); in the prototype it runs on sample data.
    - **Form:** a persistent "Postcode" label, hint text under it ("For example, NB1 4XY"; no placeholder, following the GOV.UK text-input guidance), and a "Check postcode" button.
    - **States:**
      - loading: a skeleton per topic, never empty rows;
      - invalid format: an inline message, and nothing is searched until the postcode is complete;
      - **postcode not found** (well-formed but unknown or terminated): "We couldn't find that postcode", with nothing else shown (no empty topics, which would look like a clean result, rule 7);
      - outside England: per-topic coverage (#158); until then a "Not yet covered" card;
      - our stored copy of a source is missing or failed (corrected 14 Nov 2026, C3: the pilot reads only our stored copies, never a source live, so asking again changes nothing until our next refresh): that topic shows the decision 0029 label **"Unavailable"** with "We don't hold a current copy of this source", a general line ("This doesn't mean there's nothing to report"; the flood topic says "This is not the same as no warning") and an official link where one exists, with **no "Try again"**; the other topics still show;
      - the visitor's own request to us fails (network, or our API down): "Couldn't load this · Try again". This is a different state and is never shown as "not found" or as an empty result;
      - **flood warnings** (register line DA-12): refreshed every 15 minutes; the flood row always reads "Warnings in force when we last checked, at <time>" with the official flood-warning link first, never the word "live"; labelled "Old" when our copy is over 1 hour old and "Unavailable" when over 1 day old. The Environment Agency says its data updates every 15 minutes, gives no service guarantee and is not for safety-critical use; the 1 hour and 1 day limits are the founder's accepted default, not an Environment Agency rule.
    - **Export** ("Print or save as PDF"): a print-ready page made **in the browser** from the results on screen, which the visitor saves as PDF from the print dialog, so the postcode never goes back to the server and no PDF package is needed (register FE-06). Designed for A4 (the sample runs to three pages). **To be redesigned (FE-21, 13 Nov 2026):** a designed report with an isometric cover map, an "At a glance" page, topic pages and a sources page; the flat numbered map below stays inside the report. The contents below stand until the design pass updates them (to update with the report spec, FE-21: the report's contents, M8). Contents:
      - a header with "Sample data" for the example postcode only, or the made-at time for any other postcode (corrected 14 Nov 2026, C5: real postcodes are real data);
      - a **flat 2D map** whose numbered pins match the table rows (3D distorts distance and hides pins on paper);
      - every topic with its facts, gaps, source, data date, its decision 0029 label (Cached with when it was fetched, Fallback, Old or Unavailable; "Live" is reserved for a later live adapter, since the pilot reads only stored copies, C4) and its limits (on paper they are collected on a closing "How we got this" page, since there is nothing to open, FE-34). An Unavailable or Not yet covered topic prints as such and is never left out;
      - crime as a counts table only;
      - the attribution each licence requires;
      - a privacy line. Its wording ("made in your browser; Vestagraph didn't store your search") is **provisional**: it is checked against the privacy notice once SE-02 parts 1 and 2 settle logs, including the map-tile host's access logs (#85).
      - A later option: an "Include 3D view" tick box adding a small 3D picture.
  - How it works `/how-it-works`
  - About the data `/about-the-data`: every source, its date, coverage, limits and attribution.
  - Privacy notice `/privacy` and accessibility statement `/accessibility`: live before launch (0014, 0046).
  - Account features appear only as "coming next" until they are live.
- **Prototype only** (private, decision 0045)
  - Example home `/example`: choose the buyer or renter example, then go to My move in that story.
  - Costs and comparison `/costs-and-comparison`: explains what Vestagraph works out and what it doesn't.
  - Sign in `/sign-in`: simulated, labelled as such.
- **Check a home**
  - Choose buying or renting, then search the address `/check`
  - Confirm the exact home `/check/confirm?q=…`: matching units, a map pin, or "can't find it" (manual entry).
  - Not yet covered `/check/not-covered?q=…`: Wales, Scotland or Northern Ireland (WALES-1), with an illustration.
- **My move** `/move?story=buyer&step=1`: the main view across every home.
  - Homes list `/homes`: every home record. On a phone this is the same content as My move, grouped.
  - Compare `/compare?homes=flat-2-14-mill-court,9-orchard-row&step=1`: up to three homes.
- **Home record** `/homes/[home-slug]?step=n`
  - Overview `/homes/[home-slug]` (the default tab)
  - Nearby `/homes/[home-slug]/nearby` (list, the default)
    - Map view `…/nearby?view=map&selected=[area-item-id]`
  - Costs `/homes/[home-slug]/costs`
    - The working behind a category opens in a sheet: `…/costs?line=[figure-id]`
  - Viewings `/homes/[home-slug]/viewings`
    - A viewing note `…/viewings/[note-id]`
  - Questions `/homes/[home-slug]/questions`
    - Question detail `…/questions/[question-slug]`
    - Reply check `…/questions/[question-slug]/reply/[reply-slug]`
  - Documents `/homes/[home-slug]/documents`
    - Document and findings `…/documents/[document-slug]` (switch between the original and the findings)
  - Activity `/homes/[home-slug]/activity`
  - What changed (the hero moment) `/homes/[home-slug]/what-changed?step=n`
  - Evidence sheet: an overlay on any home page, `?evidence=[evidence-id]`
  - Ask about this home: an overlay, `?ask=1` (designed and static in the prototype, #78)
- **Share or snapshot** `/homes/[home-slug]/share` (a preview of what's shared, plus permissions; simulated)
- **Account menu (utility)**
  - Settings `/settings`: theme (light, dark, system), household members (simulated)
  - Plan `/settings/plan`: Move pass, a labelled simulated boundary (doc 02 §8)

**Home slugs** come from the fixture addresses:
- `flat-2-14-mill-court` (B1)
- `9-orchard-row` (B2)
- `flat-5-3-station-road` (R1)
- `21-canal-street` (R2)
- `7-harbour-mews` (WALES-1, not yet covered)

## Navigation Model

- **Primary navigation:**
  - **Public site (0046):** How it works · About the data · Sign in (once accounts exist), with the postcode box as the primary action.
  - **Prototype only:** How it works · Example home · Costs and comparison · Sign in (simulated), plus **Check a home**.
  - **Signed in (simulated):** **My move · Homes · Compare**, plus a persistent **Check a home**. That's three items, which is the maximum.
- **Secondary navigation (inside a home):** tabs, Overview · Nearby · Costs · Viewings · Questions · Documents · Activity. Detail opens from the fact or finding that raised it (an evidence sheet, a question, the working behind a line).
- **The example story timeline (demo control):**
  - A slim bar on My move, on every page of an example home, and on Compare: **"Example story · Demo: Step 1 · 2 · 3 · 4"**. Each step shows a one-line caption from `snapshot.json`, for example "Offer accepted; the conveyancer receives the management pack".
  - Moving forward sets `?step=n` everywhere.
  - When a step changes a figure or a status, a "What changed" link appears.
  - It's visibly a demo control: never part of the product's own chrome, and never on non-example homes.
- **Utility navigation:**
  - an account menu (settings, theme, plan, sign out);
  - a "Sample data" label on every example screen;
  - **Ask about this home**, a contextual entry inside a home (sheet or side panel).
  - **Ask about this area** (pilot, decision 0051), on Check an area only (the landing has no result; C6, 14 Nov 2026): an optional, closable panel (a drawer over the right column on desktop, a bottom sheet on a phone; see "Layering" below) with an "AI" badge on the entry (FE-13); spec `docs/specs/pilot/area-chat.feature`.
- **Mobile navigation:**
  - **App level:** bottom tabs **My move · Homes · Compare**, plus a floating **Check a home** action.
  - **Inside a home:** a compact home header and a bottom bar of **Overview · Nearby · Costs · Questions**. A labelled **More** menu holds Viewings (one tap away during a visit), Documents and Activity (doc 03 §3).
  - The demo timeline sits under the header and collapses to "Step 3 of 4".

## Content Hierarchy

### My move (the main view; perfect it first)
0. **One next step,** above the cards: the first item from "Needs your attention" in a fixed order (replies to check, then missing cost lines, then questions not yet sent, then documents to review), naming its home, e.g. "Flat 2, 14 Mill Court: add a buildings insurance figure or ask the agent". No score or urgency styling.
1. **Your homes, each as a calm summary card**, in the order the household added them.
   - Each card shows:
     - a photo;
     - the address;
     - buying or renting;
     - the **monthly cost so far** (hero figure from the engine, with its "partial" label);
     - the budget line;
     - a one-line daily-life note ("Commute: your estimate 36 min · limit 40 min");
     - **open questions** (count and the most important one);
     - **what changed** since the last step.
   - This comes first because it answers "where are we with each home?" at a glance.
2. **Needs your attention:** replies to check, missing cost lines, questions not yet sent and documents to review (the order the next step uses). These are the next useful actions across all homes (doc 03 §5, "My move / activity"); no score or urgency styling.
3. **Compare:** a prominent "Compare these homes" link once there are two or more.
4. **Recent activity:** a short timeline with dates (step captions in the demo).
5. Below the fold: the dated decision snapshot (share) and the household members (simulated).

### Home overview
1. **The home:** photo, address, unit, tenure, mode and the sample-data label. Recognition first.
2. **Real cost so far:** the hero monthly figure, partial and budget lines, then upfront cash as one line. Links to Costs.
3. **What matters here:** up to three findings with source and scope labels (doc 03 §5), for example "Service charge: the listing says £2,400 a year; the management pack hasn't arrived".
4. **Daily life:** a three-line summary (commute against your limit, nearest stop, the count of gaps) with no score. Links to Nearby.
5. **Open questions:** each one's status, plus the next action.
6. **What changed:** shown when a step changed something.
7. Below: evidence gaps, documents received and the activity preview.

### Nearby (summary first; the map is equal)
The page opens as **one row per topic with its headline fact** (founder review, 11 Nov 2026: the full list was about four phone screens long). Tapping a topic opens its detail as a **bottom sheet on a phone and a side panel on desktop, never a separate page** (register line FE-20; corrected 14 Nov 2026, C1); the open topic is linkable through the `#` part (on Check an area, the same fragment as the postcode). The detail has the full list, List and Map views, the source line and "How we got this", which holds the topic's limits (FE-34). The same summary, without the commute row, is the public Check an area page. Topic order:
1. **Your commute:** your estimate next to your limit, with no verdict until the engine produces one (#147).
2. **Getting around:** stops, with straight-line distances.
3. **Everyday places:** supermarket or shop, park, healthcare, police station and childcare, with gaps shown.
4. **Places of worship** (PD-13), its own topic: the nearest places of every faith recorded in the source, by distance; never counts or an area's religious makeup. In the fixtures it is the `place-of-worship` amenity subtype.
5. **Schools,** with framework and date.
6. **Flood:** warnings in force when we last checked, with the time and the official link first (DA-12), plus the long-term link.
7. **Recorded crime:** counts by month and category; never on the map.
8. **Sold nearby:** history, not a valuation.
9. **Planning nearby** and **broadband.**

Limits (register line FE-34, 14 Nov 2026, replacing FE-28): there is **no visible limit line** on the landing cards, the rows or the top of a topic's sheet or panel. Each topic's limits sit inside its **"How we got this"** (FE-24; closed by default, reachable by keyboard) and on About the data. A missing value is still said on the row, never zero (rule 7).

#### Layering (register line FE-26, founder, 14 Nov 2026: "one at a time")
One rule for what shows where; the feature files point here (CHAT-06, CHAT-38, CARD-22).
- **Desktop:** the topic list is on the left. The right column is the map until a topic opens, then that topic's side panel (with its own small map) replaces it. The area chat opens as a drawer over the right column; closing it returns to what was there.
- **Phone:** one sheet at a time. Opening the chat from inside a topic replaces the topic sheet, and Back returns to it.
- The card's Expand or Open map view is the chat's own answer, so it may sit above the chat; closing it returns to the chat.

Each topic detail ends with its source line. On a phone the map is a view inside each topic; on desktop it is a sticky column beside the list, with the selection kept in sync. The map has category filters, a legend, a hover card (desktop) or tap card (phone), and an optional 3D switch.

### Costs
1. **The monthly hero figure,** with the partial label and what's missing named.
2. **The budget line** from the engine.
3. **The cost bar:** one segment per line from the engine's figures, with a fixed-width dashed "?" slot for each missing or not-calculated line.
4. **The receipt** (founder, 11 Nov 2026; replaces the category cards): one line per cost with its figure from the engine, a numbered source key underneath, and missing or not-calculated lines named in place, never pushed out of sight and never £0. It ends with the engine's "Total so far" with its Partial tag and a "?" for each line not included.
5. **Upfront cash,** a separate section with its own total.
6. **"How this was worked out"** in a disclosure.
7. **Assumptions you can edit,** with any change recorded as the user's own.

### What changed (the hero moment)
1. **One sentence of what changed and why,** with its source, for example "The management pack shows £3,720 a year, not £2,400".
2. **Before and after:** the old and new monthly figures side by side, with the changed line highlighted. Both figures come from the engine. **The "Before" label names the event that caused the change:** "Before you confirmed" when the change came from the user's confirmation (step 4 in both stories); "Before the management pack arrived" for a change a document brought (buyer step 3). Earlier changes are listed with a link to the full history.
3. **What it means for you:** the budget line before and after, and the effect on the comparison.
4. **Who confirmed it and what was checked:** an attributed confirmation.
5. **Still open:** questions and partial items that remain.

### Compare
1. The homes being compared (up to three), as headers with photo and address.
2. **Each month:** the totals with their partial labels, then the budget lines, then the category rows aligned.
3. **Daily life:** commute, stops, everyday places, flood and the latest sale, aligned with gaps visible.
4. **Upfront.**
5. No winner, no highlighted "best" cell, and no totals the engine didn't produce.

### Question detail and reply check
1. The question, its recipient role and its status.
2. The evidence that raised it.
3. Replies, each with its source and date.
4. **What's still uncertain.**
5. The confirm action, explicit and attributed.

### Landing (search first, decision 0046)
1. The promise in a Bricolage Grotesque headline, with the **postcode box** (persistent label, hint text, "Check postcode", "Try an example") as the main action. "England only for now" sits under it.
2. A hero visual: the sample 3D map as a **static image** with a "Postcode centre" pin, a 400 m ring, crafted category pins (FE-08) and a compact summary card on the map (the four nearest places and "+3 more nearby"), placed where no pin is under it. Its places, distances and count come from the postcode-level sample fixture (B6a), never typed by hand.
3. **Data from:** a source wall: one card per source shown in About the data (planned: Environment Agency, covering "Flood warnings and flood risk by postcode" (DA-16), police.uk, HM Land Registry, Department for Education, Ofsted, NaPTAN, OpenStreetMap, Ofcom, Planning Data, and, added 14 Nov 2026, MHCLG (neighbourhood deprivation rank, English Indices of Deprivation 2025, decision 0054), Department for Transport (transport connectivity, 0054), Natural England (access to green space, DA-16) and the Office for National Statistics (housing affordability by council, DA-16); the final list follows DA-05), with each source and what it covers, and no limit line (FE-34); names only, no logos; links to About the data.
4. **How it works:** three illustrated steps (type a postcode, see what's around, print or save), followed by a full-width photo band (an AI-generated terraced street; honest alt text, footer note).
5. **How to read a result:** a Schools card from the sample data, labelled Sample, with four numbered callouts (distance, inspection date, source, how we got this).
6. **Honest by design:** four illustrated rules, each with a sample snippet: sources and dates; missing shown as missing; we measure, never "safe"; crime as counts, never on the map.
7. **Coming next, with a free account** (labelled "not available yet" until live): cost estimate, compare, track questions and answers per home. White panel with a slate outline in light; neutral panel with a slate outline in dark.
8. **Questions:** a short FAQ beside a photo (kitchen table; honest alt text, footer note).
9. Footer: How it works, About the data, Privacy, Accessibility.
In the private prototype the landing can also link the two example homes; the public landing doesn't until 0045 is revisited.

## User Flows

### Explore an example (the main showcase, private prototype)
1. The user opens `/example` and sees two example homes.
2. They choose **"See the buying example"** (or renting).
3. **My move** opens at the **Buyer story, step 1**, showing B1 and B2 cards with their costs so far and open questions.
4. They open B1, then its Overview, Costs and Nearby.
5. They press **Step 2** on the demo timeline. The B1 card shows "Reply received: partially answered", and the reply check shows that it gives no figure.
6. **Step 3:** the management pack arrives, and the documents and findings appear.
7. **Step 4:** the user confirms the budget. **What changed** opens with the before and after, explained. The card on My move now shows the new total and "£48.37 over budget before maintenance (not calculated)" (from the engine, `B1.from-step-4.monthly.budget`, a partial total).
8. **Compare** shows B1 and B2 aligned, with no winner.

### Check a home
1. `/check`: choose **Buying** or **Renting**, then type an address.
2. Matching units are listed.
   - **If one unit is clearly theirs:** they select it.
   - **If the postcode matches several flats** (B1 matches six): they must pick the exact flat. Nothing is guessed silently.
   - **If it can't be found:** they drop a pin on the map (founder choice) or enter the address manually.
   - **If the address is in Wales, Scotland or Northern Ireland:** a "Not yet covered" page with an illustration and no partial or empty results.
3. The home Overview opens with its evidence gaps visible, and the home card is added to My move.

### Ask a question, then check the reply
1. A finding or a missing cost (a receipt line on Costs, a card elsewhere) shows **Ask about this**.
2. The question draft is pre-filled from the evidence, with the recipient role.
3. The user copies or exports it, then **records it as sent**. This is labelled as a simulated action.
4. When a reply arrives (a demo step), it shows on My move under "Needs your attention".
5. The reply check shows the reply, its source and what's still uncertain.
   - **If it's partial:** the status stays "Partially answered" and nothing changes.
   - **If it's specific:** the user confirms it explicitly, and **What changed** opens if a figure changed.

### Look around the area
1. The user opens Nearby, which is a list.
2. They tap the map preview, and a full-screen map with a bottom sheet opens (desktop shows a split view).
3. Selecting a stop highlights it in both the list and the map.
4. Crime and flood stay in the list only (FE-25: except the pilot flood topic's own flat map).
5. Gaps ("no record in this source") are visible in the list.

### Compare homes
1. From My move or a home, the user chooses **Compare**.
2. They pick up to three homes.
3. The aligned view opens at the current story step.
4. On a phone, it shows one card per topic; they swipe between the homes.

## Naming Conventions

| Concept | Label in UI | Notes |
|---|---|---|
| Product | Vestagraph | Decision 0044 |
| The household's space | My move | Doc 03 glossary |
| Everything about one home | Home (the "home record" internally) | Users never see "record" or "passport" |
| Summary tab | Overview | |
| Daily-life context | Nearby | |
| Monthly and upfront figures | Costs. The hero figure is labelled "each month" | |
| An incomplete total | "so far", plus a "Partial" tag naming what's missing | Never "estimate" alone |
| Unknown cost line | "Missing" (always with "not £0") | Rule 7 |
| Line the engine doesn't calculate | "Not calculated" | |
| No data in a source | "No record in this source" | Plus "this doesn't mean there are none" |
| Out-of-date item | "Old" | Shows the date |
| No current stored copy of a source | "Unavailable" (decision 0029 label) | With "We don't hold a current copy of this source", the official link and "This doesn't mean there's nothing to report"; no Try again in the pilot (C3) |
| The visitor's request to us failed | "Couldn't load this" | With "Try again" (C3) |
| Nothing found in a radius | "No <place> found within <radius>" | Never "none" or zero |
| Flood warnings | "Warnings in force when we last checked, at <time>" | Official link first; "Old" over 1 hour, "Unavailable" over 1 day (DA-12) |
| Distances (England) | Under 1 mile: metres to the nearest 10 m ("120 m", "1,450 m"); from 1 mile: miles to one decimal ("1.3 miles"); crime "within 1 mile" | Stored in metres; display follows the country (FE-27) |
| Wales, Scotland, Northern Ireland | "Not yet covered" | Per topic once #158 lands |
| Postcode not found | "We couldn't find that postcode" | Nothing else shown |
| Question states | To ask · Sent · Partially answered · Reply needs checking · Answered | Fixture statuses |
| A change after confirmation | What changed | The hero moment |
| Source of a fact | Source | Origin, date and coverage |
| Supporting document | Document | |
| Demo story control | Example story · Demo | Never "simulation" in product copy |
| Sample data marker | Sample data | Everywhere fixtures are shown |
| Assistant entry | Ask about this home | No "Copilot", no "AI" badge |
| Area assistant entry (pilot) | Ask about this area | "AI" badge on the entry and "Answers are written by AI from the sources below" in the header (FE-13); no "Copilot" |
| Paid tier (simulated) | Move pass | A labelled hypothesis, doc 02 §8 |
| Forbidden labels | — | Never "verified", "safe", "approved", scores or "best" (rule 4) |

## Component Reuse Map

| Component | Used on | Behaviour differences |
|---|---|---|
| Public layout (header and footer) | Landing, Check an area, How it works, About the data, Privacy, Accessibility; in the prototype also Example, Costs and comparison, Sign in | Editorial: more space, Bricolage Grotesque display |
| App layout (top bar on desktop, bottom tabs on mobile) | My move, Homes, Compare, Settings | — |
| Home layout (home header, tabs or bottom bar, demo timeline) | Every home page | Collapses on scroll on a phone |
| Demo story timeline | My move, home pages, Compare (example homes only) | Hidden on non-example homes |
| Hero figure | My move cards (compact), Overview, Costs, What changed (before and after), Compare headers | Sizes: compact, standard, hero |
| Cost category card and receipt line | Costs (as receipt lines), What changed (the highlighted line), home cards on My move and Homes | Status variants |
| Status tag and source line | Everywhere data appears | One pattern |
| Gap card | Nearby, Costs, Compare, Overview | — |
| Sheet (bottom sheet on mobile, side panel on desktop) | Evidence, cost working, map selection, Ask about this home | Full-screen on a phone for evidence |
| Home summary card | My move, Homes, Compare picker | Compact and full variants |
| Empty state with illustration | Homes (none yet), Questions (none), Not yet covered | Isometric illustration |

## Content Growth Plan

- **Homes:** a household may add many. My move lists them in the order added, with archive ("No longer considering") as the growth pattern. Compare is capped at three.
- **Questions, replies, documents and viewing notes** grow per home. Each list is filtered by status, with the newest first, and a filter appears once there are more than about eight.
- **Activity** is a dated timeline that loads in pages.
- **Area items** are fixed per home in the prototype. With real data (stage 6, #98) they grow by category, and sections collapse to the nearest three items with "Show all".

## URL Strategy

- **Pattern:** `/section/[slug]/tab/[item-slug]`, in lower case with hyphens.
- **Slugs:** readable and derived from the address; IDs stay internal. Question and document slugs come from their fixture IDs in lower case.
- **Query parameters:**
  - `step=1..4`: the example story step. It's on every example screen, so any screen at any step can be linked and tested (the playwright-bdd `@ui` scenarios use it, decision 0049).
  - `story=buyer|renter`: on My move.
  - `homes=a,b,c`: on Compare (at most three).
  - `view=list|map` and `selected=[area-item-id]`: on Nearby.
  - `evidence=[evidence-id]`, `line=[figure-id]` and `ask=1`: open sheets.
- **Sharing:** shared views exclude personal location and the dropped pin (from the engineering note).
