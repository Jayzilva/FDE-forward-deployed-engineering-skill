# Environments

Read only the section that matches. Each lists gates (things that need approval or lead time), default controls, and the failures that only happen in that environment.

## Contents
- cloud
- regulated
- on-prem
- air-gapped

## cloud

Client runs on public cloud or SaaS and grants you access to a project, tenant, or account.

**Gates**: IAM roles in the client's account; quota for compute or model throughput; SSO integration; procurement of any new managed service.
**Default controls**: infrastructure as code from day 1 (so the client can reproduce and own it); workload identity instead of long-lived keys; private networking where offered; budgets and cost alerts.
**Failure modes**: quota discovered at launch; resources created by hand that nobody can reproduce; cost surprise in the first invoice; the FDE's personal credentials hard-wired into a pipeline.

## regulated

Finance, healthcare, government, or any client handling PII/PHI or under audit.

**Gates**: data classification; security architecture review; privacy or data-protection impact assessment; vendor and subprocessor approval (including model providers); change-advisory board.
**Default controls**: data minimisation (send only the fields needed); masking or redaction before data leaves the trust boundary; audit logs of who accessed what and, for AI, of prompts and outputs; data-residency pinning; human review for decisions that affect customers.
**Failure modes**: security review started in week 3 and takes eight weeks; model provider not on the approved-vendor list; test data copied from production without approval; audit asks for lineage you did not record.
**Note**: regulation names (HIPAA, GDPR, SOX, PCI DSS, local banking rules) are pointers. The client's compliance owner decides what applies.

## on-prem

Client data centre, legacy systems, internal networks.

**Gates**: firewall and port change tickets (often weeks); VPN or private connectivity; service accounts in the client's directory; maintenance windows for legacy systems; DBA availability.
**Default controls**: read replicas or change-data-capture instead of queries against production; containerised deployment that matches the client's platform; internal package and image registries.
**Failure modes**: bandwidth too low for the data volume (consider physical transfer); proxy breaks TLS or blocks model endpoints; undocumented dependency on a server that is rebooted monthly; "can we just run it on-prem for now" masking distrust of the cloud plan.

## air-gapped

No internet, or one-way transfer only. Defence, critical infrastructure, some industrial and research sites.

**Gates**: accreditation or authority to operate (months, not weeks); cleared personnel; approved media transfer process; cross-domain transfer approval.
**Default controls**: offline package and container mirrors; signed images and artifacts with an offline root of trust; checksummed model weights in a safe format (safetensors, not pickle); local PKI and time sync; store-and-forward telemetry; manifest-based import/export with human sign-off.
**Failure modes**: clock drift breaks TLS and tokens; certificates expire with no renewal path; no way to get day-1 configuration in; a dependency fetches from the internet at runtime; model updates impossible after go-live; telemetry needed for evals cannot leave the enclave.
**Product note**: hosted AI APIs are usually not available. Choose open-weight models and a local inference runtime, and confirm licensing and export-control constraints on the weights.
