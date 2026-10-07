"""releases — Notices: dated corrections with provenance (T7 decision 12).

    notices(flagship, pypi_edition, profile_commits, hand=(), token=None, owner=LOGIN) -> list[dict]
      each {repo, tag, date, title, url, source: "release" | "pypi" | "commit" | "hand"}

Order of instruments: GitHub Releases on the flagship → PyPI uploads (prints "four, one day":
the incentive) → profile-repo commits whose subject starts `Notice:`. Hand-entered [[notices]]
from chart.toml are kept. N = len(notices). Sorted by date, then source.
"""
from __future__ import annotations

from . import LOGIN
from .github import rest_releases
from .survey import Commit, is_ben

NOTICE_PREFIX = "Notice:"


def from_releases(owner: str, repo: str, token: str | None = None) -> list[dict] | None:
    """None when the API is unreachable (keep the cache); [] when the repo has no releases."""
    rel = rest_releases(owner, repo, token)
    if rel is None:
        return None
    out = []
    for r in rel:
        if r.get("draft"):
            continue
        date = (r.get("published_at") or r.get("created_at") or "")[:10]
        out.append({"repo": repo, "tag": r.get("tag_name") or "", "date": date or None,
                    "title": (r.get("name") or r.get("tag_name") or "").strip(), "url": r.get("html_url") or "",
                    "source": "release"})
    return out


def from_pypi(repo: str, ed: dict | None) -> list[dict]:
    if not ed or not ed.get("uploads"):
        return []
    project = ed["project"]
    return [{"repo": repo, "tag": f"v{u['version']}", "date": u["date"],
             "title": f"{project} {u['version']} on PyPI", "url": f"https://pypi.org/project/{project}/{u['version']}/",
             "source": "pypi"} for u in ed["uploads"]]


def from_commits(repo: str, commits: list[Commit], identity: dict | None = None, owner: str = LOGIN) -> list[dict]:
    out = []
    for c in sorted(commits, key=lambda c: c.when):
        if not c.subject.startswith(NOTICE_PREFIX) or not is_ben(c.name, c.email, identity):
            continue
        out.append({"repo": repo, "tag": c.sha[:7], "date": c.local_date.isoformat(),
                    "title": c.subject[len(NOTICE_PREFIX):].strip(),
                    "url": f"https://github.com/{owner}/{repo}/commit/{c.sha}", "source": "commit"})
    return out


def notices(flagship: str, pypi_edition: dict | None, profile_commits: list[Commit], hand: list[dict] = (),
            token: str | None = None, owner: str = LOGIN, profile_repo: str = LOGIN,
            identity: dict | None = None, cached: list[dict] | None = None) -> list[dict]:
    rel = from_releases(owner, flagship, token)
    if rel is None:  # API down: keep yesterday's release/pypi notices
        primary = [n for n in (cached or []) if n["source"] in ("release", "pypi")] or from_pypi(flagship, pypi_edition)
    elif rel:
        primary = rel
    else:
        primary = from_pypi(flagship, pypi_edition)
    out = [dict(n, source=n.get("source") or "hand") for n in hand]
    out += primary
    out += from_commits(profile_repo, profile_commits, identity, owner)
    seen = set()
    uniq = []
    for n in out:
        key = (n["repo"], n["tag"], n["source"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(n)
    uniq.sort(key=lambda n: (n["date"] or "", n["source"], n["tag"]))
    return uniq
