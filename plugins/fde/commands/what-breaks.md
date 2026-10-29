---
description: Trace the blast radius of a change and plan and record a rollback drill before release
argument-hint: "<change, module or release>"
allowed-tools: Read, Write, Grep, Glob, Bash
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/change-safety.md`.

For $ARGUMENTS, search the repository for callers, outbound calls and data flows. Classify the radius as contained, local or shared. Map the way back for each change type in the release. Write `fde/change-impact-<date>.md` from `change-impact.md`.

Mark every rollback that nobody has rehearsed as "untested". List the release-readiness gaps with owners. Do not run a drill on any environment without the user's explicit go-ahead and the client's change process.
