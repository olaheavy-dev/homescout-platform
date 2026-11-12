# P8: remove .NET (issue #195)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) port step P8 and item 11e; **founder merge** (CI, Dependabot, `.claude/settings.json`, dependency-review exemptions, deleting a stack). Founder chose "Do P8 now" on 12 Nov 2026. **Condition met:** all 526 rows of the [port ledger](../../planning/python-port-ledger.md) have a Python test or a written reason. **Builder:** Sonnet; **review:** Opus before push.

## Goal
Delete every .NET file and step, so `make check` and CI run Python only, with no loss of checks: every C# check now has a Python counterpart (ledger), `generated-check` keeps the byte-identical `costs.json` proof, `make mutate` keeps mutation testing, and CodeQL already scans Python.

## Delete
- `packages/cost-engine/` (engine, generator and their tests), `packages/fixtures/tools/Vestagraph.Fixtures.Validator/`, `packages/fixtures/tests/Vestagraph.Fixtures.Tests/`, `packages/specs/Vestagraph.Specs.Tests/` (**not** `packages/specs/tests/`, the Python runner).
- Root: `Vestagraph.slnx`, `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `nuget.config`, `stryker-config.json`, `.config/dotnet-tools.json` (and `.config/` if then empty).
- `.github/workflows/dependency-submission.yml` (NuGet only; not a required check).
- `.editorconfig`: the C#-only sections (keep the general `[*]`, JSON/YAML and Markdown rules; drop `slnx`, `csproj`, `props`, `targets`, `config` from the globs).
- `.gitignore`: .NET-only entries (`bin/`, `obj/`, `TestResults/` and similar) once nothing produces them.

## Change
- **Makefile:** drop the .NET exports, variables and steps (`dotnet tool restore`, `dotnet restore`, `dotnet build`, `dotnet format`, `inspect`, `dotnet test`, `mutate-dotnet`, `MUTATION_REPLAY`, .NET parts of `clean`); `check` becomes `restore build format-check generated-check validate lint test`; header comment and `help` updated.
- **CI (`ci.yml`):** remove `actions/setup-dotnet`. Required checks stay satisfied: `make check`, `Dependency review`, `actionlint`, `zizmor`, `CodeQL`.
- **`dependency-review.yml`:** remove the NuGet exemptions and their comments (JetBrains, JsonSchema.Net family, NetArchTest, Mono.Cecil) and the "dependency-submission supplies NuGet data" comment and `retry-on-snapshot-warnings` if it only served that; keep the PyPI exemptions, PSF-2.0 and the unlicensed step.
- **`dependabot.yml`:** remove the `nuget` and `dotnet-sdk` ecosystems; remove the dependency-submission action from `actions-zero-x`.
- **`.claude/settings.json`:** remove .NET-only allow and ask rules (`dotnet …`, `jb`); keep everything else (push rules untouched).
- **Docs** (search for `dotnet`, `.NET`, `C#`, `NuGet`, `Reqnroll`, `NUnit`, `FsCheck`, `Stryker`, `InspectCode`, `JsonSchema.Net`, `NetArchTest`, `slnx`, `global.json`, `mutate-dotnet` and fix every current-state statement): `AGENTS.md` (Commands rewritten for Python only; rule 2's engine wording; "When building" mentions of InspectCode; test naming; telemetry line), `README.md` (build line: uv only), `docs/architecture/README.md` (built pieces), `docs/references/third-party.md` (remove .NET rows; keep a one-line history note), `docs/specs/README.md` (Reqnroll sections removed), `packages/fixtures/README.md`, `packages/fixtures/test-cases/README.md` if it names C#, `docs/planning/python-port-ledger.md` (a "Complete: P8 merged" note at the top; rows stay as the record). Decision records, reviews and dated plans are history: change only status lines.
- **Decision status lines and register:** 0021 → Superseded by 0049 (fully, at P8); 0019 and 0032 (C# type gone; principle stands in Python); 0043 (Reqnroll withdrawn); 0035 point 9 (.NET packages withdrawn); 0042 note unchanged. Register: BE-04 Superseded by 0049; BE-05 (Python `Result`); BE-07 (JsonSchema.Net withdrawn; Python validator); BE-08, BE-09 and WW-13 lapse (their packages are gone) → "Superseded by 0049 (P8: package removed)"; BE-22 (NuGet exemptions removed); WW-14 (dependency-submission action gone from `actions-zero-x`); 0050/AGENTS.md references to `make check` still hold.
- **0049 item 11e re-check list**, run and reported: `make mutate` passes (score ≥ 85); `generated-check` passes (port proof); CodeQL's required check covers Python (default setup languages include `python`).

## Founder steps
Remove `csharp` from CodeQL's default setup languages before the PR opens, so its checks run clean (done 12 Nov 2026, founder's choice in a prompt window); after merge: close #59-#61 leftovers if any; noticed issues #202 and #210 close with this PR.

## Acceptance
- No `.cs`, `.csproj`, `.slnx`, `.props`, `global.json` or `nuget.config` left; `git grep` finds no current-state .NET instruction outside history (decision records, reviews, dated plans, the ledger's rows).
- `make check` passes with Python only; `make mutate` passes; `costs.json` unchanged; mypy, ruff and pytest file counts unchanged by the deletion.
