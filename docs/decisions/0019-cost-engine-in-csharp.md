# 0019: Calculations in a C# cost engine from day one

**ID:** DA-02  
**Status:** Accepted (partly superseded: solution file location by [0021](0021-dotnet-engineering-foundation.md))  
**Date:** 2026-10-23  
**Stage:** 2  
**Supersedes:** in [0013](0013-repo-and-tracking.md), the placement of the "calculation script" in `packages/fixtures`. The rest of 0013 stands.

## Context
Some figures in the stories are calculated, not looked up (for example £3,720 − £2,400 = £1,320 a year, or £110 a month). Image 5 showed what happens when such figures are typed by hand. The calculations need one trusted home. The founder confirmed C# for the backend (decision 0020), which will contain the real cost engine.

## Options
- **C# cost engine from day one (chosen):** write the calculations once, in the language they'll stay in, with tests from the start. A small generator writes the results into the sample-data files, so the Next.js prototype needs no running backend. Tests check the engine against independently worked examples.
- **TypeScript script now, C# later:** simpler at first, but the calculations are rewritten in stage 6.
- **Python script:** quick, but adds a third language.

## Recommendation
C# cost engine from day one.

## Decision
The founder chose the C# cost engine from day one.

## Consequences
- A .NET solution under `packages/cost-engine/`: a class library for the calculations, a test project, and a small generator that reads `packages/fixtures/data/` and writes `packages/fixtures/generated/`. The generator writes results for the prototype only, never test expectations.
- **Test expectations are independent of the engine.** They live in `packages/fixtures/test-cases/` as worked examples written and reviewed separately, each showing its working and citing its rule or source. The engine's tests compare its results against them, so a calculation error can't confirm itself by regenerating the expected values.
- The prototype reads generated JSON only. The same library later sits behind the ASP.NET Core API (stage 6).
- Doc 04 §5's "cost engine" step starts in stage 2 with the calculations the stories need, and grows in stage 6 (SDLT, stress scenarios, rule tables under BE-03).
- Installing the .NET SDK and test packages is a dependency change, so the founder approves it in the first implementation pull request. Use the current .NET long-term-support release.
