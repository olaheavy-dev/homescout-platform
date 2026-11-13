# Ordered backlog

**Written:** 10 Nov 2026 with decision 0042; reordered 12 Nov 2026 by decision [0049](../decisions/0049-back-to-python-final.md) (back to Python, final). Each item is a GitHub issue whose title starts with its order number (for example `[08]`) and which sits in its stage's milestone (or the Python port milestone). Work goes in this order unless an item says it can run alongside another. Stages 3 and 4 may overlap (decision 0035), so the design research (08 to 10) can start once the stage 2 gate passes, alongside stage 3.

Each stage starts with its decisions and ends with its gate (doc 04 §9). Items marked **epic** are split into issues when their stage starts. When an issue's plan changes, update the issue, not this list; this list only changes when the order does.

## Stage 2: close-out and back to .NET 11
| # | Issue | Item | Notes |
|---|---|---|---|
| 01 | #56 | Decision 0042, the .NET 11 plan and this backlog | Documentation |
| 02 | #57 | Remove the Python tooling | Founder merge |
| 03 | #24 | Stage 2 close-out: doc corrections, C4 diagrams, Stryker.NET report, audit, gate | Can pass on .NET 11 (C# 14) |
| 04 | #58 | Upgrade to .NET 11 (SDK and runtime; language stays C# 14) | SDK and runtime now, C# 14 |

## Python port (decision 0049)
Milestone "Python port (decision 0049)". Runs alongside the stage 3 gate (#71); #86 starts after P8. The port ledger (from PC) shows which C# test each Python test replaces.

| # | Issue | Item | Notes |
|---|---|---|---|
| PC | #186 | Language-neutral `generatedBy` and the port ledger | Before any Python |
| P0 | — | Decision 0049 | This pull request |
| P1 | #187 | Python foundation (uv workspace beside .NET) | Founder merge |
| P2 | #188 | Engine basics: `Pence`, `round_ratio`, `Result`, architecture test | Test first |
| P3a | #189 | Monthly and mortgage costs | Test first |
| P3b | #190 | Upfront costs and the builder | Test first |
| P4 | #191 | Generator with the port proof (byte-identical `costs.json`) | |
| P5 | #192 | Fixture validator and fixture tests | |
| P6 | #193 | pytest-bdd spec runner for the data scenarios | Three proofs; back to the founder if one fails |
| P7 | #194 | Mutation testing with mutmut | Replaces BE-26 |
| P8 | #195 | Remove .NET | Founder merge; only when the ledger is complete |

## C# 15 (closed by decision 0049)
#59, #60 and #61 (rows 05 to 07) close as not planned: decision 0049 moved the backend to Python.

## Design research (stage 4 milestone; starts after the stage 2 gate, alongside stage 3)
| # | Issue | Item |
|---|---|---|
| 08 | #62 | Design study of related home buying and renting products |
| 09 | #63 | Design patterns from outside the property category |
| 10 | #64 | Research synthesis: design principles and pattern choices |

## Stage 3: prototype specification
| # | Issue | Item |
|---|---|---|
| 11 | #65 | Decision: specification format (SP-01) and work breakdown (SP-02) |
| 11a | #121 | Run the Gherkin specs with Reqnroll; prove .NET 11, NUnit 5 and MTP support |
| 12 | #66 | Design brief (grill-me, design-brief) |
| 13 | #67 | Information architecture |
| 13a | #120 | Synthetic area context fixtures (schools, transport, shops, flood, police…) for the Nearby screen |
| 14 | #68 | Screen-by-screen specification |
| 14a | #117 | MCP tool surface for AI assistants (decision 0037) |
| 15 | #69 | Buyer story script |
| 16 | #70 | Renter story script |
| 17 | #71 | Brief to stage 5 issues; stage 3 gate |

## Stage 4: design, frontend and infrastructure
| # | Issue | Item |
|---|---|---|
| 18 | #72 | Decision: design tooling (DS-01) and design system foundation (DS-02) |
| 19 | #73 | Decision: frontend framework details and rendering (FE-01) |
| 20 | #74 | Decision: styling and components (FE-02) |
| 21 | #75 | Decision: maps and charts (FE-03) |
| 22 | #76 | Decision: frontend practices (FE-04) |
| 23 | #77 | Low-fidelity wireframes for both stories |
| 24 | #78 | Agent chat and approval experience (designed now, built at stage 6) |
| 25 | #79 | High-fidelity key screens |
| 26 | #80 | Image pass |
| 30 | #84 | Stage 4 gate and audit |

## Stage 5: clickable prototype

#86 may start once the pilot gate passes (decision 0052; earlier, the full stage 3 gate #71) and the .NET code is removed (P8, decision 0049), before the stage 4 gate (#84), and runs locally only until stage 5b. It starts from the founder's Next.js template in `frontend/`, with its `@ui` scenarios in playwright-bdd (0049); the rest of stage 5 waits for #84 (decision 0048). Stage 5 is never deployed: #81 to #83 (IN-01 to IN-05) moved to stage 5b, rows 38b.1 to 38b.3. Rows 18, 19, 20 and 22 are answered by 0048.

| # | Issue | Item |
|---|---|---|
| 32 | #86 | App shell, navigation, design system, fixture loading |
| 32b | #150 | Component gallery (decision 0045) |
| 32c | to open | Area screens on fixtures: summary-first Nearby, map with 3D switch, Check an area (decision 0046, TASKS B6, B6a, B7) |
| 32a | #96 | Home-to-home cost differences in the engine and `costs.json` (BE-27), after P8 in Python |
| 33 | #87 | **Epic:** buyer story end to end (split into one ticket per story step at #71, SP-02) |
| 34 | #88 | **Epic:** renter story end to end (split into one ticket per story step at #71, SP-02) |
| 35 | #89 | Edge states, mobile, accessibility (WCAG 2.2 AA) |
| 36 | #90 | Labelling, simulated-action audit; stage 5 gate on the private prototype (decision 0045) |

## Stage 5b: public area check (decision 0046)
Decisions first, then the API and the area adapters, then the public site. Items moved here from stage 5 and stage 6 keep their numbers.
| # | Issue | Item |
|---|---|---|
| 31 | #85 | Decision: privacy parts 1 and 2 (SE-02, decision 0014), analytics and feedback (FE-05) |
| 38 | #92 | Decision: API architecture and contract (BE-02; BE-01 is decided by 0049: FastAPI); rules versioning (BE-03) stays at stage 6, before the cost engine expansion |
| 38a | to open | Decisions: database and geospatial, ingestion and caching, source licences, postcode lookup (DA-03 to DA-06, postcode only); DA-08, the walking-time routing engine for wave 2 (13 Nov 2026) |
| 38b | — | Hosting for the public area check: rows 38b.1 to 38b.3 below, decided once (0048). #81's IN-02 becomes public hosting for 0046, and #82 adds the domain and secrets |
| 38b.1 | #81 | Decision: prototype architecture, hosting, infrastructure as code (IN-01 to IN-03) |
| 38b.2 | #82 | Decision: CI/CD and environments (IN-04) |
| 38b.3 | #83 | Decision: budget cap and cost alerts (IN-05) |
| 39 | #93 | FastAPI API skeleton from a one-time copy of the founder's template (decisions 0040, 0049; one area endpoint; the first cost endpoint waits for stage 6) |
| 40 | #94 | Aspire app host in TypeScript and OpenTelemetry (decision 0049) |
| 41 | #95 | Generated TypeScript types from the OpenAPI document |
| 44.1 | #126 | Foundation: data import pattern, source adapter, postcode-to-area lookup |
| 44.3 | #128 | Transport stops nearby (NaPTAN) |
| 44.4 | #129 | Schools nearby (DfE register) |
| 44.5 | #130 | Crime counts and neighbourhood police team (data.police.uk) |
| 44.6 | #131 | Flood: live warnings and river levels, plus a link to long-term risk (EA) |
| 44.7 | #132 | Nearby sold prices (HM Land Registry) |
| 44.8 | #133 | Shops, supermarkets, parks, pharmacies, police stations, hospitals, GPs, dentists (OSM extract) |
| 44.10 | #135 | School inspection results (Ofsted) |
| 44.11 | #136 | Broadband and mobile coverage (Ofcom) |
| 44.14 | #139 | Planning applications nearby |
| 38e | to open | Pilot AI (decision 0051): the AI-09 framework trial, then the model provider (AI-01) and orchestration (AI-04) |
| 38f | to open | Pilot AI evaluation set (AI-03): questions the area chat and tools must answer or refuse |
| 38g | to open | Area tools package shared by the API, the public MCP server and the area chat |
| 38h | to open | Public read-only MCP server for the area tools (no key; global and per-host caps; spec `docs/specs/pilot/area-tools.feature`), then the area card widget (FE-15 to FE-19, `area-card.feature`) |
| 38i | to open | On-page area chat with the disclaimer, daily AI cap, bot check and "paused" and "unavailable" states (spec `docs/specs/pilot/area-chat.feature`); the isometric area card component (FE-14 to FE-19, `area-card.feature`) |
| 38j | to open | Pilot features: Explain this, Share a link, Recent postcodes (opt-in), Report a problem; questions to ask; go-check-in-person list |
| 38k | to open | Pilot extras, wave 2 (pilot design, Goals 5): planning applications nearby, school inspection results with school demand (DfE applications and offers), air quality, compare two postcodes; walking times and timetabled buses per hour (needs DA-08); council tax by band (a tax table, so a founder merge); a family view. Each behind its own switch (research `docs/reviews/2026-11-13-chatgpt-ideas-research.md`) |
| 38c | to open | Public site: landing (search first), How it works, About the data, privacy notice, accessibility statement (TASKS P1 to P4) |
| 38d | to open | Stage 5b gate: sources on every fact, no searched postcode in any log, privacy notice and budget cap live, accessibility checks pass; AI caps, rate limits and bot check live; the evaluation set passes (decision 0051) |

## Stage 6: the real product
| # | Issue | Item |
|---|---|---|
| 37 | #91 | Validation study (six buyers, six renters) |
| 43 | #97 | MCP server with the official `mcp` Python SDK (read-only, local first); its public area tools come first at 5b (row 38h, decision 0051) |
| 44 | #98 | **Epic:** real England data, per-home parts (area sources moved to stage 5b by decision 0046) |
| 44.2 | #127 | Exact-home address search and matching (DA-06), needed for per-home data only |
| 44.9 | #134 | Energy rating and energy cost range (energy certificate register) |
| 44.12 | #137 | Mortgage context: Bank Rate |
| 44.13 | #138 | Commute time to your own destinations (routing, DA-06) |
| 44.15 | #140 | Leasehold: managing agent or freeholder status (Companies House) |
| 44.16 | #141 | Bus timetables (Bus Open Data Service) |
| 44.17 | #142 | Deferred: NHS services, air quality, rail and TfL, radon |
| 45 | #99 | **Epic:** accounts, households and the questions workflow |
| 46 | #100 | AI evaluation harness and model provider choice (AI-03, AI-01) |
| 47 | #101 | AI gateway: short trial of Agent Framework and LangGraph in the founder's template, then a second recorded import (decision 0049, AI-09); the trial now runs at 5b (row 38e, decision 0051), and this row keeps the gateway import |
| 48 | #102 | Agent chat over AG-UI (CopilotKit), on the framework AI-09 chooses; the pilot's area chat comes first at 5b (row 38i, decision 0051), and this row is the home chat |
| 49 | #103 | Document investigation workflow with human approval |
| 50 | #104 | **Epic:** entitlements and payments (CO-01) |
| 51 | #105 | **Epic:** monitoring, scheduling and notifications (OP-01, OP-02) |

## Not in the order
`noticed` issues are triaged at each stage gate (decision 0035). Status on 11 Nov 2026:
- #33: scheduled in stage 6.
- #115: folded into #70 (renter story script).
- #37: fixed by #119.
- #111 (Stryker's `mtp` runner ignores `test-projects`): closed by the stage 2 audit tidy-up pull request.
- #107 (repeatable mutation runs): done (pull request #112).
- #34 and #114: recommended to close; the founder to confirm.
- Item 42 (#96) moved to 32a: the founder pulled home-to-home differences into stage 5 on 11 Nov 2026 so they exist before the compare screens.
