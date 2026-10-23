# 0013: Repository and tracking conventions

**ID:** WW-03  
**Status:** Accepted (partly superseded: calculation placement by [0019](0019-cost-engine-in-csharp.md))  
**Date:** 2026-10-23  
**Stage:** 1

## Context
How the repository and task tracking are organised.

## Options
- **Standard setup:** One repo; protected main; pull requests; GitHub Issues and a project board.

## Recommendation
Standard setup.

## Decision
One repository: `apps/web` (prototype, then frontend), `packages/fixtures` (sample data, calculation script, test cases), `docs/`, `infra/` later, `apps/api` once the backend is decided. `main` is protected (pull request and passing checks required). Branches named `type/short-description`. Commit messages like `feat:`, `fix:`, `docs:`, squash-merged. GitHub Issues and one project board with a column per roadmap stage.

## Consequences
First action: a pull request merging `docs/product-exploration` into `main`. Future large images and design files use Git LFS or compressed copies.
