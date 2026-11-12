# P2: Python engine basics (issue #188)

**Decision:** [0049](../../decisions/0049-back-to-python-final.md) port step P2; rules in [0039](../../decisions/0039-python-engineering-foundation.md) sections 2–4 and [0034](../../decisions/0034-rounding-boundary-cases.md). **Ledger:** the `P2` rows of [`python-port-ledger.md`](../../planning/python-port-ledger.md). **Builder:** Sonnet, test first; **review:** Opus before push.

## Goal
Port the money basics of the C# engine (`Pence.cs`, `Result.cs`, `Error.cs`) and their tests to `packages/vestagraph-engine`, plus the `ast` architecture test that replaces NetArchTest. No cost calculations yet (P3a/P3b). The C# stays and keeps running.

## Data contract
No change. Tests read `packages/fixtures/test-cases/rounding-boundaries.json` with `json.loads(text, parse_float=Fraction)` (never `float`).

## Design (Python)
- `vestagraph_engine/pence.py`
  - `round_ratio(numerator: int, denominator: int) -> Pence`: the **only** division of money. `denominator == 0` raises `ZeroDivisionError`. Sign = sign of the fraction; size = `divmod(abs(n), abs(d))`, plus 1 when `2 * remainder >= abs(d)`. Both arguments must be `type(x) is int` (else `TypeError`).
  - `Pence`: `@dataclass(frozen=True, slots=True, order=True)` with one field `value: int`. `__post_init__` raises `TypeError` unless `type(value) is int` (rejects `bool`, `Fraction`, `float`) and `OverflowError` outside the signed 64-bit range (`-2**63` to `2**63 - 1`). Operators: `+`, `-` (binary and unary), `*` by a whole `int` on either side (`type(factor) is int`, not `bool`); every result goes through the constructor, so it is range-checked. Mixed types (`Pence + 3`) return `NotImplemented`, so Python raises `TypeError`. Method forms `add`, `subtract`, `negate`, `multiply` match the C# names in snake case.
  - `Pence.ZERO`; `Pence.from_exact(amount: Fraction) -> Pence` (C# `Round(decimal)`): `round_ratio(amount.numerator, amount.denominator)`; it accepts `Fraction` or `int` only. `Pence.annual_to_monthly(self) -> Pence` = `round_ratio(self.value, 12)`.
- `vestagraph_engine/result.py`
  - `ErrorCategory(Enum)`: exactly `VALIDATION`, `NOT_FOUND`, `CONFLICT`, `UNAVAILABLE`.
  - `Error`: frozen slotted dataclass `code: str`, `message: str`, `category: ErrorCategory`; blank or whitespace code or message raises `ValueError`; a category that isn't an `ErrorCategory` raises `TypeError`.
  - `Result[T]` (PEP 695 generic, frozen slotted): `Result.success(value)` (rejects `None`: `ValueError`), `Result.ok()` (a success with no value, C#'s non-generic `Result.Success()`, typed `Result[None]`), `Result.failure(error)` (rejects anything not an `Error`: `TypeError`); `is_success`, `is_failure`; `.value` raises `RuntimeError` on a failure; `.error` raises `RuntimeError` on a success; `to_result()` drops the value.
- `vestagraph_engine/__init__.py` exports `Pence`, `round_ratio`, `Result`, `Error`, `ErrorCategory`.
- Engine style (0039 §2): no `float`, `round()`, `decimal`, `math`, `operator`, `random`, clock, file, network or environment access; `//`, `%`, `divmod` and `int(...)` only inside `round_ratio`.

## Tasks (each: failing test first, then code, then `make check`)
1. **`round_ratio`:** ports `RoundRatioTests` (10 sign/half cases, zero denominator, large exact half without precision loss, too big/too small for 64-bit) and the six `round-*` cases from the boundary file, read by ID (a test that the file has all six).
2. **`Pence`:** ports `PenceTests` (add/subtract/multiply/negate incl. overflow at both ends, `Negate` of the minimum, comparisons and equality, `ZERO`, `from_exact` incl. half not banker's rounding, too large) and type checks (`bool`, `Fraction`, `float` rejected; `Pence + 3` is a `TypeError`).
3. **`annual_to_monthly`:** the 14 `annual-to-monthly-*` cases from the file, exact multiple of 12, maximum and minimum value don't overflow.
4. **Properties (Hypothesis):** port `PenceProperties` (commutative, associative, adding the negation gives zero, subtracting equals adding the negation, comparison agrees with sign, `from_exact` within half a penny / idempotent / negation-symmetric / exact half away from zero, `annual_to_monthly` matches rounding the exact quotient / negation-symmetric / 12×monthly gives monthly). Use Hypothesis's built-in `ci` profile (don't register one named `ci`).
5. **`Result` and `Error`:** port `ResultTests` (every row, incl. the 2- and 4-case parametrised ones).
6. **Architecture test (`ast`):** reads every `.py` file under `vestagraph_engine/`. Rules: imports only from an allow-list (`__future__`, `dataclasses`, `enum`, `fractions`, `typing`, `collections.abc`; extend only with a reason) and never another Vestagraph package; no names `float`, `round`, `eval`, `exec`, `open`, `__import__`, `input`, `print`; no attribute `now`/`today`/`utcnow`; outside the function `round_ratio`, no `//`, `%`, `//=`, `%=`, `divmod` or `int(...)`. **Each rule also has a test that applies it to a small bad source string and checks it fails** (the C# `*_failsAsExpected` tests), so a rule that silently matches nothing is caught.
7. **Ledger:** fill the **Python test** column for every P2 row (`packages/vestagraph-engine/tests/<file>::<test>`); .NET-only rows (`NamespaceMatch_*`, `FrameworkOnlyRule_*`, `CostEngine_assembly_hasNoDependencyOnSystemTextJson`, `CostEngine_everyTypeOutsideTheCoverageTracker_*`, `CostEngine_assembly_referencesOnlyTheFrameworkAndSystemLibraries`) get the Python equivalent or a one-line reason.

## Acceptance
- Every P2 ledger row has a Python test or a reason; every worked case in `rounding-boundaries.json` is checked by ID.
- `make check` passes (mypy strict, ruff, pytest) with the C# unchanged.
- Test names follow `test_<method>_<condition>_<result>`; expectations come only from the file and 0034's tables, never from running the engine.

## Out of scope
Cost lines, mortgage, upfront cash, builder (P3a/P3b); mutation testing (P7); `third-party.md` needs no change (no new package).
