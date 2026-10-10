#!/usr/bin/env python3
"""The run check (round 6, SPEC §6): the image claims only what the tool does.

Installs the released rustmapper into a clean venv, runs every executable the wheel ships, crawls a local
site that has no robots.txt, sends one SIGINT, and checks the file the crawl writes and the sitemap it
exports. Those are the entrance steps (`gate: true`); `ok` is true only when every one of them passed.

Then it probes four behaviours a stranger meets in the first minute (`gate: false`; `ok` says whether the
behaviour happened, and a route entry in chart.toml names the probes it rests on with `runs` / `fails`):

    ends_by_itself      a crawl with no signal exits by itself within ENDS_SECONDS, with every page written
    kill_writes_file    a crawl sent SIGTERM (what `kill`, `timeout` and `docker stop` send) writes sitemap.jsonl
    export_after_kill   after that kill, export-sitemap still writes a sitemap.xml with every page
    resume_after_kill   after that kill, `resume` runs and writes every page
    quiet_after_last_page  (review round 4) in the ends_by_itself run, the crawl's `Received work item` lines name
                        as many URLs as sitemap.jsonl has lines after the SIGINT, and the last of them came at
                        least QUIET_SECONDS before it: a reader can tell the crawl is done from its own output
    robots_read         (review round 6) a crawl of a local http site whose robots.txt disallows /secret.html (and
                        sets Crawl-delay: 5) asks for /robots.txt and never for /secret.html; the server's own
                        request log decides, not the crawler's output
    workers_cap         (review round 8) `--workers 1` holds a crawl to one request at a time: the fixture site,
                        each answer held WORKERS_DELAY s, crawled twice; with the default workers the server sees two
                        requests open at once (the index's two links), with `--workers 1` never more than one
    second_ctrl_c       (review round 8) a second SIGINT SECOND_AFTER s after the first quits before the export:
                        exit 1 and no sitemap.jsonl (0.1.3's "Press Ctrl+C again to force quit")
    non200_status       (review round 9) a page that answers 429 (Retry-After: 2) and a link that answers 404 are
                        written with no status_code, the 429 page is asked for once in NON200_SECONDS, and the page
                        only it links to is never asked for: a refusal looks like any other missing page. Review
                        round 11: also a 500, a 200 that is JSON and a page held past --timeout STATUS_TIMEOUT, each
                        asked for once, with status_code and crawled_at null
    redirect_kept       (review round 12) a URL that answers 301 is written under the address asked for, with the
                        target's status and title, and the links on a page reached by a redirect are resolved against
                        the old address (/dir -> /dir/ links child.html, fetched as /child.html); in the same run,
                        sitemap_keeps_noindex: export-sitemap lists the redirecting URL and a noindex, canonicalized
                        page, in one file
    ua_seen             (review round 15) in the robots_read run, every request carried one User-Agent with no URL
                        or address in it, and no From header (the name the crawl gives a site, `ua`)
    robots_stall        (review round 15) over https on 127.0.0.1:443 (0.1.3 reads robots.txt only over https, and
                        drops the port from its URL): robots.txt disallows /secret, answered at once; the home page
                        links p1-p5, secret.html, p6-p10; the behaviour happened when p1-p5 were fetched and none of
                        p6-p10 in STALL_SECONDS. `skipped` when 443 cannot be bound or no request gets through
    robots_resume       (review round 15) the stall site, but p1.html (answered RESUME_HOLD s late) links a page no
                        other links: none of p6-p10 before that answer, all five after it (a new link puts the host
                        back on the queue)
    robots_late         (review round 15) the same over https, robots.txt answered LATE_HOLD s late, the home page
                        linking ten disallowed pages and ten allowed: the behaviour happened when one disallowed page
                        was fetched
    blank_rows          (review round 16) in the robots_stall run, every row whose page the server never saw has
                        status_code and crawled_at null, and `grep -c '"crawled_at":null'` counts exactly the rows
                        with crawled_at null (the README's count of blank rows); skipped with robots_stall
    sitemap_keeps_disallowed  (review round 16) export-sitemap on the robots_late run's data lists every disallowed
                        page that run fetched; skipped with robots_late
    quiet_slow_page     (review round 9) the quiet mark has a number: on a site whose second page is held SLOW_HOLD
                        s, two `Received work item` lines are at least SLOW_HOLD s apart (silence shorter than the
                        bound is not the end), and after QUIET_BOUND s with no such line, one SIGINT writes every page

Only the robots probe, against a binary already installed (it needs no install):

    python3 scripts/runcheck.py --probe robots_read --exe <venv>/bin/rust_sitemap --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe workers_cap,second_ctrl_c --exe … --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe non200_status,quiet_slow_page --exe … --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe redirect_kept --exe … --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe robots_read,robots_stall,robots_resume,robots_late --exe … --version 0.1.3 --out steps.json

Every step carries `secs`, its wall time from time.monotonic(). The install is timed cold INSTALL_RUNS times (each
in a fresh venv with an empty CARGO_HOME, so cargo downloads every crate inside the timed step); its `secs` is the
median, and the step records `cache: "cold"`, `rustc` (the toolchain's version, or "none"), `cpus` and `runs`. Standard library only. Writes runcheck.json:

    {date, runner, python, version, scripts, install, steps: [{id, cmd, ok, gate, secs, detail}], ok}

The weekly workflow runs it on macos-14 (Apple silicon, the only platform with a prebuilt wheel) and hands
the file to build_stats (`--runcheck`). Run it anywhere else and `runner`/`install` say so: on Linux pip
builds the release from its sdist, which needs Rust.

    python3 scripts/runcheck.py --version 0.1.3 --scripts rust_sitemap --out runcheck.json
    python3 scripts/runcheck.py --stats assets/stats.json --out runcheck.json
    python3 scripts/runcheck.py --latest --out runcheck.json       # what the weekly job runs
"""
from __future__ import annotations

import argparse
import datetime as dt
import http.server
import io
import json
import os
import platform
import re
import shutil
import signal
import socketserver
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "tests" / "fixtures" / "route-site"
ROBOTS_SITE = ROOT / "tests" / "fixtures" / "robots-site"   # robots.txt: Disallow /secret.html, Crawl-delay 5
ROBOTS_SECONDS = 15     # robots_read: one SIGINT after this long (two pages; Crawl-delay 5 would space them 5 s apart)
PAGES = ("index.html", "a.html", "b.html")
KEYS = ("url", "depth", "status_code", "title")
CRAWL_SECONDS = 45      # the entrance crawl: one SIGINT after this long (three pages take well under a second)
EXIT_SECONDS = 60       # how long a stopped crawl may take to exit
ENDS_SECONDS = 150      # ends_by_itself: how long a crawl with no signal is given to exit by itself
KILL_SECONDS = 5        # kill_writes_file: SIGTERM after this long
RESUME_SECONDS = 20     # resume_after_kill: one SIGINT after this long, if it is still running
QUIET_SECONDS = 100     # quiet_after_last_page: the last work-item line at least this long before the SIGINT
WORKERS_DELAY = 1.0     # workers_cap: each answer is held this long, so two requests in flight overlap on the server
WORKERS_SECONDS = 15    # workers_cap: one SIGINT after this long (three pages, one at a time, take about 3 s)
SECOND_AFTER = 0.3      # second_ctrl_c: the second SIGINT this long after the first (0.1.3 waits 2 s before saving)
STATUS_SITE = ROOT / "tests" / "fixtures" / "status-site"   # busy.html answers 429, gone.html is not there (404)
NON200_SECONDS = 12     # non200_status: one SIGINT after this long (Retry-After: 2 would allow five more asks)
STATUS_HOLD = 8.0       # non200_status: hang.html is held this long (review round 11) ...
STATUS_TIMEOUT = 3      # ... and the probe crawls with --timeout this, so the fetch times out
SLOW_SITE = ROOT / "tests" / "fixtures" / "slow-site"       # slow.html is held SLOW_HOLD s, then links after.html
SLOW_HOLD = 15.0        # quiet_slow_page: how long the server holds slow.html (under 0.1.3's 20 s --timeout)
QUIET_BOUND = 60        # quiet_slow_page: the quiet the image prints, chart.toml H1 {quiet} (data/route.py quiet_secs)
QUIET_LIMIT = 180       # quiet_slow_page: give up waiting for the quiet after this long
WORK_ITEM = re.compile(r"Received work item: (\S+)")   # the line 0.1.3 prints for every URL it starts (stderr)


def _step(steps: list, sid: str, cmd: str, ok: bool, detail: str = "", secs: float | None = None,
          gate: bool = True) -> bool:
    steps.append({"id": sid, "cmd": cmd, "ok": bool(ok), "gate": gate,
                  "secs": None if secs is None else round(secs, 1), "detail": detail[:400]})
    tag = ("ok   " if ok else "FAIL ") if gate else ("yes  " if ok else "no   ")
    print(tag + cmd + (f"  [{secs:.1f} s]" if secs is not None else "") + (f"  ({detail[:160]})" if detail else ""),
          flush=True)
    return ok


def _timed(argv: list[str], timeout: int = 900, cwd: Path | None = None) -> tuple[subprocess.CompletedProcess, float]:
    t0 = time.monotonic()
    p = _run(argv, timeout, cwd)
    return p, time.monotonic() - t0


def _run(argv: list[str], timeout: int = 900, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=cwd)


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # noqa: D401 - silence the access log
        pass


def serve(site: Path) -> tuple[socketserver.TCPServer, int]:
    """The fixture site on 127.0.0.1, any free port; no robots.txt, so /robots.txt answers 404."""
    handler = lambda *a, **k: _Quiet(*a, directory=str(site), **k)  # noqa: E731
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


class _Logged(_Quiet):
    """The fixture server that keeps every request path it served, in order (review round 6, robots_read), and
    (review round 15) the User-Agent and From headers each request carried (probe ua_seen)."""
    paths: list = []
    agents: list = []

    def log_request(self, code="-", size="-"):
        type(self).paths.append((time.monotonic(), self.path.split("?")[0]))
        type(self).agents.append((self.headers.get("User-Agent"), self.headers.get("From")))


def serve_logged(site: Path, agents: list | None = None) -> tuple[socketserver.TCPServer, int, list]:
    """As serve(), and returns the list the server appends (time, path) to for every request; `agents`, when given,
    gets (User-Agent, From) for each."""
    paths: list = []
    cls = type("_LoggedSite", (_Logged,), {"paths": paths, "agents": agents if agents is not None else []})
    handler = lambda *a, **k: cls(*a, directory=str(site), **k)  # noqa: E731
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1], paths


def robots_verdict(paths: list[tuple[float, str]]) -> tuple[bool, str]:
    """robots_read: /robots.txt was asked for and /secret.html never was. The detail counts the requests and gives
    the shortest spacing between two page fetches (a Crawl-delay of 5 would keep them 5 s apart)."""
    got = [p for _, p in paths]
    asked = "/robots.txt" in got
    secret = "/secret.html" in got
    pages = sorted(t for t, p in paths if p != "/robots.txt")
    gap = min((b - a for a, b in zip(pages, pages[1:])), default=None)
    spacing = f"; closest two fetches {gap * 1000:.0f} ms apart" if gap is not None else ""
    return asked and not secret, (f"{len(got)} requests; /robots.txt {'asked for' if asked else 'never asked for'}; "
                                  f"/secret.html (disallowed) {'fetched' if secret else 'not fetched'}{spacing}")


def ua_verdict(agents: list[tuple[str | None, str | None]]) -> tuple[bool, str, str | None]:
    """ua_seen (review round 15): every request carried one and the same User-Agent, with no URL or address in it
    and no From header, so a site owner reading the log has no way to reach whoever ran the crawl. Returns (ok,
    detail, the name)."""
    names = sorted({str(a) for a, _f in agents if a})
    froms = sorted({str(f) for _a, f in agents if f})
    if not agents:
        return False, "no request reached the server", None
    one = names[0] if len(names) == 1 else None
    blank = sum(1 for a, _f in agents if not a)
    ok = one is not None and not blank and not froms and not re.search(r"https?:|www\.|@", one)
    return ok, (f"{len(agents)} requests; User-Agent {', '.join(repr(n) for n in names) or 'none'}"
                + (f" ({blank} with none)" if blank else "") + "; From " + (", ".join(froms) if froms else "never sent")), one


def probe_robots(steps: list, exe: str, name: str, work: Path) -> None:
    """robots_read: crawl the robots fixture over plain http, one SIGINT after ROBOTS_SECONDS, read the server's log.
    Review round 15: the same run's headers give ua_seen, the name the crawl sends."""
    agents: list = []
    httpd, port, paths = serve_logged(ROBOTS_SITE, agents)
    try:
        d4 = work / "d4"
        proc, t0 = _crawl(exe, ["crawl", "--start-url", f"http://127.0.0.1:{port}/", "--seeding-strategy", "none",
                                "--data-dir", str(d4)], work, "robots.log")
        exited, _secs = _stop(proc, signal.SIGINT, ROBOTS_SECONDS)
        took = time.monotonic() - t0
    finally:
        httpd.shutdown()
    ok, detail = robots_verdict(paths)
    _step(steps, "robots_read", f"{name} crawl of an http site whose robots.txt disallows /secret.html reads it",
          ok, f"{detail}; {exited}", took, gate=False)
    ok, detail, ua = ua_verdict(agents)
    _step(steps, "ua_seen", f"{name} crawl names itself with one User-Agent, with no contact in it and no From header",
          ok, detail, gate=False)
    steps[-1]["ua"] = ua


class _Slow(_Quiet):
    """The fixture server that holds each answer WORKERS_DELAY s and keeps (start, end) of every page request
    (review round 8, workers_cap)."""
    spans: list = []

    def do_GET(self):  # noqa: N802 - http.server's name
        t0 = time.monotonic()
        time.sleep(WORKERS_DELAY)
        try:
            super().do_GET()
        finally:
            type(self).spans.append((t0, time.monotonic(), self.path.split("?")[0]))


def serve_slow(site: Path) -> tuple[socketserver.TCPServer, int, list]:
    spans: list = []
    cls = type("_SlowSite", (_Slow,), {"spans": spans})
    handler = lambda *a, **k: cls(*a, directory=str(site), **k)  # noqa: E731
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1], spans


def max_open(spans: list[tuple[float, float, str]]) -> int:
    """The most requests the server had open at one moment (an end and a start at the same instant do not overlap)."""
    events = sorted([(a, 1) for a, _b, _p in spans] + [(b, -1) for _a, b, _p in spans], key=lambda e: (e[0], e[1]))
    cur = best = 0
    for _t, d in events:
        cur += d
        best = max(best, cur)
    return best


def workers_verdict(default_spans: list, capped_spans: list) -> tuple[bool, str]:
    """workers_cap: with the default the server saw two requests open at once (so the site can show an overlap), and
    with `--workers 1` never more than one, over at least two pages."""
    d, c = max_open(default_spans), max_open(capped_spans)
    ok = d >= 2 and c == 1 and len(capped_spans) >= 2
    return ok, (f"default workers: {len(default_spans)} requests, at most {d} open at once; --workers 1: "
                f"{len(capped_spans)} requests, at most {c} open at once")


def probe_workers(steps: list, exe: str, name: str, work: Path) -> None:
    """workers_cap: the fixture site, slowed, crawled with the default workers and with `--workers 1`."""
    runs = {}
    for tag, extra in (("default", []), ("capped", ["--workers", "1"])):
        httpd, port, spans = serve_slow(SITE)
        try:
            d = work / f"dw-{tag}"
            proc, _t0 = _crawl(exe, ["crawl", "--start-url", f"http://127.0.0.1:{port}/", "--seeding-strategy", "none",
                                     *extra, "--data-dir", str(d)], work, f"workers-{tag}.log")
            exited, _secs = _stop(proc, signal.SIGINT, WORKERS_SECONDS)
        finally:
            httpd.shutdown()
        runs[tag] = (list(spans), exited)
    ok, detail = workers_verdict(runs["default"][0], runs["capped"][0])
    _step(steps, "workers_cap", f"{name} crawl --workers 1 keeps one request open at a time", ok,
          f"{detail}; {runs['capped'][1]}", gate=False)


def second_verdict(code: int | None, wrote: bool, saved_line: bool) -> tuple[bool, str]:
    """second_ctrl_c: the second SIGINT ended the run with exit 1 before the export, so no sitemap.jsonl."""
    ok = code == 1 and not wrote
    return ok, (f"exit {code}; sitemap.jsonl {'written' if wrote else 'not written'}; "
                f"`Saved to:` {'printed' if saved_line else 'not printed'}")


def probe_second(steps: list, exe: str, name: str, work: Path) -> None:
    """second_ctrl_c: crawl the fixture, SIGINT after WORKERS_SECONDS, a second one SECOND_AFTER s later."""
    httpd, port = serve(SITE)
    try:
        d = work / "d5"
        proc, _t0 = _crawl(exe, ["crawl", "--start-url", f"http://127.0.0.1:{port}/", "--seeding-strategy", "none",
                                 "--data-dir", str(d)], work, "second.log")
        code = None
        try:
            proc.wait(WORKERS_SECONDS)
            code = proc.returncode
        except subprocess.TimeoutExpired:
            proc.send_signal(signal.SIGINT)
            time.sleep(SECOND_AFTER)
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
            try:
                code = proc.wait(EXIT_SECONDS)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        proc._log.close()  # type: ignore[attr-defined]
    finally:
        httpd.shutdown()
    try:
        log = (work / "second.log").read_text(encoding="utf-8", errors="replace")
    except OSError:
        log = ""
    ok, detail = second_verdict(code, (d / "sitemap.jsonl").is_file(), "Saved to:" in log)
    _step(steps, "second_ctrl_c", f"{name} crawl: a second SIGINT {SECOND_AFTER} s after the first quits before "
          "writing sitemap.jsonl", ok, detail, gate=False)


class _Status(_Quiet):
    """The status fixture: busy.html answers 429 with Retry-After: 2 (and its body, which links beyond.html); review
    round 11: /err answers 500, /feed answers 200 as application/json, and hang.html is held STATUS_HOLD s (longer
    than the probe's --timeout). Every request path is kept, in order, as it arrives (before a held answer)."""
    paths: list = []

    def do_GET(self):  # noqa: N802 - http.server's name
        path = self.path.split("?")[0]
        type(self).paths.append((time.monotonic(), path))
        if path == "/hang.html":
            time.sleep(STATUS_HOLD)
        try:
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError):   # the crawler gave up on hang.html
            pass

    def _send(self, code: int, ctype: str, body: bytes, extra: dict | None = None) -> io.BytesIO:
        self.send_response(code)
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return io.BytesIO(body)

    def send_head(self):  # noqa: D401 - http.server's hook: the 429 is sent with the page's own body
        path = self.path.split("?")[0]
        if path == "/busy.html":
            body = (self.directory and Path(self.directory, "busy.html").read_bytes()) or b""
            return self._send(429, "text/html; charset=utf-8", body, {"Retry-After": "2"})
        if path == "/err":
            return self._send(500, "text/html; charset=utf-8", b"<!doctype html><title>err</title><p>500</p>")
        if path == "/feed":
            return self._send(200, "application/json", b'{"links": ["beyond.html"]}')
        return super().send_head()

    def log_request(self, code="-", size="-"):
        pass


def serve_status(site: Path) -> tuple[socketserver.TCPServer, int, list]:
    paths: list = []
    cls = type("_StatusSite", (_Status,), {"paths": paths})
    handler = lambda *a, **k: cls(*a, directory=str(site), **k)  # noqa: E731
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1], paths


def jsonl_records(path: Path) -> dict[str, dict]:
    """sitemap.jsonl as {page name: record} ("index.html" for the site's root)."""
    out: dict[str, dict] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return out
    for line in text.splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        url = str(rec.get("url", "")).split("?")[0]
        tail = url.split("://", 1)[-1].split("/", 1)
        out[(tail[1] if len(tail) > 1 else "") or "index.html"] = rec
    return out


NON200_PAGES = ("busy.html", "gone.html", "err", "feed", "hang.html")   # every answer but an HTML 200


def status_verdict(paths: list[tuple[float, str]], recs: dict[str, dict]) -> tuple[bool, str]:
    """non200_status: each page that does not answer an HTML 200 (busy.html 429, gone.html 404, err 500, feed a JSON
    200, hang.html past the --timeout) was asked for once, beyond.html (linked only from busy.html) never, and their
    rows are there with no status_code and no crawled_at: in the file they look like a page never fetched."""
    got = [p for _, p in paths]
    asked = {k: got.count("/" + k) for k in NON200_PAGES}
    beyond = got.count("/beyond.html")
    rows = {k: recs.get(k) for k in NON200_PAGES}
    blank = all(r is not None and r.get("status_code") is None and r.get("crawled_at") is None for r in rows.values())
    ok = all(n == 1 for n in asked.values()) and beyond == 0 and blank
    shown = "; ".join(f"{k}: " + ("no row" if r is None else f"status_code {json.dumps(r.get('status_code'))}, "
                                  f"crawled_at {json.dumps(r.get('crawled_at'))}") for k, r in rows.items())
    times = ", ".join(f"{k} {n}" for k, n in asked.items())
    return ok, (f"{len(got)} requests; asked for: {times} (429 with Retry-After: 2, 404, 500, JSON 200, held "
                f"{STATUS_HOLD:.0f} s with --timeout {STATUS_TIMEOUT}); /beyond.html "
                f"{'never asked for' if not beyond else f'asked for {beyond} time(s)'}; {shown}")


def probe_status(steps: list, exe: str, name: str, work: Path) -> None:
    """non200_status: crawl the status fixture, one SIGINT after NON200_SECONDS, read the server's log and the file."""
    httpd, port, paths = serve_status(STATUS_SITE)
    try:
        d = work / "d6"
        proc, t0 = _crawl(exe, ["crawl", "--start-url", f"http://127.0.0.1:{port}/", "--seeding-strategy", "none",
                                "--timeout", str(STATUS_TIMEOUT), "--data-dir", str(d)], work, "status.log")
        exited, _secs = _stop(proc, signal.SIGINT, NON200_SECONDS)
        took = time.monotonic() - t0
    finally:
        httpd.shutdown()
    ok, detail = status_verdict(list(paths), jsonl_records(d / "sitemap.jsonl"))
    _step(steps, "non200_status", f"{name} crawl: every answer but an HTML 200 (429, 404, 500, a JSON 200, a "
          "timeout) is written with no status_code and no crawled_at, asked for once, and its links are not followed", ok, f"{detail}; {exited}", took, gate=False)


class _Held(_Quiet):
    """The slow fixture: slow.html is held SLOW_HOLD s before it is sent (review round 9, quiet_slow_page)."""
    hold: float = SLOW_HOLD

    def do_GET(self):  # noqa: N802 - http.server's name
        if self.path.split("?")[0] == "/slow.html":
            time.sleep(type(self).hold)
        super().do_GET()


def serve_held(site: Path, hold: float = SLOW_HOLD) -> tuple[socketserver.TCPServer, int]:
    cls = type("_HeldSite", (_Held,), {"hold": hold})
    handler = lambda *a, **k: cls(*a, directory=str(site), **k)  # noqa: E731
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def slow_verdict(stamps: list[tuple[float, str]], t_sig: float | None, recs: dict[str, dict],
                 hold: float = SLOW_HOLD, quiet: float = QUIET_BOUND) -> tuple[bool, str]:
    """quiet_slow_page: some two consecutive work-item lines are at least `hold` s apart (less 0.5 s for the
    clock), the SIGINT came at least `quiet` s after the last one, and the file then has all three pages, status
    200."""
    if t_sig is None:
        return False, "the crawl exited by itself, or never went quiet; no SIGINT was sent after the quiet"
    ts = sorted(t for t, _ in stamps)
    gap = max((b - a for a, b in zip(ts, ts[1:])), default=0.0)
    after = t_sig - ts[-1] if ts else 0.0
    pages = ("index.html", "slow.html", "after.html")
    good = [p for p in pages if (recs.get(p) or {}).get("status_code") == 200]
    ok = gap >= hold - 0.5 and after >= quiet and len(good) == len(pages)
    return ok, (f"{len(ts)} work-item lines; longest gap between two {gap:.1f} s (slow.html held {hold:.0f} s); "
                f"SIGINT {after:.0f} s after the last; {len(good)} of {len(pages)} pages in sitemap.jsonl, status 200")


def probe_slow(steps: list, exe: str, name: str, work: Path) -> None:
    """quiet_slow_page: crawl the slow fixture; once no work-item line has come for QUIET_BOUND s, one SIGINT."""
    httpd, port = serve_held(SLOW_SITE)
    t_sig = None
    try:
        d = work / "d7"
        proc, t0, stamps = _crawl_stamped(exe, ["crawl", "--start-url", f"http://127.0.0.1:{port}/",
                                                "--seeding-strategy", "none", "--data-dir", str(d)], work, "slow.log")
        while time.monotonic() - t0 < QUIET_LIMIT and proc.poll() is None:
            time.sleep(0.5)
            now = time.monotonic()
            if stamps and now - t0 > SLOW_HOLD and now - max(t for t, _ in stamps) >= QUIET_BOUND:
                t_sig = now
                break
        exited, _secs = _stop(proc, signal.SIGINT, 0)
    finally:
        httpd.shutdown()
    ok, detail = slow_verdict(list(stamps), t_sig, jsonl_records(d / "sitemap.jsonl"))
    _step(steps, "quiet_slow_page", f"{name} crawl: a page held {SLOW_HOLD:.0f} s is not the end; after "
          f"{QUIET_BOUND} s with no Received work item line, one SIGINT writes every page", ok, f"{detail}; {exited}",
          gate=False)
    steps[-1]["quiet_secs"] = QUIET_BOUND


REDIRECT_SITE = ROOT / "tests" / "fixtures" / "redirect-site"   # /old answers 301 to /new.html; /dir 301 to /dir/
REDIRECT_SECONDS = 10    # redirect_kept: one SIGINT after this long (six pages, no held answer)


class _Redirect(_Logged):
    """The redirect fixture (review round 12): /old answers 301 to /new.html; /dir is a folder, so http.server
    answers 301 to /dir/ (Apache's DirectorySlash does the same); /dir/ links child.html; canon.html is noindex with
    a canonical link to /new.html. Every request path is kept, in order."""

    def send_head(self):  # noqa: D401 - http.server's hook
        if self.path.split("?")[0] == "/old":
            self.send_response(301)
            self.send_header("Location", "/new.html")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        return super().send_head()


def serve_redirect(site: Path) -> tuple[socketserver.TCPServer, int, list]:
    paths: list = []
    cls = type("_RedirectSite", (_Redirect,), {"paths": paths})
    handler = lambda *a, **k: cls(*a, directory=str(site), **k)  # noqa: E731
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1], paths


def sitemap_locs(path: Path) -> list[str]:
    """The <loc> values of a sitemap.xml, as page names ("index.html" for the root), in order."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out = []
    for loc in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text):
        tail = loc.split("://", 1)[-1].split("/", 1)
        out.append((tail[1] if len(tail) > 1 else "") or "index.html")
    return out


def redirect_verdict(paths: list[tuple[float, str]], recs: dict[str, dict]) -> tuple[bool, str]:
    """redirect_kept: a URL that redirects is written under the address it asked for, with the target's status and
    title (/old: status_code 200, title "New"), and links on a page reached by a redirect are read against the old
    address (/dir -> /dir/ links child.html: /child.html is asked for, /dir/child.html never is)."""
    got = [p for _, p in paths]
    old = recs.get("old") or {}
    kept = old.get("status_code") == 200 and old.get("title") == "New"
    wrong, right = got.count("/child.html"), got.count("/dir/child.html")
    ok = kept and wrong >= 1 and right == 0
    return ok, (f"{len(got)} requests; /old (301 to /new.html) written as url /old, status_code "
                f"{json.dumps(old.get('status_code'))}, title {json.dumps(old.get('title'))}; /dir (301 to /dir/) "
                f"links child.html: /child.html asked for {wrong} time(s), /dir/child.html {right}")


def keeps_verdict(locs: list[str]) -> tuple[bool, str]:
    """sitemap_keeps_noindex: export-sitemap lists the redirecting /old and canon.html (noindex, canonical to
    /new.html) beside the pages they point to, all in one file."""
    ok = "old" in locs and "canon.html" in locs and "new.html" in locs
    return ok, f"{len(locs)} <loc> in one file: " + ", ".join(locs)


def probe_redirect(steps: list, exe: str, name: str, work: Path) -> None:
    """redirect_kept and sitemap_keeps_noindex (review round 12): crawl the redirect fixture, one SIGINT after
    REDIRECT_SECONDS, read the server's log and the file, then export-sitemap."""
    httpd, port, paths = serve_redirect(REDIRECT_SITE)
    try:
        d = work / "d8"
        proc, t0 = _crawl(exe, ["crawl", "--start-url", f"http://127.0.0.1:{port}/", "--seeding-strategy", "none",
                                "--timeout", str(STATUS_TIMEOUT), "--data-dir", str(d)], work, "redirect.log")
        exited, _secs = _stop(proc, signal.SIGINT, REDIRECT_SECONDS)
        took = time.monotonic() - t0
    finally:
        httpd.shutdown()
    ok, detail = redirect_verdict(list(paths), jsonl_records(d / "sitemap.jsonl"))
    _step(steps, "redirect_kept", f"{name} crawl: after a redirect it keeps the old address, with the target's status "
          "and title, and reads the page's links against the old address", ok, f"{detail}; {exited}", took, gate=False)
    xml = work / "r.xml"
    e, secs = _timed([exe, "export-sitemap", "--data-dir", str(d), "--output", str(xml)], 120, cwd=work)
    ok, detail = keeps_verdict(sitemap_locs(xml) if e.returncode == 0 else [])
    _step(steps, "sitemap_keeps_noindex", f"{name} export-sitemap: one file lists every status_code 200 row, a "
          "redirecting URL and a noindex, canonicalized page included", ok, detail, secs, gate=False)


# ---------------------------------------------------------------- review round 15: robots.txt over https
# 0.1.3 reads robots.txt only over https, and builds its URL without the port (robots.rs fetch_robots_txt,
# `format!("https://{}/robots.txt", host)`), so these probes serve the fixture over TLS on 127.0.0.1:443 with a
# certificate made for the run, and crawl https://localhost/. The crawler trusts it through SSL_CERT_FILE (reqwest's
# default TLS is OpenSSL on Linux); on macOS, in CI, through the System keychain (`sudo -n security
# add-trusted-cert`). A probe that cannot bind 443, make the certificate or get one request through is `skipped`:
# it neither passed nor failed, and nothing worded on it is drawn as measured.
HTTPS_PORT = 443
STALL_SITE = ROOT / "tests" / "fixtures" / "robots-stall-site"   # p1-p5, secret.html (disallowed), p6-p10
LATE_SITE = ROOT / "tests" / "fixtures" / "robots-late-site"     # secret1-10 (disallowed), then p1-p10
RESUME_SITE = ROOT / "tests" / "fixtures" / "robots-resume-site"  # the stall site, but p1.html links new.html
RESUME_HOLD = 3.0       # robots_resume: p1.html (the one page with a new link) is answered this late
STALL_SECONDS = 30      # robots_stall: one SIGINT after this long (eleven pages take well under a second)
STALL_HOLD = 1.0        # robots_stall: the home page is held this long, so robots.txt (answered at once) is in first
LATE_HOLD = 0.5         # robots_late: robots.txt is answered this late
LATE_SECONDS = 15       # robots_late: one SIGINT after this long
STALL_BEFORE = tuple(f"/p{i}.html" for i in range(1, 6))
STALL_AFTER = tuple(f"/p{i}.html" for i in range(6, 11))
LATE_SECRET = tuple(f"/secret{i}.html" for i in range(1, 11))
TLS_CONF = """[req]
distinguished_name = dn
prompt = no
x509_extensions = v3
[dn]
CN = localhost
[v3]
subjectAltName = DNS:localhost,IP:127.0.0.1
basicConstraints = critical,CA:TRUE
extendedKeyUsage = serverAuth
"""


def make_cert(work: Path) -> tuple[Path | None, Path | None, str]:
    """A throwaway self-signed certificate for localhost, valid two days: (cert, key, "") or (None, None, why)."""
    work = work.resolve()      # the crawler runs in `work`: a relative SSL_CERT_FILE would point nowhere
    conf, cert, key = work / "tls.cnf", work / "tls-cert.pem", work / "tls-key.pem"
    conf.write_text(TLS_CONF)
    try:
        p = _run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(key), "-out", str(cert),
                  "-days", "2", "-config", str(conf)], 120)
    except (OSError, subprocess.SubprocessError) as e:
        return None, None, f"no openssl: {e}"
    if p.returncode != 0 or not cert.is_file():
        return None, None, f"openssl req failed: {(p.stderr or p.stdout).strip()[-160:]}"
    return cert, key, ""


def trust_cert(cert: Path) -> str:
    """macOS in CI only: trust the run's certificate in the System keychain (reqwest uses the Security framework
    there, which ignores SSL_CERT_FILE). Returns what was done, for the step's detail."""
    if platform.system() != "Darwin" or not os.environ.get("CI"):
        return ""
    p = _run(["sudo", "-n", "security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k",
              "/Library/Keychains/System.keychain", str(cert)], 120)
    return "trusted in the System keychain" if p.returncode == 0 else "could not be trusted in the keychain"


def untrust_cert(cert: Path) -> None:
    if platform.system() == "Darwin" and os.environ.get("CI"):
        _run(["sudo", "-n", "security", "remove-trusted-cert", "-d", str(cert)], 120)


class _Tls(_Quiet):
    """The https fixture: every request path is kept as it arrives (before any hold), with its User-Agent; a path
    in `hold` is answered that many seconds late."""
    paths: list = []
    hold: dict = {}

    def do_GET(self):  # noqa: N802 - http.server's name
        path = self.path.split("?")[0]
        type(self).paths.append((time.monotonic(), path))
        if type(self).hold.get(path):
            time.sleep(type(self).hold[path])
        try:
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError, ssl.SSLError):
            pass

    def log_request(self, code="-", size="-"):
        pass


class _TlsServer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def serve_https(site: Path, cert: Path, key: Path, hold: dict | None = None,
                port: int = HTTPS_PORT) -> tuple[socketserver.TCPServer | None, list, str]:
    """The fixture over TLS on 127.0.0.1:`port`: (server, paths, "") or (None, [], why it could not bind)."""
    paths: list = []
    cls = type("_TlsSite", (_Tls,), {"paths": paths, "hold": dict(hold or {})})
    handler = lambda *a, **k: cls(*a, directory=str(site), **k)  # noqa: E731
    try:
        httpd = _TlsServer(("127.0.0.1", port), handler)
    except OSError as e:
        return None, [], f"port {port} could not be bound ({e.strerror or e})"
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(cert), str(key))
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, paths, ""


def tls_env(cert: Path) -> dict:
    """The crawler's environment over https: the run's certificate trusted, and no proxy for localhost."""
    keep = ",".join(x for x in (os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or "", "localhost",
                                "127.0.0.1") if x)
    return dict(os.environ, SSL_CERT_FILE=str(cert), NO_PROXY=keep, no_proxy=keep)


def _skip(steps: list, sid: str, cmd: str, why: str) -> None:
    """A probe that could not run: not ok, and marked `skipped`, so no route entry reads it as a pass or a fail."""
    _step(steps, sid, cmd, False, f"skipped: {why}", gate=False)
    steps[-1]["skipped"] = True
    print(f"runcheck: warning: {sid} skipped: {why}", file=sys.stderr, flush=True)


def stall_verdict(paths: list[tuple[float, str]]) -> tuple[bool, bool, str]:
    """robots_stall: (fault present, skipped, detail). The fault: robots.txt was read before the home page's links
    were queued, the disallowed link was not fetched, the five links before it were, and none of the five after it
    ever was. No request, no robots.txt, or the disallowed page fetched (the rules were not in yet): skipped, since the
    run says nothing about the stall."""
    got = [p for _, p in paths]
    if "/" not in got:
        return False, True, "no request reached the server over https (the certificate was not trusted?)"
    if "/robots.txt" not in got:
        return False, True, f"{len(got)} requests and no GET /robots.txt"
    if "/secret.html" in got:
        return False, True, f"{len(got)} requests; /secret.html was fetched, so robots.txt was not in time"
    before = sum(1 for p in STALL_BEFORE if p in got)
    after = sum(1 for p in STALL_AFTER if p in got)
    ok = before == len(STALL_BEFORE) and after == 0
    return ok, False, (f"{len(got)} requests; robots.txt asked for; the 5 links before the disallowed one: {before} "
                       f"fetched; /secret.html not fetched; the 5 after it: {after} fetched")


def resume_verdict(paths: list[tuple[float, str]], hold: float = RESUME_HOLD) -> tuple[bool, bool, str]:
    """robots_resume: (behaviour seen, skipped, detail). On the resume fixture the stalled host goes on once a page
    brings a link it has not seen: none of p6-p10 was asked for before p1.html (held `hold` s, the one page with a new
    link) was answered, and all five were after it. Skipped as robots_stall is."""
    got = [p for _, p in paths]
    if "/" not in got:
        return False, True, "no request reached the server over https (the certificate was not trusted?)"
    if "/robots.txt" not in got:
        return False, True, f"{len(got)} requests and no GET /robots.txt"
    if "/secret.html" in got:
        return False, True, f"{len(got)} requests; /secret.html was fetched, so robots.txt was not in time"
    t1 = next((t for t, p in paths if p == "/p1.html"), None)
    if t1 is None:
        return False, True, f"{len(got)} requests; /p1.html never asked for"
    early = [p for t, p in paths if p in STALL_AFTER and t < t1 + hold - 0.05]
    late = {p for t, p in paths if p in STALL_AFTER and t >= t1 + hold - 0.05}
    ok = not early and len(late) == len(STALL_AFTER) and "/new.html" in got
    return ok, False, (f"{len(got)} requests; before p1.html's answer ({hold:.0f} s late, the one new link): "
                       f"{len(early)} of the 5 links after the disallowed one fetched; after it: {len(late)}, and "
                       f"/new.html {'fetched' if '/new.html' in got else 'not fetched'}")


def late_verdict(paths: list[tuple[float, str]]) -> tuple[bool, bool, str]:
    """robots_late: (fault present, skipped, detail). The fault: with robots.txt answered LATE_HOLD s late, a page it
    disallows was fetched."""
    got = [p for _, p in paths]
    if "/" not in got:
        return False, True, "no request reached the server over https (the certificate was not trusted?)"
    secret = sum(1 for p in LATE_SECRET if p in got)
    allowed = sum(1 for p in got if re.fullmatch(r"/p\d+\.html", p))
    if not secret and "/robots.txt" not in got:
        return False, True, f"{len(got)} requests and no GET /robots.txt"
    return secret > 0, False, (f"{len(got)} requests; robots.txt answered {LATE_HOLD} s late; {secret} of "
                               f"{len(LATE_SECRET)} disallowed pages fetched, {allowed} allowed")


def _probe_https(steps: list, exe: str, name: str, work: Path, sid: str, cmd: str, site: Path, hold: dict,
                 secs: float, verdict) -> tuple[list, Path] | None:
    """Crawl `site` over https and record step `sid`: (the server's request log, the data dir), or None when the
    probe was skipped (review round 16: the stall and late runs read their files again, for blank_rows and
    sitemap_keeps_disallowed)."""
    cert, key, why = make_cert(work)
    if cert is None:
        _skip(steps, sid, cmd, why)
        return None
    trusted = trust_cert(cert)
    httpd, paths, why = serve_https(site, cert, key, hold)
    if httpd is None:
        untrust_cert(cert)
        _skip(steps, sid, cmd, why)
        return None
    try:
        d = work / f"d-{sid}"
        log = open(work / f"{sid}.log", "w")
        t0 = time.monotonic()
        proc = subprocess.Popen([exe, "crawl", "--start-url", "https://localhost/", "--seeding-strategy", "none",
                                 "--data-dir", str(d)], stdout=log, stderr=subprocess.STDOUT, cwd=work, env=tls_env(cert))
        proc._log = log  # type: ignore[attr-defined]
        exited, _s = _stop(proc, signal.SIGINT, secs)
        took = time.monotonic() - t0
    finally:
        httpd.shutdown()
        httpd.server_close()
        untrust_cert(cert)
    ok, skipped, detail = verdict(list(paths))
    detail = detail + (f"; certificate {trusted}" if trusted else "") + f"; {exited}"
    if skipped:
        _skip(steps, sid, cmd, detail)
        return None
    _step(steps, sid, cmd, ok, detail, took, gate=False)
    return list(paths), d


BLANK_LITERAL = '"crawled_at":null'     # what one blank row holds in 0.1.3's compact serde_json line


def blank_verdict(paths: list[tuple[float, str]], path: Path) -> tuple[bool, bool, str]:
    """blank_rows (review round 16): (holds, skipped, detail). Every row of sitemap.jsonl whose page the server never
    saw has `crawled_at` null, and `grep -c '"crawled_at":null'` (the README's count of blank rows) counts exactly the
    rows whose `crawled_at` is null. Skipped when the file is missing or every page was reached (nothing to show)."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False, True, "no sitemap.jsonl"
    recs = jsonl_records(path)
    asked = {p for _, p in paths}
    never = sorted(k for k in recs if ("/" if k == "index.html" else "/" + k) not in asked)
    if not never:
        return False, True, f"{len(recs)} rows, every page asked for"
    blank_never = [k for k in never if recs[k].get("crawled_at") is None and recs[k].get("status_code") is None]
    nulls = sum(1 for r in recs.values() if r.get("crawled_at") is None)
    grep = sum(1 for ln in raw.splitlines() if BLANK_LITERAL in ln)
    ok = len(blank_never) == len(never) and grep == nulls
    return ok, False, (f"{len(recs)} rows; {len(never)} never asked for ({', '.join(never)}), {len(blank_never)} of "
                       f"them with status_code and crawled_at null; {nulls} rows with crawled_at null, and grep -c "
                       f"'{BLANK_LITERAL}' counts {grep}")


def probe_stall(steps: list, exe: str, name: str, work: Path) -> None:
    """robots_stall: crawl the stall fixture over https (robots.txt answered at once, the home page held STALL_HOLD
    s), one SIGINT after STALL_SECONDS, read the server's log."""
    got = _probe_https(steps, exe, name, work, "robots_stall", f"{name} crawl of an https site: after a link "
                       "robots.txt disallows, the links queued behind it are not asked for", STALL_SITE,
                       {"/": STALL_HOLD}, STALL_SECONDS, stall_verdict)
    cmd = (f"{name} crawl: every page never asked for is a row with status_code and crawled_at null, and grep -c "
           f"'{BLANK_LITERAL}' counts the blank rows")
    if got is None:
        return _skip(steps, "blank_rows", cmd, "robots_stall was skipped")
    ok, skipped, detail = blank_verdict(got[0], got[1] / "sitemap.jsonl")
    if skipped:
        return _skip(steps, "blank_rows", cmd, detail)
    _step(steps, "blank_rows", cmd, ok, detail, gate=False)


def probe_resume(steps: list, exe: str, name: str, work: Path) -> None:
    """robots_resume: the stall fixture with one new link, on p1.html, answered RESUME_HOLD s late."""
    _probe_https(steps, exe, name, work, "robots_resume", f"{name} crawl of an https site: the host stalled by a "
                 "disallowed link goes on when a page brings a new link", RESUME_SITE,
                 {"/": STALL_HOLD, "/p1.html": RESUME_HOLD}, STALL_SECONDS, resume_verdict)


def probe_late(steps: list, exe: str, name: str, work: Path) -> None:
    """robots_late: crawl the late fixture over https (robots.txt answered LATE_HOLD s late), one SIGINT after
    LATE_SECONDS, read the server's log."""
    got = _probe_https(steps, exe, name, work, "robots_late", f"{name} crawl of an https site whose robots.txt comes "
                       f"{LATE_HOLD} s late fetches pages it disallows", LATE_SITE, {"/robots.txt": LATE_HOLD},
                       LATE_SECONDS, late_verdict)
    cmd = f"{name} export-sitemap: the pages robots.txt disallows that the crawl fetched are in sitemap.xml"
    if got is None:
        return _skip(steps, "sitemap_keeps_disallowed", cmd, "robots_late was skipped")
    paths, d = got
    fetched = [p for p in LATE_SECRET if p in {q for _, q in paths}]
    if not fetched:
        return _skip(steps, "sitemap_keeps_disallowed", cmd, "no disallowed page was fetched, so none could be listed")
    xml = work / "late.xml"
    e, secs = _timed([exe, "export-sitemap", "--data-dir", str(d), "--output", str(xml)], 120, cwd=work)
    ok, detail = disallowed_verdict(sitemap_locs(xml) if e.returncode == 0 else [], fetched)
    _step(steps, "sitemap_keeps_disallowed", cmd, ok, detail, secs, gate=False)


def disallowed_verdict(locs: list[str], fetched: list[str]) -> tuple[bool, str]:
    """sitemap_keeps_disallowed (review round 16): every disallowed page the crawl fetched (with its 200) is a <loc>
    of the exported sitemap.xml: 0.1.3's export keeps every status_code 200 row and reads no robots rules."""
    listed = [p for p in fetched if p.lstrip("/") in locs]
    ok = bool(fetched) and len(listed) == len(fetched)
    return ok, (f"{len(locs)} <loc> in one file; {len(listed)} of the {len(fetched)} disallowed pages fetched are "
                f"listed ({', '.join(p.lstrip('/') for p in listed[:3])}{', …' if len(listed) > 3 else ''})")


PROBES = {"robots_read": probe_robots, "workers_cap": probe_workers, "second_ctrl_c": probe_second,
          "non200_status": probe_status, "quiet_slow_page": probe_slow, "redirect_kept": probe_redirect,
          "robots_stall": probe_stall, "robots_resume": probe_resume, "robots_late": probe_late}


def check_jsonl(path: Path, port: int) -> tuple[bool, str]:
    """A line for each of the three pages, status 200, with the four keys the image prints."""
    if not path.is_file():
        return False, f"{path.name} was not written"
    seen: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        url = str(rec.get("url", ""))
        seen[url.rstrip("/").rsplit("/", 1)[-1] or "index.html"] = rec
    base = f"127.0.0.1:{port}"
    missing = []
    for page in PAGES:
        rec = seen.get(page) or (seen.get(base) if page == "index.html" else None)
        if rec is None:
            missing.append(f"{page}: no line")
            continue
        keys = [k for k in KEYS if k not in rec]
        if keys:
            missing.append(f"{page}: no {', '.join(keys)}")
        elif rec.get("status_code") != 200:
            missing.append(f"{page}: status {rec.get('status_code')}")
    if missing:
        return False, "; ".join(missing)
    return True, f"{len(seen)} lines; keys {', '.join(KEYS)} present; status 200"


def _crawl(exe: str, args: list[str], work: Path, logname: str) -> tuple[subprocess.Popen, float]:
    log = open(work / logname, "w")
    proc = subprocess.Popen([exe, *args], stdout=log, stderr=subprocess.STDOUT, cwd=work)
    proc._log = log  # type: ignore[attr-defined]
    return proc, time.monotonic()


def _crawl_stamped(exe: str, args: list[str], work: Path, logname: str) -> tuple[subprocess.Popen, float, list]:
    """As _crawl, with the output read through a pipe: each line goes to the log as it comes, and every
    `Received work item` line is stamped with time.monotonic() (review round 4: when the crawl goes quiet)."""
    log = open(work / logname, "w")
    proc = subprocess.Popen([exe, *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=work, text=True,
                            errors="replace", bufsize=1)
    stamps: list[tuple[float, str]] = []

    def pump():
        for line in proc.stdout:  # type: ignore[union-attr]
            log.write(line)
            log.flush()
            m = WORK_ITEM.search(line)
            if m:
                stamps.append((time.monotonic(), m.group(1)))

    th = threading.Thread(target=pump, daemon=True)
    th.start()

    class _Log:
        def close(self):
            th.join(10)
            log.close()
    proc._log = _Log()  # type: ignore[attr-defined]
    return proc, time.monotonic(), stamps


def jsonl_lines(path: Path) -> int:
    try:
        return sum(1 for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip())
    except OSError:
        return 0


def quiet_verdict(stamps: list[tuple[float, str]], t_sig: float | None, lines: int,
                  quiet: float = QUIET_SECONDS) -> tuple[bool, str]:
    """quiet_after_last_page: the distinct URLs on the work-item lines equal the file's lines after the SIGINT, and
    the last work-item line came at least `quiet` seconds before the SIGINT. No SIGINT (the crawl ended by itself):
    the probe does not apply and fails, so a hazard worded on it is not drawn."""
    if t_sig is None:
        return False, "the crawl exited by itself; no SIGINT was sent"
    if not stamps:
        return False, "no Received work item line"
    urls = {u.rstrip("/") for _, u in stamps}
    gap = t_sig - max(t for t, _ in stamps)
    ok = len(urls) == lines and gap >= quiet
    return ok, (f"{len(stamps)} work-item lines for {len(urls)} URLs, the last {gap:.0f} s before the SIGINT; "
                f"{lines} lines in sitemap.jsonl after it")


def probe_ends(steps: list, exe: str, name: str, url: str, port: int, work: Path) -> None:
    """ends_by_itself, then quiet_after_last_page from the same run's output."""
    d2 = work / "d2"
    proc, t0, stamps = _crawl_stamped(exe, ["crawl", "--start-url", url, "--seeding-strategy", "none", "--data-dir",
                                            str(d2)], work, "ends.log")
    t_sig = None
    try:
        proc.wait(ENDS_SECONDS)
        took = time.monotonic() - t0
        proc._log.close()  # type: ignore[attr-defined]
        good, detail = check_jsonl(d2 / "sitemap.jsonl", port)
        _step(steps, "ends_by_itself", f"{name} crawl with no signal exits by itself within {ENDS_SECONDS} s",
              proc.returncode == 0 and good, f"exit {proc.returncode} after {took:.1f} s; {detail}", took, gate=False)
    except subprocess.TimeoutExpired:
        t_sig = time.monotonic()
        _stop(proc, signal.SIGINT, 0)
        _step(steps, "ends_by_itself", f"{name} crawl with no signal exits by itself within {ENDS_SECONDS} s",
              False, f"still running at {ENDS_SECONDS} s; stopped with one SIGINT", ENDS_SECONDS, gate=False)
    ok, detail = quiet_verdict(stamps, t_sig, jsonl_lines(d2 / "sitemap.jsonl"))
    _step(steps, "quiet_after_last_page", f"{name} crawl: its Received work item lines stop once the pages run out",
          ok, detail, gate=False)


def _stop(proc: subprocess.Popen, sig: int, after: float) -> tuple[str, float | None]:
    """Wait `after` seconds, send `sig` if it is still running, wait for the exit. Returns (what happened,
    seconds from the signal to the exit; None when it had exited before the signal)."""
    name = {signal.SIGINT: "SIGINT", signal.SIGTERM: "SIGTERM"}.get(sig, str(sig))
    try:
        proc.wait(after)
        what, secs = f"exited by itself (exit {proc.returncode}) before the {name}", None
    except subprocess.TimeoutExpired:
        t0 = time.monotonic()
        proc.send_signal(sig)
        try:
            proc.wait(EXIT_SECONDS)
            secs = time.monotonic() - t0
            what = f"exit {proc.returncode} {secs:.1f} s after one {name}"
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            what, secs = f"still running {EXIT_SECONDS} s after one {name}; killed", None
    proc._log.close()  # type: ignore[attr-defined]
    return what, secs


def _tail(path: Path) -> str:
    try:
        lines = [x for x in path.read_text(encoding="utf-8", errors="replace").splitlines() if x.strip()]
    except OSError:
        return ""
    return lines[-1][:200] if lines else ""


def _export(steps: list, sid: str, exe: str, name: str, data: Path, work: Path, out: str, gate: bool) -> bool:
    xml = work / out
    e, secs = _timed([exe, "export-sitemap", "--data-dir", str(data), "--output", str(xml)], 120, cwd=work)
    locs = xml.read_text(encoding="utf-8", errors="replace").count("<loc>") if xml.is_file() else 0
    detail = f"{locs} <loc>" + ("" if e.returncode == 0 else f"; exit {e.returncode}: {(e.stderr or e.stdout).strip()[-160:]}")
    what = f"{name} export-sitemap --data-dir {data.name} --output {out}"
    return _step(steps, sid, what, e.returncode == 0 and locs == len(PAGES), detail, secs, gate=gate)


INSTALL_RUNS = 3         # the install is timed this many times, each in a fresh venv with an empty CARGO_HOME


def rustc_version(env: dict | None = None) -> str:
    """`rustc 1.97.0 (2d8144b78 2026-07-07)` -> "1.97.0"; "none" when there is no rustc on PATH."""
    try:
        p = subprocess.run(["rustc", "--version"], capture_output=True, text=True, timeout=60, env=env)
    except (OSError, subprocess.SubprocessError):
        return "none"
    m = re.match(r"rustc (\S+)", p.stdout.strip())
    return m.group(1) if p.returncode == 0 and m else "none"


def median(xs: list[float]) -> float:
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def install_detail(how: str, rustc: str, cpus: int | None, secs: list[float], tail: str) -> str:
    """The install step's detail: what was built, the cache state, the toolchain, the machine and the spread."""
    spread = (f"{len(secs)} runs: median {median(secs):.1f} s, range {min(secs):.1f}-{max(secs):.1f} s"
              if len(secs) > 1 else f"1 run: {secs[0]:.1f} s") if secs else "no run"
    return f"{how}; cache cold (empty CARGO_HOME); rustc {rustc}; {cpus or '?'} CPUs; {spread}; {tail}"


def run(version: str, scripts: list[str], work: Path, python: str, install_runs: int = INSTALL_RUNS) -> dict:
    steps: list[dict] = []
    venv = work / "v"
    bindir = venv / ("Scripts" if os.name == "nt" else "bin")
    install = ""
    p, secs = _timed([python, "-m", "venv", str(venv)])
    ok = _step(steps, "venv", f"{Path(python).name} -m venv v", p.returncode == 0, secs=secs)
    if ok:
        # Cold, every time (round 6, review 2): an empty CARGO_HOME, so the crates are downloaded inside the timed
        # step; --no-cache-dir, so a wheel pip built from the sdist last time cannot pass as a prebuilt one. The
        # first runs go to throwaway venvs; the last one, in v, is the one the probes use.
        times: list[float] = []
        out = ""
        rustc = rustc_version()
        for i in range(max(1, install_runs)):
            target = venv if i == install_runs - 1 else work / f"v{i}"
            if target != venv:
                _run([python, "-m", "venv", str(target)])
            cargo_home = Path(tempfile.mkdtemp(prefix="cargo-home-"))
            env = dict(os.environ, CARGO_HOME=str(cargo_home))
            t0 = time.monotonic()
            p = subprocess.run([str(target / bindir.name / "pip"), "install", "--disable-pip-version-check",
                                "--no-cache-dir", f"rustmapper=={version}"], capture_output=True, text=True,
                               timeout=1800, env=env)
            took = time.monotonic() - t0
            shutil.rmtree(cargo_home, ignore_errors=True)
            if target != venv:
                shutil.rmtree(target, ignore_errors=True)
            out = p.stdout + p.stderr
            if p.returncode != 0:
                break
            times.append(took)
            print(f"     install run {i + 1}/{install_runs}: {took:.1f} s", flush=True)
        install = "sdist (built with Rust)" if re.search(r"Building wheel|maturin", out) else "prebuilt wheel"
        tail = out.strip().splitlines()[-1] if out.strip() else ""
        ok = _step(steps, "install", f"v/bin/pip install --no-cache-dir rustmapper=={version}",
                   p.returncode == 0 and len(times) == max(1, install_runs),
                   install_detail(install, rustc, os.cpu_count(), times, tail), median(times) if times else None)
        steps[-1].update({"cache": "cold", "rustc": rustc, "cpus": os.cpu_count(), "runs": [round(t, 1) for t in times]})
    for exe in scripts if ok else []:
        path = bindir / exe
        ok &= _step(steps, "help", f"{exe} --help", path.exists() and _run([str(path), "--help"], 60).returncode == 0)
        h = _run([str(path), "crawl", "--help"], 60) if path.exists() else None
        ok &= _step(steps, "crawl_help", f"{exe} crawl --help mentions --start-url",
                    bool(h) and h.returncode == 0 and "--start-url" in h.stdout)
        ok &= _step(steps, "export_help", f"{exe} export-sitemap --help",
                    path.exists() and _run([str(path), "export-sitemap", "--help"], 60).returncode == 0)
    if ok and scripts:
        exe = str(bindir / scripts[0])
        name = scripts[0]
        httpd, port = serve(SITE)
        url = f"http://127.0.0.1:{port}/"
        try:
            # the entrance: crawl, one SIGINT, the file and the sitemap
            data = work / "d"
            proc, t0 = _crawl(exe, ["crawl", "--start-url", url, "--seeding-strategy", "none", "--data-dir", str(data)],
                              work, "crawl.log")
            exited, secs = _stop(proc, signal.SIGINT, CRAWL_SECONDS)
            good, detail = check_jsonl(data / "sitemap.jsonl", port)
            ok &= _step(steps, "crawl_ctrl_c", f"{name} crawl --start-url http://127.0.0.1:<port>/ --seeding-strategy "
                        f"none --data-dir d (no robots.txt; one SIGINT after {CRAWL_SECONDS} s)",
                        good, f"{exited}; {detail}", secs)
            ok &= _export(steps, "export", exe, name, data, work, "s.xml", True)

            # probes: does a crawl end by itself once the pages run out, and does its output say when it is done?
            probe_ends(steps, exe, name, url, port, work)

            # probe: does it read robots.txt on a plain-http site, and keep out of what it disallows?
            probe_robots(steps, exe, name, work)
            # review round 15: and over https, where 0.1.3 does read it: what one disallowed link does to the rest of
            # the host's queue, and what it fetches before robots.txt is back
            probe_stall(steps, exe, name, work)
            probe_resume(steps, exe, name, work)
            probe_late(steps, exe, name, work)

            # review round 8: does --workers hold it to that many requests, and what does a second Ctrl-C do?
            probe_workers(steps, exe, name, work)
            probe_second(steps, exe, name, work)

            # review round 9: what the file says about a page that refused, and how long the quiet mark is
            probe_status(steps, exe, name, work)
            probe_slow(steps, exe, name, work)

            # review round 12: what it does with a redirect, and what export-sitemap keeps
            probe_redirect(steps, exe, name, work)

            # probes: a kill, then export-sitemap and resume on what it left
            d3 = work / "d3"
            proc, t0 = _crawl(exe, ["crawl", "--start-url", url, "--seeding-strategy", "none", "--data-dir", str(d3)],
                              work, "kill.log")
            exited, secs = _stop(proc, signal.SIGTERM, KILL_SECONDS)
            good, detail = check_jsonl(d3 / "sitemap.jsonl", port)
            _step(steps, "kill_writes_file", f"{name} crawl sent SIGTERM after {KILL_SECONDS} s writes sitemap.jsonl",
                  good, f"{exited}; {detail}", secs, gate=False)
            _export(steps, "export_after_kill", exe, name, d3, work, "k.xml", False)
            (d3 / "sitemap.jsonl").unlink(missing_ok=True)
            proc, t0 = _crawl(exe, ["resume", "--data-dir", str(d3)], work, "resume.log")
            exited, secs = _stop(proc, signal.SIGINT, RESUME_SECONDS)
            good, detail = check_jsonl(d3 / "sitemap.jsonl", port)
            tail = _tail(work / "resume.log")
            _step(steps, "resume_after_kill", f"{name} resume --data-dir d3 after the kill writes every page",
                  good, f"{exited}; {detail}" + (f"; {tail}" if tail and not good else ""), secs, gate=False)
        finally:
            httpd.shutdown()
    return {
        "date": dt.datetime.now(dt.timezone.utc).date().isoformat(),
        "runner": f"{ {'Darwin': 'macOS'}.get(platform.system(), platform.system())} {platform.machine()}",
        "python": platform.python_version() if python == sys.executable else
        _run([python, "-c", "import platform;print(platform.python_version())"]).stdout.strip(),
        "version": version,
        "scripts": list(scripts),
        "install": install,
        "steps": steps,
        "ok": bool(ok and steps and all(s["ok"] for s in steps if s.get("gate", True))),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", help="rustmapper version to install (default: edition.version)")
    ap.add_argument("--scripts", help="comma-separated executables (default: edition.scripts)")
    ap.add_argument("--stats", default=str(ROOT / "assets" / "stats.json"))
    ap.add_argument("--latest", action="store_true",
                    help="test PyPI's latest release and the executables its wheels install (the weekly job)")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--work", help="work directory (default: a temporary one, removed after)")
    ap.add_argument("--out", default="runcheck.json")
    ap.add_argument("--install-runs", type=int, default=INSTALL_RUNS, help="how many cold installs to time")
    ap.add_argument("--probe", help="comma-separated probes to run alone, against --exe (no install): "
                    + ", ".join(PROBES))
    ap.add_argument("--exe", help="with --probe: the installed executable")
    a = ap.parse_args(argv)
    if a.probe:
        if not a.exe or not a.version:
            print("runcheck: --probe needs --exe and --version", file=sys.stderr)
            return 2
        work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="runcheck-probe-"))
        work.mkdir(parents=True, exist_ok=True)
        steps: list[dict] = []
        names = [x for x in a.probe.split(",") if x]
        if any(x not in PROBES for x in names):
            print(f"runcheck: --probe takes {', '.join(PROBES)}", file=sys.stderr)
            return 2
        try:
            for x in names:
                PROBES[x](steps, a.exe, Path(a.exe).name, work)
        finally:
            if not a.work:
                shutil.rmtree(work, ignore_errors=True)
        rec = {"date": dt.datetime.now(dt.timezone.utc).date().isoformat(), "version": a.version, "steps": steps}
        Path(a.out).write_text(json.dumps(rec, indent=2) + "\n")
        return 0
    edition = {}
    if a.latest:
        sys.path.insert(0, str(ROOT / "scripts"))
        from data import pypi   # standard library only, like this script
        ed = pypi.edition("rustmapper") or {}
        edition = {"version": ed.get("version"), "scripts": pypi.wheel_scripts(ed.get("_wheel_urls") or []) or []}
    elif not (a.version and a.scripts):
        edition = (json.loads(Path(a.stats).read_text()).get("edition") or {})
    version = a.version or edition.get("version")
    scripts = [s for s in (a.scripts.split(",") if a.scripts else edition.get("scripts") or []) if s]
    if not version or not scripts:
        print("runcheck: no version or no scripts to run", file=sys.stderr)
        return 2
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="runcheck-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        rec = run(version, scripts, work, a.python, a.install_runs)
    finally:
        if not a.work:
            shutil.rmtree(work, ignore_errors=True)
    Path(a.out).write_text(json.dumps(rec, indent=2) + "\n")
    print(f"runcheck: {'ok' if rec['ok'] else 'FAILED'} -> {a.out}")
    return 0 if rec["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
