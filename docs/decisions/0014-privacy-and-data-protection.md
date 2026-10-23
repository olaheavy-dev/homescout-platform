# 0014: Privacy and data protection

**ID:** SE-02  
**Status:** Proposed. The starting position below was agreed by the founder on 23 October 2026; the decision is completed in three parts: **visitor data, before the first public deployment** (stage 5, the clickable prototype); **public-record data and logs, before any real data is loaded** (stage 6, step 4); and **the full decision, before the questions workflow** (stage 6, step 5).  
**Date:** 2026-10-23  
**Stage:** 5 (part 1), 6 step 4 (part 2), 6 step 5 (full decision)

## Context
Anyone can type a postcode or address and see free public details without an account. That raises three separate storage questions: the public data itself, what the visitor searched for, and what a user chooses to save. An address search can reveal something personal, namely where someone might move, so it needs care even without an account. The prototype uses sample homes only, so the questions about public records and searched addresses don't arise until real data is introduced. **Visitor data still applies from the first public deployment:** hosting and security services handle visitors' IP addresses, browser details and logs even for a sample-data demo (see part 1 below).

## Starting position (agreed)

| What | Stored? | How |
|---|---|---|
| **Public data** (energy certificates, sold prices, planning records, flood areas) | **Yes**, as our own copy | Downloaded from official sources on a schedule and stored per home, not per person, with source and dates. Kept separate from visitor and account data, but **not automatically free of personal data**: some public sources can contain personal information, which remains subject to UK GDPR (see part 2). Each dataset's licence for commercial reuse is recorded first (DA-05). |
| **An anonymous visitor's searches** | **No**, nothing linked to the person | The result is shown and the search isn't kept against the visitor. Only anonymous counts are kept on our servers (e.g. number of checks per day, how often a source has no data) to improve the product. **This includes logs:** searched addresses are never written to server or application logs, and IP addresses are dropped or anonymised before logs are written (any short-lived raw use, such as rate limiting, is kept in memory only). This must be in place before real searches are accepted. Nothing is stored on or read from the visitor's device for this, so it needs no consent under PECR. |
| **"Recently viewed" for anonymous visitors** | **Only in the visitor's own browser, and only if they switch it on** | Never sent to us. Storing it on the device is covered by PECR (the ICO includes web storage, and using browsing history to choose what to show is not exempt), so it is **off by default**. The visitor turns on "Remember homes on this device", which serves as their consent, and can clear it at any time. Assess against [ICO guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/what-are-the-exceptions/) before building. |
| **A saved home record** | **Yes**, only when the user chooses Save (account likely required) | Stores the home, the user's notes, questions, documents and costs, plus a dated snapshot of the public facts as they saw them, which powers "what changed since you last looked". |

Supporting rules:
- The free view is built only from our stored copy: no paid routing and no AI calls per anonymous visitor.
- Searches are rate-limited per visitor to stop bulk copying of the dataset; some data licences may also require this.
- Anonymous counts must not be detailed enough to identify a person (for example, no full address plus time plus device combinations).

## Still to decide
**Before the first public deployment (stage 5):**
- Lawful basis and a short privacy notice for data about anonymous visitors that the site, hosting and security services handle: IP addresses (an IP address used to tell visitors apart can be personal data, see [ICO guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/what-is-personal-data/what-are-identifiers-and-related-factors/)), browser details, and the hosting provider's own logs. This applies even when IPs are only held in memory for rate limiting.
- Whether the project must pay the [ICO data protection fee](https://ico.org.uk/for-organisations/data-protection-fee/faqs-data-protection-fee-payment-and-online-registration) or is exempt; pay it before going public if required.
- A PECR check of anything the demo stores on or reads from the visitor's device (for example preferences or session storage), confirming each item is strictly necessary or has consent.

**Before real data is loaded (stage 6, step 4):**
- Lawful basis under UK GDPR and the privacy notice, explicitly covering **personal data that appears in public records** (for example, council planning records can include applicants' names and addresses). Check each source's actual fields at ingestion rather than assuming; HM Land Registry Price Paid Data, for instance, has no person-name fields ([schema](https://www.gov.uk/guidance/about-the-price-paid-data)). Publicly available data still carries data-protection obligations, and the [ICO requires the lawful basis to be set before processing begins](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/). Decide which personal fields to drop on ingestion.
- Lawful basis and privacy-notice wording for **search inputs**: the postcode or address a visitor types is potentially personal data (it can reveal where they may move), and receiving and using it, even briefly and alongside an IP used for rate limiting, is processing. This must be covered before real searches are accepted, even though searches aren't stored.
- How logs are configured to meet the search-retention rule above, and how long any logs are kept.

**Before the questions workflow (stage 6, step 5):**
- Lawful basis for each kind of personal data users store (accounts, saved homes, documents), and the privacy notice update.
- Retention and deletion periods for saved records, documents and snapshots, including after a paid pass expires (linked to decision 0007 and doc 02 §8).
- Per-user isolation of uploaded documents, and how user data is excluded from AI training and shared retrieval.
- Recheck the ICO fee position for the new processing, and a data protection impact assessment for document processing.
- Extend the PECR assessment to the full product (sign-in sessions, browser storage, rate-limiting techniques).

## Consequences
The anonymous free view stays cheap, privacy-friendly and simple to explain. "Pick up where you left off" across devices requires saving a home (and probably an account). The data design keeps public-data tables separate from user tables from the start.
