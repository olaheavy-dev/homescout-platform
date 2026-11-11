# Ordered backlog

**Written:** 10 Nov 2026 with decision [0042](../decisions/0042-back-to-dotnet-11.md) and the [.NET 11 and C# 15 plan](dotnet-11-and-csharp-15-plan.md). Each item is a GitHub issue whose title starts with its order number (for example `[08]`) and which sits in its stage's milestone (or the C# 15 milestone). Work goes in this order unless an item says it can run alongside another. Stages 3 and 4 may overlap (decision 0035), so the design research (08 to 10) can start once the stage 2 gate passes, alongside stage 3.

Each stage starts with its decisions and ends with its gate (doc 04 §9). Items marked **epic** are split into issues when their stage starts. When an issue's plan changes, update the issue, not this list; this list only changes when the order does.

## Stage 2: close-out and back to .NET 11
| # | Issue | Item | Notes |
|---|---|---|---|
| 01 | #56 | Decision 0042, the .NET 11 plan and this backlog | Documentation |
| 02 | #57 | Remove the Python tooling | Founder merge |
| 03 | #24 | Stage 2 close-out: doc corrections, C4 diagrams, Stryker.NET report, audit, gate | Can pass on .NET 11 (C# 14) |
| 04 | #58 | Upgrade to .NET 11 (SDK and runtime; language stays C# 14) | SDK and runtime now, C# 14 |

## C# 15 (waits for CodeQL support)
Milestone "C# 15 (waits for CodeQL support)". These start once CodeQL supports C# 15 (#59); #61 is low priority and not tied to CodeQL.

| # | Issue | Item | Notes |
|---|---|---|---|
| 05 | #59 | Closed hierarchies for `LineInput` and `EvidenceValue` | First C# 15 change. **Blocked** until CodeQL and Stryker.NET support C# 15 (#59, #60; BE-25) |
| 06 | #60 | Spike: `Result` as a C# 15 union | Outcome is a register line. **Blocked** until CodeQL supports C# 15 |
| 07 | #61 | Evaluate .NET Skills for the coding agents | Low priority |

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
| 12 | #66 | Design brief (grill-me, design-brief) |
| 13 | #67 | Information architecture |
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
| 27 | #81 | Decision: prototype architecture, hosting, infrastructure as code (IN-01 to IN-03) |
| 28 | #82 | Decision: CI/CD and environments (IN-04) |
| 29 | #83 | Decision: budget cap and cost alerts (IN-05) |
| 30 | #84 | Stage 4 gate and audit |

## Stage 5: clickable prototype
| # | Issue | Item |
|---|---|---|
| 31 | #85 | Decision: visitor privacy (SE-02 part 1), demo analytics and feedback (FE-05) |
| 32 | #86 | App shell, navigation, design system, fixture loading |
| 32a | #96 | Home-to-home cost differences in the engine and `costs.json` (BE-27) |
| 33 | #87 | Buyer story end to end |
| 34 | #88 | Renter story end to end |
| 35 | #89 | Edge states, mobile, accessibility (WCAG 2.2 AA) |
| 36 | #90 | Labelling, simulated-action audit, public launch; stage 5 gate |

## Stage 6: the real product on .NET 11
| # | Issue | Item |
|---|---|---|
| 37 | #91 | Validation study (six buyers, six renters) |
| 38 | #92 | Decision: API framework (BE-01), architecture and contract (BE-02), rules versioning (BE-03) |
| 39 | #93 | ASP.NET Core 11 API skeleton (OpenAPI 3.2, async validation, one cost endpoint) |
| 40 | #94 | Aspire app host and OpenTelemetry |
| 41 | #95 | Generated TypeScript types from the OpenAPI document |
| 43 | #97 | MCP server with the official C# SDK (read-only, local first) |
| 44 | #98 | **Epic:** real England data (DA-03 to DA-06, SE-02 part 2) |
| 44.1 | #126 | Foundation: data import pattern, source adapter, postcode-to-area lookup |
| 44.2 | #127 | Exact-home address search and matching (DA-06), needed for per-home data only |
| 44.3 | #128 | Transport stops nearby (NaPTAN) |
| 44.4 | #129 | Schools nearby (DfE register) |
| 44.5 | #130 | Crime counts and neighbourhood police team (data.police.uk) |
| 44.6 | #131 | Flood: live warnings and river levels, plus a link to long-term risk (EA) |
| 44.7 | #132 | Nearby sold prices (HM Land Registry) |
| 44.8 | #133 | Shops, supermarkets, parks, pharmacies, police stations, hospitals, GPs, dentists (OSM extract) |
| 44.9 | #134 | Energy rating and energy cost range (energy certificate register) |
| 44.10 | #135 | School inspection results (Ofsted) |
| 44.11 | #136 | Broadband and mobile coverage (Ofcom) |
| 44.12 | #137 | Mortgage context: Bank Rate |
| 44.13 | #138 | Commute time to your own destinations (routing, DA-06) |
| 44.14 | #139 | Planning applications nearby |
| 44.15 | #140 | Leasehold: managing agent or freeholder status (Companies House) |
| 44.16 | #141 | Bus timetables (Bus Open Data Service) |
| 44.17 | #142 | Deferred: NHS services, air quality, rail and TfL, radon |
| 45 | #99 | **Epic:** accounts, households and the questions workflow |
| 46 | #100 | AI evaluation harness and model provider choice (AI-03, AI-01) |
| 47 | #101 | Agent Framework gateway in .NET |
| 48 | #102 | Agent chat over AG-UI (CopilotKit and `MapAGUIServer`) |
| 49 | #103 | Document investigation workflow with human approval |
| 50 | #104 | **Epic:** entitlements and payments (CO-01) |
| 51 | #105 | **Epic:** monitoring, scheduling and notifications (OP-01, OP-02) |

## Not in the order
`noticed` issues are triaged at each stage gate (decision 0035). Status on 11 Nov 2026:
- #33: scheduled in stage 6.
- #115: folded into #70 (renter story script).
- #37: being fixed in its own pull request.
- #111 (Stryker's `mtp` runner ignores `test-projects`): closed by the stage 2 audit tidy-up pull request.
- #107 (repeatable mutation runs): done (pull request #112).
- #34 and #114: recommended to close; the founder to confirm.
- Item 42 (#96) moved to 32a: the founder pulled home-to-home differences into stage 5 on 11 Nov 2026 so they exist before the compare screens.
