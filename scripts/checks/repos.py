"""repos — the page links every public repository it counts, and counts every one it links (round 6, review 2).

REPO-SET (fail): a github.com/<login>/<name> link in README.md to a repository that stats.json does not survey; a
  surveyed repository (other than the profile) the README never links; a repository linked more than once inside
  <details>; or a "<N> more repositories" summary whose N is not the number of repositories linked in it.
"""
from __future__ import annotations

import re

from check import Finding, fail, info

TIER = "fast"


def links(text: str, login: str) -> list[str]:
    t = re.sub(r"<!--.*?-->", " ", text or "", flags=re.S)
    return re.findall(rf"github\.com/{re.escape(login)}/([A-Za-z0-9_.-]+?)(?=[/)\"'#?\s]|$)", t)


def check(ctx) -> list[Finding]:
    stats = ctx.stats or {}
    login = stats.get("login") or ((ctx.cfg or {}).get("chart") or {}).get("login") or "BenjaminSRussell"
    text = ctx.readme or ""
    names = {r.get("name") for r in stats.get("repos") or []} | {u.get("name") if isinstance(u, dict) else u
                                                                 for u in stats.get("unsurveyed") or []}
    out: list[Finding] = []
    linked = [n for n in links(text, login) if n != login]
    for n in sorted(set(linked) - names):
        out.append(fail("REPO-SET", f"README links {n}, which stats.json does not survey", "README.md"))
    for n in sorted(names - set(linked) - {login, None}):
        out.append(fail("REPO-SET", f"{n} is a public repository of his that the README never links", "README.md"))
    m = re.search(r"<details>(.*?)</details>", text, re.S)
    if m:
        inner = [n for n in links(m.group(1), login) if n != login]
        for n in sorted({x for x in inner if inner.count(x) > 1}):
            out.append(fail("REPO-SET", f"{n} is linked more than once in the folded list", "README.md"))
        sm = re.search(r"<summary>(?:<!--.*?-->)?\s*(\d+)\s*(?:<!--.*?-->)?\s*more repositories", m.group(1), re.S)
        if sm and int(sm.group(1)) != len(set(inner)):
            out.append(fail("REPO-SET", f"the summary says {sm.group(1)} more repositories; the list links "
                            f"{len(set(inner))}", "README.md"))
    if not out:
        out.append(info("REPO-SET", f"{len(names)} repositories surveyed, every one linked "
                        f"(repository list from {', '.join((stats.get('provenance') or {}).get('repo_list') or ['?'])})"))
    return out
