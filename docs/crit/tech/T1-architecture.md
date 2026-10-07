# T1 — Architecture & pipeline

The code today has the four faults 36 names (no sheet modules behind `SHEETS`, `render_all(check=False)`, `repos` int-vs-list merged through the file on disk, `seeded: true` committed) and `snake.yml` still runs nightly (23). Everything below is designed so that Ben in 2028 edits TOML and the chart follows.

## 1. Decisions

1. **One source of truth per concern, three files.** `scripts/tokens.py` (colour, ink levels, widths, dashes, type roles; `--md` regenerates DESIGN.md's tables), `chart.toml` (every printed string, notices, position, feature slots/aliases, motion switch, budgets), `assets/stats.json` (measured data, written once per run). Delete `design-tokens.json`, `svgkit.DARK/LIGHT`, the seven dead `Theme` fields and the Inter/DejaVu font entries (per 30 F1, 23 F4, 36 F5). No hex literal under `sheets/` (test: grep).
2. **One in-memory model, validated, written once.** `build_stats.py` composes `fetch_github()`, `survey_repos()`, `pypi_edition()`, `releases()` into a dict, validates it against `scripts/data/schema.json`, and writes the file at the end. `fetch_repodata.main()` never touches disk again (per 36 F2). Validation failure = render from cache with the pencil note, never a half-written cache.
3. **Populations are named, never mixed.** `commits.authored` (git, Ben's identities, the population every island and sounding is drawn from), `commits.contributions` (GraphQL, 1,828), `commits.surveyed` (all authors incl. bots, 1,868). Sheets use `authored`; the legend names the source (per 08, 32, 34, 36). T7 may show two instruments; T7 may not blend them.
4. **Hours and weekdays are counted in author-local time, per commit-day.** `git log --format=%aI|%an|%ae` keeps the author offset; `hours_days[h]` = distinct (local date, hour) pairs (per 32, 08, 36 F8). No "works at night" anywhere; no location is inferred (offsets are stored as a histogram only).
5. **The profile repo stays on the chart; the bot comes off.** Author filter excludes `github-actions[bot]` and other bots, so the fourth-largest island stops growing one commit a day, while `repo_count` = 24 honestly includes this repo and the colophon says so (36 F4 reconciled with 34: filter authors, do not hide a public repo).
6. **Six editions per sheet, one build, one timeline.** `day`, `night` (1280, full motion); `still-day`, `still-night` (1280, SMIL stripped, end values applied); `phone-day`, `phone-night` (720, portrait compositions, no indefinite motion; the hero phone may keep its ≤4 s opening). Phone editions are reduced-motion by construction (per 09 idea 1, 10 F6, 12 idea 2), so six files, not eight.
7. **Breakpoint 767, sources most-specific first:** phone+dark, phone, reduce+dark, reduce, dark, `<img>` day (per 10 F2/F3, 09). Phone before reduce because a phone edition is already motion-safe and its composition matters more than a 1280 still squeezed to 360 px. The order is proven on a scratch repo before it is relied on (11).
8. **Generated SVGs live on an orphan branch `chart`; data JSON lives on `main`.** 36's proposal weighed: 36 files × ~150 KB of path data that diffs badly would add ~3 MB to `main` per changed day, and the reader who clones the generator should get the generator. `stats.json`, `log.json`, `layout.lock.json` are small, human-readable, and *are* the chart's own log, so their daily 2 KB diff stays on `main`. Cost: a one-time URL change in the README (already paid once for `output/`).
9. **Honest job or no job.** `check=True`, non-zero on missing module, bounds warning, schema or gate failure; nothing is published that `check.py` has not passed; a failed sounding publishes yesterday's figures with a dated pencil note (per 36 F1, 21 F6, 11 §9).
10. **Determinism is the cache policy.** Seeds from `chart.toml`, integer coordinates, no timestamps in SVG except the printed `LAST SOUNDING` line; identical bytes mean identical ETags, so no `?v=` ever (per 11 §4). File names change only at design releases (`assets/v9/…` folder on the `chart` branch).
11. **Feature slots are keyed by `chart.toml` aliases and locked.** `[[features]] repo="Rust-sitemap" aliases=["rustmapper"] slot="named-5"`; `assets/layout.lock.json` records centre/radius; a move > 40 px is a warning in the build report, not a rearranged sea (per 36 F3, 30 F6).
12. **Daily survey, not weekly.** Parallel blobless clones of 24 small repos take about a minute; a failed clone keeps yesterday's record with `stale: true`. One cadence, one dateline (`SURVEYED 7 OCT 2026`), and islands grow by commits, which is the point (36 idea 2 declined for simplicity; its failure case is handled by `stale`).
13. **LICENSE: MIT for code, CC BY 4.0 for sheets and copy, OFL fonts kept** (per 23 F4, 35). "Borrow it" becomes true before it is printed.
14. **Perf and filmstrip gates run on `scripts/**` changes and weekly, not on the daily cron.** Playwright costs ~300 MB per run; the daily job runs the five-second Python gate (36 F7); design changes run 12's harness.

## 2. Design and implementation detail

### 2.1 Module layout

```
chart.toml · LICENSE (MIT) · LICENSE-ASSETS.md (CC BY 4.0)
scripts/tokens.py        Theme, INK, WIDTH, DASH, ROLE; `--md` → DESIGN.md tables
scripts/svgkit.py        glyph outlines, text(role=…), Edition, svg(), motion helpers with switch
scripts/chartlib.py      chart furniture (T6 draws, T4 moves)
scripts/data/            github.py survey.py pypi.py releases.py model.py schema.json
scripts/build_stats.py   data → validate → assets/stats.json (one write)
scripts/build_assets.py  sheet × edition → bounds → assets/v9/<sheet>-<edition>.svg
scripts/render_readme.py fills the <!-- chart:<sheet> --> and <!-- notices --> regions
scripts/check.py         XML, size, gz, elements, banned words, type floor, loops, lock diff, alt ≤25 words
scripts/preview.py       resvg → PNG stills and the social preview
scripts/perf_check.js    12's trace harness as a gate
scripts/sheets/          hero soundings approaches log instruments footer
scripts/fonts/           InstrumentSerif ×2, IBMPlexMono ×5; OFL texts only
assets/ stats.json log.json layout.lock.json           → main
assets/v9/*.svg social/*.png build-report.json          → chart branch (orphan, one commit)
```

Each sheet module exposes:

```python
NAME = "hero"; KIND = "chart"            # chart | strip | paper | edge (30)
EDITIONS = ("day","night","still-day","still-night","phone-day","phone-night")
SIZES = {"desk": (1280, 740), "phone": (720, 900)}
BREAKS = [("frame", "minute-bars", "the overture carries the only graduated neat line")]
def build(ed: Edition, data: dict, cfg: Chart) -> str
```

`Edition` (svgkit): `name`, `theme: Theme`, `motion: bool`, `scale: "desk"|"phone"`, `width`. `svgkit.svg(ed, w, h, body, defs, sheet=NAME)` prefixes every id `hero-…` (11 §10), writes an honest header (`chart v9 · built by scripts/build_assets.py · do not edit`), opaque paper in both editions (11 §1). With `ed.motion=False`, `anim/set_at/draw_in/appear/flash/loop` return the end state; `loop()` is the only way to emit `repeatCount="indefinite"` and registers itself so `check.py` can count ≤3 per page and T4's scheduler can phase-lock. Coordinates pass through `_ntos0` (integers) in sheet space; one decimal only inside glyph defs (12).

### 2.2 `chart.toml` (excerpt)

```toml
[chart]      login="BenjaminSRussell" release="v9" seed=27 breakpoint_px=767
[author]     names=["Benjamin S. Russell","BenjaminSRussell"] emails=["…"] bots=["github-actions[bot]","google-labs-jules[bot]"]
[position]   text=""                        # empty omits the slot everywhere, no placeholder
[copy]       thesis="…" role_line="…"      # [copy.review] role_line="2027-06": check.py warns past it (36)
[[notices]]  n=1 date="2025-11-08" repo="Rust-sitemap" title="…" url="…" source="pypi"
[[features]] repo="Rust-sitemap" aliases=["rustmapper"] slot="named-5" kind="vessel"
[motion]     enabled=true                   # false → every edition is a still
[budgets]    svg_kb=300 gz_kb=100 elements=3000 phone_svg_kb=120
[alt]        hero="Nautical chart of {name}'s repositories: {repo_count} features sized by commits, six named. Chart No. {repo_count}, edition {edition}."
```

`N = len(notices)` is the one source for "Corrected through Notice N" on hero, footer, alt and README. Release-derived notices are appended by `data/releases.py` from `GET /repos/{owner}/{repo}/releases` (Rust-sitemap, Scrapy), PyPI upload dates as fallback (23 F2); TOML notices are the hand-entered corrections. T8 owns the words; T1 owns the keys.

### 2.3 `assets/stats.json` schema (v2)

```json
{ "schema": 2, "updated_at": "2026-10-07T06:34:12Z", "run_id": "…", "surveyed_at": "2026-10-07",
  "sounding": {"ok": true, "stale_repos": [], "sources_failed": []},
  "since": "2024-10", "repo_count": 24, "followers": 46, "stars": 1,
  "commits": {"authored": 0, "contributions": 1828, "surveyed": 1868, "bots": 0},
  "hours_days": [24], "hours_commits": [24], "weekdays_days": [7], "busiest_hour_local": 16,
  "tz_offsets": {"-05:00": 1400, "-04:00": 400},
  "weeks": [{"start": "2025-10-06", "n": 31}],  "languages": [{"name": "Python", "share": 0.41}],
  "edition": {"project": "rustmapper", "version": "0.1.3", "date": "2025-11-08", "releases": 4, "wheels": ["cp313-macosx_11_0_arm64"]},
  "notices": [{"n": 1, "date": "…", "repo": "…", "title": "…", "url": "…", "source": "release|pypi|toml"}],
  "repos": [{"name": "Rust-sitemap", "aliases": ["rustmapper"], "slot": "named-5",
             "commits": 128, "commits_all": 131, "first": "2025-03-02", "last": "2026-10-07", "commit_days": 44,
             "active": true, "archived": false, "stale": false, "language": "Rust",
             "hours_days": [24], "weekdays_days": [7], "weeks": [52], "authors": {"ben": 128, "bots": 3, "others": 0}}] }
```

Rules: `repos` is always a list; `active` = commits in ≥3 of the last 12 weeks (32); `last` is the last *authored* commit date; `weeks` top-level comes from GraphQL, else the per-repo sum (spec-supporting A). No `seeded` key exists; `check.py` fails on it. `layout.lock.json` is `{repo: {cx, cy, r, slot}}`; `build-report.json` carries sizes, gz, element counts, warnings, `BREAKS`, loop counts, lock drift and flags (`weeks_present`, `pypi_present`, `releases_present`).

### 2.4 Editions and the `<picture>` block (emitted by `render_readme.py`)

Six entries, in this order: `(max-width: 767px) and (prefers-color-scheme: dark)` → phone-night · `(max-width: 767px)` → phone-day · `(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)` → still-night · `(prefers-reduced-motion: reduce)` → still-day · `(prefers-color-scheme: dark)` → night · `<img src=day width="100%" alt="{cfg.alt.<sheet>, ≤25 words}">`. No `height` (11 §7), no `<a>` wrapper (10 §6). Base URL `https://raw.githubusercontent.com/BenjaminSRussell/BenjaminSRussell/chart/assets/v9/`. If the sanitizer drops `max-width` or `prefers-reduced-motion`, the `dark`/`img` pair still works; if the GitHub app ignores `<picture>`, the hero's `<img>` fallback becomes the phone edition (10 idea 4), decided by T10's verification.

### 2.5 The Actions job (`profile.yml` rewritten; `snake.yml` deleted)

Triggers: `schedule "20 6 * * *"`, `workflow_dispatch` (input `dry_run`), `push` to main on `scripts/**`, `chart.toml`, `assets/log.json`, and `repository_dispatch: release-published`. `concurrency: {group: chart, cancel-in-progress: true}`, `permissions: contents: write`, `timeout-minutes: 15`, Python 3.12 with pip cache, `pip install -r scripts/requirements.txt` (`fonttools==4.56.0`, `jsonschema==4.23.0`). Steps: (1) `build_stats.py` fetch → model → validate → write; (2) `build_assets.py` then `render_readme.py`; (3) `check.py` gate; (4) `git pull --rebase`, commit `stats.json`/`layout.lock.json`/`README.md` only if changed; (5) publish: orphan worktree `chart`, add `assets/v9`, `social`, `build-report.json`, one commit `chart: soundings {date}`, `push --force`; (6) `if: failure() && steps.stats.outcome == 'failure'`: `build_assets.py --no-sounding` → `check.py` → publish with the dated pencil note; (7) `if: failure()` after the gate: no publish, job red. A second workflow `perf.yml` runs `perf_check.js` and the filmstrip on `scripts/**` pushes and Sundays.

`resvg` is downloaded once per run as a pinned release with a sha256 check. The `repository_dispatch` comes from rustmapper's future `release.yml` (23: the release is the redraw). Failure modes: GraphQL down → cache + `sounding.sources_failed`; PyPI down → previous `edition`; clone timeout (60 s, 6 in parallel) → `stale: true`, yesterday's record; schema invalid → heartbeat edition; XML/size/bounds/banned word → nothing published, red job; push race → rebase, one retry. Kill switches: `[motion] enabled=false`, `MOTION=off` for local runs, `dry_run`, and deleting the `chart` branch ref (the loudest switch; in the runbook).

### 2.6 Budgets (enforced by `check.py`, binding on all sheets)

Per SVG: ≤300 KB raw (hard), ≤100 KB gzipped, ≤3000 elements; hero target 230 KB / 70 KB gz. Phone SVG ≤120 KB raw; phone page ≤150 KB on the wire; one desktop edition set ≤250 KB gz. Motion (12): frozen sheets 0 repaints; lights-only sheets ≤2 repaints/s; footer the only ambient loop at ≤4 ms/frame; ≤3 indefinite loops per page. Type: semantic text ≥13 px at 1280 and ≥26 px at 720 (10 F1); texture ≥11/18. Build: full job <6 min; `main` stays <5 MB excluding fonts.

### 2.7 LICENSE and social preview

Root `LICENSE` = MIT (code). `LICENSE-ASSETS.md` = CC BY 4.0 for `assets/`, `chart.toml` copy and README prose, with the OFL reserved-name note. Delete Inter and DejaVu files and license texts. `preview.py --social` renders `hero.build(Edition("still-day"), …, crop=(0,50,1280,640))` to `social/hero-day.png` and `-night.png` at 1280×640 (<1 MB) and writes both to the `chart` branch; GitHub has no API for the social preview, so Ben uploads once per design release and `check.py` warns when the PNG's hash differs from the one recorded in `chart.toml` (35 idea 4).

## 3. Interfaces

**Provide**
- `tokens.Theme` with `edition` field; `tokens.INK/WIDTH/DASH/ROLE` containers (values owned by T5/T6; T1 owns the container, generation and the no-hex lint).
- `svgkit.Edition`, `svgkit.svg(ed, w, h, body, defs, sheet)`, `svgkit.loop(...)` as the only indefinite-animation emitter; `ed.motion=False` end-state contract for T4's helpers.
- Sheet module contract (§2.1) for T2, T3, T9; `cfg` = parsed `chart.toml`; `data` = schema-v2 dict.
- `stats.json` keys (§2.3) for T7 (derivations read `commits.authored`, `hours_days`, `weeks`, `edition`, `notices`, `repo_count`, `updated_at`, `surveyed_at`, `sounding.ok`).
- `render_readme.py` markers `<!-- chart:<sheet> -->…<!-- /chart -->`, `<!-- notices:start/end -->`, `<!-- position -->` for T8; alt templates in `[alt]`.
- `build-report.json` and `check.py` plug-in list for T10; `perf_check.js` schedule.
- Edition file names `<sheet>-<day|night|still-day|still-night|phone-day|phone-night>.svg` under `chart/assets/v9/`.

**Need**
- T4: every helper honours `ed.motion`; timing ids namespaced `<sheet>-…`; a `choreography` table per sheet that `check.py` can read for loop count and longest period.
- T5: `ROLE` names and sizes (desk and phone); `text(role=…)` replaces raw sizes; rendered-size check rule.
- T6: `WIDTH/DASH/INK` values day and night; integer-coordinate path emitters.
- T7: `derive(data, cfg) -> dict` (chart number, variation line, edition line, dateline, `N`), and the `--no-sounding` pencil-note text.
- T8: README template with markers; `[copy]` keys; bio text; LICENSE colophon line.
- T9: `log.json` schema (`measured` flag, heartbeat line) and the instruments plain-text mirror.
- T10: the gate list `check.py` must implement, scratch-repo results for `max-width`, `prefers-reduced-motion` and the GitHub app.

## 4. Build order, effort, risks, omissions

0. **Stop the bleeding (2 h):** delete `snake.yml` and the `output` branch; `check=True`; non-zero exits; `requirements.txt` pinned; `concurrency`; `pull --rebase`. Ship.
1. **Data (8 h):** `data/` package, author filter, iso-strict offsets, parallel clones with `stale`, releases, schema, one write; `layout.lock.json`; `chart.toml` loader.
2. **Kit (8 h):** `tokens.py` + `--md`; `Edition`, id prefixing, integer coords, motion switch, `loop()` registry; delete legacy themes/fonts.
3. **Gate (5 h):** `check.py`, `preview.py`, `render_readme.py`; LICENSE files.
4. **Sheets (T2/T3/T9, parallel) on the contract; hero first.**
5. **Job (5 h):** new `profile.yml`, orphan publish, heartbeat path, `repository_dispatch`, social PNG; perf workflow.
6. **Verify (T10, 4 h of mine):** scratch repo, four theme combinations, app; DESIGN.md generated; runbook.

T1 total ≈ 32 h plus review. Risks: the sanitizer dropping undocumented media values (harmless fallback, tested before launch); a cancelled run between the `main` commit and the `chart` push (publish is one force-push; the next run republishes); the orphan branch confusing a forker (runbook). Left out: weekly survey cadence, repo-header PNGs (28), a "Chart No. 1 symbols" sheet (30; v9.1), PRs instead of direct commits.

## 5. Repo hygiene tasks for Ben (not pipeline work)

1. Bio: replace "Scraping enthusiast and full stack developer" with T8's position line; set the hireable/location fields he is willing to state.
2. Rust-sitemap: add `LICENSE` (MIT, as pyproject declares); tag `v0.1.3` at the published commit and create a Release; set description and topics; reconcile the worker count from `governor.rs` (defaults 256–1024) across page, PyPI summary and README; add `release.yml` with `maturin-action`, abi3 wheel matrix, and a `repository_dispatch` to this repo; then cut 0.2.0; rename to `rustmapper` after `chart.toml` aliases land (23, 19).
3. Scrapy: make the coverage claim true or drop it (`fail_under` to the measured value, CI `--cov-fail-under` ≥ that); move the 930 self-filed issues to a Project; populate `bug` and `good first issue` (20, 23).
4. Archive the four "Also" repos so "below the waterline" is checkable; they become `Wk` marks for free (23 F8).
5. Fill `[position].text`, upload the social preview PNG, and create the scratch repo for T10's sanitizer test.

## 6. Acceptance criteria

- `python3 scripts/build_assets.py && python3 scripts/check.py` exits 0 locally with no token, from the committed cache, and produces 36 SVGs (6 sheets × 6 editions) in <60 s.
- `grep -c 'seeded\|ILLUSTRATIVE\|PENDING' assets/stats.json assets/v9/*.svg` → 0; `grep -rE '#[0-9A-Fa-f]{6}' scripts/sheets/` → 0.
- Changing one repo's `commits` in `stats.json` changes that feature's radius and only that feature (lock diff reports one line).
- Renaming `Rust-sitemap` → `rustmapper` with the alias in `chart.toml` produces byte-identical hero SVGs; a missing sheet module or a bounds warning makes the job red and the `chart` branch unchanged.
- A bad token publishes sheets whose only diff is the pencil note and dashed datum rule.
- Two identical runs produce identical bytes; `main` gains at most one commit per day of ≤10 KB.
- Every `<picture>` has six sources in the §2.4 order; `img.currentSrc` at 360/767/768/1280 px × light/dark × reduce on/off selects the expected file in Chromium, Firefox and WebKit.
- `LICENSE` and `LICENSE-ASSETS.md` present; `scripts/fonts/` holds only OFL files; `snake.yml` and `output` gone.
- `DESIGN.md` tables are byte-identical to `python3 scripts/tokens.py --md` output.
