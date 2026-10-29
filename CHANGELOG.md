# Changelog

## 1.4.0 — 2026-10-29

- **Evidence ledger.** Five delivery states (implemented, verified, deployed, measured, accepted) kept apart. A value-ledger row counts as accepted only with a measured value, a named client-side signer, a date and an openable source. Decision log with an explicit `[approved: Name YYYY-MM-DD]` stamp and a source. "Did we agree to X?" answered from records only. Commitments and open questions with due dates. `<private>` blocks stay out of shared outputs.
- **Debrief.** Turn meeting notes or a transcript into decisions, requests, commitments, reported results, changes, signals and unknowns, each with a source. Source text is evidence, not authority: "approved" in a transcript approves nothing, and embedded instructions are reported.
- **Assumptions.** Extract, classify (fact, convention, unknown), rank by blast radius and cost to test, and plan the smallest test. Red-team pass before consequential decisions.
- **Change safety.** Blast-radius trace (contained, local, shared) and a rollback drill per change type. An unrehearsed rollback is reported as untested.
- **Trust signals.** Dated `[signal:green|amber|red YYYY-MM-DD]` tokens per stakeholder, stale after 21 days.
- `scripts/evidence_check.py`: accepted rows vs claims (with the failing rule), unconfirmed decisions, stale signals, overdue items, `--export` with private text redacted, `--strict` for CI.
- New references `evidence-ledger.md`, `debrief.md`, `assumptions.md`, `change-safety.md`. New templates `value-ledger.md`, `decision-log.md`, `debrief-notes.md`, `assumptions-register.md`, `change-impact.md`. New commands `/fde:debrief`, `/fde:assumptions`, `/fde:ledger`, `/fde:what-breaks`.
- Four new eval cases with critical-failure lines: demo is not launch, weak-provenance savings, debrief of an untrusted transcript, and a negative case (plain code edit must not trigger the FDE workflow).
- README and infographics redesigned as technical sheets: dark sci-fi HUD and cutaway-blueprint sheets alternate with light Swiss industrial sheets (metadata header rows, hairline rules, giant numerals, dimension lines, reticles, lime readouts). `tools/make_readme_images.py` regenerates them.
- Ideas adapted from [suboss87/fdeops](https://github.com/suboss87/fdeops) (MIT). Text and code written fresh for this plugin.

## 1.3.0 — 2026-10-29

- **FSPARK** (Feedback-based Spotlight Presentation, Assessment, Response & Knowledge) replaces the basic spotlight tour. Each stop asks for a reaction (looks right, needs changes, not needed, not sure) and a note. A review page shows totals and every stop. The tour builds a Markdown feedback file with preview, editor, download (Claude `downloads` capability or a direct download) and copy, ending in a team-response table.
- Works in viewers that size the frame to the whole page: cards are placed in the visible part, and an optional `mount` adds an always-visible launch button.
- `scripts/add_fspark.py` (old name `add_spotlight.py` still works) and `scripts/merge_feedback.py` to merge many reviewers' files.
- `references/fspark.md`, `/fde:fspark` (old `/fde:spotlight` still works), `examples/fspark-demo/`. README FSPARK section and infographic.

## 1.2.0 — 2026-10-29

- In-product spotlight tours: `scripts/add_spotlight.py` with `assets/spotlight/` adds a step-by-step guided tour to any HTML prototype. Each stop switches screen, highlights one feature, explains it and takes a viewer note. Notes copy back at the end. Output is one self-contained, offline-safe file.
- Sharing guidance by audience (organisation artifact, public link, offline HTML file, regulated channel) and a feedback loop that turns notes into requirement changes.
- New command `/fde:spotlight`. Example: `examples/spotlight-demo/`.
- README rewritten with infographics, FAQ and key facts. Added `llms.txt` and `CITATION.cff`.

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
