# 0050: agent-workflows as Vestagraph's process

**ID:** WW-17  
**Status:** Accepted (founder, 12 Nov 2026)  
**Date:** 2026-11-12  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** [0035](0035-ways-of-working-v2.md) point 1 (models: Haiku added for mechanical subtasks), point 2 (how a plan is written: brainstorming and writing-plans; the plan's content is unchanged) and point 4 (how the pre-push review is run); [0031](0031-agent-roster.md) (the project agent roster: the five agents in `.claude/agents/` are retired; the design skills and the test-first skill stay; and its stage 5 note that the design skills replace a custom visual-reviewer agent: the shared `visual-reviewer` now runs on UI pull requests alongside them); and `AGENTS.md` "How work flows", "Planning" and "When building", rewritten below. Everything else in 0035 stands.

## Context
On 12 Nov 2026 the founder chose, in prompt windows, to adopt **agent-workflows**, the founder's own process kit, as the backbone for every project. The kit holds the Superpowers skills, Matt Pocock's `pr` skill, the shared `house-reviewers` agents, an MCP server catalogue and the house rules linked to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Vestagraph already had its own planner, implementer, verifier, reviewer and review-handler agents (0031, 0035). Keeping both meant two processes that disagreed in small ways, and every agent would have to choose between them.

**A skill** is a packaged set of instructions an agent loads for one kind of task (for example "write a plan"). [Claude Code skills documentation](https://code.claude.com/docs/en/skills).  
**A subagent** is a separate agent with its own context that the main session hands a task to. [Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents).

## What was checked (12 Nov 2026)
| Item | Version | Licence | Source |
|---|---|---|---|
| agent-workflows | v0.4.0 | the founder's own repository (private) | `olaheavy-dev/agent-workflows` README and CHANGELOG |
| Superpowers (vendored in agent-workflows) | 7.0.2, upstream commit `22f0b46` | MIT | [obra/superpowers](https://github.com/obra/superpowers) |
| `pr` skill (vendored) | upstream commit `5863806` | MIT | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `house-reviewers` plugin | from agent-workflows v0.4.0 | the founder's own repository (private) | agent-workflows `plugins/house-reviewers` |

These are agent instructions, not packages the product ships or `make check` runs, so the licence allow-list in [0027](0027-stage-2-engineering-hardening.md) and the pre-approved package list don't apply. They're installed on the founder's machine at user scope by `./sync claude-code` in agent-workflows.

## Options
- **Adopt agent-workflows and retire the project agents (chosen).** One process across all the founder's projects; Vestagraph's `AGENTS.md` keeps only what is specific to Vestagraph.
- **Adopt it but keep the project agents for one more stage.** Gives a fallback, but agents could follow either process, and a later pull request has to remove them.
- **Hybrid overlay, as chosen for another of the founder's projects.** Fits a project with its own specialist agents (deployer, security gates). Vestagraph's five agents all duplicate a Superpowers skill, so there is nothing left to overlay.

## Decision
The founder approved the design on 12 Nov 2026 ("Approve as described" in the prompt window), after choosing to adopt agent-workflows earlier that day.

1. **Process backbone:** Vestagraph follows the agent-workflows issue workflow. Each step uses these skills:

   | Step | Skill or agent | Model |
   |---|---|---|
   | Understand and agree the change | Superpowers `brainstorming` | Opus 5.5 |
   | Design review before planning UI or journey work | `design-reviewer` (house-reviewers) | as the agent sets |
   | Plan | Superpowers `writing-plans` | Opus 5.5 |
   | Build | Superpowers `subagent-driven-development` (or `executing-plans`), `test-driven-development`, plus Vestagraph's `test-first` skill for anything numeric or legal | Sonnet 5.5 |
   | Verify | Superpowers `verification-before-completion` and `make check` | Sonnet 5.5 |
   | Pre-push review | Superpowers `requesting-code-review` in a fresh context, plus `code-security-reviewer` (house-reviewers), plus `visual-reviewer` for UI changes | Opus 5.5 (visual: as the agent sets) |
   | Open the pull request | Superpowers `finishing-a-development-branch` and the `pr` skill | Sonnet 5.5 |
   | Codex review and replies | `@codex review`, then Superpowers `receiving-code-review` | Opus 5.5 handles comments |
   | Merge | Claude Code, under `AGENTS.md` "When merging" (unchanged) | — |

2. **Models:** Opus 5.5 plans and reviews; Sonnet 5.5 builds and verifies (0035 point 1). **Haiku** may do clearly mechanical subtasks, such as renaming across files or reformatting a table.
3. **Plans:** a plan's content is unchanged from 0035 point 2 (data contract first, then backend and frontend tasks with acceptance criteria, edge cases and the test that proves each). Specs and plans are saved in `docs/superpowers/specs/` and `docs/superpowers/plans/`, and the agent posts a short plain summary in the chat. For a process or product decision, the decision record is the spec, so no separate spec file is written. Small changes still get a short plan in the issue.
4. **Verification maps criteria to tests:** before the pre-push review, each acceptance criterion and edge case is matched to a named test (file and test name). A criterion with no test is a gap to fix (the retired verifier's rule).
5. **Retired project agents:** `.claude/agents/` planner, implementer, verifier, reviewer and review-handler are deleted. Each maps to a skill in point 1. The `test-first` skill stays as Vestagraph's extra rules on top of Superpowers test-driven development for money and legal code. The design skills (0031) stay.
6. **Codex review rules:** `AGENTS.md` "When reviewing" is renamed **`## Code Review Rules`**, which is the heading hosted `@codex review` reads. Its content is unchanged.
7. **Status file:** `docs/planning/status.md` holds the project's current state: open pull requests, what's next, blockers and the founder's to-dos. It is **overwritten** at the end of every session, not added to. It replaces the "current stage" line in the README. Agent memory keeps only personal preferences and approvals.
8. **Superpowers ledger:** `.superpowers/` (Superpowers' local working files: plan progress and brainstorming sessions, which can include a session token) is git-ignored.
9. **Weekly process review:** the weekly review (doc 04 §10) gains a 10-minute process slot. It looks at open `process` issues in agent-workflows and three numbers: review rounds per pull request, P0/P1 findings Codex caught after the pre-push review, and decisions reopened. It changes at most one or two things. Process friction is logged as it happens, as a `process` issue in agent-workflows (house rules).

## Carried over unchanged
Rules 1–9 for every agent; data contract first; `make check` before every push; the pre-push review as a fresh-context Opus pass; Codex on every pull request except small dependency updates; the fallback review; the merge conditions and founder-only list; P0–P3 severities, review rounds and debt limits; the pre-approved packages; "Teach as you build" and prompt windows (WW-16); agent permissions (0035 point 13).

## Consequences
- `AGENTS.md` "How work flows", "Planning" and "When building" are rewritten to point to the skills. "When reviewing" becomes `## Code Review Rules`. The command list stops naming `.claude/agents/`.
- `docs/README.md` lists `docs/superpowers/` and `docs/planning/status.md`. The README's current-stage line points to the status file (closes #179).
- Doc 04 §10 names the skills and the weekly process slot.
- Founder to-do: restart Claude Code so the Superpowers and house-reviewers plugins load (they are installed and switched on, but didn't load in the session that wrote this record).
- If the agent-workflows process changes, Vestagraph follows its tagged release. A change that contradicts a Vestagraph rule needs a register line or a new record here first.
