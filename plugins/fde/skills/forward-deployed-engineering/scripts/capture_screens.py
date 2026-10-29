#!/usr/bin/env python3
"""Capture every screen of a web prototype, plus the position of each control.

Needs Playwright. With uv:  uvx --with playwright python capture_screens.py ...
Without uv:                 pip install playwright && playwright install chromium

Usage:
  capture_screens.py URL --out DIR [--routes a,b,c | --sections "section[id]"]
                     [--channel chromium|msedge|chrome] [--max-height 1700] [--width 1440]

URL is http(s)://... or a local file path. Screens are reached by setting
location.hash to each route. With --sections, routes are the ids of the
matching elements (default: section[id]).

Output:
  DIR/img/<route>.jpg   full-page screenshot, cut at --max-height
  DIR/els.json          {route: {h, els: [{tag, t, x, y, w, h}]}} for build_tour.py
The original prototype is only read, never changed.
"""
import argparse, json, os, pathlib, sys

ELEMENTS_JS = r"""(maxh) => {
  const out = [], seen = new Set();
  const els = document.querySelectorAll('button,a,[role=tab],h1,h2,h3,th,label,select,input,[aria-label],[title]');
  for (const e of els) {
    const r = e.getBoundingClientRect(), y = r.top + window.scrollY;
    if (!r.width || !r.height || y > maxh || y < 0) continue;
    const st = getComputedStyle(e);
    if (st.visibility === 'hidden' || st.display === 'none') continue;
    let t = (e.getAttribute('aria-label') || e.innerText || e.getAttribute('title') || e.value || '').trim().replace(/\s+/g, ' ').slice(0, 60);
    if (!t) continue;
    const k = t + '|' + Math.round(r.left) + '|' + Math.round(y);
    if (seen.has(k)) continue; seen.add(k);
    out.push({tag: e.tagName.toLowerCase(), t, x: Math.round(r.left), y: Math.round(y), w: Math.round(r.width), h: Math.round(r.height)});
  }
  return {els: out, docH: document.documentElement.scrollHeight};
}"""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url")
    p.add_argument("--out", required=True)
    p.add_argument("--routes", default="")
    p.add_argument("--sections", default="section[id]")
    p.add_argument("--channel", default="chromium")
    p.add_argument("--max-height", type=int, default=1700)
    p.add_argument("--width", type=int, default=1440)
    a = p.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright is missing. Run with: uvx --with playwright python capture_screens.py ...")

    url = a.url if a.url.startswith(("http://", "https://", "file://")) else pathlib.Path(a.url).resolve().as_uri()
    out = pathlib.Path(a.out); (out / "img").mkdir(parents=True, exist_ok=True)
    result = {}
    with sync_playwright() as pw:
        kw = {} if a.channel == "chromium" else {"channel": a.channel}
        browser = pw.chromium.launch(headless=True, **kw)
        page = browser.new_page(viewport={"width": a.width, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url, wait_until="load")
        page.wait_for_timeout(800)
        routes = [r for r in a.routes.split(",") if r] or page.evaluate(
            "(sel) => [...document.querySelectorAll(sel)].map(e => e.id).filter(Boolean)", a.sections)
        for rid in routes:
            page.evaluate("(h) => { location.hash = h }", rid)
            page.wait_for_timeout(450)
            page.evaluate("window.scrollTo(0, 0)")
            data = page.evaluate(ELEMENTS_JS, a.max_height)
            h = min(a.max_height, data["docH"])
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in rid)
            page.screenshot(path=str(out / "img" / f"{safe}.jpg"), type="jpeg", quality=72, full_page=True,
                            clip={"x": 0, "y": 0, "width": a.width, "height": h})
            result[rid] = {"h": h, "w": a.width, "img": f"img/{safe}.jpg", "els": data["els"]}
            print(f"captured {rid} ({len(data['els'])} elements)")
        browser.close()
    (out / "els.json").write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    if errors:
        print("Page errors:\n  " + "\n  ".join(errors[:10]))
    print(f"{len(result)} screens -> {out}")


if __name__ == "__main__":
    main()
