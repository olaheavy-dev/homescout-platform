# AGENTS.md

Shared instructions for every AI agent on this project. `CLAUDE.md` is a symbolic link to this file, so Claude Code and OpenAI Codex read the same text. Edit **this** file only.

- **Claude Code** builds and merges: follow "When building" and "When merging".
- **OpenAI Codex** reviews pull requests: follow "When reviewing".

## What this project is

HomeScout (private code name; public name not chosen) is a home decision workspace for people **buying or renting in England**: check a home, see the real cost, compare homes, and track questions and answers until they decide. It is a portfolio and learning project for its founder, kept commercially viable for later. Public repository, all rights reserved.

Read before working:
- `docs/design/02_Product_Research_and_Direction.md`: product decisions and scope
- `docs/design/03_Prototype_and_Image_Direction.md`: prototype behaviour and design
- `docs/design/04_Project_Goals_and_Delivery.md`: roadmap (§9) and ways of working (§10)
- `docs/decisions/`: accepted decisions. Don't contradict one; propose a new record instead.

The current stage is in the README and `docs/planning/`.

## Rules for every agent

1. **No invented facts.** Never make up property data, legal or tax rules, sources, dates or competitor claims. If something isn't known, the product says so.
2. **No hand-typed figures.** Every number in fixtures, UI or docs comes from the calculation script or the cost engine.
3. **Rules come from cited sources.** Tax, tenancy, lease and privacy rules live in versioned tables or records with a source URL and effective date.
4. **The product never says a home is "verified", "safe" or "approved"**, and AI never calculates numbers. Follow decision 0004 for AI and chat behaviour.
5. **Public repository.** Never commit secrets, API keys, real personal data, real customer documents or licensed datasets. Use the synthetic fixtures. Record every image or media file in `docs/design/ASSETS.md` before committing it.
6. **England first.** Other UK nations show "not yet covered". Keep a nation field in data; don't hard-code English rules into shared code.
7. **Missing data is never shown as zero**, a favourable value or a clean result.
8. **Plain language for the founder.** When explaining options or decisions, say what each option means in practice and give a clear recommendation.

## When building (Claude Code)

- One issue per session, on a branch named `type/short-description` (e.g. `feat/buyer-story-costs`).
- Start from the issue's spec and acceptance criteria. If the spec is unclear or conflicts with a decision, stop and ask rather than guess.
- Small vertical slices. Tests first for anything numeric or legal.
- Commit messages: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
- Pull request description: what changed and why, how it was tested, and **any assumptions you made**.
- Update the docs and decision records affected by the change.
- Ask the founder before installing dependencies, changing infrastructure, cloud resources or repository settings. Never push to `main`.

## When reviewing (Codex)

Check in priority order:
1. **Correctness:** bugs, wrong logic, unhandled states. For money, tax, dates and lease terms, recalculate the figures and check them against the cited source.
2. **Breaches of the rules above.**
3. **Spec match:** does the change meet the linked acceptance criteria, including mobile, keyboard access and edge states?
4. **Tests:** are the important cases covered, especially numbers and edge states?
5. **Clarity:** could the founder understand and maintain this? Flag unnecessary complexity.

How to report:
- Most serious findings first. For each: file and line, what's wrong, a concrete example of the failure, and a suggested fix.
- Separate **must fix** from **suggestions**. Use plain language. Say "no issues found" if there are none.
- Don't push commits or approve merges.

## When merging (Claude Code, decision 0015)

Claude Code may merge a pull request (squash merge) only when **all** of these are true:
1. Codex has reviewed the **latest commit** of the pull request.
2. Every Codex finding is either fixed or answered with a reason, and every review thread is resolved.
3. All required checks pass.
4. The pull request doesn't fall under the founder-only list below.

**Founder merges these:**
- Changes to `LICENSE`, repository settings, CI permissions or this file's merge rules.
- New or changed tax, legal, tenancy or privacy rule tables.
- Infrastructure, cloud resources or anything that changes running costs.
- Adding or upgrading dependencies.
- Any pull request where a Codex finding was deliberately not fixed.

After merging, post a one-line summary for the founder: what merged and anything they should know.

## Commands

None yet. Add build, test and lint commands here when `apps/web` and `packages/fixtures` exist.
