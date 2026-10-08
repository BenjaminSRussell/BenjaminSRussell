"""approaches — Sheet 3, "Approaches to Scrapy Harbor" (T3; MASTERPLAN decisions 1, 5, 14, 20, 21).

The harbour chart of the two systems. Harbour to the WEST: two headlands frame a mouth opening ESE,
the WAL is a block mole with a head light shielding the entrance, quays on the basin's shores are
named for the Delta tables and the workers. A Region B channel on a final leading-line leg of 290°
true (the hero's bearing). rustmapper's survey ground to the EAST (one track line per frontier
shard), the limit of survey and the unsurveyed hatch at the east edge. The rustmapper → Scrapy
link is charted as a *proposed, unlit* channel (pecked, hollow marks): nothing runs it. Zones of
Confidence, two notes blocks and THE LEGEND (every symbol id in chartlib.symbol_defs that is a
charted symbol), both at 17 px so they survive the README column.

Honesty: every figure on the water is illustrative (italic, sloping). Upright figures are only the
chart number, the PyPI version, date and wheel, Scrapy's commit count and the legend example drawn
from stats.json. "512" is never printed. Shards = log.json.profile.shards, italic until `measured`.
No coverage figure.

Motion (§2.1, all discrete): G "1" Fl G 4s (begin 0), R "2" Fl R 4s (begin 2), the entrance gate
G "3" Fl(2) G 10s / R "4" Fl(2) R 10s, Grafana Lt Fl {scrape_interval}s, the packet boat plotted
by 7 fixes at 0, 4 … 24 s then held to 96 s; the survey vessel plots 8 fixes on the last track line
at 28, 30 … 42 s and sounding k and mole block k <set> at fix k. Still edition = the finished sheet.
Phone edition: the geography rotated 90° anticlockwise (channel down the screen, north arrow
pointing left), re-lettered at SCALE_PHONE, frozen, with a compact legend of its own symbols below.
"""
from __future__ import annotations

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.dirname(_HERE)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

import chartlib as c  # noqa: E402
import edition as E  # noqa: E402
import timeline as T  # noqa: E402
import tokens  # noqa: E402
import typeset as k  # noqa: E402
from chartlib.field import smoothstep  # noqa: E402

NAME = "approaches"
KIND = "chart"
SIZES = {"desk": (1280, 960), "phone": (720, 1880)}
BREAKS: list[tuple[str, str, str]] = [
    ("Panel headers are set in role `label` with caps and +0.6 tracking, not `label-caps`",
     "the one `label-caps` run per sheet is the unit line outside the neat line; NOTES / ZONES OF CONFIDENCE / "
     "SYMBOLS headers are structural captions inside cartouches",
     "T5's rule guards the sheet caption; a chart's notes panels are headed in small tracked caps (NOAA 1980–2000)"),
    ("Legend definitions and the notes bodies are `label` at size 17 (on SCALE), not 13",
     "47 lines at 13 px rendered at 8.8 px in the README column; 17 renders at 11.6",
     "round-3 crit from the type, accessibility and cartography critics; the floor is for chart labels, not a key"),
    ("The channel centreline from W1 inward is the leading line, not a pecked course",
     "COURSE dots run W0→W1 only; from W1 to the anchorage the solid Ldg line carries the waypoints",
     "the four inner legs are collinear on 290° by decision 1, and two line styles on one line would be noise"),
    ("No inset: the harbour works are charted at chart scale",
     "quays named for the Delta tables and workers on the basin's shores, the WAL as a block mole with a head light",
     "round-2 crit: an inset over the 10-contour was the loudest thing on the sheet; a chart puts the works where they are"),
    ("Phone edition is rotated 90° anticlockwise, 720 × 1880, with neat-line rules at 50/55 and its own legend",
     "point mapper P(x, y) → (55 + (y−20)·1.2, 180 + (1150−x)·1.2); the unsurveyed band is cropped to 54 px of desk; "
     "the head and foot marginalia sit 24 px inside the sheet edge",
     "a phone sheet reads the channel down the screen (T3 §6); the README caption promises a legend on every width"),
]

PREFIX = "c"          # symbol ids c-sym-<name>; edition.svg prefixes approaches-
SEED = 27

# ------------------------------------------------------------------ geography (1280 × 960 desk space)
W_DESK, H_DESK = SIZES["desk"]
RULES = {"desk": (14, 19), "phone": (50, 55)}
MAP_TOP, MAP_BOTTOM = 20, 520                 # the charted water; the strip (notes + legend) takes the rest
_K = (MAP_BOTTOM - MAP_TOP) / 680.0           # the T3 geography (680 tall) compressed into 500


def _y(v: float) -> int:
    """A T3 y coordinate (20 … 700) in the compressed map."""
    return E.I(MAP_TOP + (v - MAP_TOP) * _K)


BASE = 26.0                                   # open water where nothing is sampled (never on a level)
H_SND = 110.0                                 # sounding kernel support: samples ~95 px apart must overlap
LEVELS = (0.0, 5.0, 10.0, 20.0, 50.0)
INDEX_LEVELS = (10.0, 50.0)
ANCH = (172, _y(446))
LDG_BRG = 290.0                               # true, the hero's final leg (decision 1)
_DIR = (math.sin(math.radians(LDG_BRG - 180)), -math.cos(math.radians(LDG_BRG - 180)))   # seaward unit (110°)


def _along(d: float) -> tuple[int, int]:
    return (E.I(ANCH[0] + _DIR[0] * d), E.I(ANCH[1] + _DIR[1] * d))


W4, W3, W2, W1 = _along(90), _along(185), _along(270), _along(380)
W0 = (608, _y(672))
COURSE = [W0, W1, W2, W3, W4, ANCH]
LDG_FRONT, LDG_REAR = _along(-52), _along(-100)
GRAFANA = (178, _y(200))
SHOAL = (478, _y(648))
SHOAL_R = 24
WRECK = (560, _y(400))
SURVEY = (680, 124, 400, 386)                 # the survey ground (below the ZOC panel)
RESTRICTED = [(900, _y(300)), (1060, _y(300)), (1060, _y(420)), (900, _y(420))]
LIMIT_X = 1096
BAND = (LIMIT_X, MAP_TOP, 1260 - LIMIT_X, MAP_BOTTOM - MAP_TOP)
UNSURVEYED_FADE = (1080, 1150)
ZONE_Y = {"A": _y(215), "B": _y(405), "C": _y(595)}
REP, ED_, SD = (760, 150), (980, _y(480)), (842, 417)   # SD sits on a lattice node of line 7
# the WAL mole: from the north headland root toward the mouth, a light at its head
MOLE_A, MOLE_B = (238, ANCH[1] - 34), (366, ANCH[1] - 10)

# the strip: two notes blocks over a full-width legend
STRIP_Y = 524
BLOCK_RM = (36, STRIP_Y, 600, 188)
BLOCK_SH = (644, STRIP_Y, 600, 188)
LEGEND = (36, 718, 1208, 218)
TITLE_C = (470, 50)
ZOC = (680, 26, 400, 86)
PANEL_SIZE = 17                               # legend definitions and notes bodies (on SCALE)

LAND = [(60, _y(130), 230, 70), (40, _y(330), 220, 70), (50, _y(560), 230, 70), (50, _y(720), 230, 70),
        (170, _y(200), 80, 42), (40, _y(60), 120, 45), (40, _y(760), 130, 45),
        (140, ANCH[1] + 2, 170, 50),                                 # the harbour's own land
        (236, ANCH[1] - 38, 46, 58), (228, ANCH[1] + 60, 46, 58)]    # the two headlands either side of the mouth
CARVE = [(ANCH[0], ANCH[1], 52, -100), (ANCH[0] + 60, ANCH[1] + 20, 34, -62)]
ACRONYMS = {"CT LOGS": "CT logs", "SITEMAPS": "sitemaps", "COMMON CRAWL": "Common Crawl"}
ZONE_TEXT = {"A": "existence doubtful", "B": "exists, may not answer", "C": "as reported"}

# phone mapper: rotate 90° anticlockwise, east to the top, north to the left; crop the band
PH_S = 1.2
PH_X0, PH_Y0, PH_CROP = 55, 180, 1150
PH_LEGEND_Y = 1556


# ------------------------------------------------------------------ coast with per-side insets
class _Coast(c.Coast):
    """Coast falloff with a different inset per side and a fade along either axis (the unsurveyed
    margin): the west coast closes under the 14 px margin, not 24 px inside the neat line."""

    def __init__(self, rect, insets, fade):
        self.rect = rect
        self.insets = insets            # {"l","r","t","b"}
        self.fade = fade                # (axis, a, b): factor 1 at a, 0 at b
        self.unsurveyed_x = None
        self.inset = 24.0

    def factor(self, x: float, y: float) -> float:
        x0, y0, w, h = self.rect
        f = 1.0
        for d, key in ((x - x0, "l"), (x0 + w - x, "r"), (y - y0, "t"), (y0 + h - y, "b")):
            if d <= 0:
                return 0.0
            ins = self.insets[key]
            if d < ins:
                f *= smoothstep(d / ins)
        if self.fade:
            axis, a, b = self.fade
            v = x if axis == "x" else y
            t = (v - a) / (b - a)
            if t >= 1:
                return 0.0
            if t > 0:
                f *= 1.0 - smoothstep(t)
        return f


# ------------------------------------------------------------------ illustrative bathymetry
def _shore_distance(x: float, y: float) -> float:
    """Approximate distance to the shore: the land kernels' shore radius is ~0.55 h."""
    best = math.inf
    for kx, ky, kh, amp in LAND:
        if amp <= 0:
            continue
        best = min(best, math.hypot(x - kx, y - ky) - 0.55 * kh)
    return max(0.0, best)


def _depth_design(x: float, y: float) -> float:
    """The designed depth (URLs, thousands) the illustrative soundings are sampled from: a steep shelf
    (one thin tint ribbon each under 5 and under 10), then a slope seaward to the 50 line inside the
    survey ground, a deeper fairway along the course, a shallower bank north of the channel, and a gentle
    undulation so the 20 and 50 contours wander rather than rule."""
    sd = _shore_distance(x, y)
    d = 2.5 + sd * 0.09 if sd <= 85 else 10.15 + (sd - 85) * 0.055
    d += 2.6 * math.sin((y - 20) / 80.0) + 1.6 * math.cos(x / 170.0)
    fair = c.dist_to_polyline(x, y, COURSE)
    d += 5.0 * math.exp(-(fair / 44.0) ** 2)
    if x < 520 and y < ANCH[1] - 20:
        d -= 1.5 * smoothstep((ANCH[1] - 20 - y) / 90) * smoothstep((520 - x) / 150)
    return max(3.0, min(56.0, d))


def _samples(jit: c.Jitter) -> list[tuple[float, float, float]]:
    out = []
    g = jit.sub("samples")
    for gy in range(50, MAP_BOTTOM, 72):
        for gx in range(250, 1090, 96):
            x, y = gx + g.offset(16), gy + g.offset(14)
            if x < 232 or x > 1076 or y < 30 or y > MAP_BOTTOM - 8:
                continue
            if math.hypot(x - SHOAL[0], y - SHOAL[1]) < 66:
                continue
            if math.hypot(x - ANCH[0], y - ANCH[1]) < 110:
                continue
            v = _depth_design(x, y) + g.offset(1.2)
            out.append((round(x), round(y), round(max(3.0, v), 1)))
    return out


# ------------------------------------------------------------------ the sheet
class _Sheet:
    def __init__(self, ctx):
        self.ctx = ctx
        self.ed = ctx.ed
        self.t = ctx.ed.theme
        self.night = ctx.ed.dark
        self.phone = ctx.ed.phone
        self.w, self.h = SIZES[ctx.ed.scale]
        self.rules = RULES[ctx.ed.scale]
        # phone editions are frozen (MASTERPLAN 7.3); motion only on desk motion editions
        self.tl = ctx.tl if (ctx.ed.motion and not self.phone) else T.NullTimeline(NAME)
        self.data = ctx.data
        self.cfg = ctx.cfg
        self.log = ctx.log or {}
        self.jit = c.Jitter(SEED, "approaches")
        self.defs: list[str] = []
        self.layers: dict[str, list[str]] = {n: [] for n in
                                            ("paper", "water", "soundings", "lines", "marks", "panels", "frame", "margin")}
        self.symbols_used: set[str] = set()
        self.legend_ids: set[str] = set()
        self.lights: list[dict] = []
        self.extra_excl: list[tuple[float, float, float, float]] = []
        # ---- data
        self.repo_count = int(self.data.get("repo_count") or len(self.data.get("repos") or []))
        shards = (self.log.get("profile") or {}).get("shards")
        self.shards = int(shards) if shards else 8
        self.shards_measured = bool(self.log.get("measured"))
        claims = self.data.get("claims") or {}
        si = (claims.get("scrape_interval") or {}).get("value")
        try:
            si = int(float(si)) if si is not None else None
        except (TypeError, ValueError):
            si = None
        # the real monitoring/prometheus.yml says 15 s (T8); until the claim is wired it is the fallback
        self.scrape = si if si in tokens.LOOP_PERIODS else (15 if si is None else None)
        self.scrape_measured = bool((claims.get("scrape_interval") or {}).get("measured")) and self.scrape == si
        self.scrapy = next((r for r in self.data.get("repos") or [] if r.get("name") == "Scrapy"), {})
        self.edition_v = self.data.get("edition") or {}
        self.trial = self.data.get("trial")

    # ---------------------------------------------------------------- helpers
    def P(self, x: float, y: float) -> tuple[float, float]:
        if not self.phone:
            return (x, y)
        return (round(PH_X0 + (y - MAP_TOP) * PH_S, 1), round(PH_Y0 + (PH_CROP - x) * PH_S, 1))

    def Ppts(self, pts):
        return [self.P(x, y) for x, y in pts]

    def Prect(self, x, y, w, h):
        """A desk rect mapped to the phone (axis-aligned stays axis-aligned)."""
        if not self.phone:
            return (x, y, w, h)
        (x0, y0), (x1, y1) = self.P(x, y), self.P(x + w, y + h)
        return (min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))

    def txt(self, s, x, y, role="label", **kw) -> str:
        kw.setdefault("edition", self.ed)
        return k.text_use(s, x, y, role, **kw)

    def lbl(self, s, x, y, role="label", **kw) -> str:
        """chartlib's label_cb."""
        kw.setdefault("edition", self.ed)
        return k.label(s, x, y, role, **kw)

    def width(self, s, role="label", **kw) -> float:
        kw.setdefault("edition", self.ed)
        return k.text_width(s, role, **kw)

    def fit(self, s, role, avail, **kw) -> str:
        """Assert a panel string fits its cell (risk 6): the build fails loudly, never silently clips."""
        w = self.width(s, role, **kw)
        if w > avail:
            raise ValueError(f"approaches: {s!r} ({role}) is {w:.0f} px, cell allows {avail:.0f}")
        return s

    def snd(self, v, x, y, sub=None, truth="illustrative", **kw) -> str:
        kw.setdefault("edition", self.ed)
        if self.night:
            kw.setdefault("opacity", 0.7)
        return k.sounding(v, x, y, sub=sub, truth=truth, **kw)

    def use(self, name, x, y, scale=1.0, rotate=0, extra="") -> str:
        self.symbols_used.add(name)
        return c.use(name, x, y, PREFIX, scale=scale, rotate=rotate, extra=extra)

    def use_legend(self, name, x, y, scale=1.0, rotate=0) -> str:
        self.legend_ids.add(name)
        self.symbols_used.add(name)
        return c.use(name, x, y, PREFIX, scale=scale, rotate=rotate)

    def stroke(self, *a, **kw) -> str:
        return c.stroke(*a, **kw)

    def exclude(self, name, x, y, w, h):
        k.exclude(name, x, y, w, h)
        self.extra_excl.append((x, y, w, h))

    def cartouche(self, x, y, w, h, name) -> str:
        out = [f'<rect x="{E.I(x)}" y="{E.I(y)}" width="{E.I(w)}" height="{E.I(h)}" fill="{self.t.paper}" '
               f'{self.stroke("HAIR", self.t.ink, 0.85, caps="butt")}/>']
        self.exclude(name, x - 4, y - 4, w + 8, h + 8)
        return "".join(out)

    def light_group(self, x, y, lit_id, character, begin, color=None, r=2.0) -> str:
        """A flashing core (+ halo at night) whose group opacity takes the light's character."""
        anim = (self.tl.flash(character, begin=begin, still="lit", name=f"{lit_id}-fl")
                if self.tl.motion and character != "F" else "")
        core = c.lit_core(x, y, self.t, lit_id, r=r, halo_r=(14 if self.night else None), prefix=PREFIX, color=color)
        self.lights.append({"id": lit_id, "character": character, "color": color or self.t.light_core,
                            "bbox": [E.I(x - 14), E.I(y - 14), 28, 28]})
        return f"<g>{anim}{core}</g>"

    # ---------------------------------------------------------------- the field
    def build_field(self):
        jit = self.jit
        samples_d = _samples(jit)
        if not self.phone:
            coast = _Coast((6, MAP_TOP, 1254, MAP_BOTTOM - MAP_TOP + 60), {"l": 6, "r": 24, "t": 24, "b": 24},
                           ("x",) + UNSURVEYED_FADE)
            samples = samples_d
            extra = LAND + CARVE
            feats = [c.Feature("429 Shoal", 0, "shoal", SHOAL[0], SHOAL[1], r=SHOAL_R)]
            w, h = W_DESK, H_DESK
            h_snd = H_SND
        else:
            s = PH_S
            fa, fb = (self.P(UNSURVEYED_FADE[0], 0)[1], self.P(UNSURVEYED_FADE[1], 0)[1])
            x0, _ = self.P(0, MAP_TOP)
            x1, _ = self.P(0, MAP_BOTTOM)
            yb = self.P(0, 0)[1]
            coast = _Coast((x0 - 8, PH_Y0 - 10, x1 - x0 + 16, yb - PH_Y0 + 20), {"l": 24, "r": 24, "t": 24, "b": 6},
                           ("y", fa, fb))
            samples = [(*self.P(x, y), v) for x, y, v in samples_d]
            extra = [(*self.P(x, y), hh * s, amp) for x, y, hh, amp in LAND + CARVE]
            px, py = self.P(*SHOAL)
            feats = [c.Feature("429 Shoal", 0, "shoal", px, py, r=SHOAL_R * s)]
            w, h = SIZES["phone"]
            h_snd = H_SND * s
        self.field = c.Field.from_soundings(w, h, samples, BASE, feats, coast, h_snd=h_snd, extra=extra)
        self.cs = c.contours(self.field, LEVELS)
        self.ctx.extra["field_report"] = {"n_samples": self.field.report.n_samples,
                                          "residual_max": round(self.field.report.residual_max, 4),
                                          "unclosed": c.closed_check(self.cs, levels=(0.0, 5.0, 10.0))}

    # ---------------------------------------------------------------- layers
    def draw_paper(self):
        d, b = c.paper(self.w, self.h, self.t, self.ed.name, self.jit, margin=self.rules[0])
        self.defs.append(d)
        self.layers["paper"].append(b)

    def map_rect(self):
        """The water's clip: the map area on the desk, the rotated chart on the phone."""
        if self.phone:
            x0, _ = self.P(0, MAP_TOP)
            x1, _ = self.P(0, MAP_BOTTOM)
            return (x0, PH_Y0, x1 - x0, self.P(0, 0)[1] - PH_Y0)
        r1 = self.rules[1]
        return (r1, r1, self.w - 2 * r1, MAP_BOTTOM - r1)

    def draw_water(self):
        t, jit, cs = self.t, self.jit, self.cs
        W = self.layers["water"]
        mx, my, mw, mh = self.map_rect()
        self.defs.append(f'<clipPath id="neat"><rect x="{E.fmt(mx)}" y="{E.fmt(my)}" width="{E.fmt(mw)}" height="{E.fmt(mh)}"/></clipPath>')
        W.append('<g clip-path="url(#neat)">')
        W.append(c.tint_bands(cs, t, levels=(10.0, 5.0)))
        W.append(c.coastline(cs, t, swell=not (self.night or self.phone)))
        if not self.phone:                                   # the vignette is a desk texture (16 KB at phone scale)
            for poly in c.level_polygons(cs, 0.0):
                if abs(c.polygon_area(poly)) > 4000:
                    W.append(c.coast_vignette(poly, t, jit, step=8.0))
        shoal_pt = self.P(*SHOAL)
        W.append(c.danger_lines(cs, 5.0, t, jit, inside=[shoal_pt]))
        op = 0.55 * (0.6 if self.night else 1.0)
        if self.phone:
            self.breaks = []
            W.append(c.draw_contours(cs, INDEX_LEVELS, t, opacity=op, min_len=60))
        else:
            excl = [ZOC, (TITLE_C[0] - 190, 30, 380, 90), (LIMIT_X - 10, MAP_TOP, 180, MAP_BOTTOM - MAP_TOP), SURVEY,
                    (MOLE_A[0] - 10, MOLE_A[1] - 30, 160, 60)]
            breaks = c.contour_labels(cs, min_len=200, gap=18, exclusions=excl, levels=(5.0, 10.0, 20.0, 50.0))
            # no figure in the sheet's corners (where contours leave the neat line) and none within 28 px of another
            kept, anchors = [], []
            for br in breaks:
                bx, by, _a = c.break_anchor(br[0], br[1], br[2])
                if not (70 <= bx <= 1060 and 44 <= by <= MAP_BOTTOM - 22):
                    continue
                if any(math.hypot(bx - qx, by - qy) < 28 for qx, qy in anchors):
                    continue
                kept.append(br)
                anchors.append((bx, by))
            self.breaks = kept
            approx = (UNSURVEYED_FADE[0] - 40, MAP_TOP, LIMIT_X - UNSURVEYED_FADE[0] + 40, MAP_BOTTOM - MAP_TOP)
            W.append(c.draw_contours(cs, INDEX_LEVELS, t, approx_clip=approx, breaks=self.breaks, opacity=op, min_len=60))
        # the unsurveyed hatch, running to the sheet edge where the neat line is broken
        band = self.Prect(LIMIT_X, MAP_TOP, (PH_CROP if self.phone else 1260) - LIMIT_X, MAP_BOTTOM - MAP_TOP)
        ramp = None if self.phone else (band[0], band[0] + 40)
        hd, hb = c.hatch(band, t, jit.sub("band"), "unsurveyed", "hatch-band", ramp=ramp)
        self.defs.append(hd)
        W.append(f'<g opacity=".35">{hb}</g>' if self.night else hb)
        W.append("</g>")   # end map clip
        if not self.phone:
            for y0 in (_y(300), _y(560)):
                hd2, hb2 = c.hatch((1259, y0, 21, 24), t, jit.sub(f"gap{y0}"), "unsurveyed", f"hatch-gap{y0}")
                self.defs.append(hd2)
                W.append(f'<g opacity=".35">{hb2}</g>' if self.night else hb2)

    def draw_contour_figures(self):
        if self.phone:
            return
        out = []
        for ctr, i0, i1 in self.breaks:
            x, y, ang = c.break_anchor(ctr, i0, i1)
            out.append(self.txt(str(int(ctr.level)), x, y + 3.5, "contour-figure", anchor="middle", rotate=ang,
                                fill=self.t.ink2, semantic=False))
            self.extra_excl.append((x - 10, y - 8, 20, 14))
        self.layers["soundings"].extend(out)

    def draw_limit_and_zones(self):
        t, jit = self.t, self.jit
        L, M = self.layers["lines"], self.layers["marks"]
        g = jit.sub("limit")
        pts = []
        y = MAP_TOP
        while y <= MAP_BOTTOM:
            pts.append((LIMIT_X + g.offset(6), y))
            y += 48
        pts.append((LIMIT_X + g.offset(6), MAP_BOTTOM))
        P = self.Ppts(pts)
        d = "M" + "L".join(f"{E.fmt(x)} {E.fmt(y)}" for x, y in P)
        L.append(f'<path d="{d}" fill="none" {self.stroke("PEN", t.ink, 0.85, "LIMIT", caps="butt")}/>')
        # zone letters boxed on the limit line; the seeds push the edge
        for letter, zy in ZONE_Y.items():
            x, y = self.P(LIMIT_X, zy)
            if self.phone:
                bw, y = 30, y + 16          # hung below the line so the band's labels stay clear
            else:
                bw = 16
            L.append(f'<rect x="{E.fmt(x - bw / 2)}" y="{E.fmt(y - bw / 2)}" width="{bw}" height="{bw}" fill="{t.paper}" '
                     f'{self.stroke("PEN", t.ink, 0.9, caps="butt")}/>')
            L.append(self.txt(letter, x, y + (4.5 if not self.phone else 9), "label", anchor="middle"))
            self.extra_excl.append((x - bw, y - bw, 2 * bw, 2 * bw))
        limit_label = self.cfg["copy"]["limit_label"]
        if self.phone:
            lx, ly = self.P(LIMIT_X, MAP_TOP)
            M.append(self.txt(limit_label, lx + 4, ly - 12, "label"))
            rx, _ = self.P(LIMIT_X, MAP_BOTTOM)
            M.append(self.txt("UNSURVEYED", rx - 4, ly - 12, "label", anchor="end", tracking=2.0, fill=t.unsurveyed))
        else:
            M.append(self.txt(limit_label, LIMIT_X + 10, (ZONE_Y["B"] + ZONE_Y["C"]) / 2, "label", anchor="middle", rotate=-90))
            M.append(self.txt("UNSURVEYED", 1182, (MAP_TOP + MAP_BOTTOM) / 2 + 20, "label", anchor="middle", rotate=-90,
                              tracking=2.0, fill=t.unsurveyed))

    def survey_lines(self) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        x0, y0, w, h = SURVEY
        n = self.shards
        segs = []
        for i in range(n):
            y = y0 + (i + 1) * h / (n + 1)
            segs.append(((x0 + 10, round(y, 1)), (x0 + w - 10, round(y, 1))))
        return segs

    def draw_survey_ground(self):
        t = self.t
        L = self.layers["lines"]
        segs = self.survey_lines()
        self.track_segs = segs
        rx0, ry0 = RESTRICTED[0]
        rx1, ry1 = RESTRICTED[2]
        d = []
        for (ax, ay), (bx, by) in segs:
            if ry0 - 6 < ay < ry1 + 6:
                a, b = self.P(ax, ay), self.P(rx0 - 6, ay)          # stop 6 px short of the restricted area
                d.append(f"M{E.fmt(a[0])} {E.fmt(a[1])}L{E.fmt(b[0])} {E.fmt(b[1])}")
                if bx > rx1 + 12:
                    a, b = self.P(rx1 + 6, ay), self.P(bx, by)
                    d.append(f"M{E.fmt(a[0])} {E.fmt(a[1])}L{E.fmt(b[0])} {E.fmt(b[1])}")
            else:
                a, b = self.P(ax, ay), self.P(bx, by)
                d.append(f"M{E.fmt(a[0])} {E.fmt(a[1])}L{E.fmt(b[0])} {E.fmt(b[1])}")
        L.append(f'<path d="{"".join(d)}" fill="none" {self.stroke("HAIR", t.ink, 0.55, "TRACK", caps="butt")}/>')
        if not self.phone:
            d = []
            ya, yb = segs[0][0][1], segs[-1][0][1]
            for x in (790, 890, 990):            # check lines (dedup), stopping at the restricted area
                if rx0 - 6 < x < rx1 + 6:
                    d.append(f"M{x} {E.fmt(ya)}L{x} {E.fmt(ry0 - 6)}M{x} {E.fmt(ry1 + 6)}L{x} {E.fmt(yb)}")
                else:
                    d.append(f"M{x} {E.fmt(ya)}L{x} {E.fmt(yb)}")
            L.append(f'<path d="{"".join(d)}" fill="none" {self.stroke("HAIR", t.ink, 0.35, "TRACK", caps="butt")}/>')
        L.append(c.restricted_line(self.Ppts(RESTRICTED), t))
        M = self.layers["marks"]
        if self.phone:
            x, y = self.P((rx0 + rx1) / 2, (ry0 + ry1) / 2)
            M.append(self.txt("robots.txt", x, y + 9, "label", anchor="middle"))
        else:
            M.append(self.txt("robots.txt · Disallow", rx0 + 8, ry0 + 17, "label", within=(rx0, ry0, rx1 - rx0, ry1 - ry0)))
            # caption at line 1's east end: one shard per core · {n} here (n italic until measured)
            ex, ey = segs[0][1]
            head, n_s, tail = "one shard per core · ", str(self.shards), " here"
            n_role = "label" if self.shards_measured else "label-italic"
            w_head, w_n = self.width(head), self.width(n_s, n_role)
            x0, y = ex - (w_head + w_n + self.width(tail)), ey - 6
            M.append(self.txt(head, x0, y, "label"))
            M.append(self.txt(n_s, x0 + w_head, y, n_role, truth="measured" if self.shards_measured else "illustrative",
                              key="shards"))
            M.append(self.txt(tail, x0 + w_head + w_n, y, "label"))
        # doubt marks: Rep in zone A, ED in zone B, SD (beside its sounding) in zone C
        for kind, (x, y) in (("Rep", REP), ("ED", ED_)):
            px, py = self.P(x, y)
            M.append(c.doubt(kind, px, py, self.lbl, PREFIX))
            self.symbols_used.add("rep" if kind == "Rep" else "ed")
            self.extra_excl.append((px - 12, py - 12, 50, 24))
        sx, sy = self.P(*SD)
        if self.phone:
            sx, sy = self.P(SD[0], SD[1] - 36)      # clear of the last track line's fixes after the rotation
            M.append(c.doubt("SD", sx, sy, self.lbl, PREFIX))
        else:
            M.append(self.snd(E.I(self.field.value(*SD)), sx, sy + 4, truth="illustrative"))
            M.append(c.doubt("SD", sx + 10, sy, self.lbl, PREFIX))
            self.extra_excl.append((sx - 14, sy - 10, 48, 18))
            # pencil note with a leader to the Rep ring: between track lines 2 and 3
            y1, y2 = segs[0][0][1], segs[1][0][1]
            nx, ny = 696, E.I((y1 + y2) / 2 + 6)
            self.note_pos = (nx, ny)
            M.append(self.txt("sitemap says yes; the lead says no", nx, ny, "note", fill=self.t.muted, rotate=-4, opacity=0.9))
            M.append(f'<path d="M{nx + 70} {ny - 16}Q{nx + 76} {ny - 32} {REP[0] - 8} {REP[1] + 6}" fill="none" '
                     f'{self.stroke("HAIR", self.t.muted, 0.8)}/>')

    def draw_channel(self):
        t, jit = self.t, self.jit
        L, M = self.layers["lines"], self.layers["marks"]
        P = self.P
        # outer leg: pecked course with waypoints
        L.append(c.course(self.Ppts([W0, W1]), t, jit, pecked=True, prefix=PREFIX, bearings=False))
        self.symbols_used.add("waypoint")
        # the leading line: the darkest ruled line on the sheet, from the front mark out to W1 (the "1"/"2" pair)
        f, w1 = P(*LDG_FRONT), P(*W1)
        L.append(f'<path d="M{E.fmt(f[0])} {E.fmt(f[1])}L{E.fmt(w1[0])} {E.fmt(w1[1])}" fill="none" {self.stroke("LINE", t.ink)}/>')
        for wp in (W2, W3, W4, ANCH):
            x, y = P(*wp)
            M.append(self.use("waypoint", x, y))
        for pt in (LDG_FRONT, LDG_REAR):
            x, y = P(*pt)
            M.append(self.use("ldg", x, y))
        ax, ay = P(*ANCH)
        M.append(self.use("anchorage", ax, ay, scale=1.3))
        # proposed channel from the end of the last track line: pecked, hollow marks, unlit
        last = self.track_segs[-1]
        start = (last[0][0], last[0][1])
        self.proposed_start = start
        a, b = P(*start), P(*W0)
        L.append(f'<path d="M{E.fmt(a[0])} {E.fmt(a[1])}L{E.fmt(b[0])} {E.fmt(b[1])}" fill="none" '
                 f'{self.stroke("PEN", t.ink, 0.7, "PECK", caps="butt")}/>')
        for side, kind in (("starboard", "nun"), ("port", "can")):
            hx, hy = c.lateral_offset((W0, start), 0.5, side, 15)
            px, py = P(hx, hy)
            M.append(self.hollow_mark(kind, px, py))
            self.extra_excl.append((px - 12, py - 18, 24, 24))
        # lateral marks, Region B, returning: starboard = north. Pairs 1/2 off the outer end of the leading
        # line, 3/4 as the entrance gate, at honest, irregular spacing. The outer pair carries the Fl 4s the
        # hero shares; the gate is told apart by its group flash (IALA: no two neighbours alike)
        legs = [((W1, W2), 0.08, 26), ((W1, W2), 0.42, 24), ((W2, W3), 0.78, 24), ((W3, W4), 0.10, 26)]
        marks = [("can", 1, "URLS", "port", "Fl G 4s", 0.0),
                 ("nun", 2, "SCOUT", "starboard", "Fl R 4s", 2.0),
                 ("can", 3, "ANALYZE", "port", "Fl(2) G 10s", 0.0),
                 ("nun", 4, "SUMMARIZE", "starboard", "Fl(2) R 10s", 2.0)]
        self.mark_pts = []
        for (leg, frac, off), (kind, num, stage, side, char, begin) in zip(legs, marks):
            mx, my = c.lateral_offset(leg, frac, side, off)
            self.mark_pts.append((mx, my))
            x, y = P(mx, my)
            M.append(self.use(kind, x, y))
            top = y - 15 if kind == "can" else y - 16
            M.append(self.light_group(x, top, f"lt-{'g' if kind == 'can' else 'r'}{num}", char, begin))
            letter = "G" if kind == "can" else "R"
            if self.phone:
                # after the rotation north (starboard) is to the LEFT of the channel, south to the right;
                # R "4" lies under the mole's lee, so its label goes below the mark
                if num == 4:
                    M.append(self.txt(f'{letter} "{num}"', x, y + 28, "label-italic", anchor="middle"))
                elif num == 1:                       # clear of the shoal's ring
                    M.append(self.txt(f'{letter} "{num}"', x, y - 24, "label-italic", anchor="middle"))
                elif side == "starboard":
                    M.append(self.txt(f'{letter} "{num}"', x - 18, y + 2, "label-italic", anchor="end"))
                else:
                    M.append(self.txt(f'{letter} "{num}"', x + 18, y + 2, "label-italic"))
            elif side == "starboard":           # north: label above (outboard)
                M.append(self.txt(f'{letter} "{num}" {stage}', x + 8, y - 22, "label-italic"))
                M.append(self.txt(char, x + 8, y - 8, "label-italic"))
            else:                               # south: label below (outboard)
                M.append(self.txt(f'{letter} "{num}" {stage}', x + 6, y + 14, "label-italic"))
                M.append(self.txt(char, x + 6, y + 28, "label-italic"))
        # bearings: the outer leg (a drawn angle, so sloping) and the leading line (a construction, upright)
        if not self.phone:
            b0 = c.compass_bearing(W0, W1)
            M.append(self.txt(f"{round(b0) % 360:03d}°", (W0[0] + W1[0]) / 2 + 16, (W0[1] + W1[1]) / 2 + 4, "label-italic"))
            M.append(self.txt(f"Health Ldg Lts {LDG_BRG:.0f}°", (W1[0] + W2[0]) / 2 - 38, (W1[1] + W2[1]) / 2 - 57, "label",
                              anchor="middle"))
            # the shoal is drawn from an illustrative field: its position is approximate
            M.append(c.doubt("PA", SHOAL[0] + 26, SHOAL[1] + 2, self.lbl, PREFIX))
        else:
            lx, ly = P((W3[0] + W4[0]) / 2, (W3[1] + W4[1]) / 2)
            M.append(self.txt(f"Ldg {LDG_BRG:.0f}°", lx + 24, ly + 9, "label"))
        # Grafana Lt on the headland, with its horn
        gx, gy = P(*GRAFANA)
        M.append(self.use("light", gx, gy))
        M.append(self.use("horn", gx, gy))
        char = f"Fl {self.scrape}s" if self.scrape is not None else "F"
        M.append(self.light_group(gx, gy, "lt-grafana", char, 0.0, r=1.6))
        if self.night:   # two static ruled rays toward the channel (no filter)
            for ang in (96, 108):
                a = math.radians(ang)
                M.append(f'<path d="M{E.fmt(gx + 18 * math.cos(a))} {E.fmt(gy + 18 * math.sin(a))}'
                         f'L{E.fmt(gx + 150 * math.cos(a))} {E.fmt(gy + 150 * math.sin(a))}" fill="none" '
                         f'{self.stroke("HAIR", t.flare, 0.12)}/>')
        if self.phone:
            M.append(self.txt("Grafana Lt", gx + 20, gy - 6, "label"))
        else:
            M.append(self.txt(f"Grafana Lt · {char}", gx + 18, gy - 4, "label",
                              truth=("measured" if self.scrape_measured else None),
                              key=("scrape_interval" if self.scrape_measured else None)))
            M.append(self.txt("Horn", gx + 18, gy + 12, "label"))
        # harbour and water names
        if self.phone:
            hx, hy = P(110, _y(206))
            M.append(self.txt("SCRAPY HARBOR", hx, hy, "title", anchor="middle"))
            dx, dy = P(ANCH[0] - 46, ANCH[1] + 30)
            M.append(self.txt("Delta Lake", dx, dy, "place-water", anchor="middle"))
            sx, sy = P(*SHOAL)
            M.append(self.txt("429 Shoal", sx, sy + 60, "place-water", anchor="middle"))
        else:
            M.append(self.txt("SCRAPY", 96, _y(262), "title", anchor="middle"))
            M.append(self.txt("HARBOR", 96, _y(262) + 32, "title", anchor="middle"))
            M.append(self.txt("Delta Lake", ANCH[0] - 2, ANCH[1] + 30, "place-water", anchor="middle"))
            M.append(self.txt("429 Shoal", SHOAL[0] - 32, SHOAL[1] + 4, "place-water", anchor="end"))
            M.append(self.txt("Local knowledge advised · see Notices 1–5", 232, MAP_BOTTOM - 9, "label"))
            M.append(self.txt("proposed · unlit", (start[0] + W0[0]) / 2 + 4, (start[1] + W0[1]) / 2 + 30, "label-italic",
                              anchor="middle"))
        # the wreck: a real dead branch of the harbour repo
        branches = self.scrapy.get("stale_branches") or []
        if branches:
            br = next((b for b in branches if len(b.get("name", "")) <= 26), branches[0])
            wx, wy = P(*WRECK)
            M.append(self.use("wreck", wx, wy))
            name = br.get("name", "")
            if len(name) > 26:
                name = name[:24] + "…"
            yr = str(br.get("last", ""))[:4]
            if self.phone:
                M.append(self.txt(f"Wk ’{yr[2:]}", wx + 16, wy + 9, "label-italic"))
            else:
                M.append(self.txt(f"Wk ’{yr[2:]}", wx + 14, wy - 2, "label-italic"))
                M.append(self.txt(name, wx + 14, wy + 12, "label"))

    def hollow_mark(self, kind, x, y, scale: float = 1.0) -> str:
        d = "M-5.5 0v-13h11v13z" if kind == "can" else "M-6 0L6 0L0 -14Z"
        sc = f" scale({E.fmt(scale)})" if scale != 1.0 else ""
        return (f'<g transform="translate({E.fmt(x)} {E.fmt(y)}){sc}"><g transform="rotate(8)">'
                f'<path d="{d}" fill="none" {self.stroke("PEN", self.t.ink, 0.8)}/></g>'
                f'<circle r="1.2" fill="{self.t.paper}" {self.stroke("PEN", self.t.ink)}/></g>')

    # ---------------------------------------------------------------- the harbour works and the mole
    def mole_cells(self):
        """The WAL mole: (n−1)·6 + 8 blocks in two courses from the north headland root toward the mouth;
        returns [(quad, k)] with k the fix index for the last eight (None for the ones already laid)."""
        n_cells = (self.shards - 1) * 6 + 8
        per_row = math.ceil(n_cells / 2)
        ax, ay = MOLE_A
        bx, by = MOLE_B
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux
        step = L / per_row
        across = 5.2
        out = []
        for i in range(n_cells):
            col, row = divmod(i, 2)
            s0, s1 = col * step + 0.4, (col + 1) * step - 0.4
            o = (row - 0.5) * across
            quad = [(ax + ux * s0 + nx * (o - across / 2 + 0.3), ay + uy * s0 + ny * (o - across / 2 + 0.3)),
                    (ax + ux * s1 + nx * (o - across / 2 + 0.3), ay + uy * s1 + ny * (o - across / 2 + 0.3)),
                    (ax + ux * s1 + nx * (o + across / 2 - 0.3), ay + uy * s1 + ny * (o + across / 2 - 0.3)),
                    (ax + ux * s0 + nx * (o + across / 2 - 0.3), ay + uy * s0 + ny * (o + across / 2 - 0.3))]
            k_ = i - (n_cells - 8) if i >= n_cells - 8 else None
            out.append((quad, k_))
        return out

    def draw_harbour(self):
        """The harbour works at chart scale: the WAL mole with its head light, quays named for the Delta
        tables and the workers, the anchorage. Nothing here is an enlargement; it is the chart."""
        t, P = self.t, self.P
        M = self.layers["marks"]
        for quad, kidx in self.mole_cells():
            pts = self.Ppts(quad)
            d = "M" + "L".join(f"{E.fmt(x)} {E.fmt(y)}" for x, y in pts) + "Z"
            cell = f'<path class="wal" d="{d}" fill="{t.ink}" fill-opacity=".82" {self.stroke("HAIR", t.ink, 0.7, caps="butt")}/>'
            M.append(cell if kidx is None else self.tl.reveal(cell, 28.0 + 2 * kidx))
        bx, by = MOLE_B
        ax, ay = MOLE_A
        L = math.hypot(bx - ax, by - ay)
        hx, hy = bx + (bx - ax) / L * 9, by + (by - ay) / L * 9
        lx, ly = P(hx, hy)
        M.append(self.use("light", lx, ly, scale=0.8))
        M.append(self.light_group(lx, ly, "lt-mole", "F", 0.0, r=1.3))
        self.extra_excl.append((min(ax, bx) - 8, min(ay, by) - 10, abs(bx - ax) + 30, abs(by - ay) + 22))
        if self.phone:
            return
        M.append(self.txt("write-ahead log · one cell per sounding", ax + 62, ay - 8, "label"))
        q = lambda x, y, w, h: (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t.paper}" '  # noqa: E731
                                f'{self.stroke("PEN", t.ink)}/>')
        cy = ANCH[1]
        # quays on the basin's shores, named for the three Delta tables; the anchorage itself is the raw
        # table, so it alone carries a sounding (the row count, upright once stats.trial carries a run)
        M.append(q(146, cy - 46, 18, 5) + self.txt("stage4_summaries", 42, cy - 54, "label"))
        M.append(q(196, cy - 42, 5, 18) + self.txt("stage1_discovery", 158, cy - 54, "label"))
        M.append(q(146, cy + 46, 18, 5) + self.txt("stage2_page_analysis", 36, cy + 66, "label"))
        spot = next(((x, y) for x, y in ((196, cy - 18), (150, cy - 16), (204, cy), (150, cy + 20))
                     if self.field.value(x, y) > 2.0), (196, cy - 18))
        tables = (self.trial or {}).get("tables") if isinstance(self.trial, dict) else None
        if isinstance(tables, dict) and "stage1_discovery" in tables:
            rows = int(tables["stage1_discovery"].get("rows", 0))
            M.append(self.snd(rows // 1000, spot[0], spot[1], sub=(rows % 1000) // 100, truth="measured", role="label",
                              key="rows_stage1_discovery"))
        else:
            M.append(self.snd(E.I(max(1.0, self.field.value(*spot))), spot[0], spot[1], truth="illustrative"))
        self.extra_excl.append((spot[0] - 12, spot[1] - 12, 24, 16))
        # the works on the land: Prometheus mast, Redis tanks with the traffic signal beside them,
        # PostgreSQL tanks, the BART summarization shed
        M.append(f'<path d="M58 {cy - 74}V{cy - 100}M54 {cy - 94}h8M55 {cy - 87}h6" fill="none" {self.stroke("PEN", t.ink)}/>')
        M.append(self.txt("Prometheus", 66, cy - 78, "label"))
        M.append(q(160, cy + 110, 10, 10) + q(172, cy + 110, 10, 10) + self.txt("Redis · queues", 40, cy + 120, "label"))
        M.append(self.use("traffic", 196, cy + 122) + self.txt("Traffic Sig", 40, cy + 138, "label"))
        M.append(q(160, cy + 146, 14, 9) + q(160, cy + 157, 14, 9) + self.txt("PostgreSQL · metrics", 40, cy + 156, "label"))
        M.append(q(160, cy + 168, 26, 12) + self.txt("Summarization Wks", 40, cy + 174, "label"))

    # ---------------------------------------------------------------- vessels (motion)
    def draw_vessels(self):
        tl = self.tl
        M = self.layers["marks"]
        # packet boat on the lit channel: 7 fixes at 0, 4 … 24 s, held to 96
        pts = c.course_samples(self.Ppts(COURSE), 7)
        fixes = [(x, y) for x, y, _ in pts]
        ax, ay = fixes[-1]
        px, py = fixes[-2]
        L = math.hypot(ax - px, ay - py) or 1
        fixes[-1] = (ax - (ax - px) / L * 14, ay - (ay - py) / L * 14)   # lies 14 px short of her anchor
        glyph = f'<g transform="scale(-0.8 0.8)">{self.use("sloop-glyph", 0, 0)}</g>'
        mark = self.use("fix", 0, 0)
        M.append(tl.fixes(fixes, 0.0, every=4.0, hold=72.0, boat=glyph, mark=mark, name="packet"))
        for x, y in fixes:
            self.extra_excl.append((x - 8, y - 8, 16, 16))
        # survey vessel: 8 fixes east → west along the last track line at 28, 30 … 42 s; sounding k and
        # mole block k appear at fix k (the soundings fill in behind the vessel)
        (ax, ay), (bx, by) = self.track_segs[-1]
        xs = [bx - 20 - i * (bx - ax - 40) / 7 for i in range(8)]
        self.survey_fixes = [(round(x), ay) for x in xs]
        vessel = f'<g transform="scale(-1 1)">{self.use("sloop-glyph", 0, 0)}</g>'
        M.append(tl.fixes(self.Ppts(self.survey_fixes), 28.0, every=2.0, boat=vessel, mark=mark, name="survey"))
        if not self.phone:
            for i, (x, y) in enumerate(self.survey_fixes):
                v = E.I(self.field.value(x, y))
                M.append(tl.reveal(self.snd(v, x, y - 9, truth="illustrative"), 28.0 + 2 * i))
                self.extra_excl.append((x - 12, y - 20, 24, 16))

    # ---------------------------------------------------------------- soundings
    def draw_soundings(self):
        S = self.layers["soundings"]
        excl = list(k.exclusions()) + self.extra_excl
        pts = []
        if not self.phone:
            # the survey ground: six per line, laid with the lead's irregularity (seeded ±3 px along the
            # track, uneven spacing), fewer on the two lines the pencil note crosses; none on the last line
            g = self.jit.sub("lead")
            nx0, nx1 = self.note_pos[0] - 10, self.note_pos[0] + 206
            for li, seg in enumerate(self.track_segs[:-1]):
                y = seg[0][1]
                drop = {g.choice(range(6))} if li in (0, 1) else set()
                for j in range(6):
                    if j in drop:
                        continue
                    x = 722 + j * 60 + g.uniform(-9, 9)
                    if li in (0, 1) and nx0 < x < nx1 and g.uniform(0, 1) < 0.5:
                        continue
                    if math.hypot(x - SD[0], (y - 7) - SD[1]) < 30:        # the doubted sounding takes this node
                        continue
                    pts.append((round(x + g.uniform(-3, 3), 1), y - 7 + g.uniform(-1, 1), "survey"))
            g = self.jit.sub("snd")
            for i in range(1, 200):
                x = 230 + c.halton(i, 2) * (LIMIT_X - 24 - 230)
                y = 36 + c.halton(i, 3) * (MAP_BOTTOM - 12 - 36)
                pts.append((x + g.offset(4), y + g.offset(4), "water"))
        else:
            g = self.jit.sub("snd-phone")
            for i in range(1, 160):
                x = 232 + c.halton(i, 2) * (LIMIT_X - 30 - 232)
                y = 40 + c.halton(i, 3) * (MAP_BOTTOM - 20 - 40)
                pts.append((x + g.offset(6), y + g.offset(6), "water"))
        placed: list[tuple[float, float]] = []
        min_gap = 36 if not self.phone else 60
        budget = 56 if not self.phone else 14
        n = 0
        rx0, ry0 = RESTRICTED[0]
        rx1, ry1 = RESTRICTED[2]
        for x, y, kind in pts:
            if kind == "water":
                if n >= budget:
                    break
                if SURVEY[0] - 10 <= x <= SURVEY[0] + SURVEY[2] + 10 and SURVEY[1] - 10 <= y <= SURVEY[1] + SURVEY[3] + 10:
                    continue
                if c.dist_to_polyline(x, y, COURSE) < 40 or c.dist_to_polyline(x, y, [self.proposed_start, W0]) < 30:
                    continue
                if math.hypot(x - SHOAL[0], y - SHOAL[1]) < 46 or math.hypot(x - ANCH[0], y - ANCH[1]) < 60:
                    continue
                if any(math.hypot(x - mx, y - my) < 36 for mx, my in self.mark_pts):
                    continue
                if math.hypot(x - WRECK[0], y - WRECK[1]) < 28 or math.hypot(x - GRAFANA[0], y - GRAFANA[1]) < 40:
                    continue
                if c.dist_to_polyline(x, y, [MOLE_A, MOLE_B]) < 22:
                    continue
            if rx0 - 8 <= x <= rx1 + 8 and ry0 - 8 <= y <= ry1 + 8:
                continue
            px, py = self.P(x, y)
            if any(math.hypot(px - qx, py - qy) < min_gap for qx, qy in placed):
                continue
            bw, bh = (22, 12) if not self.phone else (36, 20)
            box = (px - bw / 2 - 2, py - bh + 2, bw + 4, bh + 6)   # the run's own box: ascender to descender
            if any(ex[0] < box[0] + box[2] and ex[0] + ex[2] > box[0] and ex[1] < box[1] + box[3] and ex[1] + ex[3] > box[1]
                   for ex in excl):
                continue
            v = self.field.value(px, py)
            if v < 1.0:
                continue
            placed.append((px, py))
            if kind == "water":
                n += 1
            S.append(self.snd(E.I(v), px, py + (4 if not self.phone else 7), truth="illustrative"))
        self.ctx.extra["soundings"] = len(placed)

    # ---------------------------------------------------------------- panels (desk)
    def header(self, s, x, y, within=None, anchor="start", size=None) -> str:
        return self.txt(s, x, y, "label", tracking=0.6, within=within, anchor=anchor, size=size)

    def body(self, s, x, y, **kw) -> str:
        """Legend definitions and notes bodies: `label` at PANEL_SIZE (17, on SCALE)."""
        return self.txt(s, x, y, "label", size=PANEL_SIZE, **kw)

    def draw_title_block(self):
        if self.phone:
            # open, centre-stacked, no box, no hatch behind it (the band starts below)
            x = 360
            M = self.layers["marks"]
            M.append(self.txt("Approaches to Scrapy Harbor", x, 100, "title", anchor="middle"))
            M.append(self.txt("Surveyed by rustmapper · Datum: main", x, 134, "label", anchor="middle"))
            M.append(self.txt("IALA Region B · marks numbered from seaward", x, 166, "label", anchor="middle"))
            self.exclude("title", 60, 70, 600, 104)
            return
        cx, cy = TITLE_C
        M = self.layers["panels"]
        M.append(self.header("SHEET 3", cx, cy + 6, anchor="middle"))
        M.append(self.txt("Approaches to Scrapy Harbor", cx, cy + 36, "title", anchor="middle"))
        M.append(self.txt("Surveyed by rustmapper 2026 · Datum: main", cx, cy + 56, "label", anchor="middle"))
        M.append(f'<path d="M{cx - 60} {cy + 66}h120" fill="none" {self.stroke("HAIR", self.t.ink, 0.6, caps="butt")}/>')
        self.exclude("title-block", cx - 190, cy - 8, 380, 78)

    def draw_zoc(self):
        """Zones of confidence as a ruled block: hairlines between the rows, no filled or boxed cells."""
        x, y, w, h = ZOC
        t = self.t
        Pn = self.layers["panels"]
        Pn.append(self.cartouche(x, y, w, h, "zoc"))
        Pn.append(self.header("ZONES OF CONFIDENCE", x + 12, y + 16, within=ZOC))
        sources = self.data.get("sources") or self.cfg.get("sources") or []
        names = {s.get("letter"): ACRONYMS.get(str(s.get("name", "")).upper(), str(s.get("name", "")).lower()) for s in sources}
        rule = lambda yy: f'<path d="M{x + 12} {yy}h{w - 24}" fill="none" {self.stroke("HAIR", t.ink, 0.6, caps="butt")}/>'  # noqa: E731
        Pn.append(rule(y + 22))
        for i, letter in enumerate(("A", "B", "C")):
            yy = y + 36 + i * 16
            Pn.append(self.txt(letter, x + 20, yy, "label", anchor="middle", within=ZOC))
            Pn.append(self.txt(names.get(letter, ""), x + 36, yy, "label", within=ZOC))
            Pn.append(self.txt(ZONE_TEXT[letter], x + 150, yy, "label", within=ZOC))
            Pn.append(rule(yy + 4))
        Pn.append(self.txt("A: as declared by the site.  B, C: as found.", x + 20, y + 80, "label", within=ZOC))

    def note_line(self, parts, x, y, within, avail) -> str:
        """A notes line of (role, text) parts on one baseline at PANEL_SIZE (italic parts for quoted figures)."""
        total = sum(self.width(s, role, size=PANEL_SIZE) for role, s in parts)
        if total > avail:
            raise ValueError(f"approaches: note {''.join(s for _, s in parts)!r} is {total:.0f} px, cell allows {avail:.0f}")
        out, pen = [], x
        for role, s in parts:
            truth = "illustrative" if role == "label-italic" and any(ch.isdigit() for ch in s) else None
            out.append(self.txt(s, pen, y, role, size=PANEL_SIZE, within=within, truth=truth))
            pen += self.width(s, role, size=PANEL_SIZE)
        return "".join(out)

    def draw_blocks(self):
        Pn = self.layers["panels"]
        pitch = 17
        # ---- rustmapper
        x, y, w, h = BLOCK_RM
        avail = w - 32
        Pn.append(self.cartouche(x, y, w, h, "block-rustmapper"))
        Pn.append(self.txt("rustmapper", x + 16, y + 34, "title", within=BLOCK_RM))
        ver, date = str(self.edition_v.get("version") or ""), str(self.edition_v.get("date") or "")
        status = str(self.edition_v.get("status") or "provisional")
        Pn.append(self.body(self.fit(f"PyPI {ver} · {status} · {date}", "label", avail, size=PANEL_SIZE), x + 16, y + 56,
                            within=BLOCK_RM, truth="measured", key="edition"))
        Pn.append(self.header("NOTES", x + 16, y + 80, within=BLOCK_RM))
        notes = [
            [("label", "1  Frontier hashed by registrable domain")],
            [("label", "2  One shard per core · permits "), ("label-italic", "256–1024")],
            [("label", "3  Sized by redb commit latency · "), ("label-italic", "250 ms")],
            [("label", "4  WAL crc32 · rkyv · checkpoints to redb")],
            [("label", "5  Seeds A · B · C · robots crawl-delay kept")],
        ]
        for i, parts in enumerate(notes):
            Pn.append(self.note_line(parts, x + 16, y + 98 + i * pitch, BLOCK_RM, avail))
        wheels = self.edition_v.get("wheels") or []
        if wheels:
            tag = str(wheels[0]).replace("cp313-cp313-", "cp313 · ")
            Pn.append(self.body(self.fit(f"Wheel · {tag} · elsewhere pip builds from source", "label", avail, size=PANEL_SIZE),
                                x + 16, y + 182, within=BLOCK_RM, truth="measured", key="wheel"))
        # ---- Scrapy Harbor
        x, y, w, h = BLOCK_SH
        Pn.append(self.cartouche(x, y, w, h, "block-scrapy"))
        Pn.append(self.txt("Scrapy Harbor", x + 16, y + 34, "title", within=BLOCK_SH))
        commits = self.scrapy.get("commits")
        head = f"{self.scrapy.get('language') or 'Python'} · edition main · "
        Pn.append(self.body(head, x + 16, y + 56, within=BLOCK_SH))
        if commits is not None:
            wx = x + 16 + self.width(head, size=PANEL_SIZE)
            cs = f"{int(commits):,}"
            Pn.append(self.body(cs, wx, y + 56, within=BLOCK_SH, truth="measured", key="scrapy_commits"))
            Pn.append(self.body(" commits", wx + self.width(cs, size=PANEL_SIZE), y + 56, within=BLOCK_SH))
        Pn.append(self.header("NOTES", x + 16, y + 80, within=BLOCK_SH))
        notes = ["1  Typed Arrow schema per table",
                 "2  schema_mode=merge · partition by domain",
                 "3  Dedup by URL hash and MinHash",
                 "4  OPTIMIZE / VACUUM from a maintenance queue",
                 "5  Breakers wrap http · delta · redis",
                 "6  BART-large-CNN summaries on the worker"]
        for i, s in enumerate(notes):
            Pn.append(self.body(self.fit(s, "label", avail, size=PANEL_SIZE), x + 16, y + 98 + i * pitch, within=BLOCK_SH))

    def legend_rows(self):
        """(draw(cx, cy, k), text) rows: every charted symbol id in chartlib.symbol_defs (vessels, halo and flare
        are drawn things the legend plug-in allows), the lines, tints and the figure convention."""
        t = self.t
        S = self.stroke
        ink = t.ink

        def line(d, attrs):
            return f'<path d="{d}" fill="none" {attrs}/>'

        months = self.scrapy.get("months_active")
        commits = self.scrapy.get("commits")
        weeks = [w for w in (self.data.get("weeks") or []) if isinstance(w, dict) and w.get("n")]
        hw = max(weeks, key=lambda w: w["n"]) if weeks else None
        sym = lambda name, dx=0, dy=0, sc=1.0: (lambda cx, cy, kk: self.use_legend(name, cx + dx * kk, cy + dy * kk, scale=sc * kk))  # noqa: E731
        return [
            (sym("can", 0, 6), "G can · port, returning"),
            (sym("nun", 0, 6), "R nun · starboard"),
            (sym("light"), "Light · its character"),
            (lambda cx, cy, kk: self.use_legend("ldg", cx - 6 * kk, cy + 4 * kk, scale=kk) + self.use_legend("ldg", cx + 6 * kk, cy, scale=kk)
             + line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy + 8 * kk)}L{E.fmt(cx + 12 * kk)} {E.fmt(cy - 4 * kk)}", S("HAIR", ink, 0.8)),
             "Ldg line · health check"),
            (sym("traffic", 0, 9), "Traffic Sig · breaker"),
            (lambda cx, cy, kk: self.lamps(cx, cy, kk), "go · stop · one at a time"),
            (sym("horn", -6, 0), "Horn · Alertmanager"),
            (sym("anchorage"), "Anchorage · Delta Lake"),
            (sym("wreck", 0, 0, 0.8), "Wk · dead branch, year"),
            (sym("waypoint"), "Waypoint · stage"),
            (sym("fix"), "Fix · position"),
            (sym("station"), "Station · profile repo"),
            (sym("correction"), "Correction · revised"),
            (sym("rep"), "Rep · reported, not found"),
            (sym("ed"), "ED · existence doubtful"),
            (lambda cx, cy, kk: self.txt("SD", cx, cy + 4 * kk, "label-italic", anchor="middle", size=PANEL_SIZE if (kk > 1 and not self.phone) else None),
             "SD · sounding doubtful"),
            (lambda cx, cy, kk: self.txt("PA", cx, cy + 4 * kk, "label-italic", anchor="middle", size=PANEL_SIZE if (kk > 1 and not self.phone) else None),
             "PA · position approximate"),
            (lambda cx, cy, kk: self.txt("A", cx, cy + 4 * kk, "label", anchor="middle", size=PANEL_SIZE if (kk > 1 and not self.phone) else None)
             + f'<rect x="{E.fmt(cx - 8 * kk)}" y="{E.fmt(cy - 8 * kk)}" width="{E.fmt(16 * kk)}" height="{E.fmt(16 * kk)}" fill="none" {S("PEN", ink, 0.9, caps="butt")}/>',
             "Zone · seed source"),
            (lambda cx, cy, kk: self.txt(f"{LDG_BRG:.0f}°", cx, cy + 4 * kk, "label", anchor="middle", size=PANEL_SIZE if (kk > 1 and not self.phone) else None),
             "Bearing · true"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy)}h{E.fmt(24 * kk)}", S("PEN", ink, 0.85, "COURSE")), "Course · lit channel"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy + 4 * kk)}h{E.fmt(24 * kk)}", S("PEN", ink, 0.7, "PECK", caps="butt"))
             + self.hollow_mark("can", cx + 6 * kk, cy - 2 * kk, kk), "Proposed channel · unlit"),
            (lambda cx, cy, kk: f'<circle cx="{E.fmt(cx)}" cy="{E.fmt(cy)}" r="{E.fmt(6 * kk)}" fill="none" {S("LINE", ink, 0.9, "DANGER", gap=4.3)}/>',
             "Danger line · shoal"),
            (lambda cx, cy, kk: f'<rect x="{E.fmt(cx - 12 * kk)}" y="{E.fmt(cy - 5 * kk)}" width="{E.fmt(12 * kk)}" height="{E.fmt(10 * kk)}" fill="{t.shallow_b}"/>'
             f'<rect x="{E.fmt(cx)}" y="{E.fmt(cy - 5 * kk)}" width="{E.fmt(12 * kk)}" height="{E.fmt(10 * kk)}" fill="{t.shallow_a}"/>',
             "Tints · under 5, 10"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy)}h{E.fmt(8 * kk)}M{E.fmt(cx + 4 * kk)} {E.fmt(cy)}h{E.fmt(8 * kk)}", S("LINE", t.ink2, 0.7))
             + self.txt("10", cx, cy + 3.5, "contour-figure", anchor="middle", fill=t.ink2, semantic=False), "Contours · 5 10 20 50"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy)}h{E.fmt(24 * kk)}", S("PEN", t.ink2, 0.7, "APPROX")), "Approximate contour"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy)}h{E.fmt(24 * kk)}", S("PEN", ink, 0.9, "RESTRICT", caps="butt"))
             + line(f"M{E.fmt(cx - 8 * kk)} {E.fmt(cy)}v{E.fmt(3 * kk)}M{E.fmt(cx)} {E.fmt(cy)}v{E.fmt(3 * kk)}M{E.fmt(cx + 8 * kk)} {E.fmt(cy)}v{E.fmt(3 * kk)}",
                    S("PEN", ink, 0.9, caps="butt")), "Restricted · robots.txt"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy)}h{E.fmt(24 * kk)}", S("HAIR", ink, 0.55, "TRACK", caps="butt")), "Track line · one shard"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx)} {E.fmt(cy - 7 * kk)}v{E.fmt(14 * kk)}", S("HAIR", ink, 0.35, "TRACK", caps="butt")), "Check line · dedup"),
            (lambda cx, cy, kk: self.hatch_swatch(cx, cy, kk), "Hatch · unsurveyed"),
            (lambda cx, cy, kk: line(f"M{E.fmt(cx - 12 * kk)} {E.fmt(cy + 2 * kk)}L{E.fmt(cx - 4 * kk)} {E.fmt(cy - 2 * kk)}L{E.fmt(cx + 4 * kk)} {E.fmt(cy + 2 * kk)}L{E.fmt(cx + 12 * kk)} {E.fmt(cy - 2 * kk)}",
                                     S("PEN", ink, 0.85, "LIMIT", caps="butt")), "Limit of survey"),
            (lambda cx, cy, kk: (self.snd(commits, cx, cy + 4 * kk, sub=months, truth="measured", role="label")
                                 if commits and months else self.snd(4, cx, cy + 4 * kk, sub=2, truth="illustrative", role="label")),
             "Height · commits, months" if commits and months else "Sounding · 1000s, 100s"),
            (lambda cx, cy, kk: self.snd(4, cx, cy + 4 * kk, sub=2, truth="illustrative", role="label"), "Sounding · 1000s, 100s"),
            (lambda cx, cy, kk: (self.snd(hw["n"], cx, cy + 4 * kk, sub=hw.get("days", 0), truth="measured", role="label")
                                 if hw else self.snd(108, cx, cy + 4 * kk, sub=4, truth="illustrative", role="label")),
             "Sheet 1 · week's commits, days"),
        ]

    def draw_legend(self):
        x, y, w, h = LEGEND
        Pn = self.layers["panels"]
        Pn.append(self.cartouche(x, y, w, h, "legend"))
        Pn.append(self.header(self.fit(f"SYMBOLS · CHART NO. {self.repo_count} · EVERY SHEET", "label", 600, size=PANEL_SIZE),
                              x + 14, y + 22, within=LEGEND, size=PANEL_SIZE))
        Pn.append(self.body("upright figures are measured · sloping figures are not · underlined: above datum", x + 14, y + 44,
                            within=LEGEND))
        rows = self.legend_rows()
        ncol = 4
        per = math.ceil(len(rows) / ncol)
        col_w = (w - 28) / ncol
        avail = col_w - 54
        y0, pitch = y + 66, 18.3
        kk = 1.3
        for i, (draw, text) in enumerate(rows):
            ci, ri = divmod(i, per)
            cx0 = x + 14 + ci * col_w
            cy = y0 + ri * pitch
            Pn.append(draw(cx0 + 18, cy - 5, kk))
            Pn.append(self.body(self.fit(text, "label", avail, size=PANEL_SIZE), cx0 + 48, cy, within=LEGEND))

    def draw_phone_legend(self):
        """A compact legend of the symbols the phone sheet actually carries, below the chart."""
        t = self.t
        Pn = self.layers["panels"]
        x, y, w = 55, PH_LEGEND_Y, 610
        short = {"Rep · reported, not found": "Rep · not found", "Anchorage · Delta Lake": "Anchorage · Delta L."}
        Pn.append(self.txt("SYMBOLS", x, y + 26, "label", tracking=1.0))
        Pn.append(self.txt("upright figures measured · sloping not", x + 140, y + 26, "label"))
        rows = [r for r in self.legend_rows() if r[1].split(" ·")[0] in
                ("G can", "R nun", "Light", "Ldg line", "Anchorage", "Wk", "Rep", "ED", "SD",
                 "Danger line", "Restricted", "Limit of survey")]
        per = math.ceil(len(rows) / 2)
        col_w = w / 2
        y0, pitch, kk = y + 70, 34, 1.9
        for i, (draw, text) in enumerate(rows):
            ci, ri = divmod(i, per)
            cx0 = x + ci * col_w
            cy = y0 + ri * pitch
            Pn.append(draw(cx0 + 24, cy - 8, kk))
            Pn.append(self.txt(self.fit(short.get(text, text), "label", col_w - 58), cx0 + 56, cy, "label"))
        self.exclude("phone-legend", x - 4, y, w + 8, 70 + per * pitch)

    def lamps(self, cx, cy, kk=1.0) -> str:
        t = self.t
        out = []
        for i, st in enumerate([(t.ok, t.ok, t.ok), (t.accent, t.accent, t.accent), (t.ok, t.paper, t.ok)]):
            x = cx - 10 * kk + i * 10 * kk
            for j, col in enumerate(st):
                out.append(f'<circle cx="{E.fmt(x)}" cy="{E.fmt(cy - 5 * kk + j * 5 * kk)}" r="{E.fmt(2 * kk)}" fill="{col}" '
                           f'{self.stroke("HAIR", t.ink, 0.9)}/>')
        return "".join(out)

    def hatch_swatch(self, cx, cy, kk=1.0) -> str:
        w, h = 24 * kk, 12 * kk
        d, b = c.hatch((cx - w / 2, cy - h / 2, w, h), self.t, self.jit.sub("legend-hatch"), "unsurveyed", "hatch-legend", spacing=5 * kk)
        self.defs.append(d)
        return (f'<g opacity=".35">{b}</g>' if self.night else b) + \
            f'<rect x="{E.fmt(cx - w / 2)}" y="{E.fmt(cy - h / 2)}" width="{E.fmt(w)}" height="{E.fmt(h)}" fill="none" {self.stroke("HAIR", self.t.ink, 0.6, caps="butt")}/>'

    # ---------------------------------------------------------------- frame and margin
    def draw_frame(self):
        t = self.t
        F, Mg = self.layers["frame"], self.layers["margin"]
        unit = self.cfg["copy"]["unit_approaches"]
        if self.phone:
            F.append(c.frame(self.w, self.h, t, "minute-bars", rules=self.rules))
            Mg.append(self.txt(unit, 340, 42, "label-caps", anchor="middle", fill=t.ink))
            Mg.append(self.txt(str(self.repo_count), 670, 42, "label", anchor="end", key="chart-number", truth="measured"))
            Mg.append(self.txt(f"CHART NO. {self.repo_count} · SHEET 3", 50, self.h - 14, "label", key="folio"))
            ax, ay = 70, self.P(0, 0)[1] - 30             # north arrow pointing left: the sheet is oriented to the channel
            Mg.append(f'<path d="M{ax + 44} {E.fmt(ay)}H{ax}M{ax + 12} {E.fmt(ay - 7)}L{ax} {E.fmt(ay)}L{ax + 12} {E.fmt(ay + 7)}" fill="none" {self.stroke("PEN", t.ink, 0.9)}/>')
            Mg.append(self.txt("N", ax + 56, ay + 9, "label"))
            self.exclude("north", ax - 6, ay - 14, 110, 28)
        else:
            F.append(c.frame(self.w, self.h, t, "broken", gaps=[("right", _y(300), _y(300) + 24), ("right", _y(560), _y(560) + 24)],
                             rules=self.rules))
            Mg.append(self.txt(unit, 640, 12, "label-caps", anchor="middle", fill=t.ink))
            Mg.append(self.txt(str(self.repo_count), 1262, 14, "label", anchor="end", key="chart-number", truth="measured"))
            Mg.append(self.txt(f"CHART NO. {self.repo_count} · SHEET 3 · APPROACHES TO SCRAPY HARBOR", 24, self.h - 5, "label", key="folio"))

    # ---------------------------------------------------------------- assemble
    def render(self) -> str:
        self.defs.append(c.symbol_defs(self.t, PREFIX, self.ed.name))
        self.build_field()
        self.draw_paper()
        self.draw_water()
        self.draw_limit_and_zones()
        self.draw_survey_ground()
        self.draw_channel()
        self.draw_harbour()
        self.draw_title_block()
        if not self.phone:
            self.draw_zoc()
            self.draw_blocks()
            self.draw_legend()
        else:
            self.draw_phone_legend()
        self.draw_frame()
        self.draw_vessels()
        self.draw_contour_figures()
        self.draw_soundings()
        body = "".join("".join(self.layers[n]) for n in
                       ("paper", "water", "soundings", "lines", "marks", "panels", "frame", "margin"))
        defs = "".join(self.defs) + k.glyph_defs()
        self.ctx.extra["symbols_used"] = sorted(self.symbols_used)
        self.ctx.extra["legend"] = sorted(self.legend_ids)
        self.ctx.extra["lights"] = self.lights
        self.ctx.extra["shards"] = self.shards
        return E.svg(self.ed, self.w, self.h, body, defs, sheet=NAME)


def build(ctx) -> str:
    return _Sheet(ctx).render()


def alt(data, cfg) -> str:
    return ("Sheet 3, Approaches: rustmapper's survey ground east, buoyed channel west into Scrapy Harbor, "
            "every symbol in the legend. The soundings fill in behind the vessel.")


# ------------------------------------------------------------------ build-report hook
def _report(ctx, svg_text: str, entry: dict) -> None:
    if getattr(ctx, "sheet", None) != NAME:
        return
    ex = ctx.extra or {}
    entry["symbols_used"] = ex.get("symbols_used", [])
    entry["legend"] = ex.get("legend", [])
    entry["lights"] = ex.get("lights", [])
    entry["approaches"] = {"shards": ex.get("shards"), "soundings": ex.get("soundings"), "field": ex.get("field_report")}


def _register_hook() -> None:
    """build_assets may be imported as `build_assets` or be running as `__main__`: feed both lists."""
    for modname in ("build_assets", "__main__"):
        hooks = getattr(sys.modules.get(modname), "report_hooks", None)
        if isinstance(hooks, list) and _report not in hooks:
            hooks.append(_report)


_register_hook()
