# 0033: Review fallback when Codex is unavailable

**ID:** WW-11  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2  
**Supersedes:** in [0015](0015-agent-merges-after-review.md), the requirement that Codex reviews every pull request's latest commit, **only while Codex is unavailable** and only for documentation-only pull requests.

## Context
On 23 October 2026 Codex reported: "You have reached your Codex usage limits for code reviews." Under 0015, nothing could merge until the limit reset.

## Options
- **Claude fallback for documentation-only pull requests; code waits for Codex (chosen).**
- **Add Codex credits:** reviews continue normally, at a cost.
- **Pause:** nothing merges until Codex is available.

## Recommendation
Claude fallback for documentation, code waits.

## Decision
The founder chose the fallback. While Codex is unavailable (usage limit, outage or a review stuck for over an hour):
1. **Documentation-only pull requests** (Markdown and images only, no code, workflow or configuration files) are reviewed by a **separate Claude Code review run** (the built-in `/code-review`, in a fresh context, not the session that wrote the change), following `AGENTS.md`, "When reviewing". Its findings are posted on the pull request, labelled **"Fallback review (Codex unavailable)"**, and handled with the same severity and review-round rules (0016).
2. **Pull requests with code, workflows, configuration or dependencies wait for Codex.**
3. **A pull request rebased with no content change** may merge on its earlier Codex review, if `git range-diff` shows every commit unchanged; the pull request records this (as done for #12 and #15).
4. **Use fewer reviews:** batch related changes into one pull request, and request a re-review only once per batch of fixes.

## Consequences
- The founder still merges anything on the founder-only list in `AGENTS.md`.
- When Codex is available again, normal review resumes; documentation merged under the fallback isn't re-reviewed unless a later change touches it.
