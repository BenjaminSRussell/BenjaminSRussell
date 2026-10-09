"""_concept.py — what the three round-4 concept stills share (DECISIONS D9).

A concept still is one hand-composed day-edition SVG, 1280 wide, no animation, written by a small
script in this folder that reads assets/stats.json and chart.toml for every printed figure. This
module loads those two files, opens the type engine (scripts/typeset.py) on the day theme, and
writes the envelope. Nothing here is a measurement; nothing here places anything.

    from _concept import Concept
    c = Concept("vessel")            # stats, cfg, theme, T (typeset), S (stroke)
    body = c.t("rustmapper", 40, 80, "title")
    c.write("concepts/vessel.svg", 1280, 720, body)
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
for p in (SCRIPTS,):
    if p not in sys.path:
        sys.path.insert(0, p)

import tokens  # noqa: E402
import typeset as T  # noqa: E402
from chartlib.furniture import stroke as S, op, Jitter  # noqa: E402
from chartlib.water import hatch  # noqa: E402
from edition import fmt, I  # noqa: E402

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def day(s: str) -> _dt.date:
    return _dt.date.fromisoformat(s[:10])


def long_date(d: _dt.date | str) -> str:
    """7 Oct 2026 (no leading zero)."""
    d = day(d) if isinstance(d, str) else d
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def thousands(n: int) -> str:
    return f"{n:,}"


class Concept:
    def __init__(self, name: str):
        self.name = name
        with open(os.path.join(ROOT, "assets", "stats.json"), "rb") as fh:
            raw = fh.read()
        self.stats = json.loads(raw)
        self.stats_sha = hashlib.sha256(raw).hexdigest()[:12]
        with open(os.path.join(ROOT, "chart.toml"), "rb") as fh:
            self.cfg = tomllib.load(fh)
        self.theme = tokens.THEMES["day"]
        self.T = T
        T.begin_asset(name, f"{name}-")
        self.aliases = {f["repo"]: f["aliases"][0] for f in self.cfg.get("features", []) if f.get("aliases")}

    # ---- data
    @property
    def taken(self) -> _dt.date:
        return day(self.stats["taken"])

    def repo(self, name: str) -> dict:
        for r in self.stats["repos"]:
            if r["name"] == name:
                return r
        raise KeyError(name)

    def claim(self, key: str) -> dict:
        return self.stats["claims"][key]

    def display_name(self, repo: str) -> str:
        """What the charts print for a repo: the chart.toml alias when one exists, else the name."""
        return self.aliases.get(repo, repo)

    # ---- type (the engine, day edition, desk scale)
    def t(self, s: str, x: float, y: float, role: str = "label", **kw) -> str:
        kw.setdefault("edition", "day")
        kw.setdefault("scale", "desk")
        return T.label(s, x, y, role, **kw)

    def w(self, s: str, role: str = "label", **kw) -> float:
        kw.setdefault("edition", "day")
        kw.setdefault("scale", "desk")
        return T.text_width(s, role, **kw)

    # ---- envelope
    def header(self) -> str:
        return (f"<!-- concept still · {self.name} · round 4 (D9) · drawn by scripts/concepts/{self.name}.py "
                f"from assets/stats.json {self.stats_sha} and chart.toml · day edition · no animation -->")

    def svg(self, w: int, h: int, body: str, defs: str = "", title: str = "") -> str:
        w, h = I(w), I(h)
        d = T.glyph_defs() + defs
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f"{self.header()}\n"
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" data-concept="{self.name}">\n'
            + (f"<title>{title}</title>" if title else "")
            + f'<rect width="{w}" height="{h}" fill="{self.theme.paper}"/>'
            + (f"<defs>{d}</defs>" if d else "")
            + body
            + "\n</svg>\n"
        )

    def write(self, rel_path: str, w: int, h: int, body: str, defs: str = "", title: str = "") -> str:
        path = os.path.join(ROOT, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc = self.svg(w, h, body, defs, title)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(doc)
        print(f"{rel_path}: {len(doc.encode()) / 1024:.0f} KB, {T.glyph_count()} glyph defs")
        return path


__all__ = ["Concept", "T", "S", "op", "Jitter", "hatch", "fmt", "I", "tokens", "day", "long_date", "thousands",
           "MONTHS"]
