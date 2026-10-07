#!/usr/bin/env python3
"""Draw every sheet of the chart, in the day and night editions.

    python3 scripts/build_assets.py            # all sheets
    python3 scripts/build_assets.py hero log   # some sheets

Each sheet is a module in scripts/sheets/ exposing NAME and build(theme, data) -> svg string.
Data (assets/stats.json) is loaded once and passed in, so the chart redraws from real numbers.
"""
from __future__ import annotations

import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "sheets"))
import svgkit as k  # noqa: E402

ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "assets")
W = 1280
SHEETS = ["hero", "soundings", "approaches", "log", "instruments", "footer"]


def load_data() -> dict:
    with open(os.path.join(OUT, "stats.json"), encoding="utf-8") as fh:
        return json.load(fh)


def main(only=None) -> int:
    data = load_data()
    problems = 0
    for name in SHEETS:
        if only and name not in only:
            continue
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            print(f"ERROR: no sheet module for {name}")
            problems += 1
            continue
        editions = getattr(mod, "EDITIONS", ("dark", "light"))
        for t in k.CHART_THEMES:
            if t.name not in editions:
                continue
            k.begin_asset()
            svg = mod.build(t, data)
            for p in k.check_bounds(W, margin=28):
                print(f"WARNING {name}-{t.name}:", p)
                problems += 1
            k.write(os.path.join(OUT, f"{name}-{t.name}.svg"), svg)
        if hasattr(mod, "build_phone"):
            for t in k.CHART_THEMES:
                k.begin_asset()
                k.write(os.path.join(OUT, f"{name}-phone-{t.name}.svg"), mod.build_phone(t, data))
    return problems


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:] or None) else 0)
