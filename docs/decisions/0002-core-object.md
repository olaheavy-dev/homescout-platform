# 0002: Core object

**ID:** PD-02  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 1

## Context
Everything in the app needs one thing it is organised around. This decides the sample-data structure in stage 2.

## Options
- **One record per home:** Each home has its own page with facts, costs, viewing notes, documents and questions. 'My move' holds all homes and comparisons.
- **One report per check:** Each search produces a saved report. Hard to show change over time or track answers.
- **A list of questions:** The main screen is a question to-do list. Powerful, but confusing for first-time visitors.

## Recommendation
One record per home.

## Decision
One record per home (consumer term: home record), inside a My move workspace.

## Consequences
The sample data (stage 2) is organised by home. Questions, documents, viewing notes and decisions always belong to one home; comparisons sit across homes.
