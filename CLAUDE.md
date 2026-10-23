# CLAUDE.md

Instructions for Claude Code, the main implementation agent on this project (decision 0012). OpenAI Codex reviews pull requests using `AGENTS.md`; keep the shared rules in both files in step.

## What this project is

HomeScout (private code name; public name not chosen) is a home decision workspace for people **buying or renting in England**: check a home, see the real cost, compare homes, and track questions and answers until they decide. It is a portfolio and learning project for its founder, kept commercially viable for later.

Read before working:
- `docs/design/02_Product_Research_and_Direction.md`: product decisions and scope
- `docs/design/03_Prototype_and_Image_Direction.md`: prototype behaviour and design
- `docs/design/04_Project_Goals_and_Delivery.md`: roadmap (§9) and ways of working (§10)
- `docs/decisions/`: accepted decisions. Don't contradict one; propose a new record instead.

Current stage: see the README and `docs/planning/`.

## Non-negotiable rules

1. **No invented facts.** Never make up property data, legal or tax rules, sources, dates or competitor claims. If something isn't known, the product says so.
2. **No hand-typed figures.** Every number in fixtures, UI or docs comes from the calculation script or the cost engine.
3. **Rules come from cited sources.** Tax, tenancy and lease rules live in versioned tables with a source URL and effective date. Flag rule changes for founder review.
4. **The product never says a home is "verified", "safe" or "approved"**, and AI never calculates numbers. Follow decision 0004 for AI and chat behaviour.
5. **Public repository, all rights reserved.** Never commit secrets, API keys, real personal data, real customer documents or licensed datasets. Use the synthetic fixtures.
6. **England first.** Other UK nations show "not yet covered". Keep a nation field in data; don't hard-code English rules into shared code.
7. **Ask before** installing dependencies, changing infrastructure or cloud resources, or pushing. Never push to `main`.

## How to work

- One issue per session, on a branch named `type/short-description` (e.g. `feat/buyer-story-costs`).
- Start from the issue's spec and acceptance criteria. If the spec is unclear or conflicts with a decision, stop and ask rather than guess.
- Small vertical slices. Tests first for anything numeric or legal.
- Commit messages: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
- Pull request description: what changed and why, how it was tested, and **any assumptions you made**.
- Update docs and decision records affected by the change.
- When explaining choices to the founder, use plain language: what each option means in practice, and a clear recommendation.

## Commands

None yet. Add build, test and lint commands here when `apps/web` and `packages/fixtures` exist.
