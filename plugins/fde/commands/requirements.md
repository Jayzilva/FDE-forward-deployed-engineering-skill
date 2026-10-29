---
description: Turn gaps and client reactions into stable requirement IDs with a trace table
argument-hint: "[source: gap matrix, session notes]"
allowed-tools: Read, Write, Edit
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/delivery-style.md`.

Write or update `requirements.md` from `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/assets/templates/requirements.md`. One sentence per requirement, STE strict mode, MoSCoW priority, status in the current system with an evidence label, and a wave. Keep IDs stable: never renumber. Acceptance criteria go to the spec of the change that builds it, not here. Update the trace table when a change ID exists. Lint with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/ste_lint.py requirements.md`.
