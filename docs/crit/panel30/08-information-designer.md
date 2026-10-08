# 08 — Information designer (Tufte / Bertin lens)

Information designer; I judge a mark by whether erasing it loses information. Looked at hero-day-2x, soundings-night-2x, approach-scrapy-day-2x, page-day-full; read stats.json, fetch_repodata.py, build_stats.py, chartlib.py, spec-hero.md, spec-supporting.md.

## What is good

- **The hero spec's `r = 3.2·√commits` is the right instinct**: area ∝ commits, lie factor 1.
- **Upright = measured, italic = illustrative** is a true Bertin move: one visual variable (slant) carries one meaning (certainty) everywhere, defined once. It is better than any caption.
- **The tide curve as the only live graph**, the snake deleted, and the night edition's layering (lights brightest, ink dimmed): correct figure/ground.
- **The red sector on Grafana Lt for the circuit breaker** is a genuine encoding: a sector light's wedge means "this bearing is dangerous", and here it does.

## What is bad, ranked

1. **The hero's contours and soundings encode the same noise field twice.** `soundings()` prints `(LAND − v)·38 + noise`; the contours draw `v`. Two layers, one synthetic variable, zero data. The spec fixes the features but keeps 34 open-water numerals in a *different unit* (commits/week) over a field that knows nothing about them: a "0" week will sit between the 30 and 40 contours. On a chart, contours are interpolated *from* soundings; here they will contradict them.
2. **The 24-hour clock is pointed by one sprint, in the wrong time zone.** `fetch_repodata.py` takes `fromtimestamp(s, utc).hour` and prints "busiest hour UTC". Of 317 commits at 21h, 256 are game_engine, Jan 4–14 2026 (585 commits in ten days, 31% of everything surveyed). Drop that repo and the modal hour is 16h, not 21h. The colophon builds a story ("he works at night") on ten days of one project read in the wrong zone.
3. **Rotating the dial destroys the dial.** 24 unlabelled bars at an unknown rotation; nobody can read a second hour off it. A real inner ring is rotated *and numbered*.
4. **Four units in one numeral field.** Spec §3 puts commits (count), commits/week (rate), workers (512, 256: capacities of code, not measurements of Ben) and followers in one 11px field, distinguished by slant and underline. Bertin: one variable per visual variable.
5. **Area ∝ commits is asserted, not drawn.** Polygon area depends on amplitude, level and neighbours: islands are cut at 1.5, shoals at 0.8, so a 126-commit shoal draws larger than a 169-commit island. Drawn-area/commits is never checked.
6. **Two totals, two populations.** `commits` 1,828 (GitHub, Ben's contributions) and `commits_surveyed` 1,868 (all authors on 21 clones). Per-repo counts include 2–4 authors, so the islands are partly other people's work.
7. **Smooth spline through weekly counts.** Catmull-Rom overshoots: it draws weeks that never happened and dips below zero beside a zero week.
8. **The language "depth-scale" keys nothing.** No tint anywhere means a language; a legend that explains no mark is ornament. It also spends the accent red (reserved for marks and lights) on "Python".
9. **Scale bar in URLs with nothing to measure.** No distance on the sheet is URLs; italic or not, it measures nothing.
10. **1 + 1 = 3 line noise.** Dotted course (2 6), dotted danger lines (0 4.5), dashed contours (3 3), graticule, minute bars: at 68% three of these become one vibrating texture.
11. **Approaches: depth sign undefined.** The render reads 53–62 in open water and 14 at the anchorage; the spec says depth deepens toward the anchorage. Pick one sign for the page. Minute bars and graticule carry no coordinate: frame, but the heaviest ink after the name.

## What needs to be done

- **Soundings first, contours second.** Add the 34 weekly points as field blobs along the course (amplitude ∝ √n); contours then follow the weeks and the boat crosses a shoal where a 310-commit week was. Test: every open-water numeral is bracketed by its two nearest contours.
- **Commits on land, not in water.** Each repo's count becomes a spot height (dot + upright numeral) inside its coastline or danger line. Water carries one unit. 512 and 256 move to the Approaches notes where they already live; 46 stays underlined at Profile Shoal.
- **Fix the clock's data.** Use the author's own offset (`git log --format=%ai`, parse `+hhmm`), which needs no knowledge of where he lives. Count *commit-days per hour*, not commits, so a sprint cannot set north.
- **Fix the clock's drawing.** 00 at top; numerals 00/06/12/18 on the inner ring; variation as one arrow to the modal hour, labelled with whatever the robust statistic says. Bars as lines, length ∝ value, never wedges.
- **Assert the area.** `islands()` already returns polygon area: solve r in two Newton steps so drawn area/commits is within ±8%, cutting every feature at the same level (the second band is tint only). Build fails otherwise.
- **One population.** Filter `git log --author` to Ben's identities; print 1,868 nowhere, or once as "all hands".
- **Tide curve: monotone cubic or steps, baseline zero**, HW/LW marked on the raw points. Delete the even-spread fallback (a chart of a formula); the clone pass already has every timestamp.
- **Distinct line frequencies**: graticule solid .06; contours solid .35; danger dots 0 4.5; course dashes 8 4. Day layers: soundings .5, features .9, type 1.0.
- **Replace the URL scale bar with an area key**: three circles, 10 / 100 / 500 commits, at the radii the field draws them.
- **Language bar**: keep the length encoding, drop "depth-scale", label the unit ("by bytes, GitHub"), ink ramp only, no accent.

## Improvements and high-level ideas

1. **Small multiples of the fleet (bold).** A 1280×300 sheet, 7×3 grid, one 52-week sparkline per repo on a shared y-scale, name 13px, count as spot height. game_engine reads as a ten-day spike, Scrapy as a year of steady soundings. "Sustained vs burst" said more honestly than any copy, from data the clone pass already has.
2. **One dataset, two projections.** The 52 weeks appear as contours along the hero's course and as the tide curve on Sheet 2. Mark the hero's waypoints with the tide axis's month letters; a reader who notices gets the whole system.
3. **Hatch density as a real variable.** Let the UNSURVEYED band's hatch spacing follow the source diagram: 3px where CT logs reach, 6px where only sitemaps do, blank beyond. The margin encodes coverage instead of decorating it.
4. **Author rings.** Features with >1 author get a thin second coastline per extra author: where the work was shared, in one mark.

## What the page says about its maker

Now it says: someone who studied how a chart looks, reproduced its texture, and filled it with numbers that measure nothing; a decorator who knows the conventions but has not submitted to them. It should say: someone for whom every digit was taken by a lead line, who knows which figures are measured and which drawn, who can show a ten-day sprint and a year of steady work on one scale without flinching, and whose chart survives a hydrographer, a statistician and a phone.

## Five most important lines

1. Open-water soundings must generate the contours (weekly points as field blobs along the course); today the numerals and contours are two drawings of one noise field, and the spec makes them contradict.
2. The 24-hour clock is computed in UTC and pointed at a ten-day game_engine sprint (256 of 317 at 21h; 16h without it): use author offsets and commit-days per hour, keep 00 at top, numbered, with a variation arrow.
3. Assert drawn area ∝ commits in the build (±8%, same cut level for every feature) and use Ben's own commits only; the page currently carries two totals and other people's work in the islands.
4. One unit per field: commits as spot heights on land, commits/week in water, 512/256 out of the soundings; tide curve monotone, baseline zero, no even-spread fallback.
5. Bold: a small-multiples sheet of 21 per-repo 52-week sparklines on one scale, the most honest and most telling graphic the data can give.
