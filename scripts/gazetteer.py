"""gazetteer.py — one name per repository, used by every sheet (v9.2).

The hero names a feature by its kind (island → "… I.", shoal → "… Shoal", harbour and banks by their
chart.toml alias); the fleet register on sheet 2 and the tide table's HW cause must print the same
name. Kind is decided at the chart's nominal scale (K_AREA) so a sweep week that steps the drawn scale
down never renames an island.
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from chartlib.place import kind_of  # noqa: E402

K_AREA_NOMINAL = 32.2        # px² per commit at the chart's nominal scale (hero.K_AREA)


def display_name(repo: str) -> str:
    if "_" in repo:
        return " ".join(w[:1].upper() + w[1:] for w in repo.split("_") if w)
    return repo


def kind(repo: dict, spec: dict | None = None) -> str:
    """island | islet | shoal | harbour | wreck for a stats.json repo record and its chart.toml entry."""
    spec = spec or {}
    commits = int(repo.get("commits") or 0)
    r0 = math.sqrt(K_AREA_NOMINAL * max(commits, 0) / math.pi)
    k = spec.get("kind")
    if repo.get("archived"):
        return "wreck"
    if k in ("vessel", "bank"):
        return "shoal"
    if k in ("harbour", "shoal", "island", "islet"):
        return k
    k = kind_of(r0, bool(repo.get("active")), (spec.get("aliases") or [None])[0] or repo["name"], False)
    if k == "islet" and r0 >= 16:
        k = "island"
    return k


def name(repo: dict, spec: dict | None = None) -> str:
    """The name the chart prints for this repository, every sheet alike."""
    spec = spec or {}
    aliases = spec.get("aliases") or repo.get("aliases") or []
    if aliases:
        return aliases[0]
    k = kind(repo, spec)
    base = display_name(repo["name"])
    if k == "shoal":
        return f"{base} Shoal"
    if k == "island":
        return f"{base} I."
    return base


def specs(cfg: dict) -> dict:
    return {f["repo"]: f for f in (cfg or {}).get("features", [])}


def name_of(repo_name: str, data: dict, cfg: dict) -> str:
    """By repository name, from stats.json's record (a name the survey does not carry prints as typed)."""
    rec = next((r for r in data.get("repos", []) if r["name"] == repo_name), None)
    if rec is None:
        return display_name(repo_name)
    return name(rec, specs(cfg).get(repo_name))
