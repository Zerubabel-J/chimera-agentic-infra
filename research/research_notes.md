# Research Notes - Project Chimera

## 1. The Trillion Dollar AI Code Stack (a16z)

### Key Insights

**The New Development Workflow: Plan → Code → Review**
- AI is transforming software development from "writing code" to "orchestrating AI agents"
- Background agents can now submit PRs autonomously, running for extended periods
- Simple tasks (text changes, library updates, simple features) work completely autonomously

**Critical Infrastructure Emerging:**
| Category | Why It Matters |
|----------|---------------|
| Code Search | Agents can't process entire codebases - need semantic search (Sourcegraph) |
| Execution Sandboxes | Safe isolated environments for agent code execution (E2B, Daytona) |
| Intent-Based Version Control | Track decisions, not just text diffs (Gitbutler) |
| Agent-Optimized Docs | Documentation must be machine-readable |

**Relevance to Chimera:**
- Our specs must be "agent-optimized" - precise, unambiguous, machine-parseable
- We need sandboxed execution for agent-generated content
- The Planner/Worker/Judge pattern aligns with Plan/Code/Review workflow

---

## 2. OpenClaw & The Agent Social Network (TechCrunch)

### Key Insights

**What is OpenClaw?**
- A viral personal AI assistant (formerly Clawdbot/Moltbot)
- Now building infrastructure for agent-to-agent social networking
- Represents shift from "AI serving humans" to "AI networks serving AI"

**Implications for Chimera:**
- Our agents may need to interact with OTHER agents, not just humans
- Agent Social Networks are emerging - Chimera should be compatible
- Need to design for "Social Protocols" beyond human social media APIs

---

## 3. MoltBook: Social Media for Bots (TheConversation)

### Key Insights

**What is MoltBook?**
- A social network WHERE BOTS ARE THE USERS
- Bots post, comment, share every few hours autonomously
- Has "submolts" (like subreddits) - topic-linked forums
- Discussions include: automation techniques, security, philosophy

**The "Skills" Framework:**
- OpenClaw agents use modular "skills" packages
- Skills = instructions + scripts for repeated task execution
- Range from file management to complex multi-tool operations (trading, dating apps)

**Critical Insight - Not Revolutionary, But Important:**
> "The agents are doing what many humans already use LLMs for: collating reports, generating social media posts, responding to content, mimicking social networking behaviours."

**Relevance to Chimera:**
- Our Skills architecture directly mirrors OpenClaw's approach
- Chimera agents are essentially doing what humans do on social media - but 24/7
- The "submolt" concept = niche communities our agents should target
- Agent-to-agent communication is a real protocol we should support

---

## 4. Project Chimera SRS - Key Takeaways

### The Architecture
- **FastRender Swarm**: Planner → Worker → Judge hierarchy
- **MCP (Model Context Protocol)**: Universal interface for external interactions
- **Fractal Orchestration**: Single human manages AI managers who manage worker swarms

### The Three Roles
| Role | Responsibility |
|------|---------------|
| **Planner** | Decomposes goals into task DAGs, dynamic re-planning |
| **Worker** | Executes single atomic tasks, stateless, parallel |
| **Judge** | Quality assurance, approve/reject/escalate to human |

### Critical Protocols
- **Optimistic Concurrency Control (OCC)**: Non-locking state management
- **HITL (Human-in-the-Loop)**: Human reviews based on confidence scores
- **Resources/Tools/Prompts**: MCP's three primitives

---

## Summary: How Chimera Fits the Ecosystem

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT ECOSYSTEM                       │
├─────────────────────────────────────────────────────────┤
│  OpenClaw Network ←→ Project Chimera ←→ Human Platforms │
│       (Bots)              (Our Agent)      (Twitter/IG) │
└─────────────────────────────────────────────────────────┘
```

**Chimera's Position:**
1. Consumes trends from human social media (Twitter, TikTok, News)
2. Generates content autonomously using Planner/Worker/Judge
3. Publishes to human platforms AND potentially to agent networks (MoltBook)
4. Uses Skills framework compatible with OpenClaw ecosystem
