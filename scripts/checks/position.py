"""position — the one line Ben must write himself (T10 check 12, T8 gate).

`[position] text` with ⟨ ⟩ → fail; "" → warning (the slot is omitted everywhere); non-empty → the
README's visible position line must equal it. Any ⟨ ⟩ placeholder left in README.md outside an
HTML comment fails, as does a `<!-- POSITION` comment. `[contact]` placeholders fail too."""
from __future__ import annotations

import re

from check import Finding, fail, warn

TIER = "fast"
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_TAG = re.compile(r"<[^>]+>")
_BLOCK = re.compile(r"<!--\s*position:start\b[^>]*-->(.*?)<!--\s*position:end\s*-->", re.S)


def visible(html: str) -> str:
    return re.sub(r"\s+", " ", _TAG.sub("", _COMMENT.sub("", html))).strip()


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    pos = ctx.cfg.get("position", {})
    text = pos.get("text") if isinstance(pos, dict) else None
    if text is None:
        out.append(fail("POSITION-UNSET", "[position] text is not set in chart.toml (write it, or set it to \"\")"))
    elif "⟨" in text or "⟩" in text:
        out.append(fail("POSITION-PLACEHOLDER", f"[position] text still holds a placeholder: {text!r}"))
    elif not text.strip():
        out.append(warn("POSITION-EMPTY", "[position] text is \"\": the position slot is omitted everywhere"))
    contact = ctx.cfg.get("contact", {})
    for k, v in (contact.items() if isinstance(contact, dict) else []):
        if isinstance(v, str) and ("⟨" in v or "⟩" in v):
            out.append(fail("CONTACT-PLACEHOLDER", f"[contact] {k} still holds a placeholder"))
    readme = ctx.readme
    if not readme:
        return out
    if "<!-- POSITION" in readme:
        out.append(fail("POSITION-COMMENT", "README.md carries a `<!-- POSITION` comment instead of a line"))
    stripped = _COMMENT.sub("", readme)
    for ch in ("⟨", "⟩"):
        if ch in stripped:
            line = stripped.count("\n", 0, stripped.index(ch)) + 1
            out.append(fail("README-PLACEHOLDER", f"{ch} placeholder in README.md near line {line}"))
            break
    m = _BLOCK.search(readme)
    if text and text.strip():
        if not m:
            out.append(fail("POSITION-BLOCK", "chart.toml has a position but README.md has no position:start/end block"))
        else:
            shown = visible(m.group(1))
            if shown != re.sub(r"\s+", " ", text).strip():
                out.append(fail("POSITION-MISMATCH", f"README shows {shown!r}, chart.toml says {text!r}"))
    elif m and visible(m.group(1)):
        out.append(warn("POSITION-STALE", f"position is \"\" but README.md still shows {visible(m.group(1))!r}; run render_readme.py"))
    return out
