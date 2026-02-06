# Project Chimera - Functional Specification

## User Stories

Stories are grouped by actor. Each story has an ID for traceability
(tests and code reference these IDs).

---

## Actor: Chimera Agent (The Autonomous Influencer)

### FR-A01: Trend Research
**As a** Chimera Agent,
**I want to** fetch current trending topics from configured platforms,
**so that** I can create timely, relevant content.

**Acceptance Criteria:**
- Fetch top 10 trending topics from at least one platform (Twitter)
- Each topic includes: name, category, engagement_score, source_url
- Results are filtered by the agent's niche (defined in SOUL.md)
- Fetch interval is configurable (default: 4 hours)
- Stale data (older than 8 hours) is automatically discarded

---

### FR-A02: Content Generation
**As a** Chimera Agent,
**I want to** generate platform-appropriate content based on trending topics,
**so that** my posts are engaging and relevant to my audience.

**Acceptance Criteria:**
- Generated content matches the agent's voice/tone (from SOUL.md)
- Content respects platform character limits (Twitter: 280 chars)
- Each content piece includes: text, suggested_hashtags, confidence_score
- Content referencing sensitive topics is flagged automatically
- Agent retrieves relevant memories from Weaviate before generating

---

### FR-A03: Memory Recall
**As a** Chimera Agent,
**I want to** retrieve semantically relevant past memories before creating content,
**so that** I maintain personality consistency and don't repeat myself.

**Acceptance Criteria:**
- Query Weaviate with the current topic context
- Return top 5 most relevant past memories
- Each memory includes: content, timestamp, relevance_score
- Memories older than 90 days have reduced relevance weighting
- If no relevant memories exist, proceed without (cold start)

---

### FR-A04: Memory Storage
**As a** Chimera Agent,
**I want to** store my interactions and generated content as memories,
**so that** I build a persistent identity over time.

**Acceptance Criteria:**
- Every published post is stored as a memory in Weaviate
- Memories include: content, platform, engagement_metrics, timestamp
- High-engagement posts are tagged as "core_memory" (never pruned)
- Storage operation must not block the content pipeline

---

## Actor: Judge Agent (The Quality Gate)

### FR-J01: Content Review
**As a** Judge Agent,
**I want to** evaluate worker-generated content against quality and safety criteria,
**so that** only appropriate content gets published.

**Acceptance Criteria:**
- Assign a confidence_score (0.0 to 1.0) to every content piece
- Check against: persona consistency, platform TOS, sensitivity filters
- Decision outcomes: APPROVE (score > 0.85), REVIEW (0.5-0.85), REJECT (< 0.5)
- Sensitive topic detection for: politics, religion, health claims, financial advice
- All decisions are logged with reasoning for audit trail

---

### FR-J02: HITL Escalation
**As a** Judge Agent,
**I want to** escalate uncertain content to a human reviewer,
**so that** risky content never gets auto-published.

**Acceptance Criteria:**
- Content scoring 0.5-0.85 enters the human review queue
- Sensitive topics ALWAYS enter review (regardless of score)
- Financial transactions ALWAYS require human approval
- Escalation includes: the content, the score, and the reason
- Review queue has a maximum age of 24 hours (auto-reject if unreviewed)

---

## Actor: Planner Agent (The Strategist)

### FR-P01: Task Decomposition
**As a** Planner Agent,
**I want to** break down campaign goals into executable tasks,
**so that** workers can execute in parallel without conflicts.

**Acceptance Criteria:**
- Accept a high-level goal (e.g., "Create 5 tweets about Ethiopian fashion")
- Decompose into atomic tasks with dependencies
- Each task includes: task_id, type, input_data, dependencies, priority
- Tasks with no dependencies can be dispatched in parallel
- Re-plan when a worker task fails (create alternative path)

---

## Actor: Network Operator (Human)

### FR-H01: Campaign Management
**As a** Network Operator,
**I want to** define campaign goals and constraints for my agents,
**so that** agents work toward my business objectives.

**Acceptance Criteria:**
- Create a campaign with: name, goal_description, platforms, budget, duration
- Assign one or more agents to a campaign
- Set content frequency limits (e.g., max 10 posts/day)
- Pause/resume campaigns without losing agent state

---

### FR-H02: Content Review Queue
**As a** Human Reviewer,
**I want to** review escalated content and approve, edit, or reject it,
**so that** I maintain brand safety without reviewing everything.

**Acceptance Criteria:**
- View pending content with Judge's confidence score and reasoning
- Actions: Approve (publish as-is), Edit (modify then publish), Reject (discard)
- Batch operations for efficiency (approve multiple safe items)
- Review decisions feed back into Judge's learning (improves future scoring)
