"""github — the second instrument: GraphQL metadata, contribution calendar, followers.

    fetch(token, login) -> dict        GraphQL (as the v1 build_stats did); raises on failure
    rest_repo(owner, repo, token=None) -> dict | None       repo-scoped REST fallback (token optional)
    rest_languages(owner, repo, token=None) -> dict | None  {language: bytes}
    rest_releases(owner, repo, token=None) -> list | None

The GraphQL figures are never the hero number: `calendar_total` and `calendar_weeks` are a
cross-check for the clone-derived weeks (MASTERPLAN decision 19). Token optional everywhere;
without one, GraphQL is skipped and REST runs unauthenticated (60 req/h is plenty for 24 repos).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.error
import urllib.request

from . import LOGIN, USER_AGENT

API = "https://api.github.com"

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
        createdAt
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


def _headers(token: str | None) -> dict:
    h = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"bearer {token}"
    return h


def gql(token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(
        f"{API}/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={**_headers(token), "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


def fetch(token: str, login: str = LOGIN) -> dict:
    """GraphQL metadata for the account. Keys: account_since, followers, stars, repo_count,
    repo_meta{name: {stars, archived, pushed, created, language, languages{name: bytes}}},
    languages[] (by bytes, top 5 + Other), calendar_weeks[{start, n}], calendar_total, fetched_at."""
    u = gql(token, QUERY_USER, {"login": login})["user"]
    created = dt.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    total = 0
    for year in range(created.year, now.year + 1):
        d = gql(token, QUERY_YEAR, {"login": login, "from": f"{year}-01-01T00:00:00Z",
                                    "to": f"{year}-12-31T23:59:59Z"})
        total += d["user"]["contributionsCollection"]["totalCommitContributions"]
    meta: dict[str, dict] = {}
    stars = 0
    for repo in u["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        meta[repo["name"]] = {
            "stars": repo["stargazerCount"],
            "archived": repo["isArchived"],
            "pushed": (repo["pushedAt"] or "")[:10] or None,
            "created": (repo.get("createdAt") or "")[:10] or None,
            "language": (repo["primaryLanguage"] or {}).get("name"),
            "languages": {e["node"]["name"]: e["size"] for e in repo["languages"]["edges"]},
        }
    tide = gql(token, QUERY_TIDE, {"login": login})["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    calendar_weeks = [{"start": w["contributionDays"][0]["date"],
                       "n": sum(d["contributionCount"] for d in w["contributionDays"])} for w in tide]
    return {
        "account_since": created.strftime("%Y-%m-%d"),
        "followers": u["followers"]["totalCount"],
        "stars": stars,
        "repo_count": u["repositories"]["totalCount"],
        "repo_meta": meta,
        "languages": languages_from_meta(meta),
        "calendar_weeks": calendar_weeks,
        "calendar_total": total,
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def languages_from_meta(meta: dict, top: int = 5) -> list[dict]:
    """[{name, share, bytes}] by bytes across repos; top `top` + Other."""
    langs: dict[str, int] = {}
    for m in meta.values():
        for name, size in (m.get("languages") or {}).items():
            langs[name] = langs.get(name, 0) + int(size)
    total = sum(langs.values())
    if not total:
        return []
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    out = [{"name": n, "share": round(v / total, 4), "bytes": v} for n, v in ranked[:top]]
    other = total - sum(v for _, v in ranked[:top])
    if other > 0:
        out.append({"name": "Other", "share": round(other / total, 4), "bytes": other})
    return out


# ---------------------------------------------------------------- REST (repo-scoped)

def _rest(path: str, token: str | None = None, timeout: int = 20):
    req = urllib.request.Request(f"{API}/{path.lstrip('/')}", headers=_headers(token))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError):
        return None


def rest_repo(owner: str, repo: str, token: str | None = None) -> dict | None:
    """{stars, archived, pushed, created, language, fork} for one repo, or None."""
    d = _rest(f"repos/{owner}/{repo}", token)
    if not isinstance(d, dict) or "name" not in d:
        return None
    return {
        "stars": d.get("stargazers_count", 0),
        "archived": bool(d.get("archived")),
        "pushed": (d.get("pushed_at") or "")[:10] or None,
        "created": (d.get("created_at") or "")[:10] or None,
        "language": d.get("language"),
        "fork": bool(d.get("fork")),
    }


def rest_languages(owner: str, repo: str, token: str | None = None) -> dict | None:
    d = _rest(f"repos/{owner}/{repo}/languages", token)
    return d if isinstance(d, dict) and "message" not in d else None


def rest_releases(owner: str, repo: str, token: str | None = None) -> list | None:
    d = _rest(f"repos/{owner}/{repo}/releases?per_page=100", token)
    return d if isinstance(d, list) else None


def rest_meta(owner: str, repos: list[str], token: str | None = None) -> dict[str, dict]:
    """repo_meta for the named repos via REST (what GraphQL would give, minus the account fields)."""
    meta: dict[str, dict] = {}
    for name in repos:
        r = rest_repo(owner, name, token)
        if r is None:
            continue
        r["languages"] = rest_languages(owner, name, token) or {}
        meta[name] = r
    return meta


def token_from_env() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or None
