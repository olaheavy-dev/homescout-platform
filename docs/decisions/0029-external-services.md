# 0029: Outside services: provenance and live tests

**ID:** OP-03  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 6 (rule set early)

## Context
HomeScout will call outside services: official datasets and APIs, postcode lookup, model providers. They are sometimes slow, down or changed. The founder's earlier pilot handled this well; the new plan had no rule for it.

## Options
- **Adapters with provenance labels, and live tests kept out of the merge gate (chosen).**
- **Call services directly and test against them live:** flaky builds and hidden failures.

## Recommendation
Adopt the rule.

## Decision
The founder agreed.
- **One adapter per outside service**, with a timeout and standard resilience ([HTTP resilience](https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience)). Adapters never throw for an expected failure; they return a result that says where the value came from.
- **Every externally sourced value carries a provenance label:** **Live** (fetched now), **Cached** (with when it was fetched), **Fallback** or **Unavailable**. The screen shows the label, and "Unavailable" never looks like a clean result (doc 03 §5 states).
- **Fallback is narrow:** only a named alternative source with its own provenance, or an assumption the user entered explicitly. It is **never** a default or typical value standing in for a fact about the specific property (a charge, a risk result, a certificate field); if no real source is available, the value is **Unavailable**. This applies `AGENTS.md` rule 7: missing data is never shown as zero, a favourable value or a clean result.
- **How the labels fit doc 02 §6's evidence model:** Live and Cached describe retrieval, recorded in the **Time** dimension (last retrieved); a Cached value past its refresh period is **stale** in the **Status** dimension. Fallback records the alternative source or user assumption in the **Origin** dimension. Unavailable is **missing** in the Status dimension.
- **Tests:** the merge gate runs offline, using synthetic or recorded responses. Tests that call real services are marked with an NUnit category such as `External` ([Category attribute](https://docs.nunit.org/articles/nunit/writing-tests/attributes/category.html)), run nightly, are advisory and never block merges; a failure opens an issue.

## Consequences
- Applies from the first outside service (stage 6, step 4), and to model providers in the AI layer.
- Works with decision 0022's cost-first hosting: cached values reduce paid calls.
