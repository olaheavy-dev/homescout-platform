# 0035: Ways of working v2 (consolidated rulebook)

**ID:** WW-12  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2  
**Supersedes:**
- fully: [0015](0015-agent-merges-after-review.md), [0016](0016-holistic-reviews-and-debt-limits.md), [0033](0033-review-fallback.md);
- in part: [0011](0011-ways-of-working.md) (process), [0012](0012-ai-coding-tools.md) (review flow and model use), [0024](0024-dependency-updates.md) (who merges updates and what `third-party.md` tracks), [0026](0026-learning-first-engineering.md) (where learning sections are required, when explain-back happens), [0027](0027-stage-2-engineering-hardening.md) (founder merge for its named tools), [0031](0031-agent-roster.md) (model column and planner lane).

## Context
An alignment check against the project's aims (portfolio, learning, commercial option; speed, quality, security, pace; low agent cost; no tech debt) found the product, data and security decisions sound, but the working rules had piled up through partial supersessions: knowing the current merge rule meant reading five records plus `AGENTS.md`, which cost tokens and caused the contradictions behind most review rounds. The founder also set new direction: Opus 5.5 plans and reviews; Sonnet 5.5 does everything else; every feature is planned and split into frontend and backend tasks; Claude reviews before pushing; one script runs all checks; and zero GitHub security issues.

## Options
- **One consolidated rulebook (chosen):** `AGENTS.md` holds the current rules; older records become history.
- **Keep superseding piece by piece:** cheaper today, more contradictions later.

## Recommendation
One rulebook, with the speed-ups below.

## Decision
The founder chose these; the full operational text is in `AGENTS.md`, which is now the **single current rulebook** for how work is done. Doc 04 §10 summarises it.

1. **Models:** **Opus 5.5** for all planning and reviewing (feature plans, the pre-push review, handling review comments, audits, drafting decisions). **Sonnet 5.5** for everything else (implementing, verifying, routine agent work).
2. **Feature planning:** every feature gets a plan before building (Opus). It fixes the **data contract first** (JSON Schema and generated files now, OpenAPI later), then splits the work into **backend tasks** (C# cost engine, generator, later the API) and **frontend tasks** (Next.js screens, using the design skills), each with acceptance criteria, edge cases and the test that proves each. Small changes get a short plan in the issue. Until a running backend exists (stage 5 prototype), "backend tasks" means fixtures and the cost engine.
3. **One script for all checks:** `make check` runs every automated check (build, tests, formatting, schema validation, regeneration check, analysers, JetBrains InspectCode, complexity, coverage) the same way locally and in CI. Agents run it before pushing. GitHub Actions minutes are free for this public repository, so the saving is in avoided review rounds. **InspectCode in CI:** the founder chose to run it in CI too. Its [documentation](https://www.jetbrains.com/help/resharper/ReSharper_Command_Line_Tools.html) describes the tools as free and for integrating "into your CI", and its [licence](https://www.jetbrains.com/resharper/buy/command_line_license.html) permits use "in accordance with the Software documentation". It is installed as a pinned project-local .NET tool (`JetBrains.ReSharper.GlobalTools` in the tool manifest); new InspectCode warnings fail `make check`, like any other finding.
4. **Pre-push review:** before pushing, a **fresh-context Opus review** (not the session that wrote the change) does one complete pass using `AGENTS.md`, "When reviewing". Its findings are fixed before the pull request opens.
5. **Codex stays required:** Codex reviews the latest commit of every pull request. While Codex is unavailable (usage limit, outage, or stuck over an hour), documentation-only pull requests may merge on a fresh-context Opus review posted as a fallback; code waits for Codex.
6. **Zero GitHub security issues:** no open code-scanning, Dependabot or secret-scanning alerts on `main`. A pull request that adds an alert can't merge, and an alert that appears on `main` is fixed before new feature work.
7. **Review rounds:** P0/P1 always block, in any round. P2/P3 are fixed in rounds 1–2, then deferred to `review-followup` issues. Fixes go in one batch with one re-review.
8. **Debt limits:** no stage gate passes with open `review-followup` issues; more than 5 open pauses feature work. Items an agent merely **noticed** outside its task get a separate `noticed` label: triaged at each stage gate, not counted towards the limit.
9. **Dependencies:**
   - **Pre-approved packages** (no founder merge needed when first added): JetBrains ReSharper Command Line Tools (a free, proprietary-licence build tool, used but never shipped, so a recorded exception to the 0027 open-source licence allow-list), NUnit, NUnit analysers, the NUnit Microsoft.Testing.Platform runner and its code-coverage extension, FsCheck, NetArchTest, Stryker.NET, the CodeQL, dependency-review, actionlint, zizmor and lychee GitHub Actions, and, when stage 6 starts, Aspire, OpenTelemetry, Microsoft Agent Framework, Microsoft.Extensions.AI and its evaluation libraries, and the Npgsql PostgreSQL provider. Except for the JetBrains tools above, each still passes the licence allow-list (0027); all get a `third-party.md` entry. Anything else is a founder merge.
   - **Updates:** patch and minor updates merge when every check passes, without an AI review. Major updates get the pre-push Opus review and Codex. `third-party.md` records major versions only; exact versions live in the lock files.
10. **Learning (0026):** "How it works" and "Concepts to learn" are required on **feature** pull requests only, not on documentation, chore or dependency pull requests. Explain-back happens in a **weekly** batch per significant slice, and is no longer a condition of "done".
11. **Fewer formal records:** only hard-to-reverse decisions get a full decision record. Easily reversible choices (for example a library swap behind an interface, a folder name) are recorded as one line in the register with their default. Stages 3 and 4 may overlap.
12. **Agent spend:** coding-agent spend (Claude and Codex) and review rounds per pull request are tracked in the weekly review. No fixed cap.
13. **Agent permissions:** the first code pull request adds Claude Code project settings with an allow-list for safe read, build and test commands, and requires approval for installing packages, changing infrastructure, pushing to `main` or changing repository settings.

## Consequences
- `AGENTS.md` is rewritten as the rulebook; superseded records keep their text as history, with status lines pointing here.
- The fallback review and rebase exception from 0033 remain in this simpler form (point 5); a rebased pull request otherwise gets a fresh review.
- Founder-only merges still cover: licence, repository settings, CI permissions and merge rules; tax, legal, tenancy and privacy rule tables; infrastructure and running costs; packages not on the pre-approved list; and pull requests where Claude disputes a finding.
