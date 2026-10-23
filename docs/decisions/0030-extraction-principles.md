# 0030: Document extraction principles

**ID:** AI-06  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 6 (rules set early; also inputs to AI-03 evaluation)

## Context
Reading facts out of documents (listings, leases, bills schedules, replies) is central to HomeScout and easy to get wrong. The founder's earlier pilot established principles and found concrete pitfalls; they are restated here in our own words.

## Options
- **Adopt the principles and an accuracy target now (chosen).**
- **Decide at stage 6.**

## Recommendation
Adopt now, so fixtures and the specification reflect them.

## Decision
The founder agreed.
1. **Extraction proposes; the user confirms.** Extracted facts are suggestions until the user confirms or corrects them.
2. **"Unknown" beats a guess.** A missing fact is recorded as unknown, never filled in.
3. **Every field records its source and confidence:** document, page and the exact text it came from.
4. **Precedence:** an official register outranks document text; agreement between independent sources outranks a single source.
5. **Conflicts are recorded, never silently resolved** (doc 02 §6).
6. **Accuracy target:** at most about **1% of extracted facts unsupported by the source** (invented), measured per field, alongside per-field recall. Prompt, model or parser changes that worsen these don't merge (decision 0025).
7. **Text first, images only if needed:** extract from text first; add image-based extraction only where the evaluation shows text misses facts (cost first, decision 0022).
8. **Known pitfalls in every evaluation set,** using synthetic documents: words merged by PDF text extraction (for example a bedroom count fused with other digits), the agent's address in a page footer mistaken for the property's, ratings shown only as images, and a document that contradicts itself.

## Consequences
- Synthetic extraction test documents are part of the fixture catalogue when stage 6 starts; real listings are never used (decision 0028).
- AI-03's evaluation tooling must report the per-field metrics above.
