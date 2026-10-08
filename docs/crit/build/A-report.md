# Builder A report — T1 architecture & pipeline

No git commands run. `tokens.py` untouched. Files written, all inside my ownership unless flagged in §4:
`scripts/edition.py` · `scripts/build_assets.py` (rewritten) · `scripts/check.py` · `scripts/checks/{xml,size,strings,position,expiry}.py` ·
`scripts/render_readme.py` · `scripts/publish_chart.py` · `scripts/svgkit.py` (facade; old kit moved to `scripts/svgkit_v8.py`) ·
`scripts/sheets/_blank.py` (test fixture sheet, excluded from `SHEETS`) · `chart.toml` · `.github/workflows/profile.yml` (rewritten) ·
`.github/workflows/perf.yml` · `.github/PULL_REQUEST_TEMPLATE.md` · `LICENSE` · `LICENSE-ASSETS.md` · `tests/test_edition.py` · `tests/test_pipeline.py`.
Tests: `python3 -m unittest tests.test_edition tests.test_pipeline` → 29 pass. Whole suite: 105 run, 1 failure in C's `test_data.py` (not mine).

## 1. What was built

### `scripts/edition.py`
- `Edition(name, theme, motion, scale, width)` frozen dataclass with properties `dark`, `still`, `phone`, `form` ("desk|phone|still", the report field) and `as_still()`.
- `EDITION_NAMES` = the six; `HERO_EXTRA` = `("phone-still-day", "phone-still-night")`; `EDITIONS` dict of all eight. File names are `f"{sheet}-{edition}.svg"`, so the hero's extras land as `hero-phone-still-day.svg` (decision 9's 38 files).
- `svg(ed, w, h, body, defs="", sheet="sheet", stats_sha="@STATS_SHA@", paper_fill=None)`: XML declaration; one header comment
  `<!-- chart v9 · sheet hero · edition night · built by scripts/build_assets.py from assets/stats.json <sha12> · do not edit: the next run redraws it -->`;
  `<svg viewBox="0 0 W H" width height role="img" data-sheet data-edition>`; opaque paper rect first (theme.paper, both editions); then
  `<defs>…</defs>` + body with every id prefixed. No timestamps anywhere (test enforces).
- `prefix_ids(markup, sheet)`: rewrites `id="x"`, `url(#x)`, `href="#x"`, `xlink:href="#x"` **and SMIL timing references** (`begin="arrive.end+20s; serpent.end+93.6s"`, `end="sea10.begin+3.3s"`, `x.repeat(n)`) to `<sheet>-x`. Idempotent (never double-prefixes); external hrefs untouched. Defs and body are prefixed as one unit so cross-references keep resolving.
- `I(x)` integer coordinate, half away from zero (not banker's); `fmt(v, places=1)` → "12", "12.3", "0" (never "-0"); `pt(x, y)` → "3,8".
- `stamp(doc, sha)` fills the header placeholder; `write(path, doc) -> (bytes, gz_bytes)` writes only when bytes differ, gz is `gzip(level 9, mtime 0)`; `gz_size`, `sha12`, `count_elements` (opening tags), `count_paths`, `header()`, `paper()`, `file_name()`, `edition(name)`.

### `scripts/build_assets.py`
- Sheet contract enforced at import: `NAME, KIND ∈ {chart,strip,paper,edge}, SIZES{desk,phone}, BREAKS, build(ctx), alt(data, cfg)`; optional `EDITIONS` tuple (default the six; hero adds the two phone stills unless it declares its own).
- `Ctx` dataclass: `ed, data, cfg, tl, k, sheet, log, no_sounding, heartbeat, out_dir, stats_sha, extra` (+ `size` property). `cfg` is a `Cfg(dict)` with attribute access (`cfg.alt.hero`, `cfg["fittings"]["items"]`). `tl` = `timeline.Timeline(sheet, motion=ed.motion, period=96, quantum=0.5, ambient=(sheet=="footer"))`, falling back to a local `NullTimeline` stub if the module is absent; `k` = `typeset` module or `None`. `typeset.begin_asset(sheet)` is called before every build (prefix left "" because `svg()` prefixes by regex, per D's request).
- `build(ctx)` may return the whole document (via `edition.svg`) or a bare body (wrapped). The runner then: stamps the stats sha; checks viewBox == SIZES; checks ids are prefixed; still editions carry no `<animate|animateTransform|set>`; asks `k.check_bounds` (if any) and `tl.report()["violations"]`; D's `check_type(ed, scale, sheet)` and `check_budget()`; budgets from `tokens.BUDGETS` (raw, gz, phone raw, elements). Any of these → problem → non-zero exit; nothing is hidden.
- Writes `assets/v9/<sheet>-<edition>.svg` (`--out`), and `assets/build-report.json` (`--report`) per MASTERPLAN §3.5: `built, release, stats_sha, stats, no_sounding, motion_enabled, poem[], problems[], sheets{ "<sheet>-<edition>": {svg, sha256, w, h, form, edition, sheet, kind, bytes, gz, elements, paths, breaks, alt, alt_words, text[], exclusions[], symbols_used[], legend[], lights[], motion, features[], bracket_failures, lock_drift[], area_law, glyph_defs?, type_warnings?} }`. `text`/`exclusions`/`glyph_defs` are filled from typeset (`run_records()`, `exclusions(named=True)`, `glyph_count()`), `motion` from `tl.report()`; everything else is left for plug-ins via **`build_assets.report_hooks: list[Callable[[Ctx, svg_text, entry], None]]`** (append from any module; tested).
- `poem[]` = last sentence of each sheet's alt in sheet order. `built` is deterministic: `SOURCE_DATE_EPOCH` → stats `updated_at`/`updated` → now.
- CLI: `[names…] --sheets a,b --editions day,night --out DIR --report PATH --cfg --stats --no-sounding --heartbeat/--no-heartbeat --list -q`. `[motion] enabled=false` or `MOTION=off` turns every edition into a still. `--no-sounding` sets `data["no_sounding"]=True` and `provenance.mode="cache-failed"` for the sheets' pencil note. Exit 1 on any problem (missing module, contract, bounds, budget, sheet exception). Two builds are byte-identical (test).

### `chart.toml` (Python 3.11+ `tomllib`)
`[chart]` login/release/seed 27/breakpoint 767/base_url (chart branch, assets/v9)/branch/out_dir · `[identity]` names, emails, bots · `[position] text=""` · `[contact]` linkedin="" resume="" · `[copy]` thesis, role_line, unit lines, limit label, footer line, log footnote · `[copy.review]` role_line/thesis = 2027-06 · `[motion] enabled=true` · `[budgets]` from tokens.BUDGETS · `[log] path` · `[social] hero_png_sha=""` · `[[features]]` Rust-sitemap→rustmapper (vessel, named-5), Scrapy→"Scrapy Harbor" (harbour), BenjaminSRussell→"Profile Shoal" (shoal, decision 12) · `[[sources]]` A SITEMAPS / B CT LOGS / C COMMON CRAWL (no `first`: unmeasured) · `[[notices]]` the five T8 principles verbatim as notices 1–5 (title/body/cite/repo/date/source="toml") · `[alt]` six T8 alts with decision 29 applied + `alt_poem` · `[fittings]` groups + 18 `[[fittings.items]]` from T9 table C (name, repo, group). No invented facts; `[[claims.*]]` left out (T7 owns the sha-backed values).

### `scripts/check.py` + plug-ins
- Tiers fast/render/perf; local default fast+render, `--ci` all, `--release` adds release-only plug-ins (`RELEASE_ONLY = True`), `--dev`, `--only` (mixes sheet names and plug-in names), `--tier`, `--out-dir`, `--report`, `--summary` (or `$GITHUB_STEP_SUMMARY`). Render/perf tiers do not start if fast failed. Exit 0/1/2/3 per T10 (fail → 1; else error "could not check" → 3; else warn → 2).
- Discovery: every `scripts/checks/*.py` not starting with `_`, exposing `check(ctx) -> list[Finding]`, optional `TIER`, `NAME`, `RELEASE_ONLY`. A plug-in that fails to import or raises becomes an `error` finding (exit 3), never a crash.
- **`Finding(level, code, msg, where="")` lives in `check.py`** (`from check import Finding, fail, warn, error, info`). Plug-ins from C/E that fall back to namedtuples are accepted by `normalise()`: `(level, code, msg)` and motion.py's `(check, level, file, message)` both work. `CheckCtx` is duck-typed (`ctx.get(key, default)` as well as attributes): `root, out_dir, svgs{stem→path}, svg_text(name), sheet_of/edition_of/split, sheets(), report, report_path, cfg, cfg_path, stats, stats_path, log, readme, readme_path, ci, release, dev, tier, today`.
- `checks/xml.py`: lxml parse (ET fallback); forbids `<text|tspan|textPath|script|style|foreignObject|image|animateMotion>`; external hrefs; ids unique and `<sheet>-` prefixed; every `href="#"`, `url(#)`, SMIL `x.begin/end` resolves; `values`/`keyTimes` counts; frozen opacity fade-ins need `opacity="0"` base; viewBox vs report.
- `checks/size.py`: raw/gz/phone/elements vs `tokens.BUDGETS`; per-sheet targets as warnings; desktop edition set ≤ page_gz_kb; report sha256 ↔ file, report ↔ disk both ways, `report.stats_sha` ↔ `sha256(stats.json)`.
- `checks/strings.py`: your list + T10's (ILLUSTRATIVE, PENDING, SEEDED, NOT FOR NAVIGATION, Here be dragons, Fair winds, example.com, "Oct 2024", thanks for reading, that's a mood, Hi I'm Ben, drawn not templated, REFRESHED DAILY, works at night, lorem, TODO, FIXME, v7, `<!-- POSITION`) over SVGs, report text manifest + alts, README (with `<!-- n:key -->…<!-- /n -->` spans and markers stripped, so a build-written "Oct 2024" passes and a hand-typed one fails), chart.toml.
- `checks/position.py`: ⟨ ⟩ in `[position]`/`[contact]` → fail; `""` → warn; README `<!-- POSITION` or any ⟨ ⟩ outside comments → fail; non-empty position must equal the README's visible line.
- `checks/expiry.py`: `[copy.review]` YYYY-MM(-DD) past today → warn.

### `scripts/render_readme.py`
`main(readme, cfg, stats, fittings=None, root=ROOT, use_sheet_alts=True, warnings=None) -> str`. Blocks `picture:<sheet>`, `position`, `contact`, `figures`, `notices`, `instruments`, `license`; inline `n:` keys from `figures(stats, cfg)` (commits, all_hands, calendar_total, repo_count, chart_no, followers, stars, account_since, taken, taken_time, updated_at, edition_version/date/project, notices_n, name, login, release) — reads stats v1 and v2 keys. `<picture>` in decision-9 order with the hero's two extra sources, URLs from `[chart].base_url`, no `height`, no `<a>`. Alt from `sheets.<name>.alt(data, cfg)` when importable, else the `[alt]` template; > 25 words or starting "The" → warning. Bare `<picture>` elements naming a sheet are wrapped in markers on first run (so T8's template works as committed). Idempotent (`--check` exits 1 with a unified diff when stale; tested). License block renders only when `LICENSE`, `LICENSE-ASSETS.md` and `chart.toml` exist. Verified against `docs/crit/tech/T8-README.final.md` in scratch: 32 `<source>` lines, `--check` clean on the second run.

### `scripts/publish_chart.py`
`collect(root, report_path, social_dir) -> [(src, dst)]` ships exactly the SVGs named in `build-report.json` + the report + `social/*.png`; refuses when the report lists problems or names a missing file. `publish(root, branch="chart", remote="origin", dry_run, …)` uses plumbing against the repo's own object store (a throw-away `GIT_INDEX_FILE`, staging dir as `--work-tree`): `add -A → write-tree → commit-tree` (no parent, bot author) `→ update-ref → push --force refs/heads/chart`. `--dry-run` stops after `commit-tree` and prints the tree listing. **Not run here** (no git in this session; the tree is not a git repo). `collect`/`stage` are unit-tested.

### Workflows, template, licences
`profile.yml`: cron 06:20 UTC, dispatch (`dry_run`), push on scripts/**, chart.toml, assets/log.json, requirements.txt, `repository_dispatch: release-published`; `concurrency: chart, cancel-in-progress`; `contents: write`; 15 min; Python 3.13 with pip cache; `pip install -r requirements.txt`; unittest → `build_stats.py` (id stats) → `build_assets.py --heartbeat` → `render_readme.py` → `check.py --ci` (exit 2 allowed) → upload `assets/build-report.json` + `out/check/` → commit stats/log/lock/README to main with `git pull --rebase` and one retry → `publish_chart.py`; `if: failure() && steps.stats.outcome == 'failure'` → `--no-sounding` build, render, gate, publish. `perf.yml`: scripts/** pushes, Sundays 07:40, dispatch; Node 22 + Playwright (chromium/webkit/firefox) + tesseract; `check.py --release`; uploads `out/check`, `out/perf`. PR template = T10 §5 checklist. `LICENSE` MIT 2025–2026 Benjamin Russell with scope note; `LICENSE-ASSETS.md` CC BY 4.0 for sheets, data JSON, chart.toml copy, README/DESIGN prose; OFL note for Instrument Serif and IBM Plex (reserved names).

### `scripts/svgkit.py` facade
`from tokens import (Theme, THEMES, W, INK, DASH, SCALE, SCALE_PHONE, FLOORS, ROLES, GRADE, NIGHT_LIGHT_CUTS, EASE, LOOP_PERIODS, QUANTUM, PAGE_PERIOD, BUDGETS)`; `from edition import *`; `from typeset import *` and `from timeline import *` each guarded by try/except (both present now, 85 names total); submodules reachable as `svgkit.tokens/edition/typeset/timeline`; the old kit whole as `svgkit.v8` (`scripts/svgkit_v8.py`). Verified: `k.svg is edition.svg`, `k.text is typeset.text`, timeline's `EASE/QUANTUM/LOOP_PERIODS/PAGE_PERIOD` equal tokens'. `sheets/_v8_reference.py` and `chartlib_v8.py` import `svgkit_v8` and still import cleanly.

## 2. Exact public API (signatures)

```python
# edition.py
@dataclass(frozen=True) class Edition: name: str; theme: tokens.Theme; motion: bool; scale: Literal["desk","phone"]; width: int
    dark: bool; still: bool; phone: bool; form: str; def as_still() -> Edition
EDITION_NAMES: tuple[str, ...]; HERO_EXTRA: tuple[str, ...]; EDITIONS: dict[str, Edition]
def edition(name) -> Edition;  def file_name(sheet, ed: Edition | str) -> str
def svg(ed, w, h, body, defs="", sheet="sheet", stats_sha=STATS_SHA_PLACEHOLDER, paper_fill=None) -> str
def prefix_ids(markup, sheet) -> str;  def ids_in(markup) -> list[str]
def header(ed, sheet, stats_sha=...) -> str;  def paper(ed, w, h, fill=None) -> str;  def stamp(doc, stats_sha) -> str
def I(x) -> int;  def fmt(v, places=1) -> str;  def pt(x, y) -> str
def write(path, doc) -> tuple[int, int];  def gz_size(data: bytes) -> int;  def sha12(data: bytes) -> str
def count_elements(doc) -> int;  def count_paths(doc) -> int
RELEASE="v9"; BUILDER; STATS_SHA_PLACEHOLDER="@STATS_SHA@"; DESK_W=1280; PHONE_W=720

# build_assets.py
SHEETS; ALL_EDITIONS; report_hooks: list[Callable[[Ctx, str, dict], None]]
class Cfg(dict)  # attribute access
@dataclass class Ctx: ed, data, cfg, tl, k, sheet, log=None, no_sounding=False, heartbeat=True, out_dir, stats_sha="", extra={}
class NullTimeline(sheet, motion=True, period=96.0, quantum=0.5, ambient=False)   # stub; E's module wins when present
def load_cfg(path) -> Cfg;  def load_stats(path) -> (dict, sha256_hex, bytes);  def load_log(cfg) -> dict | None
def load_sheet(name) -> module;  def editions_for(mod) -> tuple[str, ...]
def build_one(mod, ed, data, cfg, log, out_dir, stats_sha, no_sounding, heartbeat) -> (doc, entry, problems)
def main(editions=None, no_sounding=False, heartbeat=True, sheets=None, out=DEFAULT_OUT, report_path=DEFAULT_REPORT,
         cfg_path=DEFAULT_CFG, stats_path=DEFAULT_STATS, quiet=False) -> int   # number of problems; 0 = clean
def cli(argv=None) -> int   # 0 | 1

# check.py
@dataclass(frozen=True) class Finding: level: str; code: str; msg: str; where: str = ""
def fail/warn/error/info(code, msg, where="") -> Finding;  LEVELS = ("fail","warn","error","info")
@dataclass class CheckCtx: root, out_dir, svgs, report, report_path, cfg, cfg_path, stats, stats_path, log, readme, readme_path,
                           ci, release, dev, tier, today;  get(key, default); svg_text(name); split(name); sheet_of; edition_of; sheets()
def discover() -> list[Plugin];  def normalise(obj, plugin) -> Finding;  def exit_code(findings) -> int
def main(ci=False, release=False, dev=False, only=None, tiers=None, root=ROOT, out_dir=None, quiet=False,
         summary_path=None, report_path=None) -> int   # 0 · 1 · 2 · 3
# plug-in: TIER="fast"|"render"|"perf"; RELEASE_ONLY=False; def check(ctx) -> list[Finding]

# render_readme.py
def main(readme, cfg, stats, fittings=None, root=ROOT, use_sheet_alts=True, warnings=None) -> str
def figures(stats, cfg) -> dict[str, str];  def picture(sheet, cfg, alt) -> str;  def alt_for(sheet, stats, cfg, figs, use_sheets=True) -> str
def fill_block(text, name, content) -> (text, found);  def fill_inline(text, key, value) -> (text, n);  def migrate_pictures(text, sheets=SHEETS) -> str
def position_block(cfg); contact_block(cfg); figures_block(figs); notices_block(cfg, stats); instruments_block(cfg, fittings=None); license_block(root)
def fmt_n(n) -> str;  def fmt_date(s, month_only=False) -> str;  def load(cfg_path, stats_path) -> (cfg, stats)

# publish_chart.py
def collect(root, report_path, social_dir) -> list[(src, dst)];  def stage(staging, files);  def message(report_path) -> str
def publish(root, branch="chart", remote="origin", dry_run=False, report_path=REPORT, social_dir=SOCIAL, msg=None) -> int
class PublishError(Exception)
```

## 3. What I need from others

- **All sheet owners (T2/T3/T9):** return `edition.svg(ctx.ed, w, h, body, defs, sheet=NAME)` with `k.glyph_defs()` inside `defs`; use `ctx.ed.scale` / `ctx.ed.motion` for phone/still branches; read `ctx.no_sounding` for the pencil note and `ctx.heartbeat` on the log; keep `alt()` ≤ 25 words and not starting with "The"; fill `entry["symbols_used"|"legend"|"lights"|"features"]` through `build_assets.report_hooks` (or tell me and I will wire a `report(ctx) -> dict` hook into the sheet contract).
- **D:** `check_type(ed, scale, sheet)` and `check_budget()` are called per build and fail it; `run_records()`/`exclusions(named=True)`/`glyph_count()`/`warnings()` land in the report. If `check_bounds(w, h)` ever exists I call it too.
- **E:** `Timeline(sheet, motion=, period=, quantum=, ambient=)` matches; `report()["violations"]` fails the build. Please return `Finding("fail", …)` (not `"error"`) for real violations in `checks/motion.py`: in the runner's vocabulary `error` means "could not check" and exits 3, not 1 (still red, but the wrong colour of red). Also note `build_assets.NullTimeline` is my stub for when your module is absent; yours is used whenever importable.
- **C:** `checks/data.py` and `checks/log.py` already fit (`ctx.get`, 3-field findings). The report's `stats_sha` is the sha256 of `assets/stats.json` bytes; one write per run keeps check 1 honest. `render_readme.figures()` reads v2 keys (`repo_count, commits, account_since, taken, updated_at, all_hands, calendar_total, edition, notices`).
- **B:** `scripts/chartlib_v8.py` now imports `svgkit_v8` (one line, see §4).
- **T8 / README:** the committed `README.md` is still v7; `check.py` fails it on six banned phrases by design. Drop in `T8-README.final.md`: `render_readme.py` wraps its bare `<picture>` blocks in markers on first run. Two template nits: an empty `contact` block leaves a doubled `&nbsp;·&nbsp;` around it; the `<!-- T1: … -->` placeholder comments inside pictures are replaced wholesale (fine).
- **tokens.py (proposal, not edited):** nothing needed by my files.

## 4. Deviations

1. **`Finding` lives in `check.py`, not `scripts/checks/__init__.py`.** I wrote it there first; another builder overwrote `__init__.py` with an empty file at 19:43. Every other plug-in does `from check import Finding` with a namedtuple fallback, so `check.py` now owns the record, aliases itself into `sys.modules["check"]` when run as a script, and `normalise()` accepts the two namedtuple shapes in the tree. `__init__.py` is left as the empty file.
2. **One line in B's `scripts/chartlib_v8.py`** (`import svgkit as k` → `import svgkit_v8 as k`): the mechanical consequence of the contract's svgkit rename; without it `_v8_reference.py` imports the v9 facade's `text_use` and breaks. Flagged here for B.
3. **`publish_chart.py` uses plumbing (`write-tree`/`commit-tree`/`update-ref`) in the repo's own object store rather than a temp worktree**, so the checkout's credentials and remote work in Actions and `--dry-run` creates no ref. Not executed in this session (no git).
4. **Edition names for the hero stills are `phone-still-day/night`** (file `hero-phone-still-day.svg`), modelled as two extra editions the hero gets by default; any sheet can opt in with `EDITIONS`.
5. **Stats sha placeholder**: `svg()` writes `@STATS_SHA@`; the runner stamps it. A sheet built outside the runner keeps the placeholder (and the test for "no timestamps" holds).
6. **`check.py --only`** mixes sheet names and plug-in names (MASTERPLAN only shows sheets); `--tier` added. `--dev` currently only reveals `info` findings; "seeded permitted" is C's `data.py` decision via `ctx.dev`.
7. **Alts**: decision 29 applied to T8's hero and soundings alts ("A boat sails in and anchors."; soundings loses "draws in once" → "Below, one line per repository.") and to `alt_poem[]`; T8 should re-read those two lines.
8. **Notices** are T8's five principles (title/body/cite) so `N = 5` matches "Notice 5"; release notices from stats.json are appended after them with `source != "toml"`.
9. **`[fittings]`** is `groups` + `[[fittings.items]]` (TOML needs a table array for name/repo/group), and the Markdown mirror prints "Parquet and Arrow" for "Parquet · Arrow" to keep the " · " separator unambiguous.
10. **`scripts/sheets/_blank.py` kept** (NAME `_blank`, not in `SHEETS`, built only when named; the tests use it). Delete freely once the six real sheets exist.
11. **Python 3.13** in the workflows (contract) rather than T1's 3.12; `pip install -r requirements.txt` at the repo root (where the pinned file is), not `scripts/requirements.txt`.
12. A run of `build_assets.py` on the six not-yet-written sheets wrote `assets/build-report.json` listing six "no sheet module" problems and exited 1 — the honest state of the tree right now.
