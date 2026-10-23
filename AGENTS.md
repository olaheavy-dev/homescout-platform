# AGENTS.md

Shared instructions for every AI agent on this project. `CLAUDE.md` is a symbolic link to this file, so Claude Code and OpenAI Codex read the same text. Edit **this** file only.

Who does what is in **"How work flows"** below: Opus 5.5 plans and reviews, Sonnet 5.5 builds and verifies, Codex reviews every pull request, and Claude Code merges. Builders follow "When building"; every reviewer (Opus pre-push, Codex, fallback) follows "When reviewing"; merging follows "When merging".

## What this project is

HomeScout (private code name; public name not chosen) is a home decision workspace for people **buying or renting in England**: check a home, see the real cost, compare homes, and track questions and answers until they decide. It is a portfolio and learning project for its founder, kept commercially viable for later. Public repository, all rights reserved.

Read before working (the [documentation index](docs/README.md) explains the folder structure and naming rules):
- `docs/product/02-research-and-direction.md`: product decisions and scope
- `docs/product/03-prototype-and-image-direction.md`: prototype behaviour and design
- `docs/product/04-project-goals-and-delivery.md`: roadmap (§9) and ways of working (§10)
- `docs/decisions/`: accepted decisions. Don't contradict one; propose a new record instead.

The current stage is in the README and `docs/planning/`.

## Private reference sources

The founder's earlier projects and a third-party AI sample were reviewed to inform decisions (summary: `docs/reviews/2026-10-23-foundation-review.md`). Their locations are listed in **`.local/references.md`**, a file that exists only on the founder's machine and is excluded from git.

- If that file exists, you may read it and the sources it lists to understand a pattern.
- **Never copy** code, configuration, file layouts or wording from those sources. Write everything fresh for HomeScout.
- **Never write** their names, company names, paths, URLs or identifiers into any tracked file, commit message, pull request or issue. Refer to them only as "the founder's earlier projects" or "the reviewed AI sample".
- The AI sample has no licence: ideas only.

## Rules for every agent

1. **No invented facts.** Never make up property data, legal or tax rules, sources, dates or competitor claims. If something isn't known, the product says so.
2. **No hand-typed calculated figures.** Figures come in two kinds. **Inputs** (a listing's claimed charge, a figure in a document, a user-entered estimate, an official dataset value) are recorded once in the fixture or data files, each with its source. **Calculated outputs** (totals, differences, repayments, comparisons) always come from the C# cost engine (decision 0019), never typed by hand. UI and docs quote inputs from the data files and outputs from the cost engine's generated files. **Test expectations are the one exception:** they must be worked out independently of the engine, as reviewed worked examples that show their working and cite the rule or source they follow, so a wrong calculation can't confirm itself.
3. **Rules come from cited sources.** Tax, tenancy, lease and privacy rules live in versioned tables or records with a source URL and effective date.
4. **The product never says a home is "verified", "safe" or "approved"**, and AI never calculates numbers. Follow decision 0004 for AI and chat behaviour.
5. **Public repository.** Never commit secrets, API keys, real personal data, real customer documents or licensed datasets. Use the synthetic fixtures. Record every image or media file in `docs/assets/README.md` before committing it.
6. **England first.** Other UK nations show "not yet covered". Keep a nation field in data; don't hard-code English rules into shared code.
7. **Missing data is never shown as zero**, a favourable value or a clean result.
8. **Plain language for the founder.** When explaining options or decisions, say what each option means in practice and give a clear recommendation.

## How work flows (decision 0035)

This file is the **single current rulebook for how work is done** (planning, building, reviewing, merging, dependencies). Where an older decision record differs on those process matters, this file and decision 0035 apply. Product, data and technical decisions stay with their records, and this file must not contradict them.

| Step | Who | Model |
|---|---|---|
| 1. Plan the feature | Planner agent | Opus 5.5 |
| 2. Build each task | Implementer agent | Sonnet 5.5 |
| 3. Run `make check` and map criteria to tests | Verifier agent | Sonnet 5.5 |
| 4. Pre-push review (fresh context, "When reviewing") | Reviewer agent | Opus 5.5 |
| 5. Open the pull request; Codex reviews the latest commit | Codex | — |
| 6. Handle review comments | Review handler | Opus 5.5 |
| 7. Merge when the conditions below are met; post a one-line summary | Claude Code | — |

## Planning (decision 0035)

- **Every feature gets a plan** before building. Small changes get a short plan in the issue.
- The plan fixes the **data contract first** (JSON Schema and generated files now, OpenAPI later), then splits the work into **backend tasks** (C# cost engine, generator, later the API) and **frontend tasks** (Next.js screens; the design skills produce the brief and tasks, decision 0031), each with acceptance criteria, edge cases and the test that proves each.
- Until a running backend exists, "backend tasks" means fixtures and the cost engine.
- Hard-to-reverse choices get a decision record; easily reversible ones get one line in the register with their default.

## When building (Claude Code)

- One issue per session, on a branch named `type/short-description` (e.g. `feat/buyer-story-costs`).
- Start from the issue's plan and acceptance criteria. If the plan is unclear or conflicts with a decision, stop and ask rather than guess.
- Small vertical slices. Tests first for anything numeric or legal, using the test-first skill once it's added (decision 0031) and the boundary cases in decision 0034.
- **Noticed, not changed:** list anything spotted outside the task under that heading in the pull request description, and open an issue labelled `noticed` for each. Don't fix unrelated things in the same change.
- **Stop and ask** when a task needs an undecided domain rule (open a decision issue instead of inventing one), a package not on the pre-approved list, or work well beyond the issue. **Stop after 3 failed attempts** at the same problem and report what was tried.
- **Stop what you start:** servers, watchers and temporary worktrees.
- **Data sources:** never scrape or copy listing content (decision 0028). Outside services go through adapters that label values Live, Cached, Fallback or Unavailable, and live-service tests stay out of the merge gate (decision 0029).
- **Result type:** use HomeScout's own `Result` for expected failures only; programming errors throw (decisions 0021, 0032).
- Before using a framework or package API, check its official documentation for the pinned major version via `docs/references/third-party.md`, not memory. When adding a dependency or changing a major version, update that file in the same pull request.
- For a major version update, read the official migration notes, fix breaking changes in the same pull request, and summarise them in the description.
- Commit messages: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
- Pull request description: what changed and why, how it was tested, **any assumptions you made**, "Noticed, not changed", and the pre-flight check done.
- **Pre-flight check:** search the repository for every term, decision ID, rule and figure the change touches, and fix any contradiction or stale statement in the same pull request. Check new facts against their sources.
- **Run `make check` before pushing.** It runs every automated check the same way as CI, including JetBrains InspectCode.
- **Pre-push review:** before pushing, run a fresh-context Opus review using "When reviewing" below, and fix its findings first.
- Ask the founder before installing packages not on the pre-approved list, changing infrastructure, cloud resources or repository settings. Never push to `main`.
- **Agent permissions:** the first code pull request adds Claude Code project settings with an allow-list for safe read, build and test commands; installing packages, infrastructure and repository-setting changes need approval; pushing to `main` is denied.

## Teach as you build (decisions 0026, 0035)

The founder is learning the languages, frameworks and tools through this project.
- **Feature** pull requests include **"How it works"** (plain language) and **"Concepts to learn"** (links to the official documentation pages for what it uses). Documentation, chore and dependency pull requests don't need them.
- When the founder asks why, answer in plain language with a small example and a link to the official source.
- For each significant slice, offer a short walkthrough: which files matter, how data flows, why it was built this way, and the alternatives. The founder learns by understanding, not by writing the code. Explain-back happens in a weekly batch.
- AI-layer work follows decision 0025: each implementation links the official documentation it follows.

## When reviewing (Opus pre-push review, Codex, and fallback reviews)

Check in priority order:
1. **Correctness:** bugs, wrong logic, unhandled states. For money, tax, dates and lease terms, recalculate the figures and check them against the cited source.
2. **Breaches of the rules above.**
3. **Spec match:** does the change meet the plan's acceptance criteria, including mobile, keyboard access and edge states?
4. **Tests:** are the important cases covered, especially numbers and edge states?
5. **Clarity:** could the founder understand and maintain this? Flag unnecessary complexity.

How to report:
- Most serious findings first. For each: file and line, what's wrong, a concrete example of the failure, and a suggested fix.
- Give each finding a severity: **P0/P1** (wrong behaviour, wrong figures, legal or security risk, broken rules above) or **P2/P3** (wording, consistency, minor gaps). Use plain language. Say "no issues found" if there are none.
- **First review: one complete pass.** Review the whole change at once, including its knock-on effects: other files in the repository that the change contradicts or makes stale (search for the same terms, decision IDs and rules). Report every finding in that first review.
- **Re-reviews: fixes only.** Check that the fixes are correct and look at newly changed lines. Raise new P2/P3 points only on lines changed since the last review; raise P0/P1 issues anywhere. Don't re-raise issues already deferred to a follow-up issue.
- Reviewers don't push commits or approve merges.

## When merging (Claude Code, decision 0035)

Claude Code may merge a pull request (squash merge) only when **all** of these are true:
1. **Codex has reviewed the latest commit.** Exceptions:
   - (a) **Fallback:** while Codex is unavailable (usage limit, outage, or stuck over an hour), a **documentation-only** pull request (Markdown and images only; no code, workflow, configuration, schema, settings or dependency files) may merge on a fresh-context Opus review using "When reviewing" (the built-in `/code-review` alone isn't enough). Post it as **one numbered pull request comment** headed **"Fallback review (Codex unavailable)"**, not as inline review threads. The pre-push review counts as the fallback if it's posted this way and the head commit hasn't changed since.
   - (b) **Small dependency updates:** a Dependabot pull request that changes only package manifests, lock files or action pins, with **no major version bump** anywhere in it, merges on green checks without an AI review. Any major bump follows the normal route.
   Code otherwise waits for Codex, and a rebased pull request gets a fresh review.
2. Every review finding is fixed, answered with a reason, or deferred under "Review rounds" below; every Codex review thread is resolved, and every fallback finding has a reply.
3. Every check on the pull request has passed: none failing, none still running, whether or not GitHub marks it as required.
4. **Zero GitHub security issues:** the pull request adds no code-scanning, Dependabot or secret-scanning alert. While an alert is open on `main`, only pull requests that fix it, or documentation-only pull requests, may merge; feature work waits. If no fix exists yet, the founder dismisses the alert in GitHub with a recorded reason.
5. The pull request doesn't fall under the founder-only list below.

**Founder merges these:**
- Changes to `LICENSE`, repository settings, CI permissions, agent permission settings (`.claude/settings.json`) or these merge rules.
- New or changed tax, legal, tenancy or privacy rule tables.
- Infrastructure, cloud resources or anything that changes running costs.
- Adding a package that isn't on the pre-approved list in decision 0035.
- Any pull request where Claude Code disputes a finding as wrong (not merely defers it). The founder decides whether the finding stands.

P0/P1 findings always block, with no override.

After merging, post a one-line summary for the founder: what merged, and any follow-up issues created.

## Review rounds and debt (decision 0035)

- **P0/P1 findings always block.** Fix them in the pull request, in any round.
- **P2/P3 findings are fixed in rounds 1–2.** From round 3, open a `review-followup` issue instead (link it in the reply, then resolve the thread). If unsure of a severity, treat it as P1.
- **One re-review per batch of fixes:** fix every open finding, push once, then request one re-review.
- **Debt limits:** no stage gate passes with open `review-followup` issues; more than 5 open pauses feature work. `noticed` issues are triaged at each stage gate and don't count towards the limit.
- **Holistic audit at each stage gate:** one whole-repository review for contradictions, stale statements and debt, with findings cleared in a tidy-up pull request.

## Keeping agent cost down

- **Opus 5.5 plans and reviews; Sonnet 5.5 does everything else** (decision 0035).
- Keep pull requests focused on one topic, but group small related documentation changes into one pull request.
- Read only the files a task needs; don't reload whole documents to change one line.
- Run `make check` and the pre-push review before pushing, so Codex rounds are rare.
- Wait for reviews and checks in the background with long intervals; don't poll repeatedly.
- Before a long or expensive task, say so and suggest a cheaper route if there is one.
- Coding-agent spend and review rounds per pull request are reported in the weekly review (no fixed cap).

## Commands

None yet. When code exists: `make check` (every automated check, same as CI, including InspectCode), `make test` and `make generate`.
