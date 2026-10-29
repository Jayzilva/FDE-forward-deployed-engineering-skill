# Phase 3 — Prototype

Core question: **Will the client recognise their problem being solved, before we write production code?**

A clickable prototype on believable data is the fastest way to find wrong requirements. It costs days. A wrong build costs weeks. This phase sits between Scope and Build: scope says what to close, the prototype lets the client react, and only then does a spec go to build.

## Inputs

- Gap matrix and requirement IDs from Scope.
- The existing prototype or product UI, if any (`starting-points.md#prototype-exists`).
- A named client person who will react to it (the champion or a real user).

## Steps

1. **Scope the prototype** with `templates/mock-scope.md`. One journey per persona, each answering one question the persona asks ("Is this project making money?"). List what is out of scope.
2. **Version it separately.** Keep v1 exactly as the client last saw it. Build vN in its own folder from v1 plus patches and new screens. Generate the page with a build script; never hand-edit the output. The diff between versions is then reviewable.
3. **Reuse the existing design system.** New screens use the same cards, tables, chips and charts. A prototype that looks bolted-on makes the client doubt the product.
4. **Mark what is new.** Put a small "New in vN" badge on each new screen and changed card. Reviewers can then see the delta at a glance.
5. **Use fictional but consistent data.** Numbers must add up across screens (contract value = invoiced + upcoming; costs split to the total). Inconsistent demo numbers derail the meeting. State that all data is fictional.
6. **Show the hard parts, not only the happy path.** Include one item that needs review, one item blocked by a dependency, one over-budget row. Clients trust a prototype that admits friction.
7. **Add FSPARK** to the prototype (see below and `fspark.md`) and share it with the channel that fits the audience.
8. **Write a guided tour document** (`scripts/capture_screens.py` then `scripts/build_tour.py`): annotated screenshots, what each control does, and the open gaps per screen. People new to the system read it before the session.
9. **Check it renders.** Open every screen in a headless browser, light and dark, desktop and phone width. Fix script errors and overflow before the client sees it.
10. **Run the client session.** Walk the journeys in order. Record each reaction as: confirms, changes, new requirement, out of scope. Update the requirement IDs, not the prototype notes.
11. **Loop.** Change the prototype, bump the version, repeat. Stop when the client confirms the journeys and no new "must" appears in a session.
12. **Freeze and hand to Build.** The confirmed prototype becomes the acceptance mock for each spec change.

## FSPARK: show the prototype and gather feedback

Add **FSPARK** (Feedback-based Spotlight Presentation, Assessment, Response & Knowledge) to the prototype. A spotlight tour presents each new feature, the viewer rates it and adds a note, and the tour returns a Markdown feedback file. Merge the files from all reviewers and answer each row before the next version. Full method, sharing rules and measures: `fspark.md`.

## Prototype patterns

| Need | Pattern |
|---|---|
| Show a second audience (client vs internal) | A preview mode drawn over the app with its own header and a banner that says what is hidden |
| Show money in several currencies | A header switcher. Each amount shows its rate, date and source |
| Show agent work | A chip naming the agent and the person it acts for. A queue of drafts waiting for approval |
| Show a process | A stepper with done, now and next states |
| Show a decision | Options with their effect on the metric the persona cares about (for example margin) |

## Exit criteria

- The client named in the scope walked every journey.
- Each reaction is filed as a requirement change.
- The prototype version and its build script are committed.
- The client agreed which journeys go to Build first.

## Failure modes

- Building the prototype on real production data before a data agreement exists.
- Polishing visuals while a journey is still wrong.
- Letting the prototype become the product: no tests, no auth, shipped "temporarily".
- Showing only the internal view when the client's own users will use it.
