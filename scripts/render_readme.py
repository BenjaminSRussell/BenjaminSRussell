#!/usr/bin/env python3
"""render_readme.py — fill the README's build-written regions from chart.toml and stats.json.

    python3 scripts/render_readme.py            # rewrite README.md in place (only if it changes)
    python3 scripts/render_readme.py --check    # exit 1 and print a diff if README.md is stale
    python3 scripts/render_readme.py --stdout   # print the rendered README

Block markers (MASTERPLAN decision 3): `<!-- name:start -->…<!-- name:end -->` with names
`picture:<sheet>`, `position`, `contact`, `notices`, `survey`, `license` (v10), `facts:<repo>` (v11, D4),
`install:<repo>` and `handoffs` (round 6); `figures`,
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

# round 6: the hero does not move, so it ships four editions and no reduced-motion sources
HERO_ROUTE_SOURCES = [
    ("(max-width: {bp}px) and (prefers-color-scheme: dark)", "phone-night"),
    ("(max-width: {bp}px)", "phone-day"),
    ("(prefers-color-scheme: dark)", "night"),
]


def picture(sheet: str, cfg: dict, alt: str) -> str:
    base = cfg["chart"]["base_url"].rstrip("/") + "/"
    bp = cfg["chart"].get("breakpoint_px", 767)
    srcs = HERO_ROUTE_SOURCES if sheet == "hero" else SOURCES
    lines = ["<picture>"]
    for media, ed in srcs:
        lines.append(f'<source media="{media.format(bp=bp)}" srcset="{base}{sheet}-{ed}.svg">')
    alt_attr = alt.replace("&", "&amp;").replace('"', "&quot;")
    # width="100%" and no height: D8 asked for width and height so the page does not jump, but GitHub's
    # markdown CSS (`img {max-width: 100%}` with no `height: auto`) keeps a pixel height while it narrows
    # the width, and the sheet letterboxes inside a column-wide × 740 px box. A ratio hint is not possible
    # without a style attribute, which GitHub strips.
    lines.append(f'<img src="{base}{sheet}-day.svg" width="100%" alt="{alt_attr}">')
    lines.append("</picture>")
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
    line; the editions live in stats.json for the chart, not on the page)."""
    rows = []
    hand = sorted(cfg.get("notices", []), key=lambda x: x.get("n", 0))[:limit]
    for i, nt in enumerate(hand, 1):
        body = f" {nt['body']}" if nt.get("body") else ""
        cite = f" *{nt['cite']}*" if nt.get("cite") else ""
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


LICENSE_LINE = ("<sub>**License** Code MIT; images and text CC BY 4.0; fonts under their own licenses in "
                "[`scripts/fonts/`](scripts/fonts/). To make your own, fork the repository, fill in `chart.toml` "
                "and run the workflow; the images are regenerated from your repositories · how it's built → "
                "[DESIGN.md](DESIGN.md)</sub>")


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
        parts.append("Built on " + ", ".join(deps))
    tests = r.get("test_functions")
    if isinstance(tests, int) and not isinstance(tests, bool):
        parts.append(_plural(tests, "test"))
    ci = r.get("ci")
    if isinstance(ci, str):
        ci = {"conclusion": ci}
    if isinstance(ci, dict) and ci.get("conclusion"):
        word = CI_WORDS.get(str(ci["conclusion"]).lower(), str(ci["conclusion"]).replace("_", " "))
        when = fmt_date(ci.get("date") or ci.get("at") or ci.get("run_at") or ci.get("updated_at"))
        item = f"CI {word}" + (f" {when}" if when else "")
        parts.append(item + (" (last known run)" if ci.get("stale") else ""))   # stale: the API did not answer this time
    else:
        wf = _count(r.get("workflows"))
        if wf:
            parts.append(_plural(wf, "CI workflow"))
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
    return "*" + " · ".join(p.replace("*", r"\*") for p in parts) + "*" if parts else ""


def facts_repos(text: str) -> list[str]:
    """Every `facts:<repo>` block the README carries, in page order."""
    return list(dict.fromkeys(re.findall(r"<!--\s*facts:([\w.-]+):start\b", text)))


# ------------------------------------------------------------------ round 6: how to run it, where its output goes

def _wheel_sentence(wheels) -> str:
    """The note under the install block, from the release's wheels (the same facts as the hero's platform note)."""
    try:
        from data import route as route_mod
    except ImportError:
        return ""
    plats = route_mod.wheel_platforms(wheels)
    names = {n for n, _ in plats}
    if "any platform" in names or all(c in names for c in route_mod.COMMON):
        return ""
    if not plats:
        return "No prebuilt wheel: `pip` builds from source and needs a Rust toolchain."
    friendly = {"macOS arm64": "Apple silicon", "macOS x86_64": "Intel Macs"}
    parts = []
    for n, v in plats:
        piece = f"{friendly.get(n, n)} on {v.replace('Python', 'CPython')}"
        if piece not in parts:
            parts.append(piece)
    one = len(parts) == 1
    return (f"Prebuilt wheel{'' if one else 's'} for {' and '.join(parts)}; elsewhere `pip` builds from source and "
            "needs a Rust toolchain.")


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
    # no line over CODE_COLUMNS characters: a 375 px phone shows about 38 columns of GitHub's code font
    lines = ["```sh", f"pip install {ed.get('project') or 'rustmapper'}", f"{cmd} crawl \\", "    --start-url <your-site>",
             f"{cmd} export-sitemap \\", "    --data-dir ./data \\", "    --output sitemap.xml"]
    gate = ((route.get("gates") or {}).get("cargo") or {})
    if gate.get("ok"):
        lines += ["", "# newer than the release:", "cargo install --git \\",
                  f"    https://github.com/{stats.get('login') or 'BenjaminSRussell'}/{repo}"]
    lines.append("```")
    note = _wheel_sentence(ed.get("wheels"))
    return "\n".join(lines) + (f"\n\n{note}" if note else "")


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


NBSP = "\u00a0"


def agent_clause(stats: dict) -> str:
    """F3.4: `3 % of my commits carry an AI co-author trailer; 297 more were written by coding agents (Claude, jules)
    and are not counted as mine`. Each half prints only when its key is present: `coauthored_total.agent_share`
    and `agent_authored` {total, names}."""
    cot = stats.get("coauthored_total") if isinstance(stats.get("coauthored_total"), dict) else {}
    pct = _share_pct(cot.get("agent_share"))
    first = ""
    if pct == "0":
        first = "none of my commits carry an AI co-author trailer"
    elif pct:
        first = f"{pct}{NBSP}% of my commits carry an AI co-author trailer"
    aa = stats.get("agent_authored") if isinstance(stats.get("agent_authored"), dict) else {}
    total = aa.get("total")
    second = ""
    if isinstance(total, int) and not isinstance(total, bool) and total > 0:
        raw = aa.get("names")
        ranked = (sorted(raw, key=lambda k: -raw[k] if isinstance(raw[k], (int, float)) else 0) if isinstance(raw, dict)
                  else list(raw) if isinstance(raw, list) else [])
        names = list(dict.fromkeys(agent_short(n) for n in ranked if n))
        who = f" ({', '.join(names)})" if names else ""
        n = fmt_n(total)
        if total == 1:
            second = f"{'1 more was' if first else '1 commit was'} written by a coding agent{who} and is not counted as mine"
        else:
            second = f"{n} {'more' if first else 'commits'} were written by coding agents{who} and are not counted as mine"
    return "; ".join(p for p in (first, second) if p)


RUN_WORDS = (("install", "install"), ("crawl_ctrl_c", "crawl"), ("crawl_ctrl_c", "Ctrl-C"), ("kill_writes_file", "kill"),
             ("export", "export"))


def route_clause(stats: dict, figs: dict) -> str:
    """Round 6, SPEC §4 block 14 and review 1: what the drawing describes, what it was checked against, and which of
    its lines were run, against which release, when and on what."""
    route = (stats.get("routes") or {}).get("rustmapper") or {}
    repo = next((r for r in stats.get("repos") or [] if r.get("name") == route.get("repo")), {})
    head = repo.get("head") or {}
    ed = stats.get("edition") or {}
    if not route or not head.get("short") or not ed.get("version"):
        return ""
    v = ed["version"]
    out = (f"The drawing describes {ed.get('project') or 'rustmapper'} {v}, the release pip installs: every line on it "
           f"names code found there, and each line about the design also at `{head['short']}` on main")
    rc = (stats.get("runcheck") or {}).get("rustmapper") or {}
    if rc.get("ok") and rc.get("date") and str(rc.get("version")) == str(v):
        ids = {s.get("id") for s in rc.get("steps") or []}
        words = [w for sid, w in RUN_WORDS if sid in ids]
        if words:
            listed = ", ".join(words[:-1]) + (" and " if len(words) > 1 else "") + words[-1]
            out += f"; its {listed} lines were run against {v} on {fmt_date(rc['date'])} on {rc.get('runner')}"
    return out + "."


def survey_block(stats: dict, figs: dict | None = None) -> str:
    """Round 6, SPEC §4 block 14: the data line at the foot, from stats only. `The drawing is checked against
    rustmapper's code at 32c2651 and its 0.1.3 release on PyPI: … Test counts and CI results measured 9 Oct 2026 from
    clones of 21 public repositories · 3 % of my commits carry an AI co-author trailer; 297 more … · regenerated
    weekly.` An item whose key is absent is left out, never estimated. No figure on the page uses commit-days now,
    so the bulk-edit clause is gone."""
    figs = figs or figures(stats, {})
    prov = stats.get("provenance") if isinstance(stats.get("provenance"), dict) else {}
    parts: list[str] = []
    when = figs.get("taken") or ""
    repo_count = stats.get("repo_count") or (len(stats["repos"]) if isinstance(stats.get("repos"), list) else 0)
    lead = "Test counts and CI results measured" + (f" {when}" if when else "")
    if repo_count:
        lead += f" from clones of {repo_count} public repositories"
    if lead != "Test counts and CI results measured":
        parts.append(lead)
    if prov.get("mode") == "cache-failed":
        failed = fmt_date(prov.get("failed_at"))
        parts.append(f"the last run failed{' on ' + failed if failed else ''}; these figures are from the run before")
    agents = agent_clause(stats)
    if agents:
        parts.append(agents)
    if not parts:
        return ""
    parts.append("regenerated weekly")
    head = route_clause(stats, figs)
    return "<sub>" + (head + " " if head else "") + " · ".join(parts) + ".</sub>"


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
        text, _ = fill_block(text, f"picture:{sheet}", picture(sheet, cfg, alt))
    text, _ = fill_block(text, "position", position_block(cfg))
    text, _ = fill_block(text, "contact", contact_block(cfg))
    text, _ = fill_block(text, "figures", figures_block(figs))
    text, _ = fill_block(text, "notices", notices_block(cfg, stats))
    text, _ = fill_block(text, "instruments", instruments_block(cfg, fittings))
    text, _ = fill_block(text, "survey", survey_block(stats, figs))
    for name in facts_repos(text):
        text, _ = fill_block(text, f"facts:{name}", facts_block(stats, name, cfg))
    for name in install_repos(text):
        text, _ = fill_block(text, f"install:{name}", install_block(stats, name, cfg))
    text, _ = fill_block(text, "handoffs", handoffs_block(stats, cfg))
    text, _ = fill_block(text, "license", license_block(root))
    text, _ = fill_block(text, "log_lede", log_lede_block(_load_log(cfg, root)))
    for key in inline_keys(text):
        if key in figs:
            text, _ = fill_inline(text, key, figs[key])
        else:
            warnings.append(f"inline marker n:{key} has no figure; left as written")
    return text


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
