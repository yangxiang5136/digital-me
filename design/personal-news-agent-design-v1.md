# Personal News Agent — Design Document v1.0

**Author**: Sean Yang  
**Date**: March 6, 2026  
**Status**: Design complete, ready for implementation  
**System**: Digital Me Project  
**Issue**: #8 on project board

---

## 1. Vision & Role

### What the News Agent Is

The News Agent is the first outward-facing component of the Digital Me system.
While the Memory Agent listens inward (captures thoughts) and the Connection
Mapper finds structure within (reveals patterns across thoughts), the News Agent
faces outward — it is the system's eyes on the world.

Its job: **"Of everything that happened in the world, what should Sean spend
his limited attention on?"**

### Role in the System

The News Agent is the bridge between Sean's inner cognitive state and the
external world. It regulates the boundary between internal and external
information — deciding what crosses the membrane.

```
                    ┌── direction.yaml ──┐
                    │   (aspirational)    │
                    ▼                     │
World ──► News Agent ──► Sean ──► Memory Agent
              ▲                       │
              │                       ▼
              └── scored-index ◄── Connection Mapper
                  (current state)
```

The loop is the retroflexion principle in action: news items that trigger
thoughts become memories, which update the scored index, which shifts what
the News Agent surfaces tomorrow.

### What the News Agent Is NOT

- It is NOT the Connection Mapper. The Connection Mapper finds connections
  between memories (introspection). The News Agent finds connections between
  news and memories (triage). They are separate agents with a dependency
  relationship: the News Agent reads the Connection Mapper's output.
- It is NOT an engagement optimizer. Unlike TikTok, which optimizes for
  time-on-platform, this system optimizes for cognitive value — information
  that changes thinking or enables action.

---

## 2. Architecture

### Three Swappable Layers

The system has three distinct layers with different lifecycles:

```
LAYER 1: NEWS SOURCES (swappable, disposable)
  Fork repos, deploy, write thin adapters
  
LAYER 2: PERSONAL ENGINE (permanent, yours)
  Profile builder, scorer, attention optimizer, reaction processor
  
LAYER 3: USER INTERFACES (swappable, adoptable)
  Fork repos, connect to scored feed
```

```
Sources (fork & deploy)        YOUR ENGINE (permanent)       UIs (fork & deploy)
                                      │
World Monitor ──► adapter ──►  ┌──────┴──────┐    ──► Dashboard (investigation)
RSS feeds    ──► adapter ──►   │ Scored Feed │    ──► Curated page (daily briefing)
Future repo  ──► adapter ──►   │  (JSON)     │    ──► Future UI repo
                               └─────────────┘
```

### Contracts

Two interface boundaries define the system:

#### News Source Contract (what adapters produce)

```yaml
item:
  id: string              # unique identifier
  title: string           # headline
  summary: string         # 1-3 sentences (REQUIRED)
  url: string             # link to full article
  published_at: datetime  # when published
  source_name: string     # "Reuters", "Hacker News", etc.

  source_scoring:         # OPTIONAL — not all sources score
    severity: string | null
    category: string | null
    confidence: float | null
    tags: [string] | null

  geo:                    # OPTIONAL
    country: string | null
    region: string | null
    lat: float | null
    lon: float | null

  meta:
    source_system: string
    adapter_version: string
    fetched_at: datetime
```

Key design choices:
- `summary` is REQUIRED. If the source doesn't provide one, the adapter must
  generate it. The scorer needs text to evaluate.
- `source_scoring` is OPTIONAL. Rich sources (World Monitor) provide it;
  simple sources (RSS) don't. The personal scorer works either way.
- Format is flat and simple. No source-specific fields leak through.

#### User Profile Contract (what the engine reads)

```yaml
current_interests:
  topics: [string]
  keywords: [string]
  regions: [string]
  summary: string         # natural language, ~200 words

growth_directions:
  topics: [string]
  keywords: [string]
  summary: string

attention_budget:
  daily_items: int
  max_scan_time_seconds: int
  delivery_channels: [string]

scoring:
  current_weight: float
  growth_weight: float
  min_growth_items: int
```

### Agent Contract Compliance

```
Reads:
  ├── connections/scores-*.json  (from Connection Mapper)
  ├── direction.yaml             (from Sean, manually maintained)
  ├── rubric.yaml                (from Sean, manually maintained)
  └── News source APIs           (from adapters)

Writes to own folder:
  ├── scored-feed.json           (for UIs to consume)
  ├── profile.json               (built from scored memories)
  ├── reactions/YYYY-MM-DD.yaml  (user interaction log)
  └── news-digests/YYYY-MM-DD.md (archival markdown)

Trigger: scheduled cron (daily) + on-demand via UI
Config: own environment variables, own deployment
```

---

## 3. Theoretical Foundations

### Foundation 1: Attention Economics

Attention is a finite, non-renewable daily resource. Every piece of information
has an opportunity cost. The agent maximizes:

```
Attention ROI = Cognitive value gained / Attention time invested
```

"Value" is multi-dimensional:
- **Actionable value** — enables action in the next 7 days
- **Contextual value** — updates mental models without requiring action
- **Serendipitous value** — expands the map into unknown territory
- **Social value** — improves effectiveness in interactions with others

### Foundation 2: The Filtering Paradox

Exploitation (show what matches past preferences) vs. Exploration (show what
might expand horizons). Resolved through:

- `direction.yaml` growing_toward fields = explicit exploration targets
- Aspiration Gap = direction.yaml topics minus topics in recent memories
- When gap is large, increase exploration weight automatically

### Foundation 3: Information Foraging Theory (Pirolli & Card)

- **Information scent** — cues that signal whether an item is worth reading.
  The rationale line and digest tag serve as scent trails.
- **Patch switching cost** — cognitive effort to move between topics.
  Digest is clustered by topic to minimize switching.
- **Diminishing returns** — cap items per topic cluster (max 2-3).

### Foundation 4: Cognitive Load (Sweller)

- **Intrinsic load** — managed by not stacking complex items consecutively
- **Extraneous load** — minimized through clean UI and strong information scent
- **Germane load** — maximized by showing connections to existing knowledge

### Foundation 5: Push vs. Pull Temporal Modes

| Mode | When | Duration | Cognitive State |
|---|---|---|---|
| Morning briefing (push) | Once, fixed time | 2 minutes | Fresh, scanning |
| Ambient check (passive) | Sporadic | 10 seconds | Distracted, glancing |
| Investigation (pull) | Triggered by interest | Open-ended | Focused, exploring |

Each mode needs different density, thresholds, and content.

### Foundation 6: Information-to-Action Bridge

The agent delivers information AND helps act on it. Each item can carry:
- **Rationale** — "why you're seeing this" (scent)
- **Connection** — "relates to memory #X" (context)
- **Affordance** — "what you could do with this" (action)

---

## 4. Connection Mapping

### Three Types of Connections

When a news item touches Sean's memory space, it connects in one of three ways:

**Reinforcement** — confirms or extends existing thinking.
Frequency: high. Cognitive value: low-medium. Risk: confirmation bias.

**Challenge** — contradicts or complicates existing thinking.
Frequency: medium. Cognitive value: high. Forces deeper thinking.

**Bridge** — connects two memory clusters that weren't previously linked.
Frequency: rare. Cognitive value: highest. Creates new insight paths.

| Connection Type | Frequency | Immediate Value | Long-term Value | Cognitive Cost |
|---|---|---|---|---|
| Reinforcement | High | Low-medium | Low | Low |
| Challenge | Medium | Medium-high | High | High |
| Bridge | Rare | Variable | Highest | Medium |

The agent weights challenge and bridge connections higher than reinforcement.

### Detection Mechanism

**Pass 1: Surface matching (cheap, programmatic)**
Keyword and entity overlap between news item text and memory text.
Pre-filters candidates for expensive LLM analysis.

**Pass 2: Deep connection analysis (Claude)**
For candidate connections, Claude analyzes:
1. Is there a meaningful connection? (yes/no)
2. What type? (reinforcement / challenge / bridge)
3. If bridge: which OTHER memories does this also connect to?
4. One sentence: how does this change or enrich Sean's thinking?
5. Suggested action: what could Sean do with this connection?

### Connection Graph

Over time, bridge connections add new edges between previously unlinked
memory clusters. This is the mechanism by which external information
becomes integrated into the cognitive graph.

---

## 5. Multi-Dimensional Scoring

### Five Scoring Dimensions

Every news item is scored on five dimensions (0-10 each):

#### Dimension 1: Project Relevance (actionable)

"Can Sean do something with this in the next 7 days?"

- Score 0: No connection to any active project
- Score 5: Directly relevant to a project being built
- Score 7: Answers a question currently stuck on
- Score 10: Changes a decision about to be made

Driven by: high-scoring recent memories on the Projects aspect.

#### Dimension 2: Mental Model Update (contextual)

"Does this change how Sean understands something he's tracking?"

- Score 0: Tells you something already known
- Score 5: Meaningful shift in a domain you care about
- Score 7: Contradicts or complicates current understanding
- Score 10: Fundamentally reframes thinking about something

Driven by: Principles and Ideas aspect memories. Challenge items score
HIGHER than reinforcement items.

#### Dimension 3: Serendipity (bridge potential)

"Does this connect two things Sean hasn't linked yet?"

- Score 0: Connects to nothing or only one cluster
- Score 5: Touches two already-linked memory clusters
- Score 7: Connects two previously unlinked clusters
- Score 10: Connects three or more previously unlinked clusters

Driven by: connection mapping bridge detection algorithm.
Main defense against filter bubbles.

#### Dimension 4: Social Currency (relational)

"Would knowing this make Sean more effective with other people?"

- Score 0: No connection to any relationship
- Score 5: Relevant to a specific person interacted with regularly
- Score 7: Directly useful for an upcoming conversation
- Score 10: Would significantly change the outcome of an interaction

Driven by: Relationships aspect memories. Weakest signal in v1;
improves as Memory Agent captures more relational context.

#### Dimension 5: Time Sensitivity (urgency)

"Will this item lose value if seen tomorrow instead of today?"

- Score 0: Evergreen — valuable whenever read
- Score 5: Relevant today, less so tomorrow
- Score 7: Should be seen today — affects near-term decisions
- Score 10: See this NOW — high-impact, rapidly evolving

Driven by: publication recency, urgency keywords, connection to
active projects with known timelines.
Acts as tiebreaker, not primary driver.

### Composite Output Per Item

Dimensions do NOT collapse into a weighted average. They produce a profile:

```json
{
  "title": "...",
  "scoring": {
    "project_relevance": 8,
    "mental_model_update": 6,
    "serendipity": 7,
    "social_currency": 2,
    "time_sensitivity": 3,
    "primary_value": "project_relevance",
    "secondary_value": "serendipity",
    "digest_tag": "bridges your agent design + HF research",
    "rationale": "...",
    "connections": [
      {
        "memory_id": "memory_14",
        "type": "bridge",
        "bridge_to": "memory_27",
        "enrichment": "...",
        "suggested_action": "..."
      }
    ]
  }
}
```

### Selection Algorithm

```
All scored items (~50-100)
    │
    ▼
Filter: remove items where ALL dimensions ≤ 2
    │
    ▼
Selection rules (in order):
    │
    ├── 1. Must include: top item by serendipity score
    │      (anti-filter-bubble guarantee)
    │
    ├── 2. Must include: any item with time_sensitivity ≥ 7
    │      (don't miss urgent things)
    │
    ├── 3. Must include: at least 1 "mental_model_update" item
    │      (ensures thinking, not just building)
    │
    ├── 4. Fill remaining by max(project_relevance, serendipity)
    │
    ├── 5. Cap: max 2 items per topic cluster
    │      (diminishing returns)
    │
    └── 6. Cap: total ≤ attention_budget.daily_items (10)
    
    ▼
Final digest (7-10 items, grouped by primary_value)
```

### Claude Scoring Prompt

Single batch call. 20-30 items scored at once:

```
System: You are scoring news items for personal relevance.

Here is Sean's cognitive context:

CURRENT PROJECTS AND THINKING (from scored-index.json):
{top 10 recent memories with scores and memos}

GROWTH DIRECTION (from direction.yaml):
{growing_toward, growing_away_from, blind_spot_watch}

RUBRIC ASPECTS: Projects, Principles, Ideas, Relationships, Learning, Growth

---

For each news item below, score on 5 dimensions (0-10):
1. Project Relevance — can he act on this within 7 days?
2. Mental Model Update — does this change how he understands something?
3. Serendipity — does this bridge two of his thought clusters?
4. Social Currency — would knowing this help in interactions?
5. Time Sensitivity — does value decay if seen tomorrow?

Also provide:
- primary_value: which dimension scored highest
- digest_tag: 5-8 word label for scanning
- rationale: one sentence on why this matters to him
- connections: which memory IDs this relates to (if any)
- connection_type: reinforcement / challenge / bridge

NEWS ITEMS:
{batch of 20-30 items with title + summary}
```

---

## 6. Dual-Loop Feedback System

### Why Two Loops

TikTok's insight: implicit signals are more honest than explicit ones, and
real-time feedback dramatically outperforms batch processing. But TikTok
optimizes for engagement; this system optimizes for cognitive value.

Two parallel loops serve different learning timescales:

### Fast Loop (seconds to hours)

User reacts to items in the UI. Reactions update the agent's model
immediately within the current session.

#### Reaction Types

| Reaction | Signal | Weight |
|---|---|---|
| Skip (no action) | Not worth attention | -1 |
| Dismiss ("not this") | Actively irrelevant | -3 |
| Read (clicked/opened) | Worth investigating | +2 |
| Like (👍) | Valuable, noted | +3 |
| Save (🔖) | Worth returning to later | +5 |
| Share (↗️) | Valuable enough to send to someone | +6 |
| Connect (🔗) | "This relates to memory #X" | +7 |
| React (💭) | Triggers a new thought → Memory Agent | +10 |

"Connect" and "React" are unique to this system:
- **Connect**: explicitly links a news item to a memory — tells the system
  "I see the bridge"
- **React**: generates a new memory via Memory Agent — the ultimate proof
  that external information changed internal thinking

#### Fast Loop Data Model

```json
{
  "topic_affinities": {
    "AI agents": 0.85,
    "geopolitics": 0.30,
    "design thinking": 0.55
  },
  "source_trust": {
    "arXiv": 0.9,
    "TechCrunch": 0.4
  },
  "reaction_history": [
    {"item_id": "...", "reaction": "connect", "memory_linked": "memory_14", "timestamp": "..."},
    {"item_id": "...", "reaction": "skip", "timestamp": "..."}
  ]
}
```

Reactions update `topic_affinities` and `source_trust` in real-time.
Next scoring batch uses updated affinities as a boost signal alongside
Claude-based scoring.

#### Score Adjustment Formula

```
Adjusted Score = 
    Claude assessment (0-10)
    × topic_affinity_boost (0.5 to 1.5)
    × source_trust_multiplier (0.5 to 1.2)
```

Over time, pre-filtering handles more decisions and Claude only scores
ambiguous or novel items.

### Slow Loop (days to weeks)

When a news item triggers a "React" — Sean captures a thought in the
Memory Agent — the slow loop activates:

```
Day 1: News item → React → Memory Agent captures thought
Day 2: Connection Mapper scores new memory → Updates scored-index.json
Day 3: News Agent profile builder reads updated index → 
       Profile now reflects the new interest organically
```

The slow loop doesn't need explicit design — it emerges from existing
infrastructure. The Memory Agent and Connection Mapper are already running.
Reactions are the on-ramp to this loop.

### Reaction Storage

Append-only file per day, following agent contract (writes to own folder):

```yaml
# reactions/2026-03-07.yaml
date: "2026-03-07"
items_presented: 45
items_reacted: 12
reactions:
  - item_id: "wm-4521"
    title: "New framework for evaluating AI agent autonomy"
    reaction: "connect"
    memory_linked: "memory_14"
    timestamp: "2026-03-07T08:15:00Z"
    dimensions_at_scoring:
      project_relevance: 8
      serendipity: 7
    
  - item_id: "rss-9983"
    title: "TechCrunch: Another AI startup raises $50M"
    reaction: "skip"
    timestamp: "2026-03-07T08:15:04Z"
    dwell_time_seconds: 1.2

  - item_id: "wm-4530"
    title: "Japanese concept of Ma in design"
    reaction: "react"
    memory_generated: "memory_52"
    timestamp: "2026-03-07T08:16:30Z"
    dwell_time_seconds: 45
```

---

## 7. User Interface Design

### Two Cognitive Modes

The UI serves two distinct cognitive states:

**Curated Daily Page** — "morning briefing" mode.
Push-based, 2 minutes, pre-selected items, read-once.
Items grouped by primary_value dimension:

```
━━━ YOUR DAILY BRIEFING — March 7, 2026 ━━━

FOR YOUR WORK (project-relevant)
  ▸ New agent evaluation framework maps autonomy levels
    bridges your agent design + HF research | Score: 8
    [👍] [🔖] [↗️] [🔗] [💭] [✕]

SHIFTS YOUR THINKING (mental model updates)
  ▸ Study: users prefer AI that explains uncertainty
    challenges your digest design assumptions | Score: 6
    [👍] [🔖] [↗️] [🔗] [💭] [✕]

UNEXPECTED CONNECTIONS (serendipitous)
  ▸ Japanese concept of "Ma" — negative space in design
    connects design curiosity + attention budget | Score: 7
    [👍] [🔖] [↗️] [🔗] [💭] [✕]

4 items · ~40 sec scan · full feed: [dashboard link]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Dense Dashboard** — "investigation" mode.
Pull-based, open-ended, full feed with filters and layers.
Used when something from the briefing triggers deeper exploration.

Both UIs are swappable — adopted from external repos, connected to the
scored feed. The engine doesn't know or care which UI is consuming its output.

### UI as Input Layer

The UI is not just a display layer — it's an input layer. Every reaction
is data that feeds both loops. This means UI selection criteria include:
- Does it support low-friction reaction buttons?
- Can it track implicit signals (dwell time, scroll behavior)?
- Does it integrate with Memory Agent for the "React" action?

---

## 8. System Architecture — Complete

```
┌─────────────────────────────────────────────────────┐
│                    NEWS SOURCES                       │
│              (adapters, swappable)                    │
└────────────────────┬────────────────────────────────┘
                     │ raw items (News Source Contract)
                     ▼
┌─────────────────────────────────────────────────────┐
│              PRE-FILTER                              │
│  Uses: topic_affinities + source_trust (fast loop)   │
│  Removes: obvious skips based on reaction history    │
│  Passes: ~30 candidate items                         │
└────────────────────┬────────────────────────────────┘
                     │ candidates
                     ▼
┌─────────────────────────────────────────────────────┐
│        CONNECTION DETECTION (Pass 1)                 │
│  Surface matching: keywords, entities, rubric overlap │
│  Identifies candidate connections to memories         │
└────────────────────┬────────────────────────────────┘
                     │ candidates with connection hints
                     ▼
┌─────────────────────────────────────────────────────┐
│           CLAUDE SCORING (5 dimensions)              │
│  Uses: scored-index + direction.yaml (slow loop)     │
│  + topic_affinities (fast loop boost)                │
│  + connection hints from Pass 1                      │
│  Performs: deep connection analysis (Pass 2)          │
│  Output: multi-dimensional scores + connections      │
└────────────────────┬────────────────────────────────┘
                     │ scored items
                     ▼
┌─────────────────────────────────────────────────────┐
│           SELECTION (attention budget)                │
│  Must-include rules + caps + ranking                 │
│  Output: scored-feed.json (7-10 items for briefing,  │
│          full feed for dashboard)                    │
└────────────────────┬────────────────────────────────┘
                     │ scored feed
                     ▼
┌─────────────────────────────────────────────────────┐
│           UI (curated page / dashboard)              │
│  Displays: items with scent tags + reaction buttons  │
│  [Skip] [👍] [🔖] [↗️] [🔗 Connect] [💭 React] [✕] │
└────────────────────┬────────────────────────────────┘
                     │ reactions
                     ▼
┌─────────────────────────────────────────────────────┐
│           REACTION PROCESSOR                         │
│                                                      │
│  Fast path: update topic_affinities + source_trust   │
│             → affects next pre-filter + scoring boost │
│                                                      │
│  Slow path: "React" → Memory Agent → new memory →   │
│             Connection Mapper → scored-index update   │
│             → affects next profile build              │
│                                                      │
│  Archive: append to reactions/YYYY-MM-DD.yaml        │
└─────────────────────────────────────────────────────┘
```

---

## 9. Implementation Plan

### Dependencies

- Memory Agent v1: RUNNING (Railway)
- Connection Mapper v2.1: RUNNING (local)
- World Monitor: DEPLOYED (Vercel) — first news source
- direction.yaml: current (last reviewed March 6, 2026)
- scored-index.json: available in connections/ folder

### Phase 1: Profile Builder + News Scorer

Build the engine core:
1. Profile builder reads scored-index.json + direction.yaml
2. RSS adapter (5 feeds, simplest possible source)
3. Claude scoring with 5 dimensions
4. Selection algorithm with attention budget
5. Output: scored-feed.json + digest markdown
6. Deploy on Railway as cron

### Phase 2: World Monitor Adapter + Reactions

Add rich source + feedback:
1. World Monitor adapter (reads from deployed WM API)
2. Reaction UI (buttons on curated page)
3. Reaction processor (fast loop affinities)
4. Reaction storage (daily YAML files)

### Phase 3: Dashboard Integration

Investigation mode:
1. Create new repo from World Monitor fork
2. Add "For You" panel reading scored-feed.json
3. Reaction buttons in dashboard view
4. Connect "React" button to Memory Agent

### Phase 4: Commercialization

Generalize for other users:
1. Define User Profile Contract (simple YAML on-ramp)
2. Publish connector as GitHub template repo
3. 5-minute onboarding: edit profile.yaml → deploy → get digest
4. Progressive complexity: static YAML → full Digital Me stack

---

## 10. Key Decisions Log

| Decision | Choice | Rationale |
|---|---|---|
| Personalization approach | Client-side middleware | Modular, matches agent contract |
| World Monitor role | Replaces news fetching | 150+ feeds > 15-30 curated RSS |
| Scoring model | WM scores + identity overlay | Preserves WM intelligence, adds meaning |
| News Agent vs Connection Mapper | Separate agents | Different concerns, different code |
| Scoring dimensions | 5 independent (no weighted avg) | Preserves signal about value type |
| Feedback model | Dual-loop (fast + slow) | Real-time reactions + deep cognitive integration |
| Highest-value reaction | React (→ Memory Agent) | Only signal where info becomes part of thinking |
| UI approach | Two modes (briefing + dashboard) | Different cognitive states need different interfaces |
| UI sourcing | Fork external repos | UIs are swappable, not custom-built |
| Source architecture | Adapter pattern, swappable | News sources are commodities |
| Scored feed location | TBD (likely Upstash Redis) | Already part of WM infrastructure |
| Phase 3 on-ramp | Static YAML profile | 5-minute start, advanced users add Memory Agent |

---

## 11. Open Questions for Implementation

1. **Scored feed storage**: Static file (GitHub), Upstash Redis, or hybrid?
2. **Curated page UI**: Which repo to fork/adopt?
3. **React → Memory Agent integration**: Same Telegram bot or API call?
4. **Dwell time tracking**: Feasible in the chosen UI framework?
5. **Connection detection accuracy**: How much pre-filtering before Claude?
6. **Cost management**: Claude API calls per day at scale?
7. **direction.yaml review cadence**: Monthly? When friction is detected?

---

## Appendix A: System State Reference

```
Digital Me Project
├── 🤖 Memory Agent v1 ✅ RUNNING (Railway)
├── 📊 Connection Mapper v2.1 ✅ RUNNING (local)
├── 🌐 World Monitor ✅ DEPLOYED (Vercel)
├── 📰 News Agent ◄── THIS DOCUMENT
├── 📁 Repos:
│   ├── yangxiang5136/digital-me (system HQ)
│   ├── yangxiang5136/my-memories (memory files)
│   └── yangxiang5136/worldmonitor (deployed fork)
├── 📁 Config: ~/memory-agent/
│   ├── rubric.yaml
│   ├── direction.yaml
│   └── attention-budget.yaml
└── 📁 Project board: github.com/users/yangxiang5136/projects/1
```

## Appendix B: direction.yaml (current, Feb 18 2026)

```yaml
growing_toward:
  - "Thinking deeper before building — going from interesting idea to
     clear enough understanding that I know what to build and why"
  - "Making things that other people actually use, not just prototypes
     that prove a concept to myself"
  - "Exploring design, aesthetics, and creativity — learning to think
     in ways that aren't purely engineering-driven"

growing_away_from:
  - "Generating many ideas but staying shallow on all of them —
     I want fewer ideas taken further"
  - "Jumping to implementation before I've really understood
     the problem at the level that matters"

blind_spot_watch:
  - "Am I going deep on one idea this week, or scattering again?"
  - "Have I spent time on something non-technical recently?"
  - "Am I building for myself or for someone who'd actually use this?"
  - "What would a designer think about what I'm making?"
```
