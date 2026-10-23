# 0014: Privacy and data protection

**ID:** SE-02  
**Status:** Proposed. The starting position below was agreed by the founder on 23 October 2026; the full decision is completed at stage 6, before the questions workflow is built.  
**Date:** 2026-10-23  
**Stage:** 6 (starting position agreed early)

## Context
Anyone can type a postcode or address and see free public details without an account. That raises three separate storage questions: the public data itself, what the visitor searched for, and what a user chooses to save. An address search can reveal something personal, namely where someone might move, so it needs care even without an account. The prototype uses sample homes only, so none of this applies until real data is introduced.

## Starting position (agreed)

| What | Stored? | How |
|---|---|---|
| **Public data** (energy certificates, sold prices, planning records, flood areas) | **Yes**, as our own copy | Downloaded from official sources on a schedule and stored per home, not per person, with source and dates. Not user data. Each dataset's licence for commercial reuse is recorded first (DA-05). |
| **An anonymous visitor's searches** | **No**, nothing linked to the person | The result is shown and the search isn't kept against the visitor. Only anonymous counts are kept (e.g. number of checks per day, how often a source has no data) to improve the product. No tracking cookies, so no cookie banner is needed for this. |
| **"Recently viewed" for anonymous visitors** | **Only in the visitor's own browser** | Kept in the browser on their device; never sent to us. |
| **A saved home record** | **Yes**, only when the user chooses Save (account likely required) | Stores the home, the user's notes, questions, documents and costs, plus a dated snapshot of the public facts as they saw them, which powers "what changed since you last looked". |

Supporting rules:
- The free view is built only from our stored copy: no paid routing and no AI calls per anonymous visitor.
- Searches are rate-limited per visitor to stop bulk copying of the dataset; some data licences may also require this.
- Anonymous counts must not be detailed enough to identify a person (for example, no full address plus time plus device combinations).

## Still to decide at stage 6
- Lawful basis under UK GDPR for each kind of stored personal data, and the privacy notice.
- Retention and deletion periods for saved records, documents and snapshots, including after a paid pass expires (linked to decision 0007 and doc 02 §8).
- Per-user isolation of uploaded documents, and how user data is excluded from AI training and shared retrieval.
- Whether ICO registration (data protection fee) is required, and a data protection impact assessment for document processing.
- How server logs (which may contain IP addresses and searched addresses) are minimised and how long they are kept.

## Consequences
The anonymous free view stays cheap, privacy-friendly and simple to explain. "Pick up where you left off" across devices requires saving a home (and probably an account). The data design keeps public-data tables separate from user tables from the start.
