---
name: test-first
description: Test-first workflow for HomeScout code, required for anything numeric or legal (cost engine, rounding, rules). Use before writing implementation code for such a change.
---

# Test-first workflow (decision 0031)

Write the test before the code it proves. Work in small vertical slices.

For each slice:
1. **Write the test** from an independently worked example (inputs, working, source), not from the implementation. Test names follow `Method_condition_result`.
2. **State the expected failure** in words before every test run: which test, and why it should fail (for example "`Round_halfPenny_roundsAwayFromZero` fails: `Round` does not exist yet").
3. **Run the test.** Only a failure that matches your statement counts. A compile error counts only if it is the one you predicted; a different failure means your test or your understanding is wrong, so fix that first.
4. **Stop if a test passes unexpectedly.** A test that passes before the code exists proves nothing: investigate before going on.
5. Write the smallest code that makes the test pass, then run again.
6. **Never weaken an assertion** (looser tolerance, removed case, changed expected value) to make a test pass. If an expected value looks wrong, recheck the worked example and its source, and ask.
7. **Stop after 3 failed attempts** at the same problem and report what was tried.

Record a **slice table** in the pull request description:

| Slice | Test written | Expected failure | Observed failure | Passes after |
|---|---|---|---|---|

## Rounding boundary cases (decision 0034)

Every rounded calculation needs all six cases, on both sides of zero, worked out before the code (nearest penny, exact halves away from zero):

| Case | Positive | Negative |
|---|---|---|
| Just below half | 0.4999p gives 0p | -0.4999p gives 0p |
| Exactly half | 0.5p gives 1p | -0.5p gives -1p |
| Just above half | 0.5001p gives 1p | -0.5001p gives -1p |

Code passes `MidpointRounding.AwayFromZero` explicitly. If an official rule rounds differently, state that rule's own boundary cases and cite its source.
