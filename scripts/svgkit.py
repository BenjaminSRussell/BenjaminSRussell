"""Tiny SVG kit for the profile assets.

Text is set as real glyph outlines (Inter / DejaVu Sans Mono via fontTools),
so every asset renders identically on every machine, with no font fallback.
Backgrounds are transparent so the artwork sits on GitHub's own page color.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR_INTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FONT_DIR_MONO = FONT_DIR_INTER

FONTS = {
    "display": f"{FONT_DIR_INTER}/InterDisplay-Bold.otf",
    "display-semi": f"{FONT_DIR_INTER}/InterDisplay-SemiBold.otf",
    "display-medium": f"{FONT_DIR_INTER}/InterDisplay-Medium.otf",
    "text": f"{FONT_DIR_INTER}/Inter-Regular.otf",
    "text-medium": f"{FONT_DIR_INTER}/Inter-Medium.otf",
    "text-semi": f"{FONT_DIR_INTER}/Inter-SemiBold.otf",
    "mono": f"{FONT_DIR_MONO}/DejaVuSansMono.ttf",
    "mono-bold": f"{FONT_DIR_MONO}/DejaVuSansMono-Bold.ttf",
}


@lru_cache(maxsize=None)
def _font(key: str):
    f = TTFont(FONTS[key])
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    upm = f["head"].unitsPerEm
    hmtx = f["hmtx"]
    kern = {}
    # GPOS pair kerning: format 1 (explicit pairs) and format 2 (class pairs).
    try:
        gpos = f["GPOS"].table
        for lookup in gpos.LookupList.Lookup:
            for st in lookup.SubTable:
                if st.LookupType == 9:  # extension
                    st = st.ExtSubTable
                if st.LookupType != 2:
                    continue
                if st.Format == 1:
                    first = st.Coverage.glyphs
                    for i, ps in enumerate(st.PairSet):
                        for pvr in ps.PairValueRecord:
                            v = pvr.Value1
                            if v is not None and getattr(v, "XAdvance", 0):
                                kern.setdefault((first[i], pvr.SecondGlyph), v.XAdvance)
                elif st.Format == 2:
                    c1 = st.ClassDef1.classDefs
                    c2 = st.ClassDef2.classDefs
                    cov = set(st.Coverage.glyphs)
                    by1 = {}
                    for g in cov:
                        by1.setdefault(c1.get(g, 0), []).append(g)
                    by2 = {}
                    for g, c in c2.items():
                        by2.setdefault(c, []).append(g)
                    for i, cr1 in enumerate(st.Class1Record):
                        for j, cr2 in enumerate(cr1.Class2Record):
                            v = cr2.Value1
                            adv = getattr(v, "XAdvance", 0) if v is not None else 0
                            if not adv or j == 0:
                                continue
                            for a in by1.get(i, []):
                                for b in by2.get(j, []):
                                    kern.setdefault((a, b), adv)
    except Exception as exc:  # pragma: no cover
        print("kern load failed:", exc)
    return f, cmap, gs, upm, hmtx, kern


def text_width(s: str, font: str, size: float, tracking: float = 0.0) -> float:
    f, cmap, gs, upm, hmtx, kern = _font(font)
    scale = size / upm
    w = 0.0
    prev = None
    for ch in s:
        g = cmap.get(ord(ch), ".notdef")
        if prev is not None:
            w += kern.get((prev, g), 0) * scale
        w += hmtx[g][0] * scale + tracking
        prev = g
    return w - tracking if s else 0.0


# Every text run records its horizontal extent so builders can assert nothing
# leaves the canvas or the 48 px margin. Reset with begin_asset(), read with
# check_bounds().
_EXTENTS: list[tuple[str, float, float, float]] = []


def begin_asset() -> None:
    _EXTENTS.clear()


def check_bounds(w: float, margin: float = 24.0) -> list[str]:
    """Return human-readable warnings for text that crosses the safe area."""
    out = []
    for s, x0, x1, y in _EXTENTS:
        if x0 < margin or x1 > w - margin:
            out.append(f"  text {s!r} spans x={x0:.0f}..{x1:.0f} at y={y:.0f} (safe {margin:.0f}..{w-margin:.0f})")
    return out


def text(s: str, x: float, y: float, font: str = "text", size: float = 16, fill: str = "#000",
         anchor: str = "start", tracking: float = 0.0, opacity: float | None = None, extra: str = "") -> str:
    """Return a <path> for the string, baseline at (x, y)."""
    f, cmap, gs, upm, hmtx, kern = _font(font)
    scale = size / upm
    total = text_width(s, font, size, tracking)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    _EXTENTS.append((s, x, x + total, y))
    d_parts = []
    pen_x = x
    prev = None
    for ch in s:
        g = cmap.get(ord(ch), ".notdef")
        if prev is not None:
            pen_x += kern.get((prev, g), 0) * scale
        if ch != " ":
            sp = SVGPathPen(gs)
            tp = TransformPen(sp, (scale, 0, 0, -scale, pen_x, y))
            gs[g].draw(tp)
            d = sp.getCommands()
            if d:
                d_parts.append(d)
        pen_x += hmtx[g][0] * scale + tracking
        prev = g
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<path d="{" ".join(d_parts)}" fill="{fill}"{op}{(" " + extra) if extra else ""}/>'


@dataclass(frozen=True)
class Theme:
    name: str
    ink: str        # primary text
    ink2: str       # secondary text
    muted: str      # tertiary / captions
    hair: str       # hairlines
    grid: str       # dot grid
    panel: str      # card fill
    panel2: str     # deeper panel (terminal body)
    accent: str     # signal orange
    accent_soft: str
    ok: str         # mint for "clean / ok"
    cool: str       # cool blue for "web / fetch"
    field: str      # page background (for occasional solid fills only)
    line: str       # diagram strokes (a step stronger than hair)
    soft: str       # quiet filled shapes that still need to be seen


DARK = Theme(
    name="dark",
    ink="#F3EFE7", ink2="#B9BCC6", muted="#7D8290", hair="#2A2F3A", grid="#1F232C",
    panel="#13161C", panel2="#0E1014", accent="#FF5A1F", accent_soft="#FF8A5B",
    ok="#4ADE9B", cool="#6FB7FF", field="#0D1117", line="#3A4150", soft="#4B5160",
)
LIGHT = Theme(
    name="light",
    ink="#131417", ink2="#454A55", muted="#7A7F8C", hair="#DCDFE5", grid="#E6E8EC",
    panel="#F6F7F9", panel2="#FBFBFC", accent="#E8501A", accent_soft="#FF7A45",
    ok="#15A86D", cool="#2E86E6", field="#FFFFFF", line="#C4C9D2", soft="#C3C7CF",
)
THEMES = [DARK, LIGHT]


def svg(w: int, h: int, body: str, label: str, defs: str = "") -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<!-- benjaminsrussell/profile v7 · generated by scripts/build_assets.py · do not edit by hand -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{label}">\n'
        f'{("<defs>" + defs + "</defs>") if defs else ""}'
        f'{body}\n</svg>\n'
    )


def dot_grid(t: Theme, x: float, y: float, w: float, h: float, step: int = 24, r: float = 1.1,
             opacity: float = 1.0, gid: str = "dots") -> tuple[str, str]:
    """Return (defs, body) for a soft dot grid, masked with a radial fade."""
    defs = (
        f'<pattern id="{gid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{step/2}" cy="{step/2}" r="{r}" fill="{t.grid}"/></pattern>'
        f'<radialGradient id="{gid}-fade" cx="50%" cy="50%" r="60%">'
        f'<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        f'</radialGradient><mask id="{gid}-mask"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid}-fade)"/></mask>'
    )
    body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})" mask="url(#{gid}-mask)" opacity="{opacity}"/>'
    return defs, body


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"wrote {path} ({len(content.encode()) // 1024} KB)")
