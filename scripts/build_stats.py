#!/usr/bin/env python3
"""Take the day's soundings: live GitHub numbers, repository history, the PyPI edition.

    GITHUB_TOKEN=... python3 scripts/build_stats.py     # fetch + render
    python3 scripts/build_stats.py                        # render from assets/stats.json

Runs daily from .github/workflows/profile.yml. With no token it re-renders the
last cached numbers so the design can be iterated offline.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import svgkit as k  # noqa: E402
from svgkit import Theme  # noqa: E402

LOGIN = "BenjaminSRussell"
ROOT = os.path.join(os.path.dirname(__file__), "..")
CACHE = os.path.join(ROOT, "assets", "stats.json")
W = 1280
MONO = "mono"

QUERY_USER = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        name
        stargazerCount
        isArchived
        pushedAt
        primaryLanguage { name }
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}"""
QUERY_TIDE = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { contributionCount date } } }
    }
  }
}"""
QUERY_YEAR = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) { totalCommitContributions }
  }
}"""


def gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def fetch(token: str) -> dict:
    u = gql(token, QUERY_USER, {"login": LOGIN})["user"]
    created = dt.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    commits = 0
    for year in range(created.year, now.year + 1):
        d = gql(token, QUERY_YEAR, {"login": LOGIN, "from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        commits += d["user"]["contributionsCollection"]["totalCommitContributions"]
    langs: dict[str, int] = {}
    stars = 0
    for repo in u["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    other = total - sum(v for _, v in top)
    languages = [{"name": n, "share": round(v / total, 4)} for n, v in top]
    if other > 0:
        languages.append({"name": "Other", "share": round(other / total, 4)})
    tide = gql(token, QUERY_TIDE, {"login": LOGIN})["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in tide]
    week_starts = [w["contributionDays"][0]["date"] for w in tide]
    repo_meta = {r["name"]: {"stars": r["stargazerCount"], "archived": r["isArchived"], "pushed": r["pushedAt"][:10],
                             "language": (r["primaryLanguage"] or {}).get("name")} for r in u["repositories"]["nodes"]}
    return {
        "weeks": weeks,
        "week_starts": week_starts,
        "repo_meta": repo_meta,
        "updated": now.strftime("%Y-%m-%d"),
        "since": created.strftime("%b %Y"),
        "commits": commits,
        "repos": u["repositories"]["totalCount"],
        "followers": u["followers"]["totalCount"],
        "stars": stars,
        "languages": languages,
        "seeded": False,
    }


def pypi_edition(project: str = "rustmapper") -> dict | None:
    """Latest version and its upload date; the chart's edition line."""
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{project}/json", timeout=20) as r:
            d = json.load(r)
        v = d["info"]["version"]
        files = d["releases"].get(v) or []
        return {"project": project, "version": v, "date": (files[0]["upload_time"][:10] if files else None),
                "releases": len(d["releases"])}
    except Exception as exc:  # pragma: no cover
        print("pypi lookup failed:", exc)
        return None


def fmt(n: int) -> str:
    return f"{n:,}"


def render_all() -> None:
    """Delegate drawing to the sheet modules so the soundings sheet is designed with the rest."""
    import subprocess
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "build_assets.py"), "soundings", "hero", "instruments"], check=False)


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    with open(CACHE, encoding="utf-8") as fh:
        stats = json.load(fh)
    if token:
        fresh = fetch(token)
        stats.update(fresh)
        stats["seeded"] = False
        # survey the repositories' own history (commit counts, dates, hour/weekday rhythm)
        try:
            import fetch_repodata
            fetch_repodata.main(list(fresh["repo_meta"].keys()))
            with open(CACHE, encoding="utf-8") as fh:
                stats.update({k_: v for k_, v in json.load(fh).items() if k_ in ("repos", "hours", "weekdays", "commits_surveyed")})
        except Exception as exc:  # pragma: no cover
            print("repo survey skipped:", exc)
        print("fetched live stats")
    else:
        print("no GITHUB_TOKEN; using cached", CACHE)
    ed = pypi_edition()
    if ed:
        stats["edition"] = ed
    # attach GraphQL metadata to surveyed repos
    meta = stats.get("repo_meta", {})
    for r in stats.get("repos", []):
        r.update({k_: v for k_, v in meta.get(r["name"], {}).items()})
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)
        fh.write("\n")
    render_all()


if __name__ == "__main__":
    main()
