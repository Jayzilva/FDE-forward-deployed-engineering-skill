---
description: Start or resume an FDE engagement and classify it on six axes
argument-hint: "<client> — <engagement> [env] [product] [model] [start] [style]"
allowed-tools: Read, Write, Bash
---
Use the forward-deployed-engineering skill.

1. If `.fde/engagement.yaml` exists, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/fde_state.py show` and summarise the situation, gates and gaps.
2. Otherwise parse `$ARGUMENTS` and the repo for: client, engagement, environment (cloud | regulated | on-prem | air-gapped), product (ai-agent | claude-code | data-platform | api-integration | business-app), model (external | internal | programme | partner), start (greenfield | prototype-exists | legacy-replace | rescue | scale-out), style (classic | spec-driven). Infer what you can. Ask one question only if an axis is unknowable and changes the plan.
3. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/fde_state.py init --client "<client>" --engagement "<engagement>" --env <env> --product <product> --model <model> --start <start> --style <style>`.
4. If the model is programme, or the user gave dates, record each gate with `fde_state.py add-gate YYYY-MM-DD "<name>"` and run `fde_state.py calendar`. Report weekend dates.
5. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/situation-matrix.md` for the matching cells, plus the matching sections of `engagement-models.md` and `starting-points.md`. Report: what to pull forward, what will be harder, the first artifact.
6. End with the FDE check block.
