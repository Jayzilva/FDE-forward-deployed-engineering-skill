#!/usr/bin/env python3
"""Merge FSPARK feedback files from many reviewers into one summary. Stdlib only.

Usage:
  merge_feedback.py FEEDBACK.md [FEEDBACK.md ...] --out SUMMARY.md

Reads the "Feedback by feature" sections and the closing questions of each file
and writes one table per feature (reaction counts, every note with its reviewer),
the closing answers, and an open-response table for the delivery team.
"""
import pathlib, re, sys
from collections import OrderedDict


def parse(text):
    reviewer = re.search(r"\*\*Reviewer:\*\*\s*(.+)", text)
    reviewer = reviewer.group(1).strip() if reviewer else "Unknown"
    feats, answers = OrderedDict(), OrderedDict()
    body = text.split("## Feedback by feature", 1)[-1]
    for m in re.finditer(r"^### \d+\.\s*(.+?)\n(.*?)(?=^### |^## |\Z)", body, re.S | re.M):
        title, block = m.group(1).strip(), m.group(2)
        g = lambda k: (re.search(rf"\*\*{k}:\*\*\s*(.+)", block) or [None, ""])[1].strip()
        feats[title] = {"req": g("Requirement"), "reaction": g("Reaction") or "Not reviewed", "note": g("Note")}
    for m in re.finditer(r"^## (.+?)\n+(.*?)(?=^## |\Z)", text, re.S | re.M):
        h = m.group(1).strip()
        if h in ("Summary", "Feedback by feature", "Delivery team response"):
            continue
        a = m.group(2).strip()
        if a and a != "—":
            answers[h] = a
    return reviewer, feats, answers


def main():
    args = sys.argv[1:]
    if "--out" not in args or args.index("--out") == 0:
        sys.exit(__doc__)
    k = args.index("--out"); files, out = args[:k], pathlib.Path(args[k + 1])
    features, closing, n = OrderedDict(), OrderedDict(), 0
    for f in files:
        reviewer, feats, answers = parse(pathlib.Path(f).read_text(encoding="utf-8")); n += 1
        for title, d in feats.items():
            e = features.setdefault(title, {"req": d["req"], "counts": {}, "notes": []})
            e["counts"][d["reaction"]] = e["counts"].get(d["reaction"], 0) + 1
            if d["note"] and d["note"] != "—":
                e["notes"].append(f"{d['note']} ({reviewer}, {d['reaction'].lower()})")
        for q, a in answers.items():
            closing.setdefault(q, []).append(f"{a} ({reviewer})")
    reactions = ["Looks right", "Needs changes", "Not needed", "Not sure", "Not reviewed"]
    L = [f"# Feedback summary: {n} reviewer(s)", "", "| # | Feature | Requirement | " + " | ".join(reactions) + " |", "|---|---|---|" + "---|" * len(reactions)]
    for i, (t, e) in enumerate(features.items(), 1):
        L.append(f"| {i} | {t} | {e['req'] or '—'} | " + " | ".join(str(e["counts"].get(r, 0)) for r in reactions) + " |")
    L += ["", "## Notes by feature", ""]
    for i, (t, e) in enumerate(features.items(), 1):
        if e["notes"]:
            L += [f"### {i}. {t}", ""] + [f"- {x}" for x in e["notes"]] + [""]
    for q, items in closing.items():
        L += [f"## {q}", ""] + [f"- {x}" for x in items] + [""]
    L += ["## Delivery team response", "", "| # | Feature | Signal | Decision (confirms / change / new requirement / out of scope) | Requirement ID | Status |", "|---|---|---|---|---|---|"]
    for i, (t, e) in enumerate(features.items(), 1):
        c = e["counts"]; signal = ", ".join(f"{c[r]} {r.lower()}" for r in reactions[1:4] if c.get(r))
        if signal or e["notes"]:
            L.append(f"| {i} | {t} | {signal or 'notes only'} |  | {e['req'] or ''} | Open |")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{out}: {n} file(s), {len(features)} features")


if __name__ == "__main__":
    main()
