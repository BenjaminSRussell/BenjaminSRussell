"""figures — every number typed into the README's own prose rests on the code (round 6, review 2).

FIGURES (fail): a run of digits or a number word in README.md's visible text outside the build-written marker blocks
  (and outside inline `n:` figures) that no `[[figures]]` row covers, or a row that does not hold at its
  repository's HEAD (stats.json `figures`, checked by scripts/data/proof.py). Link targets, comments and repository
  names (3d-swift-widget) are not prose.
"""
from __future__ import annotations

import re

from check import Finding, fail

TIER = "fast"
_BLOCK = re.compile(r"<!--\s*([\w:.-]+):start\b[^>]*-->.*?<!--\s*\1:end\s*-->", re.S)
_INLINE = re.compile(r"<!--\s*n:[\w.-]+\s*-->.*?<!--\s*/n\s*-->", re.S)
WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
         "forty", "fifty", "hundred", "thousand", "million", "dozen")
NUMBER = re.compile(r"(?<![A-Za-z0-9_\-])\d+(?:,\d{3})*(?:\.\d+)?(?![A-Za-z0-9_\-])|"
                    r"(?<![A-Za-z0-9_\-])(?:" + "|".join(WORDS) + r")(?![A-Za-z0-9_\-]|\.[a-z])", re.I)


def prose(readme: str) -> str:
    """README text written by hand and seen by a reader: marker blocks, inline figures, comments, tags and link
    targets removed (the same span lengths are kept as spaces, so positions stay comparable)."""
    t = _BLOCK.sub(lambda m: " " * len(m.group(0)), readme or "")
    t = _INLINE.sub(lambda m: " " * len(m.group(0)), t)
    t = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), t, flags=re.S)
    t = re.sub(r"<[^>]+>", lambda m: " " * len(m.group(0)), t)
    t = re.sub(r"\]\([^)]*\)", lambda m: " " * len(m.group(0)), t)
    return t.replace("\u00a0", " ")      # review round 7: "60\u00a0s" is the row "60 s" (same length)


def uncovered(readme: str, rows: list[dict]) -> list[str]:
    text = prose(readme)
    spans = []
    for r in rows or []:
        if not r.get("holds"):
            continue
        for m in re.finditer(re.escape(str(r.get("text") or "\0")), text):
            spans.append((m.start(), m.end()))
    out = []
    for m in NUMBER.finditer(text):
        if not any(a <= m.start() and m.end() <= b for a, b in spans):
            line = text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip()
            out.append(f"{m.group(0)!r} in “…{line}…”")
    return out


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    rows = (ctx.stats or {}).get("figures") or []
    for r in rows:
        if not r.get("holds"):
            out.append(fail("FIGURES", f"{r.get('text')!r} ({r.get('repo')}) does not hold at HEAD: {r.get('why')}",
                            "stats.json figures"))
    for hit in uncovered(ctx.readme or "", rows):
        out.append(fail("FIGURES", f"{hit} is typed into the README with no [[figures]] row behind it", "README.md"))
    return out
