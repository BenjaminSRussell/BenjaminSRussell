#!/usr/bin/env python3
"""Survey the repositories themselves — a thin CLI over data.survey.

    python3 scripts/fetch_repodata.py [repo ...] [--json out.json]   # defaults to the repos in assets/stats.json

Bare, blobless clones; `%aI` author dates; Ben's identity from chart.toml [identity] (defaults in
data.survey); hours and weekdays per author-local COMMIT-DAY; 52 weeks of author-filtered commits.
Prints a table and optionally dumps the records. It does not write assets/stats.json: build_stats does.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import STATS_PATH, load_chart_toml  # noqa: E402
from data.survey import identity_from_toml, survey, survey_all  # noqa: E402,F401  (survey re-exported: T7 interface)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repos", nargs="*")
    ap.add_argument("--json", dest="json_out", help="write the records (without history) to this file")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args(argv)
    names = a.repos
    if not names:
        with open(STATS_PATH, encoding="utf-8") as fh:
            names = [r["name"] for r in json.load(fh).get("repos", [])]
    identity = identity_from_toml(load_chart_toml())
    taken = dt.datetime.now(dt.timezone.utc).date()
    with tempfile.TemporaryDirectory() as tmp:
        res = survey_all(names, tmp, identity, taken, identity["login"], workers=a.workers)
    rows = []
    print(f"{'repo':28} {'ben':>5} {'all':>5} {'days':>5} {'modal h':>7}  first        last        others")
    for name in names:
        r = res.get(name)
        if not r:
            print(f"{name:28} {'—':>5} {'—':>5} {'—':>5} {'—':>7}  clone failed or no history")
            continue
        r.pop("_commits", None); r.pop("_git_dir", None)
        modal = max(range(24), key=lambda h: (r["hours"][h], -h)) if r["commit_days"] else None
        others = ", ".join(f"{o['name']} {o['commits']}{'·bot' if o['bot'] else ''}" for o in r["others"])
        print(f"{name:28} {r['commits']:>5} {r['all_hands']:>5} {r['commit_days']:>5} {str(modal):>7}  {r['first']}  {r['last']}  {others}")
        rows.append(r)
    total_days = sum(r["commit_days"] for r in rows)
    hours = [sum(r["hours"][h] for r in rows) for h in range(24)]
    print(f"{len(rows)} repos · {sum(r['commits'] for r in rows)} commits (author-filtered) · "
          f"{sum(r['all_hands'] for r in rows)} all hands · {total_days} commit-days · "
          f"modal author-local hour {max(range(24), key=lambda h: (hours[h], -h))}h")
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=1)
            fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
