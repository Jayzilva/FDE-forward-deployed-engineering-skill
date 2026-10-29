# Runbook: <System name>

Owner: <name and team>. Escalation: <name, channel, response time>.
Write this file in STE100 Strict mode. Check it with scripts/ste_lint.py before handoff.

## 1. Purpose

This system <does one thing for one group of users>.
It reads data from <source system>. It writes data to <target system>.

## 2. Glossary

| Term | Meaning |
|---|---|
| <term> | <one meaning only> |

## 3. Daily checks

1. Open the dashboard at <link>.
2. Check that the last successful run is less than <N> hours old.
3. Check that the error count is less than <N>.
4. If a check fails, go to section 5.

## 4. Normal operations

### 4.1 Start the service

1. Connect to <host or console>.
2. Run this command: `<command>`.
3. Make sure that the status page shows "healthy".

### 4.2 Stop the service

1. Tell the users in <channel> that the service will stop.
2. Run this command: `<command>`.
3. Make sure that no jobs are in the queue.

### 4.3 Deploy a change

1. Merge the change to the main branch.
2. Make sure that the pipeline passes.
3. Run the eval suite with this command: `<command>`.
4. If the score is less than <threshold>, do not deploy. Contact the owner.

## 5. Recovery procedures

### 5.1 The pipeline stops

1. Read the last 50 lines of the log at <location>.
2. If the log shows a schema error, stop the import. Contact the data owner for <source>.
3. If the log shows a timeout, restart the job with this command: `<command>`.
4. If the job fails again, contact the escalation contact.

### 5.2 The credentials expire

1. Get a new secret from <secret store>.
2. Update the secret at <location>.
3. Restart the service. Use section 4.1.

## 6. Monitoring and alerts

| Alert | Meaning | Action |
|---|---|---|
| <alert name> | <what failed> | <section number> |

## 7. Contacts

| Role | Name | Channel |
|---|---|---|
| System owner | | |
| Data owner | | |
| Vendor support | | |
