# Phase 4 — Build

Goal: ship the minimum viable architecture into the client's real environment, with the glue, observability, and safety needed to survive contact with real data.

## Build order

1. **Walking skeleton in the real environment.** One thin end-to-end path through the client's network, identity, and data, even if it does almost nothing. Most schedule risk is in the environment, not the logic, and a skeleton exposes it in days.
2. **Golden path with real data.** Make the chosen use case work for the common case.
3. **Evals and observability** before features. If you cannot measure it, you cannot defend it at the readout.
4. **Edge cases from the data audit.** Handle the top failure categories, not every one.
5. **Hardening** for the environment: least-privilege identities, secrets management, encryption, audit logs.

## Integration patterns (glue)

| Situation | Pattern |
|---|---|
| Client system has a stable API | Adapter service with retries, idempotency keys, and rate-limit handling |
| Client system has no API, only a database | Read from a replica or CDC stream; never write behind the system's back without the owner's sign-off |
| Files arrive in batches | Landing zone (raw, immutable) → validated → business-ready layers; reject and quarantine bad files |
| Real-time need, slow AI step | Two tiers: fast deterministic path for the decision, async AI path for explanation or enrichment |
| Many tools for an AI agent to reach | Expose them through MCP servers with narrow, well-described tools (see `claude-deployments.md`) |
| Legacy proprietary format | A parser at the edge that converts to an open format, plus a sample-file test suite |

Keep glue in a repo the client can own, with a README that a new engineer can follow. Glue that only the FDE understands is a liability.

## Data circuit breakers

Upstream data will break. Add checks at ingestion (schema, row counts, null rates, freshness) that stop the pipeline and alert, so the FDE hears about it before the executive sees a broken dashboard.

## Evals (all AI products)

- Start from the golden dataset gathered in Discover. Grow it with every production failure.
- Measure what the buyer cares about: correctness on their cases, groundedness/citation accuracy for retrieval, tool-call correctness for agents, latency, cost per task.
- Run evals on every prompt, model, or retrieval change. A change without an eval run is a guess.
- Keep a small set of adversarial cases: out-of-scope questions, prompt injection in documents, missing data.

## Decisions to record (ADR)

Write an ADR for: model choice, hosting location, data flow across trust boundaries, any write path into a client system, any deviation from the product's supported extension points, any security exception. `assets/templates/adr.md`.

## Product feedback

When you build glue that another client will also need, log it: the need, the workaround, the estimated reuse. This is how FDE work becomes product, and it is the main argument for the FDE function's value inside your own company.

## Change safety

Before you touch an unfamiliar or shared system, trace the blast radius. Before a release, rehearse the rollback. `references/change-safety.md`, `assets/templates/change-impact.md`.

## Exit criteria

Running in the client environment with real data; evals green against agreed thresholds; observability live; risk register current; ADRs written; decision log sourced; rollback rehearsed for each release.
