---
description: Compute a defensible ROI scorecard from baseline and pilot numbers
argument-hint: "--units N --base-hours H --pilot-hours H --rate R [--solution-cost C] [--base-people P --pilot-people P]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/roi_calc.py $ARGUMENTS`. If the user gave numbers in prose, map them to flags first and show the mapping.
Fill `fde/roi-scorecard.md` from the template. Lead with the conservative case. State the measurement method and its weaknesses. Never invent a baseline.
