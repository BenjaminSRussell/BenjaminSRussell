"""column — the hero's smallest text, and its drawn height, at every window width GitHub serves it at (review round 6,
reviewer 3; review round 12, the owner).

HERO-COLUMN-PX (fail): for some viewport from VIEWPORTS[0] to VIEWPORTS[1] CSS px, the sheet the README's
  `<picture>` serves there (the first `<source>` whose min-width and max-width hold and which names no colour scheme,
  else the `<img>`: the day editions) has a text run under MIN_PX once GitHub scales the sheet to its README column.
  Review round 12: or, for a viewport from TALL_FROM to VIEWPORTS[1], that sheet is drawn taller than TALL_PX: from
  768 px GitHub shows the profile in two columns, so the screen is a laptop's or a tablet's held sideways, and a
  picture over 900 px tall puts the half that matters (the loop, the catch, Ctrl-C, the file) below the first screen.
  The phone sheet (600 x 1,121) was drawn 1,080 to 1,429 px tall at 1,012 to 1,199 px; the mid edition (820 wide,
  stacked, desk type) is served from `chart.toml` `mid_from_px` to `breakpoint_px`.

`derive(sheets)` gives the two numbers the serving rests on, from the column table and the built sheets: the widest
viewport where the phone sheet is drawn at most TALL_PX tall (851 for 1,121 units: column 481), and the widest mid
sheet whose smallest text holds MIN_PX at the next viewport's column (19 x 482 / 11 = 832 units; it is 820).

The column is GitHub's, measured on the live profile page (github.com/BenjaminSRussell, Playwright Chromium with an
iOS Safari user agent, 10 Oct 2026; scratchpad r6/r06-3, review-r06-3.md S1): one column with a bordered box under
768 px (Primer's `md` breakpoint), two columns from 768, a wider sidebar from 1012 (`lg`), and a capped README from
1280 (`xl`). Re-measure it when GitHub changes the profile layout (DESIGN.md says so too).

The range starts at 360, the narrowest phone the measurement and ROUTE-PHONE-PX cover: at 320 to 335 px (iPhone SE,
first generation) the 600-unit phone sheet's 26-unit text is 10.3 to 10.9 px, and a sheet narrow enough to hold
11 px there (562 units) would no longer fit one screen.
"""
from __future__ import annotations

import math
import re

from check import Finding, fail, info

TIER = "render"
MIN_PX = 11.0
VIEWPORTS = (360, 1920)
TALL_FROM = 768          # review round 12: two columns from here (a laptop, or a tablet held sideways)
TALL_PX = 900.0          # review round 12: the tallest the hero may be drawn there
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


def sources(readme: str, sheet: str = SHEET) -> list[tuple[int, int, str]]:
    """The `<source>`s for the day editions, in order: (min-width, max-width, edition name). A source that names a
    colour scheme is the night twin of the one after it and is skipped."""
    out = []
    for m in re.finditer(r'<source media="([^"]*)"\s+srcset="[^"]*/(' + re.escape(sheet) + r'-[\w-]+)\.svg"', readme or ""):
        media, name = m.group(1), m.group(2)
        if "prefers-color-scheme" in media:
            continue
        lo = re.search(r"min-width:\s*(\d+)px", media)
        hi = re.search(r"max-width:\s*(\d+)px", media)
        out.append((int(lo.group(1)) if lo else 0, int(hi.group(1)) if hi else 10 ** 6, name))
    return out


def served(readme: str, vw: int, sheet: str = SHEET) -> str:
    """The edition the README's `<picture>` shows at viewport `vw` (day): the first source whose widths hold."""
    for lo, hi, name in sources(readme, sheet):
        if lo <= vw <= hi:
            return name
    return f"{sheet}-day"


def phone_max(readme: str, sheet: str = SHEET) -> int | None:
    """The largest `max-width` of a `<source>` that serves a phone edition of the sheet; None without one."""
    widths = [int(m.group(1)) for m in re.finditer(r'<source media="[^"]*max-width:\s*(\d+)px[^"]*"\s+srcset="[^"]*/'
                                                  + re.escape(sheet) + r'-phone-[\w-]+\.svg"', readme or "")]
    return max(widths) if widths else None


def smallest(entry: dict) -> float | None:
    sizes = [float(t.get("size") or 0) for t in entry.get("text") or [] if isinstance(t, dict) and t.get("size")]
    return min(sizes) if sizes else None


def drawn_h(entry: dict, vw: int) -> float | None:
    """How tall the sheet is drawn in the column at viewport `vw` (CSS px); None without a height."""
    if not entry.get("w") or not entry.get("h"):
        return None
    return float(entry["h"]) * column_px(vw) / float(entry["w"])


def derive(sheets: dict, sheet: str = SHEET) -> dict:
    """Review round 12: {phone_until, mid_from, mid_w_max} from the column table and the built sheets. `phone_until`
    is the widest two-column viewport where the phone sheet is drawn at most TALL_PX tall; `mid_w_max` the widest
    mid sheet whose smallest text is MIN_PX at the column of `mid_from` (phone_until + 1)."""
    out: dict = {}
    ph = sheets.get(f"{sheet}-phone-day") or {}
    if ph.get("w") and ph.get("h"):
        vw = TALL_FROM
        while vw < VIEWPORTS[1] and (drawn_h(ph, vw + 1) or 0) <= TALL_PX + 1e-6:
            vw += 1
        out["phone_until"] = vw
        out["mid_from"] = vw + 1
        mid = sheets.get(f"{sheet}-mid-day") or {}
        s = smallest(mid) if mid else None
        if s:
            out["mid_w_max"] = math.floor(s * column_px(vw + 1) / MIN_PX)
    return out


def worst(readme: str, sheets: dict, lo: int = VIEWPORTS[0], hi: int = VIEWPORTS[1]) -> list[tuple[int, str, float]]:
    """[(viewport, edition, px)] for every viewport whose served sheet's smallest text is under MIN_PX."""
    out = []
    for vw in range(lo, hi + 1):
        name = served(readme, vw)
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


def tallest(readme: str, sheets: dict, lo: int = TALL_FROM, hi: int = VIEWPORTS[1] - 1) -> list[tuple[int, str, float]]:
    """Review round 12: [(viewport, edition, drawn px)] for every two-column viewport whose served sheet is drawn
    taller than TALL_PX."""
    out = []
    for vw in range(lo, hi + 1):
        name = served(readme, vw)
        h = drawn_h(sheets.get(name) or {}, vw)
        if h is not None and h > TALL_PX + 1e-6:
            out.append((vw, name, h))
    return out


def _runs(bad: list[tuple[int, str, float]], worst_of=min) -> list[str]:
    runs, start, prev = [], bad[0], bad[0]
    for b in bad[1:] + [None]:
        if b is None or b[0] != prev[0] + 1 or b[1] != prev[1]:
            v = worst_of(x[2] for x in bad if start[0] <= x[0] <= prev[0])
            runs.append(f"{start[0]}–{prev[0]} px ({start[1]}, {'down' if worst_of is min else 'up'} to {v:.1f} px)")
            if b is not None:
                start = b
        if b is not None:
            prev = b
    return runs


def check(ctx) -> list[Finding]:
    sheets = (ctx.report or {}).get("sheets") or {}
    if f"{SHEET}-day" not in sheets:
        return []
    readme = ctx.readme or ""
    out = []
    bad = worst(readme, sheets)
    if bad:
        out.append(fail("HERO-COLUMN-PX", "text under " + f"{MIN_PX:g} px at viewports " + "; ".join(_runs(bad)),
                        "README.md"))
    tall = tallest(readme, sheets)
    if tall:
        out.append(fail("HERO-COLUMN-PX", f"drawn taller than {TALL_PX:g} px at viewports "
                        + "; ".join(_runs(tall, max)), "README.md"))
    if not out:
        d = derive(sheets)
        spans = []
        for lo, hi, name in sources(readme):
            spans.append(f"{name} {lo or VIEWPORTS[0]}–{hi if hi < 10 ** 6 else ''}".rstrip("–"))
        out.append(info("HERO-COLUMN-PX", f"every viewport {VIEWPORTS[0]}–{VIEWPORTS[1]} px gets text of {MIN_PX:g} px "
                        f"or more, and from {TALL_FROM} a picture at most {TALL_PX:g} px tall ({'; '.join(spans)}; "
                        f"derived: phone up to {d.get('phone_until')}, mid at most {d.get('mid_w_max')} units wide)",
                        "README.md"))
    return out
