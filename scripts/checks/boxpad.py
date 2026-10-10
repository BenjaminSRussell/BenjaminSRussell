"""boxpad — the words inside the dotted danger line have paper round them (review round 16, the owner). TIER render.

BOX-PAD (fail): in some hero edition, the clear space sideways between a trap's words and the inner edge of the
  dotted line round them is under sheets/route.py BOX_PAD_MIN units. The words' box is the report's text manifest for
  the trap rows (advance widths, which hold the ink of these upright faces); the line's inner edge is the report's
  danger box less half the dotted stroke's width, read from the drawn <rect>. At round 15's padding of 6 the phone's
  3.4-unit stroke left 4.3 units (2.8 px at 390, 2.2 px at 308), and "60 s" touched the right edge. Up and down the
  padding is not checked here: the phone sheet has 1 unit of height to spare (checks/column.py).
"""
from __future__ import annotations

import re

from check import Finding, fail, info

TIER = "render"


def clearances(entry: dict, svg: str) -> list[tuple[str, float, float]]:
    """(trap ids, clear space left, clear space right) for each danger box drawn in one edition."""
    route = entry.get("route") or {}
    boxes: dict[tuple, list[str]] = {}
    for m in route.get("marks") or []:
        if m.get("kind") == "danger":
            boxes.setdefault(tuple(m["box"]), []).append(str(m["id"]))
    out = []
    for box, ids in boxes.items():
        x0, _y0, x1, _y1 = box
        words = [t for t in entry.get("text") or [] if isinstance(t, dict)
                 and str(t.get("key") or "") in {f"routes:{i}" for i in ids}]
        if not words:
            continue
        stroke = 0.0
        for rect in re.findall(r"<rect\b[^>]*>", svg):
            m = re.search(r'\bx="([0-9.]+)"', rect)
            if m and abs(float(m.group(1)) - x0) < 0.11 and "stroke-dasharray" in rect:
                sw = re.search(r'stroke-width="([0-9.]+)"', rect)
                stroke = float(sw.group(1)) if sw else 0.0
                break
        left = min(float(t["x0"]) for t in words) - x0 - stroke / 2
        right = x1 - max(float(t["x1"]) for t in words) - stroke / 2
        out.append(("+".join(ids), round(left, 2), round(right, 2)))
    return out


def check(ctx) -> list[Finding]:
    try:
        from sheets.route import BOX_PAD_MIN
    except Exception:
        BOX_PAD_MIN = 8
    sheets = (ctx.report or {}).get("sheets") or {}
    out: list[Finding] = []
    seen = []
    for name, entry in sorted(sheets.items()):
        if not name.startswith("hero-") or name not in ctx.svgs:
            continue
        for ids, left, right in clearances(entry, ctx.svg_text(name)):
            seen.append(f"{name} {ids} {min(left, right):.1f}")
            if min(left, right) < BOX_PAD_MIN:
                out.append(fail("BOX-PAD", f"{ids}: {left:.1f} units of paper left of the words and {right:.1f} right, "
                                f"inside the dotted line (at least {BOX_PAD_MIN})", name))
    if not out and seen:
        out.append(info("BOX-PAD", f"every danger box clears its words by {BOX_PAD_MIN} units or more sideways ("
                        + "; ".join(seen) + ")"))
    return out
