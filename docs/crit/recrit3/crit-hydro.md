# Hydrographer's crit — Chart No. 21, v9.1 (renders of 8 Oct 2026)

Lens: chart grammar and provenance. Every figure on the sheets was checked against `assets/stats.json` where the sheet carries a key; symbol use was checked against the legend by `<use href="#…-sym-…">` in `assets/v9/*.svg` and the `build-report.json` text registry.

## What passes the pen

- Fleet register and spot heights sum to 1,665 = `commits`; every island figure matches `repos[].commits`, every subscript matches `months_active` (87₆, 46₄, 33₂, 22₃ …). HW 358 · wk of 5 Oct · Data Science Bank (149/358 = 0.42, `cause_share`), LW 0 · wk of 24 Aug, slack water Jul (29 Jun–26 Jul), typical week 0: all as the data says. The 52 figures on Sheet 2 are the 52 `weeks[].n`. VAR 14h: `hours[14]` = 25 is the mode. 1,665 / 1,966 / 1,828 match `commits`, `all_hands`, `calendar_total`.
- Region B is right on both sheets: final leg 290° true, red nuns north (starboard returning), green cans south, even red / odd green, numbered from seaward (G "1" outermost, R "4" at the gate), neighbours never alike (Fl 4s vs Fl(2) 10s). Hero bearings 233° · 208° · 290° are computed from the drawn legs. The phone rotation keeps hands correct.
- Depth is a count throughout: tint B under 5, tint A under 10, deep water left paper (the 296 week is a paper hole with an approximate contour — correct, if startling). Data Science Bank and FashionDB Bank are submerged shoals with danger lines, Profile Shoal carries the station; Game Engine I. breaks the surface. Banks are not islands. Good.
- Honesty marks: every Sheet 3 sounding, the 429 Shoal, the outer-leg 306°, 256–1024, 250 ms, 8 shards, and the whole ship's log are sloping; the log says "computed from settings · unsigned". `512` is never upright. Rep / ED / SD / PA are all drawn in the right typographic register.
- Night is designed: buoy cores, Grafana Lt and the mole head are the brightest marks; the hatch dims to .35.

## Scores (0–3)

| # | Criterion | Score | One line |
|---|---|---|---|
| J1 | Thesis in one line, once | 3 | One italic line under the name; the README prose extends it, the footer answers it; nothing repeats it. |
| J2 | Cover the name: hero argues the survey edge | 2 | Band, limit line, course from the margin, rustmapper (PA) half off the sheet all argue it; the tints and a solid contour running under the hatch argue against it (finding 3). |
| J3 | Cover the titles: sheets by silhouette | 3 | Archipelago, tide curve over a register, dense chart with a key strip, ruled log, three-column equipment list, broken-edge strip. Unmistakable. |
| J4 | Hydrographer names region, unit, datum | 2 | Hero: IALA Region B · SOUNDINGS IN COMMITS · DATUM: MAIN. Sheet 3 desk gives unit and datum but no region line (the phone edition has it, line 946); Sheet 2 gives unit only. |
| J5 | Point at any mark: one sentence, reads on a phone | 1 | Legend rows with no referent (Correction, Underlined), referents with no row (Obstn, the coverage box, the dated fixes), Sheet 5 reusing fix/waypoint/anchorage/station with other meanings, and the phone key missing Zone, Fix, Waypoint while drawing all three. |
| J6 | Chart changes with the data | 3 | Areas ∝ commits (ratios 0.97–1.06 in the report), 52 week kernels, HW cause named, edition line from PyPI, wreck from `stale_branches`. |
| J7 | Honesty | 1 | Grafana Lt · Fl 15s upright on a claim stats.json carries as null/unmeasured; "Surveyed by rustmapper 2026" over an all-sloping ground with `trial: null`; one of two dead branches charted; contours beyond the limit; a five-item window printed as the small-corrections list. Each is a small fix, but a hydrographer red-pens each. |
| J8 | Every still is finished | 2 | Desk stills are finished sheets. The phone hero prints spot heights over their own islets (37₃ reads 7₃, 46₄ reads 6₄), so that still is not. |
| J9 | Copy says each thing once | 2 | On the sheets: "write-ahead log · one cell per sounding" and "one shard per core · 8 here" are captions explaining a symbol the legend already defines (Track line · one shard). Everything else is said once. |
| J10 | Recruiter finds field, systems, languages, contact | 3 | The at-a-glance table under the hero does it in plain text; links to PyPI and Email are the first line. |
| J11 | Night designed, not inverted | 2 | Lights are the brightest things; but "Health Ldg Lts 290°" is dark at night: the two leading marks are beacon triangles with no lit core (finding 4). |
| J12 | ≥ 4 uncaptioned second-look layers | 3 | Rose as a 24 h clock, chart number = repo count, Profile Shoal with its station, Wk = dead branch, 429 Shoal, ZOC letters = seed sources, HW cause as a bank name. More than four, none captioned. |

**Total 27/36.** Below the 30 gate, with J5 and J7 at 1. All but one of the findings below are S; fixing 1, 2, 4, 5, 8 and 9 alone lifts J5, J7, J8 and J11 by a point each.

## Findings, ranked

### 1. Grafana Lt · Fl 15s is upright on an unmeasured claim — Sheet 3, harbour north shore (S)
**See:** `Grafana Lt · Fl 15s` in upright `label`; `lights[]` in the report says `Fl 15s`.
**Rule:** a light character is a figure; upright means measured from the survey. `assets/stats.json` → `claims.scrape_interval = {value: null, measured: false, sha: null}`. `approaches.py:318–325` falls back to 15 when the claim is null and sets `scrape_measured = False`, then letters the character in the upright role anyway (line ~697). `chart.toml` does carry `value = 15, measured = true` with a sha, so the figure is probably true, but the sheet's own data file does not carry it, and the sheet was built from that file.
**Change:** (a) rebuild `stats.json` so `data/claims.py` writes the chart.toml claim through (value, source, sha, measured); (b) in `approaches.py` set the Grafana character role to `label-italic` with `truth="illustrative"` whenever `not self.scrape_measured`, so the fallback can never print upright again. Same guard for the mole head's `F`.

### 2. "Surveyed by rustmapper 2026 · Datum: main" over a ground that disclaims itself — Sheet 3 title block (S)
**See:** the title line is upright; every sounding under it is sloping; `trial` is null; the log is computed.
**Rule:** the source statement in a title block is the chart's strongest claim. The figures say "no survey was made"; the title says one was. A hydrographer reads that as a contradiction, not as a pun.
**Change:** wording stays; register changes. While `self.trial is None`, set the survey line sloping (`label-italic`, `truth="illustrative"`), the sheet's own convention for "not measured", and let it go upright the night `exports/run-YYYY-MM-DD.json` lands (MASTERPLAN §5 item 8). While there, add the region line the phone edition already has (`IALA Region B · marks numbered from seaward`, approaches.py:946) to the desk title block so Sheet 3 answers J4 on its own.

### 3. Tints and contours run past the limit of survey — Sheet 1, east band (M)
**See:** the shallow tint and a contour continue under the hatch to the right of the dotted LIMIT OF SURVEY 2026 line (crop at 1000–1200 × 230–520); WP1 (the course origin ⊙) sits inside the band.
**Rule:** beyond a limit of survey there are no soundings and no contours; the band is hatch alone. `hero.py:121` fades the coast factor over LIMIT_X…+70 and `band_skip` removes the soundings, but the tint polygons and the solid contour are not clipped.
**Change:** clip `tint_bands` and solid `draw_contours` output to `x ≤ limit_x` (a `<clipPath>` on the water layer, `hero.py` ~446–502, 858–864); keep only the approximate (dashed) contour inside the fade zone, which is what the legend's "Approximate contour" row is for; start the course at the limit line (WP1.x = limit_x) so the ship enters from unsurveyed water rather than from a charted lagoon inside the hatch. The 296 week hole can stay where it is: it is west of the line.

### 4. "Health Ldg Lts 290°" are beacons, unlit, and dark at night — Sheet 3, Delta Lake (S)
**See:** two `sym-ldg` triangles at (123,355) and (78,339) with no lit core, no flare, no character; at night they are the only navigational "lights" that are not magenta.
**Rule:** Ldg Lts carry light stars and characters; Ldg Bns do not. The label says lights, the symbol says beacons, the night edition proves the symbol.
**Change:** `approaches.py:634–636`: draw each leading mark through `light_group` (lit core + flare, character `F`, sloping like every other character on the sheet, `begin` 0) so they are lights by day and the brightest thing on the leading line by night; the legend row "Ldg line · health check" can keep its glyph if the glyph gains the star.

### 5. Phone hero spot heights overprint their islets — hero-phone, archipelago (S)
**See:** 37₃ reads 7₃, 46₄ reads 6₄, 33₂ reads 3₂, 39₃ reads 9₃ (readme-390 crop at 40–700 × 330–620): the first digit is drawn across the islet's coastline.
**Rule:** a spot height sits inside its feature only when the figure fits inside; otherwise it stands clear to the east. `chartlib/place.py:253` tests `f.r >= 16` in sheet units; the phone re-solves radii in phone space while the lettering is on `SCALE_PHONE`, so a 33-commit islet qualifies as "inside" and the centre point passes `point_in_polygon` though the figure's box does not.
**Change:** `hero.py:591` pass `min_r=16 * s` (the same `name_min_r` the names use) into `spot_heights`, or test the figure's box against the polygon instead of its centre; the desk edition is unaffected (its islets already fall to the "east with clearance" branch).

### 6. Doubt marks sit in the wrong zones of confidence — Sheet 3, survey ground (S)
**See:** `approaches.py:599` "Rep in zone A, ED in zone B, SD in zone C". The ZOC table says A sitemaps = existence doubtful, B CT logs = exists, may not answer, C Common Crawl = as reported.
**Rule:** a ZOC diagram and the doubt marks on the ground are the same statement twice; they must agree. ED ("existence doubtful") stands in the zone the table says exists; SD ("sounding doubtful") stands in the zone the table calls "as reported".
**Change:** `approaches.py:143–144`: move `ED_` into zone A beside Rep (the sitemap note's leader already points there), put `SD` on the zone B line ("may not answer" = sounding doubtful), and leave C with Rep or nothing. One constant each.

### 7. Dated fixes read as fix dates and run backwards — Sheet 1, course (S)
**See:** `OCT 2025` beside WP2 near the limit, `SEP 2025` beside WP4 at the harbour, both upright, both on the course the week soundings run along oldest-seaward (Oct 2025 at the margin → Oct 2026 at the anchorage).
**Rule:** a date beside a fix is the fix's time. These are `repos[].first` of rustmapper and Scrapy (`hero.py:1129–1148`), which the sheet never says; no legend row defines a dated fix. A hydrographer reads the course as sailing from Oct 2025 to Sep 2025 and distrusts the sounding order.
**Change:** drop the two reveals, or move each date off the course onto its feature as chart practice for a report date: `rustmapper (2025)` under the name, `SEP 2025` under SCRAPY HARBOR, in `label` ink2, keyed `first:` as now. Wording unchanged, provenance kept.

### 8. Legend rows with no referent, referents with no row, and symbols re-used with other meanings — Sheets 3, 5, 6 (S)
**See:** `Correction · revised` has exactly one `<use>` on the whole chart: the legend's own at (362,946). `265 Underlined · above datum` is the only `truth="datum"` figure on any sheet (`approaches.py:1105–1113`). Footer letters `Obstn rep. 2026 (PA)` with no Obstn row; the hero's dashed coverage box has no row. Sheet 5 marks languages with `fix`/`waypoint`, stores with `anchorage`, deck with `station` (`instruments.py:47–51`) while the legend says Fix · position, Waypoint · stage, Anchorage · Delta Lake, Station · profile repo.
**Rule:** the legend defines every symbol used and nothing it does not use; a symbol means one thing on every sheet of a chart.
**Change:** remove the Correction row and the Underlined sample (or give each one real use: the wreck's branch commits are honestly "above datum"); give Sheet 5 a neutral gutter tick instead of charted symbols; add an Obstn row or drop the abbreviation to `Rep (2026) PA`. In `scripts/checks/legend.py`, count legend uses separately from sheet uses and make LEGEND-UNUSED a fail; include `instruments-day` and `footer-day` text abbreviations in the sweep.

### 9. Phone Sheet 3 draws Zone boxes, fixes and waypoints its key does not define (S)
**See:** A / B / C boxes under LIMIT OF SURVEY 2026, `+` fixes down the single track line, ⊙ waypoints on the course; the phone legend filter (`approaches.py:1145–1147`) keeps 13 rows and omits Zone · seed source, Fix · position, Waypoint · stage, Track line · one shard. The ZOC table is gone on the phone, so A/B/C have no meaning at all at 360 px.
**Rule:** J5 on a phone: point at any mark, one sentence.
**Change:** add `"Zone", "Fix", "Waypoint", "Track line"` to the phone filter list (four rows, ~70 px at pitch 34, inside the 1880 canvas), or stop drawing the zone boxes on the phone.

### 10. One of two dead branches is charted — Sheet 3, Wk ’25 (S)
**See:** `repos[Scrapy].stale_branches` has two entries (`claude/ensure-this-is-…`, `fix/144-lean-docker-extras`, both last 2025-11-09); `approaches.py:729–731` charts the first name ≤ 26 characters.
**Rule:** an uncharted wreck is the one omission a chart may not make. The legend says "Wk · dead branch, year", so the reader takes the one Wk as the count.
**Change:** either drop bot-authored branches at survey time (`identity.bots` already names "Claude") so stats.json carries only branches a hydrographer would chart, or draw a second `WRECK` slot north-east of the first with its own name. Decide in `build_stats`, not in the sheet.

### 11. Sheet 2 prints 11 of the 20 non-zero weeks — tide table traverse (S–M)
**See:** `61 85 2 0 7 4 3 296 0 1 0 17 0 146 358`; culled by the 28 px rule: 240 (the sprint's first week), 108, 73, 37, 25, 16, 16, 15, 13. The report's text registry has all 52, the render has 15.
**Rule:** a tide table lists every reading; generalisation belongs on the chart, not in the table. The HW cause week (358) prints while its neighbours 108 · 37 · 146 · 73 · 13, the actual Sep–Oct story, mostly do not.
**Change:** `soundings.py` traverse: stagger figures in two rows (the hero already does four) so every non-zero week prints; zero runs keep their single 0.

### 12. One contour figure on the hero, and a five-item window printed as the corrections list — Sheet 1 (S)
**See:** `contour-figure` entries on hero-day: one, `10` at (976,713). The legend promises 5 · 10 · 20 · 50 with an index style; a hydrographer cannot tell the 5 from the 10 ring around Game Engine I. without a figure. Margin: `SMALL CORRECTIONS 2026 — 169–173`; `corrections["2026"]` holds n = 5…173 and `hero.py:1070` slices `[-5:]`.
**Rule:** every closed contour the pen carries gets a figure at least once; the small-corrections list is the full list applied since the edition (the edition line says Nov 2025).
**Change:** lower `contour_labels(min_len)` or label per level once per closed ring over the 520 px generalisation threshold; print `2026 — 5–173` (first–last of the year) or the count.

## Not findings, noted
- 296₅ on the hero appears as 296₆ at 870 px; the SVG and report carry ₅ (days = 5). A rasteriser artefact at that scale, not a data fault.
- Sheet 2's register sparklines are sub-pixel for 19 of 21 lines at 870 px; the register reads as a table. Honest (the data is bursty), but the "21 sparklines on one scale" promise is kept only on paper.
- `Obstn rep. 2026 (PA)` would normally be lettered `Obstn (PA)` with `Rep (2026)`; acceptable shorthand.
