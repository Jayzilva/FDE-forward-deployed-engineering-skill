# Situation matrix

Use this when the environment x product combination changes the plan, not just the details. Each cell lists what moves earlier, what gets harder, and the first artifact to produce.

## How to read a cell

- **Pull forward**: work that must start in week 1 for this combination.
- **Harder**: the part of the Delta that will take longer than the client expects.
- **First artifact**: what to produce before anything else.

## ai-agent (LLM apps, RAG, agents, MCP)

| Environment | Pull forward | Harder | First artifact |
|---|---|---|---|
| cloud | Golden dataset + eval harness; tool permission model | Getting real (not demo) documents and edge cases | Site survey with a data sample request |
| regulated | Data classification, DLP/redaction, model-provider DPA, audit logging of prompts and outputs | Approval to send data to a model API; human-in-the-loop requirement | Risk register (data flow + approvals) |
| on-prem | Network path to model endpoint (proxy, private link), identity integration | Connectors to legacy systems behind firewalls | Site survey: connectivity section first |
| air-gapped | Open-weight model selection, offline weights with checksums, local inference runtime, package mirrors | Eval and monitoring without cloud tooling; update path for models | ADR: model + runtime choice |

## claude-code (developer activation)

| Environment | Pull forward | Harder | First artifact |
|---|---|---|---|
| cloud | Baseline metrics from the target teams; CLAUDE.md for the pilot repos | Moving developers from supervised use to delegation | Use-case scorecard |
| regulated | Data-handling settings, approved model access path, policy on code and secrets in prompts | Security sign-off before developers touch production repos | Risk register |
| on-prem | Proxy/egress rules for the API, internal package registries, MCP servers to internal tools | Repos and tooling that assume network access | Site survey: dev-environment section |
| air-gapped | Usually not viable as hosted Claude Code. Confirm the deployment path with the vendor before scoping. | Everything | ADR documenting feasibility before any commitment |

## data-platform

| Environment | Pull forward | Harder | First artifact |
|---|---|---|---|
| cloud | Data audit and profiling; system-of-record map | Data quality, missing keys, undocumented joins | Site survey: data landscape |
| regulated | Residency, masking, lineage, access reviews | Proving lineage for auditors | Risk register |
| on-prem | Bulk transfer plan (bandwidth vs physical transfer), CDC from legacy DBs | Change windows and DBA availability | ADR: ingestion pattern |
| air-gapped | Manifest-based import/export, signed artifacts, offline package mirrors | Any outbound telemetry | ADR: sync pattern |

## api-integration

| Environment | Pull forward | Harder | First artifact |
|---|---|---|---|
| cloud | Auth model (OAuth/SSO), rate limits, sandbox access | Undocumented client APIs and field semantics | Delta map |
| regulated | Data minimisation, field-level permissions, audit trail | Change-approval boards | Risk register |
| on-prem | Firewall/port tickets (multi-week lead time), service accounts | Connectivity approvals | Site survey: connectivity |
| air-gapped | Batch file exchange instead of live API | Real-time requirements | ADR: integration pattern |

## business-app

| Environment | Pull forward | Harder | First artifact |
|---|---|---|---|
| cloud | Ecosystem map; system of record per domain; role model from the identity provider | Money logic (rates, FX, revenue rules) that lives in spreadsheets | Ecosystem map |
| regulated | Pay and personal-data privacy, audit trail, separation of duties | Proving who changed a rate or a timesheet | Risk register |
| on-prem | Read connectors to legacy databases, change windows | Running two systems during migration | ADR: migration pattern |
| air-gapped | Batch import/export with signed files | Any client-facing portal | ADR: sync pattern |

## Engagement model and starting point

These two axes change the plan as much as the environment. Read `engagement-models.md` and `starting-points.md`.

| Combination | Pull forward | First artifact |
|---|---|---|
| internal + legacy-replace | Legacy strengths list; migration pattern; parity gate per domain | ADR (migration) |
| any + prototype-exists | Run the prototype; screen inventory; guided tour | Mock review + tour |
| programme + any | Gate calendar with weekday check; evidence and signer per gate item | Outcome card + gate plan |
| external + rescue | Honest status; scope cut; re-baselined dates | Risk register |
| partner + scale-out | Partner pairing; runbooks in STE strict | Handoff runbook |

## Red-flag combinations

Escalate during Discover if you see any of these:

- Regulated or air-gapped, and no named security owner on the client side.
- AI agent, and no one can supply 30+ real examples with known correct answers (no ground truth, no eval).
- Claude Code activation, and no baseline metrics exist for the pilot teams.
- Any product, and "data will be ready in two weeks".
- Legacy replacement, and nobody can say which system owns each domain.
- Programme gate dates that fall on weekends or holidays nobody has checked.
- A prototype shown to the client with numbers that do not add up across screens.
