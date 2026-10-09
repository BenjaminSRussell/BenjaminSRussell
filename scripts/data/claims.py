"""claims — figures about the code (workers, shards, scrape interval) that are NOT measurements of Ben.

    claims(cfg=None) -> dict[id, {value, unit, source, sha, measured}]
    job_interval(prometheus_yml, job) -> int | None      a scrape job's own scrape_interval, in seconds
    verify_scrape_interval(claims, read) -> claims        re-read the cited job at the cited sha

Read from chart.toml `[claims.<id>]`. `measured` is true only when the toml says so AND a
`source` and `sha` are given; otherwise false, and the sheets set the figure italic. Nothing is
upright unless measured (MASTERPLAN decision 14: "512" is never upright). Without chart.toml the
defaults carry TECH-BRIEF's verified facts, all `measured:false`.
"""
from __future__ import annotations

import re

from . import load_chart_toml

DEFAULTS: dict[str, dict] = {
    "workers": {"value": "256–1024", "unit": "permits", "source": "Rust-sitemap:src/governor.rs", "sha": None,
                "measured": False},
    "shards": {"value": "num_cpus", "unit": "shards", "source": "Rust-sitemap:src/frontier.rs", "sha": None,
               "measured": False},
    "scrape_interval": {"value": None, "unit": "s", "source": None, "sha": None, "measured": False},
}


def normalize(cid: str, raw: dict) -> dict:
    src = raw.get("source") or None
    sha = raw.get("sha") or None
    measured = bool(raw.get("measured")) and bool(src) and bool(sha)
    value = raw.get("value")
    return {"value": value if value not in ("",) else None, "unit": raw.get("unit") or None,
            "source": src, "sha": sha, "measured": measured}


def claims(cfg: dict | None = None) -> dict[str, dict]:
    cfg = load_chart_toml() if cfg is None else cfg
    sec = (cfg or {}).get("claims") or {}
    out = {cid: normalize(cid, dict(raw)) for cid, raw in DEFAULTS.items()}
    for cid, raw in sec.items():
        if isinstance(raw, dict):
            out[cid] = normalize(cid, raw)
    return out


def upright_ok(claim: dict) -> bool:
    """check 10: a claim may print upright only with measured:true and a source + sha."""
    return bool(claim.get("measured")) and bool(claim.get("source")) and bool(claim.get("sha"))


# ---------------------------------------------------------------- scrape_interval, read from the file it cites

_UNITS = {"ms": 0.001, "s": 1, "m": 60, "h": 3600}


def duration_s(text: str) -> int | None:
    """Prometheus duration ('30s', '1m', '1m30s') → whole seconds; None when it is not one."""
    parts = re.findall(r"(\d+)(ms|s|m|h)", text or "")
    if not parts or "".join(n + u for n, u in parts) != (text or "").strip():
        return None
    return int(round(sum(int(n) * _UNITS[u] for n, u in parts)))


def job_interval(text: str, job: str) -> int | None:
    """The `scrape_interval` set inside `job_name: <job>` under scrape_configs, in seconds. Not the global:
    a job that sets none inherits it, and that is reported as None so a claim cannot quote the default
    as the job's own. Indentation-based, no YAML dependency (the build installs only requirements.txt)."""
    lines = (text or "").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)-\s*job_name:\s*['\"]?([^'\"#\s]+)['\"]?\s*(#.*)?$", line)
        if not m or m.group(2) != job:
            continue
        item_indent = len(m.group(1))
        for nxt in lines[i + 1:]:
            if not nxt.strip() or nxt.lstrip().startswith("#"):
                continue
            indent = len(nxt) - len(nxt.lstrip())
            if indent <= item_indent:          # the next job (or the end of scrape_configs)
                break
            k = re.match(r"^\s*scrape_interval:\s*['\"]?([0-9a-z]+)['\"]?\s*(#.*)?$", nxt)
            if k and indent == item_indent + 2:
                return duration_s(k.group(1))
        return None
    return None


def cited(claim: dict) -> tuple[str, str, str | None] | None:
    """('Scrapy', 'Scraping_project/monitoring/prometheus.yml', 'scrapy_app') from a claim's source, or None."""
    src = str(claim.get("source") or "")
    m = re.match(r"^([^:\s]+):([^\s(]+)", src)
    if not m:
        return None
    j = re.search(r"\bjob\s+([A-Za-z0-9_.-]+)", src)
    return m.group(1), m.group(2), (j.group(1) if j else None)


def verify_scrape_interval(claims_: dict, read) -> dict:
    """Re-read claims.scrape_interval from the file and job it cites, at its sha. `read(repo, sha, path)` returns
    the file's text or None (no clone this run). A disagreement, or a source that names no job, sets
    measured false and says why on stdout; an unreadable file leaves the claim as the toml states it."""
    c = claims_.get("scrape_interval")
    if not c or not c.get("measured"):
        return claims_
    where = cited(c)
    if where is None or where[2] is None:
        print("claims.scrape_interval: the source names no scrape job; not measured")
        return {**claims_, "scrape_interval": {**c, "measured": False}}
    repo, path, job = where
    text = read(repo, c["sha"], path)
    if text is None:
        return claims_
    found = job_interval(text, job)
    if found is None or c.get("value") is None or int(c["value"]) != found:
        print(f"claims.scrape_interval: {repo}:{path} job {job} at {c['sha'][:7]} reads {found}, toml says "
              f"{c.get('value')}; not measured")
        return {**claims_, "scrape_interval": {**c, "measured": False}}
    return claims_
