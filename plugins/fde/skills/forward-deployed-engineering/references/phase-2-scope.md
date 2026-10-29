# Phase 2 — Scope

Goal: choose which slice of the Delta to close first, and fence it so the engagement can succeed on time.

## Map the Delta

For each client need, classify what the product does today:

| Fit | Meaning | Action |
|---|---|---|
| Native | Product does it with configuration | Configure. No code. |
| Extend | Product supports it through an extension point (API, plugin, MCP, webhook) | Build glue on the supported path. |
| Gap | Product cannot do it | Build outside the product, or descope, or raise to the product team. |
| Wrong ask | The need is not real or another tool fits better | Say so, with reasons. |

`assets/templates/delta-map.md` holds this table plus effort and risk columns. Glue on unsupported paths (scraping, DB writes behind the product's back) becomes the client's maintenance problem; record it as a risk.

## Qualify use cases

Score each candidate on four criteria, 1–5:

- **Volume**: how often the task happens. Rare tasks cannot show ROI in 30 days.
- **Complexity**: enough complexity that the product adds value, not so much that the pilot cannot finish.
- **Measurability**: a baseline exists or can be captured before Day 1.
- **Readiness**: the users, data, and access are available now.

Then label the gain:

- **Structural**: the unit of work changes (team size, cycle time, number of hand-offs, a step disappears).
- **Marginal**: the same work runs faster.

Prefer structural. A marginal gain is real but hard to anchor an executive business case to inside a short pilot. Run `python scripts/qualify.py` with the candidates to rank them reproducibly.

## Minimum viable architecture

Design the simplest system that proves the chosen use case: fewest new components, managed services where allowed, one integration path. Write down what is deliberately excluded and when it would be needed. Use `assets/templates/adr.md` for each non-obvious choice so the next engineer knows why.

## Fence the scope

Every scope document needs an explicit **Out of scope** list. Scope creep arrives as reasonable small requests; the out-of-scope list is what lets you say "yes, in phase 2" instead of "yes". Tie success criteria to numbers agreed with the sponsor.

## Pressure-test before committing dates

- Are all access and network approvals requested, with lead times known?
- Is the baseline capture scheduled before kickoff?
- Is there a named client owner for each dependency?
- Does the environment allow the architecture (model access, data residency, quotas)?

## Gaps and requirements

When a prototype, legacy system or market reference exists, compare all three in `templates/gap-matrix.md` (see `market-research.md`). Turn each gap into a requirement ID with a priority (`templates/requirements.md`, `delivery-style.md`). Mark the gaps that must close before a client sees the next prototype.

## Outcome card

Write one card per piece of work (`templates/outcome-card.md`): client, problem in one sentence, success measure with a baseline, the old way that will be switched off, the demo date. Every later artifact points back to it.

## Exit artifacts

Delta map, use-case scorecard (top 1–3), gap matrix, requirement IDs, outcome card, scope with out-of-scope list, first ADR (for a legacy system: the migration ADR).
