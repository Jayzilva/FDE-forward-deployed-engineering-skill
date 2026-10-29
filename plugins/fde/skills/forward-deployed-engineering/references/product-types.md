# Product types

Read only the matching section. Each covers the Delta pattern, the metrics that matter, the evals, and what the handoff must include.

## Contents
- ai-agent
- claude-code
- data-platform
- api-integration
- business-app

## ai-agent

LLM applications, RAG, tool-using agents, multi-agent systems, MCP servers.

**Typical Delta**: client documents and systems are messier than the demo corpus; tools the agent needs live behind client auth; accuracy expectations are set by the demo, not by reality.
**Architecture defaults**: retrieval with hybrid search (semantic + keyword) for domain terms; narrow tools with clear descriptions; deterministic workflow steps where the path is known and model reasoning only where it adds value; human approval before irreversible actions; prompt injection treated as a given when the agent reads untrusted content.
**Metrics**: task success rate on the golden set; groundedness/citation accuracy; tool-call correctness; escalation rate to humans; latency p95; cost per task; downstream business metric (handle time, resolution rate).
**Evals**: golden dataset from real client cases (30+ to start, grown with every failure); rubric or model-graded checks for open answers, exact checks where possible; regression run on every change.
**Handoff must include**: the eval suite and how to run it, prompt and tool versioning, a monitoring view of failures, the process for adding cases.

## claude-code

Activating Claude Code (or Claude Enterprise for developers) across engineering teams. See also `claude-deployments.md`.

**Typical Delta**: repos lack the context an agent needs; developers stay in supervised mode and never delegate; security needs a policy before production repos.
**Metrics**: favour structural measures — elapsed time and team size for defined deliverables (migrations, test-coverage uplift, upgrade programmes, internal tools); cycle time and throughput from VCS and ticketing; review rework rate. Treat prompt counts and seat activity as adoption signals, not value.
**Evals**: a set of representative tasks per repo, rerun after CLAUDE.md or plugin changes.
**Handoff must include**: CLAUDE.md per key repo, team plugins/skills/commands, MCP servers to internal tools, a champion per team, a policy doc.

## data-platform

Pipelines, warehouses, analytics, ML feature stores.

**Typical Delta**: twenty-year-old schemas; no primary keys; business definitions disagree across departments; volumes larger than estimated.
**Architecture defaults**: layered storage (raw immutable → cleaned → business-ready); transformations as version-controlled code; partitioning and clustering chosen from real query patterns; data-quality checks as circuit breakers.
**Metrics**: data freshness; pipeline success rate; query cost and latency; time-to-answer for analysts; number of conflicting definitions resolved.
**Handoff must include**: lineage, data contracts with source owners, quality-check alerts routed to client on-call, a definitions glossary.

## api-integration

Wiring a SaaS or platform product into client systems.

**Typical Delta**: undocumented client APIs and field meanings; rate limits; identity mapping between systems; a proprietary file format.
**Architecture defaults**: adapters at the boundary; idempotent writes; retries with backoff; dead-letter queue for failures; contract tests against sample payloads.
**Metrics**: sync success rate; end-to-end latency; manual reconciliation effort before vs after; incidents caused by the integration.
**Handoff must include**: interface contracts, replay procedure for failed messages, credential-rotation steps, owner for each connected system.

## business-app

A line-of-business system for one client: PSA, ERP module, CRM, internal portal, back-office workflow. Often replaces a homegrown tool (see `starting-points.md#legacy-replace`).

**Typical Delta**: money logic nobody wrote down (rates, margin, revenue rules); several legal entities and currencies; roles and approvals; a client-facing view; integration with identity, accounting and HR systems.
**Architecture defaults**: domain modules with one system of record each; an audit log at the persistence layer; roles from the identity provider; read connectors to the legacy system during transition; every agent action under the same permissions as the UI.
**Metrics**: time to close the month; time from period end to invoice; % of work with a cost and a margin; adoption per domain (old way switched off); user-reported effort before vs after.
**Handoff must include**: the system-of-record map, role and permission matrix, rate and FX reference data owners, month-end runbook, the retired system's history archive.
