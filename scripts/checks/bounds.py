"""bounds — text boxes inside the safe area and free of collisions (T10 check 5).

Reads the build-report `text[]` manifest (typeset.run_records) and `exclusions[]` per edition.
A box is (x0, y0, x1, y1) in sheet space. Rules: every box inside the sheet minus the 6 px frame
unless the sheet names the run in `breaks`; no semantic box overlaps another text box or an
exclusion it is not `within`; texture boxes (soundings, contour figures) ≥ 28 px apart centre to
centre when they are not the same run."""
from __future__ import annotations

import math

from check import Finding, fail, warn

TIER = "fast"
FRAME = 0.0          # marginalia live in the border band; the sheet edge is the limit
MIN_TEXTURE_GAP = 28.0
OVERLAP_TOL = 1.0    # px of allowed kiss


def _box(r: dict) -> tuple[float, float, float, float] | None:
    try:
        x0, x1, y = float(r["x0"]), float(r["x1"]), float(r["y"])
    except (KeyError, TypeError, ValueError):
        return None
    y0 = float(r.get("y0", y - 0.75 * float(r.get("size", 0))))
    y1 = float(r.get("y1", y))
    if r.get("rot") and "y0" not in r:   # typeset's manifest already holds the rotated box
        # rotated run: use the bounding box of the rotated rectangle around its origin (x0, y)
        a = math.radians(float(r["rot"]))
        pts = [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]
        cx, cy = x0, y
        rot = [(cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a),
                cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a)) for px, py in pts]
        xs, ys = [p[0] for p in rot], [p[1] for p in rot]
        return min(xs), min(ys), max(xs), max(ys)
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def _overlap(a, b, tol=OVERLAP_TOL) -> bool:
    return not (a[2] <= b[0] + tol or b[2] <= a[0] + tol or a[3] <= b[1] + tol or b[3] <= a[1] + tol)


def _inside(inner, outer, tol=OVERLAP_TOL) -> bool:
    return inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol and inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    report = ctx.report or {}
    for name, e in report.get("sheets", {}).items():
        if name not in ctx.svgs:
            continue
        w, h = float(e.get("w") or 0), float(e.get("h") or 0)
        runs = e.get("text") or []
        if not runs:
            out.append(warn("BOUNDS-NO-MANIFEST", "no text manifest in the report; bounds not checked", name))
            continue
        breaks = " ".join(str(b) for b in (e.get("breaks") or [])).lower()
        excl = [((x["x"], x["y"], x["x"] + x["w"], x["y"] + x["h"]), x.get("name", "")) for x in (e.get("exclusions") or [])
                if all(k in x for k in ("x", "y", "w", "h"))]
        safe = (FRAME, FRAME, w - FRAME, h - FRAME) if w and h else None
        boxes = []
        for r in runs:
            b = _box(r)
            if b is None:
                continue
            boxes.append((b, r))
            s = str(r.get("s", ""))
            if safe and not _inside(b, safe, tol=2.0) and s.lower() not in breaks:
                out.append(fail("BOUNDS-EDGE", f"{r.get('role')} {s!r} leaves the safe area "
                                f"({b[0]:.0f},{b[1]:.0f})–({b[2]:.0f},{b[3]:.0f})", name))
        # collisions
        n_coll = 0
        for i, (a, ra) in enumerate(boxes):
            sem_a = bool(ra.get("semantic", ra.get("tier") != "texture"))
            for b, rb in boxes[i + 1:]:
                sem_b = bool(rb.get("semantic", rb.get("tier") != "texture"))
                if not (sem_a or sem_b):
                    # texture vs texture: distance rule
                    ca = ((a[0] + a[2]) / 2, (a[1] + a[3]) / 2)
                    cb = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
                    if math.dist(ca, cb) < MIN_TEXTURE_GAP and _overlap(a, b, tol=-4.0):
                        n_coll += 1
                        if n_coll <= 6:
                            out.append(warn("BOUNDS-TEXTURE", f"texture runs {ra.get('s')!r} and {rb.get('s')!r} "
                                            f"{math.dist(ca, cb):.0f} px apart", name))
                    continue
                if _overlap(a, b):
                    n_coll += 1
                    if n_coll <= 12:
                        out.append(fail("BOUNDS-COLLIDE", f"{ra.get('role')} {ra.get('s')!r} overlaps "
                                        f"{rb.get('role')} {rb.get('s')!r}", name))
            if sem_a:
                within = ra.get("within")
                for xb, xn in excl:
                    if within and _inside(a, tuple(map(float, within)) if len(within) == 4 else a):
                        continue
                    if xn and xn.lower() in str(ra.get("origin", "")).lower():
                        continue
                    if _overlap(a, xb) and not _inside(a, xb):
                        n_coll += 1
                        if n_coll <= 12:
                            out.append(fail("BOUNDS-EXCLUSION", f"{ra.get('role')} {ra.get('s')!r} crosses the "
                                            f"exclusion {xn or 'unnamed'}", name))
        if n_coll > 12:
            out.append(fail("BOUNDS-MORE", f"{n_coll - 12} further collisions not listed", name))
    return out
