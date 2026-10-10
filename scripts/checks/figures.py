"""figures — every number typed into the README's own prose rests on the code (round 6, review 2).

FIGURES (fail): a run of digits or a number word in README.md's visible text outside the build-written marker blocks
  (and outside inline `n:` figures) that no `[[figures]]` row covers, or a row that does not hold at its
  repository's HEAD (stats.json `figures`, checked by scripts/data/proof.py). Link targets, comments and repository
  names (3d-swift-widget) are not prose. Review round 10 (the owner): a CLAIMS phrase ("sample site": what a
  command crawls) in the visible prose needs a holding row whose text contains it, as a number does; the old Scrapy
  run sentence said `python start.py` "crawls a university's sample site" with no row, and it loads no seeds at all.
  Review round 11 (the owner): the printed working rules' bodies (chart.toml [[notices]], build-written, so not in
  the prose above) are read too: a typed number there needs a holding row, and a row marked `block = "notices"`
  must be in one of them (rule 1 carries the breaker's 5 URLs and 60 s, said nowhere else).
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


CLAIMS = ("sample site",)


def unbacked_claims(readme: str, rows: list[dict]) -> list[str]:
    """Each CLAIMS phrase in the visible prose that no holding row's text contains."""
    text = prose(readme)
    out = []
    for c in CLAIMS:
        for m in re.finditer(re.escape(c), text, re.I):
            if not any(c.lower() in str(r.get("text") or "").lower() for r in rows or [] if r.get("holds")):
                line = text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip()
                out.append(f"{m.group(0)!r} in “…{line}…”")
    return out


def notice_bodies(cfg: dict | None) -> str:
    """The bodies of the rules the page prints, one per line, computed `{days:…}` figures blanked (they have their
    own rows and NOTICE-DATE)."""
    from render_readme import NOTICES_ON_PAGE
    hand = sorted((n for n in (cfg or {}).get("notices") or [] if isinstance(n, dict)), key=lambda n: n.get("n", 0))
    bodies = [re.sub(r"\{[a-z]+:[^}]*\}", lambda m: " " * len(m.group(0)), str(n.get("body") or ""))
              for n in hand[:NOTICES_ON_PAGE]]
    return "\n".join(bodies)


def uncovered(readme: str, rows: list[dict], text: str | None = None) -> list[str]:
    text = prose(readme) if text is None else text
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
    for hit in unbacked_claims(ctx.readme or "", rows):
        out.append(fail("FIGURES", f"{hit} says what a command does with no [[figures]] row behind it", "README.md"))
    for hit in uncovered(ctx.readme or "", rows):
        out.append(fail("FIGURES", f"{hit} is typed into the README with no [[figures]] row behind it", "README.md"))
    bodies = notice_bodies(ctx.cfg)
    for hit in uncovered("", rows, bodies):
        out.append(fail("FIGURES", f"{hit} is typed into a working rule with no [[figures]] row behind it", "chart.toml"))
    for f in (ctx.cfg or {}).get("figures") or []:
        if f.get("block") == "notices" and str(f.get("text") or "\0") not in bodies:
            out.append(fail("FIGURES", f"{f.get('text')!r} is marked for the working rules and no printed rule says it",
                            "chart.toml"))
    return out
