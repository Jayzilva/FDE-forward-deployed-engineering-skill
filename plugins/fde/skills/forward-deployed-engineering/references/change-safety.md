# Change safety: what breaks, and how to go back

On your own system you know what breaks. On a client's system you find out in production. Use this before you change a system you do not fully understand. Use it before you touch shared infrastructure (identity, database, messaging, network) or release in the next 48 hours.

## What breaks: trace the blast radius

For the module, service or configuration you will change, answer:

| Question | How to find out |
|---|---|
| Who calls this? | Search the code for the function, endpoint or queue name. Check API gateway logs |
| What does this call? | Read the imports, outbound calls and scheduled jobs |
| What data flows through? | Trace inputs to outputs. Mark personal data and money |
| What breaks if it returns something different? | Check each caller's assumptions about the response |
| What breaks if it is slow? | Timeouts, queues, user-facing waits |
| What breaks if it is down? | Fallbacks, retries, circuit breakers, or a cascade |
| Who owns each dependency? | A named team or person on the client side |

Classify the result:

| Radius | Means | Before the change |
|---|---|---|
| Contained | Only the changed module is affected | Normal review and tests |
| Local | One client team or service is affected | Tell the owner. Test their path on staging |
| Shared | Several teams, shared infrastructure or external partners | Change approval from the client, a rollback drill, a release window, the owners on call |

Write the result in `assets/templates/change-impact.md`. Record a shared-radius change in the decision log with the approver.

## Rollback: rehearse the way back

"We can always revert" is a wish until someone has done it. Map the path for each change type:

| Change type | Way back | Watch for | Rehearse by |
|---|---|---|---|
| Code release | Redeploy the previous version | Feature flags, caches, client-side bundles | Deploy the previous version on staging. Run the smoke checks |
| Database migration | Compatible down-migration, restore, or roll forward | Irreversible transforms, concurrent writes, old and new schema at once | Run it on staging data of realistic size. Time it. Check integrity and data loss |
| Configuration | Restore the previous values | Propagation delay, restarts | Flip the value on staging. Confirm every service picks it up |
| Infrastructure | Infrastructure-as-code revert, or manual | State drift, dependent resources | Plan the revert. Review the diff |
| Data backfill | Restore from backup, or a reverse script | Writes that happened after the backfill | Restore a backup to a scratch database. Check the row counts |
| Model or prompt change (AI) | Pin the previous model or prompt version | Cached answers, eval drift | Switch versions on staging. Re-run the eval set |

Drill rules:

1. Run the drill on the environment the client approves. Never on production without the client's change process.
2. Time it. If the way back takes longer than the client can tolerate, the plan needs a different release shape (feature flag, dark launch, smaller slice).
3. Record who ran it, when, how long, and what failed.
4. A rollback that has not been drilled is reported as "untested", not "available".

## Release readiness

Before a release, all of these hold, or the gap is written down with an owner:

- Verified on a named revision in the client's staging environment.
- Unhappy paths tested, not only the demo path.
- Rollback drilled, with the time recorded.
- The client's operating owner knows the change and is on call.
- Alerts route to the client's on-call.
- The value ledger row says what will be measured after release, and when.

A demo that worked and a local test that passed are not release evidence (`references/evidence-ledger.md`).
