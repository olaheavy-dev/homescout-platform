# 0022: Cost-first hosting

**ID:** IN-00  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2 (sets the rule for stage 4's IN decisions)  
**Supersedes:** the "Microsoft Azure" cloud choice in the historical brief (doc 01 §13) and doc 04 §6's "the brief's Azure stack stays". Azure becomes a fallback, not the default.

## Context
After reviewing the founder's earlier projects, the founder clarified how hosting should be chosen. The founder already runs a self-managed virtual server with a deployment kit for several apps, and the project runs on a small monthly budget.

## Options
- **Azure first (previous direction):** a single cloud and strong Azure learning value, but every service is a new monthly cost.
- **Cost first (chosen):** use the founder's existing server and free tiers first; use Azure (or another paid service) only where no free or cheaper option meets the need.
- **Free tiers only:** cheapest, but some later needs (a database with geospatial support, background jobs) may not fit.

## Recommendation
Cost first.

## Decision
Founder's words: "we can host on the infra and just use only bits that we need, azure first if there are no cheaper or free alternatives." For each hosting need, the order of preference is:
1. **Free options**, for example free static hosting for the fixture-only prototype.
2. **The founder's existing server**, for anything that needs a running service (later the API, PostgreSQL with PostGIS, background jobs).
3. **Azure, or another paid service**, only where neither of the above meets the need, chosen for the lowest cost that does.

## Consequences
- Stage 4's decisions (IN-01 to IN-05) compare options in this order. Infrastructure-as-code follows whatever is chosen; Bicep is used only for any Azure parts.
- **HomeScout's repository stays public-safe:** it holds only the app's own deployment files (for example a container build and a Compose file with placeholders). Server addresses, hostnames, credentials and registration live in the founder's private infrastructure repository, passed in as GitHub variables or secrets.
- **Before HomeScout deploys to the existing server**, these issues found in the review must be addressed: secrets kept as plain files on the server, automatic deployment of the latest image without a gate, long-lived provider tokens, real IP addresses in its documentation, and no metrics or spend alerts.
- The budget cap (IN-05) covers all paid services, wherever they run, plus a share of the server's running cost.
- AI providers (AI-01) follow the same rule: the cheapest provider that passes the evaluation suite.
- Less Azure-specific learning than first planned; the portfolio story becomes cost-conscious engineering on mixed hosting.
