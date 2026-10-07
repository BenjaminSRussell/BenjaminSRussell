#!/usr/bin/env python3
"""Survey the repositories themselves: commit counts, dates, hour-of-day and weekday rhythms.

    python3 scripts/fetch_repodata.py [repo ...]     # defaults to the list in assets/stats.json

Uses bare, blobless clones (cheap) so the chart can be drawn from real history. Results are
merged into assets/stats.json under "repos", "hours" and "weekdays".
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..")
STATS = os.path.join(ROOT, "assets", "stats.json")
OWNER = "BenjaminSRussell"


def survey(repo: str, workdir: str) -> dict | None:
    dest = os.path.join(workdir, repo + ".git")
    url = f"https://github.com/{OWNER}/{repo}.git"
    r = subprocess.run(["git", "clone", "-q", "--bare", "--filter=blob:none", url, dest],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        print(f"  skip {repo}: {r.stderr.strip()[:80]}")
        return None
    git = ["git", f"--git-dir={dest}"]
    head = subprocess.run(git + ["rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
    log = subprocess.run(git + ["log", "--format=%at %an", head], capture_output=True, text=True).stdout.strip().splitlines()
    if not log:
        return None
    stamps = [int(l.split(" ", 1)[0]) for l in log]
    authors = Counter(l.split(" ", 1)[1] for l in log)
    import datetime as dt
    first = dt.datetime.fromtimestamp(min(stamps), dt.timezone.utc)
    last = dt.datetime.fromtimestamp(max(stamps), dt.timezone.utc)
    hours = Counter(dt.datetime.fromtimestamp(s, dt.timezone.utc).hour for s in stamps)
    weekdays = Counter(dt.datetime.fromtimestamp(s, dt.timezone.utc).isoweekday() for s in stamps)
    return {
        "name": repo,
        "commits": len(stamps),
        "first": first.strftime("%Y-%m-%d"),
        "last": last.strftime("%Y-%m-%d"),
        "authors": len(authors),
        "hours": [hours.get(h, 0) for h in range(24)],
        "weekdays": [weekdays.get(d, 0) for d in range(1, 8)],
    }


def main(repos: list[str]) -> None:
    with open(STATS, encoding="utf-8") as fh:
        stats = json.load(fh)
    repos = repos or [r["name"] for r in stats.get("repos", [])]
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        for repo in repos:
            print("surveying", repo)
            d = survey(repo, tmp)
            if d:
                out.append(d)
    out.sort(key=lambda r: -r["commits"])
    stats["repos"] = out
    stats["hours"] = [sum(r["hours"][h] for r in out) for h in range(24)]
    stats["weekdays"] = [sum(r["weekdays"][d] for r in out) for d in range(7)]
    stats["commits_surveyed"] = sum(r["commits"] for r in out)
    with open(STATS, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)
        fh.write("\n")
    print(f"{len(out)} repos, {stats['commits_surveyed']} commits; busiest hour UTC {max(range(24), key=lambda h: stats['hours'][h])}")


if __name__ == "__main__":
    main(sys.argv[1:])
