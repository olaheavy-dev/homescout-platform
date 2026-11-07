# 0041: The Microsoft Agent Framework gateway is built in the template first

**ID:** AI-08  
**Status:** Accepted (founder, 7 Nov 2026: the answer "Yes, a short superseding record" to the planning question on [template issue 33](https://github.com/olaheavy-dev/house-template-fastapi/issues/33), which says: the MAF gateway is built in the template at 0.8.0 and HomeScout consumes it later, because 0040 and 0023 say the opposite order)  
**Date:** 2026-11-07  
**Stage:** 6 (the AI layer); the template work runs earlier, beside the port  
**Supersedes in part (no older text is rewritten):**
- [0023](0023-microsoft-agent-framework.md): the "Template follow-up" paragraph. It says HomeScout builds its framework-based gateway first and the template follows. This record reverses that order for the gateway.
- [0040](0040-fastapi-template-as-api-starting-point.md): the "Template track" sentence that puts the Microsoft Agent Framework gateway after HomeScout builds it, and the "one-time import" wording, which now allows a second recorded import at stage 6 (below). The same sentence in 0040 says pluggable authentication follows HomeScout's own build; that is unchanged.

## Context
0023 chose Microsoft Agent Framework (MAF) for HomeScout and said the template would get a MAF gateway only after HomeScout had built one. 0040 said the same. Since then the template's plan changed:
- [Template issue 33](https://github.com/olaheavy-dev/house-template-fastapi/issues/33) makes the template's model layer framework-neutral: a `core` that imports no framework, with the LangChain parts as one adapter.
- [Template issue 35](https://github.com/olaheavy-dev/house-template-fastapi/issues/35) is the epic for a MAF gateway as a second adapter.
- [Template issue 38](https://github.com/olaheavy-dev/house-template-fastapi/issues/38) is the release plan: version 0.7.0 holds the optional database and storage, no default model names or prices, and the neutral layer; version 0.8.0 holds the MAF gateway (with a Postgres session store and checkpoint storage) and its docs. These are plans, not released versions.

Two copies of the idea, one in HomeScout and one lifted later, would drift, and the template's neutral core would have no second adapter to prove it is neutral until HomeScout's stage 6.

## Options
### Option A: Build the MAF gateway in the template first; HomeScout takes it by a second recorded import at stage 6 (recommended)
The gateway is built and tested once, in the template. HomeScout's P7 import (0040) still brings the API skeleton with no model layer; at stage 6, when the AI work starts, HomeScout takes the gateway from a template release that has it. The cost: HomeScout's stage 6 AI work depends on the template's release dates, and on the template's Postgres-backed design (see Consequences).

### Option B: Keep the old order
HomeScout builds its own gateway at stage 6 and the template follows. HomeScout's stage 6 never waits on a template release, but the work is done twice and the template's neutral core stays unproven by a second adapter.

## Recommendation
Option A.

## Decision
Option A.

- **Order:** the template builds the framework-neutral core (issue 33, release 0.7.0 per issue 38) and the MAF adapter (issue 35, release 0.8.0) first. The template pieces planned for HomeScout to reuse are the per-day model-spend cap (reserve a call's worst-case cost, settle the real cost, one record per call; IN-05 and 0022), price handling, call records, and prompt versioning by content hash. Context-window reporting with token-measured trimming and no summarising ([template issue 46](https://github.com/olaheavy-dev/house-template-fastapi/issues/46)) is a follow-up to the MAF work, not part of 0.8.0.
- **P7 (the API skeleton):** imports a template release at or after 0.7.0 with the model layer off and the database off, exactly as 0040 says. No model-framework code or packages arrive at P7, which keeps 0023's rule that no framework packages are added before stage 6.
- **Stage 6 (the AI work):** HomeScout takes the gateway by a second one-time import, generated in a scratch folder from a template release at or after 0.8.0 and copied across, recorded in the same way as 0040 requires (template version and commit, added to 0040). If 0.8.0 is late, only the stage 6 AI work waits; P7 does not.
- **What does not change:** HomeScout does not use the LangChain adapter (0023, 0040). HomeScout's own task interfaces stay framework-neutral (0023), and the figures, citation and number guards (0004, 0025) apply to every agent. Pluggable authentication still follows HomeScout's own build (0040's "Template track").
- **Packages and licences:** this record approves no packages. Whether the Python MAF packages are already pre-approved is read differently by 0035 point 9 (which lists Microsoft Agent Framework once stage 6 starts) and 0036 and 0039 (which treat the pre-approved list as .NET plus the Python tools, with no MAF entry), so they are treated as not pre-approved: the pull request that adds them asks for approval, checks the 0027 licence allow-list, and adds an entry to `docs/references/third-party.md`.
- **Template rules:** the template's work follows its own rulebook and release process, in its own sessions (0040).

## Consequences
- 0023 and 0040 get a status note pointing here, and the register gets a row (AI-08) and notes on AI-04 and BE-19. Neither older record's text changes.
- **The gateway needs PostgreSQL.** The template's spend cap, session store and checkpoints live in a database, so taking the gateway depends on DA-03 (the database decision, not started) choosing PostgreSQL. If DA-03 chooses something else, this record is revisited.
- Stage 6 AI work starts from the template's gateway instead of a blank file, so it depends on template releases 0.7.0 and 0.8.0.
- **Revisit if:** the MAF adapter does not meet HomeScout's needs once tried at stage 6 (for example, it cannot keep the spend cap or the number guards); MAF's Python package is not stable enough to pin; or DA-03 does not choose PostgreSQL.
