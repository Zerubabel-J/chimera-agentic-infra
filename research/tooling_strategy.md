# Tooling Strategy - Developer Tools vs. Agent Skills

## Two Categories of Tools

This project distinguishes between tools that help DEVELOPERS build the system
and tools that the AGENTS use at runtime.

---

## Category 1: Developer Tools (MCP Servers for Development)

These MCP servers assist the human developer during the build phase.
They are NOT used by Chimera agents at runtime.

| MCP Server | Purpose | Why We Need It |
|------------|---------|----------------|
| `filesystem-mcp` | Read/write project files | Lets AI assistant navigate codebase |
| `git-mcp` | Version control operations | Commit, branch, diff from AI context |
| `tenx-mcp-sense` | Telemetry and traceability | Records AI decision-making (required) |

### How They Connect

```
Developer's IDE (VSCode/Cursor)
       │
       ├── Claude Code / Cursor AI
       │      │
       │      ├── filesystem-mcp  → reads specs/, writes code
       │      ├── git-mcp         → commits, checks diffs
       │      └── tenx-mcp-sense  → logs all AI decisions
       │
       └── Developer reviews AI output
```

---

## Category 2: Agent Runtime Tools (MCP Servers for Chimera)

These MCP servers are used by the Chimera agents during operation.
They bridge the agent to the external world.

| MCP Server | Purpose | Used By | Priority |
|------------|---------|---------|----------|
| `mcp-server-twitter` | Read mentions, post tweets | Worker agents | P0 |
| `mcp-server-weaviate` | Store/retrieve memories | All agents | P0 |
| `mcp-server-news` | Fetch news for trend detection | Worker agents | P1 |
| `mcp-server-youtube` | Fetch video trends | Worker agents | P1 |
| `mcp-server-coinbase` | Financial transactions | Worker agents (future) | P2 |

### How They Connect

```
Chimera Agent Runtime
       │
       ├── Planner Agent
       │      └── (no direct MCP usage - works with internal state)
       │
       ├── Worker Agents
       │      ├── mcp-server-twitter   → fetch trends, post content
       │      ├── mcp-server-weaviate  → recall memories
       │      ├── mcp-server-news      → research current events
       │      └── mcp-server-youtube   → monitor video trends
       │
       └── Judge Agent
              └── mcp-server-weaviate  → check persona consistency
```

---

## The Relationship: Skills USE MCP Servers

```
skill_fetch_trends (the logic)
       │
       ├── USES mcp-server-twitter  → to get raw trend data
       ├── USES mcp-server-news     → to get news data
       │
       └── PRODUCES TrendResult     → filtered, scored, formatted
```

The skill contains the INTELLIGENCE (filtering, scoring, ranking).
The MCP server is just the PIPE (raw data in, raw data out).
