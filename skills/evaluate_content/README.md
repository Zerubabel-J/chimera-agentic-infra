# Skill: evaluate_content

## Spec Reference
- **Functional:** FR-J01 (Content Review), FR-J02 (HITL Escalation)
- **Contract:** JudgeDecision (specs/technical.md Section 1.3)

## Purpose
Evaluates worker-generated content against quality, safety, and persona
consistency criteria. Returns a verdict: APPROVE, REVIEW, or REJECT.

## Input
```json
{
  "content": "GeneratedContent object",
  "persona": "AgentPersona object (from SOUL.md)",
  "safety_rules": {
    "sensitive_topics": ["politics", "religion", "health", "financial_advice"],
    "auto_approve_threshold": 0.85,
    "auto_reject_threshold": 0.50
  }
}
```

## Output
```json
{
  "decision_id": "string (UUID)",
  "content_id": "string (UUID)",
  "verdict": "string (APPROVE|REVIEW|REJECT)",
  "confidence_score": "float (0.0-1.0)",
  "reasoning": "string",
  "flags": ["string"],
  "reviewed_at": "datetime"
}
```

## MCP Servers Used
- `mcp-server-weaviate` — checks persona consistency against stored traits

## Logic
1. Check content against platform TOS constraints (char limits, banned words)
2. Scan for sensitive topics (politics, religion, health, financial advice)
3. Compare content voice against persona (SOUL.md voice_traits)
4. Assign confidence_score based on all checks
5. Apply decision logic:
   - score > 0.85 AND no sensitive topics → APPROVE
   - sensitive topics detected → REVIEW (always, regardless of score)
   - 0.50 <= score <= 0.85 → REVIEW
   - score < 0.50 → REJECT
6. Log reasoning for audit trail
7. Return as JudgeDecision
