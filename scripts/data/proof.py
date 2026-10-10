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
NOTICE-AUTHOR). Review round 6: an anchor with `author = "self"` claims only his own commit: its record carries
`scope: "self"`, and NOTICE-AUTHOR then asks that his first commit adding the text exists, not that the
repository's first one is his (the cite proves the rule is how he works; who else used the call first is not its
subject).

A `[[figures]]` row backs one number typed into the README's prose: `{text, repo, path, literal}` holds when the
file at the repository's HEAD contains the literal; `{text, repo, glob, count}` holds when that many files at HEAD
match the glob. checks/figures.py fails a number in the README's own text that no holding row covers (FIGURES).
Review round 7: `{text, repo, path, keys, count}` holds when the dict literal assigned to `keys` in that Python file
(`self.methods = {…}`, read with ast) has `count` keys; `also = [{path, literal}]` must hold too; `handoff = true`
marks the row the image's hand-off label reads (sheets/route.handoff_words).

Review round 13: `absent = [{path, pattern}]` must not match (a regular expression; the file must exist): config.yml
with no top-level `scrapy:` section, so the UConn user agent is the one sent.

Review round 8: `{text, repo, glob, contains, count}` counts only the matching files that contain the literal (the four
organizers that take `List[PageContent]`), and `parts = [text, …]` on a row asks that the counts of those rows add up
to its own (25 = 21 + 4: one count for ideal-url-organizer across the page). A rule's body may print
`{days:key}`, the days from the repository's first commit (`repo_first`, any author, from git) to that anchor's
commit, and `{days:a..b}`, the days between two anchors' commits (fill_days); a day count nobody computed is not
printed (NOTICE-DATE).

Review round 7: a rule's cite must point at code that is still there. Each record carries `at_head`: the anchor's
text is in a file at HEAD that is not documentation (`head_paths` names them); NOTICE-LIVE fails a printed rule
whose anchor is not.
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


def repo_first(git_dir: str, timeout: int = 120) -> str | None:
    """The author date of the repository's earliest commit on HEAD, any author (review round 8: "after the first
    commit" in a rule's body); None without a history."""
    try:
        r = subprocess.run(["git", f"--git-dir={git_dir}", "log", "--format=%as", "HEAD"], capture_output=True,
                           text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    dates = sorted(x for x in r.stdout.split() if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x))
    return dates[0] if dates else None


def rule_records(notices: list[dict], git_dirs: dict[str, str], identity: dict, cache: list[dict] | None = None,
                 adding=commits_adding, first_of=repo_first) -> list[dict]:
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
            if str(a.get("author") or "") == "self":
                rec["scope"] = "self"
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
                live = live_paths(gd, text, a.get("path"))
                rec["at_head"] = bool(live)
                rec["head_paths"] = live[:3]          # a few of them, for the reader of stats.json
            if "{days:" in str(nt.get("body") or ""):
                rec["repo_first"] = first_of(gd)
            out.append(rec)
    return out


DOC_EXT = (".md", ".rst", ".txt", ".adoc")


def live_paths(git_dir: str, text: str, path: str | None = None, timeout: int = 120) -> list[str]:
    """The files at HEAD, documentation left out, that hold `text` (review round 7: the cited code is still there;
    a rule that names a practice may cite the month he started it even if that first file was later rebuilt, but
    the thing itself must still be in the code)."""
    args = ["git", f"--git-dir={git_dir}", "grep", "-l", "-F", "-e", text, "HEAD"]
    if path:
        args += ["--", path]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return []
    paths = [line.split(":", 1)[1] for line in r.stdout.splitlines() if ":" in line]
    return sorted(p for p in paths if not p.lower().endswith(DOC_EXT))


def dict_keys(src: str | None, name: str) -> list[str] | None:
    """The string keys of the dict literal assigned to `name` (`self.methods`, `METHODS`) anywhere in a Python file,
    read with ast; None when the file does not parse or holds no such assignment."""
    import ast
    try:
        tree = ast.parse(src or "")
    except (SyntaxError, ValueError):
        return None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Dict):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(ast.unparse(tg) == name for tg in targets):
                return [k.value for k in node.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
    return None


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


_DAYS = re.compile(r"\{days:([\w-]+)(?:\.\.([\w-]+))?\}")


def days_of(rules: list[dict], n: int, key: str, since: str | None = None) -> int | None:
    """Days from the repository's first commit (or from anchor `since`'s commit) to anchor `key`'s commit."""
    import datetime as dt
    recs = {x.get("key"): x for x in rules or [] if x.get("n") == n}
    r = recs.get(key)
    if not r or not r.get("found") or not r.get("date"):
        return None
    if since is None:
        start = r.get("repo_first")
    else:
        s0 = recs.get(since)
        start = s0.get("date") if s0 and s0.get("found") else None
    if not start:
        return None
    return (dt.date.fromisoformat(str(r["date"])[:10]) - dt.date.fromisoformat(str(start)[:10])).days


def fill_days(body: str, n: int, rules: list[dict]) -> tuple[str, list[str]]:
    """`{days:key}` and `{days:a..b}` -> whole days (review round 8); returns (text, placeholders not computed)."""
    missing = []

    def sub(m):
        a, b = m.group(1), m.group(2)
        got = days_of(rules, n, b, a) if b else days_of(rules, n, a)
        if got is None or got < 0:
            missing.append(m.group(0))
            return "?"
        return str(got)
    return _DAYS.sub(sub, str(body or "")), missing


def cite_keys(cite: str) -> list[str]:
    return _MONTH.findall(str(cite or ""))


# ---------------------------------------------------------------- the README's typed figures

def csv_rows(src: str, host: str | None = None) -> int:
    """Review round 10: the rows of a CSV file as Python's csv module reads them, which are the rows
    `pd.read_csv(path, header=None)` gives (a quoted field that never closes swallows the next line), blank rows
    left out. With `host`, only the rows whose first field's `urlsplit().hostname` is `host` or ends in "." + host."""
    import csv
    import io
    from urllib.parse import urlsplit
    n = 0
    for row in csv.reader(io.StringIO(src or "", newline="")):
        if not row:
            continue
        if host:
            try:
                h = urlsplit(row[0]).hostname or ""
            except ValueError:
                continue
            if h != host and not h.endswith("." + host):
                continue
        n += 1
    return n


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
        if f.get("keys"):        # review round 7: a count of a dict literal's keys
            rec["keys"] = str(f["keys"])
        if f.get("handoff"):
            rec["handoff"] = True
        if f.get("contains"):    # review round 8: only the matching files that contain this literal
            rec["contains"] = str(f["contains"])
        if f.get("parts"):
            rec["parts"] = [str(x) for x in f["parts"]]
        if f.get("csv_rows"):    # review round 10: a count of a CSV file's rows (and of those on one host)
            rec["csv_rows"] = True
            if f.get("host"):
                rec["host"] = str(f["host"])
        gd = git_dirs.get(rec["repo"])
        if not gd:
            old = cached.get((rec["text"], rec["repo"]))
            out.append(dict(old, stale=True) if old else dict(rec, why="no clone of the repository this run"))
            continue
        if rec["glob"]:
            files = [p for p in ls(gd) or [] if fnmatch.fnmatch(p, rec["glob"])]
            if rec.get("contains"):
                files = [p for p in files if rec["contains"] in (read(gd, p) or "")]
            n = len(files)
            rec["measured"] = n
            rec["holds"] = n == rec["count"]
            what = f" containing {rec['contains']!r}" if rec.get("contains") else ""
            rec["why"] = "" if rec["holds"] else f"{n} files match {rec['glob']}{what}, not {rec['count']}"
        else:
            src = read(gd, rec["path"]) if rec["path"] else None
            if src is None:
                rec["why"] = f"{rec['path']}: file missing at HEAD"
            elif rec["literal"] and str(rec["literal"]) not in src:
                rec["why"] = f"{rec['path']}: no {rec['literal']!r} at HEAD"
            elif rec.get("csv_rows"):
                n = csv_rows(src, rec.get("host"))
                rec["measured"] = n
                rec["holds"] = n == rec["count"]
                on = f" on {rec['host']}" if rec.get("host") else ""
                rec["why"] = "" if rec["holds"] else f"{rec['path']}: {n} rows{on}, not {rec['count']}"
            elif rec.get("keys"):
                keys = dict_keys(src, rec["keys"])
                rec["measured"] = len(keys) if keys is not None else None
                if keys is None:
                    rec["why"] = f"{rec['path']}: no dict literal assigned to {rec['keys']}"
                elif len(keys) != rec["count"]:
                    rec["why"] = f"{rec['path']}: {rec['keys']} has {len(keys)} keys, not {rec['count']}"
                else:
                    rec["holds"] = True
            else:
                rec["holds"] = True
        for a in f.get("also") or []:     # review round 7: literals the row's claim also rests on
            if not rec["holds"]:
                break
            s2 = read(gd, str(a.get("path")))
            if s2 is None or str(a.get("literal")) not in s2:
                rec["holds"] = False
                rec["why"] = f"{a.get('path')}: no {a.get('literal')!r} at HEAD"
        for a in f.get("absent") or []:   # review round 13: a pattern that would make the claim false
            if not rec["holds"]:
                break
            s2 = read(gd, str(a.get("path")))
            if s2 is None:
                rec["holds"], rec["why"] = False, f"{a.get('path')}: file missing at HEAD"
            elif re.search(str(a.get("pattern")), s2):
                rec["holds"] = False
                rec["why"] = f"{a.get('path')}: {a.get('pattern')!r} matches at HEAD"
        out.append(rec)
    by_text = {(r["text"], r["repo"]): r for r in out}
    for rec in out:          # review round 8: a split's parts add up to the whole
        if not rec.get("parts") or not rec["holds"]:
            continue
        parts = [by_text.get((t, rec["repo"])) for t in rec["parts"]]
        if any(p is None or p.get("measured") is None for p in parts):
            rec["holds"], rec["why"] = False, f"parts {rec['parts']} not all measured"
        elif sum(p["measured"] for p in parts) != rec["measured"]:
            rec["holds"] = False
            rec["why"] = (f"parts {' + '.join(str(p['measured']) for p in parts)} do not add up to "
                          f"{rec['measured']}")
    return out
