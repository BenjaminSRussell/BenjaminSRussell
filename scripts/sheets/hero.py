"""hero.py — Sheet 1, "Chart No. N": the archipelago of one person's public repositories (T2).

The chart proper. One feature per repo, its drawn area at the 5-contour proportional to Ben's own
commits (solve_radii, ±8 %); the 52 weekly totals are the soundings along the course and they
generate the depth field (depth = count, MASTERPLAN 15); contours 5 · 10 · 20 · 50 with figures in
breaks; a buoyed 290° entrance into Scrapy Harbor; a two-ring rose as a 24-hour clock in the
author's local time; an open title block; the unsurveyed band at the limit of survey. The boat
sails in once (4–28 s) and anchors; the two lateral lights are the only loop afterwards.

Every glyph goes through typeset (ctx.k), every animation through the Timeline (ctx.tl), every line
through chartlib. Phone editions are the same story redrawn at SCALE_PHONE through one affine map
of the desk layout (features, course, marks, basin, band, arc), with the field re-solved in phone space.

Round 2 (orchestrator crit): features are composed of a main kernel plus 3–6 jittered lobes and
dents (Jitter keyed by repo name, never by data) so no coastline is round; the small features sit
on a SW–NE archipelago arc; closed 10-contours shorter than 450 px are generalised away so the
10-line wanders once around the working ground instead of haloing every islet; the sounding rows
are jittered and the kernels widened (h 36) so the sounded bank reads as a shoal, not a road; names
sit on the land or offshore below their feature; the anchored sloop is 70 % and in the basin water.
"""
from __future__ import annotations

import math
import re

import chartlib as c
import edition as E
from timeline import ease_inverse
from tokens import INK

NAME = "hero"
KIND = "chart"
SIZES = {"desk": (1280, 740), "phone": (720, 900)}
EDITIONS = None   # the runner's default six plus HERO_EXTRA (phone stills)

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the title block, the margin captions, the band's UNSURVEYED and the land names are set upper-case through "
     "role `label` with tracking 0.6 (phone 1.0); only the unit line is role `label-caps`",
     "check_type allows one label-caps run per sheet; a period title block is five caps lines"),
    ("Land names in condensed caps, water names in serif italic",
     "islands and the harbour are lettered upright in Plex Sans Condensed (17 px for r ≥ 40, else 13), shoals in "
     "Instrument Serif italic 17",
     "the glyph-defs budget (40 KB) cannot carry a serif register for both; upright/italic still means land/water"),
    ("Role line in condensed caps 13", "the plain register in the chart's own face, ink, second line of the block",
     "the serif-italic 22 run cost 32 KB inline; decision 7 calls this line the plain register"),
    ("No margin graticule", "the frame carries minute bars only; no labelled meridians or parallels",
     "the sheet has no latitude or longitude, so labelled margin ticks would be invented geometry"),
    ("Islets unnamed", "features whose r < 16 (under ~25 commits) carry their spot height only",
     "twenty-one names would collide; an unnamed rock with its height is chart grammar"),
    ("Phone lights lit, not flashing", "the phone editions draw both lights lit and cull the character labels",
     "MASTERPLAN 7.3: hero-phone ≤ 0.25 repaints/s after 6 s; two Fl 4s lights alone are 1/s"),
    ("Pencil note without a notice number", "\"sitemap.xml lies again\" stands alone by the double shoal",
     "chart.toml's notices carry no sitemap item; a tie to Notice 3 would be invented"),
    ("Sounded bank softened, not smoothed (round 2, option b + a)",
     "the course threads between Game Engine I. and rustmapper into the harbour; the 52 week kernels take h = 36 "
     "(not 30) and the four rows cycle −36 / +18 / −18 / +36 with ±5 px jitter keyed by index, so the shallow "
     "water of the zero weeks is one broad irregular bank merging with the islands' shelf; amplitudes stay solved "
     "so every printed figure is the field's own value",
     "36 of 52 weeks are 0: the honest field is shallow along the course; it must read as a bank, not a road"),
    ("Contours generalised", "closed 10-contours shorter than 520 px (phone 280) are neither drawn nor tinted",
     "a 10-ring around every islet is a bubble chart; small-scale charts drop rings the pen cannot carry"),
    ("Title and land static at t=0 (five-second test; 7.2 t=0 floor)",
     "name, thesis, title block, imprint, frame, rose, band, land masses, coastlines and feature names are present "
     "at load with no fade; only the water draws in (contours deep-first, tints, soundings in course order, danger "
     "lines, course, marks, bearings), then the boat sails 4–28 s; the opening still ends at 4.0 s",
     "orchestrator decision, round 2: a reader must never land on blank paper"),
    ("Week figures surface as the boat passes (round 3)",
     "the printed week soundings and the two dated fixes are discrete reveals on the 0.5 s grid between 4 and "
     "28 s, in course order, the last landing as she anchors; zero weeks print one 0 per run; figures keep 28 px "
     "apart (the rest remain kernels); still edition shows them all",
     "the chart surveys itself: the lead goes down where the ship is"),
    ("Marginalia moved (round 3)", "small corrections bottom-left, chart number top-right, folio folded into the "
     "imprint line bottom-centre", "chart practice (13's re-crit); decision 27 put the folio bottom-left"),
    ("Lobed features", "each feature is its main kernel plus 3–6 lobes/dents, Jitter keyed by repo name, scaled by r",
     "no two islands share a silhouette; area ∝ commits is solved on the drawn 5-polygon, lobes included"),
]

# ---------------------------------------------------------------- desk layout (1280-space)
RULES = {"desk": (18, 24), "phone": (14, 19)}
DRAWABLE = (24, 24, 1232, 692)
K_AREA = 32.2                     # px² of 5-contour area per commit (r = 3.2·√commits), desk
LEVELS = c.DEFAULT_LEVELS         # (0, 5, 10, 20, 50)
INDEX = (10.0, 50.0)
COURSE = [(1136, 296), (1046, 360), (900, 470), (842, 580), (776, 556)]       # WP1 … WP5 (decision 1)
SLOTS = {                         # repo → centre; the named six (T2 §2.3 with decision 1); game_engine,
    "Scrapy": (760, 560), "Rust-sitemap": (1030, 516), "game_engine": (816, 344),        # rustmapper and
    "Data_science_dev": (992, 636), "BenjaminSRussell": (330, 405), "FashionDB": (640, 420),  # DSD moved so the
}                                 # sounding kernels (rows ±36+5, h 36) never dig a feature's 5-ring: course ≥ r + 78
ARC = [(90, 472), (260, 458), (430, 442), (600, 412), (740, 372)]    # the archipelago shelf, SW → NE (desk)
PHONE_ARC = [(55, 455), (150, 418), (260, 396), (360, 382)]            # the phone's own arc (phone coordinates)
ROWS = (-36, 18, -18, 36)         # sounding rows off the course, cycling across it
ROW_JITTER = 5                    # ± px, keyed by sounding index
H_SND = 36                        # sounding kernel support (MASTERPLAN 16 says 30; see BREAKS)
CLEAR_COURSE = 78                 # features keep r + 78 from the course (rows 36 + jitter 5 + h_snd 36)
SOUND_STOP = 70                   # the soundings end this far before the entrance (WP4): the basin is the harbour's
CELL = {"desk": 6.0, "phone": 4.0}
BIG_NAME_R = 40                   # land names at 17 px caps from this radius, 13 px below it
GENERALISE_10 = {"desk": 520, "phone": 280}   # closed 10-contours shorter than this are not drawn or tinted
BASIN = [(779, 557, 30, -2.0), (806, 567, 26, -0.66), (768, 556, 22, -0.5)]   # basin kernels (x, y, h, amp/base):
                                  # the bay, the mouth toward WP4, and the berth under the anchorage
MARK_R2 = (827, 551)              # R "2" nun, north of the 290° leg
MARK_G1 = (813, 593)              # G "1" can, south
COVERAGE = (680, 470, 210, 160)   # "SEE SHEET 3"
SEE_SHEET = (687, 484)            # inside the box, top-left (open water)
CALM = (40, 40, 800, 280)
TITLE_BOX = (70, 540, 540, 130)
ROSE = (1000, 160, 72)
ROSE_BOX = (920, 80, 160, 206)    # rings, numerals and the two VAR lines
LIMIT_X = 1080
BAND = (1080, 24, 200, 692)       # neat line to neat line (round 3): the edge of the world, not a swatch
SOUND_GAP = 28                    # printed week figures keep this apart (round 3); the rest stay kernels
ZERO_GAP = 60                     # at most one printed "0" per 60 px of course (round 4)
ZERO_CLEAR = 24                   # and none within 24 px of a non-zero figure
GENERALISE_20 = 200               # closed 20-rings shorter than this are not drawn
UNSURVEYED_FADE = 70              # the coast factor falls 1→0 over LIMIT_X … LIMIT_X+70
PA_SHIFT = (14, -10)
NOTE_AT = (700, 672, -7)          # pencil note anchor and rotation: below the harbour box, clear of the band
NOTE_TEXT = "sitemap.xml lies again — see Sheet 3"
PHONE_S = 0.55
PHONE_ORIGIN = (19, 300)          # where the desk drawable's corner lands on the phone sheet
SAIL = (4.0, 24.0)                # begin, dur (MASTERPLAN 2.1: 4–28 s)
BOAT_SCALE = 0.7                  # the detail sloop at anchor (round 2: chart vessels are small)
LIGHT_R = 2.2                     # lit core radius (round 3: the hero's lanterns match sheet 3)

LAND_KINDS = ("island", "harbour", "islet")


# ---------------------------------------------------------------- small helpers
def _fmt(v):
    return E.fmt(v)


def _month(iso: str) -> str:
    y, m = iso[:4], int(iso[5:7])
    return f"{['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'][m - 1]} {y}"


def _date(iso: str) -> str:
    y, m, d = iso[:4], int(iso[5:7]), int(iso[8:10])
    return f"{d} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m - 1]} {y}"


def _display_name(repo: str) -> str:
    if "_" in repo:
        return " ".join(w[:1].upper() + w[1:] for w in repo.split("_") if w)
    return repo


class Geo:
    """The affine map from the desk layout to this edition's sheet (identity on the desk)."""

    def __init__(self, s: float, ox: float, oy: float):
        self.s, self.ox, self.oy = s, ox, oy

    def p(self, x, y):
        return (self.ox + self.s * x, self.oy + self.s * y)

    def pi(self, x, y):
        return (E.I(self.ox + self.s * x), E.I(self.oy + self.s * y))

    def d(self, v):
        return v * self.s

    def rect(self, r):
        x, y = self.p(r[0], r[1])
        return (x, y, self.d(r[2]), self.d(r[3]))


def _soundings(course, values, rows, s: float, seed, entrance_i: int = 3) -> list:
    """Week i (oldest first) at arc position i·L'/n along the course from WP1 to SOUND_STOP px short
    of the harbour entrance (WP4); rows cycle across the course with a ±ROW_JITTER px offset keyed by
    the index (never by the value), so the oldest sit seaward in the band and the newest lie in the
    approach; nothing is sounded on the harbour's own ground. Integer coordinates."""
    n = len(values)
    L = c.polyline_length(course[:entrance_i + 1]) - SOUND_STOP * s
    out = []
    for i, v in enumerate(values):
        arc = L * i / n
        (x, y), (tx, ty) = c.polyline_at(course, arc)
        off = rows[i % len(rows)] + c.Jitter(seed, f"hero/snd/{i}").offset(ROW_JITTER)
        off *= s
        out.append((E.I(x - ty * off), E.I(y + tx * off), v))
    return out


def _lobes(f, base: float, seed, s: float) -> list:
    """3–6 sub-kernels that make a feature's coastline irregular: a dominant lobe side (positive land
    kernels, land kinds only) and a lee side of dents (negative), all scaled by the current r and
    seeded by the repo name. Returned as `extra` kernels (x, y, h, amp) in depth units."""
    j = c.Jitter(seed, f"hero/lobes/{f.alias}")
    ratio = f.ratio or 1.6
    amp_main = (base - 5.0) / c.bump(1.0 / ratio)
    th0 = j.uniform(0, 2 * math.pi)
    n = 3 + int(j.uniform(0, 3))
    out = []
    for i in range(n):
        lobe = (i % 2 == 0) and f.kind in LAND_KINDS
        if lobe:
            ang = th0 + j.uniform(-0.9, 0.9)
            d = f.r * j.uniform(0.35, 0.7)
            h = f.r * j.uniform(0.7, 1.05)
            amp = amp_main * j.uniform(0.25, 0.55)
        else:
            ang = th0 + math.pi + j.uniform(-1.1, 1.1)
            d = f.r * j.uniform(0.75, 1.1)
            h = f.r * j.uniform(0.45, 0.8)
            amp = -amp_main * j.uniform(0.15, 0.35)
        out.append((f.x + d * math.cos(ang), f.y + d * math.sin(ang), max(h, 3.0 * s), amp))
    return out


def _area_at(field, f, level: float = 5.0):
    """Area of the smallest closed shallow `level` polygon around (f.x, f.y), as solve_radii measures it."""
    hh = max(f.h, f.r * 2.0, 24.0)
    win = (f.x - 1.4 * hh, f.y - 1.4 * hh, 2.8 * hh, 2.8 * hh)
    best = None
    for q in c.contours(field, [level], clip=win):
        if q.closed and q.shallow_inside and q.contains(f.x, f.y):
            a = q.area()
            if best is None or a < best:
                best = a
    return best


def _bisect_radius(f, builder, features, target: float, lo: float, hi: float, steps: int = 14):
    """Bisection on f.r so that the measured 5-polygon area meets `target`, keeping the best radius
    seen: area(r) jumps where a harbour's bay changes topology, so the Newton step oscillates and the
    final midpoint may land on a radius whose polygon does not close."""
    best = None
    for _ in range(steps):
        f.r = (lo + hi) / 2
        area = _area_at(builder(features), f)
        if area is not None and (best is None or abs(area / target - 1) < abs(best[1] / target - 1)):
            best = (f.r, area)
        if area is None or area < target:
            lo = f.r
        else:
            hi = f.r
        if area is not None and abs(area / target - 1) < 0.02:
            break
    if best is None:
        return None
    f.r, f.area = best
    builder(features)                     # leaves every feature's kernel (h, amp) at the chosen radius
    return f.area


def _place_on_arc(features, arc_pts, drawable, exclusions, course_pts, placed, seed, s: float,
                  clear_edge: float, clear_pair: float, clear_course: float) -> list:
    """Round 2: the unslotted features (largest first) are strung along the archipelago arc,
    alternating sides, offset r + 26 (+ 40 per lap) with a ±10 px jitter keyed by repo name; a
    candidate must clear the drawable, the exclusions, every placed feature and the course.
    Returns the names that found no place."""
    dense = c.catmull_rom(arc_pts, 24)
    L = c.polyline_length(dense)
    dx0, dy0, dw, dh = drawable
    cursor, side = 20 * s, 1
    dropped = []
    for f in features:
        j = c.Jitter(seed, f"hero/arc/{f.alias}")
        jit_off, jit_along = j.offset(10 * s), j.offset(8 * s)
        ok = False
        for attempt in range(600):
            spos = cursor + jit_along + attempt * 5 * s
            lap, u = int(spos // L), spos % L
            if lap > 3:
                break
            (px, py), (tx, ty) = c.polyline_at(dense, u)
            off = (f.r + 26 * s + lap * 40 * s) * side + jit_off
            x, y = px - ty * off, py + tx * off
            m = f.r + clear_edge
            if not (dx0 + m <= x <= dx0 + dw - m and dy0 + m <= y <= dy0 + dh - m):
                continue
            me = f.r + 12 * s
            if any(ex[0] - me <= x <= ex[0] + ex[2] + me and ex[1] - me <= y <= ex[1] + ex[3] + me for ex in exclusions):
                continue
            if any(math.hypot(x - p.x, y - p.y) < f.r + p.r + (clear_pair if (f.r >= 16 * s and p.r >= 16 * s)
                                                                 else clear_pair * 0.7) for p in placed):
                continue
            if course_pts and c.dist_to_polyline(x, y, course_pts) < f.r + clear_course:
                continue
            f.x, f.y, f.placed = E.I(x), E.I(y), True
            placed.append(f)
            cursor = u + 2 * f.r + 30 * s
            side = -side
            ok = True
            break
        if not ok:
            dropped.append(f.name)
    return dropped


def _inject(el: str, child: str) -> str:
    """Put `child` inside a self-closing element string (`<circle …/>` → `<circle …>child</circle>`)."""
    m = re.match(r"^<([A-Za-z]+)(\s[^>]*?)?/>$", el.strip(), re.S)
    if not m:
        return f"<g>{child}{el}</g>"
    return f"<{m.group(1)}{m.group(2) or ''}>{child}</{m.group(1)}>"


def _boxes_overlap(a, b) -> bool:
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


# ---------------------------------------------------------------- data → features
def _features(data: dict, cfg, k_area: float) -> tuple[list, dict]:
    """One Feature per surveyed repo; name/kind from chart.toml [[features]] where present (`bank`
    reads as shoal, `vessel` as the ship's own shoal). `alias` holds the repo name (the key for
    slots and report keys); `name` is what the chart prints. Returns (features, repo_of_feature_name)."""
    spec = {f["repo"]: f for f in cfg.get("features", [])}
    feats, repo_of = [], {}
    for r in data["repos"]:
        commits = int(r.get("commits") or 0)
        if commits <= 0:
            continue
        s = spec.get(r["name"], {})
        aliases = s.get("aliases") or r.get("aliases") or []
        printed = aliases[0] if aliases else None
        r0 = math.sqrt(k_area * commits / math.pi)
        kind = s.get("kind")
        if r.get("archived"):
            kind = "wreck"
        elif kind in ("vessel", "bank"):
            kind = "shoal"          # the ground the ship surveyed, named for her (T2 decision 13); a bank is submerged
        elif kind not in ("harbour", "shoal", "island", "islet"):
            kind = c.kind_of(r0, bool(r.get("active")), printed or r["name"], bool(r.get("archived")))
        if kind == "islet" and r0 >= 16:
            kind = "island"
        if printed:
            name = printed
        elif kind == "shoal":
            name = f"{_display_name(r['name'])} Shoal"
        elif kind == "island":
            name = f"{_display_name(r['name'])} I."
        else:
            name = _display_name(r["name"])
        f = c.Feature(name, commits, kind, alias=r["name"], sub=r.get("months_active"))
        f.r = r0
        f.ratio = 1.6 if kind in LAND_KINDS else 1.82
        feats.append(f)
        repo_of[name] = r
    return feats, repo_of


# ---------------------------------------------------------------- the build
def build(ctx) -> str:
    ed, data, cfg, tl, k = ctx.ed, ctx.data, ctx.cfg, ctx.tl, ctx.k
    if k is None:
        raise RuntimeError("hero needs the type engine (scripts/typeset.py)")
    theme = ed.theme
    phone = ed.phone
    night = ed.dark
    w, h = SIZES[ed.scale]
    sc = ed.scale
    seed = int(cfg.get("chart", {}).get("seed", 27))
    jit = c.Jitter(seed, f"hero/{sc}")
    prefix = "h"                                   # edition.svg prefixes everything with "hero-"
    geo = Geo(1.0, 0.0, 0.0) if not phone else Geo(PHONE_S, PHONE_ORIGIN[0] - 24 * PHONE_S,
                                                     PHONE_ORIGIN[1] - 24 * PHONE_S)
    s = geo.s
    caps_track = 0.6 if not phone else 1.0
    opening_end = tl.cue("opening", 0, 4.0)
    report: dict = ctx.extra

    # ---- lettering: one callback, the T6 label_cb contract, caps lines through role `label`
    def lbl(text, x, y, role, anchor="start", rotate=0, fill=None, caps=False, **kw):
        tracking = kw.pop("tracking", None)
        if role == "label-caps" and not kw.get("key"):
            role, text, tracking = "label", str(text).upper(), caps_track
        elif caps:
            text, tracking = str(text).upper(), caps_track if tracking is None else tracking
        return k.label(str(text), x, y, role, anchor=anchor, rotate=rotate, fill=fill, edition=ed, scale=sc,
                       tracking=tracking, **kw)

    def snd(value, x, y, **kw):
        return k.sounding(value, x, y, edition=ed, scale=sc, **kw)

    def width(text, role, **kw):
        return k.text_width(str(text), role, edition=ed, scale=sc, **kw)

    # ---- data
    weeks = data.get("weeks") or []
    if len(weeks) < 10:
        raise RuntimeError("hero: stats.json carries no weekly soundings (weeks[]); refusing to invent them")
    values = [int(wk.get("n") or 0) for wk in weeks]
    med = sorted(values)[len(values) // 2]
    base = float(min(50, max(10, med)))
    if any(abs(base - lv) < 1e-9 for lv in LEVELS):
        base += 0.5                                # never exactly on a contour level (B's note)
    N = int(data.get("repo_count") or len(data["repos"]))
    notices_n = len(data.get("notices") or [])
    edition_d = data.get("edition") or {}
    hours = list(data.get("hours") or [0] * 24)
    var = data.get("variation") or {}
    modal = int(var.get("hour", max(range(24), key=lambda i: hours[i]) if any(hours) else 0))
    var_year = var.get("year") or (data.get("taken") or "2026")[:4]
    first_year = (data.get("first_commit") or "2025")[:4]
    upd_year = (data.get("taken") or data.get("updated_at") or "2026")[:4]
    login = data.get("login") or cfg.get("chart", {}).get("login", "")
    thesis = cfg.get("copy", {}).get("thesis", "I survey a web that is wrong about itself.")
    role_line = cfg.get("copy", {}).get("role_line", "Crawl and data infrastructure · Python and Rust")
    unit_line = cfg.get("copy", {}).get("unit_hero", "SOUNDINGS IN COMMITS")
    limit_label = cfg.get("copy", {}).get("limit_label", f"LIMIT OF SURVEY {upd_year}")

    k_area = K_AREA * s * s
    feats, repo_of = _features(data, cfg, k_area)
    if phone:
        feats = [f for f in feats if f.value >= 12]      # small-scale edition: islets under 12 culled
    culled = N - len(feats) - len(data.get("unsurveyed") or [])

    # ---- geometry in sheet space
    course = [geo.pi(*p) for p in COURSE]
    drawable = geo.rect(DRAWABLE)
    limit_x = geo.p(LIMIT_X, 0)[0]
    slots = {kname: geo.pi(*xy) for kname, xy in SLOTS.items()}
    arc = [geo.p(*p) for p in ARC] if not phone else [tuple(p) for p in PHONE_ARC]
    if phone:
        rose_cx, rose_cy, rose_r = 600, 310, 56
        rose_box = (500, 210, 200, 202)   # N above the ring, the VAR line below, both inside
        band = (E.I(limit_x), 412, w - E.I(limit_x), 300)
    else:
        rose_cx, rose_cy, rose_r = ROSE
        rose_box = ROSE_BOX
        band = BAND
    excl = [geo.rect(COVERAGE), (band[0], drawable[1], w - band[0], drawable[3]), rose_box]
    if not phone:
        excl += [CALM, (TITLE_BOX[0] - 16, TITLE_BOX[1] - 16, TITLE_BOX[2] + 32, TITLE_BOX[3] + 32)]
    # slots first (place_features with no Halton work: every unslotted feature goes to the arc)
    order = sorted((f for f in feats if f.kind != "wreck"), key=lambda f: (-f.value, f.name))
    placed = []
    for f in order:
        if f.alias in slots:
            f.x, f.y = slots[f.alias]
            f.placed, f.slot = True, f.alias
            placed.append(f)
    unslotted = [f for f in order if not f.placed]
    dropped = _place_on_arc(unslotted, arc, drawable, excl, course, placed, seed, s,
                            clear_edge=24 * s, clear_pair=44 * s, clear_course=CLEAR_COURSE * s)
    if dropped:   # whatever the arc could not take goes through chartlib's Halton search (reported)
        rest = [f for f in feats if not f.placed and f.kind != "wreck"]
        fallback = c.place_features(placed + rest, drawable, excl, course, seed, slots, cap=64,
                                    clear_edge=24 * s, clear_pair=30 * s, clear_course=CLEAR_COURSE * s,
                                    islet_min_x=drawable[0], tries=3000)
        dropped = list(fallback.dropped)
    feats = [f for f in feats if f.placed]
    for f in feats:
        f.axis = (0.0, 2 * f.r, f.x, f.y)
    harbour = next((f for f in feats if f.kind == "harbour"), None)
    vessel_ground = next((f for f in feats if f.alias == "Rust-sitemap"), None)
    profile = next((f for f in feats if f.alias == "BenjaminSRussell"), None)
    pairs = [math.hypot(a.x - b.x, a.y - b.y) - a.r - b.r for i, a in enumerate(feats) for b in feats[i + 1:]]
    too_close = [(f.name, round(c.dist_to_polyline(f.x, f.y, course) - f.r - CLEAR_COURSE * s, 1))
                 for f in feats if f.kind != "harbour" and c.dist_to_polyline(f.x, f.y, course) < f.r + CLEAR_COURSE * s]

    # ---- soundings along the course: the 52 weeks, oldest seaward
    rows = tuple(float(v) for v in ROWS)
    sounds = _soundings(course, values, rows, s, seed)
    coast = c.Coast(drawable, inset=24 * s, unsurveyed_x=(limit_x, limit_x + UNSURVEYED_FADE * s))
    basin = [(*geo.p(x, y), hh * s, amp * base) for x, y, hh, amp in BASIN]
    cell = CELL[sc]

    def extras(fs):
        out = list(basin)
        for f in fs:
            if f.kind not in ("wreck", "harbour") and f.r > 0:    # the harbour's character is its bay
                out.extend(_lobes(f, base, seed, s))
        return out

    def builder(fs):
        return c.Field.from_soundings(w, h, sounds, base, features=fs, coast=coast, h_snd=H_SND * s,
                                      extra=extras(fs), cell=cell)

    def own_ground(fs):
        # each feature's own kernels on the grid, without the soundings: what "area ∝ commits" asserts
        return c.Field.from_soundings(w, h, [], base, features=fs, coast=coast, h_snd=H_SND * s,
                                      extra=extras(fs), cell=cell)

    radii = c.solve_radii(own_ground, feats, k_area, tol=0.08, iters=4, r_bounds=(6.0 * s, 90.0 * s))
    for rep in radii:
        if rep.ok or rep.r < 10 * s:
            continue
        f = next(ff for ff in feats if ff.name == rep.name)
        area = _bisect_radius(f, own_ground, feats, f.target, 0.7 * f.r, 1.4 * f.r)
        ratio = (area / f.target) if area else None
        radii[radii.index(rep)] = c.RadiusReport(rep.name, rep.value, rep.target, round(area) if area else None,
                                                 round(f.r, 1), round(ratio, 3) if ratio else None,
                                                 ratio is not None and abs(ratio - 1) <= 0.08, rep.iters + 14, rep.clamped)
    F = builder(feats)
    cs = c.contours(F, LEVELS)
    band_skip = [i for i, (x, y, v) in enumerate(sounds) if x >= limit_x]
    fails = c.bracket_test(cs, sounds, LEVELS, base=base, skip=band_skip, field=F)
    # a sounding whose ring the grid cannot resolve, or that sits on a feature's lift, nudges 4 px
    # along the course and the field is re-solved (T2 §2.4); two rounds, then it is reported
    for _round in range(2):
        movable = [f for f in fails if f[6] in ("polygon", "field")]
        if not movable:
            break
        L = c.polyline_length(course)
        for (i, x, y, v, exp, found, cause) in movable:
            (px, py), (tx, ty) = c.polyline_at(course, L * i / len(values))
            ox, oy, vv = sounds[i]
            sounds[i] = (E.I(ox + tx * 4 * s), E.I(oy + ty * 4 * s), vv)
        F = builder(feats)
        cs = c.contours(F, LEVELS)
        fails = c.bracket_test(cs, sounds, LEVELS, base=base, skip=band_skip, field=F)
    unclosed = c.closed_check(cs, levels=(5.0, 10.0), min_len=30 * s)
    area_bad = [r for r in radii if not r.ok and r.r >= 10 * s]
    if area_bad:
        raise RuntimeError("hero: area law failed (±8 % at the 5-contour): " +
                           "; ".join(f"{r.name} {r.ratio}" for r in area_bad))
    if harbour is not None:
        hx, hy = harbour.x, harbour.y
        ax, ay = course[-1]
        half = 13 * BOAT_SCALE * s
        if not (F.value(hx, hy) < 0 and F.value(ax, ay) > 0 and F.value(ax - half, ay) > 0 and F.value(ax + half, ay) > 0):
            raise RuntimeError(f"hero: harbour basin did not open around the anchorage (land {F.value(hx, hy):.1f}, "
                               f"anchorage {F.value(ax, ay):.1f}, hull ends {F.value(ax - half, ay):.1f} / "
                               f"{F.value(ax + half, ay):.1f})")
    drawn = c.feature_polygons(cs, feats, 5.0)
    report["features"] = [{"name": r.name, "commits": r.value, "area_px": r.area, "target_px": r.target,
                           "r": r.r, "ratio": r.ratio, "ok": r.ok, "cx": f.x, "cy": f.y, "kind": f.kind,
                           "drawn_px": (round(abs(c.polygon_area(drawn[f.name]))) if f.name in drawn else None),
                           "drawn_ratio": (round(abs(c.polygon_area(drawn[f.name])) / r.target, 3)
                                           if f.name in drawn and r.target else None)}
                          for r in radii for f in feats if f.name == r.name]
    report["course_too_close"] = too_close
    report["bracket_failures"] = len(fails)
    report["bracket"] = [list(f) for f in fails]
    report["unclosed"] = unclosed
    report["place"] = {"dropped": dropped, "beyond_cap": [], "slot_conflicts": [],
                       "min_pair_clearance": round(min(pairs), 1) if pairs else None,
                       "min_course_clearance": round(min(c.dist_to_polyline(f.x, f.y, course) - f.r
                                                         for f in feats if f.kind != "harbour"), 1)}
    report["field"] = {"base": base, "residual_max": F.report.residual_max, "faded": len(F.report.faded),
                       "on_feature": len(F.report.on_feature), "clamped": len(F.report.clamped), "grid": F.report.grid}
    report["culled"] = culled

    # ---- lettering positions decided before the contour figures, so they can avoid them
    name_min_r = 16 * s
    ranked = sorted(feats, key=lambda f: -f.value)
    phone_named = {f.name for f in ranked[:4]} if phone else None
    spot_default = {f.name: (x, y) for f, x, y, _a in c.spot_heights(feats, cs, clearance=8 * s)}
    letter: dict[str, dict] = {}
    boxes: list[tuple] = []        # (x, y, w, h) of every placed run, for contour_labels and collisions
    # which week figures print (round 3): one per run of zero weeks, then a greedy SOUND_GAP spacing in
    # course order; every week remains a kernel of the field whether or not its figure is printed
    cand = []
    i_ = 0
    while i_ < len(values):
        if values[i_] == 0:
            j_ = i_
            while j_ < len(values) and values[j_] == 0:
                j_ += 1
            cand.append((i_ + j_ - 1) // 2)
            i_ = j_
        else:
            cand.append(i_)
            i_ += 1
    show: list[int] = []
    # contour outlines (every drawn level) are exclusions for the figures: a sounding never sits on a line
    line_pts = [pt_ for q in cs for pt_ in q.pts[::2]
                if q.level in (20.0, 50.0) and not (q.level == 20.0 and q.closed and c.polyline_length(q.pts, True) < GENERALISE_20 * s)]

    def on_a_line(b):
        return any(b[0] - 2 <= px_ <= b[0] + b[2] + 2 and b[1] - 2 <= py_ <= b[1] + b[3] + 2 for px_, py_ in line_pts)

    def arc_of(i_):
        return (c.polyline_length(course[:4]) - SOUND_STOP * s) * i_ / len(values)

    zero_arcs: list[float] = []
    for i_ in sorted(cand, key=lambda i: (-values[i], i)):      # the big weeks win the space (HW 358 first)
        x, y, v = sounds[i_]
        if x >= limit_x - 8 * s:
            continue
        fw = width(f"{v}{weeks[i_].get('days', '')}", "texture")
        fb = (x - fw / 2 - 3 * s, y - 6 * s, fw + 6 * s, 12 * s)
        # standard spacing: no figure within SOUND_GAP of another on its own line of soundings (|dy| < 10)
        # and no two figure boxes touching; the culled weeks remain kernels of the field
        if any((abs(y - sounds[j_][1]) < 10 * s and abs(x - sounds[j_][0]) < SOUND_GAP * s * 0.75) for j_ in show):
            continue
        if any(_boxes_overlap(fb, ob) for ob in boxes) or on_a_line(fb):
            continue
        if v == 0:   # zeros: one per ZERO_GAP of course, clear of every non-zero figure (round 4)
            if any(abs(arc_of(i_) - a_) < ZERO_GAP * s for a_ in zero_arcs):
                continue
            if any(values[j_] and math.hypot(x - sounds[j_][0], y - sounds[j_][1]) < ZERO_CLEAR * s for j_ in show):
                continue
            zero_arcs.append(arc_of(i_))
        show.append(i_)
        boxes.append(fb)
    if not phone:   # the pencil note's box is reserved early so names and contour figures keep clear of it
        nw_ = width(NOTE_TEXT, "note")
        ang_ = math.radians(NOTE_AT[2])
        boxes.append((NOTE_AT[0] - 2, NOTE_AT[1] + nw_ * math.sin(ang_) - 14, nw_ * math.cos(ang_) + 4, 14 - nw_ * math.sin(ang_) + 4))
    sz_h = 13 if not phone else 26
    for f in ranked:
        named = f.r >= name_min_r if phone_named is None else f.name in phone_named
        big = f.r >= BIG_NAME_R * s
        land = f.kind in LAND_KINDS
        hx, hy = spot_default.get(f.name, (f.x, f.y - 10 * s))
        big_shoal = (not land) and f.r >= BIG_NAME_R * s and (not phone or width(f.name, "place-water") < 1.5 * f.r)
        if f.kind == "harbour":
            hx, hy = f.x, f.y - 0.84 * f.r - 6 * s           # the basin and the anchorage take the middle
        elif named and land and not big:
            hx, hy = f.x, f.y + 4 * s                        # on the land, the name offshore below
        elif named and big_shoal:
            hx, hy = f.x, f.y - 6 * s                        # name inside the bank, under the height
        elif named and not land:
            hx, hy = f.x, f.y - 3 * s
        elif named and big:
            hx, hy = (f.x, f.y - 8 * s) if not phone else (f.x, f.y - 0.84 * f.r - 8)
        name_pos = None
        if named:
            if f.kind == "harbour":
                name_pos = (f.x, f.y + 0.84 * f.r + (16 if not phone else 30), "middle")
            elif land and big:
                name_pos = (f.x, f.y + (16 if not phone else 12), "middle")   # on the land
            elif big_shoal:
                name_pos = (f.x, f.y + (18 if not phone else 30), "middle")
            elif land:
                name_pos = (f.x, f.y + 1.2 * f.r + (14 if not phone else 26), "middle")
            else:
                name_pos = (f.x, f.y + f.r + (16 if not phone else 26), "middle")
        role = ("label" if not phone else "place-land") if land else "place-water"
        size = (17 if (f.kind == "harbour" and not phone) else None)   # the harbour leads the hierarchy
        hw = width(f"{f.value}{f.sub if f.sub is not None else ''}", "label")
        boxes.append((hx - hw / 2, hy - sz_h * 0.8, hw, sz_h))
        if name_pos:
            nw = width(f.name.upper() if (land and not phone) else f.name, role, size=size,
                       tracking=((1.0 if big else caps_track) if (land and not phone) else None))
            nh = (17 if not phone else 30)
            nx_, ny_, anc = name_pos

            def box_at(x, y, a):
                x0 = x - nw / 2 if a == "middle" else (x - nw if a == "end" else x)
                return (x0, y - nh * 0.8, nw, nh)

            def clashes(b):
                if any(_boxes_overlap(b, ob) for ob in boxes):
                    return True
                if b[1] + b[3] > drawable[1] + drawable[3] - 6 or b[0] < drawable[0] + 4 or b[0] + b[2] > band[0] - 4:
                    return True
                # another feature's disc (inflated by its r) crossing the box anywhere, not just at its centre
                for o in feats:
                    if o is f:
                        continue
                    cx_ = min(max(o.x, b[0]), b[0] + b[2])
                    cy_ = min(max(o.y, b[1]), b[1] + b[3])
                    if math.hypot(cx_ - o.x, cy_ - o.y) < o.r * 1.15 + 2:
                        return True
                return False

            nb = box_at(nx_, ny_, anc)
            if nb[0] + nb[2] > band[0] - 6:                 # a name never runs into the unsurveyed band
                nx_ -= nb[0] + nb[2] - (band[0] - 6)
                name_pos = (nx_, ny_, anc)
                nb = box_at(nx_, ny_, anc)
            if clashes(nb) and (phone or f.kind != "harbour") and (phone or not (land and big)) and not big_shoal:
                above = f.y - (1.2 * f.r if land else f.r) - 6 * s
                right = (f.x + 1.2 * f.r + 8 * s, f.y + 4 * s, "start")
                left = (f.x - 1.2 * f.r - 8 * s, f.y + 4 * s, "end")
                left_low = (f.x - 1.2 * f.r - 8 * s, f.y + 0.6 * f.r + 8 * s, "end")
                for cand_ in ((nx_, above, anc), left, left_low, right):
                    nb2 = box_at(*cand_)
                    if not clashes(nb2):
                        name_pos, nb = cand_, nb2
                        break
            boxes.append(nb)
        letter[f.name] = {"height": (hx, hy), "name": name_pos, "role": role, "size": size, "big": big, "land": land,
                          "named": named}
    k.exclude("band", *band)
    k.exclude("rose", *rose_box)

    # ================================================================ drawing
    defs, body = [], []
    pd, pb = c.paper(w, h, theme, ed.name, jit)
    defs.append(pd)
    body.append(pb)
    defs.append(c.symbol_defs(theme, prefix, ed.name))
    symbols_used: set[str] = set()

    def use(name, x, y, **kw):
        symbols_used.add(name)
        return c.use(name, x, y, prefix, **kw)

    # ---- t = 0: the blank form — frame, band (hatch emitted after the tints, on top), rose rings
    body.append(c.frame(w, h, theme, "broken", gaps=[("right", band[1], band[1] + band[3])], rules=RULES[sc]))
    ud, ub = c.unsurveyed_band(band[0], band[1], band[2], band[3], theme, jit, None, ramp_w=40 * s, clip_id="unsurv")
    defs.append(ud)
    def up(text, x, ymid, role, **kw):
        # a −90° label centred on ymid, anchored at its start: typeset registers rotated runs about the
        # start of the run, so a middle anchor would log the box 0.5·width away from where it is drawn
        caps_ = kw.get("caps") or role == "label-caps"
        wdt = width(text.upper() if caps_ else text, "label" if role == "label-caps" else role,
                    tracking=caps_track if caps_ else None)
        return lbl(text, x, ymid + wdt / 2, role, anchor="start", rotate=-90, **kw)

    band_labels = [up("UNSURVEYED", band[0] + (band[2] * 0.6 if not phone else 40), band[1] + band[3] / 2, "label-caps")]
    if not phone:
        band_labels.append(up(limit_label, band[0] + 16, band[1] + band[3] / 2, "label", caps=True))
        band_labels.append(up("soundings along the course: commits per week", band[0] + 34, band[1] + band[3] / 2,
                              "label-italic", fill=theme.ink2))
    else:   # inside the hatch like UNSURVEYED, clear of the lagoon's dashed shoals (round 3, addendum 2)
        band_labels.append(up("SMALL-SCALE EDITION", band[0] + 90, band[1] + band[3] / 2, "label", fill=theme.ink2, caps=True))

    # ---- tints (A 1.0, B 1.3), generalised: closed 10-rings under GENERALISE_10 are not tinted
    gen10 = GENERALISE_10[sc]

    def ring_len(pts):
        return c.polyline_length(pts, True)

    def fill_level(level, color, min_len: float = 0.0):
        closed = [q for q in cs if q.level == level and q.closed]
        shallow = [q for q in closed if q.shallow_inside and ring_len(q.pts) >= min_len]
        polys = [q.pts for q in shallow]
        for q in closed:
            if q.shallow_inside:
                continue
            cx_, cy_ = c.polygon_centroid(q.pts)
            if any(c.point_in_polygon(cx_, cy_, sp.pts) for sp in shallow):
                polys.append(q.pts)
        if not polys:
            return ""
        d = "".join(c.compact_path(p, True, 1 if ring_len(p) < 300 * s else 2) for p in polys)
        return f'<path d="{d}" fill="{color}" fill-rule="evenodd"/>'

    body.append(tl.fade_in(fill_level(10.0, theme.shallow_a, gen10 * s), 1.0, 1.0, rise=0))
    body.append(tl.fade_in(fill_level(5.0, theme.shallow_b), 1.3, 1.0, rise=0))
    land_svg = [fill_level(0.0, theme.land), c.coastline(cs, theme)]
    big_land = [f for f in feats if f.kind in LAND_KINDS and (f.r >= BIG_NAME_R * s or f.kind == "harbour")]
    for poly in c.level_polygons(cs, 0.0):
        if any(c.point_in_polygon(f.x, f.y, poly) for f in big_land):
            land_svg.append(c.coast_vignette(poly, theme, jit))
    water_svg = []
    shoal_pts = [(f.x, f.y) for f in feats if f.kind == "shoal"]
    if shoal_pts:
        water_svg.append(c.danger_lines(cs, 5.0, theme, jit, inside=shoal_pts))
    # the double shoal: rustmapper's ground as charted from the sitemap (pecked, PA) beside the survey
    pa_label = ""
    if vessel_ground is not None and not phone:
        poly = drawn.get(vessel_ground.name)
        if poly:
            dx, dy = PA_SHIFT
            water_svg.append(f'<path d="{c.compact_path(poly, True, 1)}" fill="none" transform="translate({dx} {dy})" '
                             f'{c.stroke("PEN", theme.ink, INK["mid"], "PECK", jit.sub("pa"))}/>')
            wpt = min(poly, key=lambda p: p[0])
            pa_label = lbl("PA", wpt[0] + dx - 3, wpt[1] + dy + 4, "label-italic", fill=theme.ink2, anchor="end")
    land_svg.append(use("anchorage", *course[-1]))
    if not phone:
        cov = COVERAGE
        land_svg.append(f'<rect x="{_fmt(cov[0])}" y="{_fmt(cov[1])}" width="{_fmt(cov[2])}" height="{_fmt(cov[3])}" fill="none" '
                        f'{c.stroke("HAIR", theme.ink, 0.7, "RESTRICT", caps="butt")}/>')
    if profile is not None:
        land_svg.append(use("station", profile.x, profile.y))
    body.append("".join(land_svg))                        # land is a sheet at t = 0 (round 2 addendum)
    body.append(tl.fade_in("".join(water_svg), 1.6, 0.65, rise=0))
    # the unsurveyed hatch lies over the faded tints at the limit of survey; the contours over it
    body.append(ub)
    body.append("".join(band_labels))

    # ---- contours draw in, deep first (0.2 + 0.12·i, 1.6 s); the approximate fringe fades with them
    approx_clip = (geo.p(1040, 0)[0], drawable[1], limit_x + UNSURVEYED_FADE * s - geo.p(1040, 0)[0], drawable[3])
    breaks = c.contour_labels(cs, min_len=220 * s, gap=20 * s,
                              exclusions=[(band[0], 0, w - band[0], h), rose_box] + boxes,
                              levels=(10.0, 20.0, 50.0)) if not phone else []
    breaks = [b for b in breaks if not (b[0].level == 10.0 and b[0].closed and ring_len(b[0].pts) < gen10 * s)]
    for i, lv in enumerate((50.0, 20.0, 10.0, 5.0)):
        begin = 0.2 + 0.12 * i
        for short in (True, False):
            sub = [q for q in cs if q.level == lv and ((q.length < 300 * s) == short)]
            if lv == 10.0:
                sub = [q for q in sub if not (q.closed and ring_len(q.pts) < gen10 * s)]
            if lv == 20.0:
                sub = [q for q in sub if not (q.closed and ring_len(q.pts) < GENERALISE_20 * s)]
            if not sub:
                continue
            svg = c.draw_contours(sub, INDEX, theme, approx_clip=approx_clip,
                                  breaks=[b for b in breaks if b[0].level == lv], min_len=40 * s,
                                  every=1 if short else 2)
            for m in re.finditer(r"<path ([^>]*)/>", svg):
                attrs = m.group(1)
                if "stroke-dasharray" in attrs:
                    body.append(tl.fade_in(f"<path {attrs}/>", begin + 0.5, 0.65, rise=0))
                else:
                    body.append(tl.draw_in(attrs, 1.6, begin))

    # ---- the course: pecked line and waypoint fixes (with the land), bearings later
    body.append(tl.fade_in(c.course(course, theme, jit, pecked=True, prefix=prefix, bearings=False), 1.6, 0.65, rise=0))
    symbols_used.add("waypoint")

    # ---- soundings in course order (1.4 + 0.04·k); none printed in the band; opacity thins toward it
    printed = 0
    course_len = c.polyline_length(course)
    cum = [0.0]
    for a_, b_ in zip(course, course[1:]):
        cum.append(cum[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))

    def pass_time(x, y) -> float:
        """When the boat passes abeam of (x, y): arc fraction along the course through the sail's ease,
        snapped to the 0.5 s grid inside [SAIL begin, SAIL end]."""
        best, arc = math.inf, 0.0
        for li_, (a_, b_) in enumerate(zip(course, course[1:])):
            dx_, dy_ = b_[0] - a_[0], b_[1] - a_[1]
            L2 = dx_ * dx_ + dy_ * dy_ or 1
            t_ = max(0.0, min(1.0, ((x - a_[0]) * dx_ + (y - a_[1]) * dy_) / L2))
            d_ = math.hypot(x - (a_[0] + t_ * dx_), y - (a_[1] + t_ * dy_))
            if d_ < best:
                best, arc = d_, cum[li_] + t_ * math.sqrt(L2)
        u = arc / course_len if course_len else 0.0
        t = SAIL[0] + SAIL[1] * ease_inverse("settle", u)
        if phone:   # the phone boat steps every 4 s: the lead goes down on the same instants (no extra repaints)
            t = SAIL[0] + 4.0 * round((t - SAIL[0]) / 4.0)
        return min(SAIL[0] + SAIL[1], max(SAIL[0], tl.snap(t)))

    phone_show = show if not phone else [i_ for k_, i_ in enumerate(show) if k_ % 2 == 0]
    for i_ in sorted(phone_show):
        x, y, v = sounds[i_]
        wk = weeks[i_]
        frag = snd(v, x, y + (4 if not phone else 6), sub=(wk.get("days") if v else None), truth="measured",
                   key=f"week:{wk.get('start', i_)}", fill=theme.ink)
        if phone:   # one repaint per fix on the phone: the figures are printed, the boat alone steps
            body.append(frag)
        else:
            body.append(tl.reveal(frag, pass_time(x, y)))  # the lead goes down where the ship is
        printed += 1
    report["soundings_printed"] = printed
    figs = []
    for q, i0, i1 in breaks:
        x, y, ang = c.break_anchor(q, i0, i1)
        figs.append(lbl(str(int(q.level)), x, y + 3.5, "contour-figure", anchor="middle", rotate=ang, fill=theme.ink2))
    if figs:
        body.append(tl.fade_in("".join(figs), 1.4, 0.4, rise=0))

    # ---- the rose: card settles at 2.0 (rotate +12 → −4 → 0, 1.6 s, sea); lettering is static
    rose_geo = c.two_ring_rose(rose_cx, rose_cy, rose_r, theme, hours, modal)
    settle = tl.xform("rotate", [f"12 {rose_cx} {rose_cy}", f"-4 {rose_cx} {rose_cy}", f"0 {rose_cx} {rose_cy}"],
                      1.6, 2.0, ease="sea", key_times=[0, 0.45, 1], name="rose_settle")
    body.append(f'<g transform="rotate(0 {rose_cx} {rose_cy})">{settle}{rose_geo}</g>')
    rose_text = [lbl("N", rose_cx, rose_cy - rose_r - 17, "label", anchor="middle")]
    ri = rose_r - 24
    for hh in (0, 6, 12, 18):
        a = math.radians(hh * 15 - 90)
        rr = ri + 10
        rose_text.append(lbl(f"{hh:02d}", round(rose_cx + rr * math.cos(a), 1), round(rose_cy + rr * math.sin(a) + 4, 1),
                             "label", anchor="middle"))
    body.append("".join(rose_text))
    var_lines = [f"VAR {modal:02d}h ({var_year})"]
    if not phone:
        var_lines.append("AUTHOR'S LOCAL TIME")
    var_svg = "".join(lbl(t, rose_cx, rose_cy + rose_r + 30 + j * 16 * (1 if not phone else 2), "label", anchor="middle",
                          fill=theme.ink2, tracking=caps_track, truth="measured" if j == 0 else None,
                          key="variation" if j == 0 else None)
                      for j, t in enumerate(var_lines))

    # ---- names and spot heights, by rank (2.2 + 0.1·rank)
    for rank, f in enumerate(ranked):
        L_ = letter[f.name]
        parts = []
        hx, hy = L_["height"]
        if phone and not L_["named"]:
            parts.append(snd(f.value, hx, hy, sub=f.sub, truth="measured", key=f"commits:{f.alias}", fill=theme.ink))
        else:
            parts.append(snd(f.value, hx, hy, sub=f.sub, role="label", truth="measured", key=f"commits:{f.alias}"))
        if L_["name"]:
            nx_, ny_, anc = L_["name"]
            if L_["land"] and not phone:
                parts.append(lbl(f.name, nx_, ny_, "label", anchor=anc, caps=True, size=L_["size"],
                                 tracking=(1.0 if L_["size"] else caps_track)))
            elif L_["land"]:
                parts.append(lbl(f.name, nx_, ny_, "place-land", anchor=anc))
            else:
                parts.append(lbl(f.name, nx_, ny_, "place-water", anchor=anc))
        body.append("".join(parts))                       # names stand at t = 0 (round 2 addendum)

    # ---- the name (discrete, two words), the thesis (3.1)
    if not phone:
        nx, ny = 64, 222
        ben = k.text("Ben", nx, ny, "display", edition=ed, scale=sc)
        wb = k.text_width("Ben ", "display", edition=ed, scale=sc)
        russ = k.text("Russell", nx + wb, ny, "display", edition=ed, scale=sc)
        body.append(ben + russ + k.text(thesis, 72, 306, "thesis", fill=theme.ink2, edition=ed, scale=sc))
    else:
        nx, ny = 40, 150
        ben = k.text("Ben", nx, ny, "display", edition=ed, scale=sc)
        wb = k.text_width("Ben ", "display", edition=ed, scale=sc)
        russ = k.text("Russell", nx + wb, ny, "display", edition=ed, scale=sc)
        body.append(ben + russ)
        words = thesis.split()
        cut = len(words) // 2 + 1
        l1, l2 = " ".join(words[:cut]), " ".join(words[cut:])
        body.append(k.text(l1, 44, 222, "thesis", fill=theme.ink2, edition=ed, scale=sc)
                    + k.text(l2, 44, 268, "thesis", fill=theme.ink2, edition=ed, scale=sc))

    # ---- title block, source diagram, margin captions (3.3)
    block = []
    if not phone:
        bx = 268
        ver = edition_d.get("version") or "—"
        ed_date = edition_d.get("date")
        ed_line = f"CHART NO. {N} · EDITION {ver}" + (f" · {_month(ed_date)}" if ed_date else "") + " · IALA REGION B"
        rows_t = [
            (560, f"THE OPEN WEB · FROM SURVEYS {first_year}–{upd_year}", "label", theme.ink, None, None),
            (616, "SOUNDINGS IN COMMITS · DATUM: MAIN", "label", theme.ink2, None, None),
            (636, ed_line, "label", theme.ink2, "measured", "chart-edition"),
            (656, f"CORRECTED THROUGH NOTICE {notices_n}", "label", theme.ink2, "measured", "notices"),
        ]
        for y, t, role, fill, truth, key in rows_t:
            block.append(lbl(t, bx, y, role, anchor="middle", fill=fill, caps=True, within=TITLE_BOX, truth=truth, key=key))
        block.append(lbl(role_line, bx, 586, "label", anchor="middle", fill=theme.ink, caps=True, within=TITLE_BOX))
        zones = [c.Zone("A", [(0, 0), (0.55, 0), (0.55, 1), (0, 1)], 0.9),
                 c.Zone("B", [(0.55, 0), (1, 0), (1, 0.5), (0.55, 0.5)], 0.5),
                 c.Zone("C", [(0.55, 0.5), (1, 0.5), (1, 1), (0.55, 1)], 0.2)]
        block.append(c.source_diagram(470, 548, 120, 68, zones, theme, jit, lbl))
        for j, src in enumerate((data.get("sources") or [])[:3]):
            first = src.get("first")
            line = f"{src.get('letter', '?')}  {src.get('name', '')}" + (f" · {first[:4]}–" if first else "")
            block.append(lbl(line, 470, 632 + 16 * j, "label", fill=theme.ink2, caps=True, within=TITLE_BOX))
        k.exclude("title-block", *TITLE_BOX)
        # outside the neat line: unit line (the one label-caps run), chart number, folio, imprint, small corrections
        block.append(lbl(unit_line, 640, 14, "label-caps", anchor="middle", fill=theme.ink, key="unit"))
        block.append(lbl(str(N), 1262, 14, "label", anchor="end", fill=theme.muted, truth="measured", key="chart-number"))
        taken = data.get("taken") or (data.get("updated_at") or "")[:10]
        imprint = (f"Published at github.com/{login} · {_date(taken)} · "
                   f"under the superintendence of B. Russell · redrawn nightly")
        block.append(lbl(imprint, 1256, 735, "label", anchor="end", fill=theme.ink2, caps=True))
        # bottom-left: the folio, then the small corrections (a range when the five are consecutive)
        corr = data.get("corrections") or {}
        folio = f"CHART NO. {N} · SHEET 1"
        if corr:
            yr = max(corr)
            nums = [int(e.get("n")) for e in corr[yr] if e.get("n") is not None][-5:]
            if nums:
                run_ = all(b_ - a_ == 1 for a_, b_ in zip(nums, nums[1:]))
                lst = f"{nums[0]}–{nums[-1]}" if run_ and len(nums) > 2 else ", ".join(str(n_) for n_ in nums)
                folio += f" · Small corrections {yr} — {lst}"
        block.append(lbl(folio, 24, 735, "label-caps", fill=theme.ink2, key="folio"))
    else:
        bx = 360
        ver = edition_d.get("version") or "—"
        rows_t = [
            (770, f"THE OPEN WEB · FROM SURVEYS {first_year}–{upd_year}", "label", theme.ink, False, None, None),
            (834, unit_line + " · DATUM: MAIN", "label-caps", theme.ink2, True, None, None),
            (866, f"CHART NO. {N} · EDITION {ver} · IALA REGION B", "label", theme.ink2, False, "measured", "chart-edition"),
        ]
        for y, t, role, fill, is_caps_role, truth, key in rows_t:
            if is_caps_role:
                block.append(k.text_use(t, bx, y, "label-caps", anchor="middle", fill=fill, edition=ed, scale=sc, key="unit"))
            else:
                block.append(lbl(t, bx, y, role, anchor="middle", fill=fill, caps=True, truth=truth, key=key,
                                 within=(19, 740, 682, 140)))
        block.append(lbl(role_line, bx, 804, "label", anchor="middle", fill=theme.ink, caps=True, within=(19, 740, 682, 140)))
        k.exclude("title-block", 19, 740, 682, 140)
    block.append(var_svg)
    body.append("".join(block))                             # the title block is printed, not revealed

    # ---- mark labels, fix labels, pencil notes, then bearings clear of all of them (by 1.5 s)
    late = []
    late_boxes: list[tuple] = []
    fixes_svg: list[str] = []       # the dated fixes surface as the boat passes them (round 3)

    def late_text(text, x, y, role, anchor="start", rotate=0, **kw):
        """A late label, its box recorded so the bearings can keep clear of it."""
        wdt = width(str(text).upper() if kw.get("caps") else str(text), role,
                    tracking=caps_track if kw.get("caps") else None)
        hgt = 17 if role == "note" else 13
        x0 = x - wdt / 2 if anchor == "middle" else (x - wdt if anchor == "end" else x)
        if rotate:
            ang = math.radians(rotate)
            xs = [x0, x0 + wdt * math.cos(ang)]
            ys = [y, y + wdt * math.sin(ang)]
            late_boxes.append((min(xs), min(ys) - hgt * 0.8, max(xs) - min(xs), max(ys) - min(ys) + hgt))
        else:
            late_boxes.append((x0, y - hgt * 0.8, wdt, hgt))
        return lbl(text, x, y, role, anchor=anchor, rotate=rotate, **kw)

    # the lateral pair: labels slope (floating things), characters as charted
    r2 = geo.pi(*MARK_R2)
    g1 = geo.pi(*MARK_G1)
    ms = 1.0 if not phone else 1.3
    if not phone:   # the phone entrance is 24 px wide: the bodies and lit cores carry the marks there
        late.append(late_text('R "2" Fl R 4s', r2[0], r2[1] - 22 * ms, "label-italic", fill=theme.ink, anchor="middle"))
        late.append(late_text('G "1" Fl G 4s', g1[0] + 10 * ms, g1[1] + 14 * ms, "label-italic", fill=theme.ink))
    # dated fixes: the first-commit month of the feature each fix is taken off (WP2 off rustmapper, WP4 the harbour)
    for wp, f, side in ((course[1], vessel_ground, -1), (course[3], harbour, 1)):
        if f is None or phone:
            continue
        rr = repo_of.get(f.name, {})
        first = rr.get("first")
        if first:
            if side < 0:     # NW of WP2, lifted until clear of the sounding figures
                fw = width(_month(first), "label")
                fy = wp[1] - 20
                for _ in range(8):
                    fb = (wp[0] - 14 - fw, fy - 11, fw, 14)
                    if not any(_boxes_overlap(fb, b) for b in boxes):
                        break
                    fy -= 6
                fixes_svg.append(tl.reveal(late_text(_month(first), wp[0] - 14, fy, "label", fill=theme.ink2, truth="measured",
                                                     key=f"first:{f.alias}", anchor="end"), pass_time(*wp)))
            else:
                fixes_svg.append(tl.reveal(late_text(_month(first), wp[0] + 7, wp[1] - 10, "label", fill=theme.ink2,
                                                     truth="measured", key=f"first:{f.alias}"), pass_time(*wp)))
    if not phone:
        nxp, nyp, rot = NOTE_AT
        late.append(late_text(NOTE_TEXT, nxp, nyp, "note", fill=theme.muted, rotate=rot))   # the tail points; no leader
        late.append(pa_label)
        if vessel_ground is not None and pa_label:
            late_boxes.append((vessel_ground.x + PA_SHIFT[0] - vessel_ground.r - 20, vessel_ground.y + PA_SHIFT[1] - 8, 20, 14))
        late.append(late_text("SEE SHEET 3", *SEE_SHEET, "label", fill=theme.muted, caps=True))
    if ctx.no_sounding or data.get("no_sounding"):
        taken = data.get("taken") or (data.get("updated_at") or "")[:10]
        note = f"no soundings tonight — figures as surveyed {_date(taken)}"
        if not phone:   # caps: the note shares the sheet's lettering (a lowercase italic set costs 8 KB of defs)
            late.append(lbl(note, 340 - width(note.upper(), "label", tracking=caps_track) / 2, 703, "label",
                            fill=theme.muted, rotate=-3, caps=True))
        else:
            late.append(lbl(note, 40, 735, "label", fill=theme.muted, rotate=-2, caps=True))
    # bearings: 54 px off the leg (outside the sounding rows), the side and distance that clear every box
    legs = list(zip(course, course[1:]))
    for li, (p, q) in enumerate(legs):
        if phone:
            break
        brg = c.compass_bearing(p, q)
        text = f"{round(brg) % 360:03d}°"
        bw = width(text, "label")
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
        nx_, ny_ = -(q[1] - p[1]) / L, (q[0] - p[0]) / L
        if li == len(legs) - 1:
            cands = [(mx - 20 * s, my + 28 * s)]             # the entrance is busy: label in the basin's south arm
        else:
            cands = [(mx + nx_ * d * side, my + ny_ * d * side) for d in (54 * s, 66 * s, 78 * s) for side in (1, -1)]
        for bx_, by_ in cands:
            bb = (bx_ - bw / 2, by_ - 6, bw, 13)
            if bx_ + bw / 2 > limit_x - 10:
                continue
            if any(_boxes_overlap(bb, ob) for ob in boxes + late_boxes + [rose_box]):
                continue
            if li < len(legs) - 1 and any(
                    math.hypot(min(max(o.x, bb[0]), bb[0] + bb[2]) - o.x, min(max(o.y, bb[1]), bb[1] + bb[3]) - o.y) < o.r * 1.15 + 2
                    for o in feats):
                continue
            late.append(late_text(text, round(bx_, 1), round(by_ + 4, 1), "label", anchor="middle", truth="measured",
                                  key="bearing"))
            break
    body.append(tl.fade_in("".join(late), 1.1, 0.4, rise=0))      # the proof layer is on the sheet by 1.5 s
    body.append("".join(fixes_svg))

    # ---- lateral marks with their lights (lit from t = 0; G begins 0, R begins 2; one loop each)
    lights = []
    halo_r = 14 * ms if night else None
    for (pos, kind, lit_id, char, bg, top) in ((r2, "nun", "r2-lit", "Fl R 4s", 2.0, 16), (g1, "can", "g1-lit", "Fl G 4s", 0.0, 15)):
        core = c.lit_core(pos[0], pos[1] - top * ms, theme, lit_id, r=LIGHT_R * ms, halo_r=halo_r, prefix=prefix)
        flash = tl.flash(char, begin=bg, still="lit", name=lit_id.replace("-lit", "-flash")) if not phone else ""
        body.append(tl.fade_in(use(kind, pos[0], pos[1], scale=ms) + f"<g>{flash}{core}</g>", 1.6, 0.65, rise=0))
        lights.append({"id": f"{NAME}-{lit_id}", "character": char, "color": theme.light_core,
                       "body": theme.accent if kind == "nun" else theme.ok, "bbox": [pos[0] - 8, pos[1] - 20, 16, 22]})
    report["lights"] = lights

    # ---- the boat: sails WP1 → WP5 over 4–28 s and anchors (desk); plotted as 7 fixes (phone)
    if not phone:
        d = c.smooth_path(course, False, every=1)
        sail = tl.sail(d, SAIL[0], SAIL[1], n=64, ease="settle", mast_x=3.0, pitch=-4.0, name="sail")
        P = c.SLOOP_DETAIL
        hull = (f'<path d="{P["hull"]}" fill="{theme.ink}"/>'
                f'<path d="{P["mast"]}{P["tiller"]}" fill="none" {c.stroke("PEN", theme.ink)}/>'
                f'<circle r="1.2" fill="{theme.ink}"/>')
        sails = (f'<path d="{P["main"]}" fill="{theme.accent}"/>'
                 f'<path d="{P["jib"]}" fill="{theme.paper}" {c.stroke("PEN", theme.ink)}/>')
        boat = sail.wrap(f'<g transform="scale({_fmt(BOAT_SCALE)})">{hull}{sails}</g>', pitch=-4.0, gid="boat")
        body.append(tl.reveal(boat, SAIL[0]))
        report["sail"] = {"begin": SAIL[0], "end": sail.end, "facing": sail.facing, "tacks": sail.tacks,
                          "scale": BOAT_SCALE}
    else:
        pts = [(E.I(x), E.I(y)) for x, y, _h in c.course_samples(course, 7)]
        glyph = f'<g transform="scale(-1 1)">{use("sloop-glyph", 0, 0, scale=1.4)}</g>'
        # seven fixes every 4 s as ONE discrete translate (the waypoint ⊙ are already plotted by course()):
        # exactly one repaint per fix, 0.25/s, the phone budget (MASTERPLAN 7.3)
        vals = [f"{x} {y}" for x, y in pts]
        kts = [i / (len(pts) - 1) for i in range(len(pts))]
        step = tl.xform("translate", vals, 24.0, SAIL[0], key_times=kts, discrete=True, cls="fixes", name="sail")
        at = pts[-1] if ed.still else pts[0]
        body.append(f'<g transform="translate({at[0]} {at[1]})">{step}{glyph}</g>')
        report["sail"] = {"begin": SAIL[0], "end": SAIL[0] + 24.0, "fixes": len(pts)}

    report["symbols_used"] = sorted(symbols_used)
    report["opening_end_s"] = opening_end
    defs.append(k.glyph_defs())
    return E.svg(ed, w, h, "".join(body), "".join(defs), sheet=NAME)


def alt(data, cfg) -> str:
    n = int(data.get("repo_count") or len(data.get("repos") or []))
    thesis = (cfg.get("copy", {}) if cfg else {}).get("thesis", "I survey a web that is wrong about itself.")
    return (f"Chart of Ben Russell's {n} repositories, titled: {thesis} "
            "Right margin unsurveyed. A boat sails in and anchors.")


# ---------------------------------------------------------------- build-report hook
def _report_hook(ctx, svg_text: str, entry: dict) -> None:
    if getattr(ctx, "sheet", None) != NAME:
        return
    x = ctx.extra
    for key in ("features", "bracket_failures", "lights", "symbols_used"):
        if key in x:
            entry[key] = x[key]
    entry["hero"] = {kk: x[kk] for kk in ("field", "place", "unclosed", "bracket", "soundings_printed", "culled", "sail",
                                          "course_too_close")
                     if kk in x}


def _register_hook() -> None:
    """Append the hook to the runner's `report_hooks`, whether it was imported as `build_assets` or
    is running as `__main__` (python3 scripts/build_assets.py)."""
    import sys
    for modname in ("build_assets", "__main__"):
        m = sys.modules.get(modname)
        hooks = getattr(m, "report_hooks", None)
        if isinstance(hooks, list) and _report_hook not in hooks:
            hooks.append(_report_hook)


_register_hook()
