"""derive — everything the sheets read that is computed from the per-repo measurements.

    derive(repos, taken, calendar=None, sweep_min=5) -> dict
      weeks[52], tide, variation, sweeps, hours[24], weekdays[7], tz_offsets, commits, all_hands,
      first_commit, days_surveyed, active/dormant written onto each repo (copies), sweep_threshold
    corrections(commits, identity) -> {year: [{n, date, title}]}
    unsurveyed(known, surveyed, failed) -> [{name, reason}]

Units (MASTERPLAN decision 18): weeks[].n = commits (author-filtered), weeks[].days = commit-days;
hours and weekdays are commit-days in author-local time. Active = commit-days in ≥ 3 of the last
12 weeks; dormant = no commit-day in 90 days; both after sweep days are removed (T7 decision 10).

A sweep day (a commit-day in ≥ sweep_threshold repos at once: a mass merge, a rename, a license
pass) is NOT removed from weeks[], tide, hours or commit_days: those count what the clones hold.
It is named instead: weeks[].sweep = commits on sweep days in that week, tide.hw.sweep_share =
their share of the high-water week, `sweep_dates` lists them. The figures the page draws from
(round 5, D2) leave sweep days out and say so: repos[].months = commit-days per month without
them, repos[].first_ns / last_ns = the first and last non-sweep commit-day.
"""
from __future__ import annotations

import copy
import datetime as dt
import math
import statistics
from collections import Counter, defaultdict

from .survey import AUTOMATION, Commit, WEEKS, is_ben, week_start, week_starts
from .tree import main_language

SWEEP_MIN_REPOS = 5
ACTIVE_WEEKS = 12
ACTIVE_MIN = 3
DORMANT_DAYS = 90
VARIATION_MIN_DAYS = 60


def sweep_threshold(n_repos: int, sweep_min: int = SWEEP_MIN_REPOS) -> int:
    """A sweep day touches ≥ ⅓ of the fleet (T7) or ≥ `sweep_min` repos (whichever is fewer), never < 2."""
    return max(2, min(sweep_min, math.ceil(n_repos / 3))) if n_repos else sweep_min


def sweeps(repos: list[dict], threshold: int) -> list[dict]:
    touched: dict[str, list[str]] = defaultdict(list)
    for r in repos:
        for day in r.get("days") or []:
            touched[day["d"]].append(r["name"])
    out = [{"date": d, "repos": len(names), "names": sorted(names)} for d, names in touched.items()
           if len(names) >= threshold]
    out.sort(key=lambda s: s["date"])
    return out


def activity(repo: dict, taken: dt.date, sweep_dates: set[str]) -> tuple[bool, bool]:
    """(active, dormant) on the repo's commit-days with sweep days removed."""
    days = [dt.date.fromisoformat(d["d"]) for d in repo.get("days") or [] if d["d"] not in sweep_dates]
    starts = week_starts(taken, ACTIVE_WEEKS)
    recent = {week_start(d) for d in days if d >= starts[0]}
    active = len(recent) >= ACTIVE_MIN
    dormant = not any((taken - d).days <= DORMANT_DAYS for d in days)
    return active, dormant


def months_without_sweeps(repo: dict, sweep_dates: set[str]) -> tuple[dict[str, int], str | None, str | None]:
    """({YYYY-MM: commit-days}, first, last) over the repo's commit-days that are not sweep days."""
    days = sorted(d["d"] for d in repo.get("days") or [] if d["d"] not in sweep_dates)
    months: Counter = Counter(d[:7] for d in days)
    return dict(sorted(months.items())), (days[0] if days else None), (days[-1] if days else None)


def weekly(repos: list[dict], taken: dt.date, sweep_dates: set[str] = frozenset()) -> list[dict]:
    starts = week_starts(taken)
    weeks = [{"start": s.isoformat(), "n": 0, "days": 0, "sweep": 0, "repos": {}} for s in starts]
    idx = {s: i for i, s in enumerate(starts)}
    dates: list[set[str]] = [set() for _ in starts]
    for r in repos:
        for i, n in enumerate(r.get("weeks") or [0] * WEEKS):
            if n:
                weeks[i]["n"] += n
                weeks[i]["repos"][r["name"]] = n
        for day in r.get("days") or []:
            i = idx.get(week_start(dt.date.fromisoformat(day["d"])))
            if i is not None:
                dates[i].add(day["d"])
                if day["d"] in sweep_dates:
                    weeks[i]["sweep"] += day["n"]
    for i, w in enumerate(weeks):
        w["days"] = len(dates[i])   # distinct commit-days in the week (≤ 7), not repo-days
    return weeks


def consecutive_run(dates: list[dt.date], lo: dt.date, hi: dt.date) -> int:
    """Length of the longest run of consecutive commit-days that intersects [lo, hi]."""
    best = 0
    ds = sorted(set(dates))
    i = 0
    while i < len(ds):
        j = i
        while j + 1 < len(ds) and (ds[j + 1] - ds[j]).days == 1:
            j += 1
        if ds[i] <= hi and ds[j] >= lo:
            best = max(best, j - i + 1)
        i = j + 1
    return best


def tide(weeks: list[dict], repos: list[dict]) -> dict:
    n = [w["n"] for w in weeks]
    hi = max(range(len(n)), key=lambda i: (n[i], i))
    hw_week = weeks[hi]
    cause, cause_days, share = None, 0, 0.0
    if hw_week["repos"]:
        cause = max(hw_week["repos"].items(), key=lambda kv: (kv[1], kv[0]))[0]
        share = hw_week["repos"][cause] / hw_week["n"] if hw_week["n"] else 0.0
        repo = next(r for r in repos if r["name"] == cause)
        lo = dt.date.fromisoformat(hw_week["start"])
        cause_days = consecutive_run([dt.date.fromisoformat(d["d"]) for d in repo.get("days") or []],
                                     lo, lo + dt.timedelta(days=6))
    complete = weeks[:-1] if len(weeks) > 1 else weeks
    lo_i = min(range(len(complete)), key=lambda i: (complete[i]["n"], -i))
    median = statistics.median([w["n"] for w in complete]) if complete else 0
    median = int(median) if float(median).is_integer() else float(median)
    # slack water: the lowest rolling four-week sum over complete weeks
    win = 4 if len(complete) >= 4 else len(complete)
    sums = [sum(w["n"] for w in complete[i:i + win]) for i in range(len(complete) - win + 1)]
    si = min(range(len(sums)), key=lambda i: (sums[i], -i)) if sums else 0
    s_start = dt.date.fromisoformat(complete[si]["start"])
    s_end = dt.date.fromisoformat(complete[si + win - 1]["start"]) + dt.timedelta(days=6)
    mid = s_start + (s_end - s_start) / 2
    return {
        "hw": {"start": hw_week["start"], "n": hw_week["n"], "cause": cause, "cause_days": cause_days,
               "cause_share": round(share, 3),
               "sweep_share": round(hw_week.get("sweep", 0) / hw_week["n"], 3) if hw_week["n"] else 0.0},
        "lw": {"start": complete[lo_i]["start"], "n": complete[lo_i]["n"]},
        "median": median,
        "slack": {"start": s_start.isoformat(), "end": s_end.isoformat(), "month": mid.strftime("%Y-%m"),
                  "n": sums[si] if sums else 0},
    }


def circ_diff(a: int, b: int) -> int:
    """a − b on the 24-hour dial, in −12…12."""
    d = (a - b) % 24
    return d - 24 if d > 12 else d


def variation(repos: list[dict], taken: dt.date, min_days: int = VARIATION_MIN_DAYS) -> dict:
    cur, prior = Counter(), Counter()
    lo_cur, lo_prior = taken - dt.timedelta(days=365), taken - dt.timedelta(days=730)
    for r in repos:
        for day in r.get("days") or []:
            d = dt.date.fromisoformat(day["d"])
            if lo_cur < d <= taken:
                cur[day["h"]] += 1
            elif lo_prior < d <= lo_cur:
                prior[day["h"]] += 1

    def modal(c: Counter) -> int | None:
        if not c:
            return None
        top = max(c.values())
        return min(h for h, k in c.items() if k == top)

    hour, prior_hour = modal(cur), modal(prior)
    basis = [sum(cur.values()), sum(prior.values())]
    change = circ_diff(hour, prior_hour) if (hour is not None and prior_hour is not None
                                            and basis[0] >= min_days and basis[1] >= min_days) else None
    return {"hour": hour, "year": taken.year, "prior_hour": prior_hour, "annual_change": change,
            "basis_days": basis, "min_basis_days": min_days}


def derive(repos: list[dict], taken: dt.date, calendar: dict | None = None,
           sweep_min: int = SWEEP_MIN_REPOS) -> dict:
    """The derived block. Repos are copied; active/dormant are written on the copies ("repos").
    `calendar` is github.fetch()'s window block (commits GitHub credits to the account over the
    same 52 weeks, per repository); with it, `calendar_check` compares like with like."""
    repos = [copy.deepcopy(r) for r in repos]
    thr = sweep_threshold(len(repos), sweep_min)
    sw = sweeps(repos, thr)
    sweep_dates = {s["date"] for s in sw}
    for r in repos:
        r["active"], r["dormant"] = activity(r, taken, sweep_dates)
        r["months"], r["first_ns"], r["last_ns"] = months_without_sweeps(r, sweep_dates)
        r["main_language"] = main_language(r.get("lines"))
        if r.get("test_functions") == 0 and r["main_language"] not in ("Rust", "Python"):
            r["test_functions"] = None     # only Rust and Python test functions are counted; no false "0 tests"
    weeks = weekly(repos, taken, sweep_dates)
    firsts = [r["first"] for r in repos if r.get("first")]
    first_commit = min(firsts) if firsts else None
    offsets: Counter = Counter()
    for r in repos:
        offsets.update(r.get("tz_offsets") or {})
    out = {
        "repos": repos,
        "commits": sum(r.get("commits", 0) for r in repos),
        "merges": sum(r.get("merges", 0) for r in repos),
        "coauthored_total": coauthored_total(repos),
        "agent_authored": agent_authored(repos),
        "all_hands": sum(r.get("all_hands", 0) for r in repos),
        "first_commit": first_commit,
        "days_surveyed": (taken - dt.date.fromisoformat(first_commit)).days if first_commit else None,
        "hours": [sum((r.get("hours") or [0] * 24)[h] for r in repos) for h in range(24)],
        "weekdays": [sum((r.get("weekdays") or [0] * 7)[d] for r in repos) for d in range(7)],
        "hours_basis": "author-local commit-days",
        "tz_offsets": dict(offsets.most_common()),
        "variation": variation(repos, taken),
        "weeks": weeks,
        "tide": tide(weeks, repos) if repos else None,
        "sweeps": sw,
        "sweep_dates": sorted(sweep_dates),
        "sweep_threshold": thr,
    }
    if isinstance(calendar, dict) and calendar.get("commits_by_repo") is not None:
        out["calendar_check"] = calendar_check(weeks, calendar, [r["name"] for r in repos])
    return out


def coauthored_total(repos: list[dict]) -> dict:
    """Σ repos[].coauthored: {count, share (of Σ commits), agent, names}."""
    count = agent = commits = 0
    names: Counter = Counter()
    for r in repos:
        c = r.get("coauthored") or {}
        count += int(c.get("count", 0))
        agent += int(c.get("agent", 0))
        commits += int(r.get("commits", 0))
        names.update(c.get("names") or {})
    return {"count": count, "share": round(count / commits, 3) if commits else 0.0, "agent": agent,
            "agent_share": round(agent / commits, 3) if commits else 0.0, "names": dict(names.most_common())}


def agent_authored(repos: list[dict]) -> dict:
    """Commits on HEAD whose *author* is a coding agent (`others[]` with bot: true, less dependency and CI
    automation): {total, names{name: commits}, automation{name: commits}}. None of these is in `commits`."""
    agents: Counter = Counter()
    automation: Counter = Counter()
    for r in repos:
        for o in r.get("others") or []:
            if not o.get("bot"):
                continue
            (automation if o["name"] in AUTOMATION else agents)[o["name"]] += int(o.get("commits", 0))
    return {"total": sum(agents.values()), "names": dict(sorted(agents.items(), key=lambda kv: (-kv[1], kv[0]))),
            "automation": dict(sorted(automation.items(), key=lambda kv: (-kv[1], kv[0])))}


def calendar_check(weeks: list[dict], calendar: dict, surveyed: list[str]) -> dict:
    """Like against like: Σ weeks[].n (Ben's commits on HEAD of the surveyed repos, the 52 clone weeks)
    against the commits GitHub credits to the account in the SAME repositories over the SAME window
    (`commits_by_repo`, from contributionsCollection(from, to)). Issues, pull requests, reviews,
    private and unsurveyed repositories are left out of both sides; check.py warns at > 10 %.

    What can still differ: a commit whose author email is not on the GitHub account (GitHub drops it),
    a day's boundary (GitHub counts UTC days, the clones author-local days) and the window's edges."""
    by_repo = calendar.get("commits_by_repo") or {}
    cal = sum(int(by_repo.get(name, 0)) for name in surveyed)
    clone = sum(w["n"] for w in weeks)
    ratio = abs(clone - cal) / cal if cal else None
    return {"clone": clone, "calendar": cal, "disagreement": None if ratio is None else round(ratio, 3),
            "from": calendar.get("from"), "to": calendar.get("to"),
            "basis": "commits by the account on the default branch of the surveyed public repositories, "
                     "52 weeks: clones vs GitHub contributionsCollection"}


def corrections(commits: list[Commit], identity: dict | None = None) -> dict[str, list[dict]]:
    """Small corrections: the profile repo's own human commits, enumerated per year, upright."""
    mine = sorted((c for c in commits if is_ben(c.name, c.email, identity)), key=lambda c: c.when)
    out: dict[str, list[dict]] = {}
    for i, c in enumerate(mine, 1):
        out.setdefault(str(c.local_date.year), []).append(
            {"n": i, "date": c.local_date.isoformat(), "title": c.subject.strip()[:120]})
    return out


def unsurveyed(known: list[str], surveyed: list[str], failed: list[str] = ()) -> list[dict]:
    """GraphQL repos that returned no history (ED), plus clone failures with no cached record."""
    have = set(surveyed)
    out = [{"name": n, "reason": "clone failed"} for n in failed if n not in have]
    out += [{"name": n, "reason": "no history"} for n in known if n not in have and n not in failed]
    return sorted(out, key=lambda u: u["name"])
