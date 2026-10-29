# Assumptions: find them, rank them, test them

Every engagement rests on assumptions. Most stay invisible until one is wrong and the build is two weeks deep. This method makes them visible and testable before they cost time. Use it in Discover and Scope. Use it when a brief feels too neat, or when the client is certain about the solution but vague about the problem. Use it when what people said contradicts what the system shows.

## 1. Extract

Read the brief, the discovery notes, the system map and the requirements line by line. Every statement without evidence is an assumption. Look in these places first:

| Where it hides | Example | The real question |
|---|---|---|
| The problem | "Approvals are slow" | Slow for whom? Measured how? Since when? |
| The solution | "We need an AI agent" | Is the bottleneck the work, or the hand-off between teams? |
| The timeline | "Six weeks is enough" | Who estimated? Based on what? Done this before? |
| The people | "Finance is on board" | Who in finance? Asked when? What did the sceptic say? |
| The data | "Our data is clean" | Defined how? Sampled when? By whom? |
| The system | "The API supports it" | Which version? Tested in their environment? Rate limits? |
| The word "just" | "We just need a button" | On which system? What breaks? Who maintains it? |
| The convention | "We always reconcile monthly" | Is it a rule, a regulation or a habit? |

## 2. Classify

For each assumption record:

- **Kind**: `FACT` (checkable, true or false today), `CONVENTION` (a habit that looks like a rule), `UNKNOWN` (nobody knows yet).
- **Status**: `OPEN`, `CONFIRMED`, `DISPROVED`.
- **Blast radius**: what fails if it is wrong. `critical` (the outcome or the date fails), `major` (a slice must change), `minor`.
- **Source**: who said it and when, or "stated, unverified".

A convention is the most valuable kind to find. If nobody can name the rule behind it, the client may drop it, and the scope shrinks.

## 3. Rank

Test first what is critical and cheapest to check. Leave minor assumptions open and note them.

| | Cheap to test | Expensive to test |
|---|---|---|
| Critical | Test this week | Design a small spike or prototype |
| Major | Test before the slice starts | Note it as a risk with an owner |
| Minor | Test when convenient | Leave open, note it |

## 4. Test

Pick the smallest test that changes a decision:

- Ask the person who owns the fact, with a specific question.
- Pull a sample: twenty real records beat an opinion about the data.
- Run the system: call the API in their environment, open the legacy screen.
- Time the task: watch one person do it end to end.
- Build a throwaway: a prototype or FSPARK stop that shows the assumed workflow.

Write the result and the date. A disproved critical assumption is good news found early. Tell the sponsor the same day, with what changes.

## Output

`assets/templates/assumptions-register.md`. Promote each confirmed critical assumption to a requirement, a risk or a decision. Store the register with the engagement records. Re-check open critical items before each gate.

## Red-team pass

Before a consequential decision, take the opposing side for ten minutes:

1. List the three claims the plan depends on most.
2. For each, ask "what evidence would prove this wrong?" and "have we looked for it?".
3. Name the most likely way the plan fails in the next month.
4. Write one corrective action per weak claim, with an owner.

Use `/fde:premortem` for a full health check against known failure modes.
