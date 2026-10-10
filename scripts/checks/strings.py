"""strings — the banned phrases, case-insensitive, over the SVGs, the report's text manifest,
README.md and chart.toml (T10 check 6 + STANDARDS 1); and, since v10 (round 4, D5: nothing unmeasured
is printed), no text run on the hero whose report `truth` is anything but measured.

Figures inside `<!-- n:key -->…<!-- /n -->` markers are build-written and exempt ("Oct 2024" is
banned as a hand-typed figure, not as a date).

STRINGS-TWICE (round 6, review 1: one home per fact): no run of more than TWICE_WORDS words appears both in the
hero's text and in README.md's visible text (the alt text, which repeats the image for screen readers by design, and
HTML comments are left out). The image keeps what a list cannot show; the text keeps what you copy or look up."""
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
PAGE_SHEETS = ("hero",)      # the sheets on the page; a figure there is measured or it is not printed
MEASURED = ("measured",)


def unmeasured(report: dict | None) -> list[Finding]:
    """Every text run on a page sheet whose `truth` is set and is not measured (illustrative, computed…)."""
    out: list[Finding] = []
    for name, e in (report or {}).get("sheets", {}).items():
        if name.split("-")[0] not in PAGE_SHEETS:
            continue
        for t in e.get("text", []):
            if not isinstance(t, dict):
                continue
            truth = t.get("truth")
            if truth is not None and str(truth) not in MEASURED:
                out.append(fail("STRINGS-UNMEASURED", f"{str(t.get('s', ''))!r} is {truth}, not measured (D5)", name))
    return out


TWICE_WORDS = 4
_WORD = re.compile(r"[a-z0-9][a-z0-9_.'/-]*[a-z0-9]|[a-z0-9]")


def _words(text: str) -> list[str]:
    return _WORD.findall(str(text or "").lower())


def readme_visible(readme: str) -> str:
    """README text a reader sees: comments, tags (with their alt and href attributes) and link targets removed."""
    t = re.sub(r"<!--.*?-->", " ", readme or "", flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\]\([^)]*\)", "] ", t)
    return t.replace("`", " ").replace("*", " ")


def twice(hero_text: list[str], readme: str, n: int = TWICE_WORDS + 1) -> list[str]:
    """The runs of `n` words found both in the hero's text runs (each run, and each element's runs joined in order)
    and in README.md's visible text."""
    page = _words(readme_visible(readme))
    grams = {tuple(page[i:i + n]) for i in range(len(page) - n + 1)}
    hits = []
    for chunk in hero_text:
        w = _words(chunk)
        for i in range(len(w) - n + 1):
            g = tuple(w[i:i + n])
            if g in grams and " ".join(g) not in hits:
                hits.append(" ".join(g))
    return hits


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
    out += unmeasured(ctx.report)
    if ctx.readme:
        for name, e in (ctx.report or {}).get("sheets", {}).items():
            if not name.startswith("hero-"):
                continue
            runs = [str(t.get("s", "")) for t in e.get("text", []) if isinstance(t, dict)]
            for hit in twice(runs + [" ".join(runs)], ctx.readme):
                out.append(fail("STRINGS-TWICE", f"{hit!r} is in the image and in the README: say it once", name))
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
