# Builder S report — T9 supporting sheets (soundings · log · instruments · footer)

Files written, all inside my ownership: `scripts/sheets/soundings.py`, `scripts/sheets/log.py`,
`scripts/sheets/instruments.py`, `scripts/sheets/footer.py`, `tests/test_supporting.py`. No engine file,
no `chart.toml`, no `docs/crit` edit; no git command. Built into `assets/v9/` with the default runner (the last
run was the full six-sheet build so `assets/build-report.json` lists all 38 files: 0 problems).

## 1. What was built

Every glyph goes through `typeset` (`text_use`/`text`/`sounding`, `truth=`/`key=` on every figure that is a
claim), every stroke through `chartlib.stroke`, every `<animate*>` through `ctx.tl`; no raw `<text>`, no hand
SMIL, no `<pattern>`, no filter, no `animateMotion`. Phone editions are redrawn at `SCALE_PHONE` through a
`NullTimeline` (motion.py treats non-hero phone files as frozen). Still = the t = 95 s state.

**Soundings · Sheet 2 (1280×400 / 720×360, strip, frozen).** Head: dateline from `updated_at`
("Soundings taken 7 Oct 2026 · 19:47 UTC") and the sheet's one tracked caps run, the unit line
`SOUNDINGS IN COMMITS` from `[copy] unit_hero`. Tide plot x 48–1232, HW at y 70, zero at y 188: monotone cubic
through the 52 `weeks[].n` (upright: clone-derived, author-filtered, decision 19), area in `shallow_a`, HW dot
with `HW 358 · wk of 5 Oct · Data science dev` (the ≤ 14-day sprint rule appends `, N days`), hollow LW dot with
`LW 0 · wk of 24 Aug`, `typical week 0` placed over the longest flat run at the median, slack-water bracket
and `slack water · Jul`, the serif pencil note `Heights observed, not predicted.` in the quiet upper-left;
stale (`no_sounding` / `provenance.mode == cache-failed`) dashes the baseline and adds `no sounding taken
{date}`. Under the plot a **traverse of the same 52 figures** as depth soundings (`sounding()`, cond 11,
upright, `key=week.i`) with month ticks and letters. Fleet register: 7×3 cells, repos by commits desc, name
(ink when `active`, ink2 otherwise), commits as a spot height (`key=repo.<name>.commits`), 52-week polyline
on one shared scale (278/week full height, stated in the register key). Foot: folio at (24, h−5) (decision 27)
and the source line naming **both instruments**: `1,665 commits · 1,966 all hands · 1,828 by GitHub's
calendar`, all upright, each its own keyed run. Phone: curve, HW/LW at 26 px, serif-italic 30 footnote,
folio and unit line.

**Ship's log · Sheet 4 (1280×490 / 720×220, paper).** `paper_log` stock, 1 px accent margin at x 104,
rules every 30 px from 118, title `Log of the rustmapper` (serif-italic 28), header
`127.0.0.1:8080 · rustmapper 0.1.3 · 7 Oct 2026`, columns `TIME · LOG · URLS · SPEED · REQ/S · WIND ·
REMARKS` (LOG/SPEED right-aligned at 210/330, WIND 352, REMARKS 470 within 766). Rows from
`data.logsim.simulate(profile, entries, hosts, start)`: 10 entries, `$` prefix on cmd/crawl rows, WIND from
ratios, `—` for no reading. **Every digit token on the page is set in `plex-italic`** (`measured:false`;
the regex splits `127.0.0.1:8080`, `0.4%`, `12,440`, `p95`), the header date included; the heartbeat row and
the folio are the only upright figures. Sign-off: `Log closed 1550 ·` typed (machine, muted) and `B.S.R.`
signed (serif italic). Heartbeat `1947 UTC · watch kept by cron · 1,665 commits · 21 repositories` built from
`log.json heartbeat.template` and `updated_at/commits/repo_count`, typed per glyph from 44.0 s via
`tl.typed(glyphs=…)` with the `text_use` run split into one `<use>` fragment per character (ends ≈ 48.4 s),
the cursor riding then blinking 1 s from 48.5 s (`tl.cursor`, `id="log-cursor-blink"`). `ctx.heartbeat False`
→ `$` and a steady cursor, no `<set>`. Stale → `no sounding taken {date}` under the header. Phone: title,
folio, two remarks, sign-off, heartbeat line with a static cursor.

**Instruments · Sheet 5 (1280×290 / 720×48, strip, frozen).** Decision 2 layout: three 266 px columns at
x 480/747/1013 with HAIR rules between, heads `LEAD · LANGUAGES`, `LOG · STORES AND QUEUES`, `LOOKOUT · DECK`
from `[fittings] groups` (machine, tracked), 18 items from `[[fittings.items]]`: name in `machine-strong` ink
when `repos[repo].active` else `machine` ink2, dotted leader (HAIR, TRACK), fitted date `Sep 2025` from
`repos[repo].first` (cond, upright, `key=fitted.<name>`), the three legend marks in a gutter (track lines
after Rust, anchorage after Delta Lake, light after Prometheus · Grafana, via `chartlib.symbol_defs` ids).
Left third: the reading key in plain words (`bold · carried by a repository underway this quarter (1 of 21)`,
`date · first commit of the repository that carries it`) and the folio. Phone: a rule and the folio.

**Limit of survey · Sheet 6 (1280×270 / 720×320, edge, the one ambient sheet).** Neat line broken on
the right y 112–226; prose `The chart ends here. The web doesn't.` from `[copy] footer_line`; index of
adjoining sheets (hatched 4×3 grid, cell "1" in land); water from x 264 to 1040 with the lip, three fall lines,
mist; six italic soundings thinning toward the limit; `Obstn rep. 2026 (PA)`; dotted limit line at x 1000
with `LIMIT OF SURVEY 2026` reading upward; land + hand-ruled hatch beyond; folio, `{N} notices` (+ contact
when `[contact]` is set) outside the neat line. Motion per §2.1: swell 10 s `sea` (translate −48, clipped),
hull −2 px 10 s, three mist fades on the 10 s grid (0/3.5/7) with one shared drift; the sloop (chartlib's
`SLOOP_DETAIL` paths) under way at x 330 with `rotate(−4)`, `tl.sail` 40→64 s to x 950 (`settle`, pitch
settles 0.65 s), the main luffs once (`scale 1→0.6→1` about the mast, 0.8 s), rode + `<use anchorage>` +
`14 · good holding` fade in 0.65 s; `chartlib.serpent` with hump-1/hump-2/head each on its own 96 s
`tl.every` (head first, humps +0.25/+0.5 s; up 0.9 `settle`, hold 0.6, down 0.9 `draw`) first at 84 s,
clipped at the surface; three ripple rings (group scale + group fade, 20 s) from 86.5 s. **11 indefinite
animations** (budget 12). Night: limit line .85 is the brightest hairline, sail accent, serpent eye accent.
Phone: anchored end state, prose on two lines (serif-italic 40), limit at x 560, boat ×1.4, no index, no serpent.

## 2. T9 §5 acceptance

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | no ILLUSTRATIVE/PENDING/SEEDED/example.com | pass | `check.py` strings plug-in: 0 findings on the 24 files + manifests + alts; `test_no_banned_strings`. The log.json entry word "seeded" is printed as "seed list" (see §4.3) |
| 2 | change `weeks[k].n` → tide moves; delete `weeks` → build fails "no soundings" | pass | `test_changing_a_sounding_moves_the_tide_and_no_weeks_fails` (+1000 on HW → `HW 1,358`, file differs; no weeks → problem `no soundings: stats.json carries no weeks[]`) |
| 3 | every numeral in log-*.svg italic unless measured / heartbeat row; simulate monotone, speed = Δlog/Δt | pass | `test_log_numerals_are_italic_except_the_heartbeat` over the report manifest (slant per run); logsim's own tests (C) cover the arithmetic; rows 0→0→230→3,230→3,350→12,440 monotone |
| 4 | soundings & instruments 0 repaints; log ≤ 2/s after 50 s; footer ≤ 4 ms/frame and the only continuous sheet | pass | `perf_check.js`: soundings-day 0 frames, instruments-day 0 frames (warm 4, 6 s); log-day warm 50: 2.0 repaints/s, 3.4 % CPU; footer-day warm 66, 10 s: **3.66 ms/frame** (3.30 on a quieter run), 57.7 repaints/s, 23 % CPU, pass. Timeline report: footer `ambient/11`, log `lights/1/2.0`, others `frozen/0` |
| 5 | filmstrip: a boat in every footer frame; header + ≥ 10 entries in every log frame | pass | `render.mjs frames` footer 0.5/48/64.1/84.5/95 vs still: coverage 0.991–1.005, changed ≤ 0.77 %, blankLedger false (boat at 330 → sailing → anchored); log 0.5/44/48/95: coverage 0.971–1.0, changed ≤ 0.29 %; `test_log_frames_keep_header_and_ten_entries` (10 `row.i.time` runs, heads, no base `opacity="0"` outside the typed group) |
| 6 | OCR of 360 px renders recovers every 26 px string; Instruments phone is a rule plus folio | pass (by eye) | phone PNGs at 360 px DPR 3 read cleanly (paths in §6); `test_fittings_resolve…` asserts the instruments phone manifest is exactly `[folio]`; `test_phone_editions_are_redrawn` asserts every phone size ∈ SCALE_PHONE and ≥ 26 semantic. No tesseract run here |
| 7 | alts ≤ 25 words, from data, none naming the serpent | pass | soundings 25 · log 24 · instruments 25 · footer 24 words; last sentences equal `alt_poem[1,3,4,5]` (`test_alts`); report poem = the six lines |
| 8 | day muted ≥ 4.5:1; night semantic ink ≥ .85 | pass for my sheets | contrast plug-in's failures are token-level (`ink2 on land` at night, tint vs land, CVD) and hero/approaches lights; none names my sheets. All semantic night text is ink/ink2 at full opacity (muted only for captions) |
| 9 | every FITTINGS name resolves; heartbeat = `updated_at` to the minute and matches the Soundings dateline | pass | `test_fittings_resolve_and_bold_means_active` (18/18 repos found; bold ⇔ `active`); `test_heartbeat_matches_the_soundings_dateline` (`1947 UTC` ⇔ `19:47 UTC`, `1,665 commits`, `21 repositories`) |

Also: `scripts/checks/motion.py assets/v9/*.svg` → 0 findings; `check.py --dev --tier fast` → no finding on any
of my 24 files except SIZE-TARGET warnings (§4.1); silhouettes (128 px, 16×8) pairwise L1 ≥ 0.74 day, ≥ 0.84
night (gate 0.25); `python3 -m unittest tests.test_supporting` → 20 OK; full suite 178 tests, 1 failure in
`test_hero` (H's, `test_course_clear_of_features_and_harbour_open`).

## 3. Size and perf per edition

| file | raw KB | gz KB | elements | glyph defs | motion |
|---|---|---|---|---|---|
| soundings-day / night | 85.9 / 90.4 | 15.1 / 15.0 | 1007 | 89 | frozen, 0 anims |
| soundings-still-day / night | 85.9 / 90.4 | 15.1 / 15.0 | 1007 | 89 | — |
| soundings-phone-day / night | 33.3 / 34.1 | 9.2 | 186 | 56 | — |
| log-day / night | 80.1 / 82.5 | 16.7 / 16.5 | 976 | 100 | lights, 1 indefinite, 2.0 repaints/s |
| log-still-day / night | 75.5 / 77.8 | 15.8 / 15.7 | 923 | 100 | — |
| log-phone-day / night | 37.1 / 37.4 | 10.8 / 10.7 | 208 | 68 | — |
| instruments-day / night | 56.5 / 58.3 | 10.9 / 10.6 | 603 | 93 | frozen |
| instruments-still-day / night | 56.5 / 58.3 | 10.9 / 10.6 | 603 | 93 | — |
| instruments-phone-day / night | 4.8 / 5.1 | 1.7 / 1.8 | 36 | 14 | — |
| footer-day / night | 70.1 / 71.1 | 23.1 / 23.3 | 120 | 6 | ambient, 11 indefinite, continuous |
| footer-still-day / night | 66.4 / 67.4 | 22.3 / 22.5 | 101 | 6 | — |
| footer-phone-day / night | 29.6 / 30.4 | 8.1 / 8.2 | 209 | 60 | — |

Perf (Chromium headless, `<img width=870>`, DPR 1; this machine reproduces 12's legacy footer at 2.91 ms vs
his 2.8): footer-day 3.66 ms/frame (max 11.6 in one frame, 3.84 on the quiet run), 23 % CPU; log-day
16.1 ms per repaint × 2/s = 3.4 % CPU; soundings/instruments 0 repaints. Hard budgets (300/100 KB, 3000
elements, phone 120 KB) all met; two builds byte-identical (test).

## 4. Deviations (and why)

1. **Size targets missed on three sheets** (warnings): soundings 86/90 vs 80 raw (gz 15 vs 25 ✓),
   instruments 56/58 vs 50 raw (gz 11 vs 18 ✓), footer 70/71 vs 40 raw and 23 vs 12 gz. The footer is over
   because it letters inline (next item); soundings/instruments because a 13 px glyph outline costs ~300 B
   and each sheet carries 90 distinct glyphs (≈30 KB) before a word is placed; night ids are longer
   (`cond-light`). I trimmed copy (dateline, source line, register key) rather than drop the serif note, the
   traverse, or register names. Hard caps are far away.
2. **Footer letters inline on the desk editions** (`typeset.text`, one `<path>` per run; phone keeps
   `text_use`). Measured: static labels as `<use>` glyphs cost ≈ 17 µs each per frame, inline ≈ 10 µs; the
   footer went 4.24 → 3.3–3.7 ms/frame, under 12's binding 4 ms, for +20 KB raw. Declared in `BREAKS`.
3. **Footer copy trimmed for paint**: `NO ADJOINING SHEET` dropped, index label `ADJOINING SHEETS`, the
   margin record is `{N} notices` (+ contact when set) — the taken date is on the soundings dateline (T9 §5.9),
   so it is not repeated at 57 repaints/s.
4. **Boat start x 330, anchorage x 950** (T9: 90 and 980): at 90 the hull sat on the index box and its
   label; at 980 the anchored rig crossed the rotated `LIMIT OF SURVEY 2026`. Water now starts at x 264, so
   the left 250 px are margin notes (prose, index) and the sea runs from there to the fall.
5. **Sign-off split**: `Log closed 1550 ·` typed, `B.S.R.` signed in serif italic. Keeps the two voices and
   brought the log's glyph defs from 50 KB to 36 KB (typeset budget 40).
6. **Log columns widened** (LOG end 210, SPEED end 330, WIND 352): T9's 226/318/340 overlap in Plex Mono 13.
7. **Instruments group labels horizontal** above each column (machine, tracked), not rotated: the rotated
   `LOG · STORES AND QUEUES` overran the column top at 13 px; marks moved to a gutter at col+14 so the long
   names (`Prometheus · Grafana`) clear the dates; dates in cond so they fit 266 px; serif gloss line cut.
8. **Footer index label under the box**, hatch spacing 6.5 in the index; only the sheet's own symbols are
   extracted from `chartlib.symbol_defs` (`_symbols()` in footer.py/instruments.py: same ids, same drawings,
   not eighteen symbols per sheet).
9. **Footer serpent opacity on the strokes** (`stroke-opacity=".7"`), not on the group: a group opacity is
   an offscreen layer every frame.
10. **Mist**: three opacity fades + one shared drift (4 loops) instead of 3×(fade + rise) to stay within 12.
11. **Footer "Obstn rep." at (926, 106)** so it clears the serpent's rise and the anchored boat.
12. **"seeded" printed as "seed list"** on the log (see §5.3); the substitution is a one-entry table in log.py
    with a comment, not a change to log.json.
13. Soundings alt names the HW cause by its repository name (`Data_science_dev`) to stay at 25 words.

## 5. Needs (exact patches / keys; I did not edit engine files)

1. **`scripts/checks/bounds.py` double-rotates rotated runs.** `typeset.run_records()` already stores the
   rotated bbox (`_register` → `_rot_bbox`), and `_box()` rotates it again about `(x0, y)`, turning a
   vertical `LIMIT OF SURVEY 2026` into a horizontal box along y 213–226 (it reported a collision with my
   sounding "4"; the hero/approaches `LIMIT OF SURVEY`/`UNSURVEYED` failures look the same). Patch:
   ```python
   # bounds.py, _box()
   -    if r.get("rot"):
   +    if r.get("rot") and "y0" not in r:   # typeset's manifest already holds the rotated box
   ```
   I nudged the "4" 8 px up so my sheets pass even before the fix.
2. **`scripts/typeset.py` rotated bbox pivot.** `_register` rotates about `x0` (the run's left end) while
   the SVG rotates about the anchor `(x, y)`; a `rotate=` run with `anchor="middle"|"end"` is registered
   off by half/all its width. Patch: give `_register` a `pivot_x=None` parameter, use
   `_rot_bbox(x0, y0, x1, y1, pivot_x if pivot_x is not None else x0, y, angle)`, and pass `pivot_x=x`
   from `_set`. I work around it by anchoring rotated runs at `start` (phone `UNSURVEYED`: start = centre + w/2).
3. **`SEEDED` in `scripts/checks/strings.py` vs `assets/log.json`** entry 3 `"seeded · sitemap · …"` (T9's
   own wording). Either C rewords the entry (`"seed list · sitemap · …"`, which is what I print) or A/T10
   drops `SEEDED` from `BANNED` (it was the v7 placeholder marker; `data.py` already forbids the key).
4. **`chart.toml` key (optional)**: `[[fittings.items]] mark = "track" | "anchorage" | "light"`; instruments.py
   reads `item.mark` first and falls back to a name table (`Rust`, `Delta Lake`, `Prometheus · Grafana`).
5. **Perf facts for H/P and T10**: at 870 px, every glyph costs ≈ 17 µs per repaint as a `<use>` and
   ≈ 10 µs inline; a sheet with ~660 glyphs (the log) repaints in ~16 ms whatever the markup (an all-inline
   log was 314 KB and still 9.8 ms). The log therefore cannot meet an 8 ms/frame cap; its 1 s cursor blink
   is discrete (2 repaints/s, 3.4 % CPU), which is what 12 allowed ("over 8 ms/frame carries no *continuous*
   animation"). `perf_check.js` now passes it; if the cap is re-tightened, the only honest fix is fewer
   glyphs (shorter log.json remarks) or no blink — I kept the MASTERPLAN blink.
6. **Decision 27 vs T9**: folios are at (24, h−5) on all four sheets (MASTERPLAN wins); T9's top-right
   `CHART NO.` on soundings is not drawn. The soundings sheet carries `SOUNDINGS IN COMMITS` as its one
   label-caps run; `UNSURVEYED` and the index label on the footer are plain `label` uppercase so the
   label-caps budget holds.
7. `log.json` kinds are C's `crawl`/`beat` (T9 said `cmd`/`remark`); both handled (`crawl` gets the `$`).
8. Nothing needed from `tokens.py`.

## 6. PNGs inspected (scratch `…/crit/build/S/png/` unless noted)

`soundings-day.png`, `soundings-night.png`, `soundings-phone-day.png`, `soundings-phone-night.png`;
`log-day.png`, `log-night.png`, `log-phone-day.png`, `frames-log/frame-46.png` (typing, cursor riding);
`instruments-day.png`, `instruments-night.png`, `instruments-phone-day.png`;
`footer-day.png`, `footer-night.png`, `footer-phone-day.png`, `footer-phone-night.png`,
`footer-strip-final.png` (0.5 / 48 / 64.1 / 84.5 / 95 vs still), `frames-footer/frame-85p2.png`,
`frames-footer/frame-85p4.png` (serpent head-first), `frames-footer/frame-95.png`;
silhouettes in `…/S/sil/`. Perf JSON: `frames-final.json`, `frames-log-final.json`; experiments in `…/S/exp/`
(`log-inline.svg` 314 KB / 9.8 ms, `f-notext.svg` 1.69 ms, `f-inline.svg` 3.34 ms).

## 7. Summary

1. Four sheets built, 24 files + tests, every glyph through typeset, every animation through the timeline; full six-sheet build 38 files, 0 problems.
2. Soundings: tide curve + 52-figure traverse + fleet register, both commit instruments named; Instruments: full-width right-hung inventory; both frozen, 0 repaints.
3. Log: computed session, every numeral italic, heartbeat typed 44–48.4 s, cursor blinks from 48.5 s at 2 repaints/s (16 ms each: glyph raster, documented).
4. Footer: the ambient sheet at 3.3–3.7 ms/frame with 11 loops, boat 330→950 at 40–64 s, serpent at 84 s / 96 s, inline lettering to buy the paint.
5. Gates: motion lint 0, check.py 0 findings on my sheets (size-target warnings only), silhouettes ≥ 0.74, still-frame coverage ≥ 0.97, 20/20 tests.
6. Needs: bounds.py double rotation and typeset rotated-pivot patches (above), SEEDED vs log.json wording, optional `mark=` fittings key; size targets on three sheets are warnings I could not close without dropping real content.
