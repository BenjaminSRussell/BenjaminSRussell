# Crit 07 — Type designer

Type designer; text faces and editorial identities. I looked at hero-day/night-2x, log-day-2x, soundings-night-2x, page-day-full, then opened the vendored fonts and `svgkit.py` with fontTools to measure what the renders only hint at.

## What is good

- **Instrument Serif at 176px is the right face in its only home.** A display cut: hairlines 25/1000 em, stems 76 (3:1 contrast), 51% x-height. At 176px the hairline is 4.4px and the serifs over the contour field are the one image nobody else on GitHub has. Tracking −3 is right at that size.
- **The pairing is sound in principle.** Plex Mono is near-monoline (hairline 69, stem 85): contrast of construction against the serif. Every digit is 600 units, so soundings align without `tnum`.
- **Italic already carries meaning.** Shoal and harbour names are italic, as water features should be, and "upright = measured, italic = illustrative" has a real precedent: surveyed soundings upright, soundings from older or smaller-scale sources sloped, drying heights underlined. Keep it.
- **Kerning is applied.** svgkit reads GPOS pairs (1,749 Regular, 1,502 Italic); "Ru" is kerned −14.

## What is bad, ranked

1. **A display face is being asked to work at text sizes it does not have.** One optical size, one weight. The hairline at 15px (island names) is 0.375px; in the README column (×0.68) 0.26px; on a phone 0.1px. Day loses the hairlines to anti-aliasing; night blooms the stems and the italic place names turn into dashed grey. The specs ask for *more* of this (14px pencil notes, 14–19px place names, 16–18px sign-offs), all where the face is weakest.
2. **All-caps mono is over-tracked and the separators are broken.** `cap()` adds +1.8px at 11px (0.16 em) to 600-unit caps with a 600-unit space; "BENJAMIN S.  RUSSELL" reads as three words. Mono caps want 0.04–0.08 em.
3. **The middle dot is mis-fitted and svgkit cannot help it.** Instrument Serif's "·" has zero sidebearings (adv 105, bounds 0–105) and the italic "r" overhangs −36, so "developer · scraping" sets 123 units left of the dot and 181 right: visibly "developer· scraping" in both cartouches. Tracking is also added to the space glyph.
4. **No ligatures.** The Italic "f" overhangs 131 units; svgkit maps characters one by one and never fires `liga`, so "fire" and "flight" (17px and 28px in the specs) set the f hook into the i's dot. fi/fl are in the subset, unused.
5. **Lining figures in running italic.** No `onum`; figures sit at 730, above the caps (720), so "512 lead lines" has three capitals shouting from a lowercase line; on Soundings a lone "6" at 96px is an orphan.
6. **Plex Mono's dotted zero is the wrong zero for soundings.** Three contours; at 11px × 0.68 the dot fills the counter and "10, 20, 30" read "1●, 2●, 3●". The subset has no plain zero.
7. **The scale has a hole.** Hero: 176 / 34 / 22 / 15 / 11 / 9.5; nothing between 34 and 176. The specs add 96, 46, 40, 28, 17, 13 as local decisions, so sizes will drift sheet to sheet.
8. **The phone floor is still too low.** The 720 edition at 360px is ×0.5: 13px soundings render at 6.5px, 15px mono at 7.5px; Plex Mono's counters close under 9px.

## What needs to be done

1. **Type floor by rendered size.** Semantic text ≥13px at 1280 (≈9px rendered) and ≥18px on the 720 phone edition, soundings there culled to the real upright ones at 16px. Build check: rendered px of every `_EXTENTS` run at ×0.68 and ×0.5; fail under 9 unless tagged texture.
2. **Grade compensation per edition, in svgkit.** Outlines can be stroked: add `grade` to `text()`. Day, serif ≤24px: `stroke=fill stroke-width=0.22 paint-order="stroke"` (ink spread restores the hairline). Night, serif ≤24px: a 0.18px paper-coloured stroke (a choke against bloom); night mono ≤13px in Plex Mono **Light** (OFL, vendor it); night small ink `#C9D3E3`, the 176px name at full ink.
3. **Fix the fitting primitives.** No tracking on spaces; synthetic thin (0.2 em) and hair (0.1 em) space advances for separators; apply `liga`; a manual kern table per font for pairs the font lacks (`r·` +40 italic). Cap tracking at 11–13px: 0.6–0.9px.
4. **Lettering by feature class, as a chart does.** One table in `chartlib`: *water, submerged, floating* (shoals, harbours, buoys and their characters) → italic; *dry, fixed* (islands, lights, structures, bearings, title block) → upright; figures upright if measured, italic if not, underlined if above datum. So `R "2" Fl R 4s` goes italic (a buoy floats), `Grafana Lt Fl(3) 10s` stays upright, and the legend says once: "Upright: measured, fixed, dry. Sloping: illustrative, floating, submerged."
5. **One scale,** enforced by the build: 11 (texture) · 13 · 17 · 22 · 28 · 36 · 46 · 60 · 96, plus 176 as the one exception, hero only. Sea areas 28, shoals 17, islands 17, structures 13, soundings 11. Figures inside a serif sentence are set in Plex at 0.86× the serif size.

## Improvements and ideas

- **Add IBM Plex Sans Condensed (OFL): the one extra face that is justified.** Charts letter soundings, bearings and title blocks in a condensed grotesque, not a typewriter face. It is the mono's own family, with a plain zero, tabular figures and a true italic; it sets "SURVEYED 2024 – 2026 · RUSTMAPPER ON PYPI" 35% narrower, which is how cartouche lines reach 13–14px without wrapping. The mono then means one thing: the machine spoke (log, WAL tape, `pip install`). Three voices: serif = the chart maker, condensed = the chart, mono = the instruments. No small caps: Instrument Serif has no `smcp`, scaled capitals drop weight, and the condensed caps do the job.
- **Bold: the night edition in a second weight.** Set every night figure and label in Plex Light so only the lights, the name and the rose arrow carry full ink. Day and night then differ in *weight*, the clearest sign the editions were designed, not inverted.
- **Hand-set the one word that matters.** "Ben Russell" repeats two l's and two s's exactly at 176px; a lettered title never does. Raise the second "l" 1.5px, open "ss" 2 units, kern `Ru` to −20 by hand.
- **Contour-following labels.** `textPath` is static SVG and works on GitHub: set "UNSURVEYED" and one sea-area name along a contour instead of rotated −90°; a label on a curve is the chart idiom the page is missing.

## What the page says about its maker

Now: someone with real taste who chose two good fonts and trusted them to do the rest; the system was set at display size and copied down, so the fine print fails first. It should say: this person knows a 25-unit hairline and a dotted zero behave differently at 7px than at 176px, and wrote the rules so the detail survives the medium. Rigour at the smallest scale is what the README claims for his crawlers; the type should prove it.

## Five most important lines

1. Instrument Serif is a single-optical-size display face (hairline 25/1000 em); at 14–19px it renders at 0.26px in the README column, so add per-edition grade strokes in svgkit (day spread 0.22px, night choke 0.18px) and never set it under 17px.
2. Cut all-caps mono tracking from 1.8px to ≤0.9px, stop adding tracking to spaces, add thin/hair-space advances, and apply `liga`; "developer· scraping" and the "fire"/"flight" f–i collisions are fitting bugs, not design.
3. Adopt IBM Plex Sans Condensed (OFL) for soundings, bearings and title-block captions: plain zero, `tnum`, true italic, 35% narrower, so semantic text reaches 13–14px; keep Plex Mono for machine output only and vendor Plex Mono Light for night.
4. One scale (11 · 13 · 17 · 22 · 28 · 36 · 46 · 60 · 96, plus 176 on the hero), enforced by the build, with lettering assigned by feature class: upright for measured/fixed/dry, sloping for illustrative/floating/submerged, underlined for heights above datum.
5. The phone floor is ≥9px *rendered*: 18px on the 720 edition; add a build check that computes rendered size at ×0.68 and ×0.5 for every text run and fails anything semantic below it.
