# 0024: Keeping dependencies and their documentation current

**ID:** WW-07  
**Status:** Accepted (partly superseded: 7-day version wait by [0027](0027-stage-2-engineering-hardening.md); who merges updates and what `third-party.md` tracks by [0035](0035-ways-of-working-v2.md))  
**Date:** 2026-10-23  
**Stage:** 2  
**Supersedes:** in [0015](0015-agent-merges-after-review.md), the founder-only merge of "upgrading dependencies". Adding a **new** dependency is still a founder merge.

## Context
Frameworks and packages release often, and agents tend to write code for older versions. The founder wants the third-party documentation list (`docs/references/third-party.md`) kept current as releases come out.

## Options
- **Patch updates by Claude Code, minor and major by the founder.**
- **All updates by the founder.**
- **All updates by Claude Code after checks and review (chosen).**

## Recommendation
Patch updates by Claude Code, minor and major by the founder.

## Decision
Founder's answer: "all updates done by you". So:
- **Dependabot** checks NuGet, npm and GitHub Actions weekly, grouping related updates into one pull request per ecosystem. It's configured in the first pull request that adds each ecosystem.
- **Claude Code merges every version update**, patch, minor and major, once all checks pass and Codex has reviewed it. For a major update, Claude Code reads the official migration notes, fixes breaking changes in the same pull request, and says what changed in the description.
- **Every pull request that changes a version updates `docs/references/third-party.md`** in the same change. Once code exists, a CI check compares the file with the real versions and fails if they differ.
- **A monthly link check** (for example lychee in GitHub Actions) finds documentation links that have moved or died.
- **At the start of each stage**, the agent re-reads the official documentation for that stage's tools.

## Consequences
- The founder still merges pull requests that **add** a new dependency, so new packages are a deliberate choice.
- A failing check or a P0/P1 finding blocks an update like any other change.
- Security updates arrive the same way and are prioritised.
