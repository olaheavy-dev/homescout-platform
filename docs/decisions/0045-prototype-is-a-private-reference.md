# 0045: The clickable prototype is a private reference, not a public demo

**ID:** PD-11  
**Status:** Accepted (founder, 11 Nov 2026)  
**Date:** 2026-11-11  
**Stage:** 3  
**Supersedes in part (no older text is rewritten):** doc 04 §8, the founder decision "first public showcase: clickable prototype" (also in the register's "Already decided" table), and the parts of doc 04 §9 stage 5 that make the prototype public (the last slice's public launch; the gate's "public demo").

## Context
During the design flow (11 Nov 2026) the founder clarified the prototype's purpose: "the prototype is more for AI coding agents and myself to have a vision of what we are building."

Asked whether it should become a public demo later, the founder chose **"Private only"**: never a public demo. The real product (stage 6) is the first public thing. (Decision [0046](0046-public-area-check-first.md), accepted the same day, makes a free public area check the first public thing instead; the prototype stays private.)

## Options
- **Private only (recommended, chosen):** the prototype is the vision and reference build for the founder and the agents, used privately in the validation study. No public-launch work (privacy notice, analytics) is needed for it.
- **Private now, public demo later:** keeps a portfolio demo option, but carries public-launch work into stage 5 for a sample-data showcase.
- **Public demo (the earlier plan):** the first public showcase, with privacy part 1 and analytics before launch.

## Recommendation
Private only. The founder's stated purpose is a shared vision for themselves and the agents, and a private reference keeps stage 5 focused on design quality rather than launch work.

## Decision
- **Purpose:** the stage 5 clickable prototype is the **vision and reference build** for the founder and the AI coding agents. It's built to full design quality, because a reference is only useful if it is the real target. It's also used, privately, in the stage 6 validation sessions with buyers and renters (doc 02 §10).
- **Never published as a public demo.** Hosting is private: local, or an access-restricted preview (IN-02 will be decided on that basis).
- **Deferred to before the first public product (stage 6):**
  - visitor privacy, part 1 (SE-02: privacy notice, ICO fee check, device storage);
  - demo analytics and feedback (FE-05).

  Neither is needed for a private reference.
- **Kept** (founder): the public-facing pages as part of the vision (landing, How it works, Costs and comparison), the full textured editorial illustration work, and both light and dark themes.
- **Added** (founder): a **component gallery**, one route showing every component in every state in light and dark. It's the agents' visual dictionary and the baseline for design review.
- **Unchanged:** every data rule (figures from the engine, missing never £0, no verdicts), the executable specifications (0043), and the stage gates.

## Exception: design frames shared by link (founder, 11 Nov 2026)
The founder chose to share the high-fidelity **design canvas** (the H1–H7 frames from phase 6 of the design flow, decision 0031) as "anyone with the link", to gather feedback. This is allowed because:
- the frames are static pictures, not a working demo: no accounts, no data entry, no analytics, no storage of visitors' information;
- every home, person and figure in them is synthetic sample data, labelled as such (rule 5);
- the canvas carries a note asking viewers not to share the link further.

The exception covers **design frames only**. The stage 5 clickable prototype stays private as decided above. If a frame ever gains forms, sign-in, analytics or real data, the exception lapses and SE-02 part 1 and FE-05 apply first.

## Consequences
- Doc 04 §9 stage 5:
  - the last slice (now 7, after 0046 added the area screens) becomes labelling, a simulated-action audit and the stage 5 gate, with no public launch;
  - the gate reads "on the private prototype".
- The register's "Already decided" row "First public showcase" is updated to point to this record.
- Backlog changes:
  - #90 is retitled;
  - #85 (SE-02 part 1 and FE-05) moves to stage 6, before the first public release;
  - #81 (IN-01 to IN-03) plans private hosting;
  - a new component-gallery issue sits after the app shell (#86).
- Decision 0044's domain and trade-mark tasks become less urgent, because nothing is public until stage 6. They're still needed before the first public release, now stage 5b (0046, 0009).
- **Revisit if** the founder later wants a public portfolio demo. A new record would then restore SE-02 part 1, FE-05 and public hosting before publishing.
