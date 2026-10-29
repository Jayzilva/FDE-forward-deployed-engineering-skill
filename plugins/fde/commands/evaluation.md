---
description: Build an evaluation pack for a programme gate, assessment or stakeholder review
argument-hint: "<piece name> <gate or review> [paths to outcome card, gap matrix, prototype, tour]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/engagement-models.md` (programme) and `phase-5-validate.md` (Evaluation and review days).

Fill `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/assets/templates/evaluation-pack.md` from the engagement state and the artifacts named in `$ARGUMENTS`. Link every claim to its artifact. Rank each concern as confident, acceptable risk or doubt. Write `TBD — ask <role>` for missing facts. If the material holds client details, write the pack to a git-ignored folder and say so. Offer to render it as a page.
