# 0041: The Microsoft Agent Framework gateway is built in the template first

**ID:** AI-08  
**Status:** Accepted (founder, 7 Nov 2026: the answer "Yes, a short superseding record" to the planning question on [template issue 33](https://github.com/olaheavy-dev/house-template-fastapi/issues/33))  
**Date:** 2026-11-07  
**Stage:** 6 (the AI layer); the template work runs earlier, beside the port  
**Supersedes in part (no older text is rewritten):**
- [0023](0023-microsoft-agent-framework.md): the "Template follow-up" paragraph. It says HomeScout builds its framework-based gateway first and the template follows. This record reverses that order for the gateway.
- [0040](0040-fastapi-template-as-api-starting-point.md): the "Template track" sentence that puts the Microsoft Agent Framework gateway after HomeScout builds it. Pluggable authentication is unchanged: HomeScout still builds it first (0038), and the template follows.

## Context
0023 chose Microsoft Agent Framework (MAF) for HomeScout and said the template would get a MAF gateway only after HomeScout had built one. 0040 said the same. Since then the template's own plan changed:
- Template issue 33 makes the template's model layer framework-neutral (a `core` that imports no framework, with the LangChain parts as one adapter).
- Template issue 35 is the epic for a MAF gateway as a second adapter. The plan on issue 33 puts it in template version 0.8.0 (that is a plan, not a released version).
- The founder wants to build and test the gateway once, in the template, where it can be tried on its own, instead of building it inside HomeScout and lifting it out later.

Two copies of the idea, one in HomeScout and one lifted later, would drift. The order in 0023 and 0040 would also make the template's neutral core wait for HomeScout's stage 6.

## Options
### Option A: Build the MAF gateway in the template first; HomeScout takes it by the one-time import (recommended)
The template releases the neutral core and the MAF adapter (0.8.0). HomeScout's P7 import (0040) uses a template release at or after 0.8.0.

### Option B: Keep the old order
HomeScout builds its own gateway at stage 6 and the template follows. Nothing in the template waits on the port, but the work is done twice and the template's neutral core has no second adapter to prove it is neutral.

## Recommendation
Option A.

## Decision
Option A.

- **Order:** the template builds the framework-neutral core (issue 33) and the MAF adapter (issue 35) first. The pieces HomeScout needs from it are the per-day model-spend cap (reserve a call's worst-case cost, settle the real cost, one record per call; IN-05 and 0022), the price handling, the call records, prompt versioning by content hash, and the context-window report with token-measured trimming (no summarising). They are built there, not rebuilt in HomeScout.
- **What HomeScout takes, and when:** the P7 import (0040) uses a template release at or after 0.8.0, so the neutral core and the MAF adapter come across. The skeleton still starts with the gateway off, as 0040 says; switching it on is the stage 6 AI work (0023).
- **What does not change:** HomeScout does not use the LangChain adapter (0023, 0040). HomeScout's own task interfaces stay framework-neutral (0023), and the figures, citation and number guards (0004, 0025) apply to every agent. Pluggable authentication still follows HomeScout's own build (0038).
- **Packages and licences:** the MAF packages and anything else that arrives with the import still need founder approval and a licence check against the 0027 allow-list, and an entry in `docs/references/third-party.md`, in the pull request that adds them. This record approves none of them.
- **Version:** the template version and commit used by the import are recorded in the P7 pull request and added to 0040, as 0040 already requires.
- **Template rules:** the template's work follows its own rulebook and release process, in its own sessions (0040).

## Consequences
- 0023 and 0040 get a status note pointing here, and the register gets a row (AI-08) and notes on AI-04 and BE-19. Neither older record's text changes.
- Stage 6 AI work starts from the template's gateway instead of a blank file, so it depends on template releases 0.7.0 (optional database) and 0.8.0 (neutral core and MAF adapter).
- If the template's MAF gateway is late, P7 can still proceed with the gateway off; only the stage 6 AI work waits.
- **Revisit if:** the MAF adapter does not meet HomeScout's needs once tried at stage 6 (for example, it cannot keep the spend cap or the number guards), or MAF's Python package is not stable enough to pin.
