# Third-party documentation

Official documentation for the tools and packages HomeScout uses or has chosen. **Check here before using an API from memory:** frameworks change between versions, and agents tend to write code for older ones.

**Rules**
- Link only to official documentation. Don't copy documentation into the repository.
- Add an entry in the same pull request that adds a dependency, with its major version.
- The version column records **major versions**; exact versions live in the lock files. Update it in the same pull request when a major version changes (decision 0035). Patch and minor updates don't touch this file.
- Official data sources (energy certificates, sold prices, planning, flood, transport) are listed with their limits in doc 02 §7, not here.

## In use or chosen

| Tool / package | Used for | Version | Decision | Documentation |
|---|---|---|---|---|
| .NET SDK and runtime | Cost engine, later the API | 10.0 (SDK pinned in `global.json`) | 0020, 0021 | [What's new in .NET 10](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview) |
| C# | Backend language | Version shipped with .NET 10 | 0020 | [C# documentation](https://learn.microsoft.com/en-us/dotnet/csharp/) |
| `global.json` | Pinning the SDK | — | 0021 | [global.json overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) |
| Solution files (`.slnx`) | Solution structure | — | 0021 | [dotnet sln](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln) |
| Central package management | One place for package versions | — | 0021 | [Central package management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) |
| NuGet lock files | Reproducible restores | — | 0021 | [Locking dependencies](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files) |
| .NET code analysis | Strict build settings | — | 0021 | [Code analysis overview](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview) |
| System.Text.Json | Reading and writing fixture JSON | Built into .NET 10 | 0018, 0021 | [System.Text.Json overview](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview) |
| NUnit | Tests | 5 | 0021 | [NUnit documentation](https://docs.nunit.org/) |
| NUnit analysers | Test code checks | 4 | 0021 | [NUnit Analyzers](https://docs.nunit.org/articles/nunit-analyzers/NUnit-Analyzers.html) |
| NetArchTest | Architecture rules | Pinned in the first implementation PR | 0021 | [NetArchTest](https://github.com/BenMorris/NetArchTest) |
| JSON Schema | Validating sample data | 2020-12 | 0018, BE-07 | [JSON Schema docs](https://json-schema.org/docs) |
| Microsoft.Testing.Platform (with NUnit3TestAdapter and coverlet.MTP) | Test runner for NUnit tests and coverage | Platform 2 (via the adapter), NUnit3TestAdapter 6, coverlet.MTP 10 (MIT; enabled with `--coverlet`) | 0027 | [dotnet test](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test), [NUnit and MTP](https://docs.nunit.org/articles/vs-test-adapter/NUnit-And-Microsoft-Test-Platform.html), [coverlet.MTP](https://github.com/coverlet-coverage/coverlet/blob/master/Documentation/Coverlet.MTP.Integration.md) |
| JetBrains ReSharper Command Line Tools (InspectCode) | Static analysis in `make check` and CI | 2026 (pinned in `.config/dotnet-tools.json`) | 0035 | [Command line tools](https://www.jetbrains.com/help/resharper/ReSharper_Command_Line_Tools.html), [InspectCode](https://www.jetbrains.com/help/resharper/InspectCode.html), [licence](https://www.jetbrains.com/resharper/buy/command_line_license.html) |
| FsCheck | Property-based tests for the cost engine | Pinned in the first implementation PR | 0027 | [FsCheck](https://fscheck.github.io/FsCheck/) |
| `MidpointRounding` | Explicit rounding in money calculations | Built into .NET | 0027 | [MidpointRounding](https://learn.microsoft.com/en-us/dotnet/api/system.midpointrounding) |
| EditorConfig and `dotnet format` | Code style checked in CI | — | 0027 | [Code style options](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/code-style-rule-options), [EditorConfig](https://editorconfig.org/) |
| CodeQL | Security scanning of C#, TypeScript and workflows | GitHub default setup | 0027 | [Configure code scanning](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning) |
| Dependency review action | Blocks vulnerable or disallowed-licence packages in pull requests | 5, pinned by SHA in the workflow | 0027 | [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review), [action](https://github.com/actions/dependency-review-action) |
| actionlint and zizmor | Linting and security checks for workflow files | actionlint 1 (Docker image digest updated by hand, not by Dependabot), zizmor 1 (action 0.8, pinned by SHA) | 0027 | [actionlint](https://github.com/rhysd/actionlint), [zizmor](https://docs.zizmor.sh/), [secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use) |
| Secret scanning and push protection | Blocks secrets from being pushed | Repository setting | 0027 | [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection), [secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning) |
| designer-skills plugin | Design process skills for stages 3–5 (brief, information architecture, tokens, tasks, build, review). Install in Claude Code: `/plugin marketplace add julianoczkowski/designer-skills`, then `/plugin install designer-skills@designer-skills`, then confirm the installed commit matches the pinned one | Commit `c259656c76d9758d7ead46b0d2f125cbe84f8665` (reviewed 23 Oct 2026); a change is a dependency update (0024, 0031) | 0031 | [designer-skills](https://github.com/julianoczkowski/designer-skills) |
| Claude Code subagents and skills | Project agents and skills in `.claude/` | — | 0031 | [Subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills) |
| Mermaid (C4 diagrams) | Architecture diagrams in Markdown | Rendered by GitHub | 0027 | [Diagrams on GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams), [C4 model](https://c4model.com/), [Mermaid C4](https://mermaid.js.org/syntax/c4.html) |
| JsonSchema.Net | Validating fixture files against JSON Schema 2020-12 in `make check` (only the fixture validator uses it, never the cost engine) | 9 (Open Source Maintenance Fee EULA; source is MIT, a fee applies only to binary-release use in revenue-generating activities with annual revenue of US$10,000 or more, otherwise build from source; see BE-08). Dependencies JsonPointer.Net 7 and Json.More.Net 3 have the same licence |  BE-07 | [JsonSchema.Net](https://docs.json-everything.net/schema/basics/)  |
| GNU Make | Single command entry point (its manual blocks automated link checkers; exclude it from lychee) | Version on the build machine | 0021 | [GNU Make manual](https://www.gnu.org/software/make/manual/) |
| Next.js | Frontend framework | Pinned at stage 4 (FE-01) | 0020 | [Next.js docs](https://nextjs.org/docs) |
| React | UI library under Next.js | Pinned at stage 4 | 0020 | [React reference](https://react.dev/reference/react) |
| TypeScript | Frontend language | Pinned at stage 4 | 0020 | [TypeScript docs](https://www.typescriptlang.org/docs/) |
| GitHub Actions (checkout 7, setup-dotnet 6, upload-artifact 7) | Automated checks and deployment; every action pinned by full commit SHA | See workflows | 0013, IN-04 | [GitHub Actions](https://docs.github.com/en/actions), [security hardening](https://docs.github.com/en/actions/reference/security/secure-use) |
| Claude Code | Building agent | — | 0012 | [Claude Code docs](https://code.claude.com/docs/en/overview) |
| OpenAI Codex code review | Reviewing agent | — | 0012, 0035 | [Codex GitHub integration](https://learn.chatgpt.com/docs/third-party/github) |
| Dependabot | Weekly version-update pull requests (`.github/dependabot.yml`: nuget and github-actions, 7-day cooldown, minor and patch grouped apart from major) | Config version 2; also covers the `dotnet-sdk` ecosystem for `global.json` | 0024 | [About version updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates), [options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) |
| Dependency submission action | Sends NuGet dependencies to GitHub's dependency graph so dependency review can see them | 0.2, pinned by SHA in the workflow | 0035 | [Action](https://github.com/advanced-security/component-detection-dependency-submission-action), [component-detection](https://github.com/microsoft/component-detection) |
| lychee | Monthly documentation link check | Action 2, pinned by SHA in the workflow | 0024 | [lychee](https://lychee.cli.rs/) |
| Microsoft Agent Framework | AI agents and workflows (stage 6) | Pinned at stage 6 | 0023 | [Overview](https://learn.microsoft.com/en-us/agent-framework/overview/), [version 1.0 announcement](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/) |

## Planned for later stages (not yet decided)

Listed so agents read the right documentation when these stages start. Versions and final choices come with each decision.

| Tool / package | Likely use | Decision | Documentation |
|---|---|---|---|
| ASP.NET Core minimal APIs | The API (stage 6) | BE-01, BE-02 | [Minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis) |
| PostgreSQL | Database (stage 6) | DA-03 | [PostgreSQL docs](https://www.postgresql.org/docs/) |
| PostGIS | Geospatial queries (stage 6) | DA-03 | [PostGIS documentation](https://postgis.net/documentation/) |
| Microsoft.Extensions.AI | Provider-neutral AI interface (stage 6) | AI-01, AI-04 | [Microsoft.Extensions.AI](https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai) |
| Microsoft.Extensions.AI evaluation | AI quality tests (stage 6) | AI-03 | [Evaluation libraries](https://learn.microsoft.com/en-us/dotnet/ai/evaluation/libraries) |
| Aspire | Local orchestration and dashboard for traces, metrics and logs (stage 6) | 0025, OP-01 | [What is Aspire](https://aspire.dev/get-started/what-is-aspire/), [dashboard](https://aspire.dev/dashboard/overview/) |
| OpenTelemetry for .NET | Tracing, metrics, logs (stage 6) | 0025, OP-01 | [OpenTelemetry .NET](https://opentelemetry.io/docs/languages/dotnet/), [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [.NET observability](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/observability-with-otel) |
| Agent Framework capabilities | Observability, evaluation, safety, middleware, workflows, human-in-the-loop, routing, streaming (stage 6) | 0023, 0025 | See the table in [decision 0025](../decisions/0025-ai-platform-capabilities.md) |
| Azure AI Content Safety | Candidate for injection detection and content filtering (cost-first) | 0025, 0022 | [Overview](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview), [Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) |
| .NET vector stores | Retrieval and semantic caching (stage 6) | AI-02, 0025 | [Vector stores in .NET](https://learn.microsoft.com/en-us/dotnet/ai/vector-stores/overview) |
| OWASP Top 10 for LLM applications | Security checklist for AI features | 0025 | [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) |
| Microsoft Foundry SDK | One AI provider candidate (stage 6) | AI-01, 0022 | [SDK overview](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview), [Azure.AI.Projects for .NET](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.projects-readme) |
