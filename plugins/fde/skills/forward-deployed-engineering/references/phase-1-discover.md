# Phase 1 — Discover

Goal: understand the real problem and the ground truth before writing code. A week of discovery prevents a month of building the wrong thing.

## Outcomes before leaving this phase

1. The business problem in the client's words, and the measurable outcome they would pay for.
2. The system of record for each data entity the solution touches.
3. Named people: sponsor, champion, likely blocker, Day-2 owner, security/compliance owner.
4. The environment classification and its gates (access, network, approvals) with lead times.
5. A candidate quick win for week 2.
6. A list of red flags, each with an owner.

## The diagnostic sequence

Run these in order. Each answer narrows the next question.

1. **Problem, not feature.** When the client asks for a feature ("we want a chatbot"), ask what decision or task it would change and what happens today. Ask "why" until you reach a cost: time, money, risk, or headcount. Often the right solution is different from the request (a chatbot request is often a search-over-policies need).
2. **System of record.** "Where does the truth for this live?" If the answer is a spreadsheet, a person, or "several places", record it as a top risk.
3. **Cost of inaction.** "If we do nothing for six months, what happens?" This sets priority and gives the champion an argument upward.
4. **Definition of done.** "What would you need to see on Day 30 to say this worked?" Push for a number.
5. **Day 2.** "Who runs this after we leave?" No name means no durable deployment.
6. **Constraints.** Data classification, residency, network, identity, approvals, change windows, quotas.

`assets/templates/discovery-questions.md` turns this into a call script grouped by stakeholder.

## Data audit (first technical task)

Before proposing architecture, look at real data:

- Get a sample (or a profile run) from each source. Count rows, nulls, duplicates, key coverage, date ranges.
- Find undocumented semantics: status codes, free-text fields used as structured data, soft deletes.
- Identify shadow IT: the spreadsheet or side database where the useful data actually lives.
- For AI products: collect 30–100 real inputs with known correct outputs. This is the start of the golden dataset.

A local tool (DuckDB, pandas, SQL against a read replica) is enough. Do not stand up infrastructure to discover.

## Stakeholder map

For each person: role, what they want, what they fear, influence level, and stance (champion / neutral / blocker). IT and security are usually blockers by default, because the project adds risk to their job without credit. Meet them early and give them ownership of something.

## Red flags (escalate now, not in week 4)

- "Data will be ready in two weeks."
- "We don't need a project manager on our side."
- No executive sponsor, or the sponsor cannot name a metric.
- Security review not started and the environment is regulated or air-gapped.
- The requester is not the user, and you have not met a user.
- Success defined as "it works" or "people like it".

## When something already exists

- **A prototype or product**: run it before the first workshop. Capture every screen and write a mock review (`starting-points.md#prototype-exists`).
- **A legacy system**: list what it does well and who depends on it. Those become keep-requirements.
- **The client's system landscape**: map every system the solution touches, its owner, and whether you replace, integrate or keep it (`templates/ecosystem-map.md`). Unknown systems (often accounting) become open questions with an owner.
- **Source documents**: load them into the knowledge base (`knowledge-base.md`) on day one.

## Exit artifact

`assets/templates/site-survey.md`, filled. Share a one-paragraph BLUF summary with the sponsor: what we found, the biggest risk, the proposed quick win.
