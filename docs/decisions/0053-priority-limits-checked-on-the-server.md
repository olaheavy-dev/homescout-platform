# 0053: Priority limits are checked on the server

**ID:** SE-04  
**Status:** Accepted (founder, 14 Nov 2026, in a prompt window)  
**Date:** 2026-11-14  
**Stage:** 3 (for the pilot, stage 5b)  
**Amends (no older text is rewritten):** register line FE-22's "Priorities stay in the browser and are never sent or stored"

## Context
FE-22 (13 Nov 2026) lets a visitor to the area check pick what matters to them and set a measurable limit, for example "a GP within a 15-minute walk". Each topic then shows which facts meet or miss that limit, never a total or a score. FE-22 also said priorities stay in the browser and are never sent or stored.

"Meets or misses" is a calculated result. `AGENTS.md` rule 2 says calculated outputs come from tested code, never typed by hand. The pilot design review on 14 Nov 2026 (`docs/reviews/2026-11-14-pilot-design-review.md`) found that nothing said where this calculation lives. If priorities never leave the browser, the server cannot work it out.

## Options
### Option A: A tested function in the browser
A small function in the frontend compares each fact with the visitor's limit, with its own independently worked test examples. Priorities stay on the device. The cost is a second place where calculations live, with its own tests. This was the agent's recommendation.

### Option B: Send the limits to the server
The browser sends the visitor's limits with each area check, in the request body. A tested module on the server, beside the other area calculations, works out meets or misses and returns it with the facts. All calculations stay in one place. The visitor's limits leave their device.

### Option C: Show the fact beside the limit, with no calculation
Show "0.8 miles" next to "your limit: 1 mile" and let the visitor judge. No calculation at all, but it loses the at-a-glance value FE-22 asked for.

## Decision
**Option B** (founder, 14 Nov 2026, prompt window: "Send limits to server", over the agent's recommendation of Option A).

**Privacy rules that come with it** (they extend [0014](0014-privacy-and-data-protection.md) and the pilot design's privacy section, which already cover the postcode):
- Limits travel only in the request body, never in a query string or a URL that reaches a log.
- Limits are never written to server, application, hosting or tracing logs, and never stored. The server forgets them when the response is sent.
- Limits are not passed to the area chat or the AI tools unless a later decision says so.
- A worship priority stays faith-neutral, as PD-13 requires: the limit is "any place of worship within <distance>", never a named faith, so what is sent names no faith. It may still suggest that the visitor practises a religion. The ICO says inferred data is special category data where processing "intends to make an inference linked to one of the special categories" ([ICO: what is special category data](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/), read 14 Nov 2026); we make no such inference, but the line is close. A visitor's own faith is never asked for, sent or stored ([0014](0014-privacy-and-data-protection.md)). Before launch, the privacy review (SE-02, part 2) decides whether a worship limit is sent like the others or checked only in the browser.
- A limit that is missing, or a fact that is missing, shows as unknown, never as a miss (rule 7).
- The privacy notice says that priorities are sent to work out the comparison, are not kept, and are not logged.

**How it is calculated:** a tested module on the server, with test expectations worked out independently of that module (rule 2). Distances are compared in metres, the stored unit, and shown in the country's display unit (register line FE-27).

## Consequences
- **FE-22's "priorities stay in the browser and are never sent or stored"** now reads "never stored or logged". Remembering the visitor's choices between visits stays in the browser and is off until the visitor turns it on, which is their consent under PECR, as for Recent postcodes.
- **The priorities specification** (first design batch, founder 14 Nov 2026: "First batch") includes scenarios for the request body only, no logging, and unknown never shown as a miss.
- **The log-privacy checks at the pilot gate** (decision 0052) cover limits as well as postcodes.
- **Revisit if** the pilot adds share links or a printed report that include priorities, because those would carry limits outside the request body.
