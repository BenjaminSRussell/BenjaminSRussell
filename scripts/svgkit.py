"""svgkit — the facade (BUILD-CONTRACT "facade plan"). One import for a sheet module:

    import svgkit as k
    k.svg(ctx.ed, w, h, body, defs, sheet=NAME)        # edition.py   (A/T1)
    k.text(...), k.sounding(...), k.text_on_path(...)   # typeset.py   (D/T5)
    k.Timeline(...), k.sample_path(...)                  # timeline.py  (E/T4)
    k.THEMES, k.W, k.DASH, k.ROLES, k.BUDGETS            # tokens.py

Everything here is re-exported from those modules; nothing is defined in this file, so there is
nothing to merge. Each collaborator is imported inside try/except so the facade loads while a
module is still being written (its names are then simply absent). The v8 kit the reference sheet
(v8) was retired with the v8 sheets; git history keeps it.
"""
from __future__ import annotations

import os as _os
import sys as _sys

_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)

# tokens: the containers every module shares
from tokens import (  # noqa: E402,F401
    Theme, THEMES, W, INK, DASH, SCALE, SCALE_PHONE, FLOORS, ROLES, GRADE, NIGHT_LIGHT_CUTS,
    EASE, LOOP_PERIODS, QUANTUM, PAGE_PERIOD, BUDGETS,
)
import tokens  # noqa: E402,F401

# edition: Edition, EDITIONS, svg(), prefix_ids(), I(), fmt(), write(), …
from edition import *  # noqa: E402,F401,F403
import edition  # noqa: E402,F401

# typeset: shape/text/text_use/runs/sounding/text_on_path/text_width/exclusions/exclude/
#          check_type/glyph_count/glyph_defs/begin_asset/FIGURES/label/run_records/…
try:
    from typeset import *  # noqa: E402,F401,F403
    import typeset  # noqa: E402,F401
except ImportError:  # pragma: no cover — D's module not present yet
    typeset = None  # type: ignore

# timeline: Timeline, NullTimeline, Sail, Tack, sample_path, path_length, flash_schedule, …
try:
    from timeline import *  # noqa: E402,F401,F403
    import timeline  # noqa: E402,F401
except ImportError:  # pragma: no cover — E's module not present yet
    timeline = None  # type: ignore


def _exports() -> list[str]:
    names = set(tokens.__dict__.keys()) & {
        "Theme", "THEMES", "W", "INK", "DASH", "SCALE", "SCALE_PHONE", "FLOORS", "ROLES", "GRADE",
        "NIGHT_LIGHT_CUTS", "EASE", "LOOP_PERIODS", "QUANTUM", "PAGE_PERIOD", "BUDGETS"}
    names |= set(edition.__all__)
    for mod in (typeset, timeline):
        if mod is not None:
            names |= set(getattr(mod, "__all__", ()) or (n for n in dir(mod) if not n.startswith("_")))
    names |= {"tokens", "edition", "typeset", "timeline"}
    return sorted(names)


__all__ = _exports()
