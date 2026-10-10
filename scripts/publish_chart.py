#!/usr/bin/env python3
"""publish_chart.py — put the sheets on the orphan `chart` branch as one force-pushed commit.

    python3 scripts/publish_chart.py --dry-run     # build the tree and commit object, print it, push nothing
    python3 scripts/publish_chart.py               # … and force-push refs/heads/chart

What ships (MASTERPLAN decision 8): every SVG named in assets/build-report.json, the report
itself, and social/*.png if present. Nothing else: no history, no generator, no fonts. The commit
has no parent, so the branch holds exactly one commit after every run and `main`'s history never
carries path data.

How: git plumbing against the repository's own object store (so the checkout's credentials and
remote are reused) with a throw-away index and a staging directory as the work tree:
`add -A` → `write-tree` → `commit-tree` (no parent) → `update-ref` → `push --force`.
A cancelled run between the `main` commit and this push is harmless: the next run republishes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPORT = os.path.join(ROOT, "assets", "build-report.json")
SOCIAL = os.path.join(ROOT, "social")
BRANCH = "chart"
RETIRED = ("hero-still-", "hero-phone-still-")
BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"


class PublishError(Exception):
    pass


def collect(root: str = ROOT, report_path: str = REPORT, social_dir: str = SOCIAL) -> list[tuple[str, str]]:
    """(absolute source, path on the branch) for everything that ships. Fails loudly when the
    report names a file that is not on disk: a half-built set is never published."""
    try:
        with open(report_path, encoding="utf-8") as fh:
            report = json.load(fh)
    except (OSError, ValueError) as exc:
        raise PublishError(f"no usable build report at {report_path}: {exc}") from exc
    if report.get("problems"):
        raise PublishError(f"build report lists {len(report['problems'])} problem(s); not publishing")
    files: list[tuple[str, str]] = []
    for name, e in sorted(report.get("sheets", {}).items()):
        rel = e.get("svg")
        if not rel:
            raise PublishError(f"report entry {name} has no svg path")
        src = rel if os.path.isabs(rel) else os.path.join(root, rel)
        if not os.path.isfile(src):
            raise PublishError(f"report names {rel}, which is not on disk")
        dst = os.path.relpath(src, root) if not os.path.isabs(rel) else os.path.join("assets", "v9", os.path.basename(src))
        files.append((src, dst.replace(os.sep, "/")))
    # round 6: the hero does not move, so its still editions are retired. The branch is one orphan commit of exactly
    # these files, so a still left from an older build is gone after this push; this filter keeps a stale report
    # from carrying one back.
    files = [(src, dst) for src, dst in files if not os.path.basename(dst).startswith(RETIRED)]
    if not files:
        raise PublishError("the build report names no sheets")
    # review round 12: the README's <picture> names six hero editions (desk, mid, phone; day and night). A branch
    # missing one would show a broken image at those widths, so the set the README names must all ship.
    gone = unshipped(files, os.path.join(root, "README.md"))
    if gone:
        raise PublishError(f"README.md names {', '.join(gone)}, which the build report does not ship")
    files.append((report_path, "build-report.json"))
    if os.path.isdir(social_dir):
        for fn in sorted(os.listdir(social_dir)):
            if fn.lower().endswith(".png"):
                files.append((os.path.join(social_dir, fn), f"social/{fn}"))
    return files


def unshipped(files: list[tuple[str, str]], readme_path: str) -> list[str]:
    """The SVG file names the README's `<source srcset>` and `<img src>` point at on the branch that are not among
    `files` (review round 12: the mid editions). No README: nothing to compare."""
    try:
        with open(readme_path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return []
    named = re.findall(r'(?:srcset|src)="[^"]*/' + re.escape(BRANCH) + r'/assets/v9/([\w-]+\.svg)"', text)
    have = {os.path.basename(dst) for _src, dst in files}
    return sorted({n for n in named if n not in have})


def stage(staging: str, files: list[tuple[str, str]]) -> None:
    for src, dst in files:
        out = os.path.join(staging, dst)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(src, out)


def message(report_path: str = REPORT) -> str:
    try:
        with open(report_path, encoding="utf-8") as fh:
            built = json.load(fh).get("built", "")
    except (OSError, ValueError):
        built = ""
    return f"chart: soundings {built[:10]}".strip()


def git(*args: str, cwd: str, env: dict | None = None, capture: bool = True) -> str:
    e = dict(os.environ)
    if env:
        e.update(env)
    res = subprocess.run(["git", *args], cwd=cwd, env=e, text=True, capture_output=capture)
    if res.returncode != 0:
        raise PublishError(f"git {' '.join(args)} failed ({res.returncode}): {(res.stderr or '').strip()}")
    return (res.stdout or "").strip()


def publish(root: str = ROOT, branch: str = BRANCH, remote: str = "origin", dry_run: bool = False,
            report_path: str = REPORT, social_dir: str = SOCIAL, msg: str | None = None) -> int:
    files = collect(root, report_path, social_dir)
    total = sum(os.path.getsize(s) for s, _ in files)
    print(f"publishing {len(files)} files, {total // 1024} KB, to {remote}/{branch}{' (dry run)' if dry_run else ''}")
    tmp = tempfile.mkdtemp(prefix="chart-publish-")
    try:
        staging = os.path.join(tmp, "tree")
        os.makedirs(staging)
        stage(staging, files)
        env = {"GIT_INDEX_FILE": os.path.join(tmp, "index"),
               "GIT_AUTHOR_NAME": BOT_NAME, "GIT_AUTHOR_EMAIL": BOT_EMAIL,
               "GIT_COMMITTER_NAME": BOT_NAME, "GIT_COMMITTER_EMAIL": BOT_EMAIL}
        git(f"--work-tree={staging}", "add", "-A", ".", cwd=root, env=env)
        tree = git("write-tree", cwd=root, env=env)
        commit = git("commit-tree", tree, "-m", msg or message(report_path), cwd=root, env=env)
        listing = git("ls-tree", "-r", "--long", tree, cwd=root)
        for line in listing.splitlines():
            meta, path = line.split("\t", 1)
            size = meta.split()[-1]
            print(f"  {int(size) // 1024:5d} KB  {path}")
        print(f"tree {tree[:12]} commit {commit[:12]} (orphan)")
        if dry_run:
            print("dry run: no ref updated, nothing pushed")
            return 0
        git("update-ref", f"refs/heads/{branch}", commit, cwd=root)
        git("push", "--force", remote, f"refs/heads/{branch}:refs/heads/{branch}", cwd=root, capture=False)
        print(f"pushed {remote}/{branch} = {commit[:12]}")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="publish assets/v9 to the orphan chart branch")
    ap.add_argument("--dry-run", action="store_true", help="build the commit object, print the tree, push nothing")
    ap.add_argument("--branch", default=BRANCH)
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--report", default=REPORT)
    ap.add_argument("--social", default=SOCIAL)
    ap.add_argument("-m", "--message")
    a = ap.parse_args(argv)
    try:
        return publish(ROOT, a.branch, a.remote, a.dry_run, a.report, a.social, a.message)
    except PublishError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(cli())
