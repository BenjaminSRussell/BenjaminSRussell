"""typeset.py — the type and lettering engine (T5).

Three faces, three voices: Instrument Serif (the chart-maker), IBM Plex Sans Condensed (the chart),
IBM Plex Mono (the machine). Every string on every sheet goes through a *role* from tokens.ROLES, is
shaped here (ligatures, GPOS kerning, the manual KERN_FIX table, synthetic spaces, tracking between inked
glyphs only) and is written as outlines: inline paths for the big roles, shared `<use>` glyphs for the rest.
Every run is registered in `_RUNS` so `check_type()` can lint sizes, floors, containers and budgets, and so
`exclusions()` can hand the cullers real text boxes.

Public surface (see MASTERPLAN §3.2 and docs/crit/tech/T5-type.md):
    shape, text, text_use, label, runs, sounding, text_on_path, text_width, glyph_defs, begin_asset,
    exclusions, exclude, check_type, check_budget, lint_records, run_records, glyph_count, warnings,
    FONTS, KERN_FIX, HAND_KERN, HAND_LIFT, FIGURES, Glyph, Run.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import tokens  # noqa: E402

FONT_DIR = os.path.join(_HERE, "fonts")

FONTS: dict[str, str] = {
    "serif": f"{FONT_DIR}/InstrumentSerif-Regular.ttf",
    "serif-italic": f"{FONT_DIR}/InstrumentSerif-Italic.ttf",
    "cond": f"{FONT_DIR}/IBMPlexSansCondensed-Regular.ttf",
    "cond-italic": f"{FONT_DIR}/IBMPlexSansCondensed-Italic.ttf",
    "cond-light": f"{FONT_DIR}/IBMPlexSansCondensed-Light.ttf",
    "plex": f"{FONT_DIR}/IBMPlexMono-Regular.ttf",
    "plex-light": f"{FONT_DIR}/IBMPlexMono-Light.ttf",
    "plex-medium": f"{FONT_DIR}/IBMPlexMono-Medium.ttf",
    "plex-italic": f"{FONT_DIR}/IBMPlexMono-Italic.ttf",
}
SERIF_FONTS = {"serif", "serif-italic"}
ITALIC_FONTS = {"serif-italic", "cond-italic", "plex-italic"}

# Manual kerning for pairs the fonts lack, in font units (1000/em). Pairs apply when the two inked glyphs
# are adjacent OR separated by one space-kind glyph (the fitting problem is visual, across the space).
# Instrument Serif's periodcentered has zero/negative sidebearings (adv 103/105, bounds -11..92 / 0..105)
# and the italic r/f/v/w/y overhang their advance, so "developer · scraping" set 123 units left of the dot
# and 166-181 right. Values below bring left and right gaps within 10 units of each other (measured).
KERN_FIX: dict[str, dict[tuple[str, str], float]] = {
    "serif-italic": {
        ("r", "periodcentered"): 40, ("f", "periodcentered"): 134, ("v", "periodcentered"): -10,
        ("w", "periodcentered"): -12, ("y", "periodcentered"): -6, ("t", "periodcentered"): 24,
        # the italic I overhangs its advance; across the narrow word space "I survey" set as "Isurvey"
        # (type designer, re-crit 07): open the space after a capital I before a lowercase
        ("I", "s"): 70, ("I", "a"): 70, ("I", "c"): 70, ("I", "w"): 70, ("I", "h"): 70, ("I", "d"): 70,
        ("I", "k"): 70, ("I", "t"): 70, ("I", "b"): 70, ("I", "m"): 70, ("I", "r"): 70, ("I", "n"): 70,
    },
    "serif": {
        ("r", "periodcentered"): 28, ("f", "periodcentered"): 52, ("v", "periodcentered"): 36,
        ("w", "periodcentered"): 36, ("y", "periodcentered"): 36,
    },
}
# Hand kerning for the one word that matters (role "display" only), by character pair, in font units.
HAND_KERN: dict[str, dict[tuple[str, str], float]] = {
    "display": {("R", "u"): -20, ("s", "s"): 2},
}
# Hand lift: dy in px applied to the SECOND glyph of the pair (the second l of Russell), role "display".
HAND_LIFT: dict[str, dict[tuple[str, str], float]] = {
    "display": {("l", "l"): -1.5},
}
# Synthetic spaces, in em. None of the three families ships U+2009 / U+200A.
SYNTHETIC_SPACES = {0x2009: ("thin", 0.20), 0x200A: ("hair", 0.10)}
SPACE_KINDS = {"space", "thin", "hair", "nbsp"}
TEXTURE_ROLES = {"texture", "texture-italic", "contour-figure"}
INLINE_INTEGER_FROM = 36          # roles >= 36 px are inline paths with integer coordinates
FIGURE_IN_SERIF = 0.86            # runs(): figures inside a serif sentence set in Condensed at this ratio
BUDGET = {"glyph_defs": 160, "size_keys": 6, "defs_kb": 40}
# a sheet with a 28 px serif title AND a legend through shared glyphs needs more defs than a plain
# sheet; inlining the serif instead pushes raw size past 300 KB (builder P, approaches report §5)
BUDGET_BY_SHEET = {"approaches": {"glyph_defs": 200, "defs_kb": 72}, "hero": {"defs_kb": 56}}


def budget_for(sheet: str | None) -> dict:
    b = dict(BUDGET)
    b.update(BUDGET_BY_SHEET.get(sheet or "", {}))
    return b


# ---------------------------------------------------------------- faces

@dataclass
class _Face:
    key: str
    tt: TTFont
    cmap: dict[int, str]
    gs: object
    upm: int
    adv: dict[str, int]
    kern_lookups: list
    liga: dict[str, list[tuple[tuple[str, ...], str]]]
    cap: float            # cap height, units
    xh: float             # x-height, units
    asc: float            # ascender used for bboxes (cap height + a hair), units
    desc: float           # descender, units (positive number)
    _bounds: dict = field(default_factory=dict)
    _kern: dict = field(default_factory=dict)

    def bounds(self, g: str):
        b = self._bounds.get(g)
        if b is None:
            bp = BoundsPen(self.gs)
            try:
                self.gs[g].draw(bp)
                b = bp.bounds or (0, 0, 0, 0)
            except KeyError:
                b = (0, 0, 0, 0)
            self._bounds[g] = b
        return b

    def kern(self, a: str, b: str) -> float:
        k = self._kern.get((a, b))
        if k is None:
            k = _resolve_kern(self.kern_lookups, a, b)
            self._kern[(a, b)] = k
        return k


def _subtables(lookup):
    for st in lookup.SubTable:
        if st.LookupType in (7, 9):        # GSUB / GPOS extension
            st = st.ExtSubTable
        yield st


def _feature_lookups(table, tag: str) -> list:
    """Lookups referenced by `tag`, in order, deduplicated (the features of every script/lang point here)."""
    seen, out = set(), []
    for fr in table.FeatureList.FeatureRecord:
        if fr.FeatureTag != tag:
            continue
        for li in fr.Feature.LookupListIndex:
            if li not in seen:
                seen.add(li)
                out.append(table.LookupList.Lookup[li])
    return out


def _load_kern(tt: TTFont) -> list:
    """Parse GPOS `kern` PairPos subtables into resolvable tables (format 1 explicit, format 2 classes).

    Resolution follows the lookup model: within a lookup the first subtable that covers the pair wins;
    lookups accumulate. This replaces the old `setdefault` flattening that could mis-pair class kerning.
    """
    if "GPOS" not in tt:
        return []
    lookups = []
    for lk in _feature_lookups(tt["GPOS"].table, "kern"):
        subs = []
        for st in _subtables(lk):
            if st.LookupType != 2:
                continue
            cov = set(st.Coverage.glyphs)
            if st.Format == 1:
                pairs = {}
                for i, ps in enumerate(st.PairSet):
                    first = st.Coverage.glyphs[i]
                    for pvr in ps.PairValueRecord:
                        v = pvr.Value1
                        pairs[(first, pvr.SecondGlyph)] = getattr(v, "XAdvance", 0) if v is not None else 0
                subs.append(("f1", cov, pairs))
            else:
                c1 = dict(st.ClassDef1.classDefs) if st.ClassDef1 else {}
                c2 = dict(st.ClassDef2.classDefs) if st.ClassDef2 else {}
                matrix = []
                for cr1 in st.Class1Record:
                    row = []
                    for cr2 in cr1.Class2Record:
                        v = cr2.Value1
                        row.append(getattr(v, "XAdvance", 0) if v is not None else 0)
                    matrix.append(row)
                subs.append(("f2", cov, c1, c2, matrix))
        if subs:
            lookups.append(subs)
    return lookups


def _resolve_kern(lookups, a: str, b: str) -> float:
    total = 0.0
    for subs in lookups:
        for st in subs:
            if a not in st[1]:
                continue
            if st[0] == "f1":
                v = st[2].get((a, b))
                if v is None:
                    continue
                total += v
                break
            c1 = st[2].get(a, 0)
            c2 = st[3].get(b, 0)
            matrix = st[4]
            if c1 < len(matrix) and c2 < len(matrix[c1]):
                total += matrix[c1][c2]
            break
    return total


def _load_liga(tt: TTFont) -> dict:
    """GSUB `liga` LigatureSubst: first glyph -> [(components after the first, ligature)], longest first."""
    out: dict[str, list] = {}
    if "GSUB" not in tt:
        return out
    for lk in _feature_lookups(tt["GSUB"].table, "liga"):
        for st in _subtables(lk):
            if st.LookupType != 4:
                continue
            for first, ligs in st.ligatures.items():
                lst = out.setdefault(first, [])
                for lig in ligs:
                    lst.append((tuple(lig.Component), lig.LigGlyph))
    for first in out:
        out[first].sort(key=lambda t: -len(t[0]))
    return out


_FACES: dict[str, _Face] = {}


def _face(key: str) -> _Face:
    face = _FACES.get(key)
    if face is None:
        if key not in FONTS:
            raise KeyError(f"unknown font key {key!r}; known: {sorted(FONTS)}")
        tt = TTFont(FONTS[key])
        hmtx = tt["hmtx"]
        adv = {g: hmtx[g][0] for g in tt.getGlyphOrder()}
        os2 = tt["OS/2"] if "OS/2" in tt else None
        upm = tt["head"].unitsPerEm
        cap = float(getattr(os2, "sCapHeight", 0) or 0) or 0.72 * upm
        xh = float(getattr(os2, "sxHeight", 0) or 0) or 0.5 * upm
        desc = abs(float(getattr(os2, "sTypoDescender", 0) or 0)) or 0.22 * upm
        face = _Face(key, tt, tt.getBestCmap(), tt.getGlyphSet(), upm, adv,
                     _load_kern(tt), _load_liga(tt), cap, xh, cap * 1.04, desc)
        _FACES[key] = face
    return face


# ---------------------------------------------------------------- shaping

@dataclass
class Glyph:
    name: str          # glyph name in the face ("a", "fi", "uni2080"); "" for a synthetic space
    adv: float         # pen advance after this glyph: own advance (+ tracking when the rule allows)
    dx: float          # kern shift applied before placing (GPOS kern, KERN_FIX, HAND_KERN), same units as adv
    kind: str          # "ink" | "lig" | "space" | "thin" | "hair" | "nbsp" | "missing"
    dy: float = 0.0    # vertical hand adjustment (px), HAND_LIFT
    cp: int | None = None   # codepoint for the <use> id; None for a ligature (its name is used)
    ch: str = ""       # the source character(s)
    tracked: bool = False   # tracking was added after this glyph

    @property
    def inked(self) -> bool:
        return self.kind in ("ink", "lig")


def shape(s: str, font: str, size: float | None = None, tracking: float = 0.0,
          hand: dict | None = None, lift: dict | None = None) -> list[Glyph]:
    """Shape `s` in `font`: liga (greedy longest match from the face's own LigatureSubst), GPOS kern
    (format 1 + format 2 class pairs, lookup-ordered), KERN_FIX manual pairs (also across one space),
    synthetic thin/hair/nbsp advances, HAND_KERN/HAND_LIFT, and tracking between two inked glyphs only.

    With `size` None the values are in font units (and `tracking` is read as units); otherwise px."""
    face = _face(font)
    scale = 1.0 if size is None else size / face.upm
    cmap = face.cmap
    fix = KERN_FIX.get(font, {})
    hand = hand or {}
    lift = lift or {}
    chars = list(s)
    # 1. characters -> glyph names, with synthetic spaces and ligatures
    items: list[Glyph] = []
    i = 0
    n = len(chars)
    space_adv = face.adv.get(cmap.get(0x20, "space"), face.upm * 0.25)
    while i < n:
        ch = chars[i]
        cp = ord(ch)
        if cp in SYNTHETIC_SPACES:
            kind, em = SYNTHETIC_SPACES[cp]
            items.append(Glyph("", em * face.upm * scale, 0.0, kind, cp=cp, ch=ch))
            i += 1
            continue
        if cp == 0xA0:
            items.append(Glyph("", space_adv * scale, 0.0, "nbsp", cp=cp, ch=ch))
            i += 1
            continue
        g = cmap.get(cp)
        if g is None:
            _WARNINGS.append(f"font {font!r} lacks U+{cp:04X} ({ch!r})")
            items.append(Glyph(".notdef", face.adv.get(".notdef", 0) * scale, 0.0, "missing", cp=cp, ch=ch))
            i += 1
            continue
        if ch == " ":
            items.append(Glyph(g, face.adv[g] * scale, 0.0, "space", cp=cp, ch=ch))
            i += 1
            continue
        matched = False
        for comps, lig in face.liga.get(g, ()):
            k = len(comps)
            if i + k < n or i + k == n:
                follow = [cmap.get(ord(c)) for c in chars[i + 1:i + 1 + k]]
                if len(follow) == k and all(a == b for a, b in zip(follow, comps)):
                    items.append(Glyph(lig, face.adv[lig] * scale, 0.0, "lig", cp=None, ch="".join(chars[i:i + 1 + k])))
                    i += 1 + k
                    matched = True
                    break
        if matched:
            continue
        items.append(Glyph(g, face.adv[g] * scale, 0.0, "ink", cp=cp, ch=ch))
        i += 1
    # 2. kerning: GPOS between adjacent glyphs; KERN_FIX across at most one space; hand kern by character
    prev: Glyph | None = None
    last_ink: Glyph | None = None
    spaces_since = 0
    for it in items:
        if it.inked:
            if prev is not None and prev.inked:
                it.dx += face.kern(prev.name, it.name) * scale
                if hand and (prev.ch[-1:], it.ch[:1]) in hand:
                    it.dx += hand[(prev.ch[-1:], it.ch[:1])] * scale
                if lift and (prev.ch[-1:], it.ch[:1]) in lift:
                    it.dy += lift[(prev.ch[-1:], it.ch[:1])] * (1.0 if size is not None else face.upm / 1000)
            if last_ink is not None and spaces_since <= 1 and (last_ink.name, it.name) in fix:
                it.dx += fix[(last_ink.name, it.name)] * scale
            last_ink = it
            spaces_since = 0
        elif it.kind in SPACE_KINDS:
            spaces_since += 1
        else:
            last_ink = None
        prev = it
    # 3. tracking between two inked glyphs only
    if tracking:
        for a, b in zip(items, items[1:]):
            if a.inked and b.inked:
                a.adv += tracking
                a.tracked = True
    return items


def _advance(glyphs: list[Glyph]) -> float:
    return sum(g.adv + g.dx for g in glyphs)


# ---------------------------------------------------------------- editions, roles

def _edition(edition, scale: str | None = None) -> tuple[str, str]:
    """Normalise (edition, scale) to ("day"|"night", "desk"|"phone"). Accepts an edition name
    ("day", "night", "phone-day", "still-night", ...), a tokens.Theme, or T1's Edition object."""
    if edition is None:
        edition = "day"
    if not isinstance(edition, str):
        theme = getattr(edition, "theme", None)
        name = getattr(edition, "name", None) or getattr(edition, "edition", None) or "day"
        if scale is None:
            scale = getattr(edition, "scale", None)
        edition = getattr(theme, "edition", None) or name
    ed = "night" if "night" in edition else "day"
    if scale is None:
        scale = "phone" if "phone" in edition else "desk"
    if scale not in tokens.ROLES:
        raise KeyError(f"unknown scale {scale!r}")
    return ed, scale


def _resolve(role: str, edition, scale, font, size, tracking):
    ed, sc = _edition(edition, scale)
    spec = tokens.ROLES[sc].get(role)
    if spec is None:
        raise KeyError(f"unknown type role {role!r} for scale {sc!r}; roles: {sorted(tokens.ROLES[sc])}")
    f, sz, tr, case, grade = spec
    if font is not None:
        f = font
    if ed == "night":
        f = tokens.NIGHT_LIGHT_CUTS.get(f, f)
    if size is not None:
        sz = size
    if tracking is not None:
        tr = tracking
    g = tokens.GRADE[ed] if grade == "grade" else None
    return ed, sc, f, sz, tr, case, g


def _cased(s: str, case: str) -> str:
    return s.upper() if case == "caps" else s


def _theme(ed: str) -> tokens.Theme:
    return tokens.THEMES[ed]


# ---------------------------------------------------------------- number formatting, glyph defs

def _ntos(v: float) -> str:
    r = round(v, 1)
    return str(int(r)) if r == int(r) else f"{r:.1f}"


def _ntos0(v: float) -> str:
    return str(int(round(v)))


def _ntos2(v: float) -> str:
    r = round(v, 2)
    return str(int(r)) if r == int(r) else f"{r:.2f}".rstrip("0")


def _fmt(v: float, size: float) -> str:
    return _ntos0(v) if size >= INLINE_INTEGER_FROM else _ntos(v)


_GLYPHS: dict[str, str] = {}
_PREFIX = ""
_SHEET = ""


def _szkey(size: float) -> str:
    return _ntos(size).replace(".", "p")


def _glyph_id(font: str, size: float, g: Glyph) -> str:
    tail = str(g.cp) if g.cp is not None else g.name
    return f"{_PREFIX}g-{font}-{_szkey(size)}-{tail}"


def _def(font: str, size: float, g: Glyph) -> str:
    gid = _glyph_id(font, size, g)
    if gid not in _GLYPHS:
        face = _face(font)
        sc = size / face.upm
        sp = SVGPathPen(face.gs, ntos=_ntos0 if size >= INLINE_INTEGER_FROM else _ntos)
        face.gs[g.name].draw(TransformPen(sp, (sc, 0, 0, -sc, 0, 0)))
        _GLYPHS[gid] = sp.getCommands()
    return gid


def glyph_defs() -> str:
    """The shared glyph outlines for this asset's <defs>, ids (prefix)g-{font}-{size}-{codepoint}."""
    return "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in _GLYPHS.items())


def glyph_count() -> int:
    return len(_GLYPHS)


def begin_asset(sheet: str = "", prefix: str = "") -> None:
    """Reset the glyph library, the run registry, exclusions, figures and warnings for a new asset."""
    global _PREFIX, _SHEET
    _PREFIX, _SHEET = prefix, sheet
    _GLYPHS.clear()
    _RUNS.clear()
    _EXCLUDE.clear()
    FIGURES.clear()
    _WARNINGS.clear()


# ---------------------------------------------------------------- run registry

@dataclass
class Run:
    text: str
    role: str
    font: str
    size: float
    x0: float
    x1: float
    y: float
    angle: float
    semantic: bool
    within: tuple | None
    truth: str | None
    key: str | None
    sheet: str
    origin: str = "text"          # "text" | "text_use" | "sounding" | "runs" | "runs-figure" | "path"
    y0: float = 0.0
    y1: float = 0.0
    tracking: float = 0.0
    tracked_spaces: int = 0

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        return (self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)


_RUNS: list[Run] = []
_EXCLUDE: list[tuple[str, float, float, float, float]] = []
_WARNINGS: list[str] = []
FIGURES: list[tuple[str, str | None, str, str]] = []     # (sheet, key, value, style)


def _rot_bbox(x0, y0, x1, y1, cx, cy, deg):
    if not deg:
        return x0, y0, x1, y1
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]
    rx = [cx + (px - cx) * ca - (py - cy) * sa for px, py in pts]
    ry = [cy + (px - cx) * sa + (py - cy) * ca for px, py in pts]
    return min(rx), min(ry), max(rx), max(ry)


def _register(s, role, font, size, x0, x1, y, angle, semantic, within, truth, key, origin, tracking,
              glyphs, y0=None, y1=None, pivot_x=None) -> Run:
    face = _face(font)
    sc = size / face.upm
    if y0 is None:
        y0 = y - face.asc * sc
        y1 = y + face.desc * sc
        # the SVG rotates about the anchor (x, y), not the run's left end (builder S, report §5.2)
        x0r, y0r, x1r, y1r = _rot_bbox(x0, y0, x1, y1, pivot_x if pivot_x is not None else x0, y, angle)
    else:
        x0r, y0r, x1r, y1r = x0, y0, x1, y1
    tracked = sum(1 for a, b in zip(glyphs, glyphs[1:])
                  if a.tracked and (a.kind in SPACE_KINDS or b.kind in SPACE_KINDS))
    run = Run(s, role, font, size, x0r, x1r, y, angle, semantic, within, truth, key, _SHEET, origin,
              y0r, y1r, tracking, tracked)
    _RUNS.append(run)
    if key is not None or truth is not None:
        style = "datum" if truth == "datum" else ("italic" if font in ITALIC_FONTS else "upright")
        FIGURES.append((_SHEET, key, s, style))
    return run


def runs_registry() -> list[Run]:
    return list(_RUNS)


def warnings() -> list[str]:
    return list(_WARNINGS)


def exclude(name: str, x: float, y: float, w: float, h: float) -> None:
    """Register a furniture box (rose, cartouche, inset, legend) the cullers must avoid."""
    _EXCLUDE.append((name, x, y, w, h))


def exclusions(named: bool = False) -> list:
    """Boxes (x, y, w, h) of every text run and every exclude()d piece of furniture."""
    out = [(f"text:{r.text}", *r.bbox) for r in _RUNS] + list(_EXCLUDE)
    return out if named else [b[1:] for b in out]


# ---------------------------------------------------------------- setting

def _anchor_x(x: float, total: float, anchor: str) -> float:
    if anchor == "middle":
        return x - total / 2
    if anchor == "end":
        return x - total
    return x


def _group_open(fill: str, grade, paper: str, opacity, rotate, x, y, extra: str = "") -> str:
    attrs = [f'fill="{fill}"']
    if grade is not None:
        kind, w = grade
        if kind == "spread":
            attrs += [f'stroke="{fill}"', f'stroke-width="{_ntos2(w)}"', 'paint-order="stroke"', 'stroke-linejoin="round"']
        else:
            attrs += [f'stroke="{paper}"', f'stroke-width="{_ntos2(w)}"', 'stroke-linejoin="round"']
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    if rotate:
        attrs.append(f'transform="rotate({_ntos(rotate)} {_ntos(x)} {_ntos(y)})"')
    if extra:
        attrs.append(extra)
    return f'<g {" ".join(attrs)}>'


def _set(s, x, y, role, fill, anchor, within, semantic, truth, key, edition, scale, font, size, tracking,
         opacity, rotate, use: bool, extra: str = "") -> str:
    ed, sc, f, sz, tr, case, grade = _resolve(role, edition, scale, font, size, tracking)
    s = _cased(s, case)
    if role in TEXTURE_ROLES:
        semantic = False
    glyphs = shape(s, f, sz, tr, HAND_KERN.get(role), HAND_LIFT.get(role))
    total = _advance(glyphs)
    x0 = _anchor_x(x, total, anchor)
    theme = _theme(ed)
    fill = fill or theme.ink
    _register(s, role, f, sz, x0, x0 + total, y, rotate, semantic, within, truth, key,
              "text_use" if use else "text", tr, glyphs, pivot_x=x)
    out = [_group_open(fill, grade, theme.paper, opacity, rotate, x, y, extra)]
    pen = x0
    parts = []
    for g in glyphs:
        pen += g.dx
        if g.inked:
            if use:
                gid = _def(f, sz, g)
                parts.append(f'<use href="#{gid}" x="{_fmt(pen, sz)}" y="{_fmt(y + g.dy, sz)}"/>')
            else:
                face = _face(f)
                k = sz / face.upm
                sp = SVGPathPen(face.gs, ntos=_ntos0 if sz >= INLINE_INTEGER_FROM else _ntos)
                face.gs[g.name].draw(TransformPen(sp, (k, 0, 0, -k, pen, y + g.dy)))
                d = sp.getCommands()
                if d:
                    parts.append(d)
        pen += g.adv
    if use:
        out.append("".join(parts))
    elif parts:
        out.append(f'<path d="{" ".join(parts)}"/>')
    out.append("</g>")
    return "".join(out)


def text(s: str, x: float, y: float, role: str = "label", fill: str | None = None, anchor: str = "start",
         within: tuple | None = None, semantic: bool = True, truth: str | None = None, key: str | None = None,
         edition="day", scale: str | None = None, font: str | None = None, size: float | None = None,
         tracking: float | None = None, opacity: float | None = None, rotate: float = 0) -> str:
    """Set `s` as inline outlines in `role`, baseline at (x, y). Returns `<g fill … grade><path d=…/></g>`.

    Roles >= 36 px write integer coordinates, smaller roles one decimal. `within` is a (x, y, w, h) box the
    run must stay inside; `truth`/`key` feed FIGURES for T7; `font`/`size`/`tracking` override the role
    (an off-scale size fails check_type). `edition` may be a name, a Theme or T1's Edition."""
    return _set(s, x, y, role, fill, anchor, within, semantic, truth, key, edition, scale, font, size,
                tracking, opacity, rotate, use=False)


def text_use(s: str, x: float, y: float, role: str = "label", fill: str | None = None, anchor: str = "start",
             within: tuple | None = None, semantic: bool = True, truth: str | None = None, key: str | None = None,
             edition="day", scale: str | None = None, font: str | None = None, size: float | None = None,
             tracking: float | None = None, opacity: float | None = None, rotate: float = 0) -> str:
    """Same as text(), through the shared glyph library: one `<use href x y>` per glyph (typed() relies
    on that), outlines emitted once by glyph_defs() under ids (prefix)g-{font}-{size}-{codepoint}."""
    return _set(s, x, y, role, fill, anchor, within, semantic, truth, key, edition, scale, font, size,
                tracking, opacity, rotate, use=True)


def label(s: str, x: float, y: float, role: str = "label", **kw) -> str:
    """T6's `label_cb(text, x, y, role, **kw)`: text_use for roles <= 28, inline text above."""
    sc = kw.get("scale") or "desk"
    spec = tokens.ROLES.get(sc if sc in tokens.ROLES else "desk", {}).get(role)
    size = kw.get("size") or (spec[1] if spec else 13)
    fn = text if size >= INLINE_INTEGER_FROM else text_use
    return fn(s, x, y, role, **kw)


def text_width(s: str, role: str | None = None, font: str | None = None, size: float | None = None,
               tracking: float | None = None, edition="day", scale: str | None = None) -> float:
    """Advance width in px of `s` in `role` (or an explicit font/size/tracking), with shaping applied."""
    if role is not None:
        ed, sc, f, sz, tr, case, _g = _resolve(role, edition, scale, font, size, tracking)
        s = _cased(s, case)
        return _advance(shape(s, f, sz, tr, HAND_KERN.get(role), HAND_LIFT.get(role)))
    if font is None or size is None:
        raise TypeError("text_width needs a role or font + size")
    return _advance(shape(s, font, size, tracking or 0.0))


def _is_figures(s: str) -> bool:
    t = s.strip()
    return bool(t) and all(c.isdigit() or c in ".,–-%/:₀₁₂₃₄₅₆₇₈₉ " for c in t) and any(c.isdigit() for c in t)


def runs(parts: list[tuple[str, str]], x: float, y: float, edition="day", scale: str | None = None,
         fill: str | None = None, anchor: str = "start", within: tuple | None = None, semantic: bool = True,
         truth: str | None = None, key: str | None = None, opacity: float | None = None) -> str:
    """Mixed roles on one baseline: `[(role, text), ...]`. Figures inside a serif sentence (a part whose role
    is "figures", or a serif part whose text is all figures) are set in Condensed (italic after an italic
    serif part) at 0.86x the serif size, registered origin="runs-figure" (exempt from the scale lint)."""
    ed, sc = _edition(edition, scale)
    resolved = []
    last_serif = None
    for role, s in parts:
        if role == "figures" or (tokens.ROLES[sc].get(role, ("",))[0] in SERIF_FONTS and _is_figures(s)):
            base = last_serif or (role if role != "figures" else None)
            if base is None:
                for r2, _s2 in parts:
                    if tokens.ROLES[sc].get(r2, ("",))[0] in SERIF_FONTS:
                        base = r2
                        break
            if base is None:
                resolved.append((role if role != "figures" else "label", s, None, None, "runs"))
                continue
            bf, bsz, _bt, _bc, _bg = tokens.ROLES[sc][base]
            f = "cond-italic" if bf == "serif-italic" else "cond"
            resolved.append((base, s, f, round(bsz * FIGURE_IN_SERIF, 1), "runs-figure"))
        else:
            if tokens.ROLES[sc].get(role, ("",))[0] in SERIF_FONTS:
                last_serif = role
            resolved.append((role, s, None, None, "runs"))
    widths = []
    for role, s, f, sz, _o in resolved:
        widths.append(text_width(s, role, font=f, size=sz, edition=ed, scale=sc))
    total = sum(widths)
    pen = _anchor_x(x, total, anchor)
    out = []
    for (role, s, f, sz, origin), w in zip(resolved, widths):
        fn = text if (sz or tokens.ROLES[sc][role][1]) >= INLINE_INTEGER_FROM else text_use
        piece = fn(s, pen, y, role, fill=fill, within=within, semantic=semantic, truth=truth, key=key,
                   edition=ed, scale=sc, font=f, size=sz, opacity=opacity)
        _RUNS[-1].origin = origin
        out.append(piece)
        pen += w
    return "".join(out)


_SUBSCRIPT = {str(d): chr(0x2080 + d) for d in range(10)}


def sounding(value, x: float, y: float, sub=None, truth: str = "measured", role: str = "texture",
             anchor: str = "middle", edition="day", scale: str | None = None, fill: str | None = None,
             key: str | None = None, opacity: float | None = None) -> str:
    """A chart sounding: digits upright (measured, datum) or italic (illustrative) in Condensed via the
    glyph library; `sub` set with the encoded subscript digits U+2080-2089 (fallback: 0.6x digits dropped
    0.15 em when a cut lacks them); truth="datum" underlines 0.8 px, 1 px below the baseline. Registers the
    run semantic=False unless role="label", origin="sounding", and appends to FIGURES."""
    if truth not in ("measured", "illustrative", "datum"):
        raise ValueError(f"truth must be measured|illustrative|datum, got {truth!r}")
    ed, sc = _edition(edition, scale)
    italic = truth == "illustrative"
    if role == "label":
        r = "label-italic" if italic else "label"
    elif role in ("texture", "texture-italic"):
        r = "texture-italic" if italic else "texture"
    else:
        r = role
    _ed, _sc, f, sz, tr, _case, _g = _resolve(r, ed, sc, None, None, None)
    face = _face(f)
    val = str(value)
    subs = "".join(_SUBSCRIPT.get(c, c) for c in str(sub)) if sub is not None else ""
    has_subs = all(ord(c) in face.cmap for c in subs) if subs else True
    theme = _theme(ed)
    fill = fill or theme.ink
    semantic = role == "label"
    if has_subs:
        s = val + subs
        out = text_use(s, x, y, r, fill=fill, anchor=anchor, semantic=semantic, truth=truth, key=key,
                       edition=ed, scale=sc, opacity=opacity)
        run = _RUNS[-1]
    else:
        w_main = text_width(val, r, edition=ed, scale=sc)
        sub_sz = round(sz * 0.6, 1)
        w_sub = text_width(str(sub), r, size=sub_sz, edition=ed, scale=sc)
        x0 = _anchor_x(x, w_main + w_sub, anchor)
        out = text_use(val, x0, y, r, fill=fill, semantic=semantic, truth=truth, key=key, edition=ed, scale=sc,
                       opacity=opacity)
        run = _RUNS[-1]
        out += text_use(str(sub), x0 + w_main, y + 0.15 * sz, r, fill=fill, semantic=False, edition=ed,
                        scale=sc, size=sub_sz, opacity=opacity)
        _RUNS[-1].origin = "sounding"
        run.x1 = x0 + w_main + w_sub
        run.text = val + subs
    run.origin = "sounding"
    if truth == "datum":
        yy = y + 1
        out += (f'<path d="M{_ntos(run.x0)} {_ntos(yy)}H{_ntos(run.x1)}" stroke="{fill}" stroke-width=".8" '
                f'fill="none"{f" opacity={chr(34)}{opacity}{chr(34)}" if opacity is not None else ""}/>')
    return out


# ---------------------------------------------------------------- text on a path

def _polyline_metrics(pts):
    segs = []
    cum = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        segs.append(L)
        cum.append(cum[-1] + L)
    return segs, cum


def _point_at(pts, segs, cum, t):
    total = cum[-1]
    t = min(max(t, 0.0), total)
    # find segment
    lo, hi = 0, len(segs) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid + 1] < t:
            lo = mid + 1
        else:
            hi = mid
    i = lo
    L = segs[i] or 1e-9
    u = (t - cum[i]) / L
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]
    tx, ty = (x1 - x0) / L, (y1 - y0) / L
    return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, tx, ty


def text_on_path(s: str, polyline: list[tuple[float, float]], role: str = "sea-name", start: float | None = 0.0,
                 side: str = "above", spread: float | None = None, edition="day", scale: str | None = None,
                 fill: str | None = None, semantic: bool = True, within: tuple | None = None,
                 truth: str | None = None, key: str | None = None, opacity: float | None = None) -> str:
    """Letter `s` along a polyline (T6's contour data), glyph by glyph: each inked glyph sits at its advance
    midpoint on the arc with `<use transform="translate(x y) rotate(a)">`. `start` is the arc fraction where
    the run begins (None = centred); `spread` letterspaces the run to that fraction of the polyline length
    (sea-name 70 %). The polyline is read left to right so names never hang upside down. Guard: if the
    local radius under any glyph is < 3x the size, the run is set straight along the chord and a warning
    is recorded (warnings())."""
    ed, sc, f, sz, tr, case, grade = _resolve(role, edition, scale, None, None, None)
    s = _cased(s, case)
    pts = [(float(px), float(py)) for px, py in polyline]
    pts = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
    if len(pts) < 2:
        raise ValueError("text_on_path needs a polyline of two or more points")
    if pts[-1][0] < pts[0][0]:
        pts = pts[::-1]
    segs, cum = _polyline_metrics(pts)
    total_len = cum[-1]
    glyphs = shape(s, f, sz, tr)
    width = _advance(glyphs)
    # spread: letterspace to a fraction of the polyline; the extra goes into every gap, so a word space
    # widens on both sides and the words stay apart (letterspaced caps on a chart keep their word gaps).
    gaps = len(glyphs) - 1
    if spread is not None and gaps > 0:
        extra = (spread * total_len - width) / gaps
        if extra > 0:
            for g in glyphs[:-1]:
                g.adv += extra
            width = _advance(glyphs)
    if start is None:
        start_len = (total_len - width) / 2
    else:
        start_len = start * total_len
    if start_len + width > total_len:
        _WARNINGS.append(f"text_on_path: {s!r} ({width:.0f} px) overruns the polyline ({total_len:.0f} px)")
        start_len = max(0.0, total_len - width)
    theme = _theme(ed)
    fill = fill or theme.ink
    face = _face(f)
    k = sz / face.upm
    gap = 0.18 * sz
    base_off = gap if side == "above" else -(face.cap * k + gap)
    # radius guard
    min_r = float("inf")
    pen = start_len
    for g in glyphs:
        pen += g.dx
        own = face.adv.get(g.name, 0) * k if g.inked else g.adv
        if g.inked and own > 0:
            _x0, _y0, tx0, ty0 = _point_at(pts, segs, cum, pen)
            _x1, _y1, tx1, ty1 = _point_at(pts, segs, cum, pen + own)
            dth = abs(math.atan2(tx0 * ty1 - ty0 * tx1, tx0 * tx1 + ty0 * ty1))
            if dth > 1e-6:
                min_r = min(min_r, own / dth)
        pen += g.adv
    if min_r < 3 * sz:
        _WARNINGS.append(f"text_on_path: {s!r} bends too tightly (radius {min_r:.0f} < {3 * sz:.0f}); set straight")
        x0, y0, tx, ty = _point_at(pts, segs, cum, start_len)
        x1, y1, _tx, _ty = _point_at(pts, segs, cum, min(total_len, start_len + width))
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        nx, ny = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
        bx, by = x0 + nx * base_off, y0 + ny * base_off
        return text_use(s, bx, by, role, fill=fill, within=within, semantic=semantic, truth=truth, key=key,
                        edition=ed, scale=sc, opacity=opacity, rotate=ang) if sz < INLINE_INTEGER_FROM else \
            text(s, bx, by, role, fill=fill, within=within, semantic=semantic, truth=truth, key=key,
                 edition=ed, scale=sc, opacity=opacity, rotate=ang)
    out = [_group_open(fill, grade, theme.paper, opacity, 0, 0, 0)]
    pen = start_len
    xs, ys, angs = [], [], []
    for g in glyphs:
        pen += g.dx
        if g.inked:
            own = face.adv.get(g.name, 0) * k
            px, py, tx, ty = _point_at(pts, segs, cum, pen + own / 2)
            nx, ny = ty, -tx
            ox = px - tx * own / 2 + nx * base_off
            oy = py - ty * own / 2 + ny * base_off + g.dy
            ang = math.degrees(math.atan2(ty, tx))
            gid = _def(f, sz, g)
            out.append(f'<use href="#{gid}" transform="translate({_fmt(ox, sz)} {_fmt(oy, sz)}) rotate({_ntos(ang)})"/>')
            b = face.bounds(g.name)
            for cx, cy in ((b[0] * k, -b[3] * k), (b[2] * k, -b[3] * k), (b[0] * k, -b[1] * k), (b[2] * k, -b[1] * k)):
                ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                xs.append(ox + cx * ca - cy * sa)
                ys.append(oy + cx * sa + cy * ca)
            angs.append(ang)
        pen += g.adv
    out.append("</g>")
    if xs:
        mean_ang = sum(angs) / len(angs)
        _register(s, role, f, sz, min(xs), max(xs), (min(ys) + max(ys)) / 2, mean_ang, semantic, within, truth,
                  key, "path", tr, glyphs, y0=min(ys), y1=max(ys))
    return "".join(out)


# ---------------------------------------------------------------- lint

def run_records(runs_: list[Run] | None = None) -> list[dict]:
    """The build-report `text[]` entries (T10 §3.5 schema plus origin/semantic/within/tracked_spaces)."""
    out = []
    for r in (runs_ if runs_ is not None else _RUNS):
        tier = "texture" if not r.semantic else ("scan" if (r.font in SERIF_FONTS and r.size >= 22) else "semantic")
        out.append({"s": r.text, "x0": round(r.x0, 1), "x1": round(r.x1, 1), "y": round(r.y, 1),
                    "y0": round(r.y0, 1), "y1": round(r.y1, 1), "size": r.size, "font": r.font,
                    "slant": "italic" if r.font in ITALIC_FONTS else "upright", "role": r.role, "tier": tier,
                    "truth": r.truth, "key": r.key, "rot": round(r.angle, 1), "origin": r.origin,
                    "semantic": r.semantic, "within": list(r.within) if r.within else None,
                    "tracked_spaces": r.tracked_spaces, "tracking": r.tracking})
    return out


def lint_records(records: list[dict], edition="day", scale: str | None = None, sheet: str | None = None) -> list[str]:
    """T5 §2.3 rules over build-report-shaped records. Returns failure strings (empty = pass):
    size off the edition's scale (176 hero only); semantic run under the floor; a texture-floor (11 px)
    run not made by sounding() or the contour-figure role; serif under the serif floor; a run leaving its
    `within` box; a second label-caps run (the chart number, key "chart-number"/"folio", is exempt);
    tracking on a space."""
    ed, sc = _edition(edition, scale)
    allowed = set(tokens.SCALE if sc == "desk" else tokens.SCALE_PHONE)
    floors = tokens.FLOORS[sc]
    errors = []
    caps = 0
    for r in records:
        s, size, font, role = r.get("s", ""), float(r.get("size", 0)), r.get("font", ""), r.get("role", "")
        origin = r.get("origin", "text")
        semantic = bool(r.get("semantic", r.get("tier") != "texture"))
        tag = f"{role} {size:g} px {s!r}"
        on_scale = any(abs(size - a) < 1e-6 for a in allowed)
        if not on_scale and origin != "runs-figure":
            errors.append(f"size off scale: {tag} (scale {sorted(allowed)})")
        if abs(size - 176) < 1e-6 and sheet and sheet != "hero":
            errors.append(f"176 px is hero-only: {tag} on sheet {sheet!r}")
        if semantic and size < floors["semantic"] - 1e-6 and origin != "runs-figure":
            errors.append(f"semantic run below floor {floors['semantic']}: {tag}")
        if abs(size - floors["texture"]) < 1e-6 and origin != "sounding" and role != "contour-figure":
            errors.append(f"{floors['texture']:g} px run not made by sounding(): {tag}")
        if font in SERIF_FONTS and size < floors["serif"] - 1e-6:
            errors.append(f"serif below floor {floors['serif']}: {tag}")
        within = r.get("within")
        if within:
            wx, wy, ww, wh = within
            x0, x1 = float(r.get("x0", 0)), float(r.get("x1", 0))
            y0, y1 = float(r.get("y0", r.get("y", 0) - size)), float(r.get("y1", r.get("y", 0)))
            if x0 < wx - 0.5 or x1 > wx + ww + 0.5 or y0 < wy - 0.5 or y1 > wy + wh + 0.5:
                errors.append(f"run leaves its box {within}: {tag} spans x {x0:.0f}..{x1:.0f} y {y0:.0f}..{y1:.0f}")
        if role == "label-caps" and r.get("key") not in ("chart-number", "folio"):
            caps += 1
        if int(r.get("tracked_spaces", 0) or 0) > 0:
            errors.append(f"tracking on a space: {tag}")
    if caps > 1:
        errors.append(f"{caps} label-caps runs (budget: one per sheet plus the chart number)")
    return errors


def check_type(edition="day", scale: str | None = None, sheet: str | None = None) -> list[str]:
    """Lint every run registered since begin_asset() for `edition`/`scale` (T5 §5.1)."""
    return lint_records(run_records(), edition, scale, sheet if sheet is not None else (_SHEET or None))


def check_budget() -> list[str]:
    """Glyph-library budget per sheet (T5 §2.3): <= 160 defs, <= 6 size keys, <= 40 KB of defs."""
    errors = []
    b = budget_for(_SHEET.split("-", 1)[0] if _SHEET else None)
    n = glyph_count()
    if n > b["glyph_defs"]:
        errors.append(f"{n} glyph defs (budget {b['glyph_defs']})")
    keys = {gid.rsplit("-", 2)[1] for gid in _GLYPHS}
    if len(keys) > b["size_keys"]:
        errors.append(f"{len(keys)} glyph size keys {sorted(keys)} (budget {b['size_keys']})")
    kb = len(glyph_defs().encode()) / 1024
    if kb > b["defs_kb"]:
        errors.append(f"glyph defs {kb:.0f} KB (budget {b['defs_kb']})")
    return errors


__all__ = ["FONTS", "KERN_FIX", "HAND_KERN", "HAND_LIFT", "FIGURES", "Glyph", "Run", "shape", "text", "text_use",
           "label", "runs", "sounding", "text_on_path", "text_width", "glyph_defs", "glyph_count", "begin_asset",
           "exclusions", "exclude", "check_type", "check_budget", "lint_records", "run_records", "runs_registry",
           "warnings"]
