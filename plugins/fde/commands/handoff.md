---
description: Build the handoff pack - STE-linted runbook, champion plan, transition checklist
argument-hint: "[system details]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill in the Handoff phase. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/phase-5-handoff.md` and `ste-writing.md`.
1. Write `fde/runbook.md` from `handoff-runbook.md` in STE100 Strict mode.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/ste_lint.py fde/runbook.md`. Fix every hard violation and rerun until it exits 0. Keep every hedge and safety condition.
3. Write `fde/champion-plan.md` and the transition checklist.
4. For Claude Code deployments, draft CLAUDE.md for each key repo in the same style and lint it.
