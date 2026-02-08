# Design Decisions - Project Chimera

## Overview

This document captures key architectural decisions, trade-offs considered, and lessons learned during the infrastructure design phase.

---

## Decision 1: Hierarchical Swarm over Sequential Chain

### The Problem
We needed a pattern to coordinate multiple AI agents working on content creation at scale.

### Options Considered

| Pattern | Pros | Cons | Decision |
|---------|------|------|----------|
| **Sequential Chain** | Simple, predictable flow | No parallelism, slow throughput | ❌ Rejected |
| **Flat Swarm** | Massively parallel | No coordination, quality chaos | ❌ Rejected |
| **Hierarchical Swarm** | Parallel + quality control | More complex | ✅ **Chosen** |

### Rationale
- Social media demands **speed** (trends are time-sensitive)
- Content quality requires **review** (brand safety critical)
- Hierarchical Swarm provides both via Planner/Worker/Judge separation

### Trade-offs
- **Accepted:** Increased architectural complexity (3 agent types vs 1)
- **Gained:** 10x parallelism in content generation + built-in quality gate

---

## Decision 2: PostgreSQL + Weaviate + Redis (Hybrid Database)

### The Problem
Different data types have different access patterns and consistency requirements.

### Options Considered

**Option A: Pure PostgreSQL**
- ✅ ACID compliance, strong consistency
- ❌ No semantic search for agent memories
- ❌ Slow for high-velocity task queues

**Option B: Pure MongoDB**
- ✅ Flexible schema, fast writes
- ❌ No ACID for financial tracking
- ❌ No vector similarity search

**Option C: Hybrid (Chosen)**
- ✅ Right tool for each job
- ❌ More operational complexity (3 databases)

### Rationale by Data Type

| Data | Database | Why |
|------|----------|-----|
| Campaigns, users | PostgreSQL | Need ACID, relational queries |
| Agent memories | Weaviate | Semantic search ("find similar memories") |
| Task queue | Redis | High velocity, ephemeral, TTL support |

### What We'd Do Differently
If starting over, we might evaluate **PostgreSQL with pgvector extension** for memories instead of Weaviate, to reduce operational complexity. However, Weaviate's specialized features (schema versioning, multi-tenancy) justify the choice for production scale.

---

## Decision 3: MCP Protocol over Direct API Integration

### The Problem
Agents need to interact with 5+ external services (Twitter, Weaviate, News APIs, etc.). Each has a different SDK.

### Options Considered

**Option A: Direct API calls in agent code**
```python
# In worker agent code
import tweepy
twitter_client = tweepy.Client(api_key=os.env["TWITTER_KEY"])
twitter_client.create_tweet(text="...")
```
- ❌ Tight coupling to external SDKs
- ❌ Agent code breaks when APIs change
- ❌ Hard to mock/test

**Option B: Abstraction layer (custom)**
```python
# In worker agent code
from integrations import TwitterClient
twitter = TwitterClient()
twitter.post("...")
```
- ✅ Decoupled from SDKs
- ❌ We have to maintain the abstraction
- ❌ Not standardized (other agents can't use it)

**Option C: MCP Protocol (Chosen)**
```python
# In worker agent code
mcp_client.call_tool("twitter", "post_tweet", {"text": "..."})
```
- ✅ Standardized protocol (industry adoption)
- ✅ Agent code immune to API changes (server updates)
- ✅ Reusable servers across projects
- ❌ Requires MCP server setup

### Rationale
MCP is the "USB-C for AI applications" - a universal plug standard. Short-term cost (server setup) is outweighed by long-term maintainability.

---

## Decision 4: Confidence-Based HITL over Full Human Review

### The Problem
Human reviewers can't check every post (too slow), but we can't auto-publish everything (too risky).

### Options Considered

| Approach | Review Rate | Risk Level | Decision |
|----------|-------------|------------|----------|
| **No human review** | 0% | High | ❌ Too risky |
| **Full human review** | 100% | Low | ❌ Too slow |
| **Confidence-based** | ~15% | Medium | ✅ **Chosen** |

### The Math
```
Assume Judge confidence is normally distributed:
- 70% of content scores > 0.85  → Auto-approved
- 15% scores 0.5-0.85           → Human review
- 15% scores < 0.5              → Auto-rejected

Human reviews 15% of content but catches 99% of risky posts.
```

### Tunable Thresholds
The 0.85/0.5 thresholds are **configurable**. For risk-averse brands:
- Raise threshold to 0.95 → more human review (30%)

For high-velocity brands:
- Lower threshold to 0.75 → less human review (5%)

---

## Decision 5: Pydantic for Data Validation

### The Problem
AI agents can hallucinate malformed data. Human developers make typos.

### Why Pydantic?

```python
# Without Pydantic
def fetch_trends(platform):
    result = api.get_trends()
    # What shape is result? Who knows!
    return result

# With Pydantic
def fetch_trends(platform: str) -> TrendResult:
    result = api.get_trends()
    return TrendResult(**result)  # ✅ Validated at runtime
```

**Benefits:**
1. **Runtime validation** - catches bad data immediately
2. **Self-documenting** - models ARE the documentation
3. **IDE autocomplete** - developers get hints
4. **FastAPI integration** - automatic API validation

### Trade-off
Slight performance cost (~5-10% slower than raw dicts). Acceptable for correctness.

---

## Decision 6: TDD (Tests Before Code)

### Why Write Failing Tests First?

Traditional: Code → Test → Deploy
- Tests just confirm what was already built
- No forcing function for good design

TDD: Test → Code → Deploy
- Tests define "done" before coding starts
- Forces you to think about interfaces first
- Tests are specifications, not afterthoughts

### The Proof
Our 21 failing tests are **contracts**. When an AI agent (or developer) implements the code and all tests pass, we KNOW it satisfies the spec.

---

## Decision 7: Spec-Driven Development

### The Core Insight
AI agents hallucinate when given vague instructions. Humans forget requirements. Solution: **Write it down, precisely.**

```
Vague:   "Make the agent fetch trends"
Precise: "specs/functional.md FR-A01: Fetch top 10 trends from Twitter,
          filtered by agent niche, return TrendResult matching
          specs/technical.md Section 1.1"
```

### The Traceability Chain
Every line of code traces back to a spec. Every spec traces back to a business need. Nothing exists without reason.

---

## Lessons Learned

### What Worked Well
1. **Reading first, coding later** - The 3+ hours of research paid off
2. **Mermaid diagrams in specs** - Visual clarity prevents misunderstanding
3. **Checkbox acceptance criteria** - Makes "done" unambiguous

### What We'd Do Differently
1. **Earlier MCP experimentation** - We spec'd MCP but didn't run a server yet
2. **More concrete examples** - Each spec could include a curl/code example
3. **Integration tests** - We have unit tests, but no end-to-end test scenarios

### Open Questions
1. **Cost management** - How do we enforce budget limits in production?
2. **Agent memory limits** - When does Weaviate memory get pruned?
3. **Multi-language** - How do we handle non-English content?

---

## Future Iterations

### Phase 2 (Implementation)
- Implement the 21 failing tests
- Deploy to staging environment
- First live agent test

### Phase 3 (Scale)
- Multi-agent coordination
- Cross-platform campaigns
- Real-time analytics dashboard

### Phase 4 (Ecosystem)
- OpenClaw network integration
- Agent skill marketplace
- Community-contributed skills

---

**Last Updated:** February 6, 2026
**Author:** Zerubabel J.
**Status:** Infrastructure phase complete, ready for implementation
