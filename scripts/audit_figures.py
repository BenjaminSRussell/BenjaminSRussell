#!/usr/bin/env python3
"""audit_figures.py — docs/data/AUDIT.md §7, the register of every figure the page prints (round 6, review 2).

    python3 scripts/audit_figures.py            # rewrite the block between the audit-figures markers
    python3 scripts/audit_figures.py --check    # exit 1 when the committed block differs (check.py AUDIT-STALE)

One row per printed figure: where it is, what is printed, the stats.json key or chart.toml row it comes from, its
definition, and the check that fails when it does not hold. The rows come from four places, so the register moves
when they do: the release label (HERO below); review round 7: every route entry whose wording carries a figure read
from the code (`{const:}`, `{field:}`, `{arg:}`, `{release}`, `{head}`), with the definition built from the anchor
that reads it and the entry's own `audit` note (route_rows), and the hand-off's count (the [[figures]] row marked
`handoff`); the README's build-written blocks (FIXED below, one row per figure each block prints); and chart.toml's
[[figures]] rows and [[notices]] anchors for the figures typed into the prose. No measured value is written here
(they change every week); the page shows them.

Review round 7: each row also says what text it covers (`covers`, regular expressions over the README's visible
text; `hero_keys`, the text-manifest keys of the image's runs), and checks/audit_cover.py (AUDIT-COVER) fails any
digit in the hero's text or the README's visible text that no row covers.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
AUDIT = os.path.join(ROOT, "docs", "data", "AUDIT.md")
CFG = os.path.join(ROOT, "chart.toml")
START, END = "<!-- audit-figures:start -->", "<!-- audit-figures:end -->"

# the image's release label: (printed, key, definition, check, hero keys)
HERO = {
    "R2": ("release and its date", "`edition.version`, `edition.date`",
           "the latest version on PyPI and the first upload of its files (PyPI JSON)",
           "ROUTE-ENTRANCE: the run check tested that version within 14 days", ("edition:version",)),
}
_DATE = r"\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}"
# the README's build-written blocks: (block, printed, key, definition, check, covers)
FIXED = [
    ("facts", "On main at `<sha>`", "`repos[].head.short`", "HEAD of the default branch of the clone the counts were "
     "taken from", "test_pipeline facts; README-STALE", (r"On main at `[0-9a-f]{7}`",)),
    ("facts", "N tests", "`repos[].test_functions`", "test functions at HEAD: Rust `#[test]`-style attributes in every "
     ".rs file, Python `def test_` in collected files (§2)", "README-STALE", (r"\d[\d,]* tests?\b",)),
    ("facts", "(CI selects all but N)", "`repos[].ci_selection`", "review round 7: of those tests, the ones the passing "
     "workflow's own commands do not select: Python tests in collected files outside every pytest command's paths, "
     "or deselected by the `-m \"not …\"` of every command whose paths hold them (markers read with ast, at "
     "function, class and module level); Rust tests when no step runs `cargo test`, else the `#[ignore]` ones. Skips "
     "decided when the tests run (`skipif`, `pytest.skip()`, `importorskip`) are not counted: they depend on the "
     "machine. Printed only when above 0 (data/tree.py `ci_selection`)", "test_round7 CiSelection; README-STALE",
     (r"\(CI selects all but \d[\d,]*\)",)),
    ("facts", "CI passed <date>", "`repos[].ci`", "the conclusion of the latest completed push run on the default "
     "branch, as the workflow defines it: a job marked continue-on-error does not fail the run, and its failure is "
     "printed as \"<job> failed (not blocking)\"; `ci.jobs` names each job and its runs-on labels", "README-STALE",
     (r"CI (?:passed|failed|cancelled|timed out|skipped|needs attention) " + _DATE,)),
    ("facts", ": tests, rustfmt, …", "`repos[].ci.gates`", "review round 9: the checks the passing run blocks on, read "
     "from the workflow file (found by its `name:`) at the commit CI ran on (`ci.head_sha`, data/tree.py `ci_gates`). "
     "A step counts when its job passed in that run (`ci.jobs`), neither it nor its job has `continue-on-error: "
     "true`, and its command starts `cargo test` or `pytest` (tests), `cargo fmt … --check` (rustfmt), `cargo "
     "clippy`, `cargo audit`, `ruff`, `mypy` or `bandit` without ending in `|| true`, `|| :` or `|| echo …` or "
     "following a `set +e`. Rust-sitemap's clippy (`|| true`), audit (continue-on-error) and benchmark (`|| echo`) "
     "do not count", "CI-GATES; README-STALE", (r"CI passed " + _DATE + r": [a-z ,]+",)),
    ("facts", "MIT license", "`repos[].license`", "the SPDX id GitHub's license detection gives the repository (REST "
     "`license.spdx_id`); printed only when it is not null or NOASSERTION", "LICENSE-FLAGSHIP; README-STALE", ()),
    ("facts", "Nk lines of <language>", "`repos[].lines`, `main_language`", "newlines of source files at HEAD, "
     "vendored and generated trees excluded (§2)", "README-STALE", (r"\d+(?:\.\d)?[kM]? lines of \w+",)),
    ("Languages", "Python, Rust; Swift, JavaScript, …", "`repos[].main_language`, chart.toml `[copy] languages_lead`",
     "review round 7: the lead pair, then every other `main_language` of his public repositories (the profile left "
     "out), by how many repositories have it, then by their lines in it. `main_language` is the language with most "
     "newlines at HEAD (§2, data/tree.py), vendored and generated trees excluded. It is not GitHub's Linguist "
     "figure, which counts bytes; where REST's `language` was read (`repos[].language`, 4 of 22 on 10 Oct 2026) "
     "the two agree", "test_round7 Languages; README-STALE", ()),
    ("install", "CPython 3.13 (Apple silicon)", "`edition.wheels`", "the wheel tags of the latest release on PyPI",
     "T-WHEELS", (r"CPython \d+\.\d+",)),
    ("install", "N min from a cold cache on a C-core <runner> machine", "`runcheck.rustmapper.steps[install]`",
     "the source build, timed INSTALL_RUNS times, each in a fresh venv with an empty CARGO_HOME; the span of the "
     "runs in whole minutes; printed only when `cache` is `cold`", "test_proof InstallTime",
     (r"\d+(?:–\d+)? min from a cold cache on a \d+-core",)),
    ("install", "Before you run <version>:", "`edition.version`", "review round 10: the release the cautions describe "
     "(the list's entries are checked on the sdist pip installs; the facts line above them dates main), the latest "
     "version on PyPI", "README-CAUTIONS; README-STALE", (r"Before you run \d+\.\d+\.\d+:",)),
    ("install", "# <version> runs until stopped … for N s", "`edition.version`, `routes.rustmapper` H1 `quiet`",
     "review round 10: the release and H1's `{quiet}`, filled as the image fills them; printed only while H1 is drawn "
     "with its number (`render_readme.stop_lines`)", "test_round10 StopLines; README-STALE",
     (r"# \d+\.\d+\.\d+ runs until stopped", r"# for \d+ s,")),
    ("survey", "rustmapper <version>, <date> (<runner>)", "`edition.version`, `runcheck.rustmapper.date`, `runner`",
     "the release the drawing describes, and the day and machine the run check ran its lines on", "ROUTE-ENTRANCE",
     (r"rustmapper \d+\.\d+\.\d+, the release pip installs", r"on " + _DATE + r" \(")),
    ("survey", "a local N-page site, `--seeding-strategy none`", "`runcheck.rustmapper.steps[crawl_ctrl_c]`",
     "the crawl as it ran: the step's own command and the lines it wrote", "test_pipeline provenance",
     (r"a local \d+-page site",)),
    ("survey", "measured <date> from N public repositories", "`taken`, `repo_count`",
     "the day of the build; the owner's public non-fork repositories (GraphQL live; in cache mode the cached names, "
     "REST's list when it answers, and README links REST confirms)", "REPO-SET", ()),
    ("survey", "coding agents authored N of <repo>'s M commits", "`repos[].others`, `repos[].all_hands`",
     "for each repository with a facts line: commits on HEAD whose author is a coding agent (`others[]` with "
     "`bot: true`, less `survey.AUTOMATION`), over all its commits on HEAD; the facts lines' tests and lines include "
     "their code", "test_pipeline AgentClause; README-STALE", (r"\d[\d,]* of [\w' -]+?'s \d[\d,]*",)),
    ("survey", "and co-signed N and M of his own", "`repos[].coauthored.agent`",
     "review round 7: of his own commits (`commits`), those carrying a `Co-authored-by` trailer that names an agent "
     "(§2 `coauthored`), printed beside the authored count as §5 allows, for the same repositories in the same order",
     "test_round7 Cosigned; README-STALE", (r"co-signed [\d, and]+ of his own",)),
    ("more_count", "N more repositories", "computed (`render_readme.more_count`)",
     "`repo_count` − the profile − the flagships − the Also list", "REPO-SET", (r"\d+\s+more repositories",)),
    ("license", "CC BY 4.0", "`LICENSE-ASSETS.md`", "the license of the profile's images and text, as that file "
     "states it", "README-LICENSE", (r"CC BY 4\.0",)),
]
_REF = __import__("re").compile(r"\{((const|field|arg):(\w+)|release|head|quiet)\}")


def route_rows(cfg: dict) -> list[dict]:
    """Review round 7: one row per route entry whose wording reads a figure from the code, its definition built from
    the anchor that reads it (any of the entry's wordings), plus the entry's `audit` note."""
    out = []
    for name, spec in ((cfg.get("route") or {}).items()):
        if not isinstance(spec, dict):
            continue
        for e in spec.get("entry") or []:
            cands = [e] + list(e.get("instead") or [])
            refs: dict[str, tuple[str, str]] = {}
            for c in cands:
                for m in _REF.finditer(str(c.get("text") or "")):
                    refs.setdefault(m.group(1), (m.group(2) or m.group(1), m.group(3) or ""))
            if not refs and not (e.get("audit") and str(e.get("kind")) == "text"):
                continue      # review round 8: a README sentence whose figure is a flag's argument has its own note
            scope = str(e.get("scope") or "both")
            defs = []
            for ref, (kind, var) in refs.items():
                if kind == "release":
                    defs.append("`{release}` is `edition.version`, the latest version on PyPI")
                    continue
                if kind == "head":
                    defs.append("`{head}` is the sha the route was read at (`routes.%s.head_sha`), short" % name)
                    continue
                if kind == "quiet":
                    defs.append("`{quiet}` is computed by `data/route.py` `quiet_secs` from the release's value "
                                "anchors `arg:timeout` and `const:MAX_FAILURES_THRESHOLD`")
                    continue
                rel = next((a for c in cands for a in c.get("release") or [] if a.get(kind) == var), None)
                hd = next((a for c in cands for a in c.get("head") or [] if a.get(kind) == var), None)
                what = {"const": f"`const {var}`", "field": f"the `{var}:` value of the struct literal",
                        "arg": f"the clap `default_value` of `{var}`"}[kind]
                where = []
                if rel:
                    where.append(f"`{rel['path']}` of the sdist")
                if hd and (scope != "release" or not rel):
                    where.append(f"`{hd['path']}` at HEAD")
                tail = "; the two must agree" if rel and hd and scope != "release" else \
                    " (the release lacks it; main's value)" if hd and not rel else ""
                defs.append(f"`{{{ref}}}` is {what} in {' and '.join(where)}{tail}")
            kind = str(e.get("kind") or "stop")
            out.append({"where": ("README " if kind == "text" else "image ") + str(e["id"]),
                        "printed": ", ".join(f"`{{{r}}}`" for r in refs) or "the flag's argument",
                        "key": f"`routes.{name}` {e['id']}",
                        "definition": ("; ".join(defs) + (f". {e['audit']}" if e.get("audit") else "")) if defs
                                      else str(e.get("audit") or ""),
                        "check": "ROUTE-UNVERIFIED (value anchors; head and release agree)",
                        "entry": str(e["id"]), "route": name, "hero_keys": (f"routes:{e['id']}",)})
    return out


def handoff_rows(cfg: dict) -> list[dict]:
    """Review round 7: the hand-off label's count, from the [[figures]] row marked `handoff`."""
    out = []
    for f in cfg.get("figures") or []:
        if not f.get("handoff"):
            continue
        how = (f"the dict literal assigned to `{f['keys']}` in `{f['path']}` has {f['count']} keys" if f.get("keys")
               else f"{f['count']} files match `{f['glob']}`" if f.get("glob") else f"`{f['path']}` contains `{f.get('literal')}`")
        also = "".join(f"; `{a['path']}` contains `{str(a['literal']).replace(chr(10), '⏎')}`" for a in f.get("also") or [])
        ids = [h["id"] for h in cfg.get("handoffs") or [] if h.get("to") == f.get("repo")]
        out.append({"where": "image R15", "printed": f"sorted {f['text']} by {f['repo']}",
                    "key": f"`[[figures]]` ({f['repo']}, handoff), `handoffs[]`",
                    "definition": f"at {f['repo']}'s HEAD, {how}{also}; drawn while the hand-off's state is `runs`",
                    "check": "FIGURES; ROUTE-HANDOFF", "hero_keys": tuple(f"handoffs:{i}" for i in ids)})
    return out


def records(cfg: dict) -> list[dict]:
    """Every register row as a dict: the table's five columns, and what text it covers (`covers`, `hero_keys`)."""
    from sheets import route as sheet
    out = []
    for gid, (printed, key, definition, check, keys) in HERO.items():
        learns = sheet.PURPOSE[gid][0]
        out.append({"where": f"image {gid}", "printed": printed, "key": key, "definition": f"{definition} ({learns})",
                    "check": check, "hero_keys": keys})
    for r in route_rows(cfg) + handoff_rows(cfg):
        gid = r["where"].split()[-1]
        if gid in sheet.PURPOSE and r["where"].startswith("image"):
            r = dict(r, definition=f"{r['definition']} ({sheet.PURPOSE[gid][0]})")
        out.append(r)
    for block, printed, key, definition, check, covers in FIXED:
        out.append({"where": f"README `{block}`", "printed": printed, "key": key, "definition": definition,
                    "check": check, "covers": covers})
    for nt in sorted(cfg.get("notices") or [], key=lambda n: n.get("n", 0))[:4]:
        for a in nt.get("anchors") or []:
            out.append({"where": f"README rule {nt.get('n')}", "printed": f"`{{month:{a['key']}}}`",
                        "key": f"`rules` ({a['repo']})",
                        "definition": f"the author month of his first commit adding `{a['text']}` (git log --reverse "
                                      "-S); the text is still in the code at HEAD (`at_head`)",
                        "check": "NOTICE-DATE, NOTICE-AUTHOR, NOTICE-LIVE", "rule": int(nt.get("n") or 0)})
        from data import proof
        for m in proof._DAYS.finditer(str(nt.get("body") or "")):
            a, b = m.group(1), m.group(2)
            what = (f"the days from his first commit adding the `{a}` anchor's text to his first commit adding the "
                    f"`{b}` anchor's text (their author dates)" if b else
                    f"the days from the repository's first commit (any author, `rules[].repo_first`, git log) to his "
                    f"first commit adding the `{a}` anchor's text (author dates)")
            out.append({"where": f"README rule {nt.get('n')}", "printed": f"`{m.group(0)}`",
                        "key": f"`rules` ({nt.get('repo')})", "definition": f"review round 8: {what}",
                        "check": "NOTICE-DATE; test_round8 RuleDays", "rule": int(nt.get("n") or 0)})
    for f in cfg.get("figures") or []:
        if f.get("handoff"):
            continue
        how = (f"{f['count']} files match `{f['glob']}`" if f.get("glob") else
               f"`{f['path']}` contains `{str(f['literal']).replace(chr(10), '⏎')}`" if f.get("literal") else
               f"the dict literal assigned to `{f['keys']}` in `{f['path']}` has {f['count']} keys" if f.get("keys") else
               (f"`{f['path']}` has {f['count']:,} rows as Python's csv module reads them (the rows "
                f"`pd.read_csv(header=None)` loads)" + (f" whose `urlsplit().hostname` is `{f['host']}` or ends in "
                f"`.{f['host']}`" if f.get("host") else "")) if f.get("csv_rows") else f"`{f['path']}` exists")
        how += "".join(f"; `{a['path']}` contains `{str(a['literal']).replace(chr(10), '⏎')}`"
                       for a in f.get("also") or [])
        out.append({"where": "README prose", "printed": f["text"], "key": f"`[[figures]]` ({f['repo']})",
                    "definition": f"at HEAD, {how}", "check": "FIGURES", "figure": f["text"]})
    return out


def rows(cfg: dict) -> list[list[str]]:
    return [[r["where"], r["printed"], r["key"], r["definition"], r["check"]] for r in records(cfg)]


def _rows_retired(cfg: dict) -> list[list[str]]:
    from sheets import route as sheet
    out = []
    for gid, (printed, key, definition, check, _k) in HERO.items():
        learns = sheet.PURPOSE[gid][0]
        out.append([f"image {gid}", printed, key, f"{definition} ({learns})", check])
    for block, printed, key, definition, check, _c in FIXED:
        out.append([f"README `{block}`", printed, key, definition, check])
    for nt in sorted(cfg.get("notices") or [], key=lambda n: n.get("n", 0))[:4]:
        for a in nt.get("anchors") or []:
            out.append([f"README rule {nt.get('n')}", f"`{{month:{a['key']}}}`", f"`rules` ({a['repo']})",
                        f"the author month of his first commit adding `{a['text']}` (git log --reverse -S)",
                        "NOTICE-DATE, NOTICE-AUTHOR"])
    for f in cfg.get("figures") or []:
        how = (f"{f['count']} files match `{f['glob']}`" if f.get("glob") else
               f"`{f['path']}` contains `{f['literal']}`" if f.get("literal") else f"`{f['path']}` exists")
        out.append(["README prose", f["text"], f"`[[figures]]` ({f['repo']})", f"at HEAD, {how}", "FIGURES"])
    return out


def block(cfg: dict) -> str:
    lines = [START, "", "| where | printed | key | definition | check |", "|---|---|---|---|---|"]
    lines += ["| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in rows(cfg)]
    lines += ["", END]
    return "\n".join(lines)


def render(text: str, cfg: dict) -> str:
    new = block(cfg)
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: new, text, flags=re.S)
    return text.rstrip("\n") + "\n\n## 7. Printed figures\n\nGenerated by `scripts/audit_figures.py`; do not edit by hand.\n\n" + new + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    with open(CFG, "rb") as fh:
        cfg = tomllib.load(fh)
    with open(AUDIT, encoding="utf-8") as fh:
        before = fh.read()
    after = render(before, cfg)
    if a.check:
        return 0 if after == before else 1
    if after != before:
        with open(AUDIT, "w", encoding="utf-8") as fh:
            fh.write(after)
        print("wrote docs/data/AUDIT.md §7")
    else:
        print("AUDIT.md §7 is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
