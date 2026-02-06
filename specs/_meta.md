# Project Chimera - Meta Specification

## Vision

Project Chimera is an **Autonomous Influencer Network** - a system of AI agents
that research trends, generate content, and manage social media engagement
with minimal human intervention.

## Problem Statement

Most AI social media tools are fragile prompt-chains that break at scale.
They hallucinate, produce off-brand content, and require constant human
babysitting. This defeats the purpose of automation.

## Solution

A **Spec-Driven, Swarm-Based architecture** where:

1. **Specifications** (this directory) define all behavior precisely
2. **Hierarchical Swarm** (Planner/Worker/Judge) ensures quality at scale
3. **Human-in-the-Loop** provides safety without bottlenecking operations
4. **MCP Protocol** standardizes all external tool integration

## Constraints

- **Ethical:** Agents must self-disclose as AI when required by platform TOS
- **Financial:** All transactions require human approval; budget governor enforced
- **Content Safety:** Sensitive topics (politics, health, religion) always route to human review
- **Cost:** Model tiering required - use cheap models for routine, expensive for complex
- **Compliance:** Must comply with EU AI Act transparency requirements

## Architecture Pattern

**Hierarchical Swarm (FastRender Pattern)**

```
Human Operator (sets goals, reviews escalations)
       │
   Planner (decomposes goals into task DAG)
       │
  ┌────┼────┐
  W1   W2   W3  (parallel workers, stateless, one task each)
  └────┼────┘
       │
     Judge (approve / reject / escalate)
```

## Scope Boundaries

### In Scope (MVP)
- Trend research from Twitter and news sources
- Text content generation (tweets, captions)
- Quality review pipeline (Judge + HITL)
- Agent persona management (SOUL.md)
- Semantic memory (Weaviate)

### Out of Scope (Future)
- Video generation
- Agentic commerce (Coinbase AgentKit)
- Multi-language support
- OpenClaw network publishing

## Source of Truth

- All behavior is defined in `specs/`
- All implementations must reference a spec
- No code should be written without a corresponding spec entry
