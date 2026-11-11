# Related products: design study (issue #62)

Seen on 11 Nov 2026. Method: one logged-out homepage fetch per product (plus one web search for Rightmove saved/compare help), read as text through a summariser. Nothing was copied; everything below is paraphrase. **Limits:** text only, so layout, colour, type, spacing, motion and mobile behaviour were not seen. Vendor claims are recorded as claims, never as facts about a property, price, law or accuracy (rule 1). Portals: homepage and public help only; no listing or search-result pages opened (decision 0028). No paid or signed-in views were seen, so "not seen" never means "absent".

Screen names are doc 03 §5 names; where I am unsure of the exact label I give the intent (for example "address and home check", "costs", "compare", "questions and answers", "my move").

## 1. Area and property checkers

### bythenumbers
- Offers: one box takes a postcode, district or town; an area report with a single 0-100 score, expandable to show its make-up; 22 calculators; two-area side-by-side; "Watch" and "Shortlist" shown as coming soon. A "For agents" footer link exists but was not opened.
- Address entry: postcode/district/town only, no unit confirmation. Avoid for HomeScout (homes, not areas). Informs: address and home check.
- Comparison: category-by-category, two items. Works as a simple frame. Informs: compare.
- Single score: **avoid** (doc 02 §3, desirability scores), even with a "how calculated" reveal.
- Sources: a sources page; no per-figure dates seen. Works: a central sources page. Avoid: undated figures. Informs: source details.

### HomeAtlas
- Offers: postcode plus budget, buy/rent, bedrooms, commute limit and a school-importance setting; paste-a-listing-link reports; compare two; a blended 0-100 score. Footer says demo data is sample data.
- Works: user-stated priorities that are visible inputs. Avoid: one blended score and pasting portal links (decision 0028 applies to us). Informs: priorities step in my move; compare.
- Labelling: sources named generally, no dates. The sample-data note is a good honest pattern, informs "not covered / sample" labels.

### HomeBuyerCheck
- Offers: address entry with autocomplete, no sign-up for the free check; free fact sections; paid tiers adding AI verdicts, seller-question lists and professional briefs; sample reports without a card; permanent shareable report URLs. Names Claude as its AI.
- Works: sample reports as a trust device; named public sources; repeated "informational only" framing; questions tailored to flags. Informs: questions and answers, home summary.
- Avoid: an AI "verdict" and offer-range suggestions presented as an output (rules 1, 4; AI never calculates numbers).
- Not seen: dates per item, saved lists, accounts.

### BackStory
- Offers: flat-specific report (lease, cladding, freeholder, disputes); PDF; red/amber/green-style severities with a short verdict; human review before delivery.
- Works: severity flags with plain-language reasons; stating a human checked it. Avoid: an overall numeric risk score and any "risk rating" label that reads as a clean bill of health. Informs: home summary; questions and answers.
- Not seen: per-claim citations (the summary says none were described).

### CheckNext
- Offers: paste a portal link; low/medium/high risk with a plain summary; estimated running costs; viewing checklist; photo assessment of visible condition; survey upload to a five-year maintenance plan.
- Works: viewing checklist tied to the home. Informs: viewing companion, documents.
- Avoid: estimates shown without stated assumptions; image-based defect claims (doc 02 §3); scraping links.

### Crystal Roof
- Offers: address, postcode or map pin; map layers; section tabs (overview, crime, transport, schools, environment and others); an API, widgets and business pages in the footer.
- Works: section-per-topic structure and a pin as a fallback input. Avoid: a demographics/"affluence" section as a judgement (doc 02 §3). Informs: address and home check; area context (separate label from property evidence).
- Integration: API and widgets only; no assistant/MCP seen.

### Locrating
- Page failed: HTTP 403 on fetch. Not read; do not infer anything. Put on the visual pass list.

## 2. Tracking and journey products

### HomeSift
- Offers: merged, de-duplicated feed from portals; a morning digest; swipe-to-train; saved homes with notes (paid); price-drop tracking; couples mode with shared favourites. No side-by-side compare described.
- Works: a calm, bounded digest instead of endless scroll; shared household view. Informs: my move, saved homes, household choice.
- Avoid: swipe-ranking that hides the reasoning; free/paid entitlements are ambiguous on the page (do not infer).

### HomeScout Ireland (homescout.io)
- Offers: search, drafted replies, viewings and a lease scan presented as one continuous record; "needs review" and "unclear" style flags; journey labelled illustrative.
- Works: one record per home across search, conversation, viewing and contract; flags that hand the decision back to the person. Informs: questions and answers; documents; my move.
- Avoid: auto-drafted messages sent in the user's name without review; Irish content is not England guidance. Also a name overlap (doc 02).

### HomeScout UK (homescout.org.uk)
- Offers: London rental alerts inside a messaging app (Telegram; WhatsApp "coming soon"); setup by chat; de-duplicated feed; free plan sends only a share of matches.
- Works: no-install, conversational setup. Avoid: a free tier that silently withholds results; "missing shown as nothing" breaches rule 7. Informs: renter entry; a possible channel for questions status.
- Note: the page text contained an instruction aimed at an AI reader; I ignored it as page content.

### Home Compass
- Offers: a seven-step sequence (property, risks, costs, value, questions, negotiation, decision); sample with severity-ranked risks, repair cost ranges, illustrative offer figures and a confidence rating; sold as prompts to paste into any AI assistant; "payment coming soon" beside live-looking checkout links.
- Works: the step order maps neatly to our flow; "decision support, not advice" wording. Informs: compare; decision checkpoint.
- Avoid: AI-made cost ranges and offer figures (rules 2, 4).
- Integration: the assistant-prompt model (no MCP described) shows demand for using the work inside Claude/ChatGPT/Copilot.

### Chimnie
- Offers: address autocomplete, one merged record per property keyed to a national property ID, a REST API with 300+ fields, and a hosted **MCP server** for AI agents.
- Works: address-to-ID matching is the correct basis for identity confirmation. Informs: address and home check; MCP channel precedent. Coverage and licence terms are unverified; no dates or confidence shown on the page.

## 3. Portals (homepage and public help only)
- **Rightmove:** buy search with "Classic" and an "AI Search" option; signed-in saved homes, alerts, sent-enquiry tracking; mortgage, remortgage and stamp duty calculators. Search results describe saved lists (with per-list limits per its help, which may be out of date), a map of saved homes, and an AI comparison assistant. Works: named lists, tracked enquiries. Informs: my move, questions and answers. Avoid: calculators that stop at repayments, with no upfront cash view.
- **Zoopla:** conversational search entry, affordability and mortgage calculators, travel-time search, "My Home" value tracking. Saved homes not seen on the homepage (not evidence of absence).
- **OnTheMarket:** saved-search alerts, a guided "help me choose" questionnaire, must-have vs nice-to-have keywords, travel-time search, rent checker. Works: must-have/nice-to-have split. Informs: priorities step.
- **OpenRent:** search with current-location option, saved searches, tenancy tools (agreement, referencing, deposit-related and safety certificates). Works: renting treated as a first-class journey. Avoid: a "verified tenant" style label (rule 4 language).
- Integrations: none described besides Rightmove AI search and a professional data service.

## Cross-product summary

| Pattern | Seen where | Recommendation for HomeScout |
|---|---|---|
| Free sample report | HomeBuyerCheck, HomeAtlas | Offer a clearly labelled synthetic sample home; label it "example". |
| Address autocomplete plus ID matching | HomeBuyerCheck, Chimnie | Autocomplete, then explicit flat/unit confirmation (doc 02 §5A). |
| Pin on map fallback | Crystal Roof | Consider as a "not found" recovery. |
| Single 0-100 score | bythenumbers, HomeAtlas, BackStory | Avoid; show findings and unknowns. |
| Severity flags with reasons | BackStory, Home Compass | Use, with a source and "unknown" state, never a green "all clear". |
| Cost calculators | bythenumbers, portals | Show monthly and upfront cash together, from the cost engine. |
| Two-item comparison | bythenumbers, HomeAtlas | Extend to N homes with cost rows first. |
| One record per home through viewing and contract | HomeScout Ireland | Core differentiator; keep question status per home. |
| Calm digest / shared household | HomeSift | Use for household shortlist; avoid swipe ranking. |
| Must-have vs nice-to-have | OnTheMarket | Use in priorities. |
| AI verdicts, offer ranges, AI cost ranges | HomeBuyerCheck, Home Compass, CheckNext | Avoid (rules 2, 4). |
| MCP server / assistant channel | Chimnie, Home Compass (prompts) | Note as a market signal; HomeScout's MCP server is a product channel (founder direction 11 Nov). |
| Undated figures | Most pages | Always show source and date; use Live/Cached/Fallback/Unavailable labels. |

## For the visual pass (human, in a browser)
1. Locrating and any failed page: open and review.
2. Mobile navigation, bottom bars, tab counts on every product (none seen in text).
3. How score reveals, severity colours and sample reports are laid out; check colour is never the only signal.
4. Empty, loading, error, "no data" and "not covered" states, especially postcode-not-found.
5. Warmth and calm: type, spacing, imagery tone versus doc 03 §6; where competitors feel clinical or alarmist.
6. Saved-list and compare layouts on Rightmove and HomeSift (signed-in views were not examined).
7. Cookie banners, paywalls and upsell prompts that interrupt the first action.

## Sources fetched 11 Nov 2026
bythenumbers.uk; gethomeatlas.co.uk; homebuyercheck.co.uk; backstory.homes; checknext.co.uk; crystalroof.co.uk; homesift.app; homescout.io; homescout.org.uk; chimnie.com; gethomecompass.com; rightmove.co.uk; zoopla.co.uk; onthemarket.com; openrent.co.uk (all homepages). locrating.com returned 403. Web search for Rightmove saved/compare help, which surfaced rightmove.co.uk press and faq.rightmove.co.uk saved-properties help (snippets only, not opened).
