# 0046: A free public area check comes first; saved homes need an account

**ID:** PD-12  
**Status:** Proposed (founder direction, 11 Nov 2026; the founder accepts or changes it in the pull request)  
**Date:** 2026-11-11  
**Stage:** 3  
**Supersedes in part, once accepted (no older text is rewritten):** [0045](0045-prototype-is-a-private-reference.md) ("the real product (stage 6) is the first public thing"); the order of doc 04 §9 stage 6, which builds data, accounts and privacy after the validation study; the register timing of SE-01 ("before questions workflow") and DA-03 to DA-06 ("before real data").

## Context
During phase 6 of the design flow (11 Nov 2026) the founder proposed a page where anyone types a postcode and sees what is around it (schools, transport, shops, health, flood, crime counts, sold prices), with a map and a download, usable by buyers, renters and businesses (#151). The founder then asked to "bring public pages forward", with accounts needed only for the home workspace.

The idea is already in the plan, but late. Decision 0014 says "anyone can type a postcode or address and see free public details without an account", and saving a home is where an account is likely needed. Area information is already the top data priority (`docs/references/data-sources.md`). What changes is **when** it goes public: before the full product, not after it.

## Options
### A. Keep the current order
Private prototype (stage 5), validation study, then the real product with data, accounts and privacy (stage 6). Lowest risk and cost, but nothing public for a long time, and the most useful free feature waits behind everything else.

### B. Public area check first, then the home workspace behind sign-in (recommended)
1. **Stage 5, area first:** build the app shell, the component gallery, the summary-first Nearby, the map and the new **Check an area** screen on fixtures before the cost screens. The prototype stays private (0045).
2. **New stage 5b, public area check:** the smallest real-data slice that can go public with no accounts:
   - decisions first: database and geospatial (DA-03), ingestion and caching (DA-04), source licences (DA-05), postcode lookup (DA-06, postcode only, no paid address lookup), hosting, infrastructure and a budget cap (IN-01 to IN-03, IN-05), rate limiting, and privacy part 1 (SE-02: privacy notice, ICO fee check, device storage);
   - build: a minimal ASP.NET Core API, one adapter per free source with Live, Cached, Fallback or Unavailable labels (0029), our own cached copies so public traffic never hammers free services, attribution for every source, and the same honesty rules as the prototype;
   - launch publicly, with no accounts and no stored searches beyond what hosting logs need (0014).
3. **Then accounts (SE-01) and saved homes:** costs, questions, compare and what changed sit behind sign-in, and 0038's API keys build on the same accounts.

### C. Skip the prototype and build the real product now
Fastest to something public, but it loses the design reference that 0045 exists for, and the money and legal parts would be built before they are validated. Not recommended.

## Recommendation
**Option B.** The area check is useful on its own, uses free sources, needs no account and shows off what makes Vestagraph different (every fact with its source and limits). It also tests the data adapters, hosting and privacy foundations on the lowest-risk data before any personal data is stored.

**What it costs:**
- **Running costs**, for the first time: hosting and storage for cached datasets. Founder-only under `AGENTS.md`; a budget cap comes first (IN-05).
- **Privacy work moves earlier:** a searched postcode can hint at where someone may move (0014), so logs are minimised and the privacy notice is live before launch.
- **Licences:** each dataset's terms for public and commercial reuse are recorded before use (DA-05), including attribution in downloads.
- **The study (doc 02 §10)** can use the public page as well as the private prototype.

**Not decided here:** the identity provider and account model (SE-01), the hosting provider (IN-02), the order of sources (taken from the priority list in `docs/references/data-sources.md`), and the download format (a PDF or CSV with sources is the default to plan). The map gets an optional **3D view** (founder, 11 Nov 2026): a switch that tilts the map and raises buildings to their approximate heights, with 2D the default on phones and whenever reduced motion is on. It must not suggest flood or crime risk, and the list stays the accessible alternative.

## Decision
Pending the founder's acceptance.

## Consequences (if accepted)
- 0045's line "the real product (stage 6) is the first public thing" no longer applies: the **public area check** is the first public thing. The clickable prototype itself stays private.
- Doc 04 §9 gains stage 5b between stages 5 and 6, and the backlog gains an epic for it, with issues for each decision above.
- The register moves SE-01 to "before saved homes" and DA-03 to DA-06 to "before the public area check".
- `.design/prototype/` gains the Check an area screen (H5) and its build task; the information architecture gains the public route `/area?postcode=`.
- Business use (#151) is answered by the same public page; any business-only feature still needs its own record.
- **Revisit if** running costs exceed the IN-05 cap, a key source's licence rules out public use, or the study shows the area check isn't what draws people in.
