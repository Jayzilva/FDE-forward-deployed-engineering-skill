# Stakeholders

Most FDE engagements that fail do so for people reasons with technical symptoms. Treat stakeholder work as part of the build.

## Roles to identify

| Role | What they need from you | Risk if ignored |
|---|---|---|
| Executive sponsor | A number tied to their goals, early and often | Funding and attention move elsewhere |
| Champion | Credibility, early wins, visible credit | No one fights for the project internally |
| End users | Less tedious work, not more process | Polite non-adoption |
| IT / platform | Assurance it will not break their systems or add on-call load | Access and network tickets stall |
| Security / compliance | Data flows, controls, evidence | Late veto |
| Day-2 owner | Understanding and ownership, not a document drop | Deployment decays after you leave |

## Executive communication

- **Bottom line up front.** Lead with the answer or decision needed; then evidence; then detail on request.
- **Numbers over adjectives.** "Cycle time down from 9 days to 4 for 22 tickets" beats "significant improvement".
- **Ask for one decision at a time**, with the owner and the date.
- **Status colours mean something.** Green: on track. Amber: at risk, mitigation in hand. Red: needs an executive decision. Never report green while waiting on a blocker you cannot remove.

## Hostile or blocking stakeholders

Treat resistance as information. Common causes and moves:

- **Fear of replacement** (often IT or the team whose work is automated): show what the tool removes from their day; give them ownership of part of the deployment, such as co-authoring the deployment scripts.
- **Burned before** by a vendor: under-promise, deliver a small thing fast, keep every commitment.
- **Risk owner** (security, compliance): bring the data-flow diagram and controls proactively; ask what evidence they need, then provide exactly that.
- **Competing priorities**: tie the project to the blocker's own goals, or escalate through the sponsor with a specific ask.

Have the one-to-one conversation before escalating. Escalate with facts, impact, and a proposed decision, never with blame.

## Trust

A useful model: trust grows with credibility, reliability, and intimacy, and shrinks with self-orientation. In practice: know their business, do what you said by when you said it, listen more than you pitch, and make it about their win, not your product.

## Scope pressure

New requests are a sign the client sees value. Respond with "yes, and here is where it fits" against the out-of-scope list: now (swap for something), next phase, or not recommended (with the reason).
