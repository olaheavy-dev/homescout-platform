# Pilot area chat panel specification — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Specify the pilot's "Ask about this area" chat panel (#223) as an executable Gherkin feature, with its canvas board, register line and site-plan entry.

**Architecture:** A new folder `docs/specs/pilot/` for the pilot's specifications; `area-chat.feature` is run by the existing pytest-bdd runner (`scenarios(_SPECS)` over `docs/specs/`, SP-03). Panel behaviour is `@ui` (stage 5b, with a fixed stand-in AI reply); one data scenario reuses existing steps so the file is exercised by `make check`. No new step wording and no new tag, so no Python or `pyproject.toml` change.

**Tech Stack:** Gherkin, pytest-bdd 9; the design canvas artifact (HTML).

**Spec:** the short design in issue #223 (founder: "Approve (Recommended)", 13 Nov 2026), on top of `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md` and decision 0051.

## Global Constraints
- Branch `docs/pilot-area-chat-spec`; `docs:` commits; no agent attribution; `make check` green before the push.
- SP-01 rules (`docs/specs/README.md`): one observable outcome per scenario; permanent IDs `CHAT-NN`, never reused; records cited by ID in quotes; missing never zero (rule 7); no scenario expects "safe", "verified", "approved", a score or a figure the AI calculated (rules 1, 4; 0004; PD-13).
- Tags: `@screen @buying @renting` on the feature (as `14-check-an-area.feature`); behaviour `@ui`; untagged = data. No new tag.
- A state needing postcode-level data: `# fixture needed: #216` directly above the scenario.
- Fixed copy (design and 0051): disclaimer "Answers come only from the sources shown, and can still be wrong. Check the source before relying on it." and "Don't type personal details. Chats aren't saved."; "Chat is paused for today, the area check still works"; "Chat unavailable right now". Entry "Ask about this area" with an "AI" badge; header line "Answers are written by AI from the sources below" (founder, 13 Nov 2026: "AI badge on the entry").
- No limit numbers (left to the build); scenarios say "the message limit" and "the turn limit".

## Review Focus
1. A failed AI provider or the paused state hiding or blocking the area result — CHAT scenarios expect the area check to keep showing.
2. A model reply containing "safe" or a score reaching the screen — an output-guard scenario with a stand-in reply that contains "safe".
3. A figure in an answer that is not in the tool results — a scenario where the stand-in reply invents a number and the answer is rejected (design, Accuracy 5).
4. Chat text from postcode A carried over after the visitor checks postcode B — a reset scenario.
5. The postcode or message text leaving in a URL, a stored item or a log — scenarios on requests and browser storage.

---

### Task 1: `docs/specs/pilot/area-chat.feature`

**Files:** Create `docs/specs/pilot/area-chat.feature`; modify `docs/specs/README.md` (Layout table row for `pilot/<feature>.feature`, issue column "#223 and later pilot specs").

- [ ] **Step 1:** Write the feature header in the README's screen-template shape: question it answers "What do the sources say about this area, in plain words?"; modes both, anyone, no account (0046, 0051); fixtures `WALES-1`, postcode-level data #216; where it appears (Check an area and the landing result, an optional closable panel, 0004); a "Required states" list mapping each state below to its IDs.
- [ ] **Step 2:** Write the scenarios, one outcome each, IDs in this order:
  - CHAT-01 (data) outside England: `Then home "WALES-1" has coverage "not-yet-covered"`; CHAT-02 `@ui` outside England shows no "Ask about this area" entry, only "Not yet covered".
  - Entry and panel: CHAT-03 entry labelled "Ask about this area" with an "AI" badge, closed by default; CHAT-04 the header shows "Answers are written by AI from the sources below", both disclaimer lines and a privacy notice link; CHAT-05 closing the panel leaves the area result unchanged; CHAT-06 desktop side panel, phone bottom sheet (390 px), area result still reachable.
  - Answers (#216): CHAT-07 each claim shows its source, data date and label (Live, Cached, Fallback, Unavailable, or Old); CHAT-08 a topic with no record answers "Not known from our sources" plus a suggested question; CHAT-09 a source-failed topic answers "Unavailable", never "none" or zero; CHAT-10 suggested questions come from the gaps list, offered before the first message.
  - Refusals and guards: CHAT-11 "is it safe" is declined with the sourced facts offered instead; CHAT-12 a request for a score or rating is declined; CHAT-13 a request to work out a sum is declined, quoting only figures from the area result; CHAT-14 personal advice ("should I buy") is declined; CHAT-15 a stand-in reply containing "safe" is blocked by the output guard and never shown; CHAT-16 a stand-in reply with a number not in the tool results is rejected; CHAT-17 a question about another postcode or a home is declined, the chat answers only about the area on screen; CHAT-18 page or tool text that looks like an instruction is treated as data (stand-in tool result with "ignore your rules").
  - Limits and failures (each also expects the area result still shown): CHAT-19 daily cap reached → "Chat is paused for today, the area check still works"; CHAT-20 provider fails → "Chat unavailable right now"; CHAT-21 message over the limit is not sent, with an inline message; CHAT-22 turn limit reached → no further messages, with a message saying so; CHAT-23 bot check fails → no message sent, honest message; CHAT-24 rate limit reached → honest "try again later" message.
  - Privacy: CHAT-25 checking a new postcode clears the chat; CHAT-26 reloading the page starts an empty chat, nothing in browser storage; CHAT-27 no request carries the postcode or message text in its URL path or query string.
  - Access: CHAT-28 the panel opens, sends and closes by keyboard, focus returns to the entry; CHAT-29 a new answer is announced to screen readers; CHAT-30 loading shows a "Writing an answer" state, never an empty reply.
  - Area card (after the plain tools, 0037): CHAT-31 an answer about nearby places may show the isometric area card, with the text answer always present; CHAT-32 every place on the card sits at its listed distance (within 2%, design Accuracy) or is named "off the map"; CHAT-33 the card carries its sources and dates and has no flood or crime shading.
- [ ] **Step 3:** Check: `uv run --locked pytest packages/specs/tests -m "not ui and not mcp and not withdrawn" -k "CHAT" -q` → 1 passed (CHAT-01); `uv run --locked pytest packages/specs/tests -q --collect-only -k CHAT | tail -1` lists 33. If the runner does not see `pilot/`, stop and report (it should: `scenarios()` takes the folder).
- [ ] **Step 4:** `grep -n -i -E "\b(safe|verified|approved)\b" docs/specs/pilot/area-chat.feature` → only lines where the word is quoted as what is blocked or declined. Commit `docs: area chat panel specification for the pilot (#223)`.

### Task 2: Register line, site plan, canvas, status

**Files:** `docs/decisions/README.md` (FE-13 after FE-12), `.design/prototype/INFORMATION_ARCHITECTURE.md`, the design canvas artifact, `docs/planning/status.md`.

- [ ] **Step 1:** FE-13 "AI label on the area chat", stage 5b, Default (founder, 13 Nov 2026, prompt window: "AI badge on the entry", over the agent's recommendation of a header line only): entry "Ask about this area" with an "AI" badge and the header line; the site plan's "no AI badge" stays for the home chat; source `docs/specs/pilot/area-chat.feature`.
- [ ] **Step 2:** Site plan: add "Ask about this area" (pilot, Check an area and the landing result; panel, bottom sheet on a phone; AI badge per FE-13) next to "Ask about this home", and note the badge exception in the assistant-entry row.
- [ ] **Step 3:** Canvas: read the artifact, add an "Ask about this area" board to the "Pilot · public area check" page (desktop side panel and phone sheet, light then dark, showing a sourced answer, "Not known from our sources", and the paused state), remove the chat from the page's "still to design" note, publish to the same URL. Record the new version.
- [ ] **Step 4:** `status.md`: Next item 1 marks the area chat spec done in this pull request; canvas version updated; FE-13 in the founder decisions; open PR listed.
- [ ] **Step 5:** Pre-flight: `grep -rn -i "ask about this area\|no \"AI\" badge\|FE-13" docs .design` → no stale or contradicting line. `make check` green. Commit `docs: FE-13 AI label, site plan entry and canvas board for the area chat (#223)`.
