#!/usr/bin/env python3
"""Add a guided spotlight tour to an HTML prototype. Stdlib only.

The tour walks the viewer through new features one stop at a time: it switches
screen, spotlights one element, explains it, and lets the viewer leave a note.
At the end the viewer copies all notes and sends them back. The result is one
self-contained HTML file: no external requests, works offline, safe to email.

Usage:
  add_spotlight.py PAGE.html STEPS.json --out OUT.html
  add_spotlight.py --example            -> prints an example STEPS.json

STEPS.json:
{
  "title": "What is new in v2",
  "kicker": "Prototype v2",
  "intro": "Eight stops, about three minutes. Every number is sample data.",
  "launchLabel": "What is new",
  "storageKey": "acme-portal-v2",
  "feedback": true,
  "autoStart": true,
  "outro": "Copy your notes and send them to your delivery lead.",
  "steps": [
    {"screen": "billing", "target": "[data-tour='drafts']",
     "title": "Invoice drafts", "body": "The agent drafts invoices. Finance approves.", "tag": "FIN-05"}
  ]
}
"screen" is optional: the location.hash the prototype uses for that view.
"target" is a CSS selector. Prefer data-tour="..." attributes you add to the
prototype, so the tour does not break when classes change.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets" / "spotlight"
EXAMPLE = {
    "title": "What is new in v2", "kicker": "Prototype v2",
    "intro": "Eight stops, about three minutes. Every number is sample data.",
    "launchLabel": "What is new", "storageKey": "acme-portal-v2", "feedback": True, "autoStart": True,
    "outro": "Copy your notes and send them to your delivery lead.",
    "steps": [{"screen": "billing", "target": "[data-tour='drafts']", "title": "Invoice drafts",
               "body": "The agent drafts invoices from approved time. Finance approves each one.", "tag": "FIN-05"}],
}


def inject(page: str, config: dict) -> str:
    for key in ("title", "steps"):
        if key not in config:
            raise SystemExit(f"STEPS.json needs '{key}'")
    for n, s in enumerate(config["steps"], 1):
        missing = [k for k in ("target", "title", "body") if not s.get(k)]
        if missing:
            raise SystemExit(f"step {n} is missing {', '.join(missing)}")
    if 'id="fde-tour"' in page:
        raise SystemExit("The page already has a spotlight tour. Edit its config instead.")
    css = (ASSETS / "spotlight.css").read_text(encoding="utf-8")
    js = (ASSETS / "spotlight.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    cfg = json.dumps(config, ensure_ascii=False).replace("</", "<\\/")
    style = f"<style id=\"fde-tour-style\">\n{css}</style>\n"
    tail = f"<script type=\"application/json\" id=\"fde-tour\">{cfg}</script>\n<script>\n{js}</script>\n"
    low = page.lower()
    i = low.rfind("</head>")
    page = page[:i] + style + page[i:] if i != -1 else style + page
    low = page.lower()
    j = low.rfind("</body>")
    return page[:j] + tail + page[j:] if j != -1 else page + "\n" + tail


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2)); return
    if len(sys.argv) != 5 or sys.argv[3] != "--out":
        sys.exit(__doc__)
    page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    config = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[4])
    out.write_text(inject(page, config), encoding="utf-8")
    print(f"{out}: {len(config['steps'])} stops added. Open it, click the launch button, and walk every stop.")


if __name__ == "__main__":
    main()
