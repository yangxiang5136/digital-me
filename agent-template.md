# Agent Template

## Standard Contract
Every agent reads from shared dirs, writes only to its own output folder.

### Reads (shared, read-only)
- ~/memory-agent/rubric.yaml
- ~/memory-agent/direction.yaml
- connections/scored-index.json

### Writes (isolated)
- [agent-name]/output/
- [agent-name]/cache/
- [agent-name]/logs/

## config.yaml Pattern
```yaml
agent:
  name: "[AGENT_NAME]"
  version: "0.1"
paths:
  rubric: "~/memory-agent/rubric.yaml"
  direction: "~/memory-agent/direction.yaml"
  scored_index: "connections/scored-index.json"
  output_dir: "[agent-name]/output/"
```

## Build Checklist
- [ ] One-line description written
- [ ] Inputs/outputs defined
- [ ] config.yaml written
- [ ] Dry run tested locally
- [ ] system-status.yaml updated (status: running)
- [ ] attention-budget.yaml reviewed
