"""furniture.py — stroke(), Jitter, frame, margin graticule, rose, source diagram, area key, paper,
course and survey geometry (T6 §2.5, §2.7; MASTERPLAN §3.2).

Text is never drawn here: every function that letters something takes a `label_cb`
(`label_cb(text, x, y, role, **kw) -> str`) and returns the svg it produced. Colour comes from
tokens.Theme; widths from tokens.W; dashes from tokens.DASH. `stroke()` is the only emitter of
stroke attributes, so the build can assert every stroke-width is one of W's four.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from tokens import W, DASH, INK  # noqa: E402

from .field import fmt, polygon_area, clip_polyline

__all__ = ["Jitter", "stroke", "op", "frame", "margin_graticule", "two_ring_rose", "Zone", "source_diagram",
           "area_key", "paper", "plate_mark", "course", "course_samples", "compass_bearing", "lateral_offset",
           "track_lines", "check_lines", "restricted_line", "catmull_rom", "polyline_at"]


# ------------------------------------------------------------------ randomness
class Jitter:
    """The one randomness source. Keyed by sheet and element (`Jitter(seed, "hero/danger/3")`),
    never by data, so identical inputs give byte-identical output. String seeds hash with sha512
    in CPython, so the stream is stable across processes."""

    def __init__(self, seed, name: str):
        self.seed, self.name = seed, name
        self._rng = random.Random(f"{seed}:{name}")

    def uniform(self, a: float, b: float) -> float:
        return self._rng.uniform(a, b)

    def gauss(self, mu: float, sigma: float) -> float:
        return self._rng.gauss(mu, sigma)

    def choice(self, seq):
        return self._rng.choice(seq)

    def offset(self, limit: float) -> float:
        return self._rng.uniform(-limit, limit)

    def phase(self, period: float) -> float:
        return self._rng.uniform(0, period)

    def sub(self, name: str) -> "Jitter":
        return Jitter(self.seed, f"{self.name}/{name}")


# ------------------------------------------------------------------ the one stroke emitter
def op(v: float) -> str:
    """Opacity to two decimals, no leading zero: .55"""
    s = f"{v:.2f}"
    return s[1:] if s.startswith("0") else s


def stroke(width_key: str, color: str, opacity: float | None = None, dash_key: str | None = None,
           jit: Jitter | None = None, caps: str = "round", gap: float | None = None) -> str:
    """stroke attributes. width_key ∈ W; dash_key ∈ DASH ('{g}' filled by `gap` or jit ∈ U(4.0, 4.6));
    with `jit`, a seeded stroke-dashoffset so nothing is in phase."""
    if width_key not in W:
        raise KeyError(f"stroke width {width_key!r} not in tokens.W")
    parts = [f'stroke="{color}"', f'stroke-width="{W[width_key]}"']
    if caps:
        parts.append(f'stroke-linecap="{caps}" stroke-linejoin="round"')
    if opacity is not None and opacity < 1:
        parts.append(f'stroke-opacity="{op(opacity)}"')
    if dash_key:
        if dash_key not in DASH:
            raise KeyError(f"dash {dash_key!r} not in tokens.DASH")
        d = DASH[dash_key]
        if "{g}" in d:
            g = gap if gap is not None else (jit.uniform(4.0, 4.6) if jit else 4.3)
            d = d.format(g=f"{g:.1f}")
        parts.append(f'stroke-dasharray="{d}"')
        if jit is not None:
            period = sum(float(t) for t in d.split())
            parts.append(f'stroke-dashoffset="{jit.phase(period):.1f}"')
    return " ".join(parts)


def _path(d: str, attrs: str, fill: str = "none") -> str:
    return f'<path d="{d}" fill="{fill}" {attrs}/>'


# ------------------------------------------------------------------ frame
def _side_runs(side: str, w: int, h: int, inset: float, gaps):
    """Line runs for one side of a rectangle inset by `inset`, minus gaps [(side, a, b)]."""
    if side in ("top", "bottom"):
        y = inset if side == "top" else h - inset
        lo, hi = inset, w - inset
        axis = lambda t: (t, y)
    else:
        x = inset if side == "left" else w - inset
        lo, hi = inset, h - inset
        axis = lambda t: (x, t)
    cuts = sorted((max(lo, a), min(hi, b)) for s, a, b in gaps if s == side)
    runs, cur = [], lo
    for a, b in cuts:
        if a > cur:
            runs.append((axis(cur), axis(a)))
        cur = max(cur, b)
    if cur < hi:
        runs.append((axis(cur), axis(hi)))
    return runs


def frame(w: int, h: int, theme, kind: str = "minute-bars", gaps=(), rules=(18, 24), bar: int = 20) -> str:
    """Neat line. kind: 'minute-bars' (outer LINE rule, inner HAIR rule, alternating bars between),
    'double' (two rules), 'none' (''), 'broken' (minute bars with gaps=[(side, a, b)] where the
    sheet's water leaves the page). rules=(outer inset, inner inset)."""
    if kind == "none":
        return ""
    r0, r1 = rules
    out = []
    sides = ("top", "right", "bottom", "left")
    gaps = list(gaps) if kind == "broken" else []
    for inset, key, o in ((r0, "LINE", 0.9), (r1, "HAIR", 0.6)):
        d = []
        for s in sides:
            for (ax, ay), (bx, by) in _side_runs(s, w, h, inset, gaps):
                d.append(f"M{fmt(ax)} {fmt(ay)}L{fmt(bx)} {fmt(by)}")
        out.append(_path("".join(d), stroke(key, theme.ink, o, caps="butt")))
    if kind in ("minute-bars", "broken"):
        band = r1 - r0
        d = []
        # top & bottom bars
        for y in (r0, h - r1):
            i = 0
            x = r1
            while x + bar <= w - r1:
                if i % 2 == 0 and not any(s in ("top", "bottom") and (y < h / 2) == (s == "top") and a < x + bar and b > x
                                           for s, a, b in gaps):
                    d.append(f"M{fmt(x)} {fmt(y)}h{bar}v{fmt(band)}h-{bar}z")
                x += bar
                i += 1
        for x in (r0, w - r1):
            i = 0
            y = r1
            while y + bar <= h - r1:
                if i % 2 == 0 and not any(s in ("left", "right") and (x < w / 2) == (s == "left") and a < y + bar and b > y
                                           for s, a, b in gaps):
                    d.append(f"M{fmt(x)} {fmt(y)}h{fmt(band)}v{bar}h-{fmt(band)}z")
                y += bar
                i += 1
        out.append(f'<path d="{"".join(d)}" fill="{theme.ink}" fill-opacity="{op(0.85)}"/>')
    return "".join(out)


def margin_graticule(rect, meridians, parallels, theme, label_cb=None, tick: int = 6) -> str:
    """Two labelled meridians and parallels at the margin only (no interior grid, T6 10).
    rect = the neat rect (x, y, w, h); meridians = [(x, label)], parallels = [(y, label)]."""
    x0, y0, w, h = rect
    d = []
    labels = []
    for x, lab in meridians:
        d.append(f"M{fmt(x)} {fmt(y0)}v-{tick}M{fmt(x)} {fmt(y0 + h)}v{tick}")
        if label_cb and lab:
            labels.append(label_cb(lab, x, y0 - tick - 3, "label", anchor="middle"))
    for y, lab in parallels:
        d.append(f"M{fmt(x0)} {fmt(y)}h-{tick}M{fmt(x0 + w)} {fmt(y)}h{tick}")
        if label_cb and lab:
            labels.append(label_cb(lab, x0 - tick - 3, y + 4, "label", anchor="end"))
    return _path("".join(d), stroke("HAIR", theme.ink, 0.6, caps="butt")) + "".join(labels)


# ------------------------------------------------------------------ rose
def two_ring_rose(cx, cy, r, theme, hours24, modal: int, var_label_cb=None, label_cb=None) -> str:
    """Two-ring rose as a 24-hour clock in author-local time (T6 13, T2 §2.5). Outer: true ring with
    10°/30° ticks, accent arrowhead at 000, 'N'. Inner: 24 bars inward with length ∝ hours24[h],
    00 at the top, numerals 00/06/12/18, one BRUSH variation arrow from the centre to the modal hour.
    No rotation of the dial. var_label_cb(x, y) -> str sets the VAR line under the rose."""
    out = [f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="none" {stroke("PEN", theme.ink, 0.8)}/>']
    small, big = [], []
    for deg in range(0, 360, 10):
        a = math.radians(deg - 90)
        L = 11 if deg % 30 == 0 else 6
        (big if deg % 30 == 0 else small).append(
            f"M{fmt(cx + (r - L) * math.cos(a))} {fmt(cy + (r - L) * math.sin(a))}"
            f"L{fmt(cx + r * math.cos(a))} {fmt(cy + r * math.sin(a))}")
    out.append(_path("".join(small), stroke("HAIR", theme.ink, 0.7, caps="butt")))
    out.append(_path("".join(big), stroke("PEN", theme.ink, 0.8, caps="butt")))
    out.append(f'<path d="M{fmt(cx)} {fmt(cy - r - 2)}l-5 -11h10z" fill="{theme.accent}"/>')
    if label_cb:
        out.append(label_cb("N", cx, cy - r - 17, "label", anchor="middle"))
    ri = r - 22
    out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(ri)}" fill="none" {stroke("HAIR", theme.ink, 0.6)}/>')
    vals = list(hours24) if hours24 else []
    mx = max(vals) if vals else 0
    if mx > 0:
        bars = []
        for hh in range(24):
            a = math.radians(hh * 15 - 90)
            L = 4 + (ri - 14) * (vals[hh] / mx)
            bars.append(f"M{fmt(cx + (ri - 3) * math.cos(a))} {fmt(cy + (ri - 3) * math.sin(a))}"
                        f"L{fmt(cx + (ri - 3 - L) * math.cos(a))} {fmt(cy + (ri - 3 - L) * math.sin(a))}")
        out.append(_path("".join(bars), stroke("LINE", theme.ink, 0.7, caps="butt")))
        # variation arrow: centre -> modal hour
        a = math.radians(modal * 15 - 90)
        tip = (cx + (ri - 6) * math.cos(a), cy + (ri - 6) * math.sin(a))
        out.append(_path(f"M{fmt(cx)} {fmt(cy)}L{fmt(tip[0])} {fmt(tip[1])}", stroke("BRUSH", theme.ink, 0.9)))
        hx, hy = math.cos(a), math.sin(a)
        head = (f"M{fmt(tip[0])} {fmt(tip[1])}"
                f"L{fmt(tip[0] - 8 * hx + 4 * hy)} {fmt(tip[1] - 8 * hy - 4 * hx)}"
                f"L{fmt(tip[0] - 8 * hx - 4 * hy)} {fmt(tip[1] - 8 * hy + 4 * hx)}Z")
        out.append(f'<path d="{head}" fill="{theme.ink}"/>')
    if label_cb:
        for hh in (0, 6, 12, 18):
            a = math.radians(hh * 15 - 90)
            rr = ri + 9
            out.append(label_cb(f"{hh:02d}", cx + rr * math.cos(a), cy + rr * math.sin(a) + 4, "label", anchor="middle"))
    out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="2" fill="{theme.ink}"/>')
    if var_label_cb:
        out.append(var_label_cb(cx, cy + r + 30))
    return "".join(out)


# ------------------------------------------------------------------ source diagram / zones of confidence
@dataclass
class Zone:
    letter: str
    poly: list          # [(fx, fy)] fractions of the panel, convex
    density: float = 0.5  # 0..1 → hatch spacing 14 → 5 px


def _clip_seg_convex(a, b, poly):
    """Cyrus–Beck clip of segment a→b to a convex polygon; None if outside."""
    t0, t1 = 0.0, 1.0
    n = len(poly)
    sign = 1.0 if polygon_area(poly) > 0 else -1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        # inward normal
        nx, ny = -ey * sign, ex * sign
        num = nx * (a[0] - p[0]) + ny * (a[1] - p[1])
        den = nx * dx + ny * dy
        if abs(den) < 1e-12:
            if num < 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return ((a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1))


def hatch_lines(poly, spacing: float, angle: float, jit: Jitter | None, overshoot: float = 2.0,
                angle_jitter: float = 1.5, spacing_jitter: float = 0.12):
    """Generated hatch lines clipped to a convex polygon: [((x0,y0),(x1,y1), opacity)].
    Varying per line, never along it (14): spacing ±12 %, angle ±1.5°, ends ±overshoot."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + spacing
    out = []
    t = -R
    while t <= R:
        a = math.radians(angle + (jit.offset(angle_jitter) if jit else 0))
        dxl, dyl = math.cos(a), math.sin(a)      # along the line
        nx, ny = -dyl, dxl                        # across
        p = (cx + nx * t, cy + ny * t)
        A = (p[0] - dxl * R * 1.5, p[1] - dyl * R * 1.5)
        B = (p[0] + dxl * R * 1.5, p[1] + dyl * R * 1.5)
        seg = _clip_seg_convex(A, B, poly)
        if seg:
            (ax, ay), (bx, by) = seg
            if jit:
                e0, e1 = jit.offset(overshoot), jit.offset(overshoot)
                ax, ay, bx, by = ax - dxl * e0, ay - dyl * e0, bx + dxl * e1, by + dyl * e1
            o = jit.uniform(0.40, 0.50) if jit else 0.45
            out.append(((ax, ay), (bx, by), o))
        t += spacing * (1 + (jit.offset(spacing_jitter) if jit else 0))
    return out


def hatch_paths(lines, attrs_for, buckets=(0.40, 0.43, 0.47, 0.50)) -> str:
    """Group lines into opacity buckets, one <path> each (elements stay few)."""
    groups = {}
    for (ax, ay), (bx, by), o in lines:
        b = min(buckets, key=lambda q: abs(q - o))
        groups.setdefault(b, []).append(f"M{fmt(ax)} {fmt(ay)}L{fmt(bx)} {fmt(by)}")
    return "".join(_path("".join(ds), attrs_for(b)) for b, ds in sorted(groups.items()))


def source_diagram(x, y, w, h, zones, theme, jit: Jitter, label_cb=None) -> str:
    """Zones-of-confidence panel: a framed mini-sheet whose zones are hatched with a density that
    encodes coverage (Zone.density 0..1). Letters via label_cb; key lines are the caller's."""
    out = [f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{theme.paper}" '
           f'{stroke("HAIR", theme.ink, 0.8, caps="butt")}/>']
    for zi, z in enumerate(zones):
        poly = [(x + fx * w, y + fy * h) for fx, fy in z.poly]
        spacing = 14 - 9 * max(0.0, min(1.0, z.density))
        lines = hatch_lines(poly, spacing, -45, jit.sub(f"zone{zi}"), overshoot=0.0)
        out.append(hatch_paths(lines, lambda b: stroke("HAIR", theme.ink2, b, caps="butt")))
        d = "M" + "L".join(f"{fmt(px)} {fmt(py)}" for px, py in poly) + "Z"
        out.append(_path(d, stroke("HAIR", theme.ink, 0.6, caps="butt")))
        if label_cb:
            cx = sum(p[0] for p in poly) / len(poly)
            cy = sum(p[1] for p in poly) / len(poly)
            out.append(label_cb(z.letter, cx, cy + 4, "label", anchor="middle"))
    return "".join(out)


def area_key(x, y, k_area: float, values=(10, 100, 500), theme=None, label_cb=None, gap: int = 14) -> str:
    """Three circles whose areas are k_area·value, bottoms on y, figures beneath (replaces the URL scale bar)."""
    out = []
    cx = x
    for v in values:
        r = math.sqrt(k_area * v / math.pi)
        cx += r
        out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(y - r)}" r="{fmt(r)}" fill="{theme.shallow_b}" '
                   f'{stroke("PEN", theme.ink, 0.8)}/>')
        if label_cb:
            out.append(label_cb(str(v), cx, y + 13, "texture", anchor="middle"))
        cx += r + gap
    return "".join(out)


# ------------------------------------------------------------------ paper
def plate_mark(w: int, h: int, theme, margin: int = 14) -> str:
    """1 px plate mark at .16 with two stepped inner rects at .08/.04: an impression, no filter."""
    out = []
    for i, o in enumerate((0.16, 0.08, 0.04)):
        m = margin + i
        out.append(f'<rect x="{m}" y="{m}" width="{w - 2 * m}" height="{h - 2 * m}" fill="none" '
                   f'{stroke("PEN", theme.ink, o, caps="butt")}/>')
    return "".join(out)


def paper(w: int, h: int, theme, edition: str, jit: Jitter, prefix: str = "paper", margin: int = 14,
          grain: bool | None = None) -> tuple[str, str]:
    """(defs, body). Opaque paper, plate mark, and: day → sparse seeded dot grain (one path of
    sub-pixel squares at .06) plus a 2 % warm radial fall-off; night → one radial wipe
    (#2A3B5A centre .18 → 0), no grain. Square sheet, 14 px unprinted margin."""
    night = theme.edition == "night"
    if grain is None:
        grain = not night and not edition.startswith("phone")
    gid = f"{prefix}-wipe"
    if night:
        defs = (f'<radialGradient id="{gid}" cx="50%" cy="45%" r="70%">'
                f'<stop offset="0" stop-color="#2A3B5A" stop-opacity=".18"/>'
                f'<stop offset="1" stop-color="#2A3B5A" stop-opacity="0"/></radialGradient>')
    else:
        defs = (f'<radialGradient id="{gid}" cx="50%" cy="50%" r="72%">'
                f'<stop offset="0" stop-color="{theme.hair}" stop-opacity="0"/>'
                f'<stop offset=".7" stop-color="{theme.hair}" stop-opacity=".08"/>'
                f'<stop offset="1" stop-color="{theme.hair}" stop-opacity=".35"/></radialGradient>')
    body = [f'<rect width="{w}" height="{h}" fill="{theme.paper}"/>',
            f'<rect width="{w}" height="{h}" fill="url(#{gid})"/>']
    if grain:
        n = int(w * h / 4200)
        g = jit.sub("grain")
        d = []
        for _ in range(n):
            px, py = g.uniform(margin, w - margin), g.uniform(margin, h - margin)
            s = g.uniform(0.6, 1.2)
            d.append(f"M{fmt(px)} {fmt(py)}h{fmt(s)}v{fmt(s)}h-{fmt(s)}z")
        body.append(f'<path d="{"".join(d)}" fill="{theme.ink}" fill-opacity=".06"/>')
    body.append(plate_mark(w, h, theme, margin))
    return defs, "".join(body)


# ------------------------------------------------------------------ course
def compass_bearing(p, q) -> float:
    """True bearing from p to q in screen coords (0 = up/north, clockwise), degrees."""
    return math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1]))) % 360


def catmull_rom(points, per_seg: int = 16, closed: bool = False):
    """Dense polyline through the points (Catmull-Rom), for smoothing a course."""
    P = list(points)
    n = len(P)
    if n < 2:
        return P
    out = []
    segs = n if closed else n - 1
    for i in range(segs):
        p1, p2 = P[i], P[(i + 1) % n]
        p0 = P[i - 1] if (i > 0 or closed) else p1
        p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
        for k in range(per_seg):
            t = k / per_seg
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(P[-1])
    return out


def polyline_at(pts, s: float):
    """Point and unit tangent at arc length s along a polyline: ((x, y), (tx, ty))."""
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L == 0:
            continue
        if acc + L >= s or (a, b) == (pts[-2], pts[-1]):
            t = max(0.0, min(1.0, (s - acc) / L))
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        acc += L
    a, b = pts[-2], pts[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    return b, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def course(points, theme, jit: Jitter, pecked: bool = True, label_cb=None, prefix: str | None = None,
           bearings: bool = True, sides=None, offset: float = 12.0) -> str:
    """The plotted course: COURSE dash (pecked, round caps, seeded phase) or solid PEN, waypoints
    as <use> of the sheet's waypoint symbol (or inline ⊙ without a prefix), bearings per leg via
    label_cb at `offset` px off the leg (sides[i] = ±1 picks the side; default left of travel)."""
    from .field import compact_path
    out = [_path(compact_path(points, False, 1),
                 stroke("PEN", theme.ink, 0.85, "COURSE" if pecked else None, jit if pecked else None))]
    for x, y in points:
        if prefix:
            out.append(f'<use href="#{prefix}-sym-waypoint" x="{fmt(x)}" y="{fmt(y)}"/>')
        else:
            out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="4" fill="none" {stroke("PEN", theme.ink)}/>'
                       f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="1.2" fill="{theme.ink}"/>')
    if bearings and label_cb:
        for i, (p, q) in enumerate(zip(points, points[1:])):
            brg = compass_bearing(p, q)
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
            nx, ny = -(q[1] - p[1]) / L, (q[0] - p[0]) / L   # right of travel
            side = (sides[i] if sides else -1)
            out.append(label_cb(f"{round(brg) % 360:03d}°", mx + nx * offset * side, my + ny * offset * side + 4,
                                "label", anchor="middle"))
    return "".join(out)


def course_samples(points, n: int = 96, per_seg: int = 24) -> list[tuple[float, float, float]]:
    """n samples at equal arc length along the smoothed course: (x, y, heading°) for T4's
    animateTransform values; heading is the true bearing of travel, coordinates to one decimal."""
    dense = catmull_rom(points, per_seg)
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(dense, dense[1:]))
    out = []
    for i in range(n):
        s = total * i / (n - 1) if n > 1 else 0.0
        (x, y), (tx, ty) = polyline_at(dense, s)
        heading = math.degrees(math.atan2(tx, -ty)) % 360
        out.append((round(x, 1), round(y, 1), round(heading, 1)))
    return out


def lateral_offset(leg, s: float, side: str, d: float) -> tuple[float, float]:
    """A point d px off leg=((x1,y1),(x2,y2)) at fraction s along it. side: 'starboard'/'right' is
    the right hand of a vessel travelling the leg; 'port'/'left' the other."""
    (x1, y1), (x2, y2) = leg
    vx, vy = x2 - x1, y2 - y1
    L = math.hypot(vx, vy) or 1
    vx, vy = vx / L, vy / L
    sx, sy = -vy, vx   # starboard in screen coords (y down)
    if side in ("port", "left"):
        sx, sy = -sx, -sy
    return (round(x1 + (x2 - x1) * s + sx * d), round(y1 + (y2 - y1) * s + sy * d))


# ------------------------------------------------------------------ survey geometry
def track_lines(x0, y0, x1, y1, n: int, spacing: float, theme, opacity: float = 0.55):
    """n parallel survey track lines centred on x0,y0→x1,y1 (HAIR, TRACK dash): (svg, segs)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    d, segs = [], []
    for i in range(n):
        off = (i - (n - 1) / 2) * spacing
        a = (x0 + nx * off, y0 + ny * off)
        b = (x1 + nx * off, y1 + ny * off)
        segs.append((a, b))
        d.append(f"M{fmt(a[0])} {fmt(a[1])}L{fmt(b[0])} {fmt(b[1])}")
    return _path("".join(d), stroke("HAIR", theme.ink, opacity, "TRACK", caps="butt")), segs


def check_lines(segs, n: int, theme, opacity: float = 0.35) -> str:
    """n check (cross) lines across a set of track segs at even fractions of their length."""
    if not segs:
        return ""
    (a0, b0), (a1, b1) = segs[0], segs[-1]
    d = []
    for j in range(n):
        t = (j + 1) / (n + 1)
        p = (a0[0] + (b0[0] - a0[0]) * t, a0[1] + (b0[1] - a0[1]) * t)
        q = (a1[0] + (b1[0] - a1[0]) * t, a1[1] + (b1[1] - a1[1]) * t)
        d.append(f"M{fmt(p[0])} {fmt(p[1])}L{fmt(q[0])} {fmt(q[1])}")
    return _path("".join(d), stroke("HAIR", theme.ink, opacity, "TRACK", caps="butt"))


def restricted_line(pts, theme, closed: bool = True, inside: bool = True, tick: float = 3.0,
                    every: float = 12.0) -> str:
    """Restricted-area limit: RESTRICT dash (PEN) with 3 px T-ticks every 12 px on the protected
    side (the interior by default). Generated, not a pattern."""
    from .field import compact_path
    seq = list(pts) + ([pts[0]] if closed else [])
    sign = 1.0 if polygon_area(pts) > 0 else -1.0
    if not inside:
        sign = -sign
    teeth = []
    for a, b in zip(seq, seq[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L == 0:
            continue
        tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, ny = -ty * sign, tx * sign   # interior normal for positive-area polygons
        s = every / 2
        while s < L:
            px, py = a[0] + tx * s, a[1] + ty * s
            teeth.append(f"M{fmt(px)} {fmt(py)}l{fmt(nx * tick)} {fmt(ny * tick)}")
            s += every
    return (_path(compact_path(pts, closed, 1), stroke("PEN", theme.ink, 0.9, "RESTRICT", caps="butt"))
            + _path("".join(teeth), stroke("PEN", theme.ink, 0.9, caps="butt")))
