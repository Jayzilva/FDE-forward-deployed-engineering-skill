# Value ledger: <Client> — <Engagement>

Updated: YYYY-MM-DD | Owner: <name>

A row counts as **accepted** only when: `Measured` has a value, `Accepted by` starts with a client-side name and a date, `Acceptance status` is `accepted`, and `Evidence` names a source someone else can open. Every other row is a **claim**. Check with `python scripts/evidence_check.py <folder>`.

| Bucket | Promised | Baseline | Measured | Accepted by | Acceptance status | Evidence |
|---|---|---|---|---|---|---|
| <time / cost / quality / risk / revenue> | <outcome and target> | <value, method, date> | <value or pending> | <Name, YYYY-MM-DD> | pending | <PR #, URL, transcript:ID, [source: meeting YYYY-MM-DD]> |

## Delivery state per slice

| Slice | Implemented | Verified (revision, environment) | Deployed | Measured | Accepted |
|---|---|---|---|---|---|
| <slice> | <PR/commit> | <verify report, env> | <release record> | <ledger row> | <yes/no> |

## Readout summary

- On record (accepted):
- In progress (implemented, verified or deployed, not measured):
- Claimed (measured, not accepted):
