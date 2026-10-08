# Re-crit 10 — Mobile, round 2 (final build)

Reviewer 10. Judged from `<qa>/sheets/*-phone.png` (360 CSS px, DPR 3), `<qa>/readme/`, `<qa>/crops/`, `check.md`,
`perf-stdout.txt` and README.md as on disk. `<qa>` still has no night-phone renders and its README harness has no
`<meta viewport>` (its 360 render lays out at 980 px and picks the desk sources), so I re-made both in my scratchpad from
`assets/v9/`: six phone-night PNGs at 360 × DPR 3 (`r2night/`), and the harness at a real 360 px viewport in both schemes
(`r2readme/`): `img.currentSrc` is the `*-phone-{day,night}.svg` edition for all six pictures in both schemes.
Note `<qa>/det/*.svg` is stale (21:32; approaches-phone there is 720×1240), so SVG-level evidence below is from `assets/v9/` (22:01–22:03).

## 1. Scores J1–J12

| # | Score | Evidence |
|---|---|---|
| J1 | 3 | hero-phone.png y≈290–400: "I survey a web that / is wrong about itself." once, two lines under the name; footer coda is a coda. |
| J2 | 3 | hero-phone, name covered: hatched UNSURVEYED band with SMALL-SCALE now inside it, soundings thinning west, boat at anchor in Scrapy Harbor. |
| J3 | 3 | instruments-phone.png is now 720×200: three ruled rows LEAD / LOG / LOOKOUT with the fittings, sheet number bottom right. Six distinct silhouettes; nothing reads as an `<hr>`. |
| J4 | 2 | Unit, datum and now region on the phone (hero line 4 "…NOTICE 9 · IALA REGION B"; approaches head "IALA Region B · marks numbered from seaward"). No light character anywhere on a phone sheet while the phone legend row says "Light · its character". |
| J5 | 3 | approaches-phone.png y≈2340–2700 (1080-space): "SYMBOLS · upright figures measured · sloping not" and a 12-row two-column key (G can, R nun, Light, Ldg line, Anchorage, Wk / Rep, ED, SD, Danger line, Restricted, Limit of survey). Caption at README l.79 is now true on the phone. |
| J6 | 3 | 21 · 0.1.3 · 1,665 · 1,966 · HW 358 · 5 Oct · LW 0 · 24 Aug · Notice 9 agree across hero, soundings, log, footer and README ll.59/81/137. |
| J7 | 3 | Phone legend header states the upright/sloping convention; "charted as proposed; nothing runs it yet"; log "Log closed 1550 · unsigned"; footer "14 · good holding" sloping. Footer 7 · 5 · 3 still unitless (minor). |
| J8 | 3 | assets/v9/hero-phone-day.svg: 16 `<animate>` + 2 `<animateTransform>`, all `begin` ≤ 4 s, one 24 s leg, 18 `fill="freeze"`, no `indefinite`; frames/hero strip identical from t=28.1 s on. Five other phone sheets static. |
| J9 | 3 | README ll.193–208: colophon complete (Type, Editions "…through `<picture>`; a phone gets a sheet redrawn…", Motion, Variation, Figures, Build, License) and closed by `</details>` before the footer block at l.212; "five principles" now lists five, with 6–9 in a `<sub>`. |
| J10 | 3 | 360 px fold: hero 294 CSS px wide in the harness (328 on GitHub's 16 px gutters), four cartouche lines legible at the fold; caption, then rustmapper · Scrapy Harbor · PyPI · Email · How it's built, then the builds/languages table. |
| J11 | 3 | My night renders: lights are the magenta glows and the brightest marks; pale name on navy. Measured contrast of the dimmest semantic text: hero cartouche lines 3–4 and "VAR 14h (2026)" 5.5–5.6:1, thesis 5.4:1, LW / footer / log / sheet numbers 7.0–7.2:1, approaches legend 9.8:1. All AA; the 5.5:1 group is the sunlight floor. |
| J12 | 3 | 0 · 17 · 108 in the lagoon, SMALL-SCALE in the hatch, Wk '25, the log coda, VAR 14h now resolves in the Variation bullet (README l.201) which is readable again. Phone footer still has no serpent (static edition; fine). |

**J-total 35/36** (was 28). Above the 30 line; J4 is the only 2.

## 2. Round-1 defects

1. Footer written into the Colophon mid-sentence — **fixed.** README ll.199–221: Editions bullet complete, motion/variation/license bullets back, footer `<picture>` is the last top-level element after `</details>`; 360 px page tail (`r2readme/tail-light.png`) ends on the edge sheet, not on "▶ Colophon".
2. Phone approaches had no legend — **fixed.** Sheet grown 720×1240 → 720×1880; 12-row key inside the neat line (see J5).
3. Edge/label collisions — **fixed** on all three: (a) approaches head and "CHART NO. 21 · SHEET 3" now sit in margin bands outside the neat line (`r2crops/appr-top.png`, `appr-bottom.png`); (b) footer "corrected through Notice 9" moved inside the frame above the water line, sheet number in a band under the bottom rule (`footer-foot.png`); (c) SMALL-SCALE set inside the hatch right of UNSURVEYED, dashed shoals end short of it (`hero-entrance.png`).
4. Instruments phone sheet read as a broken image — **fixed** (see J3): LEAD / LOG / LOOKOUT table, 720×200.
5. Night-phone ink and missing region — **fixed.** IALA REGION B on hero line 4 and the approaches head; every semantic text node I measured ≥ 5.4:1 on navy (was ≈3:1 for the .55 group). The `.55` opacities left in hero-phone-night.svg are contour/texture strokes, not text.

Also from round 1: the recruiter table's blank header row still renders as an empty ~24 CSS px strip at 360 px (`fold-light.png` y≈1170) — **not fixed**, unranked. `perf-stdout.txt` reports only hero-day (PERF-MOVING warn); the §7.3 hero-phone repaint gate is **still unmeasured**; the SVG timeline says it passes.

## 3. New defects

- **N1 (S).** Phone legend row "Light · its character" while the phone editions cull every light character (build-report: "Phone lights lit, not flashing"); on the phone the legend defines a thing no mark shows. Either print "Fl G 4s" / "Fl R 4s" beside G "1" / R "2" on the phone, or reword the row "Light · lit".
- **N2 (S).** instruments-phone sheet and the `<sub>` 100 px below it list the same 18 fittings under two vocabularies and two groupings (LEAD/LOG/LOOKOUT; "Parquet · Arrow / redb · WAL" vs Languages/Stores and queues/Deck; "Parquet and Arrow · redb and WAL"). On the desk the `<sub>` is a text fallback; on the phone it is a second, different table. Hide it on phone or make the glosses match.
- **Harness, not build.** `<qa>/readme/readme-*.html` still has no `<meta viewport>`, so the QA README render can never show the phone sources; add the meta and a 360 px capture to the harness.

## 4. Five-second read at 360 px

Day: a cream chart fills the first screen; "Ben Russell", the two-line thesis, a compass that is a clock, an archipelago of
numbered islands, a hatched UNSURVEYED / SMALL-SCALE edge, and four cartouche lines ending "CHART NO. 21 · EDITION 0.1.3 ·
NOTICE 9 · IALA REGION B", all legible without zooming. Reader has name, thesis, field, stack and the survey edge by second
four; the link row and the builds table arrive on the first thumb-scroll. Night: paper goes navy, the name pale, the two
harbor lights and the sail are the only saturated things; the cartouche's last two lines are the faintest text on the
screen but hold at 5.6:1. Nothing on the page reads as a shrunk desktop or a broken image any more.

## Summary
- J-total: 35/36 (was 28)
- Fixed: all five round-1 defects (footer/colophon, phone legend, three margin collisions, instruments sheet, night ink + region)
- Still open: recruiter table empty header strip; hero-phone perf gate unmeasured; footer 7·5·3 unitless (minor)
- New: N1 phone legend "Light · its character" with no character on the sheet (S); N2 instruments sheet vs `<sub>` double vocabulary (S); QA harness lacks viewport meta
