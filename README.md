# Digital Me — System HQ

Project management and infrastructure for the Digital Me multi-agent system. Memory content lives in [`yangxiang5136/my-memories`](https://github.com/yangxiang5136/my-memories).

## Key Files

| File | Purpose |
|------|---------|
| `system-status.yaml` | Living dashboard — agent states, metrics, open issues, next session priority |
| `session-handoff-template.md` | Standard format for ending a chat session and starting the next one |
| `agent-template.md` | Abstract framework for building a new agent |
| `gh-sync.py` | Syncs Connection Mapper improvements → GitHub Issues |

## Active Agents

| Agent | Version | Status | Deployment |
|-------|---------|--------|------------|
| Memory Agent | v1 | ✅ Running | Railway |
| Connection Mapper | v2.1 | ✅ Running | Local |
| News Agent | — | 🔲 Planned | — |

## Design Principles
- Plain files are the source of truth (markdown, YAML, JSON)
- GitHub Issues and Obsidian are *views*, not replacements
- Agents read from shared directories, write only to their own isolated output folders
- Privacy-first: no external data stores, no vendor lock-in
