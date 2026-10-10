"""strings — the banned phrases, case-insensitive, over the SVGs, the report's text manifest,
README.md and chart.toml (T10 check 6 + STANDARDS 1); and, since v10 (round 4, D5: nothing unmeasured
is printed), no text run on the hero whose report `truth` is anything but measured.

Figures inside `<!-- n:key -->…<!-- /n -->` markers are build-written and exempt ("Oct 2024" is
banned as a hand-typed figure, not as a date).

STRINGS-TWICE (round 6, review 1: one home per fact): no run of more than TWICE_WORDS words, and (review 2) no
run of SHORT_WORDS words that names code or a date, appears both in the hero's text and in README.md's visible text (the alt text, which repeats the image for screen readers by design, and
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
SHORT_WORDS = 3          # review round 2: a run this short counts when it holds a code token or a date
TWICE_ALLOW = ("pip install rustmapper",)    # the image's one command is the entrance, and the code block copies it
_WORD = re.compile(r"(?:--)?[a-z0-9][a-z0-9_.'/-]*[a-z0-9]|[a-z0-9]")
MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")


def _words(text: str) -> list[str]:
    return _WORD.findall(str(text or "").lower().replace("\u2011", "-").replace("\u00a0", " "))


def code_or_date(gram: tuple[str, ...]) -> bool:
    """A run that names code (an identifier with `_`, a `--flag`, a .rs or .jsonl file) or carries a date (a month
    with a year): short, but a fact all the same."""
    if any("_" in w or w.startswith("--") or w.endswith(".rs") or ".jsonl" in w for w in gram):
        return True
    has_month = any(w[:3] in MONTHS and w.isalpha() for w in gram)
    has_year = any(re.fullmatch(r"(19|20)\d\d", w) for w in gram)
    return has_month and has_year


def readme_visible(readme: str) -> str:
    """README text a reader sees: comments, tags (with their alt and href attributes) and link targets removed."""
    t = re.sub(r"<!--.*?-->", " ", readme or "", flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\]\([^)]*\)", "] ", t)
    return t.replace("`", " ").replace("*", " ")


def twice(hero_text: list[str], readme: str, n: int = TWICE_WORDS + 1, short: int = SHORT_WORDS) -> list[str]:
    """The runs found both in the hero's text runs (each run, and each element's runs joined in order) and in
    README.md's visible text: any run of `n` words, and any run of `short` words that names code or a date
    (review round 2: "pip install rustmapper" is the one exception)."""
    page = _words(readme_visible(readme))
    hits = []
    for size, need in ((n, None), (short, code_or_date)):
        grams = {tuple(page[i:i + size]) for i in range(len(page) - size + 1)}
        for chunk in hero_text:
            w = _words(chunk)
            for i in range(len(w) - size + 1):
                g = tuple(w[i:i + size])
                if need and not need(g):
                    continue
                phrase = " ".join(g)
                if g in grams and phrase not in hits and not any(phrase in a for a in TWICE_ALLOW):
                    hits.append(phrase)
    return hits


def scan(text: str, where: str, code: str = "STRINGS-BANNED") -> list[Finding]:
    out = []
    text = str(text or "").replace("\u00a0", " ")     # review round 7: the README joins dates with U+00A0
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
