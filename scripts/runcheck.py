#!/usr/bin/env python3
"""The run check (round 6, SPEC §6): the image claims only what the tool does.

Installs the released rustmapper into a clean venv, runs every executable the wheel ships, crawls a local
site that has no robots.txt, sends one SIGINT, and checks the file the crawl writes and the sitemap it
exports. Standard library only. Writes runcheck.json:

    {date, runner, python, version, scripts, install, steps: [{cmd, ok, detail}], ok}

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
CRAWL_SECONDS = 45
EXIT_SECONDS = 60


def _step(steps: list, cmd: str, ok: bool, detail: str = "") -> bool:
    steps.append({"cmd": cmd, "ok": bool(ok), "detail": detail[:400]})
    print(("ok   " if ok else "FAIL ") + cmd + (f"  ({detail[:160]})" if detail else ""), flush=True)
    return ok


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


def run(version: str, scripts: list[str], work: Path, python: str) -> dict:
    steps: list[dict] = []
    venv = work / "v"
    bindir = venv / ("Scripts" if os.name == "nt" else "bin")
    install = ""
    ok = _step(steps, f"{Path(python).name} -m venv v", _run([python, "-m", "venv", str(venv)]).returncode == 0)
    if ok:
        p = _run([str(bindir / "pip"), "install", "--disable-pip-version-check", "--no-cache-dir",
                  f"rustmapper=={version}"],
                 timeout=1800)
        out = p.stdout + p.stderr
        # --no-cache-dir: a wheel pip built from the sdist last time must not pass as a prebuilt one
        install = "sdist (built with Rust)" if re.search(r"Building wheel|maturin", out) else "prebuilt wheel"
        tail = out.strip().splitlines()[-1] if out.strip() else ""
        ok = _step(steps, f"v/bin/pip install --no-cache-dir rustmapper=={version}", p.returncode == 0, f"{install}; {tail}")
    for exe in scripts if ok else []:
        path = bindir / exe
        ok &= _step(steps, f"{exe} --help", path.exists() and _run([str(path), "--help"], 60).returncode == 0)
        h = _run([str(path), "crawl", "--help"], 60) if path.exists() else None
        ok &= _step(steps, f"{exe} crawl --help mentions --start-url",
                    bool(h) and h.returncode == 0 and "--start-url" in h.stdout)
        ok &= _step(steps, f"{exe} export-sitemap --help",
                    path.exists() and _run([str(path), "export-sitemap", "--help"], 60).returncode == 0)
    if ok and scripts:
        exe = str(bindir / scripts[0])
        name = scripts[0]
        httpd, port = serve(SITE)
        data = work / "d"
        try:
            log = open(work / "crawl.log", "w")
            proc = subprocess.Popen([exe, "crawl", "--start-url", f"http://127.0.0.1:{port}/",
                                     "--seeding-strategy", "none", "--data-dir", str(data)],
                                    stdout=log, stderr=subprocess.STDOUT, cwd=work)
            time.sleep(CRAWL_SECONDS)
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
            try:
                proc.wait(EXIT_SECONDS)
                exited = f"exit {proc.returncode} after one SIGINT"
            except subprocess.TimeoutExpired:
                proc.kill()
                exited = f"still running {EXIT_SECONDS} s after one SIGINT; killed"
            log.close()
            good, detail = check_jsonl(data / "sitemap.jsonl", port)
            ok &= _step(steps, f"{name} crawl --start-url http://127.0.0.1:<port>/ --seeding-strategy none "
                               f"--data-dir d (no robots.txt; one SIGINT after {CRAWL_SECONDS} s)",
                        good, f"{exited}; {detail}")
        finally:
            httpd.shutdown()
        xml = work / "s.xml"
        e = _run([exe, "export-sitemap", "--data-dir", str(data), "--output", str(xml)], 120, cwd=work)
        locs = xml.read_text(encoding="utf-8", errors="replace").count("<loc>") if xml.is_file() else 0
        ok &= _step(steps, f"{name} export-sitemap --data-dir d --output s.xml",
                    e.returncode == 0 and locs == len(PAGES), f"{locs} <loc>")
    return {
        "date": dt.datetime.now(dt.timezone.utc).date().isoformat(),
        "runner": f"{ {'Darwin': 'macOS'}.get(platform.system(), platform.system())} {platform.machine()}",
        "python": platform.python_version() if python == sys.executable else
        _run([python, "-c", "import platform;print(platform.python_version())"]).stdout.strip(),
        "version": version,
        "scripts": list(scripts),
        "install": install,
        "steps": steps,
        "ok": bool(ok and steps and all(s["ok"] for s in steps)),
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
        rec = run(version, scripts, work, a.python)
    finally:
        if not a.work:
            shutil.rmtree(work, ignore_errors=True)
    Path(a.out).write_text(json.dumps(rec, indent=2) + "\n")
    print(f"runcheck: {'ok' if rec['ok'] else 'FAILED'} -> {a.out}")
    return 0 if rec["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
