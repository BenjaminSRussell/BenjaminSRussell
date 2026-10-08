"""logsim — the ship's log, computed-consistent until Ben records a real session.

    simulate(profile, entries, hosts=1, start=None, context=None) -> list[Row]
    check_log(log) -> list[str]
    default_log(version, date, cores=8) -> dict          assets/log.json v2, source "computed"
    rows_to_dict(rows) -> list[dict]

Formula (T7 §6 / T9 B): rate = min(per-host rps × hosts, workers / latency), capped at 2 req/s per
host; position(t) = Σ rate·Δt with a linear ramp over `ramp_s` (log(t) = r·(t − ramp/2) after the
ramp); in_flight = ceil(rate × p95) (Little's law); the crawl completes when position reaches
`urls_total`. Numbers are NOT stored while measured:false; the sheet calls simulate() and sets
every numeral italic. With measured:true (source session|cc-index) the stored numbers are used
verbatim, upright, and check_log only verifies they are physically consistent.
"""
from __future__ import annotations

import datetime as dt
import math
import re
from typing import NamedTuple

MAX_ENTRIES = 10
MAX_RPS_PER_HOST = 2.0
KINDS = ("cmd", "out", "crawl", "health", "remark", "beat", "watch")
SOURCES = ("computed", "session", "cc-index")
BANNED = re.compile(r"example\.com", re.I)


class Row(NamedTuple):
    time: str            # "HHMM" resolved
    t: int | None        # seconds from crawl start (None when the row has no clock relation)
    kind: str
    text: str
    log: int | None      # URLs fetched (position)
    speed: float | None  # req/s
    wind: str | None
    in_flight: int | None


# ---------------------------------------------------------------- arithmetic

def rate_of(profile: dict, hosts: int = 1) -> float:
    r = float(profile.get("rate_rps", MAX_RPS_PER_HOST))
    permits = profile.get("permits")
    p95 = float(profile.get("p95_fetch_ms", 800)) / 1000.0
    if permits and p95 > 0:
        r = min(r, permits / p95)
    return min(r, MAX_RPS_PER_HOST * max(1, hosts))


def position(t: float, profile: dict, hosts: int = 1) -> float:
    """URLs fetched by t seconds after start: Σ rate·Δt with a linear ramp, capped at urls_total."""
    if t <= 0:
        return 0.0
    r = rate_of(profile, hosts)
    ramp = max(0.0, float(profile.get("ramp_s", 0)))
    if ramp and t < ramp:
        p = r * t * t / (2 * ramp)
    else:
        p = r * (t - ramp / 2)
    total = profile.get("urls_total")
    return min(p, float(total)) if total else p


def t_complete(profile: dict, hosts: int = 1) -> float | None:
    total = profile.get("urls_total")
    if not total:
        return None
    r = rate_of(profile, hosts)
    ramp = max(0.0, float(profile.get("ramp_s", 0)))
    return total / r + ramp / 2 if total >= r * ramp / 2 else math.sqrt(2 * ramp * total / r)


def in_flight(profile: dict, hosts: int = 1) -> int:
    return int(math.ceil(rate_of(profile, hosts) * float(profile.get("p95_fetch_ms", 800)) / 1000.0))


def wind(profile: dict) -> str:
    timeout = float(profile.get("timeout_ratio", 0))
    failed = float(profile.get("failed_ratio", 0))
    r429 = float(profile.get("r429_ratio", 0))
    if r429 >= 0.01:
        return "fresh · 429s"
    if max(timeout, failed, r429) >= 0.01:
        return "fresh"
    if timeout == 0 and r429 == 0 and failed == 0:
        return "calm"
    return "light"


def elapsed_label(seconds: float) -> str:
    s = int(round(seconds))
    h, m = s // 3600, (s % 3600) // 60
    return f"{h}h {m:02d}m" if h else f"{m}m {s % 60:02d}s"


def hhmm(start: str, t: float) -> str:
    base = int(start[:2]) * 3600 + int(start[2:]) * 60
    s = (base + int(round(t))) % 86400
    return f"{s // 3600:02d}{(s % 3600) // 60:02d}"


def resolve_times(entries: list[dict], profile: dict, start: str, hosts: int = 1) -> list[int | None]:
    """Seconds from `start` for each entry: 'HHMM' | 'complete' | '+Nm' | '+Ns'."""
    base = int(start[:2]) * 3600 + int(start[2:]) * 60
    done = t_complete(profile, hosts)
    out: list[int | None] = []
    prev: int | None = None
    for e in entries:
        tm = str(e.get("time", ""))
        if tm == "complete":
            t = int(math.ceil(done)) if done is not None else None
        elif tm.startswith("+") and tm.endswith("m"):
            t = (prev or 0) + int(tm[1:-1]) * 60
        elif tm.startswith("+") and tm.endswith("s"):
            t = (prev or 0) + int(tm[1:-1])
        elif re.fullmatch(r"\d{4}", tm):
            t = int(tm[:2]) * 3600 + int(tm[2:]) * 60 - base
        else:
            t = None
        out.append(t)
        if t is not None:
            prev = t
    return out


def fill(text: str, ctx: dict) -> str:
    def sub(m: re.Match) -> str:
        key = m.group(1)
        v = ctx.get(key)
        if v is None:
            return m.group(0)
        return f"{v:,}" if isinstance(v, int) and key in ("log", "urls_total", "permits", "fetched") else str(v)
    return re.sub(r"\{(\w+)\}", sub, text)


def health_text(profile: dict, log: int, inflight: int) -> str:
    return (f"fetched {log:,} · timeout {float(profile.get('timeout_ratio', 0)):.0%} · "
            f"failed {float(profile.get('failed_ratio', 0)):.1%} · p95 {int(profile.get('p95_fetch_ms', 0))} ms · "
            f"wal fsync {int(profile.get('wal_fsync_p95_ms', 0))} ms · {inflight} of {int(profile.get('permits', 0)):,} permits")


def simulate(profile: dict, entries: list[dict], hosts: int = 1, start: str | None = None,
             context: dict | None = None, measured: bool = False) -> list[Row]:
    """One Row per entry. Computed numbers unless `measured` (then stored `log`/`speed` are kept)."""
    if len(entries) > MAX_ENTRIES:
        raise ValueError(f"log has {len(entries)} entries; the sheet refuses more than {MAX_ENTRIES}")
    start = start or next((str(e["time"]) for e in entries if e.get("kind") == "crawl"), None) \
        or next((str(e["time"]) for e in entries if re.fullmatch(r"\d{4}", str(e.get("time", "")))), "0000")
    r = rate_of(profile, hosts)
    done = t_complete(profile, hosts)
    flight = in_flight(profile, hosts)
    w = wind(profile)
    times = resolve_times(entries, profile, start, hosts)
    rows: list[Row] = []
    for e, t in zip(entries, times):
        kind = e.get("kind", "out")
        log = speed = None
        rw = None
        if t is not None and t >= 0:
            log = int(round(position(t, profile, hosts)))
            if kind not in ("cmd", "crawl"):
                if done is None or t < done:
                    speed = r
                elif t == int(math.ceil(done)):
                    speed = 0.0
                rw = w if speed is not None else None
        if measured:
            log = e.get("log", log)
            speed = e.get("speed", speed)
            rw = e.get("wind", rw)
        ctx = {**(context or {}), "log": log, "elapsed": elapsed_label(done) if done else None,
               "in_flight": flight, "permits": profile.get("permits"), "shards": profile.get("shards"),
               "hosts": hosts, "urls_total": profile.get("urls_total"), "speed": speed}
        text = e.get("text") or ""
        if kind == "health" and not text:
            text = health_text(profile, log or 0, flight)
        text = fill(text, ctx)
        rows.append(Row(hhmm(start, t) if t is not None else str(e.get("time", "")), t, kind, text, log, speed, rw,
                        flight if (speed is not None and speed > 0) else None))
    return rows


def rows_to_dict(rows: list[Row]) -> list[dict]:
    return [r._asdict() for r in rows]


# ---------------------------------------------------------------- checks

def check_log(log: dict) -> list[str]:
    """Every violated rule as one line (T7 §6 check_log + §7 check 9 data half)."""
    errs: list[str] = []
    if log.get("schema") != 2:
        errs.append("schema must be 2")
    src = log.get("source")
    measured = bool(log.get("measured"))
    if src not in SOURCES:
        errs.append(f"source must be one of {SOURCES}, got {src!r}")
    if src == "computed" and measured:
        errs.append("source computed cannot be measured:true")
    if src in ("session", "cc-index") and not measured:
        errs.append(f"source {src} must be measured:true")
    machine = log.get("machine") or {}
    cores = machine.get("cores")
    if cores is not None and (not isinstance(cores, int) or cores < 1):
        errs.append("machine.cores must be a positive integer or null")
    profile = log.get("profile") or {}
    hosts = int(log.get("hosts") or 1)
    if hosts < 1:
        errs.append("hosts must be ≥ 1")
    if cores is not None and profile.get("shards") != cores:
        errs.append(f"profile.shards {profile.get('shards')} != machine.cores {cores} (decision 14)")
    entries = log.get("entries") or []
    if len(entries) > MAX_ENTRIES:
        errs.append(f"{len(entries)} entries > {MAX_ENTRIES}")
    for i, e in enumerate(entries):
        if e.get("kind") not in KINDS:
            errs.append(f"entries[{i}].kind {e.get('kind')!r} invalid")
        if BANNED.search(str(e.get("text", ""))):
            errs.append(f"entries[{i}] mentions example.com")
        if not measured and any(k in e for k in ("log", "speed", "position", "wind", "inflight")):
            errs.append(f"entries[{i}] stores numbers while measured:false")
    if BANNED.search(str(log.get("target", ""))):
        errs.append("target is example.com")
    r = float(profile.get("rate_rps", 0))
    if r > MAX_RPS_PER_HOST * hosts:
        errs.append(f"profile.rate_rps {r} > {MAX_RPS_PER_HOST}·hosts")
    permits = profile.get("permits")
    p95 = float(profile.get("p95_fetch_ms", 0)) / 1000
    if permits:
        allowed = min(int(permits), math.ceil(rate_of(profile, hosts) * p95) + 1)
        if in_flight(profile, hosts) > allowed:
            errs.append(f"in_flight {in_flight(profile, hosts)} > {allowed}")
    # physical consistency of whichever numbers the sheet will print
    try:
        rows = simulate(profile, entries, hosts, log.get("start"), measured=measured)
    except ValueError as exc:
        errs.append(str(exc))
        rows = []
    prev: Row | None = None
    for i, row in enumerate(rows):
        if row.speed is not None and row.speed > MAX_RPS_PER_HOST * hosts:
            errs.append(f"entries[{i}] speed {row.speed} > {MAX_RPS_PER_HOST}·hosts")
        if prev is not None and row.log is not None and prev.log is not None:
            if row.log < prev.log:
                errs.append(f"entries[{i}] position {row.log} < previous {prev.log}")
            if row.t is not None and prev.t is not None and row.t > prev.t:
                cap = (prev.speed if prev.speed is not None else MAX_RPS_PER_HOST * hosts) * (row.t - prev.t) * 1.02
                cap = max(cap, MAX_RPS_PER_HOST * hosts * (row.t - prev.t) * 1.02) if measured else cap
                if row.log - prev.log > cap + 1:
                    errs.append(f"entries[{i}] Δposition {row.log - prev.log} > rate·Δt·1.02 = {cap:.0f}")
        if measured and row.kind not in ("cmd", "crawl") and row.t is not None and row.t >= 0 and "log" not in entries[i]:
            errs.append(f"entries[{i}] measured:true but no stored log")
        if row.log is not None:
            prev = row
    return errs


# ---------------------------------------------------------------- the default (computed) log

def default_log(version: str, date: str, cores: int | None = 8, host: str | None = None,
                target: str = "http://127.0.0.1:8080") -> dict:
    """assets/log.json v2 (T9 schema + T7 source/machine). Numbers are computed, not stored."""
    shards = cores if cores else 8
    return {
        "schema": 2,
        "vessel": "rustmapper",
        "version": version,
        "target": target,
        "hosts": 1,
        "date": date,
        "measured": False,
        "source": "computed",
        "machine": {"cores": cores, "host": host},
        "profile": {"rate_rps": 2.0, "ramp_s": 10, "p95_fetch_ms": 812, "wal_fsync_p95_ms": 3, "urls_total": 12440,
                    "failed_ratio": 0.004, "timeout_ratio": 0.0, "r429_ratio": 0.0, "permits": 512, "shards": shards},
        "start": "1403",
        "entries": [
            {"time": "1402", "kind": "cmd", "text": "pip install rustmapper"},
            {"time": "1402", "kind": "out", "text": f"Successfully installed rustmapper-{version}"},
            {"time": "1403", "kind": "crawl", "text": f"rustmapper crawl --start-url {target} --workers 512"},
            {"time": "1403", "kind": "out",
             "text": "seeded · sitemap · {hosts} host · robots.txt read · delay 0.5 s · frontier {shards} shards · wal on"},
            {"time": "1405", "kind": "health"},
            {"time": "1430", "kind": "remark", "text": "remarks · nothing to report"},
            {"time": "1431", "kind": "beat", "text": "Nothing on fire."},
            {"time": "complete", "kind": "out", "text": "crawl complete · plateau · {log} urls · {elapsed}"},
            {"time": "+2m", "kind": "cmd", "text": "rustmapper export-sitemap --data-dir ./data --output sitemap.xml"},
            {"time": "+0m", "kind": "out", "text": "wrote sitemap.xml · {log} urls"},
        ],
        "signoff": {"text": "Log closed", "time": "+2m", "initials": "B.S.R."},
        "heartbeat": {"template": "{HHMM} UTC · watch kept by cron · {commits} commits · {repos} repositories"},
    }
