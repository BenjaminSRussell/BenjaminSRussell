#!/usr/bin/env python3
"""Draw the chart's sheets in every edition, from assets/stats.json, into assets/v9/.

    python3 scripts/build_assets.py                       # the page's sheet (the hero) × six editions (+ phone stills)
    python3 scripts/build_assets.py --sheets hero,log     # some sheets; the five supporting sheets build on request
    python3 scripts/build_assets.py --editions day,night  # some editions
    python3 scripts/build_assets.py --no-sounding         # yesterday's figures with the pencil note
    python3 scripts/build_assets.py --out /tmp/v9         # elsewhere

Sheet contract (MASTERPLAN decision 22). A module scripts/sheets/<name>.py exposes

    NAME: str; KIND: "chart"|"strip"|"paper"|"edge"
    SIZES = {"desk": (w, h), "phone": (w, h)}
    BREAKS: list[(what, how, why)]
    EDITIONS: tuple[str, ...]            # optional; default the six, hero adds the phone stills
    def build(ctx) -> str                # the whole document (edition.svg(...)) or a bare body
    def alt(data, cfg) -> str            # ≤ 25 words, plain, from data

and `ctx` carries `ed` (edition.Edition), `data` (stats.json), `cfg` (chart.toml), `tl` (a
timeline.Timeline, or a NullTimeline when that module is absent), `k` (the typeset module, or
None), plus `sheet`, `log` (assets/log.json or None), `no_sounding`, `heartbeat`.

Exit status is non-zero on a missing module, a contract violation, a bounds problem or a budget
overrun; nothing is published that this runner did not accept. The build report
(assets/build-report.json, MASTERPLAN §3.5) carries the skeleton per sheet-edition; other modules
append to `report_hooks` to fill text/motion/features.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import importlib
import json
import os
import re
import sys
import tomllib
from dataclasses import dataclass, field
from typing import Any, Callable

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import tokens  # noqa: E402
import edition as E  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, ".."))
ASSETS = os.path.join(ROOT, "assets")
DEFAULT_OUT = os.path.join(ASSETS, "v9")
DEFAULT_REPORT = os.path.join(ASSETS, "build-report.json")
DEFAULT_CFG = os.path.join(ROOT, "chart.toml")
DEFAULT_STATS = os.path.join(ASSETS, "stats.json")

# round 4, D1: the page is the hero and written text. The default build is the hero; the other five
# sheet modules stay in the tree and build with --sheets (tests build them that way).
SHEETS = ["hero"]
ALL_SHEETS = ["hero", "soundings", "approaches", "log", "instruments", "footer"]
ALL_EDITIONS = tuple(E.EDITIONS)
ReportHook = Callable[["Ctx", str, dict], None]
report_hooks: list[ReportHook] = []   # other modules append fn(ctx, svg_text, entry) -> None


class BuildError(Exception):
    """A sheet could not be built honestly: missing module, broken contract, bounds, budget."""


# ------------------------------------------------------------------ configuration

class Cfg(dict):
    """chart.toml as a dict with attribute access (`cfg.alt.hero`, `cfg["alt"]["hero"]`)."""

    def __getattr__(self, name: str) -> Any:
        try:
            v = self[name]
        except KeyError:
            raise AttributeError(name) from None
        return Cfg(v) if isinstance(v, dict) and not isinstance(v, Cfg) else v


def load_cfg(path: str = DEFAULT_CFG) -> Cfg:
    with open(path, "rb") as fh:
        return Cfg(tomllib.load(fh))


def load_stats(path: str = DEFAULT_STATS) -> tuple[dict, str, bytes]:
    with open(path, "rb") as fh:
        raw = fh.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest(), raw


def load_log(cfg: Cfg) -> dict | None:
    p = os.path.join(ROOT, cfg.get("log", {}).get("path", "assets/log.json"))
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


# ------------------------------------------------------------------ collaborators (lazy)

class NullTimeline:
    """Stand-in until scripts/timeline.py lands: every helper returns its end state and no
    animation element is ever emitted, which is exactly the still contract."""

    def __init__(self, sheet: str, motion: bool = True, period: float = tokens.PAGE_PERIOD,
                 quantum: float = tokens.QUANTUM, ambient: bool = False):
        self.sheet, self.motion, self.period, self.quantum, self.ambient = sheet, motion, period, quantum, ambient
        self._cues: dict[str, tuple[float, float]] = {}

    def cue(self, name: str, begin: float, dur: float) -> float:
        self._cues[name] = (begin, begin + dur)
        return begin + dur

    def t(self, name: str) -> tuple[float, float]:
        return self._cues[name]

    def anim(self, *a, **kw) -> str: return ""
    def xform(self, *a, **kw) -> str: return ""
    def fade_in(self, inner: str, *a, **kw) -> str: return inner
    def draw_in(self, path_attrs: str, *a, **kw) -> str: return f"<path {path_attrs}/>"
    def reveal(self, inner: str, *a, **kw) -> str: return inner
    def flash(self, *a, **kw) -> str: return ""
    def fixes(self, *a, **kw) -> str: return ""
    def every(self, *a, **kw) -> str: return ""

    def typed(self, s, x, y, role, begin, seed, **kw):
        return "", begin, []

    def sail(self, path_d, begin, dur, **kw):
        return dataclasses.make_dataclass("Sail", ["anim", "end", "tacks", "facing"])("", begin + dur, [], 1)

    def report(self) -> dict:
        return {"class": "frozen", "indefinite": 0, "repaints_per_s": 0.0, "opening_end_s": 0.0,
                "longest_loop_s": 0.0, "loops": [], "continuous_windows": [], "violations": [],
                "stub": "NullTimeline"}


def make_timeline(sheet: str, ed: E.Edition, cfg: Cfg):
    ambient = sheet == "footer"
    try:
        import timeline  # type: ignore
    except ImportError:
        return NullTimeline(sheet, motion=ed.motion, ambient=ambient)
    try:
        return timeline.Timeline(sheet, motion=ed.motion, period=tokens.PAGE_PERIOD,
                                 quantum=tokens.QUANTUM, ambient=ambient)
    except TypeError:
        return timeline.Timeline(sheet, motion=ed.motion)


def typeset_module():
    try:
        import typeset  # type: ignore
        return typeset
    except ImportError:
        return None


def begin_asset(k, sheet: str, ed: E.Edition) -> None:
    """Reset the type engine's per-sheet registries (glyph defs, runs, exclusions, FIGURES) if it has them."""
    fn = getattr(k, "begin_asset", None)
    if fn is None:
        return
    for args in ((sheet,), ()):          # typeset.begin_asset(sheet, prefix="") — svg() does the prefixing
        try:
            fn(*args)
            return
        except TypeError:
            continue


# ------------------------------------------------------------------ the context

@dataclass
class Ctx:
    ed: E.Edition
    data: dict
    cfg: Cfg
    tl: Any
    k: Any
    sheet: str
    log: dict | None = None
    no_sounding: bool = False
    heartbeat: bool = True
    out_dir: str = DEFAULT_OUT
    stats_sha: str = ""
    extra: dict = field(default_factory=dict)   # scratch for hooks

    @property
    def size(self) -> tuple[int, int]:
        return self.extra.get("size", (self.ed.width, 0))


# ------------------------------------------------------------------ sheets

REQUIRED = ("NAME", "KIND", "SIZES", "BREAKS", "build", "alt")
# round 6: the hero is drawn by sheets/route.py (the way into rustmapper); sheets/hero.py, the coast of the year, is
# retired. File names and README markers stay `hero`.
SHEET_MODULES = {"hero": "route"}
KINDS = ("chart", "strip", "paper", "edge")


def load_sheet(name: str):
    module = SHEET_MODULES.get(name, name)
    try:
        mod = importlib.import_module(f"sheets.{module}")
    except ModuleNotFoundError as exc:
        if exc.name in (f"sheets.{module}", "sheets"):
            raise BuildError(f"no sheet module scripts/sheets/{name}.py") from None
        raise BuildError(f"sheet {name} imports a missing module: {exc.name}") from None
    missing = [a for a in REQUIRED if not hasattr(mod, a)]
    if missing:
        raise BuildError(f"sheet {name} breaks the contract: missing {', '.join(missing)}")
    if mod.NAME != name:
        raise BuildError(f"sheet {name}: NAME is {mod.NAME!r}")
    if mod.KIND not in KINDS:
        raise BuildError(f"sheet {name}: KIND {mod.KIND!r} not in {KINDS}")
    for scale in ("desk", "phone"):
        if scale not in mod.SIZES or len(mod.SIZES[scale]) != 2:
            raise BuildError(f"sheet {name}: SIZES[{scale!r}] must be (w, h)")
    return mod


def editions_for(mod) -> tuple[str, ...]:
    names = tuple(getattr(mod, "EDITIONS", None) or E.EDITION_NAMES)
    if mod.NAME == "hero" and not getattr(mod, "EDITIONS", None):
        names = names + E.HERO_EXTRA
    unknown = [n for n in names if n not in E.EDITIONS]
    if unknown:
        raise BuildError(f"sheet {mod.NAME}: unknown editions {unknown}")
    return names


_VIEWBOX_RE = re.compile(r'viewBox="0 0 (\d+) (\d+)"')


def budget_problems(sheet: str, ed: E.Edition, nbytes: int, gz: int, elements: int) -> list[str]:
    b = tokens.BUDGETS
    out = []
    if nbytes > b["svg_kb"] * 1024:
        out.append(f"{sheet}-{ed.name}: {nbytes // 1024} KB raw exceeds {b['svg_kb']} KB")
    if gz > b["gz_kb"] * 1024:
        out.append(f"{sheet}-{ed.name}: {gz // 1024} KB gz exceeds {b['gz_kb']} KB")
    if ed.phone and nbytes > b["phone_svg_kb"] * 1024:
        out.append(f"{sheet}-{ed.name}: phone file {nbytes // 1024} KB exceeds {b['phone_svg_kb']} KB")
    if elements > b["elements"]:
        out.append(f"{sheet}-{ed.name}: {elements} elements exceed {b['elements']}")
    return out


def bounds_problems(ctx: Ctx, w: int, h: int) -> list[str]:
    """Ask the type engine (if present) whether any run left the safe area; ask the timeline for
    violations. Both are optional collaborators, so both are guarded."""
    out: list[str] = []
    fn = getattr(ctx.k, "check_bounds", None)
    if fn is not None:
        try:
            res = fn(w, h) if fn.__code__.co_argcount >= 2 else fn(w)
        except TypeError:
            res = fn(w)
        out += [f"{ctx.sheet}-{ctx.ed.name}: bounds: {p}" for p in (res or [])]
    rep = getattr(ctx.tl, "report", None)
    if rep is not None:
        try:
            viol = rep().get("violations") or []
        except Exception:  # a half-built Timeline must not take the runner down
            viol = []
        out += [f"{ctx.sheet}-{ctx.ed.name}: motion: {v}" for v in viol]
    return out


def _rel(path: str) -> str:
    """Repo-relative when inside the repo, absolute otherwise (never a ../../ trail)."""
    rel = os.path.relpath(os.path.abspath(path), ROOT)
    return os.path.abspath(path) if rel.startswith("..") else rel


def typeset_report(ctx: Ctx, entry: dict) -> list[str]:
    """What D's engine knows about the sheet just built: the text manifest, exclusion boxes, glyph
    count, and its own lint (`check_type` → problems, `check_budget` → problems). Every call is
    guarded: the engine is a collaborator, not a dependency."""
    k = ctx.k
    if k is None:
        return []
    out: list[str] = []
    fn = getattr(k, "run_records", None)
    if fn is not None:
        try:
            entry["text"] = fn()
        except Exception as exc:
            out.append(f"{ctx.sheet}-{ctx.ed.name}: typeset.run_records failed: {exc}")
    fn = getattr(k, "exclusions", None)
    if fn is not None:
        try:
            entry["exclusions"] = [{"name": n, "x": x, "y": y, "w": w, "h": h} for n, x, y, w, h in fn(named=True)]
        except Exception:
            try:
                entry["exclusions"] = [{"x": x, "y": y, "w": w, "h": h} for x, y, w, h in fn()]
            except Exception as exc:
                out.append(f"{ctx.sheet}-{ctx.ed.name}: typeset.exclusions failed: {exc}")
    fn = getattr(k, "glyph_count", None)
    if fn is not None:
        try:
            entry["glyph_defs"] = fn()
        except Exception:
            pass
    fn = getattr(k, "warnings", None)
    if fn is not None:
        try:
            entry["type_warnings"] = list(fn())
        except Exception:
            pass
    fn = getattr(k, "check_type", None)
    if fn is not None:
        try:
            res = fn(ctx.ed, ctx.ed.scale, ctx.sheet)
        except TypeError:
            res = fn(ctx.ed.theme.edition)
        out += [f"{ctx.sheet}-{ctx.ed.name}: type: {p}" for p in (res or [])]
    fn = getattr(k, "check_budget", None)
    if fn is not None:
        try:
            out += [f"{ctx.sheet}-{ctx.ed.name}: type budget: {p}" for p in (fn() or [])]
        except Exception as exc:
            out.append(f"{ctx.sheet}-{ctx.ed.name}: typeset.check_budget failed: {exc}")
    return out


def last_sentence(alt: str) -> str:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", alt.strip()) if p.strip()]
    return parts[-1] if parts else ""


def build_one(mod, ed: E.Edition, data: dict, cfg: Cfg, log: dict | None, out_dir: str,
              stats_sha: str, no_sounding: bool, heartbeat: bool) -> tuple[str, dict, list[str]]:
    """Build one sheet in one edition. Returns (document, report entry, problems)."""
    sheet = mod.NAME
    w, h = (int(v) for v in mod.SIZES[ed.scale])
    k = typeset_module()
    begin_asset(k, sheet, ed)
    tl = make_timeline(sheet, ed, cfg)
    ctx = Ctx(ed=ed, data=data, cfg=cfg, tl=tl, k=k, sheet=sheet, log=log, no_sounding=no_sounding,
              heartbeat=heartbeat, out_dir=out_dir, stats_sha=stats_sha, extra={"size": (w, h)})
    doc = mod.build(ctx)
    if not isinstance(doc, str) or not doc.strip():
        raise BuildError(f"{sheet}-{ed.name}: build() returned no document")
    if "<svg" not in doc:
        doc = E.svg(ed, w, h, doc, "", sheet=sheet)       # a bare body: wrap it
    doc = E.stamp(doc, stats_sha[:12])
    h = int(ctx.extra.get("height", h))       # a sheet whose height follows its content says so (round 6, the hero)
    problems: list[str] = []
    m = _VIEWBOX_RE.search(doc)
    if not m:
        problems.append(f"{sheet}-{ed.name}: no integer viewBox")
    elif (int(m.group(1)), int(m.group(2))) != (w, h):
        problems.append(f"{sheet}-{ed.name}: viewBox {m.group(1)}×{m.group(2)} but SIZES says {w}×{h}")
    if f'id="{sheet}-' not in doc and 'id="' in doc:
        problems.append(f"{sheet}-{ed.name}: ids are not prefixed {sheet}- (use edition.svg)")
    if not ed.motion and re.search(r"<(animate|animateTransform|set)\b", doc):
        problems.append(f"{sheet}-{ed.name}: still edition contains animation elements")
    problems += bounds_problems(ctx, w, h)

    data_bytes = doc.encode("utf-8")
    nbytes, gz = len(data_bytes), E.gz_size(data_bytes)
    elements, paths = E.count_elements(doc), E.count_paths(doc)
    problems += budget_problems(sheet, ed, nbytes, gz, elements)

    try:
        alt = str(mod.alt(data, cfg)).strip()
    except Exception as exc:
        raise BuildError(f"{sheet}: alt() failed: {exc}") from exc
    rel = _rel(os.path.join(out_dir, E.file_name(sheet, ed)))
    entry = {
        "svg": rel, "sha256": hashlib.sha256(data_bytes).hexdigest(), "w": w, "h": h,
        "form": ed.form, "edition": ed.name, "sheet": sheet, "kind": mod.KIND,
        "bytes": nbytes, "gz": gz, "elements": elements, "paths": paths,
        "breaks": [list(b) for b in mod.BREAKS], "alt": alt, "alt_words": len(alt.split()),
        # filled by plug-ins through report_hooks (typeset → text/exclusions; timeline → motion;
        # chartlib/hero → features, symbols_used, legend, lights)
        "text": [], "exclusions": [], "symbols_used": [], "legend": [], "lights": [],
        "motion": None, "features": [], "bracket_failures": 0, "lock_drift": [],
        "area_law": "area∝commits",
    }
    rep = getattr(tl, "report", None)
    if rep is not None:
        try:
            entry["motion"] = rep()
        except Exception:
            entry["motion"] = None
    problems += typeset_report(ctx, entry)
    for hook in list(report_hooks):
        hook(ctx, doc, entry)
    return doc, entry, problems


# ------------------------------------------------------------------ the run

def resolve_editions(names: list[str] | None, cfg: Cfg) -> tuple[list[str] | None, bool]:
    """Edition filter and whether `[motion] enabled=false` / MOTION=off force every edition still."""
    force_still = not cfg.get("motion", {}).get("enabled", True) or os.environ.get("MOTION", "").lower() == "off"
    if names:
        unknown = [n for n in names if n not in E.EDITIONS]
        if unknown:
            raise BuildError(f"unknown editions {unknown}; known: {', '.join(E.EDITIONS)}")
    return names, force_still


def built_stamp(data: dict) -> str:
    """Deterministic when it can be: SOURCE_DATE_EPOCH, else the stats' own timestamp, else now."""
    sde = os.environ.get("SOURCE_DATE_EPOCH")
    if sde:
        return dt.datetime.fromtimestamp(int(sde), dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for key in ("updated_at", "updated"):
        if data.get(key):
            return str(data[key])
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def main(editions: list[str] | None = None, no_sounding: bool = False, heartbeat: bool = True,
         sheets: list[str] | None = None, out: str = DEFAULT_OUT, report_path: str = DEFAULT_REPORT,
         cfg_path: str = DEFAULT_CFG, stats_path: str = DEFAULT_STATS, quiet: bool = False) -> int:
    """Build; return the number of problems (0 = clean). Raises nothing for a sheet failure: every
    failure is counted and reported so one bad sheet does not hide another."""
    cfg = load_cfg(cfg_path)
    data, stats_sha, _raw = load_stats(stats_path)
    log = load_log(cfg)
    if no_sounding:
        data = dict(data)
        data["no_sounding"] = True
        data.setdefault("provenance", {})
        if isinstance(data["provenance"], dict):
            data["provenance"] = {**data["provenance"], "mode": "cache-failed"}
    names = list(sheets) if sheets else list(SHEETS)
    problems: list[str] = []
    try:
        ed_filter, force_still = resolve_editions(editions, cfg)
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    report = {"built": built_stamp(data), "release": E.RELEASE, "stats_sha": stats_sha,
              "stats": os.path.relpath(stats_path, ROOT), "no_sounding": no_sounding,
              "motion_enabled": not force_still, "poem": [], "sheets": {}, "problems": problems}
    poem: dict[str, str] = {}
    for name in names:
        try:
            mod = load_sheet(name)
            ed_names = editions_for(mod)
        except BuildError as exc:
            problems.append(str(exc))
            print(f"ERROR: {exc}", file=sys.stderr)
            continue
        for ed_name in ed_names:
            if ed_filter and ed_name not in ed_filter:
                continue
            ed = E.EDITIONS[ed_name]
            if force_still:
                ed = ed.as_still()
            try:
                doc, entry, probs = build_one(mod, ed, data, cfg, log, out, stats_sha, no_sounding, heartbeat)
            except BuildError as exc:
                problems.append(str(exc))
                print(f"ERROR: {exc}", file=sys.stderr)
                continue
            except Exception as exc:  # a sheet's own crash is a build failure, named
                msg = f"{name}-{ed_name}: {type(exc).__name__}: {exc}"
                problems.append(msg)
                print(f"ERROR: {msg}", file=sys.stderr)
                continue
            path = os.path.join(out, E.file_name(name, ed_name))
            nbytes, gz = E.write(path, doc)
            entry["svg"] = _rel(path)
            report["sheets"][f"{name}-{ed_name}"] = entry
            if probs:
                problems.extend(probs)
                for p in probs:
                    print(f"PROBLEM: {p}", file=sys.stderr)
            if not quiet:
                print(f"wrote {_rel(path)}  {nbytes // 1024} KB / {gz // 1024} KB gz · "
                      f"{entry['elements']} elements")
            if name not in poem and entry["alt"]:
                poem[name] = last_sentence(entry["alt"])
    report["poem"] = [poem[n] for n in ALL_SHEETS if n in poem] + [poem[n] for n in poem if n not in ALL_SHEETS]
    os.makedirs(os.path.dirname(os.path.abspath(report_path)), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    if not quiet:
        print(f"report {_rel(report_path)}: {len(report['sheets'])} files, {len(problems)} problems")
    return len(problems)


def _split(s: str | None) -> list[str] | None:
    if not s:
        return None
    return [p for p in re.split(r"[,\s]+", s) if p]


def cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("names", nargs="*", help="sheet names (default: the hero)")
    ap.add_argument("--sheets", help="comma-separated sheet names")
    ap.add_argument("--editions", help="comma-separated edition names (default: every edition)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output folder (default assets/v9)")
    ap.add_argument("--report", default=DEFAULT_REPORT, help="build report path")
    ap.add_argument("--cfg", default=DEFAULT_CFG)
    ap.add_argument("--stats", default=DEFAULT_STATS)
    ap.add_argument("--no-sounding", action="store_true", help="draw from cache with the dated pencil note")
    hb = ap.add_mutually_exclusive_group()
    hb.add_argument("--heartbeat", dest="heartbeat", action="store_true", default=True,
                    help="type the heartbeat line on the log (default)")
    hb.add_argument("--no-heartbeat", dest="heartbeat", action="store_false")
    ap.add_argument("--list", action="store_true", help="print sheets and editions, build nothing")
    ap.add_argument("-q", "--quiet", action="store_true")
    a = ap.parse_args(argv)
    if a.list:
        print("sheets:", " ".join(SHEETS), "· on request:", " ".join(n for n in ALL_SHEETS if n not in SHEETS))
        print("editions:", " ".join(E.EDITIONS))
        return 0
    sheets = (_split(a.sheets) or []) + list(a.names) or None
    n = main(editions=_split(a.editions), no_sounding=a.no_sounding, heartbeat=a.heartbeat,
             sheets=sheets, out=a.out, report_path=a.report, cfg_path=a.cfg, stats_path=a.stats, quiet=a.quiet)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(cli())
