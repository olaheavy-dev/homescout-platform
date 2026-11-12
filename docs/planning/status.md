# Status

Overwritten at the end of every session (decision 0050). Last updated: **12 Nov 2026**.

## Where we are
- **Stage 3** (prototype specification) is open; its gate is issue #71. Stage 4's frontend foundation is decided: [0048](../decisions/0048-frontend-foundation.md), accepted 12 Nov 2026.
- **Backend language is changing back to Python (final)**, founder, 12 Nov 2026. Every answer is collected; the record (0049) is not written yet. Until it lands, the C# code and decision [0042](../decisions/0042-back-to-dotnet-11.md) stay current.
- **Process:** agent-workflows (Superpowers) is the process from decision [0050](../decisions/0050-agent-workflows-process.md).
- Design canvas and new ideas are frozen until something is clickable (founder, 11 Nov 2026).

## Open pull requests
- The decision 0050 pull request (branch `docs/agent-workflows-process-0050`).

## Next, in order
1. Merge decision 0050.
2. Write decision 0049 (back to Python, final), which supersedes 0042 and the .NET test-tool parts of 0043 and 0048. Its amendments: the frontend starts from the founder's Next.js template (pnpm, TypeScript 5.9, `frontend/`), and every browser test is in TypeScript with playwright-bdd. pytest-bdd runs only the scenarios without the `@ui` tag.
3. Port pull requests in order: PC (language-neutral contract), P1 (Python foundation, founder merge), P2–P3b (cost engine, test first), P4 (generator with a byte-identical `costs.json`), P5 (validator), P6 (spec runner), P7 (mutation testing), P8 (remove .NET, founder merge). The stage 3 gate (#71) runs alongside.
4. After P8: #86, the app shell, built from the Next.js template; then screens #165–#175.

## Blockers
- None. Issues #59 and #60 (C# 15) and #61 (.NET Skills repository) will close as not planned once 0049 is accepted.

## Founder to-dos
- Restart Claude Code so the Superpowers and house-reviewers plugins load in this project.
- Approve the two documentation MCP servers (Microsoft Learn, Context7) when Claude Code asks at the start of a session.
- Check the OpenAI image policy before stage 5b.
- Trade-mark clearance for "Vestagraph".
- Narrow the sharing of the design-canvas link.

## Open `noticed` issues
#33, #115, #151, #159, #179 (closed by the 0050 pull request), #184.
