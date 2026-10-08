# Re-crit 2 — 07 Type designer — final build

Judged from the regenerated snapshot: `sheets/*-{day,night,phone}.png` (870 / 1080), every 2x crop in `crops/`, `readme/readme-light.png`, `frames/*/strip.png`, `check.md`, plus 2x crops of `assets/v9/*.svg` rendered with `crop.mjs` where a size had to be measured. Sizes are measured off glyph bands (caps band = cap height ÷ 0.70; mixed-case band ÷ 0.96), native at 1280, rendered at 870 (×0.68); phone rendered at 360 (×0.5).

## J1–J12

| # | Score | Evidence |
|---|---|---|
| J1 | 2 | Thesis still said three times: hero italic line, footer "The chart ends here. The web doesn't.", and the prose paragraph "Most of what I build is survey work…" (readme-light.png y 900–990). Unchanged. |
| J2 | 3 | hero-day.png, name covered: soundings thin 512→0 eastward, LIMIT OF SURVEY 2026, hatched UNSURVEYED, PA 87₆ half in the hatch. |
| J3 | 3 | Six silhouettes still unshared; the Instruments phone sheet is now a real seventh (three words, three stacked lists) instead of a bare rule. |
| J4 | 3 | approaches-day.png: the four channel lights now carry four characters, R"4" Fl(2) R 10s, R"2" Fl R 4s, G"3" Fl(2) G 10s, G"1" Fl G 4s. Fixed. |
| J5 | 3 | approaches-phone.png y 1690–1920: SYMBOLS block of 12 entries ("G can · port, returning", "Wk · dead branch, year", Rep/ED/SD) at ~13.5 px rendered on the 360 phone; every abbreviation on the phone sheet is now resolved. |
| J6 | 3 | Last six soundings 108 37 146 73 13 358 on Soundings row = the six upright hero figures; HW 358 on the curve; 1,665 on Soundings, log last line and caption; 0.1.3 on hero, Approaches, log, prose. Unchanged. |
| J7 | 3 | 1,665 mine · 1,966 all hands · 1,828 by GitHub's calendar; "Heights observed, not predicted."; upright/sloping rule declared once and kept; POSITION-EMPTY still honest. |
| J8 | 2 | frames/hero/strip.png: t=0 already carries name and thesis, no frame is empty; instruments-phone is no longer an empty still. Easing not judgeable from stills. |
| J9 | 3 | readme-light.png y 4540–4700: five numbered principles under "five principles"; the four PyPI lines are now one line, "Notices 6–9, editions: rustmapper 0.1.0 · 0.1.1 · 0.1.2 · 0.1.3 · 8 Nov 2025". Fixed. |
| J10 | 3 | Links row, three-row table, one paragraph under the hero; the table's empty header row (readme-light.png y 718–732) is still emitted. |
| J11 | 3 | Night is now reweighted, not only recoloured: hero-night.svg carries 5 choked runs (`stroke-width="0.18"` in paper colour) and the sans/mono go to the Light cuts (`NIGHT_LIGHT_CUTS`); measured ink coverage at 870 drops day→night from 0.26→0.13 on "FashionDB Bank", 0.099→0.072 on a log row, 0.125→0.090 on the legend, and the mono's dotted zero in "timeout 0%" keeps its dot at night (log-night.png 320–620, 160–188). |
| J12 | 3 | Soundings = commits, "sitemap.xml lies again", "Nothing on fire." at 1431, 19:47 UTC / "1947 UTC", 429 Shoal, Wk '25 = fix/144-lean-docker-extras, "14 · good holding". Rose still captioned "AUTHOR'S LOCAL TIME". |

**J-total: 34/36** (was 29). No zero; J1, J2, J7, J10 all ≥ 2. Passes the 30 line.

## Round-1 defects

1. **Instruments under the floor — fixed.** instruments-columns.png (2x): list items 16 native → 10.9 px rendered (was 8.1); column heads 14.3 native caps → 9.7 (was 7); dates 13 → 9.0 (was 7.5); footnote 12.5–13 → 8.5–8.8 (was 7; still a hair under the 9 px floor). Phone edition is a real sheet: LEAD / LOG / LOOKOUT with the lists at ~16.8 px rendered and the sheet number, not a rule. The rotated-word column was not narrowed and the leader dots stay; both survive at the new size.
2. **Fine print demoted twice — half fixed.** Hero cartouche: all five lines now 14.3 native caps = 9.7 px rendered (x-cartouche 2x: L1, L3, L4 bands all 20 px), hierarchy carried by one cue (ink + the blank line). Fixed. Footer: unchanged — "Obstn rep. 2026 (PA)" 12 native / 8.2 grey italic, "9 notices · corrected through Notice 9" 12.5 / 8.5 grey, "14 · good holding" 13 / 8.9 (x-footer 2x). Not fixed. The phone footer gained "corrected through Notice 9" at ~16 px, which is the right move on that edition.
3. **Night recoloured not reweighted — fixed.** See J11: choke on the italic runs, Light cuts for sans and mono at night, dotted zero open, legend stems thinner (z-legend day/night pair).
4. **Italic I and fi — fixed.** x-title.png (2x of hero-day.svg): the word space after "I" now matches the one after "survey"; "Isurvey" is gone. x-profile.png and hero-phone.png 180–380 × 760–810: "Profile" sets with the fi ligature, no dot under the f's hook.
5. **Approaches legend and notes at 9 px — sizes fixed, title not.** approaches-legend.png (2x): legend entries and NOTES bodies both 16 native = 10.9 px rendered (was ~9); the legend is 33 entries in four columns (was 36 in three). The sheet title "Approaches to Scrapy Harbor" is still 27.5 native band ≈ 19–20 px rendered (x-apptitle 2x), one tier under the thesis and no stronger than the two box titles beneath it; the 36-native title was not taken.

Also from round 1: the four Fl 4s lights — fixed; the nine-item "five" list — fixed; the empty README table header row — not fixed.

## New defects

- **Night secondary ink is now demoted twice.** The cartouche's lines 3–5, "VAR 14h (2026) · AUTHOR'S LOCAL TIME" and the footer greys are set in the demoted night ink *and* the Light cut: measured coverage of cartouche line 3 at 870 is 0.119 by day and 0.029 by night (hero-night.png 90–290 × 405–418), the faintest text on the page. Day's fix (one cue) did not carry to night; give the demoted night ink one step more luminance (≈ #AFBACB) or keep Regular for runs already in secondary ink. Cost S.
- **Phone hero soundings collide at 360.** hero-phone.png 680–760 × 820–870: "358₁", "146₄" and "17₁" stack on the island outline east of Scrapy Harbor; at 360 the three figures read as one. One of the three should be dropped on the phone edition as the other eleven were. Cost S.
- Phone hero cartouche line 4 ("CHART NO. 21 · EDITION 0.1.3 · NOTICE 9 · IALA REGION B") runs margin to margin (x 50–1035 of 1080) with no gutter to the neat line; a tracking or one-word cut would give it air. Cost S.

## Summary

- J-total: 34/36 (was 29).
- Fixed: Instruments sizes and phone sheet; hero cartouche size tier; night reweighting (choke + Light cuts); italic I word space; fi ligature; legend and NOTES sizes; light characters; five-principles list.
- Still open: footer fine print at 8.2–8.9 px grey; Approaches title not raised; empty README table header row; thesis stated three times (J1).
- New: night demoted ink + Light cut is a double demotion (cartouche L3–5, rose caption, footer greys); phone hero 358₁/146₄/17₁ collision; phone cartouche line 4 has no side gutter.
