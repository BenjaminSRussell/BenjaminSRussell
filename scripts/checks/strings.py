"""strings — the banned phrases, case-insensitive, over the SVGs, the report's text manifest,
README.md and chart.toml (T10 check 6 + STANDARDS 1).

Figures inside `<!-- n:key -->…<!-- /n -->` markers are build-written and exempt ("Oct 2024" is
banned as a hand-typed figure, not as a date)."""
from __future__ import annotations

import os
import re

from check import Finding, fail

TIER = "fast"

BANNED = (
    "ILLUSTRATIVE", "PENDING", "SEEDED", "NOT FOR NAVIGATION", "Here be dragons", "Fair winds",
    "example.com", "Oct 2024", "thanks for reading", "that's a mood", "Hi I'm Ben", "Hi, I'm Ben",
    "drawn not templated", "drawn, not templated", "REFRESHED DAILY", "works at night", "lorem",
    "TODO", "FIXME", "<!-- POSITION",
)
# whole-word for the short ones so "pending" inside "appending" and "v7" inside a hash do not fire
_WORDISH = {"PENDING", "SEEDED", "TODO", "FIXME", "lorem"}
_N_SPAN = re.compile(r"<!--\s*n:[\w.-]+\s*-->.*?<!--\s*/n\s*-->", re.S)
_MARKER = re.compile(r"<!--\s*[\w:-]+:(?:start|end)\b[^>]*-->")


def _patterns() -> list[tuple[str, re.Pattern]]:
    out = []
    for s in BANNED:
        esc = re.escape(s)
        if s in _WORDISH:
            esc = rf"(?<![A-Za-z]){esc}(?![A-Za-z])"
        out.append((s, re.compile(esc, re.I)))
    out.append(("v7", re.compile(r"(?<![\w.])v7(?![\w.])", re.I)))
    return out


PATTERNS = _patterns()


def scan(text: str, where: str, code: str = "STRINGS-BANNED") -> list[Finding]:
    out = []
    for label, pat in PATTERNS:
        m = pat.search(text)
        if m:
            line = text.count("\n", 0, m.start()) + 1
            out.append(fail(code, f"{label!r} at line {line}", where))
    return out


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    for name in ctx.svgs:
        out += scan(ctx.svg_text(name), name)
    for name, e in (ctx.report or {}).get("sheets", {}).items():
        manifest = "\n".join(str(t.get("s", "")) for t in e.get("text", []) if isinstance(t, dict))
        out += scan(manifest, f"{name} text manifest", "STRINGS-MANIFEST")
        out += scan(str(e.get("alt", "")), f"{name} alt", "STRINGS-ALT")
    if ctx.readme:
        readme = _N_SPAN.sub("", ctx.readme)
        readme = _MARKER.sub("", readme)
        out += scan(readme, os.path.basename(ctx.readme_path), "STRINGS-README")
    try:
        with open(ctx.cfg_path, encoding="utf-8") as fh:
            out += scan(fh.read(), "chart.toml", "STRINGS-TOML")
    except OSError:
        pass
    return out
