# 10 — Mobile / responsive design

**Who.** Responsive-design lead; I ship systems that must survive a 360px phone first. I rendered every current sheet at 360 and 720 CSS px (light and night), read the full-page renders, and read spec-hero §9, the only place the phone is specified.

## What is good

- The hero's display elements survive 28% scaling: "Ben Russell" (176 → 49px), the two-line italic thesis (40 → 11px, borderline), the red boat as a locus. A phone skeleton already exists.
- Soundings is the best phone citizen: five large figures (1,828 / 24 / 46 / 6 / Oct 2024) read at 360 unaided. That is the model: one row of big numerals, everything else texture.
- "Scrapy", "rustmapper" and the hand-placed "512" read at 360; place-name titles (spec E2) will too at display size.
- Vector delivery is a mobile advantage: GitHub mobile web allows pinch-zoom and an SVG re-rasterises crisp, so second-look layers are recoverable by pinching.
- `<picture>` already carries the night edition, so the delivery mechanism exists.

## What is bad (ranked)

1. **Six of seven sheets are navy rectangles on a phone.** All 13–15px type lands at 3.6–4.2 CSS px: cartouche, compass, buoy numbers, island names, legend columns, log lines, footer copy. The log is 124 CSS px of ruled nothing; the legend 90px of grey noise; the footer a 57px band. About 60% of the phone page carries no information.
2. **Spec §9 does not fix it.** It scales the hero to 720 and grows type ~15% while the display shrinks 50%: mono 15 and soundings 13 at 720 render at 7.5 and 6.5 CSS px on a 360 phone (328px inside GitHub's gutters). The phone edition as specified fails Standard 5's own test, and only the hero has one; the 1280×880 climax becomes a 248px thumbnail.
3. **Landscape letterbox.** Every sheet is 2:1 to 6.4:1. On a portrait screen the hero is 180 of ~640 usable px, below GitHub's header. The one chance to impress is a stripe.
4. **Motion on battery.** Five sheets loop indefinitely (hero: 184 paths, 332 `<use>`). SMIL inside `<img>` re-rasterises the whole image every frame, and mobile browsers do not reliably pause offscreen image animations. No hover, no watching the boat: cost without payoff.
5. **Night contrast.** Dimmed ink (.6) on navy, in sunlight, at 11px leaves only the thesis.
6. **Links around sheets** make a tap navigate instead of zoom. The draft removes them; keep it so.
7. **Weight is fine** (782KB raw, ~231KB gzipped per edition). Rasterisation, not bytes, is the mobile cost.

## What needs to be done

**F1. Phone type floor, in 720-space.** Displayed scale is 0.46–0.53 (328–380 CSS px). Minimum semantic type **26px** (→13 CSS px); texture soundings **18px** (→9); one display size **120–132**. Three sizes plus texture, nothing else. Rewrite §9: cartouche mono 26, bearings and light labels 26, names 30, thesis 40 on two lines, name 132.

**F2. Breakpoint 767px, not 600.** GitHub's profile collapses to one column below 768; between 600 and 767 the column is 570–740px showing a 1280 sheet at 45–58%. Serve the 720 edition at `(max-width: 767px)`.

**F3. Source order, most specific first** (the browser takes the first match):
```
<source media="(max-width: 767px) and (prefers-color-scheme: dark)" srcset="…-phone-dark.svg">
<source media="(max-width: 767px)" srcset="…-phone-light.svg">
<source media="(prefers-color-scheme: dark)" srcset="…-dark.svg">
<img src="…-light.svg" width="100%" alt="…">
```
Put `(prefers-reduced-motion: reduce)` sources for the desktop end-state edition above these; phone editions are low-motion by construction (F6), so six entries per sheet, not eight.

**F4. Portrait compositions.**
- *Hero* 720×900 (4:5): name and thesis in the top 40%; archipelago below; cartouche cut to four lines (name, role, chart no./edition, datum/Notice 5) at the foot; compass r 60 with N and the VAR note; 14 soundings nearest the course; four names; unsurveyed band 64px. Fills the first screen.
- *Soundings* 720×360: commits at 120, three figures at 26, tide curve full width beneath with dated HW/LW.
- *Approaches* 720×1200: transpose the geography so the channel runs south: survey ground top, G"1"…R"4" down the middle, anchorage inset at the foot; legend cut to the five symbols used on the phone page. Cheaper fallback: two `<picture>` elements, the second serving a 1280×1 transparent SVG on desktop, so the climax stacks as two 720×600 halves.
- *Log* 720×220: a table cannot survive. Two columns (TIME · REMARKS), last four entries at 26px mono, ending "14:05 nothing to report / Nothing on fire." The joke survives; the session lives in the alt text.
- *Instruments* 720×48: a single rule with the chart number. The stack is in plain text a line above. This is the "omit" mechanism: a `<source>` cannot be empty, but it can be a hairline.
- *Footer* 720×320: same scene, taller water, limit line and closing line at 26px.

**F5. Night-phone ink** ≥.85 opacity for semantic text; muted only for texture.

**F6. One animated sheet on phones.** Hero keeps the 4 s opening and the boat; every other phone sheet ships its end state. Lights may flash if testing shows clipped repaints.

## Improvements and ideas

1. **Bold: the boat is plotted, not sailed.** On the phone hero, replace `animateMotion` with `calcMode="discrete"` fixes every 4 s: the boat jumps to the next plotted position and a 26px time label updates beside it. That is how a passage is recorded on a real chart (dead-reckoning fixes), it says the data arrives in soundings rather than streams, and it cuts repaints from ~60/s to 0.25/s. Desktop glides; the phone plots.
2. **Reward the pinch.** Keep one dense texture zone per phone sheet (soundings near the course; the WAL tape) so a reader who zooms finds the real figures. Never captioned.
3. **Phone-only marginal note.** The hero's rotated pencil note on phones reads "small-scale edition · soundings thinned": the honest convention for what was culled, visible only to phone readers.
4. **The GitHub app** may ignore `<picture>` and show the `<img>` fallback. Verify; if so, make the hero fallback the 720 edition, the one sheet that survives both widths.

## Test plan

1. Playwright at 360, 390, 412, 600, 767, 768, 1024, 1280 CSS px; DPR 2 and 3; light/dark; reduced-motion on/off. Assert the selected source via `img.currentSrc`.
2. OCR each 360-wide render; every string marked semantic must be recovered. Soundings need not.
3. Filmstrip at 0/25/50/75/99% of the longest phone loop: no empty frame.
4. Battery proxy: 60 s DevTools trace at 390 wide; paint events per second per sheet ≤ 2 outside the hero's opening.
5. Wire weight through camo with gzip: each phone SVG < 120KB raw; phone page < 150KB on the wire.
6. Real devices: iOS Safari (Low Power Mode on and off), Chrome Android, GitHub app on both; pinch-zoom crisp; no sheet wrapped in a link.

## What the page says about its maker

On a phone it says: someone who designed a poster for a wall and never checked the pocket; six handsome navy stripes with a name on the first. It should say what the desktop page is beginning to say: a surveyor who knows the scale of a chart decides what goes on it, and who draws the small-scale edition with the same care, culled soundings and all. A chart that is correct at every scale it is published at is the whole discipline.

## Five most important lines

1. At 360px six of seven sheets are navy rectangles: all 13–15px type lands at 3.6–4.2 CSS px, and spec §9's phone edition still renders mono at 6.5–7.5 CSS px, so it fails Standard 5 as written.
2. Phone type floor in 720-space: 26px semantic, 18px texture, one display size 120–132; three sizes and nothing else; night-phone semantic ink ≥.85.
3. Breakpoint `(max-width: 767px)` to match GitHub's single-column layout; sources most-specific first (phone+dark, phone, dark, img), reduced-motion above.
4. Portrait editions: hero 720×900, approaches transposed to 720×1200 with the channel running south, log cut to a two-line coda, instruments a hairline rule; one animated sheet on phones.
5. Bold: on phones the boat is plotted in discrete 4 s fixes with a time label instead of gliding; honest to how passages are recorded, and ~240× fewer repaints.
