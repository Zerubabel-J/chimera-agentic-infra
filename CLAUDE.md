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
