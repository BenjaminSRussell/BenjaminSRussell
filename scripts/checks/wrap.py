"""wrap — a flag never breaks in half on a phone (review round 10, the information designer). TIER render.

FLAG-WRAP (fail): in a paragraph or list item of the README's visible prose, an inline code span that begins with
  "-" (a flag a reader types: `--workers 1`, `--seeding-strategy none`, `--reset-delta`) wraps before its first
  space (or, with none, anywhere) at some phone width. A
  hyphen-minus is a soft wrap opportunity in CSS and nothing in GitHub's sanitised Markdown turns that off, so
  `--workers 1` split as "--" | "workers 1" at 360 px. render_readme.lever_line starts such a flag on its own line
  (<br>); this check measures it in Chromium (`render.mjs wrap`) at WIDTHS, with PADS side padding: 16 px, and 41 px
  (GitHub's profile box on a phone, checks/column.py: the column is the viewport less 82). CSS is GitHub's markdown
  body: 16 px text, `code` at 85 % in ui-monospace with `white-space: break-spaces` and .2em/.4em padding.
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import tempfile

from check import Finding, fail, info, error

TIER = "render"
WIDTHS = (320, 360, 375, 390, 412, 430)
PADS = (16, 41)
CSS = ('body{margin:0;font:16px/1.5 -apple-system,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;'
       'word-wrap:break-word}ul{padding-left:2em}code{font:85% ui-monospace,SFMono-Regular,Menlo,monospace;'
       'white-space:break-spaces;padding:.2em .4em}')
_FENCE = re.compile(r"^```.*?^```[ \t]*$", re.S | re.M)


def inline_html(md: str) -> str:
    """One line of Markdown as GitHub renders its inline parts (code spans, <br>, bold, links); the rest escaped."""
    parts = re.split(r"(`[^`]*`)", md)
    h = []
    for i, p in enumerate(parts):
        if i % 2:
            h.append(f"<code>{html.escape(p[1:-1])}</code>")
        else:
            p = html.escape(p, quote=False).replace("&lt;br&gt;", "<br>")
            p = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"<a>\1</a>", p)
            h.append(re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", p))
    return "".join(h)


def blocks_html(readme: str) -> list[tuple[str, str]]:
    """("li" | "p", html) for each list item and paragraph of the visible prose (fenced code, comments and lines that
    are HTML left out)."""
    t = re.sub(r"<!--.*?-->", "", _FENCE.sub("", readme or ""), flags=re.S)
    out = []
    for para in re.split(r"\n\s*\n", t):
        lines = [ln for ln in para.splitlines() if ln.strip() and not ln.lstrip().startswith("<")]
        if not lines:
            continue
        if all(ln.startswith("- ") for ln in lines):
            out += [("li", inline_html(ln[2:])) for ln in lines]
        else:
            out.append(("p", inline_html(" ".join(ln.strip() for ln in lines))))
    return out


def items_html(readme: str) -> list[str]:
    """The list items of the visible prose, as HTML (the cautions list among them)."""
    return [h for tag, h in blocks_html(readme) if tag == "li"]


def split_flags(rows: list[dict]) -> list[str]:
    """The measured rows where a code span that begins with "-" starts a new line before its first space."""
    out = []
    for r in rows:
        code, at = str(r.get("code") or ""), int(r.get("at", -1))
        if not code.startswith("-") or at < 0:
            continue
        first_space = code.find(" ")
        if first_space < 0 or at <= first_space:      # no space: the flag is one word, and any break splits it
            out.append(f"{code!r} splits as {code[:at]!r} | {code[at:]!r} at {r.get('width')} px "
                       f"(side padding {r.get('pad')} px)")
    return list(dict.fromkeys(out))


def measure(root: str, items: list) -> list[dict] | None:
    """`items`: HTML strings (list items) or (tag, HTML) pairs, as blocks_html gives them."""
    root = os.path.abspath(root)
    render = os.path.join(root, "scripts", "render.mjs")
    blocks = [{"tag": i[0], "html": i[1]} if isinstance(i, tuple) else {"tag": "li", "html": i} for i in items]
    spec = {"blocks": blocks, "widths": list(WIDTHS), "pads": list(PADS), "css": CSS}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(spec, fh)
        path = fh.name
    try:
        p = subprocess.run(["node", render, "wrap", path], cwd=root, capture_output=True, text=True, timeout=300)
    finally:
        os.unlink(path)
    if p.returncode != 0:
        return None
    return json.loads(p.stdout.strip().splitlines()[-1])


def check(ctx) -> list[Finding]:
    items = [b for b in blocks_html(ctx.readme or "") if "<code>-" in b[1]]
    if not items:
        return [info("FLAG-WRAP", "no flag in the README's prose", "README.md")]
    rows = measure(ctx.root, items)
    if rows is None:
        return [error("FLAG-WRAP", "render.mjs wrap failed", "README.md")]
    bad = split_flags(rows)
    if not bad:
        return [info("FLAG-WRAP", f"{len(items)} blocks with a flag: none splits before its first space at "
                     f"{', '.join(map(str, WIDTHS))} px", "README.md")]
    return [fail("FLAG-WRAP", b, "README.md") for b in bad]
