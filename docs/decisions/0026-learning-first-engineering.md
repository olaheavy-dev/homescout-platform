# 0026: Learning-first engineering

**ID:** WW-08  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2

## Context
Founder's words: "as much as agents write the code, I need to understand the tools, frameworks and programming languages so I can develop as an engineer." Agent-written code is only a portfolio asset if the founder can explain, change and defend it.

## Options
- **Explain-back after merge only (current, decision 0011):** light, but easy to skim.
- **Learning-first practices built into every change (chosen):** more time per change, much deeper understanding.

## Recommendation
Learning-first practices, proportionate to each change.

## Decision
1. **Every pull request teaches.** Its description has a "How it works" section in plain language and a "Concepts to learn" list linking the official documentation pages for the language features, frameworks and tools it uses.
2. **Docs first.** Before a new tool or framework is used, its official getting-started and concept pages are listed in `docs/references/third-party.md`. The founder reads them alongside the first pull request that uses it.
3. **Founder-built slices.** At least one small, well-specified piece per stage is written by the founder, with the agent acting as a tutor: explaining, reviewing and hinting, not writing it.
4. **Explain-back.** After each slice, the founder writes a few lines in their own words in `docs/learning-log.md` (decision 0011). If something can't be explained, the agent explains it until it can.
5. **Learning map.** Doc 04 §4 lists what each part of the system teaches. Each stage's plan names its learning goals across C# and .NET, TypeScript and React, testing, data, infrastructure and AI engineering.
6. **Ask "why" freely.** Agents answer in plain language with a small example and a link to the official source.

## Consequences
- Slower than pure agent delivery, by design; the learning is part of the deliverable.
- The founder-built slice is chosen when each stage's work is broken into issues (SP-02).
- `AGENTS.md` gains a "Teach as you build" section.
