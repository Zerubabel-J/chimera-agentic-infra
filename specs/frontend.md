# Project Chimera - Frontend Specification

## Overview

The frontend provides a Human-in-the-Loop (HITL) review interface for network operators
to manage campaigns and review escalated content before publication.

**Tech Stack:** React + TypeScript, Tailwind CSS, React Query for data fetching

---

## User Flows

### Flow 1: Review Queue - Human Reviewer

```
1. Reviewer logs in
2. Dashboard shows pending content count (badge notification)
3. Reviewer clicks "Review Queue"
4. List of escalated content items appears, sorted by urgency
5. Reviewer clicks an item
6. Detail view shows:
   - The generated content
   - Judge's confidence score and reasoning
   - Platform and agent persona
   - Suggested hashtags
7. Reviewer takes action:
   - APPROVE → content goes to publish queue
   - EDIT → inline editor opens, saves, then publishes
   - REJECT → content is discarded, logged for learning
```

### Flow 2: Campaign Management - Network Operator

```
1. Operator navigates to "Campaigns"
2. Sees list of active campaigns with metrics
3. Clicks "New Campaign"
4. Form appears:
   - Campaign name
   - Goal description (free text)
   - Platforms (checkboxes: Twitter, Instagram, LinkedIn)
   - Assigned agents (multi-select dropdown)
   - Budget (max cost in USD)
   - Duration (start date, end date)
5. Clicks "Create"
6. Campaign starts, agents begin working
7. Operator can pause/resume/stop from campaign detail page
```

---

## Components

### ContentReviewCard

**Props:**
```typescript
interface ContentReviewCardProps {
  contentId: string;
  text: string;
  platform: "twitter" | "instagram" | "linkedin";
  hashtags: string[];
  confidenceScore: number;
  reasoning: string;
  flags: string[];
  agentName: string;
  onApprove: (contentId: string) => void;
  onEdit: (contentId: string, newText: string) => void;
  onReject: (contentId: string) => void;
}
```

**Layout:**
```
┌─────────────────────────────────────────────┐
│ [Agent Icon] chimera-eth-fashion-01         │
│ Platform: Twitter  |  Score: 0.78           │
├─────────────────────────────────────────────┤
│                                             │
│  "Check out this Habesha Kemis trend! 🔥"  │
│  #EthiopianFashion #HabeshaKemis #Style    │
│                                             │
├─────────────────────────────────────────────┤
│ Reasoning: Moderate confidence due to       │
│ use of emoji and informal tone              │
│                                             │
│ Flags: [informal_tone]                      │
├─────────────────────────────────────────────┤
│ [Approve] [Edit] [Reject]                   │
└─────────────────────────────────────────────┘
```

---

### CampaignForm

**Props:**
```typescript
interface CampaignFormProps {
  onSubmit: (campaign: CreateCampaignInput) => void;
  agents: Agent[];
  onCancel: () => void;
}

interface CreateCampaignInput {
  name: string;
  goal: string;
  platforms: Platform[];
  agentIds: string[];
  budgetUsd: number;
  startDate: Date;
  endDate: Date;
  maxPostsPerDay: number;
}
```

---

### DashboardMetrics

Real-time metrics displayed at the top of the dashboard:

```
┌──────────────────────────────────────────────────────────┐
│  Active Campaigns: 3    Agents Online: 7                │
│  Pending Review: 12     Published Today: 45              │
│  Budget Used: $127 / $500                                │
└──────────────────────────────────────────────────────────┘
```

---

## API Endpoints (Frontend → Backend)

### GET /api/review-queue
**Response:**
```json
{
  "items": [
    {
      "content_id": "uuid",
      "text": "string",
      "platform": "twitter",
      "hashtags": ["string"],
      "confidence_score": 0.78,
      "reasoning": "string",
      "flags": ["string"],
      "agent_id": "string",
      "agent_name": "string",
      "created_at": "ISO8601"
    }
  ],
  "total_count": 12
}
```

### POST /api/review-queue/:id/approve
**Body:** `{}`
**Response:** `{ "status": "approved", "published_at": "ISO8601" }`

### POST /api/review-queue/:id/edit
**Body:** `{ "text": "Updated content..." }`
**Response:** `{ "status": "edited", "published_at": "ISO8601" }`

### POST /api/review-queue/:id/reject
**Body:** `{ "reason": "Off-brand tone" }`
**Response:** `{ "status": "rejected" }`

### GET /api/campaigns
**Response:**
```json
{
  "campaigns": [
    {
      "id": "uuid",
      "name": "Ethiopian Fashion Q1",
      "status": "active",
      "agents_count": 3,
      "posts_today": 12,
      "budget_used": 127.50,
      "budget_total": 500.00
    }
  ]
}
```

### POST /api/campaigns
**Body:** `CreateCampaignInput` (see above)
**Response:** `{ "campaign": Campaign }`

---

## Wireframes

### Review Queue Page

```
┌────────────────────────────────────────────────────────────┐
│  [Logo] Chimera Dashboard        [Profile] zerubabel       │
├────────────────────────────────────────────────────────────┤
│  Campaigns | Review Queue (12) | Agents | Analytics       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Pending Review (12)                    [Batch Approve]   │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ ContentReviewCard 1                                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ ContentReviewCard 2                                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ ContentReviewCard 3                                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Authentication

- JWT-based authentication
- Roles: `network_operator`, `reviewer`, `admin`
- `reviewer` can only access review queue
- `network_operator` can manage campaigns and review
- `admin` has full access

---

## State Management

Use React Query for server state:

```typescript
// Fetch review queue
const { data: reviewQueue } = useQuery({
  queryKey: ["review-queue"],
  queryFn: fetchReviewQueue,
  refetchInterval: 10000, // Poll every 10 seconds
});

// Approve content
const approveMutation = useMutation({
  mutationFn: (contentId: string) => approveContent(contentId),
  onSuccess: () => {
    queryClient.invalidateQueries(["review-queue"]);
  },
});
```

---

## Accessibility

- All interactive elements must be keyboard-navigable
- ARIA labels on all buttons and form inputs
- Color contrast ratio >= 4.5:1 for text
- Screen reader support for status updates ("Content approved")

---

## Future Enhancements

- Real-time WebSocket updates for new review items
- Bulk operations (approve multiple items at once)
- Analytics dashboard with charts
- Agent performance leaderboard
