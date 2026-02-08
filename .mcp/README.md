# MCP Server Configuration

This directory contains Model Context Protocol (MCP) server configurations for Project Chimera.

## Server Categories

### Development Servers (for building)
- **filesystem** - File operations during development
- **git** - Version control integration

### Runtime Servers (for agents)
- **weaviate** - Vector database for agent memory
- **twitter** - Social media API integration
- **news** - News and trend data fetching

## Setup

### 1. Install MCP CLI
```bash
npm install -g @modelcontextprotocol/cli
```

### 2. Configure Environment Variables
Create `.env` in project root:
```bash
WEAVIATE_API_KEY=your_key_here
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_SECRET=your_secret_here
NEWS_API_KEY=your_key_here
```

### 3. Connect to IDE

#### For Claude Desktop / Cursor
Add to your IDE's MCP settings:
```json
{
  "mcpServers": {
    "chimera": {
      "command": "mcp",
      "args": ["--config", "/path/to/chimera-agentic-infra/.mcp/servers.json"]
    }
  }
}
```

#### For VSCode with Claude Code
The `.mcp/servers.json` file is auto-detected when Claude Code runs in this directory.

## Verification

Test MCP connection:
```bash
mcp list-servers --config .mcp/servers.json
```

## Server Details

| Server | Protocol | Purpose |
|--------|----------|---------|
| weaviate | stdio | Agent memory storage and semantic search |
| filesystem | stdio | File read/write for development |
| git | stdio | Version control operations |
| twitter | stdio | Fetch trends, post content |
| news | stdio | News aggregation for trend detection |
