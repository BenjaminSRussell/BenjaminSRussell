# Re-crit 2 — 28 Art director — final build

Judged the regenerated qa/ PNGs only (readme light/dark, six sheets day/night/phone, 2x crops, four filmstrips, check.md). Coordinates at 1280 (social/hero-day.png) unless marked.

## J1–J12

| # | Was | Now | Evidence |
|---|---|---|---|
| J1 | 3 | 3 | Unchanged: name, one italic line, no second slogan (crops/hero-title.png). |
| J2 | 2 | 3 | The error is now in frame on every surface: dashed-as-charted vs solid-as-surveyed outlines, PA once, "sitemap.xml lies again — see Sheet 3" with its pointer back, and the README capture (readme-light 90–620) carries all of it. The hatch band is still a swatch (see below) so this is a 3 without margin. |
| J3 | 3 | 3 | Six silhouettes, no shared eyebrow; Sheet 5 phone now a three-row list, Sheet 3 phone a tall harbour with its own legend. |
| J4 | 3 | 3 | SOUNDINGS IN COMMITS · DATUM: MAIN · IALA REGION B · CORRECTED THROUGH NOTICE 9 on the hero; URLS · THOUSANDS on Sheet 3. |
| J5 | 2 | 2 | Sheet 3 phone has a 12-entry SYMBOLS block now (approaches-phone 60–1100 × 2340–2700) — good. But the hero phone still carries SMALL-SCALE with no gloss (hero-phone 1000–1040 × 730–960) and the boxed A/B/C on the approaches phone are not in that legend. |
| J6 | 3 | 3 | 512/308/265/173/87 on Sheet 1 and Sheet 2; Sheet 2's tail 17 15 0 0 0 108 37 146 73 13 358 is the hero channel; chart no. 21 = 21 repos. |
| J7 | 2 | 2 | Unit now stated: "soundings along the course: commits per week" along the limit line, Sheet 3 legend "Sheet 1 · week's commits" / "Sounding · 1000s, 100s". But the channel now holds ~25 upright "0"s and one "1" (840–1000 × 300–470), which still read as stippling, not slack weeks. |
| J8 | 2 | 3 | frames/hero t=0 and t=0.5 are finished sheets: cartouche, islands, hatch, SEE SHEET 3 box, PA outline all present before any sounding; approaches/footer/log strips the same. |
| J9 | 2 | 3 | Notices 6–9 collapsed to one line "rustmapper 0.1.0 · 0.1.1 · 0.1.2 · 0.1.3 · 8 Nov 2025" (readme-light 4730). Only costume left is the log's ▮ cursor on a static line. |
| J10 | 3 | 3 | Link row and the three-row table in the first screen, unchanged. |
| J11 | 2 | 3 | Hero night: R"2"/G"1" now have real halos (crops/hero-entrance-night 330–400 × 220–340), the pencil note survives in grey; Sheet 3 night and the footer sail unchanged. |
| J12 | 3 | 3 | VAR 14h, Wk '25 wreck, "watch kept by cron", "Obstn rep. 2026 (PA)", Sheet 6 shaded in the index — all still there, still uncaptioned. |

**J-total: 34/36** (was 30).

## Round-1 defects

- **Proof-layer timing — FIXED.** Note, PA outline, SEE SHEET 3, bearings and light characters are in the first group; the README render matches hero-day.png.
- **Hatch swatch — NOT FIXED.** Measured on social/hero-day.png at x 1150–1240: hatch ink runs y 149→580; cream from the neat line (y 40) to 149 and from 580 to 715. Identical to round 1. Same on the phone: hatch y 412→1070 inside a neat line at 25/1325.
- **Cluster — HALF FIXED.** Numerals are in the sounding register now (37₂ 358₁ 108₄ 146₄ 15₂ 17₁, ink, subscript tenths), PA appears once, the unit is glossed. Still two outlines per shoal, and the zeros are still "0" — more of them than before.
- **Notices stutter — FIXED.** One line, four linked editions, one date.
- **Phone instruments — FIXED.** instruments-phone is 1080×300, LEAD / LOG / LOOKOUT in three rows with the full stack; the 72px nub is gone.
- Label hierarchy (lower on my list): fixed on the phone ("Game Engine I." and "Scrapy Harbor" are now italic serif), not on the 1280 hero, where GAME ENGINE I. and SCRAPY HARBOR are still the same caps at the same size.

## New defects

1. **The 208° junction is a collision.** At 3x (hero-day 840–980 × 420–540): "15₂" overprints the surveyed outline of the 108 shoal, a "0" sits on the 37 shoal's edge, grey "13" lands on "208°" and the blue channel, "7₃" collides with the 358 outline. check.md flags the 15₂/108₄ pair at 18 px. The best idea on the sheet is now legible but crowded.
2. **Zero stippling.** ~25 "0"s plus one "1" across the channel water read as a texture fault; on the phone it is "0" and "3₃" alone at 840,725. Draw slack weeks as the no-bottom dash or drying underline, as asked.
3. **Phone hero labels still float.** "Scrapy Harbor" sits over "265₅" (hero-phone 355–580 × 880); "Data Science Bank" crosses the 308₄ danger line (590–890 × 985).
4. Minor, still open: log ▮ cursor on a static line; "robots.txt" touches both edges of its dashed box on Sheet 3 phone; Sheet 3 phone's bare "←— N" without the rose ring; footer 9 8 7 5 4 3 unitless on its own sheet.

## Months of work?

Yes, now without the asterisk I had to add last time. The two things that made the page look generated — a hero that drew its headline before its evidence, and a notices list that looped — are gone, and the README reader sees the same sheet the filmstrip ends on. The phone edition finally has a legend and a real Sheet 5. What remains is a single unmoved rectangle (the hatch that still stops 110 px short of the top neat line and 135 px short of the bottom, on the one sheet that is the cover) and one crowded square inch at 208° where the year's soundings were promoted to ink without being given room. Both are last-day fixes; neither is a concept problem. A stranger would believe a hydrographer and a studio made this, and would believe they ran out of a day, not a month.

## Summary
- J-total: 34/36 (was 30)
- Fixed: proof-layer timing, notices stutter, phone instruments, phone label hierarchy, pencil-note pointer, night hero lights
- Still open: hatch swatch (unchanged, y 149→580 of 40→715), cluster zeros and double outlines, SMALL-SCALE unglossed, 1280 label hierarchy, log cursor
- New: 208° junction collisions (15₂/108₄/13/208°), zero stippling across the channel, phone hero labels over their own soundings
