# Foundations review

**Date:** 2026-10-23  
**Purpose:** Lessons from the founder's earlier projects and one third-party AI library, reviewed as foundations for HomeScout. HomeScout builds on the patterns and improves them; it does not copy code, configuration or wording. Private project names, code, identifiers and secrets are deliberately left out.

## What was reviewed

| Source | What it is | How HomeScout uses it |
|---|---|---|
| A .NET modular monolith (earlier) | ASP.NET Core API with domain/application/infrastructure layers | Lessons on what to avoid |
| Its successor monorepo (newer) | Cleaned-up .NET foundation, ADRs, agent instructions, strict CI | Main pattern for the C# side (decision 0021) |
| A Next.js web app | App Router, Tailwind, component library, mock/live data modes | Starting point for stage 4 frontend decisions |
| The founder's infrastructure kit for a self-managed server | Terraform, Ansible and container deployment for several apps | Preferred host for running services under decision 0022, after its security issues are fixed; its process habits are reused |
| A third-party AI library and chatbot sample | AI provider abstraction and evaluation tests | **No licence: ideas only, no code.** HomeScout follows Microsoft's public `Microsoft.Extensions.AI` guidance instead |

## Backend (adopted in decision 0021)
Strict build settings, central package versions with lock files, a pinned SDK, a Makefile entry point, NUnit and architecture tests, whole-pence money with fixed rounding rules, no MediatR or SonarAnalyzer (licence restrictions). Lessons from the earlier project: test projects missing from CI because the test list was hand-written; money as a bare decimal; `DateTime` instead of explicit dates; three overlapping OpenAPI stacks; development secrets committed.

## Frontend: inputs for stage 4 (FE-01 to FE-05)
- **Keep:** colour tokens as CSS variables with a "never hard-code colours" rule; route-private components next to their routes; a component gallery page; a single typed fetch wrapper with an error type; tests that assert user-visible text; pinned Node and package manager; least-privilege CI.
- **Improve:** run the tests in CI (the earlier app didn't); enforce the colour rule automatically; keep files small (for example under 400 lines); validate configuration; switch between sample data and the API by configuration, not code edits; add route-level loading, error and not-found pages; add UK (`en-GB`) currency and date formatting; add automated accessibility tests (Playwright with axe, `jsx-a11y`); add security headers; never store login tokens in browser storage.
- **Suggested shape:** `apps/web/src/{app, components, lib/data (sample-data and API sources behind one interface), lib/schemas (zod, validating both), lib/format, styles/tokens.css}`, with unit, component and end-to-end tests.

## Infrastructure: inputs for stage 4 (IN-01 to IN-05)
- **Cost first (decision 0022):** free options, then the founder's existing server, then Azure or another paid service only where needed.
- **Cheapest start:** the Next.js prototype exported as static files on a free static host. Later: the API, PostgreSQL with PostGIS and background jobs on the existing server; Azure options (for example Container Apps scaling to zero, managed PostgreSQL) only if the server can't meet a need.
- HomeScout's repository holds only its own public-safe deployment files; server details and credentials stay in the private infrastructure repository and reach HomeScout as GitHub variables or secrets.
- **Safety habits to keep:** plan/what-if before applying, an explicit confirmation or required reviewer for infrastructure changes, minimal workflow permissions, actions pinned to commit SHAs, immutable image tags, an external uptime check.
- **Improve before HomeScout uses the server:** a proper secret store instead of plain secret files; a gate (approval or signed tag) before new images go live instead of automatic pulls of the latest image; short-lived credentials where the provider allows; remove real IP addresses from its documentation; add basic metrics and spend alerts.
- **Everywhere:** budget alerts at 50%, 80% and 100% on paid services, password-free sign-in (OIDC) for any Azure parts, never run deployments for pull requests from forks, never commit real identifiers or IP addresses.

## AI: inputs for stage 6 (AI-01 to AI-05)
- Use `Microsoft.Extensions.AI` (`IChatClient`) as the provider plug-in point, with task-specific interfaces on top (explain a finding, draft a question, check a reply, extract a document, home chat), each returning grounded-with-citations, not-known or refused.
- Guards: every claim must cite a figure ID or document page; every number in AI output must match a supplied figure; documents are passed as quoted data; tools are denied by default; retrieval always filters by user.
- Evaluation sets with reviewed answers, baselines and tolerances gate prompt or model changes.
- Dependency direction: cost engine and domain ← application ← AI ← API. Nothing points the other way (enforced by decision 0021's architecture tests).
