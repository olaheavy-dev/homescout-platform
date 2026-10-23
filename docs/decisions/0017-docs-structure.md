# 0017: Documentation folder structure and naming

**ID:** WW-06  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 1

## Context
The founder asked for a tidy folder structure for the docs. Product documents, the asset register and eight images with spaces in their names were mixed in `docs/design/`, documents used mixed naming styles, and there was no index.

## Options
- **Leave as is:** no churn, but harder to navigate as the project grows.
- **Reorganise by purpose with consistent names and an index (chosen):** one-off link updates, then a clear home for every kind of file.
- **Move everything into a wiki or external tool:** loses review history and the portfolio record in the repository.

## Recommendation
Reorganise by purpose, keep the document numbers that other text refers to ("doc 03 §2"), and add an index.

## Decision
Founder's request: "make sure we have a tidy folder structure for the docs." Adopted the structure and naming rules in [`docs/README.md`](../README.md):
- `docs/product/` for the numbered product and delivery documents, renamed to lowercase-with-hyphens (`01-` to `04-`).
- `docs/assets/` for the asset register (`README.md`, formerly `ASSETS.md`) and `docs/assets/concepts/` for the concept images, renamed by screen (`01-public-homepage.png` and so on), with original export names kept in the asset register and doc 03 §2.
- `docs/decisions/`, `docs/planning/` and `docs/reviews/` unchanged.
- Future: `docs/specs/` (stage 3) and `docs/learning-log.md`.

## Consequences
- All links were updated in the same change; a link check passed.
- New files follow the naming rules in `docs/README.md`.
- Old paths in closed pull requests and early issues no longer resolve; open issues are updated to the new paths.
