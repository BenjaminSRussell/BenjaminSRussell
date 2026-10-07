# T2 — Hero sheet ("Chart No. N", Sheet 1)

Base: spec-hero.md. Where this section is silent, spec-hero stands; where it speaks, it overrides. Canvas 1280 × 740, neat line 18/24, drawable water (24, 24, 1232, 692). Coordinates in 1280-space, emitted as integers (per 12).

## 1. Decisions

1. **Era: late paper chart, c. 1985–2000.** Nothing pre-1950 except the 176 px display serif of the name; written into DESIGN.md (per 13).
2. **Open, centre-stacked title block, no frame**; imprint and small-corrections line go **outside the neat line** (per 13). The boxed cartouche and URL scale bar are deleted (per 08: it measured nothing).
3. **"NOT FOR NAVIGATION" deleted** (per 13, 34, 02); datum, edition and the upright/italic convention carry honesty.
4. **Rustmapper Shoal drawn twice**, as charted from the sitemap (dotted, `PA`) and as surveyed (tinted, danger line), captioned only by the pencil note (per 28, 22).
5. **Soundings generate the contours**: the 52 weekly totals are field kernels along the course with amplitudes solved so the field at each sounding equals its printed value; no filler blobs, no sine wallpaper (per 08, 14).
6. **One unit per field** (per 08): water carries commits/week; each feature one spot height, commits with a legend-defined subscript (per 13); 512/256 move to Approaches, followers leaves the sheet (per 32).
7. **Area ∝ commits is asserted**: every feature cut at the same level, compact kernels, two Newton steps, build fails outside ±8%; counts are Ben's own commits (per 08, 32).
8. **Read order name → thesis → edge** (per 28): rose demoted to ticks + N, opaque quiet tints, UNSURVEYED band x 1080→1280 as the only pattern-like fill, hand-ruled (per 14).
9. **Three accent objects**: arrowhead, nun, sail; none within 120 px of the name's baseline. Lights are magenta (per 15), so they do not count.
10. **Rose: 00 at top, numbered; bars = commit-days per hour in the author's local offset; variation is one arrow** (per 08, 32). No rotated dial, no "works at night".
11. **Hero motion is change-only** (per 12, binding): opening ≤ 4.6 s, boat sails in once as sampled `animateTransform` and holds forever; two discrete lights are the only loop. Out-and-back is cut; the footer is the ambient sheet.
12. **Profile repo stays** as *Profile Shoal* with the △ station (per 34, against 36): the chart counts itself.
13. **Rustmapper Shoal keeps its name** (against 17): features are named for the ship that surveyed them; the boat *is* rustmapper.
14. **Slant stays the certainty convention** (per 02, 07, STANDARDS 1); 13's soundings are honoured as *condensed*, not slanted; the subscript is adopted.
15. **"SOUNDINGS IN COMMITS" top-centre outside the neat line, in ink** (13's unit caution loses to 28's accent budget; the words still sit where the metaphor is declared).
16. **Phone edition 720 × 900 portrait**, floor 26/18/120, boat plotted in discrete fixes (per 10, 12).

## 2. Design and implementation

### 2.1 Composition

| Element | Position | Spec |
|---|---|---|
| Name | x 64, baseline 222 | "Ben Russell" `serif` 176, tracking −3; hand-kern `Ru` −20, `ss` +2 (per 07) |
| Thesis | x 72, baseline 296 | "I survey a web that is wrong about itself." `serif-italic` 36 (scale size; one line in every edition), ink2 |
| Calm zone | (40, 40, 800, 280) | no feature centres, no soundings |
| Title block | centred x 340, baselines 560–656 | §2.2; build asserts every run inside x 70–610 |
| Rose | centre (1000, 160), r 72 | §2.5; exclusion (920, 80, 160, 195) |
| Harbour | (760, 560) | land + basin; coverage box (690, 480, 170, 150) hair dash `6 3`, "SEE SHEET 3" 13 at (862, 486) (per 26) |
| Unsurveyed | x 1080→1280, y 150→580 | §2.6 |
| Outside the neat line, `caption` 13 muted | top-right (1262, 14) `N`; top-centre (640, 14) SOUNDINGS IN COMMITS; bottom-left (24, 735) CHART NO. {N} · SHEET 1; bottom-centre (600, 735) imprint; bottom-right (1256, 735) small corrections | Imprint: "Published at github.com/BenjaminSRussell · {d Mon YYYY} · superintendence: build_assets.py". Corrections: "Small corrections {YYYY} — {m.dd}, …" = last five commits touching `assets/` |

**Course** (seaward → harbour), verified ≥ r+30 from every feature except the harbour it enters: WP1 (1136, 296) in the band · WP2 (1046, 360) off Rustmapper Shoal · WP3 (900, 470) · WP4 (812, 508) entrance · WP5 (776, 556) anchorage ⚓ "Delta Lake". Bearings 235° · 233° · 247° · 217°, `caption` 13, 12 px off the leg away from the nearest feature. Stroke PEN 1.1, dash `0.1 7` round caps, seeded dashoffset (per 14). Waypoints are fixes ⊙ (r 4); WP2 and WP4 carry the only two fix labels, "OCT 2025" and "SEP 2025" (first commit of the feature each is taken off; measured, upright) (per 26, 28).

### 2.2 Title block (verbatim; `caption` = 13 caps, tracking 0.8, muted unless noted)

```
y 560  THE OPEN WEB · FROM SURVEYS {first_year}–{updated_year}        caption, ink
y 590  Crawl and data infrastructure · Python and Rust                  serif-italic 22, ink2 (T8 confirms)
y 616  SOUNDINGS IN COMMITS · DATUM: MAIN
y 636  CHART NO. {N} · EDITION {version} · {Mon YYYY} · IALA REGION B
y 656  CORRECTED THROUGH NOTICE {notices_count}
```
Right of it, the **source diagram** at (470, 548) 120 × 68 as spec §1, but each area **dated** (per 34): key lines "A  SITEMAPS · {first}–", "B  CT LOGS · {first}–", "C  COMMON CRAWL · {year}" from T7 `sources[]`; a source without a date prints without one. The stray A/B/C letters on the chart are cut (per 28).

### 2.3 Archipelago

**Input** per repo (T7): `alias, commits` (author-filtered), `months_active, first, last, weeks_active_12, shelved`.

**Radius** `r = 3.2·√commits`, clamp [6, 90]; area target π r² = 32.2 px² per commit. Today: game_engine 77, Scrapy 58, Data_science_dev 55, profile 42, Rust-sitemap 36, FashionDB 26 … cozy-game 8.5.

**Kind** (first match): `wreck` if shelved → `harbour` if alias = scrapy → `islet` if r < 16 → `shoal` if `weeks_active_12 ≥ 3` (32's "active") → else `island`. Fallback without per-repo weeks: shoal if `last` within 90 days of `updated`.

**Kernel.** Replace the Gaussian with the compact bump `W(q) = (1 − q²)³`, q = d/h, zero beyond h, so features and soundings never leak into each other. Amplitude A = 1.3 (shoal, islet) or 5.3 (island, harbour); support h = r/q_b where A·W(q_b) = 0.44 → h = 1.82 r (shoal), 1.33 r (island). The 0.44 polygon therefore sits at distance r by construction: the **danger line** of a shoal, the **outer tint edge** of an island; island coastline (LAND 1.5) at 0.78 r, tint B (1.1) at 0.85 r / 0.42 r. **Assertion:** area(0.44 polygon)/(π r²) within ±8% after two Newton steps on h, else the build fails. Field × edge falloff (smoothstep to 0 over 24 px inside the drawable rect and over x 1040→1080); assert all 0.44 and 1.1 polygons closed.

**Levels** (chart intervals, per 13): 0.11, 0.22, 0.44, 1.1 labelled **5 · 10 · 20 · 50** commits (level = label/45.5); LAND 1.5 is the unlabelled coastline. Figures in a break of the line (T6 `contour_label`), 11 condensed upright, on polygons with perimeter ≥ 120 px. Tint A fills ≥ 0.44, tint B ≥ 1.1, opaque (§2.7), land last, coastline 1.3 with the SE offset pass (per 14).

**Harbour basin.** Two negative kernels (790, 540, h 24, −1.5) and (810, 520, h 24, −1.5) open the basin NE toward WP4; assert F(760,575) > 1.5 and F(790,540) < 0.44.

**Slots keyed by alias** (chart.toml, per 36), rank fallback in this order:

| alias | chart name | kind | centre |
|---|---|---|---|
| scrapy | Scrapy Harbor (upright) | harbour | (760, 560) |
| rustmapper | *Rustmapper Shoal* | shoal | (1004, 482) |
| game_engine | Game Engine I. (upright) | island | (838, 376) |
| data_science_dev | *Data Science Bank* | shoal | (990, 628) |
| profile | *Profile Shoal* + △ | shoal | (330, 405) |
| fashiondb | *FashionDB Bank* | shoal | (640, 420) |

Pairwise `d ≥ ri + rj + 44` holds for today's six (tightest: Game Engine–Scrapy 197 ≥ 179). Others by r descending through the Halton search (seed 2709): inside drawable minus exclusions (calm zone, title block + 16, rose box, band x ≥ 1080, coverage box) by ≥ r+28; ≥ ri+rj+44 from placed features; ≥ r+30 from the course; islets biased x > 600. go_go_go is no longer force-placed. A missing alias fills by rank and surfaces as a diff in `layout.lock.json` (T1). Wrecks fixed at (1040, 300), (905, 440), (1050, 680), (676, 668): S-4 hull-and-mast (per 31), dotted circle r 11, `Wk 'YY` 13 italic.

**Names** `serif` 17 upright (islands) / `serif-italic` 17 (shoals), centred +4 below centre (07's floor; 15 px was under the hairline). **Spot height** inside each feature: `{commits}` with `{months_active}` as subscript, 13 upright, e.g. 331₁₃, 585₁ — defined once in the legend (T3): "331₁₃ · commits, months with a commit". The sprint reads as a sprint.

### 2.4 Double shoal and soundings

**As charted / as surveyed.** Rustmapper Shoal's 0.44 polygon is drawn again translated (+24, −14): dotted 1.1 px, ink .45, no tint, `PA` 13 italic at its NE edge (position approximate, real S-4 grammar). One pencil note, `serif-italic` 17 muted, rotated −7° at (960, 420): "sitemap.xml lies again — see Notice 3", 30 px leader into the gap. The Notice 2 note is cut (per 28).

**Open-water soundings are the 52 weeks.** Course arc length 449 px; four rows at −48, −24, +24, +48 from the course; week i (oldest first) at arc position i·L/52, rows cycling, so the oldest sit seaward in the band and the four newest ring the anchor. 11 px condensed, upright, ink .75 day. Each sounding is a bump kernel, h = 30; amplitudes solved from `Σ_j a_j W_ij = n_i/45.5 − F_features(p_i)` (52 × 52 dense solve), capped so open water never exceeds 1.4: a 300-commit week is a shoal, not land, and still prints 300. **Test:** point-in-polygon against the emitted contours, each numeral n inside the band labelled ≤ n and outside the next (≥ 50 inside the 50 contour); on a near-tie (|F − level| < 0.02) the sounding nudges 4 px along the course and the test reruns. Opacity .75 → .40 over x 1000→1080, none at x ≥ 1080. West of x 600 there are no water soundings and so no contours: unsounded water is blank, the honest convention and the calm the name needs.

**Source.** T7 builds `weeks[52]` from clone timestamps (author-filtered), overwritten by the GraphQL calendar when present. Without either the build fails and the published SVG stays up; no even-spread fallback (per 32).

### 2.5 Rose

Centre (1000, 160). Outer r 72, 1 px, ticks every 10° (6 px) and 30° (11 px), "N" 13 at r 86 opacity .6, no numerals, 10 px accent arrowhead at 000. Inner r 50, 0.6 px: 24 bars inward, width 2, length `4 + 24·v[h]/max(v)`, v = `hours_days_local[24]`, **00 at top**, numerals 00/06/12/18 at 13 inside the ring; one PEN arrow centre → modal hour. One line below, `caption` 13 centred (1000, 266): `VAR {hh}h (2026) · AUTHOR'S LOCAL TIME`, plus ` · {±k}h FROM 2025` only when 2025 holds ≥ 60 commit-days (13's annual change, computed or omitted). The colophon explains the clock once (T8). Settle on load: rotate −12 → 4 → −1.5 → 0, 1.6 s `sea`, begin 0.3 s, freeze; no 96 s swing.

### 2.6 Lateral marks and margin

Entrance only, Region B. Last leg heads 217°, so starboard returning is NW: **R "2" nun** (cone, red) at (793, 494), **G "1" can** (rect, green) at (831, 522); outline PEN 1.1, canted `rotate(8)`, position circle r 1.2 at the waterline, no underline (per 31); bodies 12 / 11 × 13 px (per 15). Labels 13 italic (floating things slope, per 07): `R "2" Fl R 4s` above, `G "1" Fl G 4s` below. Light = 3 px core; flash `opacity` discrete `1;0` keyTimes `0;.1` dur 4 s, G at `sail.begin`, R at `sail.begin+2s` → 1 repaint/s.

**Band** x 1080→1280, y 150→580, bleeding to the sheet edge; `border(gap=(150,580))` east. Hand-ruled lines (T6 `hand_hatch`): spacing 8 ± 12%, angle −45° ± 1.5°, ends ± 2 px, stroke 1.0, ink .45, opacity ramp 0 → 1 over x 1080→1120 per line (per 14, 15). Limit line x 1080, 0.8 px dash `6 3`; "LIMIT OF SURVEY {year}" 13 rotated −90° at (1066, 365); "UNSURVEYED" 13 tracking 0.9 rotated −90° at (1200, 365). Contours at x ≥ 1040 go through a clipPath with dash `3 3` and stop at 1150; WP1 and one contour cross into the band (per 28).

### 2.7 Night edition

Adopt 15's OKLCH palette verbatim as opaque `Theme` keys (`shallow_a`, `shallow_b`, `flare`, `light_core`, night `ink` L .82, `ink2` L .62, desaturated land); nothing semantic derived by alpha; day `muted` → `#56657B` (AA, per 09). The name takes night `ink` L .82 like everything else (against 28/27: 15 measured the glare). Night light = `light_core` (L .97) 3 px + halo `<circle r="14">` with a radial gradient in `flare` (no feGaussianBlur, per 11/12) on the same discrete flash, peak .95; anchorage a fixed .25 halo. Line widths × 0.85. Night paper: one radial wipe, warm `#2A3B5A` centre .18 → 0 (per 14); day a 2% warm fall-off to the neat line (per 15). **Assert** max L(lit) > max L(text).

### 2.8 Opening and motion budget (hero only)

t = 0 is a finished blank form: paper, neat line + minute bars, margin graticule labels (two meridians, two parallels; no interior grid, per 13), band, rose rings, "N". Then spec §8's timeline with these amendments, all `fill="freeze"`: four contour levels deep-first at 0.2 + 0.25·i (1.6 s draw); tints 1.0/1.3; land, coastlines, danger lines, PA outline, wrecks, anchorage, coverage box at 1.6; soundings 1.4 + 0.04·k in course order; rose settle 2.0; names and spot heights 2.2 + 0.1·rank; "Ben"/"Russell" discrete at 2.6/2.85; thesis 3.1; title block and outside captions 3.3; bearings, light labels, pencil note 3.6; boat `id="sail"` at 4.0 with the lights.

**Boat.** The 11-command sloop (per 31), hull ink, main accent, jib paper with ink outline, bow right, wrapped in `scale(-1,1) rotate(-4)` (the course runs west; bow-up pitch, no heel, no `rotate="auto"`). `animateTransform type="translate"` with 64 `values` sampled along the smoothed course at eased arc positions (`sea` over the first and last 15%), dur 42 s, begin 4 s, freeze at WP5; a 10 s `sea` swell `translate 0;-2;0` ends at `sail.end`, where a `<set>` levels the trim. ⊙ and labels at WP2/WP4 `<set opacity>` as passed. After 46 s the hero carries **zero** continuous animation; the light pair is its only loop (≤ 1 repaint/s). Reduced-motion edition = end state, every `<animate*>`/`<set>` stripped, boat at anchor.

### 2.9 Phone edition (720 × 900, `media="(max-width: 767px)"`, per 10)

Neat line 14/19. Name 132 at (40, 150); thesis 40 in two lines at (44, 212)/(44, 258); rose r 56 at (620, 330), N + 00/06/12/18, VAR line 26; archipelago at uniform scale 0.545 into y 300→680, features under 12 commits culled, rotated note "small-scale edition · soundings thinned" 26 at the band; 14 week soundings nearest the course at 18; four names at 30; four title-block lines at 26 (THE OPEN WEB / role / SOUNDINGS IN COMMITS · DATUM: MAIN / CHART NO. · EDITION · NOTICE n), baselines 770–868; band x 656→720; one light pair × 1.3; no imprint, corrections, source diagram, PA outline or pencil note. Boat: 7-command glyph at 1.4×, **plotted** as 11 discrete fixes every 4 s (discrete translate), each leaving a ⊙, then hold. Same opening, stagger 60 ms; night-phone text opaque.

### 2.10 Alt text (≤ 25 words, plain, from stats)

"Nautical chart of Ben Russell's {N} GitHub repositories as islands and shoals sized by commits, with a compass, a course and an unsurveyed margin." (24 words.) Marginalia voice moves to the visible `<sub>` caption (T8).

## 3. Interfaces

**Provide:** `sheets/hero.py` with `build`, `build_phone`, `build_still(theme, data)`; `layout.lock.json` (alias → centre, r, kind); timeline ids `sail`, `lt_r2`, `lt_g1`, `rose_settle`, `open_*`; for T3: **entrance faces NE, course enters heading 217°, coverage box (690, 480, 170, 150) "SEE SHEET 3"** — Approaches agrees or carries a north arrow (per 26).

**T7 (data):** `repos[].{alias, commits (author-filtered), months_active, first, last, weeks_active_12, shelved}`, `weeks[52]`, `hours_days_local[24]`, `hours_days_local_2025[24]`, `repo_count`, `edition{version, released}`, `notices_count`, `corrections[]`, `sources[]{letter, name, first, last}`, `updated`; hard failure while `seeded` is true.
**T5 (type):** roles `display 176 · thesis 36 · role-italic 22 · name 17/17i · caption 13/13i · texture 11`; `sounding(n, x, y, sub=None, italic=False, size)` with a 0.7× subscript counted as one 13 px run; grade strokes per edition; hand-kern table for "Ben Russell"; the condensed-face decision.
**T6 (drawing):** `Field` with compact kernels and `solve_week_amplitudes(points, values, offsets)`; `contours(levels)` as relative-integer polylines with `contour_label` breaks; `tint_bands` (opaque); `coast` (1.3 + SE offset pass); `danger_line` (seeded dashoffset); `hand_hatch(rect, spacing, angle, seed, ramp)`; stroke floor 0.8 px (15 over 14); `border(gap=)`; theme keys above.
**T4 (motion):** `sampled_translate(path, n=64, dur, begin, ease_ends)`, `flash_discrete(character, begin)`, `set_at`, the opening scheduler, filmstrip at 0/25/50/75/99% of 46 s, the reduced-motion stripper.
**T3:** legend entries for PA, ⊙ fix, danger line, Wk, △ station, subscript spot height, upright/italic. **T8:** role line, pencil note, colophon sentences (clock; "the chart counts itself"). **T1:** `<picture>` order (reduce+dark, reduce, phone+dark, phone, dark, img); files `hero-{light,dark}.svg`, `hero-phone-*.svg`, `hero-still-*.svg`.

## 4. Build order, effort, risks, omissions

(1) kernels, area assertion, solver 6 h; (2) slots, Halton, lockfile, clearance checks 5 h; (3) title block and outside furniture 3 h; (4) rose 2 h; (5) double shoal, notes, marks, lights 3 h; (6) band 2 h; (7) opening and sampled boat 4 h; (8) night wiring 2 h; (9) phone 5 h; (10) checks 4 h. **≈ 36 h** once T5/T6/T7 land.

Risks: author filtering shrinks features and flips kinds (the lockfile shows it); 52 soundings crowd near WP4–WP5 (fallback: three rows at ±24/±48); the PA outline reads as a second shoal at 360 px (phone omits it); a condensed face changes caption widths (the block asserts its bounds).

Left out: hatch density by source coverage and author rings (08), the name over the edge and the A2 poster (28), paper dot grain (14), magenta unit caution (13), the 96 s compass swing (05), out-and-back sailing.

## 5. Acceptance criteria

1. grep hero SVGs for `ILLUSTRATIVE|PENDING|SEEDED|NOT FOR NAVIGATION` → 0; build exits non-zero while `seeded` is true or `weeks` is missing.
2. Every feature |area(0.44)/(π r²) − 1| ≤ 0.08; all 0.44/1.1 polygons closed; pairwise d ≥ ri+rj+44; course ≥ r+30 from every non-harbour feature.
3. Every water numeral is bracketed by its contours (§2.4); changing one week in stats.json changes that numeral and its contour.
4. No semantic run under 13 px at 1280 or 26 px at 720; soundings 11/18 only; every title-block run inside x 70–610, y 540–670; exactly three accent-filled objects, none within 120 px of y 222.
5. Night: max L(lit) > max L(text); semantic pairs ΔE_ok ≥ .06 under deutan/protan simulation.
6. Perf (T10 harness): after 46 s warm-up hero repaints ≤ 2/s; still edition 0 repaints; filmstrip at 0/25/50/75/99% of 46 s all finished sheets; 360 px DPR 3 passes.
7. < 300 KB raw per edition, phone < 120 KB; XML valid; bounds clean except the band's bleed and the five outside captions.
8. 360 px render: name, thesis, Rustmapper Shoal's two outlines (desktop) and one light recoverable; alt text ≤ 25 words.
