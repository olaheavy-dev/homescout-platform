# 0032: Our own Result type

**ID:** BE-05  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2

## Context
Decision 0021 says when to use a Result type: only for expected failures (invalid input, not found, an outside service unavailable), while programming errors throw. It didn't say where the type comes from. One earlier project wrote its own small type; another used the FluentResults package.

## Options
- **Write our own (chosen):** a small `Result`, `Result<T>` and `Error` type, about 50–100 lines.
- **FluentResults:** MIT, feature-rich and works on .NET 10, but effectively a single maintainer, no commits since July 2025 and some open bug reports ([GitHub](https://github.com/altmann/FluentResults), checked 23 October 2026). More features than needed, which makes it easy to drift into "Result for everything".
- **ErrorOr or Ardalis.Result:** close fits, but still extra dependencies; Ardalis.Result's last release was October 2024.

## Recommendation
Write our own.

## Decision
The founder chose to write our own Result type.
- `Result` and `Result<T>` represent success, or failure with an `Error`.
- `Error` has a stable code, a plain-language message and a category (for example validation, not found, conflict, unavailable), so the API can later map categories to standard error responses in one place (BE-02).
- It lives in the cost engine at first, so the engine keeps **no outside packages**, enforced by the architecture tests (0021). If the API needs it too, it moves to a small shared project.
- Written test-first, with tests for success, failure and each error category.

## Consequences
- No dependency to track or update.
- If later needs outgrow it (for example several errors per result), extend it or adopt a package through a new decision record.
