# fde — Forward Deployed Engineering plugin

A situation-aware FDE playbook. The skill classifies each request on six axes, loads only the matching playbook and produces a client-ready artifact. See the repository README for the full description.

| Axis | Values |
|---|---|
| Phase | discover, scope, prototype, build, validate, handoff |
| Environment | cloud, regulated, on-prem, air-gapped |
| Product | ai-agent, claude-code, data-platform, api-integration, business-app |
| Engagement model | external, internal, programme, partner |
| Starting point | greenfield, prototype-exists, legacy-replace, rescue, scale-out |
| Delivery style | classic, spec-driven |

## Contents

- `skills/forward-deployed-engineering/` — router `SKILL.md`, 18 references, 20 templates, 7 scripts, 5 eval cases, guided-tour page template
- `commands/` — `/fde:start`, `/fde:discover`, `/fde:research`, `/fde:scope`, `/fde:gaps`, `/fde:requirements`, `/fde:prototype`, `/fde:spotlight`, `/fde:tour`, `/fde:pilot`, `/fde:roi`, `/fde:demo`, `/fde:evaluation`, `/fde:brief`, `/fde:status`, `/fde:premortem`, `/fde:handoff`
- `agents/` — `engagement-reviewer`, `market-researcher`, `demo-reviewer`

## Scripts

| Script | Purpose | Needs |
|---|---|---|
| `fde_state.py` | Engagement state in `.fde/engagement.yaml`: six axes, stakeholders, risks, decisions, gates; `calendar` flags weekend gates | stdlib |
| `qualify.py` | Rank use cases; structural vs marginal gain | stdlib |
| `roi_calc.py` | Conservative and measured ROI; refuses to run without a baseline | stdlib |
| `capture_screens.py` | Screenshot each screen of a prototype and record control positions | Playwright |
| `build_tour.py` | Guided tour page from captures and `tour.json` | stdlib |
| `add_spotlight.py` | In-product spotlight tour with per-stop notes; one offline-safe file | stdlib |
| `ste_lint.py` | Structural plain-English lint for runbooks and agent instructions (vendored, MIT) | stdlib |
