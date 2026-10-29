---
description: Check the value ledger, decision log, stakeholder signals and open commitments; answer "did we agree to X?"
argument-hint: "[folder, or a question such as 'did we agree to ERP sync?']"
allowed-tools: Read, Write, Bash, Grep
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/evidence-ledger.md`.

If $ARGUMENTS is a question about an agreement, search the decision log, value ledger and debrief notes. Return the decision, who, when, the source and later changes. If nothing is recorded, say so. Do not reconstruct an agreement.

Otherwise run `python ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/evidence_check.py <folder>` (default `fde/`). If no ledger exists, create `fde/value-ledger.md` from `value-ledger.md` with the outcomes in the outcome card. Report accepted rows, claims with the rule each fails, unconfirmed decisions, stale signals and overdue items. Never change a claim to accepted without a named signer and a source from the user.
