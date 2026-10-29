#!/usr/bin/env python3
"""ROI calculator for FDE pilots. Stdlib only.

Refuses to run without a baseline: without pre-pilot data there is no
denominator, and an ROI claim without one will not survive a CIO review.

Usage:
  python roi_calc.py --units 120 --base-hours 6 --pilot-hours 2.5 --rate 45 \
      --solution-cost 1500 [--base-people 4 --pilot-people 2] [--haircut 0.3] [--json]

--units          units of work per month (tickets, reports, PRs, cases)
--units-per-year alternative to --units when volume is planned annually
--base-hours     hours per unit before the pilot (baseline)
--pilot-hours    hours per unit during the pilot
--rate           loaded hourly cost
--solution-cost  monthly cost of the solution (licences, infra, support)
--base-people / --pilot-people  people involved per unit (structural signal)
--haircut        fraction removed from savings for the conservative case (default 0.3)
"""
import argparse, json, sys


def compute(a):
    if a.base_hours is None or a.base_hours <= 0:
        sys.exit("ERROR: no baseline. Capture hours-per-unit before Day 1; ROI without a baseline is not defensible.")
    if a.pilot_hours < 0 or a.units <= 0 or a.rate <= 0:
        sys.exit("ERROR: units and rate must be > 0, pilot-hours >= 0.")
    saved_per_unit = a.base_hours - a.pilot_hours
    gross = saved_per_unit * a.units * a.rate
    cases = {}
    for name, factor in (("conservative", 1 - a.haircut), ("measured", 1.0)):
        net = gross * factor - a.solution_cost
        cases[name] = {
            "monthly_gross_saving": round(gross * factor, 2),
            "monthly_net_saving": round(net, 2),
            "annual_net_saving": round(net * 12, 2),
            "roi_pct": round(net / a.solution_cost * 100, 1) if a.solution_cost else None,
        }
    structural = False
    reasons = []
    if a.base_people and a.pilot_people and a.pilot_people < a.base_people:
        structural = True
        reasons.append(f"people per unit {a.base_people} -> {a.pilot_people}")
    if a.pilot_hours <= a.base_hours * 0.5:
        reasons.append(f"effort per unit cut by {round((1 - a.pilot_hours / a.base_hours) * 100)}%")
        structural = structural or a.pilot_hours <= a.base_hours * 0.35
    return {
        "hours_saved_per_unit": round(saved_per_unit, 2),
        "pct_time_reduction": round(saved_per_unit / a.base_hours * 100, 1),
        "cases": cases,
        "gain_type": "structural" if structural else "marginal",
        "gain_evidence": reasons,
        "warnings": ([] if saved_per_unit > 0 else ["Pilot is slower than baseline."])
        + ([] if cases["conservative"]["monthly_net_saving"] > 0 else ["Conservative case does not pay back."]),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--units", type=float, help="units of work per month")
    g.add_argument("--units-per-year", type=float, help="units of work per year (converted to monthly)")
    p.add_argument("--base-hours", type=float)
    p.add_argument("--pilot-hours", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--solution-cost", type=float, default=0.0)
    p.add_argument("--base-people", type=float)
    p.add_argument("--pilot-people", type=float)
    p.add_argument("--haircut", type=float, default=0.3)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.units is None:
        a.units = a.units_per_year / 12
    r = compute(a)
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2)); return
    print(f"Hours saved per unit: {r['hours_saved_per_unit']} ({r['pct_time_reduction']}% reduction)")
    print(f"Gain type: {r['gain_type'].upper()}" + (f"  [{'; '.join(r['gain_evidence'])}]" if r['gain_evidence'] else ""))
    for name, c in r["cases"].items():
        roi = f", ROI {c['roi_pct']}%" if c["roi_pct"] is not None else ""
        print(f"{name:>12}: net/month {c['monthly_net_saving']:,.2f}, net/year {c['annual_net_saving']:,.2f}{roi}")
    for w in r["warnings"]:
        print(f"WARNING: {w}")


if __name__ == "__main__":
    main()
