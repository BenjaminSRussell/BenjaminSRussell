"""github — the second instrument: GraphQL metadata, contribution calendar, followers.

    fetch(token, login, window) -> dict   GraphQL metadata + the contribution window; raises on failure
    rest_repo(owner, repo, token=None) -> dict | None       repo-scoped REST fallback (token optional)
    rest_languages(owner, repo, token=None) -> dict | None  {language: bytes}
    rest_releases(owner, repo, token=None) -> list | None

The GraphQL figures are never the hero number (MASTERPLAN decision 19). What GitHub counts and the
clones count are different things, so each figure says which it is:
  calendar_total   commits GitHub credits to the account since it was created (default branches of
                   every repository it can see, private ones only if the profile shows them);
  calendar         contributionsCollection over the clone window (`from`..`to`), itemised: commits,
                   issues, pull_requests, reviews, restricted (private), all (the green squares), and
                   commits_by_repo for the account's own repositories; derive.calendar_check compares
                   commits_by_repo of the surveyed repos with the clones, like against like;
  calendar_weeks   the green squares per week over the window (every contribution type).
Token optional everywhere; without one, GraphQL is skipped and REST runs unauthenticated.
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
        defaultBranchRef { name }
        primaryLanguage { name }
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}"""
QUERY_WINDOW = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
      commitContributionsByRepository(maxRepositories: 100) {
        repository { name owner { login } isPrivate }
        contributions { totalCount }
      }
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


def fetch(token: str, login: str = LOGIN, window: tuple[dt.date, dt.date] | None = None, gql=gql) -> dict:
    """GraphQL metadata for the account. Keys: account_since, followers, stars, repo_count,
    repo_meta{name: {stars, archived, pushed, created, language, languages{name: bytes}}},
    languages[] (by bytes, top 5 + Other), calendar_weeks[{start, n}], calendar_total, calendar{…}, fetched_at.
    `window` = (first clone week's Monday, taken): the span the contribution figures are asked for
    (GitHub allows at most one year); default the 365 days before now. `gql` is injectable for tests."""
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
            "default_branch": ((repo.get("defaultBranchRef") or {}).get("name")) or "main",
            "stars": repo["stargazerCount"],
            "archived": repo["isArchived"],
            "pushed": (repo["pushedAt"] or "")[:10] or None,
            "created": (repo.get("createdAt") or "")[:10] or None,
            "language": (repo["primaryLanguage"] or {}).get("name"),
            "languages": {e["node"]["name"]: e["size"] for e in repo["languages"]["edges"]},
        }
    lo, hi = window or (now.date() - dt.timedelta(days=365), now.date())
    frm, to = f"{lo.isoformat()}T00:00:00Z", f"{hi.isoformat()}T23:59:59Z"
    cc = gql(token, QUERY_WINDOW, {"login": login, "from": frm, "to": to})["user"]["contributionsCollection"]
    calendar_weeks = [{"start": w["contributionDays"][0]["date"],
                       "n": sum(d["contributionCount"] for d in w["contributionDays"])}
                      for w in cc["contributionCalendar"]["weeks"] if w["contributionDays"]]
    by_repo: dict[str, int] = {}
    elsewhere = 0
    for e in cc.get("commitContributionsByRepository") or []:
        repo = e["repository"]
        if (repo.get("owner") or {}).get("login") == login and not repo.get("isPrivate"):
            by_repo[repo["name"]] = int(e["contributions"]["totalCount"])
        else:
            elsewhere += int(e["contributions"]["totalCount"])
    calendar = {
        "from": lo.isoformat(), "to": hi.isoformat(),
        "commits": cc["totalCommitContributions"],
        "issues": cc["totalIssueContributions"],
        "pull_requests": cc["totalPullRequestContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
        "restricted": cc["restrictedContributionsCount"],
        "all": cc["contributionCalendar"]["totalContributions"],
        "commits_by_repo": by_repo,
        "commits_elsewhere": elsewhere,
    }
    return {
        "account_since": created.strftime("%Y-%m-%d"),
        "followers": u["followers"]["totalCount"],
        "stars": stars,
        "repo_count": u["repositories"]["totalCount"],
        "repo_meta": meta,
        "languages": languages_from_meta(meta),
        "calendar_weeks": calendar_weeks,
        "calendar_total": total,
        "calendar": calendar,
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
        "default_branch": d.get("default_branch") or "main",
    }


def rest_languages(owner: str, repo: str, token: str | None = None) -> dict | None:
    d = _rest(f"repos/{owner}/{repo}/languages", token)
    return d if isinstance(d, dict) and "message" not in d else None


def rest_releases(owner: str, repo: str, token: str | None = None) -> list | None:
    d = _rest(f"repos/{owner}/{repo}/releases?per_page=100", token)
    return d if isinstance(d, list) else None


def rest_runs(owner: str, repo: str, token: str | None = None, branch: str = "main", n: int = 5) -> dict | None:
    """The project's own CI on its default branch: the latest completed `push` run (`workflow`, `conclusion`,
    `date`, `url`) and the conclusions of the last `n` such runs (`recent`). Dependabot's updater runs and
    pull-request runs are not the question "does main pass", so they are left out. None when the API
    does not answer (no token, rate limit, a proxy) or the repository has no such run."""
    d = _rest(f"repos/{owner}/{repo}/actions/runs?branch={branch}&event=push&status=completed&per_page={n}", token)
    runs = d.get("workflow_runs") if isinstance(d, dict) else None
    if not runs:
        return None
    last = runs[0]
    return {"workflow": last.get("name"), "conclusion": last.get("conclusion"),
            "date": (last.get("updated_at") or last.get("created_at") or "")[:10] or None,
            "url": last.get("html_url"), "recent": [r.get("conclusion") for r in runs]}


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
