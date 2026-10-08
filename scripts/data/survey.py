"""survey — bare, blobless clones of each public repo → Ben's history in his own timezone.

    survey(repo, workdir, identity) -> dict | None      one repo record (schema: model.Repo)
    survey_all(repos, identity, ...) -> dict[name, record|None]   parallel, 180 s timeout each

Every statistic comes from one `git log --format=%H%x09%aI%x09%an%x09%ae%x09%s` per repo.
`%aI` keeps the author's own offset, so hours and weekdays are counted in the author's local
time, per COMMIT-DAY (a date in that offset), never per UTC instant (panel 32, 08).
"""
from __future__ import annotations

import datetime as dt
import math
import os
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import NamedTuple

from . import LOGIN, load_chart_toml

DEFAULT_IDENTITY: dict = {
    "login": LOGIN,
    "names": ["Benjamin Russell", "Ben Russell", "BenjaminSRussell"],
    "emails": ["benjamin.sheldon.russell@gmail.com", "russell27sail@gmail.com"],
    "bots": ["github-actions[bot]", "google-labs-jules[bot]", "Claude"],
}
CLONE_TIMEOUT_S = 180
STALE_BRANCH_DAYS = 90
WEEKS = 52


class Commit(NamedTuple):
    sha: str
    when: dt.datetime      # aware, in the author's own offset
    name: str
    email: str
    subject: str

    @property
    def local_date(self) -> dt.date:
        return self.when.date()

    @property
    def offset(self) -> str:
        """'+hhmm' as git prints it."""
        off = self.when.utcoffset() or dt.timedelta(0)
        sign = "-" if off < dt.timedelta(0) else "+"
        secs = abs(int(off.total_seconds()))
        return f"{sign}{secs // 3600:02d}{(secs % 3600) // 60:02d}"


# ---------------------------------------------------------------- identity

def identity_from_toml(cfg: dict | None = None) -> dict:
    """[identity] from chart.toml merged over the defaults (names, emails, bots, login)."""
    cfg = load_chart_toml() if cfg is None else cfg
    ident = dict(DEFAULT_IDENTITY)
    sec = (cfg or {}).get("identity") or {}
    for key in ("names", "emails", "bots"):
        if sec.get(key):
            ident[key] = list(sec[key])
    login = ((cfg or {}).get("chart") or {}).get("login") or sec.get("login")
    if login:
        ident["login"] = login
    return ident


def is_ben(name: str, email: str, identity: dict | None = None) -> bool:
    ident = identity or DEFAULT_IDENTITY
    n = (name or "").strip().casefold()
    e = (email or "").strip().casefold()
    if n in {x.casefold() for x in ident["names"]}:
        return True
    if e in {x.casefold() for x in ident["emails"]}:
        return True
    login = ident.get("login", LOGIN).casefold()
    return e.endswith("@users.noreply.github.com") and login in e


def is_bot(name: str, identity: dict | None = None) -> bool:
    ident = identity or DEFAULT_IDENTITY
    n = (name or "").strip()
    return n in ident.get("bots", []) or n.endswith("[bot]")


# ---------------------------------------------------------------- git plumbing

def _git(dest: str, *args: str, timeout: int = 60) -> str:
    r = subprocess.run(["git", f"--git-dir={dest}", *args], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    return r.stdout


def clone(repo: str, workdir: str, owner: str = LOGIN, timeout: int = CLONE_TIMEOUT_S) -> str | None:
    """Bare blobless clone; returns the git dir or None on failure/timeout."""
    dest = os.path.join(workdir, repo + ".git")
    url = f"https://github.com/{owner}/{repo}.git"
    try:
        r = subprocess.run(["git", "clone", "-q", "--bare", "--filter=blob:none", url, dest],
                           capture_output=True, text=True, timeout=timeout,
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except subprocess.TimeoutExpired:
        return None
    return dest if r.returncode == 0 else None


def history(dest: str, ref: str = "HEAD") -> list[Commit]:
    """Every commit reachable from HEAD, author-dated in the author's own offset."""
    try:
        out = _git(dest, "log", "--format=%H%x09%aI%x09%an%x09%ae%x09%s", ref)
    except RuntimeError:
        return []
    commits: list[Commit] = []
    for line in out.splitlines():
        parts = line.split("\t", 4)
        if len(parts) < 4:
            continue
        sha, iso, name, email = parts[:4]
        subject = parts[4] if len(parts) > 4 else ""
        try:
            when = dt.datetime.fromisoformat(iso)
        except ValueError:
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=dt.timezone.utc)
        commits.append(Commit(sha, when, name, email, subject))
    return commits


def stale_branches(dest: str, taken: dt.date, days: int = STALE_BRANCH_DAYS) -> list[dict]:
    """Branches (not HEAD's) whose last commit is older than `days` before `taken`."""
    try:
        head = _git(dest, "symbolic-ref", "--short", "HEAD").strip()
    except RuntimeError:
        head = ""
    try:
        out = _git(dest, "for-each-ref", "--format=%(refname:short)%09%(committerdate:iso-strict)", "refs/heads")
    except RuntimeError:
        return []
    cutoff = taken - dt.timedelta(days=days)
    stale = []
    for line in out.splitlines():
        name, _, iso = line.partition("\t")
        if not iso or name == head:
            continue
        try:
            last = dt.datetime.fromisoformat(iso).date()
        except ValueError:
            continue
        if last < cutoff:
            stale.append({"name": name, "last": last.isoformat()})
    stale.sort(key=lambda b: b["last"])
    return stale


def file_at_head(dest: str, path: str) -> str | None:
    """Contents of `path` at HEAD (fetches the one blob on demand); None if absent."""
    try:
        return _git(dest, "show", f"HEAD:{path}", timeout=120)
    except RuntimeError:
        return None


def ls_tree(dest: str, prefix: str = "") -> list[str]:
    try:
        out = _git(dest, "ls-tree", "-r", "--name-only", "HEAD", *( [prefix] if prefix else []))
    except RuntimeError:
        return []
    return out.split()


# ---------------------------------------------------------------- commit-days

def week_start(d: dt.date) -> dt.date:
    """Monday of d's ISO week."""
    return d - dt.timedelta(days=d.weekday())


def week_starts(taken: dt.date, n: int = WEEKS) -> list[dt.date]:
    """`n` ISO weeks ending at the week containing `taken`, oldest first."""
    last = week_start(taken)
    return [last - dt.timedelta(weeks=n - 1 - i) for i in range(n)]


def commit_days(commits: list[Commit]) -> list[dict]:
    """[{d, h, n}] per author-local date: modal hour (ties → earliest) and commit count."""
    by_day: dict[dt.date, Counter] = defaultdict(Counter)
    for c in commits:
        by_day[c.local_date][c.when.hour] += 1
    out = []
    for d in sorted(by_day):
        hist = by_day[d]
        top = max(hist.values())
        modal = min(h for h, k in hist.items() if k == top)
        out.append({"d": d.isoformat(), "h": modal, "n": sum(hist.values())})
    return out


def month_label(d: str) -> str:
    y, m = int(d[:4]), int(d[5:7])
    return dt.date(y, m, 1).strftime("%b %Y")


def span_label(first: str, last: str, taken: dt.date, dormant_days: int = 90) -> str:
    """'Jan 2026' | 'Sep 2025–' | 'Sep 2025–Mar 2026' (feature survey span, panel 32 F6)."""
    if first[:7] == last[:7]:
        return month_label(first)
    if (taken - dt.date.fromisoformat(last)).days <= dormant_days:
        return month_label(first) + "–"
    return f"{month_label(first)}–{month_label(last)}"


def summarize(repo: str, commits: list[Commit], identity: dict, taken: dt.date,
              stale_refs: list[dict] | None = None) -> dict:
    """One repos[] record from a repo's history. Pure; derive() adds active/dormant later."""
    mine = [c for c in commits if is_ben(c.name, c.email, identity)]
    others_c: Counter = Counter(c.name for c in commits if not is_ben(c.name, c.email, identity))
    others = [{"name": n, "commits": k, "bot": is_bot(n, identity)} for n, k in others_c.most_common()]
    days = commit_days(mine)
    starts = week_starts(taken)
    idx = {s: i for i, s in enumerate(starts)}
    weeks = [0] * WEEKS
    wdays = [0] * WEEKS
    for day in days:
        i = idx.get(week_start(dt.date.fromisoformat(day["d"])))
        if i is not None:
            weeks[i] += day["n"]
            wdays[i] += 1
    hours = [0] * 24
    weekdays = [0] * 7
    for day in days:
        hours[day["h"]] += 1
        weekdays[dt.date.fromisoformat(day["d"]).weekday()] += 1
    basis = mine or commits
    dates = sorted(c.local_date for c in basis)
    first = dates[0].isoformat() if dates else None
    last = dates[-1].isoformat() if dates else None
    offsets = Counter(c.offset for c in mine)
    return {
        "name": repo,
        "aliases": [],
        "slot": None,
        "commits": len(mine),
        "all_hands": len(commits),
        "others": others,
        "first": first,
        "last": last,
        "commit_days": len(days),
        "months_active": len({d["d"][:7] for d in days}),
        "hours": hours,
        "weekdays": weekdays,
        "weeks": weeks,
        "week_days": wdays,
        "days": days,
        "tz_offsets": dict(offsets.most_common()),
        "active": False,
        "dormant": False,
        "archived": False,
        "stale": False,
        "stale_since": None,
        "language": None,
        "stars": None,
        "span": span_label(first, last, taken) if first and last else None,
        "stale_branches": stale_refs or [],
    }


# ---------------------------------------------------------------- the survey

def survey(repo: str, workdir: str, identity: dict | None = None, taken: dt.date | None = None,
           owner: str = LOGIN, keep_history: bool = False, timeout: int = CLONE_TIMEOUT_S) -> dict | None:
    """Clone + log + summarize. None when the clone fails or HEAD has no history.

    With keep_history=True the record carries `_commits` (list[Commit]) for the caller
    (profile-repo corrections and `Notice:` commits); build_stats pops it before writing.
    """
    identity = identity or DEFAULT_IDENTITY
    taken = taken or dt.datetime.now(dt.timezone.utc).date()
    dest = clone(repo, workdir, owner, timeout)
    if not dest:
        return None
    commits = history(dest)
    if not commits:
        return None
    rec = summarize(repo, commits, identity, taken, stale_branches(dest, taken))
    rec["_git_dir"] = dest
    if keep_history:
        rec["_commits"] = commits
    return rec


def survey_all(repos: list[str], workdir: str, identity: dict | None = None, taken: dt.date | None = None,
               owner: str = LOGIN, keep_history_for: set[str] | None = None, workers: int = 6,
               timeout: int = CLONE_TIMEOUT_S) -> dict[str, dict | None]:
    """Parallel survey; a failed repo maps to None (the caller keeps yesterday's record, stale:true)."""
    keep = keep_history_for or set()

    def one(name: str) -> tuple[str, dict | None]:
        try:
            return name, survey(name, workdir, identity, taken, owner, name in keep, timeout)
        except Exception:
            return name, None

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        return dict(ex.map(one, repos))
