"""Nautical-chart drawing primitives for the profile artwork.

Everything is deterministic (seeded) so a rebuild produces the same chart.
Coordinates are in the 1280-wide canvas space.
"""
from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import dataclass

import svgkit as k


# ---------------------------------------------------------------- field + contours
@dataclass
class Field:
    w: float
    h: float
    blobs: list  # (x, y, radius, amplitude)
    gx: int = 150
    gy: int = 75

    def value(self, x: float, y: float) -> float:
        v = 0.0
        for bx, by, r, a in self.blobs:
            d2 = (x - bx) ** 2 + (y - by) ** 2
            v += a * math.exp(-d2 / (2 * r * r))
        v += 0.18 * math.sin(x / 290 + 0.7) * math.cos(y / 170 - 0.4)
        return v

    def grid(self):
        return [[self.value(i * self.w / (self.gx - 1), j * self.h / (self.gy - 1)) for i in range(self.gx)]
                for j in range(self.gy)]


def make_field(w: float, h: float, seed: int, n: int = 18, r=(40, 170), a=(0.45, 1.0),
               avoid: list[tuple[float, float, float, float]] | None = None, extra=None) -> Field:
    """Random gaussian blobs; `avoid` rectangles get no blob centres (keep text areas calm).
    `extra` blobs are placed deliberately (islands you want to name)."""
    rng = random.Random(seed)
    blobs = list(extra or [])
    tries = 0
    while len(blobs) < n and tries < 2000:
        tries += 1
        x, y = rng.uniform(-40, w + 40), rng.uniform(-40, h + 40)
        if avoid and any(ax <= x <= ax + aw and ay <= y <= ay + ah for ax, ay, aw, ah in avoid):
            continue
        blobs.append((x, y, rng.uniform(*r), rng.uniform(*a)))
    return Field(w, h, blobs)


def _segments(grid, level, w, h):
    gy, gx = len(grid), len(grid[0])
    out = []
    for j in range(gy - 1):
        for i in range(gx - 1):
            a, b, c, d = grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]
            x0, y0 = i * w / (gx - 1), j * h / (gy - 1)
            x1, y1 = (i + 1) * w / (gx - 1), (j + 1) * h / (gy - 1)

            def lerp(p, q, va, vb):
                t = (level - va) / (vb - va) if vb != va else 0.5
                return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

            pts = {}
            if (a >= level) != (b >= level):
                pts["t"] = lerp((x0, y0), (x1, y0), a, b)
            if (b >= level) != (c >= level):
                pts["r"] = lerp((x1, y0), (x1, y1), b, c)
            if (d >= level) != (c >= level):
                pts["b"] = lerp((x0, y1), (x1, y1), d, c)
            if (a >= level) != (d >= level):
                pts["l"] = lerp((x0, y0), (x0, y1), a, d)
            keys = list(pts)
            if len(keys) == 2:
                out.append((pts[keys[0]], pts[keys[1]]))
            elif len(keys) == 4:
                centre = (a + b + c + d) / 4
                if (centre >= level) == (a >= level):
                    out.append((pts["t"], pts["r"]))
                    out.append((pts["b"], pts["l"]))
                else:
                    out.append((pts["t"], pts["l"]))
                    out.append((pts["r"], pts["b"]))
    return out


def _chain(seglist):
    key = lambda p: (round(p[0], 1), round(p[1], 1))
    adj = defaultdict(list)
    for s in seglist:
        adj[key(s[0])].append(s)
        adj[key(s[1])].append(s)
    used, lines = set(), []
    for s in seglist:
        if id(s) in used:
            continue
        used.add(id(s))
        line = [s[0], s[1]]
        for end in (1, 0):
            while True:
                p = line[-1] if end else line[0]
                nxt = [t for t in adj[key(p)] if id(t) not in used]
                if not nxt:
                    break
                t = nxt[0]
                used.add(id(t))
                q = t[1] if key(t[0]) == key(p) else t[0]
                if end:
                    line.append(q)
                else:
                    line.insert(0, q)
        lines.append(line)
    return lines


def smooth_path(pts, closed: bool) -> str:
    """Catmull-Rom through the points, emitted as cubic Béziers."""
    if len(pts) < 3:
        return ""
    n = len(pts)
    d = f"M{pts[0][0]:.0f},{pts[0][1]:.0f}"
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else (pts[-2] if closed else pts[i])
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < n else (pts[1] if closed else pts[i + 1])
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}"
    if closed:
        d += " Z"
    return d


def _subsample(line, every=2):
    if len(line) <= 8:
        return line
    core = line[1:-1:every]
    return [line[0]] + core + [line[-1]]


def polygon_area_centroid(pts):
    a = cx = cy = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a *= 0.5
    if abs(a) < 1e-6:
        return 0.0, pts[0][0], pts[0][1]
    return abs(a), cx / (6 * a), cy / (6 * a)


def contours(field: Field, levels: list[float], grid=None):
    """[(level, [(path_d, closed, points), ...]), ...]"""
    grid = grid or field.grid()
    out = []
    for lv in levels:
        paths = []
        for line in _chain(_segments(grid, lv, field.w, field.h)):
            closed = abs(line[0][0] - line[-1][0]) < 1 and abs(line[0][1] - line[-1][1]) < 1
            line = _subsample(line, 2)
            d = smooth_path(line, closed)
            if d:
                paths.append((d, closed, line))
        out.append((lv, paths))
    return out


def islands(field: Field, land_level: float, min_area: float = 1500, grid=None):
    """Closed land polygons at land_level, largest first: [(area, cx, cy), ...]"""
    (_, paths), = contours(field, [land_level], grid)
    found = []
    for d, closed, pts in paths:
        if not closed:
            continue
        a, cx, cy = polygon_area_centroid(pts)
        if a >= min_area:
            found.append((a, cx, cy))
    return sorted(found, reverse=True)


def draw_contours(field: Field, levels: list[float], stroke: str, index_every: int = 4,
                  opacity: float = 0.5, land_level: float | None = None, land_fill: str | None = None,
                  hatch_id: str | None = None) -> str:
    out = []
    for i, (lv, paths) in enumerate(contours(field, levels)):
        is_index = (i % index_every == 0)
        w = 1.0 if is_index else 0.6
        op = opacity if is_index else opacity * 0.7
        for d, closed, _pts in paths:
            if land_level is not None and lv >= land_level and closed and land_fill:
                out.append(f'<path d="{d}" fill="{land_fill}" stroke="{stroke}" stroke-width="1" stroke-opacity="{opacity}"/>')
                if hatch_id:
                    out.append(f'<path d="{d}" fill="url(#{hatch_id})" stroke="none"/>')
            else:
                out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-opacity="{op:.2f}"/>')
    return "".join(out)


# ---------------------------------------------------------------- chart furniture
def hatch_defs(hid: str, stroke: str, spacing: float = 5.0, angle: float = 45, opacity: float = 0.35) -> str:
    return (f'<pattern id="{hid}" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate({angle})"><line x1="0" y1="0" x2="0" y2="{spacing}" stroke="{stroke}" '
            f'stroke-width="0.7" stroke-opacity="{opacity}"/></pattern>')


def graticule(x: float, y: float, w: float, h: float, stroke: str, step: float = 80, opacity: float = 0.18,
              ticks: bool = True) -> str:
    out = []
    xx = x + step
    while xx < x + w:
        out.append(f'<line x1="{xx:.0f}" y1="{y}" x2="{xx:.0f}" y2="{y+h}" stroke="{stroke}" stroke-width="0.6" stroke-opacity="{opacity}"/>')
        xx += step
    yy = y + step
    while yy < y + h:
        out.append(f'<line x1="{x}" y1="{yy:.0f}" x2="{x+w}" y2="{yy:.0f}" stroke="{stroke}" stroke-width="0.6" stroke-opacity="{opacity}"/>')
        yy += step
    return "".join(out)


def _dist_to_polyline(x, y, pts):
    best = 1e9
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy or 1
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / L2))
        px, py = x1 + t * dx, y1 + t * dy
        best = min(best, math.hypot(x - px, y - py))
    return best


def soundings(field: Field, region: tuple[float, float, float, float], stroke: str, seed: int, n: int = 60,
              size: float = 9.5, land_level: float = 1.6, avoid=None, opacity: float = 0.75,
              avoid_lines=None, line_clearance: float = 26.0, spacing: float = 36.0) -> str:
    """Scatter depth numbers over open water (where the field is low)."""
    rng = random.Random(seed)
    x0, y0, w, h = region
    out = []
    placed = []
    tries = 0
    while len(placed) < n and tries < 6000:
        tries += 1
        x, y = rng.uniform(x0 + 24, x0 + w - 24), rng.uniform(y0 + 18, y0 + h - 10)
        if avoid and any(ax <= x <= ax + aw and ay <= y <= ay + ah for ax, ay, aw, ah in avoid):
            continue
        if avoid_lines and any(_dist_to_polyline(x, y, pl) < line_clearance for pl in avoid_lines):
            continue
        v = field.value(x, y)
        if v >= land_level * 0.8:
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < spacing ** 2 for px, py in placed):
            continue
        placed.append((x, y))
        depth = int(max(2, (land_level - v) * 38 + rng.uniform(-3, 3)))
        out.append(k.text_use(str(depth), x, y, "plex", size, stroke, anchor="middle", opacity=opacity))
    return "".join(out)


def compass_rose(cx: float, cy: float, r: float, ink: str, accent: str, label_font: str = "plex") -> str:
    out = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ink}" stroke-width="0.8" stroke-opacity=".55"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.78:.1f}" fill="none" stroke="{ink}" stroke-width="0.5" stroke-opacity=".4"/>')
    # degree ticks
    for deg in range(0, 360, 10):
        a = math.radians(deg - 90)
        big = deg % 30 == 0
        r1 = r * (0.86 if big else 0.92)
        out.append(f'<line x1="{cx + r1*math.cos(a):.1f}" y1="{cy + r1*math.sin(a):.1f}" x2="{cx + r*math.cos(a):.1f}" y2="{cy + r*math.sin(a):.1f}" stroke="{ink}" stroke-width="{0.9 if big else 0.5}" stroke-opacity=".6"/>')
    # 16-point star: 8 long, 8 short
    def star(points, ro, ri, fill, op):
        d = ""
        for i in range(points * 2):
            ang = math.radians(i * 180 / points - 90)
            rr = ro if i % 2 == 0 else ri
            d += ("M" if i == 0 else "L") + f"{cx + rr*math.cos(ang):.1f},{cy + rr*math.sin(ang):.1f}"
        return f'<path d="{d}Z" fill="{fill}" fill-opacity="{op}" stroke="{ink}" stroke-width="0.6" stroke-opacity=".7"/>'
    out.append(star(8, r * 0.52, r * 0.10, ink, 0.18))
    out.append(star(4, r * 0.74, r * 0.12, ink, 0.55))
    # north point in accent
    an = math.radians(-90)
    d = (f"M{cx:.1f},{cy - r*0.74:.1f} L{cx + r*0.12*math.cos(math.radians(-45)):.1f},{cy + r*0.12*math.sin(math.radians(-45)):.1f} "
         f"L{cx:.1f},{cy:.1f} L{cx + r*0.12*math.cos(math.radians(-135)):.1f},{cy + r*0.12*math.sin(math.radians(-135)):.1f} Z")
    out.append(f'<path d="{d}" fill="{accent}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.05:.1f}" fill="{ink}"/>')
    for lab, ang in (("N", -90), ("E", 0), ("S", 90), ("W", 180)):
        a = math.radians(ang)
        lx, ly = cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a) + 4
        out.append(k.text(lab, lx, ly, label_font, 11, ink, anchor="middle"))
    return "".join(out)


def rhumb_lines(cx: float, cy: float, length: float, ink: str, n: int = 16, opacity: float = 0.14) -> str:
    out = []
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        out.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + length*math.cos(a):.1f}" y2="{cy + length*math.sin(a):.1f}" stroke="{ink}" stroke-width="0.5" stroke-opacity="{opacity}"/>')
    return "".join(out)


def boat(ink: str, sail: str, sail2: str, scale: float = 1.0) -> str:
    """A small sloop, bow to the right, origin at the waterline centre."""
    s = scale
    return (f'<g transform="scale({s})">'
            f'<path d="M-16,0 L16,0 L11,6 L-11,6 Z" fill="{ink}"/>'
            f'<path d="M-1,-1 V-34" stroke="{ink}" stroke-width="1.4"/>'
            f'<path d="M1,-32 L21,-3 L1,-3 Z" fill="{sail}"/>'
            f'<path d="M-3,-25 L-15,-3 L-3,-3 Z" fill="{sail2}"/>'
            f'</g>')


def buoy(x: float, y: float, color: str, ink: str, kind: str = "can") -> str:
    """Lateral marks: 'can' (red, flat top) or 'cone' (green, pointed)."""
    if kind == "cone":
        return (f'<path d="M{x-5},{y} L{x+5},{y} L{x},{y-11} Z" fill="{color}"/>'
                f'<line x1="{x-7}" y1="{y+2}" x2="{x+7}" y2="{y+2}" stroke="{ink}" stroke-width="0.8" stroke-opacity=".6"/>')
    return (f'<rect x="{x-4.5}" y="{y-10}" width="9" height="10" rx="1" fill="{color}"/>'
            f'<line x1="{x-7}" y1="{y+2}" x2="{x+7}" y2="{y+2}" stroke="{ink}" stroke-width="0.8" stroke-opacity=".6"/>')


def waypoint(x: float, y: float, ink: str, r: float = 5) -> str:
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ink}" stroke-width="1"/>'
            f'<line x1="{x-r-3}" y1="{y}" x2="{x+r+3}" y2="{y}" stroke="{ink}" stroke-width="0.8"/>'
            f'<line x1="{x}" y1="{y-r-3}" x2="{x}" y2="{y+r+3}" stroke="{ink}" stroke-width="0.8"/>')


def course(points: list[tuple[float, float]], ink: str, accent: str, dur: float, boat_svg: str,
           dash: str = "2 6", label_font: str = "plex", bearings: bool = True) -> str:
    """Dashed plotted course through waypoints, with bearings and a boat that sails it."""
    out = []
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)
    out.append(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="1.1" stroke-dasharray="{dash}" stroke-opacity=".8"/>')
    for i, (x, y) in enumerate(points):
        out.append(waypoint(x, y, ink))
    if bearings:
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            ang = (math.degrees(math.atan2(y2 - y1, x2 - x1)) + 90) % 360
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            nx, ny = -(y2 - y1), (x2 - x1)
            L = math.hypot(nx, ny) or 1
            out.append(k.text_use(f"{ang:03.0f}°", mx + nx / L * 12, my + ny / L * 12 + 3, label_font, 9.5, ink, anchor="middle", opacity=0.7))
    # smooth path for the boat so it does not snap at waypoints
    sd = smooth_path(points, False)
    out.append(f'<g><animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto" path="{sd}" calcMode="linear"/>'
               f'<g transform="rotate(0)">{boat_svg}</g></g>')
    return "".join(out)


def cartouche(x: float, y: float, w: float, h: float, ink: str, paper: str) -> str:
    """Double-ruled title block frame."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{paper}" fill-opacity=".92" stroke="{ink}" stroke-width="1"/>'
            f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" fill="none" stroke="{ink}" stroke-width="0.5"/>')


def border(x: float, y: float, w: float, h: float, ink: str, step: float = 20) -> str:
    """Chart neat-line with alternating black/white minute bars like a real sheet."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{ink}" stroke-width="1.2"/>',
           f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" fill="none" stroke="{ink}" stroke-width="0.6"/>']
    # minute bars along top and bottom
    i = 0
    xx = x + 6
    while xx + step <= x + w - 6:
        if i % 2 == 0:
            out.append(f'<rect x="{xx:.0f}" y="{y}" width="{step}" height="6" fill="{ink}" fill-opacity=".85"/>')
            out.append(f'<rect x="{xx:.0f}" y="{y+h-6}" width="{step}" height="6" fill="{ink}" fill-opacity=".85"/>')
        xx += step
        i += 1
    i = 0
    yy = y + 6
    while yy + step <= y + h - 6:
        if i % 2 == 0:
            out.append(f'<rect x="{x}" y="{yy:.0f}" width="6" height="{step}" fill="{ink}" fill-opacity=".85"/>')
            out.append(f'<rect x="{x+w-6}" y="{yy:.0f}" width="6" height="{step}" fill="{ink}" fill-opacity=".85"/>')
        yy += step
        i += 1
    return "".join(out)
