"""pypi — the edition line: latest version, its upload date, release count, wheels, status.

    edition(project="rustmapper") -> dict | None
      {project, version, date, releases, status, wheels[], stale:false}
    `status` from the Development Status classifier ("alpha" | "beta" | "stable" | ... | null);
    `wheels` = platform tags of the latest version's .whl files, so T8 prints the one-wheel
    sentence from data. None on any failure; the caller keeps the cached edition, stale:true.

    Round 6 (SPEC §5.2): `files` carries the latest version's wheel and sdist URLs;
    `wheel_scripts(urls)` reads each wheel's RECORD (and entry_points.txt) for the executables it
    installs, and `fetch_sdist(edition, dest)` downloads and unpacks the sdist for the release anchors.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tarfile
import urllib.request
import zipfile

from . import USER_AGENT

STATUS = {
    "1 - Planning": "planning", "2 - Pre-Alpha": "pre-alpha", "3 - Alpha": "alpha", "4 - Beta": "beta",
    "5 - Production/Stable": "stable", "6 - Mature": "mature", "7 - Inactive": "inactive",
}


def parse(d: dict, project: str) -> dict:
    info = d["info"]
    version = info["version"]
    files = d["releases"].get(version) or []
    dates = sorted(f["upload_time"][:10] for f in files if f.get("upload_time"))
    status = None
    for c in info.get("classifiers") or []:
        if c.startswith("Development Status ::"):
            status = STATUS.get(c.split("::", 1)[1].strip(), c.split("::", 1)[1].strip().lower())
    wheels = [wheel_tag(f["filename"]) for f in files if f["filename"].endswith(".whl")]
    sdist = next(({"filename": f["filename"], "url": f.get("url"), "sha256": (f.get("digests") or {}).get("sha256")}
                  for f in files if f.get("packagetype") == "sdist" or f["filename"].endswith(".tar.gz")), None)
    return {
        "project": project,
        "version": version,
        "date": dates[0] if dates else None,
        "releases": len(d["releases"]),
        "status": status,
        "wheels": wheels,
        "uploads": uploads(d),
        "stale": False,
        "_wheel_urls": [f["url"] for f in files if f["filename"].endswith(".whl") and f.get("url")],
        "_sdist": sdist,
    }


def wheel_tag(filename: str) -> str:
    """'rustmapper-0.1.3-cp313-cp313-macosx_11_0_arm64.whl' → 'cp313-cp313-macosx_11_0_arm64'."""
    stem = filename[:-4] if filename.endswith(".whl") else filename
    parts = stem.split("-")
    return "-".join(parts[-3:]) if len(parts) >= 5 else stem


def uploads(d: dict) -> list[dict]:
    """[{version, date}] one per release version (first upload), oldest first — the notices fallback."""
    out = []
    for v, files in d["releases"].items():
        ts = sorted(f["upload_time"] for f in files if f.get("upload_time"))
        if ts:
            out.append({"version": v, "date": ts[0][:10], "time": ts[0]})
    out.sort(key=lambda u: u["time"])
    return out


def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def scripts_in_wheel(data: bytes) -> list[str]:
    """The executables a wheel installs: `<name>-<version>.data/scripts/<exe>` entries of its RECORD, plus the
    console_scripts of entry_points.txt. Sorted, unique."""
    out: set[str] = set()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        record = next((n for n in names if n.endswith(".dist-info/RECORD")), None)
        rows = z.read(record).decode("utf-8", "replace").splitlines() if record else names
        for row in rows:
            path = row.split(",", 1)[0]
            m = re.fullmatch(r"[^/]+-[^/]+\.data/scripts/([^/]+)", path)
            if m:
                out.add(m.group(1))
        ep = next((n for n in names if n.endswith(".dist-info/entry_points.txt")), None)
        if ep:
            section = None
            for line in z.read(ep).decode("utf-8", "replace").splitlines():
                line = line.strip()
                if line.startswith("["):
                    section = line.strip("[]").strip()
                elif section == "console_scripts" and "=" in line:
                    out.add(line.split("=", 1)[0].strip())
    return sorted(out)


def modules_in_wheel(data: bytes) -> list[str]:
    """The top-level Python modules a wheel installs (review round 3: is there a Python API to import?): a package
    directory with an `__init__.py`, or a top-level `.py` / extension module. `.data/` and `.dist-info/` are not
    modules. Sorted, unique."""
    out: set[str] = set()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for path in z.namelist():
            top = path.split("/", 1)[0]
            if top.endswith((".dist-info", ".data")):
                continue
            if path.endswith("/__init__.py") and path.count("/") == 1:
                out.add(top)
            elif "/" not in path and re.search(r"\.(py|so|pyd)$", path):
                out.add(re.split(r"[.]", path, 1)[0])
    return sorted(out)


def wheel_modules(urls: list[str], get=_get) -> list[str] | None:
    """The union over every wheel of the release; None when any download fails (the caller keeps the cache)."""
    out: set[str] = set()
    for url in urls:
        try:
            out |= set(modules_in_wheel(get(url)))
        except Exception as exc:  # network, zip
            print("pypi wheel read failed:", exc)
            return None
    return sorted(out)


def wheel_scripts(urls: list[str], get=_get) -> list[str] | None:
    """The union over every wheel of the release; None when any download fails (the caller keeps the cache)."""
    out: set[str] = set()
    for url in urls:
        try:
            out |= set(scripts_in_wheel(get(url)))
        except Exception as exc:  # network, zip
            print("pypi wheel read failed:", exc)
            return None
    return sorted(out)


def fetch_sdist(ed: dict, dest: str, get=_get) -> dict | None:
    """Download the release's sdist into `dest` and unpack it; {filename, sha256, root} or None."""
    sd = (ed or {}).get("_sdist") or {}
    if not sd.get("url"):
        return None
    try:
        raw = get(sd["url"], timeout=120)
    except Exception as exc:
        print("pypi sdist download failed:", exc)
        return None
    sha = hashlib.sha256(raw).hexdigest()
    if sd.get("sha256") and sd["sha256"] != sha:
        print(f"pypi sdist sha256 {sha} != the index's {sd['sha256']}; not used")
        return None
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as t:
        t.extractall(dest, filter="data")
        tops = {m.name.split("/", 1)[0] for m in t.getmembers()}
    root = os.path.join(dest, sorted(tops)[0]) if len(tops) == 1 else dest
    return {"filename": sd["filename"], "sha256": sha, "root": root}


def edition(project: str = "rustmapper", timeout: int = 20) -> dict | None:
    req = urllib.request.Request(f"https://pypi.org/pypi/{project}/json", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return parse(json.load(r), project)
    except Exception as exc:  # network, JSON, schema
        print("pypi lookup failed:", exc)
        return None
