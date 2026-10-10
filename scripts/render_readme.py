#!/usr/bin/env python3
"""render_readme.py — fill the README's build-written regions from chart.toml and stats.json.

    python3 scripts/render_readme.py            # rewrite README.md in place (only if it changes)
    python3 scripts/render_readme.py --check    # exit 1 and print a diff if README.md is stale
    python3 scripts/render_readme.py --stdout   # print the rendered README

Block markers (MASTERPLAN decision 3): `<!-- name:start -->…<!-- name:end -->` with names
`picture:<sheet>`, `position`, `contact`, `notices`, `survey`, `license` (v10), `facts:<repo>` (v11, D4),
`install:<repo>` and `handoffs` (round 6), `pick` and `about:<repo>` (round 6, review 3); `figures`,
`instruments` and `log_lede` are still filled, empty, when a README carries them. A block the README
does not carry is skipped: since v10 (round 4, D1) the page is the hero and written text, and a
picture block is written only for a sheet whose markers are present. Inline figures:
`<!-- n:key -->…<!-- /n -->`. The opening marker may carry a note after the name
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
SHEETS = ["hero", "soundings", "approaches", "log", "instruments", "footer"]   # every sheet the build knows
ALT_MAX_WORDS = 25
NOTICES_ON_PAGE = 4          # round 4, D8: notices 1–4; no release line

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


NBSP = "\u00a0"
MONTHS_RX = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
UNITS = ("ms", "s", "min", "h", "characters", "MB")     # review round 7: kept on the line of their number


def fmt_date(s, month_only: bool = False) -> str:
    """'2026-10-07T06:34:12Z' → '7 Oct 2026'; '2024-10' → 'Oct 2024'; anything else passes through. Review round 7:
    joined by no-break spaces (U+00A0), so a phone never ends a line on "CI passed 8" (GitHub strips inline styles,
    so `white-space: nowrap` is not available)."""
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
        return date.strftime("%b") + NBSP + str(date.year)
    return f"{date.day}{NBSP}{date.strftime('%b')}{NBSP}{date.year}"


def keep_together(text: str) -> str:
    """Review round 7: dates ("7 Oct 2026", "Oct 2025"), a number and its unit ("3 min", "60 s", "50,000
    characters") and "16k lines of Rust" joined by U+00A0 in text the renderer writes. Code spans are left alone."""
    parts = re.split(r"(`[^`]*`)", str(text or ""))
    for i in range(0, len(parts), 2):
        s = parts[i]
        s = re.sub(rf"\b(\d{{1,2}}) ({MONTHS_RX}) (\d{{4}})\b", rf"\1{NBSP}\2{NBSP}\3", s)
        s = re.sub(rf"\b({MONTHS_RX}) (\d{{4}})\b", rf"\1{NBSP}\2", s)
        s = re.sub(rf"(\d[\d,.–]*) ({'|'.join(UNITS)})\b", rf"\1{NBSP}\2", s)
        s = re.sub(r"(\d[\d.]*[kM]?) lines of (\w+)", rf"\1{NBSP}lines{NBSP}of{NBSP}\2", s)
        parts[i] = s
    return "".join(parts)


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
    f["languages"] = languages_line(stats, cfg)
    return f


def languages_line(stats: dict, cfg: dict) -> str:
    """Review round 7: the Languages line from the data. chart.toml `[copy] languages_lead` first (each only while it
    is some repository's main_language), then every other `main_language` of his public repositories (the profile
    left out), by how many repositories have it, then by their lines in it: "Python, Rust; Swift, JavaScript,
    TypeScript, C, Go". `main_language` is the language with most lines at HEAD (data/tree.py)."""
    login = (cfg.get("chart") or {}).get("login") or stats.get("login")
    count: dict[str, int] = {}
    lines: dict[str, int] = {}
    for r in stats.get("repos") or []:
        if not isinstance(r, dict) or r.get("name") == login or not r.get("main_language"):
            continue
        lang = str(r["main_language"])
        count[lang] = count.get(lang, 0) + 1
        ln = r.get("lines") if isinstance(r.get("lines"), dict) else {}
        lines[lang] = lines.get(lang, 0) + (ln.get(lang) if isinstance(ln.get(lang), int) else 0)
    lead = [x for x in ((cfg.get("copy") or {}).get("languages_lead") or []) if x in count]
    rest = sorted((x for x in count if x not in lead), key=lambda x: (-count[x], -lines[x], x))
    if not lead:
        return ", ".join(rest)
    return ", ".join(lead) + ("; " + ", ".join(rest) if rest else "")


class _Safe(dict):
    def __missing__(self, key):
        return "{" + key + "}"


# ------------------------------------------------------------------ pieces

# round 6: the hero does not move, so it ships four editions and no reduced-motion sources
HERO_ROUTE_SOURCES = [
    ("(max-width: {bp}px) and (prefers-color-scheme: dark)", "phone-night"),
    ("(max-width: {bp}px)", "phone-day"),
    ("(prefers-color-scheme: dark)", "night"),
]


def hero_link(cfg: dict) -> str | None:
    """Review round 3: a tap on the hero opens the project it draws, not the raw SVG."""
    login = (cfg.get("chart") or {}).get("login")
    repo = next((r.get("repo") for r in ((cfg.get("route") or {}).values()) if isinstance(r, dict) and r.get("repo")), None)
    return f"https://github.com/{login}/{repo}" if login and repo else None


def picture(sheet: str, cfg: dict, alt: str, link: str | None = None) -> str:
    base = cfg["chart"]["base_url"].rstrip("/") + "/"
    bp = cfg["chart"].get("breakpoint_px", 767)
    srcs = HERO_ROUTE_SOURCES if sheet == "hero" else SOURCES
    lines = ([f'<a href="{link}">'] if link else []) + ["<picture>"]
    for media, ed in srcs:
        lines.append(f'<source media="{media.format(bp=bp)}" srcset="{base}{sheet}-{ed}.svg">')
    alt_attr = alt.replace("&", "&amp;").replace('"', "&quot;")
    # width="100%" and no height: D8 asked for width and height so the page does not jump, but GitHub's
    # markdown CSS (`img {max-width: 100%}` with no `height: auto`) keeps a pixel height while it narrows
    # the width, and the sheet letterboxes inside a column-wide × 740 px box. A ratio hint is not possible
    # without a style attribute, which GitHub strips.
    lines.append(f'<img src="{base}{sheet}-day.svg" width="100%" alt="{alt_attr}">')
    lines.append("</picture>")
    if link:
        lines.append("</a>")
    return "\n".join(lines)


def alt_for(sheet: str, stats: dict, cfg: dict, figs: dict, use_sheets: bool = True) -> str:
    if use_sheets:
        try:
            import importlib
            import build_assets
            mod = importlib.import_module(f"sheets.{build_assets.SHEET_MODULES.get(sheet, sheet)}")
            s = str(mod.alt(stats, cfg)).strip()
            if s:
                return s
        except Exception:
            pass
    tmpl = cfg.get("alt", {}).get(sheet, "")
    return tmpl.format_map(_Safe(figs)).strip()


def position_block(cfg: dict) -> str:
    """The position slot, its own line at the head of the link row (round 5, F3.1: the centred role caption under
    the image is cut, since the sheet prints the role line)."""
    text = (cfg.get("position", {}).get("text") or "").strip()
    return f"<i>{text}</i><br>" if text else ""


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


def figures_block(figs: dict) -> str:   # v9.2: sheet 2 is the source of its figures; no line under it
    return ""


def _figures_block_retired(figs: dict) -> str:
    parts = [f"{n('commits', figs['commits'])} commits of mine",
             f"{n('all_hands', figs['all_hands'])} all hands",
             f"{n('repo_count', figs['repo_count'])} repositories surveyed"]
    if figs["account_since"]:
        parts.append(f"since {n('account_since', figs['account_since'])}")
    if figs["taken"]:
        parts.append(f"soundings taken {n('taken', figs['taken'])}")
    return "<sub>" + " · ".join(parts) + "</sub>"


def notices_block(cfg: dict, stats: dict, limit: int = NOTICES_ON_PAGE) -> str:
    """The first `limit` hand notices from chart.toml, as the page prints them (v10: four, and no release
    line; the editions live in stats.json for the chart, not on the page). Review round 2: each cite's `{month:key}`
    is the month of his first commit adding the anchor (stats.json `rules`); a month not found prints "?", and
    NOTICE-DATE fails it."""
    from data import proof
    rows = []
    hand = sorted(cfg.get("notices", []), key=lambda x: x.get("n", 0))[:limit]
    for i, nt in enumerate(hand, 1):
        # review round 8: a body's `{days:…}` from the rule records (proof.fill_days); "?" fails NOTICE-DATE
        body = f" {keep_together(proof.fill_days(nt['body'], int(nt.get('n', i)), stats.get('rules') or [])[0])}" \
            if nt.get("body") else ""
        text, _missing = proof.fill_cite(nt.get("cite") or "", int(nt.get("n", i)), stats.get("rules") or [])
        cite = f" *{keep_together(text)}*" if text else ""
        rows.append(f"{nt.get('n', i)}. **{nt['title']}**{body}{cite}")
    return "\n".join(rows)


def fittings_of(cfg: dict) -> tuple[list[tuple[str, str]], list[dict]]:
    f = cfg.get("fittings", {})
    groups = [tuple(g) for g in f.get("groups", [["LEAD", "Languages"], ["LOG", "Stores and queues"], ["LOOKOUT", "Deck"]])]
    return groups, list(f.get("items", []))


def instruments_block(cfg: dict, fittings: list[dict] | None = None) -> str:   # v9.1: the sheet shows it; no mirror
    return ""


def _instruments_block_retired(cfg: dict, fittings: list[dict] | None = None) -> str:
    groups, items = fittings_of(cfg)
    items = fittings if fittings is not None else items
    cols = []
    for code, label in groups:
        # "Parquet · Arrow" would blur into the " · " separator: the mirror says "Parquet and Arrow"
        names = [it["name"].replace(" · ", " and ") for it in items if it.get("group") == code]
        if names:
            cols.append(f"<b>{label}</b> {' · '.join(names)}")
    return "<sub>" + " &nbsp;&nbsp; ".join(cols) + "</sub>"


# review round 3: whose license this is (not rustmapper's). Review round 4: the terms only; how the image is built is
# a "generated by" footer, and the data line already says what the drawing rests on (its word "drawing" links
# DESIGN.md)
LICENSE_LINE = ("<sub>**This profile** Code MIT; images and text CC BY 4.0; fonts under their own licenses in "
                "[`scripts/fonts/`](scripts/fonts/).</sub>")


# ------------------------------------------------------------------ D4: the facts line under a flagship

def _repo(stats: dict, name: str) -> dict | None:
    """The repository entry named `name` (or carrying it as an alias)."""
    for r in stats.get("repos") or []:
        if isinstance(r, dict) and (r.get("name") == name or name in (r.get("aliases") or [])):
            return r
    return None


def _count(v) -> int | None:
    """A count from an int, a list, or a dict holding one under count/files/n."""
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, (list, tuple)):
        return len(v)
    if isinstance(v, dict):
        for k in ("count", "files", "n", "total"):
            if isinstance(v.get(k), int):
                return v[k]
    return None


def _plural(n: int, one: str, many: str | None = None) -> str:
    return f"{fmt_n(n)} {one if n == 1 else (many or one + 's')}"


def fmt_k(n: int) -> str:
    """16,234 → 16k; 950 → 950; 1,200,000 → 1.2M."""
    if n >= 1_000_000:
        s = f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"{s}M"
    if n >= 1000:
        return f"{round(n / 1000)}k"
    return str(n)


HELPER_CRATE = re.compile(r"[_-](derive|macros)$", re.I)   # a helper crate that ships with the one it names


CI_WORDS = {"success": "passed", "failure": "failed", "cancelled": "cancelled", "timed_out": "timed out",
            "skipped": "skipped", "neutral": "passed", "action_required": "needs attention"}


def _dep_key(name: str) -> str:
    """PyPI and crates.io treat `-` and `_` alike and ignore case."""
    return re.sub(r"[-_.]+", "-", str(name)).lower()


def _in_manifest(name: str, deps: list[str]) -> bool:
    """`name` is in `deps` as itself, or as its `-binary` build (psycopg2 ships on PyPI as psycopg2-binary)."""
    keys = {_dep_key(d) for d in deps}
    return _dep_key(name) in keys or _dep_key(name) + "-binary" in keys


def built_on(r: dict, cfg: dict | None = None, names: tuple[str, ...] = ()) -> list[str]:
    """The dependencies worth naming: chart.toml `[facts] built_on.<repo>`, in that order, each only where the
    manifest has it; without a list, the first five manifest deps that are not helper crates."""
    man = r.get("manifest")
    if isinstance(man, dict):
        man = man.get("deps") or man.get("names") or man.get("top")
    deps = [str(d.get("name") if isinstance(d, dict) else d) for d in man if d] if isinstance(man, (list, tuple)) else []
    if not deps:
        return []
    lists = ((cfg or {}).get("facts") or {}).get("built_on") or {}
    for key in (r.get("name"), *names, *(r.get("aliases") or [])):
        if key and isinstance(lists.get(key), list):
            return [n for n in lists[key] if _in_manifest(n, deps)][:5]
    return [n for n in deps if not HELPER_CRATE.search(n)][:5]     # rkyv_derive is rkyv; tokio-macros is tokio


def facts_block(stats: dict, name: str, cfg: dict | None = None) -> str:
    """D4 / F3.3: one plain italic line under a flagship, from the D2 keys (docs/data/AUDIT.md):
    `Built on …` (chart.toml [facts] built_on, else the manifest's first five), `N tests` from `test_functions`
    (no item without it: a file count reads wrong for inline Rust tests), `CI passed <date>` from `ci`, the main
    language's lines from `lines` (`main_language` when present, else the largest). An item whose key is absent or null is left out, never estimated; no keys, no line."""
    r = _repo(stats, name)
    if not r:
        return ""
    parts: list[str] = []
    deps = built_on(r, cfg, (name,))
    if deps:
        parts.append(("built on " if (r.get("head") or {}).get("short") else "Built on ") + ", ".join(deps))
    tests = r.get("test_functions")
    if isinstance(tests, int) and not isinstance(tests, bool):
        item = _plural(tests, "test")
        # review round 7: "N tests" beside "CI passed" is read as N passing tests; say how many the passing
        # workflow's own commands do not select (repos[].ci_selection), when it is any
        sel = r.get("ci_selection") if isinstance(r.get("ci_selection"), dict) else {}
        ns = sel.get("not_selected")
        if isinstance(ns, int) and ns > 0 and sel.get("of") == tests and (r.get("ci") or {}).get("conclusion"):
            item += f" (CI selects all but {fmt_n(ns)})"
        parts.append(item)
    ci = r.get("ci")
    if isinstance(ci, str):
        ci = {"conclusion": ci}
    if isinstance(ci, dict) and ci.get("conclusion"):
        word = CI_WORDS.get(str(ci["conclusion"]).lower(), str(ci["conclusion"]).replace("_", " "))
        when = fmt_date(ci.get("date") or ci.get("at") or ci.get("run_at") or ci.get("updated_at"))
        item = f"CI {word}" + (f" {when}" if when else "")
        failed = [str(j.get("name")) for j in ci.get("jobs") or [] if str(j.get("conclusion")) == "failure"]
        if failed and str(ci["conclusion"]).lower() == "success":     # a job that may fail without failing the run
            item += f", {', '.join(failed)} failed (not blocking)"
        parts.append(item + (" (last known run)" if ci.get("stale") else ""))   # stale: the API did not answer this time
    else:
        wf = _count(r.get("workflows"))
        if wf:
            parts.append(_plural(wf, "CI workflow"))
    lic = r.get("license")
    if isinstance(lic, str) and lic and lic != "NOASSERTION":     # review round 3: only a license GitHub detects
        parts.append(f"{lic} license")
    lines = r.get("lines")
    if isinstance(lines, dict) and isinstance(lines.get("by_language"), dict):
        lines = lines["by_language"]
    if isinstance(lines, dict):
        langs = {k: v for k, v in lines.items() if isinstance(v, int) and v > 0 and k not in ("total", "all")}
        main = r.get("main_language")
        lang = main if main in langs else (max(langs, key=langs.get) if langs else None)
        if lang:
            parts.append(f"{fmt_k(langs[lang])} lines of {lang}")
    # round 6: no "last commit" date. It is sweep-adjusted, and beside a CI date and the code's own date it read as
    # inaccurate; the hero's code date answers "is it alive".
    if not parts:
        return ""
    # review round 2: the counts are main's, not the release's; say which snapshot they are
    head = (r.get("head") or {}).get("short")
    lead = f"On main at `{head}`: " if head else ""
    return "*" + lead + keep_together(" · ".join(p.replace("*", r"\*") for p in parts)) + "*"


def facts_repos(text: str) -> list[str]:
    """Every `facts:<repo>` block the README carries, in page order."""
    return list(dict.fromkeys(re.findall(r"<!--\s*facts:([\w.-]+):start\b", text)))


# ------------------------------------------------------------------ round 6: how to run it, where its output goes

def install_time(rc: dict | None) -> str | None:
    """The source build's time, only when the run check measured it cold (an empty CARGO_HOME, so every crate was
    downloaded inside the timed step): "3 min from a cold cache on a 4-core Linux x86_64 machine". None otherwise:
    a warm build says nothing about a stranger's first install."""
    if not isinstance(rc, dict) or rc.get("install") != "sdist (built with Rust)":
        return None
    st = next((x for x in rc.get("steps") or [] if x.get("id") == "install" and x.get("ok")), None)
    if not st or st.get("cache") != "cold" or not rc.get("runner"):
        return None
    runs = [float(t) for t in st.get("runs") or [] if isinstance(t, (int, float))] or \
        ([float(st["secs"])] if st.get("secs") is not None else [])
    if not runs:
        return None
    lo, hi = round(min(runs) / 60), round(max(runs) / 60)
    span = f"{lo} min" if lo == hi else f"{lo}–{hi} min"
    cores = f"{st['cpus']}-core " if isinstance(st.get("cpus"), int) else ""
    return f"{span} from a cold cache on a {cores}{rc['runner']} machine"


def _wheel_sentence(wheels, rc: dict | None = None) -> str:
    """The note under the install block, from the release's wheels, with the measured source-build time when the
    run check timed it cold (review round 2: the image no longer carries the install time)."""
    try:
        from data import route as route_mod
    except ImportError:
        return ""
    plats = route_mod.wheel_platforms(wheels)
    names = {n for n, _ in plats}
    if "any platform" in names or all(c in names for c in route_mod.COMMON):
        return ""
    t = install_time(rc)
    tail = f" ({t})" if t else ""
    if not plats:
        return f"No prebuilt wheel: `pip` builds it from source, which needs a Rust toolchain{tail}."
    friendly = {"macOS arm64": "Apple silicon", "macOS x86_64": "Intel Macs"}
    parts = []
    for n, v in plats:
        piece = f"{friendly.get(n, n)} on {v.replace('Python', 'CPython')}"
        if piece not in parts:
            parts.append(piece)
    return (f"Prebuilt for {' and '.join(parts)}; elsewhere `pip` builds it from source, which needs a Rust "
            f"toolchain{tail}.")


def install_block(stats: dict, repo: str, cfg: dict | None = None) -> str:
    """SPEC §4 block 5: the copyable lines, the command named as the release's wheel installs it (`edition.scripts`),
    the wheel note, and the cargo line once the route's `cargo` gate holds at HEAD. No release or no scripts: no
    block, never a guessed command."""
    ed = stats.get("edition") or {}
    route = next((r for r in (stats.get("routes") or {}).values() if isinstance(r, dict) and r.get("repo") == repo), None)
    if not ed.get("version") or not ed.get("scripts") or route is None:
        return ""
    try:
        from data import route as route_mod
        cmd = route_mod.command_name(ed.get("scripts"), ed.get("project") or "rustmapper")
    except Exception:
        return ""
    # no line over CODE_COLUMNS characters (checks/readme.py): a 360 px phone shows 32 columns of GitHub's code font
    rc = (stats.get("runcheck") or {}).get(ed.get("project") or "rustmapper")
    lines = ["```sh", f"pip install {ed.get('project') or 'rustmapper'}", f"{cmd} crawl \\",
             *(f"    {f} {v}" for f, v in BLOCK_CRAWL_FLAGS)]
    gates = route.get("gates") or {}
    lines += stop_lines(rc, gates)
    if (gates.get("export_defaults") or {}).get("ok"):
        # review round 4: the release's defaults (cli.rs ExportSitemap and Crawl, value-anchored) are these paths, so
        # the flags go; where it writes is said once, by the image's Ctrl-C row and the sentence under this block
        lines += [f"{cmd} export-sitemap"]
    else:
        lines += [f"{cmd} export-sitemap \\", "    --data-dir ./data \\", "    --output sitemap.xml"]
    gate = ((route.get("gates") or {}).get("cargo") or {})
    if gate.get("ok"):
        lines += ["", "# newer than the release:", "cargo install --git \\",
                  f"    https://github.com/{stats.get('login') or 'BenjaminSRussell'}/{repo}"]
    lines.append("```")
    # the wheel note, then (review round 3) what the release does to a site and to a big one, as its own paragraph
    # review round 8: an entry marked `para` starts a paragraph (what it does to a site; what it sees and writes)
    paras = [x for x in (_wheel_sentence(ed.get("wheels"), rc), *text_paragraphs(route, rc, ed, _repo(stats, repo)))
             if x]
    return "\n".join(lines) + "".join(f"\n\n{keep_together(x)}" for x in paras)


def stop_lines(rc: dict | None, gates: dict | None = None) -> list[str]:
    """Review round 4: the pasted crawl never returns, and a Ctrl-C flushes the rest of a paste (termios NOFLSH), so
    the block says how it ends: one comment line while the run check found that the crawl does not end by itself
    (`ends_by_itself` failed) and that one SIGINT writes the file (`crawl_ctrl_c` passed). Review round 5: the way
    back after a kill lives here too, above the export line, where the reader types, not in the image: "# sitemap.xml,
    even after a kill:" while a kill writes no file (`kill_writes_file` failed), the export on what it left wrote the
    pages (`export_after_kill` passed), and the release's export reads the stored state (release gate
    `export_after_kill`). Otherwise nothing."""
    steps = {s.get("id"): s for s in (rc or {}).get("steps") or [] if isinstance(s, dict)}
    ends, ctrl = steps.get("ends_by_itself"), steps.get("crawl_ctrl_c")
    out = []
    if ends is not None and not ends.get("ok") and ctrl is not None and ctrl.get("ok"):
        out.append("# stop it with one Ctrl-C")
    kill, after = steps.get("kill_writes_file"), steps.get("export_after_kill")
    gate = (gates or {}).get("export_after_kill") or {}
    if kill is not None and not kill.get("ok") and after is not None and after.get("ok") and gate.get("ok"):
        # review round 7: no colon, so the line is 32 columns and fits a 360 px phone
        out.append(f"# {_file_name((gate.get('values') or {}).get('arg:output') or './sitemap.xml')}, even after a kill")
    return out


def _file_name(path: str) -> str:
    """"./sitemap.xml" -> "sitemap.xml": a clap default as the reader would name the file."""
    return path[2:] if str(path).startswith("./") else str(path)


def text_paragraphs(route: dict | None, rc: dict | None, ed: dict | None, repo: dict | None = None) -> list[str]:
    """The text entries joined into paragraphs: a new one at each entry marked `para` (review round 8)."""
    out: list[list[str]] = [[]]
    for text, para in text_entries(route, rc, ed, repo, with_para=True):
        if para and out[-1]:
            out.append([])
        out[-1].append(text)
    return [" ".join(p) for p in out if p]


def text_entries(route: dict | None, rc: dict | None, ed: dict | None, repo: dict | None = None,
                 with_para: bool = False) -> list:
    """Review round 3: the route's `text` entries (how hard it hits a site; the release's single sitemap file), each
    printed only while its anchors hold, through the same engine as the image's rows; a retired one prints nothing,
    an unverified one nothing (ROUTE-UNVERIFIED fails it). Review round 5: an entry with `ci` (what main has fixed)
    prints only while CI passed at the sha the route was read at, with a job named `ci`* (`route.ci_ok`); `{head}`
    is that sha, short. Review round 6: an entry with `gate` prints only while that gate's record holds
    (`routes.<name>.gates[gate].ok`): M1 waits on `cargo`, as the cargo line does."""
    try:
        from data import route as route_mod
    except ImportError:
        return []
    out = []
    head = str((route or {}).get("head_sha") or "")[:7]
    for e in route_mod.drawn(route, rc):
        if e.get("kind") == "text" and str(e.get("text") or "").strip():
            if e.get("ci") and not route_mod.ci_ok(repo, (route or {}).get("head_sha"), str(e["ci"]))[0]:
                continue
            if e.get("gate") and not (((route or {}).get("gates") or {}).get(str(e["gate"])) or {}).get("ok"):
                continue
            text = str(e["text"]).replace("{release}", str((ed or {}).get("version") or "the release"))
            if "{head}" in text:
                if not head:
                    continue
                text = text.replace("{head}", head)
            out.append((text, bool(e.get("para"))) if with_para else text)
    return out


def install_repos(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"<!--\s*install:([\w.-]+):start\b", text)))


def handoffs_block(stats: dict, cfg: dict) -> str:
    """SPEC §4 block 8: one sentence per declared hand-off, following its computed state (handoffs[] in stats.json):
    `says_runs` when the receiving side's code proves the join, `says_not` otherwise ("" prints nothing)."""
    specs = {h.get("id"): h for h in cfg.get("handoffs") or [] if isinstance(h, dict)}
    out = []
    for h in stats.get("handoffs") or []:
        spec = specs.get(h.get("id")) or {}
        runs = h.get("state") == "runs"
        tmpl = spec.get("says_runs" if runs else "says_not") or ""
        if not tmpl:
            continue
        reader = h.get("reader") or ((h.get("readers") or [""])[0])
        out.append(tmpl.format_map(_Safe({"to": h.get("to") or "", "url": spec.get("url") or "", "reader": reader,
                                          "file": h.get("file") or ""})))
    return " ".join(out)


def pick_block(stats: dict, cfg: dict) -> str:
    """Review round 3: one sentence on which tool is for which job (chart.toml [copy] pick). Printed only while
    rustmapper's route header holds at HEAD and in the release (it writes one line per page: SitemapNode) and every
    [[figures]] row tagged `use = "pick"` holds at Scrapy's HEAD; otherwise nothing."""
    text = str((cfg.get("copy") or {}).get("pick") or "").strip()
    if not text:
        return ""
    route = (stats.get("routes") or {}).get("rustmapper") or {}
    if not route.get("header_verified"):
        return ""
    rows = [r for r in stats.get("figures") or [] if r.get("use") == "pick"]
    want = [f for f in cfg.get("figures") or [] if f.get("use") == "pick"]
    if len(rows) != len(want) or not all(r.get("holds") for r in rows):
        return ""
    # review round 4: "no services to run" rests on the release (Redis is an opt-in flag of its crawl)
    if "no services" in text and not ((route.get("gates") or {}).get("no_services") or {}).get("ok"):
        return ""
    return text


def about_block(stats: dict, name: str) -> str:
    """Review round 3: what rustmapper is, and what `pip install` gives you. The 0.1.3 wheel holds only the
    `rust_sitemap` binary (edition.modules is empty), so the Python API is called main's, and only while main has it
    (gate `python_api`). With a module in the wheel, it is a CLI and a Python API."""
    if name != "Rust-sitemap":
        return ""
    login = stats.get("login") or "BenjaminSRussell"
    # review round 6: one description per screen. The image's header and the pick sentence introduce the tool, and
    # the facts line says Rust, so this sentence says only what pip gives you
    link = f"**[rustmapper](https://github.com/{login}/{name})**"
    ed = stats.get("edition") or {}
    mods = ed.get("modules")
    route = next((r for r in (stats.get("routes") or {}).values() if isinstance(r, dict) and r.get("repo") == name), {})
    api_on_main = ((route.get("gates") or {}).get("python_api") or {}).get("ok")
    if isinstance(mods, list) and "rustmapper" in mods:
        return link + ": `pip install` gives you its command line and a Python API, built with maturin."
    if isinstance(mods, list) and api_on_main:
        return link + ": `pip install` gives you its command line; the Python API, built with maturin, is on main and not yet released."
    return link + ": `pip install` gives you its command line."


def about_repos(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"<!--\s*about:([\w.-]+):start\b", text)))


# ------------------------------------------------------------------ D5: the provenance line

def fmt_days(dates) -> str:
    """ISO dates → "9–10 Nov 2025, 1 and 7 Oct 2026": runs of consecutive days joined with an en dash, the rest
    with commas and "and", grouped by month."""
    days = []
    for d in dates or []:
        if isinstance(d, dict):
            d = d.get("date") or d.get("d")
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(d or ""))
        if m:
            days.append(dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    days = sorted(set(days))
    months: dict[tuple[int, int], list[str]] = {}
    i = 0
    while i < len(days):
        j = i
        while j + 1 < len(days) and days[j + 1] == days[j] + dt.timedelta(days=1) and days[j + 1].month == days[j].month:
            j += 1
        run = f"{days[i].day}–{days[j].day}" if j > i else str(days[i].day)
        months.setdefault((days[i].year, days[i].month), []).append(run)
        i = j + 1
    out = []
    for (y, mo), runs in months.items():
        label = dt.date(y, mo, 1).strftime("%b %Y")
        joined = runs[0] if len(runs) == 1 else ", ".join(runs[:-1]) + " and " + runs[-1]
        out.append(f"{joined} {label}")
    return ", ".join(out)


def sweep_dates(stats: dict) -> list:
    """`sweep_dates` (D2) when the builder writes it; else the dates of the `sweeps` entries it already writes."""
    if isinstance(stats.get("sweep_dates"), list):
        return stats["sweep_dates"]
    sw = stats.get("sweeps")
    if isinstance(sw, list):
        return [s.get("date") if isinstance(s, dict) else s for s in sw]
    return []


INSTRUMENT_WORDS = {"live": "live", "cache": "cached", "partial": "partial", "none": "not read"}
INSTRUMENT_NAMES = {"clones": "clones", "graphql": "GraphQL", "rest": "REST", "pypi": "PyPI", "releases": "releases"}


AGENT_SHORT = {"google-labs-jules": "jules", "copilot-swe-agent": "Copilot", "devin-ai-integration": "Devin"}


def agent_short(name: str) -> str:
    """`google-labs-jules[bot]` → jules, `Claude Sonnet 5` → Claude: the agent, not the account or the model."""
    n = re.sub(r"\[bot\]$", "", str(name)).strip()
    if n in AGENT_SHORT:
        return AGENT_SHORT[n]
    return n.split()[0] if n.lower().startswith("claude") else n


def _share_pct(v) -> str | None:
    """0.031 → "3", 0.004 → "under 1", 0 → "0"; a figure over 1 is read as a percentage already."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    pct = v * 100 if v <= 1 else v
    if 0 < pct < 0.5:
        return "under 1"
    return str(int(pct + 0.5))


WHOSE = "Ben's"          # review round 3: the page speaks of him in the third person throughout


def agent_clause(stats: dict, repos: list[str] | None = None, aliases: dict | None = None) -> str:
    """Review round 4: the AI disclosure qualifies the figures the page prints. The facts lines count tests and lines
    per repository, whoever wrote them, so the clause says so and gives, for each repository with a facts line, the
    commits a coding agent authored over all its commits (`repos[].others` with `bot: true`, less dependency and CI
    automation, over `repos[].all_hands`): "Tests and lines are counted per repository, whoever wrote them: coding
    agents (Claude, jules) authored 45 of rustmapper's 146 commits and 71 of Scrapy's 499". A repository without its
    counts is left out; with none, nothing."""
    try:
        from data.survey import AUTOMATION
    except ImportError:
        AUTOMATION = ("dependabot[bot]", "renovate[bot]", "github-actions[bot]", "pre-commit-ci[bot]")
    aliases = aliases or {}
    by = {r.get("name"): r for r in stats.get("repos") or [] if isinstance(r, dict)}
    parts, names, cosigned = [], {}, []
    for name in repos or []:
        r = by.get(name) or {}
        total = r.get("all_hands")
        if not isinstance(total, int) or isinstance(total, bool) or total <= 0 or not isinstance(r.get("others"), list):
            continue
        agents = [o for o in r["others"] if isinstance(o, dict) and o.get("bot") and o.get("name") not in AUTOMATION]
        n = sum(int(o.get("commits") or 0) for o in agents)
        for o in agents:
            short = agent_short(o.get("name") or "")
            names[short] = names.get(short, 0) + int(o.get("commits") or 0)
        parts.append(f"{fmt_n(n)} of {aliases.get(name, name)}'s {fmt_n(total)}")
        # review round 7: his own commits that carry an agent's Co-authored-by trailer (`coauthored.agent`), beside
        # the authored count as AUDIT §5 allows; said only when every repository listed has the count
        co = (r.get("coauthored") or {}).get("agent") if isinstance(r.get("coauthored"), dict) else None
        cosigned.append(co if isinstance(co, int) and not isinstance(co, bool) else None)
    if not parts:
        return ""
    who = [k for k, v in sorted(names.items(), key=lambda kv: -kv[1]) if v]
    if not who:
        return ""
    parts[0] += " commits"
    listed = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    tail = ""
    if cosigned and all(c is not None for c in cosigned) and any(cosigned):
        nums = [fmt_n(c) for c in cosigned]
        tail = ", and co-signed " + (nums[0] if len(nums) == 1 else ", ".join(nums[:-1]) + " and " + nums[-1]) + " of his own"
    return (f"Tests and lines are counted per repository, whoever wrote them: coding agents ({', '.join(who)}) "
            f"authored {listed}{tail}")


# The crawl command the README's block prints (install_block), as (flag, value) pairs.
BLOCK_CRAWL_FLAGS = (("--start-url", "<your-site>"),)
# Review round 6: a flag the run check's crawl used that the printed block does not is named in the data line, in
# these words; a flag not listed here is named as itself. IMMATERIAL flags change where a run writes, not what it does.
FLAG_WORDS = {("--seeding-strategy", "none"): "with seeding off"}
IMMATERIAL = ("--data-dir",)      # each run check run writes its own directory; the block uses the default ./data


def cmd_flags(cmd: str) -> list[tuple[str, str]]:
    """`x crawl --start-url u --seeding-strategy none (note)` -> [("--start-url", "u"), ("--seeding-strategy",
    "none")]: each `--flag value` pair, the parenthesised note left out."""
    cmd = re.sub(r"\([^)]*\)", "", str(cmd or ""))
    toks = cmd.split()
    out = []
    for i, t in enumerate(toks):
        if t.startswith("--"):
            nxt = toks[i + 1] if i + 1 < len(toks) and not toks[i + 1].startswith("--") else ""
            out.append((t, nxt))
    return out


def flag_words(cmd: str, printed=BLOCK_CRAWL_FLAGS) -> list[str]:
    """Review round 6: every flag of the run check's crawl that the printed block does not have, in words ("with
    seeding off") or as itself ("with `--workers 4`"); the start URL and IMMATERIAL flags are not named."""
    shown = {f for f, _ in printed}
    out = []
    for f, v in cmd_flags(cmd):
        if f in shown or f in IMMATERIAL:
            continue
        out.append(FLAG_WORDS.get((f, v)) or f"with `{(f + ' ' + v).strip()}`")
    return out


def crawl_words(step: dict | None) -> str:
    """What the run check's crawl ran against, from its own command and detail: "against a local 3-page site".
    Review round 5: the flags it ran with are in DESIGN.md. Review round 6: except a flag that changes what the
    printed command does, which is named first: ", with seeding off, against a local 3-page site" (the block's
    default seeding waits on crt.sh and the Common Crawl index before the first fetch)."""
    if not isinstance(step, dict):
        return ""
    cmd, detail = str(step.get("cmd") or ""), str(step.get("detail") or "")
    m = re.search(r"(\d+) lines", detail)
    words = flag_words(cmd)
    lead = (", " + " and ".join(words) + ",") if words else ""
    if re.search(r"127\.0\.0\.1|localhost", cmd):
        return lead + (f" against a local {m.group(1)}-page site" if m else " against a local site")
    return lead.rstrip(",")


def route_clause(stats: dict, figs: dict) -> str:
    """Round 6, SPEC §4 block 14; review round 5: which release the drawing is, and that its commands were run, when
    and on what. "The [drawing](DESIGN.md) is rustmapper 0.1.3, the release pip installs; its commands were run
    against a local 3-page site on 10 Oct 2026 (Linux x86_64)." The run is said only when the run check passed for
    that release; how the drawing is checked (its files, its reader's commit, the crawl's flags) is in DESIGN.md."""
    route = (stats.get("routes") or {}).get("rustmapper") or {}
    ed = stats.get("edition") or {}
    if not route or not ed.get("version"):
        return ""
    v = ed["version"]
    project = ed.get("project") or "rustmapper"
    out = f"The [drawing](DESIGN.md) shows {project} {v}, the release pip installs"   # review round 7: shows, not is
    rc = (stats.get("runcheck") or {}).get("rustmapper") or {}
    if rc.get("ok") and rc.get("date") and str(rc.get("version")) == str(v):
        steps = {s.get("id"): s for s in rc.get("steps") or []}
        out += (f"; its commands were run{crawl_words(steps.get('crawl_ctrl_c'))} on {fmt_date(rc['date'])}"
                + (f" ({rc['runner']})" if rc.get("runner") else ""))
    return out + "."


def survey_block(stats: dict, figs: dict | None = None, repos: list[str] | None = None,
                 aliases: dict | None = None) -> str:
    """Round 6, SPEC §4 block 14; review round 5: the data line at the foot, what a visitor needs and nothing about
    the build: which release the drawing is and that it was run (route_clause), then what the facts lines' tests and
    lines include, the commits coding agents authored in each repository with a facts line (`agent_clause`). The
    facts lines date and pin every count, so no "measured on" or schedule is repeated here. When the last build
    failed and the figures are the run before's, it says so. An item whose key is absent is left out, never
    estimated."""
    figs = figs or figures(stats, {})
    prov = stats.get("provenance") if isinstance(stats.get("provenance"), dict) else {}
    sentences = []
    head = keep_together(route_clause(stats, figs))
    if head:
        sentences.append(head)
    if prov.get("mode") == "cache-failed":
        failed = fmt_date(prov.get("failed_at"))
        sentences.append(f"The last run failed{' on ' + failed if failed else ''}; these figures are from the run before.")
    agents = agent_clause(stats, repos, aliases)
    if agents:
        sentences.append(agents[0].upper() + agents[1:] + ".")
    if not sentences:
        return ""
    return "<sub>" + " ".join(sentences) + "</sub>"


LOG_LEDE_COMPUTED = ("A rustmapper run as the log would record it, entered the way a log is kept. The figures are "
                     "computed from the crawler's own settings, not yet measured; the day I record a real session "
                     "this page sets them upright by itself.")
LOG_LEDE_MEASURED = "One rustmapper run, recorded {when} on {host}, entered the way a log is kept."


def log_lede_block(log: dict | None) -> str:   # v9.1: the sheet's own sign-off says computed/unsigned; no lede
    return ""


def _log_lede_block_retired(log: dict | None) -> str:
    """The Ship's log lede: computed-consistent until a real session is recorded (reviewer 36)."""
    log = log or {}
    if log.get("measured"):
        when = fmt_date((log.get("session") or {}).get("date") or log.get("date") or "")
        host = (log.get("machine") or {}).get("host") or "one host"
        return LOG_LEDE_MEASURED.format(when=when or "once", host=host)
    return LOG_LEDE_COMPUTED


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
    """Wrap bare <picture> elements that name a sheet in `picture:<sheet>` markers (once). A <picture> already inside
    a picture block (review round 3: inside the hero's link) is left alone."""
    inside = [(m.start(), m.end()) for m in re.finditer(r"<!--\s*picture:[\w-]+:start\b.*?<!--\s*picture:[\w-]+:end\s*-->",
                                                        text, re.S)]

    def sub(m: re.Match) -> str:
        block = m.group(0)
        if any(a <= m.start() < b for a, b in inside):
            return block
        for sheet in sheets:
            if re.search(rf"/{re.escape(sheet)}-(?:day|night|light|dark)[\w-]*\.svg", block):
                before = text[max(0, m.start() - 80):m.start()]
                if f"picture:{sheet}:start" in before:
                    return block
                return f"<!-- picture:{sheet}:start -->\n{block}\n<!-- picture:{sheet}:end -->"
        return block
    return _PICTURE_RE.sub(sub, text)


def page_sheets(text: str) -> list[str]:
    """The sheets whose picture markers the README carries, in SHEETS order (unknown names after)."""
    found = re.findall(r"<!--\s*picture:([\w-]+):start\b", text)
    return [s for s in SHEETS if s in found] + [s for s in dict.fromkeys(found) if s not in SHEETS]


# ------------------------------------------------------------------ main

def main(readme: str, cfg: dict, stats: dict, fittings: list[dict] | None = None, root: str = ROOT,
         use_sheet_alts: bool = True, warnings: list[str] | None = None) -> str:
    warnings = warnings if warnings is not None else []
    figs = figures(stats, cfg)
    text = migrate_pictures(readme)
    for sheet in page_sheets(text):
        alt = alt_for(sheet, stats, cfg, figs, use_sheet_alts)
        if len(alt.split()) > ALT_MAX_WORDS:
            warnings.append(f"alt for {sheet} is {len(alt.split())} words (> {ALT_MAX_WORDS})")
        if alt and alt.split()[0].lower() == "the":
            warnings.append(f"alt for {sheet} starts with 'The'")
        text, _ = fill_block(text, f"picture:{sheet}", picture(sheet, cfg, alt, hero_link(cfg) if sheet == "hero" else None))
    text, _ = fill_block(text, "position", position_block(cfg))
    text, _ = fill_block(text, "contact", contact_block(cfg))
    text, _ = fill_block(text, "figures", figures_block(figs))
    text, _ = fill_block(text, "notices", notices_block(cfg, stats))
    text, _ = fill_block(text, "instruments", instruments_block(cfg, fittings))
    # review round 7: "the Scrapy repository's 499", not "Scrapy's" (the framework has thousands of commits)
    words = {**((cfg.get("hero") or {}).get("aliases") or {}), **((cfg.get("copy") or {}).get("repo_words") or {})}
    text, _ = fill_block(text, "survey", survey_block(stats, figs, facts_repos(text), words))
    for name in facts_repos(text):
        text, _ = fill_block(text, f"facts:{name}", facts_block(stats, name, cfg))
    for name in install_repos(text):
        text, _ = fill_block(text, f"install:{name}", install_block(stats, name, cfg))
    text, _ = fill_block(text, "handoffs", handoffs_block(stats, cfg))
    text, _ = fill_block(text, "pick", pick_block(stats, cfg))
    for name in about_repos(text):
        text, _ = fill_block(text, f"about:{name}", about_block(stats, name))
    text, _ = fill_block(text, "license", license_block(root))
    text, _ = fill_block(text, "log_lede", log_lede_block(_load_log(cfg, root)))
    more = more_count(text, stats)
    if more is not None:
        figs = dict(figs, more_count=str(more))
    for key in inline_keys(text):
        if key in figs:
            text, _ = fill_inline(text, key, figs[key])
        else:
            warnings.append(f"inline marker n:{key} has no figure; left as written")
    return text


def also_names(text: str) -> list[str]:
    """The repositories of the **Also** list (the bullets between it and <details>), in page order."""
    m = re.search(r"\*\*Also\*\*(.*?)<details>", text, re.S)
    return re.findall(r"^- \[\*\*([\w.-]+)\*\*\]", m.group(1), re.M) if m else []


def more_count(text: str, stats: dict) -> int | None:
    """Review round 2: the "N more repositories" figure, computed: every public repository, less the profile, the
    flagships (the facts blocks) and the Also list. None without a repository count."""
    n = stats.get("repo_count")
    if not isinstance(n, int) or not n:
        return None
    return n - 1 - len(facts_repos(text)) - len(also_names(text))


def _load_log(cfg: dict, root: str = ROOT) -> dict | None:
    import json
    path = os.path.join(root, (cfg.get("log") or {}).get("path", "assets/log.json"))
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


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
