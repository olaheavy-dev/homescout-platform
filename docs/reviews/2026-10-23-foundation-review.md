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

The reviewed AI library and chatbot sample have no licence, so no code, configuration, file layout or wording is reused. Their **design ideas** are useful and are recorded here in our own words, alongside the public Microsoft documentation that describes the same techniques. Original source locations are listed only in the private local references file (see `AGENTS.md`, "Private reference sources").

### How the reviewed library integrates with Microsoft Foundry (design ideas)
- **Two hosting paths behind one facade:** the same public interface can run an agent hosted in Microsoft Foundry (through the Foundry projects SDK and its agents/Responses API) or a lightweight local agent calling a model directly. A small enum chooses the path, and each path is a separate implementation registered with keyed dependency injection.
- **Narrow public surface:** callers see only facades, records and exceptions; provider implementations are internal, so swapping providers doesn't ripple through the code.
- **One registration call:** a single `AddX(...)` extension wires everything up, taking the Foundry project endpoint and an Entra ID credential (no API keys in code).
- **Agents defined as validated configuration:** each agent (instructions, model settings, grounding source, allowed tools) is described in a config file and validated against a schema at startup, with tests for invalid configurations.
- **Tools and grounding at provisioning time:** retrieval (Azure AI Search) and tool servers (MCP) are attached when a Foundry agent is created, with an allow-list of tools.
- **Errors as values:** expected failures return a result type rather than throwing; for streaming, a failure to start fails the result, while errors during the stream arrive as explicit error events.
- **Typed citations** are mapped from provider responses into the library's own records.
- **Evaluation (from the chatbot sample):** a reviewed question set with reference answers and cited pages; model-graded equivalence and groundedness scores; a stored baseline with tolerances; checks that the grading model itself is calibrated; secret scrubbing; token cost per run; and personal data redaction before text is sent to a model.

### What HomeScout should do differently
- Keep provider SDK types out of HomeScout's own interfaces; use `Microsoft.Extensions.AI` (`IChatClient`, `IEmbeddingGenerator`) as the plug-in point, so Foundry, OpenAI or a cheaper provider (decision 0022) are adapters, not dependencies.
- Make interfaces **task-shaped** (explain a finding, draft a question, check a reply, extract a document, home chat), not generic chat, each returning grounded-with-citations, not-known or refused.
- Make capability gaps explicit: if a provider can't ground or cite, the task returns not-known rather than an answer without citations.
- Tools are denied unless allow-listed; per-user isolation is enforced at the authorisation boundary: the user scope comes from the authenticated identity on the server (never from a value the caller supplies), every retrieval adapter applies the user partition or filter inside its own implementation, and tests try to read another user's documents and must fail.
- Keep prompts versioned (embedded resources) with structured-output schemas; no API keys in configuration records; conversation state persisted, not held in memory.
- Turn evaluation into a **gate**: prompt or model changes don't merge if scores fall below the baseline.

### Guards and structure
- Every claim must cite a figure ID or document page; every number in AI output must match a supplied figure; documents are passed as quoted data.
- Dependency direction: cost engine and domain ← application ← AI ← API. Nothing points the other way (enforced by decision 0021's architecture tests).
- Proposed projects at stage 6: `HomeScout.Ai.Abstractions` (task interfaces, no SDK types), `HomeScout.Ai` (implementations built with Microsoft Agent Framework, decision 0023, plus prompts and the citation and number guards), one adapter project per chosen provider (for example `HomeScout.Ai.Foundry`), one retrieval adapter (decision AI-02), and `HomeScout.Ai.Evals`.

### Public references
- [Microsoft.Extensions.AI](https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai): the provider-neutral `IChatClient` abstraction
- [Microsoft.Extensions.AI evaluation libraries](https://learn.microsoft.com/en-us/dotnet/ai/evaluation/libraries): quality and groundedness evaluation
- [Microsoft Foundry SDK overview](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview) and [Azure.AI.Projects for .NET](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.projects-readme): connecting to a Foundry project
- [Foundry Agent Service overview](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview): hosted agents, tools and grounding
- [.NET dependency injection](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection): including keyed services
