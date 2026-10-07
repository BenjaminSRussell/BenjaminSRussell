"""pypi — the edition line: latest version, its upload date, release count, wheels, status.

    edition(project="rustmapper") -> dict | None
      {project, version, date, releases, status, wheels[], stale:false}
    `status` from the Development Status classifier ("alpha" | "beta" | "stable" | ... | null);
    `wheels` = platform tags of the latest version's .whl files, so T8 prints the one-wheel
    sentence from data. None on any failure; the caller keeps the cached edition, stale:true.
"""
from __future__ import annotations

import json
import urllib.request

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
    return {
        "project": project,
        "version": version,
        "date": dates[0] if dates else None,
        "releases": len(d["releases"]),
        "status": status,
        "wheels": wheels,
        "uploads": uploads(d),
        "stale": False,
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


def edition(project: str = "rustmapper", timeout: int = 20) -> dict | None:
    req = urllib.request.Request(f"https://pypi.org/pypi/{project}/json", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return parse(json.load(r), project)
    except Exception as exc:  # network, JSON, schema
        print("pypi lookup failed:", exc)
        return None
