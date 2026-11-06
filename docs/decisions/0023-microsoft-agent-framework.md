# 0023: Microsoft Agent Framework for the AI layer

**ID:** AI-04  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 6 (decided early)

## Context
The founder asked whether HomeScout needs agent orchestration, and whether to use Microsoft Agent Framework. The framework reached version 1.0 in April 2026 ([announcement](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)) as the successor to Semantic Kernel and AutoGen. It supports single agents with tools and graph-based workflows, and connects to Microsoft Foundry, OpenAI, Anthropic, Ollama and other providers ([overview](https://learn.microsoft.com/en-us/agent-framework/overview/)). Microsoft's guidance: use an agent for open-ended tasks, a workflow for well-defined steps, and "if you can write a function to handle the task, do that instead of using an AI agent."

## Options
- **Plan it, confirm at stage 6 with a trial:** keeps the option open.
- **Decide it now (chosen):** a fixed direction for the AI layer and for learning.
- **Leave open until stage 6.**

## Recommendation
Plan it now and confirm at stage 6 with a trial.

## Decision
Founder's choice: decide it now. Microsoft Agent Framework is HomeScout's AI framework, used like this:

| Part of HomeScout | Approach |
|---|---|
| Costs, comparisons, and **working out** what changed (cost differences, which evidence or assumptions changed and by how much) | Plain code: the cost engine and change-detection code. Never AI |
| Explain a finding, draft a question, check a reply, and **put a change into words** using the differences the code worked out | A single agent call with tools; it may only quote figures and changes the code supplied |
| Optional chat panel (decision 0004) | A single agent with a session |
| Document investigation: read several documents, find conflicts, draft questions, then the user approves | A workflow with fixed steps and a human approval step |

## Consequences
- HomeScout's own task interfaces stay framework-neutral, so the rest of the code doesn't depend on the framework directly. Framework agents and workflows implement them.
- The model provider is still chosen at stage 6 under the cost-first rule (decision 0022): the cheapest provider the framework supports that passes the evaluation suite (AI-01).
- No framework packages are added before stage 6. When they are, they're pinned and listed in `docs/references/third-party.md`.
- The evaluation, citation and number guards in the foundations review apply to every agent and workflow.

## Update, 6 November 2026: reaffirmed
The founder confirmed that HomeScout will definitely use Microsoft Agent Framework: "we would definitely be using maf for this project." This is a reaffirmation, not a change; the table above and the consequences still stand.

- **Python:** with the backend in Python (decision [0036](0036-python-backend.md)), the framework is used through its Python package. Check the official documentation for the pinned version via `docs/references/third-party.md` when it is added at stage 6.
- **Not LangChain:** HomeScout does not use the LangChain, LangGraph or LangSmith model gateway that comes with the founder's FastAPI template ([0040](0040-fastapi-template-as-api-starting-point.md)). The AI layer is built on Microsoft Agent Framework. The template's idea of a per-day model-spend cap (reserve a call's worst-case cost, settle the real cost, one record per call) is kept for IN-05 and 0022, rebuilt on this framework.
- **Task interfaces stay framework-neutral** (see Consequences). That is also what lets the template later offer Microsoft Agent Framework as a second model gateway beside LangChain.
- **Template follow-up:** once HomeScout has built its framework-based gateway at stage 6, the framework-neutral parts (budget logic, price table, call records) and a Microsoft Agent Framework gateway are lifted into the founder's template, so a project can choose `none`, `langchain` or `maf`. HomeScout builds it first; the template follows (decision 0040).
