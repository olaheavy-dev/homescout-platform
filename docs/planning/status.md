# Status

Overwritten at the end of every session (decision 0050). Last updated: **12 Nov 2026**.

## Where we are
- **Stage 3** (prototype specification) is open; its gate is issue #71. Stage 4's frontend foundation is decided: [0048](../decisions/0048-frontend-foundation.md), amended by [0049](../decisions/0049-back-to-python-final.md) (the frontend starts from the founder's Next.js template).
- **Backend: Python, final** ([0049](../decisions/0049-back-to-python-final.md), founder, 12 Nov 2026). The port finished on 12 Nov 2026: PC #186, P1 #187, P2 #188, P3a #189, P3b #190, P4 #191, P5 #192, P6 #193, P7 #194 merged; P8 #195 removes .NET (this file is updated in that pull request). Every C# test and worked case has a Python counterpart ([port ledger](python-port-ledger.md)); `costs.json` is byte-identical.
- **Checks:** `make check` runs Python only (mypy, ruff, the generated-file check, the fixture validator, pytest with the pytest-bdd specifications); `make mutate` runs mutmut (break score 85, BE-33). CodeQL scans `actions` and `python`.
- **Process:** agent-workflows (Superpowers) is the process from decision [0050](../decisions/0050-agent-workflows-process.md).
- Design canvas and new ideas are frozen until something is clickable (founder, 11 Nov 2026).

## Open pull requests
- P8, remove .NET (branch `chore/remove-dotnet`, #195). **Founder merge** (CI, Dependabot, `.claude/settings.json`, licence exemptions).

## Next, in order
1. Founder merges P8. Then close the milestone "Python port (decision 0049)".
2. The stage 3 gate (#71).
3. #86, the app shell, built from the founder's Next.js template (pnpm, TypeScript 5.9, `frontend/`, `@ui` scenarios with playwright-bdd and `@axe-core/playwright`); then screens #165–#175 and #96 (home-to-home differences, in Python).

## Blockers
- None.

## Founder to-dos
- Merge the P8 pull request.
- Approve the two documentation MCP servers (Microsoft Learn, Context7) when Claude Code asks at the start of a session.
- Check the OpenAI image policy before stage 5b.
- Trade-mark clearance for "Vestagraph".
- Narrow the sharing of the design-canvas link.
- Optional: decide on `types-jsonschema` (typing stubs for the validator, Apache-2.0, dev only; recommended after P8, not yet approved).

## Open `noticed` issues
#33, #115, #151, #159, #184, #197 (no record states the divide-by-12 rule), #207 (validators accept duplicate JSON keys), #212 (C# wording left in Python docstrings). #202 and #210 close with P8.
