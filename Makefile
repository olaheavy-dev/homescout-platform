# HomeScout: single entry point for every automated check (decisions 0021, 0035).
# CI runs `make check`; run it before pushing. Works on macOS and Linux with GNU Make 3.81 or later.

# No telemetry from the .NET CLI or the test platform.
export DOTNET_CLI_TELEMETRY_OPTOUT := 1
export TESTINGPLATFORM_TELEMETRY_OPTOUT := 1

SOLUTION      := HomeScout.slnx
CONFIGURATION := Release
ARTIFACTS     := .artifacts
GENERATED     := packages/fixtures/generated
GENERATOR     := packages/cost-engine/src/HomeScout.CostEngine.Generator/HomeScout.CostEngine.Generator.csproj
VALIDATOR     := packages/fixtures/tools/HomeScout.Fixtures.Validator/HomeScout.Fixtures.Validator.csproj

.PHONY: help restore build format-check generated-check validate inspect test check generate mutate clean

help:
	@echo "Targets: restore build format-check generated-check validate inspect test check generate clean"
	@echo "  check = restore + build + format-check + generated-check + validate + inspect + test (same as CI)"
	@echo "  mutate = Stryker.NET mutation testing of the cost engine (slow; not part of check or CI)"

# Locked mode: fails if packages.lock.json files are out of date.
restore:
	dotnet tool restore
	dotnet restore $(SOLUTION) --locked-mode

build: restore
	dotnet build $(SOLUTION) --configuration $(CONFIGURATION) --no-restore

format-check: restore
	dotnet format $(SOLUTION) --verify-no-changes --no-restore

# Checks every packages/fixtures/data and test-cases file against its JSON Schema (decision 0018, BE-07).
validate: build
	dotnet run --project $(VALIDATOR) --configuration $(CONFIGURATION) --no-build

# JetBrains InspectCode (local tool). Any issue at warning severity or above fails the target.
inspect: build
	@mkdir -p $(ARTIFACTS)
	@rm -f $(ARTIFACTS)/inspectcode.sarif
	dotnet jb inspectcode $(SOLUTION) --output=$(ARTIFACTS)/inspectcode.sarif --format=Sarif --severity=WARNING --no-build --verbosity=WARN
	@test -s $(ARTIFACTS)/inspectcode.sarif || { echo "InspectCode produced no report"; exit 1; }
	@if grep -q '"ruleId"' $(ARTIFACTS)/inspectcode.sarif; then \
		echo "InspectCode found issues (see $(ARTIFACTS)/inspectcode.sarif):"; \
		grep -E '"(ruleId|text)"' $(ARTIFACTS)/inspectcode.sarif | head -40; \
		exit 1; \
	fi
	@echo "InspectCode: no issues at warning severity or above."

test: build
	dotnet test --solution $(SOLUTION) --configuration $(CONFIGURATION) --no-build --coverlet --coverlet-output-format cobertura --results-directory $(ARTIFACTS)/test-results

check: restore build format-check generated-check validate inspect test

# Runs the cost-engine generator: it reads packages/fixtures/data and writes packages/fixtures/generated/costs.json.
# Commit the result. The generator deletes any other *.json in generated/.
generate: build
	dotnet run --project $(GENERATOR) --configuration $(CONFIGURATION) --no-build

# Regenerates, then fails if anything under packages/fixtures/generated/ differs from what is committed: a hand edit, an extra
# file, a deleted file or a stale costs.json (stage 2 plan, task 4b). It reads git status, so run it in a git checkout, and
# commit the generated files (a staged-only file still counts as a change).
generated-check: generate
	@changes="$$(git status --porcelain --untracked-files=all -- $(GENERATED))"; \
	if [ -n "$$changes" ]; then \
		echo "Generated files are out of date: run 'make generate' and commit them."; \
		echo "$$changes"; \
		git --no-pager diff --stat -- $(GENERATED); \
		exit 1; \
	fi
	@echo "Generated files: up to date."

# Mutation testing (stage 2 plan, task 5): Stryker.NET changes the cost engine's code in small ways and checks that the tests fail.
# Slow (about a minute), so it is not part of `check` or CI. Settings are in stryker-config.json; reports go to
# $(ARTIFACTS)/mutation/reports/ (HTML and JSON). Fails if the score drops below the break threshold in that file.
mutate: restore
	dotnet dotnet-stryker --config-file stryker-config.json --output $(ARTIFACTS)/mutation

clean:
	rm -rf $(ARTIFACTS)
	dotnet clean $(SOLUTION) --configuration $(CONFIGURATION) --verbosity quiet
