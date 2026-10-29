# Engagement models

The same FDE work changes shape with **who the client is** and **who judges the result**. Classify the model first. It decides who signs off, what "done" means, and which artifacts the audience expects.

| Model | Who the FDE serves | Who judges success | "Done" means |
|---|---|---|---|
| `external` | A paying customer of the vendor | Customer sponsor | Customer metric moved; Day-2 owner runs it |
| `internal` | Teams inside the FDE's own company (internal platform, back office, tooling) | Internal sponsor and the people who use the old system | Old system or old way switched off |
| `programme` | A cohort or academy where each engineer owns one real piece | Programme reviewers at fixed gates | Gate evidence signed by someone other than the engineer |
| `partner` | A client reached through a partner, SI or reseller | Partner and end client | Partner can run and resell it without the FDE |

## external

- Use the five-phase arc as written. The readout and the ROI scorecard carry the engagement.
- The sponsor is outside your company. Every number in an artifact must come from the client's systems.
- Product feedback is part of the job. Write up glue that recurs across clients.
- Before a proposal, give the sponsor a short executive brief (`templates/executive-brief.md`): opportunity, challenge, solution, value at each cadence, illustrative screens with sample data, next step. Mark it "for discussion, not a contractual offer". Reference earlier deliveries without naming those clients.

## internal

Internal work fails for different reasons: no budget line, no deadline pressure, and a legacy system that "works well enough".

- **Name the customer anyway.** Treat the internal team as a client. Write an outcome card with their metric.
- **Map the system landscape first** (`templates/ecosystem-map.md`). Internal platforms touch HR, finance, identity and dev tools. Find each system of record.
- **Replacement is a migration, not a launch.** If a homegrown system exists, read `starting-points.md#legacy-replace` and write an ADR before any build.
- **Usage data is sensitive.** Internal dashboards about people (hours, tokens, output) need a privacy rule: cost and capacity measures, never individual performance scores.
- **Adoption is the finish line.** Track an `adopted` state: the old spreadsheet, form or system is off for that domain.

## programme

A programme turns FDE practice into a curriculum: each engineer owns a real piece, works in short slices, and proves progress at dated gates.

- **Load the programme rules into the knowledge base** (`knowledge-base.md`). Rules, gates, rubric, levels and known conflicts between source documents go in one index.
- **Calendar first.** Record every gate with `fde_state.py add-gate`. Run `fde_state.py calendar`. Flag weekend dates and gates that collide with client availability.
- **Evidence over explanation.** A gate item passes only when an artifact exists and someone other than the engineer signs it. See `templates/demo-checklist.md`.
- **Short slices.** One slice is about two working days and ends in a demo. One slice is one tracked change (`delivery-style.md`).
- **The demo shows the journey**: problem, spec, build trail, verification, live result. Later demos add learnings, security and cost, and the decision.
- **Map the piece to the gates.** The roadmap names which gate each slice serves. A slice that serves no gate is scope creep.
- **Portfolio.** Each artifact records what went wrong and what changed. Reviewers read this more than the happy path.
- **Evaluation pack.** For a review day, answer the fixed questions in `templates/evaluation-pack.md`: problem, customer wish, research, prototype, success, concerns ranked by confidence, path, pending decisions.
- **Keep client material out of shared repos.** Programme repos are often shared across a cohort. Store client documents, briefs and evaluation notes in an ignored folder or the client's own space.

## partner

- The partner is your Day-2 owner. Pair them from week 1.
- Write every runbook for someone who never met the client (STE strict mode).
- Agree who owns support tiers and who talks to the end client's executive.

## Audience: write for the reader

| Reader | Format | Writing mode |
|---|---|---|
| Executive | One page, bottom line first, one decision request | STE-flavoured |
| Client users | Guided tour, plain words, no internal terms | STE-flavoured |
| Engineers and operators | Runbook, ADR, requirement IDs | STE strict |
| AI agents | CLAUDE.md, tool descriptions, acceptance criteria | STE strict |
| Reviewers or assessors | Evidence table: item, artifact path, signer | STE strict |
