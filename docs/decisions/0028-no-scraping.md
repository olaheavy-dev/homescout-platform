# 0028: Data sourcing: no scraping

**ID:** DA-07  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2 (applies to every later stage)

## Context
HomeScout shows evidence about homes. Property portals and listings are tempting sources, but their content (descriptions, photos, floor plans) is protected by copyright and database rights and by the portals' terms. The founder's earlier pilot adopted a "never scrape" stance; the new documents only implied it (doc 01 §10 bans re-publishing listings without rights, and doc 02 lists "listing claim" as an evidence origin without a rule).

## Options
- **No scraping; user-provided material and permitted sources only (chosen).**
- **Scrape listings for convenience:** legal and reputational risk, fragile, and against the independence promise.
- **Licensed listing feeds:** possible later, but paid and only with a commercial decision.

## Recommendation
No scraping.

## Decision
The founder agreed. HomeScout uses only:
1. **Material the user provides** for their own decision: documents they upload, listing text they paste, or details they enter. It is processed privately for that user, labelled by origin (for example "listing claim, supplied by you"), and never republished or shared with other users.
2. **Official or open sources used within their licence terms**, for example data published under the [Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/), with attribution and the licence recorded first (DA-05).
3. **Licensed data**, only after a recorded decision and licence check.

HomeScout never scrapes or crawls property portals or agent websites, and never copies listing descriptions, photos or floor plans into its own data. A link to a listing may be stored as the user's own reference.

## Consequences
- Doc 02 §7's "listing claim" origin means user-supplied listing content under this rule.
- Data-loading work (DA-04, DA-05) checks every source against this decision. See also the UK guidance on [database rights](https://www.gov.uk/guidance/sui-generis-database-rights).
- Test and demo data stay synthetic; real listings are never committed.
