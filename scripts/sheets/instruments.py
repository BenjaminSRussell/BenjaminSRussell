"""instruments — Sheet 5: the equipment list (T9 §2C, MASTERPLAN decision 2).

A chart's instrument inventory in three columns, LEAD · LOG · LOOKOUT (languages; stores and
queues; deck), each line a fitting from chart.toml [fittings] with the first commit of the
repository that carries it as its commissioning date. Bold = the repository is underway this
quarter (stats.json repos[].active). Full-width 1280×290; the columns hang on the right two
thirds, the left third carries the reading key and the folio. No motion. Phone: a rule and the
folio (the stack itself is in the README's plain text).
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
SIZES = {"desk": (1280, 290), "phone": (720, 48)}
BREAKS: list[tuple[str, str, str]] = [
    ("Right-hung columns", "columns at x 480→1280, the left third nearly empty",
     "the one broken hang on the page; the silhouette names the sheet (27, decision 2)"),
    ("Mono in the columns", "names and dates in Plex Mono, not Condensed",
     "an inventory is typed, not lettered (T9 §2C)"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
# the three legend-defined marks (T3): a fitting named here (or carrying mark= in chart.toml) gets one
MARKS = {"Rust": "track", "Delta Lake": "anchorage", "Prometheus · Grafana": "light"}
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
    """A legend mark in the row's gutter, centred on x: track line, anchorage or light, at 0.55."""
    if kind == "track":
        svg, _segs = C.track_lines(x - 4, y - 1, x + 4, y - 11, 3, 3.6, theme, opacity=0.9)
        return svg
    if kind == "anchorage":
        return C.use("anchorage", x, y - 4, NAME, scale=0.7)
    if kind == "light":
        return C.use("light", x, y - 4, NAME, scale=0.7)
    return ""

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



def _desk(ctx) -> str:
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["desk"]
    groups, items = _fittings(cfg)
    repos = _repo_index(data)
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    out: list[str] = []
    defs = _symbols(t, ed.name, ("anchorage", "light"))
    rows = max([sum(1 for i in items if i.get("group") == g[0]) for g in groups] + [6])
    y_top, pitch, y_first = 40, 28, 76
    y_bot = y_first + (rows - 1) * pitch + 20
    # column rules
    for x in (COL_X[1] - 1, COL_X[2] - 1):
        out.append(f'<path d="M{x} {y_top}V{y_bot}" fill="none" {C.stroke("HAIR", t.ink, 0.6, caps="butt")}/>')
    for gi, (code, gloss) in enumerate(groups[:3]):
        cx = COL_X[gi]
        # the group head: the instrument's name and its plain gloss, typed and tracked, above the column
        out.append(tx(f"{code} · {gloss.upper()}", cx + NAME_X, y_first - 24, "machine", fill=t.muted, tracking=1.0))
        col_items = [i for i in items if i.get("group") == code]
        for ri, item in enumerate(col_items):
            y = y_first + ri * pitch
            name = str(item.get("name", ""))
            repo = repos.get(str(item.get("repo", ""))) or repos.get(str(item.get("repo", "")).lower())
            active = bool(repo and repo.get("active"))
            role = "machine-strong" if active else "machine"
            fill = t.ink if active else t.ink2
            out.append(tx(name, cx + NAME_X, y, role, fill=fill, opacity=(0.9 if ed.dark and not active else None)))
            pen = cx + NAME_X + T.text_width(name, role, edition=ed)
            mark = item.get("mark") or MARKS.get(name)
            if mark:
                out.append(_mark(mark, cx + MARK_X, y, t))
            fitted = _my(repo.get("first")) if repo else ""
            fw = T.text_width(fitted, "label", edition=ed) if fitted else 0
            lead_end = cx + DATE_X - fw - 8 if fitted else cx + DATE_X
            if lead_end - (pen + 8) >= 10:
                out.append(f'<path d="M{fmt(pen + 8)} {fmt(y - 1)}H{fmt(lead_end)}" fill="none" '
                           f'{C.stroke("HAIR", t.ink2, 0.9, "TRACK")}/>')
            if fitted:
                out.append(tx(fitted, cx + DATE_X, y, "label", fill=t.muted, anchor="end", truth="measured",
                              key=f"fitted.{name}"))
    # the reading key in the left third (plain words for the recruiter, decision 2)
    n_active = sum(1 for r in (data.get("repos") or []) if r.get("active"))
    out.append(tx(f"bold · carried by a repository underway this quarter ({n_active} of {chart_no})", 48, y_bot - 20, "label",
                  fill=t.muted, truth="measured", key="active_count"))
    out.append(tx("date · first commit of the repository that carries it", 48, y_bot - 2, "label", fill=t.muted))
    out.append(tx(f"CHART NO. {chart_no} · SHEET 5", 24, H_ - 5, "label-caps", fill=t.muted, key="folio"))
    return E.svg(ed, W_, H_, "".join(out), defs + T.glyph_defs(), sheet=NAME)


def _phone(ctx) -> str:
    """A rule and the folio: the stack is in the Markdown line above (T9 §5.6)."""
    ed, t, data = ctx.ed, ctx.ed.theme, ctx.data
    W_, H_ = SIZES["phone"]
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))
    out = [f'<path d="M16 12H704" fill="none" {C.stroke("PEN", t.ink, 0.8, caps="butt")}/>',
           T.text_use(f"CHART NO. {chart_no} · SHEET 5", 704, 40, "label-caps", fill=t.muted, anchor="end",
                      edition=ed, key="folio")]
    return E.svg(ed, W_, H_, "".join(out), T.glyph_defs(), sheet=NAME)


def build(ctx) -> str:
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    groups, items = _fittings(cfg)
    glosses = [g[1].lower() for g in groups[:3]] or ["languages", "stores and queues", "deck"]
    return (f"Instruments carried, {len(items)} fittings in three columns: {', '.join(glosses)}; dated by first commit. "
            f"The daily driver in bold; the rest when asked.")


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
