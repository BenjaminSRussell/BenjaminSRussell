"""frames — the still-frame gate and the silhouette test (MASTERPLAN 7.2; T10 checks 17–18). TIER render.

For each motion sheet (day edition) with a still edition: `render.mjs frames` at the instants
{0, 0.5, opening_end+0.1, 24, 48, 72, 95, 600} ∪ event instants, compared to the still:
ink coverage ≥ 0.95 at every instant (hero: ≥ 0.6 at 0 s rising to ≥ 0.95 from 4.1 s), changed-pixel
fraction ≤ 1.5 % after opening_end, no emptied-ledger frame; still editions contain zero animation
elements. Silhouettes: six day stills at 128 px, pairwise L1 ≥ 0.25.
Writes frames under <out_dir>/frames/<sheet>/ and a contact strip for looking at."""
from __future__ import annotations

import json
import os
import re
import subprocess

from check import Finding, fail, warn, info, error

TIER = "render"
BASE_T = [0, 0.5, 24, 48, 72, 95, 600]
EVENTS = {"hero": [4.1, 28.1], "approaches": [28.1, 42.1], "log": [44.5, 48], "footer": [40.5, 64.1, 84.5]}
HERO_RAMP = {0: 0.6, 2: 0.7}                # hero coverage floors before 4.1 s: title, frame, land are static at t=0 (7.2)


def _node(args: list[str], cwd: str, timeout=600) -> tuple[int, str, str]:
    p = subprocess.run(["node", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    root = ctx.root
    render = os.path.join(root, "scripts", "render.mjs")
    if not os.path.exists(render):
        return [error("FRAMES-TOOL", "scripts/render.mjs missing")]
    report = (ctx.report or {}).get("sheets", {})
    out_dir = os.path.join(ctx.root, "out", "check", "frames")
    os.makedirs(out_dir, exist_ok=True)
    for name, path in sorted(ctx.svgs.items()):
        sheet, ed = ctx.split(name)
        if ed != "day":
            continue
        still_name = f"{sheet}-still-day"
        still = ctx.svgs.get(still_name)
        if not still:
            out.append(warn("FRAMES-NO-STILL", "no still edition to compare against", name))
            continue
        if re.search(r"<(animate|animateTransform|animateMotion|set)\b", ctx.svg_text(still_name)):
            out.append(fail("FRAMES-STILL-ANIM", "still edition contains animation elements", still_name))
        motion = (report.get(name) or {}).get("motion") or {}
        opening = float(motion.get("opening_end_s") or 0.0)
        frozen = not re.search(r"<(animate|animateTransform|set)\b", ctx.svg_text(name))
        times = sorted(set(BASE_T + EVENTS.get(sheet, []) + ([round(opening + 0.1, 2)] if opening else [])))
        if frozen:
            times = [0, 95]
        sheet_dir = os.path.join(out_dir, sheet)
        os.makedirs(sheet_dir, exist_ok=True)
        js = os.path.join(sheet_dir, "frames.json")
        rc, so, se = _node([render, "frames", path, sheet_dir, ",".join(str(t) for t in times), "--still", still,
                            "--strip", os.path.join(sheet_dir, "strip.png"), "--json", js], root)
        if rc != 0 or not os.path.exists(js):
            out.append(error("FRAMES-RENDER", f"render.mjs failed: {se.strip()[-300:]}", name))
            continue
        rows = json.load(open(js))
        rows = rows.get("frames", rows) if isinstance(rows, dict) else rows
        worst = 1.0
        for r in rows:
            t = float(r.get("t", 0))
            cov = r.get("coverage")
            if cov is None:
                continue
            worst = min(worst, cov)
            floor = 0.95
            if sheet == "hero" and t < 4.1:
                floor = max(v for k, v in HERO_RAMP.items() if t >= k)
            if cov < floor:
                out.append(fail("FRAMES-COVERAGE", f"t={t}s ink coverage {cov:.3f} < {floor}", name))
            if t < opening:
                continue                      # the sheet is drawing itself in; coverage floors above still apply
            if r.get("changedFrac") is not None and r["changedFrac"] > 0.015:
                # moving windows are allowed to differ: hero 4–28, footer 40–64, approaches/log events
                moving = (sheet == "hero" and 4 <= t <= 28.5) or (sheet == "footer" and 40 <= t <= 64.5) \
                    or (sheet == "approaches" and 28 <= t <= 42.5) or (sheet == "log" and 44 <= t <= 48.5)
                if not moving:
                    out.append(fail("FRAMES-CHANGED", f"t={t}s differs from the still by {100 * r['changedFrac']:.2f} % > 1.5 %", name))
            if r.get("blankLedger"):
                out.append(fail("FRAMES-LEDGER", f"t={t}s empties {100 * r.get('emptiedCellFrac', 0):.0f} % of the still's inked cells", name))
            if sheet == "footer" and r.get("inkFrac", 1) < 0.002:
                out.append(fail("FRAMES-EMPTY", f"t={t}s footer frame is blank", name))
        out.append(info("FRAMES", f"{len(rows)} frames · worst coverage {worst:.3f} · {sheet_dir}/strip.png", name))
    # the six desk stills: a phone still never shares a page with a desk sheet (v9.1)
    stills = [ctx.svgs[n] for n in sorted(ctx.svgs) if n.endswith("-still-day") and "phone" not in n]
    if len(stills) >= 2:
        rc, so, se = _node([render, "silhouette", *stills, "--out", os.path.join(out_dir, "silhouette")], root)
        try:
            res = json.loads(so[so.index("{"):])
        except Exception:
            res = None
        if res is None:
            out.append(error("FRAMES-SILHOUETTE", f"silhouette run failed: {se.strip()[-200:]}"))
        else:
            for p in res.get("pairs", []):
                if not p.get("pass"):
                    out.append(fail("FRAMES-SILHOUETTE", f"{p['a']} and {p['b']} look alike at 128 px (L1 {p['l1']} < 0.25)"))
            out.append(info("FRAMES-SILHOUETTE", f"min pairwise L1 {res.get('minL1')}"))
    return out
