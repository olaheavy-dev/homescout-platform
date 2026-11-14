# Pilot design review, 14 Nov 2026

**Purpose:** the founder asked for "a review of all the pilot screens, what do we need to change, add, modify, extend, polish to achieve our aim" (typed, 14 Nov 2026). The aim is the pilot's design quality bar in doc 04 §9 stage 5b: "our minimum now is to be way better than [the competitor]", for the pilot only. This page holds the **competitor benchmark checklist**, how each pilot surface scores against it, the findings, and the founder's decisions.

**How it was done:** two fresh-context design reviews ran side by side on 14 Nov 2026, using the house `design-reviewer` agent. One covered the written specifications (`docs/specs/pilot/`, `docs/specs/screens/01`, `04` and `14`, the pilot design and the site plan). The other covered the design canvas's "Pilot · public area check" page (version 90, 35 boards, rendered at 390 and 1280 px). Both compared against the competitor comparison (`2026-11-13-competitor-report-comparison.md`) and the founder's private evidence. As decided in #240, the competitor is not named here, and its paid pages are neither quoted nor described beyond what the 13 Nov comparison already records. Facts from its public website may be named elsewhere (founder, 14 Nov 2026, #241: "Keep names (Recommended)").

## Overall position
- **Already better than the competitor:** the area card (every version), the area chat, the area tools, the desktop landing page and the phone map. Each fact carries its source and date, missing data shows as missing, and the drawings are well ahead.
- **Level:** the phone landing page (nine source cards before "How it works") and the desktop map.
- **Worse:** the states board (three states against the competitor's loading and failure states) and the export (still the plain version from before FE-21).
- **The weak surface is the one every visitor sees first.** Check an area has 18 scenarios but proves only 2 of the 32 checklist items outright, and its boards have no "At a glance" block, no topic detail sheet and no desktop result. Ten boards on the pilot page still show the later home workspace (a saved home, a signed-in menu and a commute).

## The competitor benchmark checklist
Every pilot canvas board and specification passes this before the founder reviews it (doc 04 §9, stage 5b).

Each item is written so it can be tested on a screen or in a scenario. Each answers a strength or a failure recorded in the 13 Nov comparison; an item passes only if we are at least as good and do not repeat the failure.

### A. Truthful figures
| # | Item (testable) |
|---|---|
| B1 | No score, rating, band or verdict word about a place anywhere on the surface ("safe", "good", "best", "low risk", "clear", "n/100", "leads"). Tested by a scenario on that surface against one shared word list. |
| B2 | Five gap states have five different wordings and none is zero, "none", a dash beside a verdict or a clean banner: no record in this source; none found within the stated radius; Unavailable; Old; Not yet covered. |
| B3 | Every figure shows, beside it, the area it covers (postcode, street, radius, council area) and its radius. No row mixes radii without saying so. |
| B4 | Every fact shows its source, its data date and its label, and the source is one tap away. |
| B5 | Crime is counts by month and category for a stated radius. Never a rate per resident, never a band, never on a map. |
| B6 | No figure is worked out outside a tested module, and each calculated value has a one-line "How we got this". |
| B7 | No placeholder or internal text is ever visible ("NO DATA", "null", "undefined", "NaN", internal names). A stored value outside its source's documented range is withheld as Unavailable. |
| B8 | The same fact has the same value, date and label on the page, the report, the chat, the assistant tools and the card. |
| B9 | Outside England: "Not yet covered", with no England-only dataset applied. A search that crosses the border says places beyond it may be missing. |
| B10 | "What this doesn't tell you" is at least as large and as high-contrast as the fact it qualifies, and never collapsed where it changes the meaning. |
| B11 | Sample or illustrative content is labelled as a sample. No trend, average or median from a handful of sales; single recorded sales only. |
| B12 | AI: every claim is sourced or says "not known"; AI never calculates; no "confidence" label; a question it must not answer still gets a useful sourced reply, not a dead end. |

### B. Clearer on a phone
| # | Item |
|---|---|
| B13 | The result is one short row per topic; the whole summary is a short scroll, not 35 stacked sections. |
| B14 | Detail opens in a sheet with a visible Close; the phone's Back closes it; focus returns to the row; the open topic can be linked. |
| B15 | No sideways scrolling at 320 to 390 px; tables reflow into cards (WCAG 1.4.10). |
| B16 | Theme follows the device with a visible switch; an in-page text-size control; nothing lost at 200% zoom; body text and contrast meet WCAG AA in both themes. |
| B17 | Colour is never the only signal (icon and text too); touch targets at least 24 px; every map has a list; a tap card replaces hover. |
| B18 | Everything works by keyboard; focus is managed on open and close; loading and results are announced; reduced motion is respected. |

### C. Quicker to act on
| # | Item |
|---|---|
| B19 | The postcode box is the first control; one step to a result; no account; forgiving input (case, spaces). |
| B20 | "At a glance" comes first: what was found, what is unknown or unavailable, what to check in person, questions to ask, each count linking to its items, plus a coverage line (how many topics returned facts). |
| B21 | Every topic ends with what to do next: a question to ask, a thing to check in person, the official link. |
| B22 | Every state gives the cause, a reassurance and one action: loading, not found, service down, rate limit, budget cap, offline. |
| B23 | Share a link and a designed report: cover, At a glance, contents, topic pages, sources and limits, a footer on every page, readable in greyscale at a set minimum print size. |
| B24 | The map has category filters, a legend, pins that match the list order, and a line saying what distances are measured from. |

### D. About the home, where the pilot covers it
| # | Item |
|---|---|
| B25 | Energy certificate by its number (DA-09): open building fields only, no address shown, the number never logged or put in a link. |
| B26 | For each home fact the pilot cannot show (council tax band, tenure and title, long-term flood if unlicensed, ground and mining), a labelled official route. |

### E. Free public facts, no account
| # | Item |
|---|---|
| B27 | No locked, blurred or teaser content; no sign-up prompt; account features appear only as "coming next", never as an active control. |
| B28 | The postcode is never in a query string, path or log; nothing is stored in the browser before the visitor opts in; no third-party request without the visitor's action. |

### F. Other bars from the evidence
| # | Item |
|---|---|
| B29 | One anatomy for every topic, in one order. |
| B30 | Each topic the competitor shows that matters to a buyer or renter is either covered or explicitly routed: long-term flood, rents, planning constraints, mobile by network, noise and ground. |
| B31 | Two postcodes side by side with no winner, no "leads" and no sideways scroll. |
| B32 | Loading shows skeletons with a status; an AI answer shows a writing state. |

---

## 2. Scorecard

## Scorecard of the specifications
Key: **Y** meets (a scenario proves it), **P** partly (a rule or a related scenario exists, the proof for this surface is missing), **X** missing, **–** not applicable. Columns: **L** Landing (`01-landing.feature`), **A** Check an area (`14-check-an-area.feature`), **N** Nearby topics (`04-nearby.feature`, the topic summary the pilot reuses), **M** Map (no file of its own: AREA-09, NEAR-11, NEAR-12, NEAR-15 and the information architecture line 142), **C** area chat, **T** area tools, **K** area card (both versions, Expand, phone preview).

| # | L |
|---|---|---|---|---|---|---|---|---|
| B1 no verdicts | P | X | P | P | Y | P | Y | LAND-10 names three words only; nothing on A; NEAR-08, NEAR-14; CHAT-11 to 15, 39 to 43; TOOLS-11, 18, 40 cover descriptions, not result text; CARD-08 |
| B2 five gap states | – | P | Y | X | Y | Y | P | A has not found, Unavailable, not covered (AREA-05, 07, 08, 14) but no "none found within", "no record" or "Old"; CARD-14 only covers no places |
| B3 area and radius | P | X | P | X | P | Y | P | Only TOOLS-07, 08, 11, 30 prove it; AREA-13 proves the origin only |
| B4 source, date, label | P | P | P | X | Y | Y | Y | LAND-08; AREA-12 (printout only); NEAR-09; CHAT-07; TOOLS-05, 08, 20; CARD-03, 07 |
| B5 crime as counts | – | X | P | Y | P | P | Y | NEAR-12 and TOOLS-11 give counts; nothing forbids a per-resident rate |
| B6 tested maths, how we got this | P | P | P | – | Y | Y | Y | LAND-06, AREA-13; CHAT-13, 16; TOOLS-29; CARD-01, 37. "How we got this" (FE-24) has no scenario anywhere |
| B7 no placeholder text | X | X | X | X | P | P | X | Only error results: CHAT-36, TOOLS-27 |
| B8 same on every surface | X | X | – | X | P | P | Y | CARD-02, CARD-06 only |
| B9 outside England | Y | P | Y | – | Y | P | – | LAND-02; AREA-01, 02, 08, 16; NEAR-04, 10; CHAT-01, 02; TOOLS-02, 41. Border searches unproven |
| B10 limits as prominent | P | X | Y | X | P | P | P | NEAR-13 is the only proof, and it is a home-screen scenario |
| B11 samples labelled | P | P | – | – | – | Y | – | LAND-04, 09 label the example; the hero (LAND-06) is not labelled; AREA-12 says "Sample data" for every postcode; TOOLS-12, 35 |
| B12 AI behaviour | – | – | – | – | P | Y | – | CHAT-07, 08, 16; but the commonest question ends in a dead end (finding M1) |
| B13 short list | Y | P | P | – | Y | – | Y | LAND-11; NEAR-06; CHAT-06; CARD-36. The pilot's own topic list is not written down |
| B14 sheet, Back, focus, link | – | X | X | X | P | – | P | NEAR still routes to a sub-page; CHAT-28; CARD-22, 23, 38, 40. Back and deep link unproven everywhere |
| B15 no sideways scroll | P | X | X | X | P | – | P | No reflow scenario on any surface |
| B16 theme, text size, zoom | X | X | X | X | X | – | X | FE-23 has no scenario |
| B17 colour, targets, list | P | P | Y | P | – | – | P | LAND-11; NEAR-11; CARD-03, 30. No target-size scenario |
| B18 keyboard, screen reader | P | X | X | X | P | – | Y | LAND-01 label only; CHAT-28, 29; CARD-04, 05, 15, 23, 27, 28, 41 |
| B19 postcode first | P | P | – | – | – | – | – | LAND-01, 03, 11, 12; AREA-03, 04. Forgiving input unproven |
| B20 At a glance | – | X | – | – | P | P | – | Only CHAT-10 and TOOLS-15 (questions from gaps) |
| B21 what to do next | – | P | P | – | P | P | – | AREA-18 (link rules); NEAR-08; CHAT-08; TOOLS-15, 28 |
| B22 every state | P | P | P | X | Y | Y | P | A lacks service down, rate limit, cap, timeout; CHAT-19 to 24, 30, 36; TOOLS-23, 24, 27, 37 |
| B23 share and report | – | P | – | – | – | – | – | AREA-12, 16, 17 only; FE-21 and Share a link unspecified |
| B24 map | – | – | – | X | – | – | Y | AREA-09 is the only page-map scenario; CARD-01, 03, 24, 30 |
| B25 energy certificate | – | X | – | – | – | – | – | DA-09 has no scenario |
| B26 routes for the rest | – | P | P | – | – | P | – | AREA-18, NEAR-08, TOOLS-28 give link rules, not the list |
| B27 nothing locked | Y | Y | – | – | Y | Y | Y | LAND-05; AREA-11; TOOLS-17 |
| B28 privacy | Y | P | – | X | Y | Y | Y | LAND-03; AREA-03, 15, 17, 18; CHAT-25 to 27, 34, 35; TOOLS-25 to 28; CARD-11, 12. No log scenario for the page's own API; map tiles undecided |
| B29 one anatomy | – | X | P | – | – | – | – | NEAR-06 fixes the row, nothing fixes the detail |
| B30 breadth or route | – | X | – | – | – | – | – | Register lines only (FE-25, DA-10, DA-11) |
| B31 compare | – | X | – | – | – | – | – | Unspecified |
| B32 loading | – | Y | – | X | Y | – | – | AREA-06; CHAT-30 |

**Reading the scorecard.** The chat, the tools and the card are strong: their privacy, sourcing and accessibility scenarios are the best in the repository. The weak surface is the one every visitor sees first: **Check an area has 18 scenarios and proves 2 of the 32 items outright.** It leans on the home workspace's Nearby file for its topics, and has no scenario of its own for verdict words, crime, radius, stale data, a sparse area, keyboard use or a phone.

**The pieces with no specification yet** (all X by definition). Each must carry these checklist items when written:

| Piece | Checklist items it must prove |
|---|---|
| Topic detail view (FE-20) | B1 to B7, B10, B14, B15, B17, B18, B21, B29 |
| At a glance and priorities (FE-22) | B1, B2, B6, B20, and "never a total" |
| Designed report (FE-21), printout update | B1, B2, B4, B7, B8, B11, B23 |
| Theme and text size (FE-23) | B15, B16 |
| How we got this (FE-24), About the data | B4, B6 |
| Energy certificate (DA-09) | B25, B28, B2, B22 |
| Wave 1 extras (questions, check in person, broadband and mobile, sold prices) | B2, B3, B11, B20, B21, B30 |
| Wave 2 extras (walking times, buses, school demand, council tax, family view, planning, inspections, air quality) | B1, B3, B6, B30 |
| Compare two postcodes | B1, B15, B17, B31 |
| Explain this, Share a link, Recent postcodes, Report a problem | B22, B28, B12 |
| Public pages (How it works, About the data, privacy, accessibility) | B4, B16, B18, B28 |
| Map view | B17, B24, B28 |
| AI evaluation set (AI-03) | B1, B12 |

---
## Findings
Two lists: one per review. The specification review found 60 (8 change, 30 add, 8 modify, 7 extend, 7 polish; 28 of them must-haves). The canvas review found 47 (9 change, 13 add, 10 modify, 6 extend, 9 polish). Many describe the same gap from both sides.

### Wrong now (P1), fixed first
| Where | What was wrong | Fix |
|---|---|---|
| Canvas, Map desktop | Church, mosque and gurdwara all shown at 550 m; the sample data says 600 m, 950 m and 1.3 km | Canvas fix |
| Canvas, Check an area and Nearby phone | "Places of worship" carried "1 older inspection", copied from Schools | Canvas fix |
| Canvas, ten Nearby, Schools and Map boards | A saved home, signed-in menu, commute and demo strip on the pilot page | Redraw for a postcode; originals moved to "Home workspace (later)" (decision 2 below) |
| Canvas, export | Places of worship missing; "Places off the map: 9" read as a count | Canvas fix, then the designed report (FE-21) |
| `04-nearby.feature`, site plan | Topic detail opened as a separate page, against FE-20 | This pull request |
| Specifications | Map, topic and chat claimed the same space with no rule | FE-26, this pull request |
| `14-check-an-area.feature` | "Couldn't fetch · Try again" for a live fetch the pilot never makes; postcode service down shown as "not found" | This pull request |
| `14-check-an-area.feature` | The printout said "Sample data" for every postcode | This pull request |
| Specifications, design | Flood warnings called "live" though they come from a stored copy, with no age limit | DA-12, this pull request |
| `area-chat.feature` CHAT-15 | "Is this area safe?" always ended in an error | AI-11, this pull request |
| `01-landing.feature` LAND-06 | The landing hero's made-up town had no "sample" label | This pull request |

### Missing, in the design batches that follow
- **First batch (canvas, then specifications):** At a glance; the topic detail sheet and side panel (FE-20) with "How we got this" (FE-24), questions to ask and checks in person; priorities (FE-22, 0053); the desktop result for Check an area; the missing states (loading, postcode service down, sparse area, stale source, all sources down, offline, AI error); area and radius beside every figure, and source and date on every list row; an entry to the chat from the phone result; theme and text size (FE-23).
- **Then:** the designed report (FE-21) and Share a link; the energy certificate by its number (DA-09); wave 1 extras; the street map (after FE-03's tile pricing); the public pages; Explain this, Recent postcodes and Report a problem; the chat and tools fixes with the AI evaluation set (AI-03); wave 2 and Compare.
- **Polish:** touch targets under 44 px on the map and chat controls; a clipped hero tooltip and chat placeholder; dark-mode dividers; the Schools source date; one vocabulary for gaps.

## Founder decisions, 14 Nov 2026 (prompt windows)
| # | Question |
|---|---|---|---|
| 1 | Topic, map and chat on the result | "One at a time (Recommended)" | FE-26 |
| 2 | The ten home-context boards | "Redraw, move originals (Recommended)" | This page; canvas |
| 3 | Wales, Scotland and Northern Ireland | "Whole page 'Not yet covered' (Recommended)"; the comparison's "topic by topic" describes the coverage registry, not the screen | This page; 0046 |
| 4 | "Is this area safe?" | "Fixed, reviewed reply (Recommended)" | AI-11 |
| 5 | Street map tiles | "Own tiles, price it first (Recommended)" | FE-03 |
| 6 | Flood warning age | "Show time; Old 1h, off 1 day (Recommended)" | DA-12 |
| 7 | Sold prices | "Street and type only (Recommended)" | DA-13 |
| 8 | Explain this | "Pre-written only (Recommended)" | AI-12 |
| 9 | Units | Typed: "use the unit of measurement of the country"; for England, "Miles, e.g. '0.3 miles' (Recommended)" | FE-27 |
| 10 | Limits on the short list | "One line where it matters (Recommended)" | FE-28 |
| 11 | Where "meets or misses" is worked out | "Send limits to server", over the agent's recommendation of a tested browser function | [0053](../decisions/0053-priority-limits-checked-on-the-server.md), SE-04 |
| 12 | When priorities are drawn | "First batch", over the agent's recommendation of the second batch | This page; status file |

Also asked: whether the existing home page needed a review (founder, 14 Nov 2026). The landing page is part of the pilot and was reviewed above. The canvas's "Home workspace (later)" page waits for its own turn, under the pilot-only rule.
