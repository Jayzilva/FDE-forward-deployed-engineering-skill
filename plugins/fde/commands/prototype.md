---
description: Review an existing prototype, then scope and build the next version separately
argument-hint: "<path or URL of the current prototype> [gap matrix path]"
allowed-tools: Read, Write, Edit, Bash
---
Use the forward-deployed-engineering skill. Read `${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/references/phase-3-prototype.md` and `starting-points.md#prototype-exists`.

1. Run the prototype locally. Capture it: `uvx --with playwright python ${CLAUDE_PLUGIN_ROOT}/skills/forward-deployed-engineering/scripts/capture_screens.py <path-or-url> --out fde/prototype-v1`.
2. Write `fde/prototype-v1/review.md`: screen inventory, what works, what it fakes (evidence labels), numbered issues.
3. If a gap matrix exists, write `fde/mock-scope.md` from the template: journeys per persona, screens, out of scope. Stop and ask the user to approve the scope.
4. After approval, build the next version in its own folder from v1 plus patches and new screens, with a build script. Reuse the existing design system. Badge new items. Keep demo numbers consistent across screens.
5. Open every new screen headless in light and dark mode. Fix errors and overflow. Report how to run it.
