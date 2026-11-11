# Documentation index

## Folder structure

```
docs/
├── README.md            this index
├── product/             the main product and delivery documents (numbered, read in order)
├── architecture/        C4 context and container diagrams (Mermaid)
├── assets/              the asset register and media files
│   ├── concepts/        AI-generated concept images (discussion only)
│   └── imagery/         AI-generated atmosphere photos (illustrative)
├── decisions/           one record per decision, plus the register
├── planning/            stage checklists and working plans
├── references/          links to official third-party documentation
├── reviews/             dated document reviews and audits
└── specs/               the prototype specification: executable Gherkin features (decision 0043)
```

Planned folders, added when their stage starts: `.design/<feature>/` at the repository root for design-skill outputs (brief, information architecture, tasks, reviews), a deliberate exception to this structure (decision 0031), and `docs/learning-log.md` for the founder's explain-back notes (decision 0011).

## What each document is for

| Document | Owns | Status |
|---|---|---|
| [01 Product brief v1.1](product/01-product-brief-v1.1.md) | The original concept | **Historical.** Superseded where 02–04 differ |
| [02 Research and direction](product/02-research-and-direction.md) | Product decisions, scope, free/paid split, data feasibility | Current |
| [03 Prototype and image direction](product/03-prototype-and-image-direction.md) | Prototype behaviour, screens, visual direction, image review | Current |
| [04 Project goals and delivery](product/04-project-goals-and-delivery.md) | Goals, roadmap (§9), ways-of-working summary (§10; rules in `AGENTS.md`), budget, commercial safeguards | Current |
| [05 Ideas and product thinking](product/05-ideas-and-product-thinking.md) | How new features are found and shaped, and the ideas worth exploring (none scheduled) | Current |
| [Architecture (C4 diagrams)](architecture/README.md) | The system context and container diagrams: what exists today and what is planned (decision 0027) | Current |
| [Decision register](decisions/README.md) | Every decision's status and record | Current |
| [Asset register](assets/README.md) | Where each image or media file came from and its terms | Current |
| [Stage 1 confirmation list](planning/stage-1-confirmation.md) | Stage 1 decisions and gate | Stage 1 |
| [Stage 2 plan](planning/stage-2-plan.md) | Approved sample data, data contract, tasks and gate | Stage 2 |
| [.NET 11 and C# 15 plan](planning/dotnet-11-and-csharp-15-plan.md) | Which .NET 11 and C# 15 features Vestagraph uses, where, and when (decision 0042) | Stage 2 onwards |
| [Specifications](specs/README.md) | The prototype specification: rules, templates, and the executable screen, story and MCP features | Stage 3 onwards |
| [Ordered backlog](planning/backlog.md) | Every issue from the stage 2 close-out to stage 6, in order, by milestone | All stages |
| [Document review, 23 Oct 2026](reviews/2026-10-23-document-review.md) | Corrections and specification gaps found in the first review | Record |
| [Free data sources assessment](references/data-sources.md) | Licence, terms, limits and coverage of free UK data sources for area information, checked 11 Nov 2026 (#123) | Stage 3 onwards |
| [Third-party documentation](references/third-party.md) | Official documentation links and pinned versions for tools and packages | Current |
| [Best-practice audit, 23 Oct 2026](reviews/2026-10-23-best-practice-audit.md) | Gaps found and the practices planned for each stage | Record |
| [Foundations review, 23 Oct 2026](reviews/2026-10-23-foundation-review.md) | Lessons from earlier projects, as inputs for stages 2, 4 and 6 | Record |
| [Stage 2 mutation-testing report, 23 Oct 2026](reviews/2026-10-23-stage-2-mutation-report.md) | Stryker.NET scores before and after, and how each surviving mutant was handled | Record |

Accepted decision records override anything in the documents that contradicts them. For process (planning, building, reviewing, merging, dependencies), `AGENTS.md` is the single current rulebook (decision 0035). Where 02, 03 and 04 overlap, each owns the area listed above.

**Reading order for someone new:** 02 → 03 → 04 → 05 → the decision register. Read 01 only for background.

## Naming conventions

- Lowercase words separated by hyphens; no spaces. Example: `03-prototype-and-image-direction.md`.
- Numbered prefixes where order matters: `01-` to `05-` for product documents, `0001-` upwards for decisions.
- Dates as `YYYY-MM-DD` at the start of dated files, for example reviews.
- Every image or media file is added to the [asset register](assets/README.md) before it is committed.
- Documents are referred to by number in text ("doc 03 §2") and linked by path.
