# Phase 5 — Validate

Goal: produce evidence the buyer trusts, by a fixed date, that the deployment created value. A good feeling at Day 30 is not an outcome.

## Pilot design

Decide these before Day 1 and write them in `assets/templates/pilot-plan.md`:

- **Cohort**: who uses it. Pick motivated users with real volume, plus at least one sceptic. A pilot of only enthusiasts proves nothing to the rest of the org.
- **Scope**: the qualified use cases only.
- **Duration**: long enough to cover the task's natural cycle (usually 2–6 weeks), with a fixed readout date.
- **Success criteria**: numeric thresholds agreed with the sponsor, including the "stop" threshold.
- **Comparison**: the baseline from before Day 1, or a control group doing the same work the old way.

## Baseline capture (before Day 1)

Without pre-pilot data there is no denominator for ROI. Capture, for the same cohort and task:

- Cycle time per unit of work (ticket, report, case, PR, migration).
- Throughput per person per week.
- Quality: defect, rework, or error rate.
- People and hand-offs per unit of work (this is what structural gain changes).
- Cost: hours x loaded rate, or external spend.

Use existing systems (ticketing, version control, CRM, logs) where possible. Self-reported time estimates are weak; label them as such.

## Metrics that hold up

Strong: cycle time from system timestamps, throughput from system counts, error rates from QA or audit samples, team size and elapsed time for a defined deliverable.
Weak (use only as supporting colour): satisfaction surveys, "hours saved" self-reports, usage counts, number of prompts.

Usage is not value. High usage with no change in the work metric means the tool is popular, not useful.

## ROI

Run `python scripts/roi_calc.py` with baseline and pilot numbers. It reports per-unit and annualised savings, payback, and refuses to compute without a baseline. Present the conservative case first; executives trust the low number.

## UAT

Real users, real tasks, real data. Watch them work rather than demo to them. Record where they hesitate or work around the tool. If users do not change their behaviour, the pilot failed regardless of the metrics.

## Weekly rhythm

- Weekly executive status (`assets/templates/weekly-exec-status.md`): BLUF, value delivered with numbers, risks with the decision needed and from whom.
- Office hours for pilot users.
- A short internal retro: what glue recurs, what should go to the product team.

## The readout (Day 30 showcase)

Structure: the answer (did it work, by the agreed criteria) → the evidence (baseline vs pilot) → what users said and did → the recommendation (scale, adjust, or stop) → what it takes to scale (people, budget, decisions). Show the flow from their messy system to the result, not a feature tour.

## Evaluation and review days

When a programme or steering group reviews the piece, prepare `templates/evaluation-pack.md`. Rank every concern as confident, acceptable risk or doubt, and say what evidence would move it. A reviewer trusts a "doubt" you name more than a risk they find.

## Exit artifacts

Pilot plan, ROI scorecard, readout deck or doc, decision on scale/adjust/stop.
