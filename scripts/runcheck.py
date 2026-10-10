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
    quiet_slow_page     (review round 9) the quiet mark has a number: on a site whose second page is held SLOW_HOLD
                        s, two `Received work item` lines are at least SLOW_HOLD s apart (silence shorter than the
                        bound is not the end), and after QUIET_BOUND s with no such line, one SIGINT writes every page

Only the robots probe, against a binary already installed (it needs no install):

    python3 scripts/runcheck.py --probe robots_read --exe <venv>/bin/rust_sitemap --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe workers_cap,second_ctrl_c --exe … --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe non200_status,quiet_slow_page --exe … --version 0.1.3 --out steps.json
    python3 scripts/runcheck.py --probe redirect_kept --exe … --version 0.1.3 --out steps.json

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
    """The fixture server that keeps every request path it served, in order (review round 6, robots_read)."""
    paths: list = []

    def log_request(self, code="-", size="-"):
        type(self).paths.append((time.monotonic(), self.path.split("?")[0]))


def serve_logged(site: Path) -> tuple[socketserver.TCPServer, int, list]:
    """As serve(), and returns the list the server appends (time, path) to for every request."""
    paths: list = []
    cls = type("_LoggedSite", (_Logged,), {"paths": paths})
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


def probe_robots(steps: list, exe: str, name: str, work: Path) -> None:
    """robots_read: crawl the robots fixture over plain http, one SIGINT after ROBOTS_SECONDS, read the server's log."""
    httpd, port, paths = serve_logged(ROBOTS_SITE)
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


PROBES = {"robots_read": probe_robots, "workers_cap": probe_workers, "second_ctrl_c": probe_second,
          "non200_status": probe_status, "quiet_slow_page": probe_slow, "redirect_kept": probe_redirect}


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
