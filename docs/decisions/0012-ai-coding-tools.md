# 0012: AI coding tools and setup

**ID:** WW-02  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 1

## Context
Which AI tools build and review the code, and how they are controlled.

## Options
- **Claude Code only:** One tool, one rules file, AI review on each change.
- **Claude Code + GitHub Copilot:** Adds in-editor suggestions; two tools.
- **Several agents in parallel:** Faster, harder to follow and review.

## Recommendation
Claude Code only.

## Decision
**Claude Code builds; OpenAI Codex reviews.** Claude Code does the main implementation from specs, guided by `CLAUDE.md`. Codex reviews each pull request as an independent second opinion before your review. Using a different AI for review means it is less likely to share the builder's blind spots.

## Consequences
Two sets of instructions to keep in line: `CLAUDE.md` for Claude Code and `AGENTS.md` for Codex, both pointing to the same project rules (no invented facts, no hand-typed figures, public-repo rules). Codex review findings are advice: you decide what to act on. Two subscriptions, tracked in the weekly spend review separately from the Azure cap (IN-05). Neither tool may install dependencies, change infrastructure or push to main without your approval.
