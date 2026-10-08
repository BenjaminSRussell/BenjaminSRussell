"""edition.py — the Edition record, the SVG envelope and the per-sheet id prefix.

One sheet module builds one body string; this module wraps it:

    from edition import EDITIONS, svg, write, I, fmt
    doc = svg(ctx.ed, w, h, body, defs, sheet=NAME)

`svg()` prefixes every id in body+defs with ``f"{sheet}-"`` (so six inlined sheets never
collide on one page), writes an honest header comment, and lays an opaque paper rect under
the body in both editions. Coordinates that reach the sheet should pass through `I()` /
`fmt()` so two builds from one stats.json are byte-identical.

Stats sha: the header carries the placeholder ``@STATS_SHA@``; `build_assets.py` replaces it
with the sha256 prefix of the stats.json it drew from. A sheet built outside the runner keeps
the placeholder, which is itself honest.
"""
from __future__ import annotations

import gzip
import hashlib
import math
import os
import re
from dataclasses import dataclass, replace
from typing import Literal

import tokens
from tokens import Theme

RELEASE = "v9"
BUILDER = "scripts/build_assets.py"
STATS_SHA_PLACEHOLDER = "@STATS_SHA@"

DESK_W = 1280
PHONE_W = 720


@dataclass(frozen=True)
class Edition:
    name: str                         # "day" | "night" | "still-day" | ... | "phone-still-night"
    theme: Theme
    motion: bool                      # False → every helper returns its end state
    scale: Literal["desk", "phone"]
    width: int                        # 1280 desk, 720 phone

    @property
    def dark(self) -> bool:
        return self.theme.edition == "night"

    @property
    def still(self) -> bool:
        return not self.motion

    @property
    def phone(self) -> bool:
        return self.scale == "phone"

    @property
    def form(self) -> str:
        """The build-report `form` field: desk | phone | still."""
        if self.phone:
            return "phone"
        return "still" if self.still else "desk"

    def as_still(self) -> "Edition":
        return replace(self, motion=False)


def _ed(name: str, theme: str, motion: bool, scale: str) -> Edition:
    return Edition(name=name, theme=tokens.THEMES[theme], motion=motion, scale=scale,
                   width=PHONE_W if scale == "phone" else DESK_W)


# The six every sheet ships (MASTERPLAN decision 9) ...
EDITION_NAMES: tuple[str, ...] = ("day", "night", "still-day", "still-night", "phone-day", "phone-night")
# ... plus the two the hero adds (a reduced-motion phone reader is owed a still).
HERO_EXTRA: tuple[str, ...] = ("phone-still-day", "phone-still-night")

EDITIONS: dict[str, Edition] = {
    "day": _ed("day", "day", True, "desk"),
    "night": _ed("night", "night", True, "desk"),
    "still-day": _ed("still-day", "day", False, "desk"),
    "still-night": _ed("still-night", "night", False, "desk"),
    "phone-day": _ed("phone-day", "day", True, "phone"),
    "phone-night": _ed("phone-night", "night", True, "phone"),
    "phone-still-day": _ed("phone-still-day", "day", False, "phone"),
    "phone-still-night": _ed("phone-still-night", "night", False, "phone"),
}


def edition(name: str) -> Edition:
    try:
        return EDITIONS[name]
    except KeyError:
        raise KeyError(f"unknown edition {name!r}; known: {', '.join(EDITIONS)}") from None


def file_name(sheet: str, ed: Edition | str) -> str:
    """`<sheet>-<edition>.svg`; hero + phone-still-day → hero-phone-still-day.svg."""
    name = ed if isinstance(ed, str) else ed.name
    return f"{sheet}-{name}.svg"


# ------------------------------------------------------------------ numbers

def I(x: float) -> int:  # noqa: E743 — the name is the spec's
    """Integer sheet coordinate, rounded half away from zero (never banker's rounding)."""
    if x >= 0:
        return int(math.floor(x + 0.5))
    return -int(math.floor(-x + 0.5))


def fmt(v: float, places: int = 1) -> str:
    """Compact number for attributes and path data: integers print bare, otherwise at most
    `places` decimals with trailing zeros stripped. `fmt(12.0) == "12"`, `fmt(12.25) == "12.3"`,
    `fmt(-0.04) == "0"`."""
    q = 10 ** places
    a = math.floor(abs(float(v)) * q + 0.5) / q          # half away from zero, not banker's
    r = -a if v < 0 else a
    if r == 0:
        return "0"
    if r == int(r):
        return str(int(r))
    s = f"{r:.{places}f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def pt(x: float, y: float) -> str:
    """Integer point for path data: `pt(3.4, 7.6) == "3,8"`."""
    return f"{I(x)},{I(y)}"


# ------------------------------------------------------------------ id prefixing

_ID_RE = re.compile(r'\bid="([^"#]+)"')
_URL_RE = re.compile(r'url\(#([^)]+)\)')
_HREF_RE = re.compile(r'\b((?:xlink:)?href)="#([^"]+)"')
# SMIL timing references: begin="arrive.end+20s; serpent.end+93.6s", end="sea10.begin+3.3s"
_TIMING_ATTR_RE = re.compile(r'\b(begin|end)="([^"]*)"')
_TIMING_REF_RE = re.compile(r'(?<![\w.-])([A-Za-z_][\w-]*)\.(begin|end|repeat\(\d+\))')


def prefix_ids(markup: str, sheet: str) -> str:
    """Rewrite id="x", url(#x), href="#x" and SMIL `x.begin/x.end` references to `<sheet>-x`.
    Ids already carrying the prefix are left alone, so the function is idempotent."""
    p = f"{sheet}-"

    def fix(name: str) -> str:
        return name if name.startswith(p) else p + name

    markup = _ID_RE.sub(lambda m: f'id="{fix(m.group(1))}"', markup)
    markup = _URL_RE.sub(lambda m: f'url(#{fix(m.group(1))})', markup)
    markup = _HREF_RE.sub(lambda m: f'{m.group(1)}="#{fix(m.group(2))}"', markup)

    def fix_timing(m: re.Match) -> str:
        attr, val = m.group(1), m.group(2)
        val = _TIMING_REF_RE.sub(lambda r: f"{fix(r.group(1))}.{r.group(2)}", val)
        return f'{attr}="{val}"'

    markup = _TIMING_ATTR_RE.sub(fix_timing, markup)
    return markup


def ids_in(markup: str) -> list[str]:
    return _ID_RE.findall(markup)


# ------------------------------------------------------------------ the envelope

def header(ed: Edition, sheet: str, stats_sha: str = STATS_SHA_PLACEHOLDER) -> str:
    """One honest comment: what it is, who drew it, from which stats, and that editing it is futile."""
    return (f"<!-- chart {RELEASE} · sheet {sheet} · edition {ed.name} · built by {BUILDER} from "
            f"assets/stats.json {stats_sha} · do not edit: the next run redraws it -->")


def paper(ed: Edition, w: int, h: int, fill: str | None = None) -> str:
    """Opaque paper under everything, both editions (the night sheet is designed, not inverted)."""
    return f'<rect width="{I(w)}" height="{I(h)}" fill="{fill or ed.theme.paper}"/>'


def svg(ed: Edition, w: int, h: int, body: str, defs: str = "", sheet: str = "sheet",
        stats_sha: str = STATS_SHA_PLACEHOLDER, paper_fill: str | None = None) -> str:
    """The whole document. `body` and `defs` are prefixed with `f"{sheet}-"` as one unit so
    cross-references between them keep resolving. The paper rect is laid first, unprefixed."""
    w, h = I(w), I(h)
    inner = prefix_ids(f"<defs>{defs}</defs>" if defs else "", sheet) + prefix_ids(body, sheet)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"{header(ed, sheet, stats_sha)}\n"
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" data-sheet="{sheet}" data-edition="{ed.name}">\n'
        f"{paper(ed, w, h, paper_fill)}"
        f"{inner}\n</svg>\n"
    )


def stamp(doc: str, stats_sha: str) -> str:
    """Fill the header's stats sha placeholder (build_assets does this once per file)."""
    return doc.replace(STATS_SHA_PLACEHOLDER, stats_sha)


def sha12(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


# ------------------------------------------------------------------ writing

def gz_size(data: bytes) -> int:
    """Deterministic gzip size (mtime 0, level 9), the number the budgets are written in."""
    return len(gzip.compress(data, compresslevel=9, mtime=0))


def write(path: str, doc: str) -> tuple[int, int]:
    """Write the document; return (bytes, gz_bytes). Only touches the file when the bytes differ,
    so an unchanged day leaves mtimes alone too."""
    data = doc.encode("utf-8")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    try:
        with open(path, "rb") as fh:
            same = fh.read() == data
    except OSError:
        same = False
    if not same:
        with open(path, "wb") as fh:
            fh.write(data)
    return len(data), gz_size(data)


def count_elements(doc: str) -> int:
    """Opening tags, not comments or closing tags: the budget's `elements`."""
    return len(re.findall(r"<[A-Za-z]", doc))


def count_paths(doc: str) -> int:
    return len(re.findall(r"<path\b", doc))


__all__ = [
    "Edition", "EDITIONS", "EDITION_NAMES", "HERO_EXTRA", "edition", "file_name",
    "I", "fmt", "pt", "prefix_ids", "ids_in", "header", "paper", "svg", "stamp", "sha12",
    "gz_size", "write", "count_elements", "count_paths",
    "RELEASE", "BUILDER", "STATS_SHA_PLACEHOLDER", "DESK_W", "PHONE_W",
]
