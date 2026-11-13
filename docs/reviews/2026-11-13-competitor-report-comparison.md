# Competitor report comparison, 13 Nov 2026

**Purpose:** the founder asked to see a competitor's designs, reports and layouts "and see where we can go better", then: "We need to be better than [the competitor] … whatever specs we have built needs to be reviewed thoroughly" (founder, typed). This page records what was observed and what it changes for Vestagraph.

**Method:** on 13 Nov 2026 the agent used the founder's Chrome to view the website of a UK area-report product. It looked at the public pages and the free preview first. The founder then created a free account and bought a one-day pass. With the pass, the agent opened:
- full area reports for eight postcodes in England, Scotland, Wales and Northern Ireland;
- one property overview, for an address the founder chose;
- an area comparison;
- the "Find an area" and "Find nearby" searches;
- the account, usage and saved-report pages;
- three report PDFs.

Everything below was seen on the competitor's own pages that day, so it is **[F]** (seen on the product's own page) throughout. The competitor's terms of use were not read before viewing. The competitor is named only in the founder's private research notes (founder, 13 Nov 2026, prompt window: "Anonymise the paid details (Recommended)"), because these observations come from paid, signed-in pages. Screenshots and PDFs are kept privately on the founder's machine and are not committed: they are the competitor's copyright, and the repository is public (rule 5). Quotes are kept short. Figures quoted are the competitor's outputs, recorded as observations, not as facts about the places.

## What the competitor offers (observed)
- **Area report:**
  - a satellite map with layers you can switch on and off;
  - an "AI intelligence score" out of 100, with verdict tags (for example "Safe area", "Excellent healthcare") and four section scores;
  - an "AI verdict" summary;
  - about 35 sections, each with a source line, a headline status, a map focused on that topic, a list and caveats;
  - a sticky row of section links across the top.
- **Property overview (one address):**
  - portal listing history (from Home.co.uk);
  - tenure, the council tax band and charge, floor area, title number;
  - an automated sale estimate with a range and comparable sales;
  - the energy certificate with upgrade costs.
- **Comparison:** two postcodes across 12 categories. The headline is "Neither area leads", but each category is marked "A leads", "B leads" or "Not decided", and the page adds "Area A suits people prioritising …".
- **Find an area:** plain words become filters and areas are ranked with a "match score out of 100". **Find nearby:** plain words become place types on a map with distance rings, and the rings are explained on the page.
- **PDF:** an A4 report (47 pages for one postcode) with a dark cover and a map, a contents page in five chapters, a one-page "screening view", chapters, and a final page of sources, limitations and recommended next checks.
- **Account:**
  - theme (System, Light, Dark) and text size (three steps);
  - download your account data (JSON), request deletion;
  - usage with credits, a spend chart and recent activity;
  - saved and pinned reports kept "on this device";
  - a watchlist ("refresh to keep prices and school data current").
- **Onboarding:** "Which areas do you know?" and "What brings you here?" (buy, rent, invest, research, advise).
- **Pricing:** one-off passes, with no subscription. The free tier is limited, and full reports, comparisons and PDFs need a pass.

## Problems we observed in its output (13 Nov 2026)
These show what a careful buyer or renter would notice, and which of our rules prevent each:

| Observed | Example | Our rule or decision |
|---|---|---|
| Crime as a rate per resident in busy areas | SW1A 2AA: "3,713.7" crimes per 1,000 and "Very high crime area"; a Peak District village (S33 8WN) and central Cardiff (CF10 3RB) also "Very high crime area" | Counts, never per-resident rates; no "safe" words (rule 4, doc 02 §7) |
| Verdicts despite missing data | EH1 2NG: crime "unknown", education "—", overall "Below average 34/100"; BT1 5GS "Poor 25/100" | Missing never shown as a value (rule 7); "Not yet covered" per topic outside England (rule 6, coverage registry) |
| Impossible or out-of-range figures | "Rank 42,862 of 32,844"; volatility "Score 57 / 10" | Calculated figures from one tested module (rule 2) |
| Internal text shown to users | "Built NO DATA!"; "final_file_generated_alias" | A scenario must forbid placeholder text (gap; see below) |
| One coarse figure applied to many places | "Find an area", Sheffield: every candidate showed crime as "Area-level · Sheffield" with 100/100 (our reading: one city-wide figure) | Every figure shows the area it applies to (pilot design, "Countries support different things") |
| Verdict labels from their own cut-offs | "Safe area" at 41.4 per 1,000, from thresholds on the page ("< 60: safe") | No scores or verdicts; the visitor's own limits (FE-22) |

## What it does well, and what we take from it
1. A repeated layout for each topic: a headline, a source line, a topic map, a list with "show the other N", caveats and "what to do next". → FE-20 needs this shared layout specified.
2. Section links across the top of a long report. → The report and the topic list (FE-20, FE-21).
3. Honest lines in places: missing data "never as zero", distances are "screening distances", "Absence of a record is not proof". These sit in small grey type, while the verdict chips are prominent. → Ours must be at least as prominent as the facts.
4. Helpful states. A failed search says the credit was not spent; "greyed 0" means used up; the comparison marks categories "Not decided".
5. Theme and text-size controls, and a data download. → FE-23.
6. A one-page summary before the detail, and a final sources page in the PDF. → FE-21.

## Where Vestagraph must be better
- **The home, not just the area.** Their property overview has no real monthly cost and no tracked questions. Ours has the cost engine and questions per home (doc 02 §3).
- **No scores and no verdicts.** The visitor's own priorities and limits, with never a total (FE-22); "How we got this" for every calculated figure (FE-24).
- **Public facts free, with no account.** The pilot has no sign-up and no passes (0046).
- **Honest coverage outside England,** topic by topic, never a verdict built on missing data.

## Founder decisions, 13 Nov 2026 (prompt windows)
After the review of our specs against these findings:

- **D1:** energy certificates in the pilot, "Energy certificates in pilot", then, after the official licensing terms were checked, "Certificate number (Recommended)": the visitor enters the certificate number, and no address is shown (DA-09).
- **D2:** a valuation only later, as an index-adjusted past sale, "Later, index-adjusted sale" (BE-34).
- **D3:** plain-words area search later, with AI, "Later, with AI" (AI-10).
- **D4:** theme and a text-size control, "Also a text-size control" (FE-23).
- **D5:** "How we got this", "Yes, in each topic (Recommended)" (FE-24).
- **D6:** the flood band and outlines, "Band plus map outlines" (FE-25).
- **D7:** rents in wave 2 if licensed, "Wave 2 if licensed (Recommended)" (DA-10).
- **D8:** planning constraints if licensed, "Add if licensed (Recommended)" (DA-11).

## Gaps found in our own specifications
Fixes come in the next pull requests, in this order: (1) these contradictions; (2) licence research for long-term flood risk, rents, planning constraints and the house price index (DA-05); (3) canvas boards for the topic detail view, priorities and the designed report (FE-20 to FE-22), then their specifications; (4) the wave 1 and wave 2 extras, comparison and accessibility (FE-23).
- the topic detail is still a sub-page in the site plan (FE-20 says sheet or panel);
- the desktop right column is claimed by the map, the topic panel and the chat;
- NEAR-16 calls routed times paid, but wave 2 walking times are free;
- no scenario outside the landing page forbids verdict words, scores or placeholder text;
- if the postcode service is down, the spec would wrongly say the postcode was "not found" (AREA-05);
- the council tax label stated parish averaging as fact before it was confirmed (`data-sources.md`): fixed in this change;
- no scenarios yet for FE-20 to FE-25, the wave 1 and wave 2 extras, or the goal 7 features.
