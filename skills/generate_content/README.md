# Skill: generate_content

## Spec Reference
- **Functional:** FR-A02 (Content Generation)
- **Contract:** GeneratedContent (specs/technical.md Section 1.2)

## Purpose
Generates platform-appropriate social media content based on a
trending topic, using the agent's persona voice and relevant memories.

## Input
```json
{
  "agent_id": "string (UUID)",
  "trend_topic": "TrendTopic object",
  "platform": "string (twitter|instagram|linkedin)",
  "persona": "AgentPersona object (from SOUL.md)",
  "relevant_memories": ["AgentMemory objects (from Weaviate)"]
}
```

## Output
```json
{
  "content_id": "string (UUID)",
  "agent_id": "string",
  "text": "string (respects platform char limit)",
  "platform": "string",
  "suggested_hashtags": ["string"],
  "confidence_score": "float (0.0-1.0)",
  "source_trend": "string",
  "persona_voice": "string",
  "sensitive_topics_detected": ["string"],
  "created_at": "datetime"
}
```

## MCP Servers Used
- `mcp-server-weaviate` — retrieves relevant memories before generation

## Logic
1. Load agent persona from SOUL.md
2. Retrieve top 5 relevant memories from Weaviate (FR-A03)
3. Construct LLM prompt with: persona + memories + trend topic
4. Generate content respecting platform constraints
5. Scan for sensitive topics
6. Assign self-assessed confidence_score
7. Return as GeneratedContent
