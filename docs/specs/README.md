# Specifications

The prototype specification lives here (decision [0043](../decisions/0043-specification-format.md), SP-01). It describes what each screen, story step and MCP tool must do, precisely enough to build and test it from this folder and the fixtures alone (doc 04 §9 stage 3). The specifications are **executable**: a Python project (`packages/specs/tests`) runs these Gherkin files with pytest-bdd (decision 0049; the Reqnroll runner was removed in port step P8).

## Layout
| Path | Holds | Issue |
|---|---|---|
| `screens/NN-<screen>.feature` | One feature per screen in doc 03 §5, numbered in that order (for example `05-real-costs.feature`); 14 screens, with Check an area (decision 0046) appended as `14-check-an-area.feature` so earlier numbers and IDs never move | #68 |
| `stories/buyer.feature`, `stories/renter.feature` | The step-by-step story scripts | #69, #70 |
| `mcp-tools.feature` | The MCP tool surface for AI assistants | #117 |

The design skills' working notes in `.design/<feature>/` (decision 0031) feed these files. If they disagree, this folder wins.

## Rules
1. **Every acceptance criterion is a Gherkin `Scenario:`** whose name starts with a permanent ID, for example `Scenario: COSTS-02 missing insurance is not zero`. Keep each scenario to one observable outcome.
2. **IDs:** a code for the screen or area plus a number, for example `COSTS-02`, `BUY-3.2` (buyer story, step 3, scenario 2) or `MCP-01`.
   - An ID is never reused or renumbered.
   - A scenario that is no longer needed stays in the file, tagged `@withdrawn`.
3. **Figures are cited by ID, in quotes, never typed** (AGENTS.md rule 2):
   - inputs by evidence ID from `packages/fixtures/data/`;
   - calculated values by figure ID from `packages/fixtures/generated/costs.json`.

   A value the engine does not produce is written "not calculated". Missing and partial states are named explicitly, and missing is never shown as £0 (rule 7).
4. **Required states:** each feature's description maps every required state from doc 03 §5 that applies to it to at least one scenario, for example ambiguous match, not covered, stale, partial answer or source failed.
5. **No forbidden words:** a scenario never expects the product to call a home "verified", "safe" or "approved" (rule 4). An AI step never calculates a figure (decision 0004).
6. **Tags decide when a scenario runs:**
   - `@ui`: browser steps, run with playwright-bdd from stage 5 (decision 0049).
   - `@mcp`: MCP server steps, run from #97.
   - No tag: data steps (fixtures and `costs.json`), run by `make check` from stage 3.

   Tags are lower case; the filter is case-sensitive. Data scenarios (no tag) may go straight from `Given` to `Then`: they check data, not an action. `@ui` and `@mcp` scenarios always have a `When`.

   Until their stage, `@ui` and `@mcp` scenarios are excluded by tag, never deleted.

## Running the specifications
- `make test` (and so `make check` and CI) runs every scenario that is **not** tagged `@ui`, `@mcp` or `@withdrawn`. A scenario that cites an ID missing from `packages/fixtures/generated/costs.json` or `packages/fixtures/data/` fails with a message naming the ID.
- To run only the specifications (pytest-bdd, decision 0049 step P6; it replaced the Reqnroll runner in P8): `uv run --locked pytest packages/specs/tests -m "not ui and not mcp and not withdrawn"`. Each tag is a registered pytest marker (`pyproject.toml`; an unregistered tag fails), so `-m screen` runs one tag, and the test name starts with the scenario ID. `-k` matches substrings, case-insensitively: `-k COSTS-0` picks all three COSTS scenarios, so for exactly one use `-k "COSTS-02_"` (trailing underscore) or the full node ID, `packages/specs/tests/test_specs_scenarios.py::test_COSTS-02_missing_buildings_insurance_is_not_shown_as_zero`. The steps are in `packages/specs/tests/specs_steps.py` and `specs_support.py`. The `.feature` files are loaded from this folder in place; nothing is copied. A new tag must be added to `markers` in `pyproject.toml`.
- **Data steps** (`packages/specs/tests/specs_steps.py`):
  - `Given home "B1" is at story step 1`
  - `Then figure "<figure ID>" exists`
  - `Then figure "<figure ID>" has status "<calculated | missing | not-calculated | ...>"`
  - `Then figure "<figure ID>" shows no amount`
  - `Then the total "<figure ID>" is partial with reason "<category>"`
  - `Then figure "<figure ID>" cites evidence "<evidence ID>"` (the figure's evidence list contains it and the evidence exists)
  - `Then evidence "<evidence ID>" exists`
  - `Then area record "<record ID>" has status "<recorded | no-record-in-source | stale | source-failed | not-covered>"` (a record in `packages/fixtures/data/area.json`)
  - `Then area record "<record ID>" shows no value` (the record carries no `value`, so the screen has nothing to show as a result; rule 7)
  - `Then home "<home ID>" has coverage "<covered | not-yet-covered>"`

  `Given home ... is at story step N` accepts any step from a scenario's `fromStep` to its `toStep` (for B1, step 2 is `from-step-1`) and then requires every figure ID cited in that scenario to start with `<home>.<scenario>.`. `has status` and `shows no amount` apply to cost lines only, not totals. The wording in decision 0043's example is illustrative; this list is the contract.
  A step with no matching wording makes the scenario fail as undefined: add the step to `packages/specs/tests/specs_steps.py` (with tests), rather than rewording the scenario around it.

## Screen template
```gherkin
@screen @buying
Feature: <Screen name>
  Question it answers: "<from doc 03 §5>"
  Modes: buying | renting | both
  Fixtures: <home IDs>; inputs: <evidence IDs>; figures: <figure IDs>
  Required states (doc 03 §5):
    <state> -> <CODE>-NN

  Scenario: <CODE>-01 <short title>
    Given <starting state: story, step, home>
    When <action or screen opening>
    Then <one observable outcome, citing IDs in quotes>

  # Simulated or paid boundaries (labelled) and anything "not calculated" go in scenarios too.
```

## Story template
```gherkin
@story @buying
Feature: Buyer story

  Rule: Step 1 — <title> (snapshot step 1)

    Scenario: BUY-1.1 <short title>
      Given …
      When …
      Then …
```

## Work breakdown
Specifications become build tickets **one story step at a time**: each ticket makes one story step work end to end across the screens it touches (register line SP-02). The stage 5 story items #87 and #88 are epics, split into these step tickets at #71.
