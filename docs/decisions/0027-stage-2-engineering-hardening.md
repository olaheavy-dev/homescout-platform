# 0027: Stage 2 engineering and security hardening

**ID:** WW-09  
**Status:** Accepted (partly superseded: founder merge for its named tools by [0035](0035-ways-of-working-v2.md); licence allow-list extended by register line WW-13)  
**Date:** 2026-10-23  
**Stage:** 2  
**Supersedes:**
- in [0018](0018-fixture-data-format.md) and doc 04 §5 step 1, CI starting at stage 4: a minimal CI now starts in stage 2. Stage 4 (IN-04) still decides deployment and environments.
- in [0024](0024-dependency-updates.md), immediate version updates: Dependabot now waits 7 days before proposing a new version.

## Context
A best-practice audit ([record](../reviews/2026-10-23-best-practice-audit.md)) found that some GitHub settings didn't match the documents, that several stage 2 decisions needed CI before stage 4, and that money rounding and test tooling were under-specified.

## Options
- **Adopt the "do now" list (chosen):** free for public repositories, and fixes the conflicts.
- **Adopt without the version wait.**
- **Pick individually.**

## Recommendation
Adopt all.

## Decision
The founder approved all of the following.

**Repository settings (applied 23 October 2026):** secret scanning with push protection; Dependabot alerts and security updates; private vulnerability reporting with `SECURITY.md`; squash merges only; merged branches deleted automatically; GitHub Actions must be pinned to full commit SHAs. Required status checks are added to `main` as soon as the CI workflow exists.

**CI from stage 2:** one free GitHub Actions workflow running the Makefile: locked restore, build, tests, schema validation, regenerate the generated files and fail if they changed. Also CodeQL default setup for C#, JavaScript/TypeScript and Actions; the dependency review action (blocks vulnerable packages, and packages whose licence isn't on the allow-list below); actionlint and zizmor for workflow files.

**Dependency licence policy:** the dependency review action is configured with an explicit `allow-licenses` list ([configuration](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action)), chosen to keep the all-rights-reserved, commercially viable code base free of copyleft obligations: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, 0BSD, Zlib, Unlicense, CC0-1.0 and MPL-2.0 (file-level copyleft, acceptable for unmodified use). Anything else, including GPL, AGPL, LGPL, source-available or non-commercial licences, and packages with no licence, is blocked unless the founder approves an exception in a decision record.

**Dependabot:** a 7-day `cooldown` before proposing new versions; security updates are exempt and arrive immediately.

**Cost engine:**
- **Explicit rounding:** every calculation names its rounding rule (for example half away from zero) and cites the source of that rule; code always passes `MidpointRounding` explicitly and never relies on the default, which is banker's rounding.
- **Property-based tests** (FsCheck) for rules that must always hold, such as "total equals the sum of its lines", "no negative costs", and "a higher rent never lowers the monthly cost".
- **Test platform:** NUnit on Microsoft.Testing.Platform, with code coverage, settled in the first implementation pull request.
- **Code style:** an `.editorconfig`, checked in CI with `dotnet format --verify-no-changes`.

**Architecture diagrams:** a C4 context diagram and a container diagram in Mermaid, to be added in `docs/architecture/` during stage 2 (the folder doesn't exist yet) and updated as the system grows.

## Consequences
- The first implementation pull request adds the CI workflow, `dependabot.yml` and these tools; new tools are new dependencies, so that pull request is a founder merge.
- Later-stage items from the audit are recorded in the audit record and linked from their stages in doc 04.
