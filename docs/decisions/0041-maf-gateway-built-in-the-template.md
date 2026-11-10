# 0041: The Microsoft Agent Framework gateway is built in the template first

**ID:** AI-08  
**Status:** Superseded by [0042](0042-back-to-dotnet-11.md) (founder, 10 Nov 2026; the gateway is built in HomeScout's .NET API at stage 6)  
**Date:** 2026-11-07  
**Stage:** 6 (the AI layer), or P7 if the gateway is ready; the template work runs earlier, beside the port  
**Supersedes in part (no older text is rewritten):**
- [0023](0023-microsoft-agent-framework.md): the "Template follow-up" paragraph (HomeScout builds its framework-based gateway first and the template follows; this record reverses that order), and the consequence "No framework packages are added before stage 6", which becomes "none before stage 6, except with the gateway at P7 when the three conditions in Decision are met"; and "when it is added at stage 6" (Python bullet), which now reads "when it is added, at P7 or stage 6".
- [0040](0040-fastapi-template-as-api-starting-point.md): the "Template track" sentence that puts the Microsoft Agent Framework gateway after HomeScout builds it; "What does not come across at first" and the skeleton with "the database, storage and gateway off", which now allow the gateway (and with it the database and migrations) to come across at P7 when the conditions below are met; and the "one-time import" wording, which now allows a second recorded import at stage 6. The same sentence in 0040 says pluggable authentication follows HomeScout's own build; that is unchanged.

## Context
0023 chose Microsoft Agent Framework (MAF) for HomeScout and said the template would get a MAF gateway only after HomeScout had built one. 0040 said the same. Since then the template's plan changed:
- [Template issue 33](https://github.com/olaheavy-dev/house-template-fastapi/issues/33) makes the template's model layer framework-neutral: a `core` that imports no framework, with the LangChain parts as one adapter.
- [Template issue 35](https://github.com/olaheavy-dev/house-template-fastapi/issues/35) is the epic for a MAF gateway as a second adapter.
- [Template issue 38](https://github.com/olaheavy-dev/house-template-fastapi/issues/38) is the release plan: version 0.7.0 holds the optional database and storage, no default model names or prices, and the neutral layer; version 0.8.0 holds the MAF gateway (with a Postgres session store and checkpoint storage) and its docs. These are plans, not released versions.

Two copies of the idea, one in HomeScout and one lifted later, would drift, and the template's neutral core would have no second adapter to prove it is neutral until HomeScout's stage 6.

## Options
### Option A: Build the MAF gateway in the template first; HomeScout takes it at P7 if it is ready, otherwise at stage 6 (recommended)
The gateway is built and tested once, in the template. When P7 starts, if the conditions in "Decision" are met, the API and the gateway come across in the same import. If not, P7 goes ahead without the gateway and a second recorded import brings it at stage 6. The cost: HomeScout takes on the template's release dates and its PostgreSQL-backed design, and a P7 that includes the gateway also includes the database and the MAF packages earlier than 0023 and 0040 planned.

### Option B: Keep the old order
HomeScout builds its own gateway at stage 6 and the template follows. HomeScout's stage 6 never waits on a template release, but the work is done twice and the template's neutral core stays unproven by a second adapter.

### Option C: Always the skeleton at P7 and the gateway at stage 6
Keeps 0023 and 0040 as written except for who builds the gateway. Simplest, and it keeps P7 small, but it always needs a second import, even if the gateway is ready at P7.

## Recommendation
Option A. It gives one import when everything is ready, and falls back to Option C's behaviour when it is not. Option B duplicates the work.

## Decision
Option A.

- **Order:** the template builds the framework-neutral core (issue 33, release 0.7.0 per issue 38) and the MAF adapter (issue 35, release 0.8.0) first. The template pieces planned for HomeScout to reuse are the per-day model-spend cap (reserve a call's worst-case cost, settle the real cost, one record per call; IN-05 and 0022), price handling, call records, and prompt versioning by content hash. Context-window reporting with token-measured trimming and no summarising ([template issue 46](https://github.com/olaheavy-dev/house-template-fastapi/issues/46)) is a follow-up to the MAF work, not part of 0.8.0.
- **P7 (the API skeleton), "if ready":** P7 imports a template release at or after 0.7.0. It includes the gateway in the same import when all three of these are true on the day P7 starts:
  1. a template release that has the MAF gateway (planned 0.8.0) is out;
  2. HomeScout's database decision (DA-03) has chosen PostgreSQL, because the gateway keeps its spend cap, sessions and checkpoints there;
  3. the founder has approved the MAF packages in advance (for example on the P7 plan issue) and they have passed the 0027 licence check (see Packages, below).
  Condition 2 means deciding DA-03 early: it is planned for stage 6 ("before real data", doc 04), so if it has not been decided when P7 starts, P7 goes ahead without the gateway. When the gateway does come at P7, storage stays off and pgvector is not enabled until their own decisions (stage 6, AI-02); the gateway arrives unconfigured, with no provider or model, until AI-01 and 0022 choose one at stage 6.
  If any of the three is not true, P7 goes ahead without the gateway, exactly as 0040 describes (model layer off, database off), and no framework packages arrive.
- **Stage 6 (the AI work):** if the gateway did not come with P7, HomeScout takes it by a second one-time import at stage 6, generated in a scratch folder from a template release at or after 0.8.0 and copied across. Either way the template version and commit are recorded, as 0040 requires (added to 0040). P7 never waits for template release 0.8.0; only the gateway does.
- **What does not change:** HomeScout does not use the LangChain adapter (0023, 0040). HomeScout's own task interfaces stay framework-neutral (0023), and the figures, citation and number guards (0004, 0025) apply to every agent. Pluggable authentication still follows HomeScout's own build (0040's "Template track").
- **Packages and licences:** this record approves no packages; condition 3 above is a separate founder approval. Whether the Python MAF packages are already pre-approved is read differently by 0035 point 9 (which lists Microsoft Agent Framework once stage 6 starts) and 0036 and 0039 (which treat the pre-approved list as .NET plus the Python tools, with no MAF entry), so they are treated as not pre-approved: the founder's approval comes before the pull request that adds them (condition 3), which then checks the 0027 licence allow-list, adds the entry to `docs/references/third-party.md` and is a founder merge (0039).
- **Template rules:** the template's work follows its own rulebook and release process, in its own sessions (0040).

## Consequences
- 0023 and 0040 get a status note pointing here, and the register gets a row (AI-08) and notes on AI-04 and BE-19. Neither older record's text changes.
- **The gateway needs PostgreSQL.** The template's spend cap, session store and checkpoints live in a database, so taking the gateway, at P7 or at stage 6, depends on DA-03 (the database decision, not started) choosing PostgreSQL. If DA-03 chooses something else, this record is revisited.
- Stage 6 AI work starts from the template's gateway instead of a blank file, so it depends on template releases 0.7.0 and 0.8.0. If the gateway comes with P7, the skeleton also carries PostgreSQL, migrations and the MAF packages from the start, and 0040's "database off" skeleton no longer applies to that import.
- **Revisit if:** the MAF adapter does not meet HomeScout's needs once tried at stage 6 (for example, it cannot keep the spend cap or the number guards); MAF's Python package is not stable enough to pin; or DA-03 does not choose PostgreSQL.
