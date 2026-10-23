# Architecture (C4 diagrams)

Two diagrams in [Mermaid](https://mermaid.js.org/syntax/c4.html), following the [C4 model](https://c4model.com/): the **system context** (who and what HomeScout talks to) and the **containers** (the parts that run or hold data). Decision 0027 asks for them; they are updated as the system grows.

**How to read them.** Boxes marked **(later)** do not exist yet. Everything unmarked is in the repository today (stage 2). GitHub draws Mermaid diagrams on this page. Mermaid's C4 support is experimental, so if a diagram does not draw, the text under it says the same thing.

## 1. System context

```mermaid
C4Context
    title HomeScout: system context

    Person(user, "Buyer or renter", "Checks a home, sees the real cost, tracks questions and answers (England first)")
    System(homescout, "HomeScout", "Home decision workspace. Today: synthetic sample data and a cost engine; no running app")

    System_Ext(official, "Official and open data (later)", "For example EPC, Price Paid, flood and planning data. Every value labelled Live, Cached, Fallback or Unavailable (decision 0029)")
    System_Ext(models, "AI model provider (later)", "Explains findings and drafts questions; never calculates numbers (decisions 0004, 0023)")
    System_Ext(portals, "Listing portals and agent websites", "Never scraped or copied (decision 0028)")

    Rel(user, homescout, "(later) Enters or uploads their own listing details, documents and estimates")
    Rel(homescout, official, "Reads through adapters (later)")
    Rel(homescout, models, "Sends supplied text, receives wording (later)")
    Rel(user, portals, "(later) Browses the listing themselves; HomeScout never scrapes it; a link may be stored as the user's own reference (decision 0028)")
```

- **People.** The buyer or renter is the only user. Buyers and renters have equal weight (doc 03).
- **What the user gives HomeScout.** Listing text they paste, documents they upload and figures they enter, processed privately and labelled by origin (decision 0028). HomeScout never scrapes or crawls portals or agent sites and never copies listing descriptions, photos or floor plans.
- **Outside services are later.** None is called today. When added, each sits behind one adapter, and each value carries a provenance label: **Live**, **Cached**, **Fallback** or **Unavailable**. Unavailable never looks like a clean result (decision 0029). Tests that call live services stay out of the merge gate.
- **AI** only explains, drafts and checks. Costs, comparisons and what changed come from the cost engine (decisions 0004, 0019, 0023).

## 2. Containers

```mermaid
C4Container
    title HomeScout: containers

    Person(user, "Buyer or renter")

    System_Boundary(now, "In the repository today (stage 2)") {
        ContainerDb(data, "Fixture data", "JSON, packages/fixtures/data", "Inputs only: household, homes, evidence, documents, questions, replies, snapshot. Each value has a source")
        ContainerDb(schema, "Schemas", "JSON Schema 2020-12, packages/fixtures/schema", "The contract for every data, test-case and generated file")
        ContainerDb(cases, "Test cases", "JSON, packages/fixtures/test-cases", "Independently worked examples with their working")
        Container(engine, "Cost engine", "C# class library, HomeScout.CostEngine", "Calculates monthly housing cost, upfront cash and changes. No I/O, HTTP, AI, clock or random")
        Container(generator, "Generator", "C# console app, HomeScout.CostEngine.Generator", "make generate: reads the data, runs the engine, writes the generated file")
        ContainerDb(generated, "Generated costs", "JSON, packages/fixtures/generated/costs.json", "Every calculated output, each with a stable figure ID")
        Container(validator, "Validator", "C# console app, HomeScout.Fixtures.Validator", "make validate: checks every file against its schema")
        Container(ci, "Checks", "make check, GitHub Actions CI", "Restore, build, format, regenerate-and-diff, validate, InspectCode, tests. Also CodeQL and dependency review")
    }

    System_Boundary(later, "Planned (later)") {
        Container(web, "Web app (later)", "TypeScript, Next.js", "The prototype screens and the optional chat panel (decision 0020)")
        Container(api, "API (later)", "C#, ASP.NET Core (planned, to confirm: BE-01, stage 6)", "Serves costs and the question workflow from the same engine (decision 0020)")
        ContainerDb(db, "Database (later)", "PostgreSQL (planned, to confirm: DA-03)", "Persisted homes, questions, replies and decisions (hosting per decision 0022)")
        Container(ai, "AI layer (later)", "Microsoft Agent Framework", "Explains, drafts and checks; quotes only figures the engine supplied (decision 0023)")
    }

    Rel(generator, data, "Reads")
    Rel(generator, engine, "Calls")
    Rel(generator, generated, "Writes")
    Rel(validator, schema, "Loads")
    Rel(validator, data, "Checks")
    Rel(validator, cases, "Checks")
    Rel(validator, generated, "Checks")
    Rel(ci, validator, "Runs")
    Rel(ci, generator, "Runs, then fails if the generated file differs from the commit")

    Rel(user, web, "Uses (later)")
    Rel(web, api, "Calls (later)")
    Rel(api, engine, "Uses (later)")
    Rel(api, db, "Reads and writes (later)")
    Rel(api, ai, "Asks for wording (later)")
```

**What exists now**

| Container | Where | What it does |
|---|---|---|
| Fixture data | `packages/fixtures/data/` | Hand-maintained inputs only; no totals (`AGENTS.md` rule 2). |
| Schemas | `packages/fixtures/schema/` | JSON Schema 2020-12 contract for data, test cases and generated output. |
| Test cases | `packages/fixtures/test-cases/` | Calculations worked out independently of the engine, so a wrong calculation cannot confirm itself. |
| Cost engine | `packages/cost-engine/src/HomeScout.CostEngine/` | The only place calculated figures come from (decision 0019). Architecture tests keep it free of I/O. |
| Generator | `packages/cost-engine/src/HomeScout.CostEngine.Generator/` | Turns the data into `costs.json`. |
| Generated costs | `packages/fixtures/generated/costs.json` | Committed output; never edited by hand. |
| Validator | `packages/fixtures/tools/HomeScout.Fixtures.Validator/` | Schema checks for `make validate`. |
| Checks | `Makefile`, `.github/workflows/` | `make check` locally and in CI; `make generated-check` fails if the committed output is out of date. |

**What is planned, and not built.** The Next.js web app (decision 0020), the ASP.NET Core API (planned; the framework is still to be confirmed at stage 6, BE-01), PostgreSQL (planned; to be confirmed, DA-03; hosting follows decision 0022: the founder's existing server first, Azure only where needed) and the AI layer (decision 0023). How the prototype is built is decided at stage 4 (IN-01); the recommended starting point is that it reads the generated file.
