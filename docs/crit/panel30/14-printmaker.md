# 14 — Printmaker / copperplate engraver (works digitally too)

I cut plates and pull proofs, and I build SVG for a living. I looked at hero-day/night-2x, approach-scrapy-day-2x, the page renders, `chartlib.py`, `svgkit.py`, the hero SVG itself (275 KB) and spec-hero.md, through the lens of line, hatch, paper and hand.

## What is good

- **The lettering convention is an engraver's already**: upright roman for land, italic for water and shoals, small-cap mono in the title block. That is how a letter-engraver sorted a plate. Keep it, and say so in DESIGN.md.
- **Outlined type is economical**: `text_use` draws each glyph once and places it with `<use>`; 332 soundings glyphs cost 15 KB. That is what makes a real soundings field affordable.
- **The opening sequence (spec-hero §8) is the order a plate was cut**: outline, then tone (tints, soundings), lettering last, the name last of all. Letter-engraving was a separate trade that came after the chart-engraver. Make this deliberate; it is a true layer of meaning that costs nothing.
- Minute-bar neat line, double-ruled cartouche, round-capped danger line: the right furniture.

## What is bad (ranked)

1. **Every line is the same line.** Contours 0.6/1.0, graticule 0.6, coastline 1.0, neat line 1.2, hatch 0.7: five classes inside a 2× range, constant width, constant opacity. At 68 % in the README column they collapse to one grey and anti-aliasing finishes the job. A plate has a hierarchy: coastline heaviest and swelling, index, intermediate, hairline graticule, each ≥1.6× apart.
2. **The hatch is a pattern fill.** `hatch_defs` is a perfect 45° tile. No engraver ruled a hatch that did not vary; it reads as a texture swatch (Rustmapper Shoal, Scrapy Harbor on the current hero; the spec keeps the same tile for UNSURVEYED).
3. **The paper has no tone.** Flat cream, rounded-corner card, hairline at the very edge. A sheet has an unprinted margin, a plate mark, then the neat line. The rounded rect says "UI card", not "impression".
4. **Nothing has a hand in it.** No correction, no label spread across the thing it names. The one overlap on hero-day ("NOT FOR NAVIGATION" running out of the cartouche over sounding "19") is a bug, not a hand.
5. **The contours betray the procedure twice.** The `0.18·sin·cos` term wallpapers the sheet, so the top-left shows fingerprint rings cut by the neat line, and every contour is a smoothed cubic of identical gloss. Those cubics are **235 KB of the hero's 275 KB** (184 paths, four coordinates per 1–2 px step): the budget is spent on the least characterful element and leaves nothing for paper or hatch.
6. **Dashes are in phase.** Danger `0.1 4.2`, course `2 6`, tracks `1 4` all start at offset zero; neighbouring shoals' dots march in step and moiré at 68 %.
7. **Night weights are copied from day.** Light lines on a dark ground read heavier; the hairline that is quiet on cream is loud on navy.
8. **Soundings are a scatter**: one size, one opacity, perfectly upright, at `random.Random(seed)` positions. On a plate they were punched along the line of sounding and lean slightly.

## What needs to be done

**F1 Line hierarchy** (one table in chartlib). Coast 1.3, index 0.8, intermediate 0.45, graticule 0.3 at .5, neat line 1.2/0.5; night widths ×0.85. Swell on the coastline only: a second pass offset (+0.4, +0.4) at .35 opacity thickens the SE side the way a burin leans away from top-left light, which is also the hill-shading convention. Two strokes, no filter, ~2 KB.

**F2 Contour budget.** Emit contours as relative-integer polylines (`l`), subsample every third point, keep `smooth_path` for coastlines and the course only. Expect 235 → 50–70 KB. Replace the sine wallpaper with the edge falloff the spec already describes so no ring is cut by the neat line.

**F3 Hand-ruled UNSURVEYED hatch.** Individual lines from a seeded RNG: spacing 6 ± 12 %, angle −45° ± 1.5°, ends over/undershooting the band edge ±2 px, opacity .22–.34. ~95 lines, ~9 KB. Rule: vary per line, never along the line; wobble fakes a tremor, jitter records a ruler.

**F4 Coast vignette on land.** Sample the LAND polygon every 6 px, take the outward normal, draw three ticks stepping seaward (lengths 5/3.5/2, opacities .5/.3/.15). Hatching that follows form by construction; it is the Admiralty coast shading, ~8 KB per island.

**F5 Paper.** Square the sheet; 14 px unprinted margin; plate mark as a 1 px line at .16 with a 2 px `feGaussianBlur` inner shadow on one static `<rect>`. Grain: a 96×96 `<pattern>` of ~50 seeded dots r 0.6–1.2 at .05 (≈2 KB, no per-frame cost). Try `feTurbulence baseFrequency .9 numOctaves 2` first; if the 96 s boat loop makes Chrome repaint it, use the dot tile. Day only (see idea 3).

**F6 Dash phase and tapers.** Seeded `stroke-dashoffset` per path, gap 4.0–4.6; course `2 6` → `0.1 7` round caps (engraved courses were pecked). Wake and lead-line drops as three strokes of decreasing width/opacity, each 15 % shorter: a taper without filters.

**F7 Soundings as taken.** Weekly totals along the course (spec C4) plus a lean of ±2–3° toward the local course tangent; sizes 10/11/12 by class. On Approaches, set soundings on the survey track lines spaced by vessel speed. Soundings sat where the lead went down; that reads as decision, not fill.

**F8 Registration, day only.** Offset each second-colour element (nun, can, sector, accent arrow) by (+0.6, +0.4) from its outline. Two-pass printing never registered perfectly; nothing says "printed" faster.

## Improvements and ideas

1. **A manuscript correction, data-driven (bold).** "Corrected through Notice 5" is claimed and nothing shows it. Keep the previous build's values in stats.json; where a count changed, strike the old sounding with one 1.1 px diagonal and set the new value beside it in `plex-italic` 11, magenta `#A3267A` .85 (the ink of hand corrections on Admiralty sheets), "NM 5/26" in the margin. Every rebuild writes its own correction. Nothing invented.
2. **Names spread to the feature.** Letterspace each name to 70 % of its feature's diameter and bend the baseline along its long axis: a `text_use` variant placing glyphs along a quadratic with per-glyph rotation. "R U S T M A P P E R  S H O A L" across the shoal is the most engraved thing a chart does.
3. **Night is the plate, day is the print (bold).** No grain at night; instead one radial gradient, warm `#2A3B5A` at centre fading to the navy edge, .18 → 0. That is retroussage, the haze left by wiping the plate: the night sheet becomes inked copper before printing. Under 300 bytes, and a second-look layer the colophon resolves in half a line.
4. **State numbering.** Printmakers number reworked plates "state I, II…". Cartouche: "STATE {n}", n = commits that touched `assets/`. Real, measurable, a quiet joke for anyone who knows prints.

## What the page says about its maker

Now: someone with real taste found a chart aesthetic, built a competent generator and let the generator choose. Uniform line, swatch hatch and scattered soundings all read as fill, and a reader who has held a chart feels it before naming it. It should say: someone who knows a plate is a record of decisions, every line weighted on purpose, every sounding where the lead went down, corrections left visible because the survey is still running. "Months of team work" in a printed object is not more marks; it is marks that look placed, in a hierarchy, on paper with a surface, with one honest correction in another ink.

## Five most important lines

1. Four line weights ≥1.6× apart (coast 1.3 plus a 0.4 px offset second pass, index 0.8, intermediate 0.45, graticule 0.3), night ×0.85; today's near-identical hairlines collapse to grey at 68 %.
2. Contours are 235 of 275 KB: relative-integer polylines, subsample ×3, drop the sine wallpaper, spend the freed budget on paper and hatch.
3. No pattern fills: UNSURVEYED as individually generated lines with seeded spacing/angle/end jitter; land as a coast vignette of normal ticks that follow form.
4. Paper: square sheet, 14 px margin, plate mark with inner blur, seeded dot grain by day; one radial wipe gradient by night, so day is the print and night is the plate.
5. One data-driven manuscript correction in magenta whenever stats change, plus registration offsets on colour marks and seeded dash phase, so nothing on the sheet is perfectly in step.
