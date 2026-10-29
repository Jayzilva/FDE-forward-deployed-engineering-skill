---
description: Add a guided spotlight tour with feedback notes to a prototype, then share it the right way
argument-hint: "<prototype.html> [audience: internal | external-link | external-file | regulated]"
allowed-tools: Read, Write, Edit, Bash
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/phase-3-prototype.md` (Guided spotlight tour, Share it with the right audience).

1. Find what is new in the prototype (badges, the prototype scope, the gap matrix). Add `data-tour="<name>"` to each element a stop points at.
2. Write `steps.json` next to the prototype (`add_spotlight.py --example` prints the schema). One stop per new feature, one or two plain sentences each, a requirement tag where one exists, and a final "your turn" stop.
3. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/add_spotlight.py <prototype.html> steps.json --out <tour.html>`.
4. Open it headless at desktop and phone width and walk every stop. Fix any stop whose target is missing.
5. Recommend the sharing channel from the audience table and ask the user to confirm it before anything is published or sent. Never put client data or client names on a public link.
6. After feedback arrives, file each note as confirms, change, new requirement or out of scope, and update the requirement IDs.
