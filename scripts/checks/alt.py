"""alt — alt texts and their plain twins in README.md (T10 check 11).

Each <img alt> ≤ 25 words, first word not "The", last sentence ≤ 10 words; every H2 carries a
<sub> gloss; a plain paragraph (<sub>, <p> or body text) within 3 lines after each </picture>;
the six last sentences are the alt poem and must equal chart.toml alt_poem (printed as info)."""
from __future__ import annotations

import re

from check import Finding, fail, warn, info

TIER = "fast"


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    text = ctx.readme or ""
    if not text:
        return [warn("ALT-NO-README", "README.md not found")]
    alts = re.findall(r'<img[^>]*\balt="([^"]*)"', text)
    poem = []
    for alt in alts:
        words = alt.split()
        if len(words) > 25:
            out.append(fail("ALT-LONG", f"alt is {len(words)} words: {alt[:50]!r}…", "README.md"))
        if words and words[0].lower() == "the":
            out.append(fail("ALT-THE", f"alt starts with 'The': {alt[:50]!r}", "README.md"))
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", alt.strip()) if s.strip()]
        if sentences:
            last = sentences[-1]
            if len(last.split()) > 10:
                out.append(fail("ALT-LAST", f"last sentence is {len(last.split())} words: {last!r}", "README.md"))
            poem.append(last)
    for m in re.finditer(r"^## (.*)$", text, re.M):
        if "<sub>" not in m.group(1):
            out.append(fail("ALT-GLOSS", f"H2 without a <sub> gloss: {m.group(1)!r}", "README.md"))
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if "</picture>" in ln:
            if any("footer-" in l for l in lines[max(0, i - 12):i]):
                continue        # the footer carries one line and nothing follows it (T8 §9)
            window = [l for l in lines[i + 1:i + 5] if l.strip() and not l.strip().startswith("<!--")]
            plain = any(re.search(r"[A-Za-z]{3,}", re.sub(r"<[^>]+>", " ", w)) for w in window[:3])
            if not plain and i + 1 < len(lines):
                out.append(fail("ALT-TWIN", f"no plain caption within 3 lines after the picture at line {i + 1}", "README.md"))
    want = list((ctx.cfg or {}).get("alt", {}).get("alt_poem", []))
    if want and poem != want:
        out.append(warn("ALT-POEM", "alt poem differs from chart.toml alt_poem:\n    " + "\n    ".join(poem)))
    else:
        out.append(info("ALT-POEM", " / ".join(poem)))
    return out
