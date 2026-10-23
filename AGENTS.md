# AGENTS.md

Shared instructions for every AI agent on this project. `CLAUDE.md` is a symbolic link to this file, so Claude Code and OpenAI Codex read the same text. Edit **this** file only.

- **Claude Code** builds and merges: follow "When building" and "When merging".
- **OpenAI Codex** reviews pull requests: follow "When reviewing".

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

## When building (Claude Code)

- One issue per session, on a branch named `type/short-description` (e.g. `feat/buyer-story-costs`).
- Start from the issue's spec and acceptance criteria. If the spec is unclear or conflicts with a decision, stop and ask rather than guess.
- Small vertical slices. Tests first for anything numeric or legal, using the test-first skill (decision 0031).
- **Noticed, not changed:** list anything spotted outside the task under that heading in the pull request description, and open a `review-followup` issue for each. Don't fix unrelated things in the same change.
- **Stop and ask** when a task needs an undecided domain rule (open a decision issue instead of inventing one), a new dependency, or work well beyond the issue. **Stop after 3 failed attempts** at the same problem and report what was tried.
- **Stop what you start:** servers, watchers and temporary worktrees.
- **Data sources:** never scrape or copy listing content (decision 0028). Outside services go through adapters that label values Live, Cached, Fallback or Unavailable, and live-service tests stay out of the merge gate (decision 0029).
- **Result type:** use HomeScout's own `Result` for expected failures only; programming errors throw (decisions 0021, 0032).
- Before using a framework or package API, check its official documentation for the pinned version via `docs/references/third-party.md`, not memory. When adding a dependency or changing a version, update that file in the same pull request (decision 0024).
- For a major version update, read the official migration notes, fix breaking changes in the same pull request, and summarise them in the description.
- Commit messages: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
- Pull request description: what changed and why, how it was tested, and **any assumptions you made**.
- Update the docs and decision records affected by the change.
- **Pre-flight check before opening a pull request:** search the repository for every term, decision ID, rule and figure the change touches, and fix any contradiction or stale statement in the same pull request. Check new facts against their sources. Say in the pull request description what was checked. Most review rounds come from cross-document contradictions, so this is the main way to keep reviews to one round.
- Ask the founder before installing dependencies, changing infrastructure, cloud resources or repository settings. Never push to `main`.

## Teach as you build (decision 0026)

The founder is learning the languages, frameworks and tools through this project.
- Every pull request description includes **"How it works"** (plain language) and **"Concepts to learn"** (links to the official documentation pages for what it uses).
- When the founder asks why, answer in plain language with a small example and a link to the official source.
- For each significant slice, offer a short walkthrough: which files matter, how data flows, why it was built this way, and the alternatives. The founder learns by understanding, not by writing the code.
- AI-layer work follows decision 0025: each implementation links the official documentation it follows.

## When reviewing (Codex)

Check in priority order:
1. **Correctness:** bugs, wrong logic, unhandled states. For money, tax, dates and lease terms, recalculate the figures and check them against the cited source.
2. **Breaches of the rules above.**
3. **Spec match:** does the change meet the linked acceptance criteria, including mobile, keyboard access and edge states?
4. **Tests:** are the important cases covered, especially numbers and edge states?
5. **Clarity:** could the founder understand and maintain this? Flag unnecessary complexity.

How to report:
- Most serious findings first. For each: file and line, what's wrong, a concrete example of the failure, and a suggested fix.
- Give each finding a severity: **P0/P1** (wrong behaviour, wrong figures, legal or security risk, broken rules above) or **P2/P3** (wording, consistency, minor gaps). Use plain language. Say "no issues found" if there are none.
- **First review: one complete pass.** Review the whole pull request at once, including its knock-on effects: other files in the repository that the change contradicts or makes stale (search for the same terms, decision IDs and rules). Report every finding in that first review rather than spreading them over rounds.
- **Re-reviews: fixes only.** Check that the fixes are correct and look at newly changed lines. Raise new P2/P3 points only on lines changed since the last review; raise P0/P1 issues anywhere. Don't re-raise issues already deferred to a follow-up issue.
- Don't push commits or approve merges.

## When merging (Claude Code, decisions 0015 and 0016)

Claude Code may merge a pull request (squash merge) only when **all** of these are true:
1. Codex has reviewed the **latest commit** of the pull request, or, while Codex is unavailable, a documentation-only pull request has had the fallback review (decision 0033). A pull request rebased with no content change may rely on its earlier review if `git range-diff` shows every commit unchanged.
2. Every Codex finding is fixed, answered with a reason, or deferred under "Review rounds" below, and every review thread is resolved.
3. Every check on the pull request has passed: none failing, none still running, whether or not GitHub marks it as required.
4. The pull request doesn't fall under the founder-only list below.

**Founder merges these:**
- Changes to `LICENSE`, repository settings, CI permissions or this file's merge rules (including the review fallback, decision 0033).
- New or changed tax, legal, tenancy or privacy rule tables.
- Infrastructure, cloud resources or anything that changes running costs.
- Adding a new dependency. (Version updates to existing dependencies are merged by Claude Code after checks and Codex review, decision 0024.)
- Any pull request where Claude Code disagrees with a finding and proposes to dismiss it as wrong (not merely defer it). The founder decides whether the finding stands.

P0/P1 findings always block, with no override: they must be fixed before anyone merges.

After merging, post a one-line summary for the founder: what merged, and any follow-up issues created.

## Review rounds (decisions 0015 and 0016)

Optimised for quality, speed and agent cost:
- **P0/P1 findings always block.** Fix them in the pull request, in any round.
- **P2/P3 findings are fixed in the pull request only in the first two review rounds.** From round 3 onward, open a follow-up issue labelled `review-followup` instead (link it in the thread reply, then resolve the thread). If unsure of a finding's severity, treat it as P1.
- **Batch follow-ups:** clear open `review-followup` issues together in one tidy-up pull request, at least once per roadmap stage. **No stage gate passes with open follow-ups**, and if more than 5 are open, clear them before starting new feature work.
- **Holistic audit at each stage gate:** before signing off a stage, run one whole-repository review for contradictions, stale statements and debt (ask Codex with a comment describing the scope, or use Claude Code's review), and clear what it finds in the tidy-up.
- **One re-review per batch of fixes:** fix every open finding, push once, then request one Codex re-review. Don't request reviews commit by commit.

## Keeping agent cost down

- Keep pull requests focused on one topic, but group small related documentation changes into one pull request rather than several.
- Read only the files a task needs; don't reload whole documents to change one line.
- Wait for reviews and checks in the background with long intervals; don't poll repeatedly.
- Use the most capable model for planning, decisions and review triage; a faster, cheaper model is acceptable for routine, well-specified implementation (decision 0012).
- Before a long or expensive task (large refactor, many files, repeated review rounds), say so and suggest a cheaper route if there is one.

## Commands

None yet. Add build, test and lint commands here when `packages/fixtures`, `packages/cost-engine` and `apps/web` exist.
