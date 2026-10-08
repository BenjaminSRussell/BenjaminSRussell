"""place.py — features, their placement and radii, spot heights and soundings positions (T6 §2.4).

Area ∝ commits: every feature is cut at the same level (5, the danger line every island and shoal
has) and its drawn polygon area is Newton-solved to k_area·value within ±8 %. Placement is slots
keyed by alias, then a Halton search with clearances; nothing is asserted here, everything is
reported (PlaceReport) so the cron job never dies on geometry.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field as dc_field

from .field import (Field, Contour, contours, polygon_area, polygon_centroid, point_in_polygon,
                    polyline_length, KERNEL_RATIO)
from .furniture import polyline_at

__all__ = ["Feature", "PlaceReport", "RadiusReport", "place_features", "solve_radii", "feature_polygons",
           "spot_heights", "soundings_along", "soundings_lean", "halton", "polygon_area", "polygon_centroid",
           "point_in_polygon", "dist_to_polyline", "kind_of", "KERNEL_RATIO"]


@dataclass
class Feature:
    name: str
    value: float
    kind: str                 # island | shoal | islet | harbour | wreck
    x: int = 0
    y: int = 0
    r: float = 0.0
    amp: float = 0.0
    area: float = 0.0
    axis: tuple = ()          # (angle°, length, cx, cy) for T5's text-on-path
    alias: str = ""
    sub: int | None = None    # months active (hero subscript), set by the caller
    ratio: float | None = None  # kernel support / r; defaults per kind (KERNEL_RATIO)
    h: float = 0.0
    placed: bool = False
    slot: str | None = None
    target: float = 0.0


@dataclass
class PlaceReport:
    placed: list = dc_field(default_factory=list)
    dropped: list = dc_field(default_factory=list)       # names that found no clear position
    beyond_cap: list = dc_field(default_factory=list)    # names cut by `cap` ("and N islets")
    slot_conflicts: list = dc_field(default_factory=list)  # (name, other, distance, required)
    candidates_tried: int = 0
    min_pair_clearance: float | None = None
    min_course_clearance: float | None = None

    @property
    def islets_more(self) -> int:
        return len(self.dropped) + len(self.beyond_cap)


@dataclass
class RadiusReport:
    name: str
    value: float
    target: float
    area: float | None
    r: float
    ratio: float | None
    ok: bool
    iters: int
    clamped: bool


def kind_of(r: float, active: bool, alias: str = "", archived: bool = False) -> str:
    """T2 §2.3 kind rule: wreck if archived → harbour if scrapy → islet if r < 16 → shoal if active → island."""
    if archived:
        return "wreck"
    if alias.lower() == "scrapy":
        return "harbour"
    if r < 16:
        return "islet"
    return "shoal" if active else "island"


# ------------------------------------------------------------------ geometry helpers
def halton(i: int, base: int) -> float:
    f, r = 1.0, 0.0
    while i > 0:
        f /= base
        r += f * (i % base)
        i //= base
    return r


def dist_to_polyline(x, y, pts) -> float:
    best = math.inf
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dx, dy = x2 - x1, y2 - y1
        L2 = dx * dx + dy * dy or 1
        t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / L2))
        best = min(best, math.hypot(x - (x1 + t * dx), y - (y1 + t * dy)))
    return best


def _in_rect_inflated(x, y, rect, m) -> bool:
    rx, ry, rw, rh = rect
    return rx - m <= x <= rx + rw + m and ry - m <= y <= ry + rh + m


# ------------------------------------------------------------------ placement
def place_features(features, drawable, exclusions, course_pts, seed: int, slots: dict, cap: int = 32,
                   clear_edge: float = 28, clear_pair: float = 44, clear_course: float = 30,
                   islet_min_x: float = 600, tries: int = 400) -> PlaceReport:
    """Slots keyed by alias fix a centre; the rest take Halton candidates (sequence offset by `seed`)
    inside `drawable` minus `exclusions` (rects) by ≥ r+clear_edge, ≥ ri+rj+clear_pair from placed
    features, ≥ r+clear_course from the course; islets biased to x > islet_min_x. Largest first.
    Features past `cap` or unplaced after `tries` candidates are reported, never asserted."""
    rep = PlaceReport()
    order = sorted((f for f in features if f.kind != "wreck"), key=lambda f: (-f.value, f.name))
    placed = []
    # 1. slots, and whatever the caller has already placed (a sheet's own arc, say): both are fixed
    # ground the Halton candidates must clear (v9.1: pre-placed features were invisible to the search)
    for f in order:
        key = f.alias or f.name
        if key in slots:
            f.x, f.y = slots[key]
            f.placed, f.slot = True, key
            placed.append(f)
        elif f.placed:
            placed.append(f)
    for i, a in enumerate(placed):
        for b in placed[i + 1:]:
            d = math.hypot(a.x - b.x, a.y - b.y)
            need = a.r + b.r + clear_pair
            if d < need and not (a.kind == "harbour" or b.kind == "harbour"):
                rep.slot_conflicts.append((a.name, b.name, round(d), round(need)))
    # 2. Halton search
    dx0, dy0, dw, dh = drawable
    idx = seed
    for f in order:
        if f.placed:
            continue
        if len(placed) >= cap:
            rep.beyond_cap.append(f.name)
            continue
        r = f.r
        is_islet = f.kind == "islet" or r < 16
        ok = False
        for _ in range(tries):
            idx += 1
            rep.candidates_tried += 1
            x = dx0 + halton(idx, 2) * dw
            y = dy0 + halton(idx, 3) * dh
            m = r + clear_edge
            if not (dx0 + m <= x <= dx0 + dw - m and dy0 + m <= y <= dy0 + dh - m):
                continue
            if is_islet and x < islet_min_x:
                continue
            if any(_in_rect_inflated(x, y, ex, m) for ex in exclusions):
                continue
            if any(math.hypot(x - p.x, y - p.y) < r + p.r + clear_pair for p in placed):
                continue
            if course_pts and dist_to_polyline(x, y, course_pts) < r + clear_course:
                continue
            f.x, f.y, f.placed = int(round(x)), int(round(y)), True
            placed.append(f)
            ok = True
            break
        if not ok:
            rep.dropped.append(f.name)
    rep.placed = [f.name for f in placed]
    pairs = [math.hypot(a.x - b.x, a.y - b.y) - a.r - b.r for i, a in enumerate(placed) for b in placed[i + 1:]]
    rep.min_pair_clearance = round(min(pairs), 1) if pairs else None
    if course_pts and placed:
        rep.min_course_clearance = round(min(dist_to_polyline(f.x, f.y, course_pts) - f.r
                                             for f in placed if f.kind != "harbour"), 1)
    for f in placed:
        f.axis = (0.0, 2 * f.r, f.x, f.y)
    return rep


# ------------------------------------------------------------------ radii
def _measure(field: Field, f: Feature, level: float) -> float | None:
    """Area of the closed `level` polygon around (f.x, f.y) in a local window; None if not closed."""
    h = max(f.h, f.r * 2.0, 24.0)
    win = (f.x - 1.4 * h, f.y - 1.4 * h, 2.8 * h, 2.8 * h)
    best = None
    for c in contours(field, [level], clip=win):
        if c.closed and c.shallow_inside and c.contains(f.x, f.y):
            a = c.area()
            if best is None or a < best:
                best = a
    return best


def solve_radii(field_builder, features, k_area: float, tol: float = 0.08, iters: int = 4,
                level: float = 5.0, r_bounds=(6.0, 90.0)) -> list[RadiusReport]:
    """Newton on each feature's r (largest first) so the measured polygon area at `level` equals
    k_area·value. field_builder(features) -> Field rebuilds the field (soundings re-solved) with
    the current radii. Sets f.r, f.area, f.target. Returns a RadiusReport per feature; the caller
    logs any `ok == False` to build-report.json and falls back (never asserts in the cron)."""
    lo, hi = r_bounds
    todo = sorted((f for f in features if f.kind != "wreck" and f.value > 0), key=lambda f: -f.value)
    for f in todo:
        f.target = k_area * f.value
        if f.r <= 0:
            f.r = max(lo, min(hi, math.sqrt(f.target / math.pi)))
    reports = []
    for f in todo:
        area, it, clamped = None, 0, False
        for it in range(1, iters + 1):
            field = field_builder(features)
            area = _measure(field, f, level)
            if area is None:
                f.r = min(hi, f.r * 1.15)
                clamped = f.r >= hi
                continue
            f.area = area
            ratio = area / f.target
            if abs(ratio - 1) <= tol * 0.4:
                break
            nr = f.r * math.sqrt(f.target / area)
            clamped = nr < lo or nr > hi
            f.r = max(lo, min(hi, nr))
        ratio = (area / f.target) if area else None
        reports.append(RadiusReport(f.name, f.value, round(f.target), round(area) if area else None,
                                    round(f.r, 1), round(ratio, 3) if ratio else None,
                                    ratio is not None and abs(ratio - 1) <= tol, it, clamped))
    return reports


def feature_polygons(cs, features, level: float = 5.0) -> dict:
    """name -> the smallest closed shallow `level` polygon containing the feature's centre."""
    out = {}
    for f in features:
        best = None
        for c in cs:
            if c.level == level and c.closed and c.shallow_inside and c.contains(f.x, f.y):
                if best is None or c.area() < best.area():
                    best = c
        if best is not None:
            out[f.name] = best.pts
    return out


def spot_heights(features, cs, clearance: float = 8, level: float = 5.0, min_r: float = 16) -> list[tuple]:
    """(feature, x, y, angle) for each feature's spot height: inside the feature above its name
    when it fits (r ≥ 16 and the point is inside its polygon), else just outside its `level`
    polygon to the east with `clearance`."""
    polys = feature_polygons(cs, features, level)
    out = []
    for f in features:
        if f.kind == "wreck":
            continue
        poly = polys.get(f.name)
        x, y = f.x, f.y - 10
        if f.r >= min_r and (poly is None or point_in_polygon(x, y, poly)):
            out.append((f, int(round(x)), int(round(y)), 0))
            continue
        # walk east from the centre until outside the polygon, then add clearance
        ex = f.x + f.r
        if poly:
            while point_in_polygon(ex, f.y, poly) and ex < f.x + 4 * f.r + 40:
                ex += 2
        out.append((f, int(round(ex + clearance)), int(round(f.y + 4)), 0))
    return out


# ------------------------------------------------------------------ soundings along the course
def soundings_along(course_pts, values, rows=(-48, -24, 24, 48)) -> list[tuple]:
    """Week i (oldest first) at arc position i·L/n along the course, offset to rows cycling, so
    the oldest sit seaward and the newest ring the anchor: [(x, y, value)] integers."""
    n = len(values)
    if n == 0 or len(course_pts) < 2:
        return []
    L = polyline_length(course_pts)
    out = []
    for i, v in enumerate(values):
        s = L * i / n
        (x, y), (tx, ty) = polyline_at(course_pts, s)
        off = rows[i % len(rows)]
        out.append((int(round(x - ty * off)), int(round(y + tx * off)), v))
    return out


def soundings_lean(course_pts, pts, max_lean: float = 2.5) -> list[float]:
    """A lean of ±max_lean° toward the local course tangent for each sounding (14 F7)."""
    out = []
    for x, y, *_ in pts:
        # nearest point on the course → its tangent
        best, tang = math.inf, (1.0, 0.0)
        for a, b in zip(course_pts, course_pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy or 1
            t = max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / L2))
            d = math.hypot(x - (a[0] + t * dx), y - (a[1] + t * dy))
            if d < best:
                best, tang = d, (dx / math.sqrt(L2), dy / math.sqrt(L2))
        ang = math.degrees(math.atan2(tang[1], tang[0]))
        ang = ((ang + 90) % 180) - 90
        out.append(round(max(-max_lean, min(max_lean, ang / 10)), 1))
    return out
