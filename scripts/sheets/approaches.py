"""approaches — Sheet 3, "Approaches to Scrapy Harbor" (T3; MASTERPLAN decisions 1, 5, 14, 20, 21).

The harbour chart of the two systems. Harbour to the WEST (land x ≤ ~220), a buoyed Region B
channel on a final leading-line leg of 290° true (the hero's bearing), rustmapper's survey ground
to the EAST (one track line per frontier shard), the limit of survey and the unsurveyed hatch at the
east edge. The rustmapper → Scrapy link is charted as a *proposed, unlit* channel (pecked, hollow
marks): nothing runs it. Zones of Confidence, the harbour inset, two title blocks and THE LEGEND,
which defines every symbol id in chartlib.symbol_defs so the legend ↔ sheet <use> diff is empty on
every sheet of the chart.

Honesty: every figure on the water is illustrative (italic, sloping). Upright figures are only the
chart number, the PyPI version and date, Scrapy's commit count, the light character and the one
legend example drawn from stats.json. "512" is never printed. Shards = log.json.profile.shards,
italic until `measured`. No coverage figure.

Motion (§2.1, all discrete): G "1"/G "3" Fl G 4s (begin 0), R "2"/R "4" Fl R 4s (begin 2), Grafana Lt
Fl {scrape_interval}s, the packet boat plotted by 7 fixes at 0, 4 … 24 s then held to 96 s; the
survey vessel plots 8 fixes on the last track line at 28, 30 … 42 s and sounding k and WAL cell k
<set> at fix k. Still edition = the finished sheet. Phone edition: the geography rotated 90°
anticlockwise (channel down the screen, north arrow pointing left), re-lettered at SCALE_PHONE,
frozen.
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

try:
    import build_assets as _BA  # noqa: E402
except Exception:  # pragma: no cover — the sheet can be imported without the runner
    _BA = None

NAME = "approaches"
KIND = "chart"
SIZES = {"desk": (1280, 960), "phone": (720, 1240)}
BREAKS: list[tuple[str, str, str]] = [
    ("Panel headers are set in role `label` with caps and +0.6 tracking, not `label-caps`",
     "the one `label-caps` run per sheet is the unit line outside the neat line; NOTES / ZONES OF CONFIDENCE / "
     "SYMBOLS headers are structural captions inside cartouches",
     "T5's rule guards the sheet caption; a chart's notes panels are headed in small tracked caps (NOAA 1980–2000)"),
    ("The channel centreline from W1 inward is the leading line, not a pecked course",
     "COURSE dots run W0→W1 only; from W1 to the anchorage the solid-then-pecked Ldg line carries the waypoints",
     "the four inner legs are collinear on 290° by decision 1, and two line styles on one line would be noise"),
    ("The inset is not a true enlargement of the field's basin",
     "the inset header says 'the harbour works', not a scale",
     "the basins are the three Delta tables drawn as a harbour; the main-sheet basin comes from the field"),
    ("Phone edition is rotated 90° anticlockwise, with neat-line rules at 26/31 instead of 14/19",
     "point mapper P(x, y) → (y, 1260 − x) with a north arrow pointing left; the wider margin holds the 26 px folio",
     "a 720×1240 sheet reads the channel down the screen (T3 §6); charts oriented to the channel carry a north arrow"),
]

PREFIX = "c"          # symbol ids c-sym-<name>; edition.svg prefixes approaches-
SEED = 27

# ------------------------------------------------------------------ geography (1280 × 960 desk space)
W_DESK, H_DESK = SIZES["desk"]
RULES = {"desk": (14, 19), "phone": (26, 31)}
BASE = 26.0                                   # open water where nothing is sampled (never on a level)
H_SND = 110.0                                 # sounding kernel support: samples ~95 px apart must overlap
LEVELS = (0.0, 2.0, 5.0, 10.0, 20.0)
INDEX_LEVELS = (10.0,)
ANCH = (150, 440)
LDG_BRG = 290.0                               # true, the hero's final leg (decision 1)
_DIR = (math.sin(math.radians(LDG_BRG - 180)), -math.cos(math.radians(LDG_BRG - 180)))   # seaward unit (110°)


def _along(d: float) -> tuple[int, int]:
    return (E.I(ANCH[0] + _DIR[0] * d), E.I(ANCH[1] + _DIR[1] * d))


W4, W3, W2, W1 = _along(91), _along(181), _along(258), _along(383)
W0 = (600, 672)
COURSE = [W0, W1, W2, W3, W4, ANCH]
LDG_FRONT, LDG_REAR = _along(-52), _along(-100)
GRAFANA = (178, 200)
SHOAL = (478, 652)
SHOAL_R = 26
WRECK = (560, 400)
SURVEY = (680, 120, 400, 570)                 # the survey ground
RESTRICTED = [(900, 300), (1060, 300), (1060, 420), (900, 420)]
LIMIT_X = 1096
BAND = (LIMIT_X, 20, 1260 - LIMIT_X, 680)
UNSURVEYED_FADE = (1080, 1150)
ZONE_Y = {"A": 215, "B": 405, "C": 595}
REP, ED_, SD = (760, 210), (980, 480), (846, 596)

# bottom strip
STRIP_Y = 702
BLOCK_RM = (36, STRIP_Y, 312, 232)
LEGEND = (360, STRIP_Y, 560, 232)
BLOCK_SH = (932, STRIP_Y, 312, 232)
TITLE_C = (470, 50)
ZOC = (680, 26, 400, 86)
INSET = (326, 146, 330, 236)

LAND = [(60, 130, 230, 70), (40, 330, 220, 70), (50, 560, 230, 70), (50, 720, 230, 70),
        (170, 200, 80, 42), (40, 60, 120, 45), (40, 760, 130, 45),
        (125, 446, 150, 46),                   # the harbour's own land
        (196, 398, 48, 52), (196, 500, 48, 52)]  # the two entrance points
CARVE = [(150, 446, 46, -92), (200, 452, 36, -58)]
ACRONYMS = {"CT LOGS": "CT logs", "SITEMAPS": "sitemaps", "COMMON CRAWL": "Common Crawl"}
ZONE_TEXT = {"A": "existence doubtful", "B": "exists, may not answer", "C": "as reported"}


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
    """The designed depth (URLs, thousands) the illustrative soundings are sampled from: a shelf
    deepening with distance from the shore, a deeper fairway along the course, a shallower bank
    north of the channel."""
    d = 2.5 + _shore_distance(x, y) * 0.05
    fair = c.dist_to_polyline(x, y, COURSE)
    d += 5.0 * math.exp(-(fair / 48.0) ** 2)
    if x < 520 and y < 420:
        d -= 1.5 * smoothstep((420 - y) / 120) * smoothstep((520 - x) / 150)
    return max(3.0, min(48.0, d))


def _samples(jit: c.Jitter) -> list[tuple[float, float, float]]:
    out = []
    g = jit.sub("samples")
    for gy in range(60, 700, 92):
        for gx in range(250, 1090, 96):
            x, y = gx + g.offset(18), gy + g.offset(18)
            if x < 232 or x > 1076:
                continue
            if math.hypot(x - SHOAL[0], y - SHOAL[1]) < 70:
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
        # phone mapper: rotate 90° anticlockwise, east to the top, north to the left
        self.s = (SIZES["phone"][1] - 40) / 1240.0 if self.phone else 1.0
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
        return (round(20 + (y - 20) * self.s, 1), round(20 + (1260 - x) * self.s, 1))

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
        self.symbols_used.add(f"{PREFIX}-sym-{name}")
        return c.use(name, x, y, PREFIX, scale=scale, rotate=rotate, extra=extra)

    def use_legend(self, name, x, y, scale=1.0, rotate=0) -> str:
        self.legend_ids.add(f"{PREFIX}-sym-{name}")
        return c.use(name, x, y, PREFIX, scale=scale, rotate=rotate)

    def stroke(self, *a, **kw) -> str:
        return c.stroke(*a, **kw)

    def exclude(self, name, x, y, w, h):
        k.exclude(name, x, y, w, h)
        self.extra_excl.append((x, y, w, h))

    def cartouche(self, x, y, w, h, name, shadow=False) -> str:
        out = []
        if shadow:
            out.append(f'<rect x="{E.I(x + 6)}" y="{E.I(y + 6)}" width="{E.I(w)}" height="{E.I(h)}" fill="{self.t.paper}" '
                       f'{self.stroke("HAIR", self.t.ink, 0.5, caps="butt")}/>')
        out.append(f'<rect x="{E.I(x)}" y="{E.I(y)}" width="{E.I(w)}" height="{E.I(h)}" fill="{self.t.paper}" '
                   f'{self.stroke("HAIR", self.t.ink, 0.85, caps="butt")}/>')
        self.exclude(name, x - 4, y - 4, w + 8, h + 8)
        return "".join(out)

    def light_group(self, x, y, lit_id, character, begin, color=None, r=2.0) -> str:
        """A flashing core (+ halo at night) whose group opacity takes the light's character."""
        anim = self.tl.flash(character, begin=begin, still="lit", name=f"{lit_id}-fl") if self.tl.motion else ""
        core = c.lit_core(x, y, self.t, lit_id, r=r, halo_r=(14 if self.night else None), prefix=PREFIX, color=color)
        self.lights.append({"id": lit_id, "character": character, "color": color or self.t.light_core,
                            "bbox": [E.I(x - 14), E.I(y - 14), 28, 28]})
        return f"<g>{anim}{core}</g>"

    # ---------------------------------------------------------------- the field
    def build_field(self):
        jit = self.jit
        samples_d = _samples(jit)
        if not self.phone:
            coast = _Coast((6, 20, 1254, 680), {"l": 6, "r": 24, "t": 24, "b": 24}, ("x",) + UNSURVEYED_FADE)
            samples = samples_d
            extra = LAND + CARVE
            feats = [c.Feature("429 Shoal", 0, "shoal", SHOAL[0], SHOAL[1], r=SHOAL_R)]
            w, h = W_DESK, H_DESK
            h_snd = H_SND
        else:
            s = self.s
            fa, fb = (self.P(UNSURVEYED_FADE[0], 0)[1], self.P(UNSURVEYED_FADE[1], 0)[1])
            coast = _Coast((20, 20, 680, 1234), {"l": 24, "r": 24, "t": 24, "b": 6}, ("y", fa, fb))
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

    def draw_water(self):
        t, jit, cs = self.t, self.jit, self.cs
        W = self.layers["water"]
        r1 = self.rules[1]
        neat = (r1, r1, self.w - 2 * r1, self.h - 2 * r1)
        self.defs.append(f'<clipPath id="neat"><rect x="{neat[0]}" y="{neat[1]}" width="{neat[2]}" height="{neat[3]}"/></clipPath>')
        W.append('<g clip-path="url(#neat)">')
        W.append(c.tint_bands(cs, t, levels=(10.0, 5.0)))
        W.append(c.coastline(cs, t, swell=not self.night))
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
            excl = [ZOC, INSET, (TITLE_C[0] - 190, 30, 380, 90), (LIMIT_X - 10, 20, 180, 680), SURVEY]
            self.breaks = c.contour_labels(cs, min_len=220, gap=18, exclusions=excl, levels=(5.0, 10.0, 20.0))
            approx = (UNSURVEYED_FADE[0] - 40, 20, LIMIT_X - UNSURVEYED_FADE[0] + 40, 680)
            W.append(c.draw_contours(cs, INDEX_LEVELS, t, approx_clip=approx, breaks=self.breaks, opacity=op, min_len=60))
        # the unsurveyed hatch, running to the sheet edge where the neat line is broken
        band = self.Prect(*BAND)
        ramp = None if self.phone else (band[0], band[0] + 40)
        hd, hb = c.hatch(band, t, jit.sub("band"), "unsurveyed", "hatch-band", ramp=ramp)
        self.defs.append(hd)
        W.append(f'<g opacity=".35">{hb}</g>' if self.night else hb)
        W.append("</g>")   # end neat clip
        if not self.phone:
            for y0, y1 in ((300, 324), (560, 584)):
                hd2, hb2 = c.hatch((1259, y0, 21, y1 - y0), t, jit.sub(f"gap{y0}"), "unsurveyed", f"hatch-gap{y0}")
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
        y = 20
        while y <= 700:
            pts.append((LIMIT_X + g.offset(6), y))
            y += 48
        pts.append((LIMIT_X + g.offset(6), 700))
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
            lx, ly = self.P(LIMIT_X, 20)
            M.append(self.txt(limit_label, lx + 10, ly - 10, "label"))
            M.append(self.txt("UNSURVEYED", 690, ly - 10, "label", anchor="end", tracking=2.0, fill=t.unsurveyed))
        else:
            M.append(self.txt(limit_label, LIMIT_X + 10, 560, "label", anchor="middle", rotate=-90))
            M.append(self.txt("UNSURVEYED", 1182, 420, "label", anchor="middle", rotate=-90, tracking=2.0, fill=t.unsurveyed))

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
            x, y = self.P(980, 360)
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
            self.symbols_used.add(f"{PREFIX}-sym-{'rep' if kind == 'Rep' else 'ed'}")
            self.extra_excl.append((px - 12, py - 12, 50, 24))
        sx, sy = self.P(*SD)
        if self.phone:
            sx, sy = self.P(SD[0], SD[1] - 40)      # clear of the last track line's fixes after the rotation
            M.append(c.doubt("SD", sx, sy, self.lbl, PREFIX))
        else:
            M.append(self.snd(E.I(self.field.value(*SD)), sx, sy + 4, truth="illustrative"))
            M.append(c.doubt("SD", sx + 10, sy, self.lbl, PREFIX))
            self.extra_excl.append((sx - 14, sy - 10, 48, 18))
            # pencil note with a leader to the Rep ring: between track lines 1 and 2
            nx, ny = 704, 234
            M.append(self.txt("sitemap says yes; the lead says no", nx, ny, "note", fill=self.t.muted, rotate=-6, opacity=0.9))
            M.append(f'<path d="M{nx - 4} {ny - 12}Q{nx + 10} {ny - 30} {REP[0] - 8} {REP[1] + 4}" fill="none" '
                     f'{self.stroke("HAIR", self.t.muted, 0.8)}/>')

    def draw_channel(self):
        t, jit = self.t, self.jit
        L, M = self.layers["lines"], self.layers["marks"]
        P = self.P
        # outer leg: pecked course with waypoints
        L.append(c.course(self.Ppts([W0, W1]), t, jit, pecked=True, prefix=PREFIX, bearings=False))
        self.symbols_used.add(f"{PREFIX}-sym-waypoint")
        # the leading line: solid from the front mark to W3, pecked beyond to W1
        f, w3, w1 = P(*LDG_FRONT), P(*W3), P(*W1)
        L.append(f'<path d="M{E.fmt(f[0])} {E.fmt(f[1])}L{E.fmt(w3[0])} {E.fmt(w3[1])}" fill="none" {self.stroke("PEN", t.ink, 0.8)}/>')
        L.append(f'<path d="M{E.fmt(w3[0])} {E.fmt(w3[1])}L{E.fmt(w1[0])} {E.fmt(w1[1])}" fill="none" '
                 f'{self.stroke("PEN", t.ink, 0.8, "PECK", caps="butt")}/>')
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
        # lateral marks, Region B, returning heading ~290°–318°: starboard = north
        legs = [(W0, W1), (W1, W2), (W2, W3), (W3, W4)]
        marks = [("can", 1, "URLS", "port", "Fl G 4s", 0.0),
                 ("nun", 2, "SCOUT", "starboard", "Fl R 4s", 2.0),
                 ("can", 3, "ANALYZE", "port", "Fl G 4s", 0.0),
                 ("nun", 4, "SUMMARIZE", "starboard", "Fl R 4s", 2.0)]
        self.mark_pts = []
        for leg, (kind, num, stage, side, char, begin) in zip(legs, marks):
            mx, my = c.lateral_offset(leg, 0.5, side, 24)
            self.mark_pts.append((mx, my))
            x, y = P(mx, my)
            M.append(self.use(kind, x, y))
            top = y - 15 if kind == "can" else y - 16
            core = t.ok if kind == "can" else t.accent
            M.append(self.light_group(x, top, f"lt-{'g' if kind == 'can' else 'r'}{num}", char, begin,
                                      color=(core if self.night else None)))
            letter = "G" if kind == "can" else "R"
            if self.phone:
                # after the rotation north (starboard) is to the LEFT of the channel, south to the right
                if side == "starboard":
                    M.append(self.txt(f'{letter} "{num}"', x - 18, y + 2, "label-italic", anchor="end"))
                else:
                    M.append(self.txt(f'{letter} "{num}"', x + 18, y + 2, "label-italic"))
            elif side == "starboard":           # north: label above
                M.append(self.txt(f'{letter} "{num}" {stage}', x + 8, y - 22, "label-italic"))
                M.append(self.txt(char, x + 8, y - 8, "label-italic"))
            else:                               # south: label below
                M.append(self.txt(f'{letter} "{num}" {stage}', x + 6, y + 14, "label-italic"))
                M.append(self.txt(char, x + 6, y + 28, "label-italic"))
        # bearings: the outer leg, and the leading line labelled once, south of the W1–W2 leg
        if not self.phone:
            b0 = c.compass_bearing(W0, W1)
            M.append(self.txt(f"{round(b0) % 360:03d}°", (W0[0] + W1[0]) / 2 + 16, (W0[1] + W1[1]) / 2 + 4, "label"))
            M.append(self.txt(f"Health Ldg Lts {LDG_BRG:.0f}°", (W1[0] + W2[0]) / 2 + 4, (W1[1] + W2[1]) / 2 + 30, "label",
                              anchor="middle"))
        else:
            lx, ly = P((W2[0] + W3[0]) / 2, (W2[1] + W3[1]) / 2)
            M.append(self.txt(f"Ldg {LDG_BRG:.0f}°", lx - 34, ly + 9, "label", anchor="end"))
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
            hx, hy = P(110, 206)
            M.append(self.txt("SCRAPY HARBOR", hx, hy, "title", anchor="middle"))
            dx, dy = P(ANCH[0] - 40, ANCH[1] + 36)
            M.append(self.txt("Delta Lake", dx, dy, "place-water", anchor="middle"))
            sx, sy = P(*SHOAL)
            M.append(self.txt("429 Shoal", sx, sy + 62, "place-water", anchor="middle"))
        else:
            M.append(self.txt("SCRAPY", 96, 300, "title", anchor="middle"))
            M.append(self.txt("HARBOR", 96, 332, "title", anchor="middle"))
            M.append(self.txt("Delta Lake", ANCH[0], ANCH[1] + 44, "place-water", anchor="middle"))
            M.append(self.txt("429 Shoal", SHOAL[0], SHOAL[1] - 40, "place-water", anchor="middle"))
            M.append(self.txt("Local knowledge advised · see Notices 1–5", 232, 688, "label"))
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

    def hollow_mark(self, kind, x, y) -> str:
        d = "M-5.5 0v-13h11v13z" if kind == "can" else "M-6 0L6 0L0 -14Z"
        return (f'<g transform="translate({E.fmt(x)} {E.fmt(y)})"><g transform="rotate(8)">'
                f'<path d="{d}" fill="none" {self.stroke("PEN", self.t.ink, 0.8)}/></g>'
                f'<circle r="1.2" fill="{self.t.paper}" {self.stroke("PEN", self.t.ink)}/></g>')

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
        # WAL cell k appear at fix k (the soundings fill in behind the vessel)
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
            for seg in self.track_segs[:-1]:            # six per line, none on the last (the vessel sounds it)
                y = seg[0][1]
                for j in range(6):
                    pts.append((722 + j * 60, y - 7, "survey"))
            g = self.jit.sub("snd")
            for i in range(1, 200):
                x = 230 + c.halton(i, 2) * (LIMIT_X - 24 - 230)
                y = 36 + c.halton(i, 3) * (690 - 36)
                pts.append((x + g.offset(4), y + g.offset(4), "water"))
        else:
            g = self.jit.sub("snd-phone")
            for i in range(1, 160):
                x = 232 + c.halton(i, 2) * (LIMIT_X - 30 - 232)
                y = 40 + c.halton(i, 3) * 650
                pts.append((x + g.offset(6), y + g.offset(6), "water"))
        placed: list[tuple[float, float]] = []
        min_gap = 36 if not self.phone else 60
        budget = 64 if not self.phone else 14
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
            if rx0 - 8 <= x <= rx1 + 8 and ry0 - 8 <= y <= ry1 + 8:
                continue
            px, py = self.P(x, y)
            if any(math.hypot(px - qx, py - qy) < min_gap for qx, qy in placed):
                continue
            bw, bh = (22, 12) if not self.phone else (36, 20)
            box = (px - bw / 2 - 2, py - bh - 2, bw + 4, bh + 4)
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
    def header(self, s, x, y, within=None, anchor="start") -> str:
        return self.txt(s, x, y, "label", tracking=0.6, within=within, anchor=anchor)

    def draw_title_block(self):
        if self.phone:
            # a paper cartouche over the quiet (unsurveyed) water at the top of the sheet
            x, y, w, h = 70, 40, 580, 84
            Pn = self.layers["panels"]
            Pn.append(self.cartouche(x, y, w, h, "title"))
            Pn.append(self.txt("Approaches to Scrapy Harbor", x + w / 2, y + 38, "title", anchor="middle"))
            Pn.append(self.txt("Surveyed by rustmapper · Datum: main", x + w / 2, y + 70, "label", anchor="middle"))
            return
        cx, cy = TITLE_C
        M = self.layers["panels"]
        M.append(self.header("SHEET 3", cx, cy + 6, anchor="middle"))
        M.append(self.txt("Approaches to Scrapy Harbor", cx, cy + 36, "title", anchor="middle"))
        M.append(self.txt("Surveyed by rustmapper 2026 · Datum: main", cx, cy + 56, "label", anchor="middle"))
        M.append(f'<path d="M{cx - 60} {cy + 66}h120" fill="none" {self.stroke("HAIR", self.t.ink, 0.6, caps="butt")}/>')
        self.exclude("title-block", cx - 190, cy - 8, 380, 78)

    def draw_zoc(self):
        x, y, w, h = ZOC
        t = self.t
        Pn = self.layers["panels"]
        Pn.append(self.cartouche(x, y, w, h, "zoc"))
        Pn.append(self.header("ZONES OF CONFIDENCE", x + 12, y + 16, within=ZOC))
        zones = [c.Zone("A", [(0, 0), (1, 0), (1, 1 / 3), (0, 1 / 3)], 0.9),
                 c.Zone("B", [(0, 1 / 3), (1, 1 / 3), (1, 2 / 3), (0, 2 / 3)], 0.5),
                 c.Zone("C", [(0, 2 / 3), (1, 2 / 3), (1, 1), (0, 1)], 0.2)]
        Pn.append(c.source_diagram(x + 12, y + 24, 96, 54, zones, t, self.jit, self.lbl))
        sources = self.data.get("sources") or self.cfg.get("sources") or []
        names = {s.get("letter"): ACRONYMS.get(str(s.get("name", "")).upper(), str(s.get("name", "")).lower()) for s in sources}
        tx = x + 124
        for i, letter in enumerate(("A", "B", "C")):
            Pn.append(self.txt(f"{letter}  {names.get(letter, '')} · {ZONE_TEXT[letter]}", tx, y + 34 + i * 16, "label", within=ZOC))
        Pn.append(self.txt("A: as declared by the site.  B, C: as found.", tx, y + 78, "label", within=ZOC))

    def draw_inset(self):
        x, y, w, h = INSET
        t = self.t
        Pn = self.layers["panels"]
        Pn.append(self.cartouche(x, y, w, h, "inset", shadow=True))
        Pn.append(f'<path d="M{x} {y + h}L{W4[0] - 6} {W4[1] - 12}" fill="none" {self.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
        Pn.append(self.header("INSET · THE HARBOUR WORKS", x + 10, y + 16, within=INSET))
        ox, oy = x, y + 22          # content origin (u, v) → (ox + u, oy + v), 330 × 214
        U = lambda u, v: (ox + u, oy + v)  # noqa: E731
        Pn.append(f'<rect x="{x + 1}" y="{oy}" width="{w - 2}" height="{h - 23}" fill="{t.land}"/>')
        # three basins: outer stage1_discovery (deepest, raw, open to seaward at the right edge), a sill,
        # inner stage2_page_analysis, a sill, the dock stage4_summaries
        outer = [(330, 58), (330, 150), (240, 160), (156, 156), (118, 134), (112, 100), (134, 68), (200, 54), (270, 48)]
        inner = [(122, 128), (112, 110), (80, 112), (44, 120), (34, 142), (50, 164), (86, 172), (116, 160), (128, 146)]
        dock = [(66, 118), (50, 108), (32, 92), (36, 70), (56, 60), (78, 66), (86, 86), (84, 108)]
        for poly, fill in ((outer, t.paper), (inner, t.shallow_a), (dock, t.shallow_b)):
            pts = [U(u, v) for u, v in poly]
            Pn.append(f'<path d="{c.smooth_path(pts, True, 1)}" fill="{fill}" {self.stroke("LINE", t.ink2)}/>')
        depth = {"stage1_discovery": (24, 4), "stage2_page_analysis": (8, 2), "stage4_summaries": (4, 1)}
        truth = "illustrative"
        if isinstance(self.trial, dict) and isinstance(self.trial.get("tables"), dict):
            truth = "measured"
            for name, tb in self.trial["tables"].items():
                rows = int(tb.get("rows", 0))
                depth[name] = (rows // 1000, (rows % 1000) // 100)
        W = lambda s, avail, role="label": self.fit(s, role, avail)  # noqa: E731
        Pn.append(self.snd(depth["stage1_discovery"][0], *U(224, 104), sub=depth["stage1_discovery"][1], truth=truth, role="label"))
        Pn.append(self.txt(W("stage1_discovery", 150), *U(224, 122), "label", anchor="middle", within=INSET))
        Pn.append(self.txt("Delta Lake", *U(224, 148), "place-water", anchor="middle"))
        Pn.append(self.use("anchorage", *U(166, 100)))
        Pn.append(self.snd(depth["stage2_page_analysis"][0], *U(82, 146), sub=depth["stage2_page_analysis"][1], truth=truth, role="label"))
        Pn.append(self.txt(W("stage2_page_analysis", 150), *U(84, 198), "label", anchor="middle", within=INSET))
        Pn.append(self.snd(depth["stage4_summaries"][0], *U(60, 92), sub=depth["stage4_summaries"][1], truth=truth, role="label"))
        Pn.append(self.txt(W("stage4_summaries", 120), *U(10, 52), "label", within=INSET))
        q = lambda u, v, pw, ph: (f'<rect x="{ox + u}" y="{oy + v}" width="{pw}" height="{ph}" fill="{t.paper}" '  # noqa: E731
                                   f'{self.stroke("PEN", t.ink)}/>')
        # the works on the land: Prometheus mast, PostgreSQL tanks, Grafana Lt tower (lantern on the main
        # light's character) with its horn, Redis twin tanks, the traffic signal beside them, the BART shed
        Pn.append(f'<path d="M{ox + 22} {oy + 32}V{oy + 8}M{ox + 18} {oy + 14}h8M{ox + 19} {oy + 21}h6" fill="none" {self.stroke("PEN", t.ink)}/>')
        Pn.append(self.txt("Prometheus", *U(30, 30), "label", within=INSET))
        Pn.append(q(104, 12, 14, 10) + q(104, 24, 14, 10))
        Pn.append(self.txt(W("PostgreSQL · metrics", 120), *U(124, 30), "label", within=INSET))
        tx0, ty0 = U(306, 56)
        Pn.append(f'<path d="M{tx0 - 3} {ty0}L{tx0 - 2} {ty0 - 20}h4L{tx0 + 3} {ty0}Z" fill="{t.paper}" {self.stroke("PEN", t.ink)}/>')
        Pn.append(self.use("light", tx0, ty0 - 23, scale=0.8))
        Pn.append(self.light_group(tx0, ty0 - 23, "lt-grafana-inset", f"Fl {self.scrape}s" if self.scrape else "F", 0.0, r=1.3))
        Pn.append(self.use("horn", tx0, ty0 - 23, scale=0.8))
        Pn.append(self.txt("Grafana Lt", tx0 - 12, ty0 - 24, "label", anchor="end", within=INSET))
        Pn.append(q(298, 166, 10, 10) + q(310, 166, 10, 10))
        Pn.append(self.txt("Redis · queues", *U(292, 176), "label", anchor="end", within=INSET))
        Pn.append(self.use("traffic", *U(312, 208)))
        Pn.append(self.txt("Traffic Sig", *U(302, 208), "label", anchor="end", within=INSET))
        Pn.append(q(150, 180, 24, 12))
        Pn.append(self.txt(W("Summarization Wks", 110), *U(180, 192), "label", within=INSET))
        Pn.append(self.use("ldg", *U(108, 62)) + self.use("ldg", *U(96, 56)))
        self.exclude("inset", x - 4, y - 4, w + 14, h + 14)

    def note_line(self, parts, x, y, within, avail) -> str:
        """A notes line of (role, text) parts on one baseline (italic parts for quoted figures)."""
        total = sum(self.width(s, role) for role, s in parts)
        if total > avail:
            raise ValueError(f"approaches: note {''.join(s for _, s in parts)!r} is {total:.0f} px, cell allows {avail:.0f}")
        out, pen = [], x
        for role, s in parts:
            truth = "illustrative" if role == "label-italic" and any(ch.isdigit() for ch in s) else None
            out.append(self.txt(s, pen, y, role, within=within, truth=truth))
            pen += self.width(s, role)
        return "".join(out)

    def draw_blocks(self):
        t = self.t
        Pn = self.layers["panels"]
        # ---- rustmapper
        x, y, w, h = BLOCK_RM
        avail = w - 32
        Pn.append(self.cartouche(x, y, w, h, "block-rustmapper"))
        Pn.append(self.txt("rustmapper", x + 16, y + 36, "title", within=BLOCK_RM))
        ver, date = str(self.edition_v.get("version") or ""), str(self.edition_v.get("date") or "")
        status = str(self.edition_v.get("status") or "provisional")
        Pn.append(self.txt(self.fit(f"PyPI {ver} · {status} · {date}", "label", avail), x + 16, y + 56, "label", within=BLOCK_RM,
                           truth="measured", key="edition"))
        Pn.append(self.header("NOTES", x + 16, y + 80, within=BLOCK_RM))
        notes = [
            [("label", "1  Frontier hashed by registrable domain")],
            [("label", "2  One shard per core · permits "), ("label-italic", "256–1024")],
            [("label", "3  Sized by redb commit latency · "), ("label-italic", "250 ms")],
            [("label", "4  WAL crc32 · rkyv · checkpoints to redb")],
            [("label", "5  Seeds A · B · C · robots crawl-delay kept")],
        ]
        for i, parts in enumerate(notes):
            Pn.append(self.note_line(parts, x + 16, y + 98 + i * 16, BLOCK_RM, avail))
        # WAL tape: one cell per sounding; the last line's cells appear with the survey vessel's fixes
        n_cells = (self.shards - 1) * 6 + 8
        per_row, cw, ch, gap = 28, 8, 6, 2
        tx, ty = x + 16, y + 186
        rows = math.ceil(n_cells / per_row)
        cells = []
        for i in range(n_cells):
            r, col = divmod(i, per_row)
            cx, cy = tx + col * (cw + gap), ty + r * (ch + gap)
            rect = (f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="{t.ink}" fill-opacity=".8" '
                    f'{self.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
            if i < n_cells - 8:
                cells.append(rect)
            else:
                cells.append(self.tl.reveal(rect, 28.0 + 2 * (i - (n_cells - 8))))
        Pn.append("".join(cells))
        Pn.append(self.txt("write-ahead log · one cell per sounding", tx, ty + rows * (ch + gap) + 12, "label", within=BLOCK_RM))
        # ---- Scrapy Harbor
        x, y, w, h = BLOCK_SH
        Pn.append(self.cartouche(x, y, w, h, "block-scrapy"))
        Pn.append(self.txt("Scrapy Harbor", x + 16, y + 36, "title", within=BLOCK_SH))
        commits = self.scrapy.get("commits")
        head = f"{self.scrapy.get('language') or 'Python'} · edition main · "
        Pn.append(self.txt(head, x + 16, y + 56, "label", within=BLOCK_SH))
        if commits is not None:
            wx = x + 16 + self.width(head)
            cs = f"{int(commits):,}"
            Pn.append(self.txt(cs, wx, y + 56, "label", within=BLOCK_SH, truth="measured", key="scrapy_commits"))
            Pn.append(self.txt(" commits", wx + self.width(cs), y + 56, "label", within=BLOCK_SH))
        Pn.append(self.header("NOTES", x + 16, y + 80, within=BLOCK_SH))
        notes = ["1  Typed Arrow schema per table",
                 "2  schema_mode=merge · partition by domain",
                 "3  Dedup by URL hash and MinHash",
                 "4  OPTIMIZE / VACUUM from a maintenance queue",
                 "5  Breakers wrap http · delta · redis",
                 "6  BART-large-CNN summaries on the worker"]
        for i, s in enumerate(notes):
            Pn.append(self.txt(self.fit(s, "label", avail), x + 16, y + 98 + i * 16, "label", within=BLOCK_SH))

    def draw_legend(self):
        t = self.t
        x, y, w, h = LEGEND
        Pn = self.layers["panels"]
        Pn.append(self.cartouche(x, y, w, h, "legend"))
        Pn.append(self.header(f"SYMBOLS · CHART NO. {self.repo_count} · EVERY SHEET", x + 14, y + 16, within=LEGEND))
        Pn.append(self.txt("upright figures are measured · sloping figures are not · underlined: above datum", x + 14, y + 30,
                           "label", within=LEGEND))
        col_w = (w - 28) / 3
        cols = [x + 14 + i * col_w for i in range(3)]
        avail = col_w - 38
        y0, pitch = y + 50, 15
        S = self.stroke
        ink = t.ink

        def line(d, attrs):
            return f'<path d="{d}" fill="none" {attrs}/>'

        months = self.scrapy.get("months_active")
        commits = self.scrapy.get("commits")
        boxed = lambda cx, cy: (self.txt("A", cx, cy + 4, "label", anchor="middle")  # noqa: E731
                                + f'<rect x="{cx - 7}" y="{cy - 7}" width="14" height="14" fill="none" {S("PEN", ink, 0.9, caps="butt")}/>')
        rows = [[
            (lambda cx, cy: self.use_legend("can", cx, cy + 6), "G can · port, returning"),
            (lambda cx, cy: self.use_legend("nun", cx, cy + 6), "R nun · starboard"),
            (lambda cx, cy: self.use_legend("light", cx, cy), "Light · its character"),
            (lambda cx, cy: self.use_legend("flare", cx, cy + 5), "Flare · marks a light"),
            (lambda cx, cy: self.use_legend("halo", cx, cy, scale=0.7), "Halo · by night"),
            (lambda cx, cy: self.use_legend("ldg", cx - 6, cy + 4) + self.use_legend("ldg", cx + 6, cy)
             + line(f"M{cx - 12} {cy + 8}L{cx + 12} {cy - 4}", S("HAIR", ink, 0.8)), "Ldg line · health check"),
            (lambda cx, cy: self.use_legend("traffic", cx, cy + 9), "Traffic Sig · breaker"),
            (lambda cx, cy: self.lamps(cx, cy), "go · stop · one at a time"),
            (lambda cx, cy: self.use_legend("horn", cx - 6, cy), "Horn · Alertmanager"),
            (lambda cx, cy: self.use_legend("anchorage", cx, cy), "Anchorage · Delta Lake"),
            (lambda cx, cy: self.use_legend("wreck", cx, cy, scale=0.8), "Wk · dead branch, year"),
            (lambda cx, cy: self.use_legend("waypoint", cx, cy), "Waypoint · stage"),
        ], [
            (lambda cx, cy: self.use_legend("sloop", cx, cy + 8, scale=0.45), "Sloop · under way"),
            (lambda cx, cy: self.use_legend("sloop-glyph", cx, cy + 6), "Packet boat · plotted"),
            (lambda cx, cy: self.use_legend("fix", cx, cy), "Fix · position"),
            (lambda cx, cy: self.use_legend("station", cx, cy), "Station · profile repo"),
            (lambda cx, cy: self.use_legend("correction", cx, cy), "Correction · revised"),
            (lambda cx, cy: self.use_legend("rep", cx, cy), "Rep · reported, not found"),
            (lambda cx, cy: self.use_legend("ed", cx, cy), "ED · existence doubtful"),
            (lambda cx, cy: self.txt("SD", cx, cy + 4, "label-italic", anchor="middle"), "SD · sounding doubtful"),
            (lambda cx, cy: self.txt("PA", cx, cy + 4, "label-italic", anchor="middle"), "PA · position approximate"),
            (boxed, "Zone · seed source"),
            (lambda cx, cy: self.txt(f"{LDG_BRG:.0f}°", cx, cy + 4, "label", anchor="middle"), "Bearing · true"),
            (lambda cx, cy: (self.snd(commits, cx, cy + 4, sub=months, truth="measured", role="label")
                             if commits and months else self.snd(4, cx, cy + 4, sub=2, truth="illustrative", role="label")),
             "Height · commits, months" if commits and months else "Sounding · 1000s, 100s"),
        ], [
            (lambda cx, cy: line(f"M{cx - 12} {cy}h24", S("PEN", ink, 0.85, "COURSE")), "Course · lit channel"),
            (lambda cx, cy: line(f"M{cx - 12} {cy + 4}h24", S("PEN", ink, 0.7, "PECK", caps="butt")) + self.hollow_mark("can", cx + 6, cy - 2),
             "Proposed channel · unlit"),
            (lambda cx, cy: f'<circle cx="{cx}" cy="{cy}" r="6" fill="none" {S("LINE", ink, 0.9, "DANGER", gap=4.3)}/>', "Danger line · shoal"),
            (lambda cx, cy: f'<rect x="{cx - 12}" y="{cy - 5}" width="12" height="10" fill="{t.shallow_b}"/>'
             f'<rect x="{cx}" y="{cy - 5}" width="12" height="10" fill="{t.shallow_a}"/>', "Tints · under 5, 10"),
            (lambda cx, cy: line(f"M{cx - 12} {cy}h8M{cx + 4} {cy}h8", S("LINE", t.ink2, 0.7))
             + self.txt("10", cx, cy + 3.5, "contour-figure", anchor="middle", fill=t.ink2, semantic=False), "Contours · 2 5 10 20"),
            (lambda cx, cy: line(f"M{cx - 12} {cy}h24", S("PEN", t.ink2, 0.7, "APPROX")), "Approximate contour"),
            (lambda cx, cy: line(f"M{cx - 12} {cy}h24", S("PEN", ink, 0.9, "RESTRICT", caps="butt"))
             + line(f"M{cx - 8} {cy}v3M{cx} {cy}v3M{cx + 8} {cy}v3", S("PEN", ink, 0.9, caps="butt")), "Restricted · robots.txt"),
            (lambda cx, cy: line(f"M{cx - 12} {cy}h24", S("HAIR", ink, 0.55, "TRACK", caps="butt")), "Track line · one shard"),
            (lambda cx, cy: line(f"M{cx} {cy - 7}v14", S("HAIR", ink, 0.35, "TRACK", caps="butt")), "Check line · dedup"),
            (lambda cx, cy: self.hatch_swatch(cx, cy), "Hatch · unsurveyed"),
            (lambda cx, cy: line(f"M{cx - 12} {cy + 2}L{cx - 4} {cy - 2}L{cx + 4} {cy + 2}L{cx + 12} {cy - 2}", S("PEN", ink, 0.85, "LIMIT", caps="butt")),
             "Limit of survey"),
            (lambda cx, cy: self.snd(4, cx, cy + 4, sub=2, truth="illustrative", role="label"), "Sounding · 1000s, 100s"),
        ]]
        for ci, col in enumerate(rows):
            cx0 = cols[ci]
            for ri, (draw, text) in enumerate(col):
                cy = y0 + ri * pitch
                Pn.append(draw(cx0 + 14, cy - 4))
                Pn.append(self.txt(self.fit(text, "label", avail), cx0 + 36, cy, "label", within=LEGEND))

    def lamps(self, cx, cy) -> str:
        t = self.t
        out = []
        for i, st in enumerate([(t.ok, t.ok, t.ok), (t.accent, t.accent, t.accent), (t.ok, t.paper, t.ok)]):
            x = cx - 10 + i * 10
            for j, col in enumerate(st):
                out.append(f'<circle cx="{x}" cy="{cy - 5 + j * 5}" r="2" fill="{col}" {self.stroke("HAIR", t.ink, 0.9)}/>')
        return "".join(out)

    def hatch_swatch(self, cx, cy) -> str:
        d, b = c.hatch((cx - 12, cy - 6, 24, 12), self.t, self.jit.sub("legend-hatch"), "unsurveyed", "hatch-legend", spacing=5)
        self.defs.append(d)
        return (f'<g opacity=".35">{b}</g>' if self.night else b) + \
            f'<rect x="{cx - 12}" y="{cy - 6}" width="24" height="12" fill="none" {self.stroke("HAIR", self.t.ink, 0.6, caps="butt")}/>'

    # ---------------------------------------------------------------- frame and margin
    def draw_frame(self):
        t = self.t
        F, Mg = self.layers["frame"], self.layers["margin"]
        unit = self.cfg["copy"]["unit_approaches"]
        if self.phone:
            F.append(c.frame(self.w, self.h, t, "minute-bars", rules=self.rules))
            Mg.append(self.txt(unit, 360, 21, "label-caps", anchor="middle", fill=t.ink))
            Mg.append(self.txt(str(self.repo_count), 700, 21, "label", anchor="end", key="chart-number", truth="measured"))
            Mg.append(self.txt(f"CHART NO. {self.repo_count} · SHEET 3", 26, self.h - 7, "label", key="folio"))
            ax, ay = 60, 1200             # north arrow pointing left: the sheet is oriented to the channel
            Mg.append(f'<path d="M{ax + 44} {ay}H{ax}M{ax + 12} {ay - 7}L{ax} {ay}L{ax + 12} {ay + 7}" fill="none" {self.stroke("PEN", t.ink, 0.9)}/>')
            Mg.append(self.txt("N", ax + 56, ay + 9, "label"))
            self.exclude("north", ax - 6, ay - 20, 100, 40)
        else:
            F.append(c.frame(self.w, self.h, t, "broken", gaps=[("right", 300, 324), ("right", 560, 584)], rules=self.rules))
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
        self.draw_title_block()
        if not self.phone:
            self.draw_zoc()
            self.draw_inset()
            self.draw_blocks()
            self.draw_legend()
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
