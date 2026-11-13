# Screen specifications (#68): design

**Date:** 13 Nov 2026 · **Issue:** #68 · **Approved by the founder:** 13 Nov 2026, in a prompt window ("Approve").

## Intent
Stage 3's gate (doc 04 §9) needs a specification precise enough that someone who hasn't read docs 01 to 03 could build the prototype from `docs/specs/` and the fixtures alone. #68 writes one Gherkin feature per screen; the story scripts (#69, #70) and the gate (#71) build on it.

## Goals
- One `docs/specs/screens/NN-<screen>.feature` per screen, in the SP-01 format and the screen template in `docs/specs/README.md`.
- Every required state in doc 03 §5 is mapped to at least one scenario.
- Every figure is cited by evidence ID or generated figure ID, never typed (rule 2); missing is never zero (rule 7).
- Free and paid limits from doc 02 §8 appear as labelled, simulated limits.

## Non-goals
- No app code, no new step definitions beyond what a data scenario needs (and only with tests).
- No new fixture records in #68 (founder, 13 Nov 2026: "Specs now, data later").

## Anti-goals
- A spec that expects the product to call a home "verified", "safe" or "approved", or an AI step that calculates (rule 4, 0004).
- A state that silently disappears because no fixture backs it.

## Constraints
- **Screens (14):** doc 03 §5's 13, with the landing as the postcode area check (decision 0046), plus **Check an area** (0046, H5). Names follow `.design/prototype/INFORMATION_ARCHITECTURE.md` where it renames a screen.
- **Numbering:** files follow doc 03 §5's order; Check an area is appended as `14`, so `05-real-costs.feature` and its permanent IDs (COSTS-01 to 03) stay where they are.
- **Tags (SP-03):** untagged data scenarios run in `make check` now; screen behaviour is `@ui` and waits for stage 5.

## Approaches
1. **Three pull requests in build order (chosen).** Area (landing, Check an area, Nearby), then home and money (identity confirmation, home overview, costs, compare, what changed), then questions and sharing (viewing companion, document review, question detail, reply checking, My move, share). Matches 0046's stage 5 order and keeps each review small.
2. One pull request with all 14 files: fewer merges, but one very large review, likelier to need several rounds.
3. Specs and missing fixture records together: every state backed by data at once, but touches data and schemas and grows the review (founder chose against it).

## Decided by the founder
- Data gaps (13 Nov 2026, "Specs now, data later (Recommended)"): a required state with no fixture record is written as a `@ui` scenario with a comment `# fixture needed: #NNN`, and one `noticed`-style issue per missing record is opened, to be filled by the build ticket that uses it.
- Design and split (13 Nov 2026, "Approve (Recommended)").

## Calls made by the agent
- Doc 03 §5 is updated in pull request 1 (landing row, new Check an area row), as the pre-flight fix 0046 left stale.
- #67 is closed by pull request 1: its output exists as `.design/prototype/INFORMATION_ARCHITECTURE.md`.
- Screen codes (for example `AREA`, `NEAR`, `LAND`) are chosen per file and never reused.

## Left to the builder
Scenario wording, how many scenarios per screen (one observable outcome each), and which data scenarios are worth running now.
