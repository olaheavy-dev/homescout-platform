# 0004: How AI appears in the product

**ID:** PD-04  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 1

## Context
AI can appear as task buttons, as a chat assistant, or both. This is about the product the user sees, not the coding agents that build it (WW-02).

## Options
- **Inside specific tasks:** Buttons such as 'explain this', 'draft a question', 'check this reply'. Most trustworthy and easiest to test.
- **Chat assistant:** Ask anything about the home. Familiar, but can sound confident about unknowns and resembles many AI apps.
- **Both:** Task buttons plus an optional chat panel.

## Recommendation
Inside specific tasks only.

## Decision
**Both**: AI inside specific tasks, plus an optional chat panel for open questions about the current home. This differs from the earlier recommendation, so the chat panel must follow the rules below.

## Consequences
Chat rules: it is an optional, closable panel, not a permanent column (doc 03's critique of image 3 still applies). It only answers about the current home, using its evidence. Every claim links to a source or says it isn't known. It never calculates numbers itself (it calls the cost engine), never says a home is safe or verified, and can't change records without the user confirming. It needs its own evaluation set (AI-03). In the prototype, chat replies are scripted from the sample data and labelled as simulated.
