# Design Brief: Vestagraph clickable prototype

**Phase 2 of the design flow (decision 0031). Written 11 Nov 2026.** It builds on:
- doc 02 (product) and doc 03 (screens, stories, required states, §6 visual starting point);
- the seven agreed design principles (`research/synthesis.md`);
- the area-display decisions (`research/area-display-summary.md`);
- the founder's design-flow interview of 11 Nov 2026.

The founder's feedback on the first preview set the bar: "it looks like a UI created by AI, it needs a high level UI/UX design touch".

## Problem

Choosing a home to buy or rent is a big decision made with half the facts. The listing shows a headline price or rent, but the real cost is scattered across service charges, ground rent, bills, deposits and fees. Some of it is missing, some is wrong, and some only appears in documents weeks later. Daily life is guesswork:
- the commute;
- schools;
- whether the street floods;
- what's actually nearby.

People keep it all in their heads, in screenshots and in group chats. They don't know what to ask, who to ask, or whether the reply they got answered anything. Couples and housemates make the decision together but see different fragments. They end up deciding on a feeling, then find out what it really costs too late.

## Solution

Vestagraph is a calm, private workspace for each home you're considering. It keeps everything known, missing, asked and answered about that home in one place. It works out what the home would really cost you each month and up front, and is honest about what's still unknown. Alongside the cost, it shows whether daily life would work: your commute, schools, transport, shops, flood warnings and recorded crime. As replies and documents arrive, the picture updates and shows exactly what changed and why. You can then compare two or three homes side by side, with the same assumptions, and decide together without a fake "winner".

It should feel like a trusted, knowledgeable friend who works in property: warm, plain-spoken, careful with facts, and never pushy.

## Who it's for

**This prototype's own audience** (decision 0045): the founder and the AI coding agents. It is the vision and reference build for the real product, and it is used privately in the stage 6 validation sessions. It is **never a public demo**. Because agents build from what they can see, every state must be visible and reachable: by URL (`?step=n`), in the component gallery and in the executable specs.

**The product's users**, whom the design serves, all three equally (founder, 11 Nov 2026):
- **A household deciding together:** two people, or housemates, not property experts, often comparing on their phones.
- **A solo first-time buyer,** anxious about hidden costs and leasehold.
- **A solo renter,** comparing "bills included" offers and areas.

Buying and renting have equal prominence everywhere (doc 02 §4).

## Success

**Clarity first, at portfolio-grade polish** (founder). In a five-minute walk-through, a first-time viewer should:
- understand a home's real monthly and upfront cost;
- see what's still unknown and what to ask next;
- understand how a reply changed the decision;
- say they'd trust it with their own move.

This is tested in the stage 6 study (doc 02 §10). The craft must match top consumer products, never "generated" UI.

## Experience Principles

Three principles that resolve the main tensions. The seven agreed principles in `research/synthesis.md` still apply under them.

1. **Honest over reassuring.** Show what's known, its source and date, and what's missing, even when a clean answer would feel nicer.
   - A partial total says "so far" and names what's left out.
   - Missing is never £0, and "no record in this source" never looks like "all clear".
   - No verdicts, scores, "verified" or "safe" (rule 4, rule 7).
2. **Calm by default, depth on request.** The first view answers one question in plain words. Detail is one deliberate tap away and never pushed.
   - One hero figure per screen and short lists.
   - "How this was worked out" sits in a disclosure. Caveats stay visible; the working is optional.
3. **The household decides.** The product lines up evidence and trade-offs and proposes next steps; people choose and confirm.
   - No winner in Compare.
   - Every change to a record (a confirmed reply, a cost assumption) is an explicit, attributed confirmation.
   - Area information sits alongside cost, never ranked into a "best home".

## Aesthetic Direction

- **Philosophy:** **Scandinavian + Editorial** (founder).
  - Scandinavian warmth with restraint across the workspace: functional beauty, soft natural colour, accessible by default.
  - Editorial craft for public pages and key moments (the landing page, the home overview header, decision impact): typography does the heavy lifting, generous space, each key screen composed like a magazine spread.
- **Tone:** warm, calm, assured and plain. **Voice:** British English, second person ("you"), short sentences, no jargon or exclamation marks, honest about unknowns ("We don't know this yet").
- **Reference points:**

  | Reference | What to learn from it |
  |---|---|
  | **Monzo / Starling** | Confident money presentation and friendly clarity around figures |
  | **Airbnb** | Editorial photography, generous space, map and list browsing, trust signals kept soft |
  | **Linear / Things** | Precision in type and spacing, quiet UI, focused tracking (for Questions) |
  | **Apple Maps / Weather / Health** | Layered information, beautiful data presentation, motion with purpose |
- **Anti-references:**
  - **property portals:** ad-heavy listing grids, urgency, "premium listing" badges;
  - **generic AI SaaS:** purple gradients, Inter everywhere, identical card grids, sparkle icons, chatbot-first;
  - **government forms:** we borrow GOV.UK's clarity, not its bureaucratic coldness.
- **Typography: Bricolage Grotesque + Geist** (founder, 11 Nov 2026, chosen from five pairings drawn side by side; it replaces the earlier serif direction with Fraunces).
  - **Bricolage Grotesque** (weight 600, optical size set per size, tight tracking) for titles, the display headline, step numbers and the wordmark (700): contemporary and confident, with warmth.
  - **Geist** with tabular figures for UI, numbers and data. **Not Inter**: too associated with generated UI.
  - The type scale, character rules (curly quotes, non-breaking "400 m", balanced headlines) and money style (pence a step smaller and lighter) are on the craft sheet and in `tokens.css`.
- **Colour:** start from doc 03 §6:
  - deep forest `#153F35` for primary actions and brand moments;
  - ink `#182923` for text;
  - a **radiant light page**: clean near-white `#FBFAF7` under a soft wash of mint, sky and sunrise light, with crisp white working surfaces (founder, 11 Nov 2026; replaces warm paper `#F7F5EF`);
  - muted sage `#DCE7DD` as a supporting tone;
  - amber `#8F560E` for attention;
  - restrained red `#A33636` only on specific supported findings.

  **Colour roles in both themes** (founder, 11 Nov 2026): forest (light) or mint (dark) = act; **slate** (`#3A6079` light, `#93B8CE` dark) = guide the eye (eyebrow labels, step numbers, rings, the changed-line highlight, "coming next" outlines); amber = warning, nothing else; **clay only for the hearth** in the mark and drawings. Clay labels were dropped in light because clay and amber were almost the same colour (1.04:1).

  **Shine** (founder, 11 Nov 2026): light and material, never new hues. Glossy white cards with a lit top edge and forest-tinted shadows, a gem-like primary button, a frosted header; in dark, lit edges, a soft sheen, one mint glow on the one thing to press, a slate spotlight and a faint dot grid. Glass turns solid under reduced transparency; headlines turn solid under increased contrast and in print.

  Colour roles, not raw hex, come from the tokens phase. **Both themes ship** (founder): dark mode is a near-neutral charcoal with off-white text, not an inverted light theme, and every contrast is checked in both. **Dark colour roles** (founder, 11 Nov 2026, after two passes): near-neutral charcoal layers; mint for actions, links and the border that marks a selection (selection never relies on fill alone); **slate blue** (`#93B8CE`) as the one complement, only for eyebrow labels, step numbers, the hearth and ring in drawings and "coming next" outlines, with its tint behind drawings only; amber only for warnings. Tinted panels stay in the light theme, where paper carries them; in dark they compete, so they turn neutral. The demo strip is the exception: in dark it sits on the slate tint with a slate outline, so it still reads as a demo control.
- **Texture and imagery:**
  - **Photography** (founder, 11 Nov 2026):
    - **atmosphere photos** generated with ChatGPT and recorded in `docs/assets/README.md`: on the landing, a terraced-street band and a kitchen-table photo beside the FAQ; later, a high street (About the data), a park (Nearby empty state), moving boxes (404 or onboarding) and a home viewing (Viewings empty state). No visible caption (founder decision, 11 Nov 2026): honest alt text and a footer line, “Some photos on this site are AI-generated illustrations”; OpenAI's publication policy is re-checked before the public launch and a visible label restored if it requires one. None sits next to a specific home, postcode or result;
    - **a home's own photos** come only from the user (doc 03 §7); never photos copied from listings (decision 0028);
    - no photos on area results, where a street photo would imply it shows that place.
  - **Custom illustration, layered editorial style** (founder; richer pass 11 Nov 2026: layered scenes with soft light from the top left, gradient paper, cast shadows and a fine grain): paper texture, a print feel, limited palette (forest, sage, ink on paper, plus the complement for the hearth and ring: clay in light, slate on the slate tint in dark), like magazine spot illustrations. It's used for empty states, onboarding, the "not yet covered" state, the drawn Northbridge sample map, **every landing section below the hero** (How it works, Honest by design, Coming next, the FAQ) and one spot drawing per main app screen (What changed: the listing figure replaced by the management pack; Costs: a house, a slip and dashed gaps; Nearby: a distance ring; Compare: two homes on one level line). Drawings are decorative, with a text alternative, and never carry information the text doesn't. One consistent style guide is needed before any illustration is made.
  - A subtle paper grain may appear on editorial surfaces, never behind data.
- **Money visualisation:** **cards per category** (founder), held to strict rules so it doesn't become a dashboard:
  1. The total comes first: one large figure, its period, and a "so far" or "partial" label that names what's missing.
  2. Category cards share one quiet card style: hairline border or tonal surface, no stacked shadows, consistent padding, figures right-aligned in tabular numbers.
  3. Missing or unknown categories are **dashed cards with the words "Missing, not £0" or "Not calculated"**. They never show a zero and never sit at the bottom out of sight.
  4. Upfront cash is a separate section, never mixed with monthly costs.
  5. There are no pies or donuts, and no animated counters.
- **Motion:** quiet and purposeful (decision 0005, research §8). There are about five transitions:
  - the sheet expanding;
  - list and map changing over;
  - the map moving to a selection;
  - disclosure;
  - the decision-impact highlight.

  Each takes 150–400 ms, with a cut or fade under reduced motion. **Figures never count up, bounce or animate**, and risk colours never pulse.
  - **Public pages only, a deliberate extension of research §8's five transitions** (founder, 11 Nov 2026): the hero's distance ring draws once on load, places fade and settle in on the How it works drawing (no overshoot), and sections rise gently as they enter. Each plays once; the 600 ms ceiling (`--duration-slower`) applies only to these. Entrances use transform and opacity only, so they cause no layout shift (CLS budget, B18), and the static hero image is never hidden at first (LCP budget). All of it is off under reduced motion. The app screens keep the five transitions; their spot drawings rise in with the section, within the same rules.
- **The hero moment, decision impact:** before and after, explained.
  - The old and new figures sit side by side, and the changed line is highlighted with a short fade.
  - One sentence says why, with the source: "The management pack shows £3,720 a year, not £2,400."
  - The affected comparison and the questions still open are listed underneath.
  - It should be the most beautiful, most considered screen in the prototype.

## Existing Patterns

- **Code:** no frontend exists yet; the Next.js app starts in stage 5. There are no components, Tailwind config or Storybook.
- **Typography:** none in code. Doc 03 §6 asked for an editorial serif plus a clear sans; the founder chose Bricolage Grotesque + Geist instead (11 Nov 2026, see above).
- **Colours:** doc 03 §6, the palette above, contrast-checked for text on white, paper and sage.
- **Spacing:** none defined. The tokens phase sets an 8 px base scale.
- **Data:** every figure comes from `packages/fixtures/generated/costs.json` by figure ID, and every input and area item from `packages/fixtures/data/` (rule 2). The UI never calculates.
- **Specifications:** Gherkin features in `docs/specs/` (decision 0043) define behaviour, and the screens must satisfy their scenario IDs.

## Component Inventory

All components are new.

| Component | Status | Notes |
|---|---|---|
| App shell: desktop top bar, mobile bottom navigation | New | Doc 03 §3: My move · Homes · Compare. Home tabs: Overview · Nearby · Costs · Viewings · Questions · Documents · Activity. Mobile bottom nav: Overview, Nearby, Costs, Questions |
| Brand mark and wordmark | New | **Contour home** (founder's choice of four concepts drawn on the design canvas, 11 Nov 2026): three nested roof lines like map contours with a hearth at the centre; a primary mark (48 px and up) and a compact two-contour mark (32 px and below), beside the Bricolage Grotesque 700 wordmark. Trade-mark clearance (0009) and the asset register (rule 5) come before use |
| Landing hero, search first (0046) | New | The postcode box with the sample 3D map and a summary card. The private prototype's example page shows the two example homes (buy and rent) with equal weight |
| Address search and identity confirmation | New | Combobox with manual selection, never a silent postcode-to-flat match. Includes the map pin flow (founder) and a "can't find it" route |
| Home header | New | Photo thumbnail, address, mode, sample-data label |
| Hero figure | New | Large tabular figure, period, "so far" or partial label, budget line from the engine |
| Cost category card | New | Status variants: calculated, included, missing, not calculated, conflicting |
| Status tag and source line | New | One pattern everywhere: recorded, no record in this source, old, unavailable ("couldn't fetch this time"), not yet covered, missing not £0 |
| Gap card | New | Dashed outline plus "this doesn't mean there are none" |
| Nearby sections and rows | New | List first. Getting around, everyday places (including healthcare, police stations and childcare), schools (framework and date), flood, recorded crime, sold nearby |
| Map view and bottom sheet | New | MapLibre, the drawn Northbridge sample map, markers in one neutral colour with the home pin in forest. Selection stays in sync with the list. Crime is never on the map, and sold-price pins have no price labels |
| Crime counts table | New | Counts by month and category, "not a safety rating", neighbourhood team |
| Flood panel | New | The Environment Agency's warning wording, the surface-water note and the long-term checker link |
| Compare (table on desktop, cards on mobile) | New | Up to three homes. Costs and daily life aligned. Unknowns visible. No winner |
| Decision impact | New | Before and after, explained. The hero moment |
| Questions list, question detail, reply check | New | Status (to ask, sent, partially answered, reply needs checking, answered), recipient role, simulated-send label |
| Evidence sheet | New | Full-screen on mobile. Switch between the original document and the findings |
| Viewings note and photo | New | Mobile, turn an observation into a question |
| Empty, loading and error states | New | Skeletons, never fake data. Illustrated empty states |
| Theme switch (light and dark) | New | Both themes ship |
| Illustration set | New | Textured editorial style guide first; assets go in the asset register |
| Component gallery (`/gallery`) | New | Every component in every state, light and dark, using fixture data. The agents' visual dictionary and the design-review baseline (decision 0045, #150) |

## Key Interactions

- **Confirming the exact home:** the address search shows matching units. The user picks one, or drops a pin, or chooses "can't find it". The home overview opens with its gaps visible. WALES-1 shows "not yet covered" with an illustration.
- **Nearby on a phone:** a list of sections with a small map preview. Tapping it opens a full-screen map with a bottom sheet (peek, half, full). Selecting a row highlights the marker and the reverse. Focus and selection survive switching between list and map.
- **Costs:** the hero figure, then category cards. Tapping a card shows its working, source and period. A missing card offers "Ask about this", which creates a question. Upfront cash is separate.
- **Questions:** draft a question from evidence, copy or export it, and record it as sent (labelled as a simulated action). Attach a reply. The reply-check screen shows the reply, its source and what's still uncertain. The user confirms explicitly.
- **Decision impact:** when a confirmed reply changes an assumption, the user sees the before and after with the reason, the changed comparison and the questions still open. A quiet highlight shows the change; nothing animates the figures.
- **Compare:** add up to three homes. Rows are aligned, unknowns stay visible and no winner is chosen. On a phone, it's a swipeable card per topic.
- **Theme:** light and dark, following the system setting, with a manual override.

## Responsive Behaviour

**Mobile first** (founder): designed at 375–430 px first, then scaled up.
- **Phone:** bottom navigation, a compact home header, Nearby list first with a full-screen map and bottom sheet, full-screen evidence sheets, and Compare as cards.
- **Tablet (768 px):** two columns where useful, for example the Costs hero next to the categories.
- **Desktop (1280 px and up):**
  - top navigation and home tabs;
  - Nearby as a list column (about 440 px) next to a sticky map;
  - Compare as an aligned table;
  - decision impact as a composed two-column before-and-after layout.

## Accessibility Requirements

- **Standard:** WCAG 2.2 AA in **both themes**. Text contrast at least 4.5:1 (3:1 for large text and UI parts), checked in context on paper, white, sage and charcoal surfaces.
- **Colour:** never the only signal. Every status has words and an icon.
- **Keyboard:** everything works by keyboard. Map markers are not tab stops; list rows are the keyboard path, and every map fact is also in the list. Focus moves into and out of sheets and dialogs in order, and focus is always visible.
- **Screen readers:** semantic structure (headings, landmarks, tables with headers). Selection changes are announced. Every figure is read with its period and status ("one thousand five hundred and thirty-eight pounds thirty-seven a month, partial").
- **Touch:** targets at least 44 px.
- **Motion:** honours `prefers-reduced-motion`.
- **Language:** plain English. No jargon without an explanation.

## Out of Scope

- Real data, live APIs, accounts and sign-in. Sign-in is simulated; the prototype runs on the fixtures (IN-01).
- Payments. The free/paid boundaries are shown as labelled, simulated limits (doc 02 §8).
- Building the in-app assistant chat or the MCP server. The assistant's look is designed in #78, and the build is stage 6.
- Journeys for Wales, Scotland and Northern Ireland beyond the "not yet covered" state.
- The final logo files and trade-mark clearance (0009). The working mark, Contour home, is in scope as a design asset; production SVGs go through the asset register first (rule 5).
- Stamp duty, legal fees and home-to-home differences until the engine produces them (BE-27, #96 and #147). Until then the screens say "not calculated".
- Native apps.
- Public release: no public hosting, visitor privacy notice (SE-02 part 1) or analytics (FE-05). The prototype is private (decision 0045).
