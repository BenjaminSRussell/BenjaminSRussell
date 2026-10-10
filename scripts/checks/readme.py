"""readme — README.md structure (reviewer 18's finding on the colophon).

The hero's picture block is required; any other sheet's block is checked only when the README carries
it (round 4, D1: the page is the hero and written text; the supporting sheets are off the page). Each
block has exactly one start and one end marker and a <picture> that opens and closes inside it; no
picture block inside <details>; <details> balanced; the license block present when LICENSE and
LICENSE-ASSETS.md exist; render_readme --check clean (the committed README is what the renderer
would write). Round 6, review 1: no line of a fenced code block is over CODE_COLUMNS characters (a 375 px phone
shows about 38 columns of GitHub's code font; a longer line hides its end, which is where the warnings were), except a
line that is one unbreakable URL."""
from __future__ import annotations

import os
import re

from check import Finding, fail, warn

TIER = "fast"
REQUIRED = ("hero",)
CODE_COLUMNS = 38
_FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.S | re.M)


def code_too_wide(text: str, limit: int = CODE_COLUMNS) -> list[tuple[int, str]]:
    """(line number, line) for every fenced-block line over `limit` characters that is not one bare URL."""
    out = []
    for m in _FENCE.finditer(text or ""):
        first = text.count("\n", 0, m.start(1)) + 1
        for i, ln in enumerate(m.group(1).splitlines()):
            bare = ln.strip()
            if len(ln) > limit and not (re.fullmatch(r"https?://\S+", bare)):
                out.append((first + i, ln))
    return out


def page_sheets(text: str) -> list[str]:
    found = re.findall(r"<!--\s*picture:([\w-]+):(?:start|end)\b", text)
    return list(REQUIRED) + [s for s in dict.fromkeys(found) if s not in REQUIRED]


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    text = ctx.readme or ""
    if not text:
        return [warn("README-MISSING", "README.md not found")]
    for sheet in page_sheets(text):
        starts = len(re.findall(rf"<!--\s*picture:{sheet}:start\b", text))
        ends = len(re.findall(rf"<!--\s*picture:{sheet}:end\s*-->", text))
        if starts != 1 or ends != 1:
            out.append(fail("README-PICTURE", f"picture:{sheet} has {starts} start / {ends} end markers (want 1/1)", "README.md"))
            continue
        m = re.search(rf"<!--\s*picture:{sheet}:start\b[^>]*-->(.*?)<!--\s*picture:{sheet}:end\s*-->", text, re.S)
        body = m.group(1) if m else ""
        if body.count("<picture>") != 1 or body.count("</picture>") != 1:
            out.append(fail("README-PICTURE", f"picture:{sheet} block does not hold exactly one <picture>", "README.md"))
        if f"{sheet}-day.svg" not in body:
            out.append(fail("README-PICTURE", f"picture:{sheet} block does not reference {sheet}-day.svg", "README.md"))
    # picture blocks outside <details>
    depth = 0
    for i, ln in enumerate(text.splitlines(), 1):
        depth += ln.count("<details>") - ln.count("</details>")
        if depth < 0:
            out.append(fail("README-DETAILS", f"</details> without <details> at line {i}", "README.md"))
            depth = 0
        if "picture:" in ln and ":start" in ln and depth > 0:
            out.append(fail("README-PICTURE-FOLDED", f"a picture block opens inside <details> at line {i}", "README.md"))
    if depth != 0:
        out.append(fail("README-DETAILS", f"<details> left open ({depth})", "README.md"))
    for line_no, ln in code_too_wide(text):
        out.append(fail("README-CODE-WIDTH", f"line {line_no} of a code block is {len(ln)} characters (> {CODE_COLUMNS}): "
                        f"{ln.strip()[:60]!r}", "README.md"))
    root = getattr(ctx, "root", ".")
    if all(os.path.exists(os.path.join(root, f)) for f in ("LICENSE", "LICENSE-ASSETS.md")):
        m = re.search(r"<!--\s*license:start\b[^>]*-->(.*?)<!--\s*license:end\s*-->", text, re.S)
        if not m or "License" not in m.group(1):
            out.append(fail("README-LICENSE", "LICENSE files exist but the License bullet is not rendered", "README.md"))
    try:
        import render_readme as rr
        cfg, stats = rr.load()
        rendered = rr.main(text, cfg, stats)
        if rendered != text:
            out.append(fail("README-STALE", "README.md differs from what render_readme.py would write; run it", "README.md"))
    except Exception as exc:  # the renderer is a collaborator
        out.append(warn("README-RENDER", f"could not re-render README for the staleness check: {exc}", "README.md"))
    return out
