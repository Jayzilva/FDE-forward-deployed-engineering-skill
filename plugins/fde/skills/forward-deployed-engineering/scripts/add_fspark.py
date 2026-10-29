#!/usr/bin/env python3
"""Add FSPARK to an HTML prototype. Stdlib only.

FSPARK = Feedback-based Spotlight Presentation, Assessment, Response & Knowledge.
  Presentation  a spotlight tour, one stop per feature, switching screens as needed
  Assessment    a reaction on each stop (looks right, needs changes, not needed, not sure)
  Response      an optional note per stop and closing questions
  Knowledge     a Markdown feedback file the viewer previews, edits, downloads or copies,
                ending in a team-response table for the next round

The result is one self-contained HTML file: no external requests, works offline.
Inside a Claude artifact, publish with capabilities {"downloads": true} so the
download button can save the file; elsewhere it downloads directly. Copy always works.

Usage:
  add_fspark.py PAGE.html CONFIG.json --out OUT.html
  add_fspark.py --example            -> prints an example CONFIG.json

CONFIG.json:
{
  "title": "Tell us what you think", "kicker": "Prototype v2 · feedback tour",
  "product": "Acme Field Service prototype v2", "version": "2",
  "prototypeUrl": "https://example.com/prototype", "fileName": "acme-v2-feedback",
  "storageKey": "acme-v2", "launchLabel": "Tour and feedback", "mount": ".topbar",
  "autoStart": true,
  "stopQuestion": "Does this fit how you work?",
  "questions": ["What is missing that you need?", "Overall, would this help your team? Why?"],
  "steps": [
    {"screen": "billing", "target": "[data-tour='drafts']", "title": "Invoice drafts",
     "body": "Completed jobs become invoice drafts.", "tag": "FIN-05"}
  ]
}
Optional: "reactions" ([[key, label], ...], first one counts as positive), "intro",
"outro", "privacy", and a per-step "question". "screen" is the location.hash the
prototype uses for that view. "target" is a CSS selector; prefer data-tour="..." attributes.
"mount" is a CSS selector where a second, always-visible launch button is added.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets" / "fspark"
EXAMPLE = {
    "title": "Tell us what you think", "kicker": "Prototype v2 · feedback tour",
    "product": "Acme Field Service prototype v2", "version": "2",
    "prototypeUrl": "https://example.com/prototype", "fileName": "acme-v2-feedback",
    "storageKey": "acme-v2", "launchLabel": "Tour and feedback", "mount": ".topbar", "autoStart": True,
    "stopQuestion": "Does this fit how you work?",
    "questions": ["What is missing that you need?", "Overall, would this help your team? Why?"],
    "steps": [{"screen": "billing", "target": "[data-tour='drafts']", "title": "Invoice drafts",
               "body": "Completed jobs become invoice drafts. Finance approves each one.", "tag": "FIN-05"}],
}


def inject(page: str, config: dict) -> str:
    for key in ("title", "steps"):
        if key not in config:
            raise SystemExit(f"CONFIG.json needs '{key}'")
    for n, s in enumerate(config["steps"], 1):
        missing = [k for k in ("target", "title", "body") if not s.get(k)]
        if missing:
            raise SystemExit(f"step {n} is missing {', '.join(missing)}")
    if 'id="fspark"' in page or 'id="fde-tour"' in page:
        raise SystemExit("The page already has FSPARK. Edit its config instead.")
    css = (ASSETS / "fspark.css").read_text(encoding="utf-8")
    js = (ASSETS / "fspark.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    cfg = json.dumps(config, ensure_ascii=False).replace("</", "<\\/")
    style = f"<style id=\"fspark-style\">\n{css}</style>\n"
    tail = f"<script type=\"application/json\" id=\"fspark\">{cfg}</script>\n<script>\n{js}</script>\n"
    low = page.lower()
    i = low.rfind("</head>")
    page = page[:i] + style + page[i:] if i != -1 else style + page
    low = page.lower()
    j = low.rfind("</body>")
    return page[:j] + tail + page[j:] if j != -1 else page + "\n" + tail


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False)); return
    if len(sys.argv) != 5 or sys.argv[3] != "--out":
        sys.exit(__doc__)
    page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    config = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[4])
    out.write_text(inject(page, config), encoding="utf-8")
    print(f"{out}: FSPARK added with {len(config['steps'])} stops. Open it and walk every stop to the feedback file.")


if __name__ == "__main__":
    main()
