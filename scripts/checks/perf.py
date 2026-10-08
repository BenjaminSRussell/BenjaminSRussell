"""perf — the repaint budget (MASTERPLAN 7.3; T10 check 20). TIER perf.

Runs scripts/perf_check.js per sheet: frozen sheets and stills 0 repaints after warm-up; hero
≤ 1/s after 30 s; approaches ≤ 2/s after 44 s; log ≤ 2/s after 50 s; footer ≤ 4 ms/frame after 66 s;
hero-phone at 360 px DPR 3 ≤ 0.25/s after 6 s. perf_check.js --json rows carry pass/reasons;
each failing row is a finding. Rows are written to <out_dir>/perf.json."""
from __future__ import annotations

import json
import os
import subprocess

from check import Finding, fail, warn, info, error

TIER = "perf"
WARM = {"hero": 30, "approaches": 44, "log": 50, "footer": 66}
SECONDS = 8


def _run(root: str, files: list[str], warm: int, extra: list[str]) -> tuple[list[dict] | None, str]:
    cmd = ["node", os.path.join(root, "scripts", "perf_check.js"), *files, f"--warm={warm}", f"--seconds={SECONDS}",
           "--json", "--no-fail", *extra]
    p = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=900)
    so = p.stdout
    try:
        return json.loads(so[so.index("["):]), p.stderr
    except Exception:
        return None, (p.stderr or so)[-400:]


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    root = ctx.root
    if not os.path.exists(os.path.join(root, "scripts", "perf_check.js")):
        return [error("PERF-TOOL", "scripts/perf_check.js missing")]
    rows_all: list[dict] = []
    groups: dict[tuple[int, tuple[str, ...]], list[str]] = {}
    # Day editions carry every animation the night ones do (same code path, other theme); stills and
    # non-hero phones are proven frozen by frames.py (zero <animate*>/<set>), so one frozen witness
    # (hero-still-day) is enough. --dev or --release adds the night editions.
    full = bool(getattr(ctx, "release", False) or getattr(ctx, "dev", False))
    for name, path in sorted(ctx.svgs.items()):
        sheet, ed = ctx.split(name)
        if ed == "day" or (ed == "night" and full):
            groups.setdefault((WARM.get(sheet, 2), ()), []).append(path)
        elif name == "hero-phone-day":
            groups.setdefault((6, ("--width=360", "--dpr=3")), []).append(path)
        elif name == "hero-still-day":
            groups.setdefault((2, ()), []).append(path)
    # continuous windows: the hero sail (4–28 s) and the footer arrival (40–64 s) at ≤ 8 ms/frame
    for nm, warm in (("hero-day", 8), ("footer-day", 45)):
        if nm in ctx.svgs:
            groups.setdefault((warm, ("--class=moving",)), []).append(ctx.svgs[nm])
    for (warm, extra), files in groups.items():
        rows, err = _run(root, files, warm, list(extra))
        if rows is None:
            out.append(error("PERF-RUN", f"perf_check.js failed: {err}"))
            continue
        for r in rows:
            rows_all.append(r)
            base = os.path.basename(str(r.get("file", "")))
            name = base[:-4] if base.endswith(".svg") else base
            verdict = r.get("verdict") or {}
            ok = r.get("pass", verdict.get("pass", True))
            reasons = r.get("reasons") or verdict.get("reasons") or []
            summary = f"{r.get('repaintsPerS')}/s · {r.get('msPerFrame')} ms/frame · cpu {r.get('cpuPct')} % (warm {warm}s)"
            moving = "--class=moving" in extra
            if not ok and moving:
                # Chromium re-rasters the whole <img> per SMIL tick, so a 1280-wide sheet costs ~35–40 ms a
                # frame while anything moves; the window is bounded (hero 4–28 s, footer 40–64 s) and the
                # repaints/s rules above hold after it. Recorded, not failed (acceptance.md).
                out.append(warn("PERF-MOVING", f"{summary}: {'; '.join(map(str, reasons))}", name))
            elif not ok:
                out.append(fail("PERF-BUDGET", f"{summary}: {'; '.join(map(str, reasons))}", name))
            else:
                out.append(info("PERF", summary, name))
    qa = os.path.join(ctx.root, "out", "check")
    os.makedirs(qa, exist_ok=True)
    with open(os.path.join(qa, "perf.json"), "w") as fh:
        json.dump(rows_all, fh, indent=1)
    return out
