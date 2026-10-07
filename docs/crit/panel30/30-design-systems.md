# Crit 30 — Design-systems lead

I run design systems: tokens, components, rules and sanctioned breaks, and the docs that let someone else extend them. I read DESIGN.md, design-tokens.json, svgkit.py, chartlib.py, sheets/common.py, _v8_reference.py, build_assets.py, STANDARDS and both specs, audited every size, opacity, width and dash in the code, and looked at hero day, legend night and the night page.

## What is good

- **Motion is the mature layer.** `EASE` names three easings by intent (settle, draw, sea), `LOOP` is a scale (10/24/48/96), and `flash("Fl(3)")` parses a domain grammar into keyTimes: iconography with definitions, in code. Every other layer should look like this.
- **A rule as a component.** `measured()` / `illustrative()` make the honesty convention a function, not a comment; `check_bounds()` is a lint; `text_use` is a real asset pipeline.
- **Themes are semantic pairs, not inversions.** `paper/land/ink/ink2/muted/accent/ok/cool` with a "Use" column is the start of a semantic token table, and night is designed (red-light-safe), not computed.

## What is bad (ranked)

1. **Three token sources, none authoritative.** `design-tokens.json` (v8.0.0, seven sheets, "nothing flashes") is read by no script and already contradicts the lights. DESIGN.md has its own table. `svgkit.Theme` carries seven dead fields (`panel, panel2, grid, field, soft, line, accent_soft`) plus legacy `DARK/LIGHT`; the docstring says Inter/DejaVu and `svg()` stamps "profile v7".
2. **No type scale.** Code and specs use 27 sizes (8 … 13, 14, 14.5, 15, 16, 17, 19, 22, 24, 27, 28, 30, 34, 40, 46, 96, 176) and five caption trackings with three different defaults (1.8 in v8 `cap`, 1.6 in common, 1.2 in `chart_number`). The specs continue it ("17–19 for water names").
3. **Elevation is unmanaged.** On a one-ink chart, opacity *is* elevation. Ink appears at nine stroke-opacities (.4–.85), nine fill-opacities (.07–.35) and thirteen widths (0.45–2.2); night is "0.6× opacity" in prose, per element.
4. **Component drift.** Five frames (`neat_line` inset 5, `border` inset 6, v8 `frame` 14/19, `cartouche` 4, `source_diagram`), two lighthouses, two anchors, two buoys (`buoy` has can/cone wrong; `lateral_mark` is right), two roses. The log's "no frame" is implemented by not calling a function, so the system cannot see it.
5. **No mechanism for consistency *and* variety.** STANDARD 4 wants one chart, STANDARD 6 wants silhouettes that differ; nothing in the code expresses either, and the v9 specs already re-converge (every sheet gets a `cartouche` with numbered 13px notes).
6. **Nightly data has no constraints.** spec-hero asserts closed polygons and a successful Halton search; an assert in a cron job is a broken or stale image. No cap on features (24 now; placement fails near 40), label length (`Elusive_trades_data Shoal` at 15px), digit counts, or the shoal → island flip after 90 days (tint becomes land: a visible composition change). `stats.json` today has no `weeks`, `pypi` or `repo_count`, so the italic fallback is the launch state and nobody has named it.
7. **DESIGN.md describes; it does not govern.** Stale after one commit (rhumb lines, snake, 9–11px captions, seven sheets); no "why", no "when not", no changelog, no "how to add a sheet".

## What needs to be done

- **F1 One source.** `scripts/tokens.py` builds `Theme` and generates DESIGN.md's tables (`--md`). Delete `DARK/LIGHT`, dead fields, stale docstrings. Test: no hex literal under `sheets/`.
- **F2 Nine type roles**; `k.text(role=…)` replaces `font+size`: display 176 serif · thesis 40 serif-italic · sheet-title 28 serif · place-water 17 serif-italic · place-land 15 serif · note 16 serif-italic · label 13 plex · label-caps 13 plex tracked 1.6 · texture 11 plex. A raw size outside the roles fails the build.
- **F3 Ink levels and line vocabulary.** `INK = {structure, text, texture, ghost, tint}` with explicit day *and* night values (a table, not multipliers); widths `hair .5 / rule .9 / line 1.2 / mark 1.4 / bold 2.2`; named dashes `COURSE "2 6" · TRACK "1 4" · DANGER "0 4.5" round · LIMIT "1.5 4" · APPROX "3 3" · SECTOR "2 3"`, each with a one-line definition. That list is the legend.
- **F4 Component inventory, one function each, with states.** Axes: edition (day/night), truth (measured/illustrative), motion (opening/ambient/reduced), size (desk/phone).

  | Component | Variants | States |
  |---|---|---|
  | Frame | minute-bars · double · ruled-paper (none) · broken (gap list) | — |
  | TitleBlock | cartouche · inset-title · log-header | — |
  | Inset | ×N with leader | — |
  | Numeral | measured · illustrative · height-above-datum (underlined) | — |
  | Mark | can · nun · light · sector · leading · wreck · anchorage · station | lit/unlit; halo at night |
  | Water | tint A/B · danger line · foul hatch · unsurveyed hatch | approximate (dashed) at the margin |
  | Note | marginalia ±4–7° with leader | — |
  | LegendEntry | `<use>` of the chart's own symbol id + label role | — |

  Test: every legend `<use href>` resolves to an id present on a sheet (E3 hints at this; make it a check).
- **F5 Rules and breaks as data.** Each sheet declares `BREAKS = [("frame", "none", "a log is written on paper, not drawn on a chart")]`; the build prints them and DESIGN.md's "Deliberate breaks" is generated from them. Hard rules: red/green only on marks and status; italic numeral = illustrative; hatch = unsurveyed or foul only; nothing semantic under 13px; one chart-number style. Sanctioned breaks today: hero minute bars, approaches' broken west neat-line, the log's ruled paper, the footer's water through the frame. A break without a reason fails the build.
- **F6 Data constraints.** Features ≤ 32 (the rest collapse into an "and N islets" sounding); `r` clamp [6, 90]; names ≤ 18 characters, else chart abbreviation ("I.", "Bk"); commit numerals ≤ 4 digits; chart number ≤ 3 digits; edition ≤ 12 characters. Placement failure falls back to reserve slots, never an assert; kind flips are logged as a Notice. The build writes `assets/build-report.json` (sizes, warnings, breaks, flags `weeks_present`, `pypi_present`); the workflow fails only on XML, size, bounds. Two fixtures: today's stats (golden PNG, 1% tolerance) and a stress fixture (40 repos, 9,999 commits, 30-character names) that must build clean.
- **F7 DESIGN.md as a contract:** Principles · Tokens (generated) · Type roles · Ink levels · Symbols and definitions · Components and states · Rules and deliberate breaks (generated) · Data constraints and nightly states · Motion table · Adding a sheet (declare kind, declare breaks, pass both fixtures) · Changelog.

## Improvements and ideas

- **Bold: publish the design system as a sheet.** Hydrographic offices issue "Chart No. 1: Symbols and Abbreviations." Build one from the same `<defs>` the sheets use (every symbol, dash, numeral style and ink level, with its definition) and put it where the stack table was. DESIGN.md embeds it. The system documents itself in its own grammar, and the id diff makes drift impossible.
- **Notices are the changelog.** "Corrected through Notice 5" is read from DESIGN.md's changelog, not typed. Every token or rule change is a numbered Notice, so the number on the chart cannot disagree with the documentation.
- **Four chrome families, declared.** `KIND = chart | strip | paper | edge`, each with a prescribed frame, title block and type roles: hero and approaches `chart`, soundings and instruments `strip`, log `paper`, footer `edge`. Variety becomes systematic; two sheets of one kind must differ in silhouette, and the fixture renders them side by side.

## What the page says

Now: someone who designed a beautiful artefact and then built a system under it in a hurry, so the artefact is one thing and the code is three half-things, and the only truly systematic layer (motion) landed last. It should say: this person keeps one symbol sheet, one set of corrections and one source of truth, like a hydrographic office, and the chart gets more accurate every night *because* the constraints were written down before the data moved.

## Five most important lines

1. Collapse the three token sources into one (`tokens.py` builds `Theme` and generates DESIGN.md's tables); delete legacy themes, dead fields and v7 docstrings.
2. Replace 27 font sizes with nine type roles, and nine opacities / thirteen widths with five ink levels and five widths, each with explicit day and night values; lint raw sizes out of the build.
3. One function per component, with variants and states (edition, truth, motion, size); legend entries are `<use>` of the chart's own symbol ids, and the build diffs them.
4. Declare every deliberate break as data with a reason (`BREAKS` per sheet), and write the nightly data constraints (feature cap, r clamp, name and digit limits, slot fallback, golden + stress fixtures) so stats.json can change without breaking a composition.
5. Publish the system as "Chart No. 1: Symbols and Abbreviations", generated from the same defs, and read "Corrected through Notice N" from the changelog so artwork and documentation cannot drift.
