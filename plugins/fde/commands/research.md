---
description: Profile competitors or market references for a gap analysis
argument-hint: "<vendor1, vendor2, ...> [requirement areas]"
allowed-tools: Read, Write, Bash, Agent, WebSearch, WebFetch
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/market-research.md` and `knowledge-base.md`.

1. If no vendors are given, propose five or six from different segments and confirm the list in one line.
2. Give each `market-researcher` agent two vendors, the client context (size, stack, regions, currencies) and the requirement areas. Run them in parallel.
3. Each agent writes `resources/solutions/<vendor>/docs/sources.md` and `docs-md/01_<vendor>-profile.md` from `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/assets/templates/competitor-profile.md`, plus `00_INDEX.md` with conflicts.
4. Add the vendors to the knowledge-base map. Report the five strongest ideas and every fact that could not be confirmed.
