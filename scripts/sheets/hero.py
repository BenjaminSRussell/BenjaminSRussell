"""hero.py — Sheet 1 (v11, round 5, D1): the coast of the year.

Geography is time. One axis runs along the foot of the sheet from the first month of the survey to the survey
date, lettered like a latitude scale (month initials, two year figures); the right neat line is the survey date
and nothing is lettered beyond it. One row per repository with `named_min` non-sweep commit-days or more
(chart.toml `[hero] named_min`), ordered by those days: each row is a bank, a land shape whose half-thickness in
a month is proportional to that month's commit-days (sweep days excluded, so the housekeeping sweeps shape
nothing). A month with commit-days is land for the whole month and a month without is water; the coast runs
smoothly from month to month. Two derived tints mark where the month reached 5 and 10 commit-days, and the big
banks carry the coast vignette. The repositories under the threshold are merged into one last row in the lightest
ink, lettered "N more"; a repository with no non-sweep day is not drawn as land anywhere (it still counts in the
repository total).

Marks, all derived: the one light, `Fl 15s`, stands at the thickest point of the row of the repository that
`claims.scrape_interval` cites (Prometheus scrapes every 15 s there; measured, sha-cited); it is the only thing that
moves, a beat every 15 s, lit in the still editions. The one mark, `0.1.3 · PyPI`, is the edition record's date on
the row of the project it names. Mark lettering stands in the water beside its bank, clear of every coast. The
Rust-sitemap row is lettered `rustmapper` through chart.toml `[hero.aliases]`; every other row prints the GitHub
name as written. The title block: the name, the thesis, the role line, the datum and date in fine print.

Nothing is placed by hand and nothing data-placed can collide: one axis, fixed rows, the name above each bank in
the row's own band. Every glyph goes through typeset (ctx.k), every animation through the Timeline (ctx.tl), every
line through chartlib. The desk sets the title block in the left third and the rows in the right two thirds; the
phone stacks the title block over the rows at full width. Same drawing, two layouts.
"""
from __future__ import annotations

import datetime as dt
import math

import chartlib as c
import edition as E
import tokens

NAME = "hero"
KIND = "chart"
SIZES = {"desk": (1280, 624), "phone": (720, 1140)}
EDITIONS = None   # the runner's default six plus HERO_EXTRA (phone stills)

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the role line, the fine print, the row names, the axis letters and the foot are set upper-case through role "
     "`label` with explicit tracking (desk 1.6, phone 1.0); no run uses `label-caps`",
     "check_type allows one label-caps run per sheet; the sheet has a dozen caps lines"),
    ("Name at 88 on the desk (D1: display size)",
     "the desk name is set at 88 (phone 132); the thesis breaks into two lines on both scales",
     "the desk title block is the left third (56–460 px); the name at 141 is 516 px wide and the thesis at 41 is 580"),
    ("Role line on two lines on the desk",
     "CRAWL AND DATA INFRASTRUCTURE / PYTHON AND RUST, one left edge; the phone keeps it on one line",
     "486 px at 19 px tracked 1.0 does not fit the left third"),
    ("Row names above their banks",
     "each row's name (and language tag) is lettered at the axis start above its bank, in the row's own band; the "
     "gap from a bank to the next row's name is twice the gap from a name to its own bank",
     "the timeline takes the right two thirds (from 38 %); a name column beside it would halve the months"),
    ("Half-thickness floor",
     "a month with commit-days draws at least `floor` px half-thickness (desk 3, phone 3) so a one-day month "
     "prints", "thickness ∝ commit-days above the floor; a pen cannot draw a 1.3 px bank"),
    ("Thickness scale steps down",
     "half-thickness is the band's half at 15 commit-days a month; a busier month steps the whole sheet's scale down "
     "so it still fits its band", "rows are fixed; the scale is the one free constant and it is one constant for "
                                  "every row"),
    ("Month plateaus",
     "a month with commit-days is land from its first to its last day (the coast rises over q = 20 % of the month at "
     "each end of a run), crowned at mid-month; the transition between two active months is a monotone cubic",
     "a burst's width is honest to the month; no land in a month without a commit-day"),
    ("Last month's letter",
     "the survey month's initial is set flush to the neat line when the month is too short to centre it in",
     "the axis runs through October; nothing is lettered beyond the survey date"),
    ("Mark lettering in the water",
     "the light's character and the edition label stand on the bank's centreline in the water beyond its end (or "
     "before its start), at least 8 px from every coast, with a hairline leader back to the mark",
     "lettering over a coast is unreadable at 390 px"),
    ("Light character upright",
     "`Fl 15s` is set upright in role `label`, not italic caps",
     "the sheet's rule is that every printed figure is measured and upright (D5); the interval is measured"),
    ("Vignette clipped to its row", "the coast vignette is clipped to the row's band below its name",
     "a real vignette stops at the next coast"),
    ("No draw-in, no opening",
     "the whole sheet is on the paper at t = 0; motion.opening_end_s is 0 and coverage at 0 s is that of the still",
     "D1: the light is the only thing that moves"),
    ("No pencil note, no no-sounding note",
     "a cache-failed run prints nothing extra: the date in the fine print is the survey date the figures carry",
     "the pencil note is cut (D6); a stale date is itself the honest statement"),
]

# ---------------------------------------------------------------- layout (sheet space)
RULES = {"desk": (24, 30), "phone": (14, 19)}
TRACK = {"desk": 1.6, "phone": 1.0}
NAME_SIZE = {"desk": 88, "phone": 132}
NAME_TRACK = {"desk": -1.5, "phone": -2.0}
TITLE = {
    "desk": {"x": 56, "name_y": 132, "thesis_y": (202, 248), "role_y": (296, 322), "fine_y": (362, 388, 414),
             "box": (52, 44, 412, 384)},
    "phone": {"x": 36, "name_y": 146, "thesis_y": (230, 276), "role_y": (322,), "fine_y": (356, 388),
              "box": (30, 30, 668, 374)},
}
ROWS = {
    # x0: the axis start (first month) and the names' left edge; top/pitch: the row bands; label_dy: the name's
    # baseline below the band top; bank_dy: the bank's highest coast below the band top; gap: water kept under the
    # bank before the next band (≥ 2 × the name-to-bank gap)
    "desk": {"x0": 486, "top": 38, "pitch": 62, "label_dy": 16, "bank_dy": 21, "gap": 9, "floor": 3.0},
    "phone": {"x0": 36, "top": 404, "pitch": 80, "label_dy": 24, "bank_dy": 30, "gap": 16, "floor": 3.0},
}
AXIS = {"desk": {"y": 540, "letters": 562, "years": 586}, "phone": {"y": 1052, "letters": 1080, "years": 1108}}
NAMED_MIN_DEFAULT = 5
FULL_MONTH = 15                   # commit-days a month that fill a bank's band; busier months step the scale down
LEVELS = (5, 10)                  # the derived tints: where the month reached 5 and 10 commit-days
TINT_OPACITY = (0.18, 0.34)
PLATEAU = (0.2, 12.0, 0.88)       # rise over 20 % of the month (≤ 12 px); shoulders at 88 % of the mid-month height
VIGNETTE_MIN = 15                 # rows with this many commit-days carry the coast vignette ...
VIGNETTE_HALF = 8.0               # ... on the banks at least this thick (px half-thickness): land, not a sliver
VIGNETTE = {"step": 5.0, "lengths": (3.0, 1.8), "opacities": (0.45, 0.28), "gaps": (1.2, 1.4)}
STEP = 3.0                        # px between coast samples
JITTER = 0.5                      # px, the coast's hand (keyed by repo and sample, never by data)
LIGHT_R = {"desk": 2.2, "phone": 3.0}
HALO_R = {"desk": {"day": 10, "night": 14}, "phone": {"day": 13, "night": 18}}   # the beat is visible by day too
CLEAR = 8.0                       # px of water between mark lettering and any coast
LETTER_GAP = 12.0                 # px from a bank's end to its mark lettering
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
MONTHS_MIXED = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
EASTERN = {"-0400", "-0500"}


# ---------------------------------------------------------------- small helpers
def _fmt(v):
    return E.fmt(v)


def _date(iso: str) -> str:
    y, m, d = iso[:4], int(iso[5:7]), int(iso[8:10])
    return f"{d} {MONTHS_MIXED[m - 1]} {y}"


def _month_date(iso: str) -> str:
    return f"{MONTHS_MIXED[int(iso[5:7]) - 1]} {iso[:4]}"


def _iso(s) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError):
        return None


def _next_month(d: dt.date) -> dt.date:
    return dt.date(d.year + (d.month // 12), d.month % 12 + 1, 1)


def _mkey(d: dt.date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def _monotone(xs: list[float], ys: list[float]):
    """Fritsch–Carlson monotone cubic through (xs, ys): a sampler f(x). Between two control points it never
    leaves their range, so a bank never dips below water or overshoots its month."""
    n = len(xs)
    if n == 1:
        return lambda x: ys[0]
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    d = [(ys[i + 1] - ys[i]) / h[i] if h[i] else 0.0 for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, n - 1):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    for i in range(n - 1):
        if d[i] == 0:
            m[i] = m[i + 1] = 0.0
        else:
            a, b = m[i] / d[i], m[i + 1] / d[i]
            s = a * a + b * b
            if s > 9:
                t = 3 / math.sqrt(s)
                m[i], m[i + 1] = t * a * d[i], t * b * d[i]

    def f(x: float) -> float:
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        i = 0
        while i < n - 2 and x > xs[i + 1]:
            i += 1
        hh = h[i] or 1.0
        t = (x - xs[i]) / hh
        t2, t3 = t * t, t * t * t
        return ((2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * hh * m[i]
                + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * hh * m[i + 1])
    return f


def _rect_dist(px: float, py: float, r: tuple) -> float:
    x0, y0, x1, y1 = r
    dx = max(x0 - px, 0.0, px - x1)
    dy = max(y0 - py, 0.0, py - y1)
    return math.hypot(dx, dy)


# ---------------------------------------------------------------- data → rows
def sweep_dates(data: dict) -> set[str]:
    out = {str(d)[:10] for d in (data.get("sweep_dates") or [])}
    out |= {str(s.get("date", ""))[:10] for s in (data.get("sweeps") or []) if s.get("date")}
    return out


def repo_months(repo: dict, sweeps: set[str]) -> tuple[dict[str, int], str | None, str | None]:
    """(months {YYYY-MM: commit-days}, first, last) with every sweep day excluded, for every repository alike
    (a sweep day is out for all of them, named or not): the record's own `months`/`first_ns`/`last_ns` when the
    data builder wrote them, else computed here from `days` and `sweeps`."""
    months = repo.get("months")
    if isinstance(months, dict) and "first_ns" in repo:
        clean = {str(k): int(v) for k, v in months.items() if int(v or 0) > 0}
        return dict(sorted(clean.items())), repo.get("first_ns"), repo.get("last_ns")
    out: dict[str, int] = {}
    first = last = None
    for day in repo.get("days") or []:
        d = str(day.get("d", ""))[:10]
        if not d or d in sweeps:
            continue
        out[d[:7]] = out.get(d[:7], 0) + 1
        first = d if first is None or d < first else first
        last = d if last is None or d > last else last
    return dict(sorted(out.items())), first, last


def plan_rows(data: dict, cfg: dict) -> dict:
    """The rows the sheet draws, from stats.json alone: named rows (days ≥ named_min, ordered by days), the
    merged `more` row, the repositories with no non-sweep day, and the row of the light and the mark."""
    hero_cfg = cfg.get("hero", {}) or {}
    named_min = int(hero_cfg.get("named_min", NAMED_MIN_DEFAULT))
    aliases = dict(hero_cfg.get("aliases", {}) or {})
    sweeps = sweep_dates(data)
    repos = data.get("repos") or []
    if not repos:
        raise RuntimeError("hero: stats.json carries no repositories")
    if not any(r.get("days") or isinstance(r.get("months"), dict) for r in repos):
        raise RuntimeError("hero: stats.json carries no commit-days per repository (repos[].days); refusing to invent them")
    rows, small, zero, seen = [], [], [], set()
    for r in repos:
        if r["name"] in seen:          # a repository listed twice (a live survey's duplicate) is drawn once
            continue
        seen.add(r["name"])
        months, first, last = repo_months(r, sweeps)
        days = sum(months.values())
        rec = {"repo": r["name"], "name": aliases.get(r["name"], r["name"]), "days": days, "months": months,
               "first_ns": first, "last_ns": last, "language": r.get("language") or None}
        if days >= named_min:
            rows.append(rec)
        elif days > 0:
            small.append(rec)
        else:
            zero.append(r["name"])
    rows.sort(key=lambda t: (-t["days"], t["name"].lower()))
    small.sort(key=lambda t: (-t["days"], t["name"].lower()))
    merged: dict[str, int] = {}
    for rec in small:
        for m, n in rec["months"].items():
            merged[m] = merged.get(m, 0) + n
    more = None
    if small:
        more = {"repo": None, "name": f"{len(small)} more", "days": sum(merged.values()),
                "months": dict(sorted(merged.items())),
                "first_ns": min(t["first_ns"] for t in small), "last_ns": max(t["last_ns"] for t in small),
                "language": None, "repos": [t["repo"] for t in small]}
    # the light: the row of the repository claims.scrape_interval cites (measured, sha-cited), else none
    claim = (data.get("claims") or {}).get("scrape_interval") or {}
    light = None
    if claim.get("measured") and claim.get("sha") and claim.get("value") is not None:
        src_repo = str(claim.get("source", "")).split(":", 1)[0]
        row = next((t for t in rows if t["repo"] == src_repo), None)
        if row is not None:
            period = int(claim["value"])
            light = {"row": row["repo"], "character": f"Fl {period}s", "period": period}
    # the mark: the edition's date on the row of the project it names
    ed = data.get("edition") or {}
    mark = None
    if ed.get("version") and ed.get("date") and not ed.get("stale"):
        proj = str(ed.get("project", ""))
        row = next((t for t in rows if t["name"] == proj or t["repo"] == proj), None)
        if row is not None:
            mark = {"row": row["repo"], "date": str(ed["date"])[:10], "label": f"{ed['version']} · PyPI"}
    return {"named_min": named_min, "rows": rows, "more": more, "zero": zero, "light": light, "mark": mark,
            "sweeps": sorted(sweeps), "small": [t["repo"] for t in small]}


def axis_span(data: dict, plan: dict) -> tuple[dt.date, dt.date]:
    """(first day of the first month with a non-sweep day, the survey date)."""
    firsts = [t["first_ns"] for t in plan["rows"] + ([plan["more"]] if plan["more"] else []) if t["first_ns"]]
    t0 = _iso(min(firsts)) if firsts else _iso(data.get("first_commit"))
    t1 = _iso(data.get("taken")) or _iso(data.get("updated_at"))
    if t0 is None or t1 is None:
        raise RuntimeError("hero: stats.json carries no survey date (taken) or no first commit-day")
    t0 = t0.replace(day=1)
    if t1 <= t0:
        raise RuntimeError(f"hero: survey date {t1} is not after the first month {t0}")
    return t0, t1


def _eastern(data: dict) -> bool:
    offs: set[str] = set()
    for r in data.get("repos") or []:
        offs |= {str(k) for k, v in (r.get("tz_offsets") or {}).items() if int(v or 0) > 0}
    if not offs:
        offs = {str(k) for k in (data.get("tz_offsets") or {})}
    return bool(offs) and offs <= EASTERN


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
    track = TRACK[sc]
    lbl_h = tokens.ROLES[sc]["label"][1]            # 19 desk / 26 phone
    report: dict = ctx.extra
    T, R, A = TITLE[sc], ROWS[sc], AXIS[sc]
    r0, r1 = RULES[sc]
    x_end = w - r1                                 # the survey date is the right neat line
    x0 = R["x0"]

    def lbl(text, x, y, role="label", anchor="start", fill=None, caps=False, **kw):
        tracking = kw.pop("tracking", None)
        if caps:
            text, tracking = str(text).upper(), track if tracking is None else tracking
        return k.label(str(text), x, y, role, anchor=anchor, fill=fill, edition=ed, scale=sc, tracking=tracking, **kw)

    def width(text, role="label", **kw):
        return k.text_width(str(text), role, edition=ed, scale=sc, **kw)

    # ---- data
    plan = plan_rows(data, cfg)
    rows = list(plan["rows"])
    if not rows:
        raise RuntimeError(f"hero: no repository reaches {plan['named_min']} non-sweep commit-days; nothing to draw")
    drawn = rows + ([plan["more"]] if plan["more"] else [])
    repos = data.get("repos") or []
    N = int(data.get("repo_count") or len(repos))
    taken = str(data.get("taken") or data.get("updated_at") or "")[:10]
    login = data.get("login") or cfg.get("chart", {}).get("login", "")
    thesis = cfg.get("copy", {}).get("thesis", "I survey a web that is wrong about itself.")
    role_line = cfg.get("copy", {}).get("role_line", "Crawl and data infrastructure · Python and Rust")
    t0, t1 = axis_span(data, plan)
    span_days = (t1 - t0).days

    def x_of(d: dt.date) -> float:
        return x0 + (x_end - x0) * (d - t0).days / span_days

    # ---- the bands: fixed; a sheet with more rows than the pitch allows tightens the pitch, never overlaps
    top = R["top"]
    pitch = min(float(R["pitch"]), (A["y"] - 6 - top) / len(drawn))
    half_max = (pitch - R["bank_dy"] - R["gap"]) / 2
    if half_max < 6:
        raise RuntimeError(f"hero: {len(drawn)} rows do not fit the {sc} sheet (named_min {plan['named_min']}); "
                           "raise named_min")
    max_month = max((n for t in drawn for n in t["months"].values()), default=1)
    k_half = half_max / max(FULL_MONTH, max_month)
    floor = R["floor"]
    for i, t in enumerate(drawn):
        bt = top + pitch * i
        t["band"] = (round(bt, 1), round(bt + pitch, 1))
        t["label_y"] = bt + R["label_dy"]
        t["yc"] = bt + R["bank_dy"] + half_max

    # ---- the banks: per row, one land polygon per run of consecutive active months
    def profile(months: dict[str, int], level: float, use_floor: bool):
        """[(xs, ys)] control points per run of months whose commit-days exceed `level` (half-thickness above
        `level`): each month is a plateau from its first to its last day, crowned at mid-month."""
        q_frac, q_max, shoulder = PLATEAU
        m = t0
        runs, cur = [], []
        while m <= t1:
            n = int(months.get(_mkey(m), 0))
            if n > level:
                hh = (max(k_half * n, floor) if use_floor else k_half * n) - level * k_half
                cur.append((x_of(m), x_of(min(_next_month(m), t1)), hh))
            elif cur:
                runs.append(cur)
                cur = []
            m = _next_month(m)
        if cur:
            runs.append(cur)
        out = []
        for run in runs:
            xs, ys = [run[0][0]], [0.0]
            for xa, xb, hh in run:
                q = min(q_frac * (xb - xa), q_max)
                mid = (xa + xb) / 2
                pts = [(xa + q, shoulder * hh), (mid, hh), (xb - q, shoulder * hh)] if xb - xa > 3 * q else [(mid, hh)]
                for px, py in pts:
                    if px > xs[-1] + 0.5:
                        xs.append(px)
                        ys.append(py)
            if run[-1][1] > xs[-1] + 0.5:
                xs.append(run[-1][1])
                ys.append(0.0)
            else:
                ys[-1] = 0.0
            out.append((xs, ys))
        return out

    def polygon(xs, ys, yc: float, jname: str | None):
        f = _monotone(xs, ys)
        xa, xb = xs[0], xs[-1]
        n = max(2, int((xb - xa) / STEP))
        j = c.Jitter(seed, f"hero/coast/{jname}") if jname else None
        tops, bots = [], []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            hh = max(0.0, f(x))
            hb = hh
            if j is not None and 0 < i < n and hh > 1.0:
                hh = max(0.5, hh + max(-1.0, min(1.0, j.gauss(0.0, JITTER))))
                hb = max(0.5, hb + max(-1.0, min(1.0, j.gauss(0.0, JITTER))))
            tops.append((x, yc - min(hh, half_max + 1)))
            bots.append((x, yc + min(hb, half_max + 1)))
        return tops + bots[::-1][1:-1]

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

    body.append(c.frame(w, h, theme, "minute-bars", rules=RULES[sc]))

    land_svg, text_svg, mark_svg = [], [], []
    row_report = []
    all_polys: list[list[tuple[float, float]]] = []
    for i, t in enumerate(drawn):
        more = t["repo"] is None
        yc = t["yc"]
        blocks = []
        for xs, ys in profile(t["months"], 0.0, True):
            poly = polygon(xs, ys, yc, t["name"])
            blocks.append({"x0": xs[0], "x1": xs[-1], "poly": poly, "d": c.smooth_path(poly, True, 1),
                           "half": max(ys), "xs": xs, "ys": ys})
        t["blocks"] = blocks
        if not blocks:
            continue
        all_polys.extend(b["poly"] for b in blocks)
        d_all = "".join(b["d"] for b in blocks)
        op = f' fill-opacity="{c.op(0.4)}"' if more else ""
        land_svg.append(f'<path d="{d_all}" fill="{theme.land}"{op}/>')
        for level, opac in zip(LEVELS, TINT_OPACITY):
            tints = profile(t["months"], float(level), False)
            if not tints:
                continue
            dt_ = "".join(c.smooth_path(polygon(xs, ys, yc, None), True, 1) for xs, ys in tints)
            o = opac * (0.4 if more else 1.0)
            land_svg.append(f'<path d="{dt_}" fill="{theme.ink2}" fill-opacity="{c.op(o)}" '
                            f'{c.stroke("HAIR", theme.ink2, 0.45 if not more else 0.25)}/>')
        if more:
            land_svg.append(f'<path d="{d_all}" fill="none" {c.stroke("HAIR", theme.ink2, 0.6)}/>')
        else:
            cs = [c.Contour(0.0, b["poly"], True, c.polyline_length(b["poly"], True), False) for b in blocks]
            land_svg.append(c.coastline(cs, theme, every=1))
        if not more and t["days"] >= VIGNETTE_MIN:
            clip = f"row{i}"
            y_clip = t["label_y"] + 5
            defs.append(f'<clipPath id="{clip}"><rect x="{_fmt(x0 - 12)}" y="{_fmt(y_clip)}" '
                        f'width="{_fmt(x_end - x0 + 10)}" height="{_fmt(t["band"][1] - y_clip)}"/></clipPath>')
            vig = "".join(c.coast_vignette(b["poly"], theme, jit.sub(t["name"]), **VIGNETTE)
                          for b in blocks if b["half"] >= VIGNETTE_HALF)
            if vig:
                land_svg.append(f'<g clip-path="url(#{clip})">{vig}</g>')
        row_report.append({"repo": t["repo"], "name": t["name"], "days": t["days"], "months": t["months"],
                           "first_ns": t["first_ns"], "last_ns": t["last_ns"], "language": t["language"],
                           "y": round(yc, 1), "band": list(t["band"]), "more": more, "repos": t.get("repos"),
                           "blocks": [{"x0": round(b["x0"], 1), "x1": round(b["x1"], 1),
                                       "top": round(min(p[1] for p in b["poly"]), 1),
                                       "bottom": round(max(p[1] for p in b["poly"]), 1)} for b in blocks]})

    # ---- the row names above their banks, the language tag in lighter ink
    for t in drawn:
        more = t["repo"] is None
        name_w = width(t["name"].upper(), tracking=track)
        text_svg.append(lbl(t["name"], x0, t["label_y"], fill=theme.muted if more else theme.ink, caps=True,
                            truth="measured", key=("more" if more else f"row:{t['repo']}")))
        t["name_x1"] = x0 + name_w
        if t["language"]:
            tag_w = width(t["language"].upper(), tracking=track)
            if x0 + name_w + 12 + tag_w <= x_end - 6:
                text_svg.append(lbl(t["language"], x0 + name_w + 12, t["label_y"], fill=theme.muted, caps=True))
                t["name_x1"] = x0 + name_w + 12 + tag_w

    # ---- mark lettering: on the bank's centreline in the water beyond the bank (or before it), clear of coasts
    placements = []

    def place(t: dict, ax: float, text: str) -> dict:
        tw = width(text)
        y = t["yc"] + lbl_h * 0.36
        blocks = sorted(t["blocks"], key=lambda b: b["x0"])
        home = next((b for b in blocks if b["x0"] - 1 <= ax <= b["x1"] + 1),
                    min(blocks, key=lambda b: min(abs(b["x0"] - ax), abs(b["x1"] - ax))))
        i = blocks.index(home)
        nxt = blocks[i + 1]["x0"] if i + 1 < len(blocks) else x_end
        prv = blocks[i - 1]["x1"] if i > 0 else x0
        cands = [(home["x1"] + LETTER_GAP, "start", "right"), (home["x0"] - LETTER_GAP, "end", "left")]
        above_y = t["label_y"]
        for tx, anchor, side in cands:
            xa_, xb_ = (tx, tx + tw) if anchor == "start" else (tx - tw, tx)
            if side == "right" and xb_ > min(nxt - LETTER_GAP, x_end - 6):
                continue
            if side == "left" and xa_ < max(prv + LETTER_GAP, x0):
                continue
            box = (xa_ - 1, y - lbl_h * 0.75, xb_ + 1, y + lbl_h * 0.1)
            clear = min((_rect_dist(px, py, box) for poly in all_polys for px, py in poly), default=99.0)
            if clear >= CLEAR:
                return {"x": tx, "y": y, "anchor": anchor, "side": side, "box": box, "clear": round(clear, 1)}
        # last resort: above the bank, beside the row's name, in the band's lettering strip
        tx = max(t["name_x1"] + 16, ax - tw / 2)
        tx = min(tx, x_end - 6 - tw)
        box = (tx - 1, above_y - lbl_h * 0.75, tx + tw + 1, above_y + lbl_h * 0.1)
        clear = min((_rect_dist(px, py, box) for poly in all_polys for px, py in poly), default=99.0)
        return {"x": tx, "y": above_y, "anchor": "start", "side": "above", "box": box, "clear": round(clear, 1)}

    def leader(mx: float, my: float, p: dict, r_mark: float) -> str:
        if p["side"] == "above":
            return ""
        xa_ = mx + r_mark if p["side"] == "right" else mx - r_mark
        xb_ = p["box"][0] - 2 if p["side"] == "right" else p["box"][2] + 2
        if abs(xb_ - xa_) < 6:
            return ""
        return f'<path d="M{_fmt(xa_)} {_fmt(my)}H{_fmt(xb_)}" fill="none" {c.stroke("HAIR", theme.ink, 0.8, caps="butt")}/>'

    lights = []
    light = plan["light"]
    if light:
        t = next(t for t in drawn if t["repo"] == light["row"])
        best = max(((xs[j], ys[j]) for b in t["blocks"] for xs, ys in [(b["xs"], b["ys"])] for j in range(len(xs))),
                   key=lambda p: p[1])
        lx, ly = E.I(best[0]), E.I(t["yc"])
        ms = 1.0 if not phone else 1.35
        lit_id = "light-lit"
        core = c.lit_core(lx, ly, theme, lit_id, r=LIGHT_R[sc], halo_r=HALO_R[sc]["night" if night else "day"], prefix=prefix)
        flash = tl.flash(light["character"], begin=0.0, still="lit", name="light-flash")
        p = place(t, lx, light["character"])
        mark_svg.append(leader(lx, ly, p, 6 * ms))
        mark_svg.append(use("flare", lx, ly, scale=ms)
                        + f'<path d="{_star_d(lx, ly, 4.6 * ms, 1.9 * ms)}" fill="{theme.land}" {c.stroke("PEN", theme.ink)}/>'
                        + f"<g>{flash}{core}</g>")
        text_svg.append(lbl(light["character"], p["x"], p["y"], anchor=p["anchor"], fill=theme.ink,
                            truth="measured", key="light"))
        placements.append({"what": "light", "text": light["character"], **{kk: p[kk] for kk in ("side", "clear")},
                           "box": [round(v, 1) for v in p["box"]]})
        lights.append({"id": f"{NAME}-{lit_id}", "character": light["character"], "color": theme.light_core,
                       "period": light["period"], "row": light["row"], "x": lx, "y": ly})
    mark = plan["mark"]
    mark_report = None
    if mark:
        t = next(t for t in drawn if t["repo"] == mark["row"])
        md = _iso(mark["date"])
        if md and t0 <= md <= t1:
            mx, my = E.I(x_of(md)), E.I(t["yc"])
            ms = 1.0 if not phone else 1.35
            p = place(t, mx, mark["label"])
            mark_svg.append(leader(mx, my, p, 3.5 * ms))
            mark_svg.append(f'<circle cx="{_fmt(mx)}" cy="{_fmt(my)}" r="{_fmt(3.2 * ms)}" fill="{theme.land}" '
                            f'{c.stroke("PEN", theme.ink)}/><circle cx="{_fmt(mx)}" cy="{_fmt(my)}" '
                            f'r="{_fmt(1.2 * ms)}" fill="{theme.ink}"/>')
            text_svg.append(lbl(mark["label"], p["x"], p["y"], anchor=p["anchor"], fill=theme.ink,
                                truth="measured", key="edition"))
            placements.append({"what": "edition", "text": mark["label"], **{kk: p[kk] for kk in ("side", "clear")},
                               "box": [round(v, 1) for v in p["box"]]})
            mark_report = {**mark, "x": mx, "y": my}
    report["lights"] = lights
    report["mark"] = mark_report
    report["placements"] = placements

    # ---- the axis along the foot: a latitude scale — ticks at month starts, initials, the two years
    ay = A["y"]
    tick = 6 if not phone else 8
    ticks = [f"M{_fmt(x0)} {_fmt(ay)}H{_fmt(x_end)}"]
    m = t0
    year_x: dict[int, float] = {}
    letters = []
    while m <= t1:
        xm = x_of(m)
        ticks.append(f"M{_fmt(xm)} {_fmt(ay)}v{tick}")
        xe = x_of(min(_next_month(m), t1))
        initial = MONTHS[m.month - 1][0]
        iw = width(initial)
        if iw + 6 <= xe - xm:
            letters.append((initial, (xm + xe) / 2, "middle"))
        elif _next_month(m) > t1:      # the survey month, cut short by the survey date: flush to the neat line
            letters.append((initial, x_end, "end"))
        if m.month == 1 or m == t0:
            year_x.setdefault(m.year, xm)
        m = _next_month(m)
    ticks.append(f"M{_fmt(x_end)} {_fmt(ay)}v{tick}")
    body.append(f'<path d="{"".join(ticks)}" fill="none" {c.stroke("PEN", theme.ink2, 0.9, caps="butt")}/>')
    for initial, xm, anchor in letters:
        text_svg.append(lbl(initial, xm, A["letters"], anchor=anchor, fill=theme.ink2))
    for yr, xm in sorted(year_x.items()):
        anchor = "start"
        if xm + width(str(yr)) > x_end:
            anchor, xm = "end", x_end
        text_svg.append(lbl(str(yr), xm, A["years"], anchor=anchor, fill=theme.ink2, truth="measured", key=f"year:{yr}"))

    body.append("".join(land_svg))                        # land is on the sheet at t = 0
    body.append("".join(mark_svg))

    # ---- the title block: the name, the thesis on two lines, the role line, the fine print
    block = []
    bx, box = T["x"], T["box"]
    nsz = NAME_SIZE[sc]
    ben = k.text("Ben", bx, T["name_y"], "display", size=nsz, tracking=NAME_TRACK[sc], edition=ed, scale=sc, within=box)
    wb = k.text_width("Ben ", "display", size=nsz, tracking=NAME_TRACK[sc], edition=ed, scale=sc)
    russ = k.text("Russell", bx + wb, T["name_y"], "display", size=nsz, tracking=NAME_TRACK[sc], edition=ed, scale=sc,
                  within=box)
    block.append(ben + russ)
    words = thesis.split()
    cut = len(words) // 2 + 1
    for y, line in zip(T["thesis_y"], (" ".join(words[:cut]), " ".join(words[cut:]))):
        block.append(k.text(line, bx, y, "thesis", fill=theme.ink2, edition=ed, scale=sc, within=box))
    role_parts = [p_.strip() for p_ in role_line.split("·")] if len(T["role_y"]) > 1 else [role_line]
    for y, line in zip(T["role_y"], role_parts):
        block.append(lbl(line, bx, y, fill=theme.ink, caps=True, within=box))
    eastern = " · EASTERN TIME" if _eastern(data) else ""
    if phone:
        fine = [f"{N} REPOSITORIES · AUTHOR'S COMMITS · DATUM: MAIN", f"SWEEP DAYS EXCLUDED · {_date(taken)}{eastern}"]
        keys = ["datum", "survey-date"]
    else:
        fine = [f"{N} REPOSITORIES · AUTHOR'S COMMITS", "DATUM: MAIN · SWEEP DAYS EXCLUDED", f"{_date(taken)}{eastern}"]
        keys = ["repositories", "datum", "survey-date"]
    for y, line, key in zip(T["fine_y"], fine, keys):
        block.append(lbl(line, bx, y, fill=theme.ink2, caps=True, within=box, truth="measured", key=key))
    if not phone:   # the foot: the GitHub URL and the date, outside the neat line, nothing else
        block.append(lbl(f"github.com/{login} · {_date(taken)}", x_end, h - 6, anchor="end", fill=theme.ink2,
                         caps=True, truth="measured", key="imprint"))
    body.append("".join(block))
    body.append("".join(text_svg))

    # ---- the report
    report["rows"] = row_report
    report["counts"] = {"repositories": N, "rows": len(rows), "more": len(plan["small"]), "zero": len(plan["zero"]),
                        "more_days": plan["more"]["days"] if plan["more"] else 0}
    report["zero"] = plan["zero"]
    report["named_min"] = plan["named_min"]
    report["axis"] = {"start": t0.isoformat(), "end": t1.isoformat(), "x0": x0, "x_end": x_end,
                      "px_per_month": round((x_end - x0) / (span_days / 30.44), 1),
                      "letters": "".join(l_ for l_, _x, _a in letters), "years": sorted(year_x)}
    report["scale"] = {"half_px_per_day": round(k_half, 3), "half_max": round(half_max, 1), "floor": floor,
                       "max_month": max_month, "full_month": FULL_MONTH, "pitch": round(pitch, 1)}
    report["sweeps"] = plan["sweeps"]
    report["symbols_used"] = sorted(symbols_used)
    report["no_sounding"] = bool(ctx.no_sounding or data.get("no_sounding"))
    defs.append(k.glyph_defs())
    return E.svg(ed, w, h, "".join(body), "".join(defs), sheet=NAME)


def _star_d(cx: float, cy: float, r_out: float, r_in: float, points: int = 5) -> str:
    d = []
    for i in range(points * 2):
        a = math.radians(i * 180 / points - 90)
        rr = r_out if i % 2 == 0 else r_in
        d.append(("M" if i == 0 else "L") + f"{_fmt(cx + rr * math.cos(a))} {_fmt(cy + rr * math.sin(a))}")
    return "".join(d) + "Z"


def alt(data, cfg) -> str:
    n = int(data.get("repo_count") or len(data.get("repos") or []))
    try:
        plan = plan_rows(data, cfg)
        t0, t1 = axis_span(data, plan)
        names = [t["name"] for t in plan["rows"][:2]]
    except Exception:
        names, t0, t1 = [], None, None
    span = f", {_month_date(t0.isoformat())} to {_month_date(t1.isoformat())}" if t0 and t1 else ""
    big = f", {names[0]} and {names[1]} the largest" if len(names) == 2 else (f", {names[0]} the largest" if names else "")
    return f"Chart of Ben Russell's {n} repositories as a coastline{span}{big}. One row is one repository."


# ---------------------------------------------------------------- build-report hook
def _report_hook(ctx, svg_text: str, entry: dict) -> None:
    if getattr(ctx, "sheet", None) != NAME:
        return
    x = ctx.extra
    for key in ("lights", "symbols_used"):
        if key in x:
            entry[key] = x[key]
    entry["features"] = [{"repo": r["repo"], "name": r["name"], "commit_days": r["days"], "y": r["y"]}
                         for r in x.get("rows", []) if not r["more"]]
    entry["area_law"] = "half-thickness∝commit-days (sweeps out)"
    entry["hero"] = {kk: x[kk] for kk in ("rows", "counts", "zero", "named_min", "axis", "scale", "sweeps", "mark",
                                          "placements", "no_sounding") if kk in x}


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
