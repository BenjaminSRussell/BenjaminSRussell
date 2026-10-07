# 11 — Front-end engineer, GitHub Markdown pipeline

I build things that have to survive github/markup, the html-pipeline sanitizer, camo and `<img>`-mode SVG. I read README.md, README.draft.md, the three specs and profile.yml, took the hero/log/soundings/footer SVGs apart (element counts, timing attributes, refs), and HEAD-requested the live raw asset for real cache headers.

## What is good

- **The SVGs are built right for `<img>`.** No `<text>`, `<style>`, `<script>` or external refs. Glyphs are `<path>` defs reused via `<use href>` (hero: 332 uses over ~90 glyph paths), so a sheet full of type is 85 KB gzipped, not 275 KB, and raw.githubusercontent does gzip it (confirmed).
- **Root `<svg>` has `viewBox` plus `width`/`height`**, which with GitHub's `width="100%"` and injected `max-width:100%` scales correctly in every engine.
- **Timing is well-formed**: `values`/`keyTimes` counts match, every loop divides into the 48/96 s grid, `rotate="auto"` on the boat, no filters today.
- **Honest `alt`.** In `<img>` mode the `<img alt>` is the only accessible name (the root `aria-label` is ignored); the draft puts the content in the right place.

## What will not work as assumed, ranked

1. **`prefers-color-scheme` follows the OS/browser, not GitHub's theme.** OS light + GitHub Dark shows the day sheet on #0d1117; OS dark + GitHub Light shows the night chart on white. GitHub's `<picture>` support cannot override this. The v9 night edition must never assume page colour: no transparent paper, no halos fading to a page-matched navy (#0F1A2B ≠ #0d1117; "Dark dimmed" is #22272e).
2. **The one-shot openings mostly play unseen, and differently per browser.** An `<img>` SVG runs on its own clock: Firefox starts at load; Chrome and WebKit start on first paint and may suspend off-screen. Approaches (the 24 s survey) sits ~1000 px down; in Firefox it has finished before anyone scrolls there. The frozen end state must therefore be the best frame of every sheet; only the hero's 4 s opening is guaranteed an audience.
3. **Phone edition via `media="(max-width: 600px)"` is undocumented.** The sanitizer allowlists the `media` attribute, not its value, so it will almost certainly pass, but GitHub documents only `prefers-color-scheme` and a later tightening would drop it silently (fallback: desktop sheet, harmless). Media queries test the viewport, not the 870 px column. Order matters: phone×dark, phone×light, dark, then `<img>`. A `prefers-reduced-motion` `<source>` has the same status and costs two more files per sheet.
4. **Cache: the delay is small, the obvious fix is wrong.** Live headers: `cache-control: max-age=300`, ETag, Fastly. Camo forwards upstream Cache-Control, so a new sheet is visible within ~5 min at the edge plus up to 5 in the browser. Do not bust with a daily `?v=`: it forces a README commit every morning and defeats camo's URL-keyed cache. Rename files only on design releases (`hero-v9-*.svg`).
5. **The spec reintroduces the two things that cost real CPU in `<img>` SVGs.** (a) `feGaussianBlur` halos on flashing lights: a filter with an animated input is re-rasterised every frame, per mark, per sheet, forever. (b) `<pattern>` hatching at 0.68 scale: tiles are rasterised then tiled, and Chrome shows seams and moiré at 45° with 5–6 px tiles.
6. **Hairlines below the pixel.** 132 of 196 hero strokes are 0.5–0.6 px, often at `stroke-opacity .07–.29`. At 0.68 scale on a 1x display that is a 0.34–0.41 px grey smear; on a phone, 0.14 px. The spec's night contours at .30 opacity will vanish on 1x monitors.
7. **`height` is a trap.** GitHub's CSS sets `max-width:100%` but not `height:auto`, so `width="1280" height="640"` shrinks the width and keeps 640 px of letterbox. Keep `width="100%"` only, accept layout shift, keep the hero first in DOM (fetch) order.
8. **Event-wired SMIL is the fragile part of the spec.** Syncbase `.begin/.end` is solid in all three engines; `repeatEvent` and `keyPoints` on `animateMotion` with `calcMode="spline"` are where WebKit has diverged. Every element that fades in with `fill="freeze"` needs base `opacity="0"` or it flashes before `begin`.
9. **The workflow ships whatever it draws.** profile.yml has no validity, size or bounds gate before `git add assets/*.svg`; one bad float is a broken image for 24 hours, and a quietly failing job leaves "taken daily" stale on a sheet that claims it. Output must stay deterministic so no-change days make no commit.
10. **Small things.** `#colophon-how-the-chart-was-drawn` resolves (GitHub slugs the heading's text including the `<sub>`) and breaks on any copy edit. `<sub>` in an h2 inherits 600 weight and drops below baseline. The file header still says "profile v7". Glyph ids repeat across sheets: harmless in `<img>`, fatal the day two sheets are inlined in a preview, because the first `#hatch` wins.

## What needs to be done

- Static radial-gradient circle with animated opacity instead of `feGaussianBlur`. Same halo, no filter cost.
- Hatching as explicit `<line>`s inside a `<clipPath>` (a 130×430 band at 6 px is ~90 lines), not `<pattern>`.
- Stroke floor 0.9 px at 1280 for anything semantic; texture may be 0.6 at opacity ≥ .25.
- Phase-lock, don't event-wire: the tack flip is a 96 s `calcMode="discrete"` animate on the hull sharing the boat's `begin`; soundings get computed `begin` times. Base `opacity="0"` on every freeze-in element.
- `<a name="colophon"></a>` before the heading (GitHub prefixes `user-content-` and resolves `#colophon`); eyebrow as `<sub><i>…</i></sub>`.
- Opaque paper and neat line in both editions; prefix ids per sheet in svgkit.
- Gate the Actions commit: `xmllint --noout`, `gzip -9 | wc -c` ≤ 100 KB, element count ≤ 3000, bounds, filmstrip; fail loudly.
- Verify the sanitizer, not the docs: `gh api /markdown -f mode=gfm -F text=@README.draft.md` (blocked from this sandbox, fine locally) shows exactly what survives; then a scratch repo on Chrome, Firefox, Safari, iOS Safari and the GitHub iOS app, in all four OS×GitHub theme combinations; check whether `<picture>` gets GitHub's `<a target=_blank>` wrap; filmstrip with headless Chromium via `svg.pauseAnimations(); svg.setCurrentTime(t)`.

## Improvements

- **Make the full-size sheet the second look.** Wrap each `<picture>` in `<a href="raw…svg">`: the raw file opens as a document, SMIL running, at 1280 with the 11 px soundings legible.
- **Bold: resurvey instead of one-shot.** Since the opening cannot wait for scroll, let each one-shot repeat on the 96 s grid (survey 24 s, hold 72 s). A late visitor still sees the chart draw itself once, and the standards already guarantee the hold is a finished sheet.
- **Print `stats.updated` on the soundings sheet**, so a stalled workflow is visibly stale rather than silently wrong; it closes the loop on "taken daily".
- **Reduced-motion edition** from the same build with animations stripped, shipped as a `<source>` and kept as the fallback if GitHub ever restricts media values.

## What it says now, and should say

Now: someone who understands exactly what GitHub's `<img>` sandbox permits and built a type-as-outlines pipeline most front-end engineers would not attempt. The risk is that v9 spends that credibility on filters, patterns and event chains that are correct in theory and wobbly in a 68%-scaled `<img>` across three engines. It should say: the person who knows the platform well enough to make its constraints invisible, so the reader thinks about the chart and never about the renderer.

## Five lines

1. `prefers-color-scheme` follows the OS, not GitHub's theme: every edition needs opaque paper and must look deliberate on the wrong page colour.
2. One-shots run on the image's own clock (load in Firefox, first paint in Chrome/WebKit), so below-fold sheets play unseen; make the frozen end frame the sheet, or loop the survey on the 96 s grid.
3. Drop `feGaussianBlur` on animated lights and `<pattern>` hatching; use gradient-circle halos and explicit clipped lines. Stroke floor 0.9 px, opacity floor .25.
4. Cache is `max-age=300` end to end, so never `?v=` daily; gate the Actions commit with xmllint, gzip ≤ 100 KB, element count, bounds and filmstrip, and print `stats.updated` on the sheet.
5. Verify the sanitizer with `gh api /markdown` on the draft, then a scratch repo across Chrome/Firefox/Safari/iOS and all four theme combinations; `max-width` and `prefers-reduced-motion` `<source>`s are undocumented and must be proven before they are relied on.
