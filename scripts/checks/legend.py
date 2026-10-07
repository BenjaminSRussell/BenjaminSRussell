"""legend — the approaches legend defines every symbol the page uses (T10 check 10).

Symbols are chartlib `<g id="{sheet}-sym-{name}">` definitions placed with `<use href="#…-sym-…">`.
Used = every `-sym-` href on hero, approaches and footer (day edition). Legend = the approaches
report entry's `legend[]` (symbol names the legend block draws), else every `-sym-` use inside the
element whose id contains "legend". Allow-list for vessels and the serpent, which are drawn, not
charted symbols."""
from __future__ import annotations

import re

from check import Finding, fail, warn, info

TIER = "fast"
ALLOW = {"sloop", "sloop-glyph", "serpent", "hull", "sails", "sail", "boat", "packet", "halo", "flare"}
_USE = re.compile(r'<use[^>]*href="#[\w-]*?-sym-([\w-]+)"')


def _legend_names(svg: str) -> set[str]:
    m = re.search(r'<g[^>]*id="[\w-]*legend[\w-]*"[^>]*>(.*?)</g>\s*(?=<g|<path|$)', svg, re.S)
    if not m:
        # fall back: largest region of the document mentioning "legend"
        i = svg.find("legend")
        if i < 0:
            return set()
        return set(_USE.findall(svg[i:i + 60000]))
    return set(_USE.findall(m.group(1)))


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    report = (ctx.report or {}).get("sheets", {})
    legend_entry = report.get("approaches-day") or {}
    used: dict[str, set[str]] = {}
    for sheet in ("hero", "approaches", "footer"):
        name = f"{sheet}-day"
        if name not in ctx.svgs:
            continue
        svg = ctx.svg_text(name)
        used[sheet] = set(_USE.findall(svg))
        rep_used = set(legend_entry.get("symbols_used") or []) if sheet == "approaches" else None
        if rep_used is not None and rep_used and rep_used != used[sheet]:
            out.append(warn("LEGEND-REPORT", f"report symbols_used {sorted(rep_used)} ≠ hrefs {sorted(used[sheet])}", name))
    if "approaches-day" not in ctx.svgs:
        return out
    legend = set(legend_entry.get("legend") or []) or _legend_names(ctx.svg_text("approaches-day"))
    if not legend:
        out.append(fail("LEGEND-MISSING", "no legend block found on the approaches sheet", "approaches-day"))
        return out
    all_used = set().union(*used.values()) if used else set()
    for s in sorted(all_used - legend - ALLOW):
        where = ", ".join(sh for sh, u in used.items() if s in u)
        out.append(fail("LEGEND-UNDEFINED", f"symbol {s!r} is used on {where} but has no legend row", "approaches-day"))
    for s in sorted(legend - all_used):
        out.append(warn("LEGEND-UNUSED", f"legend row {s!r} is not used on any sheet", "approaches-day"))
    svg = ctx.svg_text("approaches-day")
    txt = " ".join((r.get("s") or "") for r in (legend_entry.get("text") or [])).lower()
    if not any(k in txt for k in ("upright", "measured")) and "measured" not in svg.lower():
        out.append(fail("LEGEND-CONVENTION", "the legend does not state the upright = measured / italic convention", "approaches-day"))
    if "proposed" not in txt and "proposed" not in svg.lower():
        out.append(fail("LEGEND-PROPOSED", "the legend has no row for the proposed (unlit) channel", "approaches-day"))
    out.append(info("LEGEND", f"{len(legend)} legend rows · {len(all_used)} symbols used"))
    return out
