# 0037: MCP server and coding-agent integrations

**ID:** AI-07  
**Status:** Proposed  
**Date:** 2026-11-06  
**Stage:** 6 for the remote server; a local fixture-backed server may come earlier (see "Decision")

## Context
The founder wants HomeScout to offer MCP servers that people can connect to Claude, Codex, GitHub Copilot and ChatGPT, alongside the API and HomeScout's own Next.js UI. The founder also asked whether UI components can appear inside those tools, and whether to build for Claude first.

What the official documentation says (checked on 6 November 2026; host support changes quickly, so re-check before relying on it):
- **MCP Apps** is an extension to MCP. A tool declares `_meta.ui.resourceUri` pointing to a `ui://` resource, an HTML page the host renders in a sandboxed iframe inside the conversation ([MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview)).
- **Supported hosts** listed by the MCP project: Claude, Claude Desktop, VS Code GitHub Copilot, Microsoft 365 Copilot, Goose, Postman, MCPJam and Archestra.AI. ChatGPT is not on that page, but the [January 2026 launch post](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) says ChatGPT shipped support, and [OpenAI's guide](https://developers.openai.com/plugins/build/chatgpt-ui) recommends the open `_meta.ui.resourceUri` field instead of its older OpenAI-specific key.
- **Codex:** inline rendering was reported broken in Codex Desktop ([#21019](https://github.com/openai/codex/issues/21019)); that issue was closed as completed on 5 August 2026, and a comment says a fix shipped behind a feature flag (check the current flag name in the Codex documentation before relying on it). A narrower issue is still open: widgets from nested MCP calls inside `functions.exec` aren't rendered ([#36765](https://github.com/openai/codex/issues/36765)). Both are user reports, so test before promising anything. OpenAI's own guidance says tools should work without any UI so ChatGPT and Codex can finish a workflow without a widget.
- **FastMCP** has supported MCP Apps since version 3.0.0, through a tool's `AppConfig` and a `ui://` resource ([low-level Apps page](https://gofastmcp.com/docs/apps/low-level)). Its higher-level `fastmcp[apps]` path depends on Prefab, which its docs describe as changing quickly. Check the current FastMCP major version and licence before pinning.

## Options
### Option A: Open standard, Claude first, tools before widgets (recommended)
Build tools that work everywhere, then widgets using the open MCP Apps standard, tested in Claude first and then other hosts.

### Option B: Claude-only UI
Faster to the first widget, but host-specific code is rework later and gains nothing: the open standard is no harder to write.

### Option C: Tools only, no UI in other tools
Simplest. Gives up the one thing an MCP server can offer that a chat answer can't: an interactive cost or comparison view inside the conversation.

## Recommendation
Option A.

## Decision
To be confirmed by the founder. Proposed:

**Shape**
- One MCP server, written in Python with FastMCP, in the same repository as the API. It is a thin adapter: every tool calls the same cost engine and data the API uses, so there is one source of every figure.
- **Read-only first.** Tools read the cost breakdown, the comparison and the evidence for a home. Nothing writes data until a later decision covers it.
- **Where the guarantees stop.** Decision 0004 and rules 4 and 7 bind HomeScout's own tool outputs and widgets. They can't bind the model inside Claude, ChatGPT, Codex or Copilot, and decision 0025's output guards can't run on another host's model. To reduce the risk: every figure a user might ask about, including differences, is worked out by the engine and returned as a tool result with its figure ID, so the host never needs to calculate; tool descriptions say "quote figures by ID; do not calculate them or judge a home safe"; and the docs say plainly that host wording is outside HomeScout's control. A one-line register note (or a short addition to 0004) records that 0004 applies to HomeScout's outputs only when the model is a third party's.
- Tool outputs carry the stable figure IDs (BE-11) and each value's source and Live, Cached, Fallback or Unavailable label (0029). Text from users or documents returned by a tool is data, never instructions (0025). Outputs and widgets never say a home is "verified", "safe" or "approved" (rule 4), never show missing data as zero (rule 7), and the model never calculates a figure (0004).
- A "not yet covered" result for homes outside England (rule 6).

**Order of work**
1. **Tools and structured data.** Must be fully useful with no UI. Tested in Claude Code and Codex.
2. **Widgets,** such as a cost breakdown card and a comparison table, using only the open `_meta.ui.resourceUri` and `ui://` standard (no host-specific keys such as OpenAI's older `openai/outputTemplate`). Each is a small self-contained bundle, not the Next.js app, sharing design tokens with it. Built and tested in Claude and Claude Desktop first, then VS Code Copilot, then ChatGPT and Codex as best effort. FastMCP's low-level `AppConfig` and `ui://` pattern is used, serving our own bundled HTML, until its higher-level path settles.
3. **Remote access and OAuth** for claude.ai and ChatGPT connectors, after the API-key phase in decision 0038.

**Local first.** A local (stdio) server reading only the synthetic fixtures needs no auth and can ship with the prototype as a try-it-yourself demo. A remote server needs decision 0038.

**Host support table.** `docs/planning/mcp-host-support.md` (created with the first tool and listed in the docs index; `docs/references/` is for links to official documentation, not test logs) records, for each host: tools tested, widgets tested, auth method accepted, test date and result. Entries are dated so the page can't silently go stale.

**Relationship to Microsoft Agent Framework (0023).** HomeScout's own agents are separate from this server. They may call the same engine directly or consume the MCP tools; either way the engine is the only calculator.

## Consequences
- **Privacy:** tool outputs go to a third-party model provider under the user's own account. Remote tools return only public or synthetic data until SE-02 part 3 (decision 0014) covers sharing user documents or saved-home data with hosts.
- **Roadmap:** doc 04 (§5 and the stage 6 table) is updated when this is accepted.
- New packages (FastMCP and its dependencies) need founder approval and an entry in `docs/references/third-party.md` with licence checked (0027).
- Depends on decision 0036 (Python). If 0036 is not accepted, this record is revisited: the official C# MCP SDK would be the alternative.
- Widgets add a small front-end build for the bundles; the design skills (0031) produce their brief.
- The prototype (stage 5) stays fixture-only and account-free; the local MCP demo doesn't change that.
- Revisit when a host's support changes, or when a host accepts a different auth method.
