"""Regenerate the neo-brutalist, digital-collage README infographics in docs/images.

Run from anywhere:  python tools/make_readme_images.py
"""
import math, pathlib, random
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "images"
INK, PAPER = "#111111", "#F3EEE3"
Y, PK, BL, LM, OR, MT, LV, WH = "#FFD23F", "#FF5DA2", "#3D5AFE", "#B5F23D", "#FF7A1A", "#7EE0C3", "#B69CFF", "#FFFFFF"
H = "Arial Black, Arial, Helvetica, sans-serif"
M = "Courier New, Courier, monospace"


def defs():
    return f'''<defs>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#DCD3C2" stroke-width="1"/></pattern>
<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="2.1" fill="{INK}"/></pattern>
<pattern id="dotsw" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.8" fill="{WH}" opacity=".55"/></pattern>
<pattern id="stripes" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="14" fill="{INK}"/></pattern>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>
</defs>'''


def page(w, h, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>{defs()}'
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/><rect width="{w}" height="{h}" fill="url(#grid)"/>'
            f'{body}<rect width="{w}" height="{h}" fill="{PAPER}" filter="url(#grain)"/>'
            f'<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="none" stroke="{INK}" stroke-width="6"/></svg>')


def T(x, y, s, size, fill=INK, font=H, anchor="start", weight=None, rot=0, ls=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    r = f' transform="rotate({rot} {x} {y})"' if rot else ""
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}{l}{r}{extra}>{escape(s)}</text>'


def card(x, y, w, h, fill, rot=0, sh=8, sw=4, inner=""):
    cx, cy = x + w / 2, y + h / 2
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{x+sh}" y="{y+sh}" width="{w}" height="{h}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>{inner}</g>')


def tape(x, y, w, rot, color="#FFF4A8"):
    h = 26
    pts = [(0, 0)] + [(w, 0)] + [(w - 4 * (i % 2), h * i / 6) for i in range(1, 6)] + [(w, h), (0, h)] + [(4 * (i % 2), h - h * i / 6) for i in range(1, 6)]
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<g transform="translate({x} {y}) rotate({rot})"><polygon points="{p}" fill="{color}" opacity=".82" stroke="{INK}" stroke-opacity=".25"/></g>'


def torn(x, y, w, h, fill, seed=1, jag=7, stroke=True):
    rnd = random.Random(seed)
    top = [(x + i, y + rnd.uniform(0, jag)) for i in range(0, w + 1, 14)]
    bot = [(x + i, y + h - rnd.uniform(0, jag)) for i in range(w, -1, -14)]
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in top + bot)
    s = f' stroke="{INK}" stroke-width="3"' if stroke else ""
    return f'<polygon points="{p}" fill="{fill}"{s}/>'


def burst(cx, cy, r, fill, lines, size=18, rot=-10, n=14, color=INK):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * .8
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    out = f'<g transform="rotate({rot} {cx} {cy})"><polygon points="{" ".join(pts)}" transform="translate(6 6)" fill="{INK}"/><polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
    y0 = cy - (len(lines) - 1) * size * .55 + size * .35
    for i, l in enumerate(lines):
        out += T(cx, y0 + i * size * 1.1, l, size, color, H, "middle")
    return out + "</g>"


def label(x, y, s, fill=INK, color=WH, size=15, rot=0, pad=10):
    w = len(s) * size * .62 + pad * 2
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size+14}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            + T(x + pad, y + size + 4, s, size, color, M, weight="700") + "</g>")


def word(x, y, s, size, fill, color=INK, rot=0, pad=14, sh=7, k=.74):
    w = len(s) * size * k + pad * 2
    h = size * 1.12
    return card(x, y, w, h, fill, rot, sh, 4, T(x + pad, y + size * .93, s, size, color, H)), w


def halftone_blob(cx, cy, r, pat="dots"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{pat})"/>'


def num(cx, cy, n, fill=INK, color=WH, r=22):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>' + T(cx, cy + r * .36, n, r * .95, color, H, "middle")


def side(w, s):
    return T(w - 26, 30, s, 13, INK, M, rot=90, weight="700")


# ---------------- banner ----------------
def banner():
    W, Hh = 1200, 560
    b = halftone_blob(1010, 150, 150) + torn(0, 452, W, 108, BL, 3)
    b += label(40, 34, "FDE // FIELD KIT // v1.4.0", INK, Y, 16)
    b += label(360, 34, "CLAUDE CODE PLUGIN + AGENT SKILL", WH, INK, 14)
    c, w1 = word(46, 96, "FORWARD", 74, Y, rot=-2.5)
    b += c + tape(70, 82, 120, -8)
    c, w2 = word(150, 196, "DEPLOYED", 74, PK, rot=1.6)
    b += c
    c, _ = word(46, 300, "ENGINEERING", 74, INK, WH, rot=-1)
    b += c + tape(560, 290, 110, 12, "#CFF7FF")
    b += burst(1010, 150, 92, LM, ["CLASSIFY", "THEN ACT"], 20, -12)
    b += card(860, 280, 140, 92, WH, 4, 7, 4, T(930, 330, "6", 46, INK, H, "middle") + T(930, 358, "AXES", 14, INK, M, "middle", "700"))
    b += card(1020, 270, 140, 92, Y, -5, 7, 4, T(1090, 320, "25", 46, INK, H, "middle") + T(1090, 348, "TEMPLATES", 14, INK, M, "middle", "700"))
    b += card(930, 372, 150, 70, OR, -2, 6, 4, T(1005, 413, "21 CMDS", 22, INK, H, "middle"))
    b += T(46, 500, "discovery · gap matrix · requirements · FSPARK feedback · value ledger · rollback · handoff", 19, WH, M, weight="700")
    b += T(46, 530, "classify on six axes, then produce the artifact the client can act on", 15, "#DDE3FF", M)
    b += side(W, "01 / FORWARD DEPLOYED ENGINEERING")
    return page(W, Hh, b, "Forward Deployed Engineering: Claude Code plugin and agent skill",
                "Version 1.4.0. Six axes, six phases, 25 templates, 21 commands. Classify the engagement, then produce the right artifact.")


# ---------------- six axes ----------------
def axes():
    W, Hh = 1200, 660
    b = label(40, 32, "02 // CLASSIFICATION", INK, LM, 15)
    c, _ = word(40, 78, "SIX AXES", 64, Y, rot=-2)
    b += c + T(470, 118, "the skill infers each axis, states its assumptions", 17, INK, M, weight="700")
    b += T(470, 142, "in one line, then loads only the playbook that fits.", 17, INK, M, weight="700")
    b += halftone_blob(1100, 110, 62) + burst(1084, 110, 50, PK, ["INFER", "FIRST"], 15, 10, 12)
    data = [
        ("01", "PHASE", Y, ["discover · scope · prototype", "build · validate · handoff"]),
        ("02", "ENVIRONMENT", MT, ["cloud · regulated", "on-prem · air-gapped"]),
        ("03", "PRODUCT", PK, ["ai-agent · claude-code · data-platform", "api-integration · business-app"]),
        ("04", "ENGAGEMENT MODEL", LV, ["external · internal", "programme · partner"]),
        ("05", "STARTING POINT", OR, ["greenfield · prototype-exists", "legacy-replace · rescue · scale-out"]),
        ("06", "DELIVERY STYLE", LM, ["classic (tickets)", "spec-driven: spec, plan, build, verify"]),
    ]
    rots = [-1.5, 1, -0.8, 1.2, -1, 0.8]
    for i, (n, t, col, vals) in enumerate(data):
        x = 40 + (i % 3) * 380
        y = 200 + (i // 3) * 220
        inner = num(x + 36, y + 38, n) + T(x + 70, y + 48, t, 24 if len(t) < 13 else 19, INK, H)
        inner += f'<line x1="{x+20}" y1="{y+72}" x2="{x+330}" y2="{y+72}" stroke="{INK}" stroke-width="3"/>'
        for j, v in enumerate(vals):
            inner += T(x + 22, y + 104 + j * 26, v, 14, INK, M, weight="700")
        b += card(x, y, 350, 170, col, rots[i], 9, 4, inner)
        if i in (0, 4):
            b += tape(x + 120, y - 14, 100, -6)
    b += side(W, "02 / SIX AXES")
    return page(W, Hh, b, "Six classification axes",
                "Phase, environment, product, engagement model, starting point and delivery style, with their values. The skill infers each axis before it acts.")


# ---------------- lifecycle ----------------
def lifecycle():
    W, Hh = 1200, 660
    b = label(40, 32, "03 // LIFECYCLE", INK, PK, 15)
    c, _ = word(40, 78, "SIX PHASES", 60, MT, rot=-1.5)
    b += c + T(560, 112, "every phase ends in an artifact.", 17, INK, M, weight="700")
    b += T(560, 136, "prototype notes loop back to scope.", 17, INK, M, weight="700")
    phases = [("01", "DISCOVER", Y, ["Site survey", "System map", "Competitors", "Assumptions"]),
              ("02", "SCOPE", PK, ["Gap matrix", "Requirement IDs", "Outcome card", "Exec brief"]),
              ("03", "PROTOTYPE", MT, ["Separate version", "FSPARK tour", "Tour document", "Notes loop"]),
              ("04", "BUILD", LV, ["Spec per change", "Evals + ADR", "Decision log", "Blast radius"]),
              ("05", "VALIDATE", OR, ["Value ledger", "Pilot + ROI", "Demo checklist", "Eval pack"]),
              ("06", "HANDOFF", LM, ["Runbook", "Champion plan", "Accepted rows", "Old way off"])]
    for i, (n, t, col, arts) in enumerate(phases):
        x = 30 + i * 192
        y = 250 - (i % 2) * 34
        inner = num(x + 30, y + 32, n, INK, WH, 19) + T(x + 14, y + 86, t, 20 if len(t) < 9 else 17, INK, H)
        inner += f'<rect x="{x}" y="{y+100}" width="172" height="4" fill="{INK}"/>'
        for j, a in enumerate(arts):
            inner += T(x + 14, y + 132 + j * 26, "▪ " + a, 14, INK, M, weight="700")
        b += card(x, y, 172, 236, col, (-1) ** i * 1.2, 8, 4, inner)
        if i < 5:
            ax = x + 176
            b += f'<path d="M{ax} {y+150} L{ax+16} {y+150}" stroke="{INK}" stroke-width="5" marker-end="url(#ah)"/>'
    b += f'<path d="M500 498 C 500 590, 310 590, 310 470" fill="none" stroke="{PK}" stroke-width="7" stroke-dasharray="14 9" marker-end="url(#ah)"/>'
    b += label(340, 560, "CLIENT NOTES", PK, INK, 14, -3)
    b += burst(1060, 108, 64, Y, ["SHOW,", "THEN", "BUILD"], 15, 8, 12)
    b += torn(640, 580, 530, 54, INK, 7)
    b += T(660, 614, "done = released + adopted + old way switched off", 15, LM, M, weight="700")
    b += side(W, "03 / SIX PHASES")
    return page(W, Hh, b, "Six FDE phases and the artifacts each produces",
                "Discover, scope, prototype, build, validate and handoff, each with its artifacts. Client notes from the prototype flow back into scope.")


# ---------------- fspark ----------------
def fspark():
    W, Hh = 1200, 660
    b = label(40, 32, "05 // FEEDBACK MECHANISM", INK, MT, 15)
    cols = [Y, PK, MT, OR, LV, LM]
    x = 40
    for i, ch in enumerate("FSPARK"):
        c, w = word(x, 80 + (i % 2) * 14, ch, 86, cols[i], INK, (-4, 3, -2, 5, -3, 2)[i], 16, 8, .78)
        b += c
        x += w + 10
    b += tape(60, 70, 110, -10) + tape(470, 184, 120, 8, "#CFF7FF")
    b += T(40, 236, "Feedback-based Spotlight Presentation, Assessment, Response & Knowledge", 18, INK, M, weight="700")
    b += halftone_blob(1060, 140, 110)
    b += burst(1050, 140, 80, WH, ["1 HTML", "FILE", "OFFLINE"], 16, -8)
    steps = [("P", "PRESENTATION", Y, ["Spotlight tour.", "One stop per feature.", "Screens switch for you."]),
             ("A", "ASSESSMENT", PK, ["Looks right", "Needs changes", "Not needed · Not sure"]),
             ("R", "RESPONSE", MT, ["A note per feature.", "Two closing", "questions."]),
             ("K", "KNOWLEDGE", LM, ["Markdown file:", "preview, edit,", "download, merge."])]
    for i, (L, t, col, lines) in enumerate(steps):
        x = 40 + i * 284
        y = 280
        inner = T(x + 22, y + 92, L, 88, WH, H, extra=f' stroke="{INK}" stroke-width="4" paint-order="stroke"')
        inner += T(x + 22, y + 132, t, 22, INK, H)
        for j, l in enumerate(lines):
            inner += T(x + 22, y + 166 + j * 25, l, 15, INK, M, weight="700")
        b += card(x, y, 256, 250, col, (-1.2, 1, -0.6, 1.4)[i], 9, 4, inner)
    b += torn(0, 572, W, 88, INK, 11)
    b += label(40, 594, "add_fspark.py", LM, INK, 16, -2) + label(250, 594, "merge_feedback.py", Y, INK, 16, 1.5)
    b += T(500, 618, "team-response table in every file. reply with vN+1.", 16, WH, M, weight="700")
    b += side(W, "05 / FSPARK")
    return page(W, Hh, b, "FSPARK: Feedback-based Spotlight Presentation, Assessment, Response and Knowledge",
                "Four steps: presentation with a spotlight tour, assessment with a reaction per feature, response with notes and closing questions, knowledge as a Markdown feedback file merged across reviewers.")


# ---------------- prototype loop ----------------
def loop():
    W, Hh = 1200, 660
    b = label(40, 32, "04 // PROTOTYPE LOOP", INK, OR, 15)
    c, _ = word(40, 78, "FEEDBACK LOOP", 56, PK, rot=-1.5)
    b += c
    steps = [("01", "BUILD vN", "sample data, NEW badges"), ("02", "FSPARK", "data-tour targets + config"),
             ("03", "CHECK", "every stop, desktop + phone"), ("04", "SHARE", "by audience, see right"),
             ("05", "COLLECT", "feedback files come back"), ("06", "TRIAGE", "confirms · change · new · out"),
             ("07", "SEND vN+1", "what changed because of you")]
    for i, (n, t, s) in enumerate(steps):
        x = 40 + (i % 2) * 300
        y = 180 + i * 62
        inner = num(x + 28, y + 26, n, INK, Y if i % 2 else LM, 18) + T(x + 58, y + 34, t, 20, INK, H) + T(x + 230 if len(t) < 9 else x + 250, y + 33, "", 1)
        inner += T(x + 58, y + 52, s, 12, INK, M, weight="700")
        b += card(x, y, 300, 58, WH if i % 2 else Y, 0, 5, 3, inner)
    b += f'<path d="M660 600 C 720 600, 720 200, 660 200" fill="none" stroke="{INK}" stroke-width="6" stroke-dasharray="12 8" marker-end="url(#ah)"/>'
    b += label(676, 380, "REPEAT", LM, INK, 14, 90)
    inner = T(780, 210, "SHARE BY AUDIENCE", 22, INK, H)
    rows = [("In your organisation", "Claude artifact, org sharing", MT),
            ("Outside, links allowed", "public artifact link", Y),
            ("Outside, no Claude", "one offline HTML file", PK),
            ("Regulated", "client's approved channel only", OR)]
    for j, (a, c2, col) in enumerate(rows):
        yy = 236 + j * 82
        inner += f'<rect x="780" y="{yy}" width="340" height="64" fill="{col}" stroke="{INK}" stroke-width="3"/>'
        inner += T(796, yy + 28, a, 17, INK, H) + T(796, yy + 52, c2, 14, INK, M, weight="700")
    b += card(756, 172, 390, 452, WH, 1, 10, 4, inner)
    b += tape(900, 158, 110, -5)
    b += burst(1110, 110, 58, LM, ["0 EXT", "REQUESTS"], 13, 12, 12)
    b += side(W, "04 / PROTOTYPE LOOP")
    return page(W, Hh, b, "Prototype feedback loop with FSPARK",
                "Build the next version, add FSPARK, check every stop, share by audience, collect feedback files, triage them, send the next version.")


# ---------------- evidence ledger ----------------
def ledger():
    W, Hh = 1200, 680
    b = label(40, 32, "06 // EVIDENCE LEDGER  NEW IN 1.4", INK, Y, 15)
    c, _ = word(40, 78, "CLAIM", 64, WH, rot=-3)
    b += c + T(300, 128, "or", 30, INK, H)
    c, _ = word(360, 78, "ACCEPTED?", 64, LM, rot=2)
    b += c
    states = [("IMPLEMENTED", "#D9D9D9", "commit · PR"), ("VERIFIED", MT, "test output|+ revision"),
              ("DEPLOYED", LV, "release record"), ("MEASURED", Y, "baseline vs now"),
              ("ACCEPTED", LM, "name + date|+ source")]
    for i, (s, col, ev) in enumerate(states):
        x = 40 + i * 168
        y = 470 - i * 52
        h = 150 + i * 52
        inner = T(x + 12, y + 34, s, 15 if len(s) > 9 else 17, INK, H) + "".join(T(x + 12, y + 58 + k * 17, e, 12, INK, M, weight="700") for k, e in enumerate(ev.split("|")))
        inner += T(x + 12, y + h - 16, f"0{i+1}", 30, INK, H, extra=' opacity=".25"')
        b += card(x, y, 152, h, col, 0, 7, 4, inner)
    b += T(40, 652, "five states, never merged in one sentence. a local pass is not an outcome.", 15, INK, M, weight="700")
    # ledger slip
    inner = T(900, 232, "VALUE LEDGER ROW", 18, INK, H)
    for j, (k, v, ok) in enumerate([("measured", "3.5h (was 9h)", True), ("accepted by", "Priya Shah, 2026-11-14", True),
                                    ("status", "accepted", True), ("evidence", "PR #42 · readout notes", True)]):
        yy = 262 + j * 50
        inner += f'<rect x="900" y="{yy}" width="250" height="40" fill="{WH}" stroke="{INK}" stroke-width="2"/>'
        inner += T(910, yy + 16, k, 11, "#555555", M, weight="700") + T(910, yy + 33, v, 14, INK, M, weight="700")
    b += card(880, 200, 290, 280, "#FFF9E6", 2, 9, 4, inner)
    b += tape(980, 186, 100, 6)
    b += (f'<g transform="rotate(-14 1010 560)"><rect x="880" y="520" width="260" height="78" fill="none" stroke="#E0262E" stroke-width="7"/>'
          f'<rect x="890" y="530" width="240" height="58" fill="none" stroke="#E0262E" stroke-width="2"/>'
          + T(1010, 574, "NO SIGNER = CLAIM", 22, "#E0262E", H, "middle") + "</g>")
    b += burst(650, 236, 56, PK, ["SOURCE", "OR IT", "DIDN'T", "HAPPEN"], 11, -8, 12)
    b += side(W, "06 / EVIDENCE LEDGER")
    return page(W, Hh, b, "Evidence ledger: five delivery states and acceptance",
                "Implemented, verified, deployed, measured and accepted, each with its evidence. A value-ledger row is accepted only with a measured value, a named client signer, a date and a source. Otherwise it is a claim.")


# ---------------- toolkit ----------------
def toolkit():
    W, Hh = 1200, 400
    b = label(40, 32, "07 // WHAT IS IN THE BOX", INK, LV, 15)
    items = [("1", "ROUTER SKILL", Y), ("23", "REFERENCES", PK), ("25", "TEMPLATES", MT),
             ("9", "SCRIPTS", OR), ("21", "COMMANDS", LV), ("3", "AGENTS", LM), ("9", "EVAL CASES", WH)]
    for i, (n, t, col) in enumerate(items):
        x = 40 + i * 162
        y = 110 + (i % 2) * 40
        inner = T(x + 70, y + 110, n, 84, INK, H, "middle") + T(x + 70, y + 160, t, 13, INK, M, "middle", "700")
        b += card(x, y, 140, 190, col, (-3, 2, -1.5, 3, -2, 1.5, -2.5)[i], 8, 4, inner)
    b += tape(200, 96, 90, -8) + tape(840, 136, 90, 7, "#CFF7FF")
    b += side(W, "07 / TOOLKIT")
    return page(W, Hh, b, "What is in the FDE plugin",
                "One router skill, 23 references, 25 templates, 9 scripts, 21 commands, 3 agents and 9 eval cases.")


# ---------------- divider ----------------
def divider():
    W, Hh = 1200, 60
    b = torn(0, 12, W, 36, INK, 21, 6, False)
    x = 20
    for i, s in enumerate(["CLASSIFY", "DISCOVER", "SCOPE", "PROTOTYPE", "BUILD", "VALIDATE", "HANDOFF", "REPEAT"]):
        b += T(x, 38, s, 15, (Y, PK, MT, LM, OR, LV, WH, Y)[i], M, weight="700")
        x += 148
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" role="img" aria-label="section divider">'
            f'{defs()}<rect width="{W}" height="{Hh}" fill="{PAPER}"/>{b}</svg>')


for name, fn in [("banner", banner), ("six-axes", axes), ("lifecycle", lifecycle), ("fspark", fspark),
                 ("prototype-loop", loop), ("evidence-ledger", ledger), ("toolkit", toolkit), ("divider", divider)]:
    (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
print("ok")
