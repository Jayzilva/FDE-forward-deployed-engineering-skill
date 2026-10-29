# Delivery style: requirements, tracking and the build loop

Classify the delivery style: `classic` (tickets, sprints, story points) or `spec-driven` (each change has a written spec, acceptance criteria and a verify step; agents execute tasks; people direct, review and decide). Many AI-assisted teams are spec-driven even when they do not call it that.

## Requirements that survive the handoff

- Give every requirement a stable ID: `<AREA>-NN` (for example `FIN-03`, `POR-01`). Areas follow the client's language, not the vendor's modules.
- Each row: ID, requirement (one sentence, STE strict), priority (MoSCoW), status in the current system, wave or release.
- Requirements say **what and why**. Acceptance criteria say **how we check**. Keep acceptance criteria in the spec of the change that builds it, not in the requirements file, so they have one owner.
- Keep a **trace table**: requirement ID → change ID → phase. It answers "where is FIN-03?" in one look.
- Label every claim about an existing system with its evidence level: implemented, partial, demo data, documented only, planned, not evidenced.

Template: `templates/requirements.md`.

## Tracking unit

| Style | Unit of work | Estimate | Progress signal |
|---|---|---|---|
| classic | Story or ticket | Story points | Status moved by a person |
| spec-driven | One change (one spec, about two working days) | Size class: small, medium, architectural | Phase derived from the repo: proposed, planned, building, verified, released |

For spec-driven work add two phases owned outside the repo:

- **released** — the change reached the client's production environment (set by deployment).
- **adopted** — the client switched the old way off (set by a named client person). This is "done" for an FDE.

Epics stay only as a client-facing grouping. Plan in changes.

## Measures that replace story points

| Measure | Definition |
|---|---|
| Lead time | proposed → released |
| Adoption time | released → adopted |
| First-pass verify rate | changes that pass verify on the first run |
| Rework rate | changes re-specified after a demo |
| Agent run time and AI cost per change | from agent logs and the AI gateway or usage reports |
| Cost per change | human hours × cost rate + AI cost |
| Human decision hours | review, clarification, demo time. Plan capacity in these, because review is the constraint, not typing |

## Agents as workers

When agents do billable work, put them in the resource plan as non-human workers: each acts for a named person, has a spend cap, and logs its runs. Over-allocation applies to people. Spend caps apply to agents.

## AI resource cost

AI-assisted delivery has two cost shapes. Track both or project margin is wrong.

| Shape | Examples | Allocation |
|---|---|---|
| Seat | Per-person AI subscriptions | Split the seat cost across projects by usage share, else by allocation % |
| Metered | API keys, agents in CI, in-app AI | Direct to the project or change that made the call |

Rules: store counts and cost only, never prompt content. Usage is a cost and capacity measure, never an individual performance score. Plans and prices change, so keep them as dated reference data.

## The build loop (one slice)

1. Propose: problem, scope, out of scope, requirement IDs.
2. Plan: spec with acceptance criteria, design, ordered tasks.
3. Build: tasks run in waves; commit per task; log learnings.
4. Verify: tests against every criterion; eval scores for agent work.
5. Demo: show the journey (see `templates/demo-checklist.md`).
6. Release, then adopt.

No spec, no build. No demo, no "done".
