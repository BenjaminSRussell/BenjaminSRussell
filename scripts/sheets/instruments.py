"""instruments — Sheet 5: the equipment list (T9 §2C, MASTERPLAN decision 2).

A chart's own list of fittings in three columns across the sheet, LEAD · LANGUAGES, LOG · STORES AND
QUEUES, LOOKOUT · DECK, each line a fitting from chart.toml [fittings] with the first commit of the
repository that carries it as its commissioning date (the top margin says so: DATUM: FIRST COMMIT).
Bold = the repository is underway this quarter (stats.json repos[].active). A neutral gutter tick
(chartlib.tick, no charted meaning) marks each line; `·` joins the parts of one fitting's name.
Minute-bar neat line like every sheet of the set. Full-width 1280×376; the columns at x 48, 443,
838 (395 px pitch), names and dates at 19 px on a 40 px pitch. No motion.
Phone (720×820): the same list redrawn at 26 px, each group's head across the sheet and its fittings
one to a row with a leader to the date, the bold carried.

Sizes (desk, v9.1 scale): names and dates 19 (label), the unit line and folio 19 (label-caps), the
column heads 19 (machine). Phone: names, dates and heads 26 (label), unit line and folio 26 (label-caps).
"""
from __future__ import annotations

import math
import re
import sys

import chartlib as C
import edition as E
import typeset as T
from edition import fmt

NAME = "instruments"
KIND = "strip"
SIZES = {"desk": (1280, 376), "phone": (720, 820)}
RULES = {"desk": (32, 38), "phone": (38, 44)}       # neat line insets (outer LINE, inner HAIR); 6 px minute bars between
BREAKS: list[tuple[str, str, str]] = [
    ("A chart's list, not a sidebar", "three columns span the sheet inside a minute-bar neat line; DATUM: FIRST COMMIT in the top margin",
     "v9.2 (art 4, owner 8, hydrographer 8): the rotated LEAD / LOG / LOOKOUT said what the column heads say, the sheet "
     "had no neat line and no datum, and the fix / waypoint / anchorage / station marks meant other things in the legend"),
    ("Neutral gutter tick", "chartlib.tick, a 7 px PEN dash before each fitting, defined in the sheet's own <defs>",
     "a symbol means one thing on every sheet of a chart; the tick is in no legend because it says nothing"),
    ("Mono column heads, condensed names and dates", "LEAD · LANGUAGES etc. in machine 19 at tracking 0; names in Condensed",
     "an inventory is typed, not lettered (T9 §2C); LOG · STORES AND QUEUES tracked at 1.0 crossed the next column's rule"),
    ("Columns at 48, 443, 838 on a 395 px pitch", "names 14 px after the tick, the date right-aligned 12 px before the next rule",
     "v9.2: the left third was the rotated words' panel; the columns now use the whole 1184 px between the inner rules"),
    ("Rows on a 40 px pitch, sheet 376 tall", "heads at 80, six rows 116→316, the inner rule at 338, the folio at 366",
     "19 px names on a 34 px pitch touched (v9.1); the neat line and the margin lines add 16 px over v9.1's 360"),
    ("Phone carries the heads, the dates and the bold", "720×820: a head row per group, fittings one to a row at 26 px on a 32 px "
     "pitch with a dotted leader to the date, the active fitting in the spread stroke",
     "v9.2 (mobile 11): the phone edition named the fittings and nothing else; the alt promised dates and bold; two to a row "
     "would not hold `Prometheus · Grafana` and its date in 292 px"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
COL_X = (48, 443, 838)
COL_PITCH = 395
TICK_X, NAME_X, DATE_X = 10, 24, COL_PITCH - 12     # within a column: the tick, the name, the date's right edge
PITCH, Y_HEADS, Y_FIRST = 40, 80, 116               # row pitch, the column heads' baseline, the first row's baseline


def _my(iso: str | None) -> str:
    if not iso or len(iso) < 7:
        return ""
    return f"{MONTHS[int(iso[5:7]) - 1]} {iso[:4]}"


def _fittings(cfg) -> tuple[list[tuple[str, str]], list[dict]]:
    f = cfg.get("fittings") or {}
    groups = [tuple(g) for g in (f.get("groups") or [["LEAD", "Languages"], ["LOG", "Stores and queues"], ["LOOKOUT", "Deck"]])]
    items = [dict(i) for i in (f.get("items") or [])]
    return groups, items


def _repo_index(data: dict) -> dict:
    idx = {}
    for r in data.get("repos") or []:
        idx[r["name"]] = r
        idx[r["name"].lower()] = r
        for a in r.get("aliases") or []:
            idx[a] = r
    return idx


def _repo_of(item: dict, repos: dict) -> dict | None:
    return repos.get(str(item.get("repo", ""))) or repos.get(str(item.get("repo", "")).lower())


def _tick_defs(theme) -> str:
    return f'<g id="{NAME}-sym-tick">{C.tick(theme)}</g>'


def _bold(svg: str, color: str) -> str:
    """Faux-bold for the one condensed cut: a .45 px spread stroke in the fill colour (typeset's grade trick)."""
    return svg.replace(f'<g fill="{color}"', f'<g fill="{color}" stroke="{color}" stroke-width="0.45" paint-order="stroke" '
                       f'stroke-linejoin="round"', 1)


def _desk(ctx) -> str:
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["desk"]
    R0, R1 = RULES["desk"]
    groups, items = _fittings(cfg)
    repos = _repo_index(data)
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = [C.frame(W_, H_, t, "minute-bars", rules=(R0, R1))]
    out.append(tx("DATUM: FIRST COMMIT", W_ / 2, 20, "label-caps", fill=t.ink, anchor="middle", key="unit"))
    rows = max([sum(1 for i in items if i.get("group") == g[0]) for g in groups] + [6])
    y_top = Y_HEADS - 20
    y_bot = Y_FIRST + (rows - 1) * PITCH + 10
    if y_bot > H_ - R1 - 8:
        raise ValueError(f"instruments: {rows} rows reach {y_bot}; the inner rule is at {H_ - R1}")
    for x in (COL_X[1] - 12, COL_X[2] - 12):
        out.append(f'<path d="M{x} {y_top}V{y_bot}" fill="none" {C.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
    for gi, (code, gloss) in enumerate(groups[:3]):
        cx = COL_X[gi]
        out.append(tx(f"{code} · {gloss.upper()}", cx + NAME_X, Y_HEADS, "machine", fill=t.ink2))
        col_items = [i for i in items if i.get("group") == code]
        for ri, item in enumerate(col_items):
            y = Y_FIRST + ri * PITCH
            name = str(item.get("name", ""))
            repo = _repo_of(item, repos)
            active = bool(repo and repo.get("active"))
            fill = t.ink if active else t.ink2
            run = tx(name, cx + NAME_X, y, "label", fill=fill)
            out.append(_bold(run, fill) if active else run)
            out.append(C.use("tick", cx + TICK_X, y - 6, NAME))
            pen = cx + NAME_X + T.text_width(name, "label", edition=ed)
            fitted = _my(repo.get("first")) if repo else ""
            fw = T.text_width(fitted, "label", edition=ed) if fitted else 0
            lead_end = cx + DATE_X - fw - 8 if fitted else cx + DATE_X
            if lead_end - (pen + 8) >= 10:
                out.append(f'<path d="M{fmt(pen + 8)} {fmt(y - 1)}H{fmt(lead_end)}" fill="none" '
                           f'{C.stroke("HAIR", t.ink2, 0.9, "TRACK")}/>')
            if fitted:
                out.append(tx(fitted, cx + DATE_X, y, "label", fill=t.ink2, anchor="end", truth="measured",
                              key=f"fitted.{name}"))
    out.append(tx(f"CHART NO. {chart_no} · SHEET 5", R0, H_ - 10, "label-caps", fill=t.muted, key="folio"))
    return E.svg(ed, W_, H_, "".join(out), _tick_defs(t) + T.glyph_defs(), sheet=NAME)


def _phone(ctx) -> str:
    """One list at 26 px: each group's head across the sheet, then its fittings one to a row, the name left,
    a dotted leader, the date right; the active fitting in the spread stroke. 720×820: eighteen fittings and
    three heads on a 32 px pitch (two fittings to a row would cut `Prometheus · Grafana` from its date)."""
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["phone"]
    R0, R1 = RULES["phone"]
    groups, items = _fittings(cfg)
    repos = _repo_index(data)
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))
    X0, X1 = 56, 664
    PITCH_P, HEAD_GAP, GROUP_GAP = 32, 32, 16
    TICK_P, NAME_P = 6, 22

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    ink2 = t.ink if ed.dark else t.ink2      # phone night: semantic text in full ink (10)
    out: list[str] = [C.frame(W_, H_, t, "minute-bars", rules=(R0, R1))]
    out.append(tx("DATUM: FIRST COMMIT", W_ / 2, 26, "label-caps", fill=t.ink, anchor="middle", key="unit"))
    y = R1 + 40
    for gi, (code, gloss) in enumerate(groups[:3]):
        if gi:
            y += GROUP_GAP
        out.append(tx(f"{code} · {gloss.upper()}", X0, y, "label", fill=ink2))
        out.append(f'<path d="M{X0} {y + 8}H{X1}" fill="none" {C.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
        y += HEAD_GAP
        for item in [i for i in items if i.get("group") == code]:
            name = str(item.get("name", ""))
            repo = _repo_of(item, repos)
            active = bool(repo and repo.get("active"))
            fill = t.ink if active else ink2
            fitted = _my(repo.get("first")) if repo else ""
            fw = T.text_width(fitted, "label", edition=ed) if fitted else 0
            nw = T.text_width(name, "label", edition=ed)
            if X0 + NAME_P + nw + 8 + fw > X1:
                raise ValueError(f"instruments phone: {name!r} and its date need {NAME_P + nw + 8 + fw:.0f} px; the row holds {X1 - X0}")
            run = tx(name, X0 + NAME_P, y, "label", fill=fill)
            out.append(_bold(run, fill) if active else run)
            out.append(C.use("tick", X0 + TICK_P, y - 8, NAME, scale=1.3))
            pen = X0 + NAME_P + nw
            lead_end = X1 - fw - 10 if fitted else X1
            if lead_end - (pen + 10) >= 14:
                out.append(f'<path d="M{fmt(pen + 10)} {fmt(y - 1)}H{fmt(lead_end)}" fill="none" '
                           f'{C.stroke("HAIR", t.ink2, 0.9, "TRACK")}/>')
            if fitted:
                out.append(tx(fitted, X1, y, "label", fill=ink2, anchor="end", truth="measured", key=f"fitted.{name}"))
            y += PITCH_P
    if y - PITCH_P + 10 > H_ - R1:
        raise ValueError(f"instruments phone: the list reaches {y - PITCH_P + 10}; the inner rule is at {H_ - R1}")
    out.append(tx(f"CHART NO. {chart_no} · SHEET 5", R0, H_ - 9, "label-caps", fill=t.muted, key="folio"))
    return E.svg(ed, W_, H_, "".join(out), _tick_defs(t) + T.glyph_defs(), sheet=NAME)


def build(ctx) -> str:
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    """True of every edition (v9.2): the phone carries the dates and the bold too; no column count."""
    groups, items = _fittings(cfg)
    glosses = [g[1].lower() for g in groups[:3]] or ["languages", "stores and queues", "deck"]
    return (f"Instruments carried, {len(items)} fittings: {', '.join(glosses)}; dated by first commit. "
            f"Bold: underway this quarter; the rest when asked.")


# ------------------------------------------------------------------ build-report hook: symbols used
def _hook(ctx, doc: str, entry: dict) -> None:
    if getattr(ctx, "sheet", None) != NAME:
        return
    entry["symbols_used"] = sorted(set(re.findall(rf'href="#{NAME}-sym-([\w-]+)"', doc)))


def _register_hook() -> None:
    mods = [m for m in (sys.modules.get("__main__"), sys.modules.get("build_assets"))
            if m is not None and hasattr(m, "report_hooks")]
    if not mods:
        try:
            import build_assets  # noqa: WPS433
            mods = [build_assets]
        except Exception:  # noqa: BLE001
            return
    for m in mods:
        if _hook not in m.report_hooks:
            m.report_hooks.append(_hook)


_register_hook()
