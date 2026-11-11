# 0044: Public name — Vestagraph

**ID:** PD-08  
**Status:** Accepted (founder, 11 Nov 2026)  
**Date:** 2026-11-11  
**Stage:** 3 (before the design brief; decision 0008 asked to resume "before the public demo")  
**Supersedes (no older text is rewritten):**
- fully: [0008](0008-demo-name.md) (name shown on the public demo, parked);
- in part: [0009](0009-public-brand.md) stays **Open** for commercial clearance. The name below is the working public brand, but a proper UK trade-mark search is still required before any commercial launch.

## Context
"HomeScout" clashes with two property services (HomeScout UK, a London rental-alerts service, and HomeScout Ireland, a renting app; doc 02 §3). The founder asked to "decide the name now" during the design-flow interview of 11 Nov 2026, so that the design brief and every screen carry the real name.

On 11 Nov 2026 we checked 56 candidates in six rounds:
- real English words;
- home-plus-tech blends;
- coined words;
- Latin, French and other roots;
- Domi- variants;
- the founder's own suggestions.

For each we checked:
- property, proptech and home-moving businesses using the name;
- other consumer products using it;
- UK Companies House;
- domains (registry RDAP/WHOIS for `.co.uk`, `.com`, `.app` and `.ai`);
- English pronunciation;
- any "verified/safe/approved" implication (rule 4).

These were web checks, not legal clearance. The UK IPO trade-mark register was not searched.

## Options (finalists)
- **Vestagraph** (chosen): Vesta, the Roman goddess of the hearth and home, plus "graph", a connected picture of everything about a home.
  - Said "VES-ta-graf"; easy to spell after hearing it once.
  - No Companies House entity, and no product or company found using the name.
  - `.co.uk`, `.com`, `.app` and `.ai` all unregistered at the registries on 11 Nov 2026.
- **Domigraph**: the same checks were clean, but it's harder to say on first hearing.
- **DomiCopilot**: domains free, but it reads as a Microsoft Copilot product and puts AI first (0008 had already rejected "Copilot"). Not chosen.
- **Movera**: avoided. It's an established UK home-moving and conveyancing group, and two companies called MOVERA LTD exist.
- **Homegraph**: Google's HomeGraph smart-home API, and most of its domains are taken.
- **Beforehand**: all its domains are taken.
- Other clashes found include Wayhome, Dwellio, Nestwise, Brickwise, Hestia and Movegrid.

## Recommendation
Vestagraph, as the name that is easiest to say and spell, has every domain free, and has no clash found.

## Decision
**Vestagraph** is the product's public name. Founder, 11 Nov 2026: chose "Vestagraph", then "Rename everything now".

- The repository, code namespaces (`Vestagraph.*`), solution, CI, docs and prototype use Vestagraph from this decision's pull request. The GitHub repository is renamed to `vestagraph-platform` after it merges; GitHub redirects the old address.
- **Accepted decision records and dated reviews keep "HomeScout"** where they were written with it. They are history and their bodies are not rewritten. "HomeScout" is the project's former code name.
- The founder chose **not** to buy the domains or run the trade-mark search yet. The planner noted the risk: the domains were free on 11 Nov 2026 but are not reserved until bought.

## Consequences
- Decision 0009 (commercial brand) stays Open. Before any commercial launch:
  - run a UK IPO trade-mark search (classes 9, 36, 42 and 45, plus EUIPO/WIPO);
  - buy the domains;
  - re-check Companies House.
- If the trade-mark search finds a conflict, a new record replaces this one and the rename is repeated.
- The founder's local folder name and the agent memory path are unchanged; that's a local matter only.
- **Noticed during the name checks**, for the doc 02 §3 competitor table: two UK products close to this one. Doorwise (a home and area checker app) and Brick Check (a property comparison app).
