# 0046: A free public area check comes first; saved homes need an account

**ID:** PD-12  
**Status:** Accepted (founder, 11 Nov 2026: Option B)  
**Date:** 2026-11-11  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** [0045](0045-prototype-is-a-private-reference.md) ("the real product (stage 6) is the first public thing", and its deferral of SE-02 part 1 and FE-05 to stage 6); [0006](0006-prototype-centrepiece.md) ("the first public showcase"; "isn't launched publicly until both stories are complete"); the doc 02 §9 row "the clickable prototype is the first public showcase"; the stage timing of [0014](0014-privacy-and-data-protection.md) parts 1 and 2 (both now before the public area check); the stage 6 timing of the Aspire and OpenTelemetry packages in [0025](0025-ai-platform-capabilities.md) (now with the first API, at stage 5b); the order of doc 04 §9 stage 6, which builds data, accounts and privacy after the validation study; the register timing of SE-01 ("before questions workflow") and DA-03 to DA-06 ("before real data").

## Context
During phase 6 of the design flow (11 Nov 2026) the founder proposed a page where anyone types a postcode and sees what is around it (schools, transport, shops, health, flood, crime counts, sold prices), with a map and a download, usable by buyers, renters and businesses (#151). The founder then asked to "bring public pages forward", with accounts needed only for the home workspace.

The idea is already in the plan, but late. Decision 0014 says "anyone can type a postcode or address and see free public details without an account", and saving a home is where an account is likely needed. Area information is already the top data priority (`docs/references/data-sources.md`). What changes is **when** it goes public: before the full product, not after it.

## Options
### Option A: Keep the current order
Private prototype (stage 5), validation study, then the real product with data, accounts and privacy (stage 6). Lowest risk and cost, but nothing public for a long time, and the most useful free feature waits behind everything else.

### Option B: Public area check first, then the home workspace behind sign-in (recommended)
1. **Stage 5, area first:** right after the app shell and the component gallery, build the summary-first Nearby, the map and the new **Check an area** screen on fixtures, then the cost screens. The prototype stays private (0045).
2. **New stage 5b, public area check:** the smallest real-data slice that can go public with no accounts:
   - decisions first: the API framework, architecture and contract (BE-01 framework and BE-02, issue #92) with the observability foundation (0025); database and geospatial (DA-03), ingestion and caching (DA-04), source licences (DA-05), postcode lookup (DA-06, postcode only, no paid address lookup); hosting, infrastructure, environments, secrets, the domain and a budget cap (IN-01 to IN-05, with 0044's domain check); rate limiting; and privacy **parts 1 and 2** (SE-02, 0014: privacy notice, ICO fee check, device storage, lawful basis for search inputs, personal data in public records, log configuration and retention);
   - build: a minimal ASP.NET Core API, one adapter per free source with Live, Cached, Fallback or Unavailable labels (0029), our own cached copies so public traffic never hammers free services, attribution for every source, and the same honesty rules as the prototype;
   - launch publicly, with no accounts and no stored searches. **Searched postcodes never reach server, application or hosting logs** (0014): the postcode travels in the URL fragment or the request body, never the query string, and IP addresses are dropped or anonymised before logs are written.
3. **Then accounts (SE-01) and saved homes:** costs, questions, compare and what changed sit behind sign-in, and 0038's API keys build on the same accounts.

### Option C: Skip the prototype and build the real product now
Fastest to something public, but it loses the design reference that 0045 exists for, and the money and legal parts would be built before they are validated. Not recommended.

## Recommendation
**Option B.** The area check is useful on its own, uses free sources, needs no account and shows off what makes Vestagraph different (every fact with its source and limits). It also tests the data adapters, hosting and privacy foundations on the lowest-risk data before any personal data is stored.

**What it costs:**
- **Running costs**, for the first time: hosting and storage for cached datasets. Founder-only under `AGENTS.md`; a budget cap comes first (IN-05).
- **Privacy work moves earlier:** a searched postcode can hint at where someone may move (0014), so privacy parts 1 and 2 are settled, searches stay out of every log and the privacy notice is live before launch.
- **Licences:** each dataset's terms for public and commercial reuse are recorded before use (DA-05), including attribution in downloads.
- **The study (doc 02 §10)** can use the public page as well as the private prototype.

**Not decided here:** the identity provider and account model (SE-01), the hosting provider (IN-02), the order of sources (taken from the priority list in `docs/references/data-sources.md`), and the download format (a PDF or CSV with sources is the default to plan).

## Decision
**Option B**, accepted by the founder on 11 Nov 2026, who added: "that means we need marketing pages". The public site at launch is small and honest:
- the **landing page is the area check** (postcode box first), with short sections explaining it;
- **How it works**, **About the data** (sources, dates, limits and the attribution the licences require), the **privacy notice** (0014) and an **accessibility statement**;
- features that need an account (costs, compare, questions) are described only as "coming next" until they are live;
- no pricing page (PD-10 is open), blog, business page (#151) or one search page per postcode for now;
- the map gets an optional **3D view** (founder, 11 Nov 2026): a switch that tilts the map and raises buildings to their approximate heights, with 2D the default on phones and whenever reduced motion is on. It must not suggest flood or crime risk, and the list stays the accessible alternative.

## Consequences
- 0045's line "the real product (stage 6) is the first public thing" no longer applies: the **public area check** is the first public thing. The clickable prototype itself stays private.
- Doc 04 §9 gains stage 5b between stages 5 and 6, and the backlog gains an epic for it, with issues for each decision above.
- The register moves SE-01 to "before saved homes"; DA-03 to DA-06, BE-01's framework, BE-02, FE-05 and SE-02 parts 1 and 2 to stage 5b; and adds IN-04's domain and secrets before the public area check.
- `.design/prototype/` gains the Check an area screen (H5) and its build task; the information architecture gains the public route `/area` (postcode in the URL fragment, so it never reaches a log).
- Business use (#151) is answered by the same public page; any business-only feature still needs its own record.
- **Revisit if** running costs exceed the IN-05 cap, a key source's licence rules out public use, or the study shows the area check isn't what draws people in.
