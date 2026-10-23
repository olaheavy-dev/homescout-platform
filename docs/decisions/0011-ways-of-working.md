# 0011: Ways of working

**ID:** WW-01  
**Status:** Accepted; merge step superseded by [0015](0015-agent-merges-after-review.md)  
**Date:** 2026-10-23  
**Stage:** 1

## Context
Agents produce work from stage 2, so the way decisions and changes are made needs to be fixed first.

## Options
- **Standard setup:** Every change goes through a pull request you review; tasks in GitHub Issues on a project board; weekly plan and review including spend.
- **Lighter setup:** Small changes go straight to main. Faster, less review history.
- **Separate repos:** More admin for one person with agents.

## Recommendation
Standard setup.

## Decision
Standard setup, as written in doc 04 §10: agents draft, you decide, review and merge; one decision record per decision; issue → branch → pull request → checks → AI review → your review → merge → explain-back; weekly plan and review.

## Consequences
Defaults to confirm as we go: weekly cadence, you write the 'why' of each decision, explain-back after each merge in `docs/learning-log.md`.
