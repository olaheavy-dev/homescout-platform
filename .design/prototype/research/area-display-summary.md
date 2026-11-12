# Displaying area information: summary and founder decisions (#143)

> **Note (12 Nov 2026):** the test tools named here for stage 5 (Reqnroll, Playwright for .NET, `Deque.AxeCore.Playwright`) were replaced by [decision 0049](../../../docs/decisions/0049-back-to-python-final.md): browser scenarios run with playwright-bdd and `@axe-core/playwright`, and the backend is Python.

There are two detailed notes:
- [`area-display-ux.md`](area-display-ux.md): experience and visual design (track A);
- [`area-display-engineering.md`](area-display-engineering.md): engineering (track B).

Both were researched on 11 Nov 2026 from official and public pages, and anything not confirmed is marked unverified.

## Decisions (founder, 11 Nov 2026: "Accept all nine")
1. **Sample map:** a drawn, fictional "Northbridge" base map for the prototype, labelled "Sample map, fictional area". Real tiles come only with real data (stage 6, #98). Reason: synthetic homes on real streets would place invented facts on real places (rule 1).
2. **Map positions** are added to the area data as synthetic inputs, with a test that they agree with the recorded distances (#146).
3. **Crime is never on the map.** It's a table of counts by month and category, plus the neighbourhood team. Police data moves each crime to an anonymous nearby point, and dots read as "unsafe zones".
4. **Sold prices on the map have no price labels.** The price and date are in the list and the selected row.
5. **Phones are list-first,** with a static map preview and one tap to a full-screen map with a bottom sheet. Desktop has the list and map side by side, kept in sync. The list is a complete alternative to the map, because gaps ("no record in this source") only exist in the list.
6. **Criteria results come from the engine:** "within your commute limit" and similar are generated figures (#147). Until then the screen shows the two numbers side by side with no verdict (rule 2).
7. **Distances are shown exactly as recorded** (for example "1,200 m, straight line"). Converting units or estimating walking time counts as a calculation.
8. **MapLibre GL JS** is the map engine: BSD-3, no account or key, no tracking, and lazy-loaded so it's never on the critical path. For stage 6, self-hosted Protomaps tiles are recommended; that is a running-cost decision for IN-02.
9. **Performance budgets** on a mid-range phone, checked in CI: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less; Nearby route JavaScript 170 KB gzip or less without the map; the map chunk is lazy-loaded.

## Packages approved by the founder (11 Nov 2026)
For the stage 5 prototype:
- `maplibre-gl` (BSD-3-Clause)
- `json-schema-to-typescript` (MIT, build-time only)
- `Deque.AxeCore.Playwright` (MIT, with `Deque.AxeCore.Commons`, MPL-2.0)
- `@lhci/cli` (Apache-2.0; 0.x, so a minor update counts as major)
- `size-limit` with `@size-limit/preset-app` (MIT)

Each still passes the licence check and gets a `third-party.md` entry when it's added.

**Not yet approved (stage 6, decided with IN-02):** `pmtiles`, `@protomaps/basemaps`, the `pmtiles` CLI, Protomaps basemap data (ODbL) and its hosting.

## Other points from the notes
- **Motion:** five purposeful transitions only (150 to 400 ms), each reduced to a cut or short fade under reduced motion. Figures, risk colours and alerts never animate.
- **Accessibility:** map markers aren't tab stops, and the list rows are the keyboard path. Focus moves into and back out of each sheet in a set order, targets are at least 44 px, and every map fact is also in the list.
- **One gap pattern everywhere:** "No record in this source" has a dashed outline and the line "this doesn't mean there are none", so it never looks like a clean result.
- **Privacy:** no third-party trackers; geolocation only when the user taps for it; the dropped pin stays on the device; a strict CSP.
