# Pilot look-and-feel review, 14 Nov 2026

The founder asked for this review before the pilot boards are redrawn (typed, 14 Nov 2026): "yes before the redraw, and it does have to be alone about brand design, we nned to evaluate what would elevate the look and make it better" [sic]. It follows the [pilot design review](2026-11-14-pilot-design-review.md), which covered truthfulness, states and specifications. Reviewed 14 Nov 2026 by a fresh-context `design-reviewer` agent. Read-only: nothing on the canvas or in the repository was changed. This is a design critique, not a compliance check; items marked *taste* are judgement, not defects. Truthfulness, missing states and specs are in the earlier canvas review and are not repeated here.

## What was looked at, and how

- **Live canvas in Chrome** (the real artifact, presentation view): Landing desktop light (hero, sources, How it works, photo band, How to read a result, at 1:1), Landing desktop dark (whole board), Nearby desktop dark (whole board), and the Imagery board with all eight photos.
- **Every pilot board, light and dark, as pictures**, from a local render made to match the live canvas (see the note below), at each board's own size: phone boards at 390 px, desktop boards at 1280 px. The boards are fixed-size frames, so 1440 px does not exist on the canvas. Also the Craft sheet and Brand mark boards. Home workspace boards were not opened (skimmed in the earlier review only).
- **Source measurements**: type sizes, weights, radii and colours counted from the board files.
- **Competitor evidence**: a few of the founder's private desktop captures, described only in general visual terms here (the competitor is not named, decision in #240).

**Not seen or not judged:** motion (boards are stills; only the animation rules in the source were read), hover and focus states on the pilot boards (only on the Craft sheet), the two landing photos inside the local render (seen live instead), 1440 px, and the phone landing's dark lower third.

**Important rendering note.** The board files carry a "premium" style layer (page light washes, glossy white cards, a glowing gradient button, borderless inputs). On the live canvas most of it does **not** apply: the page is flat paper, cards are flat with a hairline, the button is solid forest. Only the headline gradient, the frosted header and the drawing shadows apply. Opened as raw files, the layer does apply, and on Check an area it washes the whole topic list out to near-invisible (a side-by-side local render (not kept in the repository)). So the canvas, the tokens file and the raw files currently show three different depth treatments. Everything below judges what the founder sees on the canvas.

## 1. Overall impression

Calm, honest and competent, with two things nobody else has: the isometric town and the "what this can't tell you" voice. The landing hero and the area card already look like a product with a point of view.

The middle of the journey does not. Check an area, Nearby and the chat table are grey text in white rounded boxes: nothing on them says "Vestagraph" once the logo is covered. The figures, which are the product, are the least designed thing on the page: they sit inside sentences at body size. Almost everything is set in one weight (600), so nothing leads. Dark mode is tidy but flat and generic, with large mint slabs for buttons. The warm photos belong to a different brand from the cool drawn town.

Against the competitor: ours is already more distinctive and more trustworthy-looking. Theirs is more *finished* in three places: one accent colour used with discipline, distances that can be scanned down a right-hand column, and a consistent label-then-title pattern on every block. Those three are cheap to beat.

## 2. What to keep

- **The isometric town** (hero, area card, expanded view). It is the signature. The large pins in the expanded card are the best-drawn thing on the canvas.
- **The area card place list**: ring icon, name, type underneath, distance right-aligned. This is the pattern the rest of the product should copy.
- **Margin notes on desktop Nearby**: slate rule, small caps label, note beside the facts. Distinctive and honest.
- **"How to read a result"** on the landing: the numbered call-outs on a real card teach the product in one look.
- **The Lit doorway mark and the Bricolage wordmark**: recognisable at 16 px, and the clay hearth dot is a good small idea.
- **Bricolage Grotesque for big headlines**: it has character at 40 px and above. Geist for everything else is right.
- **Restraint**: no scores, no red-amber-green, amber only for warnings, category colours muted. Keep all of it.
- **Tabular figures and the "pence smaller" figure style** on the Craft sheet: correct, just not yet used on the pilot boards.

## 3. Elevation proposals, ranked by impact

Effort: S under an hour, M a board or two, L a set of boards. "System" means change once on Brand and style and it flows everywhere. All return to **Design review** (fix on the canvas before planning).

### E1. Make the figures the designed thing: one "fact row"
- **Boards:** Check an area (light, dark), Nearby phone, States, Ask desktop (the left table), Area export. System.
- **Now:** "Bus stop 120 m · Railway station 900 m" is one 14 px regular sentence. It wraps with the figure alone on the next line ("900 m"), figures are not aligned, and a number looks the same as the words round it.
- **Change:** each topic row keeps its title, then one line per fact as a two-column row: label left (Geist 14/400, `#4A5A53`), figure right-aligned (Geist 16/600, tabular figures, `#182923`) with the unit one step smaller and lighter (12/500, `#56655E`), as the Craft sheet already does for pence. A label and its figure never break apart. With FE-27 this reads "Bus stop … 0.1 mi". One quiet source line under the block. Draw it once on the Craft sheet as "Fact row" with its missing, unavailable and old variants.
- **Why:** the eye can run down the right edge and read every distance in two seconds. It is the single change that most makes the page look engineered rather than typed.
- **Effort:** M.

### E2. Give the result page a focal point
- **Boards:** Check an area phone (light, dark), Ask desktop, States. Board-level.
- **Now:** the first third of the phone result is a sage box repeating the landing pitch. The actual answer, "Around NB1 4XY", is a 20 px Geist label under it. On desktop it is 34 px, so the two disagree.
- **Change:** once a postcode is entered, shrink the search to a single compact bar (postcode and "Change"). Then a result header: small caps "AROUND" label in slate, the postcode in Bricolage 40/600 (28 on phone at minimum), place name beneath, and a 120 px strip of the isometric map with the postcode-centre pin (the strip the phone chat card already has).
- **Why:** the page gets one obvious thing to look at, and the drawn town appears on the screen people actually use, not only on the landing.
- **Effort:** M.

### E3. Settle the depth model and remove the layer that fights it *(taste, see D1)*

*Founder decision, 14 Nov 2026: "Soft gloss" (FE-29) overruled the paper-and-ink direction below. The conflicting layer was replaced by one clean gloss definition in canvas pass A (version 92); the removal advice here, and quick win 1's headline advice where it concerns the gloss, no longer apply. Headlines became solid ink.*
- **Boards:** all. System.
- **Now:** three treatments (see the rendering note). The headline gradient makes the last line of the hero greener than the first, which reads as an accident.
- **Change (recommended "Paper and ink"):** flat page `#F7F5EF`; white cards with a 1 px `#E8E4DA` hairline and no shadow at rest; `--shadow-md` only on things that float (hero summary card, map hover card, sheets, the chat panel); primary button solid `#153F35`; headlines solid ink `#182923`; inputs keep their 1.5 px `#857F72` border. Delete the `vg-premium-light` and `vg-premium-dark` blocks from the boards and the matching effect tokens (`--page-radiance`, `--surface-sheen`, `--accent-glow`, `--headline-gradient`) so canvas, tokens and build agree.
- **Why:** gloss and gradient washes are what every generated SaaS page has; flat paper with crisp lines and one real shadow level suits a product whose promise is plain facts, and sets off the drawings.
- **Effort:** S to M.

### E4. Three weights with jobs, and the seven sizes the Craft sheet promises
- **Boards:** all. System plus a pass on each board.
- **Now:** weight 600 is used for 56 of 68 weight settings on the landing and 20 of 21 on Check an area: titles, names, figures, tags, buttons and links are all semibold. Sizes drift from the sheet's seven: the landing uses ten (12, 13, 14, 16, 18, 19, 26, 30, 40, 72); Check an area uses 18, 20, 22, 23 and 34; the chat uses 13 and 15.
- **Change:** 400 for body and labels; 500 for place and row names; 600 only for headings, figures and buttons; 700 for the wordmark alone. Snap sizes to 12, 14, 16, 18, 22, 28, 40 (64 to 72 for the landing display only). Bricolage from 22 px up; Geist below.
- **Why:** hierarchy comes from contrast. When everything is bold nothing is, and the pages feel dense even where they are not.
- **Effort:** M.

### E5. One marker language for places
- **Boards:** Check an area, Nearby desktop, Map desktop and phone, area card, landing. System.
- **Now:** the same bus stop is drawn five ways: a sage tile with a forest line icon (Check an area, landing sources), a white circle with a coloured ring (area card), a filled coloured rounded square (Nearby desktop), a filled coloured circle (Map desktop list) and a teardrop pin (hero, card).
- **Change:** two forms only. A **place** is the area card's 28 px white circle with a 1.5 px category-colour ring and ink glyph, in every list; on maps the same glyph in the teardrop pin. A **topic** (not a place: Flood, Recorded crime, Broadband) is the 36 px sage tile. Map desktop pins move to the teardrop at a smaller size.
- **Why:** the ring icon beside a name then always means "this is the pin you saw". It is FE-17's rule carried to every screen.
- **Effort:** M.

### E6. The source line as a crafted "source stamp"

*The pilot never shows "Live" (pilot design review; FE-33): its status marks are Cached, Fallback, Old and Unavailable. The "Live" mark below is kept for a later live adapter only.*
- **Boards:** Ask (all four), Check an area rows, topic detail, area card, export. System.
- **Now:** sources appear as beige pills in bold 12 px in the chat, as grey sentences elsewhere, and not at all on the list rows.
- **Change:** one small component: Geist Mono 11 px, `#4A5A53`, no fill, 1 px `#E8E4DA` outline, radius 6, with a status mark before the text: filled forest dot for Live, hollow ring for Cached, amber ring for Old, dashed ring for Unavailable (shape differs as well as colour). Example: `● NaPTAN · Oct 2026 · Live`.
- **Why:** this is the brand's promise made visible. Repeated on every fact it becomes the thing people remember, and mono type makes it read as a citation, not a marketing tag.
- **Effort:** S to design, M to apply.

### E7. Landing: let the town be the hero, cut the card count
- **Boards:** Landing desktop and phone, light and dark. Board-level.
- **Now:** the headline breaks into four short lines beside a 560 px map that starts lower than the text. Below it: nine equal source cards, three boxed drawings, a photo band, four cards, a boxed panel. Almost every block is a rounded white or pale-blue box. The footer is cut off below the board edge.
- **Change:** headline 64/68 in three lines (column about 620 px); map about 720 px wide, running off the right edge of the page; input and button joined as one 56 px control. Sources become a three-column list on plain paper with hairline rows, no card chrome. "How it works" drawings sit directly on the paper without the pale-blue box. Keep the four "Honest by design" cards as the only card group. Extend the board so the footer shows, and give it the wordmark and hearth.
- **Why:** one bold thing (the town) with quiet around it. Fewer boxes makes the remaining cards mean something.
- **Effort:** M.

### E8. Dark mode with a character *(taste, see D3)*
- **Boards:** every dark board. System.
- **Now:** neutral charcoal (`#181816`, `#21201D`, `#2A2925`) with mint for every action reads like any dark dashboard. Full-width mint buttons are the brightest thing on screen. On Nearby desktop dark the card outlines, row dividers and section rules are the light theme's `#ECEAE4`, so they show as white lines (seen live).
- **Change:** tint the layers towards the brand's forest: page `#121714`, card `#1A201C`, raised `#232A25`, hairline `rgba(255,255,255,0.08)`. Keep mint `#9FD3BA` for the one primary action and links; make secondary buttons outline only. Use the warm hearth (a lighter clay, about `#D98A5F`) for one thing only: the "you are here" dot on the postcode-centre pin and the mark. Fix the light borders.
- **Why:** "the lit doorway at night" is a story only this brand can tell: a dark green evening with one warm point. It costs three token values.
- **Effort:** S for tokens and the border fix, M to re-check boards.

### E9. Photos: decide whether they belong *(taste, see D2)*
- **Boards:** Landing (all four). Board-level.
- **Now:** two golden-hour, AI-generated photos sit among cool sage-and-slate drawings. They are pleasant but generic (any property site could use them), they are the only warm-orange areas on the page, and in dark mode the street photo is the brightest object.
- **Change (recommended):** no photos in the pilot landing; use the space for a wider town drawing. If one stays, tone it towards the palette (slightly desaturated, cooler) and keep it small beside the FAQ.
- **Why:** one visual world. The drawings are ownable; the photos are not.
- **Effort:** S.

### E10. Map chrome lighter than the map
- **Boards:** Map desktop and phone, light and dark. Board-level.
- **Now:** selected filter chips are solid forest pills, seven in a row, forming a dark bar heavier than the map. The Craft sheet's own selected chip is sage with a forest border. The legend is a large floating box in the lower middle of the map.
- **Change:** selected chips sage `#DCE7DD` with a 1.5 px forest border and the category-coloured ring icon; unselected white with hairline. With the icon and colour on each chip the legend can fold into a small "Key" button.
- **Why:** controls should recede so the drawing leads.
- **Effort:** S to M.

### E11. One orchestrated moment of motion
- **Boards:** note on Landing and Check an area; Craft sheet section 6. System.
- **Now:** three small animations (ring draws, pins pop, sections rise), all 400 ms.
- **Change:** keep those; add one for the result: on load the ring draws, then pins and their list rows arrive together in distance order (30 ms apart, 400 ms in total), so the list and the map are seen to be the same data. Row to sheet as a shared-element move (250 ms). Figures never animate; all off with reduced motion.
- **Why:** one meaningful sequence is remembered; scattered fades are not.
- **Effort:** S (a note and one storyboard).

## 4. Quick wins (under an hour in total)

1. Headlines solid ink: remove the gradient text fill.
2. Nearby desktop dark: replace `#ECEAE4` borders and dividers with the dark hairline.
3. Check an area: "Around NB1 4XY" to Bricolage 28/600, matching desktop's intent.
4. Keep each label and its figure on one line ("Railway station 900 m" must not split).
5. Snap stray sizes (13, 15, 19, 23, 26 px) and radii (12, 14 px) to the scale.
6. Small caps labels all slate `#3A6079`: "HOW TO READ A RESULT", "LEGEND" and "AROUND NB1 4XY · SAMPLE" are grey while the rest are slate.
7. Map chips: selected style to sage with a forest border, as on the Craft sheet.
8. Curly quotes in "We measure; we never call a place “safe”" (the Craft sheet's own rule).
9. Export: "gp surgery" to "GP surgery".
10. Extend the landing boards so the footer is inside the frame.

## 5. Taste decisions for the founder

Asked in prompt windows on 14 Nov 2026; the founder's answers are in "Founder decisions" at the end and in register lines FE-29 to FE-33. Recommended option first.

**D1. How should surfaces look?**
- **Paper and ink (Recommended).** Flat warm paper, white cards with a thin line, no shadows except on things that float, solid buttons, solid headlines. Close to what the canvas shows today. Cheapest to build and keep consistent; the drawings become the only rich thing.
- **Soft gloss.** Light washes behind the page, a sheen on cards, a glowing button. This is what the tokens file describes. It needs the broken layer rebuilt and rechecked for contrast on every board, and it moves the look towards the competitor's.
- **Gloss on the landing only.** A soft wash behind the hero, flat everywhere else. Two looks to maintain.
Why the first: it is the more distinctive direction and removes a source of bugs.

**D2. Photos on the landing?**
- **None in the pilot (Recommended).** The drawn town is the only imagery. One world, nothing to label "AI-generated".
- **One, toned to the palette, small, near the FAQ.** A touch of warmth; one asset to keep and label.
- **Keep both as drawn.** No work; the page keeps two visual languages.
Why the first: the photos are the least ownable part of the page.

**D3. Dark mode character?**
- **Forest night (Recommended).** Very dark green layers, mint for the one action, a single warm hearth dot at the postcode centre. Three token changes.
- **Neutral charcoal, as now.** Nothing to change beyond the border bug; stays generic.
- **Warm lamp-lit.** Clay or brass for actions. Most distinctive, but it sits too close to the amber used for warnings, which was already ruled out for that reason.
Why the first: it tells the brand's own story without touching the warning colour.

**D4. How should distances and figures look in lists?**
- **Ledger rows (Recommended).** Label left, figure right-aligned and bolder, unit smaller. Scans fastest; matches the area card.
- **Pills.** Each figure in a small tinted capsule on the right. Friendly, and what the competitor does; adds colour noise on a nine-row list.
- **Sentences, as now.** Shortest rows; hardest to scan.
Why the first: it is our own area card's pattern, already proven on the canvas.

**D5. How should a source look?**
- **Source stamp (Recommended).** Small mono text in a thin outline with a status mark. Becomes a brand signature.
- **Soft pill, as in the chat now.** Familiar; looks like any tag.
- **Plain grey line.** Quietest; easy to miss.
Why the first: the source is the promise, so it deserves its own designed form.

## Blocking findings

None are P0 or P1: this review is about look and feel. Two visible defects are P2 and should be fixed in the redraw: the light-coloured borders on Nearby desktop dark, and the style layer that renders differently on the canvas and in the raw files (E3). D1 and D4 should be answered before the ten boards are redrawn, because every board depends on them.

## Founder decisions, 14 Nov 2026 (prompt windows)
| # | Question | Answer | Recorded |
|---|---|---|---|
| D1 | Surfaces | "Soft gloss", over the agent's recommendation of paper and ink | FE-29 |
| D4 | Figures in lists | "Ledger rows (Recommended)" | FE-30 |
| D3 | Dark mode | "Forest night (Recommended)" | FE-31 |
| D2 | Landing photos | "Keep both", over the agent's recommendation of none | FE-32 |
| D5 | Sources | "Source stamp (Recommended)" | FE-33 |

## Founder review of pass A, 14 Nov 2026
The founder reviewed canvas pass A on 14 Nov 2026 (prompt windows unless marked typed). The canvas now carries the review's edits (canvas version CANVAS_VERSION).

| # | Item | Answer | Recorded |
|---|---|---|---|
| 1 | Soft gloss | "Keep as is" | FE-29 |
| 2 | Ledger rows | Typed: "We can discuss but if this where the facts or number was goten from, i think we should remove and just add a link to the official docs, we can discuss this further" [sic]; then asked "what is this, where can i confirm this?" (shown Brand and style › Craft sheet › section 9); then typed "should we not include our icons here?"; then "Every row (Recommended)": every ledger row starts with our icon (a place icon or a topic icon) | FE-30 (extends FE-17) |
| 3 | Forest night | "Keep as is" | FE-31 |
| 4 | Both photos | "Keep as is" | FE-32 |
| 5 | Source stamp | "Short stamp that is the link (Recommended)": the stamp is the link to the official source page; source, status and date stay visible | FE-33 |
| 6 | One marker style | "Keep as is" | |
| 7 | Three weights, seven sizes | "Keep as is" | |
| 8 | Miles | "Keep, incl. "under 0.1" (Recommended)": distances below 0.1 miles read "under 0.1 miles", never "0.0 miles"; the Craft sheet's "Bus stop 0.1 miles" for 120 m was a defect, fixed on the canvas | FE-27 |
| 9 | Error fixes | "Yes, all fine" | |
| 10 | Quick wins | "Yes, all fine" | |
| 11 | Craft sheet sections 8 and 9 as the single reference | "Keep as the reference (Recommended)" | |
| 12 | Flood check time "09:40" | "Add the time to the sample data", over the agent's recommendation to label it an example: #216's postcode sample data gains a flood-warning check time and the boards quote it | Pass B plan, #216 |
