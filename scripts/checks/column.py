"""column — the hero's smallest text at every window width GitHub serves it at (review round 6, reviewer 3).

HERO-COLUMN-PX (fail): for some viewport from VIEWPORTS[0] to VIEWPORTS[1] CSS px, the sheet the README's
  `<picture>` serves there (a phone edition while the viewport is within the phone `<source>`'s max-width, the desk
  edition above it) has a text run under MIN_PX once GitHub scales the sheet to its README column.

The column is GitHub's, measured on the live profile page (github.com/BenjaminSRussell, Playwright Chromium with an
iOS Safari user agent, 10 Oct 2026; scratchpad r6/r06-3, review-r06-3.md S1): one column with a bordered box under
768 px (Primer's `md` breakpoint), two columns from 768, a wider sidebar from 1012 (`lg`), and a capped README from
1280 (`xl`). Re-measure it when GitHub changes the profile layout (DESIGN.md says so too).

The range starts at 360, the narrowest phone the measurement and ROUTE-PHONE-PX cover: at 320 to 335 px (iPhone SE,
first generation) the 600-unit phone sheet's 26-unit text is 10.3 to 10.9 px, and a sheet narrow enough to hold
11 px there (562 units) would no longer fit one screen.
"""
from __future__ import annotations

import re

from check import Finding, fail, info

TIER = "render"
MIN_PX = 11.0
VIEWPORTS = (360, 1920)
SHEET = "hero"


def column_px(vw: int) -> float:
    """GitHub's README column at a viewport `vw` (CSS px), as measured on 10 Oct 2026."""
    if vw <= 767:
        return vw - 82
    if vw <= 1011:
        return vw - 370
    if vw <= 1279:
        return vw - 434
    return 846


def phone_max(readme: str, sheet: str = SHEET) -> int | None:
    """The largest `max-width` of a `<source>` that serves a phone edition of the sheet; None without one."""
    widths = [int(m.group(1)) for m in re.finditer(r'<source media="[^"]*max-width:\s*(\d+)px[^"]*"\s+srcset="[^"]*/'
                                                  + re.escape(sheet) + r'-phone-[\w-]+\.svg"', readme or "")]
    return max(widths) if widths else None


def smallest(entry: dict) -> float | None:
    sizes = [float(t.get("size") or 0) for t in entry.get("text") or [] if isinstance(t, dict) and t.get("size")]
    return min(sizes) if sizes else None


def worst(readme: str, sheets: dict, lo: int = VIEWPORTS[0], hi: int = VIEWPORTS[1]) -> list[tuple[int, str, float]]:
    """[(viewport, edition, px)] for every viewport whose served sheet's smallest text is under MIN_PX."""
    bp = phone_max(readme)
    out = []
    for vw in range(lo, hi + 1):
        name = f"{SHEET}-phone-day" if bp is not None and vw <= bp else f"{SHEET}-day"
        e = sheets.get(name)
        if not e or not e.get("w"):
            continue
        s = smallest(e)
        if s is None:
            continue
        px = s * column_px(vw) / float(e["w"])
        if px < MIN_PX - 1e-6:
            out.append((vw, name, px))
    return out


def check(ctx) -> list[Finding]:
    sheets = (ctx.report or {}).get("sheets") or {}
    if f"{SHEET}-day" not in sheets:
        return []
    bad = worst(ctx.readme or "", sheets)
    if not bad:
        bp = phone_max(ctx.readme or "")
        return [info("HERO-COLUMN-PX", f"every viewport {VIEWPORTS[0]}–{VIEWPORTS[1]} px gets text of {MIN_PX:g} px or "
                     f"more (phone sheet up to {bp} px)", "README.md")]
    runs, start = [], bad[0]
    prev = bad[0]
    for b in bad[1:] + [None]:
        if b is None or b[0] != prev[0] + 1 or b[1] != prev[1]:
            low = min(x[2] for x in bad if start[0] <= x[0] <= prev[0])
            runs.append(f"{start[0]}–{prev[0]} px ({start[1]}, down to {low:.1f} px)")
            if b is not None:
                start = b
        if b is not None:
            prev = b
    return [fail("HERO-COLUMN-PX", "text under " + f"{MIN_PX:g} px at viewports " + "; ".join(runs), "README.md")]
