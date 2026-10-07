"""footer — Sheet 6: Limit of survey (T9 §2D, MASTERPLAN §2.1).

The water leaves the sheet through a break in the neat line. The sloop is under way at t = 0,
arrives 40–64 s, levels, luffs the main once and anchors short of the limit line in good holding;
beyond the line the ground is hatched UNSURVEYED. The only ambient sheet: a 10 s swell, the hull
riding it, three mist arcs at the fall; and once every 96 s (first at 84 s, when the boat is
anchored to witness it) a serpent rises head-first where "Obstn rep. 2026 (PA)" is charted,
holds, sinks, and leaves three ripples. An index of adjoining sheets shows the hero's extent as
the one surveyed cell. Still = anchored state. Eleven indefinite animations, ≤ 4 ms/frame.
"""
from __future__ import annotations

import re
import sys

import chartlib as C
import edition as E
import typeset as T
from edition import fmt

try:
    import timeline as TL
except ImportError:  # pragma: no cover
    TL = None

NAME = "footer"
KIND = "edge"
SIZES = {"desk": (1280, 270), "phone": (720, 320)}
BREAKS: list[tuple[str, str, str]] = [
    ("Broken neat line", "the right rule stops where the water falls off the sheet", "the chart ends here (16, 27)"),
    ("Ambient motion", "swell, hull, mist and a 96 s serpent loop continuously", "the one ambient sheet, ≤ 4 ms/frame (12, decision 10)"),
    ("Illustrative soundings", "six italic depths thinning toward the limit", "texture, not data: italic by the Sheet 3 convention"),
    ("The sloop is drawn, not <use>d", "hull, main, jib from chartlib.SLOOP_DETAIL", "the main must luff on its own; the anchor is the sheet's <use> symbol"),
    ("Inline lettering on the desk editions", "typeset.text(), one <path> per run, no glyph library",
     "the only sheet that repaints every frame: 3.3 ms/frame instead of 4.2 (12's 4 ms budget), +20 KB raw"),
]

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
HY = 150            # the water surface
WX0 = 264           # the water starts right of the margin notes (prose, index)
EDGE = 1040         # where the water leaves the sheet
LIMIT_X = 1000      # the limit of survey
ARRIVE = (40.0, 24.0)
ANCHOR_X, START_X = 950, 330     # under way at 330 (clear of the index); anchors 50 px short of the limit line
SERPENT_AT = 84.0
RIPPLE_AT = 86.5


def _dmy(iso: str) -> str:
    y, m, d = iso[:10].split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def _copy(cfg, key: str, default: str) -> str:
    return str((cfg.get("copy") or {}).get(key) or default)


def _loop(tl, kind_or_attr: str, segs, begin: float, period: float, still, base):
    """(animation, base value): the element's static value is `base` while moving, `still` when frozen."""
    a = tl.every(kind_or_attr, segs, begin, period=period, still=still)
    return a, (base if tl.motion else still)


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


def _wave_y(x: float, x0: float, hy: float) -> float:
    """y of the swell `q24 -5 48 0` wave (period 48 from x0) at x, at phase 0."""
    k = (x - x0) // 48
    u = (x - (x0 + 48 * k)) / 48
    return hy + 9 - 10 * u * (1 - u)


def _shelf(x0: float, hy: float, xa: float, xb: float, edge: float, bottom: float, theme) -> str:
    """The shallows: tint A from xa to xb, tint B from xb over the lip to `bottom`, topped by the swell."""
    def top(a, b):
        pts = [(x, _wave_y(x, x0, hy)) for x in range(int(a), int(b), 4)] + [(b, _wave_y(b, x0, hy))]
        return "".join(f"L{fmt(x)} {fmt(y)}" for x, y in pts[1:]), pts[0]
    ta, pa = top(xa, xb)
    tb, pb = top(xb, edge)
    a = f'<path d="M{fmt(pa[0])} {fmt(pa[1])}{ta}V{fmt(bottom)}H{fmt(xa)}Z" fill="{theme.shallow_a}"/>'
    b = f'<path d="M{fmt(pb[0])} {fmt(pb[1])}{tb}c10 0 16 4 19 12c3 8 4 24 4 42V{fmt(bottom)}H{fmt(xb)}Z" fill="{theme.shallow_b}"/>'
    return a + b


def _sloop_parts(theme, tl, luff_at: float | None, scale: float = 1.0) -> str:
    """31's sloop from chartlib's own paths, the main sail wrapped so it can luff once about the mast."""
    P = C.SLOOP_DETAIL
    hull = f'<path d="{P["hull"]}" fill="{theme.ink}"/>'
    jib = f'<path d="{P["jib"]}" fill="{theme.paper}" {C.stroke("PEN", theme.ink)}/>'
    rig = f'<path d="{P["mast"]}{P["tiller"]}" fill="none" {C.stroke("PEN", theme.ink)}/>'
    dot = f'<circle r="1.2" fill="{theme.ink}"/>'
    main = f'<path d="{P["main"]}" fill="{theme.accent}"/>'
    if luff_at is not None:
        luff = tl.xform("scale", ["1 1", "0.6 1", "1 1"], 0.8, luff_at, ease=["draw", "settle"], key_times=[0, 0.5, 1])
        main = f'<g transform="translate(3 0)"><g>{luff}<g transform="translate(-3 0)">{main}</g></g></g>'
    inner = hull + main + jib + rig + dot
    return f'<g transform="scale({fmt(scale)})">{inner}</g>' if scale != 1.0 else inner


def _serpent(theme, tl) -> str:
    """chartlib.serpent with each part rising head-first (humps +0.25 / +0.5 s), 96 s period."""
    sp = C.serpent(theme)
    tags = re.findall(r'(<(?:path|circle) class="([\w-]+)"[^>]*/>)', sp)
    by = {cls: tag for tag, cls in tags}
    groups = (("head", by.get("head", "") + by.get("eye", ""), 0.0), ("hump-2", by.get("hump-2", ""), 0.25),
              ("hump-1", by.get("hump-1", ""), 0.5))
    out = ['<g class="serpent" fill="none">']
    for _name, inner, delay in groups:
        inner = inner.replace("stroke-linejoin=", 'stroke-opacity=".7" stroke-linejoin=').replace('<circle class="eye"', '<circle fill-opacity=".7" class="eye"')
        segs = ([(0, "0 40")] if delay else []) + [(delay, "0 40", "settle"), (delay + 0.9, "0 0"),
                                                   (delay + 1.5, "0 0", "draw"), (delay + 2.4, "0 40")]
        a, base = _loop(tl, "translate", segs, SERPENT_AT, 96.0, "0 40", "0 40")
        out.append(f'<g transform="translate({base})">{a}{inner}</g>')
    out.append("</g>")
    return "".join(out)


def _desk(ctx) -> str:
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["desk"]
    tl = ctx.tl if ed.motion else (TL.NullTimeline(NAME, ambient=True) if TL else ctx.tl)
    seed = (cfg.get("chart") or {}).get("seed", 27)
    jit = C.Jitter(seed, "footer")
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))
    n_notices = len(data.get("notices") or [])
    taken = str(data.get("taken") or data.get("updated_at") or "")
    dark = ed.dark

    def tx(s, x, y, role="label", **kw):
        # the sheet repaints 57 times a second: inline outlines (one <path> per run) raster ~40 % cheaper
        # per glyph than a <use> each, at the price of ~20 KB raw (measured: 4.24 → 3.3 ms/frame)
        return T.text(s, x, y, role, edition=ed, **kw)

    defs = [_symbols(t, ed.name, ("anchorage",)),
            f'<clipPath id="sea"><rect x="0" y="0" width="{W_}" height="{HY}"/></clipPath>',
            f'<clipPath id="swell"><rect x="{WX0}" y="{HY - 12}" width="{EDGE - WX0}" height="30"/></clipPath>']
    out: list[str] = []

    # ---- index of sheets (27): the page's six sheets, this one filled
    IX, IY, IW, IH = 48, 166, 200, 60
    out.append(tx("INDEX OF SHEETS", IX, IY + IH + 11, "label", fill=t.muted))
    out.append(f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" fill="{t.paper}" {C.stroke("PEN", t.ink, 0.8, caps="butt")}/>')
    cw, ch = IW / 3, IH / 2
    out.append(f'<rect x="{fmt(IX + 2 * cw)}" y="{fmt(IY + ch)}" width="{fmt(cw)}" height="{fmt(ch)}" fill="{t.land}"/>')
    grid = "".join(f"M{fmt(IX + k * cw)} {IY}v{IH}" for k in (1, 2)) + f"M{IX} {fmt(IY + ch)}h{IW}"
    out.append(f'<path d="{grid}" fill="none" {C.stroke("HAIR", t.ink, 0.5, caps="butt")}/>')
    for k in range(6):
        c, r = k % 3, k // 3
        this = (k == 5)
        out.append(tx(str(k + 1), IX + (c + 0.5) * cw, IY + (r + 0.5) * ch + 4.5, "label", fill=t.ink if this else t.muted,
                      anchor="middle"))
    T.exclude("index", IX, IY, IW, IH)

    # ---- unsurveyed ground beyond the limit: land under hand-ruled hatch
    for i, rect in enumerate(((LIMIT_X, 30, 266, 120), (1120, HY, 146, 76))):
        x, y, w, h = rect
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t.land}"/>')
        hd, hb = C.hatch(rect, t, jit.sub(f"hatch{i}"), "unsurveyed", clip_id=f"unsurv{i}")
        defs.append(hd)
        out.append(hb)
    out.append(tx("UNSURVEYED", 1130, 72, "label", fill=t.ink2))

    # ---- the water: deep water is paper; tint marks the shallows at the edge the chart falls off —
    # tint A (under 10) a 24 px fringe inboard, tint B (under 5) the 40 px shelf before the lip, both topped
    # by the swell's wave; the limit line falls on the A/B boundary. Then the surface line, swell (10 s,
    # clipped), the lip, fall lines
    out.append(_shelf(WX0, HY, LIMIT_X - 24, LIMIT_X, EDGE, 226, t))
    out.append(f'<path d="M{WX0} {HY}H{EDGE}" fill="none" {C.stroke("PEN", t.ink, 0.9 if dark else None, caps="butt")}/>')
    waves = "".join("q24 -5 48 0" for _ in range((EDGE - WX0) // 48 + 2))
    a, base = _loop(tl, "translate", [(0, "0 0", "sea"), (10, "-48 0")], 0.0, 10.0, "0 0", "0 0")
    out.append(f'<g clip-path="url(#swell)"><path d="M{WX0} {HY + 9}{waves}" fill="none" transform="translate({base})" '
               f'{C.stroke("HAIR", t.ink, 0.45)}>{a}</path></g>')
    out.append(f'<path d="M{EDGE} {HY}c10 0 16 4 19 12c3 8 4 24 4 42" fill="none" {C.stroke("BRUSH", t.ink, 0.9)}/>')
    falls = f"M1046 {HY + 14}L1044 226M1053 {HY + 16}L1055 226M1060 {HY + 20}L1066 226"
    out.append(f'<path d="{falls}" fill="none" {C.stroke("HAIR", t.ink, 0.6, "TRACK")}/>')
    # mist at the fall: three arcs fading on the 10 s grid, drifting up together
    a, base = _loop(tl, "translate", [(0, "0 0", "linear"), (10, "0 -8")], 0.0, 10.0, "0 0", "0 0")
    mist = [f'<g transform="translate({base})">{a}']
    for (mx, my), begin in zip(((1056, 226), (1066, 228), (1076, 224)), (0.0, 3.5, 7.0)):
        fa, fbase = _loop(tl, "opacity", [(0, 0.5, "linear"), (1.6, 0), (10, 0)], begin, 10.0, 0, 0)
        mist.append(f'<path d="M0 0q6 -10 14 -6" transform="translate({mx} {my})" opacity="{fbase}" fill="none" '
                    f'{C.stroke("HAIR", t.ink, 0.9)}>{fa}</path>')
    mist.append("</g>")
    out.append("".join(mist))

    # ---- six illustrative soundings thinning toward the limit (italic: texture, not data)
    for x, y, v in ((700, 212, 9), (760, 190, 8), (818, 216, 7), (872, 196, 5), (924, 206, 4), (966, 188, 3)):
        out.append(T.sounding(v, x, y, truth="illustrative", edition=ed, fill=t.ink2))
    # the chart note sits above the serpent's rise (head to y≈114) and clear of the anchored sloop's rig
    out.append(tx("Obstn rep. 2026 (PA)", ANCHOR_X - 24, 106, "label-italic", fill=t.muted, anchor="end", opacity=0.7))

    # ---- ripples where the serpent sinks (three rings growing and fading over 20 s)
    ra, rbase = _loop(tl, "scale", [(0, "0.1 0.25", "settle"), (20, "1 1")], RIPPLE_AT, 96.0, "1 1", "0.1 0.25")
    oa, obase = _loop(tl, "opacity", [(0, 0.5, "settle"), (20, 0)], RIPPLE_AT, 96.0, 0, 0)
    rings = "".join(f'<ellipse rx="{rx}" ry="{ry}" fill="none" {C.stroke("HAIR", t.ink)}/>' for rx, ry in ((60, 6), (44, 4.5), (28, 3)))
    out.append(f'<g transform="translate(900 {HY})" opacity="{obase}">{oa}<g transform="scale({rbase})">{ra}{rings}</g></g>')

    # ---- the serpent, clipped by the surface, between swell and hull in z
    out.append(f'<g clip-path="url(#sea)"><g transform="translate(880 {HY})">{_serpent(t, tl)}</g></g>')

    # ---- the sloop: under way at 90, arrives 40–64 s, levels, luffs, anchors
    sail = tl.sail(f"M{START_X} {HY - 1}L{ANCHOR_X} {HY - 1}", ARRIVE[0], ARRIVE[1], n=64, ease="settle", mast_x=3.0,
                   pitch=-4.0, pitch_settle=0.65, name="arrive")
    ba, bbase = _loop(tl, "translate", [(0, "0 0", "sea"), (5, "0 -2", "sea"), (10, "0 0")], 0.0, 10.0, "0 0", "0 0")
    parts = _sloop_parts(t, tl, luff_at=sail.end if tl.motion else None)
    out.append(sail.wrap(f'<g transform="translate({bbase})">{ba}{parts}</g>', pitch=-4.0, mirror=False))
    T.exclude("boat", ANCHOR_X - 18, HY - 41, 37, 46)
    rode = (f'<path d="M{ANCHOR_X + 18} {HY - 3}L{ANCHOR_X + 26} 224" fill="none" {C.stroke("HAIR", t.ink, 0.8, "APPROX")}/>'
            + C.use("anchorage", ANCHOR_X + 26, 220, NAME, scale=0.8)
            + tx("14 · good holding", ANCHOR_X - 2, 236, "label-italic", fill=t.ink2, anchor="end"))
    out.append(tl.fade_in(f"<g>{rode}</g>", sail.end, dur=0.65, rise=0))

    # ---- the limit of survey
    out.append(f'<path d="M{LIMIT_X} 30V226" fill="none" {C.stroke("PEN", t.ink, 0.85 if dark else None, "LIMIT")}/>')
    out.append(tx(_copy(cfg, "limit_label", "LIMIT OF SURVEY 2026"), LIMIT_X - 8, 226, "label-caps", fill=t.ink, rotate=-90))

    # ---- neat line, broken where the water leaves; the one line of prose
    out.append(f'<path d="M14 14H1266V112M1266 226V240H14V14" fill="none" {C.stroke("PEN", t.ink, 0.8, caps="butt")}/>')
    # role thesis at 28 (on the scale, serif floor met) carries no grade stroke; inline like every other run
    # here (through the glyph library the sheet is 9 KB lighter but 3.95 instead of 3.55 ms/frame: measured)
    out.append(tx(_copy(cfg, "footer_line", "The chart ends here. The web doesn't."), 48, 78, "thesis", fill=t.ink, size=28))

    # ---- outside the neat line: folio, the chart's own record, no adjoining sheet
    out.append(tx(f"CHART NO. {chart_no} · SHEET 6", 24, H_ - 5, "label-caps", fill=t.muted, key="folio"))
    # the chart's record, right of the folio: notices and any contact set in chart.toml (the taken date
    # is on the soundings dateline, T9 §5.9); every glyph here repaints 57 times a second
    record = [f"{n_notices} notices · corrected through Notice {n_notices}"] if n_notices else []
    contact = cfg.get("contact") or {}
    for key in ("linkedin", "resume"):
        v = str(contact.get(key) or "").strip()
        if v:
            record.append(re.sub(r"^https?://(www\.)?", "", v).rstrip("/"))
    if record:
        out.append(tx(" · ".join(record), 1264, H_ - 5, "label", fill=t.muted, anchor="end", truth="measured", key="record"))
    return E.svg(ed, W_, H_, "".join(out), "".join(defs) + T.glyph_defs(), sheet=NAME)


def _phone(ctx) -> str:
    """Static end state, redrawn at the phone scale: the anchored boat, the limit, the fall."""
    ed, t, data, cfg = ctx.ed, ctx.ed.theme, ctx.data, ctx.cfg
    W_, H_ = SIZES["phone"]
    tl = TL.NullTimeline(NAME, ambient=True) if TL else ctx.tl
    seed = (cfg.get("chart") or {}).get("seed", 27)
    jit = C.Jitter(seed, "footer-phone")
    chart_no = int(data.get("repo_count") or len(data.get("repos") or []))
    n_notices = len(data.get("notices") or [])
    taken = str(data.get("taken") or data.get("updated_at") or "")
    HYP, LIM, EDG, BX = 200, 560, 600, 548

    def tx(s, x, y, role="label", **kw):
        return T.text_use(s, x, y, role, edition=ed, **kw)

    ink2 = t.ink if ed.dark else t.ink2      # phone night: semantic text in full ink (10)
    defs = [_symbols(t, ed.name, ("anchorage",))]
    out: list[str] = []
    for i, rect in enumerate(((LIM, 60, 144, 128), (640, HYP, 64, 78))):
        x, y, w, h = rect
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t.land}"/>')
        hd, hb = C.hatch(rect, t, jit.sub(f"hatch{i}"), "unsurveyed", clip_id=f"unsurv{i}")
        defs.append(hd)
        out.append(hb)
    uw = T.text_width("UNSURVEYED", "label", edition=ed)
    out.append(tx("UNSURVEYED", 686, 124 + uw / 2, "label", fill=ink2, rotate=-90))
    out.append(_shelf(16, HYP, LIM - 24, LIM, EDG, 278, t))
    out.append(f'<path d="M16 {HYP}H{EDG}" fill="none" {C.stroke("LINE", t.ink, caps="butt")}/>')
    waves = "".join("q24 -5 48 0" for _ in range((EDG - 16) // 48))
    out.append(f'<path d="M16 {HYP + 9}{waves}" fill="none" {C.stroke("HAIR", t.ink, 0.45)}/>')
    out.append(f'<path d="M{EDG} {HYP}c10 0 16 4 19 12c3 8 4 24 4 42" fill="none" {C.stroke("BRUSH", t.ink, 0.9)}/>')
    out.append(f'<path d="M606 {HYP + 14}L604 278M613 {HYP + 16}L615 278M620 {HYP + 20}L626 278" fill="none" '
               f'{C.stroke("HAIR", t.ink, 0.6, "TRACK")}/>')
    for x, y, v in ((380, 240, 7), (452, 250, 5), (512, 236, 3)):
        out.append(T.sounding(v, x, y, truth="illustrative", edition=ed, fill=ink2))
    out.append(f'<g transform="translate({BX} {HYP - 1})">{_sloop_parts(t, tl, None, scale=1.4)}</g>')
    out.append(f'<path d="M{BX + 25} {HYP - 4}L{BX + 32} 270" fill="none" {C.stroke("HAIR", t.ink, 0.8, "APPROX")}/>')
    out.append(C.use("anchorage", BX + 32, 266, NAME, scale=1.1))
    out.append(tx("14 · good holding", 540, 278, "label-italic", fill=ink2, anchor="end"))
    out.append(f'<path d="M{LIM} 60V278" fill="none" {C.stroke("PEN", t.ink, 0.85 if ed.dark else None, "LIMIT")}/>')
    out.append(tx(_copy(cfg, "limit_label", "LIMIT OF SURVEY 2026"), 704, 50, "label-caps", fill=t.ink, anchor="end"))
    # neat line broken at the fall; its foot at 284 so the folio row (baseline 314) sits clear below it
    out.append(f'<path d="M10 10H710V150M710 278V284H10V10" fill="none" {C.stroke("PEN", t.ink, 0.8, caps="butt")}/>')
    line = _copy(cfg, "footer_line", "The chart ends here. The web doesn't.")
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", line) if p.strip()]
    if len(parts) == 1:
        parts = [line]
    for i, p in enumerate(parts[:2]):
        out.append(tx(p, 24, 72 + 46 * i, "thesis", fill=t.ink))
    out.append(tx(f"CHART NO. {chart_no} · SHEET 6", 16, H_ - 6, "label-caps", fill=t.muted, key="folio"))
    # the record inside the frame, under the prose and above the water (10: nothing sits across the neat line)
    rec = f"corrected through Notice {n_notices}" if n_notices else ""
    if rec:
        out.append(tx(rec, 24, 162, "label", fill=t.muted, truth="measured", key="record"))
    return E.svg(ed, W_, H_, "".join(out), "".join(defs) + T.glyph_defs(), sheet=NAME)


def build(ctx) -> str:
    return _phone(ctx) if ctx.ed.phone else _desk(ctx)


def alt(data, cfg) -> str:
    n = int(data.get("repo_count") or len(data.get("repos") or []))
    return (f"Limit of survey: hatched ground beyond a dotted line, a sailboat anchored at it, {n} repositories charted. "
            f"The chart ends here; the web doesn't.")


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
