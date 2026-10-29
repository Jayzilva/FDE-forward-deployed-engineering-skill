# Starting points

Where the engagement starts changes the first two weeks more than any other axis. Ask: "What exists today that the client already uses or has already seen?"

| Start | Signals | First move | First artifact |
|---|---|---|---|
| `greenfield` | Idea, slide, RFP, "we want an AI agent for X" | Find the system of record and the baseline | Site survey |
| `prototype-exists` | A mock, demo, PoC or vendor sandbox already exists | Run it. Record what it shows and what it fakes | Mock review (see phase 3) |
| `legacy-replace` | A homegrown or old system does the job today | Map the legacy system's strengths and data. Choose a migration pattern | ADR (migration) |
| `rescue` | Slipping dates, hostile stakeholders, failed pilot | Stop building. Run a pre-mortem on the present state | Risk register + honest status |
| `scale-out` | A pilot worked; expand to more teams or sites | Find what the pilot team did by hand that others cannot | Champion plan + handoff runbook |

## greenfield

- The risk is building the wrong thing. Spend the time in Discover and Scope.
- Get 30 real examples (documents, tickets, records) before the prototype. Synthetic data hides edge cases.

## prototype-exists

A prototype is the cheapest discovery tool you will get. Use it before you write requirements.

1. **Run it locally** and capture every screen (`scripts/capture_screens.py`). Keep the original untouched.
2. **Inventory the screens**: what each one shows, which role sees it, which data is fake.
3. **Mark what it fakes.** A margin shown as a typed number is not a margin model. Label each claim: implemented, partial, demo data, planned.
4. **Write a guided tour** for people new to it (`scripts/build_tour.py`): each screen, each control, and the gaps.
5. **Compare against the market** (`market-research.md`) and build a gap matrix.
6. **Build the next version separately.** Never overwrite the version the client already saw.

## legacy-replace

Homegrown systems hold years of rules nobody wrote down. Replacing one in a single cut is the most common way internal platforms fail.

- **List what the legacy system does well.** Access models, audit, history rules and reminder chains are often better than the replacement's first version. Keep them as requirements.
- **Choose a pattern in an ADR:**

| Pattern | When | Risk |
|---|---|---|
| Strangler (domain by domain) | Several domains, a live system people rely on | Two systems run for a while. Needs a parity gate per domain |
| Big-bang cut-over | Small system, one domain, short freeze possible | One bad weekend undoes trust |
| Keep and extend | Legacy is sound; the gap is one layer (for example money or reporting) | Legacy limits the new layer |
| Buy | A commercial product covers 80% | Fit-gap, licence cost, lock-in |

- **System of record per domain.** Write which system owns each domain now and the date it moves. Record it with `fde_state.py set system_of_record`.
- **Parity gate.** A domain moves when the new system matches the old one on an agreed list, and the users confirm.
- **Read connector first.** Read from the legacy system during the transition. Write back only when unavoidable.
- **Archive history** with source IDs when a domain retires.

## rescue

- Status goes honest first. A GREEN report with a blocker that needs an executive is the main symptom.
- Cut scope to the smallest slice that proves value. Re-baseline the dates with the sponsor.
- Read `failure-modes.md` and run the `engagement-reviewer` agent.

## scale-out

- The pilot team's tacit knowledge is the product now. Write it down as runbooks and CLAUDE.md files.
- Measure the second team against its own baseline, not the pilot team's.
