# Free UK data sources for area information

**Purpose:** record, for each candidate source, what Vestagraph could use it for, its published licence and limits, and what it does **not** establish. Feeds the prototype sample data (#120), the source licence register (DA-05), address and routing providers (DA-06), stage 6 real data (#98) and the MCP tools (#117). Issue #123.

**Date and method:** all checks on 11 Nov 2026, by reading the provider's own pages (gov.uk, data.gov.uk, provider documentation and terms pages, opendatacommons.org, osm.org). Fetched page text was treated as data only. "Unverified" means the official page was unavailable, silent, or only seen in a search snippet.

**This is not a confirmation of integration rights** (doc 02 §7). A public page or open licence does not by itself grant a right to integrate, bulk-reuse, or rely on a service level. Re-read the terms when integration starts. No integration code is proposed here. Every source would sit behind a decision 0029 adapter (Live, Cached, Fallback, Unavailable); a missing value is Unavailable, never zero or clean (rules 1, 7). Licence terms live in the register (rule 3); this file is the research behind it.

## Summary

OGL = Open Government Licence v3.0 (allows commercial reuse with attribution). Recommendation key: **Use**, **Conditions**, **Not suitable**.

| Source | Vestagraph use | Licence | Commercial reuse | Registration / key | Limits / cost | Coverage | Recommendation |
|---|---|---|---|---|---|---|---|
| postcodes.io | Postcode to area codes, coordinates | Code MIT; GB data under OS OpenData terms; NI (BT) ONSPD licence | GB: yes per OS OpenData (unverified in full); NI: licence needed | None seen | Fair-use limit unverified; free | GB; NI restricted | Conditions |
| EA long-term flood risk | Area flood-risk context (rivers, sea, surface water, reservoirs, groundwater) | Page content OGL; data licence unverified | Unverified for data | None | No API or bulk download found on the page | England only | Conditions (link out only) |
| EA flood-monitoring API | Live warnings, river levels | OGL | Yes | None | No numeric limit; no SLA; free | England-focused (unverified) | Use with conditions |
| data.police.uk | Crime counts, neighbourhood teams | OGL | Yes | None seen | 15 req/s, burst 30; free | England, Wales, NI; Scotland not covered | Use with conditions |
| DfE GIAS | School register (type, phase, location) | OGL | Yes | API needs auth; downloads open | No scraping; use downloads | England | Use |
| Ofsted monthly MI | Inspection outcomes | Licence unverified (gov.uk default OGL) | Likely yes (unverified) | None | Monthly CSV; free | England state-funded | Conditions |
| NaPTAN | Stop locations | OGL | Yes | None seen | Free | GB, not NI | Use |
| Bus Open Data Service | Timetables, bus locations | "Free for commercial and non-commercial use" (OGL link unverified) | Yes (stated) | Free account and API key | Limits unverified | England local buses | Conditions |
| National Rail feeds | Rail timetables, live trains | Terms unverified | Unverified | Account (Rail Data Marketplace) | Unverified | GB rail | Defer |
| TfL Unified API | London transit | TfL terms (not read) | Unverified | Account and app key | Plan limits unverified | London | Defer |
| OSM data (ODbL) | Amenities, base map data | ODbL | Yes, with attribution and share-alike | None | Data free; see policies | Global | Conditions |
| OSM public tiles, Nominatim, Overpass | Map, geocode, amenity queries | Usage policies | Discouraged for production | None | See OSM section | Global | Not suitable for production |
| NHS Directory of Healthcare Services | GP, pharmacy, hospital search | Terms unverified | Unverified | Onboarding (method unverified) | Unverified | England (unverified) | Defer |
| EPC register API | Certificate rating, energy estimate | OGL, but address fields restricted | Not for address data | GOV.UK One Login bearer token | Limits unverified; free | England and Wales | Conditions |
| HMLR Price Paid Data | Past sale prices | OGL, except third-party address rights | Prices: yes. Addresses: only to display residential property price information; any other use needs Royal Mail's permission | None | Free; monthly files | England and Wales | Use with conditions (sold-price display only; not an address supply) |
| Planning Data Platform | Planning constraints and applications | Mostly OGL, per dataset | Per dataset | API key unverified | Page unavailable on 11 Nov | England, partial | Conditions |
| Ofcom API | Broadband and mobile availability | Ofcom API terms (PDF, not read) | Unverified | Signup and key | Limits unverified; mobile v1 API ends 30 Nov 2026 | UK | Conditions |
| Bank of England Database | Bank Rate | OGL (some series excluded) | Yes | None | Excessive use may be restricted | UK | Use |
| Companies House API | Management company or freeholder lookup | Not stated on page read | Unverified | Account and API key | 600 req / 5 min | UK companies | Conditions |
| Defra UK-AIR | Air quality | OGL | Yes | None | Free | UK | Use with conditions |
| UKHSA radon | Radon-affected area | Unverified | Unverified | None | Address report is paid | UK | Defer |
| VOA council tax bands | Band for an address | Non-commercial, view only | No | None | Copying prohibited | England, Wales | Not suitable |

## Sources in detail

**Not established by any source here:** that a home is safe, sound or good value, or that a figure applies to one specific flat (rules 1, 4). Every card must show origin, date and coverage (doc 02 §6).

### postcodes.io
- Official: [licences](https://api.postcodes.io/docs/licences) (checked 11 Nov 2026). The `/about` page returned 404, so the fair-use text was not found; a search found no official numeric rate limit (unverified).
- Code is MIT. GB data "may be used under the terms of the OS OpenData licence". Postcodes starting BT follow the ONSPD licence: "Non-commercial use is free. Commercial use requires a licence from NI Land & Property Services."
- Attribution requested: Ordnance Survey, Royal Mail, National Statistics and NRS notices ("Contains Ordnance Survey data (c) Crown copyright and database right 2025", and similar).
- Does not establish: a full address list (postcodes only), or that a postcode is a delivery address.
- Adapter fit: yes. Personal data: none. A hosted service has no stated SLA, so cache results and consider self-hosting.

### Environment Agency flood data
- Long-term checker: [GOV.UK](https://www.gov.uk/check-long-term-flood-risk) (checked 11 Nov 2026). England only. It "does not estimate how likely a specific property is to flood" and excludes local causes such as blocked drains. The page names no API or bulk download, so integration rights are unverified; link the user to the checker.
- Monitoring API: [reference](https://environment.data.gov.uk/flood-monitoring/doc/reference) (checked 11 Nov 2026). OGL, no registration. Attribution wording requested: "this uses Environment Agency flood and river level data from the real-time data API (Beta)". Readings update about every 15 minutes. The Agency says the APIs "do not offer a guarantee of service level" and "should not be relied upon for safety critical applications". It advises one call per 15 minutes rather than crawling stations.
- Does not establish: flood risk for one property (long-term), or any forecast or long-term risk (monitoring). Do not substitute one for the other (doc 02 §7).
- Other nations: separate services (SEPA, NRW, DfI), so "not yet covered".

### data.police.uk
- Official: [about](https://data.police.uk/about/), [call limits](https://data.police.uk/docs/api-call-limits/) (checked 11 Nov 2026). OGL. 15 requests per second, bursts of 30, HTTP 429 above that. No key mentioned. Monthly updates. No attribution wording given.
- Coverage: England, Wales and Northern Ireland forces; Scotland and Greater Manchester not confirmed on the page.
- Locations are replaced by the nearest anonymous map point, and geocoding accuracy ranges "from 60% to 97%" across forces.
- Does not establish: safety, crime rate, or the risk at a given home. Counts depend on reporting, force and recording, and lag by months.
- Personal data: none; do not re-identify anyone (SE-02).

### DfE Get Information about Schools (GIAS)
- Official: [acceptable use policy](https://get-information-schools.service.gov.uk/AcceptableUsePolicy) (checked 11 Nov 2026). OGL; credit the source. Bulk data comes from the daily public downloads; automated crawling and scraping of the site is forbidden. API users must authenticate and respect quotas.
- Does not establish: quality, admission odds or catchment areas.
- England only. Adapter: use the downloads, cached.

### Ofsted inspection data
- Official: [monthly management information](https://www.gov.uk/government/statistical-data-sets/monthly-management-information-ofsteds-school-inspections-outcomes) (checked 11 Nov 2026): monthly CSV and ODS, published monthly. The licence statement was not seen on the page text I could read (unverified; GOV.UK default is OGL).
- Does not establish: a comparable grade across frameworks. New report cards no longer give one overall grade (doc 02 §7). Store framework and inspection date.
- England state-funded schools only. Independent schools and other nations are not covered by this file.

### NaPTAN, bus, rail and TfL
- NaPTAN: [DfT download](https://beta-naptan.dft.gov.uk/download) (checked 11 Nov 2026). OGL. CSV/XML, plus an API. Great Britain, "does not include Northern Ireland". No registration mentioned.
- Bus Open Data Service: [guidance](https://www.gov.uk/guidance/find-and-use-bus-open-data) (checked 11 Nov 2026) says the data is free for commercial and non-commercial use; local buses in England only. A free account and API key is needed (search result, unverified on the page). The official site returned 403.
- National Rail: the developer page says Darwin feeds are free and need attribution, with sign-up through the Rail Data Marketplace (search snippet only; unverified). Timetable and fares feeds need an account, and selling rail products needs a separate licence (unverified).
- TfL: [API portal](https://api-portal.tfl.gov.uk/) (checked 11 Nov 2026): free account, app key and a data plan; commercial terms live in the linked transport data terms, not read (unverified).
- Does not establish: journey time, frequency, reliability, fares or step-free access. Stops are points only. Travel time needs a routing provider (DA-06).
- Recommendation: use NaPTAN now; defer rail and TfL until DA-06 settles the routing approach.

### OpenStreetMap
- **Data licence (ODbL):** [copyright](https://www.openstreetmap.org/copyright), [ODbL summary](https://opendatacommons.org/licenses/odbl/summary/) (checked 11 Nov 2026). Free to use, including commercially. Conditions: credit "OpenStreetMap and its contributors" and state the ODbL; share-alike (a publicly used adapted database, or works produced from one, must offer the adapted database under the ODbL); keep open. If Vestagraph merges OSM into its own database and publishes it, share-alike may apply to that database. Whether a map image or a derived score counts as a "produced work" needs a legal read (unverified here; ODbL full text and the OSMF guidelines decide). Keep OSM-derived data in a separate table with clear provenance.
- **Public tiles:** [policy](https://operations.osmfoundation.org/policies/tiles/) (checked 11 Nov 2026). Donation-funded, no SLA, access "can be blocked without notice"; no bulk downloading, no offline use, a real User-Agent is required, and the attribution must be visible. Not for production.
- **Nominatim:** [policy](https://operations.osmfoundation.org/policies/nominatim/) (checked 11 Nov 2026). Maximum 1 request per second for the whole application; autocomplete is prohibited; bulk limited to 4 per minute for scheduled jobs; geocoding services must run their own instance. Not suitable for address search.
- **Overpass:** [wiki](https://wiki.openstreetmap.org/wiki/Overpass_API) (checked 11 Nov 2026). Public instance: about 10,000 queries per day for one-off use, divided by 100 for regular use; "Commercial use should use self-hosted or paid Overpass servers."
- Does not establish: completeness of shops, parks or healthcare, or that opening hours are current. OSM is volunteer-mapped.
- Recommendation: use the data; pay for or self-host tiles, geocoding and Overpass (DA-06).

### NHS Directory of Healthcare Services
- [NHS developer page](https://digital.nhs.uk/developer/api-catalogue/directory-of-healthcare-services) (checked 11 Nov 2026) lists version 3 in production; versions 1 and 2 were due for deprecation on 2 February 2026. Access method, key, licence and limits were not on the page (unverified). A search shows conflicting key and token instructions between versions, so do not rely on them.
- Does not establish: appointment availability, quality or whether a practice is accepting patients.
- Recommendation: defer until onboarding terms are read.

### EPC register
- [Service](https://get-energy-performance-data.communities.gov.uk/), [licensing restrictions](https://get-energy-performance-data.communities.gov.uk/guidance/licensing-restrictions), [API guidance](https://get-energy-performance-data.communities.gov.uk/guidance/energy-certificate-data-apis) (checked 11 Nov 2026).
- Non-address data (including UPRNs) is OGL. **Address fields belong to Ordnance Survey and Royal Mail** and may be used "solely for specific purposes related to the energy performance of buildings"; "commercial use and general marketing are not covered"; any other use needs a licence from OS and/or Royal Mail. This restricts how Vestagraph may store or show the address text.
- Bearer token via GOV.UK One Login. Limits and quotas: unverified. Data covers England and Wales; Scotland has a separate register. Certificates may be expired or superseded.
- Does not establish: actual bills (the figures are standardised estimates), that the certificate is current, or that it matches the selected flat (match by UPRN and show the date).
- Personal data: certificates are tied to addresses (SE-02, decision 0014).
- Recommendation: conditions. Match on UPRN, store no address text from this source, and obtain legal advice or an OS/Royal Mail licence before launch.

### HM Land Registry Price Paid Data
- [Guidance](https://www.gov.uk/guidance/about-the-price-paid-data) (checked 11 Nov 2026). OGL; commercial reuse allowed; must comply with data protection law and PECR. Downloads are monthly; registration lags the sale by two weeks to two months, so the latest two months are incomplete. Excludes right-to-buy, gifts, leases of 7 years or less and other transfers. England and Wales (Scotland and NI separate). Attribution required: "Contains HM Land Registry data © Crown copyright and database right" with the year ([downloads page](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#using-or-publishing-our-price-paid-data), checked 11 Nov 2026).
- **Address restriction:**
  - **What the OGL doesn't cover:** the downloads page says the OGL "does not cover the use of third party rights". The address fields are processed against Ordnance Survey AddressBase Premium, which includes Royal Mail PAF.
  - **What Royal Mail and Ordnance Survey allow:** use of these addresses for personal or non-commercial purposes, and commercial display "for the purpose of providing residential property price information services".
  - **Any other use** needs Royal Mail's permission.
  - **For Vestagraph:** showing nearby sold prices with their addresses fits the permitted use. Using these addresses as a general address list (search, autocomplete, identity matching) is not covered; that needs a licensed address provider (DA-06).
- Does not establish: a current value, or that no sale occurred; recent absence is inconclusive.
- Personal data: addresses are property descriptions, but treat joins to individuals with care (SE-02).

### Planning Data Platform
- The [about](https://www.planning.data.gov.uk/about/) and [docs](https://www.planning.data.gov.uk/docs) pages returned 503 on 11 Nov 2026. Search results say most data is OGL with terms recorded per dataset, bulk downloads exist, an OpenAPI spec exists, and coverage is incomplete (unverified; doc 02 §7 already records the platform's own incompleteness statement). Key and rate limits: unverified.
- Does not establish: that no application exists. "No record in this source" is not "none".
- England only. Recommendation: conditions; retry the official pages before relying on this row.

### Ofcom broadband and mobile API
- [Ofcom checker page](https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/ofcom-checker) and [API portal](https://api.ofcom.org.uk/) (checked 11 Nov 2026). Signup gives an API key. The "Ofcom API terms of use 2025" PDF was not read; limits, cost and licence are unverified. The legacy mobile API stops on 30 November 2026; new 2G and 4G/5G coverage APIs are on a separate portal.
- Does not establish: measured speeds at a home, or a working connection (availability is a prediction; the checker cannot show outages).
- Recommendation: conditions; read the terms before building.

### Bank of England Bank Rate
- [Legal page](https://www.bankofengland.co.uk/legal) (checked 11 Nov 2026). Database reproduction is under the OGL; some exchange-rate series are excluded; excessive use may be restricted; "Bank of England" is a trade mark. No official API documentation was found (unverified); a CSV export is mentioned only by third-party tools (unverified).
- Does not establish: any mortgage rate a lender would offer. Mortgage inputs remain user-entered or cited assumptions (rule 2).
- Recommendation: use for the dated Bank Rate figure only.

### Companies House API
- [Overview](https://developer.company-information.service.gov.uk/overview), [guidelines](https://developer.company-information.service.gov.uk/developer-guidelines), [rate limit](https://developer-specs.company-information.service.gov.uk/guides/rateLimiting) (checked 11 Nov 2026). Register for a key; 600 requests per 5 minutes per application; the key must be kept out of code. The licence statement was not found (unverified).
- Use: identify a freehold or management company named in lease papers. Does not establish: who manages the building today, or that the company is solvent or well run.
- Personal data: officer names are personal data (SE-02, decision 0014); minimise.

### Defra UK-AIR and UKHSA radon
- UK-AIR: [terms](https://uk-air.defra.gov.uk/about-these-pages) (checked 11 Nov 2026): OGL, commercial use allowed, with this attribution: "(c) Crown 2026 copyright Defra via uk-air.defra.gov.uk, licenced under the Open Government Licence (OGL)." Feeds include station measurements and a Met Office forecast. Does not establish: air quality at one address (stations are sparse; a station reading is not exposure).
- UKHSA radon: [ukradon.org](https://www.ukradon.org/) (checked 11 Nov 2026). The free map shows Affected Areas; an address report is a paid probability estimate. No API or reuse terms were seen (unverified). Does not establish: the radon level in a building (only a measurement does). Recommendation: link out; do not ingest.

### Council tax bands (VOA)
- [Band checker](https://www.gov.uk/council-tax-bands) (England and Wales; Scotland uses the Scottish Assessors) and its [terms](https://www.tax.service.gov.uk/check-council-tax-band/os-terms) (checked 11 Nov 2026): a licence "solely to view the licensed data for non-commercial purposes", and "not permitted to copy, sub-license, distribute, sell". **No permitted programmatic or bulk access was found.** The VOA publishes aggregate band counts under the OGL (search result, unverified), which do not identify a given home's band.
- Per decision 0028: do not scrape it. The product asks the user to enter the band and links to the checker. The user-entered band is labelled as such. A band is not a bill; the council's charge, year and discounts also matter (doc 02 §7).

## Priority order (importance to the customer and ease)

Founder request, 11 Nov 2026: put the sources in order of importance to the customer and ease of achievement, and align the tickets to it.

- **Importance:** how much a buyer or renter needs this in everyday decisions (doc 02 §5).
- **Ease:** this assessment's findings. Easy means an open licence plus a file or simple API. Moderate means a key, extra conditions or our own processing. Hard means a paid provider (DA-06). Blocked means no permitted route.

The ranking is a planning judgement, not a measured fact, and the founder can reorder it. Stage 6 issues follow this order (the children of #98).

| # | Wave | What the customer gets | Source | Importance | Ease | Notes |
|---|---|---|---|---|---|---|
| 1 | 0 Foundation | Correct area for every lookup | postcodes.io (postcode to coordinates, council, area codes) | Prerequisite | Easy (fair-use limit unverified) | Needed by crime, schools, stops, flood and amenities |
| 2 | 2 (needed for per-home data only) | The exact home ("Flat 5, not the building") | Licensed address provider (DA-06) | High | Hard (paid) | Not needed for area data: the first real release uses the postcode the user types (#1), and the user confirms their own unit. Needed for energy certificates, per-home sale history and autocomplete. England has free identifiers (OS Open UPRN) but no free address list |
| 3 | 1 | Transport stops nearby | NaPTAN | High (both) | Easy | Stops only; journey times are #13 |
| 4 | 1 | Schools nearby (type, phase) | DfE Get Information about Schools | High (families) | Easy (downloads) | Inspection results are #10 |
| 5 | 1 | Crime counts and the neighbourhood police team | data.police.uk | High (both) | Easy | Counts by category and month; never "safe" or "unsafe" (rule 4) |
| 6 | 1 | Flood: live warnings and river levels, plus a link to long-term risk | EA flood monitoring, EA checker (link only) | High (buyers: mortgage and insurance) | Easy (live); long-term has no API found | Never a prediction for one property |
| 7 | 1 | Nearby sold prices | HM Land Registry Price Paid | High (buyers) | Easy | Address use limited to price display |
| 8 | 2 | Shops, supermarkets, parks, pharmacies, police stations, hospitals, GP surgeries, clinics, dentists, childcare (locations; a childcare registration source, such as the Ofsted childcare register, would need its own assessment before real use) | OSM extract we download and query ourselves | High (both) | Moderate | Own attributed table (ODbL); map picture from FE-03 |
| 9 | 2 | Energy rating and likely energy cost range | Energy certificate register | High (both: bills) | Moderate (key; address restriction) | Needs #2 for UPRN matching; never actual bills |
| 10 | 2 | School inspection results | Ofsted data | High (families) | Moderate (licence unverified) | Framework and date, no single grade (doc 02 §7) |
| 11 | 2 | Broadband and mobile coverage | Ofcom API | Medium-high (home working) | Moderate (terms unread; mobile v1 API ends 30 Nov 2026) | Predicted availability, not a tested line |
| 12 | 2 | Mortgage context: the Bank Rate | Bank of England | Medium (buyers) | Easy | Feeds rate scenarios; the engine still calculates |
| 13 | 3 | Commute time to your own destinations | Routing provider (DA-06) | High (both) | Hard (paid or self-hosted) | Household criterion "40 minutes by public transport" |
| 14 | 3 | Planning applications nearby | Planning Data Platform | Medium (buyers) | Moderate (site was down) | "No record in this source" never means none |
| 15 | 3 | Leasehold: is the managing agent or freeholder active? | Companies House API | Medium (leasehold buyers) | Moderate (licence unverified) | Status facts only |
| 16 | 3 | Bus timetables | Bus Open Data Service | Medium | Moderate (key; limits unverified) | Before #13, or replaced by the routing provider |
| 17 | 4 | GPs, dentists and pharmacy services | NHS directory | Medium | Deferred (terms unverified) | |
| 18 | 4 | Air quality | Defra UK-AIR | Low-medium | Easy | Context, not a health judgement |
| 19 | 4 | Rail and London transport detail | National Rail, TfL | Medium (London, rail commuters) | Deferred (terms unverified) | |
| 20 | 4 | Radon | UKHSA | Low | Deferred (terms unverified; address report paid) | |
| — | — | Council tax band | User enters it, with a link to the VOA checker | High (cost) | Not available as data | Already a cost-engine input; no lookup is built (decision 0028) |

## Gaps and decisions for the founder

- **Address and routing (DA-06):** open sources give postcodes, UPRNs and stop points, not an address search or journey times. OSM's public Nominatim, tile and Overpass services are not for production. Recommendation: plan a paid address and routing provider (or self-hosted OSM) before stage 6; keep the prototype on sample data.
- **EPC address restriction:** EPC addresses cannot be used commercially without an OS or Royal Mail licence. Recommendation: match by UPRN, take the address from the licensed address provider, and have the register row in DA-05 reviewed before launch.
- **Council tax:** no permitted route. Recommendation: user enters the band, with a link to the VOA checker; do not build a lookup.
- **Unverified rows:** Planning Data, NHS, Ofcom terms, rail, TfL, Ofsted licence, radon, Companies House licence. Recommendation: re-check each official page when its integration is scheduled, and do not build on them until then.
- **OSM share-alike:** merging OSM extracts into Vestagraph's database may trigger ODbL share-alike. Recommendation: keep OSM data in a separate, attributed table, and get a short legal read before publishing any derived dataset.
- **Suggested order for the real-data epic (#98):** start with HM Land Registry, NaPTAN, GIAS, police, EA monitoring, Bank Rate, UK-AIR. Add the conditional ones after the legal and terms checks above.
