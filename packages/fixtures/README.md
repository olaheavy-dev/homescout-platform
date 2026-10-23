# HomeScout fixtures

Synthetic sample data for the prototype (decision 0018, stage 2 plan section 1). Everything here is invented; nothing is a real person, address, postcode or document.

| Folder | What it holds |
|---|---|
| `schema/` | JSON Schema 2020-12 files. `common.schema.json` holds shared pieces (money, sources, dates, nations); the others describe one data file each. |
| `data/` | Hand-maintained **inputs**: household, homes, evidence, documents, questions, replies, snapshot. No totals or other calculated figures (AGENTS.md rule 2). |
| `test-cases/` | Independently worked examples (task 3), checked against `schema/test-case.schema.json`. |
| `generated/` | Cost-engine outputs (task 4b). Never edited by hand. |
| `tools/HomeScout.Fixtures.Validator/` | The checker run by `make validate` and `make check`. |
| `tests/HomeScout.Fixtures.Tests/` | NUnit tests that prove the schemas reject bad data and accept the real files. |

## Which schema checks which file

- `data/NAME.json` is checked against `schema/NAME.schema.json` (by file name). Each data file also carries a `"$schema": "../schema/NAME.schema.json"` line for editors; the validator fails if it names a different schema.
- Every file in `test-cases/` must name its schema in a top-level `"$schema"` field (a relative path into `schema/`); both current files name `../schema/test-case.schema.json`.

## How values are modelled

- **Money is whole pence** (`"pence": 160000` is £1,600). The schema accepts only integers of at least 1, so decimals and zero are rejected. A `period` (`once`, `month` or `year`) says how often it is charged, as the source states it; the cost engine does conversions.
- **Rates are basis points** (`"basisPoints": 550` is 5.5%), also an integer.
- **Missing data is never zero** (AGENTS.md rule 7). An evidence item's `status` is one of `available`, `missing`, `conflicting`, `stale`, `not-applicable`, `not-calculated` or `included`. Only `available`, `conflicting` and `stale` items may carry a `value`; the other four must not. A bill covered by the rent is `included`; stamp duty, legal fees and internal maintenance are `not-calculated`.
- **Every value has a source:** `origin` (`listing-claim`, `document`, `official-dataset`, `user-entered` or `synthetic`), the plain-language `label`, a `date` (year, year-month or full date, so a year-only source is not given an invented day), a `synthetic` flag, and an optional `citationUrl` with `citedText`.
- **Context-only costs:** `contextOnly: true` means the value is shown but never enters a total. Energy-certificate costs must be context-only.
- **Statuses are as at the snapshot** (23 October 2026), after each story has finished. `storyStep` and `usedFromStep` put events in order (1 to 4); they are not calendar time. An item with `supersedes` keeps the earlier value it replaces.
- **Nations:** every address has a `nation`. Outside England, `coverage` must be `not-yet-covered`.
- **Question statuses** are the eight in doc 02 section 6, written as `to-ask`, `waiting-for-reply`, `reply-needs-checking`, `answer-recorded`, `partially-answered`, `needs-professional-review`, `closed-by-user-without-answer` and `reopened`. Each question lists its transitions with a reason.

Run `make validate` after editing any file here.

## Fictional placeholders

WALES-1 ("7 Harbour Mews, Afonbryn", postcode `ZZ1 0AA`) is invented. A web search found no place called Afonbryn, and `ZZ` is not a geographic postcode area. Northbridge and the `NB` postcodes are also fictional (`NB` is not a UK postcode area).
