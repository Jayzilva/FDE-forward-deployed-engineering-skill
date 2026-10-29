# Failure modes

Use for a pre-mortem at kickoff and whenever an engagement starts to slip. For each, the early signal and the move.

| # | Failure mode | Early signal | Move |
|---|---|---|---|
| 1 | Wrong problem | Requester cannot name a metric; no user met | Back to Discover; meet users; restate the problem in the client's numbers |
| 2 | No ground truth | System of record unclear; "it's in a few places" | Make SoR a week-1 deliverable; scope down to data that has an owner |
| 3 | Data late or dirty | "Ready in two weeks"; samples refused | Work from a sample now; build quality checks; escalate with dates |
| 4 | Access stall | Tickets open > 5 days; no named approver | Sponsor escalation with a specific ask and impact |
| 5 | Late security veto | Review not booked in week 1 | Book it in week 1; bring data-flow diagram and controls |
| 6 | No baseline | Pilot starting, no pre-pilot numbers | Delay start by days to capture it, or use a control group |
| 7 | Demo-driven expectations | Sponsor quotes demo accuracy | Agree thresholds on the client's golden set before build |
| 8 | Gold-plating | Features nobody asked for; MVA growing | Re-read scope; cut to the use case; log extras for phase 2 |
| 9 | Adoption stalls | Usage drops after week 2; users stay in supervised mode | Office hours on real tasks; champion-led sessions; design delegation steps |
| 10 | Usage mistaken for value | Readout built on logins and prompt counts | Switch to work metrics vs baseline before the readout |
| 11 | Hero dependency | Only the FDE can fix or deploy | Pair with Day-2 owner; client ships a change unaided before exit |
| 12 | Unsupported glue | Writes behind a system's back; scraping | ADR + owner sign-off, or replace with a supported path |
| 13 | Scope creep | Many small "quick" asks | Out-of-scope list; "yes, in phase 2" |
| 14 | Sponsor drift | Sponsor misses two status meetings | One-page BLUF with a decision request; ask the champion why |
| 15 | Environment surprise | Quota, proxy, residency, or clock issues found late | Walking skeleton in the real environment in week 1 |

## Pre-mortem prompt

At kickoff, ask: "It is Day 30 and this failed. What happened?" Map each answer to a row, assign an owner, and put it in the risk register.
