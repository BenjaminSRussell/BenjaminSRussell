"""audit — docs/data/AUDIT.md §7 lists every figure the page prints, generated so it cannot drift (round 6, review 2).

AUDIT-STALE (fail): the committed register differs from what scripts/audit_figures.py writes from the hero's PURPOSE
  table, the README's blocks and chart.toml's [[figures]] and [[notices]] anchors. Run it and commit AUDIT.md.
"""
from __future__ import annotations

import os

from check import Finding, fail

TIER = "fast"


def check(ctx) -> list[Finding]:
    import audit_figures
    path = os.path.join(ctx.root, "docs", "data", "AUDIT.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return [fail("AUDIT-STALE", "docs/data/AUDIT.md is missing")]
    if audit_figures.render(text, ctx.cfg or {}) != text:
        return [fail("AUDIT-STALE", "§7 Printed figures is out of date: run python3 scripts/audit_figures.py",
                     "docs/data/AUDIT.md")]
    return []
