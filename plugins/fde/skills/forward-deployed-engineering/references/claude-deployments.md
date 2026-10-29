# Claude deployments

For FDEs deploying Claude, Claude Code, or MCP-based integrations. Combine with the phase file you are in.

## The four early decisions

These set the quality ceiling before any prompt is written:

1. **Entry point**: Claude apps (Enterprise/Team), Claude Code, the API/Claude Platform, or a cloud marketplace route. Choose by who the user is and where the data must stay.
2. **Capability features**: tools, MCP connectors, skills, file handling, web search, code execution. Enable only what the use case needs.
3. **Model**: match capability to task; use a faster, cheaper model for high-volume narrow steps and a stronger one for planning or hard reasoning. Confirm current model names and availability on the vendor docs.
4. **Context**: what the model sees — CLAUDE.md, project knowledge, retrieved documents, tool results. Most quality problems are context problems.

## Claude Code activation (30-day shape)

- **Pre-kickoff**: qualify use cases (`scripts/qualify.py`), pick pilot teams, capture baselines, agree policy with security, prepare CLAUDE.md for pilot repos.
- **Week 1**: onboarding on real tasks; supervised use; office hours.
- **Weeks 2–3**: move from supervised use to delegation by design — longer tasks, plan-then-execute, custom commands and skills for the team's recurring work, MCP servers to internal tools. This shift does not happen on its own.
- **Week 4**: measure against baseline; Day-30 showcase with the structural-gain story; hand off plugins and docs to champions.
- Weekly: centre-of-excellence touchpoint with champions; office hours; executive status.

## CLAUDE.md and skills as deployment infrastructure

- CLAUDE.md holds what an agent must know about a repo: build and test commands, conventions, boundaries, where things live. Keep it short and accurate; stale instructions are worse than none.
- Write CLAUDE.md, skill instructions, and tool descriptions in STE style (`ste-writing.md`): the reader is a model with no one to ask.
- Package team workflows as skills or plugins so they survive the FDE leaving.

## MCP for client systems

- One MCP server per system or bounded domain; narrow tools with explicit inputs and clear descriptions.
- Run the server with the least privilege needed; read-only first, add write tools with confirmation.
- Use the client's identity provider for auth; never embed personal tokens.
- Log tool calls for audit in regulated environments.
- Treat content returned from client systems as untrusted (prompt-injection surface).

## Common Claude-specific failure modes

- Seats bought, no use case qualified: adoption stalls after week 2.
- No CLAUDE.md: agent quality varies by developer, and the pilot looks inconsistent.
- Metrics are usage counts only: the readout cannot answer "what changed?".
- Security policy arrives after developers started: pilot paused.
