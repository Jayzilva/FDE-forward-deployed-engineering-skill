---
description: Run a pre-mortem or health check on the engagement against known FDE failure modes
argument-hint: "[what is going on]"
allowed-tools: Read, Write, Bash, Agent
---
Use the forward-deployed-engineering skill. Load state. Delegate to the `engagement-reviewer` agent with the state file, the `fde/` folder, and $ARGUMENTS. Then add the top risks to state with owners and print the FDE check block.
