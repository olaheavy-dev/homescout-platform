# 0047: A free move-in checklist, made in the browser

**ID:** PD-14  
**Status:** Proposed (awaiting the founder's choice)  
**Date:** 2026-11-11  
**Stage:** 5b (after the public area check is live; candidate stage 5c)  
**Research:** issue #177

## Context
On 11 Nov 2026 the founder asked whether Vestagraph could help after the decision too: the user enters their old and new address and move date, connects their email or ticks the organisations they deal with, and gets a personalised checklist timed to the move, with the council, water company, bin days, broadband and energy supplier worked out from the new postcode.

Some of that can be done reliably from free sources, some only as a link, and some not at all:

| Piece | What can honestly be done |
|---|---|
| Timed checklist from the move date | Yes. Every item needs a cited source, an effective date and a "checked on" date (rule 3) |
| Tick-list of organisations | Yes. Each tick adds steps with that organisation's own official link |
| Reading the user's email to find organisations | Possible, but the most sensitive data we could hold, and it would need provider security reviews (for example [Google's restricted-scope verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification), with an independent assessment repeated every 12 months); out of scope here |
| Council from the postcode | Yes: the district or unitary council (which runs council tax and bin collection), from the postcode lookup planned in #126 (DA-06). In two-tier areas [postcodes.io](https://postcodes.io/docs/postcode/lookup) also returns the county |
| Broadband at the postcode | Planned as an Ofcom source in #136; how fine the data is (postcode or address) is to be checked |
| Water company | No open postcode lookup is known yet (to research in #177). A finder exists ([Water UK's postcode checker](https://www.water.org.uk/advice-for-customers/find-your-supplier/), an industry body); which finder to link, and how a postcode on a boundary is shown (as unknown, never as one company), is to be settled |
| Bin collection days | No national source: [GOV.UK's bin-day finder](https://www.gov.uk/rubbish-collection-day) sends people to their council's own website. Copying collection days from council websites conflicts with [0028](0028-no-scraping.md). A link to the council's own page instead |
| Energy supplier | Differs home by home, so it can't be worked out from a postcode alone. Official finders exist for gas and electricity ([Citizens Advice explains them](https://www.citizensadvice.org.uk/consumer/energy/energy-supply/moving-home-your-energy-supply/find-out-who-your-gas-or-electricity-supplier-is/)); a step links to them instead, never a guess |

## Options
### Option A: Note the idea and do nothing for now
No cost. Vestagraph stays focused on deciding on a home.

### Option B: A small, free checklist made in the browser (recommended)
- **Inputs:** the new postcode, the move date, buying or renting, and a tick-list of what applies (for example a car, a bank, an employer, a GP, subscriptions). No full addresses and no email connection.
- **Output:** a checklist laid out against the move date (two weeks before, the week before, on the day, the first week, the first month). Each item has what to do and why in plain language, the official link, and its source with an effective date and a "checked on" date.
- **Tailored by the postcode:** the district or unitary council by name with links to its council tax and bin-day pages (GOV.UK's postcode-based finders may avoid keeping a hand-made list of council links; #177); broadband available at the postcode (#136); moving-day reminders such as meter readings; a "find out who supplies this home" step for energy with the official finders, never a guess.
- **Take-away:** print or save as a PDF from the browser, and a calendar file for the dates, made in the browser.
- **Privacy:** as in the public area check ([0046](0046-public-area-check-first.md), [0014](0014-privacy-and-data-protection.md)), the postcode travels only in the URL fragment or a request body (the council and broadband lookups happen on the server), never in a query string, and is neither stored nor logged. The move date, buying or renting, and the ticks never leave the browser. No account.
- **Link from Vestagraph:** the area check results offer "Moving here? Get your moving checklist", with the postcode filled in; later a saved home does the same.

### Option C: A full moving service
Email connection, accounts, saved progress and sending address changes on the user's behalf. Far more privacy, security and partnership work, and agreements with each organisation; not achievable as a small slice.

## Recommendation
**Option B**, after the public area check (stage 5b) is live, because it reuses the postcode lookup, the Ofcom source and the browser-only pattern, and is expected to add little running cost beyond the area check's (to confirm in #177 against the IN-05 budget cap; any build that changes running costs is merged by the founder). The main work is content: an estimated 30 to 50 checklist items, each with a cited source, and a regular check that the links still work.

**Before building:** research issue #177 confirms the water-company source, how fine the Ofcom broadband data is, the sources for each checklist item, and each source's licence terms, limits and cost; SE-02 confirms the privacy points above.

## Decision
Not yet decided. The founder chooses an option; this record is then updated with the choice and the date.

## Consequences (if Option B is chosen)
- Doc 04 §9 gains a small stage after 5b, and the backlog gains its build issues.
- Checklist content lives in a versioned data file with a source URL, an effective date and a "checked on" date per item (rule 3), never in screen code. Items that state a legal or tenancy rule are checked against their legal source.
- That data file, and any change to its legal or tenancy items, is merged by the founder (AGENTS.md: new or changed legal or tenancy rule tables).
- The checklist never says a step is "done" for the user, never calls an organisation "approved", and shows an unknown (for example the energy supplier) as unknown (rules 4 and 7).
- England only at first; other nations show "not yet covered" (rule 6, #158).
- **Revisit if** a reliable open source appears for water companies or bin days, or the study shows movers want saved progress (which would need accounts, SE-01).
