---
description: Prepare discovery - call script by stakeholder, data-audit plan, and site survey draft
argument-hint: "[notes, transcript, or client brief]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill in the Discover phase. Load state if present.
Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/phase-1-discover.md` and the matching sections of `environments.md` and `product-types.md`.
Input: $ARGUMENTS (notes, a transcript, or a brief).
Produce `fde/site-survey.md` from `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/assets/templates/site-survey.md` and `fde/discovery-questions.md` tailored to this client. Mark unknowns as `TBD — ask <role>`. List red flags with owners. Record new risks and stakeholders in state.
