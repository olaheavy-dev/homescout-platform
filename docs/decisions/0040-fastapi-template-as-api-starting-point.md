# 0040: The founder's FastAPI template as the API starting point

**ID:** BE-19  
**Status:** Superseded by [0042](0042-back-to-dotnet-11.md) (founder, 10 Nov 2026; nothing was imported from the template)  
**Date:** 2026-11-06  
**Stage:** 6 (the API slice, P7 of the port plan); the template changes can run earlier, in parallel with the port  
**Amends:** the "Private reference sources" rule in `AGENTS.md`, for this one public repository only.

## Context
Decision 0036 moves the backend to Python, and 0037 and 0038 add an MCP server and API keys. The founder has a public, all-rights-reserved Copier template, [house-template-fastapi](https://github.com/olaheavy-dev/house-template-fastapi) (the founder is its copyright holder), that already provides a FastAPI app factory, settings from the environment, RFC 9457 problem responses, structured logs, OpenTelemetry, health endpoints, security headers, cursor pagination, a fail-closed authentication hook, and a strict toolchain (uv, ruff, mypy strict, import-linter, pytest). It also provides things HomeScout has not decided on or conflicts with: PostgreSQL with pgvector and migrations (DA-03 and AI-02 are undecided), S3 storage, and a LangChain, LangGraph and LangSmith model gateway (decision 0023 chooses Microsoft Agent Framework).

`AGENTS.md` says never to copy from the founder's earlier projects or name them in tracked files. That rule exists to keep HomeScout fresh and the private sources private. This template is public, the founder owns it, and the founder chose to use it as a starting point and as a template for future projects.

## Options
### Option A: One-time import, trimmed, then HomeScout owns its copy (recommended)
Generate the layer once in a scratch folder, bring `apps/api/` into HomeScout trimmed to what it needs, and record the template version and commit here. Improvements that suit every project are fed back to the template by hand.

### Option B: Keep a live `copier update` link
Fewer manual ports, but HomeScout will diverge (workspace layout, engine, MCP, API keys), so updates would become messy merges. The template also assumes its base layer, which would overwrite HomeScout's rulebook, CI and settings.

### Option C: Reference only, write everything fresh
Cleanest on the old rule, but throws away working, tested conventions the founder wants to reuse.

## Recommendation
Option A.

## Decision
Option A, as the founder asked on 6 November 2026 ("make it a starting point ... it would be a template for other projects going forward").

- **Scope of the exception:** only `house-template-fastapi` (and the `house-template-base` repository it depends on) may be named in tracked files and used as a starting point. The founder's other earlier projects and the reviewed AI sample stay private under the existing rule.
- **What comes across:** the app conventions and structure (factory, settings, problems, logging, health, security headers, pagination, auth hook, tests, rules file), adapted to the HomeScout workspace (`apps/api/` beside `packages/`), the strict toolchain chosen in the port plan, and the engine as a workspace member that the API only calls.
- **What does not come across at first:** the base layer, the database, migrations and storage (stage 6 decisions), and the LangChain gateway. The AI layer uses Microsoft Agent Framework (0023). The gateway's idea of a per-day model-spend cap, reserved before a call and settled after it, is kept for IN-05 and 0022, to be rebuilt for that framework.
- **Licence and provenance:** the template's licence is the founder's own; this record is the provenance. Every dependency that comes across is still checked against the 0027 licence allow-list and added to `docs/references/third-party.md`.
- **Template track (separate repository):** three small changes are made in the template first, so the import is a configuration, not hand-trimming: make the database and storage optional (template issue 29), make the LLM gateway optional without a framework choice (issue 30), and stop shipping default model names and prices (issue 31). Pluggable authentication and a Microsoft Agent Framework gateway (a second option beside LangChain, behind one framework-neutral interface, so the template offers `none`, `langchain` or `maf`) come after HomeScout builds them (0038 and the stage 6 AI work, decision 0023), and are then lifted into the template; a template issue for the second gateway is filed when HomeScout starts that work.
- **Template repository rules:** work there follows that repository's own rulebook and release process, in its own sessions.

## Consequences
- `AGENTS.md` gets an exception paragraph under "Private reference sources".
- The port plan gains **P7, the API skeleton**, after the engine port: `apps/api/` built from the template with the database, storage and gateway off, health and problem responses, one read-only cost endpoint that calls the engine, the OpenAPI file checked in CI, and tests in the template's style. Accounts and keys (0038) and the MCP server (0037) build on it.
- New packages that arrive with P7 (FastAPI and its dependencies, pydantic-settings, structlog and others) need founder approval and licence checks, like every other package.
- If the template changes in a way that makes the import stale before P7 starts, the import uses the newer version and this record is updated with the commit used.
- Revisit if the template's structure fights HomeScout's workspace, or if maintaining both costs more than writing fresh.
