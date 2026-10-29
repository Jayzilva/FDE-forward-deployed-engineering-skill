#!/usr/bin/env python3
"""Check FDE evidence records: value ledger, decision log, stakeholder signals, commitments.

Reads Markdown files (a folder or file list) and reports:
  - value-ledger rows that are accepted, and claims with the rule each one fails
  - decision lines with or without an [approved: Name YYYY-MM-DD] stamp
  - stakeholder signals [signal:green|amber|red YYYY-MM-DD], stale after 21 days
  - open commitments and questions (- [ ] ... due: YYYY-MM-DD) past their date

It checks recorded fields only. It cannot verify that a client really consented.

Usage:
  python evidence_check.py fde/                       # report
  python evidence_check.py fde/ --json                # machine-readable
  python evidence_check.py fde/ --strict              # exit 1 if any claim or overdue item
  python evidence_check.py --export fde/readout.md    # print with <private> blocks redacted
  python evidence_check.py fde/ --today 2026-11-20    # fixed date for tests
"""
import argparse, datetime as dt, json, pathlib, re, sys

DATE = r"\d{4}-\d{2}-\d{2}"
NOT_A_NAME = {"approved", "accepted", "customer", "client", "sponsor", "pending", "tbd", "yes", "ok",
              "signed", "agreed", "team", "owner", "stakeholder", "the", "n/a", "-", "none", "lead"}
EMPTY = {"", "-", "—", "pending", "tbd", "n/a", "none", "?"}
SOURCE = re.compile(r"(PR\s*#\d+|https?://\S+|transcript:\S+|\[source:[^\]]+\]|\b[A-Z][A-Z0-9]+-\d+\b|[\w.-]+/[\w./-]+\.\w+)")
BAD_SOURCE = re.compile(r"^\s*(pending|staging run|local run|tbd|-|—)\b", re.I)
PRIVATE = re.compile(r"<private>.*?</private>", re.S | re.I)
SIGNAL = re.compile(r"\[signal:(green|amber|red)\s+(" + DATE + r")\]", re.I)
APPROVED = re.compile(r"\[approved:\s*([^\]]+?)\s+(" + DATE + r")\]")
OPEN_ITEM = re.compile(r"^\s*-\s*\[ \]\s*(.+)$")
DUE = re.compile(r"due:\s*(" + DATE + ")")
DECISION_LINE = re.compile(r"^\s*-\s*(" + DATE + r")\s+(.+)$")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_placeholder(row):
    return any("<" in c and ">" in c for c in row)


def signer_ok(text):
    m = re.match(r"^\s*([^,]+?)\s*,\s*.*?(" + DATE + ")", text or "")
    if not m:
        return False
    words = [w.lower().strip(".") for w in m.group(1).split()]
    return bool(words) and not all(w in NOT_A_NAME for w in words) and any(ch.isupper() for ch in m.group(1))


def check_row(head, row):
    col = {h.lower(): i for i, h in enumerate(head)}
    get = lambda k: row[col[k]] if k in col and col[k] < len(row) else ""
    fails = []
    if get("measured").lower() in EMPTY:
        fails.append("measured is empty or pending")
    if not signer_ok(get("accepted by")):
        fails.append("accepted by needs a client-side name, then a date")
    if "acceptance status" in col and get("acceptance status").lower() != "accepted":
        fails.append(f"acceptance status is '{get('acceptance status') or 'empty'}'")
    ev = get("evidence")
    if not ev or BAD_SOURCE.match(ev) or not SOURCE.search(ev):
        fails.append("evidence needs a source others can open")
    return fails


def scan(files, today):
    out = {"accepted": [], "claims": [], "decisions_approved": [], "decisions_unconfirmed": [],
           "signals": [], "overdue": [], "open_items": 0}
    for f in files:
        text = PRIVATE.sub("[private]", f.read_text(encoding="utf-8", errors="replace"))
        lines = text.splitlines()
        is_decisions = "decision" in f.name.lower()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
                head = cells(line)
                lower = [h.lower() for h in head]
                i += 2
                while i < len(lines) and lines[i].strip().startswith("|"):
                    row = cells(lines[i])
                    if "accepted by" in lower and "measured" in lower and not is_placeholder(row) and any(row):
                        label = row[lower.index("promised")] if "promised" in lower else row[0]
                        fails = check_row(head, row)
                        item = {"file": f.name, "outcome": label}
                        (out["claims"] if fails else out["accepted"]).append({**item, "fails": fails} if fails else item)
                    i += 1
                continue
            m = DECISION_LINE.match(line)
            if m and is_decisions and "<" not in line:
                a = APPROVED.search(line)
                if a and signer_ok(f"{a.group(1)}, {a.group(2)}"):
                    out["decisions_approved"].append({"file": f.name, "date": m.group(1), "by": a.group(1), "text": m.group(2)[:90]})
                else:
                    out["decisions_unconfirmed"].append({"file": f.name, "date": m.group(1), "text": m.group(2)[:90]})
            for s in SIGNAL.finditer(line):
                if "<" in line:
                    continue
                who = re.sub(r"^\s*[-*]\s*", "", line[:s.start()]).strip(" :—-") or "?"
                age = (today - dt.date.fromisoformat(s.group(2))).days
                out["signals"].append({"file": f.name, "who": who[:40], "signal": s.group(1).lower(),
                                       "date": s.group(2), "stale": age > 21})
            o = OPEN_ITEM.match(line)
            if o and "<" not in line:
                out["open_items"] += 1
                d = DUE.search(line)
                if d and dt.date.fromisoformat(d.group(1)) < today:
                    out["overdue"].append({"file": f.name, "item": o.group(1)[:100], "due": d.group(1)})
            i += 1
    latest = {}
    for s in out["signals"]:
        if s["who"] not in latest or s["date"] > latest[s["who"]]["date"]:
            latest[s["who"]] = s
    out["signals"] = sorted(latest.values(), key=lambda s: s["who"])
    return out


def report(r):
    p = print
    p(f"VALUE LEDGER  accepted {len(r['accepted'])}  |  claims {len(r['claims'])}")
    for a in r["accepted"]:
        p(f"  ACCEPTED  {a['outcome']}  ({a['file']})")
    for c in r["claims"]:
        p(f"  CLAIM     {c['outcome']}  ({c['file']})")
        for f in c["fails"]:
            p(f"            - {f}")
    p(f"\nDECISIONS  client-approved {len(r['decisions_approved'])}  |  unconfirmed {len(r['decisions_unconfirmed'])}")
    for d in r["decisions_unconfirmed"]:
        p(f"  (unconfirmed) {d['date']} {d['text']}")
    p(f"\nSTAKEHOLDER SIGNALS  {len(r['signals'])}")
    for s in r["signals"]:
        p(f"  {s['signal'].upper():5}  {s['who']}  {s['date']}{'  STALE (>21 days)' if s['stale'] else ''}")
    p(f"\nOPEN ITEMS  {r['open_items']}  |  overdue {len(r['overdue'])}")
    for o in r["overdue"]:
        p(f"  OVERDUE {o['due']}  {o['item']}  ({o['file']})")
    p("\nRecorded fields only. A recorded acceptance is not proof the client consented.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", help="folders or Markdown files")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if claims or overdue items exist")
    ap.add_argument("--export", metavar="FILE", help="print FILE with <private> blocks redacted")
    ap.add_argument("--today", help="YYYY-MM-DD (default: today)")
    a = ap.parse_args()
    if a.export:
        sys.stdout.write(PRIVATE.sub("[private]", pathlib.Path(a.export).read_text(encoding="utf-8")))
        return 0
    if not a.paths:
        ap.error("give a folder or Markdown files")
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    files = []
    for p in map(pathlib.Path, a.paths):
        files += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    r = scan(files, today)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        report(r)
    return 1 if a.strict and (r["claims"] or r["overdue"]) else 0


if __name__ == "__main__":
    sys.exit(main())
