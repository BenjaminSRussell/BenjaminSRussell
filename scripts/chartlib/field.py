"""field.py — the depth field, its contours and path compaction (T6 §2.2, MASTERPLAN 15–17).

Depth = count, on every sheet. The soundings generate the field: each weekly value is a compact
bump kernel W(q) = (1 − q²)³ of support h_snd whose amplitude is solved so the field equals the
printed value at its position. Features lift the field: islands break the surface (coastline at
depth 0), shoals stop between 0 and 5 (danger line at the 5-contour). Area is asserted at the
5-contour for every feature. A Coast falloff drives the field back to `base` within `inset` px
of the drawable rect and across the unsurveyed boundary, so every tint polygon closes.

No text, no colour, no randomness here. Pure Python (stdlib only).
"""
from __future__ import annotations

import math
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field as dc_field

# ------------------------------------------------------------------ numbers
def fmt(v: float) -> str:
    """Integer when within 0.05 of one, else one decimal. Never '-0'."""
    r = round(v)
    if abs(v - r) < 0.05:
        return str(int(r)) if r != 0 else "0"
    s = f"{v:.1f}"
    return "0" if s in ("-0.0", "0.0") else s


def smoothstep(t: float) -> float:
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return t * t * (3 - 2 * t)


def bump(q: float) -> float:
    """The compact bump kernel W(q) = (1 − q²)³, zero at and beyond q = 1."""
    return (1 - q * q) ** 3 if q < 1 else 0.0


# Support ratio h / r per feature kind, within MASTERPLAN 16's 1.33–1.82 r. In the depth frame the
# amplitude is solved so the 5-ring sits at r, and the ratio only sets the shelf width: at 1.33 an
# island's 0, 5 and 10 contours fall within ~4 % of r (a cliff); at 1.82 the coastline sits at
# ~0.88 r and the 10-contour at ~1.14 r (base 20), a shelf the eye can read. Override per feature
# with Feature.ratio.
KERNEL_RATIO = {"island": 1.82, "harbour": 1.82, "islet": 1.82, "shoal": 1.82, "wreck": 0.0}
LAND_KINDS = ("island", "harbour", "islet")
SHOAL_KINDS = ("shoal",)
DEFAULT_LEVELS = (0.0, 5.0, 10.0, 20.0, 50.0)


# ------------------------------------------------------------------ coast falloff
@dataclass
class Coast:
    """Edge falloff: factor() is 1 in open water, smoothsteps to 0 over `inset` px inside the
    drawable rect, and over `unsurveyed_x=(a, b)` from a to b. The field is `base + factor·(d − base)`."""
    rect: tuple  # (x, y, w, h)
    inset: float = 24.0
    unsurveyed_x: tuple | None = (1080, 1150)

    def factor(self, x: float, y: float) -> float:
        x0, y0, w, h = self.rect
        f = 1.0
        for d in (x - x0, x0 + w - x, y - y0, y0 + h - y):
            if d <= 0:
                return 0.0
            if d < self.inset:
                f *= smoothstep(d / self.inset)
        if self.unsurveyed_x:
            a, b = self.unsurveyed_x
            if x >= b:
                return 0.0
            if x > a:
                f *= 1.0 - smoothstep((x - a) / (b - a))
        return f


# ------------------------------------------------------------------ kernels
@dataclass
class Kernel:
    x: float
    y: float
    h: float      # support radius
    amp: float    # lift (positive = shallower) for land/shoal kinds; water delta for "water"
    kind: str     # "water" | "land" | "shoal"


@dataclass
class FieldReport:
    n_samples: int = 0
    residual_max: float = 0.0          # max |field(p_k) − value_k| over unfaded samples
    faded: list = dc_field(default_factory=list)      # sample indices with coast factor < 0.35
    on_feature: list = dc_field(default_factory=list)  # sample indices sitting on a feature's lift
    clamped: list = dc_field(default_factory=list)     # samples < shoal_floor held at the floor by a shoal
    ridge_used: float = 0.0
    refine_steps: int = 0
    bracket_failures: list = dc_field(default_factory=list)
    unclosed: list = dc_field(default_factory=list)   # (level, length) of open contours
    grid: tuple = (0, 0)


# ------------------------------------------------------------------ the field
@dataclass
class Field:
    w: int
    h: int
    base: float = 20.0
    cell: float = 8.0
    coast: Coast | None = None
    kernels: list = dc_field(default_factory=list)
    floor: float = 0.5          # open water never shallower than this (no spurious coastline)
    shoal_floor: float = 2.0    # a shoal alone never shallower than this (tinted, never land)
    report: FieldReport = dc_field(default_factory=FieldReport)
    _grid: list | None = dc_field(default=None, repr=False)
    _xs: list | None = dc_field(default=None, repr=False)
    _ys: list | None = dc_field(default=None, repr=False)

    # ---- construction
    @classmethod
    def from_soundings(cls, w, h, samples, base, features=(), coast: Coast | None = None,
                       kernel: str = "bump", h_snd: float = 30.0, ridge: float = 1e-3,
                       extra=(), level: float = 5.0, cell: float = 8.0, refine: int = 4) -> "Field":
        """samples: [(x, y, value)]; features: Feature objects (kind, x, y, r; amp/h are set here);
        extra: [(x, y, h, amp)] free land kernels (negative amp deepens: harbour basins, carves).
        Solves the sounding amplitudes so field(x_k, y_k) == value_k (zero weeks → floor)."""
        if kernel != "bump":
            raise ValueError("only the compact bump kernel is implemented (MASTERPLAN 16)")
        f = cls(w=int(w), h=int(h), base=float(base), cell=float(cell), coast=coast)
        f.report.ridge_used = ridge
        for ft in features:
            k = feature_kernel(ft, base, level)
            if k is not None:
                f.kernels.append(k)
        for (x, y, hh, amp) in extra:
            f.kernels.append(Kernel(x, y, hh, amp, "land"))
        f._solve_soundings(samples, h_snd, ridge, refine)
        return f

    @classmethod
    def synthetic(cls, w, h, seed, base, features=(), coast: Coast | None = None, n: int = 6,
                  spread: float = 0.5, cell: float = 8.0) -> "Field":
        """Illustrative sheets (T3): n seeded soundings around base ± spread·base, Halton positions."""
        from .place import halton
        from .furniture import Jitter
        jit = Jitter(seed, "synthetic")
        samples = []
        for i in range(n):
            u, v = halton(i + 1, 2), halton(i + 1, 3)
            samples.append((w * (0.1 + 0.8 * u), h * (0.1 + 0.8 * v),
                            max(0.5, base * (1 + spread * jit.uniform(-1, 1)))))
        return cls.from_soundings(w, h, samples, base, features, coast, cell=cell)

    def _solve_soundings(self, samples, h_snd, ridge, refine):
        n = len(samples)
        self.report.n_samples = n
        if n == 0:
            return
        base = self.base
        targets = []
        for i, (x, y, v) in enumerate(samples):
            fct = self.coast.factor(x, y) if self.coast else 1.0
            land, shoal = self._lift(x, y)
            if fct < 0.35:
                self.report.faded.append(i)
            if land + shoal > 0.5 * base:
                self.report.on_feature.append(i)
            t = max(float(v), self.floor)
            fe = max(fct, 0.35)
            water_k = base + (t - base) / fe + land + shoal
            targets.append(water_k - base)
        # matrix W_kj = W(|p_k − p_j| / h_snd)
        M = [[bump(math.hypot(samples[k][0] - samples[j][0], samples[k][1] - samples[j][1]) / h_snd)
              for j in range(n)] for k in range(n)]
        amps, steps = solve_ridge(M, targets, ridge, refine)
        self.report.refine_steps = steps
        for (x, y, _v), a in zip(samples, amps):
            self.kernels.append(Kernel(x, y, h_snd, a, "water"))
        self._grid = None
        # residuals (unfaded samples only); a sounding shallower than shoal_floor inside a shoal's
        # support is held at the floor (shoals never break the surface) and reported as clamped
        worst = 0.0
        for i, (x, y, v) in enumerate(samples):
            if i in self.report.faded:
                continue
            res = abs(self.value(x, y) - max(float(v), self.floor))
            if res > 1e-6 and float(v) < self.shoal_floor and self._lift(x, y)[1] > 0:
                self.report.clamped.append(i)
                continue
            worst = max(worst, res)
        self.report.residual_max = worst

    # ---- evaluation
    def _lift(self, x, y):
        land = shoal = 0.0
        for k in self.kernels:
            if k.kind == "water":
                continue
            dx, dy = x - k.x, y - k.y
            if abs(dx) >= k.h or abs(dy) >= k.h:
                continue
            q = math.hypot(dx, dy) / k.h
            if q < 1:
                if k.kind == "land":
                    land += k.amp * bump(q)
                else:
                    shoal += k.amp * bump(q)
        return land, shoal

    def _combine(self, water, land, shoal, fct):
        water = max(water, self.floor)
        if shoal > 0:
            shoal = min(shoal, max(0.0, water - self.shoal_floor))
        d = water - land - shoal
        return self.base + fct * (d - self.base)

    def value(self, x: float, y: float) -> float:
        """Depth in sheet units at (x, y); land < 0."""
        water = self.base
        land = shoal = 0.0
        for k in self.kernels:
            dx, dy = x - k.x, y - k.y
            if abs(dx) >= k.h or abs(dy) >= k.h:
                continue
            q = math.hypot(dx, dy) / k.h
            if q >= 1:
                continue
            wv = k.amp * bump(q)
            if k.kind == "water":
                water += wv
            elif k.kind == "land":
                land += wv
            else:
                shoal += wv
        fct = self.coast.factor(x, y) if self.coast else 1.0
        return self._combine(water, land, shoal, fct)

    def axes(self):
        if self._xs is None:
            gx = int(round(self.w / self.cell)) + 1
            gy = int(round(self.h / self.cell)) + 1
            self._xs = [i * self.w / (gx - 1) for i in range(gx)]
            self._ys = [j * self.h / (gy - 1) for j in range(gy)]
        return self._xs, self._ys

    def grid(self) -> list[list[float]]:
        """Cached depth grid (rows of gy × gx); cleared when kernels change (call invalidate())."""
        if self._grid is None:
            xs, ys = self.axes()
            self._grid = self._evaluate(xs, ys)
            self.report.grid = (len(xs), len(ys))
        return self._grid

    def invalidate(self):
        self._grid = None

    def local_grid(self, rect) -> tuple[list, list, list]:
        """The global grid's own nodes inside rect=(x, y, w, h), evaluated: (xs, ys, rows)."""
        xs, ys = self.axes()
        x0, y0, w, h = rect
        i0, i1 = max(0, bisect_left(xs, x0) - 1), min(len(xs), bisect_right(xs, x0 + w) + 1)
        j0, j1 = max(0, bisect_left(ys, y0) - 1), min(len(ys), bisect_right(ys, y0 + h) + 1)
        sx, sy = xs[i0:i1], ys[j0:j1]
        if self._grid is not None:
            return sx, sy, [row[i0:i1] for row in self._grid[j0:j1]]
        return sx, sy, self._evaluate(sx, sy)

    def _evaluate(self, xs, ys):
        nx, ny = len(xs), len(ys)
        water = [[self.base] * nx for _ in range(ny)]
        land = [[0.0] * nx for _ in range(ny)]
        shoal = [[0.0] * nx for _ in range(ny)]
        for k in self.kernels:
            tgt = water if k.kind == "water" else land if k.kind == "land" else shoal
            i0, i1 = bisect_left(xs, k.x - k.h), bisect_right(xs, k.x + k.h)
            j0, j1 = bisect_left(ys, k.y - k.h), bisect_right(ys, k.y + k.h)
            if i0 >= i1 or j0 >= j1:
                continue
            h2, amp = k.h * k.h, k.amp
            for j in range(j0, j1):
                dy2 = (ys[j] - k.y) ** 2
                row = tgt[j]
                for i in range(i0, i1):
                    d2 = (xs[i] - k.x) ** 2 + dy2
                    if d2 < h2:
                        q2 = d2 / h2
                        row[i] += amp * (1 - q2) ** 3
        out = []
        coast = self.coast
        for j in range(ny):
            y = ys[j]
            wr, lr, sr = water[j], land[j], shoal[j]
            out.append([self._combine(wr[i], lr[i], sr[i], coast.factor(xs[i], y) if coast else 1.0)
                        for i in range(nx)])
        return out


def feature_kernel(ft, base: float, level: float = 5.0) -> Kernel | None:
    """The lift kernel of a Feature: support h = ratio·r, amplitude so depth == level at distance r.
    Sets ft.h and ft.amp. Wrecks (r == 0) have no kernel."""
    kind = ft.kind
    ratio = getattr(ft, "ratio", None) or KERNEL_RATIO.get(kind, 1.82)
    if ft.r <= 0 or ratio <= 0:
        return None
    h = ratio * ft.r
    wb = bump(1.0 / ratio)
    amp = (base - level) / wb if wb > 0 else 0.0
    ft.h, ft.amp = h, amp
    return Kernel(ft.x, ft.y, h, amp, "land" if kind in LAND_KINDS else "shoal")


# ------------------------------------------------------------------ linear algebra (n ≤ 60)
def lu_solve(A: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting on a copy of A (n×n) and b. Pure Python."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-14:
            continue  # singular column: leave it (ridge should prevent this)
        if p != c:
            M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / piv
            if f:
                rowr, rowc = M[r], M[c]
                for k in range(c, n + 1):
                    rowr[k] -= f * rowc[k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / M[r][r] if abs(M[r][r]) > 1e-14 else 0.0
    return x


def solve_ridge(M, d, ridge: float = 1e-3, refine: int = 3) -> tuple[list[float], int]:
    """Solve M a = d. Factor (M + ridge·I) and refine against M itself: well-conditioned systems
    converge to the exact solution (residual ~1e-9), clustered points stay damped by the ridge.
    Returns (a, refinement steps taken)."""
    n = len(d)
    R = [[M[i][j] + (ridge if i == j else 0.0) for j in range(n)] for i in range(n)]
    a = lu_solve(R, d)
    steps = 0
    prev = math.inf
    for _ in range(refine):
        res = [d[i] - sum(M[i][j] * a[j] for j in range(n)) for i in range(n)]
        norm = max((abs(v) for v in res), default=0.0)
        if norm < 1e-12 or norm > 0.5 * prev:
            break
        prev = norm
        corr = lu_solve(R, res)
        a = [ai + ci for ai, ci in zip(a, corr)]
        steps += 1
    return a, steps


# ------------------------------------------------------------------ contours
@dataclass
class Contour:
    level: float
    pts: list                 # [(x, y)] floats in sheet space; closed polygons do not repeat pt 0
    closed: bool
    length: float
    shallow_inside: bool | None = None   # closed only: True when the enclosed region is < level

    def area(self) -> float:
        return abs(polygon_area(self.pts)) if self.closed else 0.0

    def centroid(self):
        return polygon_centroid(self.pts)

    def contains(self, x, y) -> bool:
        return self.closed and point_in_polygon(x, y, self.pts)


def polygon_area(pts) -> float:
    """Signed shoelace area (positive when the interior is on the left of travel)."""
    a = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return a / 2


def polygon_centroid(pts):
    a = cx = cy = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    if abs(a) < 1e-9:
        return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
    return (cx / (3 * a), cy / (3 * a))


def point_in_polygon(x, y, pts) -> bool:
    inside = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y):
            xx = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < xx:
                inside = not inside
        j = i
    return inside


def polyline_length(pts, closed=False) -> float:
    L = 0.0
    n = len(pts)
    for i in range(n - 1):
        L += math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
    if closed and n > 1:
        L += math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1])
    return L


def _cell_segments(xs, ys, rows, level):
    """Marching squares. Segments are directed so the shallow (< level) side is on the LEFT
    (positive cross product), which makes closed chains with shallow interiors have positive area."""
    out = []
    ny, nx = len(ys), len(xs)
    for j in range(ny - 1):
        r0, r1 = rows[j], rows[j + 1]
        y0, y1 = ys[j], ys[j + 1]
        for i in range(nx - 1):
            a, b, c, d = r0[i], r0[i + 1], r1[i + 1], r1[i]
            sa, sb, sc, sd = a < level, b < level, c < level, d < level
            if sa == sb == sc == sd:
                continue
            x0, x1 = xs[i], xs[i + 1]

            def lerp(px, py, qx, qy, va, vb):
                t = (level - va) / (vb - va) if vb != va else 0.5
                return (px + (qx - px) * t, py + (qy - py) * t)

            pts = {}
            if sa != sb:
                pts["t"] = lerp(x0, y0, x1, y0, a, b)
            if sb != sc:
                pts["r"] = lerp(x1, y0, x1, y1, b, c)
            if sd != sc:
                pts["b"] = lerp(x0, y1, x1, y1, d, c)
            if sa != sd:
                pts["l"] = lerp(x0, y0, x0, y1, a, d)
            corners = ((x0, y0, sa), (x1, y0, sb), (x1, y1, sc), (x0, y1, sd))
            keys = list(pts)
            if len(keys) == 2:
                pairs = [(pts[keys[0]], pts[keys[1]])]
            elif len(keys) == 4:
                centre_shallow = (a + b + c + d) / 4 < level
                if centre_shallow == sa:
                    pairs = [(pts["t"], pts["r"]), (pts["b"], pts["l"])]
                else:
                    pairs = [(pts["t"], pts["l"]), (pts["r"], pts["b"])]
            else:
                continue
            for A, B in pairs:
                if abs(A[0] - B[0]) < 1e-9 and abs(A[1] - B[1]) < 1e-9:
                    continue  # a node exactly on the level: degenerate
                side = 0.0
                for cx, cy, sh in corners:
                    if sh:
                        side += (B[0] - A[0]) * (cy - A[1]) - (B[1] - A[1]) * (cx - A[0])
                out.append((A, B) if side >= 0 else (B, A))
    return out


def _chain(segs):
    key = lambda p: (round(p[0], 6), round(p[1], 6))
    by_start, by_end = {}, {}
    for idx, (A, B) in enumerate(segs):
        by_start.setdefault(key(A), []).append(idx)
        by_end.setdefault(key(B), []).append(idx)
    used = [False] * len(segs)
    lines = []
    for idx in range(len(segs)):
        if used[idx]:
            continue
        used[idx] = True
        A, B = segs[idx]
        line = [A, B]
        # forward
        while True:
            cands = [t for t in by_start.get(key(line[-1]), []) if not used[t]]
            if not cands:
                break
            t = cands[0]
            used[t] = True
            line.append(segs[t][1])
        # backward
        while True:
            cands = [t for t in by_end.get(key(line[0]), []) if not used[t]]
            if not cands:
                break
            t = cands[0]
            used[t] = True
            line.insert(0, segs[t][0])
        lines.append(line)
    return lines


def contours(field: Field, levels, clip=None) -> list[Contour]:
    """Marching squares + chaining on the field grid (or on the grid nodes inside clip=(x,y,w,h)).
    Closed contours drop the repeated end point and carry shallow_inside."""
    if clip is None:
        xs, ys = field.axes()
        rows = field.grid()
    else:
        xs, ys, rows = field.local_grid(clip)
    out = []
    for lv in levels:
        for line in _chain(_cell_segments(xs, ys, rows, lv)):
            closed = (abs(line[0][0] - line[-1][0]) < 1e-6 and abs(line[0][1] - line[-1][1]) < 1e-6
                      and len(line) > 3)
            if closed:
                line = line[:-1]
            if len(line) < 2:
                continue
            c = Contour(lv, line, closed, polyline_length(line, closed))
            if closed:
                c.shallow_inside = polygon_area(line) > 0
            out.append(c)
    return out


def closed_check(cs: list[Contour], levels=None, min_len: float = 30.0) -> list[tuple]:
    """Open contours longer than min_len at the given levels: [(level, length)]. Empty is good."""
    bad = []
    for c in cs:
        if not c.closed and c.length >= min_len and (levels is None or c.level in levels):
            bad.append((c.level, round(c.length)))
    return bad


def band_of(cs: list[Contour], x, y, levels, base: float | None = None) -> float | None:
    """The smallest level L such that (x, y) is under L: inside an odd number of closed L-polygons
    (evenodd nesting) when the ambient water is deeper than L, or inside an even number when the
    ambient water (`base`) is itself under L. None = deeper than every level. With base=None the
    unbounded region counts as deep."""
    for lv in sorted(levels):
        inside = base is not None and base < lv
        for c in cs:
            if c.level != lv or not c.closed:
                continue
            if c.contains(x, y):
                inside = not inside
        if inside:
            return lv
    return None


def bracket_test(cs: list[Contour], samples, levels=DEFAULT_LEVELS, base: float | None = None,
                 tie: float = 0.02, skip=(), field: Field | None = None) -> list[tuple]:
    """Every numeral must sit inside the band labelled ≤ n and outside the next (T2 §2.4).
    Returns failures [(index, x, y, value, expected_band, found_band, cause)]; near-ties
    (|v − L| < tie·L) and indices in `skip` (faded soundings the sheet does not print) are not
    tested. Pass the field's `base` so the unbounded open-water region is banded correctly. With
    `field`, cause is 'field' when the field itself is wrong there and 'unresolved' when the field
    is right but the ring is too small for the grid (a lone sounding far from base makes a ring of
    a few px; nudge it or draw it at a finer cell)."""
    fails = []
    lv = sorted(levels)
    skip = set(skip)
    for i, (x, y, v) in enumerate(samples):
        if i in skip or any(abs(v - L) < max(tie * L, 1e-9) for L in lv):
            continue
        expected = next((L for L in lv if v < L), None)
        found = band_of(cs, x, y, lv, base)
        if expected != found:
            cause = "polygon"
            if field is not None:
                fv = field.value(x, y)
                cause = "field" if next((L for L in lv if fv < L), None) != expected else "unresolved"
            fails.append((i, round(x), round(y), v, expected, found, cause))
    return fails


# ------------------------------------------------------------------ paths
def _subsample(pts, every: int, closed: bool):
    if every <= 1 or len(pts) <= 6:
        return list(pts)
    core = pts[::every]
    if not closed and (len(pts) - 1) % every:
        core = core + [pts[-1]]
    return core


def compact_path(pts, closed: bool, every: int = 3) -> str:
    """Relative integer commands: 'M x y l dx dy … Z', h/v where one delta is 0; subsampled."""
    sub = _subsample(pts, every, closed)
    ints = [(int(round(x)), int(round(y))) for x, y in sub]
    out = []
    px = py = None
    for x, y in ints:
        if px is None:
            out.append(f"M{x} {y}")
        else:
            dx, dy = x - px, y - py
            if dx == 0 and dy == 0:
                continue
            out.append(f"l{dx} {dy}" if dx and dy else (f"h{dx}" if dx else f"v{dy}"))
        px, py = x, y
    if closed:
        if len(out) > 1 and ints[0] == (px, py):
            out.pop()  # already back at the start
        out.append("Z")
    return "".join(out)


def parse_path(d: str) -> list[tuple[int, int]]:
    """Inverse of compact_path for tests/consumers: absolute integer points (closing Z ignored)."""
    import re
    pts = []
    x = y = 0
    for cmd, args in re.findall(r"([MmLlHhVvZz])([^MmLlHhVvZz]*)", d):
        nums = [int(float(n)) for n in re.findall(r"-?\d+(?:\.\d+)?", args)]
        if cmd == "M":
            x, y = nums[0], nums[1]
            pts.append((x, y))
            for i in range(2, len(nums), 2):
                x, y = nums[i], nums[i + 1]
                pts.append((x, y))
        elif cmd == "l":
            for i in range(0, len(nums), 2):
                x, y = x + nums[i], y + nums[i + 1]
                pts.append((x, y))
        elif cmd == "L":
            for i in range(0, len(nums), 2):
                x, y = nums[i], nums[i + 1]
                pts.append((x, y))
        elif cmd == "h":
            for n in nums:
                x += n
                pts.append((x, y))
        elif cmd == "v":
            for n in nums:
                y += n
                pts.append((x, y))
        elif cmd == "H":
            for n in nums:
                x = n
                pts.append((x, y))
        elif cmd == "V":
            for n in nums:
                y = n
                pts.append((x, y))
    return pts


def smooth_path(pts, closed: bool, every: int = 2) -> str:
    """Catmull-Rom through the (subsampled) points as relative integer cubics. Coast and course only."""
    sub = _subsample(pts, every, closed)
    if len(sub) < 3:
        return compact_path(sub, closed, 1)
    n = len(sub)
    P = [(int(round(x)), int(round(y))) for x, y in sub]
    out = [f"M{P[0][0]} {P[0][1]}"]
    cx, cy = P[0]
    segs = n if closed else n - 1
    for i in range(segs):
        p1, p2 = P[i], P[(i + 1) % n]
        p0 = P[i - 1] if (i > 0 or closed) else p1
        p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (round(p1[0] + (p2[0] - p0[0]) / 6), round(p1[1] + (p2[1] - p0[1]) / 6))
        c2 = (round(p2[0] - (p3[0] - p1[0]) / 6), round(p2[1] - (p3[1] - p1[1]) / 6))
        out.append(f"c{c1[0]-cx} {c1[1]-cy} {c2[0]-cx} {c2[1]-cy} {p2[0]-cx} {p2[1]-cy}")
        cx, cy = p2
    if closed:
        out.append("Z")
    return "".join(out)


def monotone_path(pts, baseline: float | None = None) -> str:
    """Fritsch–Carlson monotone cubic through (x, y) points with increasing x; one-decimal coords.
    With baseline=y0 the path closes down to that y (a filled tide curve)."""
    n = len(pts)
    if n == 0:
        return ""
    if n == 1:
        return f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    dx = [xs[i + 1] - xs[i] for i in range(n - 1)]
    dy = [ys[i + 1] - ys[i] for i in range(n - 1)]
    delta = [dy[i] / dx[i] if dx[i] else 0.0 for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = delta[0], delta[-1]
    for i in range(1, n - 1):
        if delta[i - 1] * delta[i] <= 0:
            m[i] = 0.0
        else:
            w1, w2 = 2 * dx[i] + dx[i - 1], dx[i] + 2 * dx[i - 1]
            m[i] = (w1 + w2) / (w1 / delta[i - 1] + w2 / delta[i])
    for i in range(n - 1):
        if delta[i] == 0:
            m[i] = m[i + 1] = 0.0
        else:
            a, b = m[i] / delta[i], m[i + 1] / delta[i]
            s = a * a + b * b
            if s > 9:
                t = 3 / math.sqrt(s)
                m[i], m[i + 1] = t * a * delta[i], t * b * delta[i]
    out = [f"M{fmt(xs[0])} {fmt(ys[0])}"]
    for i in range(n - 1):
        h = dx[i]
        c1 = (xs[i] + h / 3, ys[i] + m[i] * h / 3)
        c2 = (xs[i + 1] - h / 3, ys[i + 1] - m[i + 1] * h / 3)
        out.append(f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(xs[i+1])} {fmt(ys[i+1])}")
    if baseline is not None:
        out.append(f"V{fmt(baseline)}H{fmt(xs[0])}Z")
    return "".join(out)


def clip_polyline(pts, rect, closed=False):
    """Split a polyline at the edges of rect=(x, y, w, h): (inside_parts, outside_parts)."""
    x0, y0, w, h = rect
    x1, y1 = x0 + w, y0 + h
    inside_fn = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    seq = list(pts) + ([pts[0]] if closed and pts else [])
    ins, outs = [], []
    cur, cur_in = [], None
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]
        # parametric crossings with the four edges
        ts = [0.0, 1.0]
        for edge, (p, q) in (("x", (a[0], b[0])), ("y", (a[1], b[1]))):
            lo, hi = (x0, x1) if edge == "x" else (y0, y1)
            if q != p:
                for bound in (lo, hi):
                    t = (bound - p) / (q - p)
                    if 0 < t < 1:
                        ts.append(t)
        ts.sort()
        for t0, t1 in zip(ts, ts[1:]):
            if t1 - t0 < 1e-9:
                continue
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            is_in = inside_fn(mid)
            if cur_in is None or is_in != cur_in:
                if cur:
                    (ins if cur_in else outs).append(cur)
                cur, cur_in = [p0, p1], is_in
            else:
                cur.append(p1)
    if cur:
        (ins if cur_in else outs).append(cur)
    return ins, outs


# ------------------------------------------------------------------ labels in breaks
def _tangent_angle(pts, i, closed):
    n = len(pts)
    if closed:
        p, q = pts[(i - 1) % n], pts[(i + 1) % n]
    else:
        p, q = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def contour_labels(cs: list[Contour], role: str = "contour-figure", min_len: float = 160.0,
                   gap: float = 20.0, exclusions=(), max_tilt: float = 30.0, levels=None,
                   skip_levels=(0.0,)) -> list[tuple]:
    """For every contour with length ≥ min_len (at `levels`, or all but skip_levels — the coastline
    is never figured): the break (contour, i0, i1) around the point of lowest curvature whose
    tangent is within max_tilt° of horizontal and which avoids `exclusions` (rects). The figure is
    set by the caller at break_anchor(); the gap is `width + 6`, by default 20."""
    out = []
    for c in cs:
        if c.length < min_len or len(c.pts) < 8:
            continue
        if (levels is not None and c.level not in levels) or c.level in skip_levels:
            continue
        n = len(c.pts)
        best, best_i = None, None
        for i in range(n):
            if not c.closed and (i < 3 or i > n - 4):
                continue
            ang = _tangent_angle(c.pts, i, c.closed)
            tilt = abs(((ang + 90) % 180) - 90)
            if tilt > max_tilt:
                continue
            x, y = c.pts[i]
            if any(ex[0] <= x <= ex[0] + ex[2] and ex[1] <= y <= ex[1] + ex[3] for ex in exclusions):
                continue
            # curvature over a ±3 window: total turning per arc length
            turn = 0.0
            for k in range(-3, 3):
                a0 = _tangent_angle(c.pts, (i + k) % n if c.closed else min(max(i + k, 0), n - 1), c.closed)
                a1 = _tangent_angle(c.pts, (i + k + 1) % n if c.closed else min(max(i + k + 1, 0), n - 1), c.closed)
                turn += abs(((a1 - a0 + 180) % 360) - 180)
            score = turn + tilt * 0.2
            if best is None or score < best:
                best, best_i = score, i
        if best_i is None:
            continue
        # walk gap/2 each way
        def walk(i, step):
            acc, j = 0.0, i
            while acc < gap / 2:
                nj = (j + step) % n if c.closed else j + step
                if not c.closed and (nj < 0 or nj >= n):
                    break
                acc += math.hypot(c.pts[nj][0] - c.pts[j][0], c.pts[nj][1] - c.pts[j][1])
                j = nj
            return j
        i0, i1 = walk(best_i, -1), walk(best_i, +1)
        if i0 == i1:
            continue
        out.append((c, i0, i1))
    return out


def break_anchor(c: Contour, i0: int, i1: int) -> tuple[float, float, float]:
    """(x, y, angle°) at the middle of the break, angle within ±90 so the figure reads upright."""
    n = len(c.pts)
    if c.closed:
        span = (i1 - i0) % n
        mid = (i0 + span // 2) % n
    else:
        mid = (i0 + i1) // 2
    x, y = c.pts[mid]
    ang = _tangent_angle(c.pts, mid, c.closed)
    if ang > 90:
        ang -= 180
    elif ang < -90:
        ang += 180
    return (round(x, 1), round(y, 1), round(ang, 1))


def broken_polylines(c: Contour, i0: int, i1: int) -> list[list]:
    """The contour minus the vertices strictly between i0 and i1 (the gap), as open polylines."""
    n = len(c.pts)
    if c.closed:
        # one open run from i1 forward around to i0
        run = []
        j = i1
        while True:
            run.append(c.pts[j])
            if j == i0:
                break
            j = (j + 1) % n
        return [run]
    return [p for p in (c.pts[:i0 + 1], c.pts[i1:]) if len(p) >= 2]


def draw_contours(cs: list[Contour], index_levels, theme, approx_clip=None, breaks=(),
                  opacity: float = 0.55, every: int = 3, skip_levels=(0.0,), min_len: float = 0.0) -> str:
    """Intermediate levels at PEN, index levels at LINE, both ink2 at `opacity`; broken where
    `breaks` (from contour_labels) say; portions inside approx_clip redrawn with DASH['APPROX'].
    Level 0 (the coastline) is skipped by default: coastline() draws it. Closed loops shorter than
    min_len (the ring a lone sounding makes under its own numeral) are not drawn."""
    from .furniture import stroke
    bmap = {id(c): (i0, i1) for c, i0, i1 in breaks}
    groups = {}  # (is_index, approx) -> [d]
    for c in cs:
        if c.level in skip_levels or (c.closed and c.length < min_len):
            continue
        is_index = c.level in index_levels
        runs = broken_polylines(c, *bmap[id(c)]) if id(c) in bmap else [c.pts]
        run_closed = c.closed and id(c) not in bmap
        for run in runs:
            if approx_clip:
                ins, outs = clip_polyline(run, approx_clip, run_closed)
                for part in outs:
                    groups.setdefault((is_index, False), []).append(compact_path(part, False, every))
                for part in ins:
                    groups.setdefault((is_index, True), []).append(compact_path(part, False, every))
            else:
                groups.setdefault((is_index, False), []).append(compact_path(run, run_closed, every))
    out = []
    for (is_index, approx), ds in sorted(groups.items()):
        attrs = stroke("LINE" if is_index else "PEN", theme.ink2, opacity, "APPROX" if approx else None)
        out.append(f'<path d="{"".join(ds)}" fill="none" {attrs}/>')
    return "".join(out)
