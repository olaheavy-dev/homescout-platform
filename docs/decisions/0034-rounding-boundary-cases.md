# 0034: Rounding boundary test cases

**ID:** BE-06  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2  
**Supersedes:** in [0021](0021-dotnet-engineering-foundation.md), the "boundary examples before implementation" rule, which listed half-penny, just-below-half and negative cases only.

## Context
Follow-up #14 (from the review of #11) found that the boundary cases didn't pin nearest-penny behaviour: an implementation that truncates every non-exact fraction but special-cases exactly 0.5 would pass. Accepted records aren't edited, so the stronger rule is recorded here.

## Options
- **Require the full set of boundary cases on both sides of zero (chosen).**
- **Keep 0021's list:** leaves a gap a wrong implementation could pass.

## Recommendation
The full set.

## Decision
For every rounded calculation, the independently worked test cases, written before the code, include all of these, on both sides of zero:

| Case | Positive example | Negative example |
|---|---|---|
| Just below half | 0.4999p → 0p | −0.4999p → 0p |
| Exactly half | 0.5p → 1p | −0.5p → −1p |
| Just above half | 0.5001p → 1p | −0.5001p → −1p |

These follow 0021's default rule (nearest penny, half away from zero). A calculation that uses an official rule with different rounding states its own boundary cases from that rule's source.

## Consequences
- Closes follow-up #14.
- The test-first skill (decision 0031) uses this table when it's added.
