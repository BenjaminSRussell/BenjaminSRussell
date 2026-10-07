# Design notes — profile v7 "Signal & Structure"

The README is a designed page, not a template. These notes keep it coherent.

## Idea

Everything Ben builds points the same way: the open web goes in messy, trusted
rows come out. The hero draws exactly that (a tangle of nodes → a parser → rows),
and every other asset reuses the same three ingredients: hairline structure,
one warm signal colour, and small tracked mono captions.

## Palette

Backgrounds are transparent. Artwork sits on GitHub's own page colour, so there
is never a "different black" seam, and every asset ships in two themes selected
with `<picture>` + `prefers-color-scheme`.

| Token    | Dark      | Light     | Use                                   |
|----------|-----------|-----------|---------------------------------------|
| ink      | `#F3EFE7` | `#131417` | display type, primary text            |
| ink2     | `#B9BCC6` | `#454A55` | body copy inside artwork              |
| muted    | `#7D8290` | `#7A7F8C` | captions, mono labels                 |
| hair     | `#2A2F3A` | `#DCDFE5` | hairlines, chip borders, meters       |
| panel    | `#13161C` | `#F6F7F9` | chip and node fills                   |
| accent   | `#FF5A1F` | `#E8501A` | the signal: packets, cursors, numbers |
| ok       | `#4ADE9B` | `#15A86D` | "clean / done" states only            |
| cool     | `#6FB7FF` | `#2E86E6` | the open web, fetch                   |

One accent. Green only means "ok". Blue only means "web". Nothing else is coloured.

## Type

- Display: **Inter Display Bold**, tight tracking (−4 to −2 px), for the name and card titles.
- Text: **Inter** Regular / Medium / SemiBold for copy inside artwork.
- Captions: **DejaVu Sans Mono**, 11–12 px, uppercase, +1.6 px tracking.

All type inside SVGs is converted to outlines by `scripts/svgkit.py`, so it renders
identically everywhere (GitHub serves `<img>` SVGs without web fonts). Subsetted
fonts live in `scripts/fonts/` (SIL OFL / Bitstream licences included).

## Grid and sizes

Every asset is 1280 wide and shown at 100% width, so one horizontal grid holds
across the page: 48 px outer margin, 24 px gutters, 22 px dot-grid in diagrams.

| Asset             | Size       |
|-------------------|------------|
| hero              | 1280 × 440 |
| stats             | 1280 × 212 |
| project cards     | 1280 × 300 |
| terminal          | 1280 × 392 |
| stack             | 1280 × 150 |
| footer            | 1280 × 150 |

## Motion

SMIL only (no JS runs inside README images). Slow and purposeful:
packets travel pipelines (6–9 s loops), rows resolve in sequence, a terminal types
and loops every 14 s, the sailboat crosses the footer in 75 s. Nothing flashes.

## Build

```
python3 scripts/build_assets.py        # all static assets, dark + light
python3 scripts/build_stats.py         # live numbers (GITHUB_TOKEN) → stats SVGs
```

`.github/workflows/profile.yml` refreshes the stats daily; `snake.yml` regenerates
the contribution snake on the `output` branch in the same palette.
