# Best-practice audit

**Date:** 2026-10-23  
**Scope:** All decisions (0001–0026), docs 02–04, `AGENTS.md`, the reference documents and the live GitHub settings, compared with current official guidance. All links were checked on the audit date.  
**Outcome:** "Do now" items were adopted in decision [0027](../decisions/0027-stage-2-engineering-hardening.md). The rest are recorded here and linked from their stages in doc 04.

## Fixed by this audit
- GitHub settings didn't match the documents: secret scanning, push protection, Dependabot security updates and private vulnerability reporting were off, and more merge styles were allowed than the squash-only convention. Now applied (0027).
- Several stage 2 decisions needed CI before stage 4. A minimal CI now starts in stage 2 (0027).
- Money rounding was under-specified; C#'s default midpoint rounding is banker's rounding. Every rule now names its rounding mode and source (0027).
- Two schema sources (JSON Schema and zod) would drift. TypeScript types are generated from the one JSON Schema.
- Paid entitlements were described as feature flags. They are business rules; flags are only for gradual rollout (doc 04 §5, CO-01).
- Version updates were proposed immediately. A 7-day wait now guards against freshly published malicious releases (0027).
- Several documentation links had moved; they are updated.

## Plan for its stage

| Stage | Practice | What it is | Official documentation |
|---|---|---|---|
| End of 2, then each gate | **Mutation testing (Stryker.NET)** on the cost engine only, on a schedule | Plants small deliberate bugs to prove the tests catch them | [Stryker.NET](https://stryker-mutator.io/docs/stryker-net/introduction/) |
| 4 | **One schema → TypeScript types**, validated with the same schema | No duplicate schema definitions | [json-schema-to-typescript](https://github.com/bcherny/json-schema-to-typescript), [Ajv](https://ajv.js.org/) |
| 4 | **Frontend quality gates** (FE-04) | Accessibility linting, Playwright with axe, Lighthouse performance budgets | [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing), [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y), [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) |
| 4/6 | **Build provenance and SBOM** | A signed record of which workflow built an image, plus its package list; the approval gate before images go live on the server (0022) | [Artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [SBOM export](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom) |
| 6 (BE-02) | **OpenAPI → TypeScript client, with breaking-change checks** | One OpenAPI stack, generated frontend types, CI fails on accidental API breaks | [ASP.NET Core OpenAPI](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/aspnetcore-openapi), [openapi-typescript](https://openapi-ts.dev/), [oasdiff](https://github.com/oasdiff/oasdiff) |
| 6 | **Testable time** (`TimeProvider`) | A clock tests can control, for jobs, change detection, retention and caches | [TimeProvider](https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview), [FakeTimeProvider](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.time.testing.faketimeprovider) |
| 6 | **Validated settings and local secrets** | Typed settings checked at startup; local secrets outside the repository | [Options pattern](https://learn.microsoft.com/en-us/dotnet/core/extensions/options), [app secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) |
| 6 (step 4) | **HTTP resilience** | Standard retries, timeouts and circuit breakers for outside services | [HTTP resilience](https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience) |
| 6 (step 4) | **Log redaction and source-generated logging** | Puts the "no addresses in logs, IPs anonymised" rule (0014) into code | [Data redaction](https://learn.microsoft.com/en-us/dotnet/core/extensions/data-redaction), [logging source generation](https://learn.microsoft.com/en-us/dotnet/core/extensions/logging/source-generation), [ICO data protection by design](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/data-protection-by-design-and-by-default/) |
| 6 | **Rate limiting and Problem Details** | Built-in request limits (0014) and a standard error format | [Rate limiting](https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit), [API error handling](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling-api) |
| 6 (DA-03) | **Real-database tests and deliberate migrations** | PostGIS in tests via Testcontainers; migrations applied as reviewed scripts or bundles, not at app startup | [Testcontainers PostgreSQL](https://dotnet.testcontainers.org/modules/postgres/), [applying migrations](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying), [Npgsql EF Core](https://www.npgsql.org/efcore/) |
| 6 | **Health checks and simple SLOs** | `/health` endpoints and two or three service targets; uptime check | [Health checks](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks), [implementing SLOs](https://sre.google/workbook/implementing-slos/) |
| 6 (AI-03) | **AI red-teaming and judge calibration** | Automated attack prompts; checks that an AI grader agrees with human-reviewed labels | [Responsible AI evaluators](https://learn.microsoft.com/en-us/dotnet/ai/evaluation/responsible-ai), [promptfoo red teaming](https://www.promptfoo.dev/docs/red-team/), [PyRIT](https://github.com/Azure/PyRIT) |
| 6 | **Threat model checklist** before accounts and document upload | A structured security checklist | [OWASP ASVS](https://asvs.owasp.org/) |
| Note for 6 | **Invariant globalisation** (0021) suits the cost engine, but server-side en-GB formatting won't work in that mode; keep display formatting in the frontend | | [Globalization config](https://learn.microsoft.com/en-us/dotnet/core/runtime-config/globalization) |

## Optional, later
- **MCP tools through the Agent Framework**, for example read-only cost-engine tools, allow-listed and never with write access ([local MCP tools](https://learn.microsoft.com/en-us/agent-framework/agents/tools/local-mcp-tools), [MCP C# SDK](https://github.com/modelcontextprotocol/csharp-sdk)).
- **Feature flags for gradual rollout** with Microsoft.FeatureManagement on plain configuration ([reference](https://learn.microsoft.com/en-us/azure/azure-app-configuration/feature-management-dotnet-reference)) or OpenFeature ([.NET](https://openfeature.dev/docs/reference/technologies/server/dotnet/)).
- **Error tracking:** start with OpenTelemetry and Aspire; if grouped exceptions are needed, self-host GlitchTip on the server ([GlitchTip](https://glitchtip.com/)) or use a free tier ([Sentry .NET](https://docs.sentry.io/platforms/dotnet/)).
- **Load testing** with k6 before the public API ([k6](https://grafana.com/docs/k6/latest/)).
- **OpenSSF Scorecard** for a public security score ([scorecard-action](https://github.com/ossf/scorecard-action)).
- **Pre-commit hooks** with lefthook for formatting and linting ([lefthook](https://lefthook.dev/)).
- **Dev container** for one-click setup ([containers.dev](https://containers.dev/)).
- **Release notes** with release-please once there are real releases ([release-please](https://github.com/googleapis/release-please)).

## Not adopted, and why
- **Required signed commits:** friction for agent commits; squash merges through GitHub are already signed, and push protection and required pull requests give the real protection.
- **Snapshot tests on money outputs:** they would make the engine's own output the expected answer, breaking the independent-expectations rule; use them only for shapes such as the OpenAPI document.
- **Full arc42 documentation:** too heavy; decision records plus two C4 diagrams are enough.
- **Renovate alongside Dependabot**, **Infracost**, and **paid monitoring or feature-flag services:** duplicate tools or break the cost-first rule.
- **Consumer-driven contract testing (Pact):** one consumer; OpenAPI with generated types and breaking-change checks is enough.
- **Mutation testing on every pull request:** too slow; run it on a schedule.
- **Kubernetes, microservices or a separate flag server:** a modular monolith on the existing server fits the budget and scale.
