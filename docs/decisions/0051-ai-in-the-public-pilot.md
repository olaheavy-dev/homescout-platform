# 0051: AI in the public pilot — an area chat and a public read-only MCP server

**ID:** PD-14  
**Status:** Accepted (founder, 13 Nov 2026, in prompt windows)  
**Date:** 2026-11-13  
**Stage:** 5b  
**Supersedes in part (no older text is rewritten):** [0038](0038-accounts-and-api-keys-for-mcp.md) Option C's limit ("not acceptable for any remote server that returns anything but public synthetic data") for the area tools only; [0046](0046-public-area-check-first.md)'s pilot scope (no AI named) and its "then accounts" order for the MCP server; [0004](0004-ai-in-the-product.md)'s rule that the chat "only answers about the current home", extended to the current area; the register's stage 6 timing for AI-01 and AI-04 (brought forward to 5b for the pilot)

## Context
The public pilot (stage 5b, 0046) lets anyone check what is around a postcode with no account. On 13 Nov 2026 the founder asked for AI in it, in two places: "both, on the page and in their own ChatGPT or Claude", from day one. The design, approved by the founder the same day, is `docs/superpowers/specs/2026-11-13-pilot-area-ai-design.md`.

Three earlier records stood in the way:
- 0038 allows a remote MCP server without keys only for synthetic fixture data, and plans accounts and keys first.
- 0046 names no AI in the pilot and puts accounts before the MCP server.
- 0004 lets the chat answer only about the current home.

## Options
### Option A: Staged pilot (recommended by the agent)
The area check and the public read-only MCP server launch first; the on-page chat follows a few weeks later with a daily spend cap, once traffic and abuse are known. Lowest risk; almost no AI running cost on day one, because a visitor's own assistant pays for its AI.

### Option B: Both on day one
The MCP server and the on-page chat launch with the area check. A bigger launch; the AI bill and abuse exposure start with everything else, so every safeguard becomes a launch blocker.

### Option C: Area check alone, AI at stage 6
Today's plan. Cheapest, but drops the founder's request.

## Recommendation
Option A, for the lower day-one risk. Option B is workable if every safeguard below blocks launch.

## Decision
**Option B**, the founder's choice ("Both on day one", 13 Nov 2026), with these answers, each from a prompt window on 13 Nov 2026:
- Where: "both, on the page and in their own ChatGPT or Claude".
- Disclaimer: the founder asked "can we not have disclaimer?"; yes, a short disclaimer in the chat and the MCP server's description, on top of the safeguards, never instead of them.
- AI provider: "No training, short checks OK (Recommended)": standard business terms are accepted if inputs are never used for training and are kept only briefly for abuse checks; the privacy notice names the provider and how long it keeps inputs. Zero retention is not required.
- Design: "Approve (Recommended)".

What this allows, and its limits:
1. **A public, read-only MCP server without keys,** for public area data only (the area tools in the design). No home, cost, document or personal data, and no write tool. Any other tool on a remote server still needs 0038's accounts and keys.
2. **An on-page area chat** on the public pilot: an optional, closable panel (0004) that answers only about the area result on the page, using the area tools, with every claim sourced or "not known", never calculating, never calling an area safe or good, never scoring crime, flood or places of worship (PD-13).
3. **Launch blockers:** the IN-05 monthly cap and a daily AI cap (the chat then shows an honest "paused for today" state); rate limits (a global and a per-host cap for the MCP server, whose calls come from the hosts' servers); a bot check on the chat; no postcode, message text or tool argument in any log (0014); the privacy notice covering the chat (SE-02 parts 1 and 2); an evaluation set the chat and tools pass (AI-03, 0025).

## Consequences
- **AI-01 (model provider) and AI-04 (orchestration)** move from stage 6 to stage 5b for the pilot, and AI-09's trial runs first (below).
- **0038** still governs every other remote tool; this record adds one narrow exception.
- **0046's pilot** gains the AI pieces; its data decisions (DA-03 to DA-06, BE-02, IN-01 to IN-05) still come first, and the area tools read only our cached copies.
- **Doc 04 §9 and the register** change with the pull request that adds this record.
- **Revisit if** AI spend reaches the daily cap on most days, abuse gets past the limits, the evaluation set shows answers breaking 0004's rules, or a host's terms rule out a keyless server.

## Framework timing
Founder, 13 Nov 2026, asked in a prompt window: "Trial first (Recommended)". AI-09's short trial (Microsoft Agent Framework for Python against LangChain with LangGraph) runs at the start of the pilot's AI work, and its winner builds the chat (AI-04). The other option was the provider's own SDK behind a small interface, with the trial at stage 6.
