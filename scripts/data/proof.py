"""proof — the dates of the working rules and the hand-typed figures, checked against the code (round 6, review 2).

    rule_records(notices, git_dirs, identity, cache) -> list[dict]      stats.json `rules`
    month_of(rules, key) -> str | None                                   "Sep 2025" from a rule record
    fill_cite(cite, rules) -> (text, missing)                            "{month:key}" filled from the records
    figure_records(figures, git_dirs, cache) -> list[dict]               stats.json `figures`

A working rule's cite says where and when he did the thing it names. Each `[[notices]]` entry in chart.toml may
carry `anchors = [{key, repo, text, path?}]`; for each anchor the build runs `git log --reverse -S<text>` on that
repository's history clone and keeps two commits: the first one by any author (`first_*`) and the first one by an
`[identity]` author (`sha`, `date`, `author`; the date is the author date, which a rebase keeps). The cite's
`{month:<key>}` prints that commit's month. checks/notices.py fails a printed cite whose anchor was not found
(NOTICE-DATE) and one whose code an agent wrote first, unless the notice says so (`names_agent = true`,
NOTICE-AUTHOR).

A `[[figures]]` row backs one number typed into the README's prose: `{text, repo, path, literal}` holds when the
file at the repository's HEAD contains the literal; `{text, repo, glob, count}` holds when that many files at HEAD
match the glob. checks/figures.py fails a number in the README's own text that no holding row covers (FIGURES).
"""
from __future__ import annotations

import fnmatch
import re
import subprocess

from . import survey as survey_mod

_MONTH = re.compile(r"\{month:([\w-]+)\}")


def commits_adding(git_dir: str, text: str, path: str | None = None, timeout: int = 300) -> list[dict]:
    """Commits whose diff changes the number of occurrences of `text` (git's pickaxe), oldest first:
    [{sha, date, name, email}]. On a blobless clone git fetches the blobs it needs."""
    args = ["git", f"--git-dir={git_dir}", "log", "--reverse", "--format=%H%x09%as%x09%an%x09%ae", f"-S{text}", "HEAD"]
    if path:
        args += ["--", path]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return []
    out = []
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) == 4:
            out.append({"sha": parts[0], "date": parts[1], "name": parts[2], "email": parts[3]})
    return out


def first_his(commits: list[dict], identity: dict) -> dict | None:
    return next((c for c in commits if survey_mod.is_ben(c["name"], c["email"], identity)), None)


def rule_records(notices: list[dict], git_dirs: dict[str, str], identity: dict, cache: list[dict] | None = None,
                 adding=commits_adding) -> list[dict]:
    """One record per anchor of every hand notice. Without a clone of its repository, the cache's record is carried,
    marked stale; with no cache either, the anchor is `found: false`."""
    cached = {(r.get("n"), r.get("key")): r for r in cache or []}
    out = []
    for nt in notices:
        for a in nt.get("anchors") or []:
            key, repo, text = str(a.get("key")), str(a.get("repo")), str(a.get("text"))
            rec = {"n": int(nt.get("n") or 0), "key": key, "repo": repo, "path": a.get("path"), "text": text,
                   "found": False, "sha": None, "date": None, "author": None, "first_sha": None,
                   "first_author": None, "first_is_his": None}
            gd = git_dirs.get(repo)
            if not gd:
                old = cached.get((rec["n"], key))
                out.append(dict(old, stale=True) if old else rec)
                continue
            commits = adding(gd, text, a.get("path"))
            if commits:
                first = commits[0]
                rec["first_sha"], rec["first_author"] = first["sha"][:7], first["name"]
                rec["first_is_his"] = survey_mod.is_ben(first["name"], first["email"], identity)
            mine = first_his(commits, identity)
            if mine:
                rec.update(found=True, sha=mine["sha"][:7], date=mine["date"], author=mine["name"])
            out.append(rec)
    return out


def month_of(rules: list[dict], n: int, key: str) -> str | None:
    import datetime as dt
    r = next((x for x in rules or [] if x.get("n") == n and x.get("key") == key), None)
    if not r or not r.get("found") or not r.get("date"):
        return None
    d = dt.date.fromisoformat(str(r["date"])[:10])
    return d.strftime("%b %Y")


def fill_cite(cite: str, n: int, rules: list[dict]) -> tuple[str, list[str]]:
    """`{month:key}` -> "Oct 2025" from the rule records; returns (text, keys not found). A key not found leaves the
    placeholder's month out of the text (the gate fails it; nothing is printed on faith)."""
    missing = []

    def sub(m):
        got = month_of(rules, n, m.group(1))
        if got is None:
            missing.append(m.group(1))
            return "?"
        return got
    return _MONTH.sub(sub, str(cite or "")), missing


def cite_keys(cite: str) -> list[str]:
    return _MONTH.findall(str(cite or ""))


# ---------------------------------------------------------------- the README's typed figures

def figure_records(figures: list[dict], git_dirs: dict[str, str], cache: list[dict] | None = None,
                   read=None, ls=None) -> list[dict]:
    """Each `[[figures]]` row checked at its repository's HEAD. `read(git_dir, path)` and `ls(git_dir)` default to
    the survey's plumbing; the tests pass fixture trees."""
    read = read or (lambda gd, p: survey_mod.file_at(gd, "HEAD", p))
    ls = ls or (lambda gd: survey_mod.ls_tree(gd, ""))
    cached = {(r.get("text"), r.get("repo")): r for r in cache or []}
    out = []
    for f in figures or []:
        rec = {"text": str(f.get("text")), "repo": str(f.get("repo")), "path": f.get("path"),
               "literal": f.get("literal"), "glob": f.get("glob"), "count": f.get("count"), "measured": None,
               "holds": False, "why": ""}
        if f.get("use"):        # review round 3: a row that a build-written sentence rests on (`pick`)
            rec["use"] = str(f["use"])
        gd = git_dirs.get(rec["repo"])
        if not gd:
            old = cached.get((rec["text"], rec["repo"]))
            out.append(dict(old, stale=True) if old else dict(rec, why="no clone of the repository this run"))
            continue
        if rec["glob"]:
            n = len([p for p in ls(gd) or [] if fnmatch.fnmatch(p, rec["glob"])])
            rec["measured"] = n
            rec["holds"] = n == rec["count"]
            rec["why"] = "" if rec["holds"] else f"{n} files match {rec['glob']}, not {rec['count']}"
        else:
            src = read(gd, rec["path"]) if rec["path"] else None
            if src is None:
                rec["why"] = f"{rec['path']}: file missing at HEAD"
            elif rec["literal"] and str(rec["literal"]) not in src:
                rec["why"] = f"{rec['path']}: no {rec['literal']!r} at HEAD"
            else:
                rec["holds"] = True
        out.append(rec)
    return out
