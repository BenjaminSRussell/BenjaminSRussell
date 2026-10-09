"""checks/data.py — the honesty checks on assets/stats.json (T7 §7: 1, 3, 10 and the data half of 8).

    check(ctx) -> list[Finding]        Finding(level: "fail"|"warn"|"info", code, msg)

ctx may carry `.stats` (dict) or `.root`; failing that assets/stats.json is loaded. Pure Python, fast tier.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
try:  # T10's runner defines the Finding type; stand alone until it lands
    from check import Finding  # type: ignore
except Exception:  # pragma: no cover
    Finding = namedtuple("Finding", "level code msg")

from data import STATS_PATH, model  # noqa: E402
from data.claims import upright_ok  # noqa: E402

CALENDAR_TOLERANCE = 0.10


def _get(ctx, key, default=None):
    if ctx is None:
        return default
    if isinstance(ctx, dict):
        return ctx.get(key, default)
    return getattr(ctx, key, default)


def load_stats(ctx=None) -> dict:
    stats = _get(ctx, "stats")
    if isinstance(stats, dict):
        return stats
    root = _get(ctx, "root")
    path = os.path.join(root, "assets", "stats.json") if root else STATS_PATH
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check(ctx=None) -> list[Finding]:
    out: list[Finding] = []
    try:
        stats = load_stats(ctx)
    except (OSError, ValueError) as exc:
        return [Finding("fail", "data.load", f"stats.json unreadable: {exc}")]
    today = _get(ctx, "today") or dt.datetime.now(dt.timezone.utc).date()
    for e in model.validate(stats, today=today):
        code = "data.seeded" if "seeded" in e else "data.provenance" if e.startswith(("provenance", "taken")) \
            else "data.schema" if e.startswith("$") else "data.invariant"
        out.append(Finding("fail", code, e))
    cc = stats.get("calendar_check")
    if cc and cc.get("disagreement") is not None and cc["disagreement"] > CALENDAR_TOLERANCE:
        span = f" {cc['from']}..{cc['to']}" if cc.get("from") and cc.get("to") else " the last 52 weeks"
        out.append(Finding("warn", "data.calendar",
                           f"commits on the surveyed repositories over{span}: clones count {cc['clone']}, GitHub credits "
                           f"{cc['calendar']}: {cc['disagreement']:.0%} apart (> 10 %): mark SD"))
    elif cc and cc.get("disagreement") is None:
        out.append(Finding("warn", "data.calendar", "GitHub credits no commits on the surveyed repositories in the window: "
                           "check the author emails on the account"))
    elif stats.get("calendar") is None:
        out.append(Finding("info", "data.calendar", "no GraphQL contribution window in this run; the second instrument is absent"))
    for r in stats.get("repos", []):
        if r.get("stale"):
            out.append(Finding("warn", "data.stale", f"{r['name']}: not re-surveyed since {r.get('stale_since')} (Rep)"))
    for u in stats.get("unsurveyed", []):
        out.append(Finding("warn", "data.unsurveyed", f"{u['name']}: {u['reason']} (ED)"))
    ed = stats.get("edition")
    if not ed:
        out.append(Finding("fail", "data.edition", "no edition: PyPI unreachable and no cache"))
    elif ed.get("stale"):
        out.append(Finding("warn", "data.edition", "edition from cache (PyPI unreachable this run)"))
    if not stats.get("notices"):
        out.append(Finding("warn", "data.notices", "no notices: N = 0"))
    tide = stats.get("tide") or {}
    if tide and not (tide.get("hw") or {}).get("cause"):
        out.append(Finding("fail", "data.tide", "tide.hw has no cause repo"))
    v = stats.get("variation") or {}
    if v.get("annual_change") is not None and min(v.get("basis_days") or [0, 0]) < v.get("min_basis_days", 60):
        out.append(Finding("fail", "data.variation", "annual_change stated on a window under 60 commit-days"))
    for cid, c in (stats.get("claims") or {}).items():
        if c.get("measured") and not upright_ok(c):
            out.append(Finding("fail", "data.claims", f"claims.{cid} measured without source+sha"))
    prov = stats.get("provenance") or {}
    inst = prov.get("instruments") or {}
    if inst.get("clones") != "live":
        out.append(Finding("warn", "data.clones", "no live clone in this run; every feature is Rep"))
    if stats.get("repo_count") is not None and stats["repo_count"] != len(stats.get("repos", [])) + len(stats.get("unsurveyed", [])):
        out.append(Finding("warn", "data.repo_count",
                           f"repo_count {stats['repo_count']} != surveyed {len(stats.get('repos', []))} + unsurveyed {len(stats.get('unsurveyed', []))}"))
    return out


if __name__ == "__main__":
    for f in check():
        print(f"{f.level:5} {f.code:18} {f.msg}")
