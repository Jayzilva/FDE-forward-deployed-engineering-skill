---
description: Build a guided tour of a prototype for people new to it (screens, controls, gaps)
argument-hint: "<capture folder from capture_screens.py>"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill.

1. If the folder has no `els.json`, run `uvx --with playwright python ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/capture_screens.py <prototype> --out <folder>` first.
2. Read `els.json`. For each screen write plain-language spots (control text, label, what it does), gaps with a level (demo | next | later) and a requirement ID, and what to keep. Add screens that do not exist yet under "missing". Save `tour.json` (run `build_tour.py --example` for the schema).
3. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/build_tour.py <folder>`. Fix any "no element starts with" error by copying the exact text from `els.json`.
4. Report the path to `index.html` and offer to publish it.
