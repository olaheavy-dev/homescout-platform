# Pilot area tools and area card specifications — Implementation Plan

> **Dated plan (13 Nov 2026).** Some rules it describes changed on 14 Nov 2026 (FE-33 stamps, FE-34 limits, DA-12 flood time, FE-27 units). The current rules are in the specifications under `docs/specs/` and the register in `docs/decisions/README.md`.


> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Specify the pilot's public read-only area tools for ChatGPT and Claude (`TOOLS-`) and the isometric area card in both its versions (`CARD-`) (#225), with register lines FE-14 and FE-15, setup notes and a canvas row.

**Architecture:** Two Gherkin features in `docs/specs/pilot/`, run by the existing pytest-bdd runner (data scenarios) and later by the MCP suite (`@mcp`, #97) and playwright-bdd (`@ui`). No new step wording and no new tag, so no Python or `pyproject.toml` change.

**Tech Stack:** Gherkin, pytest-bdd 9; the design canvas artifact.

**Spec:** issue #225 (short design, founder "Approve (Recommended)", 13 Nov 2026), on top of `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`, decisions 0051, 0037, 0029, 0014, 0004, and `docs/specs/pilot/area-chat.feature` (CHAT-31 to CHAT-33).

## Global Constraints
- Branch `docs/pilot-area-tools-spec`; `docs:` commits; no agent attribution; `make check` green before the push.
- SP-01 rules (`docs/specs/README.md`); permanent IDs `TOOLS-NN`, `CARD-NN`; records cited by ID; missing never zero (rule 7); no scenario expects "safe", "verified", "approved", a score or an AI-calculated figure.
- A Gherkin description line must not start with `@` (the parser reads it as a tag).
- Tags: feature `@screen @buying @renting` as the other pilot specs; tools `@mcp`; card scenarios carry **both** `@ui` and `@mcp`, and the header says each runs once per version (our chat component in playwright-bdd, the widget in the MCP suite) (founder: "Two versions"; FE-15).
- `# fixture needed: #216` above scenarios needing postcode-level data. Proposed copy is labelled as proposed in the header.
- Tool names and signatures are left to the build (design); scenarios name tools by job ("the nearby places tool").
- Lessons from #224's review, applied from the start: server-side checks (refusals with no work done, logs, nothing stored) are scenarios, not only page states; each rule that a fixed stand-in cannot falsify is phrased as what the server returns or sends.

## Review Focus
1. A failed or unlicensed source returned as an empty list or "none" through MCP — TOOLS scenarios expect "Unavailable" and "No <place> found within N km".
2. A radius above 5 km requested by the host model — a TOOLS scenario expects it capped at 5 km and the cap stated.
3. The two card versions drifting (a place drawn at different spots) — every CARD scenario runs for both versions; positions come from the tool result, never computed in a card.
4. The widget fetching from the network (leaking the postcode) — a CARD scenario on no network requests.
5. A host without widgets getting nothing useful — a CARD scenario expects the text answer with the same places.

---

### Task 1: `docs/specs/pilot/area-tools.feature`

**Files:** Create `docs/specs/pilot/area-tools.feature`.

- [ ] **Step 1:** Header in the screen-template shape: question "What do the official sources say about this postcode, from inside my own assistant?"; public, read-only, no key (0051 point 1); clients and setup, dated 13 Nov 2026 with links (Claude custom connector "No sign-in", free plan one custom connector, support.claude.com article 11175166; ChatGPT developer mode, "No Authentication", admin on work plans, developers.openai.com developer-mode guide and help.openai.com article 12584461; ChatGPT widgets "to confirm when tested", MCP Apps client list at modelcontextprotocol.io/extensions/apps/overview); host support recorded per 0037 in `docs/planning/mcp-host-support.md` when #97 builds; tools named by job; Required states list.
- [ ] **Step 2:** Scenarios, in order:
  - TOOLS-01 (data) `Then home "WALES-1" has coverage "not-yet-covered"`; TOOLS-02 the find-area tool returns "not yet covered" for a postcode outside England and no topics.
  - TOOLS-03 unknown postcode → "postcode not found", no topics; TOOLS-04 malformed postcode → refused with the format, no lookup.
  - Nearby (#216): TOOLS-05 places carry straight-line distance from the postcode centre, source, data date, label; TOOLS-06 no place within the radius → "No <place> found within <radius>", never "none" or empty; TOOLS-07 a radius over 5 km is capped at 5 km and the result states the radius used.
  - Topics (#216): TOOLS-08 each value carries source, date, label and geographic level; TOOLS-09 a failed source → "Unavailable", never empty or zero; TOOLS-10 a stale source → "Old" with its date; TOOLS-11 crime counts for the fixed 1 mile radius with "not a safety rating"; TOOLS-12 sold prices as individual sales with date, the address only beside its price, no average or median.
  - TOOLS-13 explain-source returns stored text and makes no AI call; TOOLS-14 missing text → "Explanation not yet available" with no text; TOOLS-15 questions-for-gaps returns rule-built questions and makes no AI call.
  - Server: TOOLS-16 the tool list holds only read tools, no write tool; TOOLS-17 no key or sign-in is needed; TOOLS-18 every tool description says "quote the sourced facts; do not calculate, score or call an area safe or good"; TOOLS-19 the server description carries the disclaimer and says the host's wording is not Vestagraph's; TOOLS-20 every result names its sources (attribution); TOOLS-21 text inside a result is marked as data from the source; TOOLS-22 tools read only stored copies — with every live source unreachable, results still come from the cache with their labels; TOOLS-23 global rate limit reached → refused, no lookup; TOOLS-24 per-host limit reached → that host refused, another host still served; TOOLS-25 no log holds a postcode, tool argument or raw IP address; TOOLS-26 the server keeps no copy of calls beyond the rate-limit store's anonymised keys that expire; TOOLS-27 an error result never repeats the postcode or argument text; TOOLS-28 a postcode is never echoed into a URL the server builds, except an outbound link labelled as carrying it (FE-11).
- [ ] **Step 3:** `uv run --locked pytest packages/specs/tests -q --collect-only -k TOOLS | tail -1` → 28 collected; `-m "not ui and not mcp and not withdrawn" -k TOOLS` → 1 passed.
- [ ] **Step 4:** Forbidden-word scan: `grep -n -i -E "\b(safe|verified|approved|good)\b" docs/specs/pilot/area-tools.feature` → only quoted rule text. Commit `docs: pilot area tools specification for ChatGPT and Claude (#225)`.

### Task 2: `docs/specs/pilot/area-card.feature`

**Files:** Create `docs/specs/pilot/area-card.feature`; modify `docs/specs/pilot/area-chat.feature` header (one line: CHAT-31 to CHAT-33 are detailed in `area-card.feature`).

- [ ] **Step 1:** Header: what the card is (nearest places as a small isometric scene, FE-10, from the nearby tool's result); two versions (our chat component, the ChatGPT and Claude widget, `ui://`, 0037) per FE-15, each scenario run once per version; positions and distances come in the tool result from the area tools' geometry module, never computed by a card (design, Accuracy 2); tap per FE-14; after the plain tools work (0037).
- [ ] **Step 2:** Scenarios (all `@ui @mcp`, #216 where data needed):
  - CARD-01 places drawn from the result's positions, every place within 2% of its listed distance, in list order, or named "off the map"; CARD-02 both versions draw the same places at the same positions for the same result.
  - CARD-03 tapping a pin shows its name, distance and source; CARD-04 keyboard: Tab reaches each pin, Enter or Space shows the same details, Escape closes them; CARD-05 a screen reader hears each pin as a button named with its place and distance; CARD-06 the text answer lists the same places in the same order (the accessible version).
  - CARD-07 the card shows sources and data dates; CARD-08 no flood or crime shading or colour; CARD-09 building heights labelled "approximate"; CARD-10 the postcode-centre pin is labelled "Postcode centre", no address pin.
  - CARD-11 the card makes no network request; CARD-12 nothing stored by the card (no storage or cookies); CARD-13 in a host without widgets the text answer still lists every place with its distance and source; CARD-14 a result with no places shows no card and the text says "No places found within <radius>", never an empty card; CARD-15 reduced motion: no animation.
- [ ] **Step 3:** `--collect-only -k CARD` → 15 collected; `make check` green.
- [ ] **Step 4:** Commit `docs: area card specification for both versions (#225)`.

### Task 3: Register, canvas, status, #117

**Files:** `docs/decisions/README.md`, `docs/specs/README.md` (Layout row example list), canvas, `docs/planning/status.md`.

- [ ] **Step 1:** FE-14 "Area card: tap a pin" (Default; founder, 13 Nov 2026, prompt window: "Tap a pin for its name", over the agent's still picture with a numbered list); FE-15 "Area card: two versions" (Default; founder: "Two versions", over the agent's one shared card page; safeguards: positions from the area tools only, every CARD scenario per version). Source `docs/specs/pilot/area-card.feature`.
- [ ] **Step 2:** Canvas row "Pilot 6 · Area card" after Pilot 5: our chat answer with the card and one tapped pin (desktop panel width), and the widget in a neutral "Your assistant" frame, light then dark (4 boards); sticky note; take "the isometric area card for answers" off the Pilot page's still-to-design list.
- [ ] **Step 3:** `status.md`: #224 merged in "Done on 13 Nov 2026"; open PR line replaced; canvas version; FE-14 and FE-15 in the founder decisions; Next item 1 (chat and tools specs done or in review; next Explain this).
- [ ] **Step 4:** Pre-flight: `grep -rn -i "area card\|FE-14\|FE-15\|mcp-host-support\|still to design" docs .design` → nothing stale. Comment on #117: the pilot's area tools are specified in `docs/specs/pilot/area-tools.feature` (#225); #117 keeps the home-level tools. `make check`; commit `docs: FE-14, FE-15, canvas row and status for the area tools and card (#225)`.
