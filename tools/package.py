#!/usr/bin/env python3
"""Validate the marketplace and plugin, run the script self-tests, and build
dist/forward-deployed-engineering.skill (a zip for claude.ai skill upload).

Run from the repo root:  python tools/package.py
"""
import json, os, pathlib, re, subprocess, sys, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "fde"
SKILL = PLUGIN / "skills" / "forward-deployed-engineering"
DIST = ROOT / "dist"
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
check(market["plugins"][0]["name"] == plugin["name"], "marketplace plugin name differs from plugin.json")
check(market["plugins"][0].get("version") == plugin["version"], "marketplace version differs from plugin.json")
check((ROOT / market["plugins"][0]["source"]).resolve() == PLUGIN.resolve(), "marketplace source path is wrong")

text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
fm = re.match(r"---\nname: (.+)\ndescription: \"(.+)\"\n---\n", text)
check(fm is not None, "SKILL.md frontmatter must have name and a quoted description")
if fm:
    check(fm.group(1) == SKILL.name, "skill name must match its folder")
    check(len(fm.group(2)) <= 1024, f"description is {len(fm.group(2))} chars (max 1024)")
check(len(text.splitlines()) < 500, "SKILL.md must stay under 500 lines")

# every referenced file exists
for ref in set(re.findall(r"`((?:references|assets/templates|scripts)/[\w./-]+\.(?:md|py))", text)):
    check((SKILL / ref).exists(), f"SKILL.md points to missing {ref}")
for name in re.findall(r"`([\w-]+\.md)`", text):
    if not any(SKILL.rglob(name)):
        errors.append(f"SKILL.md names {name}, which does not exist")
for md in list((PLUGIN / "commands").glob("*.md")) + list((PLUGIN / "agents").glob("*.md")):
    head = md.read_text(encoding="utf-8").split("---")
    check(len(head) >= 3 and "description:" in head[1], f"{md.name}: missing frontmatter description")

# script self-tests
with tempfile.TemporaryDirectory() as tmp:
    st = [sys.executable, str(SKILL / "scripts" / "fde_state.py")]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    run = lambda *a: subprocess.run(list(a), cwd=tmp, capture_output=True, text=True, encoding="utf-8", env=env)
    r = run(*st, "init", "--client", "T", "--engagement", "E", "--model", "programme", "--start", "prototype-exists", "--style", "spec-driven")
    check(r.returncode == 0, "fde_state init failed: " + r.stderr)
    r = run(*st, "add-gate", "2026-10-31", "Gate")
    check("WEEKEND" in r.stdout, "fde_state did not flag a Saturday gate")
    r = run(*st, "set", "start", "nonsense")
    check(r.returncode != 0, "fde_state accepted an invalid starting point")
    cases = pathlib.Path(tmp) / "cases.json"
    cases.write_text(json.dumps([{"name": "a", "volume": 4, "complexity": 3, "measurability": 4, "readiness": 4}]))
    r = run(sys.executable, str(SKILL / "scripts" / "qualify.py"), str(cases))
    check(r.returncode == 0, "qualify.py failed: " + r.stderr)
    r = run(sys.executable, str(SKILL / "scripts" / "build_tour.py"), "--example")
    check(r.returncode == 0 and json.loads(r.stdout)["screens"], "build_tour.py --example failed")
    r = run(sys.executable, str(SKILL / "scripts" / "ste_lint.py"), str(SKILL / "assets" / "templates" / "handoff-runbook.md"))
    check(r.returncode == 0, "handoff-runbook template has hard STE violations:\n" + r.stdout[-800:])

if errors:
    print("FAILED:\n  " + "\n  ".join(errors))
    sys.exit(1)

DIST.mkdir(exist_ok=True)
out = DIST / f"{SKILL.name}.skill"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SKILL.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts and not f.name.endswith(".pyc"):
            z.write(f, f"{SKILL.name}/{f.relative_to(SKILL).as_posix()}")
print(f"OK  plugin {plugin['name']} {plugin['version']}  ->  {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
