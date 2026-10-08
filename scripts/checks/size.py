"""size — raw and gzip bytes, element counts and the report's hashes against tokens.BUDGETS.

T10 checks 1 and 3 (+ the element half of 4): report sha256 matches each SVG and stats.json; raw ≤
300 KB, gz ≤ 100 KB, phone raw ≤ 120 KB; one desktop edition set ≤ 250 KB gz; ≤ 3000 elements.
Per-sheet targets (hero 170/60 …) are warnings."""
from __future__ import annotations

import gzip
import hashlib
import os
import re

import tokens
from check import Finding, fail, warn, error

TIER = "fast"


def _gz(data: bytes) -> int:
    return len(gzip.compress(data, compresslevel=9, mtime=0))


def check(ctx) -> list[Finding]:
    out: list[Finding] = []
    b = tokens.BUDGETS
    report = ctx.report or {}
    sheets = report.get("sheets", {})
    per_edition_gz: dict[str, int] = {}
    for name, path in ctx.svgs.items():
        with open(path, "rb") as fh:
            data = fh.read()
        raw, gz = len(data), _gz(data)
        elements = len(re.findall(rb"<[A-Za-z]", data))
        sheet, ed = ctx.split(name)
        phone = ed.startswith("phone")
        if raw > b["svg_kb"] * 1024:
            out.append(fail("SIZE-RAW", f"{raw // 1024} KB raw > {b['svg_kb']} KB", name))
        if gz > b["gz_kb"] * 1024:
            out.append(fail("SIZE-GZ", f"{gz // 1024} KB gz > {b['gz_kb']} KB", name))
        if phone and raw > b["phone_svg_kb"] * 1024:
            out.append(fail("SIZE-PHONE", f"{raw // 1024} KB raw > phone budget {b['phone_svg_kb']} KB", name))
        if elements > b["elements"]:
            out.append(fail("SIZE-ELEMENTS", f"{elements} elements > {b['elements']}", name))
        tgt = b.get("targets_kb", {}).get(sheet)
        if tgt and not phone and (raw > tgt[0] * 1024 or gz > tgt[1] * 1024):
            out.append(warn("SIZE-TARGET", f"{raw // 1024}/{gz // 1024} KB over the {tgt[0]}/{tgt[1]} KB target", name))
        if not phone:
            per_edition_gz[ed] = per_edition_gz.get(ed, 0) + gz
        e = sheets.get(name)
        if e is None:
            out.append(fail("REPORT-MISSING", "file is not in build-report.json", name))
        else:
            if e.get("sha256") != hashlib.sha256(data).hexdigest():
                out.append(fail("REPORT-SHA", "sha256 in build-report.json does not match the file", name))
            if e.get("bytes") != raw:
                out.append(warn("REPORT-BYTES", f"report says {e.get('bytes')} bytes, file has {raw}", name))
    for ed, total in per_edition_gz.items():
        if total > b["page_gz_kb"] * 1024:
            out.append(fail("SIZE-PAGE", f"the {ed} edition set is {total // 1024} KB gz > {b['page_gz_kb']} KB"))
    for name in sheets:
        if name not in ctx.svgs and (not ctx.svgs or ctx.sheet_of(name) in ctx.sheets()):
            out.append(fail("REPORT-ORPHAN", "build-report.json lists a file that is not on disk", name))
    if report and ctx.stats is not None:
        try:
            with open(ctx.stats_path, "rb") as fh:
                sha = hashlib.sha256(fh.read()).hexdigest()
            if report.get("stats_sha") and report["stats_sha"] != sha:
                out.append(fail("REPORT-STATS", "report.stats_sha is not the sha256 of assets/stats.json: rebuild"))
        except OSError:
            out.append(error("REPORT-STATS", f"cannot read {os.path.relpath(ctx.stats_path, ctx.root)}"))
    return out
