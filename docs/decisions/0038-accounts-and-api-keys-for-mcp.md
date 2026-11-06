# 0038: Accounts and API keys for MCP and API access

**ID:** SE-03  
**Status:** Proposed  
**Date:** 2026-11-06  
**Stage:** 6 (before any public remote MCP server or API); partly brings forward SE-01

## Context
The founder wants authentication built in, even though this is a portfolio project, with users generating API keys for their MCP connections. Today SE-01 (accounts) is scheduled for stage 6, before the questions workflow, and the prototype (stage 5) is fixture-only with no accounts. A remote MCP server (decision 0037) needs callers to be identified before it is public.

What hosts accept (taken from third-party setup guides, not official Anthropic, OpenAI, GitHub or Microsoft documentation, so **unverified**: check each official configuration page before promising anything): Claude Code, Codex and VS Code can send a bearer-token header, so an API key works for them. Whether claude.ai custom connectors and ChatGPT accept a raw API-key header is **unconfirmed**; their connector flows appear to be OAuth-based. FastMCP offers token-verification hooks and a static-token verifier that its docs position for development and prototyping only ([FastMCP token verification](https://gofastmcp.com/servers/auth/token-verification)).

## Options
### Option A: API keys first, OAuth later (recommended)
Signed-in users create keys for coding agents now; add OAuth when claude.ai and ChatGPT connectors are wanted.

### Option B: OAuth only
Works with every host but is the largest piece of work and delays any remote use.

### Option C: No auth, fixture data only
Acceptable only for the local, fixture-backed server. Not acceptable for any remote server that returns anything but public synthetic data.

## Recommendation
Option A.

## Decision
To be confirmed by the founder. Proposed:

**Accounts.** Creating a key needs a signed-in user, so a minimal account system comes with this work. The identity provider and account model are chosen under SE-01 before building; this record doesn't pick one. Household sharing is not part of this slice.

**Keys.**
- Random, high-entropy, with a visible prefix that identifies the key type and an id; shown to the user **once** at creation.
- Stored only as a hash, with the prefix and last four characters kept for display. The exact hashing approach is set in the plan and checked against current guidance.
- Each key has a name, **scopes** (for example read costs, read comparisons), an **expiry**, a **last-used** time, and can be **revoked** immediately.
- Per-key rate limits. Keys are never written to logs, error messages or tool outputs, and the redaction is tested.
- Keys are secrets: the repository never contains a real one (rule 5); tests use obviously fake keys.
- FastMCP's static-token verifier is not used outside local development. Production uses our own verifier that checks the hash and scopes.

**Later phase: OAuth** for claude.ai and ChatGPT connectors, once their official docs confirm what they accept (decision 0037, host support table).

**Privacy.** Accounts add personal data (an email address at least) and usage logs. Decision 0014 and SE-02 parts 2 and 3 must be settled for that data before the remote server goes public; the privacy notice covers it.

## Consequences
- The roadmap changes: a small accounts and keys slice is planned before any public remote MCP server, instead of staying inside stage 6 step 5. The clickable prototype (stage 5) is unaffected.
- An identity provider and a database are needed, so DA-03, SE-01 and the hosting cost (0022) need decisions first. Adding either raises running costs, so the founder approves it.
- Auth code is ordinary code under `AGENTS.md`, but this record proposes adding authentication and key-handling changes to the founder-only merge list. That is a merge-rule change, so the founder merges it, in the pull request that accepts this record.
- Doc 04 (§5 and the stage 6 table) and the SE-01 register row ("6, before questions workflow") are updated when this is accepted.
- Revisit if a host's connector docs change what it accepts, or if keys prove awkward for the target users.
