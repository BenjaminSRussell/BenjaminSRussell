"""checks/type.py — check.py plug-in: the type lint (T5 §5.1) and the glyph budget (T5 §2.3).

Fast tier, pure Python. Reads the build-report `text[]` runs when the runner hands them over, otherwise
lints whatever the type engine registered in this process (`typeset.check_type`).

`check(ctx) -> list[str]`: failure strings, empty on pass. `ctx` may be
  - a dict or object carrying `report` (the build-report dict, `sheets{"<sheet>-<edition>": {text[], ...}}`),
  - the build-report dict itself (has "sheets"),
  - anything else: falls back to the in-process registry with ctx.edition / ctx.scale / ctx.sheet if present.
Each run record needs: s, size, font, role, and ideally origin, semantic, within, x0, x1, y0, y1,
tracked_spaces, key — `typeset.run_records()` writes exactly these.
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.dirname(_HERE)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
import typeset  # noqa: E402

NAME = "type"
TIER = "fast"
def _wrap(x):
    """check_type/check_budget return strings ("sheet-ed: message"); check.py wants Findings."""
    if not isinstance(x, str):
        return x
    try:
        from check import fail
    except Exception:  # standalone run
        return x
    where, _, msg = x.partition(": ")
    return fail("TYPE", msg or x, where if msg else "")


DESCRIPTION = "type roles: scale, floors, soundings, serif floor, containers, label-caps budget, tracking"


def _get(ctx, key, default=None):
    if isinstance(ctx, dict):
        return ctx.get(key, default)
    return getattr(ctx, key, default)


def _edition_of(name: str) -> tuple[str, str]:
    """'hero-phone-night' -> ('night', 'phone'); 'approaches-still-day' -> ('day', 'desk')."""
    ed = "night" if "night" in name else "day"
    sc = "phone" if "phone" in name else ("mid" if "-mid-" in name else "desk")
    return ed, sc


def _sheet_of(name: str) -> str:
    return name.split("-", 1)[0]


def check_report(report: dict) -> list[str]:
    out = []
    for name, sheet in (report.get("sheets") or {}).items():
        runs = sheet.get("text") or []
        ed, sc = _edition_of(name)
        for err in typeset.lint_records(runs, ed, sc, _sheet_of(name)):
            out.append(f"{name}: {err}")
        n = sheet.get("glyph_defs")
        if n is not None and n > typeset.budget_for(name.split("-", 1)[0])["glyph_defs"]:
            out.append(f"{name}: {n} glyph defs (budget {typeset.budget_for(name.split('-', 1)[0])['glyph_defs']})")
    return out


def check(ctx=None) -> list[str]:
    report = _get(ctx, "report") if ctx is not None else None
    if report is None and isinstance(ctx, dict) and "sheets" in ctx:
        report = ctx
    if isinstance(report, dict) and "sheets" in report:
        return [_wrap(x) for x in check_report(report)]
    edition = _get(ctx, "edition", "day") if ctx is not None else "day"
    scale = _get(ctx, "scale", None) if ctx is not None else None
    sheet = _get(ctx, "sheet", None) if ctx is not None else None
    return [_wrap(x) for x in typeset.check_type(edition, scale, sheet) + typeset.check_budget()]


if __name__ == "__main__":
    import json
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_SCRIPTS, "..", "assets", "build-report.json")
    with open(path, encoding="utf-8") as fh:
        errs = check_report(json.load(fh))
    print("\n".join(errs) or "type: ok")
    sys.exit(1 if errs else 0)
