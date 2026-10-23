# 0018: Sample data format

**ID:** DA-01  
**Status:** Accepted (partly superseded: CI timing by [0027](0027-stage-2-engineering-hardening.md))  
**Date:** 2026-10-23  
**Stage:** 2

## Context
The prototype runs on synthetic sample data: one household, four homes, their evidence, documents, replies and cost inputs. The format decides how the website reads the data now, how the C# backend reuses it later, and how mistakes are caught.

## Options
- **JSON files with a JSON Schema (chosen):** readable by any language, including TypeScript and C#; the schema checks automatically that every record has the right fields.
- **YAML files:** easier to read and edit by hand, and allows comments, but needs converting, and indentation mistakes can silently change data.
- **TypeScript objects:** type-checked inside the website, but tied to the frontend language, so the C# backend couldn't reuse them.

## Recommendation
JSON files with a JSON Schema.

## Decision
The founder chose JSON with a schema.

## Consequences
- Sample data lives in `packages/fixtures/`: hand-maintained **inputs** in `data/`, the **schemas** in `schema/`, independently worked **test cases** in `test-cases/` (decision 0019), and **generated outputs** (calculated by the cost engine) in `generated/`, never edited by hand.
- Every input figure carries its source (document, listing, user entry or dataset) and date, following the inputs-versus-outputs rule in `AGENTS.md`.
- Schema validation runs in CI once CI exists (stage 4), and locally before then.
- Money is stored as whole pence (integers) to avoid rounding errors.
