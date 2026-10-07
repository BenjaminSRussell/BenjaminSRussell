#!/usr/bin/env python3
"""render_readme.py — fill the README's build-written regions from chart.toml and stats.json.

    python3 scripts/render_readme.py            # rewrite README.md in place (only if it changes)
    python3 scripts/render_readme.py --check    # exit 1 and print a diff if README.md is stale
    python3 scripts/render_readme.py --stdout   # print the rendered README

Block markers (MASTERPLAN decision 3): `<!-- name:start -->…<!-- name:end -->` with names
`picture:<sheet>`, `position`, `contact`, `figures`, `notices`, `instruments`, `license`.
Inline figures: `<!-- n:key -->…<!-- /n -->`. The opening marker may carry a note after the name
(`<!-- contact:start — Ben: … -->`); it is kept verbatim. Everything outside the markers is T8's
and is never touched. Idempotent: rendering twice is a no-op.

A bare `<picture>` whose sources name a sheet (`…/hero-day.svg`) is wrapped in picture markers
on first run, so T8's template needs no hand edit.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import os
import re
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

ROOT = os.path.abspath(os.path.join(HERE, ".."))
README = os.path.join(ROOT, "README.md")
CFG = os.path.join(ROOT, "chart.toml")
STATS = os.path.join(ROOT, "assets", "stats.json")
SHEETS = ["hero", "soundings", "approaches", "log", "instruments", "footer"]
ALT_MAX_WORDS = 25

# decision 9: most specific first; the hero prepends the two phone stills.
SOURCES = [
    ("(max-width: {bp}px) and (prefers-color-scheme: dark)", "phone-night"),
    ("(max-width: {bp}px)", "phone-day"),
    ("(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)", "still-night"),
    ("(prefers-reduced-motion: reduce)", "still-day"),
    ("(prefers-color-scheme: dark)", "night"),
]
HERO_SOURCES = [
    ("(max-width: {bp}px) and (prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)", "phone-still-night"),
    ("(max-width: {bp}px) and (prefers-reduced-motion: reduce)", "phone-still-day"),
]


# ------------------------------------------------------------------ formatting

def fmt_n(n) -> str:
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


def fmt_date(s, month_only: bool = False) -> str:
    """'2026-10-07T06:34:12Z' → '7 Oct 2026'; '2024-10' → 'Oct 2024'; anything else passes through."""
    if not s:
        return ""
    s = str(s)
    m = re.match(r"^(\d{4})-(\d{2})(?:-(\d{2}))?", s)
    if not m:
        return s
    y, mo, d = int(m.group(1)), int(m.group(2)), m.group(3)
    try:
        date = dt.date(y, mo, int(d) if d else 1)
    except ValueError:
        return s
    if month_only or not d:
        return date.strftime("%b %Y")
    return f"{date.day} {date.strftime('%b %Y')}"


def fmt_time(s) -> str:
    m = re.search(r"T(\d{2}):(\d{2})", str(s or ""))
    return f"{m.group(1)}:{m.group(2)} UTC" if m else ""


def figures(stats: dict, cfg: dict) -> dict:
    """Every inline `n:key` the README may print, derived once (stats.json v1 and v2 keys)."""
    repos = stats.get("repos")
    repo_count = stats.get("repo_count") or (len(repos) if isinstance(repos, list) else repos) or 0
    commits = stats.get("commits")
    if isinstance(commits, dict):           # a T1-shaped draft: {"authored": …}
        commits = commits.get("authored") or commits.get("contributions") or 0
    since = stats.get("account_since") or stats.get("since") or ""
    taken = stats.get("taken") or stats.get("updated") or (stats.get("updated_at") or "")[:10]
    edition = stats.get("edition") or {}
    notices = list(cfg.get("notices", [])) + [n for n in stats.get("notices", []) if n.get("source") != "toml"]
    f = {
        "commits": fmt_n(commits or 0),
        "all_hands": fmt_n(stats.get("all_hands") or stats.get("commits_surveyed") or 0),
        "calendar_total": fmt_n(stats.get("calendar_total") or 0),
        "repo_count": str(repo_count),
        "chart_no": str(repo_count),
        "followers": fmt_n(stats.get("followers") or 0),
        "stars": fmt_n(stats.get("stars") or 0),
        "account_since": fmt_date(since, month_only=True) if re.match(r"^\d{4}-", str(since)) else str(since),
        "taken": fmt_date(taken),
        "taken_time": fmt_time(stats.get("updated_at")),
        "updated_at": str(stats.get("updated_at") or taken),
        "edition_version": str(edition.get("version") or ""),
        "edition_date": fmt_date(edition.get("date")),
        "edition_project": str(edition.get("project") or ""),
        "notices_n": str(len(notices)),
        "name": "Ben Russell",
        "login": cfg.get("chart", {}).get("login", ""),
        "release": cfg.get("chart", {}).get("release", ""),
    }
    f["edition"] = f["edition_version"]
    return f


class _Safe(dict):
    def __missing__(self, key):
        return "{" + key + "}"


# ------------------------------------------------------------------ pieces

def picture(sheet: str, cfg: dict, alt: str) -> str:
    base = cfg["chart"]["base_url"].rstrip("/") + "/"
    bp = cfg["chart"].get("breakpoint_px", 767)
    srcs = (HERO_SOURCES if sheet == "hero" else []) + SOURCES
    lines = ["<picture>"]
    for media, ed in srcs:
        lines.append(f'<source media="{media.format(bp=bp)}" srcset="{base}{sheet}-{ed}.svg">')
    alt_attr = alt.replace("&", "&amp;").replace('"', "&quot;")
    lines.append(f'<img src="{base}{sheet}-day.svg" width="100%" alt="{alt_attr}">')
    lines.append("</picture>")
    return "\n".join(lines)


def alt_for(sheet: str, stats: dict, cfg: dict, figs: dict, use_sheets: bool = True) -> str:
    if use_sheets:
        try:
            import importlib
            mod = importlib.import_module(f"sheets.{sheet}")
            s = str(mod.alt(stats, cfg)).strip()
            if s:
                return s
        except Exception:
            pass
    tmpl = cfg.get("alt", {}).get(sheet, "")
    return tmpl.format_map(_Safe(figs)).strip()


def position_block(cfg: dict) -> str:
    text = (cfg.get("position", {}).get("text") or "").strip()
    return f'<p align="center">{text}</p>' if text else ""


def contact_block(cfg: dict) -> str:
    c = cfg.get("contact", {})
    links = []
    if c.get("linkedin"):
        links.append(f'<a href="{c["linkedin"]}">LinkedIn</a>')
    if c.get("resume"):
        links.append(f'<a href="{c["resume"]}">Résumé</a>')
    return "\n  &nbsp;·&nbsp;\n  ".join(links)


def n(key: str, value: str) -> str:
    return f"<!-- n:{key} -->{value}<!-- /n -->"


def figures_block(figs: dict) -> str:
    parts = [f"{n('commits', figs['commits'])} commits of mine",
             f"{n('all_hands', figs['all_hands'])} all hands",
             f"{n('repo_count', figs['repo_count'])} repositories surveyed"]
    if figs["account_since"]:
        parts.append(f"since {n('account_since', figs['account_since'])}")
    if figs["taken"]:
        parts.append(f"soundings taken {n('taken', figs['taken'])}")
    return "<sub>" + " · ".join(parts) + "</sub>"


def notices_block(cfg: dict, stats: dict) -> str:
    rows = []
    hand = sorted(cfg.get("notices", []), key=lambda x: x.get("n", 0))
    for i, nt in enumerate(hand, 1):
        body = f" {nt['body']}" if nt.get("body") else ""
        cite = f" *{nt['cite']}*" if nt.get("cite") else ""
        rows.append(f"{nt.get('n', i)}. **{nt['title']}**{body}{cite}")
    hand_titles = {h.get("title", "").strip() for h in hand}
    # stats.json carries the hand notices too (source "hand"/"toml"); the README prints chart.toml's richer
    # copy above, and folds the dated release notices (PyPI uploads, GitHub Releases) into one trailing line
    # so "five principles" stays five (reviewer 18).
    releases = [nt for nt in stats.get("notices", [])
                if nt.get("source") not in ("toml", "hand") and (nt.get("title") or "").strip() not in hand_titles]
    if releases:
        first, last = len(hand) + 1, len(hand) + len(releases)
        links = []
        for nt in releases:
            title = nt.get("title") or f"{nt.get('repo', '')} {nt.get('tag', '')}".strip()
            short = title.replace(" on PyPI", "")
            links.append(f"[{short}]({nt['url']})" if nt.get("url") else short)
        dates = sorted({fmt_date(nt.get("date")) for nt in releases if nt.get("date")})
        when = dates[0] if len(dates) == 1 else f"{dates[0]} – {dates[-1]}"
        rng = f"Notice {first}" if first == last else f"Notices {first}–{last}"
        rows.append(f"\n<sub>{rng}, editions: {' · '.join(links)} · *{when}*.</sub>")
    return "\n".join(rows)


def fittings_of(cfg: dict) -> tuple[list[tuple[str, str]], list[dict]]:
    f = cfg.get("fittings", {})
    groups = [tuple(g) for g in f.get("groups", [["LEAD", "Languages"], ["LOG", "Stores and queues"], ["LOOKOUT", "Deck"]])]
    return groups, list(f.get("items", []))


def instruments_block(cfg: dict, fittings: list[dict] | None = None) -> str:
    groups, items = fittings_of(cfg)
    items = fittings if fittings is not None else items
    cols = []
    for code, label in groups:
        # "Parquet · Arrow" would blur into the " · " separator: the mirror says "Parquet and Arrow"
        names = [it["name"].replace(" · ", " and ") for it in items if it.get("group") == code]
        if names:
            cols.append(f"<b>{label}</b> {' · '.join(names)}")
    return "<sub>" + " &nbsp;&nbsp; ".join(cols) + "</sub>"


LICENSE_LINE = ("- **License.** Code MIT; sheets and copy CC BY 4.0; fonts under their own licenses in "
                "[`scripts/fonts/`](scripts/fonts/). To draw your own, fork the repository, fill in `chart.toml` "
                "and run the workflow; the sheets redraw from your repositories.")


def license_block(root: str = ROOT) -> str:
    have = all(os.path.exists(os.path.join(root, f)) for f in ("LICENSE", "LICENSE-ASSETS.md", "chart.toml"))
    return LICENSE_LINE if have else ""


# ------------------------------------------------------------------ markers

def _block_re(name: str) -> re.Pattern:
    esc = re.escape(name)
    return re.compile(rf"(<!--\s*{esc}:start\b[^>]*-->)(.*?)(<!--\s*{esc}:end\s*-->)", re.S)


def fill_block(text: str, name: str, content: str) -> tuple[str, bool]:
    """Replace the body of one block; keep its opening and closing markers. Returns (text, found)."""
    pat = _block_re(name)
    if not pat.search(text):
        return text, False
    body = f"\n{content}\n" if content else "\n"

    def sub(m: re.Match) -> str:
        return f"{m.group(1)}{body}{m.group(3)}"

    return pat.sub(sub, text, count=1), True


def fill_inline(text: str, key: str, value: str) -> tuple[str, int]:
    pat = re.compile(rf"(<!--\s*n:{re.escape(key)}\s*-->)(.*?)(<!--\s*/n\s*-->)", re.S)
    return pat.subn(lambda m: f"{m.group(1)}{value}{m.group(3)}", text)


def inline_keys(text: str) -> list[str]:
    return sorted(set(re.findall(r"<!--\s*n:([\w.-]+)\s*-->", text)))


_PICTURE_RE = re.compile(r"^<picture>.*?</picture>", re.S | re.M)    # element at line start; a `<picture>` in prose is not one


def migrate_pictures(text: str, sheets: list[str] = SHEETS) -> str:
    """Wrap bare <picture> elements that name a sheet in `picture:<sheet>` markers (once)."""
    def sub(m: re.Match) -> str:
        block = m.group(0)
        for sheet in sheets:
            if re.search(rf"/{re.escape(sheet)}-(?:day|night|light|dark)[\w-]*\.svg", block):
                before = text[max(0, m.start() - 80):m.start()]
                if f"picture:{sheet}:start" in before:
                    return block
                return f"<!-- picture:{sheet}:start -->\n{block}\n<!-- picture:{sheet}:end -->"
        return block
    return _PICTURE_RE.sub(sub, text)


# ------------------------------------------------------------------ main

def main(readme: str, cfg: dict, stats: dict, fittings: list[dict] | None = None, root: str = ROOT,
         use_sheet_alts: bool = True, warnings: list[str] | None = None) -> str:
    warnings = warnings if warnings is not None else []
    figs = figures(stats, cfg)
    text = migrate_pictures(readme)
    for sheet in SHEETS:
        alt = alt_for(sheet, stats, cfg, figs, use_sheet_alts)
        if len(alt.split()) > ALT_MAX_WORDS:
            warnings.append(f"alt for {sheet} is {len(alt.split())} words (> {ALT_MAX_WORDS})")
        if alt and alt.split()[0].lower() == "the":
            warnings.append(f"alt for {sheet} starts with 'The'")
        text, _ = fill_block(text, f"picture:{sheet}", picture(sheet, cfg, alt))
    text, _ = fill_block(text, "position", position_block(cfg))
    text, _ = fill_block(text, "contact", contact_block(cfg))
    text, _ = fill_block(text, "figures", figures_block(figs))
    text, _ = fill_block(text, "notices", notices_block(cfg, stats))
    text, _ = fill_block(text, "instruments", instruments_block(cfg, fittings))
    text, _ = fill_block(text, "license", license_block(root))
    for key in inline_keys(text):
        if key in figs:
            text, _ = fill_inline(text, key, figs[key])
        else:
            warnings.append(f"inline marker n:{key} has no figure; left as written")
    return text


def load(cfg_path: str = CFG, stats_path: str = STATS) -> tuple[dict, dict]:
    import json
    with open(cfg_path, "rb") as fh:
        cfg = tomllib.load(fh)
    with open(stats_path, encoding="utf-8") as fh:
        stats = json.load(fh)
    return cfg, stats


def cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="fill README.md's build-written regions")
    ap.add_argument("--readme", default=README)
    ap.add_argument("--cfg", default=CFG)
    ap.add_argument("--stats", default=STATS)
    ap.add_argument("--check", action="store_true", help="exit 1 with a diff if the README is stale")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing")
    ap.add_argument("--no-sheet-alts", action="store_true", help="use [alt] templates, not sheets' alt()")
    a = ap.parse_args(argv)
    cfg, stats = load(a.cfg, a.stats)
    with open(a.readme, encoding="utf-8") as fh:
        before = fh.read()
    warnings: list[str] = []
    after = main(before, cfg, stats, root=os.path.dirname(os.path.abspath(a.readme)) if a.readme != README else ROOT,
                 use_sheet_alts=not a.no_sheet_alts, warnings=warnings)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    if a.stdout:
        sys.stdout.write(after)
        return 0
    if after == before:
        print("README.md is current")
        return 0
    if a.check:
        sys.stdout.writelines(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                                   "README.md (committed)", "README.md (rendered)"))
        return 1
    with open(a.readme, "w", encoding="utf-8") as fh:
        fh.write(after)
    print(f"wrote {os.path.relpath(a.readme, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(cli())
