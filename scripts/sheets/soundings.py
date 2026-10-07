"""soundings — Sheet 2: the tide table of the last 52 weeks and the fleet register (T9 §2A).

Depth = count. The 52 weekly commit counts are the same soundings the hero's contours are
solved from, shown twice here: as the tide curve (monotone cubic, baseline zero, HW labelled
with its cause, LW, typical week, slack water) and as a traverse of 52 depth figures under it.
Beneath, one 52-week line per repository on one shared scale, with its commits as a spot
height. Both commit instruments are named once in the source line (author-filtered clones
upright, GitHub's calendar as the second instrument). No motion: this sheet is finished at
t = 0 in every edition.
"""
from __future__ import annotations

import math

import chartlib as C
import edition as E
import typeset as T
from edition import fmt, I

NAME = "soundings"
KIND = "strip"
SIZES = {"desk": (1280, 400), "phone": (720, 360)}
BREAKS: list[tuple[str, str, str]] = [
    ("No neat line", "paper only, head and foot rules", "a tide table is printed in the margin, not framed (27)"),
    ("Two projections of one series", "curve above, 52 depth figures along a traverse below",
     "the hydrographer reads the figures, the reader reads the curve (08, 13)"),
    ("Register on a shared scale", "15 of 21 lines are nearly flat at 26 px", "the data is bursty; smoothing or per-line scales would lie (32)"),
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
    out.append(tx(lw_label, lxx, BASE + 13, "label", fill=t.muted, anchor="middle", truth="measured", key="tide.lw"))
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

    # the pencil note in the quiet upper-left of the plot (and the stale note under it)
    out.append(tx(_copy(ctx.cfg, "log_footnote", "Heights observed, not predicted."),
                  X0 + 8, 90, "note", fill=t.ink2))
    if stale:
        out.append(tx(f"no sounding taken {_dmy(str(data.get('taken') or taken))}", X0 + 8, 112, "note", fill=t.ink2))

    # the traverse: 52 depth figures (upright: measured from the clones), month ticks and letters
    TRV = 214
    out.append(f'<path d="M{X0} {TRV + 4}H{X1}" fill="none" {C.stroke("HAIR", t.ink, 0.5, caps="butt")}/>')
    for i, (x, v) in enumerate(zip(xs, ns)):
        out.append(T.sounding(v, round(x, 1), TRV, truth="measured", edition=ed, key=f"week.{i}"))
    ticks = _month_ticks(starts)
    d = "".join(f"M{fmt(xs[i])} {TRV + 4}v5" for i, _ in ticks)
    out.append(f'<path d="{d}" fill="none" {C.stroke("HAIR", t.ink, 0.7, caps="butt")}/>')
    for i, letter in ticks:
        out.append(tx(letter, xs[i], 236, "label", fill=t.ink2, anchor="middle"))

    # fleet register as a tide-table block: ruled rows and columns, one 52-week line per repository on
    # one shared scale with its own baseline, name in caps, commits as a spot height
    repos = sorted((r for r in data.get("repos") or [] if r.get("weeks")), key=lambda r: (-int(r.get("commits") or 0), r["name"]))
    if repos:
        cols = max(7, math.ceil(len(repos) / 3))
        rows = math.ceil(len(repos) / cols)
        pitch_x = (X1 - X0 + 9) / cols
        cell_w = pitch_x - 9
        HEAD, y0, pitch_y, spark_h = 250, 256, 44, 26
        ymax = max(max(int(v) for v in r["weeks"]) for r in repos) or 1
        out.append(tx("REPOSITORY · 52 WEEKS · COMMITS", X0, HEAD, "label", fill=t.muted))
        out.append(tx(f"one line per repository · 52 weeks · {_n(ymax)} commits a week at full height · ink: underway this quarter",
                      X1, HEAD, "label", fill=t.muted, anchor="end"))
        rules = "".join(f"M{X0} {fmt(y0 + r * pitch_y)}H{X1}" for r in range(rows + 1))
        rules += "".join(f"M{fmt(X0 + c * pitch_x - 4.5)} {y0}v{rows * pitch_y}" for c in range(1, cols))
        out.append(f'<path d="{rules}" fill="none" {C.stroke("HAIR", t.ink, 0.5, caps="butt")}/>')
        for k, r in enumerate(repos[:cols * rows]):
            c, rr = k % cols, k // cols
            cx, cy = X0 + c * pitch_x, y0 + rr * pitch_y
            active = bool(r.get("active"))
            name = _chart_name(r["name"], ctx.cfg).upper()
            count = _n(r.get("commits") or 0)
            cw = T.text_width(count, "label", edition=ed)
            room = cell_w - cw - 6
            while name and T.text_width(name, "label", edition=ed) > room:
                name = (name[:-2] if name.endswith("…") else name[:-1]).rstrip() + "…"
            out.append(tx(name, cx, cy + 12, "label", fill=t.ink if active else t.ink2))
            out.append(tx(count, cx + cell_w, cy + 12, "label", fill=t.ink, anchor="end", truth="measured",
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
    out.append(tx(_copy(ctx.cfg, "log_footnote", "Heights observed, not predicted."),
                  X0, 312, "place-water", fill=t.ink if ed.dark else t.ink2))
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
