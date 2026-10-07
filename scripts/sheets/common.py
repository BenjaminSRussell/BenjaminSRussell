"""Helpers shared by the sheet modules (not chart furniture: that is chartlib)."""
from __future__ import annotations

import svgkit as k
from svgkit import Theme

W = 1280


def cap(t: Theme, s: str, x: float, y: float, size: float = 13, fill=None, anchor="start", tracking=1.6, opacity=None,
        font: str = "plex"):
    """Tracked mono caption. Semantic captions are >= 13px (STANDARDS 5); 9-11 only for texture."""
    return k.text_use(s.upper(), x, y, font, size, fill or t.muted, anchor=anchor, tracking=tracking, opacity=opacity)


def sheet(t: Theme, w: float, h: float, rx: float = 10, paper: str | None = None) -> str:
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{paper or t.paper}" stroke="{t.hair}"/>'


def neat_line(t: Theme, x: float, y: float, w: float, h: float, double: bool = True) -> str:
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{t.ink}" stroke-width="0.9" stroke-opacity=".85"/>'
    if double:
        out += f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" fill="none" stroke="{t.ink}" stroke-width="0.5" stroke-opacity=".6"/>'
    return out


def chart_number(t: Theme, text: str, w: float, h: float) -> str:
    """Chart number outside the neat line, top-right and bottom-left corners, as on a real sheet."""
    return (k.text_use(text, w - 22, 13, "plex", 10, t.ink, anchor="end", tracking=1.2, opacity=0.8)
            + k.text_use(text, 22, h - 6, "plex", 10, t.ink, tracking=1.2, opacity=0.8))


def measured(t: Theme, s: str, x: float, y: float, size: float = 13, fill=None, anchor="start") -> str:
    """Upright numeral: a measured value (chart convention defined on the Approaches legend)."""
    return k.text_use(s, x, y, "plex", size, fill or t.ink, anchor=anchor)


def illustrative(t: Theme, s: str, x: float, y: float, size: float = 13, fill=None, anchor="start") -> str:
    """Italic numeral: an illustrative value, not a measurement."""
    return k.text_use(s, x, y, "plex-italic", size, fill or t.ink, anchor=anchor)
