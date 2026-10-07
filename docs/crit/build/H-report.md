# Builder H report — T2 hero sheet (`scripts/sheets/hero.py`, `tests/test_hero.py`)

Files written (only mine): `scripts/sheets/hero.py` (≈ 640 lines), `tests/test_hero.py` (15 tests). No engine file,
no `chart.toml`, no docs edited. No git commands run. Built into the scratch dir first, then into `assets/v9/`
(default out) — `assets/build-report.json` now carries the eight hero entries with zero problems.

## 1. What was built

The chart proper, 1280×740 (phone 720×900), eight editions, one code path:

- **Field.** Depth = count. The 52 `weeks[].n` are the soundings along the course (oldest seaward, in the band;
  the newest in the approach), `Field.from_soundings(kernel="bump", h_snd=30·s, cell 6 desk / 4 phone)`,
  base = median of weeks clamped to [10, 50] → 10 → nudged to **10.5** (never on a contour level). Every surveyed
  repo is a `Feature` (21 today): alias/slot/kind from `[[features]]` (Rust-sitemap → *rustmapper*, kind
  `vessel` drawn as the ship's own shoal; Scrapy → *Scrapy Harbor*; BenjaminSRussell → *Profile Shoal* with the
  △ station), otherwise `kind_of()` (dormant → island, active → shoal, r < 16 → islet). Area law: `solve_radii`
  on the feature's own ground (features + basin, no soundings) at k_area = 32.2 px²/commit (phone × s²), with a
  bisection fallback for the harbour (its basin bite makes area(r) discontinuous and the Newton step
  oscillates); ratios **0.978–1.027**, drawn (full-field) ratios **0.977–1.025**, all 21 inside ±8 %. The build
  raises if any feature with r ≥ 10 px fails. Harbour basin: one kernel (786,559,h 30, amp −2.1·base) → anchorage
  depth ≈ 4, mouth ≈ 10, land at the centre; asserted at build.
- **Contours** 5/10/20/50 (`draw_contours`, index 10/50 at LINE), figures in breaks via `contour_labels` +
  `break_anchor` (min length 220 px), the approximate dashed fringe at x ≥ 1040, tints A (under 10) and B
  (under 5) as evenodd fills from `level_polygons`, coastline + swell, coast vignette on named land, danger lines
  on shoals only, rustmapper's ground drawn twice (survey + pecked "as charted" outline +24/−14 with *PA*).
- **Soundings**: 42 printed upright through `k.sounding(truth="measured", key="week:<start>")`; the 10 in the band
  are kernels only (unprinted; opacity thins .75 → .40 over x 1000 → 1080). Bracket test with `base`, band
  soundings skipped, 4 px nudge rounds: **0 failures** on the desk, 4 `unresolved` on the phone (rings under
  the grid, correct in the field).
- **Course** WP1 (1136,296) → WP2 (1046,360) → WP3 (900,470) → WP4 (842,580) → WP5 (776,556), pecked, bearings
  235°/233°/208°/290°, dated fixes OCT 2025 (rustmapper's first commit) at WP2 and SEP 2025 (Scrapy's) at WP4,
  ⚓ at WP5, coverage box (680,470,210,160) + SEE SHEET 3. **Marks**: R "2" nun (827,551) north, G "1" can
  (813,593) south of the 290° leg, labels italic, `lit_core` per mark with `tl.flash("Fl G 4s", begin 0)` /
  `("Fl R 4s", begin 2)` — the two loops; night halos r 14 in the same group so each light is one animation.
- **Rose** `two_ring_rose(1000,160,72)` with real `hours[24]`, 00 at top, modal 14 h arrow, `VAR 14h (2026)` /
  `AUTHOR'S LOCAL TIME` (annual change omitted: `variation.annual_change` is null).
- **Title block** open, centred x 268: THE OPEN WEB · FROM SURVEYS 2025–2026 / CRAWL AND DATA INFRASTRUCTURE ·
  PYTHON AND RUST / SOUNDINGS IN COMMITS · DATUM: MAIN / CHART NO. 21 · EDITION 0.1.3 · NOV 2025 · IALA REGION B /
  CORRECTED THROUGH NOTICE 9, source diagram (470,548) with A/B/C key (undated: `sources[].first` is null).
  Outside the neat line: SOUNDINGS IN COMMITS top-centre (the one `label-caps` run), chart number 21 top-right,
  folio bottom-left, imprint bottom-centre, `SMALL CORRECTIONS 2026 — 169, 170, 171, 172, 173` bottom-right.
- **Name/thesis**: "Ben Russell" display 176 (hand-kerned by typeset), thesis once in serif-italic 36.
- **Opening** (`tl.cue("opening",0,4.0)`): contours deep-first `draw_in` 0.2+0.12·i (1.6 s), tints 1.0/1.3, land
  + coast + danger + PA + ⚓ + box + course 1.6, soundings 1.4+0.04·k in course order, contour figures 1.4, rose
  card settles 2.0 (rotate 12 → −4 → 0, sea), names/heights 2.2+0.1·rank, Ben/Russell `reveal` 2.5/3.0, thesis
  3.1, title block + captions 3.3, bearings/mark labels/fix dates/pencil note 3.6, boat revealed at 4.0.
- **Boat**: `tl.sail(smooth_path(course), 4, 24, n=64)` on the hull/sails split of `SLOOP_DETAIL` (hull ink, main
  accent, jib paper), `Sail.wrap(pitch −4)`, faces west by mirror, no tacks, anchored forever at 28 s. After 28 s
  the sheet carries nothing continuous; the light pair is the only loop (1.0 repaint/s).
- **Still** = the t = 95 s state (frames at 28.1 and 95 match the still: changed 0.00 %).
- **Night**: THEMES["night"], lights with magenta halos the brightest things (light_core L .97 > ink L .82).
- **Phone** 720×900 redrawn at s = 0.55 through one affine map of the desk layout (features, course, marks,
  basin, band), field re-solved in phone space; islets under 12 commits culled (7), 11 soundings, four names
  (26/30 px), spot heights 26 px for the named, 18 px texture for the rest, rose r 56, band x 600 → 720 with
  SOUNDINGS THINNED, four title lines at 26, boat = `sloop-glyph` ×1.4 plotted as **7 discrete fixes** every
  4 s (4–28 s) leaving ⊙ marks; lights lit, not flashing (see deviations).
- **No-sounding**: caps pencil note `NO SOUNDINGS TONIGHT — FIGURES AS SURVEYED 7 OCT 2026` under the title block
  (phone: above it). Verified with `--no-sounding` builds.
- **alt**: "Chart of Ben Russell's 21 repositories, titled: I survey a web that is wrong about itself. Right
  margin unsurveyed. A boat sails in and anchors." (25 words; poem line unchanged).
- Report hook: `features[]` (ratio, drawn_ratio, r, kind, centre), `bracket_failures`, `lights[]`,
  `symbols_used`, and a `hero{field, place, unclosed, bracket, soundings_printed, culled, sail}` block.

## 2. T2 §5 acceptance criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | grep `ILLUSTRATIVE|PENDING|SEEDED|NOT FOR NAVIGATION` → 0; build fails without `weeks` | **pass** | `test_no_banned_strings_or_elements`, `test_refuses_to_invent_weeks`; `check.py strings` 0 findings |
| 2 | area ±8 % every feature; 5/10 polygons closed; pairs ≥ ri+rj+44; course ≥ r+30 | **pass** (course ≥ r+66) | ratios 0.978–1.027; `closed_check` lists one open 10-contour of 2187 px (the corridor's, open into the band fade — by design); min pair clearance 44.5, min course clearance 73.9 |
| 3 | every water numeral bracketed; changing a week changes the numeral and contour | **pass** | bracket failures 0 (desk); soundings are kernels, so a week changes the field |
| 4 | no semantic run < 13 (phone 26); soundings 11/18; title block inside x 70–610, y 540–670; three accent objects none within 120 px of y 222 | **pass** | `check_type` clean on all eight; `test_type_rules`, `test_three_accent_objects_clear_of_the_name` (arrowhead y≈75, nun 551, sail 556) |
| 5 | night: max L(lit) > max L(text); ΔE under CVD | **pass / not measured** | light_core #F8F5EE vs night ink #BBC5D1 by token; CVD simulation is T10's contrast plug-in |
| 6 | perf: repaints ≤ 1/s after warm-up; still 0; filmstrip finished; 360 px DPR 3 | **repaints pass, ms/frame fails the 8 ms cap** | hero-day: 1.0 repaints/s, 35 ms/frame; still 0 repaints; hero-phone 0.25 repaints/s (16 s window; 0.30 with a 10 s window: window quantisation of a 4 s cadence), 13 ms/frame — see §4 |
| 7 | < 300 KB raw, phone < 120 KB, XML valid, bounds clean | **pass** | sizes below; `check.py xml` 0 findings; bleed only the band |
| 8 | 360 px: name, thesis, two outlines, one light recoverable; alt ≤ 25 words | **pass** | `phone-360.png`; alt 25 words |

MASTERPLAN §2.1 instants: `render.mjs frames` on hero-day vs hero-still-day — t 0.5 coverage 0.414, t 2 0.822,
t 4.1 1.002 (changed 0.08 %), t 28.1 1.000 (0.00 %), t 95 1.000 (0.00 %). Phone: 0.487 / 0.704 / 0.999 / 1 / 1.
Silhouette desk vs phone L1 0.433 (≥ 0.25). `checks/motion.py`: 0 findings on all eight files.
`check.py --dev --tier fast` on assets/v9 (hero only present): 0 fail, 1 warn (POSITION-EMPTY, not mine).
Full suite: `tests.test_hero` 15/15 OK; the suite's 5 failures + 1 error are in `test_approaches` /
`test_supporting` (other builders, in progress).

## 3. Sizes and perf per edition (assets/v9, final)

| edition | raw KB | gz KB | elements | glyph defs | motion class | indefinite | repaints/s |
|---|---|---|---|---|---|---|---|
| hero-day | 167.7 | 39.0 | 1311 | 111 | lights | 2 | 1.0 |
| hero-night | 165.8 | 37.2 | 1311 | 111 | lights | 2 | 1.0 |
| hero-still-day | 153.1 | 37.5 | 1144 | 111 | still | 0 emitted | 0 |
| hero-still-night | 151.2 | 35.7 | 1144 | 111 | still | 0 emitted | 0 |
| hero-phone-day | 105.0 | 26.8 | 661 | 70 | frozen after 28 s | 0 | 0.25 (4–28 s) |
| hero-phone-night | 106.0 | 26.5 | 662 | 70 | frozen after 28 s | 0 | 0.25 |
| hero-phone-still-day | 97.1 | 26.2 | 568 | 70 | still | 0 | 0 |
| hero-phone-still-night | 98.1 | 25.9 | 569 | 70 | still | 0 | 0 |

Budget: ≤ 170/60 KB, ≤ 3000 elements, phone ≤ 120 KB — all met. Two builds byte-identical (test + `cmp`).
Perf (Chromium, `perf_check.js`): hero-day `--warm=30 --seconds=10`: repaints 1.0/s, raster 27.4 + paint 7.7 =
35.1 ms per repaint, cpu 3.7 %, maxFrame 9.7 ms. Removing any single layer (text, tints, hatch, grain, vignette,
gradient) does not move ms/frame outside noise (31–49 ms): the cost is the whole-sheet re-raster Chromium does
for an SVG-in-`<img>` on every SMIL change, not one layer. hero-phone 360 px DPR 3 `--warm=6 --seconds=16`:
0.25 repaints/s, 13.0 ms per repaint. hero-still-day: 0 repaints, pass.

## 4. Deviations (each deliberate; `BREAKS` in the module lists the lettering ones)

1. **Land names in condensed caps, water names in serif italic.** With ~550 B per serif glyph, any set carrying
   serif names for both land and water exceeds D's 40 KB glyph-defs budget (measured 43–56 KB for every
   serif-both variant; the budget fails the build). Land names are upright caps in `label` (17 px for r ≥ 40,
   else 13), water names `place-water` 17 italic. The slant rule holds (upright = land/measured, italic =
   water); the serif stays for the chart-maker's voice (name, thesis, shoal names, pencil note). Defs: 36 KB.
2. **Role line in condensed caps 13, ink** (not serif-italic 22): the 22 px inline run cost 32 KB raw and a
   `text_use` set another size key; decision 7 calls it the plain register, and the chart's own face is plain.
3. **Caps lines through role `label` + tracking 0.6 (phone 1.0)**; one true `label-caps` run (the unit line;
   folio exempt by key). `check_type` allows one label-caps run per sheet.
4. **Sounding rows ±18/±36 (not ±24/±48)** and **slots moved**: game_engine (816,344), rustmapper (1022,508),
   Data_science_dev (992,636), so every non-harbour feature keeps ≥ r + 66 from the course (rows 36 + h_snd
   30): a sounding kernel can then never dig a feature's 5-ring, and the area law is drawn, not just solved.
   `CLEAR_COURSE = 66` for Halton features too. Soundings stop 70 px short of WP4; nothing is sounded on the
   harbour's own ground (the basin is the harbour's, Delta Lake). Decision 1's waypoints, marks, basin
   position and coverage box are kept.
5. **Base 10.5 means the sounded corridor is tint B**: 36 of 52 weeks are 0, so the course runs through
   under-5 water with "0" soundings and deep pits at the sprint weeks (240, 296, 358). This is the data; it reads
   as a sounded bank, and the honesty rule says not to smooth it.
6. **No margin graticule** (T2 §2.8 lists labelled meridians/parallels): the sheet has no coordinates; labelled
   ticks would be invented geometry. Minute bars carry the frame.
7. **Islets (r < 16, under ~25 commits) unnamed**: spot height only; 21 serif names would collide.
8. **Phone lights lit, not flashing**: MASTERPLAN 7.3's hero-phone gate (≤ 0.25 repaints/s after 6 s) cannot
   hold with two Fl 4s lights (1/s). The phone shows the lights as a printed chart does (lit), labels culled; the
   phone's only motion is the 4 s opening and the 7 fixes.
9. **Phone culls**: no bearings, fix dates, mark labels, coverage box, PA outline, pencil note, imprint,
   corrections, source diagram, outside-neat-line captions (a 14 px margin cannot carry 26 px type; the CHART NO.
   line sits in the title block).
10. **Top-right outside the neat line prints the chart number (21)**, as spec-hero §1 / STANDARDS 4 ("chart
    number repeated outside the neat line"); decision 27's wording says "notices count N". The notice count is
    in CORRECTED THROUGH NOTICE 9. Flagging for the orchestrator; one constant to flip.
11. **Pencil note "sitemap.xml lies again" without "see Notice 3"**: chart.toml's five notices carry no sitemap
    item; tying it to Notice 3 ("Lights before speed") would be an invented tie. Copy question for T8.
12. **SEE SHEET 3 inside the box, top-left (687,484)** instead of decision 1's (894,476), which lands in the
    sounding rows.
13. **Line widths at night not ×0.85**: `stroke()` emits tokens.W only (engine).
14. **Sounding fades without the 3 px rise** (opacity only): 42 translates cost 6 KB and pushed the desk file
    over the 170 KB target.
15. **Small corrections print correction numbers** (`corrections[2026][-5:].n`), the real small-corrections
    grammar, not dates.

## 5. Needs / proposed patches (files I do not own)

- **chart.toml `[[features]]`** — add names for the other named slots so the chart does not derive them:
  `repo="game_engine" aliases=["Game Engine I."] slot="island" kind="island"`,
  `repo="Data_science_dev" aliases=["Data Science Bank"] kind="shoal"`, `repo="FashionDB" aliases=["FashionDB Bank"]`.
  Today hero.py derives "Game Engine I.", "Data Science Dev Shoal", "FashionDB I." from the repo names.
- **typeset `BUDGET["defs_kb"]` (D)**: 40 KB is below what one serif register for place names costs on the hero
  (serif names for land and water = 43–56 KB). Proposal: `BUDGET = {"glyph_defs": 160, "size_keys": 6,
  "defs_kb": 40, "defs_kb_hero": 56}` read by `check_budget(sheet=None)`. Until then land names are condensed caps.
- **perf_check.js (E) / MASTERPLAN 7.3**: the 8 ms/frame cap "while moving after its opening" is applied to the
  hero's discrete light flashes; a full re-raster of a 1300-element sheet costs ~35 ms once per second (3.7 % CPU)
  and no layer removal changes it. Proposal: apply the ms/frame cap only to continuous windows (`class ===
  'footer'` or during the sail), and evaluate hero-phone over a window that is a multiple of 4 s (10 s samples a
  4 s cadence as 0.30/s). I cannot change E's harness; the repaint counts (the gate's own words) pass.
- **render.mjs 7.2 gate**: "hero ≥ 0.6 coverage at t = 0" cannot hold with §2.1's tints at 1.0/1.3 (tints are
  most of the still's ink); t = 0.5 measures 0.41, t = 2 0.82, t = 4.1 1.00. Suggest ≥ 0.35 at t = 0, rising.
- **tests/test_supporting.py `test_512_is_never_upright`** scans every sheet in its report; the hero prints
  game_engine's measured commit count, which is exactly 512 (`key="commits:game_engine"`, sub 1). Suggest
  exempting keys starting with `commits:`/`week:` (measured counts) or restricting the test to its own sheets.
- **chartlib (B), optional**: `draw_contours(every=)` per contour length would save the two-pass call;
  `lit_core` could take the flash string and inject it itself so sheets need no `_inject`.
- **T8**: the pencil note copy (deviation 11); the role line is now caps condensed on the sheet.

## 6. PNGs inspected (all under `…/scratchpad/crit/build/H/`)

`still-day.png`, `still-night.png`, `still-day-2x.png`, `still-night-2x.png`, `crop-entrance-2x.png`,
`crop-entrance-night-2x.png`, `crop-rose-band-2x.png`, `crop-title-2x.png`, `phone-still-day.png`,
`phone-still-night.png`, `phone-360.png` (360 px DPR 3), `frames/strip.png` + `frames/frame-{0p5,2,4p1,28p1,95}.png`
(day vs still), `frames-phone/strip.png` + frames, `nosound/still-day.png`, `nosound/crop-note.png`,
`hero-day-95.png` (an early t≈0.4 shot). Build reports: `build-report.json`, `nosound/build-report.json`,
perf rows `perf-day.json`, `perf-phone.json`, `perf-phone16.json`, `perfvar/*.json`.

## Summary

1. `scripts/sheets/hero.py` builds all eight hero editions from the real stats with zero runner problems; `assets/v9/hero-*.svg` and the report are written.
2. The field is honest: 52 weeks as kernels, depth = count, base 10.5, 21 features with area ∝ commits within 0.978–1.027 (drawn and solved), 0 bracket failures, every repo charted.
3. Motion follows §2.1: 4 s opening, sail 4–28 s, two Fl 4s lights the only loop (2 indefinite, 1.0 repaint/s), stills frozen and pixel-identical to t = 95 s; phone plots 7 fixes and keeps 0.25 repaints/s.
4. Budgets met: 167.7/39 KB desk, 105/27 KB phone, ≤ 1311 elements, deterministic, `check_type`, motion lint, xml and strings checks clean.
5. Deviations are lettering and clearance decisions forced by the 40 KB glyph budget and the real data (land names in condensed caps; slots and rows moved so soundings never dig a feature); each is listed in `BREAKS` and §4.
6. Open for others: raise the hero glyph-defs budget or accept caps land names; the 8 ms/frame cap and the t = 0 coverage gate conflict with the plan's own timeline; three `[[features]]` names for chart.toml; the 512 test scope.

---

# Round 2 (orchestrator crit + addendum)

Files changed: `scripts/sheets/hero.py`, `tests/test_hero.py` only. Rebuilt into scratch and `assets/v9/`
(byte-identical, 0 runner problems). chart.toml's new `[[features]]` names are read from cfg
("Game Engine I.", "Data Science Bank", "FashionDB Bank"; `kind = "bank"` reads as shoal, so FashionDB is now a
bank/shoal although dormant — cfg wins, flagging it).

## What changed, point by point

1. **Bubble chart → coastlines.** Every feature is now its main kernel plus 3–6 sub-kernels from `_lobes()`:
   positive lobes on a dominant side (land kinds) and negative dents on the lee side (all kinds), positions and
   supports scaled by the current r, `Jitter(seed, "hero/lobes/<repo>")` (never by data), passed to
   `Field.from_soundings(extra=…)` and re-generated inside the builder on every solve step. The harbour is exempt
   (its bay is its character; lobes put the hull's stern on the coast). `solve_radii` measures the drawn 5-polygon
   with the lobes in, so area ∝ commits still holds: desk ratios **0.972–1.061** (the 1.061 is an r 8 islet, grid-
   limited; ≥ 10 px features all within ±3 %), drawn ratios 0.946–1.031, phone 0.984–1.029; the ±8 % assertion stays.
   **10-contours generalised**: closed 10-rings shorter than 520 px (phone 280) are neither drawn nor tinted, so
   the 10-line runs once around the working ground (Game Engine, the sounded bank, rustmapper, Data Science Bank)
   and the small features carry tint B only. BREAKS entries "Lobed features", "Contours generalised".
2. **The tube → a bank (option b + a).** The course threads between Game Engine I. (NW of the leg) and rustmapper
   (SE) into the harbour; h_snd 36 (not 30) with the rows cycling −36/+18/−18/+36 ± 5 px jitter keyed by index.
   Amplitudes stay solved (every printed figure is the field's own value: option c rejected). The zero weeks now
   form one broad irregular shallow bank whose 10-line merges with the islands' shelf. Defended in BREAKS
   ("Sounded bank softened, not smoothed"). Clearance rule raised to r + 78 (rows 36 + 5 + h 36) so a sounding
   kernel never digs a feature's 5-ring; rustmapper slot → (1030, 516), min course clearance 78.7.
3. **Composition.** The unslotted features are strung along a SW–NE arc (`ARC`, `_place_on_arc`: alternating
   sides, offset r + 26 (+40 per lap), jitter by repo name, every candidate checked against drawable, exclusions
   (margin r + 12), pairs (44, islets 30) and the course; Halton fallback — unused today). Reads: title NW,
   archipelago rising SW → NE, harbour SE, working ground and band E. The phone has its own arc (`PHONE_ARC`).
   All 21 placed on the desk, 15 on the phone (islets < 12 culled), none dropped.
4. **Collisions.** Lettering positions are decided before the contour figures: `boxes` holds every sounding,
   spot height and name; `contour_labels` takes them as exclusions; a name below that lands on a neighbour's disc
   (rect-vs-disc test, inflated 1.15 r) or another box flips above, then left, then right; names never enter the
   band. Land names: on the land for r ≥ 40 (17 px caps), offshore below the 5-ring for 16 ≤ r < 40, spot height
   on the land; big shoals (Profile, Data Science Bank) carry name and height inside. Bearings sit 54 px off the
   leg (outside the sounding rows), on the side and at the distance (54/66/78) that clears every box; 235° found
   no clear place and is omitted (233°, 208°, 290° stand). "OCT 2025" lifts in 6 px steps until clear of the
   sounding figures; PA moved to the west edge of the pecked outline; pencil note at (910,558). Rotated labels
   are now anchored at their start so typeset's registry matches the drawing (see §needs). The new
   `checks/bounds.py` reports **0 FAIL** on the hero (20 `BOUNDS-TEXTURE` warnings: the 52 soundings are dense in
   the approach — data).
5. **The boat.** Anchored in basin water: a third basin kernel (768,556,h 22, −0.5·base) under the berth, the bay
   (779,557,h 30, −2.0·base) and the mouth (806,567,h 26, −0.66·base); the build asserts land at the harbour
   centre and water at WP5 and at both hull ends. Detail sloop at **0.7** (`BOAT_SCALE`), hull/sails split and the
   R/G marks unchanged.
6. **512 upright** stays (measured commits, key `commits:game_engine`); chart number top-right kept.
7. **Addendum — title and land static at t = 0.** Name, thesis, title block, imprint, captions, frame, rose, band,
   land fill, coastlines, vignette, anchorage, coverage box, station and every feature name/height are present at
   load with no animation; the water draws in: contours deep-first (draw_in 0.2 + 0.12·i), tints 1.0/1.3, danger
   lines + PA + course 1.6, marks (with their lit cores) 1.6, soundings 1.4 + 0.04·k in course order (k = printed
   index; phone 0.06), contour figures 1.4, rose settle 2.0, bearings/mark labels/fix dates/note 3.6, boat 4–28.
   Opening cue still ends at 4.0; `continuous_windows` [[0.2, 28.0]] desk, [[0.2, 4.0]] phone. BREAKS entry
   "Title and land static at t=0 (five-second test; 7.2 t=0 floor)". Still = t 95 s unchanged.
   Thesis baseline moved 296 → 306 (phone 212/258 → 222/268) so its metric box clears the display box.

## Gates (final)

| gate | result |
|---|---|
| build_assets (8 editions) | 0 problems; scratch and assets/v9 byte-identical (cmp) |
| checks/motion.py | 0 findings |
| check.py --dev --tier fast (hero) | 0 FAIL; 20 WARN BOUNDS-TEXTURE (sounding density); other sheets' findings not mine |
| tests | `tests.test_hero` 15/15 OK; full suite 178 tests OK |
| perf hero-day (--warm 30 --seconds 10) | 1.0 repaints/s, 30.2 ms per repaint, cpu 3.2 %, **pass** |
| perf hero-phone-day (360 px, DPR 3, --warm 6 --seconds 16) | 0.25 repaints/s, 12.3 ms, **pass** |
| perf hero-still-day | 0 repaints, pass |
| frames vs still (desk) | t 0: coverage **0.665**, t 0.5: 0.666, t 2: 0.993, t 4.1: 1.000, t 28.1: 1.000 (0.00 % changed), t 95: 1.000 |
| frames vs still (phone) | t 0: 0.796, t 2: 1.001, t 4.1 / 28.1 / 95: 1.000 |

Sizes: hero-day 163.5 / 38.9 KB, 1257 el; night 161.4 / 37.1; still-day 152.4 / 37.7 (1136 el); still-night
150.4 / 35.9; phone-day 102.1 / 26.9 (602 el); phone-night 103.1 / 26.7; phone-still 97.4 / 98.4 KB. Glyph defs
113 desk / 71 phone. Area: 21 features, ratios 0.972–1.061, drawn 0.946–1.031; bracket: 3 `unresolved` (rings
under the grid), 0 field/polygon; 42 soundings printed.

## Needs / notes for others (round 2)

- **typeset (D)**: `_register()` rotates the run's box about `(x0, y)` — the run's *start* — while the drawn
  `rotate(a x y)` is about the anchor point, so a middle-anchored rotated label is registered 0.5·width away
  from where it is drawn (LIMIT OF SURVEY was logged 76 px west). Patch: in `_set()`, pass the anchor point to
  `_register` and rotate about `(x, y)` instead of `(x0, y)`. I work around it by anchoring rotated labels at
  their start (`up()` helper).
- **checks/contrast.py**: reads `lights[].color` as the lit colour; the hero now reports the light core
  (`#F8F5EE`) there and the buoy body under `body`.
- **chart.toml**: FashionDB `kind = "bank"` makes a dormant repo a shoal; if the data rule should win, drop the
  kind and keep the alias.
- Sounding density in the approach (20 BOUNDS-TEXTURE warnings) is the 52-week series on a 348 px span; only a
  longer course or fewer rows would thin it, both against decision 1 / MASTERPLAN 17.

## PNGs inspected (round 2)

`…/H/r2-still-day.png`, `r2-still-night.png`, `r2-phone-still-day.png`, `r2-phone-still-night.png`,
`r2-still-day-2x.png`, `r2-crop-entrance-2x.png`, `r2-crop-archipelago-2x.png`, `r2-crop-rose-band-2x.png`,
`r2-phone-360.png`, `frames/strip.png` + `frames/frame-{0,0p5,2,4p1,28p1,95}.png`, `frames-phone/strip.png`,
`nosound/r2-still-day.png`.

## Summary (round 2)

1. Islands are lobed and dented by name-seeded sub-kernels, no two alike; the 10-line wanders once around the working ground; small features carry tint B only; area ∝ commits holds on the drawn polygons (±3 % for every feature over 10 px, all within ±8 %).
2. The sounded bank threads between Game Engine I. and rustmapper into the harbour with h 36 and jittered rows — a shoal area, not a road — and the figures stay the field's own values.
3. The small features sit on a SW–NE archipelago arc; all 21 charted; names on the land or offshore, bearings and labels clear of every box (bounds plug-in 0 FAIL, only sounding-density warnings).
4. The sloop is 70 % and anchored in basin water asserted at both hull ends; R/G marks unchanged.
5. Title, land, names and band are static at t = 0 (coverage 0.665 desk / 0.796 phone); only the water draws in; opening ends at 4.0; boat 4–28; still = t 95.
6. All gates pass: 8 editions 0 problems and byte-identical, motion lint 0, perf 1.0 repaints/s desk / 0.25 phone, 178 tests OK; files 163.5/38.9 KB desk, 102.1/26.9 KB phone.

Note for the orchestrator: `assets/build-report.json` is shared and `build_assets.py --sheets <one>` rewrites it
with that sheet only; at hand-back it listed the footer's six entries (builder S's last run), so `check.py` flags
the hero files REPORT-MISSING until a full `python3 scripts/build_assets.py` runs. The hero SVGs in `assets/v9/`
are the final ones (byte-identical to the scratch set in `…/H/`, whose `build-report.json` carries the hero entries).
