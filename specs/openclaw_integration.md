# Project Chimera - OpenClaw Integration Specification

## Overview

This spec defines how Chimera agents interact with the emerging
Agent Social Network ecosystem (OpenClaw / MoltBook).

**Status:** Future scope. Not part of MVP. Included for architectural planning.

---

## 1. Agent Discovery Protocol

### Problem
Other agents on the OpenClaw network need to know what Chimera agents
can do and when they're available.

### Solution: Status Broadcasting
Chimera agents publish a status object to the network:

```json
{
  "AgentStatus": {
    "agent_id": "string (UUID)",
    "agent_name": "string",
    "capabilities": ["string (skill names: trend_research, content_generation)"],
    "niche": "string (e.g., 'Ethiopian Fashion')",
    "availability": "string (enum: active|busy|offline)",
    "last_active": "string (ISO 8601)",
    "reputation_score": "float (0.0 - 1.0)"
  }
}
```

## 2. Skill Sharing Protocol

### Problem
Agents on the network may have skills that Chimera agents lack (and vice versa).

### Solution
Expose skill interfaces as MCP-compatible tool definitions:

```json
{
  "SkillListing": {
    "skill_name": "string",
    "description": "string",
    "input_schema": "object (JSON Schema)",
    "output_schema": "object (JSON Schema)",
    "cost_per_call": "float (in tokens or crypto)",
    "avg_latency_ms": "integer"
  }
}
```

## 3. Collaboration Request Protocol

### Problem
An external agent wants to request content creation from a Chimera agent.

### Solution
```json
{
  "CollaborationRequest": {
    "request_id": "string (UUID)",
    "requester_id": "string (external agent ID)",
    "requested_skill": "string",
    "input_data": "object",
    "offered_payment": "float",
    "deadline": "string (ISO 8601)",
    "status": "string (enum: pending|accepted|rejected|completed)"
  }
}
```

**Governance:** All collaboration requests route through the Judge agent.
Requests from agents with reputation_score < 0.5 are auto-rejected.
