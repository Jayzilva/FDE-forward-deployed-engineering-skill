#!/usr/bin/env python3
"""Build a guided tour page of a prototype: annotated screenshots, what each
control does, and the gaps on each screen. Stdlib only.

Inputs (in one folder, usually the --out of capture_screens.py):
  els.json      element boxes from capture_screens.py
  img/*.jpg     screenshots from capture_screens.py
  tour.json     the content you write (schema below)

Usage:
  build_tour.py DIR            -> writes DIR/index.html
  build_tour.py --example      -> prints an example tour.json

tour.json:
{
  "title": "Acme Portal Tour",
  "subtitle": "Prototype v1 · 2026-11-02",
  "headline": "What is in the prototype, and what it still needs",
  "intro": "One paragraph for someone new to the system.",
  "missing_intro": "Screens the prototype does not have yet.",
  "levels": {"demo": "Before client demo", "next": "Next wave", "later": "Later"},
  "screens": [
    {"id": "<route from els.json>", "group": "Start here", "name": "Overview",
     "roles": "Everyone", "purpose": "What the screen is for.",
     "spots": [["<text the control starts with, or exact text ending in $>", "Label", "What it does."]],
     "gaps":  [["demo|next|later", "What is missing.", "REQ-ID"]],
     "keep":  ["What works and must stay."]}
  ],
  "missing": [["Screen name", "demo|next|later", "What it would do.", "Who does it well today", "REQ-ID"]]
}
A spot is matched to the first captured element whose text starts with the
match string (or equals it, when the string ends in "$"). Elements in the
left 130 px (a side menu) lose to content elements with the same text.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "tour" / "template.html"
EXAMPLE = {
    "title": "Acme Portal Tour", "subtitle": "Prototype v1", "headline": "What is in the prototype, and what it still needs",
    "intro": "This page walks through the prototype one screen at a time. Numbers mark what each control does. Notes list the gaps.",
    "missing_intro": "These screens do not exist yet. Each one closes a gap.",
    "levels": {"demo": "Before client demo", "next": "Next wave", "later": "Later"},
    "screens": [{"id": "home", "group": "Start here", "name": "Overview", "roles": "Everyone",
                 "purpose": "The home page.", "spots": [["Search", "Search", "Finds records anywhere."]],
                 "gaps": [["demo", "No cost or margin view.", "FIN-03"]], "keep": ["Clear weekly summary."]}],
    "missing": [["Client portal", "demo", "Clients see status and approve releases.", "Vendor X", "POR-01"]],
}


def hit(text, match):
    return text == match[:-1] if match.endswith("$") else text.startswith(match)


def find(els, match, sid):
    for e in els:
        if e["x"] >= 130 and hit(e["t"], match) and e["y"] >= 40:
            return e
    for e in els:
        if hit(e["t"], match):
            return e
    raise SystemExit(f"Screen '{sid}': no element starts with '{match}'. Check els.json for the exact text.")


def build(folder):
    folder = pathlib.Path(folder)
    spec = json.loads((folder / "tour.json").read_text(encoding="utf-8"))
    els = json.loads((folder / "els.json").read_text(encoding="utf-8"))
    levels = {"demo": "Before client demo", "next": "Next wave", "later": "Later", **spec.get("levels", {})}
    screens = []
    for s in spec["screens"]:
        cap = els.get(s["id"]) or sys.exit(f"Screen '{s['id']}' is not in els.json")
        W, H = cap.get("w", 1440), cap["h"]
        spots = []
        for n, (match, label, desc) in enumerate(s.get("spots", []), 1):
            e = find(cap["els"], match, s["id"])
            w = min(e["w"], W - e["x"]); h = min(e["h"], H - e["y"])
            spots.append({"n": n, "label": label, "desc": desc, "x": round(e["x"] / W * 100, 2), "y": round(e["y"] / H * 100, 2),
                          "w": round(w / W * 100, 2), "h": round(h / H * 100, 2)})
        screens.append({"id": s["id"], "group": s.get("group", "Screens"), "name": s["name"], "roles": s.get("roles", "Everyone"),
                        "purpose": s.get("purpose", ""), "img": cap.get("img", f"img/{s['id']}.jpg"), "ratio": round(H / W, 4),
                        "spots": spots, "gaps": [{"level": l, "text": t, "req": q} for l, t, q in s.get("gaps", [])],
                        "keep": s.get("keep", [])})
    missing = [{"name": n, "level": l, "text": t, "ref": r, "req": q} for n, l, t, r, q in spec.get("missing", [])]
    html = TEMPLATE.read_text(encoding="utf-8")
    for k, v in {"{{TITLE}}": spec.get("title", "Prototype Tour"), "{{SUBTITLE}}": spec.get("subtitle", ""),
                 "{{HEADLINE}}": spec.get("headline", ""), "{{INTRO}}": spec.get("intro", ""),
                 "{{MISSING_INTRO}}": spec.get("missing_intro", ""), "{{L_DEMO}}": levels["demo"],
                 "{{L_NEXT}}": levels["next"], "{{L_LATER}}": levels["later"]}.items():
        html = html.replace(k, v.replace("<", "&lt;"))
    html = html.replace("/*DATA*/", "const SCREENS=" + json.dumps(screens, ensure_ascii=False) + ";\nconst MISSING=" +
                        json.dumps(missing, ensure_ascii=False) + ";\nconst LEVELS=" + json.dumps(levels) + ";")
    (folder / "index.html").write_text(html, encoding="utf-8")
    print(f"{folder / 'index.html'}: {len(screens)} screens, {sum(len(s['spots']) for s in screens)} spots, "
          f"{sum(len(s['gaps']) for s in screens) + len(missing)} gaps")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2))
    else:
        build(sys.argv[1])
