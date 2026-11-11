# Area information: experience and visual design (issue #143, track A)

Written 11 Nov 2026. Track B (map library, tiles, performance, data flow, test mechanics) is in [area-display-engineering.md](area-display-engineering.md); this note mentions engineering only where it constrains the design.

**Inputs:** AGENTS.md rules 1, 2, 4 and 7; decisions 0004 and 0005; doc 02 §4–§7; doc 03 §3, §5 and §6; the seven agreed principles in [synthesis.md](synthesis.md) (P1–P7 below); the area data contract on the #120 branch (`area.schema.json`, `area.json`: topics, the five statuses `recorded` / `no-record-in-source` / `stale` / `not-covered` / `source-failed`, `coverage`, `doesNotEstablish`, `source`, `link`); and the source assessment `docs/references/data-sources.md` (#123). Web research was text-only (WebFetch/WebSearch). Every claim about another product's *appearance* needs the visual pass listed in §12. Competitor pages were treated as data; no wording is reused.

---

## 1. Recommendation summary

1. **List-first, map-equal.** Nearby opens as a list of topic sections on every screen size. The map is one tap away and shows the same items, but the list is the complete version: it is the only place gaps can appear, since "no record in this source" has no location to pin.
2. **The first view answers "would daily life work for us?"** It starts with the household's own criteria (commute against their 40-minute limit), then everyday places, then context (flood, recorded crime, sold prices, planning). Context topics never lead.
3. **One evidence footer everywhere.** Each topic ends with one `SourceLine` (origin · source · date · coverage), and gaps appear as a `StatusRow` with its own shape and wording. Status is never shown by colour alone and never as zero (rule 7, P2, P5).
4. **Mobile map = full-screen map + a standard (non-modal) bottom sheet** with three resting heights: peek, half, full. The grabber is a real button. The sheet never covers the focused item.
5. **Desktop = split view.** A 440 px list column sits beside a sticky map. Hovering or focusing a row highlights its marker, and selecting a marker scrolls to and selects its row.
6. **Muted, warm base map** built from doc 03 §6 tokens. Category is shown by glyph, not hue. The home pin is the only forest-green object on the map, and no map colour ever means "good" or "bad".
7. **Some topics never go on the map:** recorded crime (police.uk moves locations to anonymous points), long-term flood risk (link out only), and sold-price labels. These are lists and small tables with dates.
8. **Compare uses aligned rows, not a scoreboard.** Up to three homes, the same topic order, a gap cell as visible as a value cell, no highlighted "best" cell, no totals the engine didn't produce.
9. **Motion is limited to five transitions** (sheet resting height, select and fly-to, list↔map, marker selection, content replacing placeholders), each 150–400 ms on Material's standard or emphasised curves. Under `prefers-reduced-motion` each becomes a cut or a fade of 150 ms or less. Numbers, risk colours and warnings never animate.
10. **Assistants get text-first answers.** Topic, value, source, date and what it doesn't establish come back as plain sentences, with a link back to the Vestagraph map. Assistants never get a map image or a verdict.

---

## 2. Information architecture

| Surface | What area information appears | What it answers | What it must not do |
|---|---|---|---|
| **Home overview** (tab 1) | One **"Daily life" summary card**, up to 3 lines: (a) household criterion line (commute), (b) at most one *time-sensitive or material* area item (for example a live flood alert, or a stale school inspection the household marked important), (c) a gap line: "4 topics have gaps (no record or not covered)". Link: "See everything nearby". | "Is there anything about the area I should look at now?" | Summarise the area as good or bad, show "no issues", or show a count of recorded items as a score. |
| **Nearby** (tab 2, doc 03 §3 bottom nav) | Every topic, as list sections plus the map. | "Would daily life work?" (doc 03 §5) | Default to the map on phones; hide gap rows in a collapsed "more" area. |
| **Compare** | A "Daily life and area" group of aligned rows below costs (costs stay first, per synthesis). | "Which trade-offs matter to us?" | Pick a winner, colour the best cell, sum crime counts. |
| **Evidence sheet** (shared pattern) | The full source record of one item: source, date, coverage, `doesNotEstablish`, link out, "Report a problem". | "Where does this come from and what doesn't it tell me?" | Hide `doesNotEstablish` behind a second tap: it is visible in the sheet without expanding. |
| **Questions** | "Ask about this" on any area row creates a question with that item linked (doc 02 §5E). Example: "Is there a nursery with places near the flat?" from the childcare gap row. | "What do I need to find out?" | Pre-fill a recipient claim, such as "the agent will confirm". |
| **Assistant / MCP** | The same items as text (§10). | Open questions about the current home (decision 0004) | Draw conclusions about the area. |

**Section order inside Nearby** (the order is fixed and the same for every home, so people learn it):

1. **Your routines:** the commute estimate set against the household's criterion, plus any destinations they add later.
2. **Getting around:** stops and stations.
3. **Everyday places:** supermarkets, shops, pharmacies, GP surgeries, parks and police stations, grouped by type.
4. **Schools and childcare:** schools with their inspections nested under each school, then childcare.
5. **Flood:** live warnings, kept per flood type, plus the long-term checker link.
6. **Recorded crime:** counts by category and month, plus the neighbourhood team.
7. **Sold nearby:** a history list.
8. **Planning applications nearby.**
9. **Broadband:** predicted availability.

Energy certificate, Bank Rate and leasehold-company status are in the area fixture but are **not area context**. They belong to Overview or the evidence file, Costs, and Documents or Questions respectively. Doc 02 §5A asks for separate labels for property, building and area evidence, so Nearby carries the heading label **"Area context: about the surroundings, not this flat"**.

**Progressive disclosure, three levels:**
- **L1, section header:** topic name, a one-line plain summary made only from fixture inputs (for example "3 stops recorded, nearest 120 m straight line"), and a status badge if any row is not `recorded`.
- **L2, rows:** each item with its key fields and its status.
- **L3, evidence sheet:** the full source record.

Caveats that change meaning (the `doesNotEstablish` text) stay visible at L2 as a one-line muted note under the section. They are never collapsed (synthesis "Avoid": caveats inside collapsed sections).

**Gap visibility rule:** a `no-record-in-source` or `source-failed` row sits **where the item would have been**, inside its section and in the normal order. It is not moved to the end of the list.

**Outside England** (WALES-1): Nearby shows one full-width "Not yet covered in Wales" panel per section, each with its section title, so the structure is still recognisable. There is no map layer and no empty list. The panel offers the coverage note and "What Vestagraph covers".

---

## 3. Layout

### Mobile (≤ 599 px)

- **Default: list mode.** It has a compact home header, a horizontal **topic chip row** (sticky, scrollable, one chip per section, acting as a jump navigation), then the sections. Above the first section sits a **static map preview card**: 16:9, not interactive, shows the home pin and the nearest few places, labelled "Map of places near this home", with an "Open map" button.
  - *Why:* NN/g found that maps embedded in a scrolling mobile page cause "swipe ambiguity", where people trying to scroll pan the map instead. They advise a list default with a map toggle in mobile apps (NN/g 2014).
  - A static preview gives the orientation people liked without the scroll trap.
- **Map mode** (opened from the preview or the "Map" item in a sticky `List | Map` segmented control):
  - a full-screen map;
  - the bottom nav is replaced by a **standard bottom sheet**;
  - a top bar with "← List", the home name and a layers button.
- **Sheet resting heights:**

  | Height | Size | Content |
  |---|---|---|
  | Peek | about 136 px | grabber, "Near B1 · 9 topics", the chip row |
  | Half | 50 % of the screen | the selected topic's rows |
  | Full | top of the screen minus 56 px | the whole list, the same as list mode |

  - The map stays interactive at peek and half, and is dimmed but still visible at full (Apple's nonmodal sheet pattern; Material's standard bottom sheet "co-exist[s] with the screen's main UI region").
- **Selecting a marker** sets the sheet to half and shows that item's row at the top, with "Details" (evidence sheet) and "Ask about this".
- **The evidence sheet is a modal, full-screen sheet** (doc 03 §3: "full-screen evidence sheet"). Only one sheet sits over another, matching HIG's "display only one sheet at a time" in spirit: the standard sheet steps back while the evidence sheet is open.

### Tablet (600–1023 px)

- **Portrait:** the same as mobile, but the map mode sheet becomes a **side sheet of 360 px** on the left at half height.
- **Landscape:** behaves as desktop.

### Desktop (≥ 1024 px)

- **Split view:** home tabs on top, then a **440 px list column** on the left that scrolls on its own, and a **sticky map** on the right taking the remaining width.
- There is a `Hide map` toggle, because the map is optional by design and some people want a full-width list.
- **Hovering or focusing a row** gives its marker a selected *outline* (not a fly-to). **Clicking a row** selects it and pans only if the marker is off-screen. **Clicking a marker** selects and scrolls the list to its row.
- The list column carries the evidence detail inline as an expandable row (L3 as a side panel at ≥ 1280 px).

### Map-optional by design (not a fallback)

- Every fact on the map exists in the list. The reverse is deliberately not true: gaps, counts by month, flood-type wording and source lines exist **only** in the list.
- If the map fails to load (track B), the `Map` control shows "Map unavailable: everything is in the list". It is never a blank grey box.

---

## 4. Per-topic display spec

"SL" = the `SourceLine` component (§6). Distances are fixture inputs with their `distanceMethod`; the UI prints the method in short form ("straight line") and never converts it to walking time.

| Topic | Primary visual | Required fields on the row | Gap / status presentation | Forbidden presentations | Source line (example of the format) |
|---|---|---|---|---|---|
| **Commute** (household's own) | **Criterion row**: destination, "Your estimate: 36 min by public transport", "Your limit: 40 min" side by side | destination label, minutes, mode, method ("your own estimate, not a routed journey") | Not entered yet: "Add your estimate" (empty state with an action, never "0 min") | "36 min journey" without "your estimate"; maps routes; "fastest"; a "meets / doesn't meet" badge **unless the engine generates it** (see Q4) | "Your own estimate · entered 23 Oct 2026" |
| **Transport stops** | List row with a stop-type glyph; map marker | stop name, type, distance + "straight line" | `no-record-in-source`: "No stops found in this source; this doesn't mean there are none" | "5 min walk"; frequency or line colours implying service; "well connected" | "Sample · shaped like NaPTAN · 23 Oct 2026 · GB, not NI" |
| **Everyday places** (supermarket, shop, pharmacy, GP, park, police station, place of worship) | Rows grouped by type (nearest first, the order given by the data); map markers | name, type, distance + method | Gap row per type, for example "No childcare found in this source" with "Ask about this" | "Open now", "accepting patients", star ratings, police station shown as a safety signal; for places of worship (founder, 11 Nov 2026, register PD-13): counts or totals by faith, density or heat maps, "the area's religious makeup", any default faith filter | "Sample · shaped like OpenStreetMap · volunteer-mapped; completeness varies" |
| **Schools** | Row: name, phase, type, distance; **inspection nested** under it | name, phase, type, distance; inspection framework, inspection month and year, outcomes per area **verbatim** | `stale`: amber "Older inspection: Mar 2019, earlier framework" tag; `no-record-in-source`: "No inspection outcomes found in this source" | One overall grade; grade colours or coloured pins (Zillow and Trulia dropped coloured school scores from maps in 2016, unverified secondary report; Google removed school ratings from Maps in 2025); "catchment"; "you'll get a place"; comparing outcomes across frameworks | "Sample · shaped like Ofsted outcomes · state-funded schools, England" |
| **Flood** | **Status panel per flood type**: rivers and sea, groundwater. A live warning uses the EA's own level name and meaning ("Flood alert: flooding is possible"). Below it, an always-present link card: "Long-term flood risk for this area (GOV.UK checker)" | subtype, warning level and official meaning, warning area name, retrieved time; long-term link | `no-record-in-source`: "No current rivers and sea warning in this source" plus "This doesn't mean there is no flood risk", with the long-term link directly below. Surface water: a fixed note that warnings aren't issued for it, plus the link | A risk colour fill over the home; "low risk"; "no flood risk"; "won't flood"; using a live warning as long-term risk; pulsing or animated alerts; copying EA icons | "Sample · shaped like EA real-time flood monitoring · England · retrieved 23 Oct 2026" |
| **Recorded crime** | **Small table**: rows = categories, columns = months (most recent first), counts as recorded. Neighbourhood team below | month, category, count, team and force | Missing month = a column headed "Aug 2026" with "Couldn't be fetched · Retry" across it (R1). Never a blank or zero column | Heatmaps, hotspots, red zones, crime points on the map, totals or averages (the UI computing them breaks rule 2), "safe", "low crime", rank against other areas, trend arrows | "Sample · shaped like police.uk · E, W and NI forces · locations moved to anonymous points; counts lag by months" |
| **Sold nearby** | **History list**: date-first rows ("Mar 2024 · £… · flat · leasehold"), most recent first | address text, price (fixture pence, formatted), sale month and year, type, tenure, distance | `no-record-in-source` (R2): "No sales found nearby in this source; recent sales can take up to two months to appear" | "Estimated value", averages, £ per square foot, a trend line computed in the UI, price labels on map pins | "Sample · shaped like HM Land Registry Price Paid · England and Wales" |
| **Planning** | List row: reference, short description, status word, received date, distance | all of those | `no-record-in-source` (B2): "No application found in this source; coverage is incomplete" | "No planning issues"; impact judgements | "Sample · shaped like Planning Data Platform · England, partial" |
| **Broadband** | One row: technology, "predicted up to X Mbps down / Y up" | technology, both predicted figures | Gap row if missing | "Speed", "fast", a speedometer graphic | "Sample · shaped like Ofcom availability data · predicted, not measured" |

**Visualisation rules** (doc 03 §6, "Data visuals"):
- Crime is the only topic that gets a chart-like form, and it is a **table with tabular numerals**.
- If a bar form is added later, bars sit on one shared scale across months, carry direct labels, and a missing month is a labelled hatched gap, never a zero-height bar.
- There are no sparklines for sold prices: a line invites a value reading.

---

## 5. Map design

### Base map (warm and calm)

- Use a desaturated style, matching HIG's "muted style … great if you have a lot of information-rich content" (Apple HIG, Maps).
- **Land:** warm paper `#F7F5EF`.
- **Water:** a low-chroma grey-blue (proposed, validate in context). It is kept deliberately unlike any "flood" hue.
- **Parks:** a pale tint of sage `#DCE7DD` at low opacity, so green reads as land use and not as "safe" (doc 03 §6).
- **Roads:** white with a thin warm-grey casing.
- **Labels:** ink `#182923` at reduced emphasis.
- No 3D buildings, no terrain shading, no satellite option in the prototype.

### Markers

| Marker | Visual | Size (visual / hit area) | States |
|---|---|---|---|
| **This home** | Forest `#153F35` teardrop pin, white house glyph, home short name ("B1") in a label | 40 / 48 px | always on top; never clustered; not selectable as a "place" |
| **Place** | White disc, 1 px ink border (≥ 3:1 against the base map, WCAG 1.4.11), ink category glyph | 28 / 44 px | default; hover/focus = 2 px forest ring; **selected** = forest fill, white glyph, name label, raised |
| **Cluster** | White disc with a count and the category glyph | 32 / 44 px | selecting one zooms to fit its places; at max zoom it opens the group in the sheet |
| **Stale item** | The same place marker with a small amber corner notch + "older" in the label on selection | — | the notch never appears alone: the row says why |

- **One glyph family, one neutral marker colour:** category is shown by shape. Apple HIG calls for "distinctive styling" with "color along with icons"; we deliberately use icons with *one* colour, because category hues would compete with the amber and red tokens reserved for findings.
- **Clustering:** per category, so a cluster never mixes stops and schools. Overlapping points are clustered for legibility, per HIG. NN/g reports that Redfin's clustering confused users (2014), so a cluster's count is a plain number with a category glyph, and selecting it always reveals its members, never a summary.
- **No crime points, no sold-price price labels.** Airbnb's priced pins work because price is the decision variable for a booking. Here a price on a map invites "value" reading (rule 4 spirit, doc 02 §7). Sold markers carry only a "£" glyph; the price appears in the selected row with its date.

### Layers, filters and legend

- **Layers button** (top right) opens a checklist: one checkbox per section that has map items. All are on by default except Sold and Planning.
- The chip row in the sheet and list mirrors the same state; one state drives both.
- **The legend is the layer list:** each checkbox shows its glyph. A fixed caption at the bottom of the legend reads "Distances are straight-line. The map shows recorded places only; gaps are in the list."
- **Radius rings:** none by default. Concentric rings read as walkable catchments.
- **Distance display:** "350 m · straight line" in rows and the selected label. There is no ruler tool in the prototype.

### Map pin flow (founder chose it; identity confirmation recovery)

| Step | Screen | Behaviour |
|---|---|---|
| 1 | Address search, "Can't find the address?" | Two equal options: **Enter address manually** (form) and **Place a pin on a map**. |
| 2 | Pin map | Map centred on the postcode or town entered. **A fixed crosshair pin at the centre: the map moves under the pin.** Nothing is dragged, so a single tap, arrow buttons or arrow keys work (WCAG 2.5.7; W3C's own example is map arrow buttons). Live caption: "Pin is on Mill Court". |
| 3 | "Use this location" | Shows the buildings near the pin as a **list** to choose from, plus "None of these". |
| 4 | Which flat? | Manual flat or unit entry. A pin cannot tell flats apart (synthesis). |
| 5 | Confirm | A summary card: "Location: from your pin · Building: chosen by you · Flat: typed by you, not matched to a record". Buttons: Confirm or Change. The record stores the origin "user-placed pin". |

- **Accessibility alternative:** step 1's manual entry is a complete path, not a lesser one.
- **The pin map has visible controls:** `+`, `−`, and four arrow buttons with 44 px targets.
- **Prototype data:** the pin flow runs on the schematic map (Q1). It must never land on a real address.

---

## 6. Data quality and gap pattern

### Component A: `SourceLine` (one per section, and per row only when a row's source differs)

`[origin glyph] Sample · shaped like police.uk · 23 Oct 2026 · England, Wales, NI forces · About this source ›`

- The type is the body sans at 14 px, in ink at 75 % emphasis. It must still pass 4.5:1 on paper: validate it, and **do not shrink it** (doc 03 §6).
- The **origin glyph** distinguishes official dataset, user-entered, document, listing claim and plan or not-covered (doc 02 §6). The "Sample" word appears on every synthetic item (rule 1).
- "About this source ›" opens the evidence sheet.

### Component B: `StatusRow` — one shape and one wording per status

| Status | Glyph (shape carries meaning) | Wording pattern | Colour | Action |
|---|---|---|---|---|
| `recorded` | none (the content is the signal) | the value | ink | Details |
| `no-record-in-source` | **dashed open circle** ◌ | "No {thing} found **in this source**" + second line "This doesn't mean there are none." | ink on paper, dashed 1 px border around the row | Ask about this |
| `stale` | clock glyph | value shown + tag "Older: {date}" | amber `#8F560E` text tag on sage | Details |
| `source-failed` | broken-link glyph | "Couldn't load {topic} from {source}" | amber | **Retry**, Details |
| `not-covered` | map-outline glyph | "{Topic}: not yet covered in {nation}" | ink, sage panel | What we cover |

**How "no record" avoids looking like "all clear"** (rule 7, P2):
1. It is never a tick, never green, never "0", never "None nearby".
2. It keeps the same row height as a recorded item, so the gap occupies real space.
3. The dashed border reads as "unfilled" in the same way a placeholder does.
4. The second line states the limit in plain words.
5. Section summaries count gaps explicitly, for example "2 recorded · 1 no record". They never just omit gaps.

**`source-failed` vs `no-record`:** the two must never share a glyph, a colour or wording. A failed lookup is amber and offers Retry. It says "couldn't load" (doc 03 §5: "must not look like a clean result").

---

## 7. Comparing area information (up to three homes)

- **Structure:** a "Daily life and area" group *below* costs. There is one row per section from §2, a sticky first column holding topic names, and home columns in a fixed order (the order the household added them).
- **Cells:** each cell holds the L1 summary only (for example "Nearest stop 120 m, straight line"), plus its status glyph and word. A gap cell uses the same StatusRow wording and the same height.
- **Rows the fixtures make interesting:**
  - **Commute row:** B1 shows "36 min (your estimate) · limit 40", B2 shows "52 min (your estimate) · limit 40". Whether either is within the limit is shown only if the engine emits it (Q4).
  - **Crime row:** counts *per month, aligned by month* across homes. If one home's month failed (R1, Aug 2026), that cell says "Couldn't be fetched" and the month still lines up. A text note sits under the row: "Counts depend on reporting and force; they are not a rate and are not comparable as safety."
  - **School inspection row:** the framework and date are shown in every cell. If frameworks differ, a row note reads "Different inspection frameworks: outcomes aren't comparable" (Ofsted guidance via doc 02 §7).
- **No winner:**
  - no row highlight, no "best" badge, no green or red cells, no sorting of homes by a row;
  - plain trade-off statements, as doc 02 §5D suggests, come only from engine or generator outputs. AI may explain them but not compose figures.
- **Mobile:** three columns don't fit, so Compare on a phone switches to **topic cards**. Each card is one topic with three stacked rows (B1 / B2 / R…), each row prefixed with the home's short name and thumbnail. Cards are in the same order as the desktop rows, and a chip row jumps between topics.

---

## 8. Motion spec

Easing and duration values are from Material's motion tokens (M3 standard `cubic-bezier(0.2, 0, 0, 1)`, emphasised decelerate `(0.05, 0.7, 0.1, 1)`, emphasised accelerate `(0.3, 0, 0.8, 0.15)`; durations from 50 to 1000 ms, and "duration should increase as the area/traversal of an animation increases"). They are read from the Material Components for Android docs because m3.material.io did not render as text. HIG backs the intent: "Add motion purposefully", "Make motion optional", "Let people cancel motion", and avoid motion on "UI interactions that occur frequently".

| Transition | Purpose | Spec | Reduced motion (`prefers-reduced-motion: reduce`) |
|---|---|---|---|
| Sheet resting height change (drag release or grabber tap) | Shows where the content went | 300 ms (medium2), emphasised decelerate; follows the finger while dragging; interruptible | Snap to the height instantly; 100 ms opacity on the content only |
| Select place → map pans or zooms to it | Keeps place and row linked | Pan only if the marker is off-screen; ≤ 400 ms standard; never zooms out and in ("fly arcs") | No camera movement beyond a jump cut; selected marker fades its selected state in over 150 ms |
| List ↔ map switch | Same items, different view | 200 ms crossfade (short4), standard | Instant switch |
| Marker select / deselect | Feedback | 150 ms colour and ring change; scale ≤ 1.1, no bounce | Colour change only, no scale |
| Content replacing placeholders | Avoids layout jump | **Static** placeholder blocks the exact height of the rows (no shimmer); content fades in over 150 ms | Instant |

**Never animated:**
- figures counting up or ticking;
- crime counts, prices or minutes appearing one by one;
- pulsing flood alerts, pulsing markers or "live" beacons;
- risk colours;
- auto-panning tours or map rotation;
- a parallax header photo;
- a "typing" or "thinking" assistant animation (decision 0005: "no theatrical agent activity"; one quiet status line per tool call).

The MDN guidance names "scaling or panning large objects" as vestibular triggers, which is why map camera moves are the first thing reduced.

---

## 9. Accessibility (WCAG 2.2 AA)

**Model: the list is the accessible interface, and the map is an enhancement that never holds unique facts.**

**Map region**
- The map is a `region` named "Map of places near {home}. Every place is also in the list."
- It takes **one tab stop**. Arrow keys pan and `+`/`−` zoom, and visible buttons do the same (2.1.1, 2.5.7).
- **Markers are not individual tab stops.** With dozens of markers this would trap keyboard users. Instead, the list rows are the keyboard path, and focusing a row highlights its marker.
- A "Places on the map" button jumps to the list.

**Focus**
- Opening map mode moves focus to the map region's heading. "← List" returns focus to the control that opened it.
- Opening the evidence sheet moves focus to its heading; closing it returns focus to the row's "Details" button.
- The standard sheet is non-modal (no `aria-modal`) at peek and half. At full height it behaves as a page section.
- The full-screen evidence sheet *is* modal, with focus contained and Escape to close.
- **Focus not obscured (2.4.11):** the standard sheet and the sticky chip row use scroll padding, so a focused row is never fully hidden behind them.

**Grabber:** a `button` labelled "Expand list" or "Collapse list", with `aria-expanded`. Material's drag handle exposes expand and collapse to TalkBack and cycles on tap, and Apple's grabber "works with VoiceOver". Dragging is never the only way (2.5.7).

**Announcements:**
- Changing a layer or chip updates a polite live region, for example "Showing 3 sections, 11 places. 2 gaps listed."
- Retry results are announced. Map pans are not.

**Colour not alone (1.4.1):** every status has a glyph *and* words (§6). Selected markers change both fill and ring.

**Contrast:**
- **Text:** forest and ink exceed 9:1, and amber and red reach ≥ 4.5:1 on white, paper and sage, per doc 03 §6. Re-validate amber on the base map's tints.
- **Non-text (1.4.11):** marker borders, the focus ring (2 px forest plus a 2 px white halo for use on the map) and map control outlines are ≥ 3:1 against both paper and base-map surfaces.

**Targets:**
- All controls are ≥ 44 × 44 px (Apple HIG default), well above the WCAG 2.5.8 minimum of 24 px.
- Marker hit areas are 44 px. Dense pins fall under 2.5.8's "essential" exception for maps, but we don't rely on it: the list covers them.

**Text alternatives (1.1.1):**
- The static map preview has the text alternative "Map preview: this home and the nearest places in 4 categories; the full list follows."
- Cluster counts, distances and flood-area names all exist in the list.
- No fact is map-only.

**Zoom and reflow:** the list reflows at 320 CSS px. Map controls stay reachable at 200 % text size (HIG: support enlarging text by at least 200 %).

---

## 10. Assistant / MCP channel

This follows the eight agent-channel principles in synthesis.md and decision 0004, with #117 read-only first.

**Shape of a returned topic (design view; the schema is #117's):**
- `topic`, `status`, `label`, `value`, `source` {label, date, synthetic}, `coverage`, `doesNotEstablish`, and `link` back to the Vestagraph Nearby section with the item selected.
- Gaps are returned as items with a status, never as an empty array.

**How the host should render it**, steered by tool descriptions and tested by the evaluation set:
- **Text first.** One short paragraph per topic group, value then limit, with a source and date per paragraph. Example for B1 crime: "Recorded crime counts for July 2026 (sample data shaped like police.uk): anti-social behaviour 6, shoplifting 4, burglary 2. These are recorded incidents, not a crime rate or a measure of safety, and locations are approximate."
- **Gaps are said out loud:** "No childcare was found in this source; that doesn't mean there is none."
- **No images or maps in the reply.** Instead: "See these places on the map in Vestagraph ›" (hand-off for depth, principle 8).
  - MCP Apps or ChatGPT UI resources could embed a card later. That is unverified (patterns §7) and not in the prototype.
- **Forbidden in answers** (tool descriptions forbid them and the evaluation set checks for them): "safe", "unsafe", "low or high crime", "no flood risk", "good area", "value", "catchment", any total or difference not returned by the engine, and any travel time not marked as the household's own estimate.
- **Outside England:** "Area information isn't covered in Wales yet." There is no partial answer.

---

## 11. Risks and open questions for the founder

1. **Should the sample homes sit on a real map?** The sample homes are fictional (`NB` postcodes, synthetic places). Putting them on real map tiles would put made-up stops, crime counts and sold prices onto real streets, which risks rule 1 and could describe a real neighbourhood wrongly. **Recommendation: a hand-drawn "Northbridge" sample map** (a simple vector town in our map style, labelled "Sample map") for the prototype. Use real tiles only when real data arrives (stage 6, #98).
2. **Where do map positions come from?** The area fixture has distances but no positions, so markers can't be placed honestly from it. **Recommendation:** add sample map positions (on the sample map's grid) to the area data as inputs with their method, in a small follow-up to #120. The founder merges it, because it is a data-contract change.
3. **Should crime ever appear on the map?** Police.uk moves each crime to the nearest anonymous point, so dots look precise but aren't, and dots and heatmaps read as "unsafe zones". **Recommendation: never on the map.** Show a table of counts by month and category, with the neighbourhood team.
4. **Can the commute row say "within your limit"?** Comparing 36 with 40 is a calculation, and rule 2 says calculated outputs come from the engine. **Recommendation:** have the generator emit each criterion's met or not-met result for Compare and Overview. Until it does, show the two numbers side by side without a verdict.
5. **What should Nearby show first on phones?** **Recommendation: list-first, with a static map preview and a one-tap full-screen map**, per NN/g's mobile findings. Revisit only if testing shows people expect the map first.
6. **Should sold prices show on the map?** **Recommendation: markers without price labels**, with the price and date in the selected row and the list. Price-labelled pins turn a history into a "value" map. Revisit with testing.

---

## 12. Sources (all checked 11 Nov 2026)

**Guidance**
- Apple HIG, Maps: https://developer.apple.com/design/human-interface-guidelines/maps (muted style, clustering, selection styling, category filtering). Read through the HIG page data, since the page itself renders in a browser only.
- Apple HIG, Sheets: https://developer.apple.com/design/human-interface-guidelines/sheets (detents, grabber works with VoiceOver, nonmodal sheets, one sheet at a time).
- Apple HIG, Motion: https://developer.apple.com/design/human-interface-guidelines/motion. Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility (44 × 44 pt, 200 % text).
- Material motion tokens and easing: https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md. m3.material.io (https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) did not render as text, so its *web* token names need confirming.
- Material bottom sheets (standard vs modal, accessible drag handle, 48 dp): https://github.com/material-components/material-components-android/blob/master/docs/components/BottomSheet.md
- WCAG 2.2 Understanding 2.5.7 Dragging Movements: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
- WCAG 2.2 Understanding 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- WCAG 2.2 Understanding 2.4.11 Focus Not Obscured (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- WCAG 2.2 Understanding 2.3.3 Animation from Interactions (AAA, used as a target): https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- NN/g, "Maps and Location Finders on Mobile Devices" (Harley, 2014): https://www.nngroup.com/articles/mobile-maps-locations/. It is dated, but its touch findings are consistent with the guidance above.

**Official services**
- GOV.UK long-term flood risk: https://www.gov.uk/check-long-term-flood-risk ("how likely it is that an individual property will flood" is not given; flood types listed). The service's own risk wording was not seen in text and needs the visual pass.
- GOV.UK flood alerts and warnings (level names, meanings and icon descriptions): https://www.gov.uk/guidance/flood-alerts-and-warnings-what-they-are-and-what-to-do
- data.police.uk About (anonymous map points, monthly, accuracy caveats): https://data.police.uk/about/. The police.uk crime map page returned 403, so the visual pass must confirm how the public map draws counts.

**Products** (secondary or unverified where marked)
- Google Business Profile help, school reviews and ratings removed (no date on the page): https://support.google.com/business/answer/10313341. The 30 Apr 2025 date comes from search results only.
- Zillow removed First Street climate scores from listings, Nov 2025, and links out instead (Insurance Journal): https://www.insurancejournal.com/news/national/2025/12/10/850442.htm
- Zillow and Trulia stopped coloured school scores on maps, 2016. Search snippet only, as Inman returned 403: https://www.inman.com/2016/12/20/zillow-wipes-colors-school-ratings-media-coverage/ (unverified).
- Airbnb map ranking (list cards plus map pins, priced pins vs mini-pins): https://arxiv.org/abs/2407.00091 (Airbnb authors; unverified as current UI).
- Citymapper "Pick the best time to leave": https://citymapper.com/i/2571/pick-the-best-time-to-leave-and-spend-less-time-waiting (search snippet only).
- Rightmove help, sold prices: https://faq.rightmove.co.uk/support/solutions/articles/7000048760-sold-prices (states no source or caveats). The Zoopla help article returned 403 (unverified).
- Crystal Roof homepage: https://crystalroof.co.uk/ (topics, address or pin search, a crime "hotspots" map, sources listed). Its postcode pages surfaced in search show 1–10 ratings, which is the pattern we avoid.
- Google Maps saved and nearby help: https://support.google.com/maps/answer/9948049. Its Explore bottom sheet and category behaviour was not confirmed in text.

**Visual pass must confirm:**
- Apple and Google Maps sheet resting heights and category chips;
- Airbnb's split view, and pin behaviour at narrow widths;
- Citymapper's journey cards;
- Rightmove and Zoopla area panels on public pages;
- the GOV.UK long-term flood map's colours and wording;
- the police.uk crime map's presentation;
- Crystal Roof's crime map and ratings;
- Zillow and Redfin neighbourhood panels;
- that the proposed base-map tints keep amber text at ≥ 4.5:1 and markers at ≥ 3:1.
