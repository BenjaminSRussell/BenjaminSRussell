# T10 — QA & verification

## 1. Decisions

1. **One checker, three tiers.** `scripts/check.py` runs `fast` (pure Python, ~5 s), `render` (Playwright, ~15 s) and `perf` (trace, ~40 s); local default = fast+render, `--ci` = all, `--release` adds OCR, engines and GitHub checks. Per 36, 12, 11.
2. **Checks read artefacts plus a sidecar, never the Python.** The build writes `assets/build-report.json` (text runs with role/tier/truth/key, exclusion boxes, symbol ids, motion class, features); the SVG carries no extra bytes. Type is outlines, so *STANDARDS 1 is amended: grep the text manifest, README.md and chart.toml*, not the SVGs.
3. **Still frames by `setCurrentTime`, not wall clock.** `filmstrip.mjs` waits up to 95 s per frame; the checker inlines each sheet and calls `pauseAnimations(); setCurrentTime(t)`. Per 12, 11.
4. **"Finished sheet" is quantified:** ink coverage (non-paper pixels) ≥ 95 % of the frozen end state at every sampled time; only the hero may build during its opening (≥ 60 % at t = 0, rising). Per 05, 29 and the binding fact that other sheets are finished at t = 0.
5. **Perf thresholds are 12's, verbatim:** frozen sheets 0 repaints; lights-only ≤ 2 repaints/s; footer the only ambient loop at ≤ 4 ms/frame; nothing > 8 ms/frame while moving after its opening; a 360 px DPR 3 run. 10's battery proxy is the same gate.
6. **OCR gates releases, not nights:** tesseract on italic serif at 12 CSS px is noisy; the deterministic rendered-size lint (07) gates nightly.
7. **Phone floors follow 10 (26 px semantic, 18 texture in 720-space)** over 07's 18, because 10 measured GitHub's gutters (scale 0.455); the lint reads floors from `tokens.py`.
8. **Alt ≤ 25 words, plain register** (09). *Amends STANDARDS 12*: alt is a replacement; voice moves to the visible `<sub>` caption (T8). The poem (24) prints from the alts' last sentences.
9. **`seeded: true` fails the build**; `--dev` permits it locally and the build sets every figure italic (T7). Per 34.
10. **Colour is checked twice:** from `tokens.py` (WCAG, APCA, Machado deutan/protan ΔE_ok ≥ .06) and from sampled pixels of the 870 render (hatch ΔL ≥ .04, lights > text), because antialiasing decides the real colour. Per 15, 09.
11. **Golden fixtures at 1 % pixel tolerance** (30) plus byte determinism, so a no-change day makes no commit (36, 11).
12. **Masterpiece = automated floor + scored rubric** (≥ 30/36, no zero, thesis criteria ≥ 2) + 29's five-second criteria, run on one scratch repo that is both 11's staging repo and 29's shadow profile.

## 2. `scripts/check.py`

```
check.py [--ci] [--release] [--dev] [--only hero,footer]
exit 0 pass · 1 fail · 2 pass with warnings (CI commits, posts summary) · 3 could not check (CI fails)
```
Cheapest first; the render tier does not start if the fast tier failed.

| # | Check | Rule (fail unless noted) | Per |
|---|---|---|---|
| 1 | Report ↔ SVG | report sha256 matches each SVG and `stats.json` | 36 |
| 2 | XML | lxml parses; no `<text> <script> <style>` or external href; ids unique, sheet-prefixed, every `<use href>` resolves; `values`/`keyTimes` lengths equal; freeze fade-ins have base `opacity="0"` | 11 |
| 3 | Size | raw ≤ 300 KB, gzip ≤ 100 KB, phone ≤ 120 KB raw; page ≤ 250 KB gz per edition | 11, 10 |
| 4 | Counts & motion | elements ≤ 3000; no `animateMotion`; no indefinite animate on geometry attributes; no filter or `patternTransform` under an animated ancestor; loops match `motion.class` (frozen 0, lights = discrete opacity, ambient = footer only); strokes ≥ 0.8, semantic ≥ 0.9, texture 0.6 only at opacity ≥ .25 | 12, 11, 15 |
| 5 | Bounds & collisions | text box (x0, y−0.75·size, x1, y) inside the safe area unless named in `breaks`; no semantic box overlaps a text or exclusion box (rose ring + letters, cartouche, insets, legend, title blocks); texture boxes ≥ 28 px apart and outside exclusions (build culls, checker verifies) | 33, 28 |
| 6 | Banned strings | case-insensitive over manifest + README + chart.toml: ILLUSTRATIVE, PENDING, SEEDED, NOT FOR NAVIGATION, Here be dragons, Fair winds, thanks for reading, that's a mood, Hi I'm Ben, drawn not templated, REFRESHED DAILY, works at night, lorem, TODO, FIXME, v7, `<!-- POSITION` | STD 1, 13, 25, 32, 36 |
| 7 | Type | size ∈ `SCALE`, role ∈ `ROLES`; rendered size (×0.68 desk, ×0.455 phone) ≥ 9 px unless texture; 11 px only as texture; caps tracking ≤ 0.9 at ≤ 13 px; `scan` runs ≥ 22 px in the F-path (top 25 % or left 40 %); ≥ 4 sizes per sheet; a rotated note on the hero | 07, 30, 33, 29 |
| 8 | Contrast (tokens) | text ≥ 4.5:1 (< 24 px) / 3:1 on paper and land; APCA Lc ≥ 75 at ≤ 13 px; coastline, index contour, danger line ≥ 3:1; semantic pairs ΔE_ok ≥ .06 under normal, deutan, protan; red/green L gap ≥ .06 day, ≥ .10 night | 09, 15 |
| 9 | Lights > text | night: max L of `lights[].color` > max L of any text fill | 15 |
| 10 | Legend diff | every legend id ∈ some sheet's `symbols_used`; every symbol on hero/approaches/footer has a legend row (allow-list: boat, serpent); the upright/italic row exists | 30, 09 |
| 11 | Alt & plain twin | each alt ≤ 25 words, first word not "The", last sentence ≤ 10 words; every H2 has `<sub>`; a plain paragraph within 3 lines of each `<picture>`; poem printed to stdout and `report.poem` | 09, 24, 29 |
| 12 | Position | `<!-- POSITION` → fail; `chart.toml position=""` → warning, slot omitted everywhere; non-empty → README visible line equals cartouche string | 29, 18, 36 |
| 13 | Seeded | `stats.seeded` → fail unless `--dev` | 34 |
| 14 | Data consistency | every measured run has a `key` and `format(stats[key]) == s`; one key prints one string across sheets, alts and README markers `<!-- n:key -->…<!-- /n -->`; `hours_basis == "author-local commit-days"`; area follows `area_law` ± 8 %; features ≤ 32, names ≤ 18 chars; both commit totals shown when they differ | 34, 08, 32, 30 |
| 15 | Flash | each indefinite opacity loop ≤ 3 lit transitions/s, bbox ≤ 2 % of sheet; characters parse via `flash()` | 09 |
| 16 | Expiry | `review=` dates past today → warning | 36 |
| 17 | Still frames (render) | t ∈ {0, 0.5, opening_end+0.1, 0.25L, 0.5L, 0.75L, 0.99L, 600 s}, L = `longest_loop_s`; rule 4; writes `out/check/filmstrip-*.png` | 05, 12 |
| 18 | Silhouettes (render) | frozen state at 128 px → grey → threshold → 16×8 mass grid; pairwise L1 ≥ 0.25; ≤ 1 sheet with heaviest cell top-left; contact sheet written | 33 |
| 19 | 360 renders (render) | phone editions at 360 CSS px DPR 3, both schemes; pixel sampling for hatch ΔL, tint vs land, night semantic ink L ≥ .82; OCR when tesseract present (required by `--release`): name, thesis, Scrapy, rustmapper, one light character, one shoal at match ≥ 0.8; semantic recall ≥ 0.9 | 10, 15, STD 5 |
| 20 | Repaint budget (perf) | `perf_check.js`: warm `opening_end+0.5 s`, trace 3 s; light edition for frozen/lights sheets, both for hero and footer, hero-phone at 360/DPR 3; thresholds per decision 5 | 12, 10 |
| 21 | Source matrix (`--ci`) | preview page at 360/390/412/600/767/768/1024/1280 × DPR 1,3 × scheme × reduced-motion; `img.currentSrc` equals the file expected by source order (phone+dark, phone, reduce+dark, reduce, dark, img) | 10, 09 |

Runtime: fast ≤ 5 s, render ≤ 15 s (one browser, page reuse), perf ≈ 40 s (five sheets × 3.5 s, hero 2 × 8 s, phone 8 s); `--ci` ≈ 60 s. If the first run overshoots, trim trace length before coverage.

**Report schema** (written by `build_assets.py`, owned here):

```json
{"built":"2026-10-07T06:34Z","stats_sha":"…","poem":["…"],
 "sheets":{"hero-light":{"svg":"assets/hero-light.svg","sha256":"…","w":1280,"h":740,"form":"desk|phone|still",
  "text":[{"s":"Ben Russell","x0":72,"x1":690,"y":210,"size":176,"font":"serif","slant":"upright",
           "role":"display","tier":"scan|semantic|texture","truth":"measured|illustrative|null","key":"commits|null","rot":0}],
  "exclusions":[{"name":"rose","x":0,"y":0,"w":0,"h":0}],
  "breaks":[["frame","minute-bars","the hero is the one full chart"]],
  "symbols_used":["can","nun","light","danger","wreck","anchorage","track"],
  "legend":["can","nun","light","sector","danger","wreck","anchorage","track","numerals"],
  "lights":[{"id":"h-r2","character":"Fl R 4s","color":"#FF6853","bbox":[808,470,10,18]}],
  "motion":{"class":"opening+lights|frozen|lights|ambient","opening_end_s":4.0,"longest_loop_s":96,"loops":["h-sail","h-r2","h-g1"]},
  "features":[{"name":"game_engine","commits":585,"area_px":4120,"cx":0,"cy":0}],"area_law":"area∝commits"}}}
```

**Regression harness.** `tests/` (pytest, before the build in `--ci`): fixtures `stats-golden.json` (today's real data, `seeded:false`), `stats-stress.json` (40 repos, 9,999 commits, 30-character names, no `weeks`, no `pypi`), `stats-rename.json` (Rust-sitemap → rustmapper alias; `layout.lock.json` centres move ≤ 40 px), `stats-noweeks.json` (italic fallback, no placeholder). Per fixture × sheet × edition: build twice → identical bytes; frozen render at 435 px vs `tests/golden/*.png`, ≤ 1 % pixels with ΔE_ok > .02; `make golden` re-blesses with a reason. Unit tests: `flash()` on every character in `lights[]`, course sampling lengths, area law, author-local hour binning, number formatter, box collision, Machado matrices on a known pair. STANDARDS 2 test: +50 commits on one repo → the hero differs and that feature's `area_px` grows.

## 3. GitHub post-merge verification

1. **Sanitizer:** `gh api /markdown -f mode=gfm -F text=@README.md > out/gh.html`; six `<source media>` per picture, `<sub>` in H2, `<details>`, `<a name>` anchors survive; diff against the previous run. Local only (needs auth).
2. **Shadow profile:** push candidate README + assets to the scratch repo; `render.mjs shadow` screenshots the live profile at 870 and 360, OS light and dark; a logged-in test account checks the two mismatched GitHub-theme combinations quarterly (11).
3. **Live DOM:** no `loading="lazy"` on README images (re-verify quarterly); whether `<picture>` is `<a>`-wrapped; `currentSrc` at 360 is the phone edition.
4. **Camo and cache:** `curl -sI` each camo URL → `image/svg+xml`, gzip; ETag turns over within 10 min; no `?v=`.
5. **Real devices (release):** iOS Safari (Low Power on/off), Chrome Android, both GitHub apps: phone edition selected, dark follows OS, pinch-zoom crisp, no link wrap, lights flash, hero opening plays once.
6. **Social preview** 1200×630 from the hero (35), checked at 600 px.
7. **Browser matrix** (`--release`; Playwright chromium, webkit, firefox): still-frame ink coverage within 3 %, boat position at t = 10 s within 6 px, lights flash in all three, identical source selection; Firefox's t = 0 frame is read after a 1 s settle because its clock starts at load.

## 4. Acceptance test for "masterpiece"

**Floor (automated):** `check.py --ci` exit 0, or 2 with only position/expiry warnings; regression suite green; post-merge steps 1–4 clean.

**Judged** (two reviewers new to the page plus Ben; median; 0–3 each):

| # | Criterion | From |
|---|---|---|
| J1 | Thesis read in one line, said once | 24, STD |
| J2 | Cover the name: the hero picture alone argues the survey edge | 28 |
| J3 | Cover the titles: a stranger names every sheet by silhouette | 33, STD 6 |
| J4 | A hydrographer names region, unit and datum from the sheet | STD 4, 13, 26 |
| J5 | Point at any mark: one sentence says its job, and it reads on a phone | 33 |
| J6 | Change a number in stats.json → the chart visibly changes | 06, STD 2 |
| J7 | Honesty: both commit instruments, unit per sheet, no invented geometry or unsupported claim | 34, 19, 20 |
| J8 | Motion reads as the chart surveying itself; every still is finished | 05, 12 |
| J9 | Copy says each thing once; no borrowed jokes; glossed headings | 04, 24, 25, 29 |
| J10 | Recruiter finds field, systems, languages, contact in plain text within 60 s | 03, 18, 29 |
| J11 | Night is designed, not inverted: lights are the brightest things | 15, 27 |
| J12 | ≥ 4 uncaptioned second-look layers, each making the first reading truer | STD 13, 33 |

**Pass:** ≥ 30/36, no zero, J1/J2/J7/J10 each ≥ 2, **and** 29's five-second test on the shadow profile (3 cohorts × 10; 870 px day, repeated at 360 and night): ≥ 80 % name the field, ≥ 60 % recall the name, ≤ 10 % call him a Scrapy maintainer, ≥ 80 % read name and thesis at 360, glossed headings ≥ 1.5/2. The thesis A/B (plain vs "wrong about itself") runs in the same session and decides the hero line.

## 5. Review checklist for every change (PR template)

1. `check.py` exit 0 locally, summary pasted. 2. Which `chart.toml`/`tokens.py` key changed; no hex or raw size in `sheets/`. 3. Every printed number has a `key` or is italic. 4. New symbol → legend row → defs id. 5. New motion: class declared, no geometry attribute, no filter, loop on the 10/24/48/96 grid, base opacity 0. 6. New text: role, tier, rendered ≥ 9 px, collision-free. 7. Alt ≤ 25 words; poem re-read. 8. Filmstrip and contact sheet attached. 9. Golden re-blessed only with a reason. 10. No banned phrase, "chart" ≤ 7 times, no explained trick. 11. `scripts/**` changed → `--release` matrix. 12. README changed → `gh api /markdown` diff.

## 6. CI vs local

| Where | What |
|---|---|
| Nightly job (T1) | pytest → build → `check.py --ci` → commit only on exit 0/2; artefacts: report, filmstrips, contact sheet, perf JSON; summary lists warnings |
| Push to `scripts/**` | plus `--release` engine matrix and golden diff |
| Local default | `check.py` ≈ 20 s; `make preview` regenerates crit PNGs |
| Local, manual | `gh api /markdown`, shadow push, OCR, real devices, five-second test |
| Quarterly | lazy-load and `<a>`-wrap DOM check, four theme combinations, cache headers |

## Interfaces

**Provide:** `scripts/check.py`; `scripts/perf_check.js` (from `scratchpad/perf/harness.js`; `--warm --trace --width --dpr --json`); `scripts/render.mjs` with subcommands `frames | silhouette | phone | matrix | shadow`, replacing the five tools in `scratchpad/tools/`; `tests/` fixtures, goldens, unit tests; `.github/PULL_REQUEST_TEMPLATE.md`; the `build-report.json` schema.

**Need:** **T1** — workflow runs pytest and `check.py --ci` before `git add`, uploads `out/check/*`, installs Playwright (webkit/firefox on `scripts/**`) and `tesseract-ocr`; `chart.toml` keys `position`, `review`; scratch repo name; orphan-branch URL. **T4** — `motion` block per sheet (`class`, `opening_end_s`, `longest_loop_s`, loop ids); `flash()` as the one character parser; no `animateMotion`. **T5** — `tokens.SCALE`, `ROLES`, floors (13 desk, 26/18 phone), tracking caps; every `text()` tagged `role`, `tier`, `truth`, `key`. **T6** — `k.exclude(name,x,y,w,h)` for rose, cartouche, insets, legend, title blocks; `BREAKS`; stroke floors in tokens; the 28 px cull in the build. **T7** — figures keyed to stats paths, one formatter, `hours_basis`, `area_law`, italic under `--dev`, both commit totals. **T8** — `<!-- n:key -->` markers, visible position line, `<sub>` on every H2, alt ≤ 25 words, plain paragraph after each picture. **T2/T3** — `symbols_used`, `legend`, `lights[]`, the pictorial allow-list. **T9** — `log.json.measured`; the footer as the one `ambient` sheet.

## Build order, effort, risks, left out

Report schema in svgkit/build 3 h → fast tier 6 h → render tier 6 h → `perf_check.js` 3 h → fixtures and goldens 4 h → matrix and shadow script 3 h → PR template and CI wiring 2 h → OCR and engine matrix 3 h. ≈ 30 h.

Risks: inline SVG id collisions (per-sheet prefixes, one page per sheet); trace timings vary ±20 % on shared runners (2× headroom; perf fails only on two consecutive runs); tesseract absent in this sandbox (verified), apt-installed in CI; the sanitizer check needs `gh` auth and stays local.

Left out: pixel-perfect goldens; judging "finished" beyond ink coverage; WebKit/Gecko traces (Chromium gates, others compared by frames); anything needing a logged-in GitHub session in CI.

## Acceptance criteria (T10)

- `check.py --ci` on the golden fixture exits 0 in ≤ 60 s on ubuntu-latest; local run ≤ 25 s.
- Each injected fault yields exit 1 naming its check: 0.5 px semantic stroke; `animateMotion`; 12 px label; sounding inside the rose box; "PENDING" in a manifest string; 26-word alt; `seeded:true`; chart numbers differing between sheets; 4 Hz flash; legend id with no symbol; hero loop over 8 ms/frame.
- Filmstrips at the eight times are CI artefacts; every frame passes the coverage rule; contact sheet shows pairwise distance ≥ 0.25.
- Source matrix: 64 contexts, 100 % expected `currentSrc`.
- Two builds from one stats file are byte-identical; a no-change day makes no commit.
- Rubric and five-second results recorded in `tech/acceptance.md` before the page is called shipped.
