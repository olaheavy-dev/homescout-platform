# 0015: Claude Code merges after Codex review

**ID:** WW-04  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 1  
**Supersedes:** the merge step of [0011](0011-ways-of-working.md) ("you … merge"); the rest of 0011 still stands.

## Context
Under 0011, the founder merged every pull request. With Codex reviewing every pull request automatically, the founder decided that Claude Code should merge once that review is satisfied, so routine changes don't wait. At the same time, the founder asked to keep a single instructions file for all agents.

## Options
- **Founder merges everything:** maximum control, but slows routine changes.
- **Claude merges after Codex review, with exceptions (chosen):** routine changes flow; sensitive changes still go to the founder.
- **Claude merges anything that passes checks:** fastest, but loses the independent review.

## Decision
Claude Code merges a pull request once Codex has reviewed its latest commit, every finding is fixed or answered, all threads are resolved and checks pass. The founder still merges changes to the licence, repository settings and merge rules; tax, legal, tenancy and privacy rule tables; infrastructure and costs; dependencies; and any pull request where a Codex finding was deliberately not fixed. The full conditions are in `AGENTS.md`, "When merging".

`AGENTS.md` becomes the single instructions file for all agents. `CLAUDE.md` is a symbolic link to it.

## Consequences
- The founder reviews by exception and through Claude's post-merge summaries, and can still review any pull request.
- Branch protection on `main` (pull request required, threads resolved) stays in place and enforces the review step.
- Claude Code's own safety checks may still ask the founder to approve a merge; that is expected.
- On systems without symbolic-link support, `CLAUDE.md` shows as a one-line file containing `AGENTS.md`. All current work is on macOS and GitHub, which support symbolic links.
