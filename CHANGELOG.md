# Changelog

## 1.1.1 — 2026-10-29

- Evaluation pack lists supporting artifacts in reading order and puts the decisions needed at the top.

## 1.1.0 — 2026-10-29

- New templates: `evaluation-pack.md` (programme gate or stakeholder review: problem, customer wish, research, prototype, success, concerns ranked by confidence, path, pending decisions) and `executive-brief.md` (short proposal for a sponsor, value per cadence, illustrative screens with sample data).
- New commands: `/fde:evaluation`, `/fde:brief`.
- Guidance to keep client material out of shared programme repos.

## 1.0.0 — 2026-10-29

Rebuilt from the 0.1 field kit into a universal FDE plugin.

- Three new classification axes: engagement model (external, internal, programme, partner), starting point (greenfield, prototype-exists, legacy-replace, rescue, scale-out) and delivery style (classic, spec-driven).
- New Prototype phase between Scope and Build: review what exists, scope the next version, build it separately, guided tour, client feedback loop.
- New product type: business-app (PSA, ERP module, CRM, internal portal).
- New references: engagement models and audience, starting points and legacy migration patterns, market and competitor research, delivery style (requirements, change-based tracking, AI cost), engagement knowledge base.
- New templates: outcome card, system landscape map, competitor profile, gap matrix, requirements with trace, prototype scope, demo checklist.
- New scripts: `capture_screens.py`, `build_tour.py`. `fde_state.py` gains the new axes, dated gates and a weekend check.
- New commands: research, gaps, requirements, prototype, tour, demo. New agents: market-researcher, demo-reviewer.
- Two new eval cases. `tools/package.py` validates the plugin and builds the `.skill` file.

## 0.1.0

Router skill on phase × environment × product, 11 templates, ROI and use-case scoring, engagement state, STE linting, engagement reviewer.
