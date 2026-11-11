# Design patterns from outside the property category (issue #63)

Checked 11 Nov 2026. Method: official pages read with WebFetch/WebSearch, which return text, not visuals; the fetch tool summarises pages, so wording below is paraphrased and a few details may be incomplete. Nothing here is copied. Anything marked **unverified** was not confirmed. A visual pass should check: GOV.UK component spacing, status-tag colours and focus rings in the live component pages; the MoneyHelper calculators in a browser; Monzo's Trends screens in the app; how Claude, ChatGPT and VS Code actually render approval prompts and tool results.

Screen names follow doc 03 §5. "Chat" = agent chat (#78, decision 0004). "MCP" = tool surface (#117).

## 1. GOV.UK Design System

Solves long, error-prone form journeys for the public. Licence: the pages say content is under the Open Government Licence v3.0 with a Crown copyright notice; the fetched page did **not** state terms for code, the crown logo, GOV.UK branding or the Transport font (unverified). Recommendation: imitate the patterns, do not reuse the branding or font, and do not imply government endorsement.

- **Task list.** Users pick tasks in any order; each row shows a short status; the whole row is the link; names short, sentence case; hints one short sentence with no links; hold off if the service can be simplified. Use: the buyer/renter "My move" checklist and the questions-to-resolve list on a home (Home overview, My move/activity). Statuses must be words plus colour, matching doc 03 §6.
- **Question pages and error summary.** One clear question per page; on error, show a summary at the top of the main area, move focus to it, link each message to its field (first option for radios), and repeat the same wording beside the field; prefix the page title with "Error". Use: Identity confirmation, editable cost inputs in Real costs, Question detail forms.
- **Check answers / summary list.** Review everything before sending; rows of question, answer and a "Change" link with hidden item-specific text; unanswered optional items read "Not provided"; return the user to the review page after an edit. Use: Share / snapshot preview, and the "copied, not yet recorded as sent" request state. "Not provided" is a direct model for rule 7: missing is stated, never blank or zero.
- **Warning text vs inset text.** Warning text is for consequences that matter, with a hidden "Warning" prefix for screen readers; inset text is for supporting asides and should be used sparingly because people skip it. Use: warning for expired certificate, failed source request and Wales/Scotland "not yet covered"; inset for source and scope notes.
- **Details.** Hides content only some users need; not for what most need; short, descriptive label; voice-control and toggle-discovery issues noted. Use: "How this was worked out" under a figure. **Avoid** hiding the caveat itself inside a collapsed section (rule 7).

Avoid: the GOV.UK crown, colours or font.

## 2. MoneyHelper calculators

Fetch of the mortgage calculator returned HTTP 403; search results showed only navigation (mortgage calculator, affordability, repayment, stamp duty, overall buying and moving costs pages exist). **Everything about their presentation is unverified; a manual visual pass is required.** Provisional reading from page titles: separate tools for monthly repayment, upfront tax and moving costs, which mirrors Vestagraph's split of monthly estimate and upfront timeline (Real costs). Check on the visual pass: whether assumptions sit beside the result, whether editable inputs are labelled with units, and how results and disclaimers are worded. Do not copy figures or thresholds; Vestagraph's come from the cost engine (rule 2).

## 3. W3C ARIA Authoring Practices (WCAG 2.2 AA target)

Solves keyboard and screen-reader behaviour for custom widgets.

- **Tabs.** Roles tablist/tab/tabpanel, aria-selected, aria-controls; Tab enters the list then the panel; arrow keys move between tabs; Home/End optional. Automatic activation only if panels appear instantly, otherwise manual (Enter/Space). Use: the home tabs (Overview, Nearby, Costs, Viewings, Questions, Documents, Activity); Nearby and Documents load slowly, so prefer manual activation there. On mobile the bottom navigation is navigation links, not tabs.
- **Combobox.** Input with role combobox, listbox popup, aria-expanded, focus stays on the input via aria-activedescendant; Down opens, Enter accepts, Escape closes. Use: address search on the landing page and Identity confirmation. Use "list" autocomplete with manual selection so a postcode never silently picks a flat (doc 03 §5).
- **Disclosure.** A button with aria-expanded toggled by Enter/Space. Use: assumptions and "how worked out".
- **Modal dialog.** role dialog, aria-modal, labelled title, focus moves in, Tab cycles inside, Escape closes, focus returns to the opener; for irreversible actions focus the least destructive option. Use: the full-screen evidence sheet on mobile, share confirmation, and the chat approval card if modal. Use aria-modal only if the rest of the page is truly blocked.

Avoid: a map without a list alternative (doc 03 §5), and any status shown by colour alone (doc 03 §6).

## 4. FT Visual Vocabulary

Groups charts by the job: deviation, correlation, ranking, distribution, change over time, magnitude, part-to-whole, spatial, flow. Inference for Vestagraph (the page does not discuss costs): magnitude bars for comparing monthly costs across homes; part-to-whole stacked bar or waterfall for how a monthly total builds up; deviation for "against your budget"; change over time for rent or service charge history; avoid flow diagrams (too busy for lay users). Bars start at zero. Apply doc 03 §6: direct labels, units, same scale across compared homes, uncertainty shown as a range with the assumption beside it. **Avoid:** ranking homes into a single winner (Compare "no universal winner"), and drawing a missing value as a zero-height bar; use a labelled gap ("not known") instead. Use: Real costs, Compare, Decision impact (before/after delta from the engine).

## 5. A UK bank's spending breakdowns (Monzo)

Direct page fetches 404'd; the summary comes from search results of Monzo help pages (**partly unverified, older content mixed with newer**). Pattern: a Trends area with Balance, Spending and Target views; monthly or yearly overview; split by category or by merchant via a toggle; income, savings and transfers kept out of "spending"; a target per category defaulting to last month's amount. Use: the monthly estimate by category, with different kinds of money kept apart (rent, deposit, one-off fees, running costs) and a toggle between monthly and upfront. Calm tone comes from few colours, plain labels, no alarm. **Avoid:** default targets or "you're over" nudges, and personalised suggestions that read like advice (decision 0004: no confident claims about unknowns).

## 6. AG-UI and CopilotKit

- **AG-UI events (docs.ag-ui.com).** A run has start and finish or error events; messages and tool calls stream as start, content, end sequences linked by an ID; tool results arrive as one complete result; state arrives as a snapshot plus JSON-Patch deltas; custom named events are allowed if documented. Chat use: show text as it streams, show a quiet "Checking costs" line per tool call (doc 03 §6: no theatrical agent activity), then the result; show the error event as a visible failure, not an empty answer. Process events in arrival order.
- **CopilotKit.** Offers generative UI, human-in-the-loop and shared state. Human-in-the-loop: the model calls a client-side tool, the chat renders a component (for example a picker), the user's answer returns as the tool result and the run continues; status of the tool call is shown inline. Use: confirmation cards for any record change (decision 0004: no changes without confirmation), and a figure card that renders a cost-engine result rather than free text. I could not confirm the exact page for tool-call rendering (**unverified**); check docs.copilotkit.ai before #78.

Avoid: letting generated UI invent numbers; figure cards must be filled from engine output only (rule 2, rule 4).

## 7. Agent channel: MCP and assistants

Specification read: the version served as "latest" was dated 2026-07-28 (check which version the C# SDK targets).

- **Tools.** Model-controlled; schema-defined inputs; optional outputSchema; results may carry structuredContent (plus a text copy), resource links and embedded resources, each with audience/priority/lastModified annotations. The spec says there should always be a human able to deny calls, clients should show inputs before sending, and tool annotations are untrusted unless the server is trusted. Execution errors use isError so the model can self-correct.
- **Resources and prompts.** Resources are application-controlled context identified by URIs (the user or app picks them); a missing resource must be an error, never an empty list (a close parallel to rule 7). Prompts (not fetched in detail) are user-triggered templates.
- **Elicitation.** Servers can ask the user for input in form mode (flat primitive fields, with accept/decline/cancel outcomes) or URL mode for anything sensitive; form mode must not ask for secrets. Use: ask which unit or which tenure; send document upload and sign-in to our own web page via URL mode.
- **Assistants.** Claude's help pages say it asks before invoking connector tools, with per-tool settings of always allow, needs approval or blocked, grouped by read-only and write tools, and warn of prompt injection and that research mode can run tools without per-call approval. VS Code Copilot shows a trust review for servers, tool-approval requests, expandable tool calls and input forms (and experimental MCP Apps UI). ChatGPT: the Apps SDK index page confirms tools, optional UI resources, and a security guide; confirmation, citation and UX-guideline detail was not retrieved (**unverified**).

### Principles for Vestagraph inside someone else's assistant

1. **Figures are engine outputs with IDs.** Every number returned carries a stable figure ID, its period and its basis; tools never return a prose-only number; the assistant is told to quote, not recompute (rules 2, 4).
2. **Sources travel with answers.** Return source name, date and scope as structured fields and resource links, so the host can show citations; no claim without a source or an explicit "not known".
3. **Missing and partial are explicit states.** Use status values (known, estimated, missing, not covered, source failed) in the output schema; a missing value is null with a reason, never 0 or an empty list; Wales/Scotland/Northern Ireland return "not yet covered".
4. **Never output the forbidden words.** Results carry no "verified", "safe" or "approved" labels, and the tool descriptions tell the model not to add them; test this in the evaluation set (decision 0004).
5. **Read tools are open, write tools need approval.** Mark reads and writes separately so hosts can group them; any write (create question, record decision, mark sent) needs a host approval plus a recorded confirmation, and "copied but not sent" stays a distinct state. Assume the host's approval UI may be skipped (for example, research modes), so server-side confirmation is the real guard.
6. **Elicit narrowly.** Ask only for what the next step needs (nation, buy or rent, unit) via form mode; never request credentials or documents in form mode; use a URL to our own site for sign-in and private document upload.
7. **Privacy by minimum.** Return the smallest slice of a home record, no private document text unless asked and permitted, scopes per tool, and assume the assistant's provider sees everything returned. Treat all tool inputs from the model as untrusted and validate them; treat prompt injection in listings or documents as expected.
8. **Hand off to the app for depth.** Return a link to the home record or snapshot for evidence sheets, comparisons and charts that a chat cannot show well; use the web app for visual detail.

## Summary table

| Pattern | Source | Vestagraph use |
|---|---|---|
| Task list with word statuses | [GOV.UK task list](https://design-system.service.gov.uk/components/task-list/) | My move, questions to resolve |
| Error summary linked to fields | [GOV.UK error summary](https://design-system.service.gov.uk/components/error-summary/) | Cost inputs, forms |
| Check answers, "Not provided" | [GOV.UK check answers](https://design-system.service.gov.uk/patterns/check-answers/) | Share / snapshot, missing-data wording |
| Warning vs inset text | [GOV.UK warning](https://design-system.service.gov.uk/components/warning-text/), [inset](https://design-system.service.gov.uk/components/inset-text/) | Caveats and source notes |
| Details for secondary content | [GOV.UK details](https://design-system.service.gov.uk/components/details/) | "How worked out" (not caveats) |
| Tabs, manual activation | [APG tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/) | Home tabs |
| Combobox, manual selection | [APG combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) | Address search |
| Modal dialog, focus return | [APG dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Evidence sheet, approvals |
| Magnitude and part-to-whole charts | [FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) | Real costs, Compare |
| Category split, separate income | [Monzo help](https://monzo.com/help/budgeting-overdrafts-savings/trends-spending-and-balance-web) | Monthly cost breakdown |
| Streaming events, tool-call lifecycle | [AG-UI events](https://docs.ag-ui.com/concepts/events) | Chat #78 |
| Human-in-the-loop cards | [CopilotKit](https://docs.copilotkit.ai/human-in-the-loop) | Chat confirmations |
| structuredContent, outputSchema, isError | [MCP tools](https://modelcontextprotocol.io/specification/latest/server/tools) | #117 |
| Resource links and annotations | [MCP resources](https://modelcontextprotocol.io/specification/latest/server/resources) | #117 sources |
| Form vs URL elicitation | [MCP elicitation](https://modelcontextprotocol.io/specification/latest/client/elicitation) | #117 approvals, privacy |
| Per-tool permissions | [Claude custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) | #117 read/write split |
| Server trust and tool approval | [VS Code MCP](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) | #117 |

## Sources

- https://design-system.service.gov.uk/ (components and patterns above; get-started page for licence)
- https://www.moneyhelper.org.uk/en/homes/buying-a-home/mortgage-calculator (403; unverified)
- https://www.w3.org/WAI/ARIA/apg/patterns/ (tabs, combobox, dialog-modal, disclosure)
- https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
- https://monzo.com/help/budgeting-overdrafts-savings/trends-spending-and-balance-web
- https://docs.ag-ui.com/concepts/events
- https://docs.copilotkit.ai/ and https://docs.copilotkit.ai/human-in-the-loop
- https://modelcontextprotocol.io/specification/latest/ (server/tools, server/resources, client/elicitation)
- https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp and https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- https://developers.openai.com/apps-sdk/
- https://code.visualstudio.com/docs/copilot/customization/mcp-servers
