"""hero.py — Sheet 1, "Chart No. N": one person's public repositories, composed by hand around Scrapy Harbor (v10).

Soundings in commit-days (round 4, D2): a repository's drawn area at the 5-contour is proportional to the
days it was committed to (solve_radii, ±8 %) and its printed figure is that count, upright, no subscript.
The repositories with NAMED_MIN commit-days or more are named features with hand-set slots in chart.toml
(D3); their radii follow the data and their places never move. Every other repository is a rock on the
fringe south-west of the archipelago: a mark, no name, no figure, counted in the title block. The 52
weekly totals stay the kernels that shape the sounded bank along the course from the limit of survey into
the harbour, but only the high-water week prints, flagged as a sweep when the data flags it (D5). Tints at
5 and 10, generalised; no 20/50 contours, no contour figures, no PA outline, no inset, no bearings (D4).

One cartouche top-left on one left edge: the name, the thesis, then the title lines at 25 and 19 tracked
+2.0; under it the rose as a 24-hour clock whose ticks are the hour histogram of commit-days. The chart
fills the rest: the harbour large and centre-right, rustmapper's ground beside it toward the limit of
survey, the course from the limit into the harbour, the boat sailing in once (4–28 s) and anchoring; the
two lateral lights are the only loop afterwards. Night is redrawn at +20 % weight (D6).

Every glyph goes through typeset (ctx.k), every animation through the Timeline (ctx.tl), every line through
chartlib. The phone editions are the same composition redrawn at the phone scale from the phone slots.
"""
from __future__ import annotations

import datetime as dt
import math
import os
import re

import chartlib as c
import edition as E
from timeline import ease_inverse
import tokens
from tokens import INK
import gazetteer

NAME = "hero"
KIND = "chart"
SIZES = {"desk": (1280, 740), "phone": (720, 900)}
EDITIONS = None   # the runner's default six plus HERO_EXTRA (phone stills)

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the title lines, the margin captions, the band's UNSURVEYED and the land names are set upper-case through "
     "role `label` with explicit tracking (caps 1.6, title lines 2.0; phone 1.4); only the unit line is role `label-caps`",
     "check_type allows one label-caps run per sheet; a period title block is five caps lines"),
    ("Land names in condensed caps, water names in serif italic",
     "islands and the harbour are lettered upright in Plex Sans Condensed (25 px for the harbour, else 19), banks and "
     "shoals in Instrument Serif italic 25",
     "the glyph-defs budget (40 KB) cannot carry a serif register for both; upright/italic still means land/water"),
    ("Role line in condensed caps 19", "the plain register in the chart's own face, ink, in the cartouche",
     "the serif-italic 22 run cost 32 KB inline; decision 7 calls this line the plain register"),
    ("No margin graticule", "the frame carries minute bars only; no labelled meridians or parallels",
     "the sheet has no latitude or longitude, so labelled margin ticks would be invented geometry"),
    ("Phone lights lit, not flashing", "the phone editions draw both lights lit and cull the character labels",
     "MASTERPLAN 7.3: hero-phone ≤ 0.25 repaints/s after 6 s; two Fl 4s lights alone are 1/s"),
    ("Pencil note without a notice number", "\"sitemap.xml lies again\" stands alone, scribbled by the limit of survey",
     "chart.toml's notices carry no sitemap item; a tie to Notice 3 would be invented"),
    ("Sounded bank softened, not smoothed (round 2, option b + a)",
     "the 52 week kernels take h = 36 (not 30) and the four rows cycle −36 / +18 / −18 / +36 with ±5 px jitter keyed "
     "by index, so the shallow water of the zero weeks is one broad irregular bank; amplitudes stay solved so the one "
     "printed figure is the field's own value",
     "36 of 52 weeks are 0: the honest field is shallow along the course; it must read as a bank, not a road"),
    ("Contours generalised", "closed 10-contours shorter than 520 px (phone 280) and 5-rings shorter than 150 (90) are "
     "neither drawn nor tinted",
     "a 10-ring around every feature is a bubble chart; small-scale charts drop rings the pen cannot carry"),
    ("Title and land static at t=0 (five-second test; 7.2 t=0 floor)",
     "name, thesis, title lines, imprint, frame, rose, band, land masses, coastlines and feature names are present "
     "at load with no fade; only the water draws in (contours deep-first, tints, danger lines, rocks, course, marks), "
     "then the boat sails 4–28 s; the opening still ends at 4.0 s",
     "orchestrator decision, round 2: a reader must never land on blank paper"),
    ("Marginalia moved (round 3)", "small corrections bottom-left, chart number top-right, folio folded into the "
     "imprint line bottom-centre", "chart practice (13's re-crit); decision 27 put the folio bottom-left"),
    ("Lobed features", "each feature is its main kernel plus 3–6 lobes/dents, Jitter keyed by repo name, scaled by r",
     "no two islands share a silhouette; area ∝ commit-days is solved on the drawn 5-polygon, lobes included"),
    # ---- round 4 (v10): decisions D2–D7
    ("The measure is commit-days (D2)",
     "area ∝ repos[].commit_days at K_AREA px² per day (Scrapy's 26 days draw at r ≈ 80); the printed figure is the "
     "day count, upright, no months subscript; the unit line says SOUNDINGS IN COMMIT-DAYS",
     "commits crowned a two-day burst and a housekeeping sweep; commit-days put the two flagships first and second "
     "and are immune to both (crit-infodesign §1, DECISIONS D2)"),
    ("Composed by hand, driven by data (D3)",
     "the named features (commit_days ≥ 7, nine today) take the desk and phone slots on their chart.toml [[features]] "
     "entry; the rest are rocks along the hand-set fringe polyline [hero].rocks_*, counted in the title block; the arc "
     "placer, the Halton fallback, the lock file and the drift warnings are not called; a feature whose data grows "
     "changes its figure, never its place",
     "the mid-sheet scatter of twenty islets was the strongest tell of a generated drawing (crit-type §2)"),
    ("Rocks, not islets (D3)",
     "a repository under seven commit-days is one rock mark (+ with four dots, one <path> for the fringe), no figure, "
     "no name; a repository with the days but no slot in chart.toml is a rock too and is reported (`unslotted`)",
     "an unnamed rock with no figure is chart grammar; a figure nobody can read at 870 is not honesty"),
    ("One cartouche (D4)",
     "name (display 141), thesis (41 italic), then five title lines on one left edge: 25 tracked +2.0, then 19 "
     "tracked +2.0 (role, unit · datum, edition, the repository count); the source diagram, the coverage inset and "
     "SEE SHEET 3 are gone; the rose is a 24-hour clock of r 44 under the cartouche with the hour histogram as ticks",
     "the name was a wordmark dropped on a chart; on a real chart the name is the title block (crit-type §4)"),
    ("Only the high-water week prints (D4/D5)",
     "the 52 weeks remain kernels of the field; the one printed week figure is the tide's high water, with a caption "
     "that names the sweep day when a sweep falls in that week; no other week figure, no zero, no contour figure",
     "fifty-two 11 px figures along a course with no axis were texture nobody could read (crit-infodesign §2)"),
    ("Nothing sloping, nothing unmeasured (D5)",
     "every printed figure is truth=measured and upright: the mark labels R \"2\" / G \"1\" are set in role `label`, "
     "not `label-italic`; the PA outline, the course bearings and the 20/50 contour figures are not drawn",
     "a figure that was not measured is not printed; the slant convention retires as an expression"),
    ("Night redrawn, not swapped (D6)",
     "the night build calls chartlib.set_night(True) so every stroke is ×1.2; the night land, tints and the ink2/muted "
     "swap live in tokens.py",
     "light-on-dark reads thinner and the night caption hierarchy was inverted (crit-type §1, §3)"),
    ("No 16 px type on the hero (D7)",
     "the texture floor stays for the other sheets; the hero's smallest type is 19 (phone 26)",
     "11 px shown is below reading matter at page scale"),
]

# ---------------------------------------------------------------- layout
RULES = {"desk": (24, 30), "phone": (14, 19)}
DRAWABLE = {"desk": (30, 30, 1220, 680), "phone": (19, 460, 682, 421)}   # phone: the chart under the cartouche
NAMED_MIN = 7                     # commit-days: a repository with this many is a named feature (D3); fewer, a rock
K_AREA = 773.0                    # px² of 5-contour area per commit-day: Scrapy's 26 days at r ≈ 80 (desk)
R_FIT = 84.0                      # px: the largest feature must fit under solve_radii's 90 px bound
LEVELS = (0.0, 5.0, 10.0)         # D4: no 20, no 50
INDEX = (10.0,)
ROWS = (-36, 18, -18, 36)         # sounding rows off the course, cycling across it
ROW_JITTER = 5                    # ± px, keyed by sounding index
H_SND = 36                        # sounding kernel support (see BREAKS)
CLEAR_COURSE = 78                 # features keep r + 78 from the course (rows 36 + jitter 5 + h_snd 36)
SOUND_STOP = 110                  # the soundings end this far before the entrance: the approach is the harbour's own
CELL = {"desk": 6.0, "phone": 4.0}
GENERALISE_10 = {"desk": 520, "phone": 280}   # closed 10-contours shorter than this are not drawn or tinted
GENERALISE_5 = {"desk": 150, "phone": 90}      # closed 5-rings shorter than this likewise
BIG_LAND_R = 40                   # islands from this radius carry the coast vignette
BIG_SHOAL_R = 60                  # a bank this wide carries its name inside
# the harbour cluster in units of the harbour's nominal radius about its slot: basin kernels (dx, dy, h, amp/base) —
# the bay, the mouth toward the entrance, the berth under the anchorage — the two lateral marks, the entrance (WP4)
# and the anchorage (WP5). The shape was tuned at r 52 (v9) and scales with the data.
HARBOUR = {"basin": [(0.365, -0.058, 0.577, -2.0), (0.885, 0.135, 0.5, -0.66), (0.154, -0.077, 0.423, -0.5)],
           "r2": (1.29, -0.17), "g1": (1.02, 0.63), "wp4": (1.58, 0.385), "wp5": (0.31, -0.077)}
CARTOUCHE = {"desk": (56, 56, 594, 376), "phone": (30, 48, 670, 412)}
NAME_AT = {"desk": (64, 176), "phone": (40, 150)}
THESIS_AT = {"desk": [(64, 252)], "phone": [(44, 226), (44, 272)]}
TITLE_AT = {"desk": (64, 298, 330, 30), "phone": (40, 322, 356, 30)}   # x, first baseline (big), second, pitch
TITLE_TRACK = {"desk": 2.0, "phone": 1.0}   # phone: the role line at 26 px fills the width at 1.0
CAPS_TRACK = {"desk": 1.6, "phone": 1.0}
NAME_SIZE = {"desk": 141, "phone": 132}      # D4: 141, not 176 — the name is the title of the picture, not a wordmark
ROSE = {"desk": (130, 560, 44), "phone": (612, 130, 36)}
ROSE_BOX = {"desk": (54, 490, 152, 176), "phone": (538, 62, 152, 136)}
VAR_DY = 44                       # the VAR line's baseline below the ring (desk only)
LIMIT_X = {"desk": 1080, "phone": 600}
BAND = {"desk": (1080, 30, 200, 680), "phone": (600, 460, 120, 421)}
UNSURVEYED_FADE = 70              # the coast factor falls 1→0 over LIMIT_X … LIMIT_X+70 (desk; ×s on the phone)
NOTE_TEXT = "sitemap.xml lies again"
NOTE_PHONE = (36, 482, -2)
PHONE_S = 0.55
SAIL = (4.0, 24.0)                # begin, dur (MASTERPLAN 2.1: 4–28 s)
BOAT_SCALE = 0.7
LIGHT_R = 2.2
ROCK_ACROSS = 9                   # rocks sit ± this off the fringe polyline (jitter keyed by repo name)

LAND_KINDS = ("island", "harbour", "islet")
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


# ---------------------------------------------------------------- small helpers
def _fmt(v):
    return E.fmt(v)


def _month(iso: str) -> str:
    return f"{MONTHS[int(iso[5:7]) - 1]} {iso[:4]}"


def _day_month(iso: str) -> str:
    return f"{int(iso[8:10])} {MONTHS[int(iso[5:7]) - 1]}"


def _date(iso: str) -> str:
    y, m, d = iso[:4], int(iso[5:7]), int(iso[8:10])
    return f"{d} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m - 1]} {y}"


def _iso_date(iso: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return None


def _soundings(course, values, rows, s: float, seed, entrance_i: int) -> list:
    """Week i (oldest first) at arc position i·L'/n along the course from WP1 to SOUND_STOP px short of
    the harbour entrance; rows cycle across the course with a ±ROW_JITTER px offset keyed by the index
    (never by the value), so the oldest sit seaward in the band and the newest lie in the approach."""
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
    seen: area(r) jumps where a harbour's bay changes topology, so the Newton step oscillates."""
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


def _boxes_overlap(a, b) -> bool:
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


# ---------------------------------------------------------------- data → features
def _area_scale(data: dict, s: float) -> float:
    """px² of 5-contour area per commit-day for this build: K_AREA, or less when the busiest repository
    would not fit the sheet. One constant for every feature, so area ∝ commit-days still holds."""
    biggest = max((int(r.get("commit_days") or 0) for r in data.get("repos", [])), default=1)
    k = min(K_AREA, math.pi * R_FIT * R_FIT / max(biggest, 1))
    return k * s * s


def _kind(spec: dict) -> str:
    k = spec.get("kind")
    if k in ("vessel", "bank"):
        return "shoal"          # the ground the ship surveyed, named for her (T2 decision 13); a bank is submerged
    if k in ("harbour", "shoal", "island", "islet"):
        return k
    return "island"


def _features(data: dict, cfg, k_area: float, scale: str) -> tuple[list, list, list, dict]:
    """(named, rocks, unslotted, repo_of_feature_name). A repository with NAMED_MIN commit-days or more and a
    slot on its chart.toml entry is a named Feature at that slot; the rest are rocks. `unslotted` lists
    the repositories that have the days but no slot (charted as rocks, reported, never placed by a search)."""
    spec = {f["repo"]: f for f in cfg.get("features", [])}
    named, rocks, unslotted, repo_of = [], [], [], {}
    for r in data["repos"]:
        days = int(r.get("commit_days") or 0)
        sp = spec.get(r["name"], {})
        slot = sp.get(scale)
        if days < NAMED_MIN or not slot:
            rocks.append(r)
            if days >= NAMED_MIN:
                unslotted.append(r["name"])
            continue
        kind = _kind(sp)
        name = gazetteer.name(r, sp)          # one gazetteer for every sheet (v9.2)
        f = c.Feature(name, days, kind, alias=r["name"])
        f.r = math.sqrt(k_area * days / math.pi)
        f.ratio = 1.6 if kind in LAND_KINDS else 1.82
        f.x, f.y = int(slot[0]), int(slot[1])
        f.placed, f.slot = True, r["name"]
        named.append(f)
        repo_of[name] = r
    named.sort(key=lambda f: (-f.value, f.name))
    rocks.sort(key=lambda r: (-int(r.get("commit_days") or 0), r["name"]))
    return named, rocks, unslotted, repo_of


# ---------------------------------------------------------------- the build
def build(ctx) -> str:
    c.set_night(ctx.ed.dark)                    # D6: the night edition is drawn at +20 % weight
    try:
        return _build(ctx)
    finally:
        c.set_night(False)


def _build(ctx) -> str:
    ed, data, cfg, tl, k = ctx.ed, ctx.data, ctx.cfg, ctx.tl, ctx.k
    if k is None:
        raise RuntimeError("hero needs the type engine (scripts/typeset.py)")
    theme = ed.theme
    phone = ed.phone
    night = ed.dark
    sc = ed.scale
    w, h = SIZES[sc]
    seed = int(cfg.get("chart", {}).get("seed", 27))
    jit = c.Jitter(seed, f"hero/{sc}")
    prefix = "h"                                   # edition.svg prefixes everything with "hero-"
    s = PHONE_S if phone else 1.0
    caps_track = CAPS_TRACK[sc]
    title_track = TITLE_TRACK[sc]
    lbl_h = tokens.ROLES[sc]["label"][1]            # 19 desk / 26 phone: every box below is sized by its role
    place_h = tokens.ROLES[sc]["place-land"][1]     # 25 / 30
    note_h = tokens.ROLES[sc]["note"][1] if "note" in tokens.ROLES[sc] else place_h
    opening_end = tl.cue("opening", 0, 4.0)
    report: dict = ctx.extra
    hero_cfg = cfg.get("hero", {})

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
    repos = data["repos"]
    N = int(data.get("repo_count") or len(repos))
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
    unit_line = cfg.get("copy", {}).get("unit_chart", "SOUNDINGS IN COMMIT-DAYS")
    limit_label = cfg.get("copy", {}).get("limit_label", f"LIMIT OF SURVEY {upd_year}")
    # the high-water week (the tide table's), and the sweep day in it when the survey flagged one
    hw = (data.get("tide") or {}).get("hw") or {}
    hw_i = next((i for i, wk in enumerate(weeks) if wk.get("start") == hw.get("start")), None)
    if hw_i is None:
        hw_i = max(range(len(values)), key=lambda i: values[i])
    hw_start = _iso_date(weeks[hw_i].get("start", ""))
    sweep = None
    if hw_start:
        for sw in data.get("sweeps") or []:
            d_ = _iso_date(sw.get("date", ""))
            if d_ and hw_start <= d_ < hw_start + dt.timedelta(days=7):
                if sweep is None or int(sw.get("repos") or 0) > int(sweep.get("repos") or 0):
                    sweep = sw

    # ---- geometry in sheet space (the composition is chart.toml's; the drawing rules are this module's)
    drawable = DRAWABLE[sc]
    limit_x = LIMIT_X[sc]
    band = BAND[sc]
    rose_cx, rose_cy, rose_r = ROSE[sc]
    rose_box = ROSE_BOX[sc]
    cartouche = CARTOUCHE[sc]
    fringe_pts = [tuple(p) for p in hero_cfg.get(f"rocks_{sc}", [])]
    course_cfg = [tuple(p) for p in hero_cfg.get(f"course_{sc}", [])]
    if not fringe_pts or len(course_cfg) < 2:
        raise RuntimeError(f"hero: chart.toml [hero] needs rocks_{sc} and course_{sc}")
    note_at = tuple(hero_cfg.get("note_desk", (850, 85, -3))) if not phone else NOTE_PHONE

    # ---- the chart's scale: area ∝ commit-days at K_AREA px² per day, unless the busiest feature would not
    # fit the sheet; then the whole sheet is drawn at the largest scale that fits, and if two 5-polygons still
    # merge the scale steps down once more (≤ 3 times). Places never change; radii do.
    k_area = _area_scale(data, s)
    for _attempt in range(4):
        feats, rocks, unslotted, repo_of = _features(data, cfg, k_area, sc)
        harbour = next((f for f in feats if f.kind == "harbour"), None)
        if harbour is None:
            raise RuntimeError("hero: no harbour among the named features (chart.toml kind = \"harbour\")")
        vessel_ground = next((f for f in feats if f.alias == "Rust-sitemap"), None)
        profile = next((f for f in feats if f.alias == "BenjaminSRussell"), None)
        hr = harbour.r                                 # the nominal radius: the cluster scales with the data
        hx0, hy0 = harbour.x, harbour.y
        wp4 = (E.I(hx0 + HARBOUR["wp4"][0] * hr), E.I(hy0 + HARBOUR["wp4"][1] * hr))
        wp5 = (E.I(hx0 + HARBOUR["wp5"][0] * hr), E.I(hy0 + HARBOUR["wp5"][1] * hr))
        course = [(E.I(x), E.I(y)) for x, y in course_cfg] + [wp4, wp5]
        entrance_i = len(course) - 2
        r2 = (E.I(hx0 + HARBOUR["r2"][0] * hr), E.I(hy0 + HARBOUR["r2"][1] * hr))
        g1 = (E.I(hx0 + HARBOUR["g1"][0] * hr), E.I(hy0 + HARBOUR["g1"][1] * hr))
        basin = [(hx0 + dx * hr, hy0 + dy * hr, hh * hr, amp * base) for dx, dy, hh, amp in HARBOUR["basin"]]
        for f in feats:
            f.axis = (0.0, 2 * f.r, f.x, f.y)
        # the sounded part of the course: WP1 to SOUND_STOP short of the entrance (the kernels reach no further)
        L_sounded = c.polyline_length(course[:entrance_i + 1]) - SOUND_STOP * s
        sounded = course[:entrance_i] + [c.polyline_at(course, L_sounded)[0]]

        # ---- soundings along the course: the 52 weeks, oldest seaward
        rows = tuple(float(v) for v in ROWS)
        sounds = _soundings(course, values, rows, s, seed, entrance_i)
        coast = c.Coast(drawable, inset=24 * s, unsurveyed_x=(limit_x, limit_x + UNSURVEYED_FADE * s))
        cell = CELL[sc]

        def extras(fs):
            out = list(basin)
            for f in fs:
                if f.kind != "harbour" and f.r > 0:          # the harbour's character is its bay
                    out.extend(_lobes(f, base, seed, s))
            return out

        def builder(fs):
            return c.Field.from_soundings(w, h, sounds, base, features=fs, coast=coast, h_snd=H_SND * s,
                                          extra=extras(fs), cell=cell)

        def own_ground(fs):
            # each feature's own kernels on the grid, without the soundings: what "area ∝ commit-days" asserts
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
        if not area_bad:
            break
        k_area *= 0.85
    area_scale = k_area / (s * s)
    if area_bad:
        raise RuntimeError("hero: area law failed (±8 % at the 5-contour): " +
                           "; ".join(f"{r.name} {r.ratio}" for r in area_bad))
    ax, ay = course[-1]
    half = 13 * BOAT_SCALE * s
    if not (F.value(hx0, hy0) < 0 and F.value(ax, ay) > 0 and F.value(ax - half, ay) > 0 and F.value(ax + half, ay) > 0):
        raise RuntimeError(f"hero: harbour basin did not open around the anchorage (land {F.value(hx0, hy0):.1f}, "
                           f"anchorage {F.value(ax, ay):.1f}, hull ends {F.value(ax - half, ay):.1f} / "
                           f"{F.value(ax + half, ay):.1f})")
    drawn = c.feature_polygons(cs, feats, 5.0)
    pairs = [math.hypot(a.x - b.x, a.y - b.y) - a.r - b.r for i, a in enumerate(feats) for b in feats[i + 1:]]
    too_close = [(f.name, round(c.dist_to_polyline(f.x, f.y, sounded) - f.r - CLEAR_COURSE * s, 1))
                 for f in feats if f.kind != "harbour" and c.dist_to_polyline(f.x, f.y, sounded) < f.r + CLEAR_COURSE * s]
    report["features"] = [{"name": r.name, "repo": f.alias, "commit_days": r.value, "area_px": r.area, "target_px": r.target,
                           "r": r.r, "ratio": r.ratio, "ok": r.ok, "cx": f.x, "cy": f.y, "kind": f.kind, "slot": f.slot,
                           "drawn_px": (round(abs(c.polygon_area(drawn[f.name]))) if f.name in drawn else None),
                           "drawn_ratio": (round(abs(c.polygon_area(drawn[f.name])) / r.target, 3)
                                           if f.name in drawn and r.target else None)}
                          for r in radii for f in feats if f.name == r.name]
    report["course_too_close"] = too_close
    report["bracket_failures"] = len(fails)
    report["bracket"] = [list(f) for f in fails]
    report["unclosed"] = unclosed
    report["unslotted"] = unslotted
    report["place"] = {"dropped": [], "beyond_cap": [], "slot_conflicts": [],
                       "min_pair_clearance": round(min(pairs), 1) if pairs else None,
                       "min_course_clearance": round(min(c.dist_to_polyline(f.x, f.y, sounded) - f.r
                                                         for f in feats if f.kind != "harbour"), 1)}
    report["field"] = {"base": base, "area_scale_px2_per_day": round(area_scale, 2), "scale_steps": _attempt,
                       "residual_max": F.report.residual_max, "faded": len(F.report.faded),
                       "on_feature": len(F.report.on_feature), "clamped": len(F.report.clamped), "grid": F.report.grid}

    # ---- the rocks: the unnamed repositories along the fringe, spaced by arc length, jittered by name (never by data)
    dense = c.catmull_rom(fringe_pts, 24)
    Lf = c.polyline_length(dense)
    rock_pts: list[tuple[int, int, str]] = []
    for i, r in enumerate(rocks):
        j = c.Jitter(seed, f"hero/rock/{r['name']}")
        u = Lf * (i + 0.5) / max(len(rocks), 1) + j.offset(0.3 * Lf / max(len(rocks), 1))
        (px, py), (tx, ty) = c.polyline_at(dense, max(0.0, min(Lf, u)))
        off = j.offset(ROCK_ACROSS * s)
        rock_pts.append((E.I(px - ty * off), E.I(py + tx * off), r["name"]))
    report["rocks"] = [{"repo": nm, "x": x, "y": y, "commit_days": int(next(r.get("commit_days") or 0 for r in rocks if r["name"] == nm))}
                       for x, y, nm in rock_pts]
    report["counts"] = {"repositories": len(repos), "charted": len(feats), "rocks": len(rocks)}

    # ---- lettering positions decided before anything is drawn, so every run can keep clear of the rest
    ranked = sorted(feats, key=lambda f: -f.value)
    letter: dict[str, dict] = {}
    boxes: list[tuple] = []        # (x, y, w, h) of every placed run
    for _mx, _my in (r2, g1):      # the marks' own glyphs
        boxes.append((_mx - 9, _my - 22, 18, 26))
    for x, y, _nm in rock_pts:     # the rocks
        boxes.append((x - 6, y - 6, 12, 12))
    mark_labels: list[tuple] = []  # (text, x, y, anchor)
    if not phone:
        # the lateral marks' labels sit at fixed places by the entrance (upright: D5 retires the slope)
        for _txt, _x, _y, _anc in (('R "2" Fl R 4s', r2[0], r2[1] - 22, "middle"),
                                   ('G "1" Fl G 4s', g1[0] + 10, g1[1] + 14, "start")):
            _w = width(_txt, "label")
            _x0 = _x - _w / 2 if _anc == "middle" else _x
            if _x0 + _w > band[0] - 6:          # a label never runs into the unsurveyed band
                _x -= _x0 + _w - (band[0] - 6)
                _x0 = _x - _w / 2 if _anc == "middle" else _x
            boxes.append((_x0 - 2, _y - lbl_h * 0.8 - 1, _w + 4, lbl_h + 2))
            mark_labels.append((_txt, _x, _y, _anc))
    note_box = None
    if not phone:   # the pencil note's box is reserved early so names keep clear of it
        nw_ = width(NOTE_TEXT, "note")
        ang_ = math.radians(note_at[2])
        note_box = (note_at[0] - 2, note_at[1] + nw_ * math.sin(ang_) - note_h * 0.8, nw_ * math.cos(ang_) + 4,
                    note_h - nw_ * math.sin(ang_) + 4)
        boxes.append(note_box)

    def disc_hit(b, skip=None) -> bool:
        """Another feature's disc (inflated by its r) crossing the box anywhere, not just at its centre."""
        for o in feats:
            if o is skip:
                continue
            cx_ = min(max(o.x, b[0]), b[0] + b[2])
            cy_ = min(max(o.y, b[1]), b[1] + b[3])
            if math.hypot(cx_ - o.x, cy_ - o.y) < o.r * 1.15 + 2:
                return True
        return False

    def furniture_hit(b) -> bool:
        fixed = [cartouche, rose_box] + ([note_box] if note_box else [])
        if any(_boxes_overlap(b, fr) for fr in fixed):
            return True
        return (b[1] + b[3] > drawable[1] + drawable[3] - 6 or b[1] < drawable[1] + 4
                or b[0] < drawable[0] + 4 or b[0] + b[2] > band[0] - 4)

    # the one printed week: high water, where its kernel is; its caption beside it where there is room
    hw_plan = None
    hw_x, hw_y, hw_v = sounds[hw_i]
    hw_base = hw_y + (4 if not phone else 6)
    if hw_x < limit_x - 8 * s:
        fw = width(str(hw_v), "label")
        fb = (hw_x - fw / 2 - 3, hw_base - lbl_h * 0.8 - 1, fw + 6, lbl_h + 2)
        if not any(_boxes_overlap(fb, ob) for ob in boxes) and not disc_hit(fb) and not furniture_hit(fb):
            boxes.append(fb)
            cap = f"HW · SWEEP {_day_month(sweep['date'])}" if sweep else (f"HW · {_day_month(weeks[hw_i]['start'])}" if hw_start else "HW")
            cw = width(cap, "label", tracking=caps_track)
            above, below = hw_base - lbl_h - 2, hw_base + lbl_h + 2
            cands = [(hw_x - fw / 2 - 8, hw_base, "end"), (hw_x + fw / 2 + 8, hw_base, "start"),
                     (hw_x, above, "middle"), (hw_x, below, "middle"),
                     (hw_x + fw / 2, above, "end"), (hw_x + fw / 2, below, "end"),
                     (hw_x - fw / 2, above, "start"), (hw_x - fw / 2, below, "start")]
            cap_pos = None
            for cx_, cy_, anc in cands:
                x0 = cx_ - cw / 2 if anc == "middle" else (cx_ - cw if anc == "end" else cx_)
                cb = (x0 - 2, cy_ - lbl_h * 0.8 - 1, cw + 4, lbl_h + 2)
                if any(_boxes_overlap(cb, ob) for ob in boxes) or disc_hit(cb) or furniture_hit(cb):
                    continue
                boxes.append(cb)
                cap_pos = (cx_, cy_, anc)
                break
            hw_plan = {"x": hw_x, "y": hw_base, "value": hw_v, "week": weeks[hw_i].get("start"), "caption": cap,
                       "caption_at": cap_pos, "sweep": (sweep or {}).get("date")}
    report["hw"] = hw_plan or {"printed": False, "week": weeks[hw_i].get("start"), "value": hw_v}

    date_pos: dict[str, tuple] = {}     # feature -> where its report date prints (v9.2)
    name_clashes: list[str] = []
    for f in ranked:
        land = f.kind in LAND_KINDS
        role = "label" if land else "place-water"
        size = place_h if f.kind == "harbour" else None     # the harbour leads the hierarchy (25; phone 30)
        nw = width(f.name.upper() if land else f.name, role, size=size,
                   tracking=((title_track if size else caps_track) if land else None))
        nh = (size or lbl_h) if land else place_h
        big_shoal = (not land) and f.r >= BIG_SHOAL_R * s and nw < 1.5 * f.r
        if f.kind == "harbour":
            hx, hy = f.x, f.y - 0.84 * f.r - 6 * s           # the basin and the anchorage take the middle
            name_pos = (f.x, f.y + 0.84 * f.r + (22 if not phone else 30), "middle")
        elif land:
            hx, hy = f.x, f.y + 6 * s                        # on the land, the name offshore below
            name_pos = (f.x, f.y + 1.2 * f.r + (16 if not phone else 26), "middle")
        elif big_shoal:
            hx, hy = f.x, f.y - 8 * s                        # inside the bank, the name under the figure
            name_pos = (f.x, f.y + (16 if not phone else 24), "middle")
        else:
            hx, hy = f.x, f.y + 6 * s                        # inside the bank, the name below it
            name_pos = (f.x, f.y + f.r + (18 if not phone else 26), "middle")
        hw_ = width(str(f.value), "label")
        boxes.append((hx - hw_ / 2, hy - lbl_h * 0.8, hw_, lbl_h))

        def box_at(x, y, a):
            x0 = x - nw / 2 if a == "middle" else (x - nw if a == "end" else x)
            return (x0, y - nh * 0.8, nw, nh)

        def clashes(b):
            hit = any(_boxes_overlap(b, ob) for ob in boxes) or furniture_hit(b) or disc_hit(b, skip=f)
            if hit and os.environ.get("HERO_DEBUG"):   # HERO_DEBUG=1: say what a name's candidate ran into
                print(f"  {f.name}: {tuple(round(v) for v in b)} runs={[tuple(round(v) for v in ob) for ob in boxes if _boxes_overlap(b, ob)]}"
                      f" furniture={furniture_hit(b)} disc={disc_hit(b, skip=f)}")
            return hit

        nx_, ny_, anc = name_pos
        nb = box_at(nx_, ny_, anc)
        if nb[0] + nb[2] > band[0] - 6:                 # a name never runs into the unsurveyed band
            nx_ -= nb[0] + nb[2] - (band[0] - 6)
            nb = box_at(nx_, ny_, anc)
        if nb[0] < drawable[0] + 6:                     # nor out of the neat line on the west
            nx_ += drawable[0] + 6 - nb[0]
            nb = box_at(nx_, ny_, anc)
        name_pos = (nx_, ny_, anc)
        if clashes(nb) and f.kind != "harbour" and not big_shoal:
            above = f.y - (1.2 * f.r if land else f.r) - 6 * s
            right = (f.x + 1.2 * f.r + 8 * s, f.y + 4 * s, "start")
            left = (f.x - 1.2 * f.r - 8 * s, f.y + 4 * s, "end")
            left_low = (f.x - 1.2 * f.r - 8 * s, f.y + 0.6 * f.r + 8 * s, "end")
            right_low = (f.x + 1.2 * f.r + 8 * s, f.y + 0.6 * f.r + 8 * s, "start")
            right_high = (f.x + 1.2 * f.r + 8 * s, f.y - 0.6 * f.r + 2 * s, "start")
            left_high = (f.x - 1.2 * f.r - 8 * s, f.y - 0.6 * f.r + 2 * s, "end")
            below2 = (f.x, ny_ + lbl_h + 2, "middle")
            above2 = (f.x, above - lbl_h - 2, "middle")
            found = False
            for cand_ in ((nx_, above, anc), left, right, left_low, right_low, left_high, right_high, below2, above2):
                nb2 = box_at(*cand_)
                if not clashes(nb2):
                    name_pos, nb, found = cand_, nb2, True
                    break
            if not found:
                name_clashes.append(f.name)          # kept where it was planned, reported (a slot wants moving)
        boxes.append(nb)
        nx_, ny_, anc = name_pos
        if not phone and f.alias in ("Rust-sitemap", "Scrapy") and repo_of.get(f.name, {}).get("first"):
            # the report date printed under the name (v9.2) is reserved now so later runs keep clear; where the
            # ground under the name is already taken the date is left off, never overprinted
            _dw = width(f"({_month(repo_of[f.name]['first'])})", "label")
            _dy = ny_ + (size or lbl_h) + 4
            _dx0 = nx_ - _dw / 2 if anc == "middle" else (nx_ - _dw if anc == "end" else nx_)
            _db = (_dx0 - 2, _dy - lbl_h * 0.8 - 1, _dw + 4, lbl_h + 2)
            if not any(_boxes_overlap(_db, ob) for ob in boxes) and not disc_hit(_db, skip=f):
                boxes.append(_db)
                date_pos[f.name] = (nx_, _dy, anc)
        letter[f.name] = {"height": (hx, hy), "name": name_pos, "role": role, "size": size, "land": land}
    report["name_clashes"] = name_clashes
    k.exclude("band", *band)
    k.exclude("rose", *rose_box)
    k.exclude("cartouche", *cartouche)

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

    # ---- t = 0: the blank form — frame, band (hatch emitted after the tints, on top), rose
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

    band_labels = [up("UNSURVEYED", band[0] + (band[2] * 0.6 if not phone else 80), band[1] + band[3] / 2, "label-caps"),
                   up(limit_label, band[0] + (22 if not phone else 24), band[1] + band[3] / 2, "label", caps=True)]

    # ---- tints (A 1.0, B 1.3), generalised: closed 10-rings under GENERALISE_10 are not tinted
    gen10 = GENERALISE_10[sc]
    gen5 = GENERALISE_5[sc]

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

    defs.append(f'<clipPath id="surveyed"><rect x="{_fmt(drawable[0])}" y="{_fmt(drawable[1])}" '
                f'width="{_fmt(limit_x - drawable[0])}" height="{_fmt(drawable[3])}"/></clipPath>')
    body.append('<g clip-path="url(#surveyed)">')          # nothing charted lies beyond the limit of survey (v9.2)
    body.append(tl.fade_in(fill_level(10.0, theme.shallow_a, gen10 * s), 1.0, 1.0, rise=0))
    body.append(tl.fade_in(fill_level(5.0, theme.shallow_b, gen5 * s), 1.3, 1.0, rise=0))
    body.append('</g>')
    land_svg = [fill_level(0.0, theme.land), c.coastline(cs, theme)]
    big_land = [f for f in feats if f.kind in LAND_KINDS and (f.r >= BIG_LAND_R * s or f.kind == "harbour")]
    for poly in c.level_polygons(cs, 0.0):
        if any(c.point_in_polygon(f.x, f.y, poly) for f in big_land):
            land_svg.append(c.coast_vignette(poly, theme, jit))
    water_svg = []
    shoal_pts = [(f.x, f.y) for f in feats if f.kind == "shoal"]
    if shoal_pts:
        water_svg.append(c.danger_lines(cs, 5.0, theme, jit, inside=shoal_pts))
    # the rocks: one path for the fringe, PEN ink, round caps make the dots
    if rock_pts:
        water_svg.append(f'<path d="{"".join(c.rock_d(x, y) for x, y, _n in rock_pts)}" fill="none" '
                         f'{c.stroke("PEN", theme.ink, 0.9)}/>')
    land_svg.append(use("anchorage", *course[-1]))
    if profile is not None:   # the survey station on the profile shoal, under its figure
        land_svg.append(use("station", profile.x, profile.y + 20 * s))
    body.append("".join(land_svg))                        # land is a sheet at t = 0 (round 2 addendum)
    body.append(tl.fade_in("".join(water_svg), 1.6, 0.65, rise=0))
    # the unsurveyed hatch lies over the faded tints at the limit of survey; the contours over it
    body.append(ub)
    body.append("".join(band_labels))

    # ---- contours draw in, deep first (0.2 + 0.12·i, 1.6 s); the approximate fringe fades with them; no figures
    approx_clip = (limit_x - 40 * s, drawable[1], 40 * s + UNSURVEYED_FADE * s, drawable[3])
    gap_breaks = []
    if hw_plan:   # the printed week figure breaks every contour it would cross (lines yield to soundings)
        fw = width(str(hw_v), "label")
        rect = (hw_plan["x"] - fw / 2 - 5 * s, hw_plan["y"] - lbl_h * 0.8 - 3 * s, fw + 10 * s, lbl_h + 5 * s)
        for q in cs:
            if q.level in (5.0, 10.0):
                gap_breaks.extend((q, i0, i1) for i0, i1 in c.gaps_in_rect(q, rect))
    for i, lv in enumerate((10.0, 5.0)):
        begin = 0.2 + 0.12 * i
        for short in (True, False):
            sub = [q for q in cs if q.level == lv and ((q.length < 300 * s) == short)]
            if lv == 10.0:
                sub = [q for q in sub if not (q.closed and ring_len(q.pts) < gen10 * s)]
            if lv == 5.0:
                sub = [q for q in sub if not (q.closed and ring_len(q.pts) < gen5 * s)]
            if not sub:
                continue
            svg = c.draw_contours(sub, INDEX, theme, approx_clip=approx_clip,
                                  breaks=[b for b in gap_breaks if b[0].level == lv], min_len=40 * s,
                                  every=1 if short else 2)
            for m in re.finditer(r"<path ([^>]*)/>", svg):
                attrs = m.group(1)
                if "stroke-dasharray" in attrs:
                    body.append(tl.fade_in(f"<path {attrs}/>", begin + 0.5, 0.65, rise=0))
                else:   # solid contours end at the limit of survey; the approximate fringe runs on
                    body.append('<g clip-path="url(#surveyed)">' + tl.draw_in(attrs, 1.6, begin) + '</g>')

    # ---- the course: pecked line and waypoint fixes (with the land); no bearings (D5)
    course_svg = c.course(course, theme, jit, pecked=True, prefix=prefix, bearings=False)
    course_svg = course_svg.replace(f'stroke-width="{c.width("PEN")}"', f'stroke-width="{c.width("LINE")}"', 1)
    body.append(tl.fade_in(course_svg, 1.6, 0.65, rise=0))
    symbols_used.add("waypoint")

    # ---- the one week figure surfaces as the boat passes it (the lead goes down where the ship is)
    course_len = c.polyline_length(course)
    cum = [0.0]
    for a_, b_ in zip(course, course[1:]):
        cum.append(cum[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))

    def pass_time(x, y) -> float:
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

    printed = 0
    if hw_plan:
        wk = weeks[hw_i]
        frag = snd(hw_v, hw_plan["x"], hw_plan["y"], role="label", truth="measured",
                   key=f"week:{wk.get('start', hw_i)}", fill=theme.ink)
        if hw_plan["caption_at"]:
            cx_, cy_, anc = hw_plan["caption_at"]
            frag += lbl(hw_plan["caption"], cx_, cy_, "label", anchor=anc, fill=theme.ink2, caps=True,
                        truth="measured", key="high-water")
        body.append(frag if phone else tl.reveal(frag, pass_time(hw_plan["x"], hw_plan["y"])))
        printed = 1
    report["soundings_printed"] = printed

    # ---- the rose: a 24-hour clock whose ticks are the hour histogram; the card settles at 2.0 s
    rose_geo = c.clock_rose(rose_cx, rose_cy, rose_r, theme, hours, label_cb=None)
    settle = tl.xform("rotate", [f"12 {rose_cx} {rose_cy}", f"-4 {rose_cx} {rose_cy}", f"0 {rose_cx} {rose_cy}"],
                      1.6, 2.0, ease="sea", key_times=[0, 0.45, 1], name="rose_settle")
    body.append(f'<g transform="rotate(0 {rose_cx} {rose_cy})">{settle}{rose_geo}</g>')
    rose_text = []
    for hh in (0, 6, 12, 18):
        a = math.radians(hh * 15 - 90)
        ca, sa = math.cos(a), math.sin(a)
        if abs(ca) < 0.01:
            x_, y_, anc = rose_cx, (rose_cy - rose_r - 7) if sa < 0 else (rose_cy + rose_r + 18), "middle"
        else:
            x_, y_, anc = (rose_cx + rose_r + 6, rose_cy + 5, "start") if ca > 0 else (rose_cx - rose_r - 6, rose_cy + 5, "end")
        rose_text.append(lbl(f"{hh:02d}", x_, y_, "label", anchor=anc, within=rose_box))
    if not phone:
        rose_text.append(lbl(f"VAR {modal:02d}h ({var_year})", rose_cx, rose_cy + rose_r + VAR_DY, "label", anchor="middle",
                             fill=theme.ink2, tracking=caps_track, truth="measured", key="variation", within=rose_box))
    body.append("".join(rose_text))

    # ---- names and spot heights, by rank (static: names stand at t = 0)
    for f in ranked:
        L_ = letter[f.name]
        parts = []
        hx, hy = L_["height"]
        parts.append(snd(f.value, hx, hy, role="label", truth="measured", key=f"days:{f.alias}"))
        nx_, ny_, anc = L_["name"]
        if L_["land"]:
            parts.append(lbl(f.name, nx_, ny_, "label", anchor=anc, caps=True, size=L_["size"],
                             tracking=(title_track if L_["size"] else caps_track)))
        else:
            parts.append(lbl(f.name, nx_, ny_, "place-water", anchor=anc))
        body.append("".join(parts))

    # ---- the cartouche: the name (two words), the thesis, the title lines on one left edge
    block = []
    nx, ny = NAME_AT[sc]
    nsz = NAME_SIZE[sc]
    ben = k.text("Ben", nx, ny, "display", size=nsz, edition=ed, scale=sc, within=cartouche)
    wb = k.text_width("Ben ", "display", size=nsz, edition=ed, scale=sc)
    russ = k.text("Russell", nx + wb, ny, "display", size=nsz, edition=ed, scale=sc, within=cartouche)
    block.append(ben + russ)
    if not phone:
        block.append(k.text(thesis, *THESIS_AT[sc][0], "thesis", fill=theme.ink2, edition=ed, scale=sc, within=cartouche))
    else:
        words = thesis.split()
        cut = len(words) // 2 + 1
        for (tx_, ty_), line in zip(THESIS_AT[sc], (" ".join(words[:cut]), " ".join(words[cut:]))):
            block.append(k.text(line, tx_, ty_, "thesis", fill=theme.ink2, edition=ed, scale=sc, within=cartouche))
    ver = edition_d.get("version") or "—"
    ed_date = edition_d.get("date")
    ed_line = f"CHART NO. {N} · EDITION {ver}" + (f" · {_month(ed_date)}" if (ed_date and not phone) else "") + " · IALA REGION B"
    count_line = f"{len(repos)} REPOSITORIES · {len(feats)} CHARTED · {len(rocks)} AS ROCKS"
    bx, y_big, y0, pitch = TITLE_AT[sc]
    big_size = 25 if not phone else 30
    rows_t = [
        (y_big, f"THE OPEN WEB · FROM SURVEYS {first_year}–{upd_year}", "label", theme.ink, "measured", "surveys", big_size),
        (y0, role_line, "label", theme.ink, None, None, None),
        (y0 + pitch, f"{unit_line} · DATUM: MAIN", "label-caps" if phone else "label", theme.ink2, None, "unit" if phone else None, None),
        (y0 + 2 * pitch, ed_line, "label", theme.ink2, "measured", "chart-edition", None),
        (y0 + 3 * pitch, count_line, "label", theme.ink2, "measured", "repositories", None),
    ]
    for y, t, role, fill, truth, key, size in rows_t:
        if role == "label-caps":   # the phone's one label-caps run: the unit line (the desk's is outside the neat line)
            block.append(k.text_use(t, bx, y, "label-caps", fill=fill, edition=ed, scale=sc, key=key, within=cartouche))
        else:
            block.append(lbl(t, bx, y, role, anchor="start", fill=fill, caps=True, within=cartouche, truth=truth, key=key,
                             size=size, tracking=title_track))
    if not phone:
        # outside the neat line: unit line (the one label-caps run), chart number, folio, imprint, small corrections
        block.append(lbl(unit_line, 640, 18, "label-caps", anchor="middle", fill=theme.ink, key="unit"))
        block.append(lbl(str(N), 1250, 18, "label", anchor="end", fill=theme.muted, truth="measured", key="chart-number"))
        taken = data.get("taken") or (data.get("updated_at") or "")[:10]
        corr = data.get("corrections") or {}
        folio = f"CHART NO. {N} · SHEET 1"
        if corr:
            yr = max(corr)
            nums = sorted(int(e.get("n")) for e in corr[yr] if e.get("n") is not None)
            if nums:   # the whole year's list, first to last (v9.2: a window read as the list)
                lst = f"{nums[0]}–{nums[-1]}" if len(nums) > 1 else str(nums[0])
                folio += f" · Small corrections {yr} — {lst}"
        block.append(lbl(folio, 30, h - 6, "label-caps", fill=theme.ink2, key="folio"))
        folio_w = width(folio.upper(), "label", tracking=caps_track)
        imprints = [f"github.com/{login} · {_date(taken)} · under the superintendence of B. Russell · redrawn weekly",
                    f"github.com/{login} · {_date(taken)} · redrawn weekly"]
        imprint = next((t for t in imprints if 30 + folio_w + 30 + width(t.upper(), "label", tracking=caps_track) <= 1250),
                       imprints[-1])
        block.append(lbl(imprint, 1250, h - 6, "label", anchor="end", fill=theme.ink2, caps=True, truth="measured", key="imprint"))
    body.append("".join(block))                             # the cartouche is printed, not revealed

    # ---- mark labels, the pencil note, the no-sounding note (by 1.5 s); the report dates static
    late = []
    for _txt, _x, _y, _anc in mark_labels:
        late.append(lbl(_txt, _x, _y, "label", fill=theme.ink, anchor=_anc))
    fixes_svg: list[str] = []
    for f in (vessel_ground, harbour):   # v9.2: a report date under the feature's name, not a date on a fix
        if f is None or phone or f.name not in date_pos:
            continue
        first = repo_of[f.name]["first"]
        nx_, dy_, anc = date_pos[f.name]
        fixes_svg.append(lbl(f"({_month(first)})", nx_, dy_, "label", fill=theme.ink2, truth="measured",
                             key=f"first:{f.alias}", anchor=anc))
    if not phone:
        late.append(lbl(NOTE_TEXT, note_at[0], note_at[1], "note", fill=theme.muted, rotate=note_at[2]))
    if ctx.no_sounding or data.get("no_sounding"):
        taken = data.get("taken") or (data.get("updated_at") or "")[:10]
        note = f"no soundings this week — figures as surveyed {_date(taken)}"
        if not phone:   # caps: the note shares the sheet's lettering (a lowercase italic set costs 8 KB of defs)
            late.append(lbl(note, 340 - width(note.upper(), "label", tracking=caps_track) / 2, 703, "label",
                            fill=theme.muted, rotate=-3, caps=True))
        else:
            late.append(lbl(note, NOTE_PHONE[0], NOTE_PHONE[1], "label", fill=theme.muted, rotate=NOTE_PHONE[2], caps=True))
    body.append(tl.fade_in("".join(late), 1.1, 0.4, rise=0))
    body.append("".join(fixes_svg))

    # ---- lateral marks with their lights (lit from t = 0; G begins 0, R begins 2; one loop each)
    lights = []
    ms = 1.0 if not phone else 1.3
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
    return (f"Chart of Ben Russell's {n} repositories, soundings in commit-days: Scrapy Harbor, rustmapper's ground, "
            "the rest as islands and rocks. A boat sails in and anchors.")


# ---------------------------------------------------------------- build-report hook
def _report_hook(ctx, svg_text: str, entry: dict) -> None:
    if getattr(ctx, "sheet", None) != NAME:
        return
    x = ctx.extra
    for key in ("features", "bracket_failures", "lights", "symbols_used"):
        if key in x:
            entry[key] = x[key]
    entry["area_law"] = "area∝commit-days"
    entry["hero"] = {kk: x[kk] for kk in ("field", "place", "unclosed", "bracket", "soundings_printed", "sail",
                                          "course_too_close", "rocks", "unslotted", "counts", "hw", "name_clashes")
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
