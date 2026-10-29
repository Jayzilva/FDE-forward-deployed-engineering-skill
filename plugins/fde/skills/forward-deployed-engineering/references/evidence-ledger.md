# Evidence ledger: claims, receipts and acceptance

A deployment is judged on what the client accepts, not on what the team reports. This reference keeps five delivery states apart, records decisions with a source, and tracks open commitments. Use it in Build, Validate and Handoff, at every readout, and whenever someone asks "did we agree to X?" or "is it done?".

## Five delivery states

Never merge two states in one sentence. A local test pass is not a client outcome.

| State | Means | Evidence that proves it |
|---|---|---|
| Implemented | The code or configuration exists | A commit, PR or change ID |
| Verified | Agreed checks passed on a named revision and environment | Test output, verify report or eval score with the revision |
| Deployed | Running in the client's environment | Release record, deployment log or preview URL in their environment |
| Measured | The outcome metric moved against a baseline | Baseline and current value, method, sample size, date |
| Accepted | A named client-side person accepted the measured result | Name, date and a source: an email, meeting note, signed form or ticket |

Write each claim with its state: "Implemented and verified on staging (PR #42, verify report 2026-11-03). Not yet deployed." Say "claimed, not yet accepted" for anything without a signer.

## Value ledger

One row per promised outcome. Use `assets/templates/value-ledger.md`.

| Bucket | Promised | Baseline | Measured | Accepted by | Acceptance status | Evidence |
|---|---|---|---|---|---|---|

Rules for a row to count as **accepted**:

1. `Measured` holds a value, not `pending`.
2. `Accepted by` starts with a client-side person's name, then a date: `Priya Shah, 2026-11-14`. A role ("customer sponsor") or a bare word ("approved") does not identify a signer.
3. `Acceptance status` is `accepted`. Other values: `pending`, `rejected`, `revoked`. A later rejection or revocation updates the row.
4. `Evidence` names a source someone else can open: `PR #42`, a URL, `transcript:2026-11-14`, `evidence/replay.json`, `[source: meeting 2026-11-14]`. "Staging run" or "pending PR" is not a source.

Any row that fails a rule stays a **claim**. Run `python scripts/evidence_check.py <folder>` to list claims, accepted rows and the rule each claim fails. The script checks recorded fields. It cannot check that the client really consented.

FSPARK reactions are opinions on a prototype. "Looks right" from twenty reviewers is not acceptance of a delivered outcome.

## Decision log

Short form, one line per decision:

```
- 2026-11-03 Keep CSV upload for phase 1 [approved: Mara Ortiz 2026-11-03] [source: kickoff notes]
```

Only an explicit `[approved: Name YYYY-MM-DD]` stamp records client approval. "Agreed", "OK'd" or a name in the prose does not. Without the stamp, the decision is a team decision.

Long form, when the reasoning must survive the engagement (`assets/templates/decision-log.md`):

- Context: what prompted the decision.
- Options considered.
- Decision.
- Rationale: the line a successor cannot reconstruct from the code.
- Owner: the client-side person who approved it, or "team".
- Source: meeting date, PR, URL or transcript ID. Never infer it.

Use an ADR (`assets/templates/adr.md`) for architecture decisions. Link the ADR from the decision log.

## Answering "did we agree to X?"

1. Search the decision log, the value ledger and the debrief notes for the term.
2. Return the decision, the person, the date, the source and any later change.
3. If nothing is recorded, say so. Do not reconstruct an agreement from memory or code.

## Commitments and open questions

Keep these two lists in the engagement status file or the debrief notes:

```
## Commitments
- [ ] Delivery lead sends the ops runbook; due: 2026-11-20; source: workshop 2026-11-12
## Open questions
- [ ] Who accepts the staging replay? source: workshop 2026-11-12
```

Tick an item `[x]` only when its resolution is confirmed. When an agreed date changes, update the item and log the change as a decision. `evidence_check.py` flags items past their `due:` date.

## Private text

Wrap sensitive text in `<private>…</private>`: names of patients or customers, credentials, contract values, anything the trust profile marks as sacred. Rules:

- Never copy a private block into a readout, executive status, evaluation pack, FSPARK file, handoff export or commit message.
- Never paste a private block into a prompt for another tool or agent.
- `evidence_check.py --export` prints a file with private blocks replaced by `[private]`. Use that output when sharing.

## Readout discipline

At a readout, show the value ledger before anything else. Separate three groups: **on record** (accepted rows), **in progress** (implemented, verified or deployed, not measured), **claimed** (measured, not accepted). An executive repeats your top number. Make sure it is an accepted one.
