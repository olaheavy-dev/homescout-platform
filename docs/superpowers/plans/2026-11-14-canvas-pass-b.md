# Canvas pass B: redraw the pilot's home-context boards

**Date:** 14 Nov 2026  
**Status:** Waiting for #216 (not started). The founder asked for it to be written down before stopping: "make sure to document B, we will stop after A has a merge request opened" (typed, 14 Nov 2026).  
**Where:** the design canvas (https://claude.ai/artifact/MpvQNDVYCePp4iWM3j3Jx4), "Pilot · public area check" page. Canvas work, so it needs no code; the repository only records decisions and the status.  
**Inputs:** [pilot design review](../../reviews/2026-11-14-pilot-design-review.md) (the "ten Nearby, Schools and Map boards" row under "Wrong now (P1), fixed first", and founder decision 2), [look-and-feel review](../../reviews/2026-11-14-pilot-look-and-feel-review.md), register lines FE-20 and FE-26 to FE-33, DA-12 to DA-14, and the postcode-level sample data from #216.

## Before starting: the postcode sample data (#216)
Pass B cannot start until #216 has merged. Every distance on these boards is measured from the postcode centre (AREA-13), but `packages/fixtures/data/area.json` holds only distances from a saved home (records keyed by `homeId`). Using those figures would label a home's distances as postcode distances (rules 1 and 2). Codex raised this as a P1 on #245; the founder chose "#216 first, with levels (Recommended)" (14 Nov 2026, prompt window). #216 adds a postcode-level sample fixture in which every fact also records the area it covers (DA-14).

## Why
Ten boards on the pilot page still show the later home workspace: a saved home ("Flat 2, 14 Mill Court", "This home"), a signed-in menu (My move, Homes, Compare), a demo step strip and a commute row. The pilot has no accounts (decision 0046), and the boards are the reference the build follows. The founder chose "Redraw, move originals (Recommended)" (14 Nov 2026, prompt window).

## What pass A already did
Pass A, published before this plan, set the brand system on "Brand and style" and carried it to the existing pilot boards: one soft-gloss layer (FE-29), ledger rows (FE-30), forest-night dark mode (FE-31), both landing photos kept (FE-32), the source stamp (FE-33) and one marker style. It also fixed the four wrong boards and the quick wins. Pass B uses those components, never local copies.

## The boards (each light and dark)
1. Nearby topics, phone
2. Nearby › Schools, phone
3. Nearby desktop with margin notes
4. Map, phone
5. Map, desktop

That is five boards in two themes, ten in all.

## Steps
1. **Copy, then move.** Copy each original to the "Home workspace (later)" page, labelled "Home workspace version". Pass B changes only the pilot copies.
2. **Strip the home context.** Remove the saved-home title, the signed-in menu, the demo step strip, the commute row and anything that needs an account. The header becomes the public header (logo, How it works, About the data, theme and text-size controls when FE-23 is drawn). The page title is the postcode ("Around NB1 4XY", Bricolage 28, from the look review's quick wins).
3. **Topic detail follows FE-20 and FE-26.** "Nearby › Schools" becomes the Schools topic opened as a bottom sheet on the phone over the Check an area list, and as the right-column side panel on desktop. It is never a separate page. One panel shows at a time; the chat opens as a drawer.
4. **Desktop Nearby with margin notes** stays the strongest honesty device (look review "What to keep"). Redraw it as the desktop Check an area result: the topic list on the left with margin notes, and the map in the right column until a topic opens. This also covers the missing desktop result board ("the desktop result for Check an area" in the review's first batch).
5. **Maps.** The map shows the postcode centre, not a home. Distances are measured from the postcode centre and say so. Filter chips stay clear of the list panel. Every control is at least 44 px. Phone and desktop markers use the one marker style.
6. **Content rules:**
   - Figures as ledger rows, England in miles to one decimal place (FE-27), crime "within 1 mile".
   - A source stamp on every fact (Cached, Old or Unavailable; never Live).
   - One-line limits on flood, crime, sold prices and schools (FE-28).
   - Sold prices show street and property type only (DA-13).
   - Flood wording from AREA-21.
   - Every name and distance comes from the postcode-level sample fixture added by #216, never from the home records in `area.json`; no typed figure (rules 1, 2 and 7).
   - Every fact names the area it covers (DA-14), for example "from the postcode centre", "within 1 mile", "within 500 m" (sold prices, with the radius stated), "this postcode", "this neighbourhood" or the council's name.
7. **Check:** render every redrawn board at 390 px and 1280 px, light and dark. Check contrast on the gloss surfaces (WCAG AA), compare each board with its pass A neighbours for consistency, and update the page's "still to design" note.
8. **Sync the repository design files** in a small pull request: `.design/prototype/tokens.css` and `DESIGN_BRIEF.md` take the version 92 values for soft gloss (FE-29), forest night (FE-31) and the source stamp (FE-33), so the build reads the same system as the canvas.
9. **Publish once** to the same canvas URL, with a label. Tell the founder the version number and what changed, then ask the founder to review.

## Acceptance
- No board on the pilot page shows a saved home, an account menu, a commute or a demo strip.
- The originals sit on "Home workspace (later)", labelled.
- Schools opens as a sheet or panel, never a page.
- Every figure traces to the postcode-level fixture from #216, every fact carries a source stamp and names the area it covers (DA-14).
- Light and dark boards match the pass A system, with no local style overrides.

## After pass B
The first design batch from the pilot design review comes next. It covers At a glance, the topic detail anatomy for every topic, priorities (FE-22, decision 0053), the missing states and theme and text size (FE-23). The founder reviews the canvas, and then the specifications are written.
