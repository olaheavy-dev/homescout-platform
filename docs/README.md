# Documentation index

## Folder structure

```
docs/
├── README.md            this index
├── product/             the main product and delivery documents (numbered, read in order)
├── assets/              the asset register and media files
│   └── concepts/        AI-generated concept images (discussion only)
├── decisions/           one record per decision, plus the register
├── planning/            stage checklists and working plans
├── references/          links to official third-party documentation
└── reviews/             dated document reviews and audits
```

Planned folders, added when their stage starts: `.design/<feature>/` at the repository root for design-skill outputs (brief, information architecture, tasks, reviews), a deliberate exception to this structure (decision 0031), `docs/architecture/` for C4 diagrams in Mermaid (stage 2, decision 0027), `docs/specs/` for the prototype specification (stage 3), and `docs/learning-log.md` for the founder's explain-back notes (decision 0011).

## What each document is for

| Document | Owns | Status |
|---|---|---|
| [01 Product brief v1.1](product/01-product-brief-v1.1.md) | The original concept | **Historical.** Superseded where 02–04 differ |
| [02 Research and direction](product/02-research-and-direction.md) | Product decisions, scope, free/paid split, data feasibility | Current |
| [03 Prototype and image direction](product/03-prototype-and-image-direction.md) | Prototype behaviour, screens, visual direction, image review | Current |
| [04 Project goals and delivery](product/04-project-goals-and-delivery.md) | Goals, roadmap (§9), ways-of-working summary (§10; rules in `AGENTS.md`), budget, commercial safeguards | Current |
| [Decision register](decisions/README.md) | Every decision's status and record | Current |
| [Asset register](assets/README.md) | Where each image or media file came from and its terms | Current |
| [Stage 1 confirmation list](planning/stage-1-confirmation.md) | Stage 1 decisions and gate | Stage 1 |
| [Stage 2 plan](planning/stage-2-plan.md) | Approved sample data, data contract, tasks and gate | Stage 2 |
| [Document review, 23 Oct 2026](reviews/2026-10-23-document-review.md) | Corrections and specification gaps found in the first review | Record |
| [Third-party documentation](references/third-party.md) | Official documentation links and pinned versions for tools and packages | Current |
| [Best-practice audit, 23 Oct 2026](reviews/2026-10-23-best-practice-audit.md) | Gaps found and the practices planned for each stage | Record |
| [Foundations review, 23 Oct 2026](reviews/2026-10-23-foundation-review.md) | Lessons from earlier projects, as inputs for stages 2, 4 and 6 | Record |

Accepted decision records override anything in the documents that contradicts them. For process (planning, building, reviewing, merging, dependencies), `AGENTS.md` is the single current rulebook (decision 0035). Where 02, 03 and 04 overlap, each owns the area listed above.

**Reading order for someone new:** 02 → 03 → 04 → the decision register. Read 01 only for background.

## Naming conventions

- Lowercase words separated by hyphens; no spaces. Example: `03-prototype-and-image-direction.md`.
- Numbered prefixes where order matters: `01-` to `04-` for product documents, `0001-` upwards for decisions.
- Dates as `YYYY-MM-DD` at the start of dated files, for example reviews.
- Every image or media file is added to the [asset register](assets/README.md) before it is committed.
- Documents are referred to by number in text ("doc 03 §2") and linked by path.
