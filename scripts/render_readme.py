#!/usr/bin/env python3
"""render_readme.py — fill the README's build-written regions from chart.toml and stats.json.

    python3 scripts/render_readme.py            # rewrite README.md in place (only if it changes)
    python3 scripts/render_readme.py --check    # exit 1 and print a diff if README.md is stale
    python3 scripts/render_readme.py --stdout   # print the rendered README

Block markers (MASTERPLAN decision 3): `<!-- name:start -->…<!-- name:end -->` with names
`picture:<sheet>`, `position`, `contact`, `notices`, `survey`, `license` (v10), `facts:<repo>` (v11, D4); `figures`,
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

def picture(sheet: str, cfg: dict, alt: str) -> str:
    base = cfg["chart"]["base_url"].rstrip("/") + "/"
    bp = cfg["chart"].get("breakpoint_px", 767)
    srcs = (HERO_SOURCES if sheet == "hero" else []) + SOURCES
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
            mod = importlib.import_module(f"sheets.{sheet}")
            s = str(mod.alt(stats, cfg)).strip()
            if s:
                return s
        except Exception:
            pass
    tmpl = cfg.get("alt", {}).get(sheet, "")
    return tmpl.format_map(_Safe(figs)).strip()


def position_block(cfg: dict) -> str:
    """The position slot, inline after the role line (D8: field · languages · position)."""
    text = (cfg.get("position", {}).get("text") or "").strip()
    return f"&nbsp;· <i>{text}</i>" if text else ""


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
                "and run the workflow; the images are regenerated from your repositories.</sub>")


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


CI_WORDS = {"success": "passed", "failure": "failed", "cancelled": "cancelled", "timed_out": "timed out",
            "skipped": "skipped", "neutral": "passed", "action_required": "needs attention"}


def facts_block(stats: dict, name: str) -> str:
    """D4: one plain line under a flagship from the D2 keys (`manifest`, `tests`, `workflows`, `ci`, `lines`,
    `last_ns`). An item whose key is absent is left out, never estimated; no keys, no line."""
    r = _repo(stats, name)
    if not r:
        return ""
    parts: list[str] = []
    man = r.get("manifest")
    if isinstance(man, dict):
        man = man.get("deps") or man.get("names") or man.get("top")
    if isinstance(man, (list, tuple)):
        names = [str(d.get("name") if isinstance(d, dict) else d) for d in man if d]
        if names:
            parts.append("Built on " + ", ".join(names[:5]))
    tests = _count(r.get("tests"))
    if tests is not None:
        parts.append(_plural(tests, "test file"))
    wf = _count(r.get("workflows"))
    ci = r.get("ci")
    if isinstance(ci, str):
        ci = {"conclusion": ci}
    run = ""
    if isinstance(ci, dict) and ci.get("conclusion"):
        word = CI_WORDS.get(str(ci["conclusion"]).lower(), str(ci["conclusion"]).replace("_", " "))
        when = fmt_date(ci.get("date") or ci.get("at") or ci.get("run_at") or ci.get("updated_at"))
        run = f"last run {word}" + (f" {when}" if when else "")
    if wf is not None:
        parts.append(_plural(wf, "workflow") + (f", {run}" if run else ""))
    elif run:
        parts.append(run)
    lines = r.get("lines")
    if isinstance(lines, dict) and isinstance(lines.get("by_language"), dict):
        lines = lines["by_language"]
    if isinstance(lines, dict):
        langs = [(k, v) for k, v in lines.items() if isinstance(v, int) and v > 0 and k not in ("total", "all")]
        if langs:
            lang, n = max(langs, key=lambda kv: kv[1])
            parts.append(f"{fmt_k(n)} lines of {lang}")
    last = fmt_date(r.get("last_ns"))
    if last:
        parts.append(f"last worked {last}")
    return "<sub>" + " · ".join(parts) + "</sub>" if parts else ""


def facts_repos(text: str) -> list[str]:
    """Every `facts:<repo>` block the README carries, in page order."""
    return list(dict.fromkeys(re.findall(r"<!--\s*facts:([\w.-]+):start\b", text)))


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


def survey_block(stats: dict, figs: dict | None = None) -> str:
    """D5: the provenance line at the foot, from stats only. `Measured 7 Oct 2026 from clones of 21 public
    repositories, author's commits on main, sweep days (9–10 Nov 2025, 1 and 7 Oct 2026) excluded · N commits carry
    agent co-author trailers · regenerated weekly.` An item whose key is absent is left out, never estimated: the
    sweep item needs `sweep_dates` (or the `sweeps` entries), the co-author item `coauthored_total`. No commit
    totals (the three counts disagreed; the audit decides) and no instrument roll-call."""
    figs = figs or figures(stats, {})
    prov = stats.get("provenance") if isinstance(stats.get("provenance"), dict) else {}
    parts: list[str] = []
    when = figs.get("taken") or ""
    repo_count = stats.get("repo_count") or (len(stats["repos"]) if isinstance(stats.get("repos"), list) else 0)
    lead = "Measured" + (f" {when}" if when else "")
    if repo_count:
        lead += f" from clones of {repo_count} public repositories, author's commits on main"
        dates = fmt_days(sweep_dates(stats))
        if dates:
            lead += f", sweep days ({dates}) excluded"
    if lead != "Measured":
        parts.append(lead)
    if prov.get("mode") == "cache-failed":
        failed = fmt_date(prov.get("failed_at"))
        parts.append(f"the last run failed{' on ' + failed if failed else ''}; these figures are from the run before")
    co = _count(stats.get("coauthored_total"))
    if co is not None:
        parts.append("no commits carry agent co-author trailers" if co == 0 else
                     f"{fmt_n(co)} commit{'' if co == 1 else 's'} carr{'ies' if co == 1 else 'y'} agent co-author trailers")
    if not parts:
        return ""
    parts.append("regenerated weekly")
    return "<sub>" + " · ".join(parts) + ".</sub>"


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
        text, _ = fill_block(text, f"facts:{name}", facts_block(stats, name))
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
