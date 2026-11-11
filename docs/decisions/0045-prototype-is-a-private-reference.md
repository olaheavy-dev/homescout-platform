# 0045: The clickable prototype is a private reference, not a public demo

**ID:** PD-10  
**Status:** Accepted (founder, 11 Nov 2026)  
**Date:** 2026-11-11  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** doc 04 §8, the founder decision "first public showcase: clickable prototype" (also in the register's "Already decided" table), and the parts of doc 04 §9 stage 5 that make the prototype public (slice 5's public launch; the gate's "public demo").

## Context
During the design flow (11 Nov 2026) the founder clarified the prototype's purpose: "the prototype is more for AI coding agents and myself to have a vision of what we are building."

Asked whether it should become a public demo later, the founder chose **"Private only"**: never a public demo. The real product (stage 6) is the first public thing.

## Decision
- **Purpose:** the stage 5 clickable prototype is the **vision and reference build** for the founder and the AI coding agents. It's built to full design quality, because a reference is only useful if it is the real target. It's also used, privately, in the stage 6 validation sessions with buyers and renters (doc 02 §10).
- **Never published as a public demo.** Hosting is private: local, or an access-restricted preview (IN-02 is decided on that basis).
- **Deferred to before the first public product (stage 6):**
  - visitor privacy, part 1 (SE-02: privacy notice, ICO fee check, device storage);
  - demo analytics and feedback (FE-05).

  Neither is needed for a private reference.
- **Kept** (founder): the public-facing pages as part of the vision (landing, How it works, Costs and comparison), the full textured editorial illustration work, and both light and dark themes.
- **Added** (founder): a **component gallery**, one route showing every component in every state in light and dark. It's the agents' visual dictionary and the baseline for design review.
- **Unchanged:** every data rule (figures from the engine, missing never £0, no verdicts), the executable specifications (0043), and the stage gates.

## Consequences
- Doc 04 §9 stage 5:
  - slice 5 becomes labelling, a simulated-action audit and the stage 5 gate, with no public launch;
  - the gate reads "on the private prototype".
- The register's "Already decided" row "First public showcase" is updated to point to this record.
- Backlog changes:
  - #90 is retitled;
  - #85 (SE-02 part 1 and FE-05) moves to stage 6, before the first public release;
  - #81 (IN-01 to IN-03) plans private hosting;
  - a new component-gallery issue sits after the app shell (#86).
- Decision 0044's domain and trade-mark tasks become less urgent, because nothing is public until stage 6. They're still needed before then (0009).
- **Revisit if** the founder later wants a public portfolio demo. A new record would then restore SE-02 part 1, FE-05 and public hosting before publishing.
