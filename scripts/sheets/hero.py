"""hero.py — Sheet 1 (v11, round 5, D1 + F1): the coast of the year, by the week.

Geography is time. One axis runs along the foot from the Monday of the first month of the survey to the survey
date, lettered like a latitude scale (week ticks, month ticks and initials, two year figures, the survey date at the
last tick, 14 px inside the border). One row per repository with `named_min` non-sweep commit-days or more
(chart.toml `[hero] named_min`), ordered by those days; the profile repository (the one named like the login) is
never a named row. Each row is a run of banks: a week with commit-days is land for that week only, its
half-thickness linear in that week's commit-days (0–7), one scale for the sheet so the busiest week fills about
0.8 of the bank's band; a single-day week is an islet. Sweep days are out of every shape and figure. Land is buff
with its coastline, a two-step shallows tint runs along every coast, the paper is the water, and the big banks
carry the coast vignette. Every repository not named is merged into
the last row, lettered `N MORE` so that the named rows and N add up to the repository count; its land is drawn
from those with days, in the lightest ink.

Lettering: each row's name, the language it is mostly written in (`main_language`, else the largest key of
`lines`), and its commit-days as a figure (`DAYS` after the first row's figure only). The one light, `Fl <n>s`, has
its period from `claims.scrape_interval` (measured, sha-cited) and stands on the latest bank of the repository the
claim cites; it is the only thing that moves, one beat per period, lit in the still editions. The one mark,
`<version> · PyPI`, is the edition record's date on the row of the project it names. Mark lettering is set in the
water, at least 8 px from every coast, with a hairline leader.

Desk: the title block in the left column, the row names in a second column, the banks to the right; names cannot
meet land by construction. Phone: the title block stacked over the rows; each row's name line sits above its banks
in the row's own band, and the gap from a bank to the next name is about twice the gap from a name to its bank.
Every glyph goes through typeset (ctx.k), every animation through the Timeline (ctx.tl), every line through chartlib.
"""
from __future__ import annotations

import datetime as dt
import math

import chartlib as c
import edition as E
import tokens

NAME = "hero"
KIND = "chart"
SIZES = {"desk": (1280, 624), "phone": (720, 1226)}
EDITIONS = None   # the runner's default six plus HERO_EXTRA (phone stills)

BREAKS: list[tuple[str, str, str]] = [
    ("Caps lines in role `label`",
     "the role line, the fine print, the row names, tags and figures, the axis and the foot are set through role "
     "`label` with explicit tracking (desk 1.6, phone 1.0); no run uses `label-caps`",
     "check_type allows one label-caps run per sheet; the sheet has a dozen caps lines"),
    ("Name at 88 on the desk (D1: display size)",
     "the desk name is set at 88 (phone 132); the thesis wraps to the title column on both scales",
     "the desk title column is 56–386 px; the name at 141 is 516 px wide"),
    ("Weekly bins (F1.1)",
     "a week with commit-days (sweep days out) is land for that week only; half-thickness = k × days, one k for the "
     "sheet, the busiest week filling 0.8 of the bank band (desk: the row pitch; phone: the band under the name "
     "line); no floor, so one day is an islet",
     "a month-long bar for one commit drew the work bigger than it was (review-data §3.1, review-skeptic §3.4)"),
    ("Shallows along every coast (F1.2)",
     "two tints of water (shallow_b to 3.5 px, shallow_a to 7 px) are the exact 2-D buffer of the land; the paper "
     "is the open water", "land, shallows and water read as a chart at a glance, without a word"),
    ("Desk name column",
     "on the desk the row names, tags and figures sit in a column between the title block and the banks, so the "
     "busiest week can fill 0.8 of the pitch and no name can meet land",
     "a name line over the banks would cost a third of every row's height"),
    ("Phone name line",
     "on the phone each row's name line is the top of the row's band and the banks sit below it",
     "the phone has no width for a name column"),
    ("Rows add up (F1.3)",
     "the last row is `N MORE` with N = repo_count − named rows: every repository not named, including the profile "
     "repository and those whose only days are sweep days; its land is drawn from those with days",
     "21 repositories on the title line must be 21 on the sheet"),
    ("Survey date at the last tick (F1.8)",
     "the axis ends 14 px inside the border at the survey date, lettered `9 OCT` on the year line; the survey month, "
     "cut short, carries no initial", "a partial month's letter ran into the neat line"),
    ("Mark lettering in the water",
     "the light's character and the edition label are set at least 8 px from every coast (right, left, above or "
     "below the mark, first clear in that order), with a hairline leader",
     "lettering over a coast is unreadable at 390 px"),
    ("Light character upright",
     "`Fl 30s` is set upright in role `label`", "every printed figure on the sheet is measured and upright (D5)"),
    ("Vignette clipped to its row", "the coast vignette is clipped to the row's band",
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
INSIDE = 14                        # the axis ends this far inside the border (F1.8)
TRACK = {"desk": 1.6, "phone": 1.0}
NAME_SIZE = {"desk": 88, "phone": 132}
NAME_TRACK = {"desk": -1.5, "phone": -2.0}
TITLE = {
    "desk": {"x": 56, "w": 330, "name_y": 132, "thesis_y": (196, 242), "role_y": (290, 316), "role_size": None,
             "fine_y": (356, 382), "box": (52, 44, 338, 350)},
    "phone": {"x": 36, "w": 300, "name_y": 146, "thesis_y": (230, 276), "role_y": (330, 366), "role_size": 30,
              "fine_y": (404, 436), "box": (30, 30, 668, 418)},
}
ROWS = {
    # x_name / x_fig: the name's left edge and the figure's right edge; x0: the axis start; top/pitch: the bands.
    # desk: the bank band is the whole pitch (names in their own column); phone: the band under the name line.
    "desk": {"x_name": 400, "x_fig": 630, "x0": 648, "top": 50, "pitch": 68, "name_dy": None, "bank_dy": 0, "gap": 0},
    "phone": {"x_name": 36, "x_fig": None, "x0": 36, "top": 460, "pitch": 96, "name_dy": 24, "bank_dy": 32, "gap": 10},
}
AXIS = {"desk": {"y": 536, "letters": 558, "years": 582}, "phone": {"y": 1142, "letters": 1170, "years": 1198}}
FILL = 0.8                         # the busiest week's thickness as a share of the bank band
NAMED_MIN_DEFAULT = 5
SHALLOWS = ((7.0, "shallow_a"), (3.5, "shallow_b"))   # (px beyond the coast, theme tint), outer first
VIGNETTE_MIN = 15                  # rows with this many commit-days carry the coast vignette ...
VIGNETTE_HALF = 12.0               # ... on the banks at least this thick (px half-thickness)
VIGNETTE = {"step": 5.0, "lengths": (3.0, 1.8), "opacities": (0.45, 0.28), "gaps": (1.2, 1.4)}
STEP = 2.0                         # px between coast samples
JITTER = 0.4                       # px, the coast's hand (keyed by repo and sample, never by data)
LIGHT = {"desk": {"r": 7.0, "core": 2.6, "flare": 1.2, "halo": (10, 14)},
         "phone": {"r": 9.0, "core": 3.4, "flare": 1.5, "halo": (13, 18)}}
CLEAR = 8.0                        # px of water between mark lettering and any coast
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
MONTHS_MIXED = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
EASTERN = {"-0400", "-0500"}


# ---------------------------------------------------------------- small helpers
def _fmt(v):
    return E.fmt(v)


def _date(iso: str) -> str:
    y, m, d = iso[:4], int(iso[5:7]), int(iso[8:10])
    return f"{d} {MONTHS_MIXED[m - 1]} {y}"


def _month_date(d: dt.date) -> str:
    return f"{MONTHS_MIXED[d.month - 1]} {d.year}"


def _iso(s) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(s)[:10])
    except (TypeError, ValueError):
        return None


def _next_month(d: dt.date) -> dt.date:
    return dt.date(d.year + (d.month // 12), d.month % 12 + 1, 1)


def _monotone(xs: list[float], ys: list[float]):
    """Fritsch–Carlson monotone cubic through (xs, ys): a sampler f(x) that never leaves the range of two
    neighbouring control points, so a bank never dips below water or overshoots its week."""
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
    return math.hypot(max(x0 - px, 0.0, px - x1), max(y0 - py, 0.0, py - y1))


def _overlap(a: tuple, b: tuple) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


# ---------------------------------------------------------------- data → rows
def sweep_dates(data: dict) -> set[str]:
    out = {str(d)[:10] for d in (data.get("sweep_dates") or [])}
    out |= {str(s.get("date", ""))[:10] for s in (data.get("sweeps") or []) if s.get("date")}
    return out


def main_language(repo: dict) -> str | None:
    """The language the repository is mostly written in: `main_language` when the data builder wrote it, else the
    largest key of `lines` (by lines at HEAD). Never the REST `language` field."""
    if repo.get("main_language"):
        return str(repo["main_language"])
    lines = repo.get("lines") or {}
    if isinstance(lines, dict) and lines:
        return max(sorted(lines), key=lambda k_: lines[k_])
    return None


def repo_days(repo: dict, sweeps: set[str]) -> list[str]:
    """The repository's commit-days with every sweep day excluded (a sweep day is out for every repository)."""
    return sorted({str(d.get("d", ""))[:10] for d in repo.get("days") or [] if d.get("d") and str(d["d"])[:10] not in sweeps})


def plan_rows(data: dict, cfg: dict) -> dict:
    """The rows the sheet draws, from stats.json alone: named rows (days ≥ named_min, not the profile repository,
    ordered by days), the merged `more` row (every other repository, so rows + N = repo_count), the repositories
    with no non-sweep day, and the row of the light and the mark."""
    hero_cfg = cfg.get("hero", {}) or {}
    named_min = int(hero_cfg.get("named_min", NAMED_MIN_DEFAULT))
    aliases = dict(hero_cfg.get("aliases", {}) or {})
    profile = str(data.get("login") or (cfg.get("chart", {}) or {}).get("login") or "")
    sweeps = sweep_dates(data)
    repos = data.get("repos") or []
    if not repos:
        raise RuntimeError("hero: stats.json carries no repositories")
    if not any(r.get("days") for r in repos):
        raise RuntimeError("hero: stats.json carries no commit-days per repository (repos[].days); refusing to invent them")
    named, rest, zero = [], [], []
    for r in repos:
        days = repo_days(r, sweeps)
        rec = {"repo": r["name"], "name": aliases.get(r["name"], r["name"]), "days": len(days), "dates": days,
               "first_ns": days[0] if days else None, "last_ns": days[-1] if days else None,
               "language": main_language(r)}
        if not days:
            zero.append(r["name"])
        if days and len(days) >= named_min and r["name"] != profile:
            named.append(rec)
        else:
            rest.append(rec)
    named.sort(key=lambda t: (-t["days"], t["name"].lower()))
    rest.sort(key=lambda t: (-t["days"], t["name"].lower()))
    total = int(data.get("repo_count") or len(repos))
    n_more = max(total - len(named), len(rest))
    more = None
    if n_more:
        dates = sorted(d for t in rest for d in t["dates"])           # a day per repository: commit-days add up
        more = {"repo": None, "name": f"{n_more} more", "days": len(dates), "dates": dates,
                "first_ns": dates[0] if dates else None, "last_ns": dates[-1] if dates else None,
                "language": None, "repos": [t["repo"] for t in rest], "n": n_more}
    claim = (data.get("claims") or {}).get("scrape_interval") or {}
    light = None
    if claim.get("measured") and claim.get("sha") and claim.get("value") is not None:
        src_repo = str(claim.get("source", "")).split(":", 1)[0]
        row = next((t for t in named if t["repo"] == src_repo), None)
        if row is not None:
            period = float(claim["value"])
            period = int(period) if period == int(period) else period
            light = {"row": row["repo"], "character": f"Fl {period}s", "period": period}
    ed = data.get("edition") or {}
    mark = None
    if ed.get("version") and ed.get("date") and not ed.get("stale"):
        proj = str(ed.get("project", ""))
        row = next((t for t in named if t["name"] == proj or t["repo"] == proj), None)
        if row is not None:
            mark = {"row": row["repo"], "date": str(ed["date"])[:10], "label": f"{ed['version']} · PyPI"}
    return {"named_min": named_min, "rows": named, "more": more, "zero": zero, "light": light, "mark": mark,
            "sweeps": sorted(sweeps), "rest": [t["repo"] for t in rest], "profile": profile, "repo_count": total}


def axis_span(data: dict, plan: dict) -> tuple[dt.date, dt.date]:
    """(the Monday on or before the first day of the first month with a non-sweep day, the survey date)."""
    firsts = [t["first_ns"] for t in plan["rows"] + ([plan["more"]] if plan["more"] else []) if t["first_ns"]]
    t0 = _iso(min(firsts)) if firsts else _iso(data.get("first_commit"))
    t1 = _iso(data.get("taken")) or _iso(data.get("updated_at"))
    if t0 is None or t1 is None:
        raise RuntimeError("hero: stats.json carries no survey date (taken) or no first commit-day")
    t0 = t0.replace(day=1)
    t0 -= dt.timedelta(days=t0.weekday())
    if t1 <= t0:
        raise RuntimeError(f"hero: survey date {t1} is not after the first week {t0}")
    return t0, t1


def weeks_of(dates: list[str], t0: dt.date, t1: dt.date) -> list[int]:
    n = (t1 - t0).days // 7 + 1
    out = [0] * n
    for d in dates:
        dd = _iso(d)
        if dd and t0 <= dd <= t1:
            out[(dd - t0).days // 7] += 1
    return out


def quiet_stretch(plan: dict, t0: dt.date, t1: dt.date) -> tuple[dt.date, dt.date] | None:
    """The longest run (≥ 3) of whole months in which the whole account has at most one commit-day: plain words
    for the alt text, from the data."""
    days = [d for t in plan["rows"] + ([plan["more"]] if plan["more"] else []) for d in t["dates"]]
    per = {}
    for d in days:
        per[d[:7]] = per.get(d[:7], 0) + 1
    best, cur = None, []
    m = t0.replace(day=1) if t0.day == 1 else _next_month(t0)
    while _next_month(m) <= t1:
        if per.get(f"{m.year:04d}-{m.month:02d}", 0) <= 1:
            cur.append(m)
            if best is None or len(cur) > len(best):
                best = list(cur)
        else:
            cur = []
        m = _next_month(m)
    return (best[0], best[-1]) if best and len(best) >= 3 else None


def _eastern(data: dict) -> bool:
    offs: set[str] = set()
    for r in data.get("repos") or []:
        offs |= {str(k) for k, v in (r.get("tz_offsets") or {}).items() if int(v or 0) > 0}
    if not offs:
        offs = {str(k) for k in (data.get("tz_offsets") or {})}
    return bool(offs) and offs <= EASTERN


def _wrap(words: list[str], width_fn, max_w: float) -> list[str]:
    lines, cur = [], []
    for w_ in words:
        trial = " ".join(cur + [w_])
        if cur and width_fn(trial) > max_w:
            lines.append(" ".join(cur))
            cur = [w_]
        else:
            cur.append(w_)
    if cur:
        lines.append(" ".join(cur))
    return lines


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
    x0 = R["x0"]
    x_end = w - r1 - INSIDE                        # the survey date: 14 px inside the border

    def lbl(text, x, y, role="label", anchor="start", fill=None, caps=False, **kw):
        tracking = kw.pop("tracking", None)
        if caps:
            text, tracking = str(text).upper(), track if tracking is None else tracking
        return k.label(str(text), x, y, role, anchor=anchor, fill=fill, edition=ed, scale=sc, tracking=tracking, **kw)

    def width(text, role="label", caps=False, **kw):
        if caps:
            return k.text_width(str(text).upper(), role, edition=ed, scale=sc, tracking=track, **kw)
        return k.text_width(str(text), role, edition=ed, scale=sc, **kw)

    # ---- data
    plan = plan_rows(data, cfg)
    rows = list(plan["rows"])
    if not rows:
        raise RuntimeError(f"hero: no repository reaches {plan['named_min']} non-sweep commit-days; nothing to draw")
    drawn = rows + ([plan["more"]] if plan["more"] else [])
    N = plan["repo_count"]
    taken = str(data.get("taken") or data.get("updated_at") or "")[:10]
    t1d = _iso(taken)
    login = data.get("login") or cfg.get("chart", {}).get("login", "")
    thesis = cfg.get("copy", {}).get("thesis", "I survey a web that is wrong about itself.")
    role_line = cfg.get("copy", {}).get("role_line", "Crawl and data infrastructure · Python and Rust")
    t0, t1 = axis_span(data, plan)
    span_days = (t1 - t0).days + 1                 # the survey day is a whole day on the axis

    def x_of(d: dt.date) -> float:
        return x0 + (x_end - x0) * (d - t0).days / span_days

    wk_px = (x_end - x0) * 7 / span_days
    for t in drawn:      # the merged row's land counts a calendar day once, so a week holds at most seven
        t["weeks"] = weeks_of(sorted(set(t["dates"])) if t["repo"] is None else t["dates"], t0, t1)

    # ---- the bands and the one scale
    top = R["top"]
    pitch = min(float(R["pitch"]), (A["y"] - 10 - top) / len(drawn))
    band_h = pitch - R["bank_dy"] - R["gap"]       # the banks' band (desk: the pitch; phone: under the name line)
    max_week = max((n for t in drawn for n in t["weeks"]), default=1) or 1
    half_max = FILL * band_h / 2
    k_half = half_max / max_week
    for i, t in enumerate(drawn):
        bt = top + pitch * i
        t["band"] = (round(bt, 1), round(bt + pitch, 1))
        t["yc"] = bt + R["bank_dy"] + band_h / 2
        t["name_y"] = (bt + R["name_dy"]) if R["name_dy"] is not None else t["yc"] - 3

    # ---- the banks: one run of land per run of consecutive weeks with commit-days
    def runs_of(weeks: list[int], level: int = 0):
        out, cur = [], []
        for i, n in enumerate(weeks):
            if n > level:
                cur.append(i)
            elif cur:
                out.append(cur)
                cur = []
        if cur:
            out.append(cur)
        return out

    def profile(weeks: list[int], run: list[int], level: int = 0):
        """(xs, ys): the run's ends (half-thickness 0 at the first and last week's boundaries) and one control point
        at each week's centre, half-thickness k × (days − level)."""
        xa = x_of(t0 + dt.timedelta(days=7 * run[0]))
        xb = min(x_of(t0 + dt.timedelta(days=7 * run[-1] + 7)), x_end)
        xs, ys = [xa], [0.0]
        for i in run:
            wa = x_of(t0 + dt.timedelta(days=7 * i))
            wb = min(x_of(t0 + dt.timedelta(days=7 * i + 7)), x_end)
            xs.append((wa + wb) / 2)
            ys.append(k_half * (weeks[i] - level))
        xs.append(xb)
        ys.append(0.0)
        return xs, ys

    def shape_fn(xs, ys):
        """Elliptical ends from each end of the run to its first / last week's centre, a monotone cubic between the
        centres: a one-week run is an ellipse (an islet), a longer run a smooth bank."""
        inner = _monotone(xs[1:-1], ys[1:-1])
        xa, xc0, xcn, xb = xs[0], xs[1], xs[-2], xs[-1]

        def f(x):
            if x <= xc0:
                u = (xc0 - x) / max(xc0 - xa, 1e-6)
                return ys[1] * math.sqrt(max(0.0, 1 - u * u))
            if x >= xcn:
                u = (x - xcn) / max(xb - xcn, 1e-6)
                return ys[-2] * math.sqrt(max(0.0, 1 - u * u))
            return inner(x)
        return f

    def samples(xs, ys, jname):
        f = shape_fn(xs, ys)
        xa, xb = xs[0], xs[-1]
        n = max(4, int((xb - xa) / STEP))
        j = c.Jitter(seed, f"hero/coast/{jname}") if jname else None
        out = []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            hu = hd = max(0.0, f(x))
            if j is not None and 0 < i < n and hu > 1.5:
                hu = max(0.6, hu + max(-0.8, min(0.8, j.gauss(0.0, JITTER))))
                hd = max(0.6, hd + max(-0.8, min(0.8, j.gauss(0.0, JITTER))))
            out.append((x, hu, hd))
        return out

    def polygon(smp, yc):
        tops = [(x, yc - hu) for x, hu, _hd in smp]
        bots = [(x, yc + hd) for x, _hu, hd in smp]
        return tops + bots[::-1][1:-1]

    def buffer(smp, yc, off):
        """The exact 2-D buffer of the land (y-symmetric about the centreline) by `off` px."""
        xa, xb = smp[0][0] - off, smp[-1][0] + off
        n = max(6, int((xb - xa) / STEP))
        tops, bots = [], []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            up = dn = 0.0
            for sx, hu, hd in smp:
                dx = abs(sx - x)
                if dx <= off:
                    r_ = math.sqrt(off * off - dx * dx)
                    up = max(up, hu + r_)
                    dn = max(dn, hd + r_)
            tops.append((x, yc - up))
            bots.append((x, yc + dn))
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

    shallows_svg, land_svg, text_svg, mark_svg = [], [], [], []
    shallow_d = {key: [] for _off, key in SHALLOWS}
    more_shallow_d = {key: [] for _off, key in SHALLOWS}
    row_report = []
    all_polys: list[list[tuple[float, float]]] = []
    for i, t in enumerate(drawn):
        more = t["repo"] is None
        yc = t["yc"]
        blocks = []
        for run in runs_of(t["weeks"]):
            xs, ys = profile(t["weeks"], run)
            smp = samples(xs, ys, f"{t['name']}/{run[0]}")
            poly = polygon(smp, yc)
            blocks.append({"x0": xs[0], "x1": xs[-1], "poly": poly, "smp": smp, "half": max(ys), "xs": xs, "ys": ys,
                           "weeks": run})
            for off, key in SHALLOWS:
                (more_shallow_d if more else shallow_d)[key].append(c.compact_path(buffer(smp, yc, off), True, 1))
        t["blocks"] = blocks
        all_polys.extend(b["poly"] for b in blocks)
        if blocks:
            d_all = "".join(c.smooth_path(b["poly"], True, 1) for b in blocks)
            op = f' fill-opacity="{c.op(0.45)}"' if more else ""
            land_svg.append(f'<path d="{d_all}" fill="{theme.land}"{op}/>')
            if more:
                land_svg.append(f'<path d="{d_all}" fill="none" {c.stroke("HAIR", theme.ink2, 0.6)}/>')
            else:
                cs = [c.Contour(0.0, b["poly"], True, c.polyline_length(b["poly"], True), False) for b in blocks]
                land_svg.append(c.coastline(cs, theme, every=1))
            if not more and t["days"] >= VIGNETTE_MIN:
                clip = f"row{i}"
                defs.append(f'<clipPath id="{clip}"><rect x="{_fmt(x0 - 10)}" y="{_fmt(t["band"][0] + R["bank_dy"])}" '
                            f'width="{_fmt(x_end - x0 + 20)}" height="{_fmt(band_h)}"/></clipPath>')
                vig = "".join(c.coast_vignette(b["poly"], theme, jit.sub(t["name"]), **VIGNETTE)
                              for b in blocks if b["half"] >= VIGNETTE_HALF)
                if vig:
                    land_svg.append(f'<g clip-path="url(#{clip})">{vig}</g>')
        row_report.append({"repo": t["repo"], "name": t["name"], "days": t["days"], "weeks": t["weeks"],
                           "first_ns": t["first_ns"], "last_ns": t["last_ns"], "language": t["language"],
                           "y": round(yc, 1), "band": list(t["band"]), "more": more, "repos": t.get("repos"),
                           "n": t.get("n"),
                           "blocks": [{"x0": round(b["x0"], 1), "x1": round(b["x1"], 1),
                                       "top": round(min(p[1] for p in b["poly"]), 1),
                                       "bottom": round(max(p[1] for p in b["poly"]), 1),
                                       "weeks": [b["weeks"][0], b["weeks"][-1]]} for b in blocks]})
    for off, key in SHALLOWS:
        col = getattr(theme, key)
        if shallow_d[key]:
            shallows_svg.append(f'<path d="{"".join(shallow_d[key])}" fill="{col}"/>')
        if more_shallow_d[key]:
            shallows_svg.append(f'<path d="{"".join(more_shallow_d[key])}" fill="{col}" fill-opacity="{c.op(0.5)}"/>')

    # ---- the row lettering: name, main language, commit-days ("DAYS" after the first figure)
    text_boxes: list[tuple] = []
    gap_tag = 12 if not phone else 14
    for i, t in enumerate(drawn):
        more = t["repo"] is None
        nx, ny = R["x_name"], t["name_y"]
        name_w = width(t["name"], caps=True)
        text_svg.append(lbl(t["name"], nx, ny, fill=theme.muted if more else theme.ink, caps=True,
                            truth="measured", key=("more" if more else f"row:{t['repo']}")))
        text_boxes.append((nx - 1, ny - lbl_h * 0.75, nx + name_w + 1, ny + lbl_h * 0.2))
        fig = f"{t['days']} DAYS" if i == 0 else str(t["days"])
        fx = R["x_fig"] if R["x_fig"] is not None else x_end
        fw = width(fig, caps=True)
        text_svg.append(lbl(fig, fx, ny, anchor="end", fill=theme.muted if more else theme.ink, caps=True,
                            truth="measured", key=f"days:{t['repo'] or 'more'}"))
        text_boxes.append((fx - fw - 1, ny - lbl_h * 0.75, fx + 1, ny + lbl_h * 0.2))
        if t["language"]:
            tag_w = width(t["language"], caps=True)
            if phone:
                tx, ty = nx + name_w + gap_tag, ny
                fits = tx + tag_w <= fx - fw - gap_tag
            else:
                tx, ty = nx, ny + 22
                fits = tx + tag_w <= fx
            if fits:
                text_svg.append(lbl(t["language"], tx, ty, fill=theme.muted, caps=True, key=f"lang:{t['repo']}"))
                text_boxes.append((tx - 1, ty - lbl_h * 0.75, tx + tag_w + 1, ty + lbl_h * 0.2))
            t["tag_shown"] = fits
        if R["name_dy"] is not None:   # phone: the name line is the row's own; no mark lettering in it
            text_boxes.append((x0 - 2, t["band"][0] + R["name_dy"] - lbl_h * 0.75, x_end + 2, t["band"][0] + R["name_dy"] + 6))
            for b in t["blocks"]:
                assert min(p[1] for p in b["poly"]) > ny + 3, f"hero: {t['name']}'s bank meets its name line"

    # ---- mark lettering: in the water beside the mark, clear of every coast and every run
    placements = []
    y_lo = drawn[0]["band"][0] - 4 if phone else r1 + 24          # desk: nothing within 24 px of the top border
    y_hi = A["y"] - 6

    def clearance(box) -> float:
        return min((_rect_dist(px, py, box) for poly in all_polys for px, py in poly), default=99.0)

    def place(t: dict, mx: float, my: float, text: str, r_mark: float) -> dict:
        """The first clear place for a mark's lettering, in a fixed order: on the centreline right of the mark's
        bank, left of it, then above and below the mark (sliding sideways and outwards in 4 px steps), each at least
        CLEAR px from every coast and clear of every other run, inside the row's own band."""
        tw = width(text)
        blocks = sorted(t["blocks"], key=lambda b: b["x0"])
        home = next((b for b in blocks if b["x0"] - 1 <= mx <= b["x1"] + 1),
                    min(blocks, key=lambda b: min(abs(b["x0"] - mx), abs(b["x1"] - mx))))
        top_ = min(p[1] for p in home["poly"])
        bot_ = max(p[1] for p in home["poly"])
        yb = my + lbl_h * 0.36

        def box_at(xa_, ty):
            return (xa_ - 1, ty - lbl_h * 0.75, xa_ + tw + 1, ty + lbl_h * 0.2)

        others = [poly for poly in all_polys if not any(poly is b["poly"] for b in blocks)]   # other rows' land
        r_lo = max(y_lo, t["band"][0] + (R["name_dy"] + 6 if R["name_dy"] is not None else 0))
        r_hi = min(y_hi, t["band"][1])

        def leader_clear(box) -> bool:
            """The leader from the mark to the box crosses no other row's land (it may cross its own row's)."""
            bx0, by0, bx1, by1 = box
            tx_, ty_ = min(max(mx, bx0), bx1), min(max(my, by0), by1)
            L = math.hypot(tx_ - mx, ty_ - my)
            for q in range(int(L / 2) + 1):
                px = mx + (tx_ - mx) * q * 2 / max(L, 1)
                py = my + (ty_ - my) * q * 2 / max(L, 1)
                for poly in others:
                    if c.point_in_polygon(px, py, poly) or min(math.hypot(px - a_, py - b_) for a_, b_ in poly) < 3:
                        return False
            return True

        def ok(box):
            if box[0] < x0 - 0.5 or box[2] > x_end + 0.5 or box[1] < r_lo or box[3] > r_hi:
                return None
            if any(_overlap(box, ob) for ob in text_boxes):
                return None
            cl = clearance(box)
            return cl if cl >= CLEAR and leader_clear(box) else None

        tries = [("right", [(home["x1"] + CLEAR + 3 + d, yb) for d in range(0, 400, 4)]),
                 ("left", [(home["x0"] - CLEAR - 3 - tw - d, yb) for d in range(0, 400, 4)])]
        slides = [0] + [s_ * d for d in range(4, 260, 4) for s_ in (1, -1)]
        above = [(mx - tw / 2 + dx, top_ - CLEAR - lbl_h * 0.2 - dy) for dy in range(0, 40, 4) for dx in slides]
        below = [(mx - tw / 2 + dx, bot_ + CLEAR + lbl_h * 0.75 + dy) for dy in range(0, 40, 4) for dx in slides]
        tries += [("above", above), ("below", below)]
        for side, spots in tries:
            for xa_, ty in spots:
                box = box_at(xa_, ty)
                cl = ok(box)
                if cl is not None:
                    return {"x": xa_, "y": ty, "anchor": "start", "side": side, "box": box, "clear": round(cl, 1)}
        raise RuntimeError(f"hero: no clear water for {text!r} on {t['name']}'s row")

    def leader(mx: float, my: float, p: dict, r_mark: float) -> str:
        bx0, by0, bx1, by1 = p["box"]
        tx_, ty_ = min(max(mx, bx0), bx1), min(max(my, by0), by1)
        dx, dy = tx_ - mx, ty_ - my
        dist = math.hypot(dx, dy)
        if dist < r_mark + 6:
            return ""
        ux, uy = dx / dist, dy / dist
        a = (mx + ux * (r_mark + 2), my + uy * (r_mark + 2))
        b = (tx_ - ux * 3, ty_ - uy * 3)
        return (f'<path d="M{_fmt(a[0])} {_fmt(a[1])}L{_fmt(b[0])} {_fmt(b[1])}" fill="none" '
                f'{c.stroke("HAIR", theme.ink, 0.8, caps="butt")}/>')

    lights = []
    light = plan["light"]
    if light:
        t = next(t for t in drawn if t["repo"] == light["row"])
        last = max(t["blocks"], key=lambda b: b["x0"])                 # the latest bank: the code as it is now
        j_ = max(range(len(last["ys"])), key=lambda q: last["ys"][q])
        lx, ly = E.I(last["xs"][j_]), E.I(t["yc"])
        L = LIGHT[sc]
        lit_id = "light-lit"
        halo = L["halo"][1] if night else L["halo"][0]
        core = c.lit_core(lx, ly, theme, lit_id, r=L["core"], halo_r=halo, prefix=prefix)
        try:
            flash = tl.flash(light["character"], begin=0.0, still="lit", name="light-flash")
            beat = True
        except ValueError:                                              # a period off the loop grid: lit, not flashing
            flash, beat = "", False
        p = place(t, lx, ly, light["character"], L["r"])
        mark_svg.append(leader(lx, ly, p, L["r"]))
        mark_svg.append(use("flare", lx, ly, scale=L["flare"])
                        + f'<path d="{_star_d(lx, ly, L["r"], L["r"] * 0.42)}" fill="{theme.land}" '
                        f'{c.stroke("PEN", theme.ink)}/>' + f"<g>{flash}{core}</g>")
        text_svg.append(lbl(light["character"], p["x"], p["y"], fill=theme.ink, truth="measured", key="light"))
        text_boxes.append(p["box"])
        placements.append({"what": "light", "text": light["character"], "side": p["side"], "clear": p["clear"],
                           "box": [round(v, 1) for v in p["box"]]})
        lights.append({"id": f"{NAME}-{lit_id}", "character": light["character"], "color": theme.light_core,
                       "period": light["period"], "row": light["row"], "x": lx, "y": ly, "beat": beat,
                       "week": last["weeks"][0] + max(0, j_ - 1)})
    mark = plan["mark"]
    mark_report = None
    if mark:
        t = next(t for t in drawn if t["repo"] == mark["row"])
        md = _iso(mark["date"])
        if md and t0 <= md <= t1 and t["blocks"]:
            mx, my = E.I(x_of(md) + wk_px / 14), E.I(t["yc"])
            ms = 1.0 if not phone else 1.35
            p = place(t, mx, my, mark["label"], 3.5 * ms)
            mark_svg.append(leader(mx, my, p, 3.5 * ms))
            mark_svg.append(f'<circle cx="{_fmt(mx)}" cy="{_fmt(my)}" r="{_fmt(3.2 * ms)}" fill="{theme.land}" '
                            f'{c.stroke("PEN", theme.ink)}/><circle cx="{_fmt(mx)}" cy="{_fmt(my)}" '
                            f'r="{_fmt(1.2 * ms)}" fill="{theme.ink}"/>')
            text_svg.append(lbl(mark["label"], p["x"], p["y"], fill=theme.ink, truth="measured", key="edition"))
            text_boxes.append(p["box"])
            placements.append({"what": "edition", "text": mark["label"], "side": p["side"], "clear": p["clear"],
                               "box": [round(v, 1) for v in p["box"]]})
            mark_report = {**mark, "x": mx, "y": my}
    report["lights"] = lights
    report["mark"] = mark_report
    report["placements"] = placements

    # ---- the axis: a latitude scale — week ticks, month ticks and initials, the years, the survey date
    ay = A["y"]
    tick = 6 if not phone else 8
    wticks, mticks = [], [f"M{_fmt(x0)} {_fmt(ay)}H{_fmt(x_end)}"]
    for i in range((t1 - t0).days // 7 + 1):
        xw = x_of(t0 + dt.timedelta(days=7 * i))
        wticks.append(f"M{_fmt(xw)} {_fmt(ay)}v{_fmt(tick / 2)}")
    m = t0.replace(day=1) if t0.day == 1 else _next_month(t0)
    year_x: dict[int, float] = {}
    letters = []
    first_month = True
    while m <= t1:
        xm = x_of(m)
        mticks.append(f"M{_fmt(xm)} {_fmt(ay)}v{tick}")
        nm = _next_month(m)
        if nm <= t1 + dt.timedelta(days=1):                    # a whole month: its initial at mid-month
            letters.append((MONTHS[m.month - 1][0], (xm + x_of(nm)) / 2))
        if m.month == 1 or first_month:
            year_x.setdefault(m.year, xm)
        first_month = False
        m = nm
    mticks.append(f"M{_fmt(x_end)} {_fmt(ay)}v{tick * 2}")    # the survey date
    body.append(f'<path d="{"".join(wticks)}" fill="none" {c.stroke("HAIR", theme.ink2, 0.7, caps="butt")}/>'
                f'<path d="{"".join(mticks)}" fill="none" {c.stroke("PEN", theme.ink2, 0.9, caps="butt")}/>')
    for initial, xm in letters:
        text_svg.append(lbl(initial, xm, A["letters"], anchor="middle", fill=theme.ink2))
    for yr, xm in sorted(year_x.items()):
        text_svg.append(lbl(str(yr), xm, A["years"], fill=theme.ink2, truth="measured", key=f"year:{yr}"))
    survey = f"{t1d.day} {MONTHS[t1d.month - 1]}" if t1d else ""
    if survey:
        text_svg.append(lbl(survey, x_end, A["years"], anchor="end", fill=theme.ink, truth="measured", key="survey-tick"))

    body.append("".join(shallows_svg))
    body.append("".join(land_svg))                       # land is on the sheet at t = 0
    body.append("".join(mark_svg))

    # ---- the title block: the name, the thesis, the role line, the fine print
    block = []
    bx, box = T["x"], T["box"]
    nsz = NAME_SIZE[sc]
    ben = k.text("Ben", bx, T["name_y"], "display", size=nsz, tracking=NAME_TRACK[sc], edition=ed, scale=sc, within=box)
    wb = k.text_width("Ben ", "display", size=nsz, tracking=NAME_TRACK[sc], edition=ed, scale=sc)
    russ = k.text("Russell", bx + wb, T["name_y"], "display", size=nsz, tracking=NAME_TRACK[sc], edition=ed, scale=sc,
                  within=box)
    block.append(ben + russ)
    th_lines = _wrap(thesis.split(), lambda s: k.text_width(s, "thesis", edition=ed, scale=sc), T["w"])
    if len(th_lines) > len(T["thesis_y"]):
        th_lines = th_lines[:len(T["thesis_y"]) - 1] + [" ".join(th_lines[len(T["thesis_y"]) - 1:])]
    for y, line in zip(T["thesis_y"], th_lines):
        block.append(k.text(line, bx, y, "thesis", fill=theme.ink2, edition=ed, scale=sc, within=box))
    rs = T["role_size"]
    role_parts = [p_.strip() for p_ in role_line.split("·")]
    if len(T["role_y"]) == 1:
        role_parts = [role_line]
    for y, line in zip(T["role_y"], role_parts):
        block.append(lbl(line, bx, y, fill=theme.ink, caps=True, within=box, size=rs))
    eastern = " · EASTERN TIME" if _eastern(data) else ""
    fine = [f"{N} REPOSITORIES · DATUM: MAIN", f"{_date(taken)}{eastern}"]
    for y, line, key in zip(T["fine_y"], fine, ("repositories", "survey-date")):
        block.append(lbl(line, bx, y, fill=theme.ink2, caps=True, within=box, truth="measured", key=key))
    if not phone:   # the foot, inside the neat line: the GitHub URL and the date, nothing else
        block.append(lbl(f"github.com/{login} · {_date(taken)}", bx, A["years"], fill=theme.ink2, caps=True,
                         truth="measured", key="imprint"))
    body.append("".join(block))
    body.append("".join(text_svg))

    # ---- the report
    report["rows"] = row_report
    report["counts"] = {"repositories": N, "rows": len(rows), "more": plan["more"]["n"] if plan["more"] else 0,
                        "zero": len(plan["zero"]), "more_days": plan["more"]["days"] if plan["more"] else 0}
    report["zero"] = plan["zero"]
    report["named_min"] = plan["named_min"]
    report["profile"] = plan["profile"]
    report["axis"] = {"start": t0.isoformat(), "end": t1.isoformat(), "x0": x0, "x_end": x_end,
                      "border": w - r1, "week_px": round(wk_px, 2), "weeks": (t1 - t0).days // 7 + 1,
                      "letters": "".join(l_ for l_, _x in letters), "years": sorted(year_x), "survey": survey}
    report["scale"] = {"half_px_per_day": round(k_half, 3), "half_max": round(half_max, 1), "max_week": max_week,
                       "band": round(band_h, 1), "pitch": round(pitch, 1), "fill": FILL}
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
    """≤ 25 words, plain: what the sheet shows, from the data. The last sentence is chart.toml's alt_poem line."""
    try:
        plan = plan_rows(data, cfg)
        n = plan["repo_count"]
        t0, t1 = axis_span(data, plan)
        names = [t["name"] for t in plan["rows"][:2]]
        quiet = quiet_stretch(plan, t0, t1)
    except Exception:
        n = int(data.get("repo_count") or len(data.get("repos") or []))
        names, t0, t1, quiet = [], None, None, None
    first = (t0 + dt.timedelta(days=6)) if t0 else None              # the first month the axis covers whole
    span = f", {_month_date(first)} to {_month_date(t1)}" if first and t1 else ""
    busy = f": {' and '.join(names)} busiest" if names else ""
    q = ""
    if quiet:
        a, b = quiet
        q = f", quiet {MONTHS_MIXED[a.month - 1]} to {MONTHS_MIXED[b.month - 1]} {b.year}"
    return f"Ben Russell's {n} repositories by week{span}{busy}{q}. The rest share one row."


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
    entry["area_law"] = "half-thickness∝commit-days per week (sweeps out)"
    entry["hero"] = {kk: x[kk] for kk in ("rows", "counts", "zero", "named_min", "profile", "axis", "scale", "sweeps",
                                          "mark", "placements", "no_sounding") if kk in x}


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
