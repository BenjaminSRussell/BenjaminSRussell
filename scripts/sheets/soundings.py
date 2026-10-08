"""soundings — Sheet 2: the tide table of the last 52 weeks and the fleet register (T9 §2A).

Depth = count. The 52 weekly commit counts are the same soundings the hero's contours are
solved from, shown twice here: as the tide curve (monotone cubic, baseline zero, HW labelled
with its cause, LW, typical week, slack water) and as a traverse of depth figures under it, one
per week where they fit: HW and LW always, then the largest first, and one 0 for a run of zero
weeks (52 figures at 16 px on a 23 px pitch overprinted each other). Beneath, one 52-week line
per repository on one shared scale, with its commits as a spot height, five to a row. Both commit
instruments are named once in the source line (author-filtered clones upright, GitHub's calendar
as the second instrument). No motion: this sheet is finished at t = 0 in every edition.

Sizes (desk 1280×520, v9.1 scale): dateline, tide labels, month letters, register names and
counts, source line and folio 19 (label / label-caps); the pencil note 25 (note); the week
figures 16 (texture, sounding()). Phone (720×360): labels 26, the note 30 (place-water).
"""
from __future__ import annotations

import math

import chartlib as C
import edition as E
import typeset as T
from edition import fmt, I

NAME = "soundings"
KIND = "strip"
SIZES = {"desk": (1280, 500), "phone": (720, 360)}
BREAKS: list[tuple[str, str, str]] = [
    ("No neat line", "paper only, head and foot rules", "a tide table is printed in the margin, not framed (27)"),
    ("Two projections of one series", "curve above, 52 depth figures along a traverse below",
     "the hydrographer reads the figures, the reader reads the curve (08, 13)"),
    ("Register on a shared scale", "15 of 21 lines are nearly flat at 18 px", "the data is bursty; smoothing or per-line scales would lie (32)"),
    ("Traverse thinned, not shrunk", "HW and LW always; then the largest figures first while 8 px of paper separates them; one 0 at the middle of a run of zero weeks (or at LW)",
     "v9.1: 52 figures at 16 px on a 23 px pitch overprint; a chart thins its soundings rather than crowd them"),
    ("Register five to a row, 520 px sheet", "5 × 5 cells of 229 px on a 44 px pitch, rules drawn per filled cell",
     "every chart name fits uncut at 19 px (SPOTIFY TO APPLE MUSIC is 206 px); the ragged last row has no empty boxes"),
    ("Everything under the curve moved down", "LW label at BASE + 26, traverse at 226, month letters at 250, register head at 272",
     "at 19 px the LW label sat on the slack bracket and the month letters on the register head"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


# ------------------------------------------------------------------ small helpers
def _dmy(iso: str) -> str:
    y, m, d = iso[:10].split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def _dm(iso: str) -> str:
    _y, m, d = iso[:10].split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]}"


def _hm(iso: str) -> str:
    """'2026-10-07T19:47:47Z' → '19:47'."""
    if "T" in iso and len(iso) >= 16:
        return iso[11:16]
    return ""


def _n(v) -> str:
    return f"{int(v):,}"


def _pretty(name: str) -> str:
    return name.replace("_", " ").replace("-", " ")


def _aliases(cfg) -> dict:
    """repo → chart name from chart.toml [[features]] aliases[0] (rustmapper, Scrapy Harbor, Profile Shoal)."""
    out = {}
    for f in (cfg.get("features") or []) if cfg else []:
        al = f.get("aliases") or []
        if f.get("repo") and al:
            out[str(f["repo"])] = str(al[0])
    return out


def _chart_name(name: str, cfg) -> str:
    return _aliases(cfg).get(name) or _pretty(name)


def _days_between(a: str, b: str) -> int:
    import datetime as dt
    try:
        return (dt.date.fromisoformat(b[:10]) - dt.date.fromisoformat(a[:10])).days
    except ValueError:
        return 10 ** 6


def _tide(data: dict) -> dict:
    """The tide figures from stats.json, with index positions resolved against weeks[]."""
    weeks = data.get("weeks") or []
    if len(weeks) < 2 or not all("n" in w for w in weeks):
        raise ValueError("no soundings: stats.json carries no weeks[] (the build refuses an even spread)")
    ns = [int(w["n"]) for w in weeks]
    starts = [str(w.get("start", "")) for w in weeks]
    tide = data.get("tide") or {}
    hw = tide.get("hw") or {}
    lw = tide.get("lw") or {}
    slack = tide.get("slack") or {}
    hw_i = starts.index(hw["start"]) if hw.get("start") in starts else max(range(len(ns)), key=lambda i: ns[i])
    hw_n = int(hw.get("n", ns[hw_i]))
    body = ns[:-1] if len(ns) > 1 else ns
    lw_i = starts.index(lw["start"]) if lw.get("start") in starts else min(range(len(body)), key=lambda i: body[i])
    lw_n = int(lw.get("n", ns[lw_i]))
    median = tide.get("median")
    if median is None:
        s = sorted(body)
        median = s[len(s) // 2]
    if slack.get("start") in starts:
        s0 = starts.index(slack["start"])
        s1 = starts.index(slack["end"]) if slack.get("end") in starts else min(s0 + 3, len(ns) - 1)
    else:  # lowest rolling 4-week sum over the complete weeks
        best, s0 = None, 0
        for i in range(0, max(1, len(body) - 3)):
            tot = sum(body[i:i + 4])
            if best is None or tot < best:
                best, s0 = tot, i
        s1 = min(s0 + 3, len(ns) - 1)
    cause = hw.get("cause") or max((weeks[hw_i].get("repos") or {"": 0}).items(), key=lambda kv: kv[1])[0]
    repos = {r["name"]: r for r in data.get("repos") or []}
    sprint = ""
    cr = repos.get(cause)
    if cr and cr.get("first") and cr.get("last") and _days_between(cr["first"], cr["last"]) <= 14:
        days = int(cr.get("commit_days") or hw.get("cause_days") or 0) or _days_between(cr["first"], cr["last"]) + 1
        sprint = f", {days} day{'s' if days != 1 else ''}"
    slack_month = slack.get("month") or starts[s0][:7]
    return {"ns": ns, "starts": starts, "hw_i": hw_i, "hw_n": hw_n, "lw_i": lw_i, "lw_n": lw_n,
            "median": int(median), "slack": (s0, s1), "slack_month": MONTHS[int(slack_month[5:7]) - 1],
            "cause": cause, "sprint": sprint}


def _copy(cfg, key: str, default: str) -> str:
    """chart.toml [copy] strings (`cfg.copy` is dict.copy, so index it)."""
    return str((cfg.get("copy") or {}).get(key) or default)


def _stale(data: dict) -> bool:
    prov = data.get("provenance") or {}
    return bool(data.get("no_sounding")) or prov.get("mode") == "cache-failed"


def _month_ticks(starts: list[str]) -> list[tuple[int, str]]:
    """(index, letter) at each week that starts a new month."""
    out = []
    for i, s in enumerate(starts):
        if not s:
            continue
        if i == 0 or s[:7] != starts[i - 1][:7]:
            out.append((i, MONTHS[int(s[5:7]) - 1][0]))
    return out


def _traverse(ns: list[int], xs: list[float], hw_i: int, lw_i: int, width_of, gap: float = 8.0) -> list[int]:
    """The week indices whose figures are printed on the traverse, in week order: HW and LW first, then the
    non-zero weeks largest first, then one 0 for each run of zero weeks (at LW when LW lies in the run,
    else at its middle); a figure is placed only when `gap` px of paper separates it from every figure
    already placed. Nothing is invented and nothing printed is moved: a figure that does not fit is left off."""
    n = len(ns)
    order = [hw_i] + ([lw_i] if lw_i != hw_i else [])
    order += sorted((i for i in range(n) if ns[i] > 0 and i not in order), key=lambda i: (-ns[i], i))
    i = 0
    while i < n:
        if ns[i] > 0:
            i += 1
            continue
        j = i
        while j + 1 < n and ns[j + 1] == 0:
            j += 1
        pick = lw_i if i <= lw_i <= j else (i + j) // 2
        if pick not in order:
            order.append(pick)
        i = j + 1
    placed: list[tuple[float, float]] = []
    chosen: list[int] = []
    for i in order:
        w = width_of(ns[i])
        x0, x1 = xs[i] - w / 2, xs[i] + w / 2
        if all(x1 + gap <= p0 or x0 >= p1 + gap for p0, p1 in placed):
            placed.append((x0, x1))
            chosen.append(i)
    return sorted(chosen)


# ------------------------------------------------------------------ the desk sheet
def _desk(ctx) -> str:
    ed, t, data = ctx.ed, ctx.ed.theme, ctx.data
    td = _tide(data)
    ns, starts = td["ns"], td["starts"]
    n = len(ns)
    stale = _stale(data)
    repo_count = int(data.get("repo_count") or len(data.get("repos") or []))
    chart_no = repo_count
    W_, H_ = SIZES["desk"]
    X0, X1 = 48, 1232
    TOP, BASE = 64, 180          # HW at TOP, zero at BASE
    TRV = 226                    # the traverse's baseline; the month letters at 250, the register head at 272
    jit = C.Jitter((ctx.cfg.get("chart") or {}).get("seed", 27), "soundings")

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = []
    # head: dateline left, unit line right (the sheet's one tracked caps run), hair rule
    taken = str(data.get("updated_at") or data.get("taken") or "")
    date_s = _dmy(taken) if taken else ""
    hm = _hm(taken)
    dateline = f"Soundings taken {date_s}" + (f" · {hm} UTC" if hm else "")
    out.append(tx(dateline, X0, 40, "label", fill=t.ink, truth="measured", key="dateline"))
    out.append(tx(_copy(ctx.cfg, "unit_hero", "SOUNDINGS IN COMMITS"), X1, 40, "label-caps",
                  fill=t.ink, anchor="end"))
    out.append(f'<path d="M{X0} 50H{X1}" fill="none" {C.stroke("HAIR", t.ink, 0.8, caps="butt")}/>')

    # the tide curve
    scale_n = max(td["hw_n"], 1)
    xs = [X0 + i * (X1 - X0) / (n - 1) for i in range(n)]

    def y_of(v: float) -> float:
        return BASE - (BASE - TOP) * v / scale_n

    pts = [(round(x, 1), round(y_of(v), 1)) for x, v in zip(xs, ns)]
    area = C.monotone_path(pts, baseline=BASE)
    curve = C.monotone_path(pts)
    out.append(f'<path d="{area}" fill="{t.shallow_a}" fill-opacity=".55"/>')
    # typical week: dotted rule (coincides with the baseline when the median is 0)
    y_med = y_of(td["median"])
    if td["median"] > 0:
        out.append(f'<path d="M{X0} {fmt(y_med)}H{X1}" fill="none" {C.stroke("HAIR", t.ink2, 0.9, "TRACK", caps="butt")}/>')
    # baseline (dashed when the sounding is stale)
    out.append(f'<path d="M{X0} {BASE}H{X1}" fill="none" '
               f'{C.stroke("PEN", t.ink, 0.8, "PECK" if stale else None, caps="butt")}/>')
    out.append(f'<path d="{curve}" fill="none" {C.stroke("PEN", t.ink, 0.85 if ed.dark else None)}/>')

    # marks: HW (filled dot), LW (hollow), slack bracket
    hx, hy = pts[td["hw_i"]]
    lx, ly = pts[td["lw_i"]]
    out.append(f'<circle cx="{fmt(hx)}" cy="{fmt(hy)}" r="3.5" fill="{t.ink}"/>')
    out.append(f'<circle cx="{fmt(lx)}" cy="{fmt(ly)}" r="3" fill="{t.paper}" {C.stroke("PEN", t.ink)}/>')
    s0, s1 = td["slack"]
    bx0, bx1 = xs[s0], xs[s1]
    out.append(f'<path d="M{fmt(bx0)} {BASE + 9}v-4H{fmt(bx1)}v4" fill="none" {C.stroke("HAIR", t.ink2, 0.9, caps="butt")}/>')

    # labels (HW with its cause, LW, typical week, slack water)
    hw_label = f"HW {_n(td['hw_n'])} · wk of {_dm(starts[td['hw_i']])} · {_chart_name(td['cause'], ctx.cfg)}{td['sprint']}"
    if hx > (X0 + X1) / 2:
        out.append(tx(hw_label, hx - 9, hy + 4, "label", fill=t.ink, anchor="end", truth="measured", key="tide.hw"))
    else:
        out.append(tx(hw_label, hx + 9, hy + 4, "label", fill=t.ink, truth="measured", key="tide.hw"))
    lw_label = f"LW {_n(td['lw_n'])} · wk of {_dm(starts[td['lw_i']])}"
    lw_w = T.text_width(lw_label, "label", edition=ed)
    lxx = min(max(lx, X0 + lw_w / 2), X1 - lw_w / 2)
    out.append(tx(lw_label, lxx, BASE + 26, "label", fill=t.muted, anchor="middle", truth="measured", key="tide.lw"))
    # typical week: labelled over the longest flat run of the curve at that level, so it never sits on ink
    med_label = f"typical week {_n(td['median'])}"
    med_y = y_med - 5
    best, run, start = (0, 0), 0, 0
    for i, v in enumerate(ns + [-1]):
        if v == td["median"] and i < n:
            run += 1
            if run > best[1]:
                best = (i - run + 1, run)
        else:
            run = 0
    mi = best[0] + best[1] / 2 if best[1] >= 3 else 0.5
    med_x = X0 + mi * (X1 - X0) / (n - 1)
    med_w = T.text_width(med_label, "label", edition=ed)
    med_x = min(max(med_x, X0 + med_w / 2 + 4), X1 - med_w / 2 - 4)
    out.append(tx(med_label, med_x, med_y, "label", fill=t.muted, anchor="middle", truth="measured", key="tide.median"))
    out.append(tx(f"slack water · {td['slack_month']}", (bx0 + bx1) / 2, BASE - 5, "label", fill=t.muted,
                  anchor="middle", truth="measured", key="tide.slack"))

    # the stale note in the quiet upper-left of the plot (v9.1: the pencil footnote is gone; the curve shows)
    if stale:
        out.append(tx(f"no sounding taken {_dmy(str(data.get('taken') or taken))}", X0 + 8, 90, "note", fill=t.ink2))

    # the traverse: the depth figures that fit (upright: measured from the clones), month ticks and letters
    out.append(f'<path d="M{X0} {TRV + 4}H{X1}" fill="none" {C.stroke("HAIR", t.ink, 0.5, caps="butt")}/>')
    for i in _traverse(ns, xs, td["hw_i"], td["lw_i"], lambda v: T.text_width(str(v), "texture", edition=ed)):
        out.append(T.sounding(ns[i], round(xs[i], 1), TRV, truth="measured", edition=ed, key=f"week.{i}"))
    ticks = _month_ticks(starts)
    d = "".join(f"M{fmt(xs[i])} {TRV + 4}v5" for i, _ in ticks)
    out.append(f'<path d="{d}" fill="none" {C.stroke("HAIR", t.ink, 0.7, caps="butt")}/>')
    for i, letter in ticks:
        out.append(tx(letter, xs[i], TRV + 24, "label", fill=t.ink2, anchor="middle"))

    # fleet register as a tide-table block: ruled rows and columns, one 52-week line per repository on
    # one shared scale with its own baseline, name in caps, commits as a spot height
    repos = sorted((r for r in data.get("repos") or [] if r.get("weeks")), key=lambda r: (-int(r.get("commits") or 0), r["name"]))
    if repos:
        cols = max(5, math.ceil(len(repos) / 5))      # five to a row: every chart name fits uncut at 19 px
        rows = math.ceil(len(repos) / cols)
        pitch_x = (X1 - X0 + 9) / cols
        cell_w = pitch_x - 9
        y0, pitch_y, spark_h = TRV + 36, 44, 18          # v9.1: no register head line; the rows start 36 under the traverse
        ymax = max(max(int(v) for v in r["weeks"]) for r in repos) or 1
        # rules per filled cell (the last row is ragged): the top rule, each cell's foot and its left rule
        filled = repos[:cols * rows]
        rules = f"M{X0} {y0}H{fmt(X0 + min(cols, len(filled)) * pitch_x - 9)}"
        for k in range(len(filled)):
            c, rr = k % cols, k // cols
            cx, cy = X0 + c * pitch_x, y0 + rr * pitch_y
            rules += f"M{fmt(cx - (4.5 if c else 0))} {fmt(cy + pitch_y)}H{fmt(cx + cell_w + (4.5 if c < cols - 1 else 0))}"
            if c:
                rules += f"M{fmt(cx - 4.5)} {fmt(cy)}v{pitch_y}"
        out.append(f'<path d="{rules}" fill="none" {C.stroke("HAIR", t.ink, 0.5, caps="butt")}/>')
        for k, r in enumerate(filled):
            c, rr = k % cols, k // cols
            cx, cy = X0 + c * pitch_x, y0 + rr * pitch_y
            active = bool(r.get("active"))
            name = _chart_name(r["name"], ctx.cfg).upper()
            count = _n(r.get("commits") or 0)
            cw = T.text_width(count, "label", edition=ed)
            room = cell_w - cw - 6
            while name and T.text_width(name, "label", edition=ed) > room:
                name = (name[:-2] if name.endswith("…") else name[:-1]).rstrip() + "…"
            out.append(tx(name, cx, cy + 17, "label", fill=t.ink if active else t.ink2))
            out.append(tx(count, cx + cell_w, cy + 17, "label", fill=t.ink, anchor="end", truth="measured",
                          key=f"repo.{r['name']}.commits"))
            base_y = cy + 40
            wk = [int(v) for v in r["weeks"]]
            m = len(wk)
            spts = [(cx + i * cell_w / (m - 1), base_y - spark_h * v / ymax) for i, v in enumerate(wk)]
            out.append(f'<path d="M{fmt(cx)} {fmt(base_y)}H{fmt(cx + cell_w)}" fill="none" {C.stroke("HAIR", t.hair, caps="butt")}/>')
            out.append(f'<path d="{C.compact_path(spts, False, 1)}" fill="none" '
                       f'{C.stroke("PEN", t.ink2 if ed.dark else t.ink, 0.8)}/>')

    # foot: folio (decision 27) and the source line naming both commit instruments
    FOOT = H_ - 5
    out.append(tx(f"CHART NO. {chart_no} · SHEET 2", 24, FOOT, "label-caps", fill=t.muted, key="folio"))
    commits = data.get("commits")
    all_hands = data.get("all_hands")
    cal = data.get("calendar_total")
    parts: list[tuple[str, str | None, str | None]] = [
        (f"Source · {repo_count} public repositories cloned, author's commits only · ", None, None),
    ]
    if commits is not None:
        parts += [(_n(commits), "measured", "commits"), (" commits", None, None)]
    if all_hands is not None:
        parts += [(" · ", None, None), (_n(all_hands), "measured", "all_hands"), (" all hands", None, None)]
    if cal is not None:
        parts += [(" · ", None, None), (_n(cal), "measured", "calendar_total"), (" by GitHub's calendar", None, None)]
    widths = [T.text_width(s, "label", edition=ed) for s, _tr, _k in parts]
    pen = X1 - sum(widths)
    for (s, tr, key), w in zip(parts, widths):
        out.append(tx(s, pen, FOOT, "label", fill=t.ink if tr else t.muted, truth=tr, key=key))
        pen += w
    body = "".join(out)
    return E.svg(ed, W_, H_, body, T.glyph_defs(), sheet=NAME)


# ------------------------------------------------------------------ the phone sheet (redrawn, not scaled)
def _phone(ctx) -> str:
    ed, t, data = ctx.ed, ctx.ed.theme, ctx.data
    td = _tide(data)
    ns, starts = td["ns"], td["starts"]
    n = len(ns)
    stale = _stale(data)
    repo_count = int(data.get("repo_count") or len(data.get("repos") or []))
    W_, H_ = SIZES["phone"]
    X0, X1 = 16, 704
    TOP, BASE = 80, 236

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = []
    taken = str(data.get("updated_at") or data.get("taken") or "")
    out.append(tx(f"52 weeks to {_dmy(taken) if taken else '—'} · {repo_count} repositories", X0, 40, "label",
                  fill=t.ink, truth="measured", key="dateline"))
    out.append(f'<path d="M{X0} 52H{X1}" fill="none" {C.stroke("PEN", t.ink, 0.8, caps="butt")}/>')
    scale_n = max(td["hw_n"], 1)
    xs = [X0 + i * (X1 - X0) / (n - 1) for i in range(n)]
    y_of = lambda v: BASE - (BASE - TOP) * v / scale_n  # noqa: E731
    pts = [(round(x, 1), round(y_of(v), 1)) for x, v in zip(xs, ns)]
    out.append(f'<path d="{C.monotone_path(pts, baseline=BASE)}" fill="{t.shallow_a}" fill-opacity=".55"/>')
    if td["median"] > 0:
        out.append(f'<path d="M{X0} {fmt(y_of(td["median"]))}H{X1}" fill="none" {C.stroke("PEN", t.ink2, 0.9, "TRACK", caps="butt")}/>')
    out.append(f'<path d="M{X0} {BASE}H{X1}" fill="none" {C.stroke("LINE", t.ink, 0.8, "PECK" if stale else None, caps="butt")}/>')
    out.append(f'<path d="{C.monotone_path(pts)}" fill="none" {C.stroke("LINE", t.ink)}/>')
    hx, hy = pts[td["hw_i"]]
    lx, ly = pts[td["lw_i"]]
    out.append(f'<circle cx="{fmt(hx)}" cy="{fmt(hy)}" r="5" fill="{t.ink}"/>')
    out.append(f'<circle cx="{fmt(lx)}" cy="{fmt(ly)}" r="4.5" fill="{t.paper}" {C.stroke("LINE", t.ink)}/>')
    hw_label = f"HW {_n(td['hw_n'])} · {_dm(starts[td['hw_i']])}"
    if hx > (X0 + X1) / 2:
        out.append(tx(hw_label, hx - 14, hy + 9, "label", fill=t.ink, anchor="end", truth="measured", key="tide.hw"))
    else:
        out.append(tx(hw_label, hx + 14, hy + 9, "label", fill=t.ink, truth="measured", key="tide.hw"))
    lw_label = f"LW {_n(td['lw_n'])} · {_dm(starts[td['lw_i']])}"
    lw_w = T.text_width(lw_label, "label", edition=ed)
    lxx = min(max(lx, X0 + lw_w / 2), X1 - lw_w / 2)
    out.append(tx(lw_label, lxx, BASE + 30, "label", fill=t.muted, anchor="middle", truth="measured", key="tide.lw"))
    if stale:
        out.append(tx(f"no sounding taken {_dmy(str(data.get('taken') or taken))}", X1, 312, "label-italic",
                      fill=t.ink2, anchor="end"))
    out.append(tx(f"CHART NO. {repo_count} · SHEET 2", X0, 350, "label-caps", fill=t.muted, key="folio"))
    out.append(tx(_copy(ctx.cfg, "unit_hero", "SOUNDINGS IN COMMITS"), X1, 350, "label-caps",
                  fill=t.ink, anchor="end"))
    return E.svg(ed, W_, H_, "".join(out), T.glyph_defs(), sheet=NAME)


def build(ctx) -> str:
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    try:
        td = _tide(data)
    except ValueError:
        return "Tide table of weekly commits, fifty-two weeks, high and low water dated. Below, one line per repository."
    def alt_for(cause: str) -> str:
        return (f"Tide table of commits: high water {_n(td['hw_n'])}, week of {_dm(td['starts'][td['hw_i']])}, {cause}; "
                f"low water {_n(td['lw_n'])}; typical week {_n(td['median'])}. Below, one line per repository.")
    text = alt_for(_aliases(cfg).get(td["cause"], td["cause"]))
    if len(text.split()) > 25:
        text = alt_for(td["cause"])
    return text
