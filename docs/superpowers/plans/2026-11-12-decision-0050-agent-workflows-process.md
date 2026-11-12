# Plan: decision 0050, agent-workflows as Vestagraph's process

**Spec:** the decision record [0050](../../decisions/0050-agent-workflows-process.md). For a process decision, the record is the spec. Design approved by the founder on 12 Nov 2026 ("Approve as described").

**Kind of change:** documentation only (Markdown, plus one `.gitignore` line and deleted agent files). No code, so there are no tests; `make check` still runs before pushing.

## Tasks
1. Write `docs/decisions/0050-agent-workflows-process.md` (WW-17), and add the WW-17 line to the register. Update the status lines of 0031 and 0035 and their register rows. Check: every superseded point is named; no older text is rewritten.
2. `AGENTS.md`: rewrite "How work flows" as the step-to-skill table, add the plan location to "Planning", add the criteria-to-tests mapping, the security and visual reviewers and the status-file handover to "When building", rename "When reviewing" to `## Code Review Rules` (and every reference to it), add Haiku to "Keeping agent cost down", and stop naming `.claude/agents/` in "Commands". Check: `grep -n "When reviewing\|planner\|implementer\|verifier" AGENTS.md` returns nothing.
3. Delete `.claude/agents/` (planner, implementer, verifier, reviewer, review-handler). Check: no tracked file outside the decision history names them.
4. Add `.superpowers/` to `.gitignore`.
5. Create `docs/planning/status.md`, and point the README's current-stage line to it (closes #179).
6. `docs/README.md`: add `superpowers/` to the folder tree and the status file and Superpowers folder to the table.
7. Doc 04 §10: the skills, the new step order, the weekly 10-minute process slot and the handover.
8. Pre-flight: search for "When reviewing", ".claude/agents", "planner agent", "Reviewer agent", "0035" (process wording) and "current stage", and fix stale wording.
9. `make check`, a fresh-context Opus pre-push review, push, `@codex review`, then merge under the founder's standing approval once Codex is clean.
