# CLAUDE.md - Project Chimera AI Context Rules

## Project Context

This is **Project Chimera**, an Autonomous Influencer Network.
The system uses AI agents (Planner/Worker/Judge swarm pattern) to
research trends, generate social media content, and manage engagement
with human-in-the-loop safety oversight.

Repository: chimera-agentic-infra
Stack: Python 3.11+, Pydantic, Weaviate, Redis, PostgreSQL, MCP

## Prime Directive

**NEVER generate implementation code without checking `specs/` first.**

Before writing ANY code:
1. Read the relevant spec in `specs/` to understand the contract
2. Check `specs/technical.md` for the exact data shapes (Pydantic models)
3. Check `specs/functional.md` for acceptance criteria
4. Ensure your code satisfies the acceptance criteria, not more, not less

## Traceability

**Always explain your plan before writing code.**

When implementing a feature:
1. State which spec ID you are implementing (e.g., "Implementing FR-A01")
2. Explain your approach in 2-3 sentences
3. Reference the API contract from `specs/technical.md`
4. Only then write the code

## Architecture Rules

- Follow the Hierarchical Swarm pattern: Planner → Worker → Judge
- All external integrations go through MCP servers, never direct API calls
- Use Pydantic models for ALL data validation (defined in specs/technical.md)
- Skills are modular packages in `skills/` - each skill does ONE thing

## Code Style

- Use `ruff` for linting (config in pyproject.toml)
- Async by default for I/O operations
- Type hints on all function signatures
- Tests go in `tests/` and must reference a spec ID in their docstring

## Directory Structure

```
specs/          → Source of truth. Read these FIRST.
skills/         → Agent capability packages (modular, one skill = one job)
tests/          → TDD tests that validate spec compliance
research/       → Architecture decisions and research notes
.github/        → CI/CD workflows
```

## What NOT To Do

- Do NOT write code that contradicts a spec - update the spec first
- Do NOT skip the Judge review step in any content pipeline
- Do NOT hardcode API keys - use environment variables
- Do NOT create monolithic files - keep modules focused and small
- Do NOT auto-publish content without Judge evaluation

## Agent Behavior Guidelines

### Decision-Making Framework

When implementing agent logic, follow this decision tree:

1. **Is there a spec for this?**
   - YES → Follow the spec exactly
   - NO → Ask for clarification or create a spec proposal

2. **Does this involve external data?**
   - YES → Use an MCP server, never direct API calls
   - NO → Proceed with internal logic

3. **Does this create content for publishing?**
   - YES → Must go through Judge agent review
   - NO → Can proceed directly

### Error Handling

```python
# Good: Specific errors with context
try:
    result = fetch_trends(agent_id, platform, niche)
except MCPConnectionError as e:
    logger.error(f"MCP server unreachable: {e}")
    # Escalate to human operator
except ValidationError as e:
    logger.error(f"Invalid data shape from {platform}: {e}")
    # Retry with fallback

# Bad: Silent failures or generic catches
try:
    result = fetch_trends(agent_id, platform, niche)
except Exception:
    pass  # ❌ Never do this
```

### When to Escalate to Human

Automatically escalate when:
- Confidence score < 0.85 on any decision
- Sensitive topic detected (politics, health, religion, finance)
- API rate limit exceeded
- Data validation fails repeatedly
- MCP server is unreachable for > 5 minutes

### Example Agent Prompts

**For Planner Agent:**
```
You are the Planner. Your job is to decompose campaign goals into atomic tasks.

Goal: "Create 5 tweets about Ethiopian fashion trends"

Your output:
1. fetch_trends(agent_id, "twitter", "Ethiopian fashion") → Worker1
2. For each trend → generate_content(agent_id, trend, "twitter") → Worker2-6
3. For each content → evaluate_content(content) → Judge
4. For approved → publish(content) → Worker7-11

Dependencies: Task 2 depends on Task 1. Tasks 3-4 depend on Task 2.
```

**For Worker Agent:**
```
You are a Worker. You execute exactly ONE task and return a result.

Task: generate_content
Input: agent_id="chimera-001", trend="Habesha Kemis Revival", platform="twitter"

Steps:
1. Load agent persona from SOUL.md
2. Query Weaviate for relevant memories
3. Generate content using LLM
4. Return GeneratedContent object (specs/technical.md Section 1.2)
```

**For Judge Agent:**
```
You are the Judge. You review worker output for quality and safety.

Input: GeneratedContent(text="Check out this Habesha Kemis trend! 🔥")

Checks:
1. Matches persona voice? ✓
2. Within 280 chars? ✓
3. Sensitive topics? ✗ (none detected)
4. Confidence: 0.92

Decision: APPROVE (confidence > 0.85, no flags)
```

## Logging and Observability

Every agent action must log:
- Timestamp
- Agent ID and role (Planner/Worker/Judge)
- Task/Decision ID
- Input/Output summary
- Confidence score (for Judge decisions)
- Execution time

```python
logger.info(
    "Agent action",
    extra={
        "agent_id": agent_id,
        "role": "worker",
        "task_id": task_id,
        "skill": "fetch_trends",
        "platform": platform,
        "result_count": len(result.topics),
        "duration_ms": execution_time,
    }
)
```
