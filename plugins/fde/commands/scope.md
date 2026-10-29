---
description: Map the Delta, qualify use cases (structural vs marginal), and fence scope
argument-hint: "[candidate use cases or client asks]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill in the Scope phase. Load state if present.
Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/phase-2-scope.md`.
1. Build `fde/delta-map.md` from the template: classify each need as native, extend, gap, or wrong ask.
2. Write the candidates to `fde/use-cases.json` and run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/qualify.py fde/use-cases.json`. Explain any score you assigned and its evidence.
3. Write `fde/use-case-scorecard.md` with the top 1-3, the metric each moves, and an explicit out-of-scope list.
4. Write an ADR for the minimum viable architecture.
