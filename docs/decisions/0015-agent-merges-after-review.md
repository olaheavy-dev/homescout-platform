# 0015: Claude Code merges after Codex review

**ID:** WW-04  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 1  
**Supersedes:** the review and merge steps of [0011](0011-ways-of-working.md) ("you … review and merge", "your review → merge") and the review-order, finding-triage and two-instruction-file parts of [0012](0012-ai-coding-tools.md) ("before your review", "you decide what to act on", keeping `CLAUDE.md` and `AGENTS.md` as separate files in step). The rest of 0011 and 0012 still stands.

## Context
Under 0011, the founder merged every pull request. With Codex reviewing every pull request automatically, the founder decided that Claude Code should merge once that review is satisfied, so routine changes don't wait. At the same time, the founder asked to keep a single instructions file for all agents.

## Options
- **Founder merges everything:** maximum control, but slows routine changes.
- **Claude merges after Codex review, with exceptions (chosen):** routine changes flow; sensitive changes still go to the founder.
- **Claude merges anything that passes checks:** fastest, but loses the independent review.

## Decision
Claude Code merges a pull request once Codex has reviewed its latest commit, every finding is fixed or answered, all threads are resolved and every check on the pull request has passed (none failing or still running). The founder still merges changes to the licence, repository settings and merge rules; tax, legal, tenancy and privacy rule tables; infrastructure and costs; dependencies; and any pull request where a Codex finding was deliberately not fixed. The full conditions are in `AGENTS.md`, "When merging".

**Review rounds** (added by the founder: "let us fix minor issues separately; our ways of working should be optimised for quality, speed and coding agent cost"): serious findings (P0/P1) always block a merge. Minor findings (P2/P3) are fixed in the pull request during the first two review rounds; from round 3 onward they go to a `review-followup` issue, cleared in batched tidy-up pull requests at least once per stage and before each stage gate. Fixes are pushed in one batch per round, with one re-review request. Cost-saving working rules are in `AGENTS.md`, "Keeping agent cost down".

`AGENTS.md` becomes the single instructions file for all agents. `CLAUDE.md` is a symbolic link to it.

## Consequences
- One workflow (doc 04 §10, steps 5–7): Codex reviews, Claude Code fixes or answers each finding, then merges routine pull requests. The founder reviews founder-only pull requests and any where a finding is proposed to be left unfixed, and decides on those findings. Otherwise the founder reviews by exception and through post-merge summaries.
- Branch protection on `main` (pull request required, threads resolved) stays in place and enforces the review step.
- Claude Code's own safety checks may still ask the founder to approve a merge; that is expected.
- On systems without symbolic-link support, `CLAUDE.md` shows as a one-line file containing `AGENTS.md`. All current work is on macOS and GitHub, which support symbolic links.
