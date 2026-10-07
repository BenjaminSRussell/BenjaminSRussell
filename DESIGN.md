# Design notes — profile v7 "Signal & Structure"

The README is a designed page, not a template. These notes keep it coherent.

## Idea

Everything I build points the same way: the open web goes in messy, trusted
rows come out. The hero draws exactly that (a tangle of nodes → a parser → rows),
and every other asset reuses the same three ingredients: hairline structure,
one warm signal color, and small tracked mono captions.

## Palette

Backgrounds are transparent. Artwork sits on GitHub's own page color, so there
is never a "different black" seam, and every asset ships in two themes selected
with `<picture>` + `prefers-color-scheme`.

| Token    | Dark      | Light     | Use                                   |
|----------|-----------|-----------|---------------------------------------|
| ink      | `#F3EFE7` | `#131417` | display type, primary text            |
| ink2     | `#B9BCC6` | `#454A55` | body copy inside artwork              |
| muted    | `#7D8290` | `#7A7F8C` | captions, mono labels                 |
| hair     | `#2A2F3A` | `#DCDFE5` | hairlines, chip borders, meters       |
| line     | `#3A4150` | `#C4C9D2` | diagram strokes, one step above hair  |
| soft     | `#4B5160` | `#C3C7CF` | quiet fills that still have to read   |
| panel    | `#13161C` | `#F6F7F9` | chip and node fills                   |
| accent   | `#FF5A1F` | `#E8501A` | the signal: packets, cursors, numbers |
| ok       | `#4ADE9B` | `#15A86D` | "clean / done" states only            |
| cool     | `#6FB7FF` | `#2E86E6` | the open web, fetch                   |

One accent. Green only means "ok". Blue only means "web". Nothing else is colored;
the language bar in the stats strip is a tonal ramp from the accent through the inks.

## Type

- Display: **Inter Display Bold**, tight tracking (−4 to −2 px), for the name and card titles.
- Text: **Inter** Regular / Medium / SemiBold for copy inside artwork.
- Captions: **DejaVu Sans Mono**, 12–12.5 px, uppercase, +1.6 px tracking. Sized for the
  profile page, where the README column is about two thirds of the 1280 canvas.

All type inside SVGs is converted to outlines by `scripts/svgkit.py`, so it renders
identically everywhere (GitHub serves `<img>` SVGs without web fonts). Subsetted
fonts live in `scripts/fonts/` (SIL OFL / Bitstream licenses included).

## Grid and sizes

Every asset is 1280 wide and shown at 100% width, so one horizontal grid holds
across the page: 48 px outer margin, 24 px gutters, 22 px dot-grid in diagrams.

| Asset             | Size       |
|-------------------|------------|
| hero              | 1280 × 420 |
| stats             | 1280 × 226 |
| project cards     | 1280 × 318 |
| terminal          | 1280 × 384 |
| stack             | 1280 × 220 (height follows the chip rows) |
| footer            | 1280 × 150 |

## Motion

SMIL only (no JS runs inside README images). Slow and purposeful:
packets travel pipelines (6–9 s loops), rows resolve in sequence, a terminal types
and loops every 14 s, the sailboat crosses the footer in 75 s. Nothing flashes.

## Build

```
python3 scripts/build_assets.py        # all static assets, dark + light; warns if text leaves the safe area
python3 scripts/build_stats.py         # live numbers (GITHUB_TOKEN) → stats SVGs
```

`.github/workflows/profile.yml` refreshes the stats daily; `snake.yml` regenerates
the contribution snake on the `output` branch in the same palette.
