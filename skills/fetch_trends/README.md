# Skill: fetch_trends

## Spec Reference
- **Functional:** FR-A01 (Trend Research)
- **Contract:** TrendResult (specs/technical.md Section 1.1)

## Purpose
Fetches current trending topics from configured platforms,
filters them by agent niche, and scores them by engagement.

## Input
```json
{
  "agent_id": "string (UUID)",
  "platform": "string (twitter|news|youtube)",
  "niche": "string (from agent's SOUL.md)",
  "count": "integer (default: 10)",
  "max_age_hours": "integer (default: 8)"
}
```

## Output
```json
{
  "topics": [
    {
      "name": "string",
      "category": "string",
      "engagement_score": "float (0.0-1.0)",
      "source_url": "string",
      "source_platform": "string",
      "fetched_at": "datetime"
    }
  ],
  "agent_id": "string",
  "fetch_timestamp": "datetime",
  "platform": "string",
  "topic_count": "integer"
}
```

## MCP Servers Used
- `mcp-server-twitter` — for Twitter trend data
- `mcp-server-news` — for news-based trend detection

## Logic
1. Query platform MCP server for raw trending data
2. Filter by agent niche (semantic matching via Weaviate)
3. Score by engagement metrics
4. Discard stale data (older than max_age_hours)
5. Return top N results as TrendResult
