# Phase 6 — Handoff

Goal: the deployment keeps running and keeps growing after the FDE leaves. A system that needs the FDE to survive is not finished.

## Start handoff in week 1

The Day-2 owner should be named in Discover and should pair with the FDE during Build. Handoff in the final week is a document drop; handoff from the start is a transfer of ownership.

## Champion enablement

- **Who**: a respected practitioner (not only a manager) on the client side who already uses the tool well and wants to own it.
- **Invest**: pair on real work, give them commit rights on the glue repo, make them the first responder during the pilot with the FDE as backup.
- **Equip**: internal docs, the eval suite, the runbook, and the escalation path to your company.
- **Credit**: make their work visible to the sponsor. Champions stay when the role helps their career.

Use `assets/templates/champion-plan.md`.

## Documentation as deployment infrastructure

Docs are part of the system, not an afterthought. Minimum set:

- **Runbook**: how to operate, monitor, and recover. Written in STE100 Strict mode (see `ste-writing.md`) because the reader is under pressure, may be a non-native English speaker, or may be an agent. Template: `assets/templates/handoff-runbook.md`. Lint it with `python scripts/ste_lint.py <file>`.
- **Architecture overview + ADRs**: why it is built this way.
- **Eval suite with instructions**: how to check nothing regressed after a change.
- **For Claude Code deployments**: a CLAUDE.md per key repo and any team plugins or skills, also in STE style. These are what keep agent behaviour consistent after you leave.

## Transition checklist

- Access: client owns all credentials, service accounts, and cloud resources; FDE access removed or time-boxed.
- Operations: alerts route to client on-call; client has run at least one incident or recovery drill.
- Change: client has shipped at least one change through the pipeline without FDE help.
- Support: escalation path to your company documented with response expectations.
- Commercial: renewal or expansion conversation scheduled with the sponsor, using the ROI evidence.

## Feed back to HQ

Write a short field report for your product team: recurring glue, product gaps, environment surprises, what to template for the next client.

## Exit artifacts

Handoff runbook (STE-linted), champion plan, transition checklist signed off, field report.
