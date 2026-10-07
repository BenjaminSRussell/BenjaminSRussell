"""checks/motion.py — static motion lint for the built SVGs (T4; plug-in for scripts/check.py).

`check(ctx) -> list[Finding]`. The ctx is duck-typed: it may carry `svgs` / `files` (paths),
`assets_dir`, `report` (the build-report dict) or `report_path`; anything missing falls back to
`assets/v9/*.svg`, `assets/*.svg` and `assets/build-report.json` under the repository root.

Per file (MASTERPLAN 7.3, T4 §2.6):
  * no `animateMotion`
  * no animated geometry attribute outside a finite one-shot <= 4 s (stroke-dashoffset tracing)
  * no `filter` on an element with an animated ancestor (or on an animated element)
  * `repeatCount` only on `opacity` / `transform`; every loop period in tokens.LOOP_PERIODS
  * discrete instants (begin + keyTime·dur of calcMode="discrete" animations and loops, `<set>` begins)
    on the 0.5 s grid — typing bursts (`<set>` inside a `<use>`/glyph group between 44 and 50 s) are
    exempt, see T4 deviation note
  * no syncbase (`.end`, `.begin`, `repeatEvent`) in any `begin`/`end`
  * every opacity freeze-in has base opacity="0"
  * `*-still*.svg` and phone non-hero files contain zero <animate*>/<set>
  * per-sheet indefinite count and estimated repaints/s within the budget table
  * build-report.json["motion"][sheet]["violations"] is empty (Timeline.report() agrees)

Run directly: `python3 scripts/checks/motion.py assets/v9/*.svg` (exit 1 on errors).
"""
from __future__ import annotations

import glob
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

try:  # the runner's record when it has one
    from check import Finding  # type: ignore
except Exception:  # noqa: BLE001
    Finding = namedtuple("Finding", "check level file message")

import tokens  # noqa: E402

CHECK = "motion"
QUANTUM = float(tokens.QUANTUM)
LOOP_PERIODS = tuple(float(p) for p in tokens.LOOP_PERIODS)
GEOMETRY_ATTRS = frozenset({
    "x", "y", "cx", "cy", "width", "height", "r", "rx", "ry", "x1", "y1", "x2", "y2", "d",
    "points", "stroke-dashoffset", "stroke-dasharray", "stroke-width", "font-size", "offset",
    "startOffset", "pathLength", "viewBox",
})
GEOMETRY_MAX_DUR = 4.0
LOOP_ATTRS = frozenset({"opacity", "transform"})
ANIM_TAGS = ("animate", "animateTransform", "animateMotion", "set")
SYNCBASE = re.compile(r"(?:[A-Za-z_][\w-]*\.(?:end|begin|repeat)|repeatEvent|accessKey)")
# indefinite animations and repaints/s after the opening, per sheet (T4 §2.7 + MASTERPLAN 2.1)
BUDGET = {
    "hero": {"indefinite": 2, "repaints": 1.0},
    "soundings": {"indefinite": 0, "repaints": 0.0},
    "approaches": {"indefinite": 10, "repaints": 2.0},
    "log": {"indefinite": 1, "repaints": 2.0},
    "instruments": {"indefinite": 0, "repaints": 0.0},
    "footer": {"indefinite": 12, "repaints": None},   # the one ambient sheet; perf gate measures ms/frame
}
TYPED_WINDOW = (40.0, 52.0)   # typing bursts are off-grid by nature (MASTERPLAN 2.1: 44–48 s)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _secs(v: str | None) -> float | None:
    if v is None:
        return None
    v = v.strip()
    if v in ("indefinite", ""):
        return None
    m = re.match(r"^(-?\d+(?:\.\d+)?)\s*(ms|s|min)?$", v)
    if not m:
        return None
    x = float(m.group(1))
    unit = m.group(2) or "s"
    return x / 1000 if unit == "ms" else x * 60 if unit == "min" else x


def _on_grid(t: float) -> bool:
    q = t / QUANTUM
    return abs(q - round(q)) < 1e-6


def sheet_of(path: str) -> str:
    base = os.path.basename(path)
    return re.split(r"[-.]", base)[0]


def is_frozen_file(path: str) -> bool:
    base = os.path.basename(path)
    if "-still" in base:
        return True
    if "-phone" in base and not base.startswith("hero"):
        return True
    return sheet_of(path) in ("soundings", "instruments", "legend")


def scan(svg_text: str, name: str = "<svg>") -> list[Finding]:
    """Lint one SVG document; `name` labels the findings (and decides frozen-file rules)."""
    out: list[Finding] = []
    err = lambda msg: out.append(Finding(CHECK, "error", name, msg))  # noqa: E731
    warn = lambda msg: out.append(Finding(CHECK, "warn", name, msg))  # noqa: E731
    try:
        root = ET.fromstring(svg_text.encode("utf-8") if isinstance(svg_text, str) else svg_text)
    except ET.ParseError as exc:
        err(f"not well-formed XML: {exc}")
        return out

    frozen = is_frozen_file(name)
    anims: list[tuple[ET.Element, ET.Element]] = []  # (anim element, its parent)
    instants: set[float] = set()
    loops = 0

    def walk(el: ET.Element, animated_ancestor: bool):
        has_anim_child = any(_local(c.tag) in ANIM_TAGS for c in el)
        if "filter" in el.attrib and (animated_ancestor or has_anim_child):
            err(f"<{_local(el.tag)} filter=…> under an animated ancestor (12: never filter what moves)")
        for c in el:
            if _local(c.tag) in ANIM_TAGS:
                anims.append((c, el))
            walk(c, animated_ancestor or has_anim_child)

    walk(root, False)

    if frozen and anims:
        err(f"frozen edition contains {len(anims)} animation element(s); stills carry zero <animate*>/<set>")

    for a, parent in anims:
        tag = _local(a.tag)
        attr = a.get("attributeName", "")
        begin_raw = a.get("begin", "0s")
        end_raw = a.get("end")
        for raw in (begin_raw, end_raw):
            if raw and SYNCBASE.search(raw):
                err(f"syncbase in {tag} {attr}: {raw!r}")
        if tag == "animateMotion":
            err("animateMotion (re-rasters every frame while active, holds included)")
            continue
        begin = _secs(begin_raw)
        if begin is None:
            err(f"{tag} {attr}: unreadable begin {begin_raw!r}")
            continue
        repeat = a.get("repeatCount")
        loop = repeat is not None and repeat not in ("1",)
        dur = _secs(a.get("dur"))
        calc = a.get("calcMode", "linear")
        if tag == "set":
            where = _local(parent.tag)
            typed = where in ("use", "text", "tspan", "path") and TYPED_WINDOW[0] <= begin <= TYPED_WINDOW[1]
            if not _on_grid(begin) and not typed:
                err(f"<set {attr}> begins off the {QUANTUM:g} s grid at {begin:g} s")
            if attr == "opacity" and a.get("to") == "1" and parent.get("opacity") != "0":
                err(f"<set opacity to=1 at {begin:g}s> on a <{where}> without base opacity=\"0\"")
            continue
        if attr == "transform" or tag == "animateTransform":
            attr_name = "transform"
        else:
            attr_name = attr
        if loop:
            loops += 1
            if attr_name not in LOOP_ATTRS:
                err(f"repeatCount on {attr_name!r}: only opacity/transform may loop")
            if dur is None or not any(abs(dur - p) < 1e-9 for p in LOOP_PERIODS):
                err(f"loop period {a.get('dur')!r} on {attr_name} not in LOOP_PERIODS {tokens.LOOP_PERIODS}")
            if calc != "discrete" and sheet_of(name) != "footer":
                err(f"continuous loop on {attr_name} ({calc}) outside the ambient sheet")
        if attr_name in GEOMETRY_ATTRS:
            if loop:
                err(f"geometry attribute {attr_name!r} loops")
            elif dur is None or dur > GEOMETRY_MAX_DUR or a.get("fill") != "freeze":
                err(f"geometry attribute {attr_name!r} animated for {a.get('dur')} (limit a frozen {GEOMETRY_MAX_DUR:g} s one-shot)")
            elif begin + dur > 60:
                warn(f"geometry one-shot {attr_name!r} ends at {begin + dur:g} s (openings are ≤ 4 s after their group starts)")
        # opacity freeze-in: base must be 0
        if attr_name == "opacity" and not loop and a.get("fill") == "freeze":
            vals = (a.get("values") or "").split(";")
            if vals and vals[0].strip() == "0" and parent.get("opacity") != "0":
                err(f"opacity freeze-in at {begin:g}s without base opacity=\"0\" on <{_local(parent.tag)}>")
        # discrete instants on the grid
        if calc == "discrete" or loop:
            if not _on_grid(begin):
                err(f"{tag} {attr_name} begins off the grid at {begin:g} s")
            if calc == "discrete" and dur:
                kts = [float(k) for k in (a.get("keyTimes") or "").split(";") if k.strip()]
                vals = (a.get("values") or "").split(";")
                if not kts:
                    kts = [i / max(len(vals) - 1, 1) for i in range(len(vals))]
                for k, (v0, v1) in zip(kts[1:], zip(vals, vals[1:])):
                    if v0 == v1:
                        continue
                    inst = begin + k * dur
                    if not _on_grid(inst):
                        err(f"discrete instant {inst:.3f} s off the grid ({attr_name}, begin {begin:g}, keyTime {k:g})")
                    if loop:
                        instants.add(round(inst % 96.0, 3))
                if loop and vals and vals[-1] != vals[0]:
                    instants.add(round((begin + dur) % 96.0, 3))
            elif loop and calc != "discrete":
                instants.add(math.inf)

    sheet = sheet_of(name)
    budget = BUDGET.get(sheet)
    if budget and not frozen:
        if loops > budget["indefinite"]:
            err(f"{loops} indefinite animations, budget {budget['indefinite']} for {sheet}")
        if budget["repaints"] is not None:
            if math.inf in instants:
                err(f"continuous loop on {sheet}: budget is {budget['repaints']} repaints/s discrete")
            else:
                rate = len(instants) / 96.0
                if rate > budget["repaints"] + 1e-9:
                    err(f"≈{rate:.2f} repaints/s after the opening, budget {budget['repaints']} for {sheet}")
    return out


def _files_from(ctx) -> list[str]:
    for key in ("svgs", "files", "paths"):
        v = getattr(ctx, key, None) if not isinstance(ctx, dict) else ctx.get(key)
        if v:
            return [p for p in v if str(p).endswith(".svg")]
    d = getattr(ctx, "assets_dir", None) if not isinstance(ctx, dict) else ctx.get("assets_dir")
    cands = []
    for base in ([d] if d else []) + [os.path.join(ROOT, "assets", "v9"), os.path.join(ROOT, "assets")]:
        if base and os.path.isdir(base):
            cands = sorted(glob.glob(os.path.join(base, "*.svg")))
            if cands:
                break
    return cands


def _report_from(ctx) -> dict | None:
    rep = getattr(ctx, "report", None) if not isinstance(ctx, dict) else ctx.get("report")
    if isinstance(rep, dict):
        return rep
    p = getattr(ctx, "report_path", None) if not isinstance(ctx, dict) else ctx.get("report_path")
    for cand in ([p] if p else []) + [os.path.join(ROOT, "assets", "build-report.json"),
                                        os.path.join(ROOT, "build-report.json")]:
        if cand and os.path.exists(cand):
            try:
                with open(cand, encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:  # noqa: BLE001
                return None
    return None


def check(ctx=None) -> list[Finding]:
    out: list[Finding] = []
    for path in _files_from(ctx):
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            out.append(Finding(CHECK, "error", path, f"unreadable: {exc}"))
            continue
        out.extend(scan(text, os.path.relpath(path, ROOT) if path.startswith(ROOT) else path))
    rep = _report_from(ctx)
    if rep:
        motion = rep.get("motion") or {}
        # either {sheet: report} at the top or sheets{...}.motion per MASTERPLAN 3.5
        if not motion:
            motion = {k: v.get("motion") for k, v in (rep.get("sheets") or {}).items() if isinstance(v, dict) and v.get("motion")}
        for sheet, m in motion.items():
            for v in (m or {}).get("violations") or []:
                out.append(Finding(CHECK, "error", f"build-report:{sheet}", f"Timeline violation: {v}"))
            cls = (m or {}).get("class")
            if cls == "ambient" and not str(sheet).startswith("footer"):
                out.append(Finding(CHECK, "error", f"build-report:{sheet}", "ambient class on a non-footer sheet"))
    return out


def main(argv: list[str]) -> int:
    ctx = {"svgs": argv} if argv else None
    findings = check(ctx)
    for f in findings:
        print(f"{f.level:5s} {f.file}: {f.message}")
    errors = sum(1 for f in findings if f.level == "error")
    print(f"motion: {len(findings)} finding(s), {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
