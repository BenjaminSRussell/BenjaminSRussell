"""water.py — tints, coastline, danger lines, hatch, coast vignette, unsurveyed band (T6 §2.3).

Tint bands are opaque result colours, deepest first, land last (15): A = closed 10-polygons in
shallow_a, then B = closed 5-polygons in shallow_b, then land (0) in `land`, each level one
<path fill-rule="evenodd"> so lagoons and basins are holes. No <pattern>, no filter anywhere.
"""
from __future__ import annotations

import math

from .field import Contour, compact_path, smooth_path, clip_polyline, polygon_area, polygon_centroid, \
    point_in_polygon, fmt
from .furniture import stroke, op, Jitter, hatch_lines, hatch_paths

__all__ = ["tint_bands", "coastline", "danger_lines", "hatch", "coast_vignette", "unsurveyed_band",
           "approximate_fringe", "level_polygons"]

HATCH = {"unsurveyed": {"spacing": 8.0, "angle": -45.0},
         "foul": {"spacing": 6.0, "angle": -45.0}}


def level_polygons(cs, level: float):
    """Closed polygons at `level` for an evenodd fill: the shallow-interior ones plus the deep
    holes nested inside them (a deep hole that is nested in nothing is not drawn)."""
    closed = [c for c in cs if c.level == level and c.closed]
    shallow = [c for c in closed if c.shallow_inside]
    polys = [c.pts for c in shallow]
    for c in closed:
        if c.shallow_inside:
            continue
        cx, cy = polygon_centroid(c.pts)
        if any(point_in_polygon(cx, cy, s.pts) for s in shallow):
            polys.append(c.pts)
    return polys


def _fill_level(cs, level, color, every) -> str:
    polys = level_polygons(cs, level)
    if not polys:
        return ""
    d = "".join(compact_path(p, True, every) for p in polys)
    return f'<path d="{d}" fill="{color}" fill-rule="evenodd"/>'


def tint_bands(cs, theme, levels=(10.0, 5.0), land_level: float = 0.0, every: int = 3) -> str:
    """A (under levels[0]) in shallow_a, B (under levels[1]) in shallow_b, then land in `land`."""
    out = [_fill_level(cs, levels[0], theme.shallow_a, every),
           _fill_level(cs, levels[1], theme.shallow_b, every),
           _fill_level(cs, land_level, theme.land, every)]
    return "".join(out)


def coastline(cs, theme, swell: bool = True, level: float = 0.0, every: int = 2) -> str:
    """LINE ink2 cubic on the 0-contours; swell = a second PEN pass offset (+0.4, +0.4) at .35,
    thickening the SE side the way a burin leans away from top-left light (14 F1)."""
    ds = [smooth_path(c.pts, c.closed, every) for c in cs if c.level == level and len(c.pts) >= 2]
    if not ds:
        return ""
    d = "".join(ds)
    out = [f'<path d="{d}" fill="none" {stroke("LINE", theme.ink2)}/>']
    if swell:
        out.append(f'<path d="{d}" fill="none" transform="translate(0.4 0.4)" {stroke("PEN", theme.ink2, 0.35)}/>')
    return "".join(out)


def danger_lines(cs, level, theme, jit: Jitter, inside=None, every: int = 3, opacity: float = 0.9) -> str:
    """Round-capped LINE dots, dash '0.1 g' with g ∈ U(4.0, 4.6) per feature and a seeded phase,
    around every closed shallow polygon at `level`; with `inside=[(x, y), …]` only polygons that
    contain one of those points (shoals, not islands)."""
    out = []
    i = 0
    for c in cs:
        if c.level != level or not c.closed or not c.shallow_inside:
            continue
        if inside is not None and not any(c.contains(x, y) for x, y in inside):
            continue
        i += 1
        out.append(f'<path d="{compact_path(c.pts, True, every)}" fill="none" '
                   f'{stroke("LINE", theme.ink, opacity, "DANGER", jit.sub(f"danger{i}"))}/>')
    return "".join(out)


def _is_convex(poly) -> bool:
    n = len(poly)
    sign = 0
    for i in range(n):
        a, b, c = poly[i], poly[(i + 1) % n], poly[(i + 2) % n]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if abs(cr) < 1e-9:
            continue
        s = 1 if cr > 0 else -1
        if sign and s != sign:
            return False
        sign = s
    return True


def _as_poly(poly_or_rect):
    if len(poly_or_rect) == 4 and all(isinstance(v, (int, float)) for v in poly_or_rect):
        x, y, w, h = poly_or_rect
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    return list(poly_or_rect)


def hatch(poly_or_rect, theme, jit: Jitter, kind: str = "unsurveyed", clip_id: str = "hatch",
          ramp=None, spacing: float | None = None, angle: float | None = None,
          color: str | None = None) -> tuple[str, str]:
    """(defs, body). Hand-ruled hatch: individual PEN lines at −45° ± 1.5°, spacing s(1 ± 0.12)
    (8 unsurveyed, 6 foul), ends over/undershooting ±2 px, opacity U(.40, .50) per line, grouped
    into four opacity buckets (four <path>s). Convex regions are clipped geometrically so the end
    jitter shows; a concave polygon falls back to a clipPath named clip_id. ramp=(x0, x1) fades the
    lines in from x0 to x1 through one userSpaceOnUse gradient (the band's fade, T2 §2.6)."""
    spec = HATCH.get(kind, HATCH["unsurveyed"])
    s = spacing or spec["spacing"]
    a = spec["angle"] if angle is None else angle
    ink = color or (theme.unsurveyed if kind == "unsurveyed" else theme.ink2)
    poly = _as_poly(poly_or_rect)
    defs, body = [], []
    convex = _is_convex(poly)
    if convex:
        lines = hatch_lines(poly, s, a, jit)
    else:
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        box = [(min(xs), min(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (min(xs), max(ys))]
        lines = hatch_lines(box, s, a, jit, overshoot=0.0)
        defs.append(f'<clipPath id="{clip_id}"><path d="{compact_path(poly, True, 1)}"/></clipPath>')
    paint = ink
    if ramp:
        gid = f"{clip_id}-ramp"
        defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{fmt(ramp[0])}" y1="0" '
                    f'x2="{fmt(ramp[1])}" y2="0"><stop offset="0" stop-color="{ink}" stop-opacity="0"/>'
                    f'<stop offset="1" stop-color="{ink}" stop-opacity="1"/></linearGradient>')
        paint = f"url(#{gid})"
    paths = hatch_paths(lines, lambda b: stroke("PEN", paint, b, caps="butt"))
    body.append(paths if convex else f'<g clip-path="url(#{clip_id})">{paths}</g>')
    return "".join(defs), "".join(body)


def coast_vignette(poly, theme, jit: Jitter, step: float = 6.0, lengths=(5.0, 3.5, 2.0),
                   opacities=(0.5, 0.35, 0.25), gaps=(1.5, 2.0, 2.0)) -> str:
    """Admiralty coast shading: every `step` px along the land polygon, three HAIR ticks stepping
    seaward along the outward normal (lengths 5/3.5/2 at .5/.35/.25), one <path> per tick rank.
    Named islands only (≤ 6); islets get the coastline alone."""
    n = len(poly)
    if n < 3:
        return ""
    sign = 1.0 if polygon_area(poly) > 0 else -1.0
    ranks = [[] for _ in lengths]
    acc = 0.0
    g = jit.sub("vignette")
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L == 0:
            continue
        tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx, ny = ty * sign, -tx * sign      # outward (interior is on the left of travel when area > 0)
        s = step - acc
        while s < L:
            px, py = a[0] + tx * s, a[1] + ty * s
            d = 0.0
            for k, (ln, gp) in enumerate(zip(lengths, gaps)):
                d += gp + g.offset(0.4)
                ll = ln * (1 + g.offset(0.1))
                ranks[k].append(f"M{fmt(px + nx * d)} {fmt(py + ny * d)}l{fmt(nx * ll)} {fmt(ny * ll)}")
                d += ll
            s += step
        acc = (acc + L) % step
    out = []
    for k, d in enumerate(ranks):
        if d:
            out.append(f'<path d="{"".join(d)}" fill="none" {stroke("HAIR", theme.ink2, opacities[k], caps="butt")}/>')
    return "".join(out)


def unsurveyed_band(x, y, w, h, theme, jit: Jitter, label_cb=None, ramp_w: float = 40.0,
                    label: str = "UNSURVEYED", limit_label: str | None = None, clip_id: str = "unsurv",
                    label_at=None, limit_at=None) -> tuple[str, str]:
    """(defs, body). The hand-ruled hatch of the unsurveyed margin fading in over ramp_w from its
    west edge, a LIMIT-dashed limit line at x, and labels via label_cb (rotated −90°):
    `label` at label_at (default 60 % across, mid-height) and `limit_label` 14 px west of the line."""
    defs, body = hatch((x, y, w, h), theme, jit.sub("band"), "unsurveyed", clip_id, ramp=(x, x + ramp_w))
    body += f'<path d="M{fmt(x)} {fmt(y)}v{fmt(h)}" fill="none" {stroke("PEN", theme.ink, 0.8, "LIMIT", caps="butt")}/>'
    if label_cb:
        lx, ly = label_at or (x + w * 0.6, y + h / 2)
        body += label_cb(label, lx, ly, "label-caps", anchor="middle", rotate=-90)
        if limit_label:
            mx, my = limit_at or (x - 14, y + h / 2)
            body += label_cb(limit_label, mx, my, "label", anchor="middle", rotate=-90)
    return defs, body


def approximate_fringe(cs, clip_rect, theme, every: int = 3, opacity: float = 0.55, skip_levels=(0.0,)) -> str:
    """Contour portions inside clip_rect redrawn with DASH['APPROX'] (PEN ink2): the chart's own
    sign that the survey is unreliable there (T2: x 1080–1150 on the hero)."""
    ds = []
    for c in cs:
        if c.level in skip_levels:
            continue
        ins, _ = clip_polyline(c.pts, clip_rect, c.closed)
        ds.extend(compact_path(p, False, every) for p in ins)
    if not ds:
        return ""
    return f'<path d="{"".join(ds)}" fill="none" {stroke("PEN", theme.ink2, opacity, "APPROX")}/>'
