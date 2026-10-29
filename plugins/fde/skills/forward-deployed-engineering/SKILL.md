---
name: forward-deployed-engineering
description: "Situation-aware playbook for Forward Deployed Engineering (FDE): owning a deployment for a client, an internal team or a programme cohort from discovery through prototype, build, validation and handoff. Classifies the work on six axes (phase, environment, product, engagement model, starting point, delivery style), then produces the matching artifact: site survey, system map, competitor profile, gap matrix, requirements, outcome card, prototype scope and guided tour, migration ADR, pilot plan, ROI scorecard, exec status, demo checklist or handoff runbook. Use when deploying, piloting, prototyping or rolling out software, AI agents, Claude Code, MCP, data platforms or business apps; replacing a legacy system; running an FDE programme with gates; scoping a SOW or PoC; researching competitors for a gap analysis; preparing a discovery session, demo or readout; or rescuing a slipping deployment, even when the user does not say FDE."
---

# Forward Deployed Engineering

An FDE closes **the Delta**: the gap between what a product does out of the box and what one specific client needs to succeed. The work is half integration code and half judgment about people, scope and risk. Most engagements fail on the second half, so this skill treats documents, decisions, prototypes and stakeholder moves as engineering output.

FDE is a process, not a checklist. What to do next depends on the project, the audience and where the work starts. So the first job is always to **classify**, and only then to act.

## Step 1 — Load engagement state

If `.fde/engagement.yaml` exists, read it first: `python scripts/fde_state.py show`. It holds the situation, stakeholders, risks, decisions and dated gates from earlier sessions. Engagements run for weeks. Start from the saved state and do not re-ask answered questions.

If there is no state file and the user runs a real engagement (not a one-off question), offer `python scripts/fde_state.py init`. Do not force it for quick questions.

## Step 2 — Classify the situation on six axes

Infer each axis from what the user said and from the files in the repo. Ask only about an axis you cannot infer **and** that changes the answer. Otherwise state the assumption in one line and continue.

**What the work needs now — Phase**

| Phase | Signals | Core question |
|---|---|---|
| 1 Discover | kickoff, first call, site visit, data audit, "what do we have" | What is the real problem, and where is the ground truth? |
| 2 Scope | SOW, PoC, use cases, gap analysis, requirements, "what should we build" | Which slice of the Delta is worth closing first? |
| 3 Prototype | mock, demo UI, clickable prototype, "show the client", tour | Will the client recognise their problem solved before we build? |
| 4 Build | integration, connectors, architecture, MCP, agents, specs | What is the minimum architecture that proves value? |
| 5 Validate | pilot, UAT, evals, ROI, readout, Day-30 showcase, demo gate | Can we prove the value with numbers the buyer trusts? |
| 6 Handoff | leaving site, Day 2, champion, runbook, renewal, retire legacy | Will it keep running and growing after we leave? |

**Where it runs — Environment**: `cloud`, `regulated` (PII/PHI, audit, DLP), `on-prem` (firewalls, legacy systems), `air-gapped` (no internet, accreditation). A regulated or air-gapped flag moves security work to week 1.

**What is deployed — Product**: `ai-agent` (LLM app, RAG, agents, MCP), `claude-code` (developer activation), `data-platform`, `api-integration`, `business-app` (PSA, ERP module, CRM, internal portal). Product decides the metrics, the evals and the handoff contents.

**Who it is for — Engagement model**: `external` (a paying customer), `internal` (your own company's teams), `programme` (a cohort where each engineer owns a piece and proves it at dated gates), `partner` (through an SI or reseller). The model decides who signs off and what "done" means. Read `references/engagement-models.md`.

**Where it starts — Starting point**: `greenfield`, `prototype-exists`, `legacy-replace`, `rescue`, `scale-out`. This changes the first two weeks more than any other axis. Read `references/starting-points.md`.

**How work moves — Delivery style**: `classic` (tickets, sprints) or `spec-driven` (each change has a spec, acceptance criteria and a verify step; agents run tasks; people decide). Read `references/delivery-style.md` for requirements, tracking units, measures and AI cost.

A request can touch two phases ("scope the pilot" is Scope + Validate). Pick the primary one and pull in the other only when needed. For combinations that change the plan materially, read `references/situation-matrix.md`.

## Step 3 — Load only what the situation needs

| Need | Read |
|---|---|
| Phase playbook | `references/phase-1-discover.md` … `references/phase-6-handoff.md` (read the matching file in full) |
| Engagement model and audience | `references/engagement-models.md` (matching section) |
| Starting point, legacy migration patterns | `references/starting-points.md` (matching section) |
| Requirements, tracking, AI cost, build loop | `references/delivery-style.md` |
| Competitor and market research, gap analysis | `references/market-research.md` |
| Organising source documents for agents | `references/knowledge-base.md` |
| Environment gates | `references/environments.md` (matching section) |
| Product metrics, evals, architecture | `references/product-types.md` (matching section) |
| Claude, Claude Code, MCP specifics | `references/claude-deployments.md` |
| Stakeholders, executive comms, hostile situations | `references/stakeholders.md` |
| Something is going wrong, or a pre-mortem | `references/failure-modes.md` |
| Runbooks, CLAUDE.md, error text, agent instructions | `references/ste-writing.md` |

Load the matching section only. Loading everything wastes context and blurs the advice.

## Step 4 — Produce the artifact

FDE value is visible only through artifacts the client can act on. Default to producing one from `assets/templates/`:

| Phase | Primary artifacts |
|---|---|
| Discover | `site-survey.md`, `discovery-questions.md`, `ecosystem-map.md`, `competitor-profile.md` (one per vendor) |
| Scope | `delta-map.md`, `use-case-scorecard.md`, `gap-matrix.md`, `requirements.md`, `outcome-card.md`, `adr.md` |
| Prototype | `mock-scope.md`, the prototype as a separate version, a guided tour (`scripts/build_tour.py`) |
| Build | `adr.md`, `risk-register.md` |
| Validate | `pilot-plan.md`, `roi-scorecard.md`, `weekly-exec-status.md`, `demo-checklist.md` |
| Handoff | `handoff-runbook.md`, `champion-plan.md` |

Fill templates with the user's real facts. Where a fact is unknown, write `TBD — ask <role>`. An invented baseline is worse than a blank, because the client repeats it to their executive. Demo data in prototypes is fictional by design and must say so.

Use scripts for anything numeric or repeatable:

| Script | Use |
|---|---|
| `scripts/fde_state.py` | init, show, set, add-risk, add-decision, add-stakeholder, add-gate, calendar (flags weekend gates), advance, next |
| `scripts/qualify.py` | Rank use cases on volume, complexity, measurability, readiness. Structural vs marginal gain |
| `scripts/roi_calc.py` | Conservative and measured ROI. Refuses to run without a baseline |
| `scripts/capture_screens.py` | Screenshot every screen of a prototype and record control positions (needs Playwright) |
| `scripts/build_tour.py` | Turn captures plus a `tour.json` into a guided tour page: each screen, each control, the gaps |
| `scripts/ste_lint.py` | Lint runbooks, CLAUDE.md and acceptance criteria for STE structural rules |

If the user wants a file, write it (Markdown by default, HTML for tours and prototypes). If they asked a question, answer in chat and offer the artifact.

## Step 5 — Close with the FDE check

End substantive answers with:

```
FDE check
- Situation: <phase> / <environment> / <product> · <model> / <start> / <style> (assumptions: …)
- Biggest risk now: <one line>
- Next move: <one concrete action, owner, by when>
```

Update `.fde/engagement.yaml` when the user confirms a decision, a risk, a gate date or a phase change.

## Principles for every phase

- **Find the system of record before writing code.** If ground truth lives in a spreadsheet, the project is at risk. Say so.
- **Run what exists before you write requirements.** A prototype, a legacy screen or a vendor sandbox shows more than any interview.
- **Name the cost of inaction.** It sets priority and arms the champion.
- **Ask who owns Day 2 in week one.** No internal owner means the deployment dies when the FDE leaves.
- **Prefer structural gain over marginal gain.** "The unit of work changed" beats "the same task, faster" at a readout.
- **Capture the baseline before Day 1.** Without it there is no ROI denominator.
- **Show, then build.** A clickable prototype on consistent fictional data finds wrong requirements in days.
- **Replace legacy domain by domain.** Keep what the old system does well. Move a domain only after its parity gate.
- **Track the change, not the ticket.** Done means released and adopted: the old way is switched off.
- **Evidence over explanation.** A gate item passes when an artifact exists and someone else signs it.
- **Bottom line up front for executives.** Answer, then evidence, then detail.
- **Glue that recurs is product feedback.** Write it up when the same workaround appears twice.
- **Never promise what the environment cannot grant.** Check accreditation, quotas, residency and network paths before a date.
- **The goal is to become unnecessary.**

## Boundaries

- Not legal or contractual advice. Flag SOW and data-processing risk and point to the client's counsel.
- Compliance names (HIPAA, GDPR, FedRAMP, SOC 2) are pointers, not certification. Confirm with the client's security owner.
- Analyst reports, review sites and vendor pages: never work around a paywall, login or bot check. Use public sources and say which facts are snippets.
- Do not invent client facts, metrics, prices or quotes. Mark gaps.
