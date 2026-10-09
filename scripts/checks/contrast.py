"""contrast — token-level colour rules (T10 checks 8 and 9).

Text ink against paper and land: WCAG ≥ 4.5:1 for ink/ink2 (body sizes), ≥ 3:1 for muted
(captions, ≥ 24 px or texture only); coastline/index contour (ink2) and the danger line (accent)
≥ 3:1 on paper. Red and green marks keep an OKLab lightness gap (≥ .06 day, ≥ .10 night) and are
told apart under deutan/protan simulation (ΔE_ok ≥ .06). Night: the lights (flare, light_core,
accent, ok) are lighter than every text fill. Lights brighter than text is also checked on the
report's lights[] when a sheet fills it."""
from __future__ import annotations

import re

import tokens
from check import Finding, fail, warn

TIER = "fast"


def _srgb(hexs: str) -> tuple[float, float, float]:
    h = hexs.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(hexs: str) -> float:
    r, g, b = (_lin(c) for c in _srgb(hexs))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag(a: str, b: str) -> float:
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def oklab(hexs: str) -> tuple[float, float, float]:
    r, g, b = (_lin(c) for c in _srgb(hexs))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def de_ok(a: str, b: str) -> float:
    la, lb = oklab(a), oklab(b)
    return sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5


# Machado et al. 2009 severity-1.0 matrices in linear RGB
_DEUTAN = ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881))
_PROTAN = ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998))


def _simulate(hexs: str, m) -> str:
    lin = [_lin(c) for c in _srgb(hexs)]
    out = []
    for row in m:
        v = sum(a * b for a, b in zip(row, lin))
        v = min(1.0, max(0.0, v))
        v = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out.append(round(v * 255))
    return "#%02X%02X%02X" % tuple(out)


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    for ed_name, th in tokens.THEMES.items():
        night = ed_name == "night"
        for ground_name in ("paper", "land"):
            ground = getattr(th, ground_name)
            # round 6: muted carries 19 px text on the hero (the title block), so it needs 4.5:1 on paper too
            for ink_name, floor in (("ink", 4.5), ("ink2", 4.5), ("muted", 4.5 if ground_name == "paper" else 3.0)):
                c = wcag(getattr(th, ink_name), ground)
                if c < floor:
                    out.append(fail("CONTRAST-TEXT", f"{ed_name}: {ink_name} on {ground_name} is {c:.2f}:1 < {floor}:1"))
            for line_name in ("ink2", "accent", "flare"):   # flare: the route's track and bars (round 6)
                c = wcag(getattr(th, line_name), ground)
                if c < 3.0:
                    out.append(fail("CONTRAST-LINE", f"{ed_name}: {line_name} line on {ground_name} is {c:.2f}:1 < 3:1"))
        # tints must stay lighter/darker than paper in the right direction, and distinct from land
        for tint in ("shallow_a", "shallow_b"):
            if de_ok(getattr(th, tint), th.land) < 0.04:
                out.append(fail("CONTRAST-TINT", f"{ed_name}: {tint} is indistinguishable from land (ΔE_ok < .04)"))
        # red / green
        gap = abs(oklab(th.accent)[0] - oklab(th.ok)[0])
        need = 0.10 if night else 0.06
        if gap < need:
            out.append(fail("CONTRAST-RG", f"{ed_name}: red/green lightness gap {gap:.3f} < {need}"))
        for label, m in (("deutan", _DEUTAN), ("protan", _PROTAN)):
            d = de_ok(_simulate(th.accent, m), _simulate(th.ok, m))
            if d < 0.06:
                out.append(fail("CONTRAST-CVD", f"{ed_name}: red/green marks merge under {label} (ΔE_ok {d:.3f} < .06)"))
        if night:
            text_l = max(oklab(getattr(th, k))[0] for k in ("ink", "ink2", "muted"))
            light_l = max(oklab(getattr(th, k))[0] for k in ("flare", "light_core", "ok", "accent"))
            if light_l <= text_l:
                out.append(fail("CONTRAST-LIGHTS", f"night: brightest light L {light_l:.3f} ≤ brightest text L {text_l:.3f}"))
    # per-sheet lights[] when present
    report = ctx.report or {}
    for name, e in report.get("sheets", {}).items():
        if "night" not in name or name not in ctx.svgs:
            continue
        lights = e.get("lights") or []
        if not lights:
            continue
        fills = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', ctx.svg_text(name)))
        th = tokens.THEMES["night"]
        text_fills = {f for f in fills if f.upper() in {th.ink.upper(), th.ink2.upper(), th.muted.upper()}}
        text_l = max((oklab(f)[0] for f in text_fills), default=0.0)
        for lt in lights:
            col = lt.get("color")
            if col and oklab(col)[0] <= text_l:
                out.append(fail("CONTRAST-LIGHT", f"light {lt.get('id')} {col} is not lighter than the text", name))
    return out
