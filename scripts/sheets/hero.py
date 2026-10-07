"""hero.py — Sheet 1, "Chart No. N": the archipelago of one person's public repositories (T2).

The chart proper. One feature per repo, its drawn area at the 5-contour proportional to Ben's own
commits (solve_radii, ±8 %); the 52 weekly totals are the soundings along the course and they
generate the depth field (depth = count, MASTERPLAN 15); contours 5 · 10 · 20 · 50 with figures in
breaks; a buoyed 290° entrance into Scrapy Harbor; a two-ring rose as a 24-hour clock in the
author's local time; an open title block; the unsurveyed band at the limit of survey. The boat
sails in once (4–28 s) and anchors; the two lateral lights are the only loop afterwards.

Every glyph goes through typeset (ctx.k), every animation through the Timeline (ctx.tl), every line
through chartlib. Phone editions are the same story redrawn at SCALE_PHONE through one affine map
of the desk layout (features, course, marks, basin, band), with the field re-solved in phone space.
"""
from __future__ import annotations

import math
import re

import chartlib as c
import edition as E
from tokens import INK, W as _W  # noqa: F401  (W is read for the report only)

NAME = "hero"
KIND = "chart"
SIZES = {"desk": (1280, 740), "phone": (720, 900)}
EDITIONS = None   # the runner's default six plus HERO_EXTRA (phone stills)

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the title block, the margin captions and the band's UNSURVEYED are set upper-case through role "
     "`label` with tracking 0.6 (phone 1.0); only the unit line top-centre is role `label-caps`",
     "check_type allows one label-caps run per sheet; a period title block is five caps lines"),
    ("Role line at 22 px", "role `note` (serif-italic) with size=22, inline outlines",
     "T2 §2.2 asks serif-italic 22 and tokens has no role at that size; 22 is on the scale"),
    ("No margin graticule", "the frame carries minute bars only; no labelled meridians or parallels",
     "the sheet has no latitude or longitude, so labelled margin ticks would be invented geometry"),
    ("Islets unnamed", "features whose r < 16 (under ~25 commits) carry their spot height only",
     "twenty-one serif names would collide; an unnamed rock with its height is chart grammar"),
    ("Phone lights lit, not flashing", "the phone editions draw both lights lit and keep the character labels",
     "MASTERPLAN 7.3: hero-phone ≤ 0.25 repaints/s after 6 s; two Fl 4s lights alone are 1/s"),
    ("Pencil note without a notice number", "\"sitemap.xml lies again\" stands alone by the double shoal",
     "chart.toml's notices carry no sitemap item; a tie to Notice 3 would be invented"),
]

# ---------------------------------------------------------------- desk layout (1280-space)
RULES = {"desk": (18, 24), "phone": (14, 19)}
DRAWABLE = (24, 24, 1232, 692)
K_AREA = 32.2                     # px² of 5-contour area per commit (r = 3.2·√commits), desk
LEVELS = c.DEFAULT_LEVELS         # (0, 5, 10, 20, 50)
INDEX = (10.0, 50.0)
COURSE = [(1136, 296), (1046, 360), (900, 470), (842, 580), (776, 556)]       # WP1 … WP5 (decision 1)
SLOTS = {                         # alias → centre; the named six (T2 §2.3 with decision 1; game_engine,
    "Scrapy Harbor": (760, 560), "rustmapper": (1022, 508), "game_engine": (816, 344),   # rustmapper and
    "Data_science_dev": (992, 636), "Profile Shoal": (330, 405), "FashionDB": (640, 420),  # DSD moved so the
}                                 # sounding rows (±36, h 30) never dig a feature's 5-ring: course ≥ r + 66
ROWS = (-36, -18, 18, 36)         # sounding rows off the course (T2 §2.4 had ±24/±48)
CLEAR_COURSE = 66                 # Halton features keep r + 66 from the course (rows 36 + h_snd 30)
SOUND_STOP = 70                   # the soundings end this far before the entrance (WP4): the basin is the harbour's
CELL = {"desk": 6.0, "phone": 4.0}
BIG_NAME_R = 40                   # land names at 17 px caps from this radius, 13 px below it
BASIN = [(786, 559, 30)]          # harbour basin kernel (x, y, h), amp −2.1·base: anchorage ≈ 4, mouth ≈ 10
MARK_R2 = (827, 551)              # R "2" nun, north of the 290° leg
MARK_G1 = (813, 593)              # G "1" can, south
COVERAGE = (680, 470, 210, 160)   # "SEE SHEET 3"
SEE_SHEET = (687, 484)            # inside the box, top-left (open water)
CALM = (40, 40, 800, 280)
TITLE_BOX = (70, 540, 540, 130)
ROSE = (1000, 160, 72)
ROSE_BOX = (920, 80, 160, 195)
LIMIT_X = 1080
BAND = (1080, 150, 200, 430)
UNSURVEYED_FADE = 70              # the coast factor falls 1→0 over LIMIT_X … LIMIT_X+70
PA_SHIFT = (24, -14)
NOTE_AT = (898, 556, -7)          # pencil note anchor and rotation
PHONE_S = 0.55
PHONE_ORIGIN = (19, 300)          # where the desk drawable's corner lands on the phone sheet
SAIL = (4.0, 24.0)                # begin, dur (MASTERPLAN 2.1: 4–28 s)

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


def _soundings(course, values, rows, s: float, entrance_i: int = 3) -> list:
    """Week i (oldest first) at arc position i·L'/n along the course from WP1 to SOUND_STOP px short
    of the harbour entrance (WP4), rows cycling, so the oldest sit seaward in the band and the newest
    lie in the approach; nothing is sounded on the harbour's own ground. Integer coordinates."""
    n = len(values)
    L = c.polyline_length(course[:entrance_i + 1]) - SOUND_STOP * s
    out = []
    for i, v in enumerate(values):
        arc = L * i / n
        (x, y), (tx, ty) = c.polyline_at(course, arc)
        off = rows[i % len(rows)]
        out.append((E.I(x - ty * off), E.I(y + tx * off), v))
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


def _inject(el: str, child: str) -> str:
    """Put `child` inside a self-closing element string (`<circle …/>` → `<circle …>child</circle>`)."""
    m = re.match(r"^<([A-Za-z]+)(\s[^>]*?)?/>$", el.strip(), re.S)
    if not m:
        return f"<g>{child}{el}</g>"
    return f"<{m.group(1)}{m.group(2) or ''}>{child}</{m.group(1)}>"


# ---------------------------------------------------------------- data → features
def _features(data: dict, cfg, k_area: float) -> tuple[list, dict]:
    """One Feature per surveyed repo; alias/slot/kind from chart.toml [[features]] where present.
    Returns (features, repo_of_feature_name)."""
    spec = {f["repo"]: f for f in cfg.get("features", [])}
    feats, repo_of = [], {}
    for r in data["repos"]:
        commits = int(r.get("commits") or 0)
        if commits <= 0:
            continue
        s = spec.get(r["name"], {})
        aliases = s.get("aliases") or r.get("aliases") or []
        alias = aliases[0] if aliases else r["name"]
        r0 = math.sqrt(k_area * commits / math.pi)
        kind = s.get("kind")
        if r.get("archived"):
            kind = "wreck"
        elif kind == "vessel":
            kind = "shoal"          # the ground the ship surveyed, named for her (T2 decision 13)
        elif kind not in ("harbour", "shoal", "island", "islet"):
            kind = c.kind_of(r0, bool(r.get("active")), alias, bool(r.get("archived")))
        if kind in ("harbour",):
            name = alias
        elif alias != r["name"]:
            name = alias
        elif kind == "shoal":
            name = f"{_display_name(r['name'])} Shoal"
        elif kind == "island":
            name = f"{_display_name(r['name'])} I."
        else:
            name = _display_name(r["name"])
        f = c.Feature(name, commits, kind, alias=alias, sub=r.get("months_active"))
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
    if phone:
        rose_cx, rose_cy, rose_r = 600, 310, 56
        rose_box = (536, 236, 130, 170)
        band = (E.I(limit_x), 412, w - E.I(limit_x), 228)
    else:
        rose_cx, rose_cy, rose_r = ROSE
        rose_box = ROSE_BOX
        band = BAND
    excl = [geo.rect(COVERAGE), (band[0], drawable[1], w - band[0], drawable[3]), rose_box]
    if not phone:
        excl += [CALM, (TITLE_BOX[0] - 16, TITLE_BOX[1] - 16, TITLE_BOX[2] + 32, TITLE_BOX[3] + 32)]
    place = c.place_features(feats, drawable, excl, course, seed, slots, cap=32,
                             clear_edge=24 * s, clear_pair=44 * s, clear_course=CLEAR_COURSE * s,
                             islet_min_x=geo.p(400, 0)[0], tries=2000)
    feats = [f for f in feats if f.placed]
    harbour = next((f for f in feats if f.kind == "harbour"), None)
    vessel_ground = next((f for f in feats if f.alias == "rustmapper"), None)
    profile = next((f for f in feats if f.alias == "Profile Shoal"), None)

    # ---- soundings along the course: the 52 weeks, oldest seaward
    rows = tuple(v * s for v in ROWS)
    sounds = _soundings(course, values, rows, s)
    too_close = [(f.name, round(c.dist_to_polyline(f.x, f.y, course) - f.r - CLEAR_COURSE * s, 1))
                 for f in feats if f.kind != "harbour" and c.dist_to_polyline(f.x, f.y, course) < f.r + CLEAR_COURSE * s]
    coast = c.Coast(drawable, inset=24 * s, unsurveyed_x=(limit_x, limit_x + UNSURVEYED_FADE * s))
    basin = [(*geo.p(x, y), hh * s, -2.1 * base) for x, y, hh in BASIN]
    cell = CELL[sc]

    def builder(fs):
        return c.Field.from_soundings(w, h, sounds, base, features=fs, coast=coast, h_snd=30 * s,
                                      extra=basin, cell=cell)

    def own_ground(fs):
        # each feature's own kernel on the grid, without the soundings: what "area ∝ commits" asserts
        return c.Field.from_soundings(w, h, [], base, features=fs, coast=coast, h_snd=30 * s, extra=basin, cell=cell)

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
        if not (F.value(hx, hy) < 0 and F.value(ax, ay) > 0):
            raise RuntimeError(f"hero: harbour basin did not open (land {F.value(hx, hy):.1f}, "
                               f"anchorage {F.value(ax, ay):.1f})")
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
    report["place"] = {"dropped": place.dropped, "beyond_cap": place.beyond_cap, "slot_conflicts": place.slot_conflicts,
                       "min_pair_clearance": place.min_pair_clearance, "min_course_clearance": place.min_course_clearance}
    report["field"] = {"base": base, "residual_max": F.report.residual_max, "faded": len(F.report.faded),
                       "on_feature": len(F.report.on_feature), "clamped": len(F.report.clamped), "grid": F.report.grid}
    report["culled"] = culled

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

    # ---- t = 0: the blank form — frame, band, rose rings
    body.append(c.frame(w, h, theme, "broken", gaps=[("right", band[1], band[1] + band[3])], rules=RULES[sc]))
    k.exclude("band", *band)
    k.exclude("rose", *rose_box)
    ud, ub = c.unsurveyed_band(band[0], band[1], band[2], band[3], theme, jit, None, ramp_w=40 * s, clip_id="unsurv")
    defs.append(ud)
    band_labels = [lbl("UNSURVEYED", band[0] + band[2] * 0.6, band[1] + band[3] / 2, "label-caps", anchor="middle", rotate=-90)]
    if not phone:
        band_labels.append(lbl(limit_label, band[0] - 14, band[1] + band[3] / 2, "label", anchor="middle", rotate=-90, caps=True))
    else:
        band_labels.append(lbl("SOUNDINGS THINNED", band[0] + 26, band[1] + band[3] / 2, "label", anchor="middle", rotate=-90,
                               fill=theme.muted, caps=True))

    # ---- tints (A 1.0, B 1.3), then land, coast, danger lines, PA outline, anchorage, box at 1.6
    def fill_level(level, color):
        polys = c.level_polygons(cs, level)
        if not polys:
            return ""
        d = "".join(c.compact_path(p, True, 1 if c.polyline_length(p, True) < 300 * s else 2) for p in polys)
        return f'<path d="{d}" fill="{color}" fill-rule="evenodd"/>'

    body.append(tl.fade_in(fill_level(10.0, theme.shallow_a), 1.0, 1.0, rise=0))
    body.append(tl.fade_in(fill_level(5.0, theme.shallow_b), 1.3, 1.0, rise=0))
    land = [fill_level(0.0, theme.land), c.coastline(cs, theme)]
    for poly in c.level_polygons(cs, 0.0):
        if abs(c.polygon_area(poly)) > 1500 * s * s:
            land.append(c.coast_vignette(poly, theme, jit))
    shoal_pts = [(f.x, f.y) for f in feats if f.kind == "shoal"]
    if shoal_pts:
        land.append(c.danger_lines(cs, 5.0, theme, jit, inside=shoal_pts))
    # the double shoal: rustmapper's ground as charted from the sitemap (dotted, PA) beside the survey
    pa_label = ""
    if vessel_ground is not None and not phone:
        poly = c.feature_polygons(cs, [vessel_ground], 5.0).get(vessel_ground.name)
        if poly:
            dx, dy = PA_SHIFT
            land.append(f'<path d="{c.compact_path(poly, True, 1)}" fill="none" transform="translate({dx} {dy})" '
                        f'{c.stroke("PEN", theme.ink, INK["mid"], "PECK", jit.sub("pa"))}/>')
            ne = max(poly, key=lambda p: p[0] - p[1])
            pa_label = lbl("PA", ne[0] + dx + 4, ne[1] + dy + 2, "label-italic", fill=theme.ink2)
    land.append(use("anchorage", *course[-1]))
    symbols_used.add("anchorage")
    if not phone:
        cov = COVERAGE
        land.append(f'<rect x="{_fmt(cov[0])}" y="{_fmt(cov[1])}" width="{_fmt(cov[2])}" height="{_fmt(cov[3])}" fill="none" '
                    f'{c.stroke("HAIR", theme.ink, 0.7, "RESTRICT", caps="butt")}/>')
    if profile is not None:
        land.append(use("station", profile.x, profile.y))
    body.append(tl.fade_in("".join(land), 1.6, 0.65, rise=0))

    # the unsurveyed hatch lies over the faded tints at the limit of survey; the contours over it
    body.append(ub)
    body.append("".join(band_labels))

    # ---- contours draw in, deep first (0.2 + 0.12·i, 1.6 s); the approximate fringe fades with them
    approx_clip = (geo.p(1040, 0)[0], drawable[1], limit_x + UNSURVEYED_FADE * s - geo.p(1040, 0)[0], drawable[3])
    breaks = c.contour_labels(cs, min_len=220 * s, gap=20 * s, exclusions=[(band[0], 0, w - band[0], h), rose_box],
                              levels=(10.0, 20.0, 50.0)) if not phone else []
    for i, lv in enumerate((50.0, 20.0, 10.0, 5.0)):
        begin = 0.2 + 0.12 * i
        for short in (True, False):
            sub = [q for q in cs if q.level == lv and ((q.length < 300 * s) == short)]
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
    thin = set()
    if phone:
        # inner rows only, every other one: 14 or so nearest the course
        inner = [i for i, (x, y, v) in enumerate(sounds) if abs(((i % 4) in (1, 2))) and x < limit_x]
        thin = set(inner[::2]) if len(inner) > 16 else set(inner)
    stagger = 0.04 if not phone else 0.06
    for i, (x, y, v) in enumerate(sounds):
        if x >= limit_x or (phone and i not in thin):
            continue
        ramp0 = geo.p(1000, 0)[0]
        o = 0.75 if x <= ramp0 else max(0.40, 0.75 - 0.35 * (x - ramp0) / (limit_x - ramp0))
        wk = weeks[i]
        frag = snd(v, x, y + (4 if not phone else 6), truth="measured", key=f"week:{wk.get('start', i)}",
                   fill=theme.ink2 if not night else theme.ink, opacity=round(o, 2))
        body.append(tl.fade_in(frag, 1.4 + stagger * i, 0.25, rise=0))   # no rise: 42 translates cost 6 KB
        printed += 1
    report["soundings_printed"] = printed
    # contour figures in the breaks
    figs = []
    for q, i0, i1 in breaks:
        x, y, ang = c.break_anchor(q, i0, i1)
        figs.append(lbl(str(int(q.level)), x, y + 3.5 * (1 if not phone else 1.6), "contour-figure", anchor="middle",
                        rotate=ang, fill=theme.ink2))
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
                          fill=theme.muted, tracking=caps_track, truth="measured" if j == 0 else None,
                          key="variation" if j == 0 else None)
                      for j, t in enumerate(var_lines))

    # ---- names and spot heights, by rank (2.2 + 0.1·rank)
    ranked = sorted(feats, key=lambda f: -f.value)
    heights = {f.name: (x, y) for f, x, y, _a in c.spot_heights(feats, cs, clearance=8 * s)}
    name_min_r = 16 * s
    phone_named = {f.name for f in ranked[:4]} if phone else None
    for rank, f in enumerate(ranked):
        parts = []
        hx, hy = heights.get(f.name, (f.x, f.y - 10 * s))
        named = f.r >= name_min_r if phone_named is None else f.name in phone_named
        if f.kind == "harbour":
            hx, hy = f.x, f.y - 0.84 * f.r - 6 * s          # the basin and the anchorage take the middle
        elif phone and named:
            hx, hy = f.x, f.y + 6
        if phone and not named:
            parts.append(snd(f.value, hx, hy, sub=f.sub, truth="measured", key=f"commits:{f.alias}", fill=theme.ink))
        else:
            parts.append(snd(f.value, hx, hy, sub=f.sub, role="label", truth="measured", key=f"commits:{f.alias}"))
        if named:
            if f.kind in LAND_KINDS:
                big = f.r >= BIG_NAME_R * s
                nx_, anchor = f.x, "middle"
                if phone:
                    if f.kind == "harbour":
                        nx_, ny_, anchor = f.x - f.r - 8, f.y + 8, "end"
                    else:
                        ny_ = f.y - 0.84 * f.r - 10
                else:
                    ny_ = f.y + (0.84 * f.r + 16 if f.kind == "harbour" else (18 if big else 15))
                parts.append(lbl(f.name, nx_, ny_, "label", anchor=anchor, caps=True,
                                 size=(17 if big else None) if not phone else None,
                                 tracking=(1.0 if big else caps_track) if not phone else caps_track))
            else:
                ny_ = f.y + 16 if not phone else f.y + f.r + 26
                parts.append(lbl(f.name, f.x, ny_, "place-water", anchor="middle"))
        body.append(tl.fade_in("".join(parts), 2.2 + 0.1 * rank, 0.4, rise=0))

    # ---- the name (discrete, two words), the thesis (3.1)
    if not phone:
        nx, ny = 64, 222
        ben = k.text("Ben", nx, ny, "display", edition=ed, scale=sc)
        wb = k.text_width("Ben ", "display", edition=ed, scale=sc)
        russ = k.text("Russell", nx + wb, ny, "display", edition=ed, scale=sc)
        body.append(tl.reveal(ben, 2.5))
        body.append(tl.reveal(russ, 3.0))
        body.append(tl.fade_in(k.text(thesis, 72, 296, "thesis", fill=theme.ink2, edition=ed, scale=sc), 3.1, 0.4, rise=4))
    else:
        nx, ny = 40, 150
        ben = k.text("Ben", nx, ny, "display", edition=ed, scale=sc)
        wb = k.text_width("Ben ", "display", edition=ed, scale=sc)
        russ = k.text("Russell", nx + wb, ny, "display", edition=ed, scale=sc)
        body.append(tl.reveal(ben, 2.5))
        body.append(tl.reveal(russ, 3.0))
        words = thesis.split()
        cut = len(words) // 2 + 1
        l1, l2 = " ".join(words[:cut]), " ".join(words[cut:])
        body.append(tl.fade_in(k.text(l1, 44, 212, "thesis", fill=theme.ink2, edition=ed, scale=sc)
                               + k.text(l2, 44, 258, "thesis", fill=theme.ink2, edition=ed, scale=sc), 3.1, 0.4, rise=4))

    # ---- title block, source diagram, margin captions (3.3)
    block = []
    if not phone:
        bx = 268
        ver = edition_d.get("version") or "—"
        ed_date = edition_d.get("date")
        ed_line = f"CHART NO. {N} · EDITION {ver}" + (f" · {_month(ed_date)}" if ed_date else "") + " · IALA REGION B"
        rows_t = [
            (560, f"THE OPEN WEB · FROM SURVEYS {first_year}–{upd_year}", "label", theme.ink, None, None),
            (616, "SOUNDINGS IN COMMITS · DATUM: MAIN", "label", theme.muted, None, None),
            (636, ed_line, "label", theme.muted, "measured", "chart-edition"),
            (656, f"CORRECTED THROUGH NOTICE {notices_n}", "label", theme.muted, "measured", "notices"),
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
            block.append(lbl(line, 470, 632 + 16 * j, "label", fill=theme.muted, caps=True, within=TITLE_BOX))
        k.exclude("title-block", *TITLE_BOX)
        # outside the neat line: unit line (the one label-caps run), N, folio, imprint, small corrections
        block.append(lbl(unit_line, 640, 14, "label-caps", anchor="middle", fill=theme.ink, key="unit"))
        block.append(lbl(str(N), 1262, 14, "label", anchor="end", fill=theme.muted, truth="measured", key="chart-number"))
        block.append(lbl(f"CHART NO. {N} · SHEET 1", 24, 735, "label-caps", fill=theme.muted, key="folio"))
        taken = data.get("taken") or (data.get("updated_at") or "")[:10]
        imprint = f"Published at github.com/{login} · {_date(taken)} · superintendence: build_assets.py"
        block.append(lbl(imprint, 600, 735, "label", anchor="middle", fill=theme.muted, caps=True))
        corr = data.get("corrections") or {}
        if corr:
            yr = max(corr)
            nums = [str(e.get("n")) for e in corr[yr] if e.get("n") is not None][-5:]
            if nums:
                block.append(lbl(f"Small corrections {yr} — {', '.join(nums)}", 1256, 735, "label", anchor="end",
                                 fill=theme.muted, caps=True))
    else:
        bx = 360
        ver = edition_d.get("version") or "—"
        rows_t = [
            (770, f"THE OPEN WEB · FROM SURVEYS {first_year}–{upd_year}", "label", theme.ink, False, None, None),
            (834, unit_line + " · DATUM: MAIN", "label-caps", theme.muted, True, None, None),
            (866, f"CHART NO. {N} · EDITION {ver} · NOTICE {notices_n}", "label", theme.muted, False, "measured", "chart-edition"),
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
    body.append(tl.fade_in("".join(block), 3.3, 0.4, rise=0))

    # ---- bearings, mark labels, fix labels, pencil notes (3.6)
    late = []
    centres = [(f.x, f.y) for f in feats]
    legs = list(zip(course, course[1:]))
    for li, (p, q) in enumerate(legs):
        if phone:
            break
        brg = c.compass_bearing(p, q)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
        nx_, ny_ = -(q[1] - p[1]) / L, (q[0] - p[0]) / L
        if li == len(legs) - 1:
            best = (mx - 20 * s, my + 28 * s)            # the entrance is busy: label in the basin's south arm
        else:
            cands = [(mx + nx_ * 12 * s * side, my + ny_ * 12 * s * side) for side in (1, -1)]
            best = max(cands, key=lambda pt: min((math.hypot(pt[0] - cx, pt[1] - cy) for cx, cy in centres), default=0))
        if best[0] < limit_x - 10:
            late.append(lbl(f"{round(brg) % 360:03d}°", round(best[0], 1), round(best[1] + 4, 1), "label", anchor="middle",
                            truth="measured", key="bearing"))
    # the lateral pair: labels slope (floating things), characters as charted
    r2 = geo.pi(*MARK_R2)
    g1 = geo.pi(*MARK_G1)
    ms = 1.0 if not phone else 1.3
    if not phone:   # the phone entrance is 24 px wide: the bodies and lit cores carry the marks there
        late.append(lbl('R "2" Fl R 4s', r2[0], r2[1] - 22 * ms, "label-italic", fill=theme.ink, anchor="middle"))
        late.append(lbl('G "1" Fl G 4s', g1[0] + 10 * ms, g1[1] + 14 * ms, "label-italic", fill=theme.ink))
    # dated fixes: the first-commit month of the feature each fix is taken off (WP2 off rustmapper, WP4 the harbour)
    for wp, f, side in ((course[1], vessel_ground, -1), (course[3], harbour, 1)):
        if f is None or phone:
            continue
        rr = repo_of.get(f.name, {})
        first = rr.get("first")
        if first:
            late.append(lbl(_month(first), wp[0] + 7 * side, wp[1] - 10, "label", fill=theme.ink2, truth="measured",
                            key=f"first:{f.alias}", anchor="start" if side > 0 else "end"))
    if not phone:
        nxp, nyp, rot = NOTE_AT
        late.append(lbl("sitemap.xml lies again", nxp, nyp, "note", fill=theme.muted, rotate=rot))
        if vessel_ground is not None:
            nw = k.text_width("sitemap.xml lies again", "note", edition=ed, scale=sc)
            ex_, ey_ = nxp + nw * math.cos(math.radians(rot)) + 6, nyp + nw * math.sin(math.radians(rot)) - 4
            tx_ = vessel_ground.x + PA_SHIFT[0] - 0.72 * vessel_ground.r
            ty_ = vessel_ground.y + PA_SHIFT[1] + 0.72 * vessel_ground.r
            late.append(f'<path d="M{_fmt(ex_)} {_fmt(ey_)}L{_fmt(tx_)} {_fmt(ty_)}" fill="none" '
                        f'{c.stroke("HAIR", theme.muted, 0.8)}/>')
        late.append(pa_label)
        late.append(lbl("SEE SHEET 3", *SEE_SHEET, "label", fill=theme.muted, caps=True))
    if ctx.no_sounding or data.get("no_sounding"):
        taken = data.get("taken") or (data.get("updated_at") or "")[:10]
        note = f"no soundings tonight — figures as surveyed {_date(taken)}"
        if not phone:   # caps: the note shares the sheet's lettering (a lowercase italic set costs 8 KB of defs)
            late.append(lbl(note, 340, 703, "label", fill=theme.muted, rotate=-3, anchor="middle", caps=True))
        else:
            late.append(lbl(note, 40, 735, "label", fill=theme.muted, rotate=-2, caps=True))
    body.append(tl.fade_in("".join(late), 3.6, 0.4, rise=0))

    # ---- lateral marks with their lights (lit from t = 0; G begins 0, R begins 2; one loop each)
    lights = []
    halo_r = 14 * ms if night else None
    for (pos, kind, lit_id, char, bg, top) in ((r2, "nun", "r2-lit", "Fl R 4s", 2.0, 16), (g1, "can", "g1-lit", "Fl G 4s", 0.0, 15)):
        body.append(use(kind, pos[0], pos[1], scale=ms))
        core = c.lit_core(pos[0], pos[1] - top * ms, theme, lit_id, r=1.5 * ms, halo_r=halo_r, prefix=prefix)
        flash = tl.flash(char, begin=bg, still="lit", name=lit_id.replace("-lit", "-flash")) if not phone else ""
        body.append(f"<g>{flash}{core}</g>")
        lights.append({"id": f"{NAME}-{lit_id}", "character": char, "color": theme.accent if kind == "nun" else theme.ok,
                       "bbox": [pos[0] - 8, pos[1] - 20, 16, 22]})
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
        boat = sail.wrap(hull + sails, pitch=-4.0, gid="boat")
        body.append(tl.reveal(boat, SAIL[0]))
        # the dated fixes are passed: nothing else moves after 28 s
        report["sail"] = {"begin": SAIL[0], "end": sail.end, "facing": sail.facing, "tacks": sail.tacks}
    else:
        pts = [(x, y) for x, y, _h in c.course_samples(course, 7)]
        glyph = f'<g transform="scale(-1 1)">{use("sloop-glyph", 0, 0, scale=1.4)}</g>'
        mark = use("fix", 0, 0)
        body.append(f'<g color="{theme.ink}">{tl.fixes(pts, SAIL[0], every=4.0, boat=glyph, mark=mark, name="sail")}</g>')
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
    entry["hero"] = {kk: x[kk] for kk in ("field", "place", "unclosed", "bracket", "soundings_printed", "culled", "sail")
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
