# Decision register

Every significant product, technical and working decision gets its own record in this folder, named `NNNN-short-title.md` (for example `0011-ways-of-working.md`). The process is in `AGENTS.md` (decision 0035). Each decision is made at the stage listed, the latest point that still lets the work go ahead.

Hard-to-reverse decisions get a full record; easily reversible choices get one line in this register with their default (decision 0035).

**Statuses** (use exactly these; a short note in brackets may follow):
- **Not started:** no record yet.
- **Proposed:** options drafted, or a starting position agreed, but not yet fully decided.
- **Accepted:** decided by the founder.
- **Accepted (partly superseded by NNNN):** some parts replaced by a later record.
- **Proposed (partly superseded by NNNN):** not yet fully decided, and some parts already replaced by a later record.
- **Superseded by NNNN:** fully replaced.
- **Default:** an easily reversible choice recorded as one register line with its default value (decision 0035); changed by a new line.
- **Open:** deliberately undecided, with a reason and a revisit point.
- **Parked:** paused, with a point by which it must resume.

## Already decided

| ID | Decision | Outcome | Where recorded |
|---|---|---|---|
| — | Audience | Buyers and renters with equal weight | Doc 02 §9 |
| — | Launch geography | England first | Doc 02 §7, §9 |
| — | Project purpose | Portfolio and learning first, built by AI coding agents, small monthly budget, kept commercially viable | Doc 04 |
| — | Repository | Public, all rights reserved | Doc 04 §8, `LICENSE` |
| — | First public showcase | Not the clickable prototype, which stays a private reference ([0045](0045-prototype-is-a-private-reference.md)); a free public area check is the first public thing ([0046](0046-public-area-check-first.md)) | [0045](0045-prototype-is-a-private-reference.md) and [0046](0046-public-area-check-first.md), superseding doc 04 §8 |
| — | Stage 1 sign-off | Signed off by the founder on 23 October 2026 | `docs/planning/stage-1-confirmation.md` |

## Register

| ID | Decision | Stage | Status | Record |
|---|---|---|---|---|
| PD-01 | Product category | 1 | Accepted | [0001](0001-product-category.md) |
| PD-02 | Core object | 1 | Accepted | [0002](0002-core-object.md) |
| PD-03 | Main value | 1 | Accepted | [0003](0003-main-value.md) |
| PD-04 | AI presentation in the product | 1 | Accepted | [0004](0004-ai-in-the-product.md) |
| PD-05 | Visual direction | 1 | Accepted | [0005](0005-visual-direction.md) |
| PD-06 | Prototype centrepiece | 1 | Accepted (partly superseded by 0045 and 0046: the prototype is not launched publicly) | [0006](0006-prototype-centrepiece.md) |
| PD-07 | Free/paid principle | 1 | Accepted | [0007](0007-free-paid-principle.md) |
| PD-08 | Name shown on the public demo | 3 | Accepted (founder, 11 Nov 2026: Vestagraph; supersedes parked 0008) | [0044](0044-public-name-vestagraph.md) (supersedes [0008](0008-demo-name.md)) |
| PD-09 | Public brand | 1 | Open (working public brand Vestagraph per [0044](0044-public-name-vestagraph.md); working mark "Contour home", chosen by the founder on 11 Nov 2026 (`.design/prototype/DESIGN_BRIEF.md`); trade-mark clearance of name and mark still to do) | [0009](0009-public-brand.md) |
| PD-10 | Commercial model and prices | 1 | Open (needs user study) | [0010](0010-commercial-model.md) |
| PD-11 | Purpose of the clickable prototype | 3 | Accepted (founder, 11 Nov 2026: private reference, with an exception for design frames shared by link; partly superseded by 0046) | [0045](0045-prototype-is-a-private-reference.md) |
| PD-12 | Public area check first; saved homes need an account | 3 | Accepted (founder, 11 Nov 2026) | [0046](0046-public-area-check-first.md) |
| PD-13 | Places of worship in area information | 3 | Accepted (founder, 11 Nov 2026): one category covering every faith alike, shown only as the nearest places by distance; never counts, densities or an area's religious makeup; a user's own faith is special category data (0014) and is never stored | `docs/references/data-sources.md` (OpenStreetMap), `packages/fixtures/README.md` |
| PD-14 | Move-in checklist (free, made in the browser) | 5b (after the public area check is live, [0047](0047-move-in-checklist.md); candidate stage 5c) | Proposed (11 Nov 2026; research #177) | [0047](0047-move-in-checklist.md) |
| WW-01 | Ways of working | 1 | Accepted (partly superseded by 0015, 0035) | [0011](0011-ways-of-working.md) |
| WW-02 | AI coding tools and setup | 1 | Accepted (partly superseded by 0015, 0035) | [0012](0012-ai-coding-tools.md) |
| WW-03 | Repository and tracking conventions | 1 | Accepted (partly superseded by 0019: calculation placement) | [0013](0013-repo-and-tracking.md) |
| WW-04 | Merge policy and single agent instructions file | 1 | Superseded by 0035 | [0015](0015-agent-merges-after-review.md) |
| WW-05 | Holistic reviews and debt limits | 1 | Superseded by 0035 | [0016](0016-holistic-reviews-and-debt-limits.md) |
| WW-06 | Documentation folder structure and naming | 1 | Accepted | [0017](0017-docs-structure.md) |
| WW-07 | Dependency updates and documentation upkeep | 2 | Accepted (partly superseded by 0027, 0035) | [0024](0024-dependency-updates.md) |
| WW-08 | Learning-first engineering | 2 | Accepted (partly superseded by 0035) | [0026](0026-learning-first-engineering.md) |
| WW-09 | Stage 2 engineering and security hardening | 2 | Accepted (partly superseded by 0035; by 0049: PSF-2.0 joins the allow-list, CodeQL adds Python, `libcst` is a tool-only exemption again) | [0027](0027-stage-2-engineering-hardening.md) |
| WW-10 | Agent roster, design skills and working rules | 2 | Accepted (partly superseded by 0035 and 0050: the project agents are retired and the shared visual reviewer runs on UI pull requests; the design skills and test-first skill stay) | [0031](0031-agent-roster.md) |
| WW-11 | Review fallback when Codex is unavailable | 2 | Superseded by 0035 | [0033](0033-review-fallback.md) |
| WW-12 | Ways of working v2 (consolidated rulebook) | 2 | Accepted (partly superseded by 0042, 0043, 0049 and 0050; 0050 replaces points 1, 2 and 4's how (skills from agent-workflows, Haiku for mechanical subtasks); point 9's pre-approved list gains the packages in 0042 and 0043 (their .NET packages withdrawn when the .NET code is removed, port step P8) and the Python, frontend-template and Aspire lists in 0049; point 9's small-update rule changes: a minor bump of a direct `0.x` dependency or action pin counts as major, from 0039 Q3, carried over by 0042 and 0049) | [0035](0035-ways-of-working-v2.md) |
| DA-01 | Fixture data format | 2 | Accepted (partly superseded by 0027) | [0018](0018-fixture-data-format.md) |
| DA-02 | Calculation script and test vectors | 2 | Accepted (partly superseded by 0021: solution location; by 0049: the engine is written in Python) | [0019](0019-cost-engine-in-csharp.md) |
| SP-01 | Specification format | 3 | Accepted (founder, 11 Nov 2026: executable Gherkin scenarios with permanent IDs in `docs/specs/`; partly superseded by 0049: data scenarios run with pytest-bdd and `@ui` scenarios with playwright-bdd, SP-03) | [0043](0043-specification-format.md) |
| SP-02 | Work breakdown | 3 | Accepted (register line: specifications become build tickets one story step at a time, each step working end to end across the screens it touches; default limit about 8 scenarios and about 400 hand-written lines per ticket (excluding generated files and fixtures), split if larger; the stage 5 story items #87 and #88 are epics split into step tickets at #71; founder, 11 Nov 2026) | — |
| DS-01 | Design tooling | 4 | Accepted (founder, 12 Nov 2026: code-first, no design tool) | [0048](0048-frontend-foundation.md) |
| DS-02 | Design system foundation | 4 | Accepted (founder, 12 Nov 2026: `tokens.css` as the source of truth, the component gallery #150 as the living reference; fonts FE-07, both themes per 0045) | [0048](0048-frontend-foundation.md) |
| FE-01 | Frontend framework and rendering | 4 | Accepted (founder, 12 Nov 2026: TypeScript and Next.js from 0020; App Router with server rendering, run locally only in stage 5; no backend code before stage 5b; hosting decided at 5b) | [0020](0020-application-languages.md), [0048](0048-frontend-foundation.md) |
| FE-02 | Styling and components | 4 | Accepted (founder, 12 Nov 2026: Tailwind CSS v4 mapped to the `tokens.css` custom properties, React Aria Components for complex widgets) | [0048](0048-frontend-foundation.md) |
| FE-03 | Maps and charts | 4 | Not started | |
| FE-04 | Frontend practices | 4 | Accepted (founder, 12 Nov 2026: Vitest and Testing Library, ESLint 9 and Prettier, fixture types from the schemas, axe in the `@ui` scenarios, size-limit and Lighthouse CI; partly superseded by 0049: pnpm, the Next.js template's TypeScript 5.9 and the `frontend/` folder, axe through `@axe-core/playwright`) | [0048](0048-frontend-foundation.md) |
| IN-00 | Hosting strategy | 2 (brought forward) | Accepted (cost first) | [0022](0022-cost-first-hosting.md) |
| IN-01 | Prototype architecture | 5b (moved from 4 by 0048: stage 5 runs locally only) | Not started | |
| IN-02 | Hosting: private prototype (0045), then the public area check (0046) | 5b (moved from 4 by 0048) | Not started | |
| IN-03 | Infrastructure as code | 5b (moved from 4 by 0048) | Not started | |
| IN-04 | CI/CD and environments | 5b (moved from 4 by 0048; domain and secrets before the public area check, 0046) | Not started | |
| IN-05 | Budget cap and cost alerts | 5b (moved from 4 by 0048; before any running cost, 0046) | Not started | |
| FE-05 | Demo analytics and feedback | 5b (before the public area check, [0046](0046-public-area-check-first.md)) | Not started | |
| FE-06 | Area summary export format | 3 | Default (11 Nov 2026): a PDF printed from the browser (no package; the postcode never reaches the server). CSV is not planned for now; a later option | `.design/prototype/INFORMATION_ARCHITECTURE.md` (Check an area) |
| FE-07 | Typefaces | 3 | Default (founder, 11 Nov 2026): Bricolage Grotesque for headlines and the wordmark, Geist for UI and figures; replaces Fraunces. Both SIL Open Font License, Google Fonts | `.design/prototype/tokens.css`, `DESIGN_BRIEF.md` |
| FE-08 | Map marker colours | 3 | Default (founder, 11 Nov 2026): one muted colour and one crafted icon per category (transport slate, shops plum, health teal, schools and childcare indigo, parks olive, police graphite, places of worship taupe; the subtype mapping is in `tokens.css`); the home or postcode-centre pin is the only deep-forest pin. Replaces "one neutral marker colour" (research `area-display-ux.md`); no red, amber or orange, so findings keep those; each at least 3:1 against the map in both themes; colour never the only signal | `.design/prototype/tokens.css`, `DESIGN_BRIEF.md` |
| BE-01 | Backend language and framework | 2 (language), 5b (framework, [0046](0046-public-area-check-first.md)) | Accepted (founder, 12 Nov 2026: Python, final; FastAPI from a one-time import of the founder's template at stage 5b, #93) | [0049](0049-back-to-python-final.md), [0040](0040-fastapi-template-as-api-starting-point.md) |
| BE-02 | Backend architecture and API contract | 5b (before the first API, [0046](0046-public-area-check-first.md)) | Not started | |
| BE-03 | Rules versioning | 6 (before cost engine) | Not started | |
| BE-04 | .NET engineering foundation | 2 | Accepted (partly superseded by 0034; the toolchain by 0049, which adopts 0039 again; fully superseded when the .NET code is removed, port step P8) | [0021](0021-dotnet-engineering-foundation.md) |
| BE-05 | Our own Result type | 2 | Accepted (the principle stands under 0049; the type is rewritten in Python in port step P2) | [0032](0032-own-result-type.md) |
| BE-06 | Rounding boundary test cases | 2 | Accepted | [0034](0034-rounding-boundary-cases.md) |
| WW-13 | Licence allow-list addition | 2 | Accepted (register line: `zlib-acknowledgement`, a permissive Zlib-family licence used by NUnit 5, added to the 0027 allow-list; founder, 23 Oct 2026) | — |
| BE-07 | Fixture schema validator | 2 | Accepted (register line: JsonSchema.Net with JSON Schema 2020-12; added to the pre-approved packages; founder, 23 Oct 2026) | — |
| BE-08 | Validator licence | 2 | Accepted (register line, which is the founder's recorded licence-exception decision required by 0027: JsonSchema.Net 9.x and its two dependencies accepted under their Open Source Maintenance Fee EULA; source remains MIT; fee applies only to binary-release use in revenue-generating activities with ≥ US$10,000 annual revenue, otherwise build from source; founder, 23 Oct 2026) | — |
| BE-09 | Architecture-test package licence | 2 | Accepted (register line, the founder's recorded licence-exception decision required by 0027: NetArchTest.Rules 1.3.2 and its dependency Mono.Cecil are MIT per their GitHub repositories, but their NuGet metadata declares no SPDX licence; founder approved their use, 23 Oct 2026; from P1 the unlicensed step is a safeguard in case GitHub cannot detect their licence (GitHub's dependency graph shows MIT for both on 9 Nov 2026), so P1 exempts them by package (BE-22) and the note that no dependency-review workflow change is needed is out of date) | — |
| BE-10 | Cost-engine output file | 2 | Accepted (register line: the generator writes one file, `packages/fixtures/generated/costs.json`, checked by `schema/generated-costs.schema.json`; the generator owns the folder; founder, 23 Oct 2026) | — |
| BE-11 | Figure ID format | 2 | Accepted (register line: `{homeId}.{scenarioId}.{section}.{name}`, for example `B1.from-step-4.monthly.service-charge`; unique across the file; founder, 23 Oct 2026) | — |
| BE-12 | Scenario IDs | 2 | Accepted (register line: scenarios are worked out from the data; consecutive story steps that use the same evidence merge, and the ID is `from-step-N` for the first step; founder, 23 Oct 2026) | — |
| BE-13 | Lines that do not apply | 2 | Accepted (register line: a line a home does not have is left out of the output, never shown as zero; the line order is fixed by the engine per mode; founder, 23 Oct 2026) | — |
| BE-14 | Monthly differences | 2 | Accepted (register line: a monthly difference is the difference of the two rounded monthly lines, not a rounded difference of yearly figures; founder, 23 Oct 2026) | — |
| BE-15 | Rates in whole basis points | 2 | Accepted (register line: the engine takes rates as whole basis points (550 is 5.5%); a rate that is not a whole number of basis points is not accepted until a decision says otherwise; founder, 23 Oct 2026) | — |
| BE-16 | Missing inputs in a calculation | 2 | Accepted (register line: an anchor input (asking price, mortgage deposit, rate and term when buying; rent when renting) that is missing stops the calculation with a `Result` failure; any other missing bill becomes a `missing` line and makes the total partial; founder, 23 Oct 2026) | — |
| BE-17 | Mortgage term limit | 2 | Accepted (register line: the engine fails a mortgage term over 100 years with `mortgage.term-too-long`, and the evidence and output schemas allow at most 100; this is a technical computation limit because the exact arithmetic gets very slow for huge terms, not a lending rule; founder, 23 Oct 2026) | — |
| BE-18 | Python for the backend, cost engine and AI layer | 2 (reopens stage 2) | Accepted (adopted again by 0049, founder, 12 Nov 2026; had been superseded by 0042 on 10 Nov 2026) | [0036](0036-python-backend.md) |
| AI-07 | MCP server and coding-agent integrations | 6 (local fixture-backed server may come earlier) | Proposed (partly superseded by 0049: the server uses the official `mcp` Python SDK, confirmed at #97. Founder direction, 11 Nov 2026: the MCP server is a product channel for Claude, ChatGPT/Codex, GitHub Copilot and other assistants; the tool surface is specified in stage 3 (#117); whether a local fixture-backed server comes forward to stage 5 is decided after #117) | [0037](0037-mcp-server-and-agent-integrations.md) |
| SE-03 | Accounts and API keys for MCP and API access | 6 (before any public remote MCP server) | Proposed (partly superseded by 0049: token checks use the API's authentication hook from the founder's FastAPI template) | [0038](0038-accounts-and-api-keys-for-mcp.md) |
| BE-19 | The founder's FastAPI template as the API starting point | 5b (moved from 6 by 0049) | Accepted (adopted again by 0049, founder, 12 Nov 2026: the import happens at stage 5b, #93, recording the template version) | [0040](0040-fastapi-template-as-api-starting-point.md) |
| BE-20 | Python engineering foundation | 2 (port step P0) | Accepted (adopted again by 0049, founder, 12 Nov 2026, with its amendments: `vestagraph_*` package names, PSF-2.0 allowed, the port order in 0049) | [0039](0039-python-engineering-foundation.md) |
| BE-21 | Python build backend | 2 (port step P1) | Accepted (adopted again by 0049: `uv_build` is the build backend of each Python package, as in P1, commit `4bbca27`) | — |
| BE-22 | Licence gate fails on unlicensed packages | 2 (port step P1) | Accepted (register line: issue #30 is fixed in P1: dependency review gets a step that fails on packages with no detectable licence, as 0027 requires; actions are not exempted; named exemptions `pkg:nuget/NetArchTest.Rules` and `pkg:nuget/Mono.Cecil` (BE-09); founder, 9 Nov 2026; under 0049 port step P1 (#187) adds PSF-2.0 to `allow-licenses` and the PyPI exemptions `pkg:pypi/libcst` and Vestagraph's own `pkg:pypi/vestagraph-engine`, `vestagraph-generator` and `vestagraph-fixture-validator`; `pkg:pypi/typing-extensions` stays named as a safeguard because GitHub reported its licence as a Python-2.0/GPL expression on 9 Nov 2026; the NuGet exemptions go with the .NET code at P8) | — |
| BE-23 | Export of `uv.lock` (not committed) | 2 (port step P1) | Accepted (adopted again by 0049, as first recorded: the 9 Nov 2026 proof (PRs #50, #51) showed dependency review reads `uv.lock` directly and fails on disallowed and undetectable licences, so **no** export file is committed; the Makefile `requirements` targets stay as the fallback. P1 of 0049 (#187) repeated the proof on 12 Nov 2026: PR #199 failed on `uv.lock » psycopg` (LGPL-3.0-only) and PR #200 on an undetectable licence in `uv.lock`. Corrected 12 Nov 2026: 0049 first said the export would be committed) | — |
| WW-14 | Dependabot groups for `0.x` tools | 2 (port step P1) | Accepted (register line, follows 0039 Q3, kept by 0042 and 0049: the zizmor and dependency-submission actions share the `actions-zero-x` group, listed before the minor-and-patch group, so their minor bumps go to full review; founder, 9 Nov 2026; under 0049 port step P1 (#187) adds a `uv-zero-x` group for `ruff`, `referencing` and `uv-build`) | — |
| WW-15 | Documentation MCP servers for agents | 3 | Default (founder, 12 Nov 2026: "do it"): Microsoft Learn MCP and Context7 in `.mcp.json`, remote HTTP, no API key; for reading documentation only, citing the official page; queries never carry secrets, personal data or `.local/` content (`docs/references/third-party.md`) | `.mcp.json`, `docs/references/third-party.md` |
| WW-16 | Founder decisions asked in a prompt window | 3 | Accepted (register line; founder, 12 Nov 2026: "present decisions to me as a prompt window, with detailed explanation, option and your recommendation and why"): Claude Code uses its question tool, one question per decision, recommended option first with the reason; detail that doesn't fit goes in text just before; the answer and reason are recorded; subagents and Codex hand the content back as text for the main session to ask | `AGENTS.md` "Teach as you build" |
| WW-17 | agent-workflows as Vestagraph's process | 3 | Accepted (founder, 12 Nov 2026) | [0050](0050-agent-workflows-process.md) |
| BE-24 | Back to .NET: C# 15 on .NET 11 for the backend, React stays for the frontend | 2 (reopens the backend language) | Superseded by 0049 (founder, 12 Nov 2026: "Switch to python"; its frontend stack, frontend packages, prerelease rule, `0.x` rule and BE-22 gate are carried over) | [0042](0042-back-to-dotnet-11.md) |
| BE-25 | .NET 11 upgrade split: SDK and runtime now, C# 15 later | 2 | Superseded by 0049 (no further .NET upgrade work; the C# 15 issues #59 and #60 close as not planned) | — |
| BE-26 | Mutation survivors kept and explained | 2 | Accepted (register line, superseded by a mutmut line in port step P7 under 0049, which keeps its principle: survivors are explained in the mutation report, not removed by changing engine code. Original: the surviving Stryker.NET mutants on the cost engine are equivalent, unreachable defensive code, or error-message wording that tests deliberately do not pin; each is explained in the [mutation report](../reviews/2026-10-23-stage-2-mutation-report.md) (11 Nov 2026 update, #112); `break` stays 92; baseline 92.70 %; founder, 11 Nov 2026) | — |
| BE-27 | Differences between homes | 2 (deferred) | Accepted (register line: calculated differences between homes, B1 against B2 and R1 against R2, were deferred by the founder on 23 Oct 2026 until independently worked test cases exist; they are needed before the stage 5 compare and decision-impact screens; stage 2 shows each home's own figures; recorded 11 Nov 2026 from the #24 hand-off; pulled into stage 5 by the founder on 11 Nov 2026: built in #96 ([32a]) before the compare screens) | — |
| BE-28 | Back to Python for the backend (final); frontend from the founder's Next.js template | 3 (reopens the backend language) | Accepted (founder, 12 Nov 2026: "Switch to python"; supersedes 0042 and BE-25; adopts again 0036, 0039, 0040, BE-20, BE-21, BE-23; partly supersedes 0019, 0020, 0021, 0023, 0024, 0025, 0026, 0027, 0029, 0035 point 9, 0037, 0038, 0043, 0046, 0048) | [0049](0049-back-to-python-final.md) |
| BE-29 | Python version | 3 | Default (0049: Python 3.14, the highest CodeQL lists on 12 Nov 2026; move to 3.15 by a new line once CodeQL lists it) | `.python-version` (from port step P1) |
| BE-30 | pytest run limits | 3 | Default (0049: `--maxfail=5`; CI keeps `timeout-minutes: 20`; no local time limit) | `pyproject.toml` (from port step P1) |
| BE-31 | Language-neutral `generatedBy` in `costs.json` | 3 | Default (0049: the generator's `generatedBy` value names neither a language nor a package, so the Python port changes no byte of `costs.json`; set in port step PC) | `packages/fixtures/generated/costs.json` |
| BE-32 | Architecture test bans true division and float routes | 3 | Default (0049 port step P2, #188: `/` and `/=` are not allowed anywhere in the engine, because dividing two ints gives a float, and every division of money goes through `round_ratio`; the test also bans float literals, `>>`, `pow`/negative `**` and the dunder routes to floor, truncate or round. P3a (#189) needed no `Fraction` division: the mortgage formula is whole-number arithmetic plus one `round_ratio`, so the `/` ban stands unchanged. `**` with a variable exponent stays banned too; `whole_power` multiplies in a loop instead) | `packages/vestagraph-engine/tests/test_engine_architecture.py` |
| SP-03 | Two scenario runners, split by tag | 3 | Accepted (founder, 12 Nov 2026, 0049: pytest-bdd runs every scenario except `@ui`, `@mcp` and `@withdrawn`, tags as strict pytest markers; playwright-bdd runs only `@ui`; if a pytest-bdd proof fails in port step P6, the choice goes back to the founder) | [0049](0049-back-to-python-final.md) |
| FE-09 | Automated accessibility route | 3 | Default (0049: `@axe-core/playwright` inside the playwright-bdd `@ui` scenarios, as the founder's Next.js template does; replaces `Deque.AxeCore.Playwright` from 0048) | [0049](0049-back-to-python-final.md) |
| OP-04 | Aspire fallback | 5b | Default (0049: if the TypeScript app host can't run, use the standalone Aspire dashboard container for local telemetry) | [0049](0049-back-to-python-final.md) |
| AI-09 | AI framework trial | 6 | Accepted (founder, 12 Nov 2026, 0049: a short trial of Microsoft Agent Framework for Python and LangChain with LangGraph in the founder's template, the same task on both, compared on AG-UI connection, tracing, evaluation and cost; decides AI-04 at stage 6) | [0049](0049-back-to-python-final.md) |
| DA-03 | Database and geospatial | 5b (before the public area check, [0046](0046-public-area-check-first.md)) | Not started | |
| DA-04 | Ingestion and scheduling | 5b (before the public area check, [0046](0046-public-area-check-first.md)) | Not started | |
| DA-05 | Source licence register | 5b (before the public area check, [0046](0046-public-area-check-first.md)) | Not started | |
| DA-06 | Address and routing providers | 5b (before the public area check, [0046](0046-public-area-check-first.md)) | Not started | |
| DA-07 | Data sourcing: no scraping | 2 | Accepted | [0028](0028-no-scraping.md) |
| SE-01 | Authentication and accounts | 6 (before saved homes, [0046](0046-public-area-check-first.md)) | Not started | |
| SE-02 | Privacy and data protection | 5b (parts 1 and 2, [0046](0046-public-area-check-first.md)), 6 (full, before saved homes) | Proposed (starting position agreed) | [0014](0014-privacy-and-data-protection.md) |
| AI-01 | Model provider and runtime | 6 (before document extraction) | Not started | |
| AI-02 | Retrieval | 6 (before document extraction) | Not started | |
| AI-03 | Evaluation tooling | 6 (before document extraction) | Proposed (evaluation-first accepted in 0025; tooling at stage 6) | [0025](0025-ai-platform-capabilities.md) |
| AI-04 | Orchestration | 6 (decided early) | Open (0049 reopened it: the framework is chosen at stage 6 after a short trial of Microsoft Agent Framework for Python against LangChain and LangGraph in the founder's template (AI-09); task interfaces stay framework-neutral; no framework packages before stage 6; 0023's single agents and approval workflow stand) | [0023](0023-microsoft-agent-framework.md) |
| AI-05 | AI safety | 6 (requirements decided early) | Accepted (capability requirements; partly superseded by 0035) | [0025](0025-ai-platform-capabilities.md) |
| AI-06 | Document extraction principles | 6 (rules set early) | Accepted | [0030](0030-extraction-principles.md) |
| AI-08 | MAF gateway built in the template first | 6 (template work runs earlier) | Superseded by 0042 (founder, 10 Nov 2026); 0049 brings back only a second recorded import of the template's AI gateway at stage 6, after the AI-09 trial | [0041](0041-maf-gateway-built-in-the-template.md) |
| CO-01 | Entitlements and payments | 6 (before entitlements) | Not started | |
| OP-01 | Observability | 6 (before monitoring) | Proposed (OpenTelemetry and local Aspire accepted in 0025; 0049: the Aspire app host is written in TypeScript from stage 5b, OP-04; production telemetry at stage 6) | [0025](0025-ai-platform-capabilities.md) |
| OP-02 | Scheduling and notifications | 6 (before monitoring) | Not started | |
| OP-03 | Outside services: provenance and live tests | 6 (rule set early) | Accepted (partly superseded by 0049: live-service tests are excluded with a pytest marker) | [0029](0029-external-services.md) |

## Record template

```markdown
# NNNN: <decision title>

**ID:** <register ID>  
**Status:** Not started | Proposed | Accepted | Accepted (partly superseded by NNNN) | Superseded by NNNN | Open | Parked  
**Date:** <YYYY-MM-DD>  
**Stage:** <roadmap stage>

## Context
What needs deciding, why now, and the constraints (goals, budget, England first, public repo).

## Options
### Option A: <name>
What it is. Trade-offs, cost, learning value, effect on commercial options.

### Option B: <name>
…

## Recommendation
The drafter's recommendation and why.

## Decision
The founder's choice, and the reason in their own words.

## Consequences
What this commits us to, what it rules out, and what would make us revisit it.
```
