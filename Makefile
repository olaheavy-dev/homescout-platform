# HomeScout: single entry point for every automated check (decisions 0021, 0035).
# CI runs `make check`; run it before pushing. Works on macOS and Linux with GNU Make 3.81 or later.

# No telemetry from the .NET CLI or the test platform.
export DOTNET_CLI_TELEMETRY_OPTOUT := 1
export TESTINGPLATFORM_TELEMETRY_OPTOUT := 1

SOLUTION      := HomeScout.slnx
CONFIGURATION := Release
ARTIFACTS     := .artifacts
GENERATOR     := packages/cost-engine/src/HomeScout.CostEngine.Generator/HomeScout.CostEngine.Generator.csproj
VALIDATOR     := packages/fixtures/tools/HomeScout.Fixtures.Validator/HomeScout.Fixtures.Validator.csproj

.PHONY: help restore build format-check validate inspect test check generate clean

help:
	@echo "Targets: restore build format-check validate inspect test check generate clean"
	@echo "  check = restore + build + format-check + validate + inspect + test (same as CI)"

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

check: restore build format-check validate inspect test

# Placeholder: the generator writes packages/fixtures/generated/ from task 4b onwards.
generate:
	dotnet run --project $(GENERATOR) --configuration $(CONFIGURATION)

clean:
	rm -rf $(ARTIFACTS)
	dotnet clean $(SOLUTION) --configuration $(CONFIGURATION) --verbosity quiet
