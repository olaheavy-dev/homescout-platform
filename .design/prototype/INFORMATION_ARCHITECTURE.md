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
  - Check an area `/area#postcode=…`: postcode in, the Nearby topic summary out (without the commute row, which needs the household's own destination), with Summary and Map views, a download with sources, and "Save a home here" (needs an account). No account to use it. **The postcode goes in the URL fragment, never the query string**, so it never reaches server, application or hosting logs (0014); on live data the API call sends it in the request body (POST), never in a query string or URL path. The first public page (decision 0046, accepted); in the prototype it runs on sample data.
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
- **Mobile navigation:**
  - **App level:** bottom tabs **My move · Homes · Compare**, plus a floating **Check a home** action.
  - **Inside a home:** a compact home header and a bottom bar of **Overview · Nearby · Costs · Questions**. A labelled **More** menu holds Viewings (one tap away during a visit), Documents and Activity (doc 03 §3).
  - The demo timeline sits under the header and collapses to "Step 3 of 4".

## Content Hierarchy

### My move (the main view; perfect it first)
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
2. **Needs your attention:** replies to check, documents to review and questions not yet sent. These are the next useful actions across all homes (doc 03 §5, "My move / activity"); no score or urgency styling.
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
The page opens as **one row per topic with its headline fact** (founder review, 11 Nov 2026: the full list was about four phone screens long). Tapping a topic opens its detail `/homes/[slug]/nearby/[topic]` with the full list, List and Map views, the source line and "What this doesn't tell you". The same summary, without the commute row, is the public Check an area page. Topic order:
1. **Your commute:** your estimate next to your limit, with no verdict until the engine produces one (#147).
2. **Getting around:** stops, with straight-line distances.
3. **Everyday places:** supermarket or shop, park, healthcare, police station and childcare, with gaps shown.
4. **Schools,** with framework and date.
5. **Flood:** live warnings, plus the long-term link.
6. **Recorded crime:** counts by month and category; never on the map.
7. **Sold nearby:** history, not a valuation.
8. **Planning nearby** and **broadband.**

Each topic detail ends with its source line. On a phone the map is a view inside each topic; on desktop it is a sticky column beside the list, with the selection kept in sync. The map has category filters, a legend, a hover card (desktop) or tap card (phone), and an optional 3D switch.

### Costs
1. **The monthly hero figure,** with the partial label and what's missing named.
2. **The budget line** from the engine.
3. **Category cards** (founder choice): calculated, then included, then missing or not calculated. Missing cards are never pushed out of sight.
4. **Upfront cash,** a separate section with its own total.
5. **"How this was worked out"** in a disclosure.
6. **Assumptions you can edit,** with any change recorded as the user's own.

### What changed (the hero moment)
1. **One sentence of what changed and why,** with its source, for example "The management pack shows £3,720 a year, not £2,400".
2. **Before and after:** the old and new monthly figures side by side, with the changed line highlighted. Both figures come from the engine.
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
1. The promise in a serif headline, with the **postcode box** as the main action. "England only for now" sits under it.
2. A hero visual: the sample 3D map with a topic summary card.
3. **What you'll see:** getting around and everyday places; schools with framework and date; flood and recorded crime, honestly labelled.
4. **Honest by design:** sources and dates on every fact; missing shown as missing; never "safe" or "verified"; crime as counts, never on the map.
5. **Coming next, with a free account** (clay tint, labelled "not available yet" until live): cost estimate, compare, questions.
6. Footer: How it works, About the data, Privacy, Accessibility.
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
1. A finding or a missing cost card shows **Ask about this**.
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
4. Crime and flood stay in the list only.
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
| Failed fetch | "Couldn't fetch" | With "Try again" |
| Wales, Scotland, Northern Ireland | "Not yet covered" | |
| Question states | To ask · Sent · Partially answered · Reply needs checking · Answered | Fixture statuses |
| A change after confirmation | What changed | The hero moment |
| Source of a fact | Source | Origin, date and coverage |
| Supporting document | Document | |
| Demo story control | Example story · Demo | Never "simulation" in product copy |
| Sample data marker | Sample data | Everywhere fixtures are shown |
| Assistant entry | Ask about this home | No "Copilot", no "AI" badge |
| Paid tier (simulated) | Move pass | A labelled hypothesis, doc 02 §8 |
| Forbidden labels | — | Never "verified", "safe", "approved", scores or "best" (rule 4) |

## Component Reuse Map

| Component | Used on | Behaviour differences |
|---|---|---|
| Public layout (header and footer) | Landing, Check an area, How it works, About the data, Privacy, Accessibility; in the prototype also Example, Costs and comparison, Sign in | Editorial: more space, serif display |
| App layout (top bar on desktop, bottom tabs on mobile) | My move, Homes, Compare, Settings | — |
| Home layout (home header, tabs or bottom bar, demo timeline) | Every home page | Collapses on scroll on a phone |
| Demo story timeline | My move, home pages, Compare (example homes only) | Hidden on non-example homes |
| Hero figure | My move cards (compact), Overview, Costs, What changed (before and after), Compare headers | Sizes: compact, standard, hero |
| Cost category card | Costs, What changed (the highlighted line) | Status variants |
| Status tag and source line | Everywhere data appears | One pattern |
| Gap card | Nearby, Costs, Compare, Overview | — |
| Sheet (bottom sheet on mobile, side panel on desktop) | Evidence, cost working, map selection, Ask about this home | Full-screen on a phone for evidence |
| Home summary card | My move, Homes, Compare picker | Compact and full variants |
| Empty state with illustration | Homes (none yet), Questions (none), Not yet covered | Textured editorial illustration |

## Content Growth Plan

- **Homes:** a household may add many. My move lists them in the order added, with archive ("No longer considering") as the growth pattern. Compare is capped at three.
- **Questions, replies, documents and viewing notes** grow per home. Each list is filtered by status, with the newest first, and a filter appears once there are more than about eight.
- **Activity** is a dated timeline that loads in pages.
- **Area items** are fixed per home in the prototype. With real data (stage 6, #98) they grow by category, and sections collapse to the nearest three items with "Show all".

## URL Strategy

- **Pattern:** `/section/[slug]/tab/[item-slug]`, in lower case with hyphens.
- **Slugs:** readable and derived from the address; IDs stay internal. Question and document slugs come from their fixture IDs in lower case.
- **Query parameters:**
  - `step=1..4`: the example story step. It's on every example screen, so any screen at any step can be linked and tested (Reqnroll and Playwright `@ui` scenarios use it).
  - `story=buyer|renter`: on My move.
  - `homes=a,b,c`: on Compare (at most three).
  - `view=list|map` and `selected=[area-item-id]`: on Nearby.
  - `evidence=[evidence-id]`, `line=[figure-id]` and `ask=1`: open sheets.
- **Sharing:** shared views exclude personal location and the dropped pin (from the engineering note).
