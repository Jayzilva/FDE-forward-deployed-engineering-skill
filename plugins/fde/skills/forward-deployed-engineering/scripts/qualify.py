#!/usr/bin/env python3
"""Score and rank candidate FDE use cases. Stdlib only.

Criteria (1-5 each): volume, complexity, measurability, readiness.
Complexity scores best in the middle: too simple adds little value, too
complex will not finish in a pilot. Measurability and readiness are gates:
a score below 3 on either flags the use case as not pilot-ready.

Input: JSON file or stdin, a list of objects:
  [{"name": "...", "volume": 4, "complexity": 3, "measurability": 5,
    "readiness": 4, "structural": true, "note": "4 people x 6 wks -> 2 x 2"}]
Usage: python qualify.py cases.json [--json]
"""
import json, sys

COMPLEXITY_VALUE = {1: 1, 2: 3, 3: 5, 4: 4, 5: 2}


def score(c):
    for k in ("volume", "complexity", "measurability", "readiness"):
        v = c.get(k)
        if not isinstance(v, (int, float)) or not 1 <= v <= 5:
            raise ValueError(f"{c.get('name', '?')}: '{k}' must be 1-5, got {v!r}")
    total = c["volume"] + COMPLEXITY_VALUE[int(round(c["complexity"]))] + c["measurability"] + c["readiness"]
    bonus = 3 if c.get("structural") else 0
    gates = [g for g in ("measurability", "readiness") if c[g] < 3]
    return {
        "name": c.get("name", "?"),
        "score": total + bonus,
        "max": 23,
        "gain": "structural" if c.get("structural") else "marginal",
        "pilot_ready": not gates,
        "blocked_by": gates,
        "note": c.get("note", ""),
    }


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__)
        return
    args = [a for a in sys.argv[1:] if a != "--json"]
    data = json.load(open(args[0])) if args else json.load(sys.stdin)
    ranked = sorted((score(c) for c in data), key=lambda r: (r["pilot_ready"], r["score"]), reverse=True)
    if "--json" in sys.argv:
        print(json.dumps(ranked, indent=2)); return
    print(f"{'#':<3}{'Use case':<40}{'Score':>7}  {'Gain':<11}{'Pilot-ready'}")
    for i, r in enumerate(ranked, 1):
        ready = "yes" if r["pilot_ready"] else "NO (" + ", ".join(r["blocked_by"]) + " < 3)"
        print(f"{i:<3}{r['name'][:39]:<40}{r['score']:>4}/{r['max']}  {r['gain']:<11}{ready}")
    print("\nScore = volume + complexity value (middle is best) + measurability + readiness, +3 if structural.")


if __name__ == "__main__":
    main()
