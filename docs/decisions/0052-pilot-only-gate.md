# 0052: A pilot-only gate, so the pilot is built before the home workspace

**ID:** WW-18  
**Status:** Accepted (founder, 13 Nov 2026, in a prompt window)  
**Date:** 2026-11-13  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** doc 04 §9's order "stage 3 gate, then stage 5, then stage 5b" for the pilot's screens; the stage 3 gate (#71) as one gate over every screen

## Context
The founder chose, on 13 Nov 2026, to write the pilot's specifications first ("Pilot specs first (Recommended)") and then asked to "start the development tickets as soon as we are done with pilot specs". The stage 3 gate (#71) expects every screen's specification, including the home workspace screens (#68 parts 2 and 3) and the story scripts (#69, #70), before anything is built. The pilot (stage 5b, decisions 0046 and 0051) needs none of the home screens.

## Options
### Option A: Pilot-only gate (recommended)
Split the gate. A short gate checks that the pilot's specifications alone are complete and buildable; then the pilot's development tickets start. The home specifications, story scripts and the full stage 3 gate resume before the home workspace is built.

### Option B: No gate
Write the pilot's tickets as soon as its specifications merge. Fastest, but nothing checks the specifications are complete before building.

### Option C: Keep the full gate
Finish every specification and pass the whole stage 3 gate first. Slowest; today's plan.

## Decision
**Option A** (founder, 13 Nov 2026: "Pilot-only gate (Recommended)").

**The pilot gate passes when:**
- every pilot screen and feature in the design (`docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`) has a specification in `docs/specs/` and, where it is a screen, a board on the design canvas's "Pilot · public area check" page;
- every required state in those specifications maps to a scenario, and every missing fixture has a `noticed` issue;
- the AI evaluation set (AI-03) is written;
- no `review-followup` issue is open against the pilot specifications.

**Then:** one development ticket per buildable slice, each with acceptance criteria and its tests, starting with the stage 5b decisions (0046) and the app shell (#86).

## Consequences
- **#68 pauses** after part 1 (#217), with the resume point recorded on the issue (13 Nov 2026). #69, #70 and the full gate (#71) follow later, before the home workspace is built.
- **The private prototype (stage 5) for the home workspace** comes after the pilot. The pilot's own screens are built on real data in stage 5b, not first as a fixture-only prototype; the area fixtures still serve the tests.
- **Doc 04 §9 and the status file** show the pilot track first.
- **Revisit if** the pilot's build shows that the home screens' design changes the shared components (the app shell, the topic summary or the map) enough to rework the pilot.
