---
description: Find, classify, rank and plan tests for the assumptions behind a brief, plan or requirement set
argument-hint: "[brief, plan or folder to read]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill. Load state. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/assumptions.md`.

Read $ARGUMENTS (or the brief, discovery notes and requirements in `fde/`). Extract every claim without evidence. Classify kind (FACT, CONVENTION, UNKNOWN), blast radius and source. Rank by blast radius and cost to test. Write `fde/assumptions-register.md` from `assumptions-register.md`.

End with the three critical assumptions to test this week, each with the smallest test, an owner and a date. Then run the red-team pass from the reference on the top claim.
