# 0049: Back to Python for the backend (final); the frontend starts from the founder's Next.js template

**ID:** BE-28  
**Status:** Accepted (founder, 12 Nov 2026)  
**Date:** 2026-11-12  
**Stage:** 3 (reopens the backend language before stage 4; the port runs alongside the stage 3 gate, #71)  
**Supersedes (no older text is rewritten; each record's status line says what changed):**
- fully: [0042](0042-back-to-dotnet-11.md) (back to .NET 11), except the parts listed under "Carried over" below, and register line BE-25 (the .NET 11 upgrade split);
- adopts again, with the amendments below: [0036](0036-python-backend.md) (Python backend), [0039](0039-python-engineering-foundation.md) (Python engineering foundation), [0040](0040-fastapi-template-as-api-starting-point.md) (the FastAPI template as the API starting point) and register lines BE-20, BE-21 and BE-23; [0041](0041-maf-gateway-built-in-the-template.md) only as the second template import (decision item 11d);
- in part: [0019](0019-cost-engine-in-csharp.md) (the engine's language), [0020](0020-application-languages.md) (the backend half), [0021](0021-dotnet-engineering-foundation.md) (the toolchain; fully when the .NET code is removed), [0023](0023-microsoft-agent-framework.md) (the framework choice is reopened for a trial at stage 6), [0024](0024-dependency-updates.md) and [0026](0026-learning-first-engineering.md) (Dependabot's ecosystems and the learning map), [0025](0025-ai-platform-capabilities.md) (the Aspire app host is written in TypeScript; OpenTelemetry for Python), [0027](0027-stage-2-engineering-hardening.md) (CodeQL for Python, the PSF-2.0 licence, test tool names), [0029](0029-external-services.md) (live-service tests are excluded with a pytest marker), [0035](0035-ways-of-working-v2.md) point 9 (the pre-approved package lists), [0037](0037-mcp-server-and-agent-integrations.md) and [0038](0038-accounts-and-api-keys-for-mcp.md) (Proposed; the MCP server is written in Python), [0043](0043-specification-format.md) (the scenario runners and the browser driver), [0046](0046-public-area-check-first.md) ("a minimal ASP.NET Core API" becomes the FastAPI API from the template) and [0048](0048-frontend-foundation.md) (its package manager, TypeScript version, folder and browser-test lines).
- unchanged: [0032](0032-own-result-type.md)'s principle (expected failures return a `Result`; programming errors throw) and [0034](0034-rounding-boundary-cases.md) (the rounding boundary cases).

## Context
On 10 November 2026 decision 0042 moved the backend back to C# on .NET 11, because the founder then wanted to learn .NET and its new features. Since then the SDK moved to .NET 11 (#58) and the specification test project was built on it (#121); the C# cost engine, generator, validator and specification tests pass `make check` (mutation testing runs separately with `make mutate`), and port step P1 of the earlier Python plan (the uv workspace, PR #49, commit `4bbca27`) was removed by #57.

On 12 November 2026 the founder decided, in a prompt window (register WW-16): **"Switch to python"**. The reason: they now prefer to learn Python and FastAPI. The founder's own public FastAPI template (`house-template-fastapi`, v0.9.0, released 11 Nov 2026) already provides the API foundation, and their Next.js template (`house-template-nextjs`, v0.3.0) provides the frontend foundation. The founder answered every question for this record in prompt windows on 12 Nov 2026; their answers are quoted below as "founder, 12 Nov 2026".

Constraints: the rules in `AGENTS.md` don't change with the language (no invented facts, no hand-typed calculated figures, missing data never shown as zero); the fixtures, schemas, worked test cases and the shape of `costs.json` stay as they are; the public repository; stage 5 runs locally only (0048); the stage 3 gate (#71) is still open.

## Terms used here
- **uv:** installs Python and packages and runs commands, from one lock file. **ruff:** checks and formats Python code. **mypy:** checks types before the code runs. **pytest:** runs Python tests. **Hypothesis:** generates many test inputs automatically; *derandomised* means it uses a fixed seed, so every run is the same.
- **mutmut:** mutation testing: it changes the code on purpose and checks that a test fails each time.
- **`ast` architecture test:** a test that reads the engine's source code as a tree and fails if it uses a banned feature (for example floating-point numbers).
- **pytest-bdd** and **playwright-bdd:** tools that run the Gherkin scenarios in `docs/specs/` as tests, the first in Python, the second in a browser with Playwright.
- **SPDX:** the standard short names for licences (for example `MIT`). **AG-UI:** an open protocol for streaming an agent's replies to a web page.

## Options
### Option A: Python for the backend, final (chosen)
- **For:** the language the founder wants to learn; the founder's FastAPI template gives a working, strictly checked API foundation (settings, problem responses, logs, OpenTelemetry, health endpoints, security headers, authentication hook); the Python toolchain was already decided in detail (0039) and proven once (P1); one language covers the cost engine, the API, the MCP server and the AI layer.
- **Against:** the C# engine, generator, validator and specification tests must be ported, about 11 small pull requests (roughly 2 to 3 weeks of agent sessions, estimate given to the founder on 12 Nov 2026); Python checks less before running, so the safety must come from mypy strict, ruff, an `ast` architecture test and mutation testing (0039); a third change of direction in a week costs review time.

### Option B: stay on .NET 11 (0042)
- **For:** no port; the C# code and its checks are already green.
- **Against:** the founder no longer wants to learn .NET first. Not chosen.

## Recommendation
Option A, because the founder's learning goal decides the backend language (doc 04), and the cost is lowest now, before the API (stage 5b) or the app shell (#86) exists. The drafter recommended porting first, so that #86's browser tests never start in C#, and making this choice final (item 11f), so that a fourth change needs a written cost estimate first.

## Decision
Option A. The founder's answers (founder, 12 Nov 2026):

1. **Backend language: Python, final.** "Switch to python." The cost engine, generator, fixture validator, API, MCP server and AI layer are written in Python. The frontend stays TypeScript with Next.js and React (0020, 0048).
2. **API starting point:** a one-time, trimmed copy of `house-template-fastapi` (0040 option A), made at stage 5b (#93) from the template version current at the time of import (v0.9.0 today; the version used is recorded in #93's pull request). Vestagraph then owns its copy; there is no live `copier update` link.
3. **Timing: port first.** The port pull requests (below) run alongside the stage 3 gate (#71). #86 (the app shell) starts after the .NET code is removed (P8), so its browser tests are never written for .NET.
4. **Gherkin runner for the data scenarios: pytest-bdd** (9.0.1, 31 Oct 2026, MIT, maintained by pytest-dev; [PyPI](https://pypi.org/project/pytest-bdd/), [documentation](https://pytest-bdd.readthedocs.io/en/stable/)). Gherkin tags become **strict pytest markers** (a **marker** is a label on a test that pytest can filter on, for example `-m "not ui"`; [pytest markers](https://docs.pytest.org/en/stable/how-to/mark.html)), and `make test` runs `-m "not ui and not mcp and not withdrawn"`. Three things are proved in the spec-runner pull request (P6): the scenario ID appears in each test's name, `Rule:` blocks are handled, and feature files can live in `docs/specs/` outside the Python package. If one fails, the choice goes back to the founder (0043's fallback).
5. **Browser and accessibility tests: all in TypeScript** (the founder chose "Everything in TypeScript" over the drafter's recommended split, which kept browser steps in Python with Playwright for Python). The `@ui` scenarios in `docs/specs/` run with **playwright-bdd** (9.2.1, MIT; needs `@playwright/test` 1.44 or later) on `@playwright/test`, and axe runs through **`@axe-core/playwright`** (4.14, MPL-2.0), as the Next.js template already does. So the specifications run in **two runners, split by tag**: pytest-bdd runs every scenario except `@ui` (and `@mcp` and `@withdrawn` until they apply); playwright-bdd runs only `@ui`. 0043's scenario IDs, tags and wording don't change. This replaces Microsoft.Playwright for .NET (0043) and `Deque.AxeCore.Playwright` (0048). The founder's choice approves playwright-bdd; its transitive packages still pass the licence check when it is added.
6. **Python 3.14.** CodeQL lists Python up to 3.14 ([supported languages](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/)); 3.14 is a supported release ([Python versions](https://devguide.python.org/versions/)). The move to 3.15 is a register line once CodeQL lists it.
7. **Licences:** **PSF-2.0** (the Python Software Foundation licence, permissive) joins the 0027 allow-list, because `typing_extensions` uses it and FastAPI, Pydantic, `mcp`, mypy and pytest-bdd all need it; this replaces 0039 section 7's tool-only exception for it. **`libcst`** returns as a tool-only exemption (mutmut needs it; its metadata gives no single SPDX licence, 0039 section 6). Changing the allow-list is a founder merge.
8. **Money: 0039 section 3, unchanged.** `Pence` wraps an exact `int` within the signed 64-bit range; one `round_ratio` function rounds half away from zero; exact inputs are read as `Fraction` through `json.loads(parse_float=Fraction)`; no `decimal`, `float`, `round()`, `//`, `%`, `divmod` or `int()` outside `round_ratio`, enforced by the `ast` architecture test.
9. **AI framework: decided at stage 6 with a short trial.** Both paths are tried in the founder's template on the same task: Microsoft Agent Framework for Python (`agent-framework` 1.25.0, stable, MIT; `agent-framework-ag-ui` 1.8.0) and LangChain with LangGraph (`langgraph` 1.2.20, stable, MIT; `ag-ui-langgraph` 0.0.47, pre-1.0). They are compared on the AG-UI connection, tracing, evaluation and cost. This reopens 0023's choice (reaffirmed for MAF on 6 Nov 2026). Vestagraph's task interfaces stay framework-neutral, and no framework package is added before stage 6. Template v0.9.0 ships the LangChain/LangGraph gateway (it needs PostgreSQL); its MAF path is merged on the template's main branch (template PR #112) but not yet in a release.
10. **Aspire: the app host is written in TypeScript.** From stage 5b, local orchestration and telemetry use an Aspire app host in TypeScript (`apphost.mts`; generally available since Aspire 13.5, 18 Aug 2026, [what's new](https://aspire.dev/whats-new/aspire-13-5/)), which needs Node.js and Docker but no .NET SDK ([prerequisites](https://aspire.dev/get-started/prerequisites/)); the Python API runs through `addUvicornApp` with `withUv` ([Python integration](https://aspire.dev/integrations/frameworks/python/)). **Aspire** is Microsoft's tool that starts an app's pieces together on a developer's machine and shows their logs and traces in one dashboard. #94 stays the Aspire step at 5b, after #93. The Aspire CLI (MIT) and the npm packages a TypeScript app host needs are pre-approved; #94 names them and checks their licences. The CLI is installed by script, outside the lock files: #94 records its version in `third-party.md` and doesn't install it in `make check` or CI without founder approval. `make check` never needs Aspire. Fallback (a register line): the standalone Aspire dashboard container. Deploying with `aspire deploy` to Docker Compose is an option for IN-02 and IN-03 at 5b, not decided here; any experimental Aspire API is used only under the carried-over prerelease rule.
11. **Defaults, accepted as a set:**
    - (a) 0048 stays accepted; this record supersedes only the parts named under "Frontend" below.
    - (b) Mutation testing uses **mutmut** (0039), with a break score just below its first measured run; surviving mutants are explained in the mutation report (BE-26's principle); Hypothesis is derandomised during `make mutate` so the score is repeatable.
    - (c) The MCP library is the official **`mcp`** Python SDK (2.3.0, MIT), confirmed at #97.
    - (d) The template's AI gateway comes into Vestagraph by a second recorded import at stage 6, with item 9's trial.
    - (e) Stage 2 isn't reopened. A short re-check list runs in the .NET-removal pull request (P8): the mutation run, CodeQL for Python as a required check, and the port proof.
    - (f) **"Final":** any further change of backend language needs a new decision record with a written cost estimate before any code, and can't be decided in a prompt window alone.
    - (g) pytest runs with `--maxfail=5` (the run stops after 5 failures); CI keeps `timeout-minutes: 20`; there is no local 10-minute stop.

### Frontend: the Next.js template (amends 0048; founder, 12 Nov 2026)
**#86 starts from the founder's `house-template-nextjs`** (v0.3.0 today; the version used is recorded at import), as a one-time trimmed copy like 0040 option A, with backend "none" for stage 5 and the FastAPI connection switched on at 5b. Vestagraph **adopts the template's choices** where they differ from 0048:

| 0048 said | Now | Why |
|---|---|---|
| npm with `package-lock.json` | **pnpm 12** with `pnpm-lock.yaml` | the template's package manager |
| TypeScript 6.0 | **the template's TypeScript (5.9.x)** | the template's pin; moving up is a later register line |
| folder `apps/web` | **`frontend/`** | the template's layout |
| `Deque.AxeCore.Playwright` inside Reqnroll | **`@axe-core/playwright`** inside playwright-bdd | item 5 |
| Reqnroll with Microsoft.Playwright for .NET for `@ui` | **playwright-bdd** on `@playwright/test` | item 5 |
| `@ui` scenarios started by a .NET test project | started by Playwright's own `webServer` setting | item 5; settled in #86's plan |

The rest of 0048 stands: the App Router with server rendering run locally only, Tailwind CSS v4 on Vestagraph's `tokens.css` (swapped in for the template's), React Aria Components, ESLint 9 and Prettier, Vitest and Testing Library, fixture types from the JSON Schemas, size-limit with `@size-limit/file`, Lighthouse CI, code-first design, and "no backend before stage 5b". The template also brings Next.js 16.4 standalone output, security headers with a per-request CSP (`proxy.ts`), safe error pages, an `/api` proxy with `openapi-fetch` and `openapi-typescript`, `@vercel/otel`, a Dockerfile and `mk/nextjs.mk`, and Playwright tests in light, dark and phone sizes with screenshots taken in Playwright's Linux image. #86's plan lists what it keeps and what it trims; nothing that fetches or stores data is switched on before stage 5b.

### Carried over from 0042 (unchanged)
- The frontend stack: Next.js with React, the CopilotKit runtime route (open-source path only) for the agent chat, and TypeScript types generated from the API's OpenAPI document, never hand-written.
- The frontend pre-approved packages in 0042, and the rule that packages a later decision names become pre-approved once its record is accepted.
- The prerelease rule: prerelease or experimental packages only in the AI layer, behind Vestagraph's adapter (0029), pinned exactly, never on the path that produces a calculated figure; no alpha packages.
- A minor bump of a direct `0.x` dependency or action pin counts as major (from 0039 Q3; the live rule is in `AGENTS.md`).
- The licence gate that fails on packages with no detectable licence (BE-22).

### Pre-approved packages (amends 0035 point 9)
Each passes the 0027 allow-list (with PSF-2.0 added) and gets a `docs/references/third-party.md` entry in the pull request that adds it; exact versions live in the lock files. Versions below were read from PyPI and the npm registry on 12 Nov 2026, for reference.
- **Python tools (0039 section 6, adopted again):** uv (0.13.7 pinned at P1; 0.13.8 came out on 12 Nov 2026 and waits the 7 days 0027 sets), ruff 0.17.4, mypy 2.4.1, pytest 9.2.0, pytest-cov, coverage, Hypothesis 6.170.15, jsonschema 4.26.0 with referencing, mutmut 3.8.1, with the dependencies 0039 lists; plus **pytest-bdd** 9.0.1.
- **Python, stage 5b and later:** `mcp` (item 11c). **Not pre-approved:** FastAPI, Pydantic, import-linter and the template's other runtime packages; the founder approves them at #93, with licence checks, as 0040 says.
- **Frontend** (the founder adopted the template's choices): the packages `house-template-nextjs` v0.3.0 lists in `frontend/package.json`: `next`, `react`, `react-dom`, `@vercel/otel`, `@opentelemetry/api`, `@opentelemetry/api-logs`, `@opentelemetry/instrumentation`, `@opentelemetry/resources`, `@opentelemetry/sdk-logs`, `@opentelemetry/sdk-metrics`, `@opentelemetry/sdk-trace-base`, `openapi-fetch`, `server-only`, `@playwright/test`, `@axe-core/playwright`, `tailwindcss`, `@tailwindcss/turbopack` (the template's Tailwind route, in place of 0048's `@tailwindcss/postcss`), `@testing-library/react`, `@testing-library/jest-dom`, `@types/node`, `@types/react`, `@types/react-dom`, `@vitejs/plugin-react`, `eslint`, `eslint-config-next`, `jsdom`, `openapi-typescript`, `prettier`, `prettier-plugin-tailwindcss`, `typescript`, `vitest`; plus `playwright-bdd` and the 0048 packages that remain (React Aria Components, size-limit, `@size-limit/file`, `@lhci/cli`, `json-schema-to-typescript`). Several are `0.x` (`@opentelemetry/*-logs` and `instrumentation`, `openapi-fetch`, `server-only`, `prettier-plugin-tailwindcss`), so their minor bumps count as major.
- **Aspire:** the Aspire CLI and the npm packages of a TypeScript app host (named in #94).
- **Withdrawn when the .NET code is removed (P8):** the .NET packages in 0035 point 9, 0042 and 0043, and `Deque.AxeCore.Playwright` from 0048 (never added).

## How the earlier records change
| Record | What changes |
|---|---|
| [0019](0019-cost-engine-in-csharp.md) | The engine is written in Python; everything else (one engine, generated figures only) stands. |
| [0020](0020-application-languages.md) | Backend half: Python. Frontend half unchanged. |
| [0021](0021-dotnet-engineering-foundation.md) | Toolchain replaced by 0039's; fully superseded when the .NET code is removed (P8). |
| [0023](0023-microsoft-agent-framework.md) | Framework choice reopened for the stage 6 trial (item 9). |
| [0024](0024-dependency-updates.md), [0026](0026-learning-first-engineering.md) | Dependabot gains `uv` (and its `npm` ecosystem, which also covers a pnpm project, with #86) and loses NuGet at P8; the learning map covers Python and FastAPI. |
| [0025](0025-ai-platform-capabilities.md) | Aspire app host in TypeScript (item 10); OpenTelemetry through the Python packages the template uses. |
| [0027](0027-stage-2-engineering-hardening.md) | CodeQL adds Python (founder setting); PSF-2.0 allowed; test tools are pytest and mutmut. |
| [0029](0029-external-services.md) | Live-service tests are excluded with a pytest marker. |
| [0035](0035-ways-of-working-v2.md) point 9 | Gains the lists above; loses the .NET list at P8. |
| [0036](0036-python-backend.md), [0039](0039-python-engineering-foundation.md) | Adopted again, with: package names `vestagraph_*`; the API at stage 5b, not 6; the MCP library per item 11c; the spec runner and browser tools added; the licence change in item 7; the port order below. |
| [0037](0037-mcp-server-and-agent-integrations.md), [0038](0038-accounts-and-api-keys-for-mcp.md) | Proposed; the MCP server uses the `mcp` Python SDK, and token checks use the API's authentication hook from the template. |
| [0040](0040-fastapi-template-as-api-starting-point.md) | Adopted again, at stage 5b, recording the template version at import; its packages still need founder approval at #93. `AGENTS.md`'s exception for the founder's templates is active again and now also covers `house-template-nextjs`. |
| [0041](0041-maf-gateway-built-in-the-template.md) | Only as item 11d (a second recorded import at stage 6). |
| [0043](0043-specification-format.md) | Data scenarios run with pytest-bdd, `@ui` scenarios with playwright-bdd; IDs, tags and wording unchanged. |
| [0046](0046-public-area-check-first.md) | "A minimal ASP.NET Core API" becomes the FastAPI API from the template. |
| [0048](0048-frontend-foundation.md) | The table under "Frontend" above. |

**Register lines:** BE-01 becomes Accepted (Python with FastAPI); BE-04 is superseded when the .NET code is removed; BE-20, BE-21 (`uv_build` as the build backend) and BE-23 (no committed `uv export`: the 9 Nov 2026 proof showed dependency review reads `uv.lock` directly, although GitHub's [supported ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems) page doesn't list uv; P1 repeats the proof; *corrected 12 Nov 2026, the first version of this record said the export would be committed*)) are adopted again; BE-22 gets its PyPI exemptions back (`libcst` and Vestagraph's own packages; `typing-extensions` is now allowed by licence); WW-14 adds a `uv-zero-x` group; BE-25 is superseded; BE-26 is superseded by a mutmut line at P7; BE-07 to BE-09 and WW-13 (the C# validator, architecture-test and NUnit licence lines) lapse when P8 removes the .NET code. New lines: BE-29 (Python version), BE-30 (pytest run limits), SP-03 (two scenario runners split by tag), FE-09 (axe route), OP-04 (Aspire fallback), AI-09 (AI framework trial) and BE-31 (language-neutral `generatedBy`).

## The port plan
One pull request each, in this order; each has an issue in the "Python port" milestone and a row in [`docs/planning/backlog.md`](../planning/backlog.md).
- **PC: language-neutral contract.** The generator's `generatedBy` value no longer names a language or package, so the port changes no byte of `costs.json`; a **port ledger** (`docs/planning/python-port-ledger.md`) lists every C# test and worked case and the Python test that covers it.
- **P0: this record.**
- **P1: Python foundation** (founder merge). The uv workspace from commit `4bbca27`, renamed to `vestagraph-*`; Python steps beside .NET in each Makefile target; `setup-uv` in CI (pinned by SHA); Dependabot `uv`; dependency-review PyPI exemptions; `.claude/settings.json` rules; the founder adds Python to CodeQL's default setup.
- **P2: engine basics** (test first): `Pence`, `round_ratio`, annual to monthly, `Result`, the architecture test, every 0034 case.
- **P3a: monthly and mortgage costs. P3b: upfront costs and the builder.**
- **P4: generator**, with the port proof: the regenerated `costs.json` is byte-identical.
- **P5: validator and fixture tests.**
- **P6: spec runner** (pytest-bdd, item 4's three proofs).
- **P7: mutation testing** (mutmut; BE-26's replacement line).
- **P8: remove .NET** (founder merge), only when the port ledger shows every C# test and worked case covered; runs item 11e's re-check list.

Then #86 (from the Next.js template, with the `@ui` harness in playwright-bdd), and at stage 5b #93 (the FastAPI template import), #94 (the Aspire app host in TypeScript) and #95 (TypeScript types from OpenAPI).

## Consequences
- **Until each port pull request merges, the C# code keeps running and the documents that describe it (`AGENTS.md` "Commands", the README, `third-party.md`, `docs/specs/README.md`, the architecture page's built pieces) keep describing it.** Each port pull request updates them for what it changes; P8 removes the last .NET references.
- **Issues:** #59 and #60 (C# 15) and #61 (.NET Skills) close as not planned. #93 becomes the FastAPI API from the template; #94 the Aspire app host in TypeScript; #92 narrows to BE-02 (the API contract); #97 becomes the MCP server in Python; #101 and #102 follow item 9's trial; #96 waits for P8. The backlog's stage 6 heading no longer names .NET 11.
- **The [.NET 11 and C# 15 plan](../planning/dotnet-11-and-csharp-15-plan.md)** is superseded and kept only because accepted records link to it.
- **Founder-only steps:** merging this record (it changes the licence allow-list), P1 and P8; adding Python to CodeQL's default setup; installing the Aspire CLI in CI if ever wanted.
- **Revisit if:** a pytest-bdd proof fails (P6, back to the founder); the port proof finds a figure that moves (stop and report; the engine is fixed, never the expectations); CodeQL drops Python 3.14 support before 3.15 is listed. A further change of language follows item 11f.

## Not verified
- That pytest-bdd puts the scenario ID in test names, handles `Rule:` blocks and reads feature files from `docs/specs/` (P6 proves them).
- That playwright-bdd's tag filtering and `@axe-core/playwright` run together with the template's light, dark and phone projects (#86 proves it).
- The template's exact package list and TypeScript patch version (recorded at import in #86 and #93).
