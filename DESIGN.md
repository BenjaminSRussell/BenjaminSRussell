# Design notes — "Chart"

The README is a nautical chart of the open web. Every image is a sheet from the
same chart: one typeface pairing, one ink, one paper, one set of symbols.

## Why a chart

The avatar is a sailboat. The work is survey work: crawlers take soundings of a
badly charted web and come back with rows you can trust. A chart gives that story
a visual language nobody else on GitHub is using, and it is dense with the kind of
detail that rewards a second look: bathymetric contours, soundings, a compass rose
with rhumb lines, lateral buoys, a lighthouse, a title cartouche, minute bars on
the neat line.

## Sheets

| Sheet | File              | Size        | What it shows |
|-------|-------------------|-------------|---------------|
| 1     | hero              | 1280 × 640  | Chart No. 27: name, tagline, cartouche, compass, plotted course with a sailing boat, islands named for the projects |
| 2     | soundings         | 1280 × 268  | Live figures in Instrument Serif, a language depth-scale, a tide curve of 52 weeks of contributions |
| 3     | approach-scrapy   | 1280 × 420  | Harbor approach: a buoyed channel through the pipeline stages, past the Grafana light, into Delta Lake anchorage |
| 4     | survey-rustmapper | 1280 × 420  | Survey: a vessel sounds a shoal along a fan of lines; depths fill in, contours resolve |
| 5     | log               | 1280 × 440  | Ship's log: a ruled logbook page that types a real rustmapper session |
| 6     | legend            | 1280 × ~318 | Legend and symbols: the stack, each column with its chart symbol |
| 7     | footer            | 1280 × 200  | The edge of the chart: a boat sails toward a waterfall it never reaches |

Every sheet is a paper rectangle with a double neat-line, so the page reads as one
document laid on GitHub's background. Only the hero carries minute bars.

## Palette

Two editions, chosen by `<picture>` + `prefers-color-scheme`.

| Token  | Day (light) | Night (dark) | Use |
|--------|-------------|--------------|-----|
| paper  | `#F4EEE1`   | `#0F1A2B`    | the sheet |
| land   | `#E6DCC6`   | `#172740`    | islands and coast, hatched |
| ink    | `#1B2A41`   | `#DCE4F0`    | type, contours, symbols |
| ink2   | `#34465F`   | `#B4C0D4`    | secondary type |
| muted  | `#6B7A90`   | `#7F8FA9`    | captions |
| hair   | `#CDC3AE`   | `#2A3A55`    | rules, sheet edge |
| accent | `#D9442B`   | `#FF6A3D`    | red cans, the north point, the cursor, the signal |
| ok     | `#2F8F5B`   | `#4ADE9B`    | green cones, "done" |
| cool   | `#2E6FB0`   | `#7CB8FF`    | reserved |

Red and green appear only as lateral marks and status. Everything else is ink.

## Type

- **Instrument Serif** Regular for titles and figures, Italic for the asides.
- **IBM Plex Mono** Regular / Medium for captions, soundings, bearings and the log.
- Captions are uppercase, 9–11 px, tracked +1.8 px.

All type is converted to outlines by `scripts/svgkit.py`. Repeated glyphs
(soundings, captions) are defined once and placed with `<use>`, which is what
keeps a sheet full of numbers under 300 KB. Subsetted fonts and their licenses
live in `scripts/fonts/`.

## Chart engine

`scripts/chartlib.py` draws the chart furniture:

- a scalar field of Gaussian blobs, traced with marching squares and smoothed
  through Catmull-Rom into Béziers; closed polygons above the land level fill
  and hatch as islands, and the largest ones are labelled;
- soundings scattered over open water, kept clear of text boxes and the course;
- graticule, rhumb lines, compass rose, cartouche, neat-line with minute bars;
- a boat, lateral buoys, waypoints, a dashed course with bearings.

Fields can be larger than the sheet and drawn with an offset so a coastline
closes off-canvas and still fills as land (the Scrapy approach does this).

## Motion

SMIL only. Slow: the hero boat takes 48 s to sail its course, the packet boat 16 s,
the survey fills in over 14 s, the light sweeps every 9 s, the footer boat takes 70 s.

## Build

```
python3 scripts/build_assets.py        # every sheet, both editions; warns if text leaves the safe area
python3 scripts/build_stats.py         # live figures (GITHUB_TOKEN) → soundings sheet
```

`.github/workflows/profile.yml` refreshes the soundings daily. `snake.yml` draws
the contribution snake on the `output` branch in the chart's palette.
