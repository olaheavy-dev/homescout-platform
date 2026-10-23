# 0020: Application languages

**ID:** BE-01 (accepted), FE-01 (in part)  
**Status:** Accepted  
**Date:** 2026-10-23  
**Stage:** 2 (brought forward from stage 6 for BE-01 and stage 4 for FE-01)

## Context
While deciding where calculations live (DA-02), the founder confirmed the application languages. BE-01 was scheduled for stage 6 and FE-01 for stage 4; confirming them now lets the cost engine start in the right language.

## Options
- **C# backend; TypeScript with Next.js frontend (chosen):** matches the original brief and the Azure direction; two languages, which suits the learning goals.
- **TypeScript everywhere:** one language and simpler for agents, but drops the planned .NET learning and the brief's stack.

## Recommendation
Keep the brief's stack.

## Decision
Founder's words: "we will use C# for backend and typescript and next js for frontend."

## Consequences
- **BE-01 accepted:** C# on .NET. ASP.NET Core remains the planned web framework, used when the API is built (stage 6), together with BE-02.
- **FE-01 accepted in part:** TypeScript with Next.js (React). The routing model and static versus server rendering are still decided in stage 4.
- Doc 04's stage 6 table no longer re-confirms the backend language.
