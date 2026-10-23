# 0031: Agent roster and working rules

**ID:** WW-10  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2

## Context
The founder asked whether HomeScout needs custom Claude Code agents, given a reference 11-stage agent pipeline from an earlier project, under the mantra of speed, quality, security and pace. Most of that pipeline's stages are already covered more cheaply by Codex review (0012, 0015), CodeQL and dependency review (0027), and GitHub's own issue handling.

## Options
- **Lean set at stage 2 (chosen).**
- **Full 11-stage pipeline:** maximum rigour, but many handoffs and high model cost per change.
- **No custom agents yet.**

## Recommendation
The lean set.

## Decision
The founder chose the lean set, written fresh for HomeScout in `.claude/` ([subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills)), added with the first code pull request:

| Agent or skill | Model | Job |
|---|---|---|
| **Implementer** | Faster, cheaper model | Builds one issue in its own worktree, runs `make check test`, opens a pull request with "How it works", "Concepts to learn" and "Noticed, not changed" |
| **Verifier** | Faster, cheaper model | Before Codex review: runs every check at the head commit and maps each acceptance criterion and edge case to a named test; a gap goes back to the implementer |
| **Review-comment handler** | Faster model; escalates money, legal, privacy, security and AI findings to the most capable model | Applies decisions 0015 and 0016 to Codex comments: severity, review rounds, follow-up issues |
| **Planner** | Most capable model | High-risk lane only (money, legal, privacy, auth, AI): a plan listing edge cases and the test that proves each |
| **Test-first skill** | — | Before each test run, state the expected failure; only valid failures count; stop if a test passes unexpectedly; never weaken an assertion; stop after 3 failed attempts; record a slice table in the pull request |

**Lanes:** light (docs and small, low-risk changes) skips the planner; full (money, legal, privacy, auth, AI) uses it, plus an on-demand `/security-review`.

**Design work uses the designer-skills plugin** ([repository](https://github.com/julianoczkowski/designer-skills), Apache-2.0, installed on the founder's machine) instead of custom agents:

| Stage | Skill | Use |
|---|---|---|
| 3 (SP-01, SP-02) | `information-architecture`, `design-brief`, `brief-to-tasks` | Navigation, page structure and flows; the prototype design brief; ordered, buildable tasks that become GitHub issues |
| 4 (DS-02) | `design-tokens` | Doc 03 §6's colours as a light and dark token file the Next.js app imports |
| 5 | `frontend-design`, `design-review` | Building screens; screenshot reviews at phone, tablet and desktop widths in light and dark mode, **replacing a custom visual-reviewer agent**. Automated accessibility tests (Playwright with axe, FE-04) still run in CI |
| Any | `grill-me` | Stress-testing a plan before committing to it |

The plugin isn't stored in the repository; the setup notes list how to install it. Its outputs (briefs, tokens, task lists) are HomeScout's own work.

Notes on using it:
- **Sequence:** `/design-flow` runs grill-me → design brief → information architecture → design tokens → brief-to-tasks → frontend-design → design review; steps can be skipped or run on their own.
- **Style:** name the aesthetic explicitly so results stay consistent: doc 03's warm, calm editorial direction maps to the plugin's **Editorial / Magazine** style, with **Scandinavian** as the alternative.
- **Where outputs go:** the skills save to `.design/<feature>/` (brief, information architecture, tasks, review). Keep that folder, list it in the docs index, and settle the full specification format in SP-01 (stage 3).
- **Dark mode:** the token skill generates light and dark palettes by default; whether the prototype ships dark mode is decided in DS-02 (stage 4).
- **Updates:** the plugin tracks its author's latest version, and its files are instructions agents follow. Update it deliberately (`/plugin update`), after reviewing what changed, like any dependency.

**Later:** a deployer once there is somewhere to deploy (stages 4–5).

**Working rules added to `AGENTS.md`:**
- Every pull request lists **"Noticed, not changed"**: anything spotted outside the task becomes a `review-followup` issue, never a side fix.
- **Stop and ask** when a task needs an undecided domain rule (open a decision issue instead of inventing one), a new dependency, or work well beyond the issue.
- **Stop after 3 failed attempts** at the same problem and report what was tried.
- **Stop what you start:** servers, watchers and temporary worktrees.

## Consequences
- Not adopted from the reference pipeline, because they duplicate existing checks or the design skills: separate plan and design reviewers, a separate security reviewer, a custom visual reviewer, a manual-review script and a closer.
- Agent files are written fresh; nothing is copied from the reference projects.
