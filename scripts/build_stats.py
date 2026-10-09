#!/usr/bin/env python3
"""Take the day's soundings and write assets/stats.json v2 — one in-memory model, validated, written once.

    python3 scripts/build_stats.py                    # mode from the environment: live with GITHUB_TOKEN, else cache
    python3 scripts/build_stats.py --mode cache       # survey the clones + PyPI + REST; GraphQL from the cache
    python3 scripts/build_stats.py --mode cache-failed  # no sounding: re-stamp the cache (T1's `if: failure()` step)
    python3 scripts/build_stats.py --out /tmp/s.json  # the cache is still assets/stats.json unless --cache says otherwise

Cache mode carries a GraphQL figure (followers, stars, account_since, calendar_*) only when the cache
says when it was fetched (`provenance.graphql_at`); a figure with no dated fetch behind it is dropped,
not reprinted (the v1 file's seeded figures lived on that way until round 5).

    build_stats.main(mode) -> dict                     the model that was written
    build_stats.derive(repos, calendar, pypi, releases) -> dict   (T7 interface; thin over data.derive)

No rendering happens here (build_assets.py is separate). Nothing is written when validation fails.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ASSETS, LOG_PATH, LOGIN, ROOT, STATS_PATH, claims as claims_mod, derive as derive_mod  # noqa: E402
from data import github, logsim, model, pypi, releases as releases_mod, survey as survey_mod, tree as tree_mod  # noqa: E402
from data import load_chart_toml  # noqa: E402

MODES = ("live", "cache", "cache-failed")
FLAGSHIP = "Rust-sitemap"
PYPI_PROJECT = "rustmapper"
SOUNDING_WINDOW_DAYS = 150


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def load_cache(path: str = STATS_PATH) -> dict:
    """The last written model, or {} when there is none. A corrupted cache is a hard failure:
    nothing can be re-stamped from it and nothing ships (T7 §4 "no cache and no clone")."""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}
    except ValueError as exc:
        raise SystemExit(f"cache {path} is not valid JSON: {exc}")


def cache_fields(cache: dict) -> dict:
    """GraphQL-sourced fields from the last v2 file, carried only when that file records the fetch
    (`provenance.graphql_at`). A file without one (a v1 file, or a v2 file built from it) has no
    measurement behind those figures, so they come back None and the instrument reads "none"."""
    if not cache:
        return {}
    fetched = (cache.get("provenance") or {}).get("graphql_at") if cache.get("schema") == 2 else None
    if not fetched:
        return {"graphql_at": None, "languages": []}
    return {
        "account_since": cache.get("account_since"),
        "followers": cache.get("followers"),
        "stars": cache.get("stars"),
        "repo_count": cache.get("repo_count"),
        "calendar_total": cache.get("calendar_total"),
        "calendar_weeks": cache.get("calendar_weeks"),
        "calendar": cache.get("calendar"),
        "languages": cache.get("languages") or [],
        "graphql_at": fetched,
    }


def soundings_taken(path: str = STATS_PATH, days: int = SOUNDING_WINDOW_DAYS) -> dict | None:
    """{taken, of}: days in the window on which stats.json was committed (needs fetch-depth: 0)."""
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        return None
    try:
        out = subprocess.run(["git", "-C", ROOT, "log", f"--since={days} days ago", "--format=%cs", "--",
                              os.path.relpath(path, ROOT)], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return {"taken": len(set(out.stdout.split())), "of": days}


def trial_from_clone(git_dir: str | None) -> dict | None:
    """Scrapy's exports/run-YYYY-MM-DD.json at HEAD → the anchorage soundings, or None."""
    if not git_dir:
        return None
    runs = sorted(p for p in survey_mod.ls_tree(git_dir, "exports") if re.fullmatch(r"exports/run-\d{4}-\d{2}-\d{2}\.json", p))
    if not runs:
        return None
    raw = survey_mod.file_at_head(git_dir, runs[-1])
    try:
        d = json.loads(raw or "")
    except ValueError:
        return None
    if not isinstance(d, dict) or "rows" not in d:
        return None
    return {"date": d.get("date") or runs[-1][12:22], "host": d.get("host"), "rows": d.get("rows") or {},
            "delta_versions": d.get("delta_versions") or {}, "wall_s": float(d.get("wall_s") or 0),
            "fivexx_rate": float(d.get("fivexx_rate") or 0)}


def charted_branches(branches: list[dict] | None, identity: dict | None = None) -> list[dict]:
    """The stale branches a hydrographer would chart as wrecks: a branch whose tip was authored by a bot
    (`identity.bots` in chart.toml) is dropped; a branch surveyed without an author (an older cache) stays."""
    return [b for b in branches or [] if not survey_mod.is_bot(str(b.get("author") or ""), identity)]


def derive(repos: list[dict], calendar: list[dict] | None = None, pypi_edition: dict | None = None,
           releases: list[dict] | None = None, taken: dt.date | None = None) -> dict:
    """T7 interface: the derived block for a list of repos[] records."""
    return derive_mod.derive(repos, taken or now_utc().date(), calendar)


def assemble(records: list[dict], taken: dt.date, updated_at: str, run_id: str, mode: str, gh: dict,
             edition: dict | None, notices: list[dict], corrections: dict, claims: dict, trial: dict | None,
             sources: list[dict], unsurveyed: list[dict], instruments: dict, features: dict | None = None,
             failed_at: str | None = None, soundings: dict | None = None) -> dict:
    """Pure: records + fetched blocks → the v2 model (also what the tests build fixtures with)."""
    d = derive_mod.derive(records, taken, gh.get("calendar"))
    repos = d.pop("repos")
    for r in repos:
        f = (features or {}).get(r["name"]) or {}
        r["aliases"] = list(f.get("aliases") or r.get("aliases") or [])
        r["slot"] = f.get("slot") or r.get("slot")
    repos.sort(key=lambda r: (-r["commits"], r["name"]))
    stats = {
        "schema": 2,
        "updated_at": updated_at,
        "taken": taken.isoformat(),
        "run_id": run_id,
        "provenance": {"mode": mode, "failed_at": failed_at, "soundings_taken": soundings, "instruments": instruments,
                       "graphql_at": gh.get("fetched_at") or gh.get("graphql_at")},
        "login": LOGIN,
        "account_since": gh.get("account_since"),
        "repo_count": gh.get("repo_count") if gh.get("repo_count") is not None else len(repos) + len(unsurveyed),
        "followers": gh.get("followers"),
        "stars": gh.get("stars"),
        "calendar_total": gh.get("calendar_total"),
        "calendar_weeks": gh.get("calendar_weeks"),
        "calendar": gh.get("calendar"),
        "languages": gh.get("languages") or [],
        "repos": repos,
        "unsurveyed": unsurveyed,
        "edition": edition,
        "notices": [dict(n, n=i + 1) for i, n in enumerate(notices)],
        "corrections": corrections,
        "claims": claims,
        "trial": trial,
        "sources": sources,
    }
    stats.update(d)
    return stats


def ensure_log(stats: dict, path: str = LOG_PATH) -> dict:
    """assets/log.json: write the computed default once; never touch a measured session."""
    version = (stats.get("edition") or {}).get("version") or "0.0.0"
    try:
        with open(path, encoding="utf-8") as fh:
            existing = json.load(fh)
    except (FileNotFoundError, ValueError):
        existing = None
    if existing and existing.get("schema") == 2 and existing.get("measured"):
        return existing
    cores = ((existing or {}).get("machine") or {}).get("cores", 8)
    date = (existing or {}).get("date") or stats["taken"]
    log = logsim.default_log(version, date, cores=cores, host=((existing or {}).get("machine") or {}).get("host"))
    errs = logsim.check_log(log) + model.schema_errors(log, model.load_schema(model.LOG_SCHEMA_PATH))
    if errs:
        raise SystemExit("log.json would be inconsistent:\n  " + "\n  ".join(errs))
    if existing != log:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(log, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
    return log


def main(mode: str | None = None, out: str = STATS_PATH, workdir: str | None = None, repos: list[str] | None = None,
         write_log: bool = True, workers: int = 6, cache_path: str | None = None) -> dict:
    cfg = load_chart_toml()
    token = github.token_from_env()
    mode = mode or ("live" if token else "cache")
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    cache = load_cache(cache_path or STATS_PATH)
    now = now_utc()
    updated_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    taken = now.date()
    run_id = os.environ.get("GITHUB_RUN_ID") or "local"
    identity = survey_mod.identity_from_toml(cfg)
    owner = identity.get("login", LOGIN)
    features = {f["repo"]: f for f in cfg.get("features", []) if isinstance(f, dict) and f.get("repo")}
    flagship = next((f["repo"] for f in features.values() if f.get("kind") == "vessel"), FLAGSHIP)
    flagships = {flagship, "Scrapy"} | {f["repo"] for f in features.values() if f.get("kind") in ("vessel", "harbour")}
    lines_cfg = tree_mod.lines_config(cfg)
    sources = [{"letter": s.get("letter", ""), "name": s.get("name", ""), "first": s.get("first")} for s in cfg.get("sources", [])]

    if mode == "cache-failed":
        if cache.get("schema") != 2:
            raise SystemExit("cache-failed needs a v2 cache; nothing to re-stamp")
        stats = dict(cache)
        stats["updated_at"] = updated_at
        stats["run_id"] = run_id
        stats["provenance"] = {**stats["provenance"], "mode": "cache-failed", "failed_at": updated_at}
        errs = model.validate(stats, allow_failed=True)
        if errs:
            raise SystemExit("cache is not a valid v2 model:\n  " + "\n  ".join(errs))
        _write(stats, out)
        print(f"mode=cache-failed · re-stamped {out}")
        return stats

    gh = cache_fields(cache)
    instruments = {"clones": "none", "graphql": "cache" if gh.get("graphql_at") else "none",
                   "rest": "none", "pypi": "none", "releases": "none"}
    if cache and not gh.get("graphql_at"):
        print("cache has no dated GraphQL fetch: followers, stars, account_since and calendar figures are not carried")
    if mode == "live":
        try:
            window = (survey_mod.week_starts(taken)[0], taken)   # the 52 clone weeks, so the check compares like with like
            gh = github.fetch(token, owner, window) if token else gh
            instruments["graphql"] = "live" if token else instruments["graphql"]
        except Exception as exc:  # the second instrument is optional; the clones are the measurement
            print("graphql failed, keeping cached fields:", exc)
            mode = "cache"
    names = repos or (list(gh["repo_meta"].keys()) if gh.get("repo_meta") else [r["name"] for r in cache.get("repos", [])])
    if not names:
        raise SystemExit("no repository list: no GraphQL and no cache")
    meta = gh.get("repo_meta") or github.rest_meta(owner, names, token)
    if meta and not gh.get("repo_meta"):
        # the REST instrument only counts as a fleet measurement when it answered for every repo;
        # a partial sample must not pose as "languages by bytes" (keep the cached GraphQL shares)
        complete = all(n in meta for n in names)
        instruments["rest"] = "live" if complete else "partial"
        if complete and any(m.get("languages") for m in meta.values()):
            gh["languages"] = github.languages_from_meta(meta)
        if complete:   # the fleet's stars, measured today, rather than a cached account total
            gh["stars"] = sum(int(m.get("stars") or 0) for m in meta.values())
    ed = pypi.edition(PYPI_PROJECT)
    if ed:
        instruments["pypi"] = "live"
    elif cache.get("edition"):
        ed = {**cache["edition"], "stale": True}
        ed.setdefault("status", None); ed.setdefault("wheels", [])
        instruments["pypi"] = "cache"

    tmp = tempfile.TemporaryDirectory() if workdir is None else None
    wd = workdir or tmp.name
    try:
        results = survey_mod.survey_all(names, wd, identity, taken, owner, keep_history_for={owner} | flagships,
                                        workers=workers, lines_cfg=lines_cfg)
        cached_v2 = {r["name"]: r for r in cache.get("repos", [])} if cache.get("schema") == 2 else {}
        records, failed = [], []
        profile_commits: list = []
        scrapy_dir = None
        for name in names:
            rec = results.get(name)
            if rec:
                instruments["clones"] = "live"
                if name == owner:
                    profile_commits = rec.get("_commits", [])
                if name == "Scrapy":
                    scrapy_dir = rec.get("_git_dir")
                rec.pop("_commits", None)
                rec.pop("_git_dir", None)
            elif name in cached_v2:
                rec = dict(cached_v2[name], stale=True, stale_since=cached_v2[name].get("stale_since") or cache.get("taken"))
            else:
                failed.append(name)
                continue
            m = meta.get(name) or {}
            rec["stale_branches"] = charted_branches(rec.get("stale_branches"), identity)
            rec["stale_branch_count"] = len(rec["stale_branches"])
            if (features.get(name) or {}).get("kind") != "harbour" and name != "Scrapy":
                rec["stale_branches"] = []      # the list is charted only in the harbour (MASTERPLAN 25)
            rec["archived"] = bool(m.get("archived", rec.get("archived", False)))
            rec["stars"] = m.get("stars", rec.get("stars"))
            rec["language"] = m.get("language", rec.get("language"))
            if name in flagships:   # D4: the project's own CI on its default branch, where the API answers
                ci = github.rest_runs(owner, name, token, m.get("default_branch") or "main")
                if ci is not None:
                    rec["ci"] = ci
                elif name in cached_v2 and cached_v2[name].get("ci"):
                    rec["ci"] = dict(cached_v2[name]["ci"], stale=True)
            records.append(rec)
        if not records:
            raise SystemExit("no history and no cache: nothing ships")
        trial = trial_from_clone(scrapy_dir)
        hand = [n for n in cfg.get("notices", []) if isinstance(n, dict)]
        notices = releases_mod.notices(flagship, ed, profile_commits, hand, token, owner, owner, identity,
                                       cached=cache.get("notices"))
        instruments["releases"] = "live" if github.rest_releases(owner, flagship, token) is not None else \
            ("cache" if cache.get("notices") else "none")
    finally:
        if tmp:
            tmp.cleanup()

    known = list(gh["repo_meta"].keys()) if gh.get("repo_meta") else []
    unsurveyed = derive_mod.unsurveyed(known, [r["name"] for r in records], failed)
    stats = assemble(records, taken, updated_at, run_id, mode, gh, ed, notices,
                     derive_mod.corrections(profile_commits, identity), claims_mod.claims(cfg), trial, sources,
                     unsurveyed, instruments, features, soundings=soundings_taken(out))
    errs = model.validate(stats)
    if errs:
        raise SystemExit("model invalid; nothing written:\n  " + "\n  ".join(errs))
    _write(stats, out)
    if write_log:
        ensure_log(stats)
    v = stats["variation"]
    cc = stats.get("calendar_check") or {}
    cal = stats.get("calendar") or {}
    in_window = sum(w["n"] for w in stats["weeks"])
    co = stats["coauthored_total"]
    print(f"mode={mode} · {len(stats['repos'])} repos · {stats['commits']} commits authored by {owner} on HEAD "
          f"({stats['merges']} merges, {co['count']} with co-author trailers, {co['agent']} naming an agent) of "
          f"{stats['all_hands']} by anyone · sweeps {', '.join(stats['sweep_dates']) or 'none'} · "
          f"{in_window} in the 52 clone weeks" +
          (f" vs {cc.get('calendar')} GitHub credits on the same repos ({cc.get('disagreement', 0) or 0:.0%} apart)"
           if cc else "") +
          (f" · GitHub's green squares {cal['all']} = commits {cal['commits']} + issues {cal['issues']} + PRs "
           f"{cal['pull_requests']} + reviews {cal['reviews']} + private {cal['restricted']}" if cal else "") +
          f" · GitHub's all-time commit credit {stats['calendar_total']} · Var. {v['hour']}h ({v['year']}) · "
          f"HW {stats['tide']['hw']['n']} wk of {stats['tide']['hw']['start']} ({stats['tide']['hw']['cause']}, "
          f"{stats['tide']['hw']['cause_days']} days) · N={len(stats['notices'])}")
    return stats


def _write(stats: dict, out: str) -> None:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--mode", choices=MODES, default=None)
    ap.add_argument("--out", default=STATS_PATH)
    ap.add_argument("--cache", default=None, help="the previous stats.json to carry fields from (default: assets/stats.json)")
    ap.add_argument("--no-log", action="store_true", help="do not touch assets/log.json")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("repos", nargs="*", help="survey only these repositories")
    a = ap.parse_args(argv)
    main(a.mode, a.out, repos=a.repos or None, write_log=not a.no_log, workers=a.workers, cache_path=a.cache)
    return 0


if __name__ == "__main__":
    sys.exit(cli())
