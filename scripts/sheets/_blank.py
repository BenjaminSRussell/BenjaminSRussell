"""_blank — the empty sheet that proves the runner: paper, neat line, one prefixed id, no type.

Not in build_assets.SHEETS; built only when named (`build_assets.py _blank`) and by the tests.
Harmless to leave in place.
"""
from __future__ import annotations

import edition as E

NAME = "_blank"
KIND = "chart"
SIZES = {"desk": (1280, 200), "phone": (720, 120)}
BREAKS: list[tuple[str, str, str]] = []


def build(ctx) -> str:
    ed = ctx.ed
    w, h = SIZES[ed.scale]
    t = ed.theme
    defs = f'<clipPath id="neat"><rect x="14" y="14" width="{w - 28}" height="{h - 28}"/></clipPath>'
    body = (f'<rect x="14" y="14" width="{w - 28}" height="{h - 28}" fill="none" stroke="{t.ink}" '
            f'stroke-width="1" stroke-opacity="0.8"/>'
            f'<g clip-path="url(#neat)"><line x1="{E.I(w / 2)}" y1="14" x2="{E.I(w / 2)}" y2="{h - 14}" '
            f'stroke="{t.hair}" stroke-width="0.6"/></g>')
    if ed.motion:
        body += ctx.tl.anim("opacity", [1, 1], 1.0, 0.0)   # NullTimeline → "", Timeline → something
    return E.svg(ed, w, h, body, defs, sheet=NAME)


def alt(data, cfg) -> str:
    return "Blank sheet: paper and a neat line. Nothing is charted here yet."
