# Status

Overwritten at the end of every session (decision 0050). Last updated: **12 Nov 2026**.

## Where we are
- **Stage 3** (prototype specification) is open; its gate is issue #71. Stage 4's frontend foundation is decided: [0048](../decisions/0048-frontend-foundation.md), amended by [0049](../decisions/0049-back-to-python-final.md) (the frontend starts from the founder's Next.js template).
- **Backend: Python, final** ([0049](../decisions/0049-back-to-python-final.md)). The port is complete and .NET is gone: every C# test and worked case has a Python counterpart ([port ledger](python-port-ledger.md)), and `costs.json` stayed byte-identical throughout.
- **Checks:** `make check` runs Python only (mypy, ruff, the generated-file check, the fixture validator, pytest with the pytest-bdd specifications). `make mutate` runs mutmut by hand (break score 85, BE-33). CodeQL scans `actions` and `python`.
- **Process:** agent-workflows (Superpowers) is the process from decision [0050](../decisions/0050-agent-workflows-process.md).
- Design canvas and new ideas are frozen until something is clickable (founder, 11 Nov 2026).

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
1. **The stage 3 gate (#71).**
2. **#86, the app shell**, built from the founder's Next.js template (pnpm, TypeScript 5.9, `frontend/`, `@ui` scenarios with playwright-bdd and `@axe-core/playwright`). Then screens #165–#175, and #96 (home-to-home differences, now in Python).

## Blockers
- None.

## Founder to-dos
Domains `vestagraph.com` and `vestagraph.co.uk` were bought on 12 Nov 2026 (register line IN-06); turn on DNSSEC for both in Cloudflare when convenient.

| To-do | Why | How | When |
|---|---|---|---|
| Approve the two documentation MCP servers (Microsoft Learn, Context7) | Agents read current official documentation instead of memory (WW-15) | Accept them when Claude Code asks at the start of an interactive session in this project | Next session |
| Check the OpenAI image policy | Carried over from earlier sessions: any AI-made image used on the public site must be allowed by the provider's terms | Read OpenAI's current usage and image terms; tell the agent what you find so it is recorded | Before stage 5b |
| Trade-mark clearance for "Vestagraph" | The public name (0044, PD-09) must be safe to use | A UK IPO search, or a professional clearance; PD-09 stays Open until done | Before the public area check (stage 5b) |
| Narrow the sharing of the design-canvas link | The prototype is a private reference (0045) | In claude.ai, set the canvas artifact's sharing to only the people who need it | Any time |
| Optional: decide on `types-jsonschema` | Typing information for the validator's `jsonschema` imports, so two `# type: ignore` lines can go | Say yes or no; it is dev-only, free, Apache-2.0, not on the approved list | Any time (recommended after P8, which is done) |

## Open `noticed` issues
#33, #115, #151, #159, #184, #197 (no record states the divide-by-12 rule), #207 (validators accept duplicate JSON keys), #212 (C# wording left in Python docstrings). #202 and #210 closed with P8.
