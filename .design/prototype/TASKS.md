# Build Tasks: Vestagraph clickable prototype

Generated from: `.design/prototype/DESIGN_BRIEF.md`, `INFORMATION_ARCHITECTURE.md` and `tokens.css`
Date: 11 Nov 2026 (phase 5 of the design flow)

**How this list is used:**
- Phase 6 of the design flow works through **H1–H7** now, as high-fidelity design frames on the design canvas, so the founder confirms the visual direction before any app code exists (stage 4 #79, high-fidelity key screens).
- The rest is the **stage 5 build order** for the coding agents. At #71 ("brief to issues") each build task becomes or refines a GitHub issue. Story slices are one ticket per story step (SP-02).
- Every figure comes from `costs.json` by figure ID, and every input and area item from the fixtures (rule 2). Behaviour is proved by the Gherkin specs in `docs/specs/` (decision 0043).

**Existing code:** none on the frontend. Every component below is new. Tokens: `.design/prototype/tokens.css`, which becomes the app's token file in B1.

## High-fidelity design (phase 6 now, on the canvas)
- [ ] **H1 My move on a phone, buyer story step 1 (light):** the main view, which establishes the **Scandinavian + Editorial** direction for everything after it.
  - It shows Bricolage Grotesque titles, Geist tabular figures, one next-step row naming its home, then B1 and B2 summary cards (photo, address, monthly cost so far with its partial label, the budget line, the commute line, open questions).
  - Below them come "Needs your attention" and the bottom tabs; the slate-tinted demo strip sits after the headline summary.
  - **Done:** the founder agrees it no longer "looks made by AI". _New: home summary card, hero figure (compact), demo timeline, bottom tabs._
- [ ] **H2 What changed, buyer step 4 (phone and desktop):** the hero moment.
  - One sentence of why, with its source; old and new figures side by side ("Before you confirmed" and "Now") with the changed service-charge line highlighted; the budget line before and after; the earlier change (insurance) with a history link; the attributed confirmation; what's still open.
  - **Done:** it reads in 5 seconds and nothing animates the figures. _New: decision-impact layout, cost category card (highlighted)._ _Risk first._
- [ ] **H3 Costs and Nearby on a phone, B1 step 1:**
  - The hero figure with category cards (calculated, missing "not £0", not calculated) and upfront cash separate.
  - Nearby list-first: commute, getting around, everyday places with a childcare gap card, schools with framework and date, the flood panel, the crime counts table, sold nearby, and a sage-tinted daily-life section.

  _New: category cards, gap card, status tag and source line, Nearby rows, crime table, flood panel._
  - **Round 2 (founder, 11 Nov 2026):** Nearby is summary first, one row per topic, with a topic detail (Schools) holding List and Map. The long list stays in the detail screens.
- [ ] **H4 Desktop split and dark theme:**
  - (Nearby desktop moved to H6, the immersive map with a floating list; the earlier 2D split frame was removed.)
  - Compare with B1 and B2 aligned and no winner.
  - H1 repeated in the near-neutral charcoal dark theme.

  _Depends on: H1–H3._
- [ ] **H6 Immersive map** (founder, 11 Nov 2026): a 3D switch (tilt and approximate building heights), category filters with icons, a legend, a hover card on desktop and a tap card on phones, all on the sample map. Crime and flood stay off the map.
- [ ] **H7 Public landing, desktop and phone** (decision 0046): search first, the sample 3D map with a summary card, and account features in a "Coming next · not available yet" panel. **Design passes 2 and 3 (11 Nov 2026):**
  - a labelled postcode box with hint text and "Not ready to type? Try an example";
  - a "Data from" strip with source names only (no logos, which could read as endorsement);
  - "How it works" as three illustrated steps;
  - "How to read a result": a Schools card from the sample data (labelled Sample) with four numbered callouts, replacing generic feature columns;
  - "Honest by design" as four illustrated cards, each with a sample snippet;
  - an illustrated "Coming next" panel and a short FAQ beside the brand mark;
  - no testimonials, counters, recent searches or pricing teaser (rule 1, decision 0014, PD-10).
- [ ] **Brand mark** (Lit doorway, D1 · Ruled light, the founder's choice on 13 Nov 2026; a single wider ruled line at 16 px still to try, the agent's suggestion): primary and compact marks, lockups in both themes and one colour, the app icon, the browser icon, and clear space. Trade-mark clearance (0009) and the asset register first.
- [ ] **H5 Check an area, public, phone** (decision 0046, accepted): postcode in, the Nearby topic summary out, Summary and Map, download with sources, and saving shown only as "Coming next". No commute row (it needs the household's own destination). States: loading, invalid format, postcode not found, outside England, one source unavailable (the frame shows three; loading and not found are added in the build).
- [ ] **H8 Area summary export** (designed for A4; the sample runs to three pages): made in the browser and saved from the print dialog ("Print or save as PDF"), a flat numbered map matching the tables, sources and limits on every topic, attribution and a privacy line. **To be redesigned (FE-21, 13 Nov 2026):** an isometric cover, an "At a glance" page, topic pages and a sources page, with the flat numbered map kept inside.

## Foundation (stage 5 build)
- [ ] **B1 App shell, tokens and the first screen** (#86):
  - the Next.js app (FE-01) loads `tokens.css`, Bricolage Grotesque and Geist, and the light and dark theme switch;
  - the public layout, app layout and home layout from the IA;
  - fixture types generated from the JSON Schemas;
  - My move rendered at `?story=buyer&step=1` exactly as H1.

  **Done:** H1 matches in the browser in both themes. _Philosophy: Scandinavian + Editorial. New layouts._
- [ ] **B2 Component gallery** (#150): every component from the brief's inventory in every state, light and dark, from fixture data, at `/gallery`. Axe passes in both themes. _Depends on: B1._
- [ ] **B3 Demo story timeline and step routing:** `?step=1..4` drives every example screen. The step captions come from `snapshot.json`, and "What changed" links appear when a step changes a figure. The playwright-bdd `@ui` scenarios (decision 0049) open any screen at any step. _Depends on: B1._
  - **One place for the demo strip:** on a phone, directly after the page's headline summary; on desktop, in the header. Step buttons are 44 px tall. Screens never mention step numbers outside the strip ("Before" and "Now", not "Step 3" and "Step 4").
  - **Shorter captions** (founder review of H1, 11 Nov 2026): update the step labels in `snapshot.json` to the shorter wording, e.g. step 1 "Listing costs added. Service charge question sent."
  - **Rules from the fourth design review (11 Nov 2026):**
    - the "Before" label on What changed names the event that caused the change: "Before you confirmed" for a user confirmation (step 4), "Before the management pack arrived" for buyer step 3;
    - My move shows **one next step** above the home cards, chosen by the fixed order in the IA and naming its home; the full "Needs your attention" list stays below.
  - **Wording rules from the third design review (11 Nov 2026):**
    - a partial total names what it excludes, with each gap's own status ("Excludes buildings insurance (missing) and maintenance (not calculated)"); "missing" and "not calculated" are never merged;
    - a budget margin on a partial total says "before those costs", never "left";
    - earlier changes on What changed (insurance: Missing → Included in service charge) are listed with a link to the full history;
    - Costs links to What changed whenever a figure has changed since the last step;
    - on a phone, the home tabs are Overview, Nearby, Costs, Questions and More (Viewings, Documents, Activity, What changed);
    - the public area check shows only area facts; building facts appear after a home is chosen.
  - **Link targets drawn in H1 and H2** (dead in the design frames; must work here):
    - "See what's missing" on a home card → that home's Costs, scrolled to its missing and not-calculated monthly lines (`/homes/[slug]/costs?step=n#missing`).
    - "See the 2026 budget" on What changed → the evidence sheet for that item (`?evidence=B1-SC-BUDGET`). The fixtures record no page number, so none is shown.
    - "Undo this confirmation" → restores the previous value and keeps both in the history.
    - Each demo step button → the same screen at that step.

## Core UI (stage 5)
**Order (decision 0046):** the area screens B6, B6a and B7 come first, right after B1 to B3; then B4, B5 and B8 onwards.

- [ ] **B4 Home overview** (all four example homes, step 1): the home header, the real cost so far, up to three findings with source labels, the daily-life summary, open questions and evidence gaps. _Reuses: hero figure, status tag._
- [ ] **B5 Costs:** hero figure, the cost bar, the monthly lines as a receipt with a numbered source key and every status, ending with the engine's "Total so far" with its Partial tag and "?" slots, upfront section, the "How this was worked out" disclosure, and editable assumptions recorded as the user's own. _Reuses: hero figure, cost bar, gap card._
- [ ] **B6 Nearby, list first:** every section from the IA (including places of worship, PD-13) with source lines and gap cards; limits inside each topic's "How we got this" and no visible limit line (FE-34, 14 Nov 2026, replacing the 11 Nov margin-note plan); crime and flood in the list only. _Depends on: area fixtures (merged in #145)._
- [ ] **B6a Check an area** (`/area#postcode=`, decision 0046; the postcode stays in the URL fragment so it never reaches a log): reuses the Nearby topic summary and topic details. Needs a postcode-level fixture (distances from the postcode centre) so the screen doesn't borrow one home's distances. Includes the states from the IA (loading, invalid format, postcode not found, outside England, one source unavailable) and the browser-made export (H8). Public pages never offer an account feature as an active control before it exists, and the map's centre pin is "Postcode centre". _Depends on: B6._
- [ ] **B7 Nearby map** (MapLibre, approved):
  - the drawn Northbridge sample map (#146);
  - one muted colour and one crafted icon per category (FE-08; tokens `--color-map-marker-*`), with the home or postcode-centre pin the only deep-forest pin; colour is never the only signal (icon, legend and list name too);
  - the bottom sheet (peek, half, full) on a phone and the split view on desktop;
  - selection kept in sync between list and map;
  - category filters, a legend, a hover card on desktop and a tap card on phones (name, type, straight-line distance, source, "Show in the list");
  - an optional 3D switch (pitch and building extrusion), off by default on phones and with reduced motion, plus a reset-to-north button;
  - map markers aren't tab stops.

  _Risk: canvas accessibility and performance budgets (research §4–5)._ _Depends on: #146._
- [ ] **B8 Compare:** up to three homes, a table on desktop and cards per topic on a phone; costs, daily life and upfront aligned; unknowns visible; no winner. Home-to-home differences appear only once #96 lands, and criteria results once #147 does. _Reuses: hero figure, gap card._
- [ ] **B9 Questions, question detail and reply check:** statuses; the draft from evidence; record as sent (labelled simulated); reply check with what's still uncertain; explicit attributed confirmation.
- [ ] **B10 Check a home:** buying or renting choice, address combobox, exact-unit confirmation (B1 matches six flats), the map pin flow, "can't find it", and "not yet covered" (WALES-1) with an illustration.

## Story slices (stage 5; epics #87 and #88, one ticket per story step, SP-02)
- [ ] **S-B1 to S-B4 Buyer steps 1–4,** each working end to end across My move, Overview, Costs, Questions, Documents and What changed. Step 4 delivers the hero moment exactly as H2.
- [ ] **S-R1 to S-R4 Renter steps 1–4,** to the same standard: water conflicting, then partial, then specific, then the estimate added; "now complete" rather than "+£X" (#115).

## Craft and brand pass (design canvas, 11 Nov 2026)
- [ ] **Craft sheet** on the canvas is the reference: seven type sizes plus Title 3 (22) in `tokens.css`, the 8-point spacing, four radii (6, 10, 16, 24) with nested corners, three elevation levels, one 30-icon set at a 1.75 stroke (no tick, shield or star), every component state (rest, hover, pressed, focus, loading, disabled, error; selection is border plus fill), and one motion physics. The component gallery (#150) shows it live.
- [ ] **Cost bar** on Costs and each home card: a proportional bar drawn from the engine's line figures (one ordered ramp, 2 px gaps, labels on the largest segments, names also listed), with fixed-width dashed "?" slots for missing and not-calculated lines, never a guessed length.
- [ ] **Partial totals carry their gap on the figure** ("£1,538.37 + ? + ?" for `B1.from-step-1.monthly.total` with its two partial reasons at steps 1–2, "+ 2 costs not included"; one slot at step 3, where only maintenance remains), so a partial total can't read as cheaper than a complete one (Compare, My move).
- [ ] **Source wall** on the landing: one card per source shown in About the data, with what each covers (no limit line, FE-34); names only, no logos.
- [ ] **Photos:** the street band and the FAQ photo on the landing, no visible caption, honest alt text and the footer line; the other four kept for the pages named in `docs/assets/README.md`. **Before stage 5b goes public:** re-check OpenAI's publication policy and restore a visible label if it requires one (#157 gate).
- [x] **Explorations decided** (founder, 11 Nov 2026; the "doesn't tell you" notes were later moved inside "How we got this", FE-34, 14 Nov 2026): costs as a receipt under the cost bar (B5); "What this doesn't tell you" as margin notes on desktop Nearby and a visible note on phones (B6); contour rings declined in favour of the immersive 3D map (B7, P1).
- Review fixes from the independent design review: no tick icon anywhere; "All tracked costs included" is neutral, not a pass mark; nothing that holds figures animates; every entrance ends within 600 ms; only real buttons glow; "Sign in" appears only once accounts exist; household estimates are labelled "your estimate".

## Public site (stage 5b, decision 0046)
- [ ] **P1 Landing** as H7, with the area check as the main action. Account features labelled "coming next" until live, never as active controls; the hero map's pin is "Postcode centre", with crafted category pins and the compact summary card (four nearest places, "+3 more nearby") placed where it covers no pin; its places, distances and count come from the postcode-level sample fixture (B6a), never typed by hand. **The hero map is a static image** (SVG or an optimised raster), not the live map library, so the largest element loads within the 2.5 s budget (B18); the live map loads only on the results page.
- [ ] **P2 How it works** and **About the data:** every source with its icon, name and link, its date, its decision 0029 status (Cached, Fallback, Old or Unavailable), coverage, limits and the attribution its licence requires (DA-05). This is the one place dates and statuses are shown; a fact on a page carries only its source's icon, name and ↗ link (FE-33 amended 14 Nov 2026; the flood check time is here too, DA-12).
- [ ] **P3 Privacy notice and accessibility statement** (SE-02 part 1, decision 0014), live before launch.
- [ ] **P4 Area check on live data:** the B6a screens through the API adapters (0029), with Live, Cached, Fallback or Unavailable labels kept in the data and shown on About the data, not beside each fact (FE-33). The API call sends the postcode in the request body (POST), never in a query string or URL path, so it stays out of every log (0014).
- Not now: pricing (PD-10 open), blog, business page (#151), one search page per postcode.

## Interactions & States
- [ ] **B11 Edge and required states** (#89): every doc 03 §5 state is reachable by URL and shown in the gallery. Covers:
  - several flats at one postcode;
  - an expired certificate;
  - not covered;
  - a source that failed (never shown as a clean result);
  - a stale item;
  - a partial answer and a reopened question;
  - "copied but not recorded as sent";
  - a declined correction;
  - an unchanged refresh;
  - loading skeletons;
  - empty states with illustration.
- [ ] **B12 Viewings and Documents:** a viewing note or photo on mobile becoming a question; a document with findings and a switch to the original; the full-screen evidence sheet.
- [ ] **B13 Ask about this home** (static, #78 design): the sheet or side panel preview, read-only, with figures by ID and no "AI" badge.

## Responsive & Polish
- [ ] **B14 Responsive pass:** 375, 430, 768, 1024, 1280 and 1536 px; the mobile bottom bar plus the More menu; desktop tabs; Compare cards on a phone. Breakpoints come from the tokens.
- [ ] **B15 Motion pass:** the five purposeful transitions plus the public-page entrances in the brief (ring draw, places popping in, sections rising), all from the tokens and 600 ms or less, each playing once; reduced motion respected; figures never animate.
- [ ] **B16 Accessibility pass** (WCAG 2.2 AA in both themes):
  - contrast checked in context;
  - keyboard paths, with the list as the map's alternative;
  - focus moving into and out of sheets in order;
  - screen-reader labels that read each figure with its period and status;
  - 44 px targets;
  - axe and Playwright in CI.
- [ ] **B17 Illustration and photography:** the isometric style guide first (FE-10), then the illustrations for empty states, not covered, onboarding and the landing; home photos through the asset register (rule 5).
- [ ] **B18 Performance budgets:** LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, and the Nearby route JavaScript ≤ 170 KB gzip without the map. Checked by @lhci/cli and size-limit (approved).

## Review
- [ ] **Design review:** run `/designer-skills:design-review` against the brief after H4, and after each build slice, using the gallery as the baseline. Screenshots go in `.design/prototype/screenshots/`, which is git-ignored.
- [ ] **Stage 5 gate** (#90, private prototype, decision 0045).
