#!/usr/bin/env python3
"""Profile artwork — "Chart". Every asset is a sheet from the same nautical chart.

    python3 scripts/build_assets.py            # all sheets, dark + light
    python3 scripts/build_assets.py hero       # one sheet
"""
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import svgkit as k  # noqa: E402
import chartlib as c  # noqa: E402
from svgkit import Theme  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "assets")
W = 1280


def cap(t: Theme, s: str, x: float, y: float, size: float = 11, fill=None, anchor="start", tracking=1.8, opacity=None):
    """Tracked mono caption. Glyphs are shared through <use>, so captions cost almost nothing."""
    return k.text_use(s.upper(), x, y, "plex", size, fill or t.muted, anchor=anchor, tracking=tracking, opacity=opacity)


def frame(t: Theme, w: float, h: float) -> str:
    """Sheet with a quiet double neat-line (the hero alone gets the minute bars)."""
    return (sheet(t, w, h)
            + f'<rect x="14" y="14" width="{w-28}" height="{h-28}" fill="none" stroke="{t.ink}" stroke-width="0.9" stroke-opacity=".8"/>'
            + f'<rect x="19" y="19" width="{w-38}" height="{h-38}" fill="none" stroke="{t.ink}" stroke-width="0.5" stroke-opacity=".6"/>')


def chip(t: Theme, s: str, x: float, y: float, strong: bool = False):
    pad = 9
    w = k.text_width(s, "plex", 11, 0.4) + pad * 2
    out = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="3" fill="{t.panel}" '
           f'stroke="{t.accent if strong else t.ink}" stroke-width="{1 if strong else 0.6}" stroke-opacity="{1 if strong else 0.6}"/>'
           + k.text_use(s, x + pad, y + 15, "plex", 11, t.ink, tracking=0.4))
    return out, w


def chips(t: Theme, items, x: float, y: float, max_x: float, strong_first=True) -> float:
    """Flow chips within max_x; returns the svg and the y of the last row."""
    out, x0 = [], x
    for i, s in enumerate(items):
        c, w = chip(t, s, x, y, strong=(strong_first and i == 0))
        if x + w > max_x and x > x0:
            x, y = x0, y + 30
            c, w = chip(t, s, x, y, strong=(strong_first and i == 0))
        out.append(c)
        x += w + 8
    return "".join(out), y


def anchor_glyph(x: float, y: float, ink: str, s: float = 1.0) -> str:
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{ink}" stroke-width="1.3" stroke-linecap="round">'
            f'<circle cx="0" cy="-9" r="2.4"/><path d="M0,-6.5 V9"/><path d="M-6,-1 H6"/>'
            f'<path d="M-8,4 Q-8,10 0,10 Q8,10 8,4"/></g>')


def lighthouse(x: float, y: float, ink: str, accent: str, paper: str, beam: bool = True, s: float = 1.0) -> str:
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    if beam:
        g.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/>'
                 f'<path d="M0,-22 L150,-60 L150,16 Z" fill="{accent}" fill-opacity=".16"/></g>')
    g.append(f'<path d="M-7,10 L-5,-18 H5 L7,10 Z" fill="{paper}" stroke="{ink}" stroke-width="1.2"/>')
    g.append(f'<path d="M-7,-2 H7 M-6,-10 H6" stroke="{ink}" stroke-width="1"/>')
    g.append(f'<rect x="-5" y="-26" width="10" height="8" fill="{accent}"/>')
    g.append(f'<path d="M-6,-26 L0,-32 L6,-26 Z" fill="{ink}"/>')
    g.append(f'<path d="M-10,10 H10" stroke="{ink}" stroke-width="1.2"/>')
    g.append("</g>")
    return "".join(g)


def wal_tape(t: Theme, x: float, y: float, n: int = 16, dur: float = 6.0) -> str:
    out = []
    for i in range(n):
        out.append(f'<rect x="{x + i*12}" y="{y}" width="9" height="10" rx="1" fill="{t.ok}" opacity=".2">'
                   f'<animate attributeName="opacity" values=".2;.2;1;1" keyTimes="0;{i/n:.3f};{(i+1)/n:.3f};1" dur="{dur}s" repeatCount="indefinite"/></rect>')
    return "".join(out)





def sheet(t: Theme, w: float, h: float, rx: float = 10) -> str:
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{t.paper}" stroke="{t.hair}"/>'


def halo_defs(hid: str, paper: str) -> str:
    return (f'<radialGradient id="{hid}" cx="50%" cy="50%" r="50%"><stop offset="0.55" stop-color="{paper}" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="{paper}" stop-opacity="0"/></radialGradient>')


# ---------------------------------------------------------------- hero
def hero(t: Theme) -> str:
    H = 640
    M = 18  # neat-line inset
    inner = (M, M, W - 2 * M, H - 2 * M)
    defs = [c.hatch_defs("hatch", t.ink, spacing=5, angle=45, opacity=0.22), halo_defs("halo", t.paper),
            f'<clipPath id="sheetclip"><rect x="{M+6}" y="{M+6}" width="{W-2*M-12}" height="{H-2*M-12}"/></clipPath>']
    b = [sheet(t, W, H)]

    # water + graticule + bathymetry, clipped to the neat line
    name_box = (40, 40, 760, 300)      # keep the field calm under the name
    cart_box = (40, 455, 560, 170)     # and under the cartouche
    # three deliberate islands (named below) plus random bathymetry around them
    island_blobs = [(690, 575, 46, 2.1), (1125, 555, 58, 2.3), (905, 118, 40, 1.9)]
    field = c.make_field(W, H, seed=2709, n=22, r=(42, 150), a=(0.5, 1.1), avoid=[name_box, cart_box], extra=island_blobs)
    LAND = 1.5
    levels = [0.5 + i * 0.1 for i in range(11)]
    pts = [(120, 440), (330, 392), (545, 452), (735, 352), (905, 420), (1100, 392), (1215, 300)]
    g = [f'<g clip-path="url(#sheetclip)">']
    g.append(c.graticule(M, M, W - 2 * M, H - 2 * M, t.ink, step=80, opacity=0.10))
    g.append(c.rhumb_lines(1040, 250, 900, t.ink, n=32, opacity=0.07))
    g.append(c.draw_contours(field, levels, t.ink, index_every=5, opacity=0.42, land_level=LAND, land_fill=t.land, hatch_id="hatch"))
    g.append(c.soundings(field, (M, M, W - 2 * M, H - 2 * M), t.ink, seed=11, n=56, size=9.5, land_level=LAND,
                         avoid=[name_box, cart_box, (930, 130, 240, 250), (960, 560, 300, 60)], opacity=0.55,
                         avoid_lines=[pts], line_clearance=28))
    # named islands: the biggest land masses carry project names, like real charts carry ports
    names = ["Rustmapper Shoal", "Scrapy Harbor", "Common Crawl Bank", "Delta Lake", "CT Ledge"]
    for (area, ix, iy), nm in zip([i for i in c.islands(field, LAND, 900) if not (40 <= i[1] <= 800 and 40 <= i[2] <= 340)], names):
        g.append(k.text(nm, ix, iy + 4, "serif-italic", 15, t.ink, anchor="middle", opacity=0.9))
    # halos so type sits on calm paper
    g.append(f'<ellipse cx="420" cy="190" rx="470" ry="190" fill="url(#halo)"/>')
    g.append(f'<rect x="{M+6}" y="462" width="560" height="150" fill="{t.paper}" fill-opacity=".0"/>')
    g.append("</g>")
    b.extend(g)

    # compass rose + rhumb centre
    b.append(c.compass_rose(1040, 250, 74, t.ink, t.accent))

    # plotted course with the boat, entrance buoys red-left / green-right
    b.append(c.course(pts, t.ink, t.accent, dur=48, boat_svg=c.boat(t.ink, t.accent, t.ink2, 0.9)))
    b.append(c.buoy(84, 414, t.accent, t.ink, "can"))
    b.append(c.buoy(150, 486, t.ok, t.ink, "cone"))
    b.append(c.buoy(1196, 246, t.accent, t.ink, "can"))
    b.append(c.buoy(1246, 336, t.ok, t.ink, "cone"))

    # the name
    b.append(cap(t, "Chart No. 27  ·  The open web  ·  Soundings in rows", 72, 76, 11, t.ink2))
    b.append(k.text("Ben Russell", 64, 222, "serif", 176, t.ink, tracking=-3))
    b.append(k.text("I build crawlers that survive the open web,", 72, 282, "serif-italic", 34, t.ink2, tracking=-0.2))
    b.append(k.text("and the systems that make sense of what they bring back.", 72, 322, "serif-italic", 34, t.ink2, tracking=-0.2))

    # cartouche (title block)
    cx, cy, cw, ch = 48, 462, 532, 150
    b.append(c.cartouche(cx, cy, cw, ch, t.ink, t.paper))
    b.append(cap(t, "Benjamin S. Russell", cx + 22, cy + 34, 11.5, t.ink))
    b.append(k.text("Full-stack developer · scraping enthusiast", cx + 22, cy + 60, "serif-italic", 22, t.ink2))
    b.append(f'<line x1="{cx+22}" y1="{cy+74}" x2="{cx+cw-22}" y2="{cy+74}" stroke="{t.ink}" stroke-width="0.6" stroke-opacity=".6"/>')
    b.append(cap(t, "Surveyed 2024 – 2026  ·  rustmapper on PyPI  ·  Scrapy platform", cx + 22, cy + 96, 10, t.muted))
    b.append(cap(t, "Python · Rust · Swift · C   ·   depths in trusted rows", cx + 22, cy + 114, 10, t.muted))

    # scale bar inside the title block, as on a real sheet
    sx, sy = cx + 22, cy + 136
    b.append(f'<rect x="{sx}" y="{sy}" width="200" height="5" fill="none" stroke="{t.ink}" stroke-width="0.8"/>')
    for i in range(4):
        if i % 2 == 0:
            b.append(f'<rect x="{sx + i*50}" y="{sy}" width="50" height="5" fill="{t.ink}"/>')
    for i, lab in enumerate(["0", "10k", "20k", "30k", "40k urls"]):
        b.append(k.text_use(lab, sx + i * 50, sy - 5, "plex", 9, t.muted, anchor="middle" if i < 4 else "start"))
    b.append(cap(t, "scale of discovered urls  ·  not for navigation", sx + 236, sy + 5, 9.5, t.muted))

    b.append(c.border(M, M, W - 2 * M, H - 2 * M, t.ink, step=20))
    return k.svg(W, H, "".join(b), "Ben Russell — a nautical chart of the open web. I build crawlers that survive it, and the systems that make sense of what they bring back.", "".join(defs) + k.glyph_defs())




# ---------------------------------------------------------------- approach · Scrapy
def approach_scrapy(t: Theme) -> str:
    H = 420
    defs = [c.hatch_defs("hs", t.ink, 5, 45, 0.22),
            f'<clipPath id="ap"><rect x="596" y="34" width="650" height="{H-68}"/></clipPath>']
    b = [frame(t, W, H)]
    # left: title block
    b.append(cap(t, "Sheet 3  ·  Approaches  ·  01  ·  Scrapy Harbor", 48, 60, 10.5, t.ink2))
    b.append(k.text("Scrapy", 44, 152, "serif", 96, t.ink, tracking=-2))
    b.append(k.text("The platform. A harbor with the lights on.", 48, 194, "serif-italic", 27, t.ink2))
    notes = ["Scout spider  ·  JS-heavy page detection  ·  adaptive rate limits",
             "Delta Lake raw  ·  PostgreSQL metrics  ·  Redis queues  ·  one interface",
             "Circuit breakers  ·  health checks  ·  Grafana on Prometheus  ·  K8s"]
    for i, ln in enumerate(notes):
        b.append(k.text_use(ln, 48, 232 + i * 22, "plex", 12, t.ink2))
    cs, _ = chips(t, ["Python 3.11", "Scrapy", "Delta Lake", "PostgreSQL", "Redis", "Prometheus", "Grafana", "Docker", "Kubernetes"], 48, 312, 545)
    b.append(cs)

    # right: the approach chart
    px, py, pw, ph = 596, 34, 650, H - 68
    # The field is larger than the sheet (offset OX, OY) so the coastline closes off-canvas and fills as land.
    OX, OY = 0, 120
    FW, FH = W + 260, H + 2 * OY
    coast = [(1330 + OX, 200 + OY, 120, 3.0), (1250 + OX, 40 + OY, 90, 2.8), (1255 + OX, 390 + OY, 90, 2.8),
             (1215 + OX, 214 + OY, 52, -1.7)]  # the last one carves the harbor basin
    field = c.make_field(FW, FH, seed=31, n=10, r=(40, 110), a=(0.4, 0.9), avoid=[(560, 0, 900, FH)], extra=coast)
    LAND = 1.5
    g = [f'<g clip-path="url(#ap)">']
    g.append(c.graticule(px, py, pw, ph, t.ink, 70, 0.10))
    g.append(f'<g transform="translate({-OX},{-OY})">' + c.draw_contours(field, [0.5 + i * 0.1 for i in range(11)], t.ink, 5, 0.38, LAND, t.land, "hs") + "</g>")
    channel = [(606, 300), (750, 252), (900, 222), (1060, 214), (1176, 214)]
    shifted = [(x + OX, y + OY) for x, y in channel]
    g.append(f'<g transform="translate({-OX},{-OY})">' + c.soundings(field, (px + OX, py + OY, pw, ph), t.ink, 5, n=26, size=9, land_level=LAND, opacity=0.5,
                         avoid_lines=[shifted], line_clearance=40, avoid=[(1100 + OX, 60 + OY, 160, 120)]) + "</g>")
    g.append("</g>")
    b.extend(g)
    # channel + lateral marks
    d = "M" + " L".join(f"{x},{y}" for x, y in channel)
    b.append(f'<path d="{d}" fill="none" stroke="{t.ink}" stroke-width="1" stroke-dasharray="2 6" stroke-opacity=".8"/>')
    stations = ["urls", "scout", "analyze", "summarize"]
    for i, name in enumerate(stations):
        (x1, y1), (x2, y2) = channel[i], channel[i + 1]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        b.append(c.buoy(mx + nx * 30, my + ny * 30 + 6, t.accent, t.ink, "can"))     # starboard hand, returning
        b.append(c.buoy(mx - nx * 30, my - ny * 30 + 6, t.ok, t.ink, "cone"))
        b.append(cap(t, name, mx - nx * 30, my - ny * 30 - 14, 9.5, t.ink, anchor="middle"))
        b.append(f'<circle cx="{mx}" cy="{my}" r="2.6" fill="{t.ink}"/>')
    # harbor
    b.append(anchor_glyph(1200, 238, t.ink, 1.1))
    b.append(cap(t, "Delta Lake", 1200, 268, 9.5, t.ink, anchor="middle"))
    b.append(cap(t, "anchorage", 1200, 282, 8.5, t.muted, anchor="middle"))
    b.append(lighthouse(1196, 118, t.ink, t.accent, t.paper, True, 1.0))
    b.append(cap(t, "Grafana Lt · Fl(3) 10s", 1232, 150, 8.5, t.ink2, anchor="end"))
    b.append(cap(t, "open water", 616, 352, 9.5, t.muted))
    b.append(f'<circle cx="620" cy="62" r="3" fill="{t.ok}"/>')
    b.append(cap(t, "breaker closed", 630, 66, 9.5, t.ok))
    # packet boat running the channel
    sd = c.smooth_path(channel, False)
    b.append(f'<g><animateMotion dur="16s" repeatCount="indefinite" rotate="auto" path="{sd}"/>{c.boat(t.ink, t.accent, t.ink2, 0.55)}</g>')
    return k.svg(W, H, "".join(b), "Scrapy — approach chart. A channel marked by buoys leads from open water past the Grafana light into Delta Lake anchorage.", "".join(defs) + k.glyph_defs())


# ---------------------------------------------------------------- survey · rustmapper
def survey_rustmapper(t: Theme) -> str:
    H = 420
    defs = [c.hatch_defs("hr", t.ink, 5, 45, 0.22),
            f'<clipPath id="sv"><rect x="596" y="34" width="650" height="{H-68}"/></clipPath>']
    b = [frame(t, W, H)]
    b.append(cap(t, "Sheet 4  ·  Surveys  ·  02  ·  Rustmapper Shoal", 48, 60, 10.5, t.ink2))
    b.append(k.text("rustmapper", 44, 152, "serif", 96, t.ink, tracking=-2))
    b.append(k.text("The engine. A survey vessel with 512 lead lines.", 48, 194, "serif-italic", 27, t.ink2))
    notes = ["Up to 512 adaptive workers  ·  sharded frontier  ·  resumable WAL",
             "Seeds from sitemaps, CT logs and Common Crawl  ·  Redis for fleets",
             "Rust 2024  ·  tokio  ·  reqwest  ·  redb  ·  a Python package via maturin"]
    for i, ln in enumerate(notes):
        b.append(k.text_use(ln, 48, 232 + i * 22, "plex", 12, t.ink2))
    cs, _ = chips(t, ["pip install rustmapper", "Rust 2024", "tokio", "reqwest", "redb", "maturin", "PyPI"], 48, 312, 545)
    b.append(cs)

    px, py, pw, ph = 596, 34, 650, H - 68
    shoal = [(1120, 140, 86, 2.4), (960, 330, 52, 2.0)]
    field = c.make_field(W, H, seed=57, n=10, r=(40, 120), a=(0.4, 0.9), avoid=[(560, 0, 720, 420)], extra=shoal)
    LAND = 1.5
    LOOP = 14.0
    g = [f'<g clip-path="url(#sv)">']
    g.append(c.graticule(px, py, pw, ph, t.ink, 70, 0.10))
    # contours fade in once the survey has run
    g.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.55;0.7;0.95;1" dur="{LOOP}s" repeatCount="indefinite"/>'
             + c.draw_contours(field, [0.5 + i * 0.1 for i in range(11)], t.ink, 5, 0.38, LAND, t.land, "hr") + "</g>")
    # the vessel and its fan of survey lines
    vx, vy = 668, 222
    rng = random.Random(9)
    lines = []
    for i in range(9):
        ang = math.radians(-42 + i * 8.2)
        lines.append(ang)
        ex, ey = vx + 600 * math.cos(ang), vy + 600 * math.sin(ang)
        g.append(f'<line x1="{vx}" y1="{vy}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{t.ink}" stroke-width="0.6" stroke-dasharray="1 5" stroke-opacity=".55"/>')
    # soundings appear in order along the lines (lead line over the side, read, next)
    k_ = 0
    total = 9 * 7
    for li, ang in enumerate(lines):
        for j in range(7):
            r = 70 + j * 74 + rng.uniform(-8, 8)
            x, y = vx + r * math.cos(ang), vy + r * math.sin(ang)
            if x > 1236 or y < 46 or y > H - 46 or (x > 960 and y > 300):
                continue
            v = field.value(x, y)
            if v >= LAND * 0.85:
                continue
            depth = int(max(2, (LAND - v) * 38 + rng.uniform(-2, 2)))
            t0 = 0.04 + 0.5 * (k_ / total)
            k_ += 1
            g.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.3f};{t0+0.01:.3f};0.95;1" dur="{LOOP}s" repeatCount="indefinite"/>'
                     + k.text_use(str(depth), x, y + 3, "plex", 9.5, t.ink, anchor="middle", opacity=0.85) + "</g>")
    g.append("</g>")
    b.extend(g)
    b.append(f'<g transform="translate({vx},{vy+6})">{c.boat(t.ink, t.accent, t.ink2, 0.9)}</g>')
    b.append(cap(t, "survey vessel", vx, vy + 30, 9, t.muted, anchor="middle"))
    # instruments, bottom right
    b.append(f'<rect x="976" y="306" width="258" height="64" fill="{t.paper}" fill-opacity=".9"/>')
    b.append(k.text("512", 988, 362, "serif", 46, t.ink, tracking=-1))
    b.append(cap(t, "lead lines over the side", 1062, 362, 8.5, t.muted))
    b.append(cap(t, "write-ahead log", 1062, 328, 8.5, t.muted))
    b.append(wal_tape(t, 1062, 334, 14, LOOP / 2))
    return k.svg(W, H, "".join(b), "rustmapper — survey chart. A vessel sounds the shoal along a fan of survey lines; depths fill in and the contours resolve.", "".join(defs) + k.glyph_defs())


# ---------------------------------------------------------------- ship's log (terminal)
def log(t: Theme) -> str:
    H = 440
    LOOP = 14.0
    FS = 14.5
    cw = k.text_width("x", "plex", FS)
    X0, Y0, LH = 150, 132, 30
    b = [frame(t, W, H)]
    for i in range(10):
        yy = Y0 + 8 + i * LH
        b.append(f'<line x1="36" y1="{yy}" x2="{W-36}" y2="{yy}" stroke="{t.hair}" stroke-width="0.8"/>')
    b.append(f'<line x1="134" y1="100" x2="134" y2="{H-30}" stroke="{t.accent}" stroke-width="1" stroke-opacity=".5"/>')
    b.append(k.text("Log of the rustmapper", 48, 70, "serif-italic", 30, t.ink))
    b.append(cap(t, "Sheet 5  ·  Ship's log  ·  typed live  ·  numbers illustrative, the package is real", W - 44, 66, 9.5, t.muted, anchor="end"))
    b.append(cap(t, "time", 48, 104, 9, t.muted))
    b.append(cap(t, "entry", X0, 104, 9, t.muted))

    def keyt(t0, t1=None):
        t1 = t1 or t0 + 0.02
        return f'keyTimes="0;{t0/LOOP:.4f};{t1/LOOP:.4f};{(LOOP-0.6)/LOOP:.4f};1"'

    def appear(t0):
        return f'<animate attributeName="opacity" values="0;0;1;1;0" {keyt(t0)} dur="{LOOP}s" repeatCount="indefinite"/>'

    defs = []

    def stamp(row, when, t0):
        y = Y0 + row * LH
        return f'<g opacity="0">{appear(t0)}' + k.text_use(when, 48, y, "plex", 12, t.muted) + "</g>"

    def typed(s, row, t0, t1, gid):
        y = Y0 + row * LH
        wid = k.text_width(s, "plex", FS)
        defs.append(f'<clipPath id="{gid}"><rect x="{X0+2*cw:.1f}" y="{y-20}" width="0" height="28">'
                    f'<animate attributeName="width" values="0;0;{wid:.0f};{wid:.0f};0" {keyt(t0, t1)} dur="{LOOP}s" repeatCount="indefinite"/></rect></clipPath>')
        g = (f'<g opacity="0">{appear(t0)}' + k.text_use("$", X0, y, "plex-medium", FS, t.accent) + "</g>"
             + f'<g clip-path="url(#{gid})">' + k.text_use(s, X0 + 2 * cw, y, "plex", FS, t.ink) + "</g>")
        g += (f'<rect y="{y-14}" width="{cw:.1f}" height="18" fill="{t.accent}" opacity="0">'
              f'<animate attributeName="x" values="{X0+2*cw:.1f};{X0+2*cw:.1f};{X0+2*cw+wid:.1f};{X0+2*cw+wid:.1f}" keyTimes="0;{t0/LOOP:.4f};{t1/LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{t0/LOOP:.4f};{(t0+0.01)/LOOP:.4f};{(t1+0.7)/LOOP:.4f};{(t1+0.72)/LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/></rect>')
        return g

    def line(parts, row, t0):
        y = Y0 + row * LH
        x = X0
        out = [f'<g opacity="0">{appear(t0)}']
        for s, col in parts:
            out.append(k.text_use(s, x, y, "plex", FS, col))
            x += k.text_width(s, "plex", FS)
        out.append("</g>")
        return "".join(out)

    b.append(stamp(0, "14:02", 0.4)); b.append(typed("pip install rustmapper", 0, 0.4, 1.6, "lc1"))
    b.append(stamp(1, "14:02", 2.2)); b.append(line([("Successfully installed ", t.muted), ("rustmapper-0.1.3", t.ink)], 1, 2.2))
    b.append(stamp(2, "14:03", 2.9)); b.append(typed("rustmapper crawl --start-url example.com --workers 512", 2, 2.9, 5.0, "lc2"))
    b.append(stamp(3, "14:03", 5.5)); b.append(line([("seeding   ", t.muted), ("sitemap ", t.ink), ("✓", t.ok), ("   ct-logs ", t.ink), ("✓", t.ok), ("   commoncrawl ", t.ink), ("✓", t.ok)], 3, 5.5))
    b.append(stamp(4, "14:03", 6.0)); b.append(line([("frontier  ", t.muted), ("16 shards", t.ink), ("  ·  ", t.muted), ("wal on", t.ink), ("  ·  ", t.muted), ("redis off", t.ink)], 4, 6.0))
    y = Y0 + 5 * LH
    b.append(stamp(5, "14:04", 6.5))
    b.append(f'<g opacity="0">{appear(6.5)}' + k.text_use("crawl     ", X0, y, "plex", FS, t.muted)
             + f'<rect x="{X0+10*cw:.1f}" y="{y-12}" width="{28*cw:.1f}" height="12" rx="2" fill="{t.hair}"/>'
             + f'<rect x="{X0+10*cw:.1f}" y="{y-12}" width="0" height="12" rx="2" fill="{t.accent}">'
             + f'<animate attributeName="width" values="0;0;{28*cw:.1f};{28*cw:.1f}" keyTimes="0;{6.6/LOOP:.4f};{10.6/LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/></rect>'
             + k.text_use("48,213 discovered  ·  512 in flight", X0 + 40 * cw, y, "plex", FS, t.ink2) + "</g>")
    b.append(stamp(6, "14:08", 10.9)); b.append(line([("export    ", t.muted), ("sitemap.xml", t.ink), ("  48,213 urls  ", t.ink2), ("done", t.ok), ("  4m 12s", t.muted)], 6, 10.9))
    y = Y0 + 7 * LH
    b.append(stamp(7, "14:08", 11.6))
    b.append(f'<g opacity="0">{appear(11.6)}' + k.text_use("$", X0, y, "plex-medium", FS, t.accent)
             + f'<rect x="{X0+2*cw:.1f}" y="{y-14}" width="{cw:.1f}" height="18" fill="{t.ink}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    b.append(k.text("Wind light, visibility good. Nothing on fire.", W - 44, H - 42, "serif-italic", 16, t.muted, anchor="end"))
    return k.svg(W, H, "".join(b), "Ship's log: pip install rustmapper; rustmapper crawl --start-url example.com --workers 512; seeding, frontier, crawl, export sitemap.xml.", "".join(defs) + k.glyph_defs())


# ---------------------------------------------------------------- legend (stack)
def legend(t: Theme) -> str:
    cols = [
        ("languages", "anchor", ["Python", "Rust", "Swift", "C", "TypeScript", "SQL"]),
        ("data", "can", ["Scrapy", "Delta Lake", "PostgreSQL", "Redis", "SQLite · GRDB", "Parquet"]),
        ("ops", "light", ["Docker", "Kubernetes", "Prometheus", "Grafana", "GitHub Actions", "tokio"]),
        ("surfaces & ml", "star", ["SwiftUI", "MapKit", "React Native", "MLX", "Qwen", "Ollama"]),
    ]
    rows = max(len(c_[2]) for c_ in cols)
    H = 126 + rows * 26 + 36
    b = [frame(t, W, H)]
    b.append(k.text("Legend & symbols", 48, 70, "serif-italic", 30, t.ink))
    b.append(cap(t, "Sheet 6  ·  what the marks mean  ·  first in each column is the daily driver", W - 44, 66, 9.5, t.muted, anchor="end"))

    def symbol(kind, x, y, strong):
        col = t.accent if strong else t.ink
        if kind == "anchor":
            return anchor_glyph(x, y + 1, col, 0.55)
        if kind == "can":
            return f'<rect x="{x-4}" y="{y-5}" width="8" height="8" rx="1" fill="{col}"/>'
        if kind == "light":
            return f'<path d="M{x-4},{y+4} L{x-2.5},{y-5} H{x+2.5} L{x+4},{y+4} Z" fill="none" stroke="{col}" stroke-width="1.2"/><rect x="{x-2.5}" y="{y-8}" width="5" height="3" fill="{col}"/>'
        d = ""
        for i in range(8):
            a = math.radians(i * 45 - 90)
            r = 6 if i % 2 == 0 else 2.4
            d += ("M" if i == 0 else "L") + f"{x + r*math.cos(a):.1f},{y - 1 + r*math.sin(a):.1f}"
        return f'<path d="{d}Z" fill="{col}"/>'

    for ci, (head, kind, items) in enumerate(cols):
        x = 48 + ci * 298
        b.append(cap(t, head, x, 112, 10, t.ink2))
        b.append(f'<line x1="{x}" y1="122" x2="{x+250}" y2="122" stroke="{t.ink}" stroke-width="0.6" stroke-opacity=".6"/>')
        for i, item in enumerate(items):
            y = 150 + i * 26
            b.append(symbol(kind, x + 7, y - 4, i == 0))
            b.append(k.text_use(item, x + 24, y, "plex-medium" if i == 0 else "plex", 12.5, t.ink if i == 0 else t.ink2))
    return k.svg(W, H, "".join(b), "Legend. Languages: Python, Rust, Swift, C, TypeScript, SQL. Data: Scrapy, Delta Lake, PostgreSQL, Redis, SQLite with GRDB, Parquet. Ops: Docker, Kubernetes, Prometheus, Grafana, GitHub Actions, tokio. Surfaces and ML: SwiftUI, MapKit, React Native, MLX, Qwen, Ollama.", k.glyph_defs())


# ---------------------------------------------------------------- footer · the edge of the chart
def footer(t: Theme) -> str:
    H = 200
    b = [frame(t, W, H)]
    hy = 112
    edge = 1010
    b.append(f'<path d="M40,{hy} H{edge}" stroke="{t.ink}" stroke-width="1.2"/>')
    # the swell
    b.append(f'<path d="M40,{hy+9} ' + " ".join("q24,-5 48,0" if i == 0 else "t48,0" for i in range(21)) +
             f'" fill="none" stroke="{t.ink}" stroke-width="0.8" stroke-opacity=".45">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;-48 0" dur="6s" repeatCount="indefinite"/></path>')
    # the drop
    b.append(f'<path d="M{edge},{hy} q14,2 18,16 v40" fill="none" stroke="{t.ink}" stroke-width="1.2"/>')
    for i in range(6):
        x = edge + 6 + i * 7
        b.append(f'<line x1="{x}" y1="{hy+10+i*2}" x2="{x}" y2="{H-24}" stroke="{t.ink}" stroke-width="0.8" stroke-opacity=".5" stroke-dasharray="3 7">'
                 f'<animate attributeName="stroke-dashoffset" from="0" to="-40" dur="{1.1+i*0.15:.2f}s" repeatCount="indefinite"/></line>')
    for i in range(7):
        b.append(f'<circle cx="{edge + 10 + i*9}" cy="{H-30 - (i%3)*6}" r="1.4" fill="{t.ink}" opacity=".35">'
                 f'<animate attributeName="cy" values="{H-28};{H-44};{H-28}" dur="{2+i*0.3:.1f}s" repeatCount="indefinite"/></circle>')
    # the boat sails toward the edge, and never quite gets there
    b.append(f'<g><animateTransform attributeName="transform" type="translate" values="70 {hy-1};{edge-60} {hy-1}" dur="70s" repeatCount="indefinite"/>'
             f'<g><animateTransform attributeName="transform" type="rotate" values="-2.5;2.5;-2.5" dur="4s" repeatCount="indefinite"/>{c.boat(t.ink, t.accent, t.ink2, 1.0)}</g></g>')
    b.append(k.text("Here be dragons.", W - 44, 72, "serif-italic", 24, t.ink, anchor="end"))
    b.append(cap(t, "the view is best right before the drop", W - 44, 94, 8.5, t.muted, anchor="end"))
    b.append(cap(t, "end of chart  ·  fair winds  ·  thanks for reading this far", 48, H - 44, 9.5, t.muted))
    return k.svg(W, H, "".join(b), "The edge of the chart: a sailboat crosses toward a waterfall it never reaches. Here be dragons.", k.glyph_defs())


BUILDERS = {"hero": hero, "approach-scrapy": approach_scrapy, "survey-rustmapper": survey_rustmapper,
            "log": log, "legend": legend, "footer": footer}



def main(only=None):
    for name, fn in BUILDERS.items():
        if only and name not in only:
            continue
        for t in k.CHART_THEMES:
            k.begin_asset()
            out = fn(t)
            for p in k.check_bounds(W, margin=30):
                print(f"WARNING {name}-{t.name}:", p)
            k.write(os.path.join(OUT, f"{name}-{t.name}.svg"), out)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
