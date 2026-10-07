"""checks/log.py — assets/log.json v2: schema, check_log rules, consistency with stats.json (T7 §7 check 9, data half).

    check(ctx) -> list[Finding]
"""
from __future__ import annotations

import json
import os
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
try:
    from check import Finding  # type: ignore
except Exception:  # pragma: no cover
    Finding = namedtuple("Finding", "level code msg")

from data import LOG_PATH, STATS_PATH, load_chart_toml, logsim, model  # noqa: E402


def _get(ctx, key, default=None):
    if ctx is None:
        return default
    if isinstance(ctx, dict):
        return ctx.get(key, default)
    return getattr(ctx, key, default)


def log_path(ctx=None) -> str:
    cfg = _get(ctx, "cfg") or load_chart_toml()
    rel = ((cfg or {}).get("log") or {}).get("path")
    root = _get(ctx, "root") or os.path.dirname(SCRIPTS)
    return os.path.join(root, rel) if rel else (os.path.join(root, "assets", "log.json") if _get(ctx, "root") else LOG_PATH)


def check(ctx=None) -> list[Finding]:
    out: list[Finding] = []
    log = _get(ctx, "log")
    if not isinstance(log, dict):
        try:
            with open(log_path(ctx), encoding="utf-8") as fh:
                log = json.load(fh)
        except (OSError, ValueError) as exc:
            return [Finding("fail", "log.load", f"log.json unreadable: {exc}")]
    for e in model.schema_errors(log, model.load_schema(model.LOG_SCHEMA_PATH)):
        out.append(Finding("fail", "log.schema", e))
    for e in logsim.check_log(log):
        out.append(Finding("fail", "log.rule", e))
    if not log.get("measured"):
        out.append(Finding("info", "log.computed", "log is computed-consistent (italic) until Ben records a real session"))
    stats = _get(ctx, "stats")
    if not isinstance(stats, dict):
        try:
            with open(os.path.join(_get(ctx, "root"), "assets", "stats.json") if _get(ctx, "root") else STATS_PATH,
                      encoding="utf-8") as fh:
                stats = json.load(fh)
        except (OSError, ValueError, TypeError):
            stats = None
    if stats:
        ev = (stats.get("edition") or {}).get("version")
        if ev and log.get("version") != ev:
            out.append(Finding("warn", "log.version", f"log version {log.get('version')} != edition {ev}"))
        cores = (log.get("machine") or {}).get("cores")
        shards = (stats.get("claims") or {}).get("shards") or {}
        if shards.get("measured") and cores is not None and str(shards.get("value")) != str(cores):
            out.append(Finding("warn", "log.shards", f"claims.shards {shards.get('value')} != machine.cores {cores}"))
    return out


if __name__ == "__main__":
    for f in check():
        print(f"{f.level:5} {f.code:18} {f.msg}")
