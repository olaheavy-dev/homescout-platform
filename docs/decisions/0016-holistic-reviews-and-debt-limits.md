# 0016: Holistic reviews and debt limits

**ID:** WW-05  
**Status:** Superseded by [0035](0035-ways-of-working-v2.md)  
**Date:** 2026-10-23  
**Stage:** 1  
**Supersedes:** in [0015](0015-agent-merges-after-review.md), the founder-merge condition "any pull request where a Codex finding was deliberately not fixed", and the matching consequence that the founder decides on findings "proposed to be left unfixed". The rest of 0015 still stands, including the review-round rule.

## Context
Pull requests #4–#6 took several review rounds each. Codex raised new points every round, mostly contradictions between documents that could have been caught before review. The founder asked for Codex to review holistically, with all changes presented once, because they are worried about accumulating tech debt and also want speed. Separately, follow-up issue #7 found that 0015 was ambiguous about whether the founder could merge with an unfixed serious finding.

## Options
- **Keep 0015 as is:** more review rounds, slow, and the serious-finding ambiguity remains.
- **Holistic reviews plus debt limits (chosen):** fewer rounds, and debt can't silently pile up.
- **Drop Codex re-reviews entirely:** fastest, but fixes go unchecked.

## Recommendation
Holistic reviews plus debt limits, with serious findings always blocking.

## Decision
Founder's words: "can codex review issues holistically and make sure that all the changes are presented once. I am scared of us accumulating tech debts and also want speed." Adopted:

1. **Pre-flight check by Claude Code:** before opening a pull request, search the repository for every term, decision ID, rule and figure the change touches, fix contradictions in the same pull request, and say in the description what was checked.
2. **One complete first review by Codex:** report every finding at once, including knock-on effects in other files. Re-reviews check only the fixes; new P2/P3 points only on lines changed since the last review, P0/P1 anywhere.
3. **Debt limits:** no stage gate passes with open `review-followup` issues; more than 5 open follow-ups pause new feature work; every stage gate includes a whole-repository audit for contradictions and debt.
4. **Serious findings always block (resolves #7):** P0/P1 findings must be fixed before anyone merges, with no override. For review findings specifically, the founder is needed only where Claude disputes a finding as wrong; P2/P3 findings validly deferred to a follow-up issue don't require the founder. This doesn't change the other founder-only merges in 0015 and `AGENTS.md` (licence, settings and merge rules, rule tables, infrastructure and costs, dependencies).

## Consequences
- Rules live in `AGENTS.md` ("When building", "When reviewing", "When merging", "Review rounds") and doc 04 §9–§10.
- More effort per pull request before review, in exchange for fewer review rounds and lower total agent cost.
- If Codex still spreads findings over many rounds, revisit with a scoped manual review request or a different review setup.
