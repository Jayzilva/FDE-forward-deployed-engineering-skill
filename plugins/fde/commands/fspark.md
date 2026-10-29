---
description: Add FSPARK to a prototype (spotlight tour, feedback per feature, Markdown feedback file) and share it the right way
argument-hint: "<prototype.html> [audience: internal | external-link | external-file | regulated]"
allowed-tools: Read, Write, Edit, Bash
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/fspark.md`.

1. Find what is new in the prototype (badges, the prototype scope, the gap matrix). Add `data-tour="<name>"` to each element a stop points at.
2. Write `config.json` next to the prototype (`add_fspark.py --example` prints the schema): one stop per new feature in plain words, a requirement tag where one exists, a final "your turn" stop, `product`, `prototypeUrl`, `fileName` and a `mount` selector for an always-visible launch button.
3. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/add_fspark.py <prototype.html> config.json --out <tour.html>`.
4. Open it headless at desktop and phone width. Walk every stop, give reactions, create the feedback file and download it. Fix any stop whose target is missing.
5. Recommend the sharing channel from the table in `fspark.md` and ask the user to confirm before anything is published or sent. As a Claude artifact, publish with capabilities `{"downloads": true}`. Never put client data or client names on a public link.
6. When files come back, run `merge_feedback.py *.md --out feedback-summary.md`, decide each row (confirms, change, new requirement, out of scope), update the requirement IDs and fill the team-response column.
