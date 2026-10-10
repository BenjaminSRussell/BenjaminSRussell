"""design — DESIGN.md is the page the README's data line links as "drawing" (review round 12, the copy editor).

DESIGN-FRESH (fail): DESIGN.md differs from `python3 scripts/tokens.py --md` (its opening paragraph is written from
  the drawn route, so a stale file describes rows the picture no longer draws; the committed file had been edited by
  hand, and regenerating it restored a wording retired in round 8), or its prose outside code spans, code blocks and
  HTML comments holds a theme word: the hero's T-WORDS (checks/route.py THEME_WORDS) and the words the old page used
  for marks that are not drawn (EXTRA_WORDS). A visitor who opens the method page gets the profile's register, not
  the vocabulary the owner cut.
"""
from __future__ import annotations

import os
import re

from check import Finding, fail, info

TIER = "fast"
EXTRA_WORDS = ("ship's", "islands", "lateral", "soundings", "unsurveyed", "pecked", "datum", "survey")


def prose(text: str) -> str:
    """DESIGN.md without fenced code, code spans and HTML comments."""
    t = re.sub(r"```.*?```", " ", text or "", flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    return re.sub(r"`[^`\n]*`", " ", t)


def theme_words(text: str) -> list[str]:
    from checks.route import THEME_WORDS
    words = tuple(THEME_WORDS) + EXTRA_WORDS
    rx = re.compile(r"(?<![\w'])(" + "|".join(re.escape(w) for w in words) + r")(?![\w'])", re.I)
    return sorted({m.group(1).lower() for m in rx.finditer(prose(text))})


def check(ctx) -> list[Finding]:
    path = os.path.join(ctx.root, "DESIGN.md")
    try:
        with open(path, encoding="utf-8") as fh:
            have = fh.read()
    except OSError:
        return [fail("DESIGN-FRESH", "DESIGN.md is missing: run python3 scripts/tokens.py --md > DESIGN.md")]
    import tokens
    out = []
    try:
        want = tokens.design_md(ctx.stats or None, ctx.cfg or None) + "\n"
    except Exception as exc:       # the route cannot be planned: the page cannot be written from it
        want = None
        out.append(fail("DESIGN-FRESH", f"tokens.design_md() failed: {exc}", "DESIGN.md"))
    if want is not None and have != want:
        a, b = have.splitlines(), want.splitlines()
        i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        out.append(fail("DESIGN-FRESH", f"DESIGN.md differs from tokens.py --md at line {i + 1}: run python3 "
                        "scripts/tokens.py --md > DESIGN.md", "DESIGN.md"))
    words = theme_words(have)
    if words:
        out.append(fail("DESIGN-FRESH", f"theme words in DESIGN.md's prose: {', '.join(words)}", "DESIGN.md"))
    if not out:
        out.append(info("DESIGN-FRESH", "DESIGN.md matches tokens.py --md and names no theme word", "DESIGN.md"))
    return out
