#!/usr/bin/env python3
"""Generate every SVG asset for the profile README, in dark and light.

    python3 scripts/build_assets.py            # writes assets/*.svg

Each asset is emitted twice (assets/<name>-dark.svg, assets/<name>-light.svg) and
the README picks one with <picture> + prefers-color-scheme.
"""
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import svgkit as k  # noqa: E402
from svgkit import Theme  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "assets")
W = 1280  # canvas width shared by every asset; README shows them at 100%

MONO = "mono"


def label(t: Theme, s: str, x: float, y: float, fill: str | None = None, size: float = 11.5,
          anchor: str = "start", opacity: float | None = None) -> str:
    """Small tracked mono caption."""
    return k.text(s.upper(), x, y, MONO, size, fill or t.muted, anchor=anchor, tracking=1.6, opacity=opacity)


def dot(t: Theme, x: float, y: float, r: float = 4, pulse: bool = True, dur: float = 2.6) -> str:
    anim = (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t.accent}" opacity=".35">'
            f'<animate attributeName="r" values="{r};{r*3};{r}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".35;0;.35" dur="{dur}s" repeatCount="indefinite"/></circle>') if pulse else ""
    return anim + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t.accent}"/>'


# ---------------------------------------------------------------- hero
def hero(t: Theme) -> str:
    H = 440
    defs, grid = k.dot_grid(t, 760, 20, 520, 400, step=22, r=1.1, gid="hg")
    b = [grid]

    # eyebrow
    b.append(dot(t, 54, 64, r=3.5))
    b.append(label(t, "Benjamin S. Russell  ·  full-stack developer  ·  scraping enthusiast", 70, 68, t.ink2))

    # name
    b.append(k.text("Ben Russell", 46, 196, "display", 124, t.ink, tracking=-5))

    # tagline
    b.append(k.text("I build crawlers that survive the open web,", 50, 250, "text-medium", 23, t.ink2, tracking=-0.3))
    b.append(k.text("and the systems that make sense of what they bring back.", 50, 282, "text-medium", 23, t.ink2, tracking=-0.3))

    # meta row
    y = 352
    x = 50
    items = [("rustmapper", "on PyPI"), ("Scrapy", "pipeline platform"), ("Python · Rust · Swift · C", "daily drivers")]
    for head, sub in items:
        b.append(k.text(head, x, y, "text-semi", 15, t.ink, tracking=-0.2))
        b.append(k.text(sub, x, y + 20, "text", 13, t.muted))
        x += max(k.text_width(head, "text-semi", 15), k.text_width(sub, "text", 13)) + 44
        if head != items[-1][0]:
            b.append(f'<rect x="{x-22}" y="{y-14}" width="1" height="38" fill="{t.hair}"/>')

    # ---- right panel: the web, parsed into rows
    rng = random.Random(27)
    nodes = []
    for i in range(13):
        ang = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(26, 118)
        nodes.append((round(905 + rad * math.cos(ang), 1), round(222 + rad * 0.95 * math.sin(ang), 1)))
    edges = set()
    for i, (x1, y1) in enumerate(nodes):
        near = sorted(range(len(nodes)), key=lambda j: (nodes[j][0]-x1)**2 + (nodes[j][1]-y1)**2)[1:3]
        for j in near:
            edges.add(tuple(sorted((i, j))))
    for i, j in sorted(edges):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t.hair}" stroke-width="1.2"/>')
    # pulse path wandering the tangle
    order = [0, 4, 7, 2, 9, 5, 11, 1, 8, 3, 12, 6, 10, 0]
    pd = "M" + " L".join(f"{nodes[i][0]},{nodes[i][1]}" for i in order)
    b.append(f'<path d="{pd}" fill="none" stroke="{t.accent}" stroke-width="1.3" stroke-opacity=".32" stroke-dasharray="5 11">'
             f'<animate attributeName="stroke-dashoffset" from="0" to="-160" dur="9s" repeatCount="indefinite"/></path>')
    for i, (x, y) in enumerate(nodes):
        b.append(f'<circle cx="{x}" cy="{y}" r="4.2" fill="{t.field}" stroke="{t.ink2}" stroke-width="1.3">'
                 f'<animate attributeName="stroke" values="{t.ink2};{t.accent};{t.ink2}" begin="{(i*0.61)%8:.2f}s" dur="8s" repeatCount="indefinite"/></circle>')
    b.append(f'<circle r="5" fill="{t.accent}"><animateMotion dur="9s" repeatCount="indefinite" path="{pd}"/></circle>')
    b.append(label(t, "the open web", 905, 372, anchor="middle"))

    # funnel into the parser
    px, py = 1046, 222
    for yy in (150, 222, 294):
        b.append(f'<path d="M1012,{yy} C1030,{yy} 1026,{py} {px-14},{py}" fill="none" stroke="{t.hair}" stroke-width="1.2"/>')
    b.append(f'<rect x="{px-14}" y="{py-14}" width="28" height="28" rx="7" fill="{t.panel}" stroke="{t.ink2}" stroke-width="1.3"/>')
    b.append(f'<path d="M{px-6},{py} h12 M{px},{py-6} v12" stroke="{t.accent}" stroke-width="2" stroke-linecap="round">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {px} {py}" to="90 {px} {py}" dur="3s" repeatCount="indefinite"/></path>')
    b.append(label(t, "parse", px, 372, anchor="middle"))

    # rows
    rx = 1092
    row_y0 = 136
    n = 8
    for i in range(n):
        y = row_y0 + i * 24
        t0 = 0.12 + i * 0.075
        t1 = t0 + 0.05
        anim = (f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.3f};{t1:.3f};0.92;1" dur="8s" repeatCount="indefinite"/>')
        w1 = 26 + (i * 37) % 40
        w2 = 60 + (i * 53) % 46
        b.append(f'<g opacity="0">{anim}'
                 f'<rect x="{rx}" y="{y}" width="14" height="12" rx="3" fill="{t.accent}"/>'
                 f'<rect x="{rx+20}" y="{y}" width="{w1}" height="12" rx="3" fill="{t.ink2}" opacity=".75"/>'
                 f'<rect x="{rx+26+w1}" y="{y}" width="{w2}" height="12" rx="3" fill="{t.hair}"/>'
                 f'</g>')
    b.append(f'<path d="M{px+14},{py} H{rx-16}" stroke="{t.hair}" stroke-width="1.2"/>')
    b.append(f'<circle r="3" fill="{t.ok}"><animateMotion dur="2s" repeatCount="indefinite" path="M{px+14},{py} H{rx-16}"/></circle>')
    b.append(label(t, "trusted rows", rx + 72, 372, anchor="middle"))

    return k.svg(W, H, "".join(b), "Ben Russell — I build crawlers that survive the open web", defs)


# ---------------------------------------------------------------- shared card chrome
def chip(t: Theme, s: str, x: float, y: float, accent: bool = False) -> tuple[str, float]:
    """Rounded chip with mono label; returns (svg, width)."""
    pad = 10
    w = k.text_width(s, MONO, 11, 0.6) + pad * 2
    stroke = t.accent if accent else t.hair
    fill = t.ink if accent else t.ink2
    out = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="{t.panel}" stroke="{stroke}" stroke-width="1"/>'
           + k.text(s, x + pad, y + 16, MONO, 11, fill, tracking=0.6))
    return out, w


def chips(t: Theme, items: list[str], x: float, y: float, accent_first: bool = False, gap: float = 8,
          max_x: float | None = None) -> str:
    out = []
    x0 = x
    for i, s in enumerate(items):
        c, w = chip(t, s, x, y, accent=(accent_first and i == 0))
        if max_x and x + w > max_x and x > x0:
            x, y = x0, y + 32
            c, w = chip(t, s, x, y, accent=(accent_first and i == 0))
        out.append(c)
        x += w + gap
    return "".join(out)


def card_left(t: Theme, index: str, title: str, lines: list[str], tags: list[str], y_title: float = 112) -> str:
    b = [label(t, f"featured  ·  {index}", 52, 58, t.accent)]
    b.append(k.text(title, 48, y_title, "display", 58, t.ink, tracking=-2.2))
    y = y_title + 40
    for ln in lines:
        b.append(k.text(ln, 50, y, "text", 17, t.ink2, tracking=-0.1))
        y += 25
    b.append(chips(t, tags, 50, y + 10, accent_first=True, max_x=690))
    return "".join(b)


# ---------------------------------------------------------------- Scrapy card
def card_scrapy(t: Theme) -> str:
    H = 318
    defs, grid = k.dot_grid(t, 700, 10, 580, 298, step=22, gid="sg")
    b = [grid]
    b.append(card_left(t, "01", "Scrapy", [
        "A multi-stage crawler platform: discover, analyze, summarize,",
        "land it in Delta Lake. Dashboards and circuit breakers included,",
        "because a crawler you cannot watch is a crawler you cannot trust.",
    ], ["Python 3.11", "Scrapy", "Delta Lake", "PostgreSQL", "Redis", "Prometheus", "Grafana", "Docker · K8s"]))

    # pipeline diagram
    stages = ["urls", "scout", "analyze", "summarize", "delta lake"]
    x0, x1, yy = 762, 1212, 128
    n = len(stages)
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    b.append(f'<path d="M{xs[0]},{yy} H{xs[-1]}" stroke="{t.hair}" stroke-width="1.4"/>')
    for i, (x, name) in enumerate(zip(xs, stages)):
        last = i == n - 1
        if i == 0:
            # a loose bundle of urls
            for j in range(3):
                b.append(f'<path d="M{x-26+j*6},{yy-34+j*10} q18,-6 36,0" fill="none" stroke="{t.cool}" stroke-width="1.4" stroke-opacity=".8"/>')
            b.append(f'<circle cx="{x}" cy="{yy}" r="9" fill="{t.panel}" stroke="{t.cool}" stroke-width="1.6"/>')
        elif last:
            b.append(f'<rect x="{x-16}" y="{yy-16}" width="32" height="32" rx="8" fill="{t.panel}" stroke="{t.ok}" stroke-width="1.6"/>')
            for j in range(3):
                b.append(f'<rect x="{x-9}" y="{yy-8+j*6}" width="18" height="3" rx="1.5" fill="{t.ok}" opacity="{.45+.25*j:.2f}"/>')
        else:
            b.append(f'<rect x="{x-14}" y="{yy-14}" width="28" height="28" rx="7" fill="{t.panel}" stroke="{t.ink2}" stroke-width="1.4"/>')
            b.append(f'<circle cx="{x}" cy="{yy}" r="3" fill="{t.accent}">'
                     f'<animate attributeName="opacity" values="1;.25;1" begin="{i*0.5}s" dur="2s" repeatCount="indefinite"/></circle>')
        b.append(label(t, name, x, yy + 44, anchor="middle"))
        # tiny throughput meter under each stage
        if 0 < i < n - 1:
            b.append(f'<rect x="{x-20}" y="{yy+56}" width="40" height="3" rx="1.5" fill="{t.hair}"/>'
                     f'<rect x="{x-20}" y="{yy+56}" width="40" height="3" rx="1.5" fill="{t.accent}">'
                     f'<animate attributeName="width" values="8;40;16;34;8" dur="{5+i}s" repeatCount="indefinite"/></rect>')
    # packets travelling the line
    for d in (0, 2.3, 4.1):
        b.append(f'<circle r="4" fill="{t.accent}"><animateMotion dur="6.5s" begin="{d}s" repeatCount="indefinite" path="M{xs[0]},{yy} H{xs[-1]}"/></circle>')
    # monitoring strip: sparkline + 'breaker closed'
    sx, sy = 760, 238
    rng = random.Random(7)
    pts = [(sx + i * 10, sy - rng.uniform(0, 14)) for i in range(25)]
    d = "M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in pts)
    b.append(f'<path d="{d}" fill="none" stroke="{t.ink2}" stroke-width="1.3" stroke-linejoin="round" stroke-opacity=".8"/>')
    b.append(f'<path d="{d}" fill="none" stroke="{t.accent}" stroke-width="1.3" stroke-dasharray="260 260">'
             f'<animate attributeName="stroke-dashoffset" from="260" to="-260" dur="7s" repeatCount="indefinite"/></path>')
    b.append(label(t, "requests / s", sx, sy + 26))
    b.append(f'<circle cx="1066" cy="{sy-6}" r="4" fill="{t.ok}"/>')
    b.append(label(t, "breaker closed", 1078, sy - 2, t.ink2))
    b.append(label(t, "prometheus · grafana", 1062, sy + 26))
    return k.svg(W, H, "".join(b), "Scrapy — discover, analyze, summarize, store", defs)


# ---------------------------------------------------------------- rustmapper card
def card_rustmapper(t: Theme) -> str:
    H = 318
    defs, grid = k.dot_grid(t, 700, 10, 580, 298, step=22, gid="rg")
    b = [grid]
    b.append(card_left(t, "02", "rustmapper", [
        "A concurrent sitemap crawler in Rust: up to 512 adaptive workers,",
        "a sharded frontier, write-ahead persistence, optional Redis for",
        "distributed runs. Seeds from sitemaps, CT logs and Common Crawl.",
    ], ["pip install rustmapper", "Rust 2024", "tokio", "reqwest", "redb", "rkyv", "maturin"]))

    # tree fan-out: root -> 4 -> 12
    rx, ry = 778, 150
    b.append(f'<circle cx="{rx}" cy="{ry}" r="9" fill="{t.panel}" stroke="{t.accent}" stroke-width="1.8"/>')
    b.append(f'<circle cx="{rx}" cy="{ry}" r="3" fill="{t.accent}"/>')
    mids = [(900, 66), (900, 122), (900, 178), (900, 234)]
    leaves_x = 1010
    paths = []
    for i, (mx, my) in enumerate(mids):
        d = f"M{rx+9},{ry} C{rx+60},{ry} {mx-60},{my} {mx-7},{my}"
        paths.append(d)
        b.append(f'<path d="{d}" fill="none" stroke="{t.hair}" stroke-width="1.4"/>')
        b.append(f'<circle cx="{mx}" cy="{my}" r="6" fill="{t.panel}" stroke="{t.ink2}" stroke-width="1.4"/>')
        for j in range(3):
            ly = my - 16 + j * 16
            d2 = f"M{mx+6},{my} C{mx+40},{my} {leaves_x-40},{ly} {leaves_x-4},{ly}"
            b.append(f'<path d="{d2}" fill="none" stroke="{t.hair}" stroke-width="1.2"/>')
            b.append(f'<circle cx="{leaves_x}" cy="{ly}" r="3.2" fill="{t.ink2}" opacity=".9"/>')
            paths.append(d2)
    for i, d in enumerate(paths):
        b.append(f'<circle r="3" fill="{t.accent}"><animateMotion dur="{2.4 + (i*0.37)%1.6:.2f}s" begin="{(i*0.53)%2.2:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
    b.append(label(t, "root", rx, ry + 32, anchor="middle"))
    b.append(label(t, "shards", 900, 262, anchor="middle"))
    b.append(label(t, "discovered", leaves_x + 8, 262, anchor="middle"))

    # worker meter
    wx, wy = 1062, 64
    cols, rows = 16, 4
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            x = wx + c * 10
            y = wy + r * 10
            b.append(f'<rect x="{x}" y="{y}" width="7" height="7" rx="1.5" fill="{t.accent}" opacity=".18">'
                     f'<animate attributeName="opacity" values=".18;1;.18" begin="{(i*0.09)%3.4:.2f}s" dur="3.4s" repeatCount="indefinite"/></rect>')
    b.append(k.text("512", wx, wy + 72, "display-semi", 26, t.ink, tracking=-1))
    b.append(label(t, "adaptive workers", wx + 48, wy + 72))
    # WAL strip
    b.append(label(t, "wal", wx, 178))
    for i in range(14):
        b.append(f'<rect x="{wx + 34 + i*11}" y="170" width="8" height="9" rx="1.5" fill="{t.ok}" opacity=".25">'
                 f'<animate attributeName="opacity" values=".25;.25;1;1" keyTimes="0;{i/14:.3f};{(i+1)/14:.3f};1" dur="5s" repeatCount="indefinite"/></rect>')
    b.append(label(t, "seeds", wx, 212))
    b.append(k.text("sitemaps · CT logs · Common Crawl", wx, 234, "text-medium", 12.5, t.ink2))
    return k.svg(W, H, "".join(b), "rustmapper — concurrent sitemap crawler in Rust", defs)


# ---------------------------------------------------------------- terminal
def terminal(t: Theme) -> str:
    H = 392
    LOOP = 14.0
    FS = 15.5
    cw = k.text_width("x", MONO, FS)  # mono advance
    X0, Y0 = 44, 96
    LH = 28
    b = []
    # window
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{t.panel2}" stroke="{t.hair}"/>')
    b.append(f'<path d="M0.5,52 H{W-0.5}" stroke="{t.hair}"/>')
    for i, c in enumerate((t.accent, t.muted, t.ok)):
        b.append(f'<circle cx="{28 + i*22}" cy="27" r="6" fill="{c}" opacity=".9"/>')
    b.append(label(t, "ben@studio  —  rustmapper  —  a typical afternoon", W / 2, 31, anchor="middle"))

    def keyt(t0: float, t1: float | None = None):
        t1 = t1 or t0 + 0.02
        return f'keyTimes="0;{t0/LOOP:.4f};{t1/LOOP:.4f};{(LOOP-0.6)/LOOP:.4f};1"'

    def appear(t0: float) -> str:
        return f'<animate attributeName="opacity" values="0;0;1;1;0" {keyt(t0)} dur="{LOOP}s" repeatCount="indefinite"/>'

    def typed(s: str, row: int, t0: float, t1: float, gid: str) -> str:
        """Prompt + command revealed left-to-right between t0 and t1."""
        y = Y0 + row * LH
        wid = k.text_width(s, MONO, FS)
        clip = (f'<clipPath id="{gid}"><rect x="{X0+2*cw}" y="{y-20}" width="0" height="28">'
                f'<animate attributeName="width" values="0;0;{wid:.0f};{wid:.0f};0" {keyt(t0, t1)} dur="{LOOP}s" repeatCount="indefinite"/></rect></clipPath>')
        g = (f'<g opacity="0">{appear(t0)}' + k.text("$", X0, y, "mono-bold", FS, t.accent) + "</g>"
             + f'<g clip-path="url(#{gid})">' + k.text(s, X0 + 2 * cw, y, MONO, FS, t.ink) + "</g>")
        # cursor block that follows the typing then parks
        g += (f'<rect y="{y-15}" width="{cw:.1f}" height="19" fill="{t.accent}" opacity="0">'
              f'<animate attributeName="x" values="{X0+2*cw:.1f};{X0+2*cw:.1f};{X0+2*cw+wid:.1f};{X0+2*cw+wid:.1f}" keyTimes="0;{t0/LOOP:.4f};{t1/LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{t0/LOOP:.4f};{(t0+0.01)/LOOP:.4f};{(t1+0.7)/LOOP:.4f};{(t1+0.72)/LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/></rect>')
        return clip, g

    def line(parts: list[tuple[str, str]], row: int, t0: float) -> str:
        """Output line made of (text, colour) runs."""
        y = Y0 + row * LH
        x = X0
        out = [f'<g opacity="0">{appear(t0)}']
        for s, col in parts:
            out.append(k.text(s, x, y, MONO, FS, col))
            x += k.text_width(s, MONO, FS)
        out.append("</g>")
        return "".join(out)

    defs = []
    c1, g1 = typed("pip install rustmapper", 0, 0.4, 1.6, "tc1")
    defs.append(c1); b.append(g1)
    b.append(line([("Successfully installed ", t.muted), ("rustmapper-0.1.3", t.ink)], 1, 2.2))
    c2, g2 = typed("rustmapper crawl --start-url example.com --workers 512", 2, 2.9, 5.0, "tc2")
    defs.append(c2); b.append(g2)
    b.append(line([("seeding   ", t.muted), ("sitemap ", t.ink), ("✓", t.ok), ("   ct-logs ", t.ink), ("✓", t.ok), ("   commoncrawl ", t.ink), ("✓", t.ok)], 3, 5.5))
    b.append(line([("frontier  ", t.muted), ("16 shards", t.ink), ("  ·  ", t.muted), ("wal on", t.ink), ("  ·  ", t.muted), ("redis off", t.ink)], 4, 6.0))
    # progress bar line
    y = Y0 + 5 * LH
    b.append(f'<g opacity="0">{appear(6.5)}' + k.text("crawl     ", X0, y, MONO, FS, t.muted)
             + f'<rect x="{X0+10*cw:.1f}" y="{y-13}" width="{28*cw:.1f}" height="14" rx="3" fill="{t.hair}"/>'
             + f'<rect x="{X0+10*cw:.1f}" y="{y-13}" width="0" height="14" rx="3" fill="{t.accent}">'
             + f'<animate attributeName="width" values="0;0;{28*cw:.1f};{28*cw:.1f}" keyTimes="0;{6.6/LOOP:.4f};{10.6/LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/></rect>'
             + k.text("48,213 discovered  ·  512 in flight", X0 + 40 * cw, y, MONO, FS, t.ink2) + "</g>")
    b.append(line([("export    ", t.muted), ("sitemap.xml", t.ink), ("  48,213 urls  ", t.ink2), ("done", t.ok), ("  4m 12s", t.muted)], 6, 10.9))
    # closing prompt with blinking cursor
    y = Y0 + 7 * LH
    b.append(f'<g opacity="0">{appear(11.6)}' + k.text("$", X0, y, "mono-bold", FS, t.accent)
             + f'<rect x="{X0+2*cw:.1f}" y="{y-15}" width="{cw:.1f}" height="19" fill="{t.ink}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    b.append(label(t, "numbers are illustrative · the package is real", W - 44, H - 22, anchor="end", opacity=.9))
    return k.svg(W, H, "".join(b), "terminal: pip install rustmapper; rustmapper crawl --start-url example.com --workers 512", "".join(defs))


# ---------------------------------------------------------------- stack
def stack(t: Theme) -> str:
    cols = [
        ("languages", ["Python", "Rust", "Swift", "C", "TypeScript", "SQL"]),
        ("data", ["Scrapy", "Delta Lake", "PostgreSQL", "Redis", "SQLite · GRDB", "Parquet"]),
        ("ops", ["Docker", "Kubernetes", "Prometheus", "Grafana", "GitHub Actions", "tokio"]),
        ("surfaces & ml", ["SwiftUI", "MapKit", "React Native", "MLX", "Qwen", "Ollama"]),
    ]
    colw = (W - 96) / 4
    H = 150
    b = []
    for ci, (head, items) in enumerate(cols):
        x = 48 + ci * colw
        b.append(dot(t, x + 4, 48, r=3, pulse=False))
        b.append(label(t, head, x + 16, 52, t.ink2))
        b.append(f'<path d="M{x},68 H{x+colw-24}" stroke="{t.hair}"/>')
        # flow chips, wrapping within column
        cx, cy = x, 86
        for i, s in enumerate(items):
            c, w = chip(t, s, cx, cy, accent=(i == 0))
            if cx + w > x + colw - 24 and cx > x:
                cy += 32
                cx = x
                c, w = chip(t, s, cx, cy, accent=(i == 0))
            b.append(c)
            cx += w + 8
    return k.svg(W, H, "".join(b), "Stack: Python, Rust, Swift, C, TypeScript; Scrapy, Delta Lake, PostgreSQL, Redis; Docker, Kubernetes, Prometheus, Grafana; SwiftUI, React Native, MLX")


# ---------------------------------------------------------------- footer with a small sailboat
def footer(t: Theme) -> str:
    H = 150
    b = []
    hy = 96
    b.append(f'<path d="M48,{hy} H{W-48}" stroke="{t.hair}" stroke-width="1.2"/>')
    # a slow swell under the horizon
    b.append(f'<path d="M48,{hy+10} q24,-5 48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0 t48,0" '
             f'fill="none" stroke="{t.hair}" stroke-width="1" stroke-opacity=".8">'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;-48 0" dur="6s" repeatCount="indefinite"/></path>')
    # boat: hull + two sails, drifting across the whole footer
    boat = (f'<path d="M-22,0 L22,0 L15,9 L-15,9 Z" fill="{t.ink}"/>'
            f'<path d="M0,-2 V-46" stroke="{t.ink}" stroke-width="1.6"/>'
            f'<path d="M2,-44 L30,-4 L2,-4 Z" fill="{t.accent}"/>'
            f'<path d="M-2,-34 L-20,-4 L-2,-4 Z" fill="{t.ink2}"/>')
    b.append(f'<g><animateTransform attributeName="transform" type="translate" values="60 {hy-2};{W-60} {hy-2}" dur="75s" repeatCount="indefinite"/>'
             f'<g><animateTransform attributeName="transform" type="rotate" values="-2.5;2.5;-2.5" dur="4s" repeatCount="indefinite"/>{boat}</g></g>')
    b.append(k.text("Fair winds. Thanks for reading this far.", W / 2, 136, "text-medium", 14, t.muted, anchor="middle"))
    return k.svg(W, H, "".join(b), "A small sailboat crossing a horizon line. Fair winds.")


BUILDERS = {"hero": hero, "card-scrapy": card_scrapy, "card-rustmapper": card_rustmapper,
            "terminal": terminal, "stack": stack, "footer": footer}


def main(only: list[str] | None = None) -> None:
    for name, fn in BUILDERS.items():
        if only and name not in only:
            continue
        for t in k.THEMES:
            k.write(os.path.join(OUT, f"{name}-{t.name}.svg"), fn(t))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
