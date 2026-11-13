# Research on a ChatGPT product review, 13 Nov 2026

**Purpose:** the founder pasted a ChatGPT conversation proposing eight "differentiators" for Vestagraph and asked to "discuss, research, and then document", then to "present all the free ones that chatgpt suggested … and let us discuss the ones that should go in and make us standout. We can document the paid ones as follow up" [sic]. This page records what the research found, what the founder chose, and the paid or licence-gated sources kept as follow-ups.

**Method:** three research passes on 13 Nov 2026 (school admissions; walking routes and bus frequency; ChatGPT's competitor and data claims), reading providers' own pages. **[F]** = seen on the provider's or product's own fetched page (PDFs read as text are marked [F-PDF]); **[S]** = seen only in a search result, not verified on the page. "Not found" is not proof of absence. Prices were not tested in paid accounts. Not legal advice. The 11 Nov [competitor check](2026-11-11-competitor-check-of-ideas.md) and [`data-sources.md`](../references/data-sources.md) were read first and not redone.

## ChatGPT's suggestions, weighed

| # | Suggestion | Weighing (agent) | Outcome |
|---|---|---|---|
| 1 | School admission intelligence | Right that parents need more than a list; "last distance offered" has no national source (below). National applications and offers are free | School demand into pilot wave 2; last distance offered a follow-up |
| 2 | True accessibility (walking routes, transport frequency, commute times) | Right: straight-line distance understates walks. Free engines and data exist; commute and rail are heavier | Walking times and buses per hour into pilot wave 2; commute and rail later |
| 3 | Hidden neighbourhood risks | Mostly planned already (flood, crime, planning, air; doc 05 idea i). Address-level subsidence data is paid | Unchanged; subsidence a follow-up |
| 4 | Family suitability | Fine as a grouping of facts; "suits a family" would be a verdict (rule 4) | Family view into pilot wave 2, facts only |
| 5 | Real cost of living | Already the core (cost engine). Council tax charges per band are open; energy use is kWh, not £ | Council tax by band on the pilot area check and, later, in the home's monthly cost |
| 6 | Personalised comparison with weights | A weighted total is a verdict; doc 05 dropped "Priorities as a score" (l); 0004 says AI never decides | Not adopted; compare two postcodes stays as planned (wave 2) |
| 7 | Neighbourhood change tracking | Already lead idea (n), "One watch feed per saved home"; needs accounts | Unchanged |
| 8 | "Verified local intelligence" | Source, date, coverage and limits per fact is already a rule; the word "verified" is not allowed (rule 4) | Unchanged |

ChatGPT's positioning, "a neighbourhood decision-intelligence platform", would move Vestagraph from a home decision workspace to an area data product. The agent's view: area data is crowded (below), so the home (its real cost and tracked questions) stays the centre and the area check stays the way in. No consumer property product was found using the phrase; only public-sector and business-to-business uses [S] ([techUK](https://www.techuk.org/insights/guest-insights/neighbourhood-decision-intelligence-from-citizen-360-to-population-360)).

## Competitor claims checked

| Product | What was found | Mark |
|---|---|---|
| [Crystal Roof](https://crystalroof.co.uk/) | Schools (Ofsted, admission policy, results), crime, flood from rivers and sea, NO2 and particulates, transport, demographics, affluence, noise, amenities. Free basic checks; paid £12.99 a week, £22.99 a month, £49.99 for 3 months ([pricing](https://crystalroof.co.uk/pricing)). API pages linked, no price shown. No MCP server or ChatGPT app found | [F] |
| [PropertyData](https://propertydata.co.uk/) | Investor analytics, £15 to £60 a month ex VAT ([pricing](https://propertydata.co.uk/pricing)). API endpoints for schools, crime, flood risk (England), PTAL (London only), demographics, internet speed ([api](https://propertydata.co.uk/api)). **An MCP server and a ChatGPT connector**, and "Ask Claude about any UK property"; saved areas with planning and sourcing alerts | [F] |
| [AreaSense](https://areasense.co.uk/) (founder confirmed this is the one ChatGPT meant) | Crime, schools, NHS access, sold prices and rents, transport, flood, radon, coal and soil risk, road and rail noise, planning, demographics, EPC, "red flags"; source and date per figure; **a score per section** (method not explained). Free tier of 1 search a day; passes from £3.99 a day to £25.99 for 3 months; compare two postcodes; "area recommendations" that match "what matters to you" (no weights described). No alerts, API or MCP server seen | [F] |
| Locrating | Its site returned HTTP 403. Search results say it began collecting last distance offered from council websites in 2020, for "some, but not all" schools in England ([blog](https://www.locrating.com/blog/collecting-last-distance-offered-data.aspx)), with a premium plan around £12.99 a month. Years held and what is free are not confirmed, so not recorded as fact | [S] |
| [School Atlas](https://www.schoolatlas.co.uk/blog/school-catchment-distances-2026-has-your-cut-off-shrunk) | Last distance offered for "thousands of schools in England", some extracted by AI from council documents, some with no recorded source; shows the year with each figure | [F] |
| BestPlaceUK "Find My Match" | Search results describe user-weighted area rankings and "alerts when an area you follow changes". Operator unclear and the page failed to load, so a weak signal only | [S] |

**What this changes:** AreaSense shows scores **with** a source and date per figure, so "we cite sources" alone does not set Vestagraph apart. PropertyData already has an MCP server and ChatGPT connector, so doc 05 idea (q) is more crowded than thought. BestPlaceUK, if confirmed, would be an area-level example of change alerts, so idea (n)'s "none combined" now reads "none combined per home; one unverified area-level example".

## Free sources found

| Source | What it gives | Licence | Mark |
|---|---|---|---|
| DfE [applications and offers](https://explore-education-statistics.service.gov.uk/find-statistics/secondary-and-primary-school-applications-and-offers) | Per school: 1st, 2nd, 3rd and total preferences and offers; entry September 2026, series from 2014; linked to GIAS by LAEstab (some dummy codes). **No distance.** No oversubscription field; a places column not confirmed | OGL v3.0 | [F] |
| Ofsted [childcare providers](https://www.gov.uk/government/statistical-data-sets/childcare-providers-and-inspections-management-information) | Registered providers and inspections, twice a year (latest 5 Aug 2026, data at 30 June 2026). Places are "the legal maximum number of children", not vacancies; childminders' details are redacted, so a postcode search misses them | OGL v3.0 | [F] |
| [Bus Open Data Service](https://www.gov.uk/guidance/find-and-use-bus-open-data) | Timetables (TransXChange), vehicle locations (SIRI-VM), fares (NeTEx). A UK-wide GTFS file is reported [S]. Departures per hour per stop can be counted from the timetables, as scheduled services. No DfT stop-level frequency dataset found ([bus statistics](https://www.gov.uk/government/statistical-data-sets/bus-statistics-data-tables) are by local authority) | OGL v3.0 "except where otherwise stated" | [F] |
| Routing engines: [OSRM](https://github.com/Project-OSRM/osrm-backend) (BSD-2), [Valhalla](https://github.com/valhalla/valhalla) (MIT), [GraphHopper](https://github.com/graphhopper/graphhopper) (Apache-2.0) | Walking routes over OpenStreetMap paths, run on our own machine. No official England size figure; OSRM's [wiki](https://github.com/Project-OSRM/osrm-backend/wiki/Disk-and-Memory-Requirements) gives planet figures and says sizes scale roughly linearly. Transit journeys need OpenTripPlanner, r5 or GraphHopper's GTFS module | Open-source licences as named | [F] |
| MHCLG [council tax levels 2026-27](https://www.gov.uk/government/statistics/council-tax-levels-set-by-local-authorities-in-england-2026-to-2027) | Table 9: area council tax for a dwelling occupied by 2 adults, by band, per local authority (published 25 Mar 2026). "Area" figures average in parish precepts, so a bill can differ within a council. Layout of the ODS not yet opened | OGL v3.0 | [F] |
| DESNZ [sub-national consumption](https://www.gov.uk/government/collections/sub-national-electricity-consumption-data) | Electricity and gas use in kWh by local authority, LSOA and MSOA, and electricity by postcode (2013 to 2024). kWh, not £; a domestic-only figure not confirmed | OGL v3.0 | [F] |
| BGS GeoSure [5 km hex grid](https://www.bgs.ac.uk/products/geosure/home.html) | A generalised overview of six ground hazards; too coarse to say anything about one address | Labelled "Open" [F]; OGL only per a catalogue search result [S] | [F]/[S] |

## Paid or licence-gated: follow-ups
Opened as research issues: last distance offered #232, BGS GeoSure #233, rail timetables #234. Radon and hosted routing are already covered by `data-sources.md` and DA-06; the VOA band is a link, not a purchase.

| Source | Why it is not free to use | Mark |
|---|---|---|
| Council "last distance offered" | No national dataset. Sheffield ([PDF](https://www.sheffield.gov.uk/sites/default/files/2025-07/oversubscribed_infant_and_primary_schools.pdf), miles, oversubscribed schools only, "as at 16th April"), Leeds ([PDF](https://www.leeds.gov.uk/sites/default/files/2026-04/cut%20off%20distances%20and%20criteria%20for%20primary%20and%20junior%20schools%202026.pdf), one row reads "314", likely an error) and [Haringey](https://haringey.gov.uk/schools-learning/schools/school-admissions/how-school-place-offers-were-made/how-offers-school-places-were-made-national-offer-day) publish it in different units and dates; no licence statement seen on any. Academies and faith schools often set their own criteria. Scraping is ruled out (0028), so it needs per-council written permission or a licensed supplier | [F]/[F-PDF] |
| School admission criteria and faith requirements | Published by each admission authority as PDFs or web pages; nothing machine-readable found | [S] |
| BGS GeoSure 1:50 000 (shrink-swell and others) | "Premium"; the standard [licence](https://www.bgs.ac.uk/information-hub/licensing/) bars use in commercial products; commercial use needs a fee-bearing licence or a reseller agreement | [F] |
| UKHSA radon for one address | The address report is paid (already in `data-sources.md`) | — |
| Rail timetables | Free timetable downloads are reportedly for development only; use beyond testing needs a paid licence | [S] |
| Hosted routing | GraphHopper's free plan is non-commercial; paid plans €69 to €479 a month ([pricing](https://graphhopper.com/pricing/)) [F]. openrouteservice's free tier reportedly bars commercial use [S] | [F]/[S] |
| VOA council tax band for one address | Licensed for non-commercial viewing only; no copying or redistribution ([terms](https://www.tax.service.gov.uk/check-council-tax-band/os-terms)). Not a follow-up to buy: link to the VOA checker instead | [F] |

## Points to carry into the specs
- **Walking times and buses per hour are calculated outputs** (rule 2): one tested module, stored with the area result, quoted by the page, chat and tools. Label walking times "from the postcode centre", never "from your door"; show "route not found" when paths are missing, never zero (rule 7); bus counts are "timetabled", never "reliable"; never say step-free or safe at night.
- **OpenStreetMap share-alike:** routes are derived from OSM (ODbL). The OSM Foundation's [Produced Work guideline](https://osmfoundation.org/wiki/Licence/Community_Guidelines/Produced_Work_-_Guideline) covers images; no routing guideline was found. Keep derived times in a separate attributed table and get a legal read before publishing them in bulk (DA-05).
- **School demand is last year's facts**, never a chance of a place, with the admission authority's policy linked. Ofsted inspection results already sit in wave 2.
- **Council tax:** per-band charges come from the MHCLG table as inputs; the area check shows the council's table with "your parish may add to this"; the user's band comes from the user (linking to the VOA checker), never looked up. A pull request adding the charges table is a tax table, so the founder merges it (`AGENTS.md`, "When merging").
- **Family view:** groups childcare (capacity, not vacancies; childminders not listed), schools, parks and playgrounds; facts only, never "suits a family".
