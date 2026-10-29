# FSPARK — Feedback-based Spotlight Presentation, Assessment, Response & Knowledge

FSPARK turns a prototype into a structured conversation with the people who will use it. It shows them what was built, asks what they think of each feature, and returns their answers as a Markdown file you can act on. Use it in Phase 3 (Prototype) and at every demo where you need reactions, not applause.

| Letter | Step | What happens | Output |
|---|---|---|---|
| P | Presentation | A spotlight tour opens each screen, highlights one feature and explains it in one or two sentences | The viewer sees exactly what is new |
| A | Assessment | The viewer picks a reaction on each feature: looks right, needs changes, not needed, not sure | A count per feature |
| R | Response | The viewer adds a note per feature and answers two closing questions | Their words, tied to a feature and a requirement ID |
| K | Knowledge | The tour builds a Markdown file the viewer previews, edits, downloads or copies | A feedback file with a team-response table |

## Build it

1. Mark each feature the tour points at with `data-tour="<name>"`. Selectors on classes break when the design changes.
2. Write `config.json` next to the prototype. `scripts/add_fspark.py --example` prints the schema. Per stop: `screen` (the hash the prototype uses), `target`, `title`, `body` (one or two plain sentences), `tag` (requirement ID). Set `product`, `prototypeUrl`, `fileName`, and `mount` (where an always-visible launch button goes, for example the top bar).
3. Run `scripts/add_fspark.py prototype.html config.json --out index.html`. The output is one self-contained file.
4. Walk every stop headless at desktop and phone width, through to the downloaded file. Each stop must find its target.

Write stop text in plain words. Name the benefit, not the widget: "Completed jobs become invoice drafts. A draft that needs a person says why." End with a "your turn" stop.

## Share it

| Audience | Channel | Notes |
|---|---|---|
| Inside your organisation | Claude artifact shared with the organisation | Publish with capabilities `{"downloads": true}`. The viewer confirms each save |
| Outside, public links allowed | Claude artifact with "anyone with the link" | Same capability. Viewers without Claude use Copy text |
| Outside, no Claude access | The single HTML file by email, portal or file share | Downloads directly. Works offline |
| Regulated or confidential | The single HTML file through the client's approved channel only | Never a public link |

Every number in a shared prototype is sample data and says so. Answers stay in the viewer's browser until they download or copy the file. Decide the channel with the sponsor before sending.

Some viewers size the frame to the whole page. FSPARK measures the visible part of the page and places its cards there, and the `mount` button keeps the tour reachable. Test inside the real viewer before a client session.

## Close the loop

1. Collect the files. Merge them: `scripts/merge_feedback.py *.md --out feedback-summary.md`. The summary counts reactions per feature, lists every note with its reviewer, and ends with a delivery-team response table.
2. For each row, decide: confirms, change, new requirement, out of scope. Update the requirement IDs (`delivery-style.md`).
3. Fill the "Team response" column and send it back with the next prototype version. Say what changed because of their notes.
4. A reaction is an opinion on a prototype. "Looks right" is not acceptance of a delivered outcome. Record acceptance only in the value ledger (`evidence-ledger.md`).
5. Store the summaries in the knowledge base (`knowledge-base.md`). They are evidence for the gate review and the evaluation pack.

## Measures

| Measure | Use |
|---|---|
| Stops reviewed ÷ stops | Engagement with the prototype |
| "Needs changes" + "Not needed" per feature | Where to spend the next slice |
| "Not sure" per feature | Where the explanation, not the feature, needs work |
| Notes turned into requirement changes | How much the client shaped the build |
| Days from file received to team response | How fast the loop closes |
