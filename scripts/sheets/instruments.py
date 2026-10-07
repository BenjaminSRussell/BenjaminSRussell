"""instruments — Sheet 5: the equipment list (T9 §2C, MASTERPLAN decision 2).

A chart's instrument inventory in three columns, LEAD · LOG · LOOKOUT (languages; stores and
queues; deck), each line a fitting from chart.toml [fittings] with the first commit of the
repository that carries it as its commissioning date. Bold = the repository is underway this
quarter (stats.json repos[].active). Full-width 1280×290; the columns hang on the right two
thirds, the left third carries the title, key and the three groups as large rotated caps. No motion.
Phone (720×200): three stacked lines, the group word as a caps head and its fittings after it.
"""
from __future__ import annotations

import re
import sys

import chartlib as C
import edition as E
import typeset as T
from edition import fmt

NAME = "instruments"
KIND = "strip"
SIZES = {"desk": (1280, 290), "phone": (720, 200)}
BREAKS: list[tuple[str, str, str]] = [
    ("Right-hung columns", "columns at x 480→1280, the left third nearly empty",
     "the one broken hang on the page; the silhouette names the sheet (27, decision 2)"),
    ("Mono in the columns", "names in Plex Mono, dates in Condensed",
     "an inventory is typed, not lettered (T9 §2C); the dates fit the column in the narrower face"),
    ("Large rotated group caps", "LEAD · LOG · LOOKOUT at 46 px in the left panel",
     "the left third is the sheet's title block, not blank paper (round 2)"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
# marks in the gutter, all from chartlib.symbol_defs: a named override, else by group (languages are
# points on the course: a fix for the flagship repos, a waypoint otherwise; stores anchor; deck watches)
MARKS = {"Prometheus · Grafana": "light"}
GROUP_MARK = {"LEAD": "waypoint", "LOG": "anchorage", "LOOKOUT": "station"}
FLAGSHIP = ("Scrapy", "Rust-sitemap")
GLOSS = {"LEAD": "what measures depth", "LOG": "what keeps the record", "LOOKOUT": "what watches"}
MARK_NAMES = ("fix", "waypoint", "anchorage", "light", "station")
COL_X = (480, 747, 1013)
COL_W = 266
MARK_X, NAME_X, DATE_X = 14, 30, 250      # within a column: the symbol gutter, the name, the date's right edge


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
    for ft in (data.get("features") or []):
        pass
    return idx


def _mark(kind: str, x: float, y: float, theme) -> str:
    """A legend mark in the row's gutter, centred on x, at 0.9 (the same <use> ids the legend defines)."""
    if kind not in MARK_NAMES:
        return ""
    return C.use(kind, x, y - 5, NAME, scale=0.9)


def _mark_for(item: dict, code: str) -> str | None:
    name = str(item.get("name", ""))
    if item.get("mark"):
        return str(item["mark"])
    if name in MARKS:
        return MARKS[name]
    if code == "LEAD" and str(item.get("repo", "")) in FLAGSHIP:
        return "fix"
    return GROUP_MARK.get(code)

def _symbols(theme, edition: str, names) -> str:
    """Only the sheet's own symbols out of chartlib.symbol_defs (same ids, same drawings), so a sheet
    that places one anchor does not carry eighteen symbols."""
    full = C.symbol_defs(theme, NAME, edition)
    tag = re.compile(r"<(/?)g\b[^>]*?(/?)>")
    out = []
    for n in names:
        start = full.find(f'<g id="{NAME}-sym-{n}">')
        if start < 0:
            continue
        depth, i = 0, start
        while True:
            m = tag.search(full, i)
            if not m:
                break
            if m.group(1) == "/":
                depth -= 1
            elif m.group(2) != "/":
                depth += 1
            i = m.end()
            if depth == 0:
                out.append(full[start:i])
                break
    return "".join(out)



def _bold(svg: str, color: str) -> str:
    """Faux-bold for the one condensed cut: a .45 px spread stroke in the fill colour (typeset's grade trick)."""
    return svg.replace(f'<g fill="{color}"', f'<g fill="{color}" stroke="{color}" stroke-width="0.45" paint-order="stroke" '
                       f'stroke-linejoin="round"', 1)


def _desk(ctx) -> str:
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["desk"]
    groups, items = _fittings(cfg)
    repos = _repo_index(data)
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = []
    defs = _symbols(t, ed.name, MARK_NAMES)
    rows = max([sum(1 for i in items if i.get("group") == g[0]) for g in groups] + [6])
    y_top, pitch, y_first = 44, 34, 80            # six rows at 34 px: 80 … 250 (17 px names read at 870)
    y_bot = y_first + (rows - 1) * pitch + 8
    for x in (COL_X[1] - 1, COL_X[2] - 1):
        out.append(f'<path d="M{x} {y_top}V{y_bot}" fill="none" {C.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
    for gi, (code, gloss) in enumerate(groups[:3]):
        cx = COL_X[gi]
        out.append(tx(f"{code} · {gloss.upper()}", cx + NAME_X, y_first - 24, "machine", fill=t.ink2, tracking=1.0))
        col_items = [i for i in items if i.get("group") == code]
        for ri, item in enumerate(col_items):
            y = y_first + ri * pitch
            name = str(item.get("name", ""))
            repo = repos.get(str(item.get("repo", ""))) or repos.get(str(item.get("repo", "")).lower())
            active = bool(repo and repo.get("active"))
            fill = t.ink if active else t.ink2
            run = tx(name, cx + NAME_X, y, "label", fill=fill, size=17)
            out.append(_bold(run, fill) if active else run)
            pen = cx + NAME_X + T.text_width(name, "label", size=17, edition=ed)
            mark = _mark_for(item, code)
            if mark:
                out.append(_mark(mark, cx + MARK_X, y, t))
            fitted = _my(repo.get("first")) if repo else ""
            fw = T.text_width(fitted, "label", edition=ed) if fitted else 0
            lead_end = cx + DATE_X - fw - 8 if fitted else cx + DATE_X
            if lead_end - (pen + 8) >= 10:
                out.append(f'<path d="M{fmt(pen + 8)} {fmt(y - 1)}H{fmt(lead_end)}" fill="none" '
                           f'{C.stroke("HAIR", t.ink2, 0.9, "TRACK")}/>')
            if fitted:
                out.append(tx(fitted, cx + DATE_X, y, "label", fill=t.ink2, anchor="end", truth="measured",
                              key=f"fitted.{name}"))
    # the left third (decision 2): the sheet's name and key, the three groups as large rotated condensed caps
    # with their plain-words gloss, hairlines between
    out.append(tx("INSTRUMENTS · EQUIPMENT LIST", 48, 40, "label-caps", fill=t.ink2))
    n_active = sum(1 for r in (data.get("repos") or []) if r.get("active"))
    band_w = 142
    # the key sits top-right above the column heads, clear of the rotated block (round 6)
    out.append(tx(f"bold · underway this quarter ({n_active} of {chart_no}) · date · first commit of its repository",
                  COL_X[2] + DATE_X, 40, "label", fill=t.ink2, anchor="end", truth="measured", key="active_count"))
    for gi, (code, _gloss) in enumerate(groups[:3]):
        bx = 48 + gi * band_w
        if gi:
            out.append(f'<path d="M{bx - 12} {y_first - 10}V{y_bot}" fill="none" {C.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
        out.append(tx(code.upper(), bx + 34, y_bot - 4, "label", fill=t.ink2, size=46, tracking=2.0, rotate=-90))
        out.append(tx(GLOSS.get(code, _gloss.lower()), bx, y_bot + 14, "label", fill=t.ink2))
    out.append(tx(f"CHART NO. {chart_no} · SHEET 5", 24, H_ - 5, "label-caps", fill=t.muted, key="folio"))
    return E.svg(ed, W_, H_, "".join(out), defs + T.glyph_defs(), sheet=NAME)


def _wrap(words: list[str], width: float, measure) -> list[str]:
    lines, cur = [], ""
    for w in words:
        cand = f"{cur}, {w}" if cur else w
        if cur and measure(cand) > width:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def _phone(ctx) -> str:
    """Three stacked lines: the group word as a 26 px caps head, its fittings after it, wrapped."""
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["phone"]
    groups, items = _fittings(cfg)
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = []
    ink2 = t.ink if ed.dark else t.ink2      # phone night: semantic text in full ink (10)
    y, X_ITEMS, PITCH = 42, 150, 30
    for gi, (code, _gloss) in enumerate(groups[:3]):
        names = [str(i.get("name", "")) for i in items if i.get("group") == code]
        lines = _wrap(names, W_ - 16 - X_ITEMS, lambda s_: T.text_width(s_, "label", edition=ed))
        out.append(tx(code.upper(), 16, y, "label", fill=t.ink))
        for ln in lines:
            out.append(tx(ln, X_ITEMS, y, "label", fill=ink2))
            y += PITCH
    out.append(tx(f"CHART NO. {chart_no} · SHEET 5", 704, H_ - 8, "label-caps", fill=t.muted, anchor="end", key="folio"))
    return E.svg(ed, W_, H_, "".join(out), T.glyph_defs(), sheet=NAME)


def build(ctx) -> str:
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    groups, items = _fittings(cfg)
    glosses = [g[1].lower() for g in groups[:3]] or ["languages", "stores and queues", "deck"]
    return (f"Instruments carried, {len(items)} fittings in three columns: {', '.join(glosses)}; dated by first commit. "
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
