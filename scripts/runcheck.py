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
PAGES = ("index.html", "a.html", "b.html")
KEYS = ("url", "depth", "status_code", "title")
CRAWL_SECONDS = 45      # the entrance crawl: one SIGINT after this long (three pages take well under a second)
EXIT_SECONDS = 60       # how long a stopped crawl may take to exit
ENDS_SECONDS = 150      # ends_by_itself: how long a crawl with no signal is given to exit by itself
KILL_SECONDS = 5        # kill_writes_file: SIGTERM after this long
RESUME_SECONDS = 20     # resume_after_kill: one SIGINT after this long, if it is still running


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

            # probe: does a crawl end by itself once the pages run out?
            d2 = work / "d2"
            proc, t0 = _crawl(exe, ["crawl", "--start-url", url, "--seeding-strategy", "none", "--data-dir", str(d2)],
                              work, "ends.log")
            try:
                proc.wait(ENDS_SECONDS)
                took = time.monotonic() - t0
                good, detail = check_jsonl(d2 / "sitemap.jsonl", port)
                _step(steps, "ends_by_itself", f"{name} crawl with no signal exits by itself within {ENDS_SECONDS} s",
                      proc.returncode == 0 and good, f"exit {proc.returncode} after {took:.1f} s; {detail}", took,
                      gate=False)
            except subprocess.TimeoutExpired:
                _stop(proc, signal.SIGINT, 0)
                _step(steps, "ends_by_itself", f"{name} crawl with no signal exits by itself within {ENDS_SECONDS} s",
                      False, f"still running at {ENDS_SECONDS} s; stopped with one SIGINT", ENDS_SECONDS, gate=False)

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
    a = ap.parse_args(argv)
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
