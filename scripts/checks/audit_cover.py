"""audit_cover — every figure the page prints has a row in docs/data/AUDIT.md §7 (review round 7, review 2).

AUDIT-COVER (fail): a run of digits in the hero's text (every edition's text manifest in the build report) or in the
  README's visible text that no register row covers. A hero run is covered when its manifest key is one a row names
  (`hero_keys`: the release label, each route entry whose wording reads a figure, the hand-off). A README digit is
  covered when it sits inside a match of a row's `covers` pattern (the build-written blocks), inside the printed
  text of a route `text` entry that has a row (L1, X1), of a holding [[figures]] row, or of a rule's filled cite.
  Ordered-list numbers, link targets, comments and tags are not printed figures; repository names (3d-swift-widget)
  and joined tokens (x86_64, 4-core) are not figures either (the FIGURES check's NUMBER rule).
"""
from __future__ import annotations

import re

from check import Finding, fail

TIER = "fast"
DIGITS = re.compile(r"(?<![A-Za-z0-9_\-])\d+(?:,\d{3})*(?:\.\d+)*(?![A-Za-z0-9_\-])")


def visible(readme: str) -> str:
    t = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), readme or "", flags=re.S)
    t = re.sub(r"<[^>]+>", lambda m: " " * len(m.group(0)), t)
    t = re.sub(r"\]\([^)]*\)", lambda m: " " * len(m.group(0)), t)
    t = re.sub(r"^\d+\.(?= )", lambda m: " " * len(m.group(0)), t, flags=re.M)     # ordered-list numbers
    t = t.replace("&nbsp;", "      ")
    return t.replace(" ", " ").replace("*", " ")


def readme_spans(readme: str, recs: list[dict], stats: dict, cfg: dict) -> list[tuple[int, int]]:
    text = visible(readme)
    spans: list[tuple[int, int]] = []

    def literal(s: str) -> None:
        s = str(s or "").replace(" ", " ").replace("*", " ")
        # review round 15: a placeholder in angle brackets (`<your-bot>`) is a tag to visible(), so it is to the literal
        s = re.sub(r"<[^>]+>", " ", s)
        if not s.strip():
            return
        # review round 10: any run of white space matches any other (an item's <br> is blanked to four spaces)
        for m in re.finditer(r"\s+".join(re.escape(w) for w in s.split()), text):
            spans.append((m.start(), m.end()))
    for r in recs:
        for pat in r.get("covers") or ():
            for m in re.finditer(pat, text):
                spans.append((m.start(), m.end()))
    # the route's README sentences, as printed, for each entry with a row
    entries_with_rows = {r["entry"] for r in recs if r.get("entry")}
    ed = stats.get("edition") or {}
    for name, route in (stats.get("routes") or {}).items():
        rc = (stats.get("runcheck") or {}).get(name)
        try:
            from data import route as route_mod
            drawn = route_mod.drawn(route, rc)
        except Exception:
            drawn = []
        for e in drawn:
            if e.get("id") in entries_with_rows and e.get("kind") == "text":
                literal(str(e.get("text") or "").replace("{release}", str(ed.get("version") or "")))
    figs = {r.get("figure") for r in recs if r.get("figure")}
    for f in stats.get("figures") or []:
        if f.get("holds") and f.get("text") in figs:
            literal(f["text"])
    from data import proof
    for nt in cfg.get("notices") or []:
        if any(r.get("rule") == int(nt.get("n") or 0) for r in recs):
            filled, missing = proof.fill_cite(nt.get("cite") or "", int(nt.get("n") or 0), stats.get("rules") or [])
            if not missing:
                literal(filled)
            body, no_days = proof.fill_days(nt.get("body") or "", int(nt.get("n") or 0), stats.get("rules") or [])
            if not no_days and "{days:" in str(nt.get("body") or ""):
                literal(body)        # review round 8: the rule's day counts, with their rows
    return spans


def uncovered_readme(readme: str, recs: list[dict], stats: dict, cfg: dict) -> list[str]:
    text = visible(readme)
    spans = readme_spans(readme, recs, stats, cfg)
    out = []
    for m in DIGITS.finditer(text):
        if not any(a <= m.start() and m.end() <= b for a, b in spans):
            out.append(f"{m.group(0)!r} in “…{text[max(0, m.start() - 30):m.end() + 30].strip()}…”".replace("\n", " "))
    return out


def uncovered_hero(report: dict | None, recs: list[dict]) -> list[str]:
    keys = {k for r in recs for k in r.get("hero_keys") or ()}
    out = []
    for name, e in ((report or {}).get("sheets") or {}).items():
        if not name.startswith("hero"):
            continue
        for t in e.get("text") or []:
            if not isinstance(t, dict):
                continue
            s, key = str(t.get("s") or ""), str(t.get("key") or "")
            if DIGITS.search(s) and key not in keys:
                out.append(f"{name}: {s!r} ({key})")
    return out


def check(ctx) -> list[Finding]:
    import audit_figures
    recs = audit_figures.records(ctx.cfg or {}, ctx.stats)
    out: list[Finding] = []
    for hit in uncovered_hero(ctx.report, recs):
        out.append(fail("AUDIT-COVER", f"{hit} prints a figure with no row in AUDIT.md §7", "build report"))
    for hit in uncovered_readme(ctx.readme or "", recs, ctx.stats or {}, ctx.cfg or {}):
        out.append(fail("AUDIT-COVER", f"{hit} prints a figure with no row in AUDIT.md §7", "README.md"))
    return out
