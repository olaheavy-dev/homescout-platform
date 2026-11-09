# 0039: Python engineering foundation

**ID:** BE-20  
**Status:** Accepted (the founder's answers of 7 Nov 2026 to the port plan's nine questions on issue #42; the rest of the port plan and the details listed under "Decision" are confirmed by the founder's merge; the founder's answers of 8 Nov 2026 settle Q1 (commit an exported requirements file), Q2 (CodeQL default setup, no workflow) and Q3 (a `0.x` minor bump counts as a major bump); what is still to do is listed under "Open questions" and in section 8; P1 amends Q1 and adds licence exemptions: see register lines BE-23 and BE-22)  
**Date:** 2026-11-07  
**Stage:** 2 (the Python port, step P0 of the port plan in issue #42)  
**Supersedes in part (no older text is rewritten):**
- [0021](0021-dotnet-engineering-foundation.md): this record is its Python successor for the toolchain, build, strictness and test setup. 0021's design rules already carried over by [0036](0036-python-backend.md) stay in force.
- [0035](0035-ways-of-working-v2.md) point 9: the pre-approved package list gains the Python list below. The .NET entries stay until the C# is deleted (P6). From 8 Nov 2026 the same point's rule for small Dependabot updates also changes: a minor bump of a direct `0.x` dependency or action pin counts as a major bump (Q3 below; the live rule is in `AGENTS.md`).
- [0036](0036-python-backend.md): one rounding detail. 0036 allowed `decimal` with `ROUND_HALF_UP` to quantise a decimal input; this record replaces that with `fractions.Fraction`, so `decimal` is not used at all. 0036's "tooling to propose" list is settled here.
- [0027](0027-stage-2-engineering-hardening.md): this record is the decision record 0027 requires for one licence exception (`typing_extensions`, below). The allow-list itself is unchanged.

## Context
Decision 0036 moves the cost engine, generator and later the API to Python. In C#, much of the safety came from the compiler and analysers (0021). Python checks almost nothing before running, so the same safety has to come from a type checker, a linter, strict test settings and a few tests that read the code itself. The Opus port plan (issue #42) proposed a toolchain; the founder answered its nine questions on 7 November 2026. This record fixes those choices so P1 to P7 can be built without re-deciding them.

What does not change: the `AGENTS.md` rules, the fixtures, schemas, worked test cases and the shape of `costs.json`, the register lines BE-10 to BE-17, and `make check` as the one command that runs every check the same way locally and in CI.

## Options
### Option A: the port plan's strict toolchain (recommended)
uv, ruff, mypy in strict mode, pytest, Hypothesis, coverage, jsonschema and mutmut, all configured strictly from the first commit. It shares uv, ruff, mypy strict and pytest with the founder's FastAPI template (0040), so the engine and the API (P7) share one way of working.

### Option B: a lighter setup
Fewer tools and default settings. Faster to start, but mistakes in money code are found later, by review rather than by `make check`.

### Rejected alternatives (and why)
- **Poetry or plain pip** instead of uv: uv gives one lock file for several packages in a workspace and also installs Python itself, and the template already uses it. A second tool would mean two ways of working. (Poetry's and pip's own workspace and locking features were not compared here.)
- **pyright as the gate:** good, but mypy is what the template uses, and two checkers would disagree. A newer checker (Astral's ty) was still described as beta in the plan; not re-checked here.
- **Flat layout** (packages at the folder root): tests can then import the code without installing it, which hides packaging mistakes. pytest's guide strongly suggests the `src` layout.
- **One big package:** separate packages make the "engine depends on nothing" rule easy to check.
- **A percentage coverage gate:** a target number invites tests written to raise the number, not to check behaviour. Mutation testing measures test strength better.
- **`Decimal` for money:** its default precision is 28 digits, so a long chain of calculations can be rounded more than once without anyone noticing. Whole pence and exact fractions cannot.
- **Pre-commit hooks:** a second place where checks live; `make check` stays the single entry point.
- **Mutation testing in CI:** slow, and it runs by hand today (`make mutate`); kept that way.

## Recommendation
Option A. What it means in practice: an agent's mistake in money code, typing or style fails `make check` on their own machine, before review.

## Decision
Option A. On 7 November 2026 the founder answered the port plan's nine questions on issue #42 and asked for this record. The rest of Option A follows the port plan (the body of issue #42); that part, together with the details below, is confirmed by the founder's merge of this record.

**Details beyond the port plan and the founder's answers** (set by this record; confirmed by the founder's merge; each can change later with a register line):
- the folder layout (section 1);
- the extra mypy settings beyond `--strict` and `warn_unreachable`: the optional error codes and a reason on every `# type: ignore` (section 2);
- the exact ruff rule list, including `S101` ignored for tests (section 2);
- `Pence` as a range-checked frozen value type that accepts only an exact `int` (section 3);
- the banned rounding routes outside `round_ratio`, beyond the plan's "never `//` or `%`" (section 3);
- pytest's `strict = true`, which adds strict parametrisation IDs and strict xfail to the plan's strict markers and configuration, and `--import-mode=importlib` (section 4);
- the use of Hypothesis's built-in `ci` profile (section 4);
- the list of checks in the architecture test (section 4);
- branch coverage through pytest-cov (section 4);
- import-linter left unapproved for now and possibly added with P7 (the plan placed it at stage 6) (section 4);
- the package-URL form of the licence exception, `pkg:pypi/typing-extensions` (section 7).

The stable-JSON rules (section 5) are the plan's, spelled out; they add nothing beyond it.

**Plan items the founder's merge confirms that change an accepted record:**
- **`Fraction` for exact decimal inputs, and no `Decimal` at all** (section 3). This changes part of accepted decision 0036, which allowed `decimal` with `ROUND_HALF_UP` to quantise a decimal input. 0036 itself is not rewritten; its status points here.

No other plan item overrides an accepted record: the rest either settles a choice 0036 left open (its "tooling to propose" list) or carries out a change 0036 already made (for example, BE-07 to BE-09 superseded at P6).

### 1. Toolchain and layout
- **Python 3.14** is the baseline (`requires-python = ">=3.14"`, and a `.python-version` file). 3.14 was released on 7 October 2025 and gets security fixes until about October 2030. The founder's FastAPI template defaults to 3.14 too. Python 3.15 was released on 9 October 2026; moving to it later is a minor change with a register line.
- **uv** manages Python, packages and the virtual environment. One **uv workspace** with **one `uv.lock`** at the repository root; `make restore` runs `uv sync --locked`, which fails if the lock file is out of date.
- **src layout**, one package per job:

  | Package | Job | May import |
  |---|---|---|
  | `homescout_engine` | the cost engine: pure calculations | the standard library only, from an allow-list |
  | `homescout_generator` | reads fixtures, calls the engine, writes `costs.json` | `homescout_engine`, the standard library |
  | `homescout_fixture_validator` | checks fixture files against their schemas (`make validate`) | `jsonschema`, `referencing`, the standard library; never the engine |

  Default folders (P1 may change them with a register line): `packages/<package-name>/src/<package_name>/` with tests in `packages/<package-name>/tests/`. The API and MCP server join the workspace later (P7, 0037).
- The engine has **no runtime dependencies**. Every tool above is a development dependency, used but never shipped.

### 2. Strictness
- **mypy** is the type gate: `strict = true` plus `warn_unreachable = true` (mypy's documentation says `--strict` does not include it), and the optional error codes `redundant-expr`, `possibly-undefined`, `truthy-bool`, `ignore-without-code` and `exhaustive-match`. Every `# type: ignore` needs a code and a reason.
- **ruff** lints and formats (`ruff check` and `ruff format --check`). The rule list is explicit, never `ALL`, so a ruff update cannot switch new rules on silently: `E`, `W`, `F`, `I`, `B`, `UP`, `S`, `C4`, `SIM`, `RUF`, `PT`, `TID`, `N`, `DTZ`, `T20`, `PERF`, with `S101` (use of `assert`) ignored for tests, because every pytest check is an `assert`. Preview rules stay off.
- **Engine style:** immutable data as frozen, slotted dataclasses (`@dataclass(frozen=True, slots=True)`); a functional core with input and output only in the generator; `match` statements end with `assert_never` so a new case cannot be forgotten. **Pydantic only at the API edge** (P7, not yet approved), never in the engine.

### 3. Money rules
- **`Pence`** is a small frozen value type that holds money as one `int` number of pence, as 0036 requires. Wrapping the `int` means `Pence + 3` is a type error and every result is range-checked. It accepts only an exact `int` (`type(value) is int`): it rejects `bool` (which Python treats as an integer), `Fraction` and `float`.
- **Range:** signed 64-bit, −9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 pence, the same as the C# engine. Python integers never overflow, so `Pence` checks the range on creation and after every operation and **raises** outside it (a programming error, as in C#). The port plan's 64-bit minimum and overflow cases test this. Note for stage 4: JavaScript numbers are exact only up to 2^53 − 1 (9,007,199,254,740,991), so the frontend must not do arithmetic on figures above that; no realistic home cost comes near it.
- **One rounding helper, `round_ratio(n, d)`:** nearest penny, exact halves away from zero (0021, 0034). It takes `divmod(abs(n), abs(d))`, rounds up when twice the remainder is at least `abs(d)`, then restores the sign. It is the only place a division of money is rounded.
- **Outside `round_ratio`, never** `//`, `%` or `divmod` (Python rounds those towards minus infinity, C# towards zero), any `int(...)` call (on a `Fraction` it truncates towards zero, and in source code `int(rate * amount)` looks the same as a harmless `int(count)`), the `math` module (its `floor`, `ceil` and `trunc` each round in one fixed direction) or the `operator` module (its `floordiv`, `mod` and `ifloordiv` are `//` and `%` under another name). **Never** `round()` (it rounds halves to even), **never** `float`, and **no `decimal`**. Inside `round_ratio`, `divmod` is used only on the non-negative `abs(n)` and `abs(d)`, where every rounding direction agrees. A `Fraction` that reaches money by another route is stopped by `Pence`, which accepts only `type(value) is int`.
- **Exact decimal inputs** become `fractions.Fraction`, which converts a decimal string exactly (`Fraction("1.1")` is 11/10). Fixture JSON is read with `json.loads(..., parse_float=Fraction)`, so no JSON number ever becomes a `float`. Rates stay whole basis points (BE-15).
- **Results:** HomeScout's own `Result` and `Error` (stable code, plain-language message, category) for expected failures; programming errors raise (0032's principle).

### 4. Tests
- **pytest** with `strict = true` (pytest 9.0 and later: strict markers, strict configuration, strict parametrisation IDs, strict xfail; pytest's guide advises this only with a locked version, which `uv.lock` gives), **warnings as errors** (`filterwarnings = ["error"]`) and `--import-mode=importlib`.
- **Test names:** `test_<method>_<condition>_<result>` (0036).
- **Test expectations** are the independently worked examples in `packages/fixtures/test-cases/` and the boundary tables of 0034, worked out by hand with their working and source (rule 2). They are never produced by running the engine, and never edited to make a test pass.
- **Hypothesis** for properties (total equals the sum of its lines, and so on), using Hypothesis's **built-in `ci` profile**, which is active whenever the `CI` environment variable is set and already sets `derandomize=True` (so CI runs the same cases every time), `deadline=None`, `database=None`, `print_blob=True` and suppresses the `too_slow` health check. HomeScout does **not** register its own profile named `ci`: that would overwrite the built-in one and bring back the default deadline (200 ms). If the profile needs a change, register it with the built-in one as its parent (`settings.register_profile("ci", parent=settings.get_profile("ci"), ...)`).
- **Architecture test** (pytest reading the engine's source with Python's `ast` module): the engine imports only allow-listed standard-library modules and no other HomeScout package; no `float`, `round`, `decimal`, `random`, clock (`datetime.now`, `time`), file, network or environment access; `math` and `operator` are not on the allow-list, so `floor`, `ceil`, `trunc`, `floordiv`, `mod` and `ifloordiv` cannot be imported under any name; outside `round_ratio`, no `//`, `%`, `//=`, `%=`, `divmod` or `int(...)` call at all. These are checks on the source text, which `ast` can make; it cannot see types, so it cannot tell whether a value is already an `int` (mypy does not flag `int(Fraction(...))` either). That remaining gap, a `Fraction` reaching a money value, is closed at run time by `Pence` accepting only `type(value) is int`, and tested there. This replaces NetArchTest. **import-linter** is not approved yet; it can come with P7 (the template uses it).
- **Coverage** (coverage.py with pytest-cov, branch coverage on) is **report only**: no `fail_under`.
- **Mutation testing** with **mutmut**, run by hand (`make mutate`), **not** in `make check` or CI. mutmut has no built-in pass mark, so a small script reads its statistics and fails below a break score. The score is set **just below the first measured run** and recorded in the port pull request. mutmut needs `fork`, so it runs on macOS and Linux only (Windows through WSL), which matches the Makefile.

### 5. The port proof and stable JSON
- After the Python generator regenerates `costs.json`, `git diff` shows changes **only** in `generatedBy` (now `"homescout_generator"`) and `rounding` (its text now cites decision 0036 instead of 0021). The `homes` data is byte-for-byte the same. If it is not, the engine is fixed, never the expectations; stop after 3 attempts (`AGENTS.md`).
- **Stable JSON:** `json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)` plus a final newline; keys in the order the generator builds them (never `sort_keys`); keys with no value left out; empty lists kept; LF line endings; written to a temporary file and then renamed, so a failed run never leaves half a file. Two runs give identical bytes.

### 6. Python pre-approved packages (amends 0035 point 9)
These may be added without a founder merge. Each still passes the 0027 licence allow-list (except the exception in section 7) and gets a `docs/references/third-party.md` entry in the pull request that adds it (P1). Licences were read from PyPI metadata (`license_expression`, or the `license` field and classifiers where no expression is given) and GitHub on 7 November 2026; the versions are the latest at that date, for reference only, as the exact versions live in `uv.lock`.

| Package | Licence | Latest (7 Nov 2026) | Brings in (licence) |
|---|---|---|---|
| uv | MIT OR Apache-2.0 | 0.13.7 | — (a standalone tool) |
| pytest | MIT | 9.2.0 | iniconfig (MIT), packaging (Apache-2.0 OR BSD-2-Clause), pluggy (MIT), Pygments (BSD-2-Clause), colorama (on Windows only; "BSD License" classifier only, no licence field or expression on PyPI for 0.4.6) |
| pytest-cov | MIT | 7.1.0 | coverage, pluggy, pytest |
| coverage | Apache-2.0 | 7.17.2 | — |
| Hypothesis | MPL-2.0 | 6.170.15 | sortedcontainers (Apache 2.0, written that way rather than as SPDX `Apache-2.0`) |
| ruff | MIT | 0.17.4 | — |
| mypy | MIT | 2.4.1 | mypy_extensions (MIT), **typing_extensions (PSF-2.0)**, pathspec (MPL-2.0, classifier only), librt (MIT), ast-serialize (MIT) |
| jsonschema | MIT | 4.26.0 | attrs (MIT), jsonschema-specifications (MIT), referencing, rpds-py (MIT) |
| referencing | MIT | 0.37.0 | attrs, rpds-py |
| mutmut | BSD-3-Clause | 3.8.1 | click (BSD-3-Clause), LibCST (PyPI classifier only says MIT; GitHub reports Apache-2.0 AND MIT AND Python-2.0, and its LICENSE is MIT plus files derived from the Python standard library and from dataclasses, so P1 exempts `pkg:pypi/libcst` as a tool-only exception, register line BE-22) with PyYAML (MIT), setproctitle (BSD-3-Clause), Textual (MIT) with Rich, markdown-it-py, mdit-py-plugins, mdurl, linkify-it-py, uc-micro-py and platformdirs (all MIT), plus coverage, pytest and typing_extensions |
| `astral-sh/setup-uv` GitHub Action | MIT (GitHub repository licence) | v10.3.3 (28 Oct 2026) | — (pinned by full commit SHA, 0027) |

Packages not in this table, including import-linter, Pydantic, FastAPI and FastMCP, still need founder approval.

### 7. Licence exception: `typing_extensions` (PSF-2.0)
`typing_extensions` uses the Python Software Foundation licence, which is permissive but not on the 0027 allow-list. The founder approves it as a **tool-only exception**: allowed as a dependency of development tools, never imported by HomeScout code and never shipped. PyPI metadata for mypy 2.4.1 requires it on every Python version (`typing_extensions>=4.6.0` before Python 3.15 and `>=4.14.0` from 3.15), and Textual (through mutmut) lists it too, so it will be in the lock file. P1 adds it to the dependency review's `allow-dependencies-licenses` as `pkg:pypi/typing-extensions` (package URLs write PyPI names in lower case with `_` replaced by `-`) with a comment citing this record, and the architecture test makes sure the engine never imports it.

### 8. CodeQL for Python
**Decided (Q2, founder, 8 Nov 2026): default setup, no workflow.** Python joins CodeQL scanning when the Python lands (P1). The repository uses CodeQL **default setup** (a repository setting, currently `actions` and `csharp`). The founder adds Python to the default setup languages in the repository settings (a founder action; Claude Code cannot change repository settings) and P1 adds no CodeQL workflow. **Still to do:** after P1 merges, the founder checks that the default setup languages include Python and adds it if not. GitHub's documentation says it adds a newly detected language to default setup on the default branch automatically, so P1's own pull request is probably not scanned for Python whatever is set beforehand; whether the settings page offers Python earlier is not verified. Source: https://docs.github.com/en/code-security/concepts/code-scanning/setup-types (read 8 Nov 2026).

## Open questions
- **Q1 (decided 8 Nov 2026; blocks P1 until its proof passes): can dependency review read `uv.lock`?** **Founder's answer: commit an exported file** (the decided fix below); the alternative route is not taken. GitHub's list of supported dependency-graph ecosystems (read 7 Nov 2026) names pip (`requirements.txt`) and Poetry (`poetry.lock`) for Python, but not uv; dependency review supports the same ecosystems as the dependency graph. If it cannot read `uv.lock`, the licence and vulnerability gate would silently pass every Python package. This ties to [issue #30](https://github.com/olaheavy-dev/homescout-platform/issues/30): dependency review already lets packages with no detectable licence through (it logs them as "unlicensed" and passes them), which 0027 does not allow.
  - **Decided fix:** commit an exported file, `uv export --locked --all-packages --all-groups --no-emit-workspace --format requirements.txt --output-file <path>`, which the dependency graph's pip (`requirements.txt`) support should read (not yet proven: the P1 proof below confirms it, including that the file name and location are ones GitHub detects), and add a `make check` step that regenerates it and fails if it differs (like `generated-check`). By default the export also lists HomeScout's own workspace members as editable lines (`-e ./packages/...`); `--no-emit-workspace` leaves them out (checked with uv 0.11.14 on a scratch workspace). Whether GitHub's parser would cope with the editable lines is not verified; P1 confirms the flag choice in its proof.
  - **Alternative (not taken):** submit the Python dependencies through the existing `.github/workflows/dependency-submission.yml` (GitHub's dependency review page says the action also considers dependencies submitted through the dependency submission API). That workflow today submits NuGet only; under this route P1 adds a Python step beside NuGet and P6 removes the NuGet step, and no export file is committed. Whether its detector reads `uv.lock` is not verified. Under the chosen route the workflow keeps submitting NuGet until P6, which then removes it, since nothing is left for it to submit (0036 ties its replacement to issue #30).
  - **Before P1 merges, prove the gate works:** a throwaway pull request adds (a) a package with a disallowed licence and (b) a package whose licence cannot be detected, and shows dependency review failing on both; record the result in the P1 description. If (b) passes, issue #30 must be fixed (a founder merge, as it changes CI) before P1 merges. P1 also checks whether licence strings such as sortedcontainers' "Apache 2.0" and classifier-only licences (pathspec, LibCST, colorama's "BSD License") are recognised, and adds named exceptions (founder-approved) if they are not.
- **Q2 (decided 8 Nov 2026): CodeQL workflow or setting?** The founder's first answer (7 Nov) was "P1 adds the workflow". GitHub's documentation says default setup disables existing CodeQL workflows and blocks their uploads, so a workflow and default setup cannot both run. **Founder's answer (8 Nov): keep default setup** and add Python to its languages in the repository settings (a founder action, no workflow). A workflow would only be chosen for a custom query set, which means switching the whole repository to advanced setup.
- **Q3 (decided 8 Nov 2026): some of our tools and libraries are still `0.x`** (uv and ruff, and also the zizmor action and `referencing` at the time of writing). For `0.x` versions, a minor bump (for example 0.13 to 0.14) may break things, but the Dependabot merge rule (0035 point 9) only routed **major** bumps to review. **Founder's answer: treat a minor bump of a `0.x` tool as a major bump for that rule, and (second answer, 8 Nov) the scope is direct dependencies and action pins; indirect packages that only appear in a lock file follow their parent.** This changes a merge rule, so it is an `AGENTS.md` change ("When merging" 1(b)) in the pull request that records this answer, and a founder merge.

## Consequences
- **This record's pull request is a founder merge.** It changes the "Founder merges these" list in `AGENTS.md` (a merge rule), extends the pre-approved package list (0036: changing it is a founder merge) and records a licence exception (0027: only the founder approves one). Although it changes documentation only, a fallback review alone is not enough to merge it: Claude Code does not merge it, even with Codex unavailable; the founder does.
- **Pull requests that follow** (issue #42): P1 `chore/python-foundation` (workspace, lock file, empty engine package, Python steps beside .NET in each Makefile target plus `lint`, setup-uv pinned by SHA, Dependabot `uv`, `.claude/settings.json` rules, `third-party.md`, the Q1 export and its proof, CodeQL for Python through default setup per Q2 with no workflow; how the `uv` Dependabot group treats a `0.x` minor bump, because `.github/dependabot.yml` groups minor and patch updates together and one `0.x` minor bump would send the whole grouped pull request to full review (a separate group, or accept the cost); founder merge); P2 `feat/engine-basics` (`Pence`, `round_ratio`, annual-to-monthly, `Result`/`Error`, architecture test, every 0034 case); P3 `feat/engine-costs-and-builder` (one pull request); P4 `feat/python-generator` (with the port-proof test, and the one data-contract wording fix: the description in `packages/fixtures/schema/generated-costs.schema.json` says "calculated by the C# engine", which becomes the cost engine without naming a language); P5 `test/python-validator-and-mutation` (one pull request; sets the break score); P6 `chore/remove-csharp` (founder merge: deletes the C#, marks BE-07, BE-08, BE-09 and WW-13 superseded, and corrects the docs listed in 0036); P7 `feat/api-skeleton` (0040; founder merge for its new packages).
- `make check` keeps its name and order (0036): restore (locked), build or type-check, format-check, generated-check, validate, lint, test.
- `AGENTS.md` changes with P1 and P6 (commands, test naming, the "C# cost engine" wording), not in this record's pull request, except the pointer to the pre-approved list.
- No `third-party.md` entries yet: its rule is to add them in the pull request that adds the dependency (P1).
- **Revisit if:** mypy proves too weak to protect money code; uv's dependency data cannot be fed to dependency review at all, neither as an export (the route chosen in Q1) nor through dependency submission (the alternative); or mutmut fails three times on the same problem (the plan's fallback is cosmic-ray, which would need approval).

## Sources (all read 7 November 2026)
- Python 3.14 schedule, [PEP 745](https://peps.python.org/pep-0745/) (3.14.0 on 2025-10-07; security fixes until about October 2030), and [status of Python versions](https://devguide.python.org/versions/) (3.14 bugfix, end of life 2030-10 scheduled; 3.15 first released 2026-10-09).
- The founder's template defaults to Python 3.14: `copier.yml` in [house-template-fastapi](https://github.com/olaheavy-dev/house-template-fastapi).
- uv: [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) (one shared lock file), [exporting a lock file](https://docs.astral.sh/uv/concepts/projects/export/), [CLI reference](https://docs.astral.sh/uv/reference/cli/) (`uv sync --locked`, `uv export --all-packages`, `--format`, `--no-emit-workspace`: "Do not emit any workspace members, including the root project"); the editable-line behaviour was checked locally with uv 0.11.14.
- mypy 2.4.1: [command line](https://mypy.readthedocs.io/en/stable/command_line.html) (`--warn-unreachable` is not part of `--strict`), [configuration file](https://mypy.readthedocs.io/en/stable/config_file.html), [optional error codes](https://mypy.readthedocs.io/en/stable/error_code_list2.html).
- ruff: [rules](https://docs.astral.sh/ruff/rules/) (all sixteen prefixes above exist), [banned-api (TID251)](https://docs.astral.sh/ruff/rules/banned-api/).
- pytest: [good practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) (strict mode added in 9.0; `src` layout; `importlib` import mode).
- Hypothesis: [settings reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html) (`derandomize`; the built-in `ci` profile, its settings and the `CI` variable; the default deadline of 200 milliseconds; a profile registered under an existing name overwrites it; `get_profile`).
- coverage.py: [configuration](https://coverage.readthedocs.io/en/latest/config.html) (`branch`, `fail_under`).
- mutmut: [documentation](https://mutmut.readthedocs.io/en/latest/) (configuration in `[tool.mutmut]`; needs `fork`; no built-in threshold).
- jsonschema 4.26.0: [validation](https://python-jsonschema.readthedocs.io/en/stable/validate/) (`Draft202012Validator`; format checks off by default; `registry=`); referencing 0.37.0: [introduction](https://referencing.readthedocs.io/en/stable/intro/) (no network retrieval unless asked).
- Python standard library: [`json`](https://docs.python.org/3.14/library/json.html) (`parse_float`, `ensure_ascii`, `allow_nan`), [`fractions`](https://docs.python.org/3.14/library/fractions.html) (decimal strings).
- JavaScript limit: [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER).
- GitHub: [dependency graph supported ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems), [dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) ("The action also considers dependencies submitted via the dependency submission API"), [two CodeQL workflows](https://docs.github.com/en/code-security/code-scanning/troubleshooting-code-scanning/two-codeql-workflows).
- Licences and versions: each package's PyPI JSON metadata (`https://pypi.org/pypi/<name>/json`) and the [setup-uv repository](https://github.com/astral-sh/setup-uv); package URL naming for PyPI: the [purl `pypi` type definition](https://github.com/package-url/purl-spec/blob/main/types/pypi-definition.json) (lower case, `_` replaced by `-`).

**Not verified:** whether ruff's TID251 can ban a built-in such as `round` (its page speaks only of modules and their members; the architecture test covers it instead); the fields of `mutmut export-cicd-stats`; whether dependency review maps non-SPDX licence strings (Q1); the exact CodeQL steps for adding Python to default setup; whether GitHub's dependency graph parses the editable lines of a uv export (Q1); whether the component-detection action in `dependency-submission.yml` reads `uv.lock` (Q1); whether dependency review matches `allow-dependencies-licenses` entries by the normalised name `pkg:pypi/typing-extensions` (P1 checks); the ty beta status quoted in the plan; that mypy accepts `int(Fraction(...))` without an error (not run here; P2's architecture test does not rely on it).
