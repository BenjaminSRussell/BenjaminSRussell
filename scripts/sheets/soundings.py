"""soundings — Sheet 2: the tide table of the last 52 weeks and the fleet register (T9 §2A).

Depth = count. The 52 weekly commit counts are the same soundings the hero's contours are
solved from, shown twice here: as the tide curve (monotone cubic, baseline zero, HW labelled
with its cause, LW, typical week, slack water) and as a traverse of depth figures under it: every
non-zero week on one of two staggered baselines (a tide table lists every reading), one 0 for a
run of zero weeks. Beneath, one 52-week line per repository on one shared scale, with its commits
as a spot height, five to a row, every repository under the chart's one gazetteer name. Both
commit instruments are named once in the source line (author-filtered clones upright, GitHub's
calendar as the second instrument). Minute-bar neat line like every sheet of the set (v9.2); the
margins carry the dateline and `SOUNDINGS IN COMMITS · DATUM: MAIN` above, the folio and the
source line below. No motion: this sheet is finished at t = 0 in every edition.

Sizes (desk 1280×560, v9.1 scale): dateline, unit line, tide labels, month letters, register names
and counts, source line and folio 19 (label / label-caps); the week figures 16 (texture,
sounding()). Phone (720×370): unit line, dateline, HW/LW labels, month letters and folio 26
(label / label-caps); the stale note 26 (label-italic).
"""
from __future__ import annotations

import math

import chartlib as C
import edition as E
import gazetteer
import typeset as T
from edition import fmt, I

NAME = "soundings"
KIND = "strip"
SIZES = {"desk": (1280, 560), "phone": (720, 370)}
RULES = {"desk": (32, 38), "phone": (38, 44)}       # neat line insets (outer LINE, inner HAIR); 6 px minute bars between
BREAKS: list[tuple[str, str, str]] = [
    ("Minute-bar neat line, 560 px sheet", "chartlib.frame at 32/38 (phone 38/44); the dateline and unit line at baseline 20 "
     "above it, the folio and source line at 550 below it; the curve spans 60→1220 inside the register's 48→1232 so the first "
     "and last week figures stay off the rule",
     "v9.2: one neat line for the set (sheets 1, 3 and 6 had one; 2, 4 and 5 floated); a 19 px margin line clears the "
     "outer rule by 6 px or more"),
    ("Two projections of one series", "curve above, the depth figures along a traverse below",
     "the hydrographer reads the figures, the reader reads the curve (08, 13)"),
    ("Register on a shared scale", "15 of 21 lines are nearly flat at 18 px", "the data is bursty; smoothing or per-line scales would lie (32)"),
    ("Traverse staggered, not thinned", "every non-zero week on one of two baselines 18 px apart (alternate weeks), "
     "8 px of paper between figures on a row; one 0 at the middle of a run of zero weeks (or at LW); HW and LW always",
     "v9.2 (hydrographer): a tide table lists every reading; v9.1's thinning left 11 of 20 non-zero weeks unprinted"),
    ("Register names from the gazetteer", "COURSE CRUSADER I., IDEAL-URL-ORGANIZER I., DATA-VISUALIZER I. as the hero prints them",
     "v9.2: one gazetteer for every sheet; a name that will not fit five to a row drops the register to four columns, never a cut"),
    ("Register five to a row", "5 × 5 cells of 229 px on a 44 px pitch, rules drawn per filled cell (four to a row on a 36 px pitch "
     "when a name needs it)", "every chart name fits uncut at 19 px (3D-SWIFT-GLOBE-WIDGET is 212 px); the ragged last row has no empty boxes"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
TRAVERSE_ROWS = 2
ROW_DY = 18                  # the second traverse baseline, under the first (16 px figures: 6 px of paper between rows)


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


def _chart_name(name: str, data: dict, cfg) -> str:
    """The gazetteer's name for a repository (the hero prints the same one)."""
    return gazetteer.name_of(name, data, cfg or {})


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


def _unit_line(cfg) -> str:
    return _copy(cfg, "unit_hero", "SOUNDINGS IN COMMITS") + " · DATUM: MAIN"


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


def _traverse(ns: list[int], xs: list[float], hw_i: int, lw_i: int, width_of, gap: float = 8.0,
              rows: int = TRAVERSE_ROWS) -> list[tuple[int, int]]:
    """(week index, row) for every figure printed on the traverse, in week order. Every non-zero week is
    wanted, plus one 0 for each run of zero weeks (at LW when LW lies in the run, else at its middle);
    HW and LW are placed first. A week's own row alternates with its index (week i on row i mod `rows`)
    so neighbours never share a baseline; a figure prints on its row only when `gap` px of paper
    separates it from every figure already on that row, else on another row that has the room, else not
    at all. Nothing is invented and nothing printed is moved."""
    n = len(ns)
    wanted = [i for i in range(n) if ns[i] > 0]
    i = 0
    while i < n:
        if ns[i] > 0:
            i += 1
            continue
        j = i
        while j + 1 < n and ns[j + 1] == 0:
            j += 1
        pick = lw_i if i <= lw_i <= j else (i + j) // 2
        if pick not in wanted:
            wanted.append(pick)
        i = j + 1
    order = [hw_i] + ([lw_i] if lw_i != hw_i else [])
    order += sorted(i for i in wanted if i not in order)
    placed: list[list[tuple[float, float]]] = [[] for _ in range(rows)]
    chosen: list[tuple[int, int]] = []
    for i in order:
        w = width_of(ns[i])
        x0, x1 = xs[i] - w / 2, xs[i] + w / 2
        own = i % rows
        for r in [own] + [r for r in range(rows) if r != own]:
            if all(x1 + gap <= p0 or x0 >= p1 + gap for p0, p1 in placed[r]):
                placed[r].append((x0, x1))
                chosen.append((i, r))
                break
    return sorted(chosen)


def _register_layout(names: list[str], counts: list[str], x0: float, x1: float, ed) -> tuple[int, float, int]:
    """(columns, row pitch, sparkline height): five to a row while every name fits its cell uncut beside
    its count, else four to a row on a tighter pitch (the sheet height is fixed; the names are not cut)."""
    for cols, pitch_y, spark_h in ((5, 44, 18), (4, 36, 14)):
        cell_w = (x1 - x0 + 9) / cols - 9
        if all(T.text_width(nm, "label", edition=ed) + T.text_width(ct, "label", edition=ed) + 4 <= cell_w
               for nm, ct in zip(names, counts)):
            return cols, pitch_y, spark_h
    widest = max(names, key=lambda nm: T.text_width(nm, "label", edition=ed))
    raise ValueError(f"register: {widest!r} is {T.text_width(widest, 'label', edition=ed):.0f} px; no cell holds it uncut")


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
    R0, R1 = RULES["desk"]
    X0, X1 = 48, 1232            # the register, 10 px inside the inner rule
    CX0, CX1 = 60, 1220          # the curve and traverse: a 16 px figure centred on the first or last week stays off the rule
    TOP, BASE = 68, 186          # HW at TOP, zero at BASE
    TRV = 236                    # the traverse's first baseline; the second at TRV + ROW_DY; letters under the rule
    MARGIN_TOP, MARGIN_BOT = 20, H_ - 10      # the margin lines' baselines, clear of the outer rule by ≥ 6 px

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = [C.frame(W_, H_, t, "minute-bars", rules=(R0, R1))]
    # top margin: dateline left, the unit and datum line centred (the sheet's one tracked caps run)
    taken = str(data.get("updated_at") or data.get("taken") or "")
    date_s = _dmy(taken) if taken else ""
    hm = _hm(taken)
    dateline = f"Soundings taken {date_s}" + (f" · {hm} UTC" if hm else "")
    out.append(tx(dateline, R0, MARGIN_TOP, "label", fill=t.ink, truth="measured", key="dateline"))
    out.append(tx(_unit_line(ctx.cfg), W_ / 2, MARGIN_TOP, "label-caps", fill=t.ink, anchor="middle", key="unit"))

    # the tide curve
    scale_n = max(td["hw_n"], 1)
    xs = [CX0 + i * (CX1 - CX0) / (n - 1) for i in range(n)]

    def y_of(v: float) -> float:
        return BASE - (BASE - TOP) * v / scale_n

    pts = [(round(x, 1), round(y_of(v), 1)) for x, v in zip(xs, ns)]
    area = C.monotone_path(pts, baseline=BASE)
    curve = C.monotone_path(pts)
    out.append(f'<path d="{area}" fill="{t.shallow_a}" fill-opacity=".55"/>')
    # typical week: dotted rule (coincides with the baseline when the median is 0)
    y_med = y_of(td["median"])
    if td["median"] > 0:
        out.append(f'<path d="M{CX0} {fmt(y_med)}H{CX1}" fill="none" {C.stroke("HAIR", t.ink2, 0.9, "TRACK", caps="butt")}/>')
    # baseline (dashed when the sounding is stale)
    out.append(f'<path d="M{CX0} {BASE}H{CX1}" fill="none" '
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
    hw_label = f"HW {_n(td['hw_n'])} · wk of {_dm(starts[td['hw_i']])} · {_chart_name(td['cause'], data, ctx.cfg)}{td['sprint']}"
    if hx > (CX0 + CX1) / 2:
        out.append(tx(hw_label, hx - 9, hy + 4, "label", fill=t.ink, anchor="end", truth="measured", key="tide.hw"))
    else:
        out.append(tx(hw_label, hx + 9, hy + 4, "label", fill=t.ink, truth="measured", key="tide.hw"))
    lw_label = f"LW {_n(td['lw_n'])} · wk of {_dm(starts[td['lw_i']])}"
    lw_w = T.text_width(lw_label, "label", edition=ed)
    lxx = min(max(lx, CX0 + lw_w / 2), CX1 - lw_w / 2)
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
    med_x = CX0 + mi * (CX1 - CX0) / (n - 1)
    med_w = T.text_width(med_label, "label", edition=ed)
    med_x = min(max(med_x, CX0 + med_w / 2 + 4), CX1 - med_w / 2 - 4)
    out.append(tx(med_label, med_x, med_y, "label", fill=t.muted, anchor="middle", truth="measured", key="tide.median"))
    out.append(tx(f"slack water · {td['slack_month']}", (bx0 + bx1) / 2, BASE - 5, "label", fill=t.muted,
                  anchor="middle", truth="measured", key="tide.slack"))

    # the stale note in the quiet upper-left of the plot (v9.1: the pencil footnote is gone; the curve shows)
    if stale:
        out.append(tx(f"no sounding taken {_dmy(str(data.get('taken') or taken))}", X0 + 8, 94, "note", fill=t.ink2))

    # the traverse: every reading (upright: measured from the clones) on two staggered baselines, the rule
    # under the lower one, month ticks and letters
    rule_y = TRV + ROW_DY * (TRAVERSE_ROWS - 1) + 4
    out.append(f'<path d="M{CX0} {rule_y}H{CX1}" fill="none" {C.stroke("HAIR", t.ink, 0.5, caps="butt")}/>')
    for i, row in _traverse(ns, xs, td["hw_i"], td["lw_i"], lambda v: T.text_width(str(v), "texture", edition=ed)):
        out.append(T.sounding(ns[i], round(xs[i], 1), TRV + ROW_DY * row, truth="measured", edition=ed, key=f"week.{i}"))
    ticks = _month_ticks(starts)
    d = "".join(f"M{fmt(xs[i])} {rule_y}v5" for i, _ in ticks)
    out.append(f'<path d="{d}" fill="none" {C.stroke("HAIR", t.ink, 0.7, caps="butt")}/>')
    for i, letter in ticks:
        out.append(tx(letter, xs[i], rule_y + 20, "label", fill=t.ink2, anchor="middle"))

    # fleet register as a tide-table block: ruled rows and columns, one 52-week line per repository on
    # one shared scale with its own baseline, the gazetteer name in caps, commits as a spot height
    repos = sorted((r for r in data.get("repos") or [] if r.get("weeks")), key=lambda r: (-int(r.get("commits") or 0), r["name"]))
    if repos:
        names = [_chart_name(r["name"], data, ctx.cfg).upper() for r in repos]
        counts = [_n(r.get("commits") or 0) for r in repos]
        cols, pitch_y, spark_h = _register_layout(names, counts, X0, X1, ed)
        rows = math.ceil(len(repos) / cols)
        pitch_x = (X1 - X0 + 9) / cols
        cell_w = pitch_x - 9
        y0 = rule_y + 32                                   # the register's top rule, 12 under the month letters
        if y0 + rows * pitch_y > H_ - R1 - 10:
            raise ValueError(f"register: {rows} rows of {pitch_y} px from {y0} overrun the inner rule at {H_ - R1}")
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
        name_dy = 17 if pitch_y >= 44 else 15
        for k, r in enumerate(filled):
            c, rr = k % cols, k // cols
            cx, cy = X0 + c * pitch_x, y0 + rr * pitch_y
            active = bool(r.get("active"))
            out.append(tx(names[k], cx, cy + name_dy, "label", fill=t.ink if active else t.ink2))
            out.append(tx(counts[k], cx + cell_w, cy + name_dy, "label", fill=t.ink, anchor="end", truth="measured",
                          key=f"repo.{r['name']}.commits"))
            base_y = cy + pitch_y - 4
            wk = [int(v) for v in r["weeks"]]
            m = len(wk)
            spts = [(cx + i * cell_w / (m - 1), base_y - spark_h * v / ymax) for i, v in enumerate(wk)]
            out.append(f'<path d="M{fmt(cx)} {fmt(base_y)}H{fmt(cx + cell_w)}" fill="none" {C.stroke("HAIR", t.hair, caps="butt")}/>')
            out.append(f'<path d="{C.compact_path(spts, False, 1)}" fill="none" '
                       f'{C.stroke("PEN", t.ink2 if ed.dark else t.ink, 0.8)}/>')

    # bottom margin: folio left (decision 27), the source line naming both commit instruments right
    out.append(tx(f"CHART NO. {chart_no} · SHEET 2", R0, MARGIN_BOT, "label-caps", fill=t.muted, key="folio"))
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
    pen = W_ - R0 - sum(widths)
    for (s, tr, key), w in zip(parts, widths):
        out.append(tx(s, pen, MARGIN_BOT, "label", fill=t.ink if tr else t.muted, truth=tr, key=key))
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
    R0, R1 = RULES["phone"]
    X0, X1 = 56, 664
    TOP, BASE = 108, 250
    MARGIN_TOP, MARGIN_BOT = 26, H_ - 9

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = [C.frame(W_, H_, t, "minute-bars", rules=(R0, R1))]
    out.append(tx(_unit_line(ctx.cfg), W_ / 2, MARGIN_TOP, "label-caps", fill=t.ink, anchor="middle", key="unit"))
    taken = str(data.get("updated_at") or data.get("taken") or "")
    out.append(tx(f"52 weeks to {_dmy(taken) if taken else '—'} · {repo_count} repositories", X0, 78, "label",
                  fill=t.ink, truth="measured", key="dateline"))
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
    # HW with its cause (the desk wording; "wk of" because the figure is a week's, not a day's)
    hw_label = f"HW {_n(td['hw_n'])} · wk of {_dm(starts[td['hw_i']])} · {_chart_name(td['cause'], data, ctx.cfg)}{td['sprint']}"
    if T.text_width(hw_label, "label", edition=ed) > (X1 - X0) - 40:
        hw_label = f"HW {_n(td['hw_n'])} · wk of {_dm(starts[td['hw_i']])}"
    if hx > (X0 + X1) / 2:
        out.append(tx(hw_label, hx - 14, hy + 9, "label", fill=t.ink, anchor="end", truth="measured", key="tide.hw"))
    else:
        out.append(tx(hw_label, hx + 14, hy + 9, "label", fill=t.ink, truth="measured", key="tide.hw"))
    # month ticks and initials along the baseline, the LW label on the row under them
    ticks = _month_ticks(starts)
    out.append(f'<path d="{"".join(f"M{fmt(xs[i])} {BASE}v6" for i, _ in ticks)}" fill="none" {C.stroke("HAIR", t.ink, 0.7, caps="butt")}/>')
    for i, letter in ticks:
        out.append(tx(letter, xs[i], BASE + 30, "label", fill=t.ink2, anchor="middle"))
    lw_label = f"LW {_n(td['lw_n'])} · wk of {_dm(starts[td['lw_i']])}"
    lw_w = T.text_width(lw_label, "label", edition=ed)
    lxx = min(max(lx, X0 + lw_w / 2), X1 - lw_w / 2)
    out.append(tx(lw_label, lxx, BASE + 58, "label", fill=t.muted, anchor="middle", truth="measured", key="tide.lw"))
    if stale:
        out.append(tx(f"no sounding taken {_dmy(str(data.get('taken') or taken))}", X0, 140, "label-italic", fill=t.ink2))
    out.append(tx(f"CHART NO. {repo_count} · SHEET 2", R0, MARGIN_BOT, "label-caps", fill=t.muted, key="folio"))
    return E.svg(ed, W_, H_, "".join(out), T.glyph_defs(), sheet=NAME)


def build(ctx) -> str:
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    """True of every edition (v9.2): the desk register is not on the phone, so the alt does not promise it."""
    try:
        td = _tide(data)
    except ValueError:
        return "Tide table of weekly commits, fifty-two weeks, high and low water dated. Every week sounded."
    def alt_for(cause: str) -> str:
        return (f"Tide table of commits: high water {_n(td['hw_n'])}, week of {_dm(td['starts'][td['hw_i']])}, {cause}; "
                f"low water {_n(td['lw_n'])}; typical week {_n(td['median'])}. Every week sounded.")
    text = alt_for(_chart_name(td["cause"], data, cfg))
    if len(text.split()) > 25:
        text = alt_for(td["cause"])
    return text
