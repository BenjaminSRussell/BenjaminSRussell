#!/usr/bin/env python3
"""audit_figures.py — docs/data/AUDIT.md §7, the register of every figure the page prints (round 6, review 2).

    python3 scripts/audit_figures.py            # rewrite the block between the audit-figures markers
    python3 scripts/audit_figures.py --check    # exit 1 when the committed block differs (check.py AUDIT-STALE)

One row per printed figure: where it is, what is printed, the stats.json key or chart.toml row it comes from, its
definition, and the check that fails when it does not hold. The rows come from three places, so the register moves
when they do: the hero's PURPOSE table (scripts/sheets/route.py) for the image, the README's build-written blocks
(FIXED below, one row per figure each block prints), and chart.toml's [[figures]] rows and [[notices]] anchors for
the figures typed into the prose. No measured value is written here (they change every week); the page shows them.
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

# the image: the PURPOSE ids whose text carries a figure, and what the figure is
HERO = {
    "R2": ("release and its date", "`edition.version`, `edition.date`",
           "the latest version on PyPI and the first upload of its files (PyPI JSON)",
           "ROUTE-ENTRANCE: the run check tested that version within 14 days"),
    "W1": ("the writer's batch interval, in ms", "`routes.rustmapper` W1, `{const:BATCH_TIMEOUT_MS}`",
           "`const BATCH_TIMEOUT_MS` in `src/writer_thread.rs`, read at HEAD and in the sdist; the two must agree",
           "ROUTE-UNVERIFIED (anchor `const`), T-ANCHOR"),
}
# the README's build-written blocks: (block, printed, key, definition, check)
FIXED = [
    ("facts", "On main at `<sha>`", "`repos[].head.short`", "HEAD of the default branch of the clone the counts were "
     "taken from", "test_pipeline facts; README-STALE"),
    ("facts", "N tests", "`repos[].test_functions`", "test functions at HEAD: Rust `#[test]`-style attributes in every "
     ".rs file, Python `def test_` in collected files (§2)", "README-STALE"),
    ("facts", "CI passed <date>", "`repos[].ci`", "the conclusion of the latest completed push run on the default "
     "branch, as the workflow defines it: a job marked continue-on-error does not fail the run, and its failure is "
     "printed as \"<job> failed (not blocking)\"; `ci.jobs` names each job and its runs-on labels", "README-STALE"),
    ("facts", "Nk lines of <language>", "`repos[].lines`, `main_language`", "newlines of source files at HEAD, "
     "vendored and generated trees excluded (§2)", "README-STALE"),
    ("install", "CPython 3.13 (Apple silicon)", "`edition.wheels`", "the wheel tags of the latest release on PyPI",
     "T-WHEELS"),
    ("install", "N min from a cold cache on a C-core <runner> machine", "`runcheck.rustmapper.steps[install]`",
     "the source build, timed INSTALL_RUNS times, each in a fresh venv with an empty CARGO_HOME; the span of the "
     "runs in whole minutes; printed only when `cache` is `cold`", "test_proof InstallTime"),
    ("survey", "rustmapper <version>, <date> (<runner>)", "`edition.version`, `runcheck.rustmapper.date`, `runner`",
     "the release the drawing describes, and the day and machine the run check ran its lines on", "ROUTE-ENTRANCE"),
    ("survey", "a local N-page site, `--seeding-strategy none`", "`runcheck.rustmapper.steps[crawl_ctrl_c]`",
     "the crawl as it ran: the step's own command and the lines it wrote", "test_pipeline provenance"),
    ("survey", "measured <date> from N public repositories", "`taken`, `repo_count`",
     "the day of the build; the owner's public non-fork repositories (GraphQL live; in cache mode the cached names, "
     "REST's list when it answers, and README links REST confirms)", "REPO-SET"),
    ("survey", "coding agents authored N of <repo>'s M commits", "`repos[].others`, `repos[].all_hands`",
     "for each repository with a facts line: commits on HEAD whose author is a coding agent (`others[]` with "
     "`bot: true`, less `survey.AUTOMATION`), over all its commits on HEAD; the facts lines' tests and lines include "
     "their code", "test_pipeline AgentClause; README-STALE"),
    ("more_count", "N more repositories", "computed (`render_readme.more_count`)",
     "`repo_count` − the profile − the flagships − the Also list", "REPO-SET"),
]


def rows(cfg: dict) -> list[list[str]]:
    from sheets import route as sheet
    out = []
    for gid, (printed, key, definition, check) in HERO.items():
        learns = sheet.PURPOSE[gid][0]
        out.append([f"image {gid}", printed, key, f"{definition} ({learns})", check])
    for block, printed, key, definition, check in FIXED:
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
