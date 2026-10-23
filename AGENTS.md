# AGENTS.md

Instructions for OpenAI Codex, which **reviews** pull requests on this project (decision 0012). Claude Code implements, using `CLAUDE.md`; keep the shared rules in both files in step. Your review is an independent second opinion. The founder decides what to act on.

## Project context

A home decision workspace for people buying or renting in **England**: check a home, see the real cost, compare homes, and track questions and answers until they decide. Public repository, all rights reserved; a portfolio project kept commercially viable. Accepted decisions are in `docs/decisions/`; product and design rules are in `docs/design/02`, `03` and `04`.

## What to check, in priority order

1. **Correctness:** bugs, wrong logic, unhandled states. For money, tax, dates and lease terms, recalculate the figures and check them against the cited source.
2. **Rule breaches:**
   - Invented facts, sources or rules, or numbers typed by hand instead of coming from the calculation script or cost engine.
   - AI calculating numbers, or the product calling a home "verified", "safe" or "approved".
   - Secrets, real personal data or licensed datasets committed.
   - English rules hard-coded into shared code, or a non-England address getting anything other than "not yet covered".
   - Missing data shown as zero, a favourable value or a clean result.
3. **Spec match:** does the change meet the linked acceptance criteria, including mobile, keyboard access and edge states?
4. **Tests:** are the important cases covered, especially numbers and edge states?
5. **Clarity:** could the founder understand and maintain this? Flag unnecessary complexity.

## How to report

- Lead with the most serious findings. For each: file and line, what's wrong, a concrete example of the failure, and a suggested fix.
- Separate **must fix** from **suggestions**.
- Use plain language. Don't restate the diff or praise; say "no issues found" if there are none.
- Don't push commits or approve merges.
