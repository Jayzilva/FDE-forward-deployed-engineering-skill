# Writing for the field: STE100 style

Runbooks, CLAUDE.md files, skill instructions, MCP tool descriptions, error messages, and handoff notes are read by people under pressure, non-native English speakers, and AI agents — none of whom can ask the author what was meant. Apply ASD-STE100 Simplified Technical English discipline to these texts.

Adapted from the asd-ste100 skill by danyuchn (MIT): https://github.com/danyuchn/asd-ste100-skill

## Which mode

- **Strict**: runbooks, recovery procedures, CLAUDE.md, tool descriptions, error messages, agent instructions. Apply every rule.
- **STE-flavoured**: status reports, architecture overviews, ADRs. Apply the structural rules; vary vocabulary where it helps.
- **Do not apply**: executive narratives and readouts where persuasion matters. Use BLUF instead.

## Structural rules

- Active voice: "The on-call engineer restarts the service." Not "The service is restarted."
- One instruction per sentence. Numbered list for 3+ steps.
- Sentence length: 20 words or fewer for instructions, 25 for descriptions.
- No semicolons. Split the sentence.
- No phrasal verbs: "start", not "spin up"; "contact", not "reach out".
- Noun clusters: 3 words or fewer.
- Do not drop articles or subjects to save space.
- Simple tenses. Keep a compound tense only when it carries information ("may have failed").
- Keep every hedge. "May have failed" never becomes "failed".
- One word, one meaning: pick one term per thing and reuse it.
- Verbs, not nominalisations: "analyse the log", not "perform an analysis of the log".
- Put safety conditions first: "If the queue has more than 1,000 items, stop the import."

## Lint

`python scripts/ste_lint.py <file>` checks the structural rules mechanically. Exit code 1 means hard violations. Use `--json` for structured output and `--disable rule1,rule2` to silence rules. Fix the findings, then reread for meaning: the linter checks form, not truth.
