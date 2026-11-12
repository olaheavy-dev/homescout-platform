# Status

Overwritten at the end of every session (decision 0050). Last updated: **12 Nov 2026**.

## Where we are
- **Stage 3** (prototype specification) is open; its gate is issue #71. Stage 4's frontend foundation is decided: [0048](../decisions/0048-frontend-foundation.md), accepted 12 Nov 2026.
- **Backend language: Python, final** ([0049](../decisions/0049-back-to-python-final.md), founder, 12 Nov 2026). The C# code keeps running until the port removes it (P8).
- **Process:** agent-workflows (Superpowers) is the process from decision [0050](../decisions/0050-agent-workflows-process.md).
- Design canvas and new ideas are frozen until something is clickable (founder, 11 Nov 2026).

## Open pull requests
- Decision 0049 (branch `docs/back-to-python-0049`). Founder merge: it adds PSF-2.0 to the licence allow-list.

## Next, in order
1. Merge decision 0049, then do its issue changes: close #59, #60, #61 as not planned; retitle #93, #94, #97, #101, #102; rename the stage 6 milestone.
2. Port pull requests in order (milestone "Python port (decision 0049)"): PC #186, P1 #187 (founder merge), P2 #188, P3a #189, P3b #190, P4 #191, P5 #192, P6 #193, P7 #194, P8 #195 (founder merge). The stage 3 gate (#71) runs alongside.
3. After P8: #86, the app shell, built from the Next.js template; then screens #165–#175.

## Blockers
- None.

## Founder to-dos
- Merge the decision 0049 pull request (licence allow-list change).
- After P1 merges: add Python to CodeQL's default setup in the repository settings.
- Approve the two documentation MCP servers (Microsoft Learn, Context7) when Claude Code asks at the start of a session.
- Check the OpenAI image policy before stage 5b.
- Trade-mark clearance for "Vestagraph".
- Narrow the sharing of the design-canvas link.

## Open `noticed` issues
#33, #115, #151, #159, #184.
