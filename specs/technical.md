# Project Chimera - Technical Specification

## 1. API Contracts

All data flowing through the system must conform to these contracts.
Tests in `tests/` validate against these exact shapes.

---

### 1.1 Trend Data Contract

**Used by:** FR-A01 (Trend Research)
**Producer:** `skill_fetch_trends`
**Consumer:** Planner Agent

```json
{
  "TrendResult": {
    "topics": [
      {
        "name": "string",
        "category": "string (enum: fashion|tech|politics|entertainment|sports|business|other)",
        "engagement_score": "float (0.0 - 1.0)",
        "source_url": "string (valid URL)",
        "source_platform": "string (enum: twitter|news|youtube)",
        "fetched_at": "string (ISO 8601 datetime)"
      }
    ],
    "agent_id": "string (UUID)",
    "fetch_timestamp": "string (ISO 8601 datetime)",
    "platform": "string",
    "topic_count": "integer"
  }
}
```

**Example:**
```json
{
  "topics": [
    {
      "name": "Habesha Fashion Week 2026",
      "category": "fashion",
      "engagement_score": 0.92,
      "source_url": "https://twitter.com/trending/ethiopia-fashion",
      "source_platform": "twitter",
      "fetched_at": "2026-02-06T10:00:00Z"
    }
  ],
  "agent_id": "chimera-eth-fashion-01",
  "fetch_timestamp": "2026-02-06T10:00:00Z",
  "platform": "twitter",
  "topic_count": 1
}
```

---

### 1.2 Generated Content Contract

**Used by:** FR-A02 (Content Generation)
**Producer:** Worker Agent
**Consumer:** Judge Agent

```json
{
  "GeneratedContent": {
    "content_id": "string (UUID)",
    "agent_id": "string (UUID)",
    "text": "string (max length varies by platform)",
    "platform": "string (enum: twitter|instagram|linkedin)",
    "suggested_hashtags": ["string"],
    "confidence_score": "float (0.0 - 1.0)",
    "source_trend": "string (trend name that inspired this)",
    "persona_voice": "string (voice trait used)",
    "sensitive_topics_detected": ["string"],
    "created_at": "string (ISO 8601 datetime)"
  }
}
```

**Platform Constraints:**
| Platform | Max Text Length | Hashtag Limit |
|----------|----------------|---------------|
| Twitter | 280 chars | 5 |
| Instagram | 2200 chars | 30 |
| LinkedIn | 3000 chars | 10 |

---

### 1.3 Judge Decision Contract

**Used by:** FR-J01 (Content Review)
**Producer:** Judge Agent
**Consumer:** Orchestrator (routes to publish or human review)

```json
{
  "JudgeDecision": {
    "decision_id": "string (UUID)",
    "content_id": "string (UUID, references GeneratedContent)",
    "verdict": "string (enum: APPROVE|REVIEW|REJECT)",
    "confidence_score": "float (0.0 - 1.0)",
    "reasoning": "string (explanation of the decision)",
    "flags": ["string (e.g., 'sensitive_topic', 'off_brand', 'too_long')"],
    "reviewed_at": "string (ISO 8601 datetime)"
  }
}
```

**Decision Logic:**
```
confidence_score > 0.85           → verdict: APPROVE
0.50 <= confidence_score <= 0.85  → verdict: REVIEW
confidence_score < 0.50           → verdict: REJECT
sensitive_topics_detected != []   → verdict: REVIEW (override)
```

---

### 1.4 Memory Contract

**Used by:** FR-A03 (Memory Recall), FR-A04 (Memory Storage)
**Storage:** Weaviate vector database

```json
{
  "AgentMemory": {
    "memory_id": "string (UUID)",
    "agent_id": "string (UUID)",
    "content": "string (the memory text)",
    "memory_type": "string (enum: post|interaction|observation|core_memory)",
    "platform": "string (where this happened)",
    "engagement_metrics": {
      "likes": "integer",
      "shares": "integer",
      "comments": "integer"
    },
    "relevance_score": "float (0.0 - 1.0, computed at query time)",
    "created_at": "string (ISO 8601 datetime)",
    "tags": ["string"]
  }
}
```

---

### 1.5 Task Contract

**Used by:** FR-P01 (Task Decomposition)
**Producer:** Planner Agent
**Consumer:** Worker Agents

```json
{
  "PlannerTask": {
    "task_id": "string (UUID)",
    "campaign_id": "string (UUID)",
    "task_type": "string (enum: fetch_trends|generate_content|review_content|store_memory)",
    "input_data": "object (varies by task_type)",
    "dependencies": ["string (task_ids that must complete first)"],
    "priority": "integer (1=highest, 5=lowest)",
    "status": "string (enum: pending|in_progress|completed|failed)",
    "assigned_worker": "string (worker_id, null if unassigned)",
    "created_at": "string (ISO 8601 datetime)"
  }
}
```

---

## 2. Database Schema

### 2.1 PostgreSQL (Transactional Data)

```
┌─────────────────────┐       ┌─────────────────────┐
│     campaigns       │       │      agents         │
├─────────────────────┤       ├─────────────────────┤
│ id          UUID PK │──┐    │ id          UUID PK │
│ name        VARCHAR │  │    │ name        VARCHAR │
│ goal        TEXT    │  │    │ persona_file TEXT   │
│ platforms   JSONB   │  │    │ niche       VARCHAR │
│ budget      DECIMAL │  │    │ status      VARCHAR │
│ max_posts   INTEGER │  │    │ created_at  TIMESTAMP│
│ status      VARCHAR │  │    └─────────────────────┘
│ start_date  TIMESTAMP│  │              │
│ end_date    TIMESTAMP│  │              │
│ created_at  TIMESTAMP│  │              │
└─────────────────────┘  │              │
                         │              │
              ┌──────────┴──────────────┴──┐
              │   campaign_agents (join)    │
              ├────────────────────────────┤
              │ campaign_id  UUID FK       │
              │ agent_id     UUID FK       │
              │ assigned_at  TIMESTAMP     │
              └────────────────────────────┘

┌─────────────────────────┐
│   content_log           │
├─────────────────────────┤
│ id            UUID PK   │
│ agent_id      UUID FK   │
│ campaign_id   UUID FK   │
│ platform      VARCHAR   │
│ text          TEXT       │
│ hashtags      JSONB     │
│ status        VARCHAR   │  (draft|approved|published|rejected)
│ judge_verdict VARCHAR   │
│ confidence    DECIMAL   │
│ published_at  TIMESTAMP │
│ created_at    TIMESTAMP │
└─────────────────────────┘

┌─────────────────────────┐
│   review_queue          │
├─────────────────────────┤
│ id            UUID PK   │
│ content_id    UUID FK   │
│ reason        TEXT       │
│ confidence    DECIMAL   │
│ flags         JSONB     │
│ reviewer_id   UUID FK   │  (null until claimed)
│ decision      VARCHAR   │  (pending|approved|edited|rejected)
│ decided_at    TIMESTAMP │
│ expires_at    TIMESTAMP │  (auto-reject after 24h)
│ created_at    TIMESTAMP │
└─────────────────────────┘
```

### 2.2 Weaviate (Vector Database)

**Collection: AgentMemories**
- Properties: agent_id, content, memory_type, platform, tags, created_at
- Vectorizer: text2vec-openai (or text2vec-cohere)
- Vector index: HNSW (default, optimized for recall)

**Collection: AgentPersonas**
- Properties: agent_id, backstory, voice_traits, directives, niche
- Used for: Semantic matching of persona to content tone

### 2.3 Redis (Cache / Queue)

| Key Pattern | Purpose | TTL |
|-------------|---------|-----|
| `session:{agent_id}` | Short-term conversation memory | 1 hour |
| `queue:tasks:{priority}` | Task queue for workers | Until consumed |
| `rate_limit:{agent_id}:{platform}` | API rate limit tracking | Platform-specific |
| `trending:{platform}` | Cached trend data | 4 hours |

---

## 3. Pydantic Models (Python Implementation Reference)

These models enforce the contracts at runtime.

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TopicCategory(str, Enum):
    FASHION = "fashion"
    TECH = "tech"
    POLITICS = "politics"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    BUSINESS = "business"
    OTHER = "other"

class Platform(str, Enum):
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"

class Verdict(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    REJECT = "REJECT"

class TrendTopic(BaseModel):
    name: str
    category: TopicCategory
    engagement_score: float = Field(ge=0.0, le=1.0)
    source_url: str
    source_platform: str
    fetched_at: datetime

class TrendResult(BaseModel):
    topics: list[TrendTopic]
    agent_id: str
    fetch_timestamp: datetime
    platform: str
    topic_count: int

class GeneratedContent(BaseModel):
    content_id: str
    agent_id: str
    text: str
    platform: Platform
    suggested_hashtags: list[str] = Field(max_length=30)
    confidence_score: float = Field(ge=0.0, le=1.0)
    source_trend: str
    persona_voice: str
    sensitive_topics_detected: list[str] = []
    created_at: datetime

class JudgeDecision(BaseModel):
    decision_id: str
    content_id: str
    verdict: Verdict
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    flags: list[str] = []
    reviewed_at: datetime
```
