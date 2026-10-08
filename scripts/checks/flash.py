"""flash — indefinite opacity loops are lights, not strobes (T10 check 15).

For each `<animate attributeName="opacity" repeatCount="indefinite">`: lit transitions per second
(changes between consecutive `values`, over `dur`) ≤ 3; the animated element's bounding size
(r, width/height, or the <use> symbol's) ≤ 2 % of the sheet area when it can be read; the
character printed next to the light (e.g. `Fl R 4s`, `Fl(2) 10s`, `Oc 4s`, `Iso 4s`, `Q`) parses
with timeline.flash's grammar when timeline is importable."""
from __future__ import annotations

import re

from check import Finding, fail, warn

TIER = "fast"
_ANIM = re.compile(r'<animate\b([^>]*)/?>', re.S)
_CHAR = re.compile(r'\b(L?Fl(?:\(\d\))?|Oc(?:\(\d\))?|Iso|Q|VQ)\s+([RGWY])?\s*(\d+(?:\.\d+)?)\s*s\b')


def _attr(s: str, k: str) -> str | None:
    m = re.search(rf'\b{k}="([^"]*)"', s)
    return m.group(1) if m else None


def _dur(s: str | None) -> float | None:
    if not s:
        return None
    m = re.match(r"\s*([\d.]+)\s*(ms|s|min)?", s)
    if not m:
        return None
    v = float(m.group(1))
    return v / 1000 if m.group(2) == "ms" else v * 60 if m.group(2) == "min" else v


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    try:
        import tokens
        periods = set(float(p) for p in tokens.LOOP_PERIODS)
    except Exception:
        periods = set()
    for name, path in ctx.svgs.items():
        svg = ctx.svg_text(name)
        vb = re.search(r'viewBox="\s*[\d.-]+\s+[\d.-]+\s+([\d.]+)\s+([\d.]+)"', svg)
        area = float(vb.group(1)) * float(vb.group(2)) if vb else None
        for m in _ANIM.finditer(svg):
            a = m.group(1)
            if _attr(a, "repeatCount") != "indefinite" or _attr(a, "attributeName") != "opacity":
                continue
            vals = [v.strip() for v in (_attr(a, "values") or "").split(";") if v.strip()]
            dur = _dur(_attr(a, "dur"))
            if not vals or not dur:
                continue
            trans = sum(1 for i in range(1, len(vals)) if vals[i] != vals[i - 1])
            rate = trans / dur
            if rate > 3.0:
                out.append(fail("FLASH-RATE", f"{rate:.1f} lit transitions/s > 3 (dur {dur}s, {trans} changes)", name))
            if periods and dur not in periods:
                out.append(fail("FLASH-PERIOD", f"loop period {dur}s not in {sorted(periods)}", name))
            # size of the parent element, when readable from the 300 chars before the animate
            head = svg[max(0, m.start() - 300):m.start()]
            parent = re.findall(r"<(circle|rect|use|path|g)\b([^>]*)>", head)
            if parent and area:
                tag, attrs = parent[-1]
                size = None
                if tag == "circle" and _attr(attrs, "r"):
                    r = float(_attr(attrs, "r"))
                    size = 3.1416 * r * r
                elif tag == "rect" and _attr(attrs, "width") and _attr(attrs, "height"):
                    size = float(_attr(attrs, "width")) * float(_attr(attrs, "height"))
                if size is not None and size > 0.02 * area:
                    out.append(fail("FLASH-SIZE", f"flashing {tag} covers {100 * size / area:.1f} % of the sheet > 2 %", name))
        # light characters printed on the sheet must be parseable
        try:
            import timeline
            flash_fn = getattr(timeline, "parse_character", None) or getattr(timeline, "parse_flash", None)
        except Exception:
            flash_fn = None
        if flash_fn is not None:
            texts = {r.get("s", "") for r in ((ctx.report or {}).get("sheets", {}).get(name, {}).get("text") or [])}
            for s in texts:
                for cm in _CHAR.finditer(s):
                    try:
                        flash_fn(cm.group(0))
                    except Exception as exc:
                        out.append(fail("FLASH-CHAR", f"light character {cm.group(0)!r} does not parse: {exc}", name))
    return out
