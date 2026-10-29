---
description: Draft the weekly executive status (BLUF, decision needed, value, risks)
argument-hint: "[this week's notes]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill. Load state and open risks. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/stakeholders.md` (executive communication).
Draft `fde/status-<date>.md` from `weekly-exec-status.md` using $ARGUMENTS. Status colour must match reality: any blocker that needs an executive is RED or AMBER, never GREEN. One decision request, with owner and date.
