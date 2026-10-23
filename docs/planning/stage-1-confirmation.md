# Stage 1 confirmation list

**Purpose:** Close the stage 1 decisions in `docs/product/04-project-goals-and-delivery.md` §9 so stage 2 (the fixture catalogue) can start.  
**How to use:** For each item, tick one box and add a line on why. Accepted items become decision records in `docs/decisions/` and their status is updated in the register.  
**Gate:** every product item is confirmed, changed, or kept open with a reason; WW-01 to WW-03 are accepted; `CLAUDE.md` and the decision-record template are in the repository.

## Progress (23 October 2026)

| Item | Answer | Record |
|---|---|---|
| PD-01 Product category | Decision workspace | [0001](../decisions/0001-product-category.md) |
| PD-02 Core object | One record per home | [0002](../decisions/0002-core-object.md) |
| PD-03 Main value | Answers change the decision | [0003](../decisions/0003-main-value.md) |
| PD-04 AI in the product | **Both**: task buttons plus an optional chat panel, with grounding rules | [0004](../decisions/0004-ai-in-the-product.md) |
| PD-05 Visual direction | Warm and calm | [0005](../decisions/0005-visual-direction.md) |
| PD-06 Prototype | Both stories in full | [0006](../decisions/0006-prototype-centrepiece.md) |
| PD-07 Free/paid | Free basics, paid extras | [0007](../decisions/0007-free-paid-principle.md) |
| PD-08 Demo name | **Parked** until before the public demo; strongest so far Plumbline, Lookbefore, Homeknown | [0008](../decisions/0008-demo-name.md) |
| PD-09 Public brand | Kept open | [0009](../decisions/0009-public-brand.md) |
| PD-10 Commercial model | Kept open | [0010](../decisions/0010-commercial-model.md) |
| WW-01 Ways of working | Standard setup | [0011](../decisions/0011-ways-of-working.md) |
| WW-02 AI coding tools | Claude Code builds, OpenAI Codex reviews | [0012](../decisions/0012-ai-coding-tools.md) |
| WW-03 Repo and tracking | Standard setup | [0013](../decisions/0013-repo-and-tracking.md) |
| WW-04 Merge policy and instructions file | Claude Code merges routine PRs after Codex review; founder merges sensitive ones; single `AGENTS.md` with `CLAUDE.md` linked to it | [0015](../decisions/0015-agent-merges-after-review.md) |
| WW-05 Holistic reviews and debt limits | Pre-flight check, one complete Codex pass, debt limits, serious findings always block | [0016](../decisions/0016-holistic-reviews-and-debt-limits.md) |
| WW-06 Docs structure and naming | `docs/product/`, `docs/assets/`, index in `docs/README.md` | [0017](../decisions/0017-docs-structure.md) |

**Stage 1 gate:** `AGENTS.md` (with `CLAUDE.md` linked to it), the merge to `main`, branch protection and the project board are done. The last requirement is the whole-repository audit (pull request #9) with no open `review-followup` issues. The demo name doesn't block stage 2.

The sections below keep the original options for reference. **Where they describe reviews and merges (WW-01, WW-02), they are superseded by decisions 0015 and 0016**: follow `AGENTS.md` and doc 04 §10, not these options.

## Already decided (for reference)

Buyers and renters with equal weight · England first · Portfolio and learning first, built by AI coding agents, small monthly budget, kept commercially viable · Public repository, all rights reserved · Clickable prototype as the first showcase.

---

## Part A: Product decisions

### PD-01 Product category
**Recommendation:** A home decision workspace, described in plain consumer language ("check a home, test the cost, get your questions answered"), not "property intelligence" jargon.  
**Alternatives:** A one-off property report product (closer to most competitors, weaker differentiation) · a buyer due-diligence tool only (contradicts equal renter weight).  
**Why it matters now:** It sets the landing-page copy and what the prototype has to prove.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-02 Core object
**Recommendation:** One **home record** per home, inside a **My move** workspace. Questions, documents, viewings and decisions belong to the home record; comparisons sit across homes in My move.  
**Alternatives:** The report as the core object (static, harder to show change over time) · the question as the core object (strong for the workflow, weak for first-time visitors).  
**Why it matters now:** It decides the fixture schema in stage 2.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-03 Main value
**Recommendation:** Evidence, real costs, comparison and answers connected together: a supported answer visibly changes the cost and the comparison.  
**Alternatives:** Lead with comparison (familiar, already well served) · lead with reports (cheap to copy).  
**Why it matters now:** It is the "aha" moment the prototype stories are built around.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-04 AI presentation in the product
**Recommendation:** AI appears inside specific tasks (explain a finding, draft a question, check a reply, explain a change), never as a dashboard of named agents. Numbers always come from deterministic code. Consistent with the founder decision that "agent-driven" means built by coding agents.  
**Alternatives:** Chat-first copilot as the main surface (resembles many AI wrappers, can hide missing evidence) · visible named agents as in images 3 and 6 (doc 03 recommends against).  
**Why it matters now:** It decides how much chat UI the prototype needs. With the recommendation, it needs very little.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-05 Visual direction
**Recommendation:** Warm editorial clarity (doc 03 §1 and §6): editorial photography on public pages, a precise, restrained workspace, the forest/ink/paper/sage tokens with the darkened amber and red. Image 8's lighter shell is the starting point.  
**Alternatives:** Technical dashboard (dense, favours experienced users) · AI concierge (conversational, hides evidence).  
**Why it matters now:** Design work in stage 4 starts from it; changing direction later means redoing screens.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-06 Prototype centrepiece
**Recommendation:** Both complete stories, buyer (service-charge conflict) and renter (water bill), each from address check to recorded decision, built to the same standard (doc 03 §4).  
**Alternatives:** Buyer story first, then renter (faster first demo, but breaks equal weight in the showcase) · a broader tour of every screen without a story (looks busy, proves less).  
**Why it matters now:** It sets the scope of the fixtures and the spec.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-07 Free/paid principle
**Recommendation:** Free is a complete first look and includes every public-interest fact; paid covers depth that costs money to run (documents, AI assistance, routing, monitoring, shared editing, snapshots). The draft table in doc 02 §8 stays a hypothesis; limits and prices stay open.  
**Alternatives:** Limit by count only (e.g. three free homes, everything else equal) · a paid-only product with a free sample.  
**Why it matters now:** The prototype shows the boundary as simulated labels, and the fixtures need to know which features are marked paid.

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-08 Name shown on the public demo
**Context:** The repo and demo are public, so the demo is a public use of a name. "HomeScout" overlaps with existing services (HomeScout UK, a London rental service with an adjacent audience; HomeScout Ireland), and the brand isn't cleared.  
**Recommendation:** Keep "HomeScout" as the repository and code name, but label the demo clearly as a portfolio concept ("HomeScout — portfolio concept, not a live service") and keep the name configurable in one place.  
**Alternatives:** Use a neutral placeholder name on the demo now (safest, less memorable) · pick and clear a real brand before the demo (slows stage 5).

- [ ] Confirm recommendation
- [ ] Change to: ______
- [ ] Keep open because: ______

### PD-09 Public brand — recommended to keep open
**Reason:** It needs a UK trade mark, domain and Companies House check, and nothing in stages 2–5 depends on it if the name is configurable.

- [ ] Agree to keep open
- [ ] Decide now: ______

### PD-10 Commercial model and prices — recommended to keep open
**Reason:** The Move pass, a monthly plan and a one-off report are hypotheses for the user study in stage 6. The prototype only needs simulated plan labels.

- [ ] Agree to keep open
- [ ] Decide now: ______

---

## Part B: Ways of working

### WW-01 Ways of working
**Recommendation:** Adopt doc 04 §10 as written:
- You decide, review and merge; agents draft.
- Every decision is a record in `docs/decisions/`.
- Every change goes issue → agent branch → pull request → checks → your review → merge → explain-back.
- The definitions of ready and done as listed.
- A weekly plan and review, including actual spend.

**Points to confirm or adjust:**
- [ ] Weekly cadence suits me / change to: ______
- [ ] I'll write the "why" of each decision myself (recommended for learning) / agents may draft it
- [ ] Explain-back after every merge / only after each slice
- [ ] Learning log location: `docs/learning-log.md` / elsewhere: ______

- [ ] Confirm recommendation
- [ ] Change: ______

### WW-02 AI coding tools and setup
**Recommendation:**
- **Primary agent:** Claude Code as the single coding agent at the start. One tool keeps the workflow learnable and the instructions in one place. Add others later only for a specific gap.
- **Models:** the most capable model for planning, decision drafts and reviews; a faster model is acceptable for routine, well-specified implementation.
- **`CLAUDE.md`** at the repo root: project purpose, conventions, commands, the "no invented facts or hand-typed figures" rule, the public-repo rules (no secrets, personal data or licensed datasets), and links to docs 02–04.
- **Project settings in the repo:** permission allowlist for safe read-only and test commands; anything that installs dependencies, changes infrastructure or pushes needs your approval.
- **Hooks:** run the formatter and linter after edits once the codebase exists.
- **Reviews:** an agent code review on each pull request before yours, as a second pair of eyes, never a replacement for your review.
- **Integrations:** GitHub only at first; a design-tool integration only if DS-01 chooses a design tool.
- **Cost:** track the AI tool subscription separately from the Azure budget cap (IN-05), and log both in the weekly review.

**Alternatives:** several agents in parallel from the start (faster, but harder to learn from and review) · an editor-integrated assistant as primary (good for small edits, weaker for multi-file slices).

- [ ] Confirm recommendation
- [ ] Change: ______

### WW-03 Repository and tracking conventions
**Recommendation:**
- **Layout:** a monorepo, `apps/web` (prototype, then product frontend), `packages/fixtures` (catalogue, calculation script, test vectors), `docs/` (design, decisions, planning, reviews; now organised as set out in `docs/README.md`, decision 0017), `infra/` (later), and `apps/api` only when BE-01 is decided.
- **Branches:** `main` protected (pull request and passing checks required, no direct pushes); short-lived branches named `type/short-description` (e.g. `feat/buyer-story-costs`, `docs/stage-1-decisions`).
- **Commits:** Conventional Commits style (`feat:`, `fix:`, `docs:`, `chore:`), squash-merged so each PR is one commit on `main`.
- **Tracking:** GitHub Issues for work, one GitHub Project board with columns per roadmap stage, and labels for decision IDs.
- **First action:** open a pull request to merge the current `docs/product-exploration` branch into `main`, so `main` holds the agreed documents before stage 2.
- **Large files:** the concept images are already committed. Add Git LFS (or keep compressed copies) for future images and design files.

**Alternatives:** separate repositories for frontend and backend (more overhead for one person and for agents) · trunk-based development without pull requests (faster, but loses the review and portfolio record).

- [ ] Confirm recommendation
- [ ] Change: ______

---

## After this list

1. Write the accepted items up as decision records `0001`–`0013` and update the register.
2. Add `CLAUDE.md` and the project settings from WW-02.
3. Merge to `main` and set up branch protection and the project board from WW-03.
4. Stage 2 starts with DA-01 and DA-02.
