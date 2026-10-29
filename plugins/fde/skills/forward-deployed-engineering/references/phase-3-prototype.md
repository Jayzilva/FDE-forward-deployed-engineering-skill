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
7. **Add a spotlight tour** to the prototype (see below) and share it with the channel that fits the audience.
8. **Write a guided tour document** (`scripts/capture_screens.py` then `scripts/build_tour.py`): annotated screenshots, what each control does, and the open gaps per screen. People new to the system read it before the session.
9. **Check it renders.** Open every screen in a headless browser, light and dark, desktop and phone width. Fix script errors and overflow before the client sees it.
10. **Run the client session.** Walk the journeys in order. Record each reaction as: confirms, changes, new requirement, out of scope. Update the requirement IDs, not the prototype notes.
11. **Loop.** Change the prototype, bump the version, repeat. Stop when the client confirms the journeys and no new "must" appears in a session.
12. **Freeze and hand to Build.** The confirmed prototype becomes the acceptance mock for each spec change.

## Guided spotlight tour inside the prototype

A static tour document explains a prototype. A **spotlight tour inside the prototype** lets the client use it. Each stop opens the right screen, highlights one new feature, explains it in plain words, and lets the viewer leave a note. At the end the viewer copies all notes and sends them back. This gives the client a clear picture of what will be built, and gives you their reactions stop by stop.

1. Add `data-tour="<name>"` to each element a stop points at. Selectors on classes break when the design changes.
2. Write `steps.json`: title, intro, outro, and one stop per new feature (screen, target, title, body, requirement tag). Run `scripts/add_spotlight.py --example` for the schema. Keep each body to one or two sentences. End with a "your turn" stop that asks for notes.
3. Run `scripts/add_spotlight.py prototype.html steps.json --out index.html`. The output is one self-contained file.
4. Walk every stop headless (desktop and phone). Each stop must find its target.

### Share it with the right audience

| Audience | Channel | How feedback comes back |
|---|---|---|
| Inside your organisation, uses Claude | Publish as a Claude artifact shared with the organisation | Comments on the artifact, plus the copied notes |
| Outside, and your organisation allows public links | Publish the artifact with "anyone with the link" | Copied notes in a reply. Invite named people if they should comment |
| Outside, no Claude access, or public links not allowed | Send the single HTML file (email, client portal, file share). It works offline and makes no external calls | "Copy my notes" pasted into a reply |
| Regulated client or confidential context | Single HTML file through the client's approved channel only. Never a public link | As above. Store replies with the engagement records |

Rules: every number in a shared prototype is sample data and says so. Never publish client data or client names on a public link. Decide the channel with the sponsor before sending.

### Close the loop

File each note as one of: confirms, change, new requirement, out of scope. Update the requirement IDs, bump the prototype version, regenerate the tour, and send the new version with a one-line summary of what changed because of their notes. Clients engage more when they see their notes acted on.

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
