"""model — the stats.json v2 shape (TypedDicts) and `validate(stats) -> list[str]`.

The invariants MASTERPLAN §3.3 asks check.py to enforce live here so build_stats, the
checks plug-in and the tests share one implementation:
  repos is a list · sum(hours) == sum(weekdays) == commit_days per repo ·
  commits + Σ others == all_hands · no `seeded` key anywhere · provenance.mode ∈ {live, cache} ·
  taken ≤ 8 days old. Plus the JSON Schema (stats_schema.json, draft 2020-12) through a small
  stdlib validator (`schema_errors`) that covers the keywords the schema uses.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from typing import Any, TypedDict

SCHEMA_VERSION = 2
MAX_TAKEN_AGE_DAYS = 8
HERE = os.path.dirname(__file__)
STATS_SCHEMA_PATH = os.path.join(HERE, "stats_schema.json")
LOG_SCHEMA_PATH = os.path.join(HERE, "log_schema.json")


class Other(TypedDict):
    name: str
    commits: int
    bot: bool


class Day(TypedDict):
    d: str      # author-local date YYYY-MM-DD
    h: int      # modal hour that day (ties → earliest)
    n: int      # commits that day


class Repo(TypedDict, total=False):
    name: str
    aliases: list[str]
    slot: str | None
    commits: int
    merges: int          # of `commits`, those with two or more parents
    co_authored: int     # of `commits`, those carrying a Co-authored-by trailer
    all_hands: int
    others: list[Other]
    first: str | None
    last: str | None
    commit_days: int
    months_active: int
    hours: list[int]
    weekdays: list[int]
    weeks: list[int]
    week_days: list[int]
    days: list[Day]
    tz_offsets: dict[str, int]
    active: bool
    dormant: bool
    archived: bool
    stale: bool
    stale_since: str | None
    language: str | None
    stars: int | None
    span: str | None
    stale_branches: list[dict]


class Week(TypedDict):
    start: str
    n: int
    days: int
    repos: dict[str, int]


class Tide(TypedDict):
    hw: dict
    lw: dict
    median: float
    slack: dict


class Variation(TypedDict):
    hour: int | None
    year: int
    prior_hour: int | None
    annual_change: int | None
    basis_days: list[int]


class Provenance(TypedDict, total=False):
    mode: str
    failed_at: str | None
    soundings_taken: dict | None
    instruments: dict[str, str]


class Stats(TypedDict, total=False):
    schema: int
    updated_at: str
    taken: str
    run_id: str
    provenance: Provenance
    login: str
    account_since: str | None
    repo_count: int
    followers: int | None
    stars: int | None
    commits: int
    merges: int
    co_authored: int
    all_hands: int
    calendar_total: int | None
    calendar_weeks: list[dict] | None
    calendar: dict | None
    first_commit: str | None
    days_surveyed: int | None
    languages: list[dict]
    repos: list[Repo]
    unsurveyed: list[dict]
    hours: list[int]
    weekdays: list[int]
    hours_basis: str
    tz_offsets: dict[str, int]
    variation: Variation
    weeks: list[Week]
    tide: Tide
    sweeps: list[dict]
    edition: dict | None
    notices: list[dict]
    corrections: dict[str, list[dict]]
    claims: dict[str, dict]
    trial: dict | None
    sources: list[dict]


# ---------------------------------------------------------------- mini JSON Schema

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def _is_type(v: Any, t: str) -> bool:
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    return isinstance(v, _TYPES[t])


def schema_errors(obj: Any, schema: dict, root: dict | None = None, path: str = "$") -> list[str]:
    """Validate `obj` against a JSON Schema subset: type, enum, const, properties, required,
    additionalProperties, items, minItems/maxItems, minimum/maximum, pattern, anyOf, $ref (#/$defs)."""
    root = root if root is not None else schema
    errs: list[str] = []
    if "$ref" in schema:
        ref = schema["$ref"]
        target = root
        for part in ref.lstrip("#/").split("/"):
            target = target[part]
        return schema_errors(obj, target, root, path)
    if "anyOf" in schema:
        branches = [schema_errors(obj, s, root, path) for s in schema["anyOf"]]
        if not any(not b for b in branches):
            errs.append(f"{path}: matches none of anyOf ({'; '.join(b[0] for b in branches if b)})")
        return errs
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(obj, x) for x in types):
            return [f"{path}: expected {'|'.join(types)}, got {type(obj).__name__}"]
    if "enum" in schema and obj not in schema["enum"]:
        errs.append(f"{path}: {obj!r} not in {schema['enum']}")
    if "const" in schema and obj != schema["const"]:
        errs.append(f"{path}: {obj!r} != {schema['const']!r}")
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        if "minimum" in schema and obj < schema["minimum"]:
            errs.append(f"{path}: {obj} < minimum {schema['minimum']}")
        if "maximum" in schema and obj > schema["maximum"]:
            errs.append(f"{path}: {obj} > maximum {schema['maximum']}")
    if isinstance(obj, str):
        if "pattern" in schema and not re.search(schema["pattern"], obj):
            errs.append(f"{path}: {obj!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and len(obj) < schema["minLength"]:
            errs.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(obj) > schema["maxLength"]:
            errs.append(f"{path}: longer than maxLength {schema['maxLength']}")
    if isinstance(obj, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in obj:
                errs.append(f"{path}: missing required key {key!r}")
        for key, val in obj.items():
            if key in props:
                errs += schema_errors(val, props[key], root, f"{path}.{key}")
            else:
                extra = schema.get("additionalProperties", True)
                if extra is False:
                    errs.append(f"{path}: unexpected key {key!r}")
                elif isinstance(extra, dict):
                    errs += schema_errors(val, extra, root, f"{path}.{key}")
    if isinstance(obj, list):
        if "minItems" in schema and len(obj) < schema["minItems"]:
            errs.append(f"{path}: {len(obj)} items < minItems {schema['minItems']}")
        if "maxItems" in schema and len(obj) > schema["maxItems"]:
            errs.append(f"{path}: {len(obj)} items > maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(obj):
                errs += schema_errors(item, schema["items"], root, f"{path}[{i}]")
    return errs


def load_schema(path: str = STATS_SCHEMA_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- invariants

def find_key(obj: Any, key: str, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                hits.append(f"{path}.{k}")
            hits += find_key(v, key, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += find_key(v, key, f"{path}[{i}]")
    return hits


def validate(stats: dict, today: dt.date | None = None, schema: dict | None = None,
             allow_failed: bool = False) -> list[str]:
    """Every violated invariant as one line; [] means the model may be written.

    `allow_failed` lets build_stats re-stamp the cache as mode cache-failed (T1's failure step);
    check.py never passes it, so a cache-failed file fails CI as T7 decision 16 asks."""
    errs: list[str] = []
    today = today or dt.datetime.now(dt.timezone.utc).date()
    if not isinstance(stats, dict):
        return ["stats is not an object"]
    if stats.get("schema") != SCHEMA_VERSION:
        errs.append(f"schema must be {SCHEMA_VERSION}, got {stats.get('schema')!r}")
    for hit in find_key(stats, "seeded"):
        errs.append(f"forbidden key `seeded` at {hit}")
    repos = stats.get("repos")
    if not isinstance(repos, list):
        errs.append("repos must be a list")
        repos = []
    prov = stats.get("provenance") or {}
    mode = prov.get("mode")
    allowed = ("live", "cache", "cache-failed") if allow_failed else ("live", "cache")
    if mode not in allowed:
        errs.append(f"provenance.mode must be live|cache, got {mode!r}")
    taken = stats.get("taken")
    try:
        age = (today - dt.date.fromisoformat(taken)).days
        if age > MAX_TAKEN_AGE_DAYS:
            errs.append(f"taken {taken} is {age} days old (> {MAX_TAKEN_AGE_DAYS})")
        if age < -1:
            errs.append(f"taken {taken} is in the future")
    except (TypeError, ValueError):
        errs.append(f"taken must be YYYY-MM-DD, got {taken!r}")

    names = [r.get("name") for r in repos]
    if len(set(names)) != len(names):
        errs.append("repos[].name not unique")
    for r in repos:
        n = r.get("name", "?")
        hours, wdays = r.get("hours") or [], r.get("weekdays") or []
        if len(hours) != 24 or len(wdays) != 7:
            errs.append(f"{n}: hours[{len(hours)}]/weekdays[{len(wdays)}] wrong length")
        cd = r.get("commit_days")
        if not (sum(hours) == sum(wdays) == cd):
            errs.append(f"{n}: sum(hours)={sum(hours)} sum(weekdays)={sum(wdays)} commit_days={cd}")
        days = r.get("days")
        if isinstance(days, list) and len(days) != cd:
            errs.append(f"{n}: len(days)={len(days)} != commit_days={cd}")
        others = sum(o.get("commits", 0) for o in r.get("others") or [])
        if r.get("commits", 0) + others != r.get("all_hands"):
            errs.append(f"{n}: commits {r.get('commits')} + others {others} != all_hands {r.get('all_hands')}")
        for key in ("merges", "co_authored"):
            if key in r and r[key] > r.get("commits", 0):
                errs.append(f"{n}: {key} {r[key]} > commits {r.get('commits')}")
        if len(r.get("weeks") or []) != 52:
            errs.append(f"{n}: weeks must have 52 entries")
        if isinstance(days, list) and r.get("weeks") and sum(r["weeks"]) > sum(d.get("n", 0) for d in days):
            errs.append(f"{n}: weekly commits exceed commit-day commits")
    if repos:
        if stats.get("commits") != sum(r.get("commits", 0) for r in repos):
            errs.append("commits != Σ repos[].commits")
        if stats.get("all_hands") != sum(r.get("all_hands", 0) for r in repos):
            errs.append("all_hands != Σ repos[].all_hands")
        for key in ("merges", "co_authored"):
            if key in stats and stats[key] != sum(r.get(key, 0) for r in repos):
                errs.append(f"{key} != Σ repos[].{key}")
        for key, n in (("hours", 24), ("weekdays", 7)):
            tot = stats.get(key) or []
            if len(tot) != n or any(tot[i] != sum((r.get(key) or [0] * n)[i] for r in repos) for i in range(n)):
                errs.append(f"{key} != Σ repos[].{key}")
    weeks = stats.get("weeks") or []
    if len(weeks) != 52:
        errs.append(f"weeks must have 52 entries, got {len(weeks)}")
    for i, w in enumerate(weeks):
        if isinstance(w, dict) and w.get("n") != sum((w.get("repos") or {}).values()):
            errs.append(f"weeks[{i}].n != Σ repos")
        if isinstance(w, dict) and w.get("sweep", 0) > w.get("n", 0):
            errs.append(f"weeks[{i}].sweep > n")
    tide = stats.get("tide") or {}
    if weeks and tide.get("hw") and tide["hw"].get("n") != max(w.get("n", 0) for w in weeks):
        errs.append("tide.hw.n != max weeks[].n")
    if stats.get("repo_count") is not None and len(repos) + len(stats.get("unsurveyed") or []) > stats["repo_count"]:
        errs.append("len(repos) + len(unsurveyed) > repo_count")
    for cid, c in (stats.get("claims") or {}).items():
        if c.get("measured") and not (c.get("source") and c.get("sha")):
            errs.append(f"claims.{cid}: measured without source+sha")
    if stats.get("hours_basis") != "author-local commit-days":
        errs.append("hours_basis must be 'author-local commit-days'")
    try:
        errs += schema_errors(stats, schema or load_schema())
    except (OSError, ValueError) as exc:
        errs.append(f"schema unreadable: {exc}")
    return errs
