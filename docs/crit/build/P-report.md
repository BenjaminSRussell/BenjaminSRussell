# Builder P report — T3 Approaches sheet (`scripts/sheets/approaches.py`, `tests/test_approaches.py`)

No git commands run. Files written, both inside my ownership: `scripts/sheets/approaches.py` (≈ 900 lines) and
`tests/test_approaches.py` (16 tests, all green). Built into the scratch dir and then into `assets/v9/` (the six
`approaches-*.svg`); the six entries were merged into `assets/build-report.json` without touching H's hero entries
(the runner would otherwise have overwritten the shared report with my sheets alone). No engine file edited.

## 1. What was built

A north-up harbour chart, 1280 × 960 (phone 720 × 1240), one `Field` for the water, every glyph through typeset,
every `<animate*>`/`<set>` through `ctx.tl`, no raw `<text>`, no `<pattern>`, no filter, no `animateMotion`.

- **Geography.** Land west (ten land kernels, two entrance points, two carve kernels for the basin: the basin is the
  deepest water on the sheet, ≈ 52, so "the raw basin is deepest" holds in the field itself). A per-side `_Coast`
  subclass closes the west coast under the 14 px margin (inset 6) and fades the field to base across x 1080–1150.
  Illustrative bathymetry: a shelf deepening with distance from the shore (2.5 + 0.05 px⁻¹), a +5 fairway along the
  course, a shallower bank north of the channel; 61 samples on a jittered 96 × 92 grid, sounding-kernel support
  110 px so they blend (the default 30 px made each sample its own pond). Base 26 (never on a level). Contours 2 · 5 ·
  10 (index) · 20, tints B under 5 / A under 10, coastline with swell by day, coast vignette (step 8), danger line
  on the *429 Shoal* (r 26, clamps at depth 2), APPROX dash within 40 px of the unsurveyed fade, figures in breaks
  (role `contour-figure`), 55 culled italic soundings in the water + 42 on the survey lines + 8 on the vessel's line.
- **Channel.** W0 (600,672) → W1 → W2 → W3 → W4 (236,471) → ANCH (150,440); W1…ANCH are exactly collinear on 290°
  true (decision 1), so the leading line (solid from the front mark to W3, PECK beyond to W1) carries the inner
  legs and their ⊙ waypoints, and COURSE dots run only on the 318° outer leg. Region B returning: G "1" URLS and
  G "3" ANALYZE (cans) south of their legs, R "2" SCOUT and R "4" SUMMARIZE (nuns) north, each via `lateral_offset`
  (…, 24); lit cores through `lit_core` (halo r 14 at night) with the group's opacity on `ctx.tl.flash("Fl G 4s",
  begin 0)` / `("Fl R 4s", begin 2)`; labels italic (floating things slope, chartlib `LETTERING`); "Health Ldg Lts
  290°" and "318°" bearings; Ldg triangles astern of the anchorage; anchor ×1.3 and *Delta Lake*.
- **Grafana Lt** on the headland: `use("light")` + horn + a core flashing `Fl 15s` (15 = the real prometheus.yml
  interval per T8; `claims.scrape_interval.value` is read first and must be ∈ LOOP_PERIODS, else `F`); label
  upright "Grafana Lt · Fl 15s", "Horn" beneath; two static hairline rays toward the channel at night.
- **Survey ground** (680,120,400,570): one TRACK line per shard (`log.json.profile.shards` = 8), lines and the three
  check lines stop 6 px short of the robots.txt restricted area (`restricted_line`, teeth inward, label upright);
  caption "one shard per core · *8* here" with the figure italic until `log.measured`; Rep ring (zone A) with the
  pencil note "sitemap says yes; the lead says no" (serif-italic 17, muted, −6°, hairline leader), ED islet (zone B),
  SD beside a sounding (zone C); limit of survey as a wavering LIMIT polyline at x≈1096 with boxed A/B/C zone letters
  on it; UNSURVEYED hatch (ramped in) running to the sheet edge where the neat line is broken (y 300–324, 560–584).
- **Proposed channel** from the west end of the last track line to W0: PECK hairline, two hollow outline marks,
  "proposed · unlit" italic; legend row "Proposed channel · unlit". Nothing lit, nothing numbered.
- **Panels.** Open centred title block ("SHEET 3" / *Approaches to Scrapy Harbor* serif 28 / "Surveyed by rustmapper
  2026 · Datum: main"); ZOC cartouche (source_diagram with three hatched bands + table from `stats.sources` +
  "A: as declared by the site. B, C: as found."); harbour inset "INSET · THE HARBOUR WORKS" with the three Delta
  tables as basins (outer stage1_discovery untinted = deepest, inner tint A, dock tint B), illustrative soundings
  24₄ · 8₂ · 4₁ (upright from `stats.trial.tables[].rows` when a run is exported — tested), anchor, *Delta Lake*,
  Prometheus mast, PostgreSQL tanks, Grafana Lt tower whose lantern flashes on the main light's character, Redis
  twin tanks with the Traffic Sig beside them, Summarization Wks shed, Ldg triangles; rustmapper block (title,
  "PyPI 0.1.3 · alpha · 2025-11-08" upright from `stats.edition`, five verified notes with *256–1024* and *250 ms*
  italic, WAL tape of (n−1)·6+8 cells of which the last eight `<set>` on the fixes); Scrapy Harbor block (title,
  "Python · edition main · 265 commits" upright, six verified notes).
- **THE LEGEND** (360,702,560,232): header "SYMBOLS · CHART NO. 21 · EVERY SHEET", the convention line "upright
  figures are measured · sloping figures are not · underlined: above datum", three columns × 12 rows; every one of
  chartlib's 18 symbol ids appears as a `<use>` of the sheet's own def (can, nun, light, flare, halo, ldg, traffic,
  horn, anchorage, wreck, waypoint, sloop, sloop-glyph, fix, station, correction, rep, ed) plus the lamp states
  (go · stop · one at a time), SD, PA, boxed zone letter, bearing, the spot-height example **265₅** (Scrapy's real
  commits and months, upright), course, proposed channel, danger line, tints, contour, approximate, restricted,
  track, check, hatch, limit, and the sounding example *4₂*. `symbols_used ⊆ legend` on every edition (tested);
  legend == `symbol_ids()` so the hero/footer `<use>` diff is empty whatever H and S use.
- **Motion** (desk motion editions only; phones frozen): 6 lights (`lt-g1 lt-g3` begin 0, `lt-r2 lt-r4` begin 2,
  `lt-grafana`, `lt-grafana-inset` Fl 15s) + packet boat `ctx.tl.fixes(7 fixes, every 4, hold 72)` on the smoothed
  course (lies 14 px short of her anchor) + survey vessel `fixes(8, begin 28, every 2)` east → west on the last
  track line with sounding k and WAL cell k `ctx.tl.reveal(…, 28 + 2k)`. `Timeline.report()`: class lights,
  8 indefinite, 1.094 repaints/s, loops {4, 15, 96}, no continuous window, no violations. Still edition = same code
  path with `motion=False`.
- **Phone** 720 × 1240: `P(x, y) → (20 + (y−20)·s, 20 + (1260−x)·s)`, s = 1200/1240 — the chart rotated 90°
  anticlockwise so the channel runs down the screen; the field is rebuilt in phone space from the mapped kernels; a
  north arrow pointing left; neat-line rules 26/31 (the 26 px folio needs the margin); title cartouche over the
  hatch; kept: SCRAPY HARBOR, Delta Lake, 429 Shoal, four marks with 'G "1"'… labels on the correct side after the
  rotation, Grafana Lt, Ldg 290°, LIMIT OF SURVEY 2026, UNSURVEYED, zone letters, robots.txt, Rep/ED/SD, Wk ’25,
  14 soundings (texture-italic 18), both vessels static. Cut: inset, ZOC, blocks, legend, note, check lines.
- **Build-report hook** fills `symbols_used`, `legend`, `lights[]` and an `approaches{shards, soundings, field}`
  block; registered on both `build_assets.report_hooks` and `__main__.report_hooks` (the sheet imports
  `build_assets` while the runner is `__main__`, so the two lists differ).

## 2. T3 §10 acceptance criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | No `512 / ILLUSTRATIVE / PENDING / SEEDED / 90%`; upright figures only chart number, PyPI version/date, Scrapy commits, `Fl {s}s`, run-backed basin rows | **pass** | `checks/strings.scan` clean on the six SVGs and the text manifests (`test_no_banned_strings_no_512_no_coverage`); measured runs in the report: `PyPI 0.1.3 · alpha · 2025-11-08` (edition), `265` (scrapy_commits), `265₅` (legend example), `21` (chart-number); the only upright sounding on the sheet is that example (`test_upright_figures_are_the_measured_ones`); shards `8` italic with `truth=illustrative` |
| 2 | Legend `<use>` ↔ sheet ids; no string overflows its cartouche | **pass** | `test_legend_defines_every_symbol_and_covers_every_use`: legend == all 18 `symbol_ids("c")`, used ⊆ legend, each id defined once; every panel string carries `within=` and `check_type` is clean (the build's only problems are the glyph budget, §4); `fit()` raises at build time if a legend/notes string exceeds its cell |
| 3 | Odd greens south, even reds north of a 270–310° channel; Ldg bearing = final leg; chart-number position matches | **pass** | `test_region_b_buoyage_on_a_290_leading_line` (legs 318°, 290°, 290°, 290°; cans y > leg, nuns y < leg; bearing W1→marks = 290.0 ± 1); `test_chart_number_position_matches_the_series`: `21` anchor-end at (1262,14), folio at (24,955) |
| 4 | After 42 s: ≤ 2 repaints/s, 0 with lights/boat stripped; no animateMotion/geometry/filter; raw < 300 KB | **pass / see §4 perf** | `perf_check --warm=44 --seconds=10`: day 1.3/s, night 1.2/s; stills and phones 0 repaints; `checks/motion.py` 0 findings on the six files; `--static` is 0 by construction (no `<animate*>` left). Raw 262–264 KB. The harness also prints "58–63 ms/frame (cap 8)" — the evaluator applies 12's *continuous-motion* cap to discrete repaints; see §4.3 |
| 5 | Filmstrip frames finished; still = end state | **pass** | `render.mjs frames` at 0, 0.5, 4.1, 24, 28.1, 36, 42.1, 48, 72, 95, 600 vs the still: coverage 0.996–1.000, changed-pixel fraction ≤ 0.17 %, no blank ledger; stills contain zero `<animate*>`/`<set>` (`test_stills_and_phones_carry_no_animation`) |
| 6 | Phone at 360 px: SCRAPY HARBOR, Delta Lake, UNSURVEYED, four mark numbers, Grafana Lt readable; nothing under 18 px | **pass (by eye + lint)** | `phone360.png` (DPR 3) inspected: all legible; `test_phone_floors_and_kept_names`: every run ≥ 18, semantic ≥ 26, all the names present; no OCR run (tesseract not in this session) |
| 7 | `scrape_interval`, `log.shards`, `stats.trial` change the light character, track-line count, basin soundings | **pass** | `test_scrape_interval_changes_the_light_character` (value 10 → "Grafana Lt · Fl 10s", `dur="10s"`, figure upright when measured), `test_shards_change_the_track_lines_and_the_tape` (12 shards → 12 lines, 74 WAL cells, "12" italic → upright with `measured`), `test_a_trial_export_makes_the_basin_soundings_upright` (12,345 rows → `12₃` upright) |

Other gates: `python3 scripts/check.py --dev --tier fast --only approaches` → 0 fail (warnings: SIZE-TARGET ×4,
POSITION-EMPTY; 4 "errors" are D's `checks/type.py` returning strings, §5). `python3 -m unittest tests.test_approaches`
→ 16 OK. Full suite: 178 tests, 4 failures + 1 error, all in `tests/test_supporting.py` (S's, mid-build); none in mine,
A's, B's, C's, D's, E's or H's.

## 3. Size and perf per edition (final, `assets/v9`)

| edition | raw | gz | elements | glyph defs | motion | repaints/s (report / trace) | ms per repaint (trace) |
|---|---|---|---|---|---|---|---|
| approaches-day | 262.1 KB | 48.5 KB | 2809 | 174 | lights, 8 indefinite, loops 4/15/96 | 1.094 / 1.3 | 58.0 (paint 19 + raster 39) |
| approaches-night | 264.3 KB | 46.2 KB | 2818 | 174 | same | 1.094 / 1.2 | 62.7 |
| approaches-still-day | 258.7 KB | 47.9 KB | 2771 | 174 | still | 0 / 0 | – |
| approaches-still-night | 261.0 KB | 45.7 KB | 2780 | 174 | still | 0 / 0 | – |
| approaches-phone-day | 83.1 KB | 21.3 KB | 555 | 104 | frozen | 0 / 0 | – |
| approaches-phone-night | 82.7 KB | 21.3 KB | 561 | 104 | frozen | 0 / 0 | – |

Budgets: raw ≤ 300 ✓, gz ≤ 75 target ✓ (46–49), phone ≤ 120 ✓, elements ≤ 3000 ✓, two builds byte-identical ✓
(tested), stats sha stamped ✓. Raw is over the 200 KB *target* (warning): 119 KB of the body is 2,100 glyph `<use>`s
at ~58 B each (the `approaches-g-cond-italic-13-104` ids are the engine's), 49 KB paths (vignette 13, grain 7,
contours, hatch), 75 KB defs. Silhouette: approaches-still-day vs hero-still-day vs approaches-phone-day pairwise
L1 ≥ 0.455 (pass ≥ 0.25). Field: 61 samples, residual 0.0, no unclosed 0/5/10 contours.

## 4. Deviations (and why)

1. **Glyph-library budget (D's `typeset.BUDGET`: ≤ 160 defs, ≤ 40 KB) is exceeded: 174 defs / 66 KB on desk, 104 /
   44 KB on phone.** These are the only build problems. The sheet's lettering is cond 13 upright (70 defs, 15 KB) +
   cond-italic 13 (53, 14 KB) + cond 11 / cond-italic 11 (14, 5 KB) + serif 28 (22, 13 KB) + serif-italic 17 (15,
   8 KB) at night the Light cuts. Any sheet carrying a 28 px serif title *and* a legend through shared glyphs passes
   40 KB; inlining the serif (k.text) instead pushes raw to ≈ 300 KB (one 28 px Instrument Serif glyph is ~800 B at
   one decimal) and gz to ~65. I measured both and kept the smaller, shared design. Already trimmed: plex `machine`
   role dropped (table names in `label`), wreck branch name upright, pencil note the only serif-italic besides the
   two water names. **Patch requested in §5.1.** `check_type` itself is clean.
2. **Raw 262 KB vs the 200 KB target** (gz 48 ≤ 75). Cutting to 200 means cutting the legend or the notes; both are
   the sheet's content. Element count 2,809 leaves 190 of headroom; 16 shards would add ≈ 60 elements.
3. **Per-repaint cost 58–63 ms at 870 px** (1.2–1.3 discrete repaints/s, CPU 7.8 %). Attribution (one layer dropped
   at a time, scratch `P/perfx/`): panels ≈ 45 ms, lines+marks ≈ 22, soundings ≈ 12, water ≈ 10 of ≈ 75. The whole
   `<img>` re-rasters on every SMIL change (12's fact 1), so the cost is the sheet's complexity, not the animation.
   MASTERPLAN 7.3 and 12's rule bound ms/frame "while moving" (continuous windows); this sheet has none after 0 s. The
   harness applies the cap to any repainting sheet; see §5.2. Repaint *rate* (the gate for lights-only sheets) passes.
4. Panel headers (NOTES, ZONES OF CONFIDENCE, SYMBOLS …, INSET …, SHEET 3) are role `label` in caps with +0.6
   tracking, not `label-caps` (the one allowed `label-caps` is the unit line). Recorded in `BREAKS`.
5. The channel's inner legs are collinear on 290° (decision 1 makes W1…ANCH one leading line), so bearings are shown
   twice (318° outer, "Health Ldg Lts 290°"), not per leg; the Ldg line carries the waypoints and COURSE dots run
   only W0→W1.
6. Mark labels are italic (chartlib `LETTERING["mark-label"]`: floating things slope) where T3 §2 said upright; the
   light label and bearings are upright. Mark positions follow decision 1's geometry, not T3's table.
7. The inset is not a ×3 enlargement (header says "THE HARBOUR WORKS"); the inset carries no "Horn" label (the horn
   arcs are drawn on both lights, the label sits at the main light). "SCRAPY HARBOR" is stacked on two 28 px lines.
8. SD sits at (846,596) in zone C, not (840,640): (840,640) is the survey vessel's line. The pencil note sits between
   track lines 1 and 2 at (704,234) with its leader to the Rep ring (T3's (700,232)).
9. The wreck is the first Scrapy stale branch whose name is ≤ 26 characters (`fix/144-lean-docker-extras`, ’25), not
   `stale_branches[0]` (`claude/ensure-this-is-011CUw…`), which would need truncation.
10. The title block is an open centred block in quiet water (13's request), with the folio carrying the series lock-up.
11. Phone: rotated 90° anticlockwise with rules 26/31 (not 14/19) so the 26 px folio fits the margin; the title is a
    paper cartouche over the unsurveyed hatch; phones are frozen (7.3), so the lights do not flash there.
12. Water soundings are placed by Halton + culling against typeset's exclusions and my furniture boxes, not by a
    `soundings()` helper (none exists in chartlib v9).
13. Alt ends with the poem line "The soundings fill in behind the vessel." (`alt_poem[2]`), 25 words.

## 5. Needs

### 5.1 typeset.py (D) — the glyph budget: exact patch
```python
# scripts/typeset.py
-BUDGET = {"glyph_defs": 160, "size_keys": 6, "defs_kb": 40}
+BUDGET = {"glyph_defs": 160, "size_keys": 6, "defs_kb": 40}
+# sheets with a serif title block and a full legend carry more shared glyphs (the alternative, inline serif,
+# costs 2× the bytes): per-sheet ceilings, keyed by begin_asset(sheet)
+BUDGET_BY_SHEET = {"approaches": {"glyph_defs": 200, "defs_kb": 72}}
...
 def check_budget() -> list[str]:
-    errors = []
+    b = {**BUDGET, **BUDGET_BY_SHEET.get(_SHEET, {})}
+    errors = []
     n = glyph_count()
-    if n > BUDGET["glyph_defs"]:
-        errors.append(f"{n} glyph defs (budget {BUDGET['glyph_defs']})")
+    if n > b["glyph_defs"]:
+        errors.append(f"{n} glyph defs (budget {b['glyph_defs']})")
...
-    if kb > BUDGET["defs_kb"]:
-        errors.append(f"glyph defs {kb:.0f} KB (budget {BUDGET['defs_kb']})")
+    if kb > b["defs_kb"]:
+        errors.append(f"glyph defs {kb:.0f} KB (budget {b['defs_kb']})")
```
(Phone editions reach 44 KB with 104 defs; 72 KB / 200 covers both.) Until this lands, `build_assets` reports
10 "type budget" problems for approaches and exits 1; the files are written and all other checks pass.

### 5.2 perf_check.js (E) — the 8 ms cap
12's rule: "after its opening, any sheet over 8 ms/frame carries no **continuous** animation"; MASTERPLAN 7.3: "nothing
over 8 ms/frame **while moving**". `evaluate()` applies the cap to every sheet with `frames > 2`, which fails a
lights-only sheet (approaches, and the hero after 30 s) whose discrete repaints are exactly what the repaints/s gate
budgets. Proposed: apply the cap only to `cls === 'hero'` (its sail) and `cls === 'footer'` (already 4 ms), or read
`continuous_windows` from the build report and apply it only when the trace window overlaps one:
```js
-  if (cls !== 'footer' && cls !== 'none' && ms !== null && ms > 8.0 && row.frames > 2) {
+  const continuous = cls === 'hero' && opt.warm < 28;   // the only continuous window off the ambient sheet
+  if (continuous && ms !== null && ms > 8.0 && row.frames > 2) {
```

### 5.3 checks/type.py (D) / check.py (A)
`checks/type.py` returns plain strings for the budget lines; `check.normalise()` turns them into
`PLUGIN-RESULT` errors (exit 3 "could not check"). Return `fail("TYPE-BUDGET", msg, where)` (or let A's normaliser
accept `str` as a fail).

### 5.4 chart.toml (orchestrator) — one key
```toml
[claims.scrape_interval]
source = "Scrapy:monitoring/prometheus.yml"
sha = "<blob sha of that file at HEAD>"
value = 15
unit = "s"
measured = true
```
C's `claims()` then carries it into `stats.claims.scrape_interval`; the sheet reads the value (must be ∈ LOOP_PERIODS,
else the light is drawn `F`), prints "Grafana Lt · Fl 15s" with `truth=measured key=scrape_interval`, and the inset
lantern follows. Today the sheet falls back to 15 (T8's verified figure) and prints it without a truth mark.

### 5.5 Coordination
- **H (hero) / S (footer):** every `<use>` of a chartlib symbol must use prefix-independent names from
  `chartlib.SYMBOL_NAMES`; the legend defines all 18, so the diff is empty by construction. If either sheet draws a
  symbol *not* in `symbol_defs` (e.g. an inline serpent), it is not a `<use>` and the legend test does not see it;
  the serpent is inline in chartlib and is not in the legend (MASTERPLAN 6 keeps it uncaptioned).
- **Orchestrator:** the full `build_assets.py` run regenerates `assets/build-report.json`; my merge only kept the
  tree checkable meanwhile. `render_readme` alt for approaches now comes from `sheets.approaches.alt`.
- **T8:** the legend's convention line reads "upright figures are measured · sloping figures are not · underlined:
  above datum" (the word "illustrative" is on T10's banned list, case-insensitively, so it cannot appear on a sheet).

## 6. PNGs inspected (scratch `crit/build/P/`)

`day-final.png`, `night-final.png`, `phone-final.png` (from `assets/v9`); `day2.png`, `phone2.png`,
`night2.png` (2×) with crops `night2-harbour.png`, `night2-inset.png`; `phone360.png` (360 CSS px, DPR 3);
`frames/strip.png` and `frames/motion-crops.png` (survey ground, WAL tape and channel at 0.5 / 28.1 / 36.1 / 42.1 s);
`frames-final/frame-*.png` (0 … 600 s vs the still). Perf JSON: `perf-final.json`, `perfx/perf.json`
(layer attribution), `perf-day.json`.

## Summary

1. Sheet 3 is built: harbour west, 290° leading line with Region B marks, rustmapper's survey ground east with one
   track line per shard, restricted area, doubt marks, limit of survey and hatch, proposed unlit channel, ZOC,
   inset, two blocks and the page's single legend defining all 18 chartlib symbols.
2. Honest by construction: every water figure italic; upright only chart number, PyPI edition, Scrapy commits,
   the legend's 265₅; "512" nowhere; shards italic until measured; no coverage figure; strings check clean.
3. Motion is discrete and on plan: lights Fl G/R 4s and Fl 15s, packet boat 7 fixes to 96 s, survey vessel 8 fixes
   at 28–42 s with sounding k and WAL cell k; 1.1–1.3 repaints/s, stills and phones at zero, frames ≤ 0.17 % from
   the still at every instant.
4. Sizes: 259–264 KB raw / 46–49 KB gz / ≤ 2,818 elements desk, 83 KB / 21 KB phone; deterministic.
5. Two gates need engine patches, not sheet changes: D's glyph-library budget (174 defs / 66 KB vs 160 / 40; exact
   per-sheet patch in §5.1) and E's perf evaluator applying the continuous 8 ms cap to discrete repaints (§5.2);
   one chart.toml key for the Grafana scrape interval (§5.4).
6. `tests/test_approaches.py`: 16 tests green (determinism, budgets, legend ⊇ used, honesty, motion plan, buoyage
   geometry, data → geometry, phone floors); the full suite's remaining failures are all in S's test_supporting.py.

---

# Round 2 (orchestrator crit on day-final.png)

Pulled first: `typeset.BUDGET_BY_SHEET` (approaches 200 defs / 72 KB), `perf_check.js --class=moving` cap, the three
`[claims.*]` keys, paler day tints, protan-safe green, retuned night ink2/tints. Changes in `scripts/sheets/approaches.py`
and `tests/test_approaches.py` only; rebuilt into scratch, then merged into `assets/v9/` and the shared
`assets/build-report.json` (38 sheet entries intact; approaches problems: none).

## What changed

1. **The harbour is harbour works, not a blob.** ANCH moved to (172,446); two headland kernels (236,408) and (228,506)
   frame a mouth that opens ESE; two carve kernels make a deep basin (≈ 55, the raw table is the deepest water).
   The 290° leading line runs between the headlands into the basin. **The WAL is the mole**: (n−1)·6+8 ink blocks
   in two courses from the north headland root toward the mouth (`MOLE_A`→`MOLE_B`), a fixed light at its head
   (`use("light")` + static `lit_core`, character `F`), caption "write-ahead log · one cell per sounding" on its north
   side; the last eight blocks are laid by the survey vessel's fixes at 28, 30 … 42 s (`ctx.tl.reveal`), so the mole
   grows with the survey (frames inspected: 48 blocks at 0.5 s, 52 at 36.1 s, complete at 42.1 s). **Quays** at chart
   scale on the basin's shores named for the Delta tables (stage4_summaries N shore, stage1_discovery N headland root,
   stage2_page_analysis S shore) with quay rects; the works on the land south-west: Prometheus mast, Redis twin tanks
   with the Traffic Sig beside them, PostgreSQL tanks, the Summarization Wks shed. One sounding in the basin, the raw
   table's (illustrative italic; `stats.trial.tables.stage1_discovery.rows` makes it upright — tested); the anchor
   and *Delta Lake* in the basin. The shelf is steep (2.5 + 0.09 px⁻¹ to 85 px) so the under-5 and under-10 tints are
   two thin ribbons along the coast, nothing concentric inside the harbour (the basin is deep).
2. **Inset deleted** (its content is now on the chart). The rustmapper block's tape is gone too; the block closes
   with the real wheel line from PyPI ("Wheel · cp313 · macosx_11_0_arm64", upright, `key=wheel`; "elsewhere pip
   builds from source · needs rustc").
3. **The channel is the reading path.** The leading line is a LINE-weight (1.6 px) full-ink rule from the front mark to
   W1, the only rule of that weight on the water; COURSE dots from the outer waypoint W0 (324°) to W1; pairs at honest,
   irregular spacing: G "1"/R "2" off the outer end (fractions .08/.42 of W1–W2), G "3"/R "4" as the entrance gate
   (.78 of W2–W3, .10 of W3–W4), labels outboard (nuns above, cans below); "Health Ldg Lts 290°" north of the line.
4. **Middle water.** Design depth now slopes to 56 with a gentle undulation (sin/cos terms) so the 10, 20 and 50 lines
   wander; levels 0 · 5 · 10 · 20 · 50 (index 10 and 50), the 50 line inside the survey ground, the 20 line through
   the middle water, figures in breaks (corner figures and figures within 28 px of another are dropped). The 429 Shoal
   keeps its danger ring and gains a *PA* doubt mark; the wreck (real stale branch) stays.
5. **Phone** keeps the rotation: `phone360-r2.png` (360 CSS px, DPR 3) inspected — every kept name legible; R "4"
   sits in the mole's lee so its label goes below the mark; "Ldg 290°" to the right of the line.
6. Fixes surfaced by the new plug-ins: lateral cores are `light_core` on every edition (decision 21; CONTRAST-LIGHT
   clean); `legend[]`/`symbols_used[]` are bare symbol names and `symbols_used` names every `-sym-` href in the file
   (LEGEND plug-in clean, no LEGEND-UNUSED); bounds: limit label between the B and C boxes, pencil note between track
   lines 2 and 3 with a longer leader, taller sounding cull boxes (ascender to descender), smaller north-arrow
   exclusion on the phone (BOUNDS clean, no texture warning).

## Gates (final, assets/v9)

`build_assets --sheets approaches`: 6 files, **0 problems**. `checks/motion.py`: 0 findings. `check.py --dev --tier fast
--only approaches`: no approaches findings except SIZE-TARGET warnings and D's `TYPE … 171 glyph defs (budget 200)`
(see below). `perf_check --warm=44 --seconds=10`: day 12 repaints / 1.2 per s, 55.7 ms per repaint, cpu 6.9 % → PASS;
still and phone 0 repaints → PASS. Frames vs still at 0.5 / 28.1 / 36.1 / 42.1 / 95 s: coverage 0.997–1.000, changed
≤ 0.12 %. `tests/test_approaches.py`: 16 OK (byte-identical rebuild included).

| edition | raw | gz | elements | glyph defs | motion |
|---|---|---|---|---|---|
| day / night | 265.5 / 268.0 KB | 48.9 / 46.7 KB | 2865 / 2874 | 171 | lights, 7 indefinite (5 lights + boat 2), 1.094 repaints/s, loops 4/15/96 |
| still-day / still-night | 262.3 / 264.9 KB | 48.4 / 46.1 KB | 2828 / 2837 | 171 | still |
| phone-day / phone-night | 94.5 / 94.0 KB | 22.7 KB | 612 / 619 | 104 | frozen |

Measured (upright) runs: `PyPI 0.1.3 · alpha · 2025-11-08` (edition), `Wheel · cp313 · macosx_11_0_arm64` (wheel),
`265` (scrapy_commits), `265₅` (legend example), `21` (chart-number). Grafana Lt prints `Fl 15s` from
`claims.scrape_interval` (measured, keyed) — the figure is part of a light character, set upright in the label role.

## One engine bug for D (checks/type.py)

`check_report()` compares `sheet["glyph_defs"]` against the global `typeset.BUDGET["glyph_defs"]` (160) while printing
the per-sheet budget it should use, so approaches fails with "171 glyph defs (budget 200)":
```python
-        if n is not None and n > typeset.BUDGET["glyph_defs"]:
+        if n is not None and n > typeset.budget_for(_sheet_of(name))["glyph_defs"]:
```
(`check_budget()` in typeset itself is already per-sheet; only the report-side check lags.)

## PNGs inspected (round 2)

`day3.png` … `day6.png`, `day-final-r2.png`, `night3.png`, `night5.png`, `night-final-r2.png`, `phone3.png` …
`phone6.png`, `phone-final-r2.png`, `phone360-r2.png`; crops `day4-harbour.png`, `day5-harbour.png`,
`day6-harbour.png`, `night6-harbour.png`, `phone5-harbour.png`; motion `frames-r2/mole-and-line.png` (0.5 / 36.1 /
42.1 s), `frames-r3/frame-42p1.png`.

## Summary (round 2)

1. The harbour is now works, not a blob: two headlands, a deep basin on the 290° leading line, the WAL as a block
   mole with a head light that the survey vessel finishes laying at 28–42 s, quays named for the Delta tables and
   workers; the inset is gone.
2. The leading line is the darkest rule on the water from "1" to the anchorage, dotted course from the outer mark,
   pairs 1/2 and 3/4 at irregular spacing with outboard labels; 10/20/50 contours wander through the middle water.
3. Honesty unchanged: every water figure italic; upright only chart number, PyPI edition and wheel, Scrapy commits,
   the legend's 265₅; "512" nowhere; shards italic; no coverage figure.
4. Motion on plan: 7 indefinite, 1.09–1.2 repaints/s, frames ≤ 0.12 % from the still, stills/phones frozen, perf PASS.
5. Gates clean on the sheet (motion, bounds, legend, contrast, flash, xml, strings, tests); sizes 262–268 KB /
   46–49 KB gz desk, 94 KB phone, ≤ 2874 elements, 171 glyph defs within the new budget.
6. One remaining fail is D's report-side glyph check comparing against the global 160 instead of the per-sheet
   budget (one-line patch above); phone rotation kept — legible at 360 px.

---

# Round 3 (re-crit panel: 07, 13, 09, 28, + 10-mobile addendum)

Changes in `scripts/sheets/approaches.py` (rewritten in place; the round-2 file is kept at scratch
`P/approaches.round2.py`) and `tests/test_approaches.py` (17 tests). Rebuilt into scratch and merged into `assets/v9/`
and the shared `assets/build-report.json`.

## What changed

1. **Legend and notes at 17 px.** Role `label` with `size=17` (17 is on SCALE; the lint accepts it) for every legend
   definition, the legend's convention line and both notes bodies; symbol cells scaled ×1.3 to match. The strip is
   reflowed: the two notes blocks side by side (36/644, 524, 600 × 194) over a full-width four-column legend
   (36, 724, 1208 × 212), 32 rows × 8 per column, pitch 19. The headline stays "SYMBOLS · CHART NO. 21 · EVERY SHEET"
   (17 px, tracked) with the upright/sloping/underlined line beneath. The four rows the legend plug-in allows as drawn
   things (Sloop, Packet boat, Flare, Halo) are gone, as 07 and 13 asked; nothing else renamed or re-explained.
   The map gave up the height: the T3 geography (680 tall) is compressed into 500 (`_y()`, k = 0.735) with the
   channel re-derived from ANCH so the leading line stays exactly 290°; the survey ground is (680,124,400,386).
2. **Phone legend and margins.** The phone edition keeps the rotation (legible at 360 px: `phone360-r3.png`) and
   now ends in a compact two-column legend of its own symbols — 12 rows at the phone label role (G can, R nun,
   Light, Ldg line, Anchorage, Wk, Rep, ED, SD, Danger line, Restricted, Limit of survey) with the convention line;
   `SIZES["phone"] = (720, 1880)`. Per 10-mobile: neat-line rules 50/55, so the unit line, chart number and folio sit
   24 px inside the sheet edge; the title is open and centre-stacked (no box, no hatch behind) with the IALA line
   "IALA Region B · marks numbered from seaward"; chart scale 1.2, band cropped to 54 px of desk; buoy labels
   'G "1"' … 'R "4"' are `label-italic` 26 (G "1" above its can, R "4" below, clear of the mole).
3. **Light characters.** G "1" Fl G 4s (0), R "2" Fl R 4s (2) — the hero's pair; the entrance gate G "3" Fl(2) G 10s (0)
   and R "4" Fl(2) R 10s (2) through `ctx.tl.flash`. Timeline.report 1.323 repaints/s; trace after 44 s: 1.4 per s
   (budget ≤ 2) → PASS. 7 indefinite animations (5 lights + packet boat ×2). Legend row "Light · its character" kept.
4. **Sounding lattice.** Survey-ground soundings jittered (seeded) ±9 px in column spacing and ±3 px along the track,
   ±1 across; one figure dropped at random on each of the two lines the pencil note crosses and half the figures under
   the note's span; the SD doubt mark now sits on a lattice node of line 7 (the lead's own figure, doubted). The
   note itself sits between track lines 1 and 2, ending west of the restricted area. BOUNDS plug-in: clean.
5. **Zones of confidence** as a ruled block: hairlines between rows, plain letters, no mini-sheet, no hatch, no boxes.
   Zone letters stay boxed only on the limit line. Also from 13: the outer-leg bearing (294°) is sloping — a drawn
   angle; 290° stays upright as the construction it is.

## Gates (final, assets/v9)

`build_assets --sheets approaches`: 6 files; the only problems are the glyph-library budget (below).
`check.py --release --tier fast --only approaches`: approaches findings = SIZE-TARGET warnings + D's report-side
TYPE line (same bug as round 2, now against 200); BOUNDS, LEGEND, FLASH, CONTRAST, XML, STRINGS, MOTION clean.
README-STALE is the README, not the sheet. `checks/motion.py`: 0. Perf: day 1.4 repaints/s, 62.8 ms per repaint,
cpu 9 % → PASS; phone/still 0 repaints. Frames vs still at 0.5/28.1/36.1/42.1/95 s: coverage 0.996–1.0, changed
≤ 0.14 %; the 42.1 s frame shows the mole complete and the eight soundings laid. Tests: 17 OK (determinism,
budgets, legend == charted symbols and used ⊆ legend ∪ allowed, phone legend ≥ 8 rows, honesty, motion plan incl.
Fl(2) 10s durations, buoyage geometry, data → geometry, phone floors, legend/notes at 17).

| edition | raw | gz | elements | glyph defs | motion |
|---|---|---|---|---|---|
| day / night | 274.9 / 277.2 KB | 53.0 / 50.8 KB | 2794 / 2803 | 248 | lights, 7 indefinite, 1.32 repaints/s |
| still-day / still-night | 271.7 / 274.1 KB | 52.5 / 50.3 KB | 2757 / 2766 | 248 | still |
| phone-day / phone-night (720 × 1880) | 115.2 / 118.1 KB | 25.4 KB | 932 / 940 | 113 | frozen |

## Needs

- **typeset.BUDGET_BY_SHEET (D / orchestrator):** the 17 px cond set is a new glyph size key, so approaches is at
  248 defs / 87 KB against the round-2 ceiling of 200 / 72. Please set
  `BUDGET_BY_SHEET["approaches"] = {"glyph_defs": 260, "defs_kb": 92}`. It is the only build problem on the sheet.
  The phone editions are at 113 / 58 KB (within). And `checks/type.py check_report()` still compares against the
  global `BUDGET["glyph_defs"]` (round-2 patch stands).
- Phone raw is 115–118 KB against the 120 KB gate: the vignette and the coast swell pass are desk-only now and the
  phone legend's convention line is upright to keep the italic glyph set small; a further phone row or label will
  need the phone budget looked at.

## PNGs inspected (round 3)

`day7.png` … `day9.png`, `night7.png` … `night9.png`, `phone7.png` … `phone9.png`, `phone360-r3.png` (360 px, DPR 3),
`frames-r4/f42-crop.png`.

## Summary (round 3)

1. Legend and both notes blocks are now 17 px (11.6 px rendered in the README column): a full-width four-column
   32-row legend under two side-by-side notes blocks; the map gave up 180 px of middle water and kept its 290° line.
2. The phone edition (720 × 1880) keeps the rotation, gains an open title with the IALA line, a 12-row two-column
   legend of its own symbols at the phone label role, buoy numbers at 26 px, and 24 px head/foot margins.
3. Light characters differ by pair: Fl G 4s / Fl R 4s outer, Fl(2) G 10s / Fl(2) R 10s at the entrance gate;
   1.4 repaints/s measured after 44 s.
4. The survey lattice has the lead's irregularity and thins under the pencil note; the ZOC is a hairline-ruled block;
   the outer-leg bearing is sloping.
5. All sheet gates clean (bounds, legend, flash, contrast, motion, xml, strings, tests, frames, perf); sizes
   272–277 KB / 50–53 KB gz desk, 115–118 KB phone.
6. One engine ask: raise the approaches glyph budget to 260 defs / 92 KB (the sheet's only build problem).

### Round 3 addendum — the hero's week soundings in the legend
A 33rd legend row: the HW week's figure from stats.json (358₁: commits in the week, days with a commit — upright,
measured) with the text "Sheet 1 · week's commits, days" beside the existing "4₂ · Sounding · 1000s, 100s", so the one
legend explains both instruments; the convention line stays. Legend now 9 rows × 4 columns (pitch 18.3, cartouche
36,718,1208×218; notes blocks 188 tall, pitch 17). Final: day 278.3 KB / 53.4 gz / 2828 el, night 280.9 / 51.3 / 2837,
stills 275–278 KB, phones 115–118 KB; glyph defs 251 / 88 KB (the budget ask becomes 260 / 92 — unchanged). Tests 17 OK;
motion 0; release fast tier: no approaches findings beyond the TYPE budget line and SIZE-TARGET warnings.
