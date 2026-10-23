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
- **Every value has a source:** `origin` (`listing-claim`, `document`, `official-dataset`, `user-entered`, `synthetic`, or `plan` for a value the stage 2 plan itself sets, such as "outside this version's scope"; an origin of `synthetic` forces `synthetic: true`, and all stage 2 data is synthetic), the plain-language `label`, a `date` (year, year-month or full date, so a year-only source is not given an invented day), a `synthetic` flag, and an optional `citationUrl` with `citedText`.
- **Context-only costs:** `contextOnly: true` means the value is shown but never enters a total. Energy-certificate costs must be context-only.
- **Statuses are as at the snapshot** (23 October 2026), after each story has finished. `storyStep` and `usedFromStep` put events in order (1 to 4); they are not calendar time. An item with `supersedes` keeps the earlier value it replaces.
- **Nations:** every address has a `nation`. Outside England, `coverage` must be `not-yet-covered`.
- **Question statuses** are the eight in doc 02 section 6, written as `to-ask`, `waiting-for-reply`, `reply-needs-checking`, `answer-recorded`, `partially-answered`, `needs-professional-review`, `closed-by-user-without-answer` and `reopened`. Each question lists its transitions with a reason.

Run `make validate` after editing any file here.

## Rules for the cost engine (task 4b)

- **Which item applies.** An evidence item applies from its `usedFromStep` (step 1 if absent) until another item names it in `supersedes`. B1's 2026 budget (`B1-SC-BUDGET`, from step 4) supersedes the listing claim (`B1-SC-LISTING`); the listing item is kept, not deleted.
- **`conflicting` is a label, not an instruction.** It says sources disagree; it does not by itself decide whether an item enters a total. The engine decides from the case being calculated: before R1's water is settled it leaves water out and flags the total partial, and from step 4 it uses `R1-WATER-ESTIMATE`.
- **R1 water.** `R1-WATER-LISTING` ("Water included", `conflicting`) and `R1-WATER-WSOT` ("Tenant pays water") are evidence about who pays, category `water-responsibility`. They never carry an amount. `R1-WATER-ESTIMATE` (category `water`, from step 4) is the amount. In `test-cases/story-calculations.json` the R1 `water` line is `conflicting` before the user confirms and carries 4,500p a month after.
- **Included and not-calculated items** carry no value and add nothing to a total; they are never treated as zero.

### Test-case line categories and data categories

| Test-case `category` | Data `category` (evidence item) |
|---|---|
| `mortgage-deposit` (buyer upfront deposit) | `mortgage-deposit` (`HH-MORTGAGE-DEPOSIT`) |
| `deposit` (renter upfront deposit) | `deposit` (`R1-DEPOSIT`, `R2-DEPOSIT`) |
| `moving-costs`, `first-month-rent`, `rent`, `service-charge`, `ground-rent`, `council-tax`, `energy`, `water`, `broadband`, `buildings-insurance`, `maintenance`, `stamp-duty`, `legal-fees` | the same name |
| `mortgage-repayment` | none: a calculated output from `mortgage-deposit`, `mortgage-rate`, `mortgage-term` and `asking-price` |

Items that only describe a home (`council-tax-band`, `energy-certificate`, `energy-certificate-cost`, `lease-term`, `tenancy-type`, `water-responsibility`) have no test-case line.

## Known limits

- `partialDate` checks the shape (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`) but not that the date exists (2026-02-31 passes). Harmless for now.
- JSON Schema cannot say that `selectedUnitId` is one of `candidateUnits`, or that a question's `status` equals its last transition, or that references point at real records. Tests in `HomeScout.Fixtures.Tests` check these.

## Fictional placeholders

WALES-1 ("7 Harbour Mews, Afonbryn", postcode `ZZ1 0AA`) is invented. A web search found no place called Afonbryn, and `ZZ` is not a geographic postcode area. Northbridge and the `NB` postcodes are also fictional (`NB` is not a UK postcode area).
