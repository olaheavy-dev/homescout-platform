# Vestagraph: single entry point for every automated check (decisions 0021, 0035).
# CI runs `make check`; run it before pushing. Works on macOS and Linux with GNU Make 3.81 or later.
# Two stacks run side by side until the C# is removed (decision 0049, port step P8): .NET and Python (uv, decision 0039).

# No telemetry from the .NET CLI or the test platform.
export DOTNET_CLI_TELEMETRY_OPTOUT := 1
export TESTINGPLATFORM_TELEMETRY_OPTOUT := 1
export REQNROLL_TELEMETRY_ENABLED := 0

SOLUTION      := Vestagraph.slnx
CONFIGURATION := Release
ARTIFACTS     := .artifacts
GENERATED     := packages/fixtures/generated

PYTEST_XML    := $(ARTIFACTS)/test-results/python/coverage.xml

.PHONY: help restore requirements requirements-check build format-check generated-check validate inspect lint test check generate mutate mutate-dotnet clean

help:
	@echo "Targets: restore build format-check generated-check validate inspect lint test check generate mutate mutate-dotnet clean"
	@echo "  check = restore + build + format-check + generated-check + validate + inspect + lint + test (same as CI)"
	@echo "  restore, build, format-check, lint and test also run the Python side (uv); build = .NET build + mypy"
	@echo "  mutate = mutmut mutation testing of the Python cost engine (about a minute; not part of check or CI)"
	@echo "  mutate-dotnet = Stryker.NET mutation testing of the C# cost engine (until the C# is removed, decision 0049 step P8)"

# Locked mode: fails if packages.lock.json (.NET) or uv.lock (Python) is out of date.
restore:
	@command -v uv >/dev/null || { echo "uv is missing: install uv 0.13.x (https://docs.astral.sh/uv/)"; exit 1; }
	dotnet tool restore
	dotnet restore $(SOLUTION) --locked-mode
	uv sync --locked --all-packages

# OPTIONAL, not part of `check` (register line BE-23): a pip-format export of uv.lock, kept as the fallback in case dependency
# review stops reading uv.lock. The 9 Nov 2026 proof (PRs #50, #51) showed it reads uv.lock directly;
# P1 of decision 0049 (#187) repeated it on 12 Nov 2026 (PRs #199, #200). To adopt it: add `requirements-check` after `restore` in `check`, commit requirements.txt, and allow both targets.
requirements:
	uv export --locked --all-packages --all-groups --no-emit-workspace --format requirements.txt --output-file requirements.txt

# Regenerates the export, then fails if it differs from what is committed (a staged-only change counts as stale).
requirements-check: requirements
	@changes="$$(git status --porcelain --untracked-files=all -- requirements.txt)"; \
	if [ -n "$$changes" ]; then \
		echo "requirements.txt is out of date: run 'make requirements' and commit it."; \
		echo "$$changes"; \
		exit 1; \
	fi
	@echo "requirements.txt: up to date."

build: restore
	dotnet build $(SOLUTION) --configuration $(CONFIGURATION) --no-restore
	uv run --locked mypy

format-check: restore
	dotnet format $(SOLUTION) --verify-no-changes --no-restore
	uv run --locked ruff format --check

# Checks every packages/fixtures/data, test-cases and generated file against its JSON Schema (decision 0018, BE-07).
# Runs the Python validator (vestagraph_fixture_validator, decision 0049 step P5); the C# validator stays until P8.
validate: restore
	uv run --locked python -m vestagraph_fixture_validator

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

# The Gherkin specs (docs/specs, run by packages/specs) tag scenarios that need a browser (@ui), an MCP server (@mcp) or that
# are withdrawn; those do not run here. NUnit exposes each tag as a test category.
SPEC_FILTER := TestCategory!=ui&TestCategory!=mcp&TestCategory!=withdrawn
# The same Gherkin files run a second time under pytest-bdd (packages/specs/tests, decision 0049 step P6), where each tag is a
# pytest marker; the Reqnroll runner stays until P8.
SPEC_MARKERS := not ui and not mcp and not withdrawn

# Python lint (ruff, explicit rule list in pyproject.toml; decision 0039 section 2).
lint: restore
	uv run --locked ruff check

# pytest stops after 5 failures (register line BE-30); CI's job timeout is the only time limit.
test: build
	dotnet test --solution $(SOLUTION) --configuration $(CONFIGURATION) --no-build --timeout 10m --maximum-failed-tests 5 --filter "$(SPEC_FILTER)" --coverlet --coverlet-output-format cobertura --results-directory $(ARTIFACTS)/test-results
	uv run --locked pytest -m "$(SPEC_MARKERS)" --maxfail=5 --cov --cov-branch --cov-report=xml:$(PYTEST_XML) --cov-report=term

check: restore build format-check generated-check validate inspect lint test

# Runs the Python generator (vestagraph_generator, decision 0049 step P4): it reads packages/fixtures/data and writes
# packages/fixtures/generated/costs.json. Commit the result. The generator deletes any other *.json in generated/.
# The C# generator stays until P8; its own test still proves it writes the same bytes as the committed file.
generate: restore
	uv run --locked python -m vestagraph_generator

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

# Mutation testing of the Python cost engine (decision 0049 item 11b, register line BE-33): mutmut changes the engine's code in
# small ways (a `<` becomes `<=`, a string is altered, a line is removed) and checks that a test fails each time. Slow (about a
# minute), so it is not part of `check` or CI: run it when the engine or its tests change.
# - mutmut reads [tool.mutmut] in packages/vestagraph-engine/pyproject.toml and must run in that folder (see the note there).
# - CI=true makes Hypothesis load its built-in `ci` profile (derandomize=True), so the property tests give the same result on
#   every run and the score is repeatable. `make test` keeps random seeds.
# - mutmut has no pass mark: tools/mutation_score.py reads its statistics and fails below MUTATION_BREAK (percent). The break
#   score sits just below the final measured score (BE-33); change it only on purpose, with the report.
# - mutants/ is deleted first so every run is a full, uncached run; the result is in mutants/mutmut-cicd-stats.json.
# Needs `fork`: macOS and Linux only (Windows through WSL).
MUTATION_BREAK  := 85
ENGINE_DIR      := packages/vestagraph-engine

mutate: restore
	rm -rf $(ENGINE_DIR)/mutants
	cd $(ENGINE_DIR) && CI=true uv run --locked mutmut run
	cd $(ENGINE_DIR) && uv run --locked mutmut export-cicd-stats
	uv run --locked python tools/mutation_score.py $(ENGINE_DIR)/mutants/mutmut-cicd-stats.json --break-score $(MUTATION_BREAK)

# Mutation testing of the C# cost engine (stage 2 plan, task 5): Stryker.NET. Kept until the C# is removed (decision 0049 step P8).
# Settings are in stryker-config.json; reports go to $(ARTIFACTS)/mutation/reports/ (HTML and JSON). Fails if the score drops below
# the break threshold in that file. The FsCheck property tests start from a fixed seed here (format seed,gamma; read by
# EngineProperty), so the score is the same on every run of the same code. Change the seed only on purpose.
MUTATION_REPLAY := 123456789,987654321

mutate-dotnet: restore
	VESTAGRAPH_FSCHECK_REPLAY=$(MUTATION_REPLAY) dotnet dotnet-stryker --config-file stryker-config.json --output $(ARTIFACTS)/mutation

clean:
	rm -rf $(ARTIFACTS) .coverage .mypy_cache .ruff_cache .pytest_cache .hypothesis mutants $(ENGINE_DIR)/mutants
	find packages -type d -name __pycache__ -prune -exec rm -rf {} +
	dotnet clean $(SOLUTION) --configuration $(CONFIGURATION) --verbosity quiet
