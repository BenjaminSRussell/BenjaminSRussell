# 12 · Rendering performance engineer — what the sheets cost to animate

I profile compositing and SVG rasterisation. I traced the fourteen SVGs in `assets/` with a Playwright/Chromium harness (`scratchpad/perf/harness.js`: `<img width=870>`, 4–8 s trace, main-thread Paint plus raster-thread RasterTask per frame), built twenty hero variants to attribute cost, and read 05-motion-designer.md and spec-hero/approaches/supporting for the proposed motion.

## Measurements (Chromium 141, 870 px column, DPR 1)

| sheet | raw / gz KB | paths · use · lines | SMIL | repaints | raster + paint / frame | CPU while visible |
|---|---|---|---|---|---|---|
| hero | 269 / 86 | 184 · 332 · 110 | 1 animateMotion | 58/s | 18.3 + 3.3 ms | **127 % of a core** |
| approach | 137 / 42 | 174 · 400 · 23 | motion + rotate | 58/s | 8.4 + 4.0 ms | 75 % |
| survey | 138 / 40 | 154 · 370 · 24 | 55 opacity loops | 57/s | 7.0 + 1.6 ms | 51 % |
| log | 91 / 25 | 77 · 356 · 11 | 24 loops | 58/s | 4.0 + 3.1 ms | 44 % |
| footer | 26 / 7.5 | 38 · 75 · 6 | 16 loops | 55/s | 1.5 + 1.3 ms | 17 % |
| soundings, legend | 49, 55 | — | none | **0** | 0 | 0 % |

Phone (360 px, DPR 3): hero 8 + 3 ms/frame, 68 % of a slower core. Offscreen: 0 repaints. SMIL stripped: 0.

Five facts that set the budget (all measured; Chromium only, so re-run on WebKit/Gecko when `playwright install` is allowed):

1. **One moving pixel costs the whole sheet.** The 9 px boat re-rasters all of 1280×640 every frame; there is no dirty rect inside an `<img>`.
2. **Frozen is free.** Ended `fill="freeze"` one-shots and dormant `begin` chains cost nothing (5 repaints in 4 s).
3. **Change-only invalidation exists for `opacity` and `animateTransform` only.** A discrete opacity flash repainted 2× in 4 s; a translate with a 6 s hold repainted only during its 2 s of motion; 16 discrete translate steps repainted 16× in 8 s.
4. **`animateMotion` and geometry attributes (`cx`, `x`, `width`, `y2`) repaint every frame while active**, holds and `calcMode="discrete"` included (464 repaints in 8 s). The specs' "arrive and hold" boats, written as animateMotion, hold at full price.
5. **Clocks run offscreen.** A one-shot that begins at load has ended before the viewer scrolls to it (0 animated frames on scroll-in after 3 s). Only the first viewport's openings are ever seen.

Hero attribution (raster ms/frame of 16.1): `<use>` glyphs 2.7, contours 2.5, 110 graticule lines 1.7, hatch pattern 0, halo gradient 0, four `feGaussianBlur` halos +1.0–1.7. Rounding sheet-space coordinates to integers: 275→229 KB raw, 86→66 KB gz, raster −16 %.

## What is good

The `<use>` glyph library (94 defs, 332 placements) is the right call. Soundings and legend prove the strategy: zero cost when nothing loops. The footer is 10× cheaper than anything else and is where ambient motion belongs; 05 saw this and the specs honour it. Everything is under 300 KB (230 KB gz per page); no filters, masks or animated patterns today.

## What is bad, ranked

1. **The heaviest sheet carries the forever loop.** Hero: 127 % of a core for a boat moving 0.4 px per frame at 68 % scale, below one device pixel. Five sheets loop; a viewport shows two, so the page idles at 150–200 % of a core; on a phone that is heat and battery.
2. **The specs keep the mistake.** spec-hero: 96 s `animateMotion` boat plus a continuous 4 s heel loop on a sheet growing to 1280×740 with tints and 34 more soundings: ≈20 ms/frame forever. spec-approaches: 48 s animateMotion packet boat on a 1280×880 sheet (≈15 ms/frame, from approach + survey) whose 16 s "hold" still repaints. Openings are fine; two continuous loops on the two heaviest sheets are not.
3. **Openings below the fold are invisible** (fact 5): the 24 s survey, 14.4 s log, 3 s tide and 1.3 s leaders all finish unseen unless GitHub lazy-loads the `<img>` (check the live DOM for `loading="lazy"`).
4. **Geometry-attribute animation** in log and footer (`x`, `width`, `cy`, dashoffset) runs per-frame for its whole span; the spec's cursor (`attributeName="x" calcMode="discrete"`) would repaint 60/s for 14 s.
5. **110 graticule `<line>`s, 66 `<g opacity>` wrappers (217 opacity attributes on survey), 11.5 k path segments on the hero.** Each group opacity is a saveLayer; the graticule costs 1.7 ms/frame for what a pattern draws free.

## Fixes

- **Rule:** after its opening, any sheet over 8 ms/frame carries no continuous animation. Today only footer, log and survey pass; hero and approaches may not loop continuously.
- **Boats as `animateTransform`, never `animateMotion`.** `chartlib.course()` samples the smooth path into `type="translate" values="x y;…"` plus a `rotate` values list of headings (48–96 samples, spline). Identical at 68 %; holds become free.
- **Hero boat sails once and holds forever** (`fill="freeze"` at anchor, no heel loop). Lights as `calcMode="discrete"` opacity are the only indefinite things on the hero: ≈1 repaint/s. If out-and-back must stay, plot discrete fixes every 2 s: 0.5 repaints/s instead of 58.
- **Packet boat:** same transform treatment, 24 s run per 96 s (25 % duty) or finite. Lights discrete.
- **Log:** cursor rides a discrete `translate`; crawl bar scales a clipped rect by transform, not `width`; blink stays discrete opacity.
- **Footer stays the one continuous loop** (3 ms/frame); spec D is fine as written.
- **Lower openings:** delay to plausible scroll times (`begin="10s"`, `"24s"`, `"40s"`) with composed t=0 frames, or accept "the hero surveys itself; the rest is finished work". Do not ship 24 s of unseen motion.
- **Graticule as a `<pattern>` on one rect**; never animate `patternTransform`.
- **Round sheet-space coordinates to integers** in `_ntos` (one decimal inside glyph defs): −23 % gz, −16 % raster. Opacity on leaves, not single-child groups.
- **Night `feGaussianBlur` halos** are affordable only because flashes repaint rarely; never put a filter inside a continuously animated group.
- **CI gate** (`scripts/perf_check.js` from the harness): warm 6 s so openings end, trace 6 s; fail if a frozen sheet repaints, a lights-only sheet exceeds 2 repaints/s, or the ambient sheet exceeds 4 ms/frame; also run `--width=360 --dpr=3`.

## Ideas

1. **Dead-reckoning boat (bold).** No continuous sailing anywhere: every 2 s the hull jumps to the next fix and leaves a ⊙ with a time label, as a navigator plots a passage. The chart records the voyage instead of filming it, which is honest to a medium with no frame rate, and the hero drops from 58 repaints/s to 0.5.
2. **Reduced-motion and phone editions from one build**, chosen by `<source media>`: SMIL stripped for `prefers-reduced-motion`, frozen end state for phones, where 68 % of a core for a sub-pixel boat is indefensible.
3. **Filmstrip and perf as one job.** Playwright screenshots an inline copy at 0/25/50/75/99 % via `svg.setCurrentTime()` while the trace reports repaints/s and ms/frame; the still-frame rule and the budget share one CI run, and the colophon can truthfully say "this page idles at zero repaints".

## What it says about the maker

Now: someone who designs beautifully and lets the browser pay for it; the heaviest sheet does the most pointless work and the specs would double it. It should say: an engineer who understands the rendering model of the medium he chose, choreographs for it (freeze what can freeze, flash what can flash, move one cheap thing), and can prove it with a trace.

## Five lines

1. One moving pixel re-rasters the whole sheet: the hero spends 18 + 3 ms per frame, 127 % of a core, on a 9 px boat; after its opening, no sheet over 8 ms/frame may carry continuous animation.
2. Use `animateTransform` (translate + rotate values sampled from the path) instead of `animateMotion`, and `opacity` instead of geometry attributes: Chromium repaints those only on change, so holds, discrete flashes and plotted fixes are free, while animateMotion and `x/width/cx` repaint every frame even while holding.
3. The SMIL clock runs offscreen: openings below the first viewport are never seen, so delay them deliberately or keep openings to the hero and let the rest be finished work.
4. Round sheet coordinates to integers and draw the graticule as a pattern: −23 % gzip, −16 % raster per frame; keep filters out of anything that loops continuously.
5. Gate it in CI with the Playwright trace harness: frozen sheets 0 repaints, lights-only ≤ 2/s, the footer the only continuous loop at ≤ 4 ms/frame, plus a 360 px DPR 3 run.
