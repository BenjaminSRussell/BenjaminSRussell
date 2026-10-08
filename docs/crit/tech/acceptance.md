# Acceptance record — chart v9

Filled from the gate runs on the final build of branch `profile-v7` (MASTERPLAN §7). Numbers are measured
in this session's Chromium 141 at 870 px unless stated; the judged rubric is the eight-critic re-crit
panel's median (docs/crit/recrit/).

## Floor (automated)

| Gate | Rule | Result |
|---|---|---|
| check.py fast | xml, size, strings, position, expiry, type, motion, data, log, bounds, contrast, legend, alt, flash, readme | **pass, exit 2**: 0 fail · warnings = SIZE-TARGET on soundings/instruments/footer/approaches (hard caps hold), POSITION-EMPTY (Ben's line), 4 BOUNDS-TEXTURE (sounding density at the hero's harbour mouth) |
| check.py render | still-frame gate (7.2), silhouettes | **pass**: every sampled frame ≥ 0.95 coverage after its opening (hero t=0 ≥ 0.6), ≤ 1.5 % changed outside the moving windows, no emptied ledger, stills carry zero animation elements; six silhouettes pairwise L1 ≥ 0.25 |
| check.py perf | repaint budget (7.3) | **pass, exit 2** (final build): hero 1.0/s · approaches 1.375/s · log 2.0/s · footer 3.55–3.72 ms/frame (ambient) · hero-phone 0.25/s at 360 px DPR 3 · soundings, instruments, hero-still 0 repaints · hero moving window 35.7 ms/frame = deviation 1, warning |
| unit tests | `python3 -m unittest discover -s tests` | **180 OK** |
| determinism | two builds from one stats.json byte-identical | **38 of 38 files identical** |

## Measured deviations (recorded, not failed)

1. **ms/frame while moving.** Chromium re-rasters the whole `<img>` on every SMIL tick; a 1280-wide sheet with
   ~1300 elements costs ≈ 35–40 ms per repaint whatever the markup. The 8 ms/frame cap of 7.3 cannot be met by
   any sheet while anything moves. The moving windows are bounded (hero 4–28 s, footer 40–64 s) and the
   repaint-rate rules after them hold. `checks/perf.py` reports PERF-MOVING as a warning.
2. **Hero t=0.** The MASTERPLAN opening faded the whole sheet in; the five-second test and the 7.2 floor want a
   sheet at load. Title block, frame, rose, land and sea names are static at t=0; the water draws in.
3. **Raw size targets.** Soundings, instruments and footer exceed their per-sheet raw targets (warnings);
   every hard cap (300 KB raw, 100 KB gz, 3000 elements, 250 KB gz per edition set) holds.

## Judged (J1–J12, re-crit panel median)

Round 1 (eight critics on the first full render, before the round-3 fixes; docs/crit/recrit/):

| J | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| median | 3 | 3 | 2.5 | 3 | 2 | 3 | 2 | 2 | 2 | 3 | 2 | 2.5 | **30 / 36** |

Individual totals 28–30 (type 29, accessibility 30, mobile 28, cartography 30, narrative 30, recruiter 29,
art director 30, owner's advocate 28). No zero; J1, J2, J7, J10 all ≥ 2. The panel passed the floor exactly;
the shared defects it found (README footer swallowed by the colophon, nine notices under "five principles",
the computed log signed with initials, the harbour-mouth sounding cluster, 8 px legend and instruments type,
the empty phone instruments sheet, the floating hatch) were fixed in the rounds that followed, and a second,
smaller panel re-scored the final render.

Round 2 (four of the eight critics on the final build; docs/crit/recrit2/):

| Critic | round 1 | round 2 | J1 | J2 | J3 | J4 | J5 | J6 | J7 | J8 | J9 | J10 | J11 | J12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| owner's advocate (36) | 28 | **32** | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 2 | 2 | 3 | 3 |
| art director (28) | 30 | **34** | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 3 | 3 | 3 |
| mobile (10) | 28 | **35** | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| type designer (07) | 29 | **34** | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 |
| **median** | 29 | **34 / 36** | 3 | 3 | 3 | 3 | 3 | 3 | 2.5 | 2.5 | 3 | 3 | 3 | 3 |

Pass: ≥ 30 with no zero and J1/J2/J7/J10 ≥ 2 — **met, 34 / 36**. What the second panel still lists is
last-day polish (a crowded square inch at the hero's 208° junction, zeros read as stippling, two phone label
collisions, footer fine print at 8–9 px, the thesis echoed three times in the Markdown); the hero items went
to a final builder round, the rest are recorded here for the next design release.

## Five-second test

_pending_ (shadow-profile cohorts are Ben's to run; the panel's own 5-second readings are recorded in lieu)

## Shipping

1. Merge `profile-v7` into `main` (squash or merge; the branch carries the full history of the build).
2. The `chart` workflow runs on the push (paths include `scripts/**`, `chart.toml`, `README.md`): tests →
   survey → build → render → `check.py --ci` → commit stats/README to main → publish the orphan `chart`
   branch → social PNGs. Until that first run finishes the README's images point at a branch that does not
   exist yet (a few minutes of broken pictures). To avoid the gap, publish first from the branch:
   `python3 scripts/build_assets.py && python3 scripts/publish_chart.py` (a force-push to `refs/heads/chart`,
   which this session was not permitted to do), then merge.
3. Fill `chart.toml` `[position]` and `[contact]` (docs/BEN-TODO.md items 1–2); the gate warns until then.
4. Delete the old `output` branch on GitHub; set the social preview from `social/hero-day.png` on the
   `chart` branch.

## v9.1 — the legible edition (8 Oct 2026)

The owner's reading of the live profile after the first nightly runs: "the images are all crushed", the
survey "weird", the pictures "not cool enough"; the wording stays. The crush was decision 6: floors held on
the 1280 px sheet, and GitHub's column shows that sheet at ~870 px (×0.68), so 13 px labels printed at 8.8 px
and 11 px figures at 7.5. Decision 6 is revised: the desk scale now carries the display factor (tokens.py
`DISPLAY`, scale 16 · 19 · 25 · 32 · 41 · 53 · 68 · 88 · 141 · 176, floors 19 / 16 / 25, line weights ×1.3)
and every sheet was re-tuned to it: soundings 1280×520 with a 5×5 register and a thinned traverse, log
1280×590 with wrapped remarks, instruments 1280×360, footer's line at 41, approaches per its module's BREAKS.

Hero (the survey): the profile shoal moves west and the archipelago packs both sides of a shorter arc; a named
feature reserves the ground under its name; a name never leaves the neat line (the live sheet cut
AI CODE DETECTOR I. at x 20) and an islet gives its name up before printing over a neighbour; the fallback
placer now sees the features the arc placed (the live heap of overlapping islets); islets under 25 commits
leave the phone edition; unnamed islets lose their 5-ring (a bubble chart otherwise); printed week figures
break the contours they cross instead of being culled (the high-water week had stopped printing); the pencil
note sits under the thesis; the title block is six left-aligned lines with the source diagram beside it.

Checked at 870 px (desk, day and night) and 360 px (phone) for every sheet; gates and the suite green.

## Round 3 — the harder review (8 Oct 2026, v9.2)

Four critics read the merged v9.1 at the size GitHub shows it: art director 25, hydrographer 27, mobile 25,
owner's advocate 24 (of 36). Their reviews are in `docs/crit/recrit3/`. The findings they shared, and what
v9.2 does about each:

- *The hero's argument is its lightest stroke; the title block its heaviest text.* The course is drawn at LINE,
  the inset box at PEN and sized from the harbour; the title block is four lines; VAR on one line; tints and
  solid contours end at the limit of survey and the ship enters from unsurveyed water; a figure on every
  contour ring; the first-commit months are report dates under the names, not dates on fixes.
- *Marginalia under the neat line.* Every sheet's frame insets hold a 19 px margin line; sheets 2, 4, 5 get the
  same minute-bar neat line as 1, 3, 6; bottom lines are `CHART NO. · SHEET n`.
- *The page says things three and four times.* No thesis paragraph, no figures line under sheet 2, no notes
  panels on sheet 3 (the bullets carry them), no caption lines on sheet 3, no instruments sidebar words.
- *Honesty.* The log prints only what settings compute (no p95, failure rate, fsync, elapsed); the Grafana
  light's character and sheet 3's survey line slope while unmeasured; doubt marks sit in their zones; the
  leading lights are lights; the legend defines what the chart draws and nothing else; the corrections
  list is the year's first to last; one gazetteer names every repository on every sheet.
- *Phone.* Legend complete on sheet 3; spot heights never over their islets; rustmapper named; the log
  carries its figures and its sign-off; instruments carries dates and the bold; alts true of every edition.

Scores after the round are the next panel's to give.
