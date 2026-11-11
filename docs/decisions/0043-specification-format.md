# 0043: Specification format — executable Gherkin scenarios in `docs/specs/`, run with Reqnroll

**ID:** SP-01  
**Status:** Accepted (founder, 11 Nov 2026)  
**Date:** 2026-11-11  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** [0035](0035-ways-of-working-v2.md) point 9 (the pre-approved package list gains Reqnroll and Microsoft.Playwright for .NET, approved by the founder below).

## Context
Stage 3 writes the prototype specification: one specification per screen for the 13 screens in doc 03 §5, plus the buyer and renter story scripts (#69, #70) and the MCP tool surface (#117). Doc 04 §9 says it must be precise enough that "someone who hasn't read docs 01–03 could build the prototype from the spec and the fixtures alone", and that agents and tests can use it directly.

Constraints:
- Every figure is either a fixture input or a calculated output from the cost engine (rule 2). Missing data is never shown as zero (rule 7).
- Decision 0017 planned `docs/specs/` for stage 3. Decision 0031 lets the design skills write working notes to `.design/<feature>/`.
- The founder is learning .NET (decision 0042).

## Options
- **A. Numbered one-line checks with permanent IDs.** Story steps use Given/When/Then.
  - For: short.
  - Against: two styles mixed, and checks that are only text.
- **B. Given/When/Then scenarios with permanent IDs, written in Gherkin and run as tests with Reqnroll (chosen).**
  - For: one style everywhere, in screens, stories and MCP tools. The spec *is* the test, so the two can't drift apart. Behaviour-driven development is a widely used .NET practice, which suits the learning goal.
  - Against: longer than one-line checks. It needs two new packages and a test project that runs the specs.
- **C. The design plugin's own files in `.design/<feature>/`.**
  - For: only one copy.
  - Against: the format belongs to a third-party plugin, there are no stable IDs, and the MCP specification doesn't fit it.

## Recommendation
The planner recommended A. When asked, the founder chose B. They then approved Reqnroll so the scenarios run, and chose Microsoft.Playwright for .NET for the browser scenarios.

## Decision
Founder, 11 Nov 2026:
- "docs/specs + Given/When/Then".
- "Reqnroll is approved".
- Browser scenarios run with "Microsoft.Playwright for .NET".

**Where specs live:**
- `docs/specs/README.md`: the rules and templates.
- `docs/specs/screens/NN-<screen>.feature`: one Gherkin feature per screen, numbered in doc 03 §5 order.
- `docs/specs/stories/buyer.feature` and `renter.feature`.
- `docs/specs/mcp-tools.feature`.

The design skills' `.design/<feature>/` files stay as working notes. If the two disagree, `docs/specs/` wins.

**Format:** standard Gherkin. The `Feature:` description holds the screen's question, modes, fixtures and the required-state map. Each acceptance criterion is a `Scenario:` whose name starts with a permanent ID:

```gherkin
@screen @buying
Scenario: COSTS-02 missing insurance is not zero
  Given the buyer story at step 1 with home "B1"
  When the Real costs screen opens
  Then the buildings insurance line shows status "missing" from figure "B1.from-step-1.monthly.buildings-insurance"
  And no line shows £0 for it
```

**Permanent IDs:** each scenario has a screen or area code and a number, such as `COSTS-02`, `BUY-3.2` or `MCP-01`.
- An ID is never reused or renumbered.
- A scenario that is no longer needed stays in the file, tagged `@withdrawn`.

**Figures:** inputs are cited by evidence ID and calculated values by figure ID from `packages/fixtures/generated/costs.json`, in quotes, never as a typed amount (rule 2). A value the engine does not produce is written "not calculated". Missing and partial states are named explicitly (rule 7).

**Executable with Reqnroll:** a .NET test project runs the `.feature` files in `docs/specs/` with Reqnroll on NUnit.
- **Data steps run from stage 3.** They read the fixtures and `costs.json`, so every cited figure ID, evidence ID, status and partial flag is checked by `make check` as soon as the spec is written.
- **Browser steps run from stage 5.** They are tagged `@ui`, and they drive the Next.js prototype with Microsoft.Playwright for .NET; until stage 5 they are excluded from `make check` by that tag.
- **MCP steps run from the MCP server's build (#97).** They are tagged `@mcp`, with the same exclusion until then.
- **Test link:** the scenario name carries the ID, so the verifier finds the scenario and its test with one search.

**Packages approved by the founder (11 Nov 2026), added to the pre-approved list:**
- **`Reqnroll`** and its NUnit integration (`Reqnroll.NUnit`), BSD-3-Clause.
- **`Microsoft.Playwright`** for .NET (with its NUnit helpers if needed), Apache-2.0.

Each still passes the 0027 licence check and gets a `docs/references/third-party.md` entry when first added. Exact versions are pinned then.

**To verify when Reqnroll is first added** (Reqnroll's compatibility page lists .NET up to 10 on 11 Nov 2026):
- that it runs on **.NET 11**, **NUnit 5** and **Microsoft.Testing.Platform**;
- that it can read feature files from `docs/specs/` outside the test project.

If any of these fails, stop and bring the options to the founder (for example a different NUnit plugin, the xUnit or MSTest integration, or copying the feature files into the test project at build time).

## Consequences
- `docs/specs/` is created with its README and templates in this decision's pull request.
- #121 (`[11a]`) adds the Reqnroll test project, the first data step definitions and the compatibility checks. It comes before the screen specifications (#68), so specs are checked as they are written.
- The screen and story specifications (#68, #69, #70) and the MCP tool surface (#117) follow in this format.
- FE-04 (#76) builds on this: browser tests use Microsoft.Playwright for .NET through Reqnroll. Automated accessibility checks with axe are still FE-04's choice.
- The work breakdown (SP-02) is a register line: one ticket per story step, and #87 and #88 become epics.
- **Revisit if:** Reqnroll can't run on .NET 11, NUnit 5 or Microsoft.Testing.Platform, or writing scenarios proves too slow for 13 screens.
