# Vestagraph platform

A home decision workspace for people buying or renting in England: check a home, see the real cost, compare homes, and track questions and answers until you decide. Vestagraph (formerly HomeScout, decision 0044) is the public name; a UK trade-mark search is still to do before any commercial launch (decision 0009).

**Status:** research and concept work only; the repository doesn't yet contain an application. **Current stage: stage 2, close-out** (issue #24 and the "Stage 2: close-out and back to .NET 11" milestone; see the [backlog](docs/planning/backlog.md)), which comes before the prototype specification (stage 3), design and infrastructure decisions (stage 4) and the clickable prototype (stage 5). See the [roadmap](docs/product/04-project-goals-and-delivery.md#9-roadmap-from-design-decisions-to-implementation). The work is listed in order in the [backlog](docs/planning/backlog.md). The backend is C# on .NET (on .NET 11, with C# 14 until CodeQL and Stryker.NET support C# 15 (#59, #60; BE-25), decision [0042](docs/decisions/0042-back-to-dotnet-11.md)); the frontend will be Next.js and React.

## Where to start

- [Documentation index](docs/README.md): what each document is for, which one owns what, and the reading order
- [Decision register](docs/decisions/README.md): every decision made and still to make
- [Roadmap](docs/product/04-project-goals-and-delivery.md#9-roadmap-from-design-decisions-to-implementation) and [ways of working](docs/product/04-project-goals-and-delivery.md#10-ways-of-working)
- Build and check: install the .NET 11 SDK (version in `global.json`), then run `make check`; `make help` lists the other commands
- [Agent instructions](AGENTS.md): rules for the AI agents that build and review this project (`CLAUDE.md` links to the same file)

Document 01 is the historical concept record. Its old labels and paid-feature descriptions are not a second current specification, but requirements it raises that later documents don't address must be considered explicitly when writing the implementation specification. The [document review](docs/reviews/2026-10-23-document-review.md) records corrections and remaining specification gaps.

**Concept images in `docs/assets/concepts/` are AI-generated with ChatGPT (OpenAI) by Sunkanmi Olawuwo.** They are design concepts, not real properties or data. Doc 03 §2 maps each image to its screen, and the [asset register](docs/assets/README.md) records where each image came from.

## Licence

Copyright © 2026 Sunkanmi Olawuwo. All rights reserved. This repository is public for portfolio purposes only; see [LICENSE](LICENSE).
