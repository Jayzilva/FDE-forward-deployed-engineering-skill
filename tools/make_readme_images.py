"""Regenerate the README infographics in docs/images.

Style: sci-fi HUD technical schematic and cutaway blueprint (dark sheets) alternating with
technical brutalism / Swiss industrial typography (light sheets). System fonts only, so the
SVGs render the same on GitHub.

Run from the repo root:  python tools/make_readme_images.py
"""
import math, pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "images"
H = "Helvetica Neue, Helvetica, Arial, sans-serif"
M = "SFMono-Regular, Consolas, Menlo, Courier New, monospace"
LIME = "#C8F53B"
DARK = dict(bg="#1B1C1E", fg="#ECECEA", mute="#8B8E93", line="#3A3C40", faint="#2A2B2E")
LIGHT = dict(bg="#EDEDE9", fg="#141414", mute="#6B6B6B", line="#141414", faint="#CFCFC9")
SERIES = "SERIES 1.4 / 07"


def T(x, y, s, size, fill, font=H, anchor="start", weight=400, ls=None, rot=0, op=None):
    r = f' transform="rotate({rot} {x} {y})"' if rot else ""
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{l}{r}{o}>{escape(s)}</text>')


def L(x1, y1, x2, y2, c, w=1, dash=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}{o}/>'


def R(x, y, w, h, fill="none", stroke=None, sw=1, dash=None, rx=0):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}{d}/>'


def C(cx, cy, r, c, w=1, fill="none", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d}/>'


def tag(x, y, s, size=14, fg="#141414", bg=LIME, mono=True):
    w = len(s) * size * (.61 if mono else .56) + 16
    return R(x, y - size - 5, round(w), size + 12, bg) + T(x + 8, y + 1, s, size, fg, M if mono else H, weight=500)


def header(k, W, cols, sheet):
    """Swiss metadata row: small caps labels in columns, hairline below."""
    out = ""
    xs = [40, 300, 560, 820]
    for i, (a, b) in enumerate(cols[:4]):
        out += T(xs[i], 34, a, 11, k["fg"], M, weight=500, ls=.4)
        if b:
            out += T(xs[i], 50, b, 11, k["mute"], M, ls=.4)
    out += T(W - 40, 34, sheet, 11, k["fg"], M, "end", 500, .4)
    out += L(40, 64, W - 40, 64, k["fg"] if k is LIGHT else k["line"], 1)
    return out


def footer(k, W, Hh, left, right):
    return (L(40, Hh - 44, W - 40, Hh - 44, k["fg"] if k is LIGHT else k["line"], 1)
            + T(40, Hh - 22, left, 11, k["mute"], M, ls=.4) + T(W - 40, Hh - 22, right, 11, k["mute"], M, "end", ls=.4))


def brackets(x, y, w, h, c, n=14, sw=1.5):
    p = f'M{x} {y+n}V{y}H{x+n} M{x+w-n} {y}H{x+w}V{y+n} M{x+w} {y+h-n}V{y+h}H{x+w-n} M{x+n} {y+h}H{x}V{y+h-n}'
    return f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{sw}"/>'


def ticks(x, y1, y2, c, step=12, major=5, length=6):
    out = ""
    for i, yy in enumerate(range(y1, y2 + 1, step)):
        out += L(x, yy, x + (length * 2 if i % major == 0 else length), yy, c, 1)
    return out


def hticks(x1, x2, y, c, step=12, major=5, length=6):
    out = ""
    for i, xx in enumerate(range(x1, x2 + 1, step)):
        out += L(xx, y, xx, y - (length * 2 if i % major == 0 else length), c, 1)
    return out


def dim(x1, x2, y, label, c, size=11):
    """Horizontal dimension line with end stops and a centred label."""
    mid = (x1 + x2) / 2
    w = len(label) * size * .62 + 14
    return (L(x1, y - 8, x1, y + 8, c) + L(x2, y - 8, x2, y + 8, c)
            + L(x1, y, mid - w / 2, y, c) + L(mid + w / 2, y, x2, y, c)
            + f'<path d="M{x1} {y}l7 -3v6z M{x2} {y}l-7 -3v6z" fill="{c}"/>'
            + T(mid, y + 4, label, size, c, M, "middle", ls=.5))


def reticle(cx, cy, r, k, accent=LIME):
    out = C(cx, cy, r, k["mute"], 1) + C(cx, cy, r * .66, k["line"], 1, dash="2 5") + C(cx, cy, r * .2, accent, 1.5)
    out += L(cx - r - 18, cy, cx + r + 18, cy, k["mute"], 1) + L(cx, cy - r - 18, cx, cy + r + 18, k["mute"], 1)
    for a in range(0, 360, 6):
        rad = math.radians(a)
        ln = 10 if a % 30 == 0 else 4
        out += L(cx + r * math.cos(rad), cy + r * math.sin(rad), cx + (r - ln) * math.cos(rad), cy + (r - ln) * math.sin(rad), k["mute"], 1)
    return out


def readout(x, y, value, unit, k, size=30):
    w = len(value) * size * .56
    return T(x, y, value, size, k["fg"], H, weight=400, ls=-.5) + T(x + w + 8, y - size * .45, unit, 10, k["mute"], H)


def page(k, W, Hh, body, title, desc):
    grid = ""
    if k is DARK:
        grid = ('<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
                f'<path d="M40 0H0V40" fill="none" stroke="{k["faint"]}" stroke-width="1"/></pattern></defs>'
                f'<rect width="{W}" height="{Hh}" fill="url(#g)"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" role="img" aria-labelledby="t d">'
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>'
            f'<rect width="{W}" height="{Hh}" fill="{k["bg"]}"/>{grid}{body}</svg>')


def side(k, W, s):
    return T(W - 22, 90, s, 12, k["fg"], H, rot=90, weight=500)


# ---------------------------------------------------------------- 01 banner (dark HUD)
def banner():
    k, W, Hh = DARK, 1200, 600
    b = header(k, W, [("FORWARD DEPLOYED", "ENGINEERING"), ("CLAUDE CODE PLUGIN", "+ AGENT SKILL"), (SERIES, "MIT LICENCE"), ("PYTHON 3.9+", "STDLIB SCRIPTS")], "SHEET 01")
    b += T(52, 222, "Forward Deployed", 92, k["mute"], weight=300, ls=-3)
    b += T(52, 322, "Engineering", 92, k["fg"], weight=500, ls=-3)
    b += dim(56, 560, 356, "ONE ENGAGEMENT : DISCOVERY TO HANDOFF", k["mute"])
    b += T(56, 420, "Field", 40, k["fg"], weight=500, ls=-1) + T(156, 420, "_kit", 40, k["mute"], weight=300, ls=-1)
    b += tag(260, 414, "classify : then act", 15)
    b += T(56, 470, "*Classifies each engagement on six axes, then produces the artifact", 13, k["mute"])
    b += T(56, 488, "the client can act on. Vendor-neutral. All examples fictional.", 13, k["mute"])
    cx, cy = 830, 300
    b += reticle(cx, cy, 140, k) + brackets(cx - 175, cy - 175, 350, 350, k["fg"])
    b += L(cx + 99, cy - 99, cx + 160, cy - 160, LIME, 1) + C(cx + 99, cy - 99, 3, LIME, 1, LIME)
    b += T(cx + 164, cy - 164, "TARGET : THE DELTA", 11, LIME, M)
    b += L(1036, 196, 1036, 432, k["fg"], 1.5)
    for i, (v, u) in enumerate([("6.00", "axes"), ("6.00", "phases"), ("25.00", "templates"), ("21.00", "commands")]):
        b += T(1050, 226 + i * 62, v, 28, k["fg"], ls=-.5) + T(1052, 244 + i * 62, u.upper(), 10, k["mute"], M)
    b += T(cx - 175, cy + 200, "LAT 06 AXES / LON 06 PHASES", 10, k["mute"], M)
    b += footer(k, W, Hh, "discovery · gap matrix · requirements · FSPARK · value ledger · rollback drill · handoff runbook", "v1.4.0")
    b += side(k, W, "01.   Forward Deployed Engineering")
    return page(k, W, Hh, b, "Forward Deployed Engineering: Claude Code plugin and agent skill",
                "Version 1.4.0. Six axes, six phases, 25 templates, 21 commands. Classify the engagement, then produce the right artifact.")


# ---------------------------------------------------------------- 02 six axes (light Swiss)
def axes():
    k, W, Hh = LIGHT, 1200, 720
    b = header(k, W, [("CLASSIFICATION", "SYSTEM"), ("INFERRED FROM", "REQUEST + REPOSITORY"), (SERIES, "SHEET 02 OF 07"), ("ASK ONLY WHEN", "THE ANSWER CHANGES")], "02")
    b += T(36, 176, "SIX AXES", 112, k["fg"], weight=500, ls=-4)
    b += T(1100, 110, "AX—", 34, k["fg"], weight=400, ls=-1) + T(1100, 148, "ES", 34, k["fg"], weight=400, ls=-1) + T(1100, 186, "06", 34, k["fg"], weight=400, ls=-1)
    b += L(40, 206, 700, 206, k["fg"])
    b += T(40, 226, "PARAMETER", 10, k["fg"], M, weight=500) + T(130, 226, "AXIS", 10, k["fg"], M, weight=500) + T(380, 226, "WHY IT MATTERS", 10, k["fg"], M, weight=500)
    rows = [("01", "Phase", "discover · scope · prototype · build · validate · handoff", "decides the playbook"),
            ("02", "Environment", "cloud · regulated · on-prem · air-gapped", "moves security to week one"),
            ("03", "Product", "ai-agent · claude-code · data-platform · api-integration · business-app", "sets metrics and evals"),
            ("04", "Engagement model", "external · internal · programme · partner", "decides who signs off"),
            ("05", "Starting point", "greenfield · prototype-exists · legacy-replace · rescue · scale-out", "changes the first two weeks"),
            ("06", "Delivery style", "classic (tickets) · spec-driven (spec, plan, build, verify)", "sets the tracking unit")]
    for i, (n, a, v, why) in enumerate(rows):
        y = 262 + i * 68
        b += T(40, y, n, 13, k["fg"], M, weight=500) + T(130, y + 2, a, 24, k["fg"], weight=500, ls=-.5)
        b += T(380, y, why, 12, k["mute"], M)
        b += T(130, y + 26, v, 12, k["fg"], M)
        b += L(40, y + 40, 700, y + 40, k["faint"] if i < 5 else k["fg"])
    b += ticks(724, 226, 660, k["fg"], 12, 5, 5)
    cx, cy = 840, 300
    b += C(cx, cy, 52, k["fg"]) + C(cx - 22, cy, 18, k["fg"]) + L(cx - 72, cy, cx + 72, cy, k["fg"]) + L(cx, cy - 72, cx, cy + 72, k["fg"])
    b += T(920, 264, "INFER", 34, k["fg"], weight=500, ls=-1) + T(920, 298, "FIRST", 34, k["fg"], weight=500, ls=-1)
    b += T(920, 322, "STATE ASSUMPTIONS IN ONE LINE", 10, k["mute"], M)
    b += T(740, 664, "06", 320, k["fg"], weight=500, ls=-18)
    b += footer(k, W, Hh, "EVERY ANSWER ENDS WITH AN FDE CHECK : SITUATION · BIGGEST RISK · NEXT MOVE", "CLASSIFY : THEN ACT")
    return page(k, W, Hh, b, "Six classification axes",
                "Phase, environment, product, engagement model, starting point and delivery style, with their values. The skill infers each axis before it acts.")


# ---------------------------------------------------------------- 03 lifecycle (dark cutaway)
def lifecycle():
    k, W, Hh = DARK, 1200, 700
    b = header(k, W, [("LIFECYCLE", "CUTAWAY"), ("SIX PHASES", "ONE ARTIFACT EACH"), (SERIES, "SHEET 03 OF 07"), ("FEEDBACK PATH", "PROTOTYPE TO SCOPE")], "03")
    b += T(40, 160, "Six", 80, k["fg"], weight=500, ls=-3) + T(184, 160, "_phases", 80, k["mute"], weight=300, ls=-3)
    b += T(760, 120, "*Every phase ends in an artifact the client", 13, k["mute"])
    b += T(760, 138, "can act on. Prototype notes return to scope", 13, k["mute"])
    b += T(760, 156, "until the journeys are confirmed.", 13, k["mute"])
    x0, y0, seg, hh = 60, 250, 180, 110
    b += dim(x0, x0 + seg * 6, 552, "ENGAGEMENT LENGTH : SET BY THE STARTING POINT AXIS", k["mute"])
    # pipe body cutaway
    b += R(x0, y0, seg * 6, hh, k["bg"], k["fg"], 1.5, rx=hh / 2)
    b += R(x0 + 10, y0 + 10, seg * 6 - 20, hh - 20, "none", k["line"], 1, "3 4", rx=(hh - 20) / 2)
    phases = [("01", "Discover", ["Site survey", "System map", "Competitors", "Assumptions"]),
              ("02", "Scope", ["Gap matrix", "Requirement IDs", "Outcome card", "Exec brief"]),
              ("03", "Prototype", ["Separate version", "FSPARK tour", "Tour document", "Notes loop"]),
              ("04", "Build", ["Spec per change", "Evals · ADR", "Decision log", "Blast radius"]),
              ("05", "Validate", ["Value ledger", "Pilot · ROI", "Demo checklist", "Eval pack"]),
              ("06", "Handoff", ["Runbook", "Champion plan", "Accepted rows", "Old way off"])]
    for i, (n, name, arts) in enumerate(phases):
        x = x0 + i * seg
        if i:
            b += L(x, y0, x, y0 + hh, k["fg"], 1)
        # hatch for cutaway
        b += T(x + 22 if i else x + 40, y0 + 42, n, 12, LIME if i in (2, 4) else k["mute"], M)
        b += T(x + 22 if i else x + 40, y0 + 78, name, 24, k["fg"], weight=500, ls=-.5)
        lx = x + seg / 2
        b += L(lx, y0 + hh, lx, y0 + hh + 46, k["mute"], 1, "2 3") + C(lx, y0 + hh + 46, 3, k["fg"], 1, k["fg"])
        for j, a in enumerate(arts):
            b += T(x + 22, y0 + hh + 82 + j * 22, a, 12, k["fg"] if j == 0 else k["mute"], M)
    # feedback loop: prototype back to scope (above the pipe)
    b += f'<path d="M{x0+seg*2.5} {y0} C {x0+seg*2.5} {y0-40}, {x0+seg*1.5} {y0-40}, {x0+seg*1.5} {y0-4}" fill="none" stroke="{LIME}" stroke-width="2" stroke-dasharray="5 5"/>'
    b += f'<path d="M{x0+seg*1.5} {y0-2}l-5 -10h10z" fill="{LIME}"/>'
    b += tag(x0 + seg * 2 - 46, y0 - 26, "client notes", 11)
    b += tag(40, 618, "show : then build", 15)
    b += T(260, 622, "Done means released and adopted: the old way is switched off for that domain.", 13, k["mute"])
    b += footer(k, W, Hh, "SECTION A-A : FDE PIPELINE, SIDE CUTAWAY", "NOT TO SCALE")
    b += side(k, W, "03.   Lifecycle")
    return page(k, W, Hh, b, "Six FDE phases and the artifacts each produces",
                "Discover, scope, prototype, build, validate and handoff, each with its artifacts. Client notes from the prototype flow back into scope.")


# ---------------------------------------------------------------- 05 FSPARK (light Swiss)
def fspark():
    k, W, Hh = LIGHT, 1200, 700
    b = header(k, W, [("FEEDBACK", "MECHANISM"), ("ONE HTML FILE", "NO EXTERNAL REQUESTS"), (SERIES, "SHEET 05 OF 07"), ("OUTPUT", "MARKDOWN FILE")], "05")
    b += T(34, 220, "FSPARK", 160, k["fg"], weight=500, ls=-7)
    b += T(1080, 110, "P—", 34, k["fg"], ls=-1) + T(1080, 148, "A—", 34, k["fg"], ls=-1) + T(1080, 186, "R—", 34, k["fg"], ls=-1) + T(1080, 224, "K", 34, k["fg"], ls=-1)
    b += L(40, 250, 700, 250, k["fg"])
    b += T(40, 270, "FEEDBACK-BASED SPOTLIGHT", 11, k["fg"], M, weight=500) + T(300, 270, "PRESENTATION · ASSESSMENT", 11, k["fg"], M, weight=500) + T(560, 270, "RESPONSE & KNOWLEDGE", 11, k["fg"], M, weight=500)
    mods = [("P", "Presentation", ["Spotlight tour", "One stop per feature", "Screens switch for you"], "1.00", "stop / feature"),
            ("A", "Assessment", ["Looks right", "Needs changes", "Not needed · Not sure"], "4.00", "reactions"),
            ("R", "Response", ["A note per feature", "Two closing", "questions"], "2.00", "closing questions"),
            ("K", "Knowledge", ["Preview · edit", "Download · copy", "Merge across reviewers"], "1.00", "file / reviewer")]
    y = 330
    b += L(40, y + 150, 1160, y + 150, k["fg"], 1)
    for i, (L1, name, lines, val, unit) in enumerate(mods):
        x = 40 + i * 282
        b += R(x, y, 262, 300, "none", k["fg"], 1)
        b += T(x + 16, y + 30, f"MODULE {i+1:02d}", 10, k["mute"], M)
        b += T(x + 248, y + 120, L1, 120, k["fg"], anchor="end", weight=300, ls=-4)
        b += T(x + 16, y + 140, name, 26, k["fg"], weight=500, ls=-.5)
        b += C(x + 131, y + 150, 4, k["fg"], 1, k["bg"])
        for j, t in enumerate(lines):
            b += T(x + 16, y + 186 + j * 20, t, 12, k["fg"], M)
        b += L(x + 16, y + 250, x + 16, y + 282, k["fg"], 1.5) + readout(x + 26, y + 278, val, unit, k, 24)
    b += tag(40, 666, "add_fspark.py : merge_feedback.py", 14, k["fg"], LIME)
    b += T(400, 666, "TEAM-RESPONSE TABLE IN EVERY FILE. ANSWER EACH ROW, SEND IT BACK WITH vN+1.", 11, k["mute"], M)
    return page(k, W, Hh, b, "FSPARK: Feedback-based Spotlight Presentation, Assessment, Response and Knowledge",
                "Four modules: presentation with a spotlight tour, assessment with a reaction per feature, response with notes and closing questions, knowledge as a Markdown feedback file merged across reviewers.")


# ---------------------------------------------------------------- 04 prototype loop (dark HUD radar)
def loop():
    k, W, Hh = DARK, 1200, 700
    b = header(k, W, [("PROTOTYPE", "FEEDBACK LOOP"), ("SEVEN STEPS", "REPEAT PER VERSION"), (SERIES, "SHEET 04 OF 07"), ("CHANNEL", "BY AUDIENCE")], "04")
    b += T(40, 150, "Feedback", 72, k["fg"], weight=500, ls=-3) + T(352, 150, "_loop", 72, k["mute"], weight=300, ls=-3)
    cx, cy, r = 320, 430, 170
    b += reticle(cx, cy, r, k)
    b += T(cx, cy - 6, "vN", 26, k["fg"], anchor="middle", weight=500) + T(cx, cy + 58, "TO vN+1", 11, k["mute"], M, "middle")
    steps = [("01", "Build vN"), ("02", "FSPARK"), ("03", "Check"), ("04", "Share"), ("05", "Collect"), ("06", "Triage"), ("07", "Send vN+1")]
    for i, (n, s) in enumerate(steps):
        a = math.radians(-90 + i * 360 / 7)
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        b += C(px, py, 6, LIME if i in (1, 6) else k["fg"], 1.5, k["bg"])
        lx, ly = cx + (r + 40) * math.cos(a), cy + (r + 40) * math.sin(a)
        anchor = "start" if math.cos(a) > .2 else ("end" if math.cos(a) < -.2 else "middle")
        b += L(px, py, lx, ly, k["mute"], 1, "2 3")
        b += T(lx + (6 if anchor == "start" else -6 if anchor == "end" else 0), ly + (4 if abs(math.sin(a)) < .9 else (-6 if math.sin(a) < 0 else 16)), f"{n} {s}", 13, k["fg"], M, anchor)
    x = 720
    b += T(x, 210, "SHARE BY AUDIENCE", 11, k["mute"], M, weight=500)
    b += L(x, 222, 1160, 222, k["line"])
    rows = [("In your organisation", "Claude artifact, org sharing"), ("Outside, links allowed", "Public artifact link"),
            ("Outside, no Claude", "One offline HTML file"), ("Regulated", "Client's approved channel only")]
    for i, (a, c2) in enumerate(rows):
        y = 266 + i * 78
        b += T(x, y, f"0{i+1}", 11, k["mute"], M) + T(x + 40, y, a, 22, k["fg"], weight=500, ls=-.5) + T(x + 40, y + 24, c2, 12, k["mute"], M)
        b += L(x, y + 44, 1160, y + 44, k["line"])
    b += tag(x, 610, "0 external requests : offline", 14)
    b += footer(k, W, Hh, "TRIAGE : CONFIRMS · CHANGE · NEW REQUIREMENT · OUT OF SCOPE", "SAY WHAT CHANGED BECAUSE OF THEM")
    b += side(k, W, "04.   Prototype loop")
    return page(k, W, Hh, b, "Prototype feedback loop with FSPARK",
                "Build the next version, add FSPARK, check every stop, share by audience, collect feedback files, triage them, send the next version.")


# ---------------------------------------------------------------- 06 evidence ledger (light Swiss schematic)
def ledger():
    k, W, Hh = LIGHT, 1200, 720
    b = header(k, W, [("EVIDENCE LEDGER", "NEW IN 1.4"), ("FIVE STATES", "NEVER MERGED"), (SERIES, "SHEET 06 OF 07"), ("RULE", "NO SIGNER = CLAIM")], "06")
    b += T(34, 196, "CLAIM", 140, k["fg"], weight=500, ls=-6) + T(500, 196, "_OR", 60, k["mute"], weight=300, ls=-2)
    b += T(36, 262, "ACCEPTED?", 64, k["fg"], weight=300, ls=-2)
    # gauge
    gx, gy, gw = 40, 360, 760
    b += L(gx, gy, gx + gw, gy, k["fg"], 2) + hticks(gx, gx + gw, gy, k["fg"], 19, 8, 6)
    states = [("01", "IMPLEMENTED", "commit · PR"), ("02", "VERIFIED", "test output + revision"),
              ("03", "DEPLOYED", "release record"), ("04", "MEASURED", "baseline vs now"),
              ("05", "ACCEPTED", "name + date + source")]
    sw = gw / 5
    for i, (n, s, ev) in enumerate(states):
        x = gx + i * sw
        b += R(x, gy + 10, sw - 8, 34, LIME if i == 4 else ("none"), k["fg"], 1)
        b += T(x + 10, gy + 32, n, 12, k["fg"], M, weight=500)
        b += T(x, gy + 74, s, 17, k["fg"], weight=500, ls=-.3)
        b += T(x, gy + 96, ev, 11, k["mute"], M)
        b += L(x, gy + 108, x, gy + 128, k["fg"])
    b += f'<path d="M{gx+4*sw+60} {gy-10}l-7 -12h14z" fill="{k["fg"]}"/>'
    b += T(gx + 4 * sw + 60, gy - 30, "ONLY THIS STATE COUNTS AS DONE", 10, k["fg"], M, "middle", 500)
    b += T(40, gy + 170, "A local pass is not an outcome. A demo is not a launch.", 18, k["fg"], weight=400)
    b += T(40, gy + 194, "A transcript that says “approved” approves nothing.", 18, k["mute"], weight=400)
    # spec card
    x, y = 850, 120
    b += R(x, y, 310, 400, "none", k["fg"], 1) + T(x + 16, y + 26, "VALUE LEDGER ROW", 11, k["fg"], M, weight=500) + T(x + 294, y + 26, "VL-01", 11, k["mute"], M, "end")
    b += L(x, y + 40, x + 310, y + 40, k["fg"])
    fields = [("MEASURED", "3.5 h  (baseline 9 h)"), ("ACCEPTED BY", "Priya Shah, 2026-11-14"), ("STATUS", "accepted"), ("EVIDENCE", "PR #42 · readout notes")]
    for j, (f, v) in enumerate(fields):
        yy = y + 80 + j * 72
        b += T(x + 16, yy, f, 10, k["mute"], M)
        if f == "STATUS":
            b += tag(x + 16, yy + 30, v, 14, k["fg"], LIME)
        else:
            b += T(x + 16, yy + 28, v, 17, k["fg"], weight=500)
        b += L(x + 16, yy + 44, x + 294, yy + 44, k["faint"])
    b += R(x, y + 410, 310, 44, k["fg"]) + T(x + 155, y + 438, "NO SIGNER = CLAIM", 15, k["bg"], M, "middle", 500)
    b += T(900, 690, "05", 200, k["fg"], weight=500, ls=-10, op=.08)
    b += footer(k, W, Hh, "python scripts/evidence_check.py fde/  --strict  --export", "RECORDED FIELDS ONLY. NOT PROOF OF CONSENT")
    return page(k, W, Hh, b, "Evidence ledger: five delivery states and acceptance",
                "Implemented, verified, deployed, measured and accepted, each with its evidence. A value-ledger row is accepted only with a measured value, a named client signer, a date and a source. Otherwise it is a claim.")


# ---------------------------------------------------------------- 07 toolkit (dark spec sheet)
def toolkit():
    k, W, Hh = DARK, 1200, 420
    b = header(k, W, [("WHAT IS IN", "THE BOX"), ("PLUGIN", "fde@forward-deployed-engineering"), (SERIES, "SHEET 07 OF 07"), ("FORMAT", "MARKDOWN + PYTHON")], "07")
    b += T(40, 150, "Field", 64, k["fg"], weight=500, ls=-2) + T(212, 150, "_specification", 64, k["mute"], weight=300, ls=-2)
    items = [("1", "router skill"), ("23", "references"), ("25", "templates"), ("9", "scripts"), ("21", "commands"), ("3", "agents"), ("9", "eval cases")]
    for i, (n, u) in enumerate(items):
        x = 40 + i * 162
        b += L(x, 216, x, 330, LIME if i in (2, 4) else k["fg"], 1.5)
        b += T(x + 14, 290, n, 72, k["fg"], weight=300, ls=-3)
        b += T(x + 16, 318, u.upper(), 10, k["mute"], M)
    b += footer(k, W, Hh, "SKILL.md UNDER 500 LINES · DESCRIPTION UNDER 1,024 CHARACTERS", "python tools/package.py")
    b += side(k, W, "07.   Toolkit")
    return page(k, W, Hh, b, "What is in the FDE plugin",
                "One router skill, 23 references, 25 templates, 9 scripts, 21 commands, 3 agents and 9 eval cases.")


# ---------------------------------------------------------------- divider (transparent ruler)
def divider():
    W, Hh, c = 1200, 40, "#8A8D91"
    b = L(0, 20, W, 20, c, 1) + hticks(0, W, 20, c, 10, 10, 5)
    for i, s in enumerate(["DISCOVER", "SCOPE", "PROTOTYPE", "BUILD", "VALIDATE", "HANDOFF"]):
        x = 20 + i * 200
        b += T(x, 36, f"{i+1:02d} {s}", 10, c, M, ls=.6)
    b += R(1170, 14, 30, 12, LIME)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" role="img" aria-label="section divider">{b}</svg>')


if __name__ == "__main__":
    for name, fn in [("banner", banner), ("six-axes", axes), ("lifecycle", lifecycle), ("fspark", fspark),
                     ("prototype-loop", loop), ("evidence-ledger", ledger), ("toolkit", toolkit), ("divider", divider)]:
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print("ok")
