#!/usr/bin/env python3
"""Engagement state for multi-week FDE work. Stdlib only.

State lives in .fde/engagement.yaml in the current directory. The file is
written as JSON, which is valid YAML, so no PyYAML is required. If the user
hand-edits it into block YAML and PyYAML is installed, it is still read.

Commands:
  init --client C --engagement E [--phase discover] [--env cloud] [--product ai-agent]
       [--model external] [--start greenfield] [--style classic]
  show
  set FIELD VALUE                      (client, engagement, phase, env, product, model, start,
                                        style, sponsor, champion, day2_owner, security_owner,
                                        readout_date, baseline_captured, system_of_record)
  add-risk TEXT [--owner O] [--impact H|M|L]
  close-risk ID
  add-decision TEXT                    (records a dated decision; link an ADR in the text)
  add-stakeholder NAME ROLE [--stance champion|neutral|blocker]
  add-gate DATE NAME                   (a dated checkpoint: readout, programme gate, demo)
  advance                              (move to the next phase)
  next                                 (gaps that block the current phase)
  calendar                             (list gates, flag weekend dates and gates in the past)
"""
import argparse, datetime, json, os, sys

PATH = os.path.join(".fde", "engagement.yaml")
PHASES = ["discover", "scope", "prototype", "build", "validate", "handoff"]
ENVS = ["cloud", "regulated", "on-prem", "air-gapped"]
PRODUCTS = ["ai-agent", "claude-code", "data-platform", "api-integration", "business-app"]
MODELS = ["external", "internal", "programme", "partner"]
STARTS = ["greenfield", "prototype-exists", "legacy-replace", "rescue", "scale-out"]
STYLES = ["classic", "spec-driven"]
FIELDS = ["client", "engagement", "phase", "env", "product", "model", "start", "style",
          "sponsor", "champion", "day2_owner", "security_owner", "readout_date",
          "baseline_captured", "system_of_record"]

# What must be true before leaving each phase. Kept short on purpose.
GATES = {
    "discover": [("sponsor", "Name the executive sponsor"),
                 ("day2_owner", "Name the Day-2 owner now, not in week 4"),
                 ("security_owner", "Name the client security/compliance owner")],
    "scope": [("readout_date", "Fix the readout date"),
              ("champion", "Name a champion")],
    "prototype": [("champion", "Name the client person who reacts to the prototype")],
    "build": [],
    "validate": [("baseline_captured", "Capture the baseline before Day 1 (set baseline_captured yes)")],
    "handoff": [],
}
ARTIFACTS = {
    "discover": "site-survey.md, discovery-questions.md, ecosystem-map.md, competitor-profile.md",
    "scope": "delta-map.md, gap-matrix.md, requirements.md, outcome-card.md, adr.md",
    "prototype": "mock-scope.md, the prototype as a separate version, guided tour (build_tour.py)",
    "build": "adr.md, risk-register.md",
    "validate": "pilot-plan.md, roi-scorecard.md, weekly-exec-status.md",
    "handoff": "handoff-runbook.md (STE-lint it), champion-plan.md",
}


def today():
    return datetime.date.today().isoformat()


def load():
    if not os.path.exists(PATH):
        sys.exit(f"No state at {PATH}. Run: fde_state.py init --client ... --engagement ...")
    raw = open(PATH, encoding="utf-8").read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            import yaml  # optional
            return yaml.safe_load(raw)
        except Exception as e:  # noqa: BLE001
            sys.exit(f"Cannot parse {PATH}: {e}")


def save(s):
    os.makedirs(".fde", exist_ok=True)
    s["updated"] = today()
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
        f.write("\n")


def check_choice(field, value):
    allowed = {"phase": PHASES, "env": ENVS, "product": PRODUCTS, "model": MODELS,
               "start": STARTS, "style": STYLES}.get(field)
    if allowed and value not in allowed:
        sys.exit(f"{field} must be one of: {', '.join(allowed)}")


def gaps(s):
    out = [msg for key, msg in GATES.get(s.get("phase"), []) if not s.get(key)]
    open_high = [r for r in s.get("risks", []) if r["status"] == "open" and r.get("impact") == "H" and not r.get("owner")]
    if open_high:
        out.append(f"{len(open_high)} high-impact risk(s) without an owner")
    if s.get("start") == "legacy-replace" and not s.get("system_of_record"):
        out.append("Legacy replacement: record which system is the system of record per domain")
    bad = [g for g in s.get("gates", []) if weekend(g["date"])]
    if bad:
        out.append(f"{len(bad)} gate(s) fall on a weekend: confirm the dates")
    if s.get("env") in ("regulated", "air-gapped") and not s.get("security_owner"):
        out = [x for x in out if "security/compliance owner" not in x]
        out.insert(0, "Regulated/air-gapped: name the security owner now; their review is a week-1 dependency")
    return out


def weekend(iso):
    try:
        return datetime.date.fromisoformat(iso).weekday() >= 5
    except ValueError:
        return False


def calendar(s):
    gates = sorted(s.get("gates", []), key=lambda g: g["date"])
    if not gates:
        print('No gates. Add one: fde_state.py add-gate 2026-11-13 "Demo 1"')
        return
    now = today()
    for g in gates:
        d = datetime.date.fromisoformat(g["date"])
        flags = []
        if d.weekday() >= 5:
            flags.append("WEEKEND")
        if g["date"] < now:
            flags.append("past")
        print(f"  {g['date']} {d.strftime('%a')}  {g['name']}" + (f"   ! {', '.join(flags)}" if flags else ""))


def show(s):
    print(f"{s.get('client','?')} — {s.get('engagement','?')}   (updated {s.get('updated','?')})")
    print(f"Situation: {s.get('phase')} / {s.get('env')} / {s.get('product')}")
    print(f"Engagement: {s.get('model', 'external')} / starts {s.get('start', 'greenfield')} / {s.get('style', 'classic')}")
    for k in ("sponsor", "champion", "day2_owner", "security_owner", "readout_date",
              "baseline_captured", "system_of_record"):
        print(f"  {k:<17} {s.get(k) or '—'}")
    if s.get("stakeholders"):
        print("Stakeholders:")
        for p in s["stakeholders"]:
            print(f"  - {p['name']} ({p['role']}, {p['stance']})")
    risks = [r for r in s.get("risks", []) if r["status"] == "open"]
    if risks:
        print("Open risks:")
        for r in risks:
            print(f"  R{r['id']} [{r.get('impact','?')}] {r['text']}  owner: {r.get('owner') or '—'}")
    if s.get("decisions"):
        print("Decisions:")
        for d in s["decisions"][-5:]:
            print(f"  {d['date']} {d['text']}")
    if s.get("gates"):
        print("Gates:")
        calendar(s)
    g = gaps(s)
    print("Gaps blocking this phase:" if g else "No gaps blocking this phase.")
    for x in g:
        print(f"  ! {x}")
    print(f"Phase artifacts: {ARTIFACTS.get(s.get('phase'), '—')}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--client", required=True); i.add_argument("--engagement", required=True)
    i.add_argument("--phase", default="discover"); i.add_argument("--env", default="cloud")
    i.add_argument("--product", default="ai-agent"); i.add_argument("--force", action="store_true")
    i.add_argument("--model", default="external"); i.add_argument("--start", default="greenfield")
    i.add_argument("--style", default="classic")
    sub.add_parser("show"); sub.add_parser("advance"); sub.add_parser("next"); sub.add_parser("calendar")
    ag = sub.add_parser("add-gate"); ag.add_argument("date"); ag.add_argument("name")
    st = sub.add_parser("set"); st.add_argument("field", choices=FIELDS); st.add_argument("value")
    ar = sub.add_parser("add-risk"); ar.add_argument("text"); ar.add_argument("--owner", default="")
    ar.add_argument("--impact", choices=["H", "M", "L"], default="M")
    cr = sub.add_parser("close-risk"); cr.add_argument("id", type=int)
    ad = sub.add_parser("add-decision"); ad.add_argument("text")
    ah = sub.add_parser("add-stakeholder"); ah.add_argument("name"); ah.add_argument("role")
    ah.add_argument("--stance", choices=["champion", "neutral", "blocker"], default="neutral")
    a = p.parse_args()

    if a.cmd == "init":
        if os.path.exists(PATH) and not a.force:
            sys.exit(f"{PATH} exists. Use --force to overwrite.")
        for f in ("phase", "env", "product", "model", "start", "style"):
            check_choice(f, getattr(a, f))
        s = {"client": a.client, "engagement": a.engagement, "phase": a.phase, "env": a.env,
             "product": a.product, "model": a.model, "start": a.start, "style": a.style,
             "created": today(), "stakeholders": [], "risks": [], "decisions": [], "gates": []}
        save(s); show(s); return

    s = load()
    if a.cmd == "show":
        show(s)
    elif a.cmd == "next":
        g = gaps(s)
        print("\n".join(f"! {x}" for x in g) if g else f"No blocking gaps. Produce: {ARTIFACTS[s['phase']]}")
    elif a.cmd == "set":
        check_choice(a.field, a.value); s[a.field] = a.value; save(s); print(f"{a.field} = {a.value}")
    elif a.cmd == "add-risk":
        rid = max([r["id"] for r in s["risks"]] or [0]) + 1
        s["risks"].append({"id": rid, "text": a.text, "owner": a.owner, "impact": a.impact,
                           "status": "open", "opened": today()})
        save(s); print(f"R{rid} added")
    elif a.cmd == "close-risk":
        for r in s["risks"]:
            if r["id"] == a.id:
                r["status"] = "closed"; r["closed"] = today(); save(s); print(f"R{a.id} closed"); return
        sys.exit(f"No risk R{a.id}")
    elif a.cmd == "add-decision":
        s["decisions"].append({"date": today(), "text": a.text}); save(s); print("Decision recorded")
    elif a.cmd == "calendar":
        calendar(s)
    elif a.cmd == "add-gate":
        try:
            datetime.date.fromisoformat(a.date)
        except ValueError:
            sys.exit("Date must be YYYY-MM-DD")
        s.setdefault("gates", []).append({"date": a.date, "name": a.name}); save(s)
        print(f"Gate {a.date} {a.name}" + ("   ! WEEKEND: confirm the date" if weekend(a.date) else ""))
    elif a.cmd == "add-stakeholder":
        s["stakeholders"].append({"name": a.name, "role": a.role, "stance": a.stance}); save(s)
        print(f"Added {a.name}")
    elif a.cmd == "advance":
        g = gaps(s)
        if g:
            print("Warning, advancing with open gaps:\n" + "\n".join(f"  ! {x}" for x in g))
        idx = PHASES.index(s["phase"])
        if idx == len(PHASES) - 1:
            sys.exit("Already in handoff, the last phase.")
        s["phase"] = PHASES[idx + 1]
        s["decisions"].append({"date": today(), "text": f"Advanced to {s['phase']}"})
        save(s); print(f"Phase -> {s['phase']}. Produce: {ARTIFACTS[s['phase']]}")


if __name__ == "__main__":
    main()
