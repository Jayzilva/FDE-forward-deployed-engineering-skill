---
description: Check a demo or programme gate against the evidence checklist before presenting
argument-hint: "<demo or gate name> [paths to outcome card, spec, verify report, preview URL]"
allowed-tools: Read, Glob, Grep, Agent
---
Use the forward-deployed-engineering skill. Run the `demo-reviewer` agent with `$ARGUMENTS` and `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/assets/templates/demo-checklist.md` (or the programme's own rubric if the knowledge base has one; the programme rubric wins).

Print its table as returned: item, result, evidence path, signer, what is missing. End with "Ready: yes/no" and the fix list in order.
