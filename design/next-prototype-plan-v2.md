# Personal News Agent — Next Prototype Plan v2
## Global Sources + Chinese Translation + Two-Tier LLM

Updated: March 6, 2026

---

## Core Principle

**Scan the world. Read in two languages.**

- English content → stays English (you read it natively)
- Chinese content → stays Chinese (you read it natively)
- Everything else (Japanese, Korean, German, French, Arabic, etc.)
  → translated to Chinese by Layer 1 LLM during scoring

Why Chinese as the translation target instead of English?
Chinese LLMs translate *into* Chinese better than into English.
DeepSeek, MiniMax, and GLM are native Chinese models — their
Chinese output is more natural than their English output. And since
you read Chinese natively, there's zero comprehension cost.

---

## The Pipeline

```
GLOBAL SOURCES (10+ languages, 200+ feeds)
│
├── English feeds ──────────── pass through as-is
├── Chinese feeds ──────────── pass through as-is
├── Japanese feeds ─────┐
├── Korean feeds ───────┤
├── German feeds ───────┤
├── French feeds ───────┼──── Layer 1 LLM translates
├── Arabic feeds ───────┤     title + summary → Chinese
├── Spanish feeds ──────┤     during scoring step
├── Russian feeds ──────┤
├── Hindi feeds ────────┘
│
▼
ALL ITEMS now in English or Chinese
│
▼
Layer 1: DeepSeek V3.2 (bulk score + translate)
  - Scores 5 dimensions
  - Translates non-EN/CN titles and summaries → Chinese
  - One combined prompt: "Score AND translate this item"
  - Cost: ~$0.05 per 1,000 items
│
▼
Top 30-50 items
│
▼
Layer 2: Claude Haiku 4.5 (connection analysis)
  - Memory connection detection
  - Bridge/challenge/reinforcement typing
  - Quality rationale (in English — your system language)
  - Cross-language bridge detection
  - Cost: ~$0.02 per 30 items
│
▼
Selection algorithm → 10 items
│
▼
YOUR BRIEFING
  - English items shown in English
  - Chinese items shown in Chinese
  - Translated items shown in Chinese with [🇯🇵][🇰🇷][🇩🇪] etc. flag
  - Original URL always preserved for deep reading
```

---

## Translation Cost: Nearly Free

Translation happens INSIDE the Layer 1 scoring call — not as a
separate step. The prompt becomes:

```
"For each item:
 1. Score on 5 dimensions (0-10)
 2. If the item is NOT in English or Chinese, translate the
    title and summary into Chinese (简体中文)
 3. Provide digest_tag and rationale in English"
```

This adds ~50 tokens of output per translated item. At DeepSeek
rates ($0.42/M output), translating 1,000 items costs $0.02 extra.
Essentially free.

---

## Global Source Map

### TIER 1: English Sources (~100 feeds)

**AI / Technology**
- Hacker News, arXiv (cs.AI, cs.HC, cs.CL), MIT Tech Review
- TechCrunch, The Verge, Wired, Ars Technica
- OpenAI Blog, Anthropic Blog, Google AI Blog, DeepMind Blog

**Design / Creativity**
- A List Apart, Smashing Magazine, Design Observer
- Sidebar.io, UX Collective, Nielsen Norman Group

**Product / Building**
- Lenny's Newsletter, SVPG, Stratechery
- Paul Graham essays, Y Combinator blog

**Cognitive Science / HCI**
- ACM DL feeds, CHI conference, Cognitive Science Society

**World News / Geopolitics**
- Reuters, AP, The Economist, Foreign Affairs
- BBC World, NPR, The Guardian

**Open Source / Infrastructure**
- Railway Blog, Vercel Blog, GitHub Blog
- Cloudflare Blog, Fly.io Blog

**Recommendation Systems / Personalization**
- Eugene Yan, RecSys feeds, Netflix Tech Blog

### TIER 2: Chinese Sources (~80 feeds)

**AI / Technology**
- 机器之心 (Jiqizhixin) — top CN AI media
- 量子位 (QbitAI) — AI research coverage
- 36氪 (36kr) — tech startups
- 少数派 (sspai) — productivity/tools
- 极客公园 (GeekPark) — tech industry
- InfoQ CN — developer news
- 开源中国 (OSChina) — open source
- SegmentFault — developer community
- V2EX — tech forum highlights
- CSDN — developer knowledge

**Design / Creativity**
- 优设 (uisdc.com) — UI/UX design
- 站酷 (zcool.com.cn) — creative community
- 数英网 (digitaling.com) — creative industry

**Business / Depth**
- 虎嗅 (Huxiu) — business + tech analysis
- 澎湃新闻 (ThePaper) — quality journalism
- 财新 (Caixin) — finance + economics
- 端传媒 (Initium) — in-depth reporting
- FT中文网 (FT Chinese) — Financial Times Chinese
- 知乎热榜 (Zhihu) — Q&A highlights

**Product / Startup**
- 创业邦 (Cyzone) — startup ecosystem
- 品玩 (PingWest) — US-China tech bridge

### TIER 3: Japanese Sources (~30 feeds, → translated to Chinese)

**AI / Technology**
- ITmedia AI+ — AI industry news
- TechCrunch Japan — tech startups
- GIGAZINE — tech/science
- Publickey — developer infrastructure
- Qiita Trending — developer knowledge

**Design / Culture**
- Spoon & Tamago — Japanese art/design
- Dezeen Japan — architecture/design
- Japan Times — English-language (stays EN)

**Business**
- Nikkei Asia — business (stays EN)
- 日経新聞 — business (→ CN)

### TIER 4: Korean Sources (~20 feeds, → translated to Chinese)

**AI / Technology**
- AI타임스 (AI Times) — Korean AI news
- ZDNet Korea — tech industry
- 블로터 (Bloter) — tech media

**Business / Culture**
- The Korea Herald (stays EN)
- 한국경제 (Korea Economic Daily, → CN)

### TIER 5: European Sources (~30 feeds, → translated to Chinese)

**German**
- Heise Online — tech news
- t3n — digital business
- Golem.de — IT news

**French**
- Le Monde Technologie — tech
- L'Usine Digitale — digital industry

**General (English editions stay EN)**
- Der Spiegel International — stays EN
- Le Monde Diplomatique EN — stays EN
- NRC (Netherlands) — → CN

### TIER 6: Other Regions (~20 feeds, → translated to Chinese)

**Arabic**
- Al Jazeera Tech — → CN
- Wired Middle East — stays EN

**Hindi / Indian**
- The Ken — stays EN
- YourStory — stays EN
- MediaNama — stays EN

**Russian**
- Habr (Хабр) — tech community → CN

**Latin America**
- MIT Tech Review Español — → CN

---

## Language Handling Summary

| Source Language | Action | LLM Used |
|---|---|---|
| English | Keep as-is | — |
| Chinese | Keep as-is | — |
| Japanese | Translate → Chinese | DeepSeek (Layer 1) |
| Korean | Translate → Chinese | DeepSeek (Layer 1) |
| German | Translate → Chinese | DeepSeek (Layer 1) |
| French | Translate → Chinese | DeepSeek (Layer 1) |
| Arabic | Translate → Chinese | DeepSeek (Layer 1) |
| Spanish | Translate → Chinese | DeepSeek (Layer 1) |
| Russian | Translate → Chinese | DeepSeek (Layer 1) |
| Other | Translate → Chinese | DeepSeek (Layer 1) |

Note: Many non-English sources have English editions (Nikkei Asia,
Korea Herald, Spiegel International). Use EN editions when available
to avoid unnecessary translation. Only translate when native-language
edition has content the EN edition doesn't cover.

---

## What the UI Shows

```
┌──────────────────────────────────────┐
│ WORK · arXiv · 2h               1/10│
│                                      │
│ New Framework for AI Agent           │
│ Autonomy Levels                      │
│                                      │
│ Maps to your 'present, never         │
│ decide' principle                    │
│ ─────────────────────────────────────│
│        [image/chart/text]            │
│                                      │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ DISCOVERY · ITmedia AI+ · 3h 🇯🇵 3/10│
│                                      │
│ 日本のAIエージェント研究が示す        │
│ → 日本AI代理研究揭示了新的自主性框架  │
│                                      │
│ 与你的"展示而非决定"原则直接相关      │
│ ─────────────────────────────────────│
│        [image/chart/text]            │
│                                      │
└──────────────────────────────────────┘
```

For translated items:
- Country flag indicates the source language
- Title shown in Chinese (translated)
- Original-language title shown in smaller text above (for reference)
- Rationale in Chinese for translated items, English for EN items
- Tap to open original URL in original language

---

## LLM Comparison (Updated with Translation)

| Model | Input $/M | Output $/M | Native CN | Translation Quality | Score+Translate |
|---|---|---|---|---|---|
| DeepSeek V3.2 | $0.28 | $0.42 | ✅✅ | ✅ JA/KO/DE/FR→CN | ✅ Best value |
| MiniMax M2.5 | $0.30 | $1.10 | ✅✅ | ✅ Good | ✅ Good |
| GLM-4.7 | $0.60 | $2.20 | ✅✅ | ✅ Good | ✅ Good |
| GLM-4.7-Flash | Free | Free | ✅✅ | ⚠️ Acceptable | ⚠️ Free option |
| Claude Haiku 4.5 | $1.00 | $5.00 | ✅ | ✅ High quality | Layer 2 only |

**Recommendation: DeepSeek V3.2 for Layer 1** — best value for
combined score + translate. Native Chinese output quality is
excellent, and JA/KO/DE/FR translation to Chinese is strong
because these are high-resource language pairs in its training data.

---

## Cost Projection (Global Scale)

| Scale | Feeds | Languages | Items/day | L1 (DeepSeek) | L2 (Haiku) | Monthly |
|---|---|---|---|---|---|---|
| Phase A | 15 | EN+CN | 150 | $0.008 | $0.02 | $0.84 |
| Phase B | 50 | EN+CN+JA | 500 | $0.025 | $0.02 | $1.35 |
| Phase C | 120 | +KO+DE+FR | 1,200 | $0.06 | $0.03 | $2.70 |
| Phase D | 200 | +AR+RU+ES | 2,000 | $0.10 | $0.05 | $4.50 |
| Full | 300 | 10+ langs | 3,500 | $0.18 | $0.05 | $6.90 |

**Full global coverage: scan 3,500 items/day from 300 feeds in
10+ languages, translated + scored, for under $7/month.**

---

## Implementation Phases

### Phase A: Fix current + add DeepSeek (Week 1)
1. Fix scorer KeyError
2. Add DeepSeek V3.2 as Layer 1 provider
3. Keep Claude Haiku as Layer 2
4. Test two-tier pipeline with current 5 EN feeds
5. Verify: 50 items scored for ~$0.003

### Phase B: Add Chinese sources (Week 2)
1. Create Chinese RSS adapter with 15 feeds
2. Test DeepSeek scoring on mixed EN+CN items
3. Verify bilingual connection detection in Layer 2

### Phase C: Add Japanese + Korean (Week 3)
1. Add 10 JA feeds + 5 KO feeds
2. Add translation prompt to Layer 1 scoring
3. Test: JA/KO items → Chinese translation quality
4. UI: add language flag indicator on cards

### Phase D: Add European + Arabic (Week 4)
1. Add 10 DE/FR feeds + 5 AR feeds
2. Test translation quality for these language pairs
3. Cross-language bridge detection testing

### Phase E: Scale + optimize (Week 5+)
1. Expand to 200+ feeds across all tiers
2. Add feed health monitoring
3. Cross-source deduplication (same story in Reuters EN,
   Reuters JP, and 澎湃 CN → show once, note multi-source)
4. Connect scored feed to card-swipe UI
5. Deploy as Railway cron job

---

## Cross-Language Bridge Detection

This is the most unique capability of the system. Examples:

**JA→EN bridge**: ITmedia reports on a Japanese robotics lab's
approach to human-AI collaboration → connects to your English
memory about "present, never decide" principle. Neither your
English feeds nor your Chinese feeds would surface this.

**DE→CN bridge**: Heise Online covers a German HCI research paper
on attention management → connects to your Chinese memory about
注意力预算 (attention budget). A bridge across three languages
that no single-language system could find.

**AR→EN bridge**: Al Jazeera Tech covers Middle Eastern adoption
of open-source AI → connects to your English memory about making
things others use. Different market, same pattern.

Layer 2 prompt explicitly asks for cross-language connections:
"Does this [translated from Japanese] article connect to any of
Sean's memories, regardless of the original language of the memory
or the article?"
