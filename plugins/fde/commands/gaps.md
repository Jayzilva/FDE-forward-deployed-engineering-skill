---
description: Build the gap matrix (market vs legacy vs prototype) and propose requirement IDs
argument-hint: "[path to prototype review or requirements]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/market-research.md` (From research to gaps) and `delivery-style.md` (Requirements).

Inputs: competitor profiles, the legacy system notes, the prototype review, the requirements file. Write `fde/gap-matrix.md` from `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/assets/templates/gap-matrix.md`. Every row cites a source. Mark which gaps must close before a client sees the next prototype. List where the solution wins, legacy strengths to keep, and new requirement IDs. Do not edit the requirements file until the user accepts the new IDs.
