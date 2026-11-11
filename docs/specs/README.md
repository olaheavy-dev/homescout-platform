# Specifications

The prototype specification lives here (decision [0043](../decisions/0043-specification-format.md), SP-01). It describes what each screen, story step and MCP tool must do, precisely enough to build and test it from this folder and the fixtures alone (doc 04 §9 stage 3). The specifications are **executable**: a .NET test project runs these Gherkin files with Reqnroll.

## Layout
| Path | Holds | Issue |
|---|---|---|
| `screens/NN-<screen>.feature` | One feature per screen in doc 03 §5, numbered in that order (for example `05-real-costs.feature`) | #68 |
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
   - `@ui`: browser steps, run with Microsoft.Playwright for .NET from stage 5.
   - `@mcp`: MCP server steps, run from #97.
   - No tag: data steps (fixtures and `costs.json`), run by `make check` from stage 3.

   Until their stage, `@ui` and `@mcp` scenarios are excluded by tag, never deleted.

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
