# Screen specifications, part 1: the area screens — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write the screen specifications for Landing, Nearby and Check an area (#68, pull request 1 of 3), with three new data steps so their data scenarios run in `make check`.

**Architecture:** Gherkin features in `docs/specs/screens/` (SP-01), run by the existing pytest-bdd runner (SP-03). Data scenarios check `packages/fixtures/data/area.json` and `homes.json` through new `DataSteps` methods; screen behaviour is tagged `@ui` and waits for stage 5.

**Tech Stack:** Gherkin, pytest-bdd 9, Python 3.14, mypy strict, ruff.

**Spec:** `docs/superpowers/specs/2026-11-13-screen-specs-design.md`

## Global Constraints
- Branch `docs/screen-specs-area`; commits `test:`/`docs:`; no agent attribution; `make check` green before every push.
- SP-01 rules in `docs/specs/README.md`: one observable outcome per scenario; permanent IDs `<CODE>-NN`; figures and records cited by ID in quotes, never typed (rule 2); missing never zero (rule 7); no "verified", "safe" or "approved" (rule 4).
- Codes: `LAND` (01-landing), `NEAR` (04-nearby), `AREA` (14-check-an-area). Never reuse an ID.
- Tags: `@screen` plus `@buying`/`@renting` as applies (both tags when both modes); screen behaviour `@ui`; untagged = data scenario.
- A state with no fixture record: an `@ui` scenario with a comment line `# fixture needed: #<issue>` directly above it.
- Public pages never show an account feature as an active control (0046); the map pin is "Postcode centre"; the postcode lives in the URL fragment, never the query string (0014).

## Review Focus
1. A not-covered (Wales) or source-failed topic presented like an empty, clean result — pinned by NEAR and AREA data scenarios using `shows no value`.
2. "No record in source" for flood read as "no flood risk" — a NEAR `@ui` scenario expects the topic's "doesn't tell you" wording and no reassuring label.
3. A data step that passes on a typo (a record ID that doesn't exist) — Task 1's tests assert the failure message names the ID.
4. A stale record shown without its date — a NEAR scenario on `B1-AREA-SCHOOL-INSPECTION-1`.
5. A postcode reaching a query string — an AREA `@ui` scenario on the URL.

---

### Task 1: Area and coverage data steps

**Files:**
- Modify: `packages/specs/tests/specs_support.py` (add `_AREA`, area loading, three `DataSteps` methods)
- Modify: `packages/specs/tests/specs_steps.py` (three bindings)
- Modify: `packages/specs/tests/test_specs_data_steps.py` (tests)
- Modify: `docs/specs/README.md` (Data steps list)

**Interfaces — Produces (step wording, the contract):**
- `Then area record "<record ID>" has status "<recorded | no-record-in-source | stale | source-failed | not-covered>"` → `DataSteps.then_area_record_has_status(record_id: str, status: str) -> None`
- `Then area record "<record ID>" shows no value` → `DataSteps.then_area_record_shows_no_value(record_id: str) -> None` (passes only when the record has no `value` key)
- `Then home "<home ID>" has coverage "<covered | not-yet-covered>"` → `DataSteps.then_home_has_coverage(home_id: str, coverage: str) -> None`

- [ ] **Step 1: Write the failing tests** (names follow `test_<method>_<condition>_<result>`):
  - `test_then_area_record_has_status_unknown_record_fails_naming_the_id` — `"B1-AREA-NOPE"` raises `AssertionError` whose message contains `B1-AREA-NOPE` and `area.json`.
  - `test_then_area_record_has_status_wrong_status_fails` — `("R1-AREA-CRIME-2", "recorded")` raises; message contains `source-failed`.
  - `test_then_area_record_has_status_correct_status_passes` — `("R1-AREA-CRIME-2", "source-failed")`.
  - `test_then_area_record_shows_no_value_record_with_value_fails` — `"B1-AREA-SCHOOL-INSPECTION-1"` (stale, has a value) raises.
  - `test_then_area_record_shows_no_value_record_without_value_passes` — `"WALES-1-AREA-FLOOD-1"`.
  - `test_then_home_has_coverage_wrong_coverage_fails` — `("WALES-1", "covered")` raises; message contains `not-yet-covered`.
  - `test_then_home_has_coverage_correct_coverage_passes` — `("WALES-1", "not-yet-covered")`.
  - `test_then_home_has_coverage_unknown_home_fails_naming_the_id` — `"ZZ-9"` raises with `ZZ-9` in the message.
- [ ] **Step 2:** `uv run --locked pytest packages/specs/tests/test_specs_data_steps.py -q` → the new tests fail (`AttributeError`).
- [ ] **Step 3:** Implement the three methods in `specs_support.py`; load `area.json` once into the existing cached `_Loaded` (a `dict[str, Json]` by `id`) and keep home records (not only IDs) for coverage. Add the three bindings in `specs_steps.py` with `parsers.parse`, in the existing style.
- [ ] **Step 4:** Same command → all pass; `make check` green (mypy strict covers the tests).
- [ ] **Step 5:** Add the three wordings to the README's "Data steps" list. Commit: `test: area record and home coverage data steps for the screen specs (#68)`.

### Task 2: The fixture-needed issue

- [ ] **Step 1:** Open one issue, labels `noticed`, `stage-5`: "fixture: postcode-level sample area data for Check an area and the landing (B6a)". Body: distances measured from a postcode centre (not from one home), the hero's four nearest places and "+N more" count, and one well-formed postcode that is unknown (for "postcode not found"); cite TASKS B6a and P1, decision 0046, and the founder's 13 Nov 2026 choice "Specs now, data later". Record its number for Tasks 4 and 5.

### Task 3: `docs/specs/screens/04-nearby.feature` (code NEAR)

**Files:** Create `docs/specs/screens/04-nearby.feature`.

Header per the README screen template: question "Would daily life work?"; Modes: both; Fixtures: B1, R1, R2, WALES-1; inputs: the area record IDs cited below. Topic order as `.design/prototype/INFORMATION_ARCHITECTURE.md` "Nearby".

Scenarios (one outcome each):
- [ ] **Data** (`Given home "<id>" is at story step 1` is not needed; data scenarios may go straight to `Then`):
  - NEAR-01 the failed crime lookup is not shown as no crime: `R1-AREA-CRIME-2` has status `source-failed` and shows no value.
  - NEAR-02 no flood record in the source is a gap, not a clean result: `B1-AREA-FLOOD-1` has status `no-record-in-source` and shows no value.
  - NEAR-03 a stale school inspection keeps its record: `B1-AREA-SCHOOL-INSPECTION-1` has status `stale`.
  - NEAR-04 a home in Wales is not yet covered: home `WALES-1` has coverage `not-yet-covered`, and `WALES-1-AREA-FLOOD-1` has status `not-covered`.
  - NEAR-05 a missing childcare place is a gap: `B1-AREA-AMENITY-6` has status `no-record-in-source`.
- [ ] **`@ui`**:
  - NEAR-06 the page opens as one summary row per topic in the IA order.
  - NEAR-07 the failed crime topic shows "Unavailable" with "Try again" and "This doesn't mean there's nothing to report".
  - NEAR-08 the flood gap shows "This is not the same as no warning", never a reassuring label.
  - NEAR-09 the stale inspection shows its date and a stale label.
  - NEAR-10 Wales shows one "Not yet covered" card, not empty topics.
  - NEAR-11 on a phone every topic has a list, and the map is an optional view (list alternative to the map).
  - NEAR-12 crime appears in the list as counts, never on the map.
  - NEAR-13 each topic's "What this doesn't tell you" is visible on a phone, never collapsed. (Superseded 14 Nov 2026 by FE-34: limits sit inside "How we got this".)
  - NEAR-14 the commute row shows the estimate next to the household's limit, with no verdict.
- [ ] Required-states block maps: source failed → NEAR-01, 07; not covered location → NEAR-04, 10; Wales → NEAR-04, 10; stale → NEAR-03, 09; missing never zero → NEAR-02, 05, 08; mobile list alternative → NEAR-11.
- [ ] `make check` green; commit `docs: Nearby screen specification (#68)`.

### Task 4: `docs/specs/screens/14-check-an-area.feature` (code AREA)

Header: question "What is around this postcode?" (the doc 03 §5 row added in Task 6); Modes: both; Fixtures: WALES-1 (outside England); postcode-level fixture: `# fixture needed: #<Task 2>`.

- [ ] **Data:** AREA-01 a postcode outside England is not yet covered: home `WALES-1` has coverage `not-yet-covered`; AREA-02 a not-covered topic has no value: `WALES-1-AREA-SCHOOL-1` has status `not-covered` and shows no value.
- [ ] **`@ui`:** AREA-03 the postcode goes in the URL fragment, never the query string; AREA-04 an incomplete postcode shows an inline message and nothing is searched; AREA-05 (fixture needed) a well-formed unknown postcode shows "We couldn't find that postcode" and no topics; AREA-06 each topic shows a skeleton while loading, never empty rows; AREA-07 a topic whose source is unavailable shows "Unavailable" and the other topics still show; AREA-08 outside England shows a "Not yet covered" card; AREA-09 the map's centre pin is labelled "Postcode centre"; AREA-10 there is no commute row; AREA-11 saving a home appears only in a "Coming next · not available yet" panel, with no active button; AREA-12 "Print or save as PDF" prints every topic, including Unavailable and Not yet covered ones, with sources and the "Sample data" header; AREA-13 (fixture needed) distances are measured from the postcode centre, not from a home.
- [ ] Required-states block; `make check` green; commit `docs: Check an area screen specification (#68)`.

### Task 5: `docs/specs/screens/01-landing.feature` (code LAND)

Header: question "What can this help me do?"; Modes: both; Fixtures: postcode-level fixture `# fixture needed: #<Task 2>`. Section order from the IA "Landing".

- [ ] **`@ui`** only (no data the landing owns yet): LAND-01 the postcode box with a persistent "Postcode" label, hint text and "Check postcode" is the main action; LAND-02 "England only for now" sits under it; LAND-03 submitting a postcode opens Check an area with the postcode in the fragment; LAND-04 "Try an example" opens the sample area; LAND-05 cost estimate, compare and questions appear only as "Coming next … not available yet", never as active controls; LAND-06 (fixture needed) the hero's places, distances and "+N more" count come from the postcode-level fixture; LAND-07 the hero map is a static image, not the live map; LAND-08 the source wall shows names only, each linking About the data; LAND-09 the sample Schools card is labelled "Sample"; LAND-10 no copy calls an area or home "safe" (rule 4).
- [ ] Required-states block (none of doc 03 §5's states belongs to the landing; it says so); `make check` green; commit `docs: Landing screen specification (#68)`.

### Task 6: Pre-flight and doc 03

- [ ] doc 03 §5: change the "Search-led landing" row to the postcode area check (decision 0046) and add a "Check an area" row ("What is around this postcode?").
- [ ] `docs/specs/README.md` layout row: "one feature per screen in doc 03 §5 (14 screens, Check an area is `14`)".
- [ ] `git grep -n "13 prototype screens\|13 screens\|Search-led landing"` and fix current-state statements (not history).
- [ ] `make check` green; commit `docs: doc 03 screen list follows decision 0046 (#68)`.
- [ ] Pull request body: `Part of #68` (not Closes), `Closes #67`, link the Task 2 issue.
