# Status

Overwritten at the end of every session (decision 0050). Last updated: **13 Nov 2026**.

## Where we are
- **Stage 3** (prototype specification) is open; its gate is issue #71. Stage 4's frontend foundation is decided: [0048](../decisions/0048-frontend-foundation.md), amended by [0049](../decisions/0049-back-to-python-final.md) (the frontend starts from the founder's Next.js template).
- **Backend: Python, final** ([0049](../decisions/0049-back-to-python-final.md)). The port is complete and .NET is gone: every C# test and worked case has a Python counterpart ([port ledger](python-port-ledger.md)), and `costs.json` stayed byte-identical throughout.
- **Checks:** `make check` runs Python only (mypy, ruff, the generated-file check, the fixture validator, pytest with the pytest-bdd specifications). `make mutate` runs mutmut by hand (break score 85, BE-33). CodeQL scans `actions` and `python`.
- **Process:** agent-workflows (Superpowers) is the process from decision [0050](../decisions/0050-agent-workflows-process.md).
- Design canvas: the 11 Nov freeze was lifted fully by the founder on 13 Nov 2026; the illustrations were redrawn in the isometric style (FE-10, canvas versions 65 and 66; the founder, before the hero was redone: "CAN YOU NOT CHECK THE CANVAS YOURSELF, IT LOOKS VERY GOOD TO ME"), and the landing hero's Northbridge sample map with recognisable buildings (version 70; the founder: "The new hero map is okay"). The brand mark Lit doorway D1 · Ruled light replaced Contour home on every board, with a D1 brand sheet, the mark beside every wordmark and a warm clay hearth in dark mode (versions 71 and 72; founder's answers "Add the mark (Recommended)", "Keep photos alongside (Recommended)", "Warm clay (Recommended)"). The data maps are being restyled isometric (founder: "restyle the data maps too").

## Done on 13 Nov 2026
| Pull request | What merged |
|---|---|
| #215 | The Vestagraph domains (register line IN-06) |
| #217 | #68 part 1: area screen specifications (Landing, Nearby, Check an area); closes #67 |
| #218 | Isometric illustration style (FE-10), canvas freeze lifted, image terms and trade-mark search recorded |

## Done on 12 Nov 2026
| Pull request | What merged |
|---|---|
| #196 | Decision 0049: back to Python (final); frontend from the founder's Next.js template |
| #198 | PC: language-neutral `generatedBy` in `costs.json` (BE-31); the port ledger |
| #201 | P1: Python tooling beside .NET (uv, mypy, ruff, pytest, CI, Dependabot, licence gate) |
| #203 | P2: engine basics (`Pence`, `round_ratio`, `Result`, architecture test; BE-32) |
| #204 | P3a: monthly costs and mortgage repayment |
| #205 | P3b: upfront cash, assumption selector, builder |
| #206 | P4: Python generator; `make generate` switched; byte-identical `costs.json` |
| #208 | P5: Python fixture validator and fixture tests; `make validate` switched |
| #209 | P6: pytest-bdd spec runner for the data scenarios (SP-03) |
| #211 | P7: mutation testing with mutmut (BE-33, supersedes BE-26) |
| #213 | P8: .NET removed; Python only |

Repository settings changed with the founder's approval: Python added to CodeQL's default setup, and `csharp` removed before P8 merged; the leftover proof branches from 9 Nov and 12 Nov deleted.

**Founder decisions on 12 Nov 2026** (each asked in a prompt window and recorded where shown):
- Back to Python, final, with the answers in [0049](../decisions/0049-back-to-python-final.md).
- Merges: 0049 ("merge it"), P1 ("start it and you can merge it"), P8 ("you can merge it once it is green"); the other port pull requests under the standing merge approval, each after Codex was clean.
- P6: keep the renaming helper so scenario IDs such as `COSTS-02` appear in test names (register line SP-03).
- P7: break score 85, just below the final run, rather than 84 from 0049's wording (register line BE-33).
- P8: remove `csharp` from CodeQL before the pull request, so no C# scan fails on it.

**Correction recorded:** 0049 first said a `uv export` file would be committed; the founder's 9 Nov proof (BE-23) showed dependency review reads `uv.lock` directly, so no export is committed. Re-proved on 12 Nov (PRs #199, #200).

## Open pull requests
- None.

## Next, in order
On 13 Nov 2026 the founder put the pilot first (decisions 0051 and 0052); the design canvas has a "Pilot · public area check" page for reviewing it.
1. **The pilot's specifications first** (founder, 13 Nov 2026: "Pilot specs first (Recommended)"; design `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`, decision 0051): the area chat panel, the ChatGPT and Claude area tools with the isometric area card, the wave 1 and wave 2 extras, Explain this, Share a link, Recent postcodes, Report a problem, the public pages (How it works, About the data, privacy notice, accessibility statement), the printout update and the AI evaluation set. Each as a screen specification, with a canvas board where it is a screen.
2. **The pilot gate, then the pilot's development tickets** (decision 0052, founder, 13 Nov 2026: "Pilot-only gate (Recommended)"): the gate checks only the pilot's specifications; then one ticket per buildable slice, starting with the stage 5b decisions (0046) and the app shell (#86).
3. **Later, before the home workspace: #68, the remaining screen specifications** (paused after part 1; the resume point is on #68), in three pull requests in the stage 5 build order (decision 0046; design `docs/superpowers/specs/2026-11-13-screen-specs-design.md`): the area screens merged as #217 (13 Nov 2026, closing #67); next, home and money (identity confirmation, home overview, costs, compare, what changed), then questions and sharing.
4. **#69 and #70, the buyer and renter story scripts.**
5. **The full stage 3 gate (#71).**
6. **The home workspace build:** after the app shell (#86), built from the founder's Next.js template (pnpm, TypeScript 5.9, `frontend/`, `@ui` scenarios with playwright-bdd and `@axe-core/playwright`). Then screens #165–#175, and #96 (home-to-home differences, now in Python).

## Blockers
- None.

## Founder to-dos
Domains `vestagraph.com` and `vestagraph.co.uk` were bought on 12 Nov 2026 (register line IN-06); DNSSEC is on for both (13 Nov 2026).

| To-do | Why | How | When |
|---|---|---|---|
| Approve the two documentation MCP servers (Microsoft Learn, Context7) | Agents read current official documentation instead of memory (WW-15) | Accept them when Claude Code asks at the start of an interactive session in this project | Next session |
| Finish the trade-mark clearance (PD-09) | Your name search was clean, and you kept the new logo (Lit doorway, D1) after its UK screen: "i think it is unique enough" (13 Nov 2026); still open: which register and classes the name search covered, EUIPO and WIPO for the name and the logo, the logo's international registrations that have no pictures on the IPO site, a light-rays picture code, and a fresh Companies House check (decision 0044) | Finish those checks (or ask an attorney about UK00004266938), then accept PD-09 | Before the public area check (stage 5b) |
| Narrow the sharing of the design-canvas link | The prototype is a private reference (0045) | In claude.ai, set the canvas artifact's sharing to only the people who need it | Any time |
| Set the pilot's budget caps (IN-05) | The pilot has running costs and an on-page AI chat (decision 0051); a monthly cap and a daily AI cap must be set before launch | Decide the two amounts in pounds when the agent asks at stage 5b | Before the pilot launches |
| Optional: decide on `types-jsonschema` | Typing information for the validator's `jsonschema` imports, so two `# type: ignore` lines can go | Say yes or no; it is dev-only, free, Apache-2.0, not on the approved list | Any time (recommended after P8, which is done) |

## Open `noticed` issues
#33, #115, #151, #159, #184, #197 (no record states the divide-by-12 rule), #207 (validators accept duplicate JSON keys), #212 (C# wording left in Python docstrings). #202 and #210 closed with P8.
