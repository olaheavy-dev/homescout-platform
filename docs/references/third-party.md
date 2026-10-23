# Third-party documentation

Official documentation for the tools and packages HomeScout uses or has chosen. **Check here before using an API from memory:** frameworks change between versions, and agents tend to write code for older ones.

**Rules**
- Link only to official documentation. Don't copy documentation into the repository.
- Add an entry in the same pull request that adds a dependency, with the pinned version.
- Update the version column whenever a version changes.
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
| NUnit | Tests | Pinned in the first implementation PR | 0021 | [NUnit documentation](https://docs.nunit.org/) |
| NUnit analysers | Test code checks | Pinned in the first implementation PR | 0021 | [NUnit Analyzers](https://docs.nunit.org/articles/nunit-analyzers/NUnit-Analyzers.html) |
| NetArchTest | Architecture rules | Pinned in the first implementation PR | 0021 | [NetArchTest](https://github.com/BenMorris/NetArchTest) |
| JSON Schema | Validating sample data | Draft version chosen in the first implementation PR | 0018 | [JSON Schema docs](https://json-schema.org/docs) |
| GNU Make | Single command entry point | Version on the build machine | 0021 | [GNU Make manual](https://www.gnu.org/software/make/manual/) |
| Next.js | Frontend framework | Pinned at stage 4 (FE-01) | 0020 | [Next.js docs](https://nextjs.org/docs) |
| React | UI library under Next.js | Pinned at stage 4 | 0020 | [React reference](https://react.dev/reference/react) |
| TypeScript | Frontend language | Pinned at stage 4 | 0020 | [TypeScript docs](https://www.typescriptlang.org/docs/) |
| GitHub Actions | Automated checks and deployment | — | 0013, IN-04 | [GitHub Actions](https://docs.github.com/en/actions), [security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) |
| Claude Code | Building agent | — | 0012 | [Claude Code docs](https://code.claude.com/docs/en/overview) |
| OpenAI Codex code review | Reviewing agent | — | 0012, 0015 | [Codex GitHub integration](https://developers.openai.com/codex/integrations/github) |

## Planned for later stages (not yet decided)

Listed so agents read the right documentation when these stages start. Versions and final choices come with each decision.

| Tool / package | Likely use | Decision | Documentation |
|---|---|---|---|
| ASP.NET Core minimal APIs | The API (stage 6) | BE-01, BE-02 | [Minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis) |
| PostgreSQL | Database (stage 6) | DA-03 | [PostgreSQL docs](https://www.postgresql.org/docs/) |
| PostGIS | Geospatial queries (stage 6) | DA-03 | [PostGIS documentation](https://postgis.net/documentation/) |
| Microsoft.Extensions.AI | Provider-neutral AI interface (stage 6) | AI-01, AI-04 | [Microsoft.Extensions.AI](https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai) |
| Microsoft.Extensions.AI evaluation | AI quality tests (stage 6) | AI-03 | [Evaluation libraries](https://learn.microsoft.com/en-us/dotnet/ai/evaluation/libraries) |
| Microsoft Foundry SDK | One AI provider candidate (stage 6) | AI-01, 0022 | [SDK overview](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview), [Azure.AI.Projects for .NET](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.projects-readme) |
