# Change impact: <change> — YYYY-MM-DD

Author: <name> | System: <service/module> | Planned release: YYYY-MM-DD | Client change process: <name or none>

## Blast radius
| Question | Answer | How checked |
|---|---|---|
| Who calls this? | | |
| What does it call? | | |
| What data flows through (personal data, money)? | | |
| What breaks if the response changes? | | |
| What breaks if it is slow? | | |
| What breaks if it is down? | | |
| Owners of each dependency | | |

Radius: contained / local / shared. Approver (if shared): <Name> [approved: Name YYYY-MM-DD]

## Way back
| Change type | Way back | Rehearsed on | Rehearsed by | Date | Time taken | Result |
|---|---|---|---|---|---|---|
| | | | | | | untested / passed / failed |

## Release readiness
- [ ] Verified on revision <sha> in <environment>
- [ ] Unhappy paths tested: <list>
- [ ] Rollback drilled, time recorded
- [ ] Client operating owner on call: <name>
- [ ] Alerts route to client on-call
- [ ] Value ledger row names the measure after release and the date
