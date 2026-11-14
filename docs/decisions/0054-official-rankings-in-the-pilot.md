# 0054: Official rankings in the pilot

**ID:** DA-15  
**Status:** Accepted (founder, 14 Nov 2026, in a prompt window)  
**Date:** 2026-11-14  
**Stage:** 3 (for the pilot, stage 5b)  
**Applies (no older text is rewritten):** `docs/product/05-ideas-and-product-thinking.md` point 5, consistent with `AGENTS.md` rule 4, "any total or ranking would need its own decision record"; this is that record, for government-published ranks only

## Context
`AGENTS.md` rule 4 says the product never calls a home "verified", "safe" or "approved". Doc 05 point 5 says "No scores or verdicts from us ... any total or ranking would need its own decision record".

On 14 Nov 2026 the founder proposed showing each topic at its official geographical level, as a table (register line DA-14). Two rows in that table were rankings that a government body already publishes: "Deprivation | Official national LSOA rank and decile | Yes, already published" and "Crime | Crime statistics and official LSOA deprivation indicators | Official LSOA ranking only". An LSOA (Lower layer Super Output Area) is a statistical neighbourhood of about 1,500 people. Showing a rank we did not make is different from making our own score, but it still needs a recorded decision because doc 05 point 5 asks for one for any ranking; rule 4 is not changed.

## Options
### Option A: Never show any ranking
Keeps the rule as written. Loses a well-known official fact that visitors may look up elsewhere.

### Option B: Official ranks and indices only, in the pilot
Show a rank or decile only where a government body publishes it, quoted with its source, edition year and level. We never make a score, a total or a ranking of our own. This was the agent's recommendation.

### Option C: Make our own area score
A single number per area. This is a verdict from us (rules 2 and 4) and was not proposed.

## Decision
**Option B**, first as "Official only, wave 2 (Recommended)" (founder, 14 Nov 2026, prompt window). The founder then typed: "all these wil be in the first wave, there should not be wave 1 and wave 2, a single pilot phase" [sic] (register line PD-16), so the official rankings ship **in the pilot**.

**What may be shown.** Only government-published ranks, indices or metrics, never a score, total or ranking we make:
- **The English Indices of Deprivation 2025** (MHCLG, published 30 Oct 2025): each LSOA's rank among 33,755 LSOAs in England, and its decile, where decile 1 is the most deprived 10% of neighbourhoods nationally. This includes the published domain deciles, such as the crime domain. Source: [statistical release](https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025/english-indices-of-deprivation-2025-statistical-release) (read 14 Nov 2026).
- **The Department for Transport's transport connectivity metric** (published 29 Sep 2025, [publication page](https://www.gov.uk/government/publications/transport-connectivity-metric), read 14 Nov 2026): the page says it is "presented at output area, lower super output area, local authority district and regional level" for England and Wales, under the Open Government Licence v3.0. It is shown only at the level its tables publish, and which table and column we quote is a check before build (the data file has not yet been read).

**Rules that come with it:**
- Each figure is quoted with its source, edition year and level, for example "this neighbourhood (LSOA), about 1,500 people" (DA-14).
- **Missing is said, never filled (rule 7):** where no published figure exists for the postcode's neighbourhood (no LSOA match, no row in the table), the page says so; never a default, a blank decile or a neighbouring area's value.
- Every rank carries a "relative, not absolute" note (a rank compares neighbourhoods with each other and says nothing about how deprived any one is in itself) and "describes the neighbourhood, not this street or home"; whether that note fits the DfT metric is checked before build, with its table choice.
- A change between editions is never shown as a change in the area. The release says indices "should not be viewed or construed as a time-series", that comparison is only "in terms of comparing the rankings as a snapshot in time", and that a change in decile may reflect changes to geographies and methods "rather than, or in addition to, real change in deprivation levels" (statistical release, sections 5 and 6, read 14 Nov 2026). We show one edition at a time.
- Ranks are never combined with each other or with anything else, never drawn on maps or isometric scenes, and never counted as good or bad in At a glance.
- The AI quotes a rank only with its source, edition and level, and never as a verdict. AI-11's fixed reply (a question such as "is it safe?") is unchanged.
- **England only.** Other UK nations publish their own indices, which are not comparable; they show "not yet covered" (rule 6).
- **Licence check in DA-05 before build** for both sources (rule 3), including the DfT table choice above.

## Consequences
- **Rule 4 and doc 05 point 5 stand.** Doc 05 point 5 now points here; "no scores from us" is not weakened, because a government-published rank is quoted, not made.
- **Data:** `docs/references/data-sources.md` records both sources; the fixtures record each fact's level (DA-14) and its edition year.
- **Specifications:** scenarios for the "relative, not absolute" note, the one-edition rule and the England-only message are written before building, with the first design batch.
- **Revisit if** a nation outside England publishes a comparable index, or if a source's licence fails DA-05.
