# Area display: engineering research (issue #143, track B)

**Status:** research notes for the founder to review. Nothing here is decided. It feeds FE-03 maps and charts (#75), FE-04 frontend practices (#76), IN-02 hosting (#81) and the Nearby screen specification (#68). The UX track is in `area-display-ux.md`.
**Date:** 11 Nov 2026. Every external fact links its official source and was checked on 11 Nov 2026 unless marked **unverified**. Bundle sizes were **measured on 11 Nov 2026**: `gzip -9` of the published `dist` files from jsDelivr, at the npm `latest` version on that day.
**Scope:** the Next.js prototype on sample data (IN-01: it reads fixture files and has no backend), then the stage 6 product with real data.

---

## 1. Recommendation summary

1. **The list is the product and the map is an enhancement.** The area list is server-rendered from the fixtures. It is complete on its own, it is the default view on mobile and it is in the HTML before any map code loads. The map is a client-only island that is lazy-loaded and never on the critical path.
2. **Map library: MapLibre GL JS 6.x** (BSD-3-Clause, no telemetry calls in the bundle, WebGL 2 vector rendering). It is the only option that is open source, renders vector tiles natively, runs without an account or API key and is not tied to a vendor.
3. **Use our own thin React component, not a wrapper.** It is about 150 lines around `maplibre-gl`. That means one fewer package, full control of focus and ARIA, and no waiting for a wrapper to support a new MapLibre major version (v6 made the library ESM-only).
4. **Prototype basemap: a fictional-town basemap (GeoJSON in the repository), not real map tiles.** The sample homes are in the fictional town "Northbridge" with fictional `NB` postcodes. Putting synthetic shops and schools onto a real town's streets would describe a real place with invented facts (rule 1). The fictional basemap is about 50 KB, has no hosting cost, needs no attribution and gives deterministic tests. **Needs a founder decision (Q1).**
5. **Stage 6 basemap: self-hosted Protomaps PMTiles** (an England extract), stored in cheap object storage behind a CDN. It costs nothing at zero traffic and passes no viewer data to a tile vendor. A provider's free tier (MapTiler or Stadia) is the fallback if self-hosting slips. Mapbox and Google are only comparators: proprietary SDKs, and the SDK sends data back to the vendor.
6. **The fixtures need positions.** `area.json` and `homes.json` have no coordinates today, so there is nothing to put on a map. Add a `position` object (`lon`, `lat`, `method: "synthetic"`) to homes and to place-type items, through a founder-merged schema change. Add a test that each position agrees with the item's `distanceMetres` input within a tolerance (Q2).
7. **Typed view models are built at build time. The UI does no calculation.** TypeScript types are generated from the JSON Schemas, and gap statuses are a discriminated union with exhaustive `switch` checks, so adding a new status breaks the build rather than rendering blank. Distances are shown exactly as recorded ("400 m"), never converted or recalculated in the UI (rule 2, Q6).
8. **Budgets are enforced in CI:**
   - Nearby route first-load JS of 170 KB gzip or less, without the map.
   - Map chunk of 470 KB gzip or less, loaded on intent.
   - LCP of 2.5 s or less, INP of 200 ms or less and CLS of 0.1 or less, at the 75th percentile on Lighthouse's mobile profile.
   - Enforced by Lighthouse CI and a bundle-size check.
9. **Testing:** Reqnroll + Playwright for .NET `@ui` scenarios (decision 0043) cover selection sync, gaps, reduced motion, attribution and "no third-party requests". The other test layers:
   - axe through `Deque.AxeCore.Playwright`;
   - ARIA snapshots (`ToMatchAriaSnapshotAsync`) for the list;
   - a narrow canvas visual check on the deterministic local basemap. Playwright for .NET has no built-in screenshot assertion, so it uses an in-browser pixel diff and needs no new package.
10. **Privacy by construction:**
    - no tracker or vendor SDK;
    - no geolocation without an explicit tap;
    - the "drop a pin" location stays on the device and out of shareable URLs by default;
    - a CSP that allows only our own origin, plus the tile host in stage 6.

**Decisions this needs:**
- **FE-03 (#75):** points 2–5.
- **FE-04 (#76):** points 3, 7, 8 and 9.
- **IN-02 (#81):** where the PMTiles file lives.
- **#120 follow-up:** point 6.
- **Founder package approvals:** section 10.

---

## 2. Options matrix

### 2.1 Map libraries

| | **MapLibre GL JS** | **Leaflet** | **OpenLayers** | **Mapbox GL JS** | **Google Maps JS API** |
|---|---|---|---|---|---|
| Version (npm, 11 Nov 2026) | 6.17.0 | 1.9.4 stable; 2.0 in beta ([install page](https://leafletjs.com/install.html)) | 10.11.0 | 3.34.2 | Loaded from Google; not on npm |
| Licence | BSD-3-Clause (on the 0027 allow-list) | BSD-2-Clause (allowed) | BSD-2-Clause (allowed) | Proprietary: "licensed under the Mapbox TOS for use only with the relevant Mapbox product(s)" for an active account holder ([LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt)). Not on the allow-list | Proprietary service terms |
| JS size, gzip (measured) | `maplibre-gl.mjs` 295 KB + worker 147 KB, plus CSS 10 KB | `leaflet.js` 42 KB, plus CSS 3.5 KB. Vector tiles need a plugin, e.g. `protomaps-leaflet` (BSD-3) | `ol.js` full build 298 KB. Tree-shaken builds are smaller (not measured) | `mapbox-gl.js` 524 KB | Not measurable (loaded at run time) |
| Rendering | WebGL 2 (the bundle calls `getContext('webgl2')` and throws if it is missing) | DOM/SVG/Canvas, raster-first | Canvas/WebGL | WebGL | Vendor |
| Vector tiles and PMTiles | Native. `pmtiles://` protocol through `addProtocol` ([Protomaps MapLibre guide](https://docs.protomaps.com/pmtiles/maplibre)) | Through a plugin (canvas rendering) | Native vector tiles; PMTiles through a community source (unverified) | Native, Mapbox tiles | Vendor tiles only |
| Accessibility built in | Canvas gets `role="region"` and an `aria-label`, and is focusable when interactive. Keyboard pan, zoom and rotate ([KeyboardHandler](https://maplibre.org/maplibre-gl-js/docs/API/classes/KeyboardHandler/)). Markers get an `aria-label`. Respects `prefers-reduced-motion` (seen in the bundle: `matchMedia('(prefers-reduced-motion: reduce)')`; behaviour not documented, **unverified**) | Best: markers are focusable DOM, with Enter/Space and Escape handling and documented guidance ([Leaflet accessibility](https://leafletjs.com/examples/accessibility/)) | Keyboard pan and zoom (unverified) | Similar to MapLibre | Vendor |
| Telemetry | Bundle has no `events.mapbox.com`, `api.mapbox.com` or `sendBeacon` (grep, 11 Nov 2026) | None known | None known | Bundle references `events.mapbox.com`; the licence says the SDK sends "de-identified location and usage data" | Vendor-controlled |
| Account, key, lock-in | None | None | None | Account, token and vendor tiles required | Key, billing account and vendor tiles |
| Maintenance | Active. Major v6 (ESM-only, new worker loading; [v5→v6 guide](https://github.com/maplibre/maplibre-gl-js/blob/main/docs/guides/v5-to-v6-migration-guide.md)) | 1.x is in maintenance; 2.0 is an ESM rewrite still in beta | Active | Active | Vendor |

### 2.2 Tile sources

Workload assumptions (labelled, not facts):
- 3 map sessions per user per month;
- 40 tile requests per session;
- so 1k users means 3k sessions and 120k tiles, and 10k users means 30k sessions and 1.2M tiles.

The costs below are estimates for comparison, with the working shown. They are not product figures.

| Tile source | Licence, attribution | Prototype | 1k users/month | 10k users/month | Privacy | Caching and offline |
|---|---|---|---|---|---|---|
| **Fictional-town GeoJSON in the repository** (prototype only) | Ours; no attribution needed | £0 | n/a | n/a | No requests leave our origin | Bundled; works offline |
| **Self-hosted Protomaps PMTiles** on Cloudflare R2 | Basemap is an "ODbL Produced Work"; "OpenStreetMap attribution required" ([downloads](https://docs.protomaps.com/basemaps/downloads)) | £0 | **$0**: 120k reads is well under R2's free 10M Class B operations a month, and egress is free ([R2 pricing](https://developers.cloudflare.com/r2/pricing/)) | **$0–5**: 1.2M reads is still within the free tier. Protomaps quotes "about $5 USD" for a Cloudflare deployment with Z/X/Y URLs and edge caching ([deploy](https://docs.protomaps.com/deploy/)) | Only our host sees which area was viewed | Edge cache. Our HTTP cache headers; a service worker is allowed (our data) |
| **MapTiler Cloud** | Free plan: "MapTiler logo on the map"; "testing, PoC, prototyping, personal, or non-commercial use". Service pauses at the limit ([pricing](https://www.maptiler.com/cloud/pricing/)) | $0 (5k sessions) | $0 (3k sessions) | **$42.50**: Flex $30 for 25k sessions, plus 5k × $2.50/1k overage. How tile requests count within a session is **unverified** | Vendor sees viewport requests and the key | Vendor terms |
| **Stadia Maps** | Free plan is "non-commercial or evaluation purposes"; demonstration is exempt. Server-side caching prohibited ([terms](https://stadiamaps.com/terms-of-service/)) | $0 (200k credits; 1 credit per vector tile) | **$20** on Starter for commercial use (1M credits) | **$26**: Starter $20, plus 0.2M × $0.03/1k ([pricing](https://stadiamaps.com/pricing/)) | Vendor sees requests | Client cache only, as headers allow (7 days if none) |
| **Mapbox** | Proprietary SDK and tiles | $0 | $0 (50k loads free) | $0 (30k is under 50k) ([pricing](https://www.mapbox.com/pricing)) | SDK telemetry | Vendor terms |
| **Google Dynamic Maps** | Proprietary | $0 | $0 (10k free events) | **$140**: 20k × $7/1k ([pricing list](https://developers.google.com/maps/billing-and-pricing/pricing)) | Vendor | Vendor terms |
| **OSM public tiles** | Policy: no SLA, "can be blocked without notice", no offline use ([tile policy](https://operations.osmfoundation.org/policies/tiles/), via `docs/references/data-sources.md`) | Not suitable | Not suitable | Not suitable | — | Bulk download and offline use forbidden |

**Recommendation: MapLibre GL JS with self-hosted PMTiles for stage 6, and a fictional GeoJSON basemap for the prototype.**
- **Why MapLibre over Leaflet:** Leaflet is 7× lighter and has better built-in marker accessibility. But it is raster-first, its 2.0 rewrite is still in beta, and vector PMTiles would need a second rendering plugin. MapLibre lets one style drive both the fictional prototype map and the real England map. Section 5 closes most of the accessibility gap by using DOM markers.
- **Cost and privacy:** self-hosting is the cheapest option at every scale above, it is the only one that sends no viewer data to a vendor, and it follows decision 0022's order (free first).
- **The real cost of self-hosting** is operational, not money:
  - a monthly extract job;
  - style, glyph and sprite assets to host ourselves (the defaults live on `protomaps.github.io`; [Protomaps MapLibre styles](https://docs.protomaps.com/basemaps/maplibre));
  - a deployment that serves range requests.
- **Hosting caveats:**
  - Cloudflare Pages caps a single asset at 25 MiB ([limits](https://developers.cloudflare.com/pages/platform/limits/)), so the England file goes in R2, not in the static site.
  - GitHub Pages is not allowed for an "online business" ([limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
  - The planet is "roughly 120 gigabytes" at zoom 0–15, and each zoom level "roughly doubles" the size ([downloads](https://docs.protomaps.com/basemaps/downloads)). An England extract at z15 is likely a low single-digit number of GB (**unverified**: measure it in the spike).

---

## 3. Architecture

### 3.1 Data flow

```
packages/fixtures/data/area.json ─┐
packages/fixtures/data/homes.json ├─► build time (Next.js server, static) ─► AreaViewModel[] ─► <AreaList> (server-rendered HTML)
packages/fixtures/data/evidence.json ┤      lib/area/load.ts (server-only)                    └► serialised GeoJSON props ─► <AreaMap> (client island, lazy)
packages/fixtures/generated/costs.json ┘  types: generated from packages/fixtures/schema/*.schema.json
```

- **Types:**
  - `json-schema-to-typescript` generates `types/fixtures.d.ts` from each schema in a `make generate-types` step.
  - `make check` fails if the generated types are stale, the same pattern as `generated-check`.
  - No hand-written fixture types.
- **Loader (`server-only`):**
  - reads the JSON;
  - asserts the schema version;
  - groups items by `homeId` and `topic`;
  - joins `evidence.json` for energy items and `costs.json` figure IDs for anything cost-related.
- **Rule 2:**
  - The loader may group, filter, sort by a field that already exists and format text.
  - It may not add, subtract, convert units or derive distances.
  - "400 m" is formatting. "0.4 km" is a conversion and needs an engine or fixture field (Q6).
  - Sort order "nearest first" uses the recorded `distanceMetres` input.
- **Gap statuses travel as a discriminated union.** The fixture statuses are `recorded`, `stale`, `no-record-in-source`, `not-covered` and `source-failed` (counted in `area.json` on the area-fixtures branch: 65 / 2 / 8 / 11 / 1 of 87 items).

```ts
type AreaItemVM =
  | { kind: "recorded"; id; topic; label; value; source; doesNotEstablish; position?: LngLat }
  | { kind: "stale"; ...same; staleSince: string }          // shown with its date, never hidden
  | { kind: "gap"; id; topic; gap: "no-record-in-source" | "not-covered" | "source-failed"; source; coverage };
// Every renderer ends with `default: assertNever(item)`.
```

- **0029 provenance:** the prototype has no live retrieval, so every item shows "Sample data · {source.date}". The view model maps the five statuses to decision 0029's dimensions:
  - `source-failed` → Unavailable;
  - `stale` → Cached past its refresh period.
  - Stage 6 adapters add a real `retrieval` field (Live/Cached/Fallback/Unavailable) that passes straight through (Q5).
- **Map input:**
  - one `FeatureCollection` per home, built only from items with `kind !== "gap"` and a `position`.
  - Items without a position are counted, not dropped: the map legend says "N items have no map position — see the list".
  - A gap never becomes a missing pin that reads as "none nearby" (rule 7).

### 3.2 Component boundaries

| Component | Kind | Responsibility |
|---|---|---|
| `NearbyPage` (`app/homes/[homeId]/nearby/page.tsx`) | Server component, static | Loads view models; renders the header, topic filter, `AreaList` and the `MapSlot` placeholder |
| `AreaList` / `AreaItem` / `GapItem` | Server components | The full information: label, value, source and date, coverage, "does not establish" text, status chip (text plus icon, never colour alone) |
| `NearbyController` | Client component (small) | Owns selection, view mode and topic filters; syncs to the URL; hosts the live region |
| `MapSlot` | Client component | Fixed-size placeholder (no CLS); decides *when* to load; `next/dynamic(() => import('./AreaMap'), { ssr: false })`. Next.js allows `ssr: false` only inside client components ([lazy loading](https://nextjs.org/docs/app/guides/lazy-loading)) |
| `AreaMap` | Client, lazy | MapLibre instance, basemap style, home marker, POI markers, attribution, map-only controls |
| `ItemSheet` (mobile) / side panel (desktop) | Client | Details of the selected item; native `<dialog>` when fully expanded |

### 3.3 State

- **One source of truth:** `selectedItemId`, `view` (`list` | `map`, mobile only) and `topics[]` live in the URL and are mirrored in React state through `useSearchParams` and `router.replace`, with no scroll and no history entry per selection.
- **Shareable URL:** `/homes/B1/nearby?topics=transport,schools&item=B1-AREA-AMENITY-1`
  - Compare uses `/compare?homes=B1,B2,R1&topic=schools`.
  - The parser rejects more than 3 homes and unknown IDs, and falls back to a visible message, never to silently dropping one.
- **Not in the URL:** map centre and zoom (noisy, and they reveal the area a user browsed), and the dropped pin (section 8).
- **Sync rules:**
  - list click → map `easeTo` the item (or `jumpTo` under reduced motion) and open the sheet;
  - marker activate → list item `aria-current="true"` and scrolled into view (`block: "nearest"`), sheet open;
  - sheet close → focus returns to the invoking element.
  - All three subscribe to the one `selectedItemId`; none calls another directly.

---

## 4. Performance budget (mid-range phone)

Reference device and network are Lighthouse's default mobile throttling: 150 ms RTT, 1.6 Mbps down, 4× CPU slowdown, "a mid-tier mobile device" ([throttling](https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md)).

| Budget | Target | How it is measured |
|---|---|---|
| LCP | 2.5 s or less | Lighthouse CI, mobile, 3 runs, median ([thresholds](https://web.dev/articles/vitals)) |
| INP | 200 ms or less | Lab proxy: TBT 200 ms or less in Lighthouse; plus a Playwright scenario that times list→map selection with `PerformanceObserver` `event` entries |
| CLS | 0.1 or less, aiming for 0 | Lighthouse CI; `MapSlot` reserves its box with `aspect-ratio` |
| Nearby first-load JS (no map) | 170 KB gzip or less, including framework | Bundle-size check on `next build` output |
| Map chunk | 470 KB gzip or less: MapLibre 295 + worker 147 + pmtiles 8 + own code ~15 | Bundle-size check; the worker is a separate same-origin file (`setWorkerUrl`; v6 guide) |
| Style + glyphs + sprite, first view | 120 KB or less (one font stack, Latin range only; one sprite at 1× and 2×) | Playwright network log in the visual scenario |
| Tiles, first viewport | 400 KB or less at z14–15; `maxzoom` 15 in the extract, overzoom above | Same; stage 6 spike |
| Fictional basemap (prototype) | 60 KB gzip or less GeoJSON | File-size test |

- **Lazy-load trigger:** the map is never in the initial bundle.
  - **Mobile:** load only when the user selects "Map", with a prefetch on `pointerdown` or focus of that toggle.
  - **Desktop (split view):** load when `MapSlot` intersects the viewport *and* after `requestIdleCallback` once the list is hydrated.
  - **Save-Data on, or `navigator.connection.effectiveType` 2G:** show a "Load map" button instead. (Network Information API support varies by browser, **unverified**; feature-detect it.)
- **Markers and clustering:**
  - The prototype has at most about 25 positioned items per home: 87 items over 5 homes, many of them gaps. Use **DOM markers (`<button>`)** for accessibility, and no clustering.
  - Switch to a GeoJSON source with MapLibre's built-in `cluster: true` (radius 40–50 px, `clusterMaxZoom` 14; [cluster example](https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/)) plus symbol layers once a view can show more than 50 points or more than 4 overlap at the default zoom.
  - The separate `supercluster` package (ISC) is not needed.
- **Icons:**
  - one SVG sprite for list icons, inlined, about 6 KB;
  - the map sprite is generated from the same SVGs at build time, so list and map icons match.
- **Clean-up:** call `map.remove()` on unmount. MapLibre warns that its worker pool persists otherwise. Keep a single map instance when switching between homes (`setStyle` / `setData`, not remount).

---

## 5. Accessibility engineering (WCAG 2.2 AA)

- **The list is a complete alternative.** Every fact, source, date, gap and caveat is in the list. The map adds only spatial arrangement. Test: hide the map and every scenario still passes (section 6).
- **Structure:**
  - The list is `<section aria-labelledby>` with `<ul>`. Each item is an `<article>` whose heading is the place or topic.
  - The selected item has `aria-current="true"`.
  - Topic filters are a group of `aria-pressed` toggle buttons, not a tab widget, because they filter rather than switch panels.
  - List/Map on mobile is a two-button segmented control with `aria-pressed`.
- **Map container:**
  - MapLibre gives the canvas `role="region"` and a label. Override the label to "Map of sample area around {home label}. The list above has the same information."
  - Show the keyboard shortcuts as visible text next to the map. Leaflet's guide makes the same point: nothing on the map tells users the keys exist.
  - Disable keyboard rotation (`map.keyboard.disableRotation()` keeps zoom) and drag-rotate/pitch: they add disorientation and no information.
- **Markers:**
  - Each marker is a `<button>` with an `aria-label` such as "Mill Road supermarket (synthetic), 400 m straight-line, sample data".
  - **Roving tabindex:** one Tab stop into the marker group; arrow keys move in *list order*, not geographic order, so the two views agree.
  - Enter opens the sheet; Escape returns focus to the map region.
  - Zoom in, zoom out and "Fit to home" buttons give the single-pointer alternative to dragging that WCAG 2.5.7 asks for (its own example is map direction buttons; [2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)).
- **Announcing:**
  - one polite live region in `NearbyController`: "Selected: {label}. {status text}."
  - Filter changes announce "Showing 7 items in 2 topics; 2 topics have gaps".
  - Debounce at 300 ms, and never announce on map pan.
- **Bottom sheet:**
  - **Peek state** is a non-modal region. Set `scroll-padding-bottom` to the sheet height so a focused list item is never fully hidden ([2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) lists sticky footers and non-modal dialogs as the risk).
  - **Expanded state** is a `<dialog>` opened with `showModal()`. That makes the background inert natively, so focus-trap libraries are not needed.
  - Focus moves to the sheet heading on open and back to the invoker on close. The drag handle has a button alternative ("Expand details").
- **Reduced motion:** see section 9. MapLibre camera moves use `jumpTo` when `matchMedia('(prefers-reduced-motion: reduce)')` matches.
- **Colour:**
  - Use doc 03's tokens: forest `#153F35`, ink `#182923`, amber `#8F560E`, red `#A33636`, which reach 4.5:1 or more as text on white, paper and sage.
  - Map pins need 3:1 against the basemap (non-text contrast), so use a white 2 px halo.
  - Status is always text plus icon. Gaps use a dashed outline in the list and no pin on the map.
  - Verify a dark-mode basemap flavour separately.
- **What a canvas map cannot do, and the mitigation:**
  - Canvas labels (street names, basemap POIs) are invisible to screen readers, cannot be zoomed by text-resize and are not in the accessibility tree.
  - Mitigations:
    1. every meaningful point is a DOM marker or is in the list;
    2. basemap POI labels are hidden in our style, so the only POIs are ours, with sources;
    3. canvas content is never the only carrier of meaning;
    4. if WebGL 2 is unavailable, the map slot shows "Map unavailable on this device — all information is in the list".

---

## 6. Testing strategy (decision 0043)

| Layer | Tool | What it proves | Gate |
|---|---|---|---|
| Data contract | NUnit/Reqnroll data steps (exist from stage 3) | Every England home has each required topic or an explicit gap; every positioned item agrees with its `distanceMetres` within ±15% (an independently worked haversine check in the *test*, which rule 2 allows); gap items carry no position | `make check` |
| Types | `generate-types` + `tsc --noEmit` | Schemas and UI agree; an unhandled status fails at compile time | `make check` (stage 5) |
| `@ui` behaviour | Reqnroll + Microsoft.Playwright for .NET | Scenarios below | `make check` from stage 5 |
| Accessibility | `Deque.AxeCore.Playwright` (needs approval) + ARIA snapshot (`ToMatchAriaSnapshotAsync`, [docs](https://playwright.dev/dotnet/docs/aria-snapshots)) | No axe violations at WCAG 2.2 AA tags on list, map-open and sheet-open states; list structure is stable | `make check` |
| Canvas visual | Playwright `ScreenshotAsync` on the map locator, compared in-browser | Pins, halo and attribution render on the deterministic basemap | CI only, pinned Linux container |
| Performance | Lighthouse CI + bundle-size check | Section 4 budgets | CI |

Example scenarios (IDs are illustrative; #68 assigns the real ones):

```gherkin
@ui @buying
Scenario: NEAR-xx selecting a list item selects the same marker
  Given the buyer story at step 1 with home "B1"
  And the Nearby screen is open in map view on a desktop viewport
  When I activate list item "B1-AREA-AMENITY-1"
  Then marker "B1-AREA-AMENITY-1" is pressed
  And the details panel shows source label and date from item "B1-AREA-AMENITY-1"
  And the live region announces the item label

@ui @renting
Scenario: NEAR-xx a source failure is shown, not hidden
  Given the renter story with home "R1"
  When the Nearby screen opens
  Then item "R1-AREA-CRIME-2" shows status "source-failed"
  And no marker exists for "R1-AREA-CRIME-2"
  And no text shows "0" or "none" for that topic

@ui
Scenario: NEAR-xx reduced motion jumps instead of flying
  Given the browser prefers reduced motion
  When I activate list item "B1-AREA-TRANSPORT-1"
  Then the map camera reaches the item with no animation frames between

@ui
Scenario: NEAR-xx the map makes no third-party requests and shows attribution
  When the Nearby map has loaded
  Then every network request went to the prototype's own origin
  And the attribution control is visible
```

**Mechanics:**
- **Waiting:** the map container exposes `data-map-state="loading|idle|error"`, set from MapLibre's `idle` and `error` events. Steps wait on it, never on timeouts.
- **Determinism:**
  - Use `ReducedMotion = ReducedMotion.Reduce` on the browser context ([emulation](https://playwright.dev/dotnet/docs/emulation)).
  - Set MapLibre `fadeDuration: 0` in test builds.
  - Fix the viewport.
  - Use the fictional basemap, or a small committed fixture PMTiles in stage 6.
  - `page.RouteAsync("**/*")` aborts any non-local host, which doubles as the privacy test.
- **Reduced-motion check:** count `move` events between `movestart` and `moveend`. With `jumpTo` there is exactly one.
- **Visual regression:**
  - Playwright for .NET documents screenshot capture to a byte array "to pass to a third-party pixel diff tool" and has no screenshot assertion ([screenshots](https://playwright.dev/dotnet/docs/screenshots)).
  - **Recommended:** a ~40-line test helper that loads the baseline and actual PNGs into an `OffscreenCanvas` *inside the browser* (`EvaluateAsync`) and counts pixels whose colour differs by more than a threshold. It fails above 0.5% of pixels. No new package is needed.
  - **Alternative:** `Verify.NUnit` + `Verify.ImageMagick` (MIT; Magick.NET Apache-2.0; the bundled native ImageMagick licence must be checked against 0027). It needs approval.
  - Baselines live in the repository and are regenerated only by an explicit `make update-snapshots`.
  - WebGL output differs by GPU and driver, and headless Chromium falls back to software rendering (**unverified** for the CI runner), so visual tests run only in the pinned Playwright container and stay out of local `make check` if they flake.
  - Keep them few: one per home and one with a sheet open.

---

## 7. Failure modes and resilience

| Failure | Detection | Behaviour |
|---|---|---|
| Map JS chunk fails to load | `next/dynamic` error boundary | Slot shows "Map couldn't load. All information is in the list." with a Retry button; list unaffected |
| No WebGL 2 | MapLibre throws at construction | Same message, worded for the device; no retry loop |
| Style, glyph or tile requests fail (offline or host down) | `map.on('error')`; tile `sourcedataabort` | Our markers still render on a plain background (they are DOM). Banner: "Base map unavailable — positions shown without streets". Never a blank map that implies nothing is nearby |
| Slow network | No `idle` within 8 s | Keep the skeleton and show "Still loading the map…"; the list is already usable |
| Partial data (gaps, stale, failed source) | View-model status | Gap rows in the list with their own wording; legend counts items without positions; stale items show their date and "stale" text |
| WebGL context lost (mobile background) | `webglcontextlost` | Recreate the map on `visibilitychange`; MapLibre 6.16 fixed workers stopping after iOS shut them down to save memory ([changelog](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md)) |
| Attribution hidden | `@ui` test | Attribution control always rendered, `compact` on narrow screens. OSMF allows collapsing to an "(i)" only after interaction or 5 seconds, and the licence must stay findable ([attribution guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines)). The fictional basemap carries "Sample map — fictional area" instead |
| Stage 6 tile host down | Adapter-style status on the tile source | Label "Base map: Unavailable" (decision 0029 wording); fallback provider only if it is a named alternative with its own attribution |

**Offline:**
- The prototype's static pages and fictional basemap can be cached by a service worker, but this is optional and not worth building in stage 5.
- With a provider's tiles, offline caching is limited by their terms. Stadia prohibits server-side caching and caps on-device caching. This is one more reason to self-host.

---

## 8. Privacy and security

- **No trackers.**
  - MapLibre has no vendor telemetry in the bundle (grep above).
  - No analytics in the prototype until FE-05 (#85) decides it.
  - Self-hosted tiles mean no third party learns which area a visitor looked at. With a provider, every pan reveals the viewport to them.
- **Geolocation:**
  - MapLibre's `GeolocateControl` (it references `navigator.geolocation`) is **not added**.
  - If "use my location" is ever offered, it is a button that explains first, then calls the browser API once, never on page load. The result stays in memory.
  - Playwright tests assert that no permission prompt appears (no `geolocation` permission granted in context).
- **The dropped pin** (founder choice: map pin included):
  - It can reveal a workplace or a child's school, so it is personal data.
  - Keep it in `sessionStorage`, out of the URL by default.
  - A "Share this view" action asks before including it.
  - Never send it to any outside service. Routing is DA-06 (stage 6) and goes through an adapter.
- **CSP** (static export headers, or Next.js middleware; FE-04):

  ```
  default-src 'self'; script-src 'self'; worker-src 'self'; img-src 'self' data: blob:;
  connect-src 'self' [stage 6: https://tiles.<our-domain>]; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'
  ```

  - MapLibre v6 with a self-hosted worker needs only `worker-src 'self'`; `blob:` is needed only when it is loaded from a CDN (v5→v6 migration guide).
  - `style-src 'unsafe-inline'` covers MapLibre's inline element styles. Try removing it in the spike (**unverified** whether it is needed).
- **Keys:** the prototype needs none. If a provider is chosen in stage 6, its key is a public, referrer-restricted key with a provider-side spend cap. No secret key ever reaches the client, and none is committed (rule 5).
- **Supply chain:**
  - pin exact versions;
  - Dependabot;
  - CodeQL already covers JS/TS (decision 0027);
  - load MapLibre from our own bundle, not a CDN.

---

## 9. Motion implementation

- **What moves:**
  - sheet open and close;
  - the selected marker's emphasis;
  - the camera easing to a selected item;
  - list ↔ map view change on mobile, as a cross-fade, not a slide.
- **No other motion:** no ambient animation, no animated counters, no pulsing pins (decision 0005, "no theatrical agent activity").
- **Durations:**
  - 150 ms for state emphasis (opacity and outline);
  - 200–250 ms for the sheet (`transform: translateY`);
  - camera `easeTo` at 400 ms or less with `essential: false`.
  - Easing: `cubic-bezier(0.2, 0, 0, 1)`.
- **Tokens:** `--motion-fast`, `--motion-medium` and `--motion-camera` in CSS. Under `@media (prefers-reduced-motion: reduce)` they become `0ms`, and opacity-only fades remain at 100 ms or less where a change of state must be noticed. MDN names "scaling or panning large objects" as vestibular triggers ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)), so camera moves become `jumpTo`.
- **No layout shift:**
  - Animate only `transform` and `opacity`.
  - The sheet is `position: fixed` and never resizes the list. Content padding is reserved through `scroll-padding`.
  - The marker emphasis uses `outline` and `transform: scale`, never border width.
- **CSS only:** use CSS transitions and the View Transitions API where supported, as progressive enhancement with a feature check. No animation library.

---

## 10. Packages to propose

**None of the JavaScript packages are on the pre-approved list** (decisions 0035 point 9 and 0043), so each needs a founder merge when first added. Next.js, React and TypeScript are already chosen by decision 0020, and the first frontend pull request brings them in.

| Package | Licence | Purpose | Cost | When | Status |
|---|---|---|---|---|---|
| `maplibre-gl` 6.x | BSD-3-Clause | Map renderer | Free | Stage 5 | **Needs founder approval** |
| `json-schema-to-typescript` 16.x | MIT | Generate UI types from fixture schemas | Free; build-time only | Stage 5 | **Needs founder approval** |
| `Deque.AxeCore.Playwright` 4.x (NuGet) | MIT (depends on `Deque.AxeCore.Commons`, MPL-2.0, on the allow-list) | axe checks in `@ui` scenarios | Free | Stage 5 | **Needs founder approval** |
| `@lhci/cli` 0.x | Apache-2.0 | Core Web Vitals budgets in CI | Free; CI minutes | Stage 5 | **Needs founder approval** (0.x: minor bumps count as major) |
| `size-limit` + `@size-limit/preset-app` 14.x | MIT | JS bundle budgets | Free | Stage 5 | **Needs founder approval**; alternative: a 30-line script over `next build` output, no package |
| `pmtiles` 4.x | BSD-3-Clause | `pmtiles://` protocol for MapLibre | Free | Stage 6 spike | **Needs founder approval** |
| `@protomaps/basemaps` 5.x | BSD-3-Clause | Generates the basemap style layers | Free | Stage 6 spike | **Needs founder approval** |
| `pmtiles` CLI (go-pmtiles) | BSD-3-Clause (**unverified**) | `pmtiles extract` of England at `--maxzoom 15` | Free; build tool, not shipped | Stage 6 | **Needs founder approval** |
| Protomaps basemap build (data) | ODbL Produced Work; OSM attribution required | Basemap tiles | Free data; R2 hosting $0–5/month at the volumes above | Stage 6 | **Founder decision** (running cost, IN-02) |
| `Verify.NUnit` + `Verify.ImageMagick` | MIT (+ Magick.NET Apache-2.0; check native ImageMagick licence) | Image diff, only if the in-browser diff proves insufficient | Free | Only if needed | **Needs founder approval** |
| *Not proposed:* `react-map-gl` / `@vis.gl/react-maplibre` (MIT), `supercluster` (ISC), `focus-trap-react` (MIT), `web-vitals` (Apache-2.0) | — | Covered by our own thin component, MapLibre's built-in clustering, native `<dialog>`, and Lighthouse (field data waits for FE-05) | — | — | Can be reconsidered if a need appears |

---

## 11. Risks and open questions

1. **Q1. Prototype basemap: fictional town or real map?** Synthetic `NB` homes on a real basemap would place invented supermarkets and crime counts on real streets, which is a rule 1 risk and confusing.
   - **Recommendation:** a fictional "Northbridge" basemap drawn as GeoJSON (roads, a river, a park, a station). It is labelled "Sample map — fictional area" and drawn with the same MapLibre style tokens.
   - Run a stage 6 spike that renders a real England PMTiles extract to measure size and performance.
2. **Q2. Positions in the fixtures.** There are no coordinates in `area.json` or `homes.json`, so the map cannot be specified (#68) without them.
   - **Recommendation:** a founder-merged schema change adds `position {lon, lat, method: "synthetic"}` to homes and place items (stops, schools, amenities, childcare, police).
   - Area-wide topics (flood area, crime counts, broadband, energy) get no point.
   - Add a test that positions agree with `distanceMetres`.
3. **Q3. Where stage 6 tiles live (IN-02).**
   - **Recommendation:** Cloudflare R2 (free tier covers 10k users per the working above), with the founder's server running `pmtiles serve` behind a CDN as the fallback. This needs founder sign-off as a running-cost item, even at $0.
4. **Q4. Visual regression tooling.**
   - **Recommendation:** start with the in-browser pixel diff (no package) and a handful of baselines.
   - Approve `Verify.ImageMagick` only if it flakes or needs better diff output.
5. **Q5. 0029 labels with no retrieval data.**
   - **Recommendation:**
     - The prototype shows "Sample data · {date}" plus the five fixture statuses mapped to 0029's dimensions.
     - Stage 6 adapters add a `retrieval` field that passes through unchanged.
     - The UI never invents "Live".
6. **Q6. Is unit conversion a calculation?** Converting 1,200 m to "1.2 km" in the UI is small, but it is still a derived figure.
   - **Recommendation:** treat it as a calculation under rule 2. Display metres exactly as recorded in the prototype. If kilometres or walking minutes are wanted, add them as labelled inputs or engine outputs, with a line in the decision register.

---

## 12. Sources (all checked 11 Nov 2026 unless noted)

- MapLibre GL JS:
  - npm `maplibre-gl` 6.17.0;
  - [KeyboardHandler](https://maplibre.org/maplibre-gl-js/docs/API/classes/KeyboardHandler/);
  - [create and style clusters](https://maplibre.org/maplibre-gl-js/docs/examples/create-and-style-clusters/);
  - [v5→v6 migration guide](https://github.com/maplibre/maplibre-gl-js/blob/main/docs/guides/v5-to-v6-migration-guide.md);
  - [CHANGELOG](https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md).
- react-map-gl: [get started](https://visgl.github.io/react-map-gl/docs/get-started) (MapLibre v6 needs worker configuration).
- Leaflet: [install](https://leafletjs.com/install.html), [accessibility](https://leafletjs.com/examples/accessibility/).
- OpenLayers: npm `ol` 10.11.0 (licence from the registry).
- Mapbox: [LICENSE.txt](https://github.com/mapbox/mapbox-gl-js/blob/main/LICENSE.txt), [pricing](https://www.mapbox.com/pricing).
- Google Maps Platform: [pricing overview](https://mapsplatform.google.com/pricing/), [pricing list](https://developers.google.com/maps/billing-and-pricing/pricing).
- Protomaps:
  - [PMTiles](https://docs.protomaps.com/pmtiles/);
  - [PMTiles with MapLibre](https://docs.protomaps.com/pmtiles/maplibre);
  - [basemap downloads](https://docs.protomaps.com/basemaps/downloads);
  - [basemap styles for MapLibre](https://docs.protomaps.com/basemaps/maplibre);
  - [deploy](https://docs.protomaps.com/deploy/).
- MapTiler: [pricing](https://www.maptiler.com/cloud/pricing/).
- Stadia Maps: [pricing](https://stadiamaps.com/pricing/), [terms of service](https://stadiamaps.com/terms-of-service/).
- Cloudflare: [R2 pricing](https://developers.cloudflare.com/r2/pricing/), [Pages limits](https://developers.cloudflare.com/pages/platform/limits/).
- GitHub Pages: [limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).
- OpenStreetMap: [copyright](https://www.openstreetmap.org/copyright), [OSMF attribution guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines), [tile policy](https://operations.osmfoundation.org/policies/tiles/) (via `docs/references/data-sources.md`).
- supercluster: [README](https://github.com/mapbox/supercluster).
- Next.js: [lazy loading](https://nextjs.org/docs/app/guides/lazy-loading) (docs last updated 10 Mar 2026; npm `next` 16.4.6).
- web.dev: [Web Vitals](https://web.dev/articles/vitals).
- Lighthouse: [throttling](https://github.com/GoogleChrome/lighthouse/blob/main/docs/throttling.md).
- MDN: [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).
- WCAG 2.2: [2.5.7 Dragging Movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html), [2.4.11 Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).
- Playwright for .NET: [screenshots](https://playwright.dev/dotnet/docs/screenshots), [emulation](https://playwright.dev/dotnet/docs/emulation), [ARIA snapshots](https://playwright.dev/dotnet/docs/aria-snapshots).
- NuGet: [Deque.AxeCore.Playwright](https://www.nuget.org/packages/Deque.AxeCore.Playwright) (4.14.0, MIT); `Verify.Playwright` 3.2.0, `Verify.ImageMagick` 4.1.0 (MIT) and `Magick.NET-Q8-AnyCPU` 15.1.0 (Apache-2.0) from the NuGet registration API.
- npm registry (licence and version):
  - `pmtiles` 4.5.0;
  - `@protomaps/basemaps` 5.7.2;
  - `protomaps-leaflet` 5.1.0;
  - `supercluster` 9.1.0;
  - `react-map-gl` 8.1.3;
  - `json-schema-to-typescript` 16.0.0;
  - `@lhci/cli` 0.16.0;
  - `size-limit` 14.3.0;
  - `web-vitals` 6.2.3.
- Repository: decisions 0005, 0019, 0020, 0022, 0027, 0029, 0035, 0043; doc 03 §5–6; issues #75, #120, #143; `docs/references/data-sources.md` (PR #125); the `packages/fixtures/data/area.json` count on the area-fixtures branch (#120).
