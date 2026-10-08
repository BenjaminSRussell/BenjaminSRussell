"""timeline.py — the motion engine (T4).

One ``Timeline`` per sheet build. It resolves cues to absolute seconds, emits SMIL that
Chromium repaints only on change (``opacity`` and ``animateTransform``), enforces the motion
rules at emit time, and in still mode (``motion=False``) returns end states from the same code
path so the ``*-still`` editions are built by the same sheet code.

Rules (MASTERPLAN 7.3, T4 §2.1; raise = ValueError, record = ``report()["violations"]``):

* an indefinite repeat only on ``opacity``/``transform`` (raise); only ``flash()``,
  ``every()`` and the looping form of ``fixes()`` emit it, and ``fixes()`` goes through ``every``.
* a continuous (non-discrete) loop only when ``ambient=True`` (raise).
* every discrete instant (loop begins and value changes, ``reveal`` begins, discrete one-shots)
  on the ``quantum`` grid: a begin that is off-grid is snapped and recorded; an internal key
  instant that cannot be snapped without changing the author's keyTimes raises.
* geometry attributes (``x y cx cy width height r x1 y1 x2 y2 d points stroke-dashoffset`` …)
  never loop (raise) and only run in a finite one-shot of ``dur <= 4 s`` (record).
* no syncbase: ``begin`` is a number, never ``"name.end+0.4s"`` (raise); emitted strings are
  checked once more before they leave.
* every freeze-in (``fade_in``, ``reveal``, ``typed``, fix marks) carries base ``opacity="0"``.
* ``motion=False``: ``anim``/``xform``/``flash``/``every`` return ``''``; ``fade_in``/``reveal``
  return the bare element; ``draw_in`` a plain path; ``sail`` a static ``translate(x_end y_end)``.
  Loops must pass ``still`` explicitly so the still edition is a decision, not a default.

Pure Python, stdlib only. Imports ``tokens`` for EASE/LOOP_PERIODS/QUANTUM/PAGE_PERIOD and
nothing else, so chartlib, typeset and the sheets can import it freely.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

try:
    import tokens
except ImportError:  # pragma: no cover — imported as scripts.timeline
    from scripts import tokens  # type: ignore

EASE: dict[str, str] = dict(tokens.EASE)
LOOP_PERIODS: tuple = tuple(tokens.LOOP_PERIODS)
QUANTUM: float = tokens.QUANTUM
PAGE_PERIOD: float = tokens.PAGE_PERIOD

# Attributes whose animation re-rasters every frame while active (12 fact 4). Never looped;
# only inside a finite one-shot of <= GEOMETRY_MAX_DUR seconds (contour tracing).
GEOMETRY_ATTRS = frozenset({
    "x", "y", "cx", "cy", "width", "height", "r", "rx", "ry", "x1", "y1", "x2", "y2", "d",
    "points", "stroke-dashoffset", "stroke-dasharray", "stroke-width", "font-size", "offset",
    "startOffset", "pathLength", "viewBox",
})
GEOMETRY_MAX_DUR = 4.0
LOOP_ATTRS = frozenset({"opacity", "transform"})
TRANSFORM_KINDS = ("translate", "scale", "rotate", "skewX", "skewY")
SYNCBASE = re.compile(r'begin="[^"]*(?:[A-Za-z_][\w-]*\.(?:end|begin|repeat)|repeatEvent|accessKey|click|mouse)')
FLATTEN_PX = 1.0   # curves are flattened to chords no longer than this
GRID_TOL = 0.0025  # a discrete instant within 2.5 ms of the grid is on it (6-decimal keyTimes × 96 s)


# ----------------------------------------------------------------------------- small helpers
def _f(v: float, nd: int = 4) -> str:
    """Compact number: up to `nd` decimals, no trailing zeros, '-0' never."""
    if isinstance(v, bool):
        return str(int(v))
    if isinstance(v, int):
        return str(v)
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s


def _s(v: float) -> str:
    """Seconds attribute value."""
    return _f(v, 3) + "s"


def _vals(values) -> list[str]:
    if isinstance(values, str):
        return [p.strip() for p in values.split(";")]
    out = []
    for v in values:
        if isinstance(v, (list, tuple)):
            out.append(" ".join(_f(x) for x in v))
        elif isinstance(v, (int, float)):
            out.append(_f(v))
        else:
            out.append(str(v))
    return out


def _bez1(p1: float, p2: float, t: float) -> float:
    mt = 1.0 - t
    return 3 * mt * mt * t * p1 + 3 * mt * t * t * p2 + t * t * t


def ease_curve(ease) -> tuple[float, float, float, float]:
    """An EASE key or a 'x1 y1 x2 y2' string → the four control numbers."""
    if ease is None:
        ease = "linear"
    s = EASE.get(ease, ease)
    try:
        x1, y1, x2, y2 = (float(p) for p in s.replace(",", " ").split())
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"unknown ease {ease!r}") from exc
    return x1, y1, x2, y2


def ease_at(ease, x: float) -> float:
    """y of the easing's cubic Bézier at time fraction x (bisection on x)."""
    x1, y1, x2, y2 = ease_curve(ease)
    x = min(max(x, 0.0), 1.0)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _bez1(x1, x2, mid) < x:
            lo = mid
        else:
            hi = mid
    return _bez1(y1, y2, (lo + hi) / 2)


def ease_inverse(ease, progress: float) -> float:
    """Time fraction x at which the easing reaches `progress` (bisection on y, then x of t)."""
    x1, y1, x2, y2 = ease_curve(ease)
    progress = min(max(progress, 0.0), 1.0)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _bez1(y1, y2, mid) < progress:
            lo = mid
        else:
            hi = mid
    return _bez1(x1, x2, (lo + hi) / 2)


# ----------------------------------------------------------------------------- path sampling
_TOKEN = re.compile(r"[MmLlHhVvCcQqZzSsTtAa]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def _flatten_path(d: str, px: float = FLATTEN_PX) -> list[tuple[float, float]]:
    """Polyline through the path with chords <= `px` on curves. M/L/H/V/C/S/Q/T/Z, abs/rel."""
    toks = _TOKEN.findall(d)
    pts: list[tuple[float, float]] = []
    i = 0
    cmd = None
    cx = cy = 0.0
    sx = sy = 0.0
    last_ctrl = None

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    def add(p):
        if not pts or (abs(pts[-1][0] - p[0]) > 1e-9 or abs(pts[-1][1] - p[1]) > 1e-9):
            pts.append(p)

    def cubic(p0, p1, p2, p3):
        # chord count from the control polygon length
        L = (math.dist(p0, p1) + math.dist(p1, p2) + math.dist(p2, p3))
        n = max(2, int(math.ceil(L / px)))
        for k in range(1, n + 1):
            t = k / n
            mt = 1 - t
            x = mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0]
            y = mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1]
            add((x, y))

    def quad(p0, p1, p2):
        L = math.dist(p0, p1) + math.dist(p1, p2)
        n = max(2, int(math.ceil(L / px)))
        for k in range(1, n + 1):
            t = k / n
            mt = 1 - t
            add((mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0],
                 mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]))

    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                add((sx, sy))
                cx, cy = sx, sy
                last_ctrl = None
                continue
        if cmd is None:
            raise ValueError("path data must start with M")
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            x, y = num(), num()
            if rel:
                x += cx
                y += cy
            cx, cy = x, y
            sx, sy = x, y
            add((x, y))
            cmd = "l" if rel else "L"  # subsequent pairs are linetos
            last_ctrl = None
        elif c == "L":
            x, y = num(), num()
            if rel:
                x += cx
                y += cy
            cx, cy = x, y
            add((x, y))
            last_ctrl = None
        elif c == "H":
            x = num()
            if rel:
                x += cx
            cx = x
            add((cx, cy))
            last_ctrl = None
        elif c == "V":
            y = num()
            if rel:
                y += cy
            cy = y
            add((cx, cy))
            last_ctrl = None
        elif c in ("C", "S"):
            if c == "C":
                x1, y1 = num(), num()
                if rel:
                    x1 += cx
                    y1 += cy
            else:
                x1, y1 = (2 * cx - last_ctrl[0], 2 * cy - last_ctrl[1]) if last_ctrl else (cx, cy)
            x2, y2 = num(), num()
            x, y = num(), num()
            if rel:
                x2 += cx
                y2 += cy
                x += cx
                y += cy
            cubic((cx, cy), (x1, y1), (x2, y2), (x, y))
            last_ctrl = (x2, y2)
            cx, cy = x, y
        elif c in ("Q", "T"):
            if c == "Q":
                x1, y1 = num(), num()
                if rel:
                    x1 += cx
                    y1 += cy
            else:
                x1, y1 = (2 * cx - last_ctrl[0], 2 * cy - last_ctrl[1]) if last_ctrl else (cx, cy)
            x, y = num(), num()
            if rel:
                x += cx
                y += cy
            quad((cx, cy), (x1, y1), (x, y))
            last_ctrl = (x1, y1)
            cx, cy = x, y
        else:  # pragma: no cover — A (arcs) are not used by the chart engine
            raise ValueError(f"unsupported path command {cmd!r} (M/L/H/V/C/S/Q/T/Z only)")
    return pts


def path_length(d: str) -> float:
    pts = _flatten_path(d)
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def sample_path(d: str, n: int) -> list[tuple[float, float, float]]:
    """`n` points equally spaced by arc length along `d`: (x, y, heading°), heading = atan2(dy, dx)
    in SVG coordinates (0 = +x, 90 = down the sheet). Pure Python; curves flattened to <= 1 px."""
    if n < 2:
        raise ValueError("sample_path needs n >= 2")
    pts = _flatten_path(d)
    if len(pts) < 2:
        raise ValueError("path has no length")
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(seg)
    if total <= 0:
        raise ValueError("path has no length")
    cum = [0.0]
    for L in seg:
        cum.append(cum[-1] + L)
    out = []
    j = 0
    for i in range(n):
        s = total * i / (n - 1)
        while j < len(seg) - 1 and cum[j + 1] < s:
            j += 1
        # segment j spans cum[j]..cum[j+1]
        L = seg[j] or 1e-12
        u = min(max((s - cum[j]) / L, 0.0), 1.0)
        (x0, y0), (x1, y1) = pts[j], pts[j + 1]
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u
        # heading from a short window so flattened chords do not jitter it
        k0, k1 = max(0, j - 1), min(len(pts) - 1, j + 2)
        hx, hy = pts[k1][0] - pts[k0][0], pts[k1][1] - pts[k0][1]
        if abs(hx) < 1e-9 and abs(hy) < 1e-9:
            hx, hy = x1 - x0, y1 - y0
        out.append((x, y, math.degrees(math.atan2(hy, hx))))
    return out


# ----------------------------------------------------------------------------- light characters
_CHAR = re.compile(r"^\s*(LFl|Fl|Oc|Iso|Q|VQ|F)(?:\((\d+)\))?(?:\s+(?:[RGWY]|Bu))?(?:\s+(\d+(?:\.\d+)?)\s*s)?\s*$")
FLASH = 0.5        # one flash: 0.5 s (chart-plausible; <= 1 flash/s per light, under 09's 3/s)
LONG_FLASH = 2.0   # LFl


def parse_character(character: str, period: float | None = None) -> tuple[str, int, float]:
    """'Fl(3) 10s' → ('Fl', 3, 10.0). `period` overrides a period written in the string."""
    m = _CHAR.match(character)
    if not m:
        raise ValueError(f"unreadable light character {character!r}")
    kind, n, p = m.group(1), int(m.group(2) or 1), m.group(3)
    if period is None:
        if p is None:
            raise ValueError(f"light character {character!r} carries no period and none was given")
        period = float(p)
    return kind, n, float(period)


def flash_schedule(character: str, period: float | None = None) -> list[tuple[float, float]]:
    """Lit intervals [t0, t1) within one period, all on the 0.5 s grid."""
    kind, n, P = parse_character(character, period)
    if kind == "F":
        return [(0.0, P)]
    if kind == "Iso":
        return [(0.0, P / 2)]
    if kind in ("Q", "VQ"):
        if kind == "VQ":
            raise ValueError("VQ (2/s) cannot sit on the 0.5 s grid; use Q")
        return [(float(k), k + FLASH) for k in range(int(P))]
    if kind in ("Fl", "LFl"):
        fl = LONG_FLASH if kind == "LFl" else FLASH
        gap = fl + 1.0   # 1.0 s dark between flashes of a group
        lit = [(k * gap, k * gap + fl) for k in range(n)]
        if lit[-1][1] >= P:
            raise ValueError(f"{character!r}: {n} flashes do not fit in {P:g} s")
        return lit
    if kind == "Oc":
        ecl = 0.5
        first = P - (1.5 * n - 1.0)
        if first <= 0:
            raise ValueError(f"{character!r}: {n} eclipses do not fit in {P:g} s")
        lit, t = [], 0.0
        for k in range(n):
            e0 = first + 1.5 * k
            lit.append((t, e0))
            t = e0 + ecl
        if t < P:
            lit.append((t, P))
        return lit
    raise ValueError(f"unsupported light character {kind!r}")  # pragma: no cover


# ----------------------------------------------------------------------------- records
@dataclass
class Sail:
    """What `Timeline.sail()` returns. `anim` goes inside the boat's group, whose base transform
    is `transform`; `wrap()` assembles the whole group (translate > facing scale > pitch rotate)."""
    anim: str
    end: float
    tacks: list[float]
    facing: int
    start: tuple[int, int]
    stop: tuple[int, int]
    transform: str
    pitch: str
    headings: list[float] = field(default_factory=list)
    begin: float = 0.0
    dur: float = 0.0
    still: bool = False

    def wrap(self, inner: str, pitch: float = -4.0, mirror: bool = True, gid: str | None = None,
             facing_anim: str = "") -> str:
        f = (self.facing if mirror else 1)
        idattr = f' id="{gid}"' if gid else ""
        rot = 0.0 if self.still else pitch
        return (f'<g{idattr} transform="{self.transform}">{self.anim}'
                f'<g transform="scale({f} 1)">{facing_anim}'
                f'<g transform="rotate({_f(rot)})">{self.pitch}{inner}</g></g></g>')


@dataclass
class Tack:
    """`sails` is the wrapped sail group (luffs flat, refills mirrored); `hull` is the discrete
    scale animateTransform to drop inside the hull's facing group; `facing` the facing afterwards."""
    sails: str
    hull: str
    begin: float
    end: float
    flip_at: float
    facing: int


class Timeline:
    """One per sheet build. See the module docstring for the rules it enforces."""

    def __init__(self, sheet: str, motion: bool = True, period: float = PAGE_PERIOD,
                 quantum: float = QUANTUM, ambient: bool = False):
        self.sheet = sheet
        self.motion = bool(motion)
        self.period = float(period)
        self.quantum = float(quantum)
        self.ambient = bool(ambient)
        self._cues: dict[str, tuple[float, float]] = {}
        self._anims: list[dict] = []
        self._violations: list[str] = []
        self._snapped: list[tuple[str, float, float]] = []
        self._emitted: list[str] = []
        self._n = 0

    # ----------------------------------------------------------------- cues
    def cue(self, name: str, begin: float, dur: float) -> float:
        """Register a named window; returns its end. A cue named 'opening' fixes opening_end_s."""
        end = float(begin) + float(dur)
        self._cues[name] = (float(begin), end)
        return end

    def t(self, name: str) -> tuple[float, float]:
        return self._cues[name]

    def id(self, name: str) -> str:
        return f"{self.sheet}-{name}"

    # ----------------------------------------------------------------- grid
    def on_grid(self, t: float) -> bool:
        return abs(t - self.snap(t)) < GRID_TOL

    def snap(self, t: float) -> float:
        return round(round(t / self.quantum) * self.quantum, 6)

    def _snap_begin(self, begin: float, what: str) -> float:
        if self.on_grid(begin):
            return float(begin)
        s = self.snap(begin)
        self._snapped.append((what, float(begin), s))
        return s

    # ----------------------------------------------------------------- validation
    def _check_begin(self, begin) -> float:
        if isinstance(begin, str):
            raise ValueError(f"begin must be seconds, not {begin!r}: no syncbase in emitted SVG")
        b = float(begin)
        if b < 0:
            raise ValueError("begin < 0")
        return b

    def _check_period(self, dur: float, what: str) -> None:
        if not any(abs(dur - p) < 1e-9 for p in LOOP_PERIODS):
            raise ValueError(f"{what}: loop period {dur:g} s not in LOOP_PERIODS {LOOP_PERIODS}")

    def _record(self, **rec) -> None:
        rec.setdefault("name", None)
        self._anims.append(rec)

    def _out(self, s: str) -> str:
        if SYNCBASE.search(s):
            raise ValueError(f"syncbase in emitted SVG: {s[:80]}")
        self._emitted.append(s)
        return s

    @staticmethod
    def _changes(values: list[str], loop: bool) -> int:
        n = sum(1 for a, b in zip(values, values[1:]) if a != b)
        if loop and values and values[-1] != values[0]:
            n += 1
        return n

    # ----------------------------------------------------------------- core emitters
    def anim(self, attr: str, values, dur: float, begin: float, ease=None, freeze: bool = True,
             repeat=None, key_times=None, discrete: bool = False, still=None, name: str | None = None,
             additive: bool = False, kind: str | None = None, cls: str = "one-shot") -> str:
        """<animate> (or <animateTransform> when `kind` is a transform type). '' in still mode."""
        values = _vals(values)
        if len(values) < 2:
            raise ValueError("anim needs at least two values")
        begin = self._check_begin(begin)
        dur = float(dur)
        if dur <= 0:
            raise ValueError("dur must be > 0")
        loop = repeat == "indefinite"
        is_transform = kind is not None
        attr_name = "transform" if is_transform else attr
        if is_transform and kind not in TRANSFORM_KINDS:
            raise ValueError(f"unknown transform kind {kind!r}")
        geometry = attr_name in GEOMETRY_ATTRS
        if loop:
            if attr_name not in LOOP_ATTRS:
                raise ValueError(f"indefinite animation on {attr_name!r}: only opacity/transform may loop")
            if not discrete and not self.ambient:
                raise ValueError(f"continuous loop on {attr_name!r} needs ambient=True ({self.sheet})")
            self._check_period(dur, f"{attr_name} loop")
            if still is None:
                raise ValueError("loops must pass still= (the frozen edition's value)")
        if geometry:
            if loop or repeat not in (None, 1, "1"):
                raise ValueError(f"geometry attribute {attr_name!r} may not repeat")
            if dur > GEOMETRY_MAX_DUR or not freeze:
                self._violations.append(f"geometry attribute {attr_name!r} animated for {dur:g} s "
                                        f"(limit {GEOMETRY_MAX_DUR:g} s one-shot) at {begin:g} s")
        if ease is not None and discrete:
            raise ValueError("discrete animation takes no ease")
        # key times
        n = len(values)
        if key_times is None:
            kts = [i / (n - 1) for i in range(n)]
        else:
            kts = [float(k) for k in key_times]
            if len(kts) != n:
                raise ValueError("keyTimes and values differ in length")
            if any(b < a - 1e-9 for a, b in zip(kts, kts[1:])) or abs(kts[0]) > 1e-9:
                raise ValueError("keyTimes must start at 0 and be non-decreasing")
            if not discrete and abs(kts[-1] - 1) > 1e-9:
                raise ValueError("keyTimes must end at 1 for linear/spline animations")
        if discrete or loop:
            begin = self._snap_begin(begin, f"{attr_name} begin")
        if discrete:
            for k in kts:
                inst = begin + k * dur
                if not self.on_grid(inst):
                    raise ValueError(f"discrete instant {inst:.3f} s off the {self.quantum:g} s grid "
                                     f"({attr_name}, begin {begin:g}, keyTime {k:g})")
        end = math.inf if loop else begin + dur
        changes = self._changes(values, loop)
        self._record(attr=attr_name, kind=kind, begin=begin, dur=dur, end=end, loop=loop,
                     discrete=bool(discrete), continuous=not discrete, geometry=geometry,
                     changes=changes, key_times=kts, cls=("loop" if loop else cls), still=still,
                     name=name, values=values)
        if not self.motion:
            return ""
        # ease → keySplines
        parts = [f'attributeName="{attr_name}"']
        if is_transform:
            parts.append(f'type="{kind}"')
        if name:
            parts.insert(0, f'id="{self.id(name)}"')
        parts.append(f'begin="{_s(begin)}"')
        parts.append(f'dur="{_s(dur)}"')
        if loop:
            parts.append('repeatCount="indefinite"')
        elif repeat not in (None, 1, "1"):
            parts.append(f'repeatCount="{repeat}"')
        elif freeze:
            parts.append('fill="freeze"')
        if discrete:
            parts.append('calcMode="discrete"')
        elif ease is not None:
            eases = ease if isinstance(ease, (list, tuple)) else [ease] * (n - 1)
            if len(eases) != n - 1:
                raise ValueError("one ease per segment")
            if all(e in (None, "linear") for e in eases):
                parts.append('calcMode="linear"')
            else:
                parts.append('calcMode="spline"')
                parts.append('keySplines="' + ";".join(EASE.get(e or "linear", e or EASE["linear"])
                                                       for e in eases) + '"')
        else:
            parts.append('calcMode="linear"')
        if additive:
            parts.append('additive="sum"')
        parts.append('values="' + ";".join(values) + '"')
        if key_times is not None or discrete:
            nd = 6 if (discrete or loop) else 4
            parts.append('keyTimes="' + ";".join(_f(k, nd) for k in kts) + '"')
        tag = "animateTransform" if is_transform else "animate"
        return self._out(f"<{tag} {' '.join(parts)}/>")

    def xform(self, kind: str, values, dur: float, begin: float, ease=None, freeze: bool = True,
              repeat=None, key_times=None, discrete: bool = False, still=None, name: str | None = None,
              additive: bool = False, cls: str = "one-shot") -> str:
        """<animateTransform type=kind>. Same rules as anim()."""
        return self.anim("transform", values, dur, begin, ease=ease, freeze=freeze, repeat=repeat,
                         key_times=key_times, discrete=discrete, still=still, name=name,
                         additive=additive, kind=kind, cls=cls)

    def set(self, attr: str, to, begin: float, name: str | None = None, exempt: bool = False) -> str:
        """<set> (a discrete freeze-in). Begin on the grid unless `exempt` (typing bursts)."""
        begin = self._check_begin(begin)
        if not exempt:
            begin = self._snap_begin(begin, f"set {attr}")
        self._record(attr=attr, kind=None, begin=begin, dur=0.0, end=begin, loop=False, discrete=True,
                     continuous=False, geometry=attr in GEOMETRY_ATTRS, changes=1,
                     cls=("typed" if exempt else "set"), still=to, name=name, values=[str(to)])
        if attr in GEOMETRY_ATTRS:
            raise ValueError(f"set on geometry attribute {attr!r}")
        if not self.motion:
            return ""
        idattr = f' id="{self.id(name)}"' if name else ""
        return self._out(f'<set{idattr} attributeName="{attr}" to="{to}" begin="{_s(begin)}"/>')

    def prop(self, attr: str, values, dur: float, begin: float, still=None, **kw) -> tuple[str, str]:
        """(base attribute string, animate string): base = first value in motion, still/end value
        in the still edition. `opacity, a = tl.prop("opacity", [0, 1], 0.4, 2.2)`."""
        vals = _vals(values)
        a = self.anim(attr, vals, dur, begin, still=still, **kw)
        base = vals[0] if self.motion else self.still_value(vals, still)
        return f'{attr}="{base}"', a

    @staticmethod
    def still_value(values, still=None) -> str:
        """The frozen edition's value: `still` when given, else the last value (freeze)."""
        vals = _vals(values)
        if still is None:
            return vals[-1]
        return _vals([still])[0]

    # ----------------------------------------------------------------- compound helpers
    def fade_in(self, inner: str, begin: float, dur: float = 0.25, rise: float = 3, ease: str = "settle",
                name: str | None = None) -> str:
        """Fade (and lift) `inner` in once, then stay. Base opacity="0". Still: `inner` unwrapped."""
        if not self.motion:
            self._record(attr="opacity", kind=None, begin=float(begin), dur=float(dur), end=float(begin) + float(dur),
                         loop=False, discrete=False, continuous=True, geometry=False, changes=0,
                         cls="fade", still=1, name=name, values=["0", "1"])
            return inner
        a = self.anim("opacity", [0, 1], dur, begin, ease=ease, cls="fade", name=name)
        if rise:
            a += self.xform("translate", [f"0 {_f(rise)}", "0 0"], dur, begin, ease=ease, cls="fade")
        return f'<g opacity="0">{a}{inner}</g>'

    def draw_in(self, path_attrs: str, dur: float = 1.6, begin: float = 0.0, ease: str = "draw",
                name: str | None = None) -> str:
        """A <path> that traces itself in (pathLength=1, dashoffset 1→0). Still: a plain path.
        The only sanctioned geometry animation: a finite one-shot <= 4 s (contour tracing)."""
        if not self.motion:
            return f"<path {path_attrs}/>"
        a = self.anim("stroke-dashoffset", [1, 0], dur, begin, ease=ease, cls="draw", name=name)
        return (f'<path {path_attrs} pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
                f'{a}</path>')

    def reveal(self, inner: str, begin: float, name: str | None = None) -> str:
        """Base opacity=0 + one discrete <set> to 1 at `begin` (grid). Still: the bare element."""
        if not self.motion:
            self.set("opacity", 1, begin, name=name)
            return inner
        s = self.set("opacity", 1, begin, name=name)
        return _inject(inner, 'opacity="0"', s)

    # ----------------------------------------------------------------- typing
    def typed(self, s: str, x: float, y: float, role: str, begin: float, seed: int,
              pace: tuple[float, float] = (0.036, 0.06), space: float = 0.16, glyphs=None,
              dash: float = 0.22) -> tuple[str, float, list[float]]:
        """Type `s` glyph by glyph from `begin` (returned inside `<g class="typed">`). `glyphs` is a callable
        `glyph_cb(s, x, y, role) -> list[(svg_fragment, x_advance)]` (one entry per character, ''
        fragment for a space) or that list prebuilt; typeset is never imported here. Times come
        from an LCG seeded on `seed` (a row index). Returns (svg, end, per-glyph times)."""
        if glyphs is None:
            raise ValueError("typed() needs glyphs: a callable or a per-character [(fragment, advance)] list")
        items = list(glyphs(s, x, y, role) if callable(glyphs) else glyphs)
        if len(items) != len(s):
            raise ValueError(f"typed(): {len(items)} glyph entries for {len(s)} characters")
        begin = self._check_begin(begin)
        rng = _LCG(seed)
        t = begin
        out, times = [], []
        for i, ch in enumerate(s):
            if i > 0 and s[i - 1] == " ":
                t += space
            if ch == "-" and s[i:i + 2] == "--" and (i == 0 or s[i - 1] != "-"):
                t += dash
            frag = items[i][0] if isinstance(items[i], (tuple, list)) else items[i]
            tt = round(t, 3)
            times.append(tt)
            if frag:
                if self.motion:
                    out.append(_inject(frag, 'opacity="0"', self.set("opacity", 1, tt, exempt=True)))
                else:
                    out.append(frag)
            t += pace[0] + rng.uniform() * (pace[1] - pace[0])
        end = round(t, 3)
        self._record(attr="opacity", kind=None, begin=begin, dur=end - begin, end=end, loop=False,
                     discrete=True, continuous=False, geometry=False, changes=len(times),
                     cls="typed-burst", still=1, name=None, values=[])
        # class="typed" marks the burst for checks/motion.py (its instants are off-grid by nature)
        return f'<g class="typed">{"".join(out)}</g>', end, times

    def cursor(self, times: list[float], xs: list[float], y: float, w: float = 8, h: float = 15,
               blink_begin: float | None = None, fill: str = "currentColor", end_x: float | None = None,
               name: str | None = None) -> str:
        """A typing cursor: a rect riding a discrete translate through `xs` at `times` (the typing
        burst, exempt from the grid like the glyphs), then an optional 1 s discrete blink loop from
        `blink_begin` (grid). Still: the cursor parked at its last x, lit."""
        if len(xs) != len(times):
            raise ValueError("cursor(): xs and times differ in length")
        last_x = end_x if end_x is not None else xs[-1]
        if not self.motion:
            return f'<rect x="0" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" fill="{fill}" transform="translate({_f(last_x)} 0)"/>'
        pts = list(zip(times, xs))
        if end_x is not None:
            pts.append((times[-1] + 0.001, end_x))
        t0, t1 = pts[0][0], pts[-1][0]
        dur = max(t1 - t0, 0.001)
        vals = [f"{_f(px)} 0" for _, px in pts]
        kts = [(tt - t0) / dur for tt, _ in pts]
        # typed instants are exempt from the grid: emit directly (recorded as a typed burst)
        self._record(attr="transform", kind="translate", begin=t0, dur=dur, end=t1, loop=False, discrete=True,
                     continuous=False, geometry=False, changes=len(pts) - 1, cls="typed-burst", still=None,
                     name=name, values=vals)
        ride = self._out(f'<animateTransform attributeName="transform" type="translate" begin="{_s(t0)}" '
                         f'dur="{_s(dur)}" fill="freeze" calcMode="discrete" values="{";".join(vals)}" '
                         f'keyTimes="{";".join(_f(k, 4) for k in kts)}"/>')
        blink = ""
        if blink_begin is not None:
            blink = self.anim("opacity", [1, 0], 1.0, blink_begin, repeat="indefinite", key_times=[0, 0.5],
                              discrete=True, still=1, cls="loop", name=(name + "-blink") if name else None)
        return (f'<rect class="typed" x="0" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" fill="{fill}" '
                f'transform="translate({_f(xs[0])} 0)">{ride}{blink}</rect>')

    # ----------------------------------------------------------------- lights
    def flash(self, character: str, period: float | None = None, begin: float = 0.0, still: str = "lit",
              lit=1, dark=0, name: str | None = None) -> str:
        """The one light-character parser. 'Fl', 'Fl(3)', 'Oc', 'Oc(2)', 'Iso', 'Q', 'LFl', 'F', with an
        optional colour letter and period ('Fl(3) 10s'). Discrete opacity loop on the 0.5 s grid,
        period validated against tokens.LOOP_PERIODS. The host element's base opacity is its lit
        value (every light lit at t=0). Still: '' (the base attribute shows the light lit)."""
        kind, n, P = parse_character(character, period)
        self._check_period(P, f"light {character!r}")
        lit_iv = flash_schedule(character, P)
        if kind == "F":
            return ""   # a fixed light: nothing to animate
        # boundaries → values/keyTimes, state at t=0 first
        vals, kts = [], []
        state = lit if lit_iv and lit_iv[0][0] == 0 else dark
        vals.append(_f(state))
        kts.append(0.0)
        bounds = sorted({b for iv in lit_iv for b in iv if 0 < b < P})
        for b in bounds:
            in_lit = any(a <= b < c for a, c in lit_iv)
            v = lit if in_lit else dark
            if _f(v) != vals[-1]:
                vals.append(_f(v))
                kts.append(b / P)
        if len(vals) < 2:
            return ""
        still_v = lit if still == "lit" else dark
        return self.anim("opacity", vals, P, begin, repeat="indefinite", key_times=kts, discrete=True,
                         still=still_v, cls="loop", name=name)

    # ----------------------------------------------------------------- boats
    def sail(self, path_d: str, begin: float, dur: float, n: int = 64, ease: str = "settle",
             mast_x: float = 3.0, pitch: float = -4.0, pitch_settle: float = 0.0, name: str | None = None) -> Sail:
        """One passage along `path_d`: animateTransform translate with `n` arc-length samples and
        ease-warped keyTimes (calcMode linear reproduces the ease), fill=freeze. Never animateMotion,
        never rotate=auto: the boat faces by mirror (`facing`), is trimmed `pitch`° bow-up under
        way and levels (discrete at `end`, or a `pitch_settle` s settle) when she anchors.
        `tacks` lists the x-reversal instants (snapped) for `tack()`."""
        begin = self._check_begin(begin)
        dur = float(dur)
        if dur <= 0 or n < 2:
            raise ValueError("sail needs dur > 0 and n >= 2")
        samples = sample_path(path_d, n)
        pts = [(int(round(x)), int(round(y))) for x, y, _ in samples]
        headings = [h for _, _, h in samples]
        kts = [ease_inverse(ease, i / (n - 1)) for i in range(n)]
        kts[0], kts[-1] = 0.0, 1.0
        for i in range(1, n):          # monotone after rounding
            kts[i] = max(kts[i], kts[i - 1])
        # facing and tacks from x-direction of travel
        facing = 1
        for (x0, _), (x1, _) in zip(pts, pts[1:]):
            if abs(x1 - x0) >= 1:
                facing = 1 if x1 > x0 else -1
                break
        tacks: list[float] = []
        sign = facing
        for i in range(1, n):
            dx = pts[i][0] - pts[i - 1][0]
            if abs(dx) < 1:
                continue
            s = 1 if dx > 0 else -1
            if s != sign:
                sign = s
                tacks.append(self.snap(begin + kts[i - 1] * dur - 0.5))   # hull flips 0.5 s into a 1.2 s tack
        end = begin + dur
        if not self.motion:
            return Sail(anim="", end=end, tacks=tacks, facing=facing * (1 if len(tacks) % 2 == 0 else -1),
                        start=pts[0], stop=pts[-1], transform=f"translate({pts[-1][0]} {pts[-1][1]})",
                        pitch="", headings=headings, begin=begin, dur=dur, still=True)
        values = [f"{x} {y}" for x, y in pts]
        self._record(attr="transform", kind="translate", begin=begin, dur=dur, end=end, loop=False, discrete=False,
                     continuous=True, geometry=False, changes=n - 1, cls="sail", still=values[-1], name=name,
                     values=values)
        idattr = f' id="{self.id(name)}"' if name else ""
        anim = self._out(f'<animateTransform{idattr} attributeName="transform" type="translate" begin="{_s(begin)}" '
                         f'dur="{_s(dur)}" fill="freeze" calcMode="linear" values="{";".join(values)}" '
                         f'keyTimes="{";".join(_f(k, 4) for k in kts)}"/>')
        if pitch_settle and pitch_settle > 0:
            p = self.xform("rotate", [pitch, 0], pitch_settle, end, ease="settle", cls="sail")
        else:
            p = self.xform("rotate", [pitch, 0], self.quantum, end,
                           discrete=True, key_times=[0, 0], cls="sail") if pitch else ""
        return Sail(anim=anim, end=end, tacks=tacks, facing=facing, start=pts[0], stop=pts[-1],
                    transform=f"translate({pts[0][0]} {pts[0][1]})", pitch=p, headings=headings,
                    begin=begin, dur=dur)

    def tack(self, begin: float, mast_x: float, sails: str, facing: int = 1, dur: float = 1.2,
             name: str | None = None) -> Tack:
        """Going about (31): the sail group scales 1 → 0.06 → −1 about the mast over `dur` s
        (draw in, settle out); the hull mirrors in one discrete step at `begin`+0.5 s while the
        sails are flat. Still: sails already on the new side, hull anim ''."""
        begin = self._snap_begin(self._check_begin(begin), "tack begin")
        flip = begin + 0.5
        end = begin + dur
        mx = _f(mast_x)
        if not self.motion:
            return Tack(sails=f'<g transform="translate({mx} 0) scale(-1 1) translate(-{mx} 0)">{sails}</g>',
                        hull="", begin=begin, end=end, flip_at=flip, facing=-facing)
        k_flat = round(0.5 / dur, 4)
        luff = self.xform("scale", ["1 1", "0.06 1", "-1 1"], dur, begin, ease=["draw", "settle"],
                          key_times=[0, k_flat, 1], cls="tack", name=name)
        hull = self.xform("scale", [f"{facing} 1", f"{-facing} 1"], self.quantum, flip, discrete=True,
                          key_times=[0, 0], cls="tack")
        wrapped = f'<g transform="translate({mx} 0)"><g>{luff}<g transform="translate(-{mx} 0)">{sails}</g></g></g>'
        return Tack(sails=wrapped, hull=hull, begin=begin, end=end, flip_at=flip, facing=-facing)

    def fixes(self, points, begin: float, every: float = 4.0, labels=None, hold: float | None = None,
              boat: str | None = None, ink: str = "currentColor", mark: str | None = None,
              fade: float | None = None, name: str | None = None) -> str:
        """Dead-reckoning fixes: the boat steps (discrete translate) to each point every `every` s
        and leaves a ⊙ mark (plus the optional label fragment, positioned relative to the fix).
        `hold=None`: a finite one-shot that freezes at the last fix. `hold=72` with 7 fixes at 4 s:
        a 96 s loop (period validated) for the boat alone, with a 0.5 s dark gap at the wrap; the
        marks are plotted once and stay. ~0.1 repaints/s, two indefinite animations.
        Still: the boat at the last fix, every mark visible."""
        pts = [(int(round(x)), int(round(y))) for x, y in points]
        if len(pts) < 2:
            raise ValueError("fixes needs at least two points")
        begin = self._snap_begin(self._check_begin(begin), "fixes begin")
        if not self.on_grid(every):
            raise ValueError(f"fixes: every={every} is off the grid")
        n = len(pts)
        run = (n - 1) * every
        labels = list(labels) if labels else [""] * n
        if len(labels) != n:
            raise ValueError("fixes: one label per point")
        mark = mark if mark is not None else (f'<circle r="3" fill="none" stroke="{ink}" stroke-width="1"/>'
                                               f'<circle r="0.9" fill="{ink}" stroke="none"/>')
        loop = hold is not None
        fade = self.quantum if fade is None else fade
        out = []
        if loop:
            P = run + float(hold)
            self._check_period(P, "fixes loop")
            # boat: discrete translate through the fixes, then hold; vanishes `fade` s before the wrap
            kts = [i * every / P for i in range(n)]
            vals = [f"{x} {y}" for x, y in pts]
            boat_anim = self.xform("translate", vals, P, begin, repeat="indefinite", key_times=kts, discrete=True,
                                   still=vals[-1], cls="loop", name=name)
            boat_anim += self.anim("opacity", [1, 0], P, begin, repeat="indefinite", key_times=[0, (P - fade) / P],
                                   discrete=True, still=1, cls="loop")
            if self.motion and boat:
                out.append(f'<g transform="translate({pts[0][0]} {pts[0][1]})" opacity="1">{boat_anim}{boat}</g>')
            # the marks are plotted once and stay (a navigator does not erase the fixes): finite
            # reveals, so the loop costs two indefinite animations however many fixes there are
            for i, (x, y) in enumerate(pts):
                inner = f'<g transform="translate({x} {y})">{mark}{labels[i]}</g>'
                out.append(inner if i == 0 else self.reveal(inner, begin + i * every))
        else:
            kts = [i / (n - 1) for i in range(n)]
            vals = [f"{x} {y}" for x, y in pts]
            boat_anim = self.xform("translate", vals, run, begin, key_times=kts, discrete=True, cls="fixes", name=name)
            if self.motion and boat:
                out.append(f'<g transform="translate({pts[0][0]} {pts[0][1]})">{boat_anim}{boat}</g>')
            for i, (x, y) in enumerate(pts):
                inner = f"{mark}{labels[i]}"
                if i == 0:
                    out.append(f'<g transform="translate({x} {y})">{inner}</g>')
                else:
                    out.append(self.reveal(f'<g transform="translate({x} {y})">{inner}</g>', begin + i * every))
        if not self.motion and boat:
            out.insert(0, f'<g transform="translate({pts[-1][0]} {pts[-1][1]})">{boat}</g>')
        return "".join(out)

    # ----------------------------------------------------------------- long-period loops
    def every(self, kind_or_attr: str, segments, begin: float, period: float = PAGE_PERIOD,
              discrete: bool = False, additive: bool = False, still=None, name: str | None = None) -> str:
        """One element, one period, no chains: `segments` = [(t_rel, value[, ease_to_next]), …]; the
        last value holds to `period`. Transform kinds emit animateTransform (additive="sum" when
        `additive`). Continuous segments need ambient=True; discrete ones sit on the grid.
        The only indefinite emitter besides flash()."""
        period = float(period)
        self._check_period(period, "every")
        segs = []
        for seg in segments:
            if len(seg) == 2:
                t, v = seg
                e = None
            else:
                t, v, e = seg
            segs.append((float(t), v, e))
        if not segs or segs[0][0] != 0:
            raise ValueError("every(): segments must start at t=0")
        if any(b[0] < a[0] for a, b in zip(segs, segs[1:])) or segs[-1][0] > period:
            raise ValueError("every(): segment times must be non-decreasing and within the period")
        if segs[-1][0] < period:
            segs.append((period, segs[-1][1], None))
        values = _vals([v for _, v, _ in segs])
        kts = [t / period for t, _, _ in segs]
        if still is None:
            raise ValueError("every(): pass still= (the frozen edition's value)")
        if kind_or_attr in TRANSFORM_KINDS:
            kind, attr = kind_or_attr, "transform"
        else:
            kind, attr = None, kind_or_attr
        if discrete:
            return self.anim(attr, values, period, begin, repeat="indefinite", key_times=kts, discrete=True,
                             still=still, kind=kind, name=name, additive=additive, cls="loop")
        eases = []
        for (_, va, e), (_, vb, _) in zip(segs, segs[1:]):
            eases.append("linear" if (e is None or _vals([va]) == _vals([vb])) else e)
        return self.anim(attr, values, period, begin, ease=eases, repeat="indefinite", key_times=kts,
                         still=still, kind=kind, name=name, additive=additive, cls="loop")

    # ----------------------------------------------------------------- report
    def opening_end(self) -> float:
        """End of the opening: the 'opening' cue when registered, else the end of the chain of
        one-shots (not sails, not loops) that starts at t=0 with gaps <= quantum."""
        if "opening" in self._cues:
            return self._cues["opening"][1]
        shots = sorted((a["begin"], a["end"]) for a in self._anims
                       if not a["loop"] and a["cls"] not in ("sail", "typed-burst", "loop") and a["end"] != math.inf)
        if not shots or shots[0][0] > self.quantum:
            return 0.0
        end = 0.0
        for b, e in shots:
            if b > end + self.quantum:
                break
            end = max(end, e)
        return round(end, 3)

    def continuous_windows(self) -> list[list[float]]:
        iv = sorted((a["begin"], a["end"]) for a in self._anims if a["continuous"] and not a["loop"])
        out: list[list[float]] = []
        for b, e in iv:
            if out and b <= out[-1][1] + 1e-9:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([b, e])
        return [[round(b, 3), round(e, 3)] for b, e in out]

    def repaints_per_s(self) -> float | str:
        """Distinct discrete change instants per second over one page period, counting every loop
        (shared instants count once, as Chromium paints them). 'continuous' when an ambient loop runs."""
        loops = [a for a in self._anims if a["loop"]]
        if any(a["continuous"] for a in loops):
            return "continuous"
        instants: set[float] = set()
        P = self.period
        for a in loops:
            vals, kts, d, b = a["values"], a["key_times"], a["dur"], a["begin"]
            k = 0
            while k * d < P + d:
                for v0, v1, kt in zip(vals, vals[1:], kts[1:]):
                    if v0 != v1:
                        instants.add(round((b + k * d + kt * d) % P, 3))
                if vals[-1] != vals[0]:
                    instants.add(round((b + (k + 1) * d) % P, 3))
                k += 1
        return round(len(instants) / P, 3)

    def report(self) -> dict:
        loops = [a for a in self._anims if a["loop"]]
        indefinite = len(loops)
        if not self.motion:
            cls = "still"
        elif self.ambient or any(a["continuous"] for a in loops):
            cls = "ambient"
        elif loops:
            cls = "lights"
        else:
            cls = "frozen"
        geometry = [a for a in self._anims if a["geometry"]]
        violations = list(self._violations)
        for s in self._emitted:
            if "animateMotion" in s:
                violations.append("animateMotion emitted")
        return {
            "sheet": self.sheet,
            "class": cls,
            "motion": self.motion,
            "ambient": self.ambient,
            "indefinite": indefinite,
            "repaints_per_s": self.repaints_per_s(),
            "opening_end_s": self.opening_end(),
            "longest_loop_s": max((a["dur"] for a in loops), default=0.0),
            "loops": [{"attr": a["attr"], "kind": a["kind"], "period": a["dur"], "begin": a["begin"],
                       "changes": a["changes"], "discrete": a["discrete"], "still": a["still"], "name": a["name"]}
                      for a in loops],
            "continuous_windows": self.continuous_windows(),
            "geometry_anims": len(geometry),
            "snapped": [{"what": w, "from": f, "to": t} for w, f, t in self._snapped],
            "cues": {k: list(v) for k, v in self._cues.items()},
            "anims": len(self._anims),
            "violations": violations,
        }


class NullTimeline(Timeline):
    """A Timeline that never animates: the still edition's engine (`motion=False`)."""

    def __init__(self, sheet: str = "still", period: float = PAGE_PERIOD, quantum: float = QUANTUM,
                 ambient: bool = False, **_):
        super().__init__(sheet, motion=False, period=period, quantum=quantum, ambient=ambient)


# ----------------------------------------------------------------------------- utilities
class _LCG:
    """Deterministic 31-bit LCG (typing cadence; seeded on the row index)."""

    def __init__(self, seed: int):
        self.state = (int(seed) * 2654435761 + 12345) & 0x7FFFFFFF

    def uniform(self) -> float:
        self.state = (self.state * 1103515245 + 12345) & 0x7FFFFFFF
        return self.state / 0x80000000


_OPEN = re.compile(r"^\s*<([A-Za-z][\w:-]*)((?:\s+[^<>]*?)?)\s*(/?)>", re.S)


def _single_element(markup: str) -> tuple[str, str, bool, str, str] | None:
    """If `markup` is exactly one element, return (tag, attrs, selfclosing, content, trailing)."""
    m = _OPEN.match(markup)
    if not m:
        return None
    tag, attrs, selfclose = m.group(1), m.group(2), m.group(3) == "/"
    rest = markup[m.end():]
    if selfclose:
        return (tag, attrs, True, "", rest) if rest.strip() == "" else None
    # scan for the matching close tag at depth 0
    depth = 1
    i = 0
    pat = re.compile(r"<(/?)([A-Za-z][\w:-]*)[^<>]*?(/?)>", re.S)
    for mm in pat.finditer(rest):
        if mm.group(1) == "/":
            depth -= 1
            if depth == 0:
                content = rest[:mm.start()]
                trailing = rest[mm.end():]
                if trailing.strip() != "" or mm.group(2) != tag:
                    return None
                return tag, attrs, False, content, ""
        elif mm.group(3) != "/":
            depth += 1
        i = mm.end()
    return None


def _inject(inner: str, attr: str, child: str) -> str:
    """Put `attr` on `inner`'s own tag and `child` inside it when `inner` is one element
    (opacity on the leaf, not a wrapper: each group opacity is a saveLayer). Otherwise wrap in <g>."""
    se = _single_element(inner)
    if se is None:
        return f"<g {attr}>{child}{inner}</g>"
    tag, attrs, selfclose, content, _ = se
    attrs = attrs.rstrip()
    attr_name = attr.split("=", 1)[0]
    if re.search(rf'\s{re.escape(attr_name)}="', " " + attrs):
        attrs = re.sub(rf'\s{re.escape(attr_name)}="[^"]*"', " " + attr, " " + attrs).strip()
        head = f"<{tag} {attrs}"
    else:
        head = f"<{tag}{attrs} {attr}" if attrs else f"<{tag} {attr}"
    if selfclose:
        return f"{head}>{child}</{tag}>"
    return f"{head}>{child}{content}</{tag}>"


__all__ = [
    "Timeline", "NullTimeline", "Sail", "Tack", "sample_path", "path_length", "flash_schedule",
    "parse_character", "ease_at", "ease_inverse", "ease_curve", "EASE", "LOOP_PERIODS", "QUANTUM",
    "PAGE_PERIOD", "GEOMETRY_ATTRS", "LOOP_ATTRS", "SYNCBASE", "GRID_TOL",
]
