#!/usr/bin/env python3
"""check.py — the gate. Three tiers, plug-ins under scripts/checks/, four exit codes.

    python3 scripts/check.py                    # local: fast + render
    python3 scripts/check.py --ci               # fast + render + perf (the nightly gate)
    python3 scripts/check.py --release          # --ci plus the release-only checks (OCR, engines)
    python3 scripts/check.py --dev              # permit what a local iteration needs (seeded data)
    python3 scripts/check.py --only hero,footer # only those sheets
    python3 scripts/check.py --only xml,size    # only those checks (names mix freely)
    python3 scripts/check.py --tier fast        # one tier

    exit 0 pass · 1 fail · 2 pass with warnings · 3 could not check

Plug-in contract (scripts/checks/<name>.py):

    from checks import Finding, fail, warn, error, info
    TIER = "fast"                       # "fast" | "render" | "perf"; default fast
    RELEASE_ONLY = False                # run only under --release
    def check(ctx: CheckCtx) -> list[Finding]

`CheckCtx` gives every plug-in the same view of the artefacts: `svgs` {file-stem: path} under
assets/v9 (filtered by --only), `svg_text(name)`, `sheet_of(name)`, `edition_of(name)`, the build
`report`, `cfg` (chart.toml), `stats` (stats.json), `log` (log.json), `readme` text, `today`,
and the flags `ci`, `release`, `dev`. Cheapest tier first; render does not start if fast failed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib
import json
import os
import pkgutil
import re
import sys
import time
import tomllib
import traceback
from dataclasses import dataclass, field
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import checks as _checks  # noqa: E402  (the plug-in package; its __init__ stays empty)

# Plug-ins do `from check import Finding`; when this file runs as a script, hand them this module
# rather than a second copy of it.
sys.modules.setdefault("check", sys.modules[__name__])

ROOT = os.path.abspath(os.path.join(HERE, ".."))
TIERS = ("fast", "render", "perf")
EDITION_SUFFIXES = ("phone-still-day", "phone-still-night", "still-day", "still-night",
                    "phone-day", "phone-night", "day", "night")


LEVELS = ("fail", "warn", "error", "info")


@dataclass(frozen=True)
class Finding:
    """One result. level: fail (exit 1) · warn (exit 2) · error = could not check (exit 3) · info."""
    level: str
    code: str
    msg: str
    where: str = ""

    def __str__(self) -> str:
        w = f" [{self.where}]" if self.where else ""
        return f"{self.level.upper():5} {self.code}{w}: {self.msg}"


def fail(code: str, msg: str, where: str = "") -> Finding:
    return Finding("fail", code, msg, where)


def warn(code: str, msg: str, where: str = "") -> Finding:
    return Finding("warn", code, msg, where)


def error(code: str, msg: str, where: str = "") -> Finding:
    return Finding("error", code, msg, where)


def info(code: str, msg: str, where: str = "") -> Finding:
    return Finding("info", code, msg, where)


_LEVEL_ALIASES = {"failure": "fail", "err": "fail", "warning": "warn", "skip": "error", "skipped": "error",
                  "blocked": "error", "note": "info", "ok": "info", "pass": "info"}


def normalise(obj, plugin: str) -> Finding:
    """Accept the shapes plug-ins actually return: this Finding, a (level, code, msg[, where])
    namedtuple, or motion.py's (check, level, file, message)."""
    if isinstance(obj, Finding) and obj.level in LEVELS:
        return obj
    fields = [getattr(obj, a) for a in ("level", "code", "msg", "where") if hasattr(obj, a)]
    if not fields and isinstance(obj, tuple):
        fields = list(obj)
    if hasattr(obj, "message") and hasattr(obj, "file"):          # (check, level, file, message)
        fields = [getattr(obj, "check", plugin), obj.level, obj.file, obj.message]
    fields = [str(x) if x is not None else "" for x in fields]
    if len(fields) >= 3 and fields[0] not in LEVELS and fields[1] in LEVELS or (
            len(fields) >= 3 and _LEVEL_ALIASES.get(fields[1]) and fields[0] not in LEVELS):
        check_name, level, where, message = (fields + ["", ""])[:4]
        return Finding(_LEVEL_ALIASES.get(level, level), check_name.upper(), message, where)
    if len(fields) >= 3:
        level, code, msg = fields[:3]
        where = fields[3] if len(fields) > 3 else ""
        level = _LEVEL_ALIASES.get(level, level)
        if level in LEVELS:
            return Finding(level, code, msg, where)
    return error("PLUGIN-RESULT", f"{plugin} returned {obj!r}, not a Finding")


@dataclass
class CheckCtx:
    root: str
    out_dir: str
    svgs: dict[str, str]                 # "hero-day" -> absolute path
    report: dict | None
    report_path: str
    cfg: dict
    cfg_path: str
    stats: dict | None
    stats_path: str
    log: dict | None
    readme: str
    readme_path: str
    ci: bool = False
    release: bool = False
    dev: bool = False
    tier: str = "fast"
    today: dt.date = field(default_factory=dt.date.today)
    _texts: dict[str, str] = field(default_factory=dict, repr=False)

    def get(self, key: str, default=None):
        """Duck-typed access for plug-ins written against a dict-shaped ctx."""
        return getattr(self, key, default)

    def svg_text(self, name: str) -> str:
        if name not in self._texts:
            with open(self.svgs[name], encoding="utf-8") as fh:
                self._texts[name] = fh.read()
        return self._texts[name]

    @staticmethod
    def split(name: str) -> tuple[str, str]:
        for suf in EDITION_SUFFIXES:
            if name.endswith("-" + suf):
                return name[: -len(suf) - 1], suf
        return name, ""

    def sheet_of(self, name: str) -> str:
        return self.split(name)[0]

    def edition_of(self, name: str) -> str:
        return self.split(name)[1]

    def sheets(self) -> list[str]:
        return sorted({self.sheet_of(n) for n in self.svgs})


# ------------------------------------------------------------------ loading

def _read_json(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _read_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def make_ctx(root: str = ROOT, only_sheets: list[str] | None = None, ci=False, release=False, dev=False,
             out_dir: str | None = None, report_path: str | None = None) -> CheckCtx:
    cfg_path = os.path.join(root, "chart.toml")
    try:
        with open(cfg_path, "rb") as fh:
            cfg = tomllib.load(fh)
    except OSError:
        cfg = {}
    out_dir = out_dir or os.path.join(root, cfg.get("chart", {}).get("out_dir", "assets/v9"))
    svgs: dict[str, str] = {}
    if os.path.isdir(out_dir):
        for fn in sorted(os.listdir(out_dir)):
            if fn.endswith(".svg"):
                stem = fn[:-4]
                if only_sheets and CheckCtx.split(stem)[0] not in only_sheets:
                    continue
                svgs[stem] = os.path.join(out_dir, fn)
    log_rel = cfg.get("log", {}).get("path", "assets/log.json")
    report_path = report_path or os.path.join(root, "assets", "build-report.json")
    return CheckCtx(
        root=root, out_dir=out_dir, svgs=svgs,
        report=_read_json(report_path), report_path=report_path,
        cfg=cfg, cfg_path=cfg_path,
        stats=_read_json(os.path.join(root, "assets", "stats.json")),
        stats_path=os.path.join(root, "assets", "stats.json"),
        log=_read_json(os.path.join(root, log_rel)),
        readme=_read_text(os.path.join(root, "README.md")), readme_path=os.path.join(root, "README.md"),
        ci=ci, release=release, dev=dev,
    )


# ------------------------------------------------------------------ plug-ins

@dataclass
class Plugin:
    name: str
    tier: str
    release_only: bool
    module: Any


def discover() -> list[Plugin]:
    out: list[Plugin] = []
    for info in pkgutil.iter_modules(_checks.__path__):
        if info.name.startswith("_"):
            continue
        try:
            mod = importlib.import_module(f"checks.{info.name}")
        except Exception as exc:  # a broken plug-in is itself a finding (could not check)
            mod = _Broken(info.name, exc)
        tier = getattr(mod, "TIER", "fast")
        if tier not in TIERS:
            tier = "fast"
        out.append(Plugin(getattr(mod, "NAME", info.name), tier, bool(getattr(mod, "RELEASE_ONLY", False)), mod))
    return sorted(out, key=lambda p: (TIERS.index(p.tier), p.name))


class _Broken:
    def __init__(self, name: str, exc: Exception):
        self.name, self.exc = name, exc

    def check(self, ctx) -> list[Finding]:
        return [error("PLUGIN-IMPORT", f"checks/{self.name}.py failed to import: {self.exc!r}")]


def run_plugin(p: Plugin, ctx: CheckCtx) -> list[Finding]:
    try:
        res = p.module.check(ctx)
    except Exception as exc:
        tb = traceback.format_exc(limit=3).strip().splitlines()[-1]
        return [error("PLUGIN-CRASH", f"{p.name} raised {type(exc).__name__}: {exc} ({tb})")]
    return [normalise(f, p.name) for f in (res or [])]


def exit_code(findings: list[Finding]) -> int:
    levels = {f.level for f in findings}
    if "fail" in levels:
        return 1
    if "error" in levels:
        return 3
    if "warn" in levels:
        return 2
    return 0


# ------------------------------------------------------------------ the run

def main(ci: bool = False, release: bool = False, dev: bool = False, only: list[str] | None = None,
         tiers: tuple[str, ...] | None = None, root: str = ROOT, out_dir: str | None = None,
         quiet: bool = False, summary_path: str | None = None, report_path: str | None = None) -> int:
    """0 pass · 1 fail · 2 warnings · 3 could not check."""
    if release:
        ci = True
    if tiers is None:
        tiers = TIERS if ci else ("fast", "render")
    plugins = discover()
    names = {p.name for p in plugins}
    only_checks = [o for o in (only or []) if o in names]
    only_sheets = [o for o in (only or []) if o not in names]
    ctx = make_ctx(root, only_sheets or None, ci=ci, release=release, dev=dev, out_dir=out_dir, report_path=report_path)
    findings: list[Finding] = []
    if not ctx.svgs:
        findings.append(error("NO-SHEETS", f"no SVGs under {os.path.relpath(ctx.out_dir, root)}; run build_assets.py first"))
    if ctx.report is None:
        findings.append(error("NO-REPORT", "assets/build-report.json missing or unreadable"))
    ran: list[tuple[str, str, int, float]] = []
    for tier in TIERS:
        if tier not in tiers:
            continue
        if tier != "fast" and exit_code(findings) == 1:
            if not quiet:
                print(f"-- {tier} tier skipped: fast tier failed")
            break
        for p in plugins:
            if p.tier != tier or (only_checks and p.name not in only_checks) or (p.release_only and not release):
                continue
            ctx.tier = tier
            t0 = time.perf_counter()
            res = run_plugin(p, ctx)
            ran.append((tier, p.name, len(res), time.perf_counter() - t0))
            findings.extend(res)
    code = exit_code(findings)
    if not quiet:
        for tier, name, n, secs in ran:
            print(f"-- {tier:6} {name:12} {n:3} finding(s)  {secs * 1000:6.0f} ms")
        for f in findings:
            if f.level != "info" or dev:
                print(f)
        verdict = {0: "pass", 1: "FAIL", 2: "pass with warnings", 3: "could not check"}[code]
        print(f"check.py: {verdict} (exit {code}) · {sum(1 for f in findings if f.level == 'fail')} fail · "
              f"{sum(1 for f in findings if f.level == 'warn')} warn · {sum(1 for f in findings if f.level == 'error')} error")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(f"### check.py — exit {code}\n\n")
            for f in findings:
                if f.level != "info":
                    fh.write(f"- `{f.level}` **{f.code}** {f.where} {f.msg}\n")
            fh.write("\n")
    return code


def _split(s: str | None) -> list[str] | None:
    return [p for p in re.split(r"[,\s]+", s) if p] if s else None


def cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="the chart's gate")
    ap.add_argument("--ci", action="store_true", help="all three tiers")
    ap.add_argument("--release", action="store_true", help="--ci plus release-only checks")
    ap.add_argument("--dev", action="store_true", help="local iteration: permit seeded data, print info")
    ap.add_argument("--only", help="comma-separated sheet names and/or check names")
    ap.add_argument("--tier", help="comma-separated tiers to run (fast,render,perf)")
    ap.add_argument("--out-dir", help="where the SVGs are (default from chart.toml: assets/v9)")
    ap.add_argument("--report", help="build report to check against (default assets/build-report.json)")
    ap.add_argument("--summary", help="append a Markdown summary here (e.g. $GITHUB_STEP_SUMMARY)")
    ap.add_argument("-q", "--quiet", action="store_true")
    a = ap.parse_args(argv)
    tiers = tuple(_split(a.tier)) if a.tier else None
    if tiers and any(t not in TIERS for t in tiers):
        ap.error(f"tiers must be among {TIERS}")
    return main(ci=a.ci, release=a.release, dev=a.dev, only=_split(a.only), tiers=tiers,
                out_dir=a.out_dir, quiet=a.quiet, summary_path=a.summary or os.environ.get("GITHUB_STEP_SUMMARY"),
                report_path=a.report)


if __name__ == "__main__":
    sys.exit(cli())
